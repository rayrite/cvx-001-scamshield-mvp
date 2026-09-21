"""The agent registry — every research mode the chat/quick surfaces offer.

Two kinds of modes:

- **skill:*** multi-turn chat running a full rdw-* staged skill. The skill's
  SKILL.md + references become the system prompt; the conversation IS the
  agent session the skills were designed for — the user's replies drive the
  gates ("go" / custom direction / "stop"). One model call per turn.
- **quick:*** single-pass research using the paste-ready system prompts from
  zai-scamshield-prompts-2026-09 (one bounded sweep, 3–4 independent
  indicator lines, no staging).

Demo mode (no ZAI_API_KEY): canned but honest responses — clearly labeled
canned examples of the real output shape, never fabricated research.
"""
from __future__ import annotations

from pathlib import Path

CONTENT = Path(__file__).parent / "content"

# --- skill modes: directory → files to concatenate into the system prompt ------

SKILLS: dict[str, dict] = {
    "skill:product-dig": {
        "kind": "skill", "dir": "rdw-product-dig",
        "label": "ProductDig", "emoji": "🔧",
        "blurb": "Physical products — cars, electronics, appliances: reliability, "
                 "owner sentiment, defect/warranty history, recalls.",
        "files": ["SKILL.md", "references/category-vein-guides.md",
                  "references/ripeness-rubric.md"],
    },
    "skill:recall-check": {
        "kind": "skill", "dir": "rdw-scamshield-recall-check-v2",
        "label": "RecallCheck v2", "emoji": "🥫",
        "blurb": "US product & food recalls — dual-mode roundup + subject lookup, "
                 "with geographic spread and smoke-test speed.",
        "files": ["SKILL.md", "references/smoke-test.md",
                  "references/subject-check-guides.md", "references/recall-source-guides.md",
                  "references/overview-map.md", "references/verdict-rubric.md",
                  "references/ripeness-rubric.md"],
    },
    "skill:corpcheck": {
        "kind": "skill", "dir": "rdw-scamshield-tea2-corpcheck",
        "label": "TEA2 CorpCheck", "emoji": "🏢",
        "blurb": "Companies & brands — dark-pattern record, complaint history, "
                 "regulatory actions; friction-based severity; balanced by mandate.",
        "files": ["SKILL.md", "references/smoke-test.md",
                  "references/check-line-guides.md", "references/corp-register.md",
                  "references/verdict-rubric.md", "references/ripeness-rubric.md"],
    },
}

# --- quick modes: single-pass system prompts -----------------------------------

QUICK: dict[str, dict] = {
    "quick:scamshield": {
        "kind": "quick", "file": "system-prompt-scamshield-check.md",
        "label": "Quick — E-commerce / email check", "emoji": "🛒",
        "blurb": "Listings, stores, social ads, suspicious emails, sellers. "
                 "One bounded pass, snap verdicts included.",
    },
    "quick:recall": {
        "kind": "quick", "file": "system-prompt-recall-check.md",
        "label": "Quick — Recall check", "emoji": "🥫",
        "blurb": "US product/food recall roundup or lookup in one pass.",
    },
    "quick:corpcheck": {
        "kind": "quick", "file": "system-prompt-corpcheck.md",
        "label": "Quick — Company check", "emoji": "🏢",
        "blurb": "Company dark-pattern background check with a Balance line.",
    },
    "quick:productdig": {
        "kind": "quick", "file": "system-prompt-product-dig.md",
        "label": "Quick — Product reliability check", "emoji": "🔧",
        "blurb": "Product reliability & ownership check in one pass.",
    },
}

CHAT_PREAMBLE = """You are running a hosted research skill inside a chat interface.
Bindings for every reply:

- This chat IS the skill's agent session. The user's messages drive the
  procedure: replying "go" approves your proposed next stage, a described
  direction redirects it, and "stop" (or consolidation language) ends it.
- Deliver ONE stage per reply — never bundle several stages to save turns.
- Follow the skill's response contract for the stage exactly (section order,
  verdict box, coverage map, gauge, plan).
- Verdict, confidence, and ripeness are three separate, independent
  indicators — never merged, never derived from each other.
- Every research reply ends with a short "**Next:**" line naming the default
  next stage so the user can reply "go" — or redirect, or stop.
- Today's date is supplied in the conversation; anchor time-sensitive
  searches to it.
- Cite only what your searches actually returned. Absence of hits is "no
  adverse record found", never "verified safe". Balanced reporting: favorable
  findings are swept and reported like adverse ones.

"""

_cache: dict[str, str] = {}


def _read(path: Path) -> str:
    key = str(path)
    if key not in _cache:
        _cache[key] = path.read_text(encoding="utf-8")
    return _cache[key]


def system_prompt(mode: str) -> str:
    """Full system prompt for a mode (cached)."""
    if mode in SKILLS:
        s = SKILLS[mode]
        base = CONTENT / "skills" / s["dir"]
        parts = [CHAT_PREAMBLE, f"# Skill: {s['label']}\n\n"]
        for f in s["files"]:
            parts.append(f"\n\n----- {f} -----\n\n{_read(base / f)}")
        return "".join(parts)
    if mode in QUICK:
        return _read(CONTENT / "prompts" / QUICK[mode]["file"])
    raise KeyError(mode)


def modes_available() -> dict[str, dict]:
    """Registry with availability (files present?) for /api/modes + flags."""
    out: dict[str, dict] = {}
    for mid, s in SKILLS.items():
        base = CONTENT / "skills" / s["dir"]
        out[mid] = {**{k: s[k] for k in ("kind", "label", "emoji", "blurb")},
                    "available": all((base / f).exists() for f in s["files"])}
    for mid, q in QUICK.items():
        out[mid] = {**{k: q[k] for k in ("kind", "label", "emoji", "blurb")},
                    "available": (CONTENT / "prompts" / q["file"]).exists()}
    return out


def registry() -> dict[str, dict]:
    return {**SKILLS, **QUICK}


# --- demo mode: canned, honestly labeled ----------------------------------------

DEMO_FIRST = {
    "skill": (
        "**Stage 1 — Triage sweep (demo)**\n\n"
        "Subject classified; smoke test found no decisive snap tells, so the "
        "Stage-1 sweep ran: 12 searches across the applicable check lines.\n\n"
        "**Coverage map** ⚪🔵🚩🔴 and the ripeness gauge would render here, "
        "with findings cited and dated.\n\n"
        "> **Provisional verdict:** 🟠 Multiple red flags — Medium confidence "
        "*(provisional)*\n\n"
        "**Next:** reply `go` for the verification stage, describe a different "
        "direction, or say `stop` to consolidate.\n\n"
        "*(Demo mode — set `ZAI_API_KEY` on the server to run the real skill "
        "with live web search. This canned reply shows the response shape only.)*"
    ),
    "quick": (
        "> **Verdict:** 🔴 Scam pattern match\n"
        "> **Confidence:** High\n"
        "> **Ripeness:** LOW — closed by direct observation\n\n"
        "The three lines above are the quick-check contract: verdict, "
        "confidence, and ripeness stay three independent indicators, each with "
        "its own basis. With `ZAI_API_KEY` set, this mode runs the real "
        "single-pass research sweep with live web search and citations.\n\n"
        "*(Demo mode canned example — no search was performed.)*"
    ),
}

DEMO_LATER = (
    "*(Demo mode continues — each further turn would run the skill's next "
    "stage with live search. Set `ZAI_API_KEY` to enable the real pipeline; "
    "the staged Check page offers a fully walkable canned example.)*"
)


def demo_reply(mode: str, turn: int) -> str:
    if turn <= 1:
        return DEMO_FIRST["skill" if mode in SKILLS else "quick"]
    return DEMO_LATER
