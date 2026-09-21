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

import os

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
# GLM-5.2+ accepts the parameter, so guard on the model id.
REASONING_EFFORT = os.getenv("ZAI_REASONING_EFFORT", "low")


def _thinking(model: str) -> dict:
    if model.startswith("glm-5") and REASONING_EFFORT in ("low", "high", "max"):
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
    def __init__(self, status: int, body: str):
        super().__init__(f"z.ai HTTP {status}: {body[:400]}")
        self.status = status


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
    resp = await client.post(
        ZAI_URL,
        json=payload,
        headers={"Authorization": f"Bearer {os.environ['ZAI_API_KEY']}"},
        timeout=timeout,
    )
    if resp.status_code >= 400:
        raise ZaiError(resp.status_code, resp.text)
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
