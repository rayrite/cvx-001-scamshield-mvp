# Verdict Rubric — deception-record bands, balance readouts, and honesty rules

The verdict answers the user's actual question: **what does this company's documented record support?** It is computed from observed evidence, never vibes, and it always ships as a **pair**: the *band* (what the adverse record shows) and the *balance readout* (which way the total picture — adverse and positive — leans). A 🔴-band company with a strong remediation record and a 🟢-band company with no history at all are different verdicts with the same band; the balance readout is what keeps them honest. Coverage rides along: a band from four unchecked lines is worth nothing.

## The two readouts (+ coverage)

| Readout | Question it answers | Scale |
|---|---|---|
| **Deception-record band** (headline) | What adverse conduct is *documented*? | 🟢🟡🟠🔴 + confidence High/Medium/Low |
| **Balance readout** | Weighing documented adverse against documented positive, which way does the total picture lean? | Adverse-leaning / Mixed / Favorable + one-line basis |
| **Coverage** | How much of the check surface backs those? | Per-line: ⚪🔵🚩🔴➖ |

A verdict without its balance line or its coverage map is invalid. Stage-1 verdicts are labeled *provisional*; register previews keep their `register` label; impersonation snaps keep `snap`.

## Band anchors — anchored, not felt

### 🔴 Documented deception record · 75–100
**Any one** of:
- An **adjudicated finding** (court or fully litigated agency decision) establishing deceptive conduct, tier 1–3 source, naming the entity or its subsidiary/brand, **or**
- A **formal resolution with relief** (agency consent order or settlement with monetary/redress terms; well-documented class settlement) — label no-admission where it applies, **or**
- A criminal conviction for consumer-facing fraud.

The band means *the record documents resolved deception* — not "bad company." The balance readout carries remediation and positives.

### 🟠 Documented concerns · 50–74
**Any** of:
- **Formal charges pending** (agency complaint, AG suit, major litigation unresolved as of today), **or**
- **Documented patterns without enforcement** (reputable investigation with primary artifacts — T4), **or**
- **≥2 independent documented issues** (e.g., a settled matter plus a separate pending one) short of a single adjudicated deception.

### 🟡 Consumer-friction signals · 25–49
**Any** of:
- Complaint-board **patterns** (specific, consistent, dated failure modes) without any tier 1–4 documentation, **or**
- Exactly **one soft signal** (single review oddity, one pending individual suit, mild pricing gripe), **or**
- **Gray-zone conduct** (disclosed fees, unpopular-but-honest policies — see the register's gray-zone list), **or**
- **Unverifiable subject**: thin record, private company with minimal paper trail — record absence, not safety, **or**
- **Contradictory record**: credible praise and credible friction in similar weight.

### 🟢 No adverse documented record · 0–24
**All** of:
- Every applicable line ran (or the unchecked ones are listed) and found **no adverse documented record**, **and**
- The entity has verifiable history (established presence, coherent identity), **and**
- **Some positive record exists** (C8 found something real).

The honest ceiling: phrase as **"no adverse documented record found across N checks"** — never "trustworthy," never "clean." Thin-history subjects floor at 🟡 unverifiable, never 🟢.

## Register previews (Stage ½)

A register hit renders a *preview* band — T1/T2 row → 🔴 zone · T3/T4 row → 🟠 zone — labeled `register (KB cutoff 2026-09-19)` and paired with the not-current-status caveat. The preview is **not** one of the anchors above and cannot stand as a final verdict; Stage 1+ converts it into a real band by verifying current status at tier 1–3 (or showing movement: dismissed, vacated, remediated — displayed as verdict history with the cause named). A register **miss** never renders a band at all — it renders "absence ≠ clean."

## Balance readout rules

- **Requires C8 swept.** No balance line may be rendered while C8 is ⚪. If Stage 1 truly could not reach C8, the readout reads `Balance: not yet assessable — C8 unchecked` and that is a gap, loudly stated.
- **Adverse-leaning** requires a documented adverse basis (🟠 band or worse, or a 🟡 pattern with real specificity). Friction noise alone never leans the readout adverse.
- **Favorable** requires no 🚩/🔴 *documented* lines — normal at-scale friction is compatible with Favorable.
- **Mixed** is the honest center: documented adverse + documented positive, or an adverse record with credible remediation.
- The one-line basis names both sides' strongest evidence: `Mixed — CFPB consent order (2025) on cancellation; post-order flow redesigned, complaint arc improving 2026`.
- Balance never discounts a band and never inflates one — they are separate readouts by design.

## Confidence

| Tag | Requires |
|---|---|
| **High** | Tier 1–3 documentation verified current, OR an impersonation tell observed directly |
| **Medium** | Single credible source, or strong signal cluster awaiting verification |
| **Low** | Community-only evidence, single anecdote, mostly inference, or stale register-only basis |

## Aggregation procedure

1. Score each **flagged line** against the anchors; each 🚩/🔴 line names its signals and DP-IDs.
2. Overall band = the **highest band triggered** by any single line's anchor. Never escalate "on balance" — balance moves the *readout*, not the band.
3. Attach the confidence of the strongest evidence; stale or unverified evidence caps at Medium.
4. Write the one-line justification naming the evidence: `🔴 High — CFPB consent order 2025 (cancellation practices, $M redress) verified current at ftc.gov; maps DP-SUB-10`. **A verdict without a named-evidence justification is invalid.**
5. Compute the balance readout per its rules, naming both sides.
6. Downgrade/hold rules: complaint volume alone caps at 🟡 · gray-zone-only caps at 🟡 · thin-history floors at 🟡 · dismissed/vacated matters do not anchor 🔴 (record the movement).

## Honest-verdict rules (anti-gaming)

- Never render 🔴 to seem damning; never render 🟢 to seem reassuring. Both are auditable against the findings index.
- **Absence is not verification**; "no adverse documented record found" is a statement about the record search, not the company's virtue. Say it exactly that way.
- **No defamation beyond evidence**: findings describe what was observed and documented; "deception"/"fraud" attach to documented and adjudicated matters; allegations are labeled allegations; inferred clusters are `[Inferred]`.
- **Settlements are not findings of wrongdoing** — no-admission clauses are stated; consent orders are resolutions, not confessions.
- **Company-size fairness**: complaints and enforcement scale with customer base and prominence. The register itself warns it maps enforcement, not incidence. Normalize before pattern-calling.
- **Both sides, always**: praise-only reports and rap-sheet-only reports are equal violations of this rubric. Contradictions are surfaced, weighed by tier and specificity, and reflected in confidence.
- **Remediation currency**: date-check every adverse finding — a 2019 order and a 2026 order are different evidence; a redesigned flow after an order changes the balance readout, not the historical band.
- A verdict changed between stages displays its history (`Stage 1: 🟠 provisional → Stage 2: 🔴 confirmed — consent order fetched`); so does a register preview corrected by current sources (`Stage ½: 🟠 register → Stage 1: 🔴 confirmed current` or `→ 🟡 matter dismissed 2026-04, cause named`). The movement is information.

## Coverage map (rendered every stage, with legend)

```markdown
## Coverage Map — after Stage 1

| Line | Status | What was checked / found |
|---|---|---|
| C1 Identity & ownership | 🔵 clean | Confirmed: Sirius XM Holdings, NYC; no unresolved rename/lineage issues |
| C2 Regulator record | 🔴 hit | CFPB consent order + NY AG settlement (2024/25) — verified current at agency pages |
| C3 Litigation | 🚩 flagged | Class tracker lead (corroboration pending) — not yet primary-verified |
| C5 Complaints | 🚩 flagged | BBB profile: cancellation-friction arc, improving 2026 |
| C8 Positives | 🔵 clean | Content-service reputation, post-order cancellation redesign coverage |

Legend: ⚪ unchecked · 🔵 checked, clean · 🚩 checked, flagged · 🔴 checked, hit · ➖ not applicable.
Unchecked applicable lines = verdict coverage gap, listed in Gaps & Caveats.
```

Register-preview stage (½) replaces the table with: `Register: hit on <Company> (T2, DP-SUB-10) · research coverage not yet run.` Snap verdicts: `Smoke test: C-W1 [Decisive] — domain is not <brand>.com; research coverage not run.`

## Verdict box (rendered every stage, first thing the user reads)

```markdown
> ## ⚠️ VERDICT: 🔴 Documented deception record — High confidence *(provisional, Stage 1)*
> **Basis:** CFPB consent order + NY AG settlement (2024/25) on cancellation practices → DP-SUB-10 service doom loops; verified current at agency pages.
> **Balance:** Mixed — documented cancellation record vs. post-order redesign and improving 2026 complaint arc.
> **For you:** if subscribing, know the cancellation flow's documented history and current state before you commit.
```

Register-preview variant:

```markdown
> ## 📋 REGISTER PREVIEW: 🟠 zone — T4 documented record *(register, as of KB cutoff 2026-09-19)*
> **Basis:** Tide row: DP-QTY-03 serving-count manipulation — documented, no enforcement.
> **Caveat:** preview only — current status, remediation, and positives unchecked until Stage 1.
```

Snap variant:

```markdown
> ## ⚠️ VERDICT: 🔴 Not <Company>'s real site — High confidence *(snap, Stage ½ — zero searches)*
> **Basis:** C-W1 — <domain> contains the major brand's name but is not <official domain>.
> **Do/don't:** type the official domain yourself · never pay/log in via the link · report it.
```

Rules: emoji + band + confidence + label in the header; one-line basis with line/DP refs; balance line always (except snap, where there is no company record to balance — it's about the site); one actionable line.

## Next-stage plan template (rendered last, followed by the command hint)

```markdown
NEXT STAGE (default, awaiting approval)
  1. [C3] Verify the class-action lead at docket/settlement-admin level (2 searches, 1–2 fetches)
  2. [C5] Pull BBB complaint arc + dates; read recent Trustpilot one-stars for specificity (2 fetches)
  3. [C8] Consumer Reports / JD Power standings + post-order remediation coverage (2 searches)
  Est. budget: 4–5 searches, 4–5 fetches. Firms C3, completes balance evidence.

Reply "go" to run this plan · describe a different direction to customize · "stop" to consolidate the final report.
```

Plan rules: 2–4 target lines; ordered by **relevance × yield** per the ripeness gauge (`references/ripeness-rubric.md`), naming each target line's gauge score; actions concrete (named fetch or query, never "research more"); budget stated; if all applicable lines are 🔵/➖ with a stable verdict, or the overall gauge reads 🟠/🔴, the plan is replaced by a consolidation recommendation (at most one targeted option offered).

## Ledger formats (report-file appendices)

**A. Query log** — `| # | Stage | Line | Query | Notable results |` — check before every new query.

**B. Findings index** — `| ID | Finding (one line) | Source | URL | Date | Line | DP-ID | Confidence | Corroborated by |` — repeats attach as corroboration to the existing ID, never a second row. Confidence: `[Documented]` tier 1–4 record · `[Reported]` consumer complaint/review (count if multiple) · `[Reported — status unverified]` tracker/snippet litigation or enforcement *status* pending primary verification (mandatory for Stage-1 status findings — stale tracker pages present closed matters as live) · `[Inferred]` signal-cluster match, no external record. Register rows enter at Stage ½ as `[Documented — register, KB cutoff 2026-09-19]`; smoke observations enter with source "user-supplied material (static observation)".

**C. Lead pool** — `| ID | Line | Lead (URL/docket/thread) | Why promising | Tier est. | Added (stage) | Status (open/fetched/dead-end) |`.

**D. Verdict history** — `| Stage | Verdict | Balance | Confidence | Trigger/justification |` — the audit trail for verdict movement; a register preview's row is Stage ½; a snap's row is Stage ½ with basis "smoke".

## Worked micro-examples

1. **Register preview, correctly bounded.** "Check on Adobe." Stage ½: register hit — DP-SUB-05, T2, $150M settlement (2024/25). Preview: 🔴 zone *(register)* + caveat; fast path targets current settlement status + C8. The preview does **not** say "Adobe is deceptive" — it says the register documents a resolved matter, pending current verification and balance.
2. **Impersonation snap.** Supplied URL `adobe-creative-billing[.]net`. C-W1 fires (major brand, domain ≠ adobe.com). Final: 🔴 High *(snap)* — not Adobe's site; do/don't + report path. Zero searches; `document` offered.
3. **Clean sweep, honest ceiling.** Mid-size reputable company, no register row, Stage 1: C2/C3/C9 clean, C5 normal friction, C8 real positives. `🟢 no adverse documented record found across 7 checks — Medium-High · Balance: Favorable (normal at-scale friction)`. Never "verified trustworthy."
4. **Balance prevents the hit job.** Company with one 2019 settled matter, complete remediation program, improving arc, top expert ratings. Band: 🔴 (the anchor is met — the record documents resolved deception). Balance: Mixed, naming both. The pair *is* the honest verdict; neither readout may silently absorb the other.
5. **Register corrected by current sources.** Register preview 🟠 (pending FTC action, T3). Stage 1 finds the action dismissed (2026-04, named). Verdict history: `Stage ½: 🟠 register → Stage 1: 🟡 — matter dismissed; friction arc remains`. Movement shown, cause named.
6. **No snap pressure.** Unfamiliar small company, no URL. Smoke resolves identity in one search; register miss → "absence ≠ clean" → Stage 1 runs the sweep. The smoke test existing is not a reason to conclude anything.
