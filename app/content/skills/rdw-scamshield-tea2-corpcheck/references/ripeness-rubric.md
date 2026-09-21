# Ripeness & Relevance Gauge — pricing the next stage, honestly

The gauge answers one question: **will another verify stage surface new decision-relevant evidence not already in the findings index?** Search results behave like result pages: pages 1–2 hold the quality sources; by pages 5–6 you're reading repeats, press re-reporting press, and slop. The gauge tells the user — per check line, and overall — which page of the check they're on, so the go/stop gate is a priced decision, not a vibe. Ported from rdw-product-dig's ripeness rubric, adapted from product veins to check lines and this skill's evidence tiers.

## The three components

Every line row shows three components. The **headline** is the composite color + score; the other columns explain it.

| Component | Question it answers | Scale |
|---|---|---|
| **Richness** | How much quality evidence *exists* in this line? (recorded + confirmed-unfetched) | 0–100 |
| **Marginal yield** (headline) | How much *new* decision-relevant evidence would one more stage surface? | 🟢🟡🟠🔴 + 0–100 |
| **Relevance** | How much does this line matter to *this user's angle*? | High / Medium / Low |

Richness ≠ yield. A rich line can be fully harvested (richness 85, yield 🔴 15 — the classic mega-company C3 where every suit is already recorded). A modest line can still be fresh (richness 40, yield 🟢 80). The headline tracks **yield**: the user is buying the next stage, not admiring the last one.

## Relevance defaults by angle

Set at Stage 1 from the user's stated angle; revise only when the user redirects. Never inflate a convenient line to High to justify a stage.

| Angle | High | Medium | Low |
|---|---|---|---|
| Pre-purchase / subscription decision | C4, C5, C7 | C2, C3, C9 | C1, C6, C10 |
| Already a customer with a problem | C4, C5 | C3, C9 | C1, C2, C6, C7, C10 |
| Due diligence / research / writing | C2, C3, C4 | C5, C9 | C1, C6, C7, C10 |
| General curiosity (default) | C2, C3, C4 | C5, C7 | C1, C6, C9, C10 |

Overrides: C1 is High while a lineage question is open (rename, defunct, parent-chain doubt); C10 follows sector salience (a gym's AG-consumer-protection pool is salient; a sock brand's isn't). **C8's Stage-1 mandate is separate from this rating** — the balance sweep always runs; the relevance column only prices *further* C8 digging (usually Medium/Low).

## Color bands and observable anchors

Match the line's observable signals to these anchors; pick the band, then place the score within it. Bands carry the meaning; the numeric score is a communication device, not a measurement.

### 🟢 Fresh · 75–100 · "pages 1–2"
Any of:
- ≥3 concrete **unfetched leads** in the pool, at least one a **tier 1–3 primary** (a named docket, an agency order page, a settlement-administrator site), **or**
- A confirmed **tier-ceiling gap**: the best source type the hierarchy says should exist hasn't been reached, and evidence shows it exists (press covered the suit ⇒ a docket exists; coverage of a consent order ⇒ an agency page exists), **or**
- (Stage 2+) last stage's **novelty rate > 50%** with the lead pool still populated.

### 🟡 Yielding · 50–74 · "pages 2–3"
Any of:
- 1–2 concrete unfetched leads, or ≥3 leads all tier 4+ (press, advocacy, boards), **or**
- Tier 1–3 primaries largely in, but the complaint-arc / community / review-trajectory digging hasn't been done and the line's story clearly runs through it, **or**
- Last stage's novelty rate 25–50%.

### 🟠 Thinning · 25–49 · "pages 4–5"
All of:
- Tier 1–3 sources reached or confirmed absent; boards and advocacy substantially mined, **and**
- Last stage's novelty rate 10–25% — new results mostly corroborate or re-report known findings, **and**
- Remaining leads are niche corners only: deep pagination, non-English press, archival threads.

Dig only for a **specific named question**.

### 🔴 Exhausted · 0–24 · "pages 6+"
All of:
- Lead pool empty or reduced to dead-ends, **and**
- Last stage's novelty rate < 10%, **and**
- Fresh searches return repeats of harvested findings and/or slop (SEO farms, AI mills) dominating results.

Further stages are not justified — say so plainly and propose consolidation.

## The five signals

| Signal | How to measure | Notes |
|---|---|---|
| **Novelty rate** | new findings recorded ÷ searches executed on that line, this stage | Exists from Stage 2 on. Stage 1 has no baseline — its scores are **prospect estimates**, labeled as such in gauge history |
| **Lead-pool depth** | count of `open` leads for that line | ≥3 strong · 2–4 moderate · ≤1 weak. Leads must be **concrete** (URL, docket, agency page) — "more articles probably exist" is not a lead |
| **Tier-ceiling gap** | best tier harvested vs. best tier the source hierarchy says should exist for that finding type | The strongest gold-left signal. "Press covered the lawsuit" + "docket never pulled" = at least 🟡, whatever else is true |
| **Repeat rate** | share of results already covered by the findings index | Rising repeat rate across stages is the decay curve made visible |
| **Slop rate** | share of results from tier 8 | Never cited; counts only toward the exhaustion signal |

## Clean-line shortcut

A 🔵 line whose absence-check reached its proper tier is exhausted **by completion**: score 🔴 with the note "confirmed absence — harvest complete" (richness records how much absence-proof was gathered; it is not nothing). Never score a clean line 🟢 without named leads — "maybe an action exists" is not a lead, and absence of hits is already the finding.

## Scoring procedure

1. Gather the line's signals — they come free from the ledger.
2. Match to a band's anchors — conjunctive/disjunctive as written; when a line sits between bands, take the **lower** band (optimism bias is the failure mode this rubric exists to prevent).
3. Place the score within the band: top if the anchor conditions are exceeded, bottom if barely met.
4. Write a one-line justification naming the evidence ("🟡 62 — docket listings in; LP-appointment order unfetched (tier-2 gap); novelty 30%"). **A score without a named-evidence justification is invalid.**

## Overall gauge

Deterministic aggregation:

1. If any **High-relevance** line ≥ 50 (🟢/🟡): overall = the score of the highest-yielding High-relevance line.
2. Else if any **Medium-relevance** line ≥ 50: overall = that line's score − 15.
3. Else: overall = the lowest band present among remaining lines → recommend consolidation.

Render as one line: `OVERALL: 🟡 62/100 — targeted stage on C3 recommended (1 High-relevance line still yielding; C4 thinning).`

Recommendation mapping: 🟢 → next stage strongly recommended · 🟡 → targeted stage on the listed lines · 🟠 → only for a specific named question · 🔴 → stop, consolidate.

## Honest-scoring rules (anti-gaming)

- 🟢/🟡 **requires named leads or a named tier gap.** An empty lead pool cannot justify green or yellow, no matter how the search "felt".
- Never score 🔴 to avoid work; never score 🟢 to seem thorough. Both are auditable against the ledger — that's the point of the ledger.
- Relevance comes from the user's actual angle, set at Stage 1 and revised only on redirect. On a custom-redirect stage, re-rate that stage's lines — the gauge serves *their* question, not the skill's convenience.
- Prospect estimates (Stage 1) may drop sharply once Stage 2 measures novelty. That's the system working, not a mistake — surface it in gauge history.
- The gauge never touches the verdict. Yield is about *more research*; the band is about *the record*. A 🔴-yield line can still be a 🚩 flagged line, and a 🟢-yield run can still end in a 🟢 verdict.

## Gauge output format (rendered every stage with the legend; not rendered at Stage ½ — research coverage not yet run)

```markdown
## Ripeness Gauge — after Stage 2

| Line | Richness | Yield (headline) | Relevance | Evidence |
|---|---|---|---|---|
| C3 Litigation | 80 | 🟡 62 | High | docket listings in; LP-appointment order unfetched (tier-2 gap); novelty 30% |
| C4 Dark patterns | 65 | 🟠 40 | High | official page 403'd; mechanics pinned via snippets ×3; 1 open lead; novelty 15% |
| C5 Complaints | 55 | 🟠 35 | Medium | BBB arc characterized; 1 marginal fetch left; novelty 10% |
| C2 Regulator | 30 | 🔴 15 | High | confirmed absence at agency-query level — clean by completion |

**OVERALL: 🟡 62/100** — targeted stage on C3 recommended (1 High-relevance line still yielding).

Legend: 🟢 75–100 fresh (pages 1–2 — new quality evidence confirmed waiting) · 🟡 50–74 yielding (pages 2–3 — targeted digging still pays) · 🟠 25–49 thinning (pages 4–5 — only named questions worth a dig) · 🔴 0–24 exhausted (pages 6+ — repeats and slop; stop).
```

## Plan integration

The next-stage plan (verdict-rubric template) is ordered by **relevance × yield** and names its target lines' gauge scores. When the overall gauge reads 🟠/🔴 — or every applicable line is 🔵/➖ with a stable verdict — the plan is replaced by a consolidation recommendation, with at most one targeted option offered. This formalizes the gate's push-back rule: `go` against a 🔴 overall gets exactly one evidence-backed push-back.

## Appendix E — Gauge history (report-file ledger)

The report body's gauge table is overwritten each stage; the history preserves the decay curve:

`| Line | S1 (prospect) | S2 | S3 | … | Trend note |`

Example row: `| C3 Litigation | 🟢 80* | 🟡 62 | 🟠 41 | docket + opinion pulled by S2; S3 mostly corroboration |` (*prospect estimate)

## Worked micro-examples

1. **Stage 1, litigation line, securities suit in the news.** Three firms' case pages + press coverage; no docket pulled. Signals: confirmed tier-ceiling gap (press ⇒ docket exists), 2 leads pooled, no novelty baseline. Score: 🟢 80 — anchor "confirmed tier-ceiling gap"; justification names the docket. Labeled prospect estimate.
2. **Stage 3, complaints line.** Last stage: 4 searches, 1 new finding (novelty 10%), 1 open lead (a BBB full-profile fetch rated marginal). Score: 🟠 28 — "primaries and boards substantially mined; niche corner only."
3. **Clean regulator line.** Agency-level queries came back empty; the sweep reached the tier the hierarchy demands for an absence claim. Score: 🔴 12 — "confirmed absence — harvest complete"; richness 30 (the absence-proof itself is the harvest).
