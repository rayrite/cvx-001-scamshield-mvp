"""The stage manager — runs rdw-scamshield-check-v2 as a hosted state machine.

Flow per job (mirrors the skill's procedure):

    intake (vision, only if images) → smoke (zero tools)
        ├─ snap verdict  → GATE(post_snap: document / stop / custom)
        └─ fall-through  → triage (web_search) → GATE(post_stage: go / stop / custom)
                              └─ go/custom → verify (web_search) → GATE …
                                  └─ stop (or cap hit) → consolidate (zero tools) → done

Every model call is logged in the job's stage_log; the cumulative report file
is rewritten at each stage boundary. The user never talks to the model
directly — the gate decisions are UI buttons that resume this machine.
"""
from __future__ import annotations

import asyncio
import datetime as dt
import json
import re

import httpx

import jobs
import skillkit
import zai

DEMO = "ZAI_API_KEY" not in __import__("os").environ


# --- AGENTMETA parsing (lenient; defaults keep the machine moving) -------------

_META_RE = re.compile(r"<!--AGENTMETA\s*(\{.*?\})\s*-->", re.DOTALL)


def parse_agentmeta(content: str) -> dict:
    m = _META_RE.search(content)
    if not m:
        return {}
    try:
        meta = json.loads(m.group(1))
        return meta if isinstance(meta, dict) else {}
    except json.JSONDecodeError:
        return {}


def extract_plan(content: str) -> str:
    """The NEXT STAGE block (plan + budget), without the gate line."""
    m = re.search(r"^NEXT STAGE.*?(?=^Reply |^Say |<!--AGENTMETA|\Z)", content,
                  re.DOTALL | re.MULTILINE)
    return m.group(0).strip() if m else "Continue the most promising check lines per the last gauge."


# --- stage plumbing ------------------------------------------------------------

async def _run_model_stage(job: dict, stage: str, stage_label: str, user_msg: str,
                           *, tools: bool, count: int = 10) -> dict:
    """One model call, logged. Returns the stage-log entry."""
    t0 = dt.datetime.now()
    async with httpx.AsyncClient() as client:
        if tools:
            content, sources, usage = await zai.research_call(
                client, skillkit.research_system(stage), user_msg,
                job["created"][:10], count=count)
            model = zai.RESEARCH_MODEL
        else:
            if stage == "smoke":
                system = skillkit.smoke_system()
            elif stage == "consolidate":
                system = skillkit.consolidate_system()
            else:
                system = skillkit.research_system(stage)
            content, usage = await zai.plain_call(client, system, user_msg)
            sources, model = [], zai.RESEARCH_MODEL
    elapsed = (dt.datetime.now() - t0).total_seconds()
    entry = {
        "stage": stage, "stage_label": stage_label,
        "ts": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "model": model, "content": content, "sources": sources,
        "usage": usage, "search_results": len(sources),
        "elapsed_s": round(elapsed, 1),
    }
    jobs.log_stage(job, entry)
    return entry


def _close_stage(job: dict, entry: dict) -> None:
    """Parse AGENTMETA, update verdict history, set the gate, persist."""
    meta = parse_agentmeta(entry["content"])
    label = meta.get("label") or ("snap" if meta.get("snap") else "provisional")
    job["verdict_history"].append({
        "stage": meta.get("stage_label") or entry["stage_label"],
        "verdict": f"{meta.get('verdict_band', '?')} {meta.get('verdict', '?')}".strip(),
        "confidence": meta.get("confidence", "?"),
        "label": label,
    })
    if meta.get("snap"):
        job["gate"] = {
            "kind": "post_snap",
            "prompt": "Snap verdict delivered. The archived report is optional documentation.",
            "options": ["document", "stop"], "custom_allowed": True,
        }
    else:
        rec = (meta.get("recommend") or "stage").lower()
        job["gate"] = {
            "kind": "post_stage",
            "prompt": "Stage complete — review the verdict, coverage, and gauge below.",
            "options": ["go", "stop"], "custom_allowed": True,
            "pushback": rec.startswith("consolid"),
            "overall_gauge": meta.get("overall_gauge", ""),
        }
    job["status"] = "awaiting_gate"
    jobs.write_report_file(job)
    jobs.save(job)


async def _fail(job: dict, exc: Exception) -> None:
    job["status"] = "error"
    job["error"] = f"{type(exc).__name__}: {exc}"
    jobs.save(job)


# --- the machine ----------------------------------------------------------------

async def run_initial(jid: str) -> None:
    job = jobs.load(jid)
    if not job:
        return
    try:
        job["status"], job["stage"] = "running", "intake"
        jobs.save(job)
        today = dt.date.today().isoformat()

        # Stage 1 — vision intake (only when screenshots were attached)
        if job["input"]["image_count"]:
            if DEMO:
                await asyncio.sleep(0.9)
                job["transcript"] = DEMO_TRANSCRIPT
                usage = {}
            else:
                async with httpx.AsyncClient() as client:
                    job["transcript"], usage = await zai.vision_intake(
                        client, job["input"]["text"], job["input"]["images"], today)
                jobs.log_stage(job, {
                    "stage": "intake", "stage_label": "Stage 1 — Vision intake (glm-5.3-flash)",
                    "ts": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                    "model": zai.INTAKE_MODEL, "content": job["transcript"],
                    "sources": [], "usage": usage, "search_results": 0, "elapsed_s": 0,
                })
            jobs.save(job)

        # Stage 0 + ½ — classify + smoke test (zero tools)
        job["stage"] = "smoke"
        jobs.save(job)
        subject = _subject_msg(job, today)
        if DEMO:
            await asyncio.sleep(0.9)
            entry = _demo_entry("smoke", "Stage 0 + ½ — Classify + smoke test", DEMO_SMOKE)
            jobs.log_stage(job, entry)
        else:
            entry = await _run_model_stage(
                job, "smoke", "Stage 0 + ½ — Classify + smoke test", subject, tools=False)
        meta = parse_agentmeta(entry["content"])

        if meta.get("snap"):
            _close_stage(job, entry)
            return

        # Stage 1 — triage (web_search)
        await _research(job, "triage", "Stage 1 — Triage sweep", today)
    except Exception as exc:  # noqa: BLE001 — surface everything to the job record
        await _fail(job, exc)


async def _research(job: dict, stage: str, label: str, today: str,
                    plan: str | None = None, custom: str | None = None) -> None:
    job["status"], job["stage"] = "running", stage
    job["stage_number"] = max(job["stage_number"], 1 if stage == "triage" else job["stage_number"])
    jobs.save(job)
    user_msg = skillkit.ledger_digest(job, today)
    if stage == "triage":
        user_msg += ("\n\n(This is Stage 1 — run the triage sweep now; the smoke-test "
                     "observations above are your opening findings.)")
    elif stage == "document":
        user_msg += "\n\n(Run the documentation pass against the pattern that fired.)"
    elif custom:
        user_msg += (f"\n\nUSER REDIRECT: \"{custom}\"\n"
                     "Restate your interpretation in one line, plan to match, execute.")
    elif plan:
        user_msg += f"\n\nThe approved plan — execute verbatim, do not re-plan:\n\n{plan}"

    if job["budget"]["model_calls"] >= zai.MAX_STAGE_CALLS:
        note = (f"Budget cap reached ({zai.MAX_STAGE_CALLS} model calls) — "
                "skipping further stages; consolidating.")
        job["stage_log"].append({"stage": "cap", "stage_label": "Budget cap",
                                 "ts": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                                 "model": "-", "content": note, "sources": [],
                                 "usage": {}, "search_results": 0, "elapsed_s": 0})
        return await consolidate(job["id"])

    if stage in ("triage", "document"):
        job["stage_number"] = max(job["stage_number"], 1)

    if DEMO:
        await asyncio.sleep(1.1)
        entry = _demo_entry(stage, label, DEMO_STAGES.get(stage, DEMO_VERIFY))
        jobs.log_stage(job, entry)
    else:
        entry = await _run_model_stage(job, stage, label, user_msg, tools=True)
    _close_stage(job, entry)


def _subject_msg(job: dict, today: str) -> str:
    parts = [f"Today: {today}",
             f"Subject (user's words): {job['input']['text']}",
             f"Worry/angle: {job['input'].get('worry') or 'legitimacy'} · "
             f"Region: {job['input'].get('region') or 'US'}"]
    if job.get("transcript"):
        parts += ["", "The subject arrived as screenshot(s); verbatim transcript (defanged):",
                  job["transcript"]]
    return "\n".join(parts)


async def run_gate(jid: str, decision: str, custom: str | None = None) -> dict | None:
    """Resume the machine from a gate decision. Returns an error dict or None."""
    job = jobs.load(jid)
    if not job:
        return {"error": "no such job", "status": 404}
    if job["status"] != "awaiting_gate":
        return {"error": f"job is {job['status']}, not awaiting a gate", "status": 409}
    decision = (decision or "").strip().lower()
    if decision not in ("go", "stop", "document", "custom") or (decision == "custom" and not custom):
        return {"error": "decision must be go|stop|document|custom (custom needs text)", "status": 400}
    job["gate"] = None
    jobs.save(job)
    today = dt.date.today().isoformat()
    try:
        if decision == "stop":
            return await consolidate(jid)
        last = job["stage_log"][-1] if job["stage_log"] else None
        if decision == "document":
            await _research(job, "document", "Documentation pass (post-snap)", today)
        elif decision == "go":
            n = job["stage_number"] + 1
            job["stage_number"] = n
            plan = extract_plan(last["content"]) if last else None
            await _research(job, "verify", f"Stage {n} — Verify", today, plan=plan)
        else:  # custom
            n = job["stage_number"] + 1
            job["stage_number"] = n
            await _research(job, "verify", f"Stage {n} — Verify (redirected)", today, custom=custom)
    except Exception as exc:  # noqa: BLE001
        await _fail(job, exc)
    return None


async def consolidate(jid: str) -> None:
    job = jobs.load(jid)
    if not job:
        return
    today = dt.date.today().isoformat()
    try:
        job["status"], job["stage"] = "running", "consolidate"
        jobs.save(job)
        user_msg = skillkit.ledger_digest(job, today) + "\n\nConsolidate now — final report."
        if DEMO:
            await asyncio.sleep(1.0)
            job["report"] = DEMO_FINAL
            usage = {}
        else:
            async with httpx.AsyncClient() as client:
                report, usage = await zai.plain_call(
                    client, skillkit.consolidate_system(), user_msg)
            job["report"] = report
        meta = parse_agentmeta(job["report"])
        job["stage_log"].append({
            "stage": "consolidate", "stage_label": "Consolidate — final report",
            "ts": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "model": "demo" if DEMO else zai.RESEARCH_MODEL,
            "content": "*Final report rendered below.*", "sources": [],
            "usage": usage, "search_results": 0, "elapsed_s": 0,
        })
        job["budget"]["model_calls"] += 1
        job["budget"]["tokens_in"] += (usage or {}).get("prompt_tokens", 0) or 0
        job["budget"]["tokens_out"] += (usage or {}).get("completion_tokens", 0) or 0
        job["verdict_history"].append({
            "stage": meta.get("stage_label", "Consolidated"),
            "verdict": f"{meta.get('verdict_band', '?')} {meta.get('verdict', '?')}".strip(),
            "confidence": meta.get("confidence", "?"),
            "label": meta.get("label", "final"),
        })
        job["status"] = "done"
        job["stage_number"] = job["stage_number"] or 1
        jobs.write_report_file(job)
        jobs.save(job)
    except Exception as exc:  # noqa: BLE001
        await _fail(job, exc)


# --- demo mode: the USPS snap example, walkable end-to-end with no key ----------

DEMO_TRANSCRIPT = """**From:** USPS Package Services <no-reply@usps-delivery-fee[.]net>
**Reply-To:** support@mail[.]usps-delivery-fee[.]net
**Subject:** Your package is on hold — action required within 48 hours
**Date:** 2026-09-20

Your package US9424012345 is on hold at our facility due to an unpaid redelivery
fee of $1.99. Click below to pay and schedule redelivery:

[pay redelivery fee]  (link: hxxps://usps-delivery-fee[.]net/pay)

If not paid within 48 hours the package will be returned to sender."""


DEMO_SMOKE = """> ## ⚠️ VERDICT: 🔴 Scam pattern match — High confidence *(snap, Stage ½ — zero searches)*
> **Basis:** S-E1 sender-identity failure (display name "USPS", @-domain usps-delivery-fee[.]net ≠ usps.com) + S-E3 carrier fee-by-link (T-0504) — both observed in the email itself.
> **Do/don't:** don't click/reply; track only at usps.com; report to USPIS + FTC.

**Classification:** suspicious email (impersonated institution: USPS).

Checked in seconds, zero searches — the material itself settles it. S-E4-class
reply-to divergence also present (corroborating).

Say "document" for the full archived report (pattern documentation, sources, ledger) ·
describe a different direction to customize · "stop" to finish here.

<!--AGENTMETA
{"stage_label": "Stage 0 + ½ — Classify + smoke test", "snap": true, "verdict_band": "🔴", "verdict": "Scam pattern match", "confidence": "High", "label": "snap", "overall_gauge": "not rendered", "recommend": "consolidate"}
-->"""

DEMO_DOCUMENT = """## Documentation pass — USPS redelivery-fee smishing (T-0504)

**C1 Advisory portals** — 🚩 USPS Inspection Service and FTC consumer alerts both
document the "package on hold / redelivery fee" smishing wave; FTC's imposter-
scam tally lists shipping imposters among the top-reported categories. *(Snippet-
verified this pass.)*

**C3 Domain forensics** — 🔴 the sender domain usps-delivery-fee[.]net is not a
USPS property; genuine USPS notices track only inside usps.com and never invoice
fees by external link. Brand-clone confirmation (T-0302 pattern applied to email).

**C9 Community** — 🚩 recurring victim reports of the same $1.99/$2.99 redelivery
lure across scam-report boards, 2024–2026, seasonal spikes each Q4.

## Coverage Map — documentation pass

| Line | Status | What was checked / found |
|---|---|---|
| C1 Advisory portals | 🚩 flagged | USPIS + FTC alerts document the pattern wave |
| C3 Domain forensics | 🔴 hit | domain ≠ usps.com; fee-by-link = T-0504 |
| C9 Community | 🚩 flagged | victim reports of the identical lure |

Legend: ⚪ unchecked · 🔵 checked, clean · 🚩 checked, flagged · 🔴 checked, hit · ➖ not applicable.

## Ripeness Gauge — documentation pass

| Line | Richness | Yield (headline) | Relevance | Evidence |
|---|---|---|---|---|
| C1 Advisory portals | 60 | 🔴 20 | High | confirmed pattern-level documentation; nothing subject-specific exists |
| C3 Domain forensics | 70 | 🔴 15 | High | static fact, already fully observed |
| C9 Community | 40 | 🔴 20 | Medium | pattern repeats only; no named-infrastructure thread |

**OVERALL: 🔴 18/100** — documentation complete by design; nothing further to dig.

NEXT STAGE (default, awaiting approval)
  1. None recommended — the gauge reads 🔴; consolidation is the honest close.

Reply "go" to run this plan · describe a different direction to customize · "stop" to finalize the background-check report.

<!--AGENTMETA
{"stage_label": "Documentation pass (post-snap)", "snap": false, "verdict_band": "🔴", "verdict": "Scam pattern match", "confidence": "High", "label": "snap", "overall_gauge": "🔴 18/100", "recommend": "consolidate"}
-->"""

DEMO_VERIFY = """## Stage 2 — Verify (redirected)

**🆕 C1** No subject-specific enforcement record exists for this sender domain —
consistent with hit-and-run infrastructure (T-0106 adjacent). *(Checked: FTC,
IC3, BBB — confirmed absence at portal-query level.)*

**🆕 C9** One board thread reports the identical domain family expiring and
re-registering under lookalikes — corroborates disposable-infrastructure read.

## Coverage Map — after Stage 2

| Line | Status | What was checked / found |
|---|---|---|
| C1 Advisory portals | 🔵 checked | pattern documented; no subject-specific record (absence, not safety) |
| C3 Domain forensics | 🔴 hit | domain ≠ usps.com; fee-by-link = T-0504 |
| C9 Community | 🔵 checked | pattern-level corroboration only |

## Ripeness Gauge — after Stage 2

| Line | Richness | Yield | Relevance | Evidence |
|---|---|---|---|---|
| C1 | 60 | 🔴 15 | High | confirmed absence — harvest complete |
| C3 | 70 | 🔴 10 | High | static fact, fully observed |
| C9 | 40 | 🔴 15 | Medium | repeats only |

**OVERALL: 🔴 15/100** — exhausted; consolidation recommended.

Reply "go" to run this plan · describe a different direction to customize · "stop" to finalize the background-check report.

<!--AGENTMETA
{"stage_label": "Stage 2 — Verify", "snap": false, "verdict_band": "🔴", "verdict": "Scam pattern match", "confidence": "High", "label": "snap", "overall_gauge": "🔴 15/100", "recommend": "consolidate"}
-->"""

DEMO_STAGES = {"triage": DEMO_DOCUMENT, "document": DEMO_DOCUMENT, "verify": DEMO_VERIFY}


def _demo_entry(stage: str, label: str, content: str) -> dict:
    return {
        "stage": stage, "stage_label": label,
        "ts": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "model": "demo", "content": content, "sources": [
            {"refer": "usps-delivery-fee[.]net", "title": "USPIS — package smishing alerts",
             "link": "https://www.uspis.gov/news/scam-alerts", "media": "uspis.gov", "publish_date": ""},
            {"refer": "FTC imposter scams", "title": "FTC — imposter scams",
             "link": "https://consumer.ftc.gov/articles/how-avoid-impersonator-scam", "media": "ftc.gov", "publish_date": ""},
        ], "usage": {}, "search_results": 2, "elapsed_s": 0.9,
    }


DEMO_FINAL = """> ## ⚠️ VERDICT: 🔴 Scam pattern match — High confidence *(snap)*
> **Basis:** S-E1 sender-identity failure (@-domain usps-delivery-fee[.]net ≠ usps.com) + S-E3 carrier fee-by-link; T-0504 order-linked carrier smishing, observed directly in the email. Documentation pass confirmed the pattern is agency-documented.

**Basis (one paragraph).** The email's own headers settle it: it claims to be
USPS while sending from a domain that is not usps.com, and it invoices a $1.99
"redelivery fee" through an external payment link — real carriers never invoice
small fees by link. The documentation pass confirmed this is the agency-
documented T-0504 smishing wave (USPIS + FTC alerts), with nothing subject-
specific beyond the pattern class, exactly as expected for disposable
infrastructure.

**Final gauge.** 🔴 exhausted across all applicable lines — further stages
would surface repeats of the pattern documentation, not new decision-relevant
evidence.

---

## Subject profile

Suspicious email, claimed sender "USPS Package Services"
<no-reply@usps-delivery-fee[.]net>, subject "Your package is on hold — action
required within 48 hours", dated 2026-09-20. Ask: pay $1.99 redelivery fee via
link. Region: US.

## Evidence by check line

### C3 Domain & identity forensics — 🔴
- Sender domain is not a USPS property; reply-to diverges to the same
  throwaway domain. *(Observed directly — S-E1, [Decisive].)*
- Fee-by-link invoicing for a carrier. *(S-E3, [Decisive]; T-0504.)*

### C1 Advisory portals — 🚩 (pattern-level)
- USPIS and FTC alerts document the redelivery-fee smishing wave.
  *(Documentation pass, [Documented].)*

### C9 Community — 🚩 (pattern-level)
- Victim reports of the identical $1.99/$2.99 lure, seasonal. *[Reported]*

## Red flags → technique mapping

T-0504 order-linked carrier smishing (near-diagnostic) · T-0302 brand
impersonation applied to email (brand-clone confirmation).

## Recommended actions

- Do not click, reply, or call. Track parcels only at usps.com or the official app.
- Report: USPIS (uspis.gov/report) and FTC (reportfraud.ftc.gov). If you paid:
  call the number on your card immediately; see the recovery ladder below.

## If victim: recovery ladder

Card issuer (number on card) → bank dispute if ACH/debit → report to FTC/IC3/USPIS →
watch for recovery-fraud follow-ups (nobody legitimate contacts victims first or
charges a fee to recover money).

## Where to report

USPIS · FTC reportfraud.ftc.gov · FBI IC3 ic3.gov · delete the message.

## Gaps & caveats

No subject-specific enforcement record exists for this exact domain — consistent
with hit-and-run infrastructure; its absence is not evidence about any other
domain. This check examined the supplied email only.

## Sources

1. USPIS scam alerts — uspis.gov (accessed 2026-09-20)
2. FTC imposter-scam guidance — consumer.ftc.gov (accessed 2026-09-20)

<!--AGENTMETA
{"stage_label": "Consolidated", "snap": false, "verdict_band": "🔴", "verdict": "Scam pattern match", "confidence": "High", "label": "final", "overall_gauge": "🔴 exhausted", "recommend": "consolidate"}
-->"""
