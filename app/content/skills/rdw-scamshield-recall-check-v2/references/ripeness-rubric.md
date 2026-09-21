# Ripeness & Relevance Gauge — pricing the next stage, honestly

The gauge answers one question: **will another verify stage surface new decision-relevant evidence not already in the findings index?** Search results behave like result pages: pages 1–2 hold the quality sources; by pages 5–6 you're reading aggregator repeats and slop. Recall research reaches that point *sooner* than reputation research, and that is fine: the recall record is a finite, dated, agency-held fact, not a diffuse opinion pool. The gauge tells the user — per check line, and overall — which page of the check they're on, so the go/stop gate is a priced decision, not a vibe. Ported from rdw-product-dig's ripeness rubric (via rdw-scamshield-tea2-corpcheck), adapted to R1–R8, this skill's source hierarchy, and its two verdict readouts.

## The three components

Every line row shows three components. The **headline** is the composite color + score; the other columns explain it.

| Component | Question it answers | Scale |
|---|---|---|
| **Richness** | How much quality evidence *exists* in this line? (recorded + confirmed-unfetched) | 0–100 |
| **Marginal yield** (headline) | How much *new* decision-relevant evidence would one more stage surface? | 🟢🟡🟠🔴 + 0–100 |
| **Relevance** | How much does this line matter to *this user's situation*? | High / Medium / Low |

Richness ≠ yield. A hit line can be fully harvested (R1 richness 85, yield 🔴 15 — the agency notice was fetched with its lots and remedy; there is nothing more R1 can add). A modest line can still be fresh (R4 richness 30, yield 🟢 80 — the state distribution pages haven't been touched). The headline tracks **yield**: the user is buying the next stage, not admiring the last one.

## Relevance defaults by situation and angle

Set at Stage 1 from the user's situation and angle; revise only when the user redirects. Never inflate a convenient line to High to justify a stage.

| Situation / angle | High | Medium | Low |
|---|---|---|---|
| Screening — is it recalled *now*? (default) | R1, R3 | R5, R6 | R2, R4, R7, R8 |
| Already owns / ate / used — is *mine* affected? | R1, R5, R4 | R3, R6 | R2, R7, R8 |
| Full history — past + current | R1, R2 | R6, R5 | R3, R4, R7, R8 |
| Outbreak concern — are people sick? | R3, R1 | R4, R6 | R2, R5, R7, R8 |
| Claim-bearing content — is this message/post/article real? | R7, R1 | R6, R8 | R2, R3, R4, R5 |

Notes: R7 is ➖ (not merely Low) for non-claim-bearing subjects — the authenticity readout doesn't exist for them. A `document` pass after an authenticity snap is a **screening** run by another door — it re-rates to that row, because its real job is answering the recall-status question. Victim-path runs (already paid a fake-recall message) re-rate toward documentation of the scam for the dispute.

## Color bands and observable anchors

Match the line's observable signals to these anchors; pick the band, then place the score within it. Bands carry the meaning; the numeric score is a communication device, not a measurement.

### 🟢 Fresh · 75–100 · "pages 1–2"
Any of:
- ≥3 concrete **unfetched leads** in the pool, at least one a **tier 1–2 primary** (the agency recall-notice page, the CDC investigation page), **or**
- A confirmed **tier-ceiling gap**: the best source type the hierarchy says should exist hasn't been reached, and evidence shows it exists (press and the retailer hub both describe the agency recall ⇒ the agency notice exists and is unfetched; states relay a distribution recall ⇒ a state page exists), **or**
- (Stage 2+) last stage's **novelty rate > 50%** with the lead pool still populated.

### 🟡 Yielding · 50–74 · "pages 2–3"
Any of:
- 1–2 concrete unfetched leads, or ≥3 leads all tier 3+ (state pages, press, retailer hubs), **or**
- Agency notice snippet-verified with date and class but not fetched in full, and the state/retailer layers haven't run, **or**
- Last stage's novelty rate 25–50%.

### 🟠 Thinning · 25–49 · "pages 4–5"
All of:
- Tier 1–2 sources fetched or confirmed absent; state/press/retailer layers substantially mined, **and**
- Last stage's novelty rate 10–25% — new results mostly corroborate or re-report known findings, **and**
- Remaining leads are niche corners only: trade-press deep pages, old outbreak-archive threads, secondary state lists.

Dig only for a **specific named question**.

### 🔴 Exhausted · 0–24 · "pages 6+"
All of:
- Lead pool empty or reduced to dead-ends, **and**
- Last stage's novelty rate < 10%, **and**
- Fresh searches return repeats of harvested findings and/or aggregator slop dominating results.

Further stages are not justified — say so plainly and propose consolidation.

## The five signals

| Signal | How to measure | Notes |
|---|---|---|
| **Novelty rate** | new findings recorded ÷ searches executed on that line, this stage | Exists from Stage 2 on. Stage 1 has no baseline — its scores are **prospect estimates**, labeled as such in gauge history |
| **Lead-pool depth** | count of `open` leads for that line | ≥3 strong · 2–4 moderate · ≤1 weak. Leads must be **concrete** (URL, agency page, state list) — "more coverage probably exists" is not a lead |
| **Tier-ceiling gap** | best tier harvested vs. best tier the hierarchy says should exist for that finding type | The strongest gold-left signal. "Press + retailer hub describe the recall" + "agency notice never pulled" = at least 🟡, whatever else is true |
| **Repeat rate** | share of results already covered by the findings index | Rising repeat rate across stages is the decay curve made visible |
| **Slop rate** | share of results from tier 8 (aggregator content farms) | Never cited; counts only toward the exhaustion signal — and recall SEO is where undated aggregator pages breed |

**Access-limited ceilings (this skill's special case):** an agency surface that is bot-walled to automated fetch (FSIS Akamai, NHTSA) and has been attempted per the documented protocol (source guide §3) does **not** count as open yield. It is a *reached-with-limitation* ceiling: the corroborating search extraction counts toward the harvest, and the line scores on that harvest. The "open it yourself" URL is a **user action** surfaced in recommended actions — never a stage, never agent yield, never a reason to keep the gauge green.

## Clean-line shortcut

A 🔵 line whose absence-check reached its proper tier is exhausted **by completion**: score 🔴 with the note "confirmed absence — harvest complete" (richness records how much absence-proof was gathered; it is not nothing). Never score a clean line 🟢 without named leads — "maybe a recall exists" is not a lead, and absence of a record is already the finding (reported as "no recall record found", never "safe"). **A hit can be exhausted too:** once the agency notice is fetched with its specifics (date, class, lots, remedy), R1 is exhausted by completion — exhaustion is about *further research*, not about the record being clean.

## When the gauge renders

Not on snap responses — no research has run, the authenticity verdict stands on direct observation, and recall status is explicitly "not checked". From the first Stage-1-shaped response on (the routed sweep, a fall-through, or a `document` pass), the gauge renders every stage. The overview map is unaffected: rendering is not research yield, is never scored, and never moves the gauge.

## Scoring procedure

1. Gather the line's signals — they come free from the ledger.
2. Match to a band's anchors — conjunctive/disjunctive as written; when a line sits between bands, take the **lower** band (optimism bias is the failure mode this rubric exists to prevent).
3. Place the score within the band: top if the anchor conditions are exceeded, bottom if barely met.
4. Write a one-line justification naming the evidence ("🟡 62 — agency notice snippet-verified 2026-08-12 Class II, full fetch pending (tier-1 gap); R4 state layer unrun; novelty 30%"). **A score without a named-evidence justification is invalid.**

## Overall gauge

Deterministic aggregation:

1. If any **High-relevance** line ≥ 50 (🟢/🟡): overall = the score of the highest-yielding High-relevance line.
2. Else if any **Medium-relevance** line ≥ 50: overall = that line's score − 15.
3. Else: overall = the lowest band present among remaining lines → recommend consolidation.

Render as one line: `OVERALL: 🟡 62/100 — targeted stage on R1/R4 recommended (notice fetch pending; state layer unrun).`

Recommendation mapping: 🟢 → next stage strongly recommended · 🟡 → targeted stage on the listed lines · 🟠 → only for a specific named question · 🔴 → stop, consolidate.

## Honest-scoring rules (anti-gaming)

- 🟢/🟡 **requires named leads or a named tier gap.** An empty lead pool cannot justify green or yellow, no matter how the search "felt".
- Never score 🔴 to avoid work; never score 🟢 to seem thorough. Both are auditable against the ledger — that's the point of the ledger.
- Relevance comes from the user's actual situation and angle, set at Stage 1 and revised only on redirect. On a custom-redirect stage, re-rate that stage's lines — the gauge serves *their* question, not the skill's convenience.
- Prospect estimates (Stage 1) may drop sharply once Stage 2 measures novelty. That's the system working, not a mistake — surface it in gauge history.
- The gauge never touches **either** verdict readout. R7's yield says nothing about the authenticity verdict; a fully exhausted R1 sitting under a 🔴 recall-status verdict is the system *working* — the finding is complete, not stale. Yield prices *more research*; the readouts describe *the record*.

## Gauge output format (rendered every stage with the legend; not on snap responses — research coverage not yet run)

```markdown
## Ripeness Gauge — after Stage 2

| Line | Richness | Yield (headline) | Relevance | Evidence |
|---|---|---|---|---|
| R1 Agency recall list | 85 | 🔴 18 | High | notice fetched — date/class/lots/remedy in hand; harvest complete |
| R4 State distribution | 35 | 🟡 55 | High | 2 state relays snippet-seen, unfetched; novelty 40% |
| R5 Retailer/manufacturer | 40 | 🟠 35 | Medium | hub lot-check done; 1 archived press lead; novelty 15% |
| R3 CDC outbreak | 20 | 🔴 12 | Medium | no investigation on record — confirmed absence at cdc.gov query level |

**OVERALL: 🟡 55/100** — targeted stage on R4 recommended (lot question runs through the state layer).

Legend: 🟢 75–100 fresh (pages 1–2 — new quality evidence confirmed waiting) · 🟡 50–74 yielding (pages 2–3 — targeted digging still pays) · 🟠 25–49 thinning (pages 4–5 — only named questions worth a dig) · 🔴 0–24 exhausted (pages 6+ — repeats and slop; stop).
```

## Plan integration

The next-stage plan (verdict-rubric template) is ordered by **relevance × yield** and names its target lines' gauge scores. When the overall gauge reads 🟠/🔴 — or coverage is already complete on all applicable lines — the plan is replaced by a consolidation recommendation, with at most one targeted option offered (the overview map, when enabled, still runs at consolidation — it is post-processing, not a stage). This formalizes the gate's push-back rule: `go` against a 🔴 overall gets exactly one evidence-backed push-back.

## Appendix E — Gauge history (report-file ledger)

The report body's gauge table is overwritten each stage; the history preserves the decay curve:

`| Line | S1 (prospect) | S2 | S3 | … | Trend note |`

Example row: `| R1 Agency list | 🟢 80* | 🔴 18 | — | notice fetched S2 with full specifics; harvest complete |` (*prospect estimate)

## Worked micro-examples

1. **Stage 1, FDA-routed food, screening.** Sweep snippet-verified a Class II notice (date + allergen visible in snippet); full page unfetched; CDC checked clean; state and retailer layers unrun. R1 signals: named tier-1 gap, no novelty baseline. Score: 🟢 80 — anchor "confirmed tier-ceiling gap"; labeled prospect estimate.
2. **Stage 2, lot-code question, already-owns.** Agency notice fetched (lots + remedy in), retailer hub lot-check done, state relays fetched; last stage novelty 8%, 0 open leads, re-queries return aggregator repeats. R1/R4/R5 all 🔴/🟠 → overall 🔴 → consolidation recommendation. The record is *complete* — exhaustion here is success, not failure.
3. **FSIS bot-wall.** Direct fetch attempted once per protocol, Akamai-blocked, labeled access-limited; two independent confirmations via search extraction (FSIS snippet + trade-press relay) with matching specifics. R1 scores on the corroboration harvest (🟡 at Stage 1, falling as relays are exhausted) — the unfetchable page is never counted as yield, and the FSIS URL rides in recommended actions as a user step, not a stage.
