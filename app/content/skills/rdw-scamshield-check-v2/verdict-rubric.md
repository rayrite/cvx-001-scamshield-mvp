# Verdict Rubric — risk verdicts, coverage, and honesty rules

The verdict answers the user's actual question: **can I trust this?** It is computed from observed evidence, never vibes, and it is always paired with **coverage** (which checks were actually run) — a 🟢 from four unchecked lines is worth nothing and must never be rendered as reassurance.

## The two readouts

| Readout | Question it answers | Scale |
|---|---|---|
| **Risk verdict** (headline) | What does the evidence show about this subject? | 🟢🟡🟠🔴 + confidence High/Medium/Low |
| **Coverage** | How much of the applicable check surface backs that verdict? | Per-line: ⚪🔵🚩🔴➖ |

A verdict without its coverage map is invalid. The Stage-1 verdict is always labeled *provisional*; it firms up (or changes — say so plainly) as stages add evidence. The **snap verdict** (Stage ½) is the exception — see below.

## Verdict bands — anchored, not felt

### 🔴 Scam pattern match · 75–100
**Any one** of:
- A **near-diagnostic signal** (catalog §2, the five) observed directly in the subject's own content, **or**
- **Documented adverse record** at source tier 1–4 (regulator action/enforcement, BBB Scam Tracker or credible-press investigation naming this store/seller/domain, court/enforcement record), **or**
- **Brand-clone confirmation**: the subject's domain is provably not the impersonated brand's official domain *and* trades on that brand (T-0302), **or**
- **Multiple independent victim reports** (≥3 specific, dated, non-generic complaints across ≥2 platforms — e.g., Trustpilot one-stars + Reddit thread) describing the same failure mode.

### 🟠 Multiple red flags · 50–74
**All** of:
- A cluster of ≥2 **independent** signals from the catalog's signal library mapping to documented techniques (e.g., weeks-old domain + 80%-off brand pricing), **and**
- No near-diagnostic signal observed, and no tier 1–4 documentation naming the subject.

High-volume complaint boards with thin specifics may hold this band, not 🔴 — specificity is what separates them.

### 🟡 Caution · 25–49
**Any** of:
- Exactly **one** soft signal (single review oddity, mild price anomaly, thin-but-clean record), **or**
- A **gray-zone pattern** (catalog §9: dropship delays, disclosed replica, gray-market goods, disclosed fees) without fraud indicators, **or**
- **Unverifiable subject**: young store/seller, no transaction history, checks came back empty — record absence, not safety, **or**
- **Contradictory record**: credible praise and credible complaints in similar weight.

### 🟢 No adverse findings · 0–24
**All** of:
- Every applicable check line ran (or the unchecked ones are listed) and found nothing adverse, **and**
- No plausibility signals fired, **and**
- The subject has *some* verifiable history (established presence, coherent record).

The honest ceiling: phrase as **"no adverse findings across N checks"** — never "verified safe," never "legitimate." If the subject is young/thin, the verdict is 🟡 unverifiable, not 🟢.

## Snap verdicts (Stage ½ — zero-search)

A snap verdict is a 🔴 delivered **before any research**, when a decisive smoke-test item (`references/smoke-test.md`) fires on the material itself. It is not a new band — it is one of two existing 🔴 anchors reached without searching:

| Snap basis | Rubric anchor used |
|---|---|
| Smoke item labeled [Decisive] for a near-diagnostic ask (S-E2, S-W2, S-P2/P3, S-T1) | Near-diagnostic signal observed directly |
| Smoke item labeled [Decisive] for identity/brand failure (S-E1, S-E3, S-W1, S-P1) | Brand-clone confirmation / institution test violation |

**Label rules:** snap verdicts are labeled `snap`, not `provisional` — *provisional* means "a partial sweep might revise this"; a snap rests on a decisive tell observed directly, whose basis is complete at zero searches. Coverage for a snap is stated as "smoke test: <items fired>" rather than a C-line map (C-lines describe research coverage, which hasn't run).

**Documentation pass expectations:** `document` runs the Stage-1 sweep to *write up* the pattern, not to justify the band. Normal outcome: band unchanged, confidence wording gains named sources. Rare outcome: documentation contradicts the snap (e.g., the "random-string domain" turns out to be a documented legitimate sending pattern) — then show verdict movement explicitly per the honest-verdict rules below, and say what changed. A snap verdict that documentation overturns is a smoke-test false positive: record it and tighten the guard's wording in future checks.

**Anti-gaming:** the snap path must never be a shortcut to decisiveness. [Corroborating] items alone (S-E4/S-E5/S-E6, S-W3, S-T2) cannot snap — they go to Stage 1. An item whose FP guard says fall through (unknown brand, blocked images, plausible ESP pattern) has not fired.

## Confidence

| Tag | Requires |
|---|---|
| **High** | Tier 1–4 documentation, OR a near-diagnostic signal observed directly, OR ≥3 independent corroborants across platforms |
| **Medium** | One credible source, OR a strong signal cluster with no external documentation |
| **Low** | Community-only evidence, single anecdotal report, or mostly-inference |

Confidence is about the *evidence quality backing the band*, separate from the band itself: 🔴 Medium (near-diagnostic signal seen but user's screenshot is the only record) is a valid, honest state. A snap verdict is High: the decisive tell was observed directly (same rule as row 1).

## Aggregation procedure

1. Score each **flagged line** against the band anchors above; each 🚩/🔴 line names its signals and T-IDs.
2. The overall verdict = the **highest band triggered** by any single line or combination that meets an anchor. Combinations that meet no anchor alone stay at the band the anchors justify — never escalate "on balance."
3. Attach the confidence of the strongest contributing evidence.
4. Write the one-line justification naming the evidence: `🔴 High — near-diagnostic T-0407 (F&F discount ask) observed in seller messages; BBB page shows 11 non-delivery complaints since <month>`. **A verdict without a named-evidence justification is invalid.** Snap verdicts justify the same way, naming smoke items + T-IDs: `🔴 High (snap) — S-E1 sender-identity failure (domain ≠ usps.com) + S-E3 carrier fee-by-link; T-0504`.
5. Downgrade/hold rules: gray-zone-only evidence caps at 🟡 · single anecdotal complaint caps at 🟡 · new-but-clean subject floors at 🟡 (unverifiable), never 🟢 with no history.

## Honest-verdict rules (anti-gaming)

- Never render 🔴 to seem decisive; never render 🟢 to seem reassuring. Both are auditable against the findings index — that's the point of the ledger.
- **Absence is not verification**; "no adverse record found" is a statement about the record, not the subject. Say it exactly that way.
- **No defamation beyond evidence**: findings describe what was observed and documented; the words "scam"/"fraud" attach to documented patterns and reports, and inferred conclusions are labeled `[Inferred]`.
- Score clusters, not single signals — every false-positive guard in the guides exists because honest sellers trip single heuristics.
- When evidence contradicts (clean board + damning thread), show both, weight by source tier and specificity, and drop confidence accordingly.
- A verdict changed between stages is displayed with its history (`Stage 1: 🟠 provisional → Stage 2: 🔴 confirmed after BBB reports fetched`) — the movement is information. Same for a snap verdict overturned by documentation (`Stage ½: 🔴 snap → after documentation: 🔴 → 🟠 reversal, cause named`).

## Coverage map (rendered every stage, with legend)

```markdown
## Coverage Map — after Stage 2

| Line | Status | What was checked / found |
|---|---|---|
| C1 Advisory portals | 🔴 hit | BBB Scam Tracker: 4 reports naming this domain (2026-03…2026-08) |
| C2 Review boards | 🚩 flagged | Trustpilot 2.1★ — 11 one-stars, all "never arrived", Feb–Aug 2026 |
| C3 Domain forensics | 🔴 hit | WHOIS: registered 2026-07-12 (22 days ago); no contact info on site |
| C6 Price plausibility | 🚩 flagged | 75% under brand MSRP across all listings |
| C7 Payment behavior | 🔵 clean | Card checkout only; no off-platform asks observed |
| C9 Community | 🔵 clean | No Reddit/forum threads found |
| C4/C5/C8/C10 | ➖ | Not applicable (no marketplace listing, no product focus) |

Legend: ⚪ unchecked · 🔵 checked, clean · 🚩 checked, flagged · 🔴 checked, hit · ➖ not applicable.
Unchecked applicable lines = verdict coverage gap, listed in Gaps & Caveats.
```

Snap verdicts replace the table with one line — `Smoke test: S-E1 [Decisive] + S-E4/S-E5 corroborating fired; research coverage not run (offered via "document")` — because research coverage does not exist yet and must not be implied.

## Verdict box (rendered every stage, first thing the user reads)

```markdown
> ## ⚠️ VERDICT: 🟠 Multiple red flags — Medium confidence *(provisional, Stage 1)*
> **Basis:** domain 19 days old (C3) + 80%-off brand pricing (C6) + no contact info (C3) → T-0301 disposable-storefront pattern. No scam-database hits yet (C1 clean so far).
> **If you're about to buy:** don't — not until Stage 2 confirms or clears. If you already paid: see Recovery Ladder.
```

Snap variant:

```markdown
> ## ⚠️ VERDICT: 🔴 Scam pattern match — High confidence *(snap, Stage ½ — zero searches)*
> **Basis:** S-E1 sender-identity failure (display name "USPS", @-domain usps-fee[.]net ≠ usps.com) + S-E3 carrier fee-by-link (T-0504) — both observed in the email itself.
> **Do/don't:** don't click/reply; track only at usps.com; report to USPIS + FTC.
```

Rules: emoji + band + confidence + provisional/snap marker in the header line; one-line basis with check-line or smoke-item refs; one actionable line. The box is identical in chat and the file. Final (consolidated) verdict drops the provisional marker; a snap verdict keeps its `snap` label (it names its basis, not its tentativeness).

## Next-stage plan template (rendered last, followed by the command hint)

```markdown
NEXT STAGE (default, awaiting approval)
  1. [C1] Fetch BBB Scam Tracker results + FTC/press sweep on `<name>` (1 search, 2 fetches)
  2. [C2] Pull Trustpilot 1-star reviews; check dates & specifics (1 fetch)
  3. [C3] WHOIS detail + contact-info reality check (1 fetch)
  Est. budget: 3–4 searches, 4–5 fetches. Targets the three flagged lines; upgrades 🟠 → firm verdict either way.

Reply "go" to run this plan · describe a different direction to customize · "stop" to finalize the background-check report.
```

After a snap verdict, the plan block is replaced by the documentation offer: `Say "document" for the full archived report (pattern documentation, sources, ledger) · describe a different direction to customize · "stop" to finish here.`

Plan rules: 2–4 target lines; ordered by **relevance × yield** per the ripeness gauge (`references/ripeness-rubric.md`), naming each target line's gauge score; actions concrete (named fetch or query, never "research more"); budget stated; if all applicable lines are 🔵/➖ with a stable verdict, or the overall gauge reads 🟠/🔴, the plan is replaced by a consolidation recommendation (at most one targeted option offered).

## Ledger formats (report-file appendices)

**A. Query log** — `| # | Stage | Line | Query | Notable results |` — check before every new query.

**B. Findings index** — `| ID | Finding (one line) | Source | URL | Date | Line | T-ID | Confidence | Corroborated by |` — repeats attach as corroboration to the existing ID, never a second row. Confidence: `[Documented]` tier 1–4 record · `[Reported]` consumer complaint/review (count if multiple) · `[Inferred]` signal-cluster match, no external record. Smoke-test findings enter the index at documentation time with source "user-supplied material (static observation)".

**C. Lead pool** — `| ID | Line | Lead (URL/thread/docket) | Why promising | Tier est. | Added (stage) | Status (open/fetched/dead-end) |`.

**D. Verdict history** — `| Stage | Verdict | Confidence | Trigger/justification |` — the audit trail for verdict movement; a snap verdict's row is Stage ½.

**E. Gauge history** — `| Line | S1 (prospect) | S2 | S3 | … | Trend note |` — the ripeness decay curve per line (`references/ripeness-rubric.md`); the report body's gauge table is overwritten each stage, this preserves it.

## Worked micro-examples

1. **Stage ½, snap.** Email claims "McAfee" renewal; @-domain is a random string ≠ mcafee.com; reply-to on a newsletter ESP. S-E1 [Decisive] fires (major brand, provably not its domain); S-E4/S-E5 corroborate. Verdict: `🔴 High (snap) — S-E1 + corroborating S-E4/S-E5; T-0603/T-0302 class`. Zero searches; documentation offered, not run.
2. **Stage 1, store check.** Domain 3 weeks old, 80%-off brand goods, no contact info; no board hits yet. Signals: three independent → cluster anchor met; no documentation → not 🔴. Score: 🟠 Medium — "T-0301 pattern cluster; C1 still unchecked-partial, Stage 2 decides."
3. **Clean new seller.** Mercari seller, 2 months, 12 sales, no reviews, no complaints anywhere. No signals, but no history → unverifiable anchor. Score: 🟡 Medium — "no adverse findings across C1/C2/C9; young account, absence ≠ verification."
4. **Documented escalation.** Stage 2 fetches a BBB Scam Tracker page: 4 dated non-delivery reports naming the domain. Independent victim reports anchor → 🔴 High; verdict history records 🟠→🔴 and names the fetched page.
5. **Gray zone, correctly capped.** Store sells disclosed "inspired by" replicas, 6 months old, mixed reviews about slow shipping. Disclosed-replica + slow-dropship = gray-zone anchors only. Score: 🟡 Medium — capped there regardless of review grumbling; note platform-policy (not fraud) dimension.
6. **Smoke fall-through, no snap pressure.** Email from an unfamiliar small store about an order the user placed; body text generic. No major brand, no visible ask → no smoke item fires. Stage 1 runs; verdict from evidence. The smoke test existing is not a reason to snap.
