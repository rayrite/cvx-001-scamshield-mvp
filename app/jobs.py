"""Job store for the hosted ScamShield Check v2 agent.

Each research job is one JSON file under DATA_DIR/jobs/<id>.json, plus a
cumulative markdown report at DATA_DIR/reports/<id>.md maintained at every
stage boundary (the skill's "one cumulative report file" rule). Point DATA_DIR
at a Railway Volume mount and jobs + reports survive deploys and restarts.

Single-process by design: one uvicorn worker, in-process asyncio tasks, files
on disk. Do not scale to multiple workers/replicas without externalizing the
running-task registry first (see PRIMER §Operational limits).
"""
from __future__ import annotations

import asyncio
import datetime as dt
import json
import os
import re
import secrets
from pathlib import Path
from typing import Any

DATA_DIR = Path(os.getenv("DATA_DIR", Path(__file__).parent / "data"))
JOBS_DIR = DATA_DIR / "jobs"
REPORTS_DIR = DATA_DIR / "reports"

JOBS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# In-memory registry of running stage tasks: job_id -> asyncio.Task
RUNNING: dict[str, asyncio.Task] = {}


def new_job(text: str, images: list[str], worry: str, region: str, demo: bool) -> dict:
    jid = "j_" + secrets.token_hex(6)
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    return {
        "id": jid,
        "created": now,
        "updated": now,
        "status": "queued",           # queued|running|awaiting_gate|done|error|stopped
        "stage": "intake",            # intake|smoke|triage|verify|document|consolidate
        "stage_number": 0,            # research stages completed (triage=1, verify=N)
        "input": {
            "text": text,
            "image_count": len(images),
            "images": images,          # kept in the job file so gates can resume
            "worry": worry,
            "region": region,
        },
        "transcript": None,
        "stage_log": [],               # one entry per completed model call
        "verdict_history": [],
        "gate": None,
        "report": None,
        "error": None,
        "demo": demo,
        "budget": {"model_calls": 0, "search_results": 0, "tokens_in": 0, "tokens_out": 0},
    }


def _path(jid: str) -> Path:
    return JOBS_DIR / f"{safe_id(jid)}.json"


def safe_id(jid: str) -> str:
    if not re.fullmatch(r"j_[0-9a-f]{6,24}", jid):
        raise ValueError("bad job id")
    return jid


def save(job: dict) -> None:
    job["updated"] = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    _path(job["id"]).write_text(json.dumps(job, ensure_ascii=False, indent=1), encoding="utf-8")


def load(jid: str) -> dict | None:
    try:
        return json.loads(_path(jid).read_text(encoding="utf-8"))
    except (FileNotFoundError, ValueError):
        return None


def list_jobs(limit: int = 25) -> list[dict]:
    out = []
    for p in sorted(JOBS_DIR.glob("j_*.json"), key=lambda p: p.stat().st_mtime, reverse=True)[:limit]:
        try:
            j = json.loads(p.read_text(encoding="utf-8"))
            out.append({
                "id": j["id"], "created": j["created"], "status": j["status"],
                "stage": j["stage"], "stage_number": j["stage_number"],
                "subject": (j["input"]["text"] or "")[:90],
                "demo": j.get("demo", False),
            })
        except (json.JSONDecodeError, KeyError):
            continue
    return out


def log_stage(job: dict, entry: dict) -> None:
    """Append a stage-log entry and roll the budget counters."""
    job["stage_log"].append(entry)
    b = job["budget"]
    b["model_calls"] += 1
    b["search_results"] += entry.get("search_results", 0)
    u = entry.get("usage") or {}
    b["tokens_in"] += u.get("prompt_tokens", 0) or 0
    b["tokens_out"] += u.get("completion_tokens", 0) or 0


def write_report_file(job: dict) -> None:
    """The cumulative report file — meta, verdict history, then every stage's
    full content in order. Rebuilt from the job record each stage boundary, so
    it can never drift from the ledger."""
    lines = [
        f"# ScamShield background check — {job['id']}",
        "",
        f"- **Subject:** {(job['input']['text'] or '')[:200]}",
        f"- **Type/region:** {job['input'].get('region', 'US')} · worry: {job['input'].get('worry', 'legitimacy')}",
        f"- **Created:** {job['created']} · **Last updated:** {job['updated']}",
        f"- **Stages completed:** {job['stage_number']} · **Status:** {job['status']}",
        f"- **Mode:** {'demo (canned)' if job.get('demo') else 'live'} · "
        f"model calls: {job['budget']['model_calls']} · search results: {job['budget']['search_results']}",
        "",
    ]
    if job["verdict_history"]:
        lines += ["## Verdict history", ""]
        lines += [f"- {v.get('stage', '?')}: {v.get('verdict', '?')} — {v.get('confidence', '?')}"
                  + (f" *({v.get('label')})*" if v.get("label") else "")
                  for v in job["verdict_history"]]
        lines += [""]
    if job["transcript"]:
        lines += ["## Stage 1 (vision intake) — verbatim transcript (defanged)", "", "```",
                  job["transcript"], "```", ""]
    for e in job["stage_log"]:
        lines += [f"## {e['stage_label']}", "", e["content"], ""]
        if e.get("sources"):
            lines += ["**Sources this stage:**"] + [
                f"- {s.get('media') or 'source'} — [{s.get('title') or s.get('link')}]({s.get('link')})"
                for s in e["sources"][:20]] + [""]
    (REPORTS_DIR / f"{job['id']}.md").write_text("\n".join(lines), encoding="utf-8")


def public_view(job: dict) -> dict:
    """What the API returns — the full job minus raw image payloads."""
    out = {k: v for k, v in job.items() if k != "input"}
    out["input"] = {k: v for k, v in job["input"].items() if k != "images"}
    out["input"]["image_count"] = job["input"].get("image_count", 0)
    return out
