"""FastAPI surface for the ScamShield demo app.

API (all JSON unless noted):

- GET  /api/health              liveness + key/demo mode (never the key)
- GET  /api/diagnostics         connectivity smoke test (key · net · ping)
- GET  /api/features            feature flags (set vs. effective) + inventory
- GET  /api/modes               chat/quick mode registry with availability
- POST /api/chat                one chat turn {mode, text, images?, conversation_id?}
- GET  /api/conversations       recent conversations
- GET  /api/conversations/{id}  full conversation (messages + sources)
- DELETE /api/conversations/{id}
- GET  /api/wikis               Learning Center menu (scans content/wikis)
- GET  /api/spas                SPA menu (scans content/spas — add/remove HTML
                                files and the menu reflects it on next load)
- GET/POST /api/udl             Universal Design Language config
- GET  /udl.css · /udl.js       generated UDL assets every page links
- POST /api/waitlist            {email} → appended to DATA_DIR/waitlist.txt
- GET  /api/waitlist            count only (never the addresses)

Staged Check v2 agent (jobs):

- GET  /api/jobs                recent jobs
- POST /api/jobs                create a job → 202 + id
- GET  /api/jobs/{id}           full job state — poll this
- POST /api/jobs/{id}/gate      {decision: go|stop|document|custom, text?}
- GET  /api/jobs/{id}/report    cumulative markdown report

Pretty pages: / (landing) · /check · /chat · /quick · /learn · /apps · /theme · /video.
Mounts: /learn/wiki → content/wikis, /apps/spa → content/spas, then the static
mount at / LAST so /api and the pretty routes win. If AGENT_TOKEN is set,
mutating agent endpoints require the X-Auth-Token header.
"""
from __future__ import annotations

import asyncio
import contextlib
import datetime as dt
import os
import re
import time
from pathlib import Path

from dotenv import load_dotenv

# Must run BEFORE the zai/orchestrator imports below — they read ZAI_API_KEY
# (and friends) from the environment at import time.
load_dotenv(Path(__file__).parent / ".env")

import httpx
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

import agents
import chatstore
import features
import jobs
import orchestrator
import udl
import zai

STATIC = Path(__file__).parent / "static"


@contextlib.asynccontextmanager
async def lifespan(_app: FastAPI):
    # Redeploys/restarts kill in-flight asyncio tasks; the RUNNING registry is
    # in-process only. Jobs saved mid-flight as queued/running can never
    # progress again — mark them so the UI says so instead of hanging.
    for j in jobs.list_jobs():
        if j.get("status") in ("queued", "running"):
            job = jobs.load(j["id"])
            if job and job.get("status") in ("queued", "running"):
                job["status"] = "error"
                job["error"] = ("interrupted by a service restart (redeploy?) — "
                                "the saved stages are kept; re-submit to continue")
                jobs.save(job)
    yield


app = FastAPI(title="ScamShield demo app", version="2.0", lifespan=lifespan)

AGENT_TOKEN = os.getenv("AGENT_TOKEN", "")
MAX_IMAGES = int(os.getenv("MAX_IMAGES", "5"))


def _auth(x_auth_token: str | None) -> None:
    if AGENT_TOKEN and x_auth_token != AGENT_TOKEN:
        raise HTTPException(status_code=401, detail="bad or missing X-Auth-Token")


def _today() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")


_TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)


def _menu(dir_name: str, url_prefix: str) -> list[dict]:
    """Scan a content folder at request time — the menus are only as stale as
    the last page load. Add/remove an HTML file, refresh, and it's reflected."""
    d = agents.CONTENT / dir_name
    out = []
    if not d.is_dir():
        return out
    for p in sorted(d.glob("*.html")):
        try:
            m = _TITLE_RE.search(p.read_text(encoding="utf-8", errors="replace")[:20000])
            title = (m.group(1).strip() if m else "") or p.stem.replace("-", " ").title()
        except OSError:
            title = p.stem
        out.append({"file": p.name, "title": title,
                    "size_kb": round(p.stat().st_size / 1024),
                    "url": f"{url_prefix}/{p.name}"})
    return out


# ---------------------------------------------------------------- health/meta

@app.get("/api/health")
async def health():
    return {
        "ok": True,
        "key_configured": "ZAI_API_KEY" in os.environ,
        "demo_mode": orchestrator.DEMO,
        "research_model": zai.RESEARCH_MODEL,
        "intake_model": zai.INTAKE_MODEL,
        "data_dir": str(jobs.DATA_DIR),
    }


@app.get("/api/diagnostics")
async def diagnostics():
    """Connectivity smoke test behind the header beacon: (a) key presence,
    (b) outbound reachability of the z.ai host, (c) one tiny ping completion.
    Public like /api/health — statuses, latencies, and error strings only;
    the key itself is never returned."""
    checks: list[dict] = []

    # (a) API key configured — presence only, same expression as /api/health
    key_ok = "ZAI_API_KEY" in os.environ
    checks.append({"id": "key", "status": "pass" if key_ok else "fail", "ms": 0,
                   "detail": "ZAI_API_KEY is set in the environment" if key_ok
                             else "no key found in environment — demo mode"})

    # (b) internet — HEAD the exact origin the app calls; ANY HTTP answer
    # (even 404/405) proves outbound connectivity, a transport error does
    # not. Catches hosts that silently block egress (unverified trials).
    zurl = httpx.URL(zai.ZAI_URL)
    hostport = zurl.host if not zurl.port else f"{zurl.host}:{zurl.port}"
    origin = f"{zurl.scheme}://{hostport}/"
    t0 = time.perf_counter()
    try:
        async with httpx.AsyncClient() as client:
            await client.head(origin, timeout=8)
        net_ok = True
        checks.append({"id": "net", "status": "pass", "ms": round((time.perf_counter() - t0) * 1000),
                       "detail": f"reachable — {origin}"})
    except httpx.HTTPError as e:
        net_ok = False
        checks.append({"id": "net", "status": "fail", "ms": round((time.perf_counter() - t0) * 1000),
                       "detail": f"unreachable — {type(e).__name__} — outbound traffic "
                                 f"to {origin} is blocked or timed out"})

    # (c) ping — one tiny glm-5.3-flash completion; skipped when an earlier
    # check already failed (nothing further would be learned)
    if not (key_ok and net_ok):
        checks.append({"id": "ping", "status": "skip", "ms": None, "model": zai.INTAKE_MODEL,
                       "detail": "skipped — earlier check failed"})
    else:
        t0 = time.perf_counter()
        try:
            async with httpx.AsyncClient() as client:
                reply, usage = await zai.plain_call(
                    client, system="You are a connectivity smoke test. "
                                   "Reply with exactly: pong",
                    user="ping", model=zai.INTAKE_MODEL, timeout=30)
            checks.append({"id": "ping", "status": "pass", "model": zai.INTAKE_MODEL,
                           "ms": round((time.perf_counter() - t0) * 1000),
                           "detail": f"replied {reply.strip()[:20]!r} · "
                                     f"{usage.get('completion_tokens', 0)} tokens"})
        except zai.ZaiError as e:
            msg = str(e)
            if e.status == 429 and ("balance" in msg.lower() or "1113" in msg):
                why = "z.ai account out of credit (HTTP 429 · insufficient " \
                      "balance) — recharge needed before live demos"
            elif e.status == 429:
                why = "rate limited (HTTP 429) — too many requests, wait a moment and re-run"
            elif e.status in (401, 403):
                why = f"key invalid or revoked (HTTP {e.status})"
            else:
                why = f"z.ai HTTP {e.status}"
            checks.append({"id": "ping", "status": "fail", "model": zai.INTAKE_MODEL,
                           "ms": round((time.perf_counter() - t0) * 1000),
                           "detail": why})
        except httpx.HTTPError as e:
            checks.append({"id": "ping", "status": "fail", "model": zai.INTAKE_MODEL,
                           "ms": round((time.perf_counter() - t0) * 1000),
                           "detail": f"network — {type(e).__name__}"})

    return {"ok": all(c["status"] == "pass" for c in checks),
            "demo_mode": orchestrator.DEMO, "checks": checks}


@app.get("/api/features")
async def get_features():
    return {"flags": features.load_flags(), "effective": features.effective(),
            "inventory": features.inventory()}


@app.get("/api/modes")
async def get_modes():
    return {"modes": agents.modes_available(),
            "max_turns": chatstore.MAX_TURNS}


# ---------------------------------------------------------------------- chat

class ChatIn(BaseModel):
    mode: str
    text: str = Field(default="", max_length=12000)
    images: list[str] = Field(default_factory=list, max_length=MAX_IMAGES)
    conversation_id: str | None = None


@app.post("/api/chat")
async def chat(chat_in: ChatIn, x_auth_token: str | None = Header(default=None)):
    _auth(x_auth_token)
    registry = agents.registry()
    eff = features.effective()
    kind = registry[chat_in.mode]["kind"] if chat_in.mode in registry else None
    if not kind:
        raise HTTPException(400, f"unknown mode {chat_in.mode!r} — see /api/modes")
    if not eff["chat" if kind == "skill" else "quick"]:
        raise HTTPException(503, f"the {kind} surface is disabled or its content is missing")
    text = chat_in.text.strip()
    if not text and not chat_in.images:
        raise HTTPException(400, "text or images required")

    # conversation: resume or create; the stored mode wins (a conversation is
    # bound to one skill)
    if chat_in.conversation_id:
        conv = chatstore.load(chatstore.safe_id(chat_in.conversation_id))
        if not conv:
            raise HTTPException(404, "no such conversation")
    else:
        conv = chatstore.new_conversation(chat_in.mode)
    mode = conv["mode"]

    turns_done = len([m for m in conv["messages"] if m.get("role") == "user"])
    if turns_done >= chatstore.MAX_TURNS:
        raise HTTPException(409, f"conversation reached the {chatstore.MAX_TURNS}-turn demo cap — start a new one")

    turn = turns_done + 1
    today = _today()

    for img in chat_in.images:
        if not (img.startswith("http://") or img.startswith("https://")
                or img.startswith("data:image/")):
            raise HTTPException(400, "images must be http(s) URLs or data:image URIs")
        if img.startswith("data:") and len(img) > 5 * 1024 * 1024 * 1.4:
            raise HTTPException(400, "image exceeds the ~5 MB z.ai limit (after base64)")

    user_content = f"Today: {today}. {text}" if text else f"Today: {today}."
    sources: list[dict] = []
    demo = orchestrator.DEMO

    if demo:
        reply = agents.demo_reply(mode, turn)
    else:
        async with httpx.AsyncClient() as client:
            try:
                if chat_in.images:
                    transcript, usage = await zai.vision_intake(
                        client, text or "(no caption — screenshots only)",
                        chat_in.images, today)
                    user_content += f"\n\n--- verbatim screenshot transcript ---\n{transcript}"
                    conv["budget"]["model_calls"] += 1
                    conv["budget"]["tokens_in"] = conv["budget"].get("tokens_in", 0) \
                        + (usage.get("prompt_tokens", 0) or 0)
                    conv["budget"]["tokens_out"] = conv["budget"].get("tokens_out", 0) \
                        + (usage.get("completion_tokens", 0) or 0)
                history = [{"role": m["role"], "content": m["content"]}
                           for m in conv["messages"]]
                reply, sources, usage = await zai.research_call(
                    client, agents.system_prompt(mode),
                    _compose(history, user_content), today)
                conv["budget"]["model_calls"] += 1
                conv["budget"]["search_results"] += len(sources)
                conv["budget"]["tokens_in"] = conv["budget"].get("tokens_in", 0) \
                    + (usage.get("prompt_tokens", 0) or 0)
                conv["budget"]["tokens_out"] = conv["budget"].get("tokens_out", 0) \
                    + (usage.get("completion_tokens", 0) or 0)
            except zai.ZaiError as e:
                raise HTTPException(502, str(e))

    chatstore.add_message(conv, "user", text or "(screenshots only)")
    chatstore.add_message(conv, "assistant", reply, sources)

    return {
        "conversation_id": conv["id"], "mode": mode, "turn": turn,
        "reply": reply, "sources": sources, "demo": demo,
        "turns_left": chatstore.MAX_TURNS - turn,
    }


def _compose(history: list[dict], user_content: str) -> str:
    """The z.ai endpoint takes plain-message turns, but our per-mode prompts
    are single system prompts; the conversation rides in one user payload so
    the transcript stays the single source of truth."""
    if not history:
        return user_content
    lines = [f"Today: {dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d')}.",
             "Conversation so far (you are the assistant):"]
    for m in history:
        who = "USER" if m["role"] == "user" else "ASSISTANT"
        lines.append(f"[{who}]\n{m['content']}")
    lines.append(f"[USER]\n{user_content.removeprefix(_today_prefix())}".strip())
    return "\n\n".join(lines)


def _today_prefix() -> str:
    return f"Today: {_today()}. "


@app.get("/api/conversations")
async def conversations():
    return {"conversations": chatstore.list_conversations()}


@app.get("/api/conversations/{cid}")
async def conversation(cid: str):
    conv = chatstore.load(chatstore.safe_id(cid))
    if not conv:
        raise HTTPException(404, "no such conversation")
    return conv


@app.delete("/api/conversations/{cid}")
async def delete_conversation(cid: str):
    if not chatstore.delete(chatstore.safe_id(cid)):
        raise HTTPException(404, "no such conversation")
    return {"deleted": True}


# ------------------------------------------------------------- learning / apps

@app.get("/api/wikis")
async def wikis():
    if not features.effective()["learning"]:
        return {"wikis": [], "disabled": True}
    return {"wikis": _menu("wikis", "/learn/wiki")}


@app.get("/api/spas")
async def spas():
    if not features.effective()["apps"]:
        return {"spas": [], "disabled": True}
    return {"spas": _menu("spas", "/apps/spa")}


# ----------------------------------------------------------------------- UDL

@app.get("/api/udl")
async def udl_get():
    return udl.load()


@app.post("/api/udl")
async def udl_post(cfg: dict, x_auth_token: str | None = Header(default=None)):
    _auth(x_auth_token)
    if not features.load_flags()["theme"]:
        raise HTTPException(503, "theme editing is disabled")
    return udl.save(cfg)


@app.get("/udl.css")
async def udl_css():
    return Response(udl.css(), media_type="text/css")


@app.get("/udl.js")
async def udl_js():
    return Response(udl.js(), media_type="application/javascript")


# ------------------------------------------------------------------ waitlist

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]{2,}$")
WAITLIST = jobs.DATA_DIR / "waitlist.txt"


@app.post("/api/waitlist")
async def waitlist_join(body: dict):
    if not features.effective()["waitlist"]:
        raise HTTPException(503, "waitlist is disabled")
    email = str(body.get("email", "")).strip().lower()
    if not _EMAIL_RE.match(email) or len(email) > 254:
        raise HTTPException(400, "that does not look like an email address")
    existing = []
    if WAITLIST.exists():
        existing = [ln.split("\t", 1)[-1].strip()
                    for ln in WAITLIST.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if email in existing:
        return {"ok": True, "already": True, "count": len(existing)}
    WAITLIST.parent.mkdir(parents=True, exist_ok=True)
    with WAITLIST.open("a", encoding="utf-8") as f:
        f.write(f"{dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')}\t{email}\n")
    return {"ok": True, "already": False, "count": len(existing) + 1}


@app.get("/api/waitlist")
async def waitlist_count():
    if not WAITLIST.exists():
        return {"count": 0}
    n = len([ln for ln in WAITLIST.read_text(encoding="utf-8").splitlines() if ln.strip()])
    return {"count": n}


# ------------------------------------------------- staged Check v2 (jobs API)

class JobIn(BaseModel):
    text: str = Field(min_length=1, max_length=8000)
    images: list[str] = Field(default_factory=list, max_length=MAX_IMAGES)
    worry: str = "legitimacy"
    region: str = "US"


class GateIn(BaseModel):
    decision: str
    text: str | None = None


@app.get("/api/jobs")
async def list_jobs():
    return {"jobs": jobs.list_jobs()}


@app.post("/api/jobs", status_code=202)
async def create_job(job_in: JobIn, request: Request,
                     x_auth_token: str | None = Header(default=None)):
    _auth(x_auth_token)
    if not features.effective()["check"]:
        raise HTTPException(503, "the staged check surface is disabled")
    text = job_in.text.strip()
    if not text and not job_in.images:
        raise HTTPException(400, "text or images required")
    for img in job_in.images:
        if not (img.startswith("http://") or img.startswith("https://")
                or img.startswith("data:image/")):
            raise HTTPException(400, "images must be http(s) URLs or data:image URIs")
        if img.startswith("data:") and len(img) > 5 * 1024 * 1024 * 1.4:
            raise HTTPException(400, "image exceeds the ~5 MB z.ai limit (after base64)")
    if job_in.worry not in ("legitimacy", "counterfeit", "non-delivery", "payment-safety"):
        raise HTTPException(400, "worry must be legitimacy|counterfeit|non-delivery|payment-safety")

    job = jobs.new_job(text, job_in.images, job_in.worry, job_in.region, orchestrator.DEMO)
    jobs.save(job)
    jobs.RUNNING[job["id"]] = asyncio.create_task(orchestrator.run_initial(job["id"]))
    return JSONResponse(
        {"id": job["id"], "status": job["status"], "poll": f"/api/jobs/{job['id']}"},
        status_code=202,
        headers={"Location": f"/api/jobs/{job['id']}"},
    )


@app.get("/api/jobs/{jid}")
async def get_job(jid: str, x_auth_token: str | None = Header(default=None)):
    _auth(x_auth_token)
    job = jobs.load(jobs.safe_id(jid))
    if not job:
        raise HTTPException(404, "no such job")
    return jobs.public_view(job)


@app.post("/api/jobs/{jid}/gate")
async def gate(jid: str, gate_in: GateIn, x_auth_token: str | None = Header(default=None)):
    _auth(x_auth_token)
    err = await orchestrator.run_gate(jobs.safe_id(jid), gate_in.decision, gate_in.text)
    if err:
        raise HTTPException(err.get("status", 400), err["error"])
    job = jobs.load(jobs.safe_id(jid))
    return jobs.public_view(job)


@app.get("/api/jobs/{jid}/report", response_class=PlainTextResponse)
async def report(jid: str, x_auth_token: str | None = Header(default=None)):
    _auth(x_auth_token)
    p = jobs.REPORTS_DIR / f"{jobs.safe_id(jid)}.md"
    if not p.exists():
        raise HTTPException(404, "no report yet")
    return PlainTextResponse(p.read_text(encoding="utf-8"), media_type="text/markdown")


# ------------------------------------------------------------- pretty pages

_PAGES = {"check": "check.html", "chat": "chat.html", "quick": "quick.html",
          "learn": "learn.html", "apps": "apps.html", "theme": "theme.html",
          "video": "video.html"}
_PAGE_FLAGS = {"check": "check", "chat": "chat", "quick": "quick",
               "learn": "learning", "apps": "apps", "theme": None,
               "video": "video"}


def _page(name: str):
    eff = features.effective()
    flag = _PAGE_FLAGS[name]
    if flag and not eff[flag]:
        raise HTTPException(503, f"the /{name} surface is disabled")
    return FileResponse(STATIC / _PAGES[name], media_type="text/html")


for _name in _PAGES:
    app.get(f"/{_name}", name=f"page-{_name}")(lambda _n=_name: _page(_n))


# ------------------------------------------------- mounts (order matters!)

app.mount("/learn/wiki", StaticFiles(directory=agents.CONTENT / "wikis"), name="wikis")
app.mount("/apps/spa", StaticFiles(directory=agents.CONTENT / "spas"), name="spas")
# sample videos — Range-streamed (206 Partial Content) from the data volume.
# StaticFiles checks the folder exists at import time, so create it or a
# fresh clone / empty volume would crash the boot instead of 404ing.
VIDEOS_DIR = jobs.DATA_DIR / "videos"
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/videos", StaticFiles(directory=VIDEOS_DIR), name="videos")
# static UI LAST — /api/* and the pretty routes above win
app.mount("/", StaticFiles(directory=STATIC, html=True), name="static")
