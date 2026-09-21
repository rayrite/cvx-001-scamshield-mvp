"""Thin async client for the z.ai chat-completions endpoint.

Two call shapes, both docs-verified (2026-09-20):

- **Vision intake** — glm-5.3-flash, multimodal content array, NO tools
  (vision requests cannot carry the built-in web_search tool).
- **Research stages** — glm-5.3, text messages, built-in `web_search` tool
  with the string-boolean quirk ("True") and the literal {{search_result}}
  placeholder inside search_prompt.

Plain httpx, no SDK: three pip packages and the app runs anywhere.
"""
from __future__ import annotations

import json
import os
import re
import threading
import time
from pathlib import Path

import httpx

ZAI_URL = os.getenv("ZAI_API_URL", "https://api.z.ai/api/paas/v4/chat/completions")
INTAKE_MODEL = os.getenv("ZAI_INTAKE_MODEL", "glm-5.3-flash")    # vision
RESEARCH_MODEL = os.getenv("ZAI_RESEARCH_MODEL", "glm-5.3")      # staged reasoning
INTAKE_TIMEOUT = float(os.getenv("ZAI_INTAKE_TIMEOUT", "120"))
RESEARCH_TIMEOUT = float(os.getenv("ZAI_RESEARCH_TIMEOUT", "300"))

MAX_STAGE_CALLS = int(os.getenv("MAX_STAGE_CALLS", "10"))

# GLM-5.x thinking cannot be disabled; reasoning_effort (low/high/max, API
# default max) is the only depth/cost lever. The skill's rubrics carry the
# heavy reasoning scaffolding, so "low" is the sane hosted default. Only
# GLM-5.2+ accepts the parameter — enforced per-model via MODELS below.
REASONING_EFFORT = os.getenv("ZAI_REASONING_EFFORT", "low")

# --- the GLM-5 family (docs-verified 2026-09-20) --------------------------------
# Prices are USD per million tokens in/out. effort_ok marks GLM-5.2+ (the
# only models that accept reasoning_effort). roles: "research" models carry
# the web_search tool (text flagships); "intake" models accept image input
# (the vision-class flash tiers — the 5-series has no separate V line).
MODELS: dict[str, dict] = {
    "glm-5.3": {
        "label": "GLM-5.3", "vision": False, "effort_ok": True,
        "price_in": 1.40, "price_out": 4.40, "ctx": "1M ctx · 128K out",
        "blurb": "Flagship reasoning — the default for staged research.",
        "roles": ("research",),
    },
    "glm-5.3-flash": {
        "label": "GLM-5.3 Flash", "vision": True, "effort_ok": True,
        "price_in": 0.15, "price_out": 0.50, "ctx": "1M ctx · 128K out",
        "blurb": "Vision intake workhorse — reads screenshots at a tenth of flagship cost.",
        "roles": ("intake",),
    },
    "glm-5.3-flashx": {
        "label": "GLM-5.3 FlashX", "vision": True, "effort_ok": True,
        "price_in": 0.37, "price_out": 1.25, "ctx": "1M ctx · 128K out · 200 tok/s",
        "blurb": "The speed tier — same multimodal intake at 200 tokens/sec.",
        "roles": ("intake",),
    },
    "glm-5.2": {
        "label": "GLM-5.2", "vision": False, "effort_ok": True,
        "price_in": 1.40, "price_out": 4.40, "ctx": "1M ctx",
        "blurb": "Previous flagship — same price, earlier reasoning generation.",
        "roles": ("research",),
    },
    "glm-5.1": {
        "label": "GLM-5.1", "vision": False, "effort_ok": False,
        "price_in": 1.40, "price_out": 4.40, "ctx": "1M ctx",
        "blurb": "Earlier generation; no reasoning_effort knob.",
        "roles": ("research",),
    },
    "glm-5": {
        "label": "GLM-5", "vision": False, "effort_ok": False,
        "price_in": 1.00, "price_out": 3.20, "ctx": "—",
        "blurb": "The original 5-series flagship at the lowest flagship price.",
        "roles": ("research",),
    },
}

# --- runtime model selection (models.json, udl.json-style) -----------------------
MODELS_FILE = Path(__file__).parent / "models.json"
_sel_lock = threading.Lock()


def apply_selection() -> None:
    """Overlay a persisted models.json selection onto the env defaults.
    Silent no-op when the file is missing or corrupt (house style —
    features.py/udl.py behave the same)."""
    global INTAKE_MODEL, RESEARCH_MODEL
    try:
        sel = json.loads(MODELS_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return
    for slot in ("intake", "research"):
        mid = sel.get(slot)
        if isinstance(mid, str) and mid in MODELS and slot in MODELS[mid]["roles"]:
            if slot == "intake":
                INTAKE_MODEL = mid
            else:
                RESEARCH_MODEL = mid


def save_selection(intake: str | None = None, research: str | None = None) -> dict:
    """Validate and persist a selection, then update the module globals so
    every call-time reader (pipeline calls, /api/health, stage-log labels)
    reflects the swap immediately. Wrong-role or unknown ids raise
    ValueError before anything is written."""
    global INTAKE_MODEL, RESEARCH_MODEL
    for slot, mid in (("intake", intake), ("research", research)):
        if mid is not None:
            if mid not in MODELS:
                raise ValueError(f"unknown model id {mid!r}")
            if slot not in MODELS[mid]["roles"]:
                why = "image input" if slot == "intake" else "the web_search tool"
                raise ValueError(f"{mid!r} cannot serve the {slot} role (no {why})")
    current = {"intake": INTAKE_MODEL, "research": RESEARCH_MODEL}
    if intake:
        current["intake"] = intake
    if research:
        current["research"] = research
    with _sel_lock:
        MODELS_FILE.write_text(json.dumps(current, indent=2) + "\n",
                               encoding="utf-8")
        INTAKE_MODEL, RESEARCH_MODEL = current["intake"], current["research"]
    return current


apply_selection()


def _thinking(model: str) -> dict:
    info = MODELS.get(model)
    if info and info["effort_ok"] and REASONING_EFFORT in ("low", "high", "max"):
        return {"reasoning_effort": REASONING_EFFORT}
    return {}

# The transcriptionist — verbatim, defanged, zero interpretation.
INTAKE_PROMPT = (
    "You are a transcription specialist for consumer-protection analysis. "
    "Transcribe the attached screenshot(s) of an email, text message, web page, "
    "or product listing VERBATIM. Rules:\n"
    "- Structured markdown output. For email/text: From (display name + full "
    "sender address), Reply-To if visible, Subject, Date, Body verbatim.\n"
    "- Reproduce every URL as defanged text (e.g. usps-delivery-fee[.]net), "
    "never as a link.\n"
    "- Mark illegible or cropped regions [illegible]; note blocked-image "
    "placeholders as [blocked image].\n"
    "- Do NOT interpret, judge, or advise. Transcription only — analysis "
    "happens downstream."
)


class ZaiError(RuntimeError):
    def __init__(self, status: int, body: str,
                 code: int | None = None, api_message: str | None = None):
        super().__init__(f"z.ai HTTP {status}: {body[:400]}")
        self.status = status
        self.body = body              # full raw response text (debugging)
        self.code = code              # numeric z.ai code (1113, 1302, ...) if parseable
        self.api_message = api_message


def _parse_error(body: str) -> tuple[int | None, str | None]:
    """Pull (code, message) out of z.ai's {"error":{...}} envelope."""
    try:
        err = (json.loads(body) or {}).get("error") or {}
        code = err.get("code")
        return (int(code) if code is not None else None), err.get("message")
    except (json.JSONDecodeError, AttributeError, TypeError, ValueError):
        return None, None


def _reset_from(message: str) -> str:
    """z.ai window-limit messages end with 'will reset at {time}'."""
    m = re.search(r"reset at [`'\"]?([^`'\"]+?)[`'\"]?\s*$", message.strip())
    return m.group(1).rstrip(".}") if m else ""


def friendly(exc: "ZaiError") -> str:
    """The ONE user-facing sentence per failure class. Every surface (chat
    bubbles, job errors, the beacon panel) speaks this — raw JSON goes to
    logs and job.error_detail only. Codes per docs.z.ai api-code reference."""
    code, status = exc.code, exc.status
    if code == 1113:
        return ("The AI account is out of credit — live results resume once "
                "it's recharged")
    if code in (1302, 1305):
        return "The AI service is at capacity right now — please retry in a minute"
    if code == 1313:
        return ("The AI service has briefly limited this account's request "
                "frequency — please slow down and retry shortly")
    if code in (1308, 1310, 1316, 1317, 1318, 1319, 1320, 1321):
        reset = _reset_from(exc.api_message or "")
        base = "The AI service's usage window is exhausted"
        return f"{base} — it resets at {reset}" if reset else f"{base}; please try again later"
    if status in (401, 403):
        return "The AI API key is invalid or revoked — the operator needs to check it"
    if status == 429:
        return "The AI service is rate limiting us — please wait a moment and retry"
    return f"The AI service returned an error (HTTP {status}) — please try again"


def friendly_transport(exc: Exception) -> str:
    """httpx-level failures (timeouts, refused connections) — currently the
    only other exception class that can escape a z.ai call."""
    return "The AI service took too long to respond — please try again"


# --- live concurrency (measured at the single HTTP choke point) ------------------
# z.ai publishes per-key concurrency limits only on the logged-in console,
# not in the docs — so the app measures its own in-flight requests. The
# event loop is single-threaded; plain int mutations between awaits are safe.
INFLIGHT = 0
MAX_SEEN = 0
LAST_LIMIT_HIT: dict | None = None   # {"code": int|None, "ts": float}


def web_search_tool(today: str, count: int = 10) -> list[dict]:
    return [{
        "type": "web_search",
        "web_search": {
            "enable": "True",
            "search_engine": "search-prime",
            "search_result": "True",
            "search_prompt": (
                f"Today is {today}. You are researching for a consumer-protection "
                "background check. Prioritize authoritative sources: regulators "
                "(.gov, FTC, CFPB, FDA, USDA-FSIS, CPSC, NHTSA, CDC), court and "
                "settlement records, official company pages, BBB, and named-outlet "
                "press. Prefer dated, specific results over aggregators; ignore SEO "
                "content farms. Use {{search_result}} to answer with the key facts "
                "ranked by importance, citing the source and its date."
            ),
            "count": str(count),
            "search_recency_filter": "noLimit",
            "content_size": "high",
        },
    }]


async def _post(client: httpx.AsyncClient, payload: dict, timeout: float) -> dict:
    global INFLIGHT, MAX_SEEN, LAST_LIMIT_HIT
    INFLIGHT += 1
    MAX_SEEN = max(MAX_SEEN, INFLIGHT)
    try:
        resp = await client.post(
            ZAI_URL,
            json=payload,
            headers={"Authorization": f"Bearer {os.environ['ZAI_API_KEY']}"},
            timeout=timeout,
        )
    finally:
        INFLIGHT -= 1
    if resp.status_code >= 400:
        code, message = _parse_error(resp.text)
        if resp.status_code == 429:
            LAST_LIMIT_HIT = {"code": code, "ts": time.time()}
        raise ZaiError(resp.status_code, resp.text, code, message)
    return resp.json()


def _finish(raw: dict) -> tuple[str, list[dict], dict]:
    msg = (raw.get("choices") or [{}])[0].get("message", {})
    content = msg.get("content") or ""
    sources = [
        {k: s.get(k, "") for k in ("refer", "title", "link", "media", "publish_date")}
        for s in (raw.get("web_search") or [])
    ]
    return content, sources, raw.get("usage") or {}


async def vision_intake(client: httpx.AsyncClient, user_text: str,
                        images: list[str], today: str) -> tuple[str, dict]:
    """Returns (transcript, usage)."""
    content: list[dict] = [{"type": "text", "text": f"Today: {today}. {user_text}"}]
    content += [{"type": "image_url", "image_url": {"url": u}} for u in images]
    raw = await _post(client, {
        "model": INTAKE_MODEL,
        "messages": [
            {"role": "system", "content": INTAKE_PROMPT},
            {"role": "user", "content": content},
        ],
        **_thinking(INTAKE_MODEL),
    }, INTAKE_TIMEOUT)
    transcript, _, usage = _finish(raw)
    return transcript, usage


async def research_call(client: httpx.AsyncClient, system: str, user: str,
                        today: str, count: int = 10) -> tuple[str, list[dict], dict]:
    """A staged reasoning call with the built-in web_search tool.
    Returns (markdown_content, slim_sources, usage)."""
    raw = await _post(client, {
        "model": RESEARCH_MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "tools": web_search_tool(today, count=count),
        **_thinking(RESEARCH_MODEL),
    }, RESEARCH_TIMEOUT)
    return _finish(raw)


async def plain_call(client: httpx.AsyncClient, system: str, user: str,
                     model: str | None = None, timeout: float | None = None) -> tuple[str, dict]:
    """A zero-tool reasoning call (smoke test, consolidation)."""
    used_model = model or RESEARCH_MODEL
    raw = await _post(client, {
        "model": used_model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        **_thinking(used_model),
    }, timeout or RESEARCH_TIMEOUT)
    content, _, usage = _finish(raw)
    return content, usage
