"""Conversation store for the chat surfaces — JSON files under DATA_DIR/chats.

z.ai chat completions are stateless (client resends full history), so each
conversation is just an ordered message list persisted between turns.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import secrets

from jobs import DATA_DIR

CHATS_DIR = DATA_DIR / "chats"
CHATS_DIR.mkdir(parents=True, exist_ok=True)

_ID_RE = re.compile(r"^c_[0-9a-f]{6,24}$")
MAX_TURNS = int(os.getenv("MAX_CHAT_TURNS", "12"))   # hard cap per conversation


def safe_id(cid: str) -> str:
    return cid if _ID_RE.match(cid or "") else ""


def _path(cid: str) -> "object":
    return CHATS_DIR / f"{cid}.json"


def new_conversation(mode: str) -> dict:
    cid = "c_" + secrets.token_hex(4)
    conv = {
        "id": cid, "mode": mode,
        "created": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "updated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "title": "", "messages": [],
        "budget": {"model_calls": 0, "search_results": 0},
    }
    save(conv)
    return conv


def load(cid: str) -> dict | None:
    p = _path(cid)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def save(conv: dict) -> None:
    conv["updated"] = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    _path(conv["id"]).write_text(json.dumps(conv, ensure_ascii=False, indent=1),
                                 encoding="utf-8")


def list_conversations(limit: int = 50) -> list[dict]:
    out = []
    for p in sorted(CHATS_DIR.glob("c_*.json"), key=lambda x: x.stat().st_mtime,
                    reverse=True)[:limit]:
        try:
            c = json.loads(p.read_text(encoding="utf-8"))
            out.append({
                "id": c.get("id"), "mode": c.get("mode"),
                "title": c.get("title") or _derive_title(c),
                "updated": c.get("updated"),
                "turns": len([m for m in c.get("messages", [])
                              if m.get("role") == "user"]),
            })
        except (json.JSONDecodeError, OSError):
            continue
    return out


def _derive_title(conv: dict) -> str:
    for m in conv.get("messages", []):
        if m.get("role") == "user" and m.get("content"):
            text = m["content"].splitlines()[0][:70]
            return text + ("…" if len(text) == 70 else "")
    return "(empty)"


def delete(cid: str) -> bool:
    p = _path(cid)
    if p.exists():
        p.unlink()
        return True
    return False


def add_message(conv: dict, role: str, content: str, sources: list | None = None):
    msg = {"role": role, "content": content, "ts":
           dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
    if sources:
        msg["sources"] = sources
    conv["messages"].append(msg)
    if role == "user" and not conv.get("title"):
        conv["title"] = _derive_title(conv)
    save(conv)
    return msg
