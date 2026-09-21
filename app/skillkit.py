"""Turns the rdw-scamshield-check-v2 skill files into per-stage system prompts.

The skill was written for a human-driven agent session; this module is the
port. The application is the stage manager (gates, ledger, budgets); the model
executes exactly one stage per call. Every stage prompt is the skill's own
prose for that stage plus:

- a hosted-execution preamble (who orchestrates, what the user sees), and
- the AGENTMETA contract — a small JSON block in an HTML comment at the end
  of every response that the app parses for gate logic and the UI chips.
  marked.js strips HTML comments, so users never see it.
"""
from __future__ import annotations

from pathlib import Path

SKILL_DIR = Path(__file__).parent / "content" / "skills" / "rdw-scamshield-check-v2"
_cache: dict[str, str] = {}


def skill_file(name: str) -> str:
    if name not in _cache:
        _cache[name] = (SKILL_DIR / name).read_text(encoding="utf-8")
    return _cache[name]


SAFETY = """
## Safety rules (binding, every stage)

- **Suspicious email = static analysis only.** Never suggest visiting, clicking,
  or replying. Domains are reputation-checked via search, never fetched.
- **Suspect stores = passive inspection only.** Never enter payment data,
  create accounts, message sellers, or download files from a subject.
- **Verdict discipline.** Evidence-linked language; documented vs inferred
  always distinguished; never call a business a scam beyond what evidence shows.
- **No fabrication.** Every cited complaint, review, or report must exist in
  search results actually returned in this conversation. Absence of hits is
  "no adverse record found", never "verified safe".
- **Defense-only posture.** Recognition and avoidance only.
- **Redact the user's PII** (name, address, order numbers) when quoting their
  material.
"""

PREAMBLE = """You are executing ONE stage of the ScamShield Check v2 skill inside a hosted
web service. The application orchestrates the stages, maintains the research
ledger between calls, and shows your response to the user in a browser. You
never see the user directly; the user sees everything you write.

Bindings for every response you produce:
- Follow the skill's output contract for the stage exactly (section order,
  verdict box format, coverage map, gauge with legend, plan block).
- End EVERY response with the AGENTMETA block — an HTML comment containing
  one JSON object on its own line, nothing else inside the comment:

<!--AGENTMETA
{"stage_label": "Stage 1 — Triage", "snap": false, "verdict_band": "🟠", "verdict": "Multiple red flags", "confidence": "Medium", "label": "provisional", "overall_gauge": "🟡 58/100", "recommend": "stage"}
-->

  Fields: stage_label (human label incl. stage number) · snap (true only for
  the initial Stage-½ snap response — later stages whose verdict label remains
  "snap" still set snap=false) · verdict_band (🟢🟡🟠🔴) · verdict (band name) ·
  confidence (High/Medium/Low) · label (snap|provisional|final) ·
  overall_gauge (e.g. "🟡 58/100" or "not rendered") · recommend
  ("stage" if a next stage pays, "consolidate" if it does not).
- The plan block ends with the gate line from the skill; the app renders it as
  buttons, so write it as written in the skill ("Reply 'go'…" or the snap
  "document" variant).
"""

AGENTMETA_SPEC = """End with the AGENTMETA block per the hosted-execution bindings. For this
stage set: stage_label, snap=false, verdict_band/verdict/confidence/label from
your verdict box, overall_gauge from your OVERALL line, and recommend.
"""


def smoke_system() -> str:
    return (
        PREAMBLE
        + SAFETY
        + "\n## Your stage: Stage 0 (classify) + Stage ½ (smoke test) — zero searches\n\n"
        + "First classify the subject into exactly one type: product listing · "
        "website/store · social post/ad · suspicious email · online seller. One "
        "subject = one check; a bundle (email pointing to a store) is ONE "
        "investigation with a primary subject. If the user named a category "
        "instead of a specific subject, ask your one clarification question and "
        "stop.\n\n"
        + "Then run the smoke test over the supplied material ONLY — zero "
        "searches, zero fetches. Follow the checklist's rules exactly, including "
        "every false-positive guard: an item fired without its guard satisfied "
        "is a false positive, not caution.\n\n"
        + "### The smoke checklist (authoritative)\n\n"
        + skill_file("smoke-test.md")
        + "\n\n### Output\n\n"
        + "If any [Decisive] item fires: deliver the ultra-short snap response "
        "from the checklist (verdict box 🔴 High labeled snap, fired tells with "
        "item IDs + T-ID mapping, 2–3 do/don't bullets, the snap gate line). "
        "Set snap=true, label=\"snap\" in AGENTMETA; overall_gauge=\"not "
        "rendered\"; recommend=\"consolidate\" (the offered doc pass is "
        "optional).\n\n"
        + "If only [Corroborating] items fire, or nothing fires: say so in 2–4 "
        "lines (classification, what fired with item IDs, that Stage 1 triage "
        "is next and starts with these observations). verdict_band/verdict may "
        "be your provisional read; label=\"provisional\"; "
        "overall_gauge=\"not rendered\"; recommend=\"stage\".\n\n"
        + AGENTMETA_SPEC
    )


def research_system(stage: str) -> str:
    assert stage in ("triage", "verify", "document")
    head = {
        "triage": (
            "## Your stage: Stage 1 — Triage (light and fast)\n\n"
            "Run the Stage-1 sweep: 10–14 searches, snippet-first, spread across "
            "the subject's applicable check lines per its guide, including the "
            "standard sweeps (<identifier> scam / complaint / reviews). Map every "
            "observed signal to technique IDs where one fits. Then deliver the "
            "Stage-1 response: verdict box (provisional), key findings with "
            "T-ID mapping, coverage map, ripeness gauge (prospect estimates, "
            "labeled as such) + OVERALL line, next-stage plan (2–4 target lines "
            "ordered by relevance × yield, budget stated), gate line."
        ),
        "verify": (
            "## Your stage: Stage N (N ≥ 2) — Verify\n\n"
            "Execute the approved plan in the user message. Ledger discipline is "
            "binding: never re-run a logged query, never re-record an existing "
            "finding (a repeat is corroboration attached to the existing finding, "
            "not a new one), park promising unfetched results in the lead pool "
            "instead of chasing them mid-stage. Record findings as: one-line "
            "finding + source + URL + date + check line + confidence tag "
            "([Documented]/[Reported]/[Inferred]). Contradictions surface "
            "explicitly. Close the stage: banner, 3–6 new findings (🆕) with "
            "T-ID mapping, verdict box, coverage map, re-scored ripeness gauge + "
            "OVERALL, next default plan (or consolidation recommendation if the "
            "gauge reads 🟠/🔴 or coverage is complete), gate line."
        ),
        "document": (
            "## Your stage: documentation pass (after a snap verdict)\n\n"
            "The snap verdict already stands on direct observation. Run the "
            "Stage-1 search sweep AGAINST THE PATTERN that fired (the technique's "
            "documented record: agency alerts, reporting on the campaign or "
            "pattern class), not to re-justify the band. Then deliver the "
            "Stage-1-shaped response with the snap verdict as its verdict box "
            "(label stays \"snap\"). Normal outcome: band unchanged, confidence "
            "wording gains named sources. If documentation contradicts the snap, "
            "show verdict movement explicitly with the cause named."
        ),
    }[stage]

    return (
        PREAMBLE
        + SAFETY
        + "\n## The skill (procedure, concepts, contracts)\n\n"
        + skill_file("SKILL.md")
        + "\n\n## Subject check guides (read only the matching guide)\n\n"
        + skill_file("subject-check-guides.md")
        + "\n\n## Technique catalog (T-IDs, signals, rails, reporting)\n\n"
        + skill_file("technique-catalog.md")
        + "\n\n## Verdict rubric (bands, confidence, boxes, plans)\n\n"
        + skill_file("verdict-rubric.md")
        + "\n\n## Ripeness & relevance gauge\n\n"
        + skill_file("ripeness-rubric.md")
        + "\n\n## "
        + head
        + "\n\n"
        + AGENTMETA_SPEC
    )


def consolidate_system() -> str:
    return (
        PREAMBLE
        + SAFETY
        + "\n## Your stage: Consolidate (final report)\n\n"
        "Restructure the ledger provided in the user message into the final "
        "background check. The consolidated report must stand alone for a reader "
        "who never saw the stages. File sections, in order: meta header "
        "(subject · type · region · created · last updated · stage count · "
        "status) · Verdict Box (final — drop provisional; a snap verdict keeps "
        "its snap label) · Subject Profile · Evidence by Check Line (H3 per "
        "line; findings cited) · Red Flags → Technique Mapping · Coverage Map · "
        "Ripeness Gauge (final table + overall) · Recommended Actions · If "
        "Victim: Recovery Ladder · Where to Report · Gaps & Caveats · Sources "
        "(tiered, with access dates).\n\n"
        "Chat-shape wrapper: begin with the verdict box, then a one-paragraph "
        "basis, then the final gauge statement (why further stages would not "
        "pay — or what remains open), then the full report body. Use only what "
        "is in the ledger — no new searching, no new claims. Set "
        "label=\"final\" and recommend=\"consolidate\" in AGENTMETA.\n\n"
        "Rubric reminders that bind consolidation:\n\n"
        + skill_file("verdict-rubric.md")
        + "\n"
        + AGENTMETA_SPEC
    )


# --- ledger digest: what the model sees of prior stages ------------------------

def ledger_digest(job: dict, today: str) -> str:
    """Compact, faithful context for the next research call. Mirrors the
    skill's ledger: query log (as already-seen sources), findings index (as the
    prior stage outputs), verdict history, gauge history."""
    inp = job["input"]
    parts = [
        f"Today: {today}",
        f"Subject (user's words): {inp['text']}",
        f"Worry/angle: {inp.get('worry') or 'legitimacy'} · Region: {inp.get('region') or 'US'}",
        f"Images attached: {inp.get('image_count', 0)}",
    ]
    if job.get("transcript"):
        parts += ["", "## Stage 1 (vision intake) — verbatim transcript (defanged):",
                  job["transcript"]]
    if job.get("verdict_history"):
        parts += ["", "## Verdict history:"]
        parts += [f"- {v.get('stage')}: {v.get('verdict')} — {v.get('confidence')}"
                  + (f" ({v.get('label')})" if v.get("label") else "")
                  for v in job["verdict_history"]]
    seen_urls: list[str] = []
    for e in job["stage_log"]:
        for s in e.get("sources") or []:
            u = s.get("link")
            if u and u not in seen_urls:
                seen_urls.append(u)
    if seen_urls:
        parts += ["", f"## Query log — sources already seen ({len(seen_urls)}; "
                      "never re-record one of these as a new finding):"]
        parts += [f"- {u}" for u in seen_urls]
    # prior stage outputs, most recent last
    for e in job["stage_log"]:
        parts += ["", f"## {e['stage_label']} — full prior output:", e["content"]]
    parts += ["", f"Budget note: {job['budget']['model_calls']} model calls used "
                  f"so far this job."]
    return "\n".join(parts)
