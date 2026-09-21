# Design: `rdw-scamshield-tea2-corpcheck`

Staged company background check with a fast smoke test. Designed 2026-09-19, combining three existing skills and one research knowledge base:

- **rdw-scamshield-check-v2** — the architecture donor: Stage ½ smoke test → Stage 1 triage → gated verify stages → consolidate; check lines, coverage map, verdict rubric, research ledger, gate protocol, safety rules.
- **rdw-product-dig** — the staging discipline donor: date-anchored intake, ledger discipline, date-precision timeline ladder on consolidation.
- **rdw-mega-product-profile** — the balance donor: the positive workstreams (awards, trust standings, parent-company lineage, price history table, per-section confidence tags) that keep a background check from becoming a hit job.

## Baseline failure (why this skill exists)

No prior live test — the baseline is the family-documented failure mode plus one new failure class specific to company checks:

1. **Inherited from the family** (scamshield DESIGN.md, product-dig intro): a single-pass "seems reputable" that misses the consent order, the pending class action, or the shrinkflation investigation — or an unprompted exhaustive dossier the user never asked to pay for.
2. **New — the bias failure**: company research tends one-sided in whichever direction the first strong finding points: a rap sheet that buries documented positives, or a puff piece built from the company's own marketing. The user explicitly required balanced reporting with citations.

## Research basis (2026-09-19)

The **US consumer dark-patterns knowledge base** (`research-us-consumer-dark-patterns-2026-09`, cutoff 2026-09-19): 73 patterns across 14 families with stable `DP-xxx-nn` IDs; a 63-company case-study register with pattern IDs and T1–T4 evidence tiers; a statute/agency-to-pattern crosswalk; and built-in balanced-reporting rules (allegations ≠ findings, no-admission labels, "enforcement maps attention, not incidence"). This is the exact analog of scamshield's technique catalog — it gives company findings a documented pattern vocabulary instead of vibes.

## Key decisions

1. **Smoke test = identity + authenticity + register (≤2 network calls).** Scamshield's smoke test reads *supplied material*; a company check's "material" is the entity itself. The three things knowable in seconds: who the entity is (product → parent chain), whether a supplied URL is really theirs (brand-clone tells, major-brand knowledge, FP guards), and whether the company is in the documented register. Anything needing more falls through to Stage 1.
2. **Two snap classes, deliberately different.** An impersonation tell is **final** (the domain settles it — same logic as scamshield's S-W1). A register hit is only a **preview**: the register is cutoff-dated, records no positives, and cannot show remediation — so it renders a labeled band + fast-path plan, never a verdict. This was an explicit design choice over scamshield-style final snaps: companies remediate, and balance requires evidence the register doesn't carry.
3. **Balance is structural, not aspirational.** C8 (positives) is swept in every Stage 1; the verdict box carries a mandatory **balance readout** (Adverse-leaning/Mixed/Favorable) with named evidence on both sides; aggregation forbids band escalation "on balance" and forbids balance discounting a band — the two readouts are separate by design (a 🔴 record with full remediation renders 🔴 + Mixed, and that pair is the honest verdict).
4. **Bands anchored to the KB's evidence tiers.** 🔴 = adjudicated or formally resolved deception (T1–T2 territory, tier 1–3 sources) · 🟠 = pending charges or documented-without-enforcement patterns (T3–T4) · 🟡 = friction signals / gray zone / unverifiable · 🟢 = no adverse documented record found (never "verified trustworthy"). Complaint volume alone caps at 🟡 — volume scales with customer base.
5. **Distilled register, not the live KB.** The 63-company register + 73-pattern index + tier rules + lookup rules live in `references/corp-register.md` (~150 lines) so the skill is portable from any working directory. Every preview cites the KB cutoff (2026-09-19) — the register is explicitly a preview, never a verdict.
6. **Check lines (10)** map the user's requested coverage: complaints (C5), price history (C7), scandals (C6), controversies (C6), litigation incl. class actions (C3), dark patterns (C4), authenticity (smoke test + C1), plus regulator record (C2), privacy (C9), sector overlay (C10), and the balance line (C8). Mega-profile workstreams that aren't background-check evidence (nicknames, product-line variations) were dropped — YAGNI.
7. **Ripeness & relevance gauge (v1.1, ported from rdw-product-dig).** The go/stop gate needs a priced menu, not just a verdict: per check line, score the marginal yield of one more stage (🟢–🔴, 0–100) from ledger signals — novelty rate, lead-pool depth, tier-ceiling gap — and rate each line's relevance to the user's angle. Adaptations from the donor: veins → check lines; a clean line is exhausted *by completion* (confirmed absence scores 🔴, never 🟢 without named leads); C8's Stage-1 mandate is separate from its yield relevance; overall 🟠/🔴 replaces the next-stage plan with a consolidation recommendation, formalizing the gate's push-back rule; gauge history rides as ledger Appendix E. The gauge is kept strictly separate from the verdict — yield prices *more research*, the band describes *the record*.

## Files

| File | Contents |
|---|---|
| `SKILL.md` | Staged procedure (Steps 1–16), check lines, safety rules (balanced-reporting mandate first), inputs, output contract, source hierarchy, failure handling, 4 examples |
| `references/corp-register.md` | **New** — lookup rules, tier table, the 63-company register (distilled verbatim), 73-pattern quick index by family, gray-zone list |
| `references/smoke-test.md` | **New** — rules (≤2 network calls), outcomes, snap/preview response shapes, identity items (C-I1–I3), website-authenticity items (C-W1–W4) with FP guards, register-lookup procedure |
| `references/check-line-guides.md` | **New** — per-line purpose/queries/hits/pitfalls for C1–C10, with the C10 sector-overlay table |
| `references/verdict-rubric.md` | **New** — band anchors, register-preview bands, balance-readout rules, confidence, aggregation, honest-verdict rules, coverage map, verdict-box variants, plan template, ledger formats, 6 worked examples |
| `references/ripeness-rubric.md` | **New (v1.1)** — ripeness/relevance gauge ported from rdw-product-dig: three components (richness/yield/relevance), band anchors from ledger signals, relevance defaults by user angle, clean-line shortcut, overall aggregation, output + Appendix E formats, worked examples |

## Testing notes

- **RED (baseline):** inherited family failure (documented above) — single-pass vs. exhaustive-dossier, plus the one-sided-report failure class. No new live baseline was run before building (v1 creation, family pattern).
- **GREEN (fact-based subagent tests, scamshield-v2 DESIGN.md pattern):**
  1. Register-hit subject (SiriusXM) → expect: identity + register preview labeled `register`, DP-SUB-10, T2→🔴-zone preview, not-current-status caveat, fast-path plan including C8; **no** final verdict.
  2. Impersonation URL (`<major-brand>-billing.net`-class) → expect: final snap 🔴 `snap`, ~10 lines, do/don't, `document` offer, zero searches.
  3. Clean/unknown company → expect: register miss rendered as "absence ≠ clean", fall-through to Stage 1 sweep, C8 swept, honest-ceiling phrasing.
  4. Negative test: a company **not** in the register must never receive an adverse snap/preview; a similar-name non-match must not fire the register (lookup rule 1).
- **Regression targets from the family:** gate compliance (no re-asking on `go`), ledger discipline (no re-run queries), coverage-map honesty, passive-only website inspection, no fabricated actions/dockets/dates.
- **Live A/B:** the user tries the skill on a real company (a register company, a clean favorite, and a product→parent case) and compares against an unskilled single-pass run.

## v1.1 changes (2026-09-19, after the first live run)

Live run: **Planet Fitness, Inc.** — register miss → Stage 1 → 2 → 3 → consolidated; 23 queries, 2 fetches (one 403). Evidence and motivated changes:

1. **C3 Stage-1 status tagging** — Stage 1 recorded *Truglio* as "pending" from an undated tracker snippet; Stage 2 found it dismissed in 2018 (360 F. Supp. 3d 274). The design recovered exactly as intended, but only because a verify stage was bought. Fix: tracker/snippet litigation or enforcement *status* is recorded `[Reported — status unverified]` at Stage 1 by construction (check-line-guides C3 pitfall + verdict-rubric ledger tag).
2. **Failure handling: corrupted search output** — one Stage-3 query returned garbled text mid-result; handled correctly ad hoc (clean source-attributed results only), now codified as a rule.
3. **Failure handling: Wayback fallback for bot-walled official sites** — planetfitness.com 403'd, leaving the Reuters-vs-official online-cancellation contradiction permanently unresolved; one labeled archive fetch is now permitted as a secondary source.
4. **Ripeness & relevance gauge ported from rdw-product-dig** (user-requested after noticing its absence) — key decision 7.

GREEN evidence from the run: register-miss fall-through with "absence ≠ clean" and no adverse snap on a non-register company; two verification corrections both *in the subject's favor* (anti-hit-job convergence — the process corrected toward accuracy, not toward severity); band/balance separation held across all four verdict renders; gray zones never mapped to DP-IDs; ledger discipline (23 unique queries, repeats absorbed as corroboration); gate compliance (no re-asking on `go`; novelty exhaustion correctly produced a consolidation recommendation instead of a Stage 4 — the behavior the gauge port now formalizes); consolidation contract (standalone file, date-precision ladder including "Date uncertain").

Still untested live: register-hit snap preview + fast path (SiriusXM-class) · impersonation snap on a supplied URL · product→parent resolution (Tide→P&G-class) · subagent-parallel verify stages · the new gauge itself (first exercised on the next live run).

## v1.2 changes (2026-09-19) — output modes

**Trigger:** user requirement — the staged-research skills roll into a ChatGPT-style app where an end-user prompt triggers research; the app needs each stage's full content printable to chat (not just highlights), the end user gets the choice, and the backend developer must flip the default on demand (file for a debugging session, chat for production) without editing skill prose. Applied family-wide the same day (rdw-product-dig, rdw-scamshield-check-v2, rdw-scamshield-recall-check-v2).

8. **Three modes, one knob.** `file` (default — current behavior untouched) · `chat` (complete stage content prints to the chat response; no report file unless requested) · `both` (chat content + file maintained). "Full stage content" is defined once in the output contract: banner, *every* finding with full citation including DP-ID mapping (no 3–6 cap), verdict box with balance readout, coverage map, gauge with legend, the stage's **ledger delta** (not a cumulative ledger reprint), the plan. Consolidation in `chat`/`both` delivers the full final dossier to chat.
9. **Three precedence levels.** In-chat user choice (any time, sticks, noted in report meta) > `corpcheck.config.json` (`"output_mode"`; absent file = `file`) > the default baked into SKILL.md's Inputs bullet — itself a developer lever: embed the prompt in the app and edit that one line to flip the default. Generalizes recall-check's `overview_map` config precedent.
10. **Snap verdicts and register previews are exempt** — they are already complete responses with nothing hidden to expand. The `document` pass follows the active mode.
11. **The `chat` trade-off is named:** no file = no ledger to resume from after a session break. Surfaced at intake and in failure handling; `both` is the resume-safe option.

Files changed: `SKILL.md` (key-concepts output-mode bullet; Inputs output-mode bullet; steps 9/10 chat-mode file skip + full-content Stage-1 response; step 15 chat-mode stage close; step 16 full final report in chat; output contract file-scoped "never paste" rule + Output modes block with config schema; failure handling chat-mode session-restart caveat) and this section. Unchanged: all references, register, smoke test, rubrics, safety rules. No config file shipped — the developer writes `corpcheck.config.json` into the working directory when a non-default mode is wanted.

Untested live — first exercised at app integration or on the next check. Regression targets: snap/register-preview responses unchanged in every mode; chat-mode full content must not truncate the verdict box, coverage map, or gauge; balance readout survives into chat-mode rendering.
