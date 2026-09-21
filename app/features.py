"""Feature flags — features.json in the app root, defaulting all-on.

A flag is only *effective* when its content exists too: `learning` needs at
least one wiki HTML, `apps` at least one SPA HTML, `chat`/`quick` need their
prompt files present. The /api/features response and `cli.py status` both
report flag vs. effective so a missing file is visible, not silent.
"""
from __future__ import annotations

import json
import threading
from pathlib import Path

import agents

FLAGS_FILE = Path(__file__).parent / "features.json"

DEFAULT_FLAGS: dict[str, bool] = {
    "check": True,      # staged ScamShield Check v2 (jobs API + /check page)
    "chat": True,       # multi-turn skill chat
    "quick": True,      # single-pass quick research
    "learning": True,   # Learning Center (static wikis)
    "apps": True,       # dynamic SPA menu
    "video": True,      # sample streaming page (/video — two placeholder players)
    "theme": True,      # UDL editor
    "waitlist": True,   # email capture
}

_lock = threading.Lock()


def load_flags() -> dict[str, bool]:
    flags = dict(DEFAULT_FLAGS)
    if FLAGS_FILE.exists():
        try:
            data = json.loads(FLAGS_FILE.read_text(encoding="utf-8"))
            for k in DEFAULT_FLAGS:
                if k in data:
                    flags[k] = bool(data[k])
        except (json.JSONDecodeError, OSError):
            pass
    return flags


def save_flags(flags: dict[str, bool]) -> dict[str, bool]:
    merged = load_flags()
    for k in DEFAULT_FLAGS:
        if k in flags:
            merged[k] = bool(flags[k])
    with _lock:
        FLAGS_FILE.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")
    return merged


def _wikis() -> list[str]:
    d = agents.CONTENT / "wikis"
    return sorted(p.name for p in d.glob("*.html")) if d.is_dir() else []


def _spas() -> list[str]:
    d = agents.CONTENT / "spas"
    return sorted(p.name for p in d.glob("*.html")) if d.is_dir() else []


def effective() -> dict[str, bool]:
    """Flag AND its content actually being there."""
    flags = load_flags()
    modes = agents.modes_available()
    skills_ok = any(m.get("available") for m in modes.values() if m["kind"] == "skill")
    quick_ok = any(m.get("available") for m in modes.values() if m["kind"] == "quick")
    return {
        **flags,
        "chat": flags["chat"] and skills_ok,
        "quick": flags["quick"] and quick_ok,
        "learning": flags["learning"] and len(_wikis()) > 0,
        "apps": flags["apps"] and len(_spas()) > 0,
    }


def inventory() -> dict:
    modes = agents.modes_available()
    return {
        "skills": sum(1 for m in modes.values() if m["kind"] == "skill"
                      and m.get("available")),
        "quick_prompts": sum(1 for m in modes.values() if m["kind"] == "quick"
                             and m.get("available")),
        "wikis": len(_wikis()),
        "spas": len(_spas()),
    }
