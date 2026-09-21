# Ripeness Rubric — scoring marginal yield, honestly

The gauge answers one question: **will another research stage surface new quality content not previously surfaced?** Think of it like search-result pages: pages 1–2 hold the quality results; by pages 5–6 you're reading repeats, irrelevance, and slop. The gauge tells the user — per vein, and overall — which page of the dig they're on.

## The three components

Every vein row in the gauge shows three components. The **headline** is the composite color + score (the user-facing value); the other two columns explain it.

| Component | Question it answers | Scale |
|---|---|---|
| **Richness** | How much quality content *exists* in this vein? (seen + confirmed-unfetched) | 0–100 |
| **Marginal yield** (headline) | How much *new* quality content would one more stage surface? | 🟢🟡🟠🔴 + 0–100 |
| **Relevance** | How much does this vein matter to *this user's request*? | High / Medium / Low |

Richness ≠ yield. A rich vein can be fully harvested (richness 85, yield 🔴 15). A modest vein can still be fresh (richness 40, yield 🟢 80). The headline must track **yield**, not richness — the user is buying the next stage, not admiring the last one.

## Color bands and observable anchors

Score by matching the vein's **observable signals** (next section) to these anchors. Pick the band that matches, then place the score within it using the signals. Bands carry the meaning; the numeric score is a communication device, not a measurement — do not imply false precision.

### 🟢 Fresh · 75–100 · "pages 1–2"
Any of:
- ≥3 concrete **unfetched leads** in the pool, at least one of which is a **tier 1–2 primary** (a named docket, recall entry, service-program page, teardown report), **or**
- A confirmed **tier-ceiling gap**: the best available source type for this vein (per the category guide) has not been reached, and evidence shows it exists (e.g., press coverage of a lawsuit ⇒ a docket exists; a recall announcement ⇒ a regulator entry exists), **or**
- (From Stage 2 on) last stage's **novelty rate > 50%** with the lead pool still populated.

### 🟡 Yielding · 50–74 · "pages 2–3"
Any of:
- 1–2 concrete unfetched leads, or ≥3 leads all of tier 3+ (press, community), **or**
- The tier-1/2 primaries are largely in, but community/archival digging (megathreads, owner threads, technician posts) has not been done and the vein's story clearly runs through it, **or**
- Last stage's novelty rate 25–50%.

### 🟠 Thinning · 25–49 · "pages 4–5"
All of:
- Tier 1–2 sources reached or confirmed absent; community coverage substantially mined, **and**
- Last stage's novelty rate 10–25% — new results are mostly corroboration, restatements, or listicles re-reporting known facts, **and**
- Remaining leads are niche corners only: deep pagination, non-English press, archival threads, low-traffic forums.

Dig only if the user has a **specific named question** left.

### 🔴 Exhausted · 0–24 · "pages 6+"
All of:
- Lead pool empty or reduced to dead-ends, **and**
- Last stage's novelty rate < 10%, **and**
- Fresh searches return repeats of harvested claims and/or slop (SEO farms, AI mills, thin affiliate pages) dominating results.

Further stages are not justified. Say so plainly and propose consolidation.

## The five signals

| Signal | How to measure | Notes |
|---|---|---|
| **Novelty rate** | new claims recorded ÷ searches executed in that vein, this stage | Exists from Stage 2 on. Stage 1 has no baseline — its scores are **prospect estimates** (richness + lead pool + tier gap) and the score history labels them as such |
| **Lead pool depth** | count of `open` leads in the pool for that vein | ≥5 strong · 2–4 moderate · ≤1 weak. Leads must be **concrete** (URL, docket ID, thread link) — "more forums probably exist" is not a lead |
| **Tier-ceiling gap** | best tier harvested vs. best tier the category guide says should exist for this vein | The strongest there-is-gold-left signal. "Press covered the lawsuit" + "docket never pulled" = at least 🟡, whatever else is true |
| **Repeat rate** | share of results already covered by the harvested-claims index | Rising repeat rate across stages is the decay curve made visible |
| **Slop rate** | share of results from tier 8 (SEO farms, AI mills, undated blogs) | Never cited. High slop rate + empty primaries = heading 🔴 |

## Scoring procedure

1. Gather the vein's signals (they come for free from the ledger).
2. Match to a band's anchors — the anchors are conjunctive/disjunctive as written; when a vein sits between bands, take the **lower** band (optimism bias is the failure mode this rubric exists to prevent).
3. Place the score within the band: top of band if the anchor conditions are exceeded (more leads, higher novelty), bottom if barely met.
4. Write a one-line justification naming the evidence ("🟡 58 — CPSC docket pulled; 3 open tier-4 community leads; last novelty 30%"). **A score without a named-evidence justification is invalid.**

## Overall gauge

Deterministic aggregation:

1. If any **High-relevance** vein ≥ 50 (🟢/🟡): overall = score of the highest-yielding High-relevance vein.
2. Else if any **Medium-relevance** vein ≥ 50: overall = that vein's score − 15.
3. Else: overall = the lowest band present among remaining veins → recommend stop.

Render as one line: `OVERALL: 🟡 62/100 — targeted stage on V6 + V7 recommended (2 High-relevance veins still yielding).`

Recommendation mapping: 🟢 → next stage strongly recommended · 🟡 → targeted stage on the listed veins · 🟠 → only for a specific named question · 🔴 → stop, consolidate.

## Honest-scoring rules (anti-gaming)

- 🟢/🟡 **requires named leads.** An empty lead pool cannot justify green or yellow, no matter how the search "felt".
- Never score 🔴 to avoid work; never score 🟢 to seem thorough. Both are auditable against the ledger — that's the point of the ledger.
- Relevance is set from the user's actual request at Stage 1 and revised only when the user redirects. Do not inflate a convenient vein to High to justify a stage.
- When the user redirects to a custom stage, re-rate relevance for that stage's veins — the gauge serves *their* question, not the skill's convenience.
- Prospect-estimate scores (Stage 1) are provisional by definition; when Stage 2 measures novelty, the score history may drop sharply. That's the system working, not a mistake — surface it.

## Gauge output format (rendered every stage, with the legend)

```markdown
## Ripeness Gauge — after Stage 2

| Vein | Richness | Yield (headline) | Relevance | Evidence |
|---|---|---|---|---|
| V5 Known Issues & Defects | 85 | 🟢 82 | High | 3 open leads incl. iFixit root-cause (tier 2); novelty 55% |
| V6 Recalls & Safety | 90 | 🟡 68 | High | CPSC docket pulled; 2 tier-4 press leads left; novelty 35% |
| V7 Legal & Liability | 70 | 🟢 78 | High | class-action docket confirmed, unfetched (tier-2 gap) |
| … | | | | |

**OVERALL: 🟡 71/100** — targeted stage on V5 + V7 recommended (2 High-relevance veins still yielding).

Legend: 🟢 75–100 fresh (pages 1–2 — new quality content confirmed waiting) · 🟡 50–74 yielding (pages 2–3 — targeted digging still pays) · 🟠 25–49 thinning (pages 4–5 — only named questions worth a dig) · 🔴 0–24 exhausted (pages 6+ — repeats and slop; stop).
```

## Discovery preview format

Listed per remaining 🟢/🟡 vein, ordered by relevance × yield; leads named concretely from the pool:

```markdown
## Discovery preview — what's still on the table

- **V7 Legal & Liability** 🟢 78 — the settlement record and terms are still unfetched.
  Leads: L-004 class-action docket (N.D. Cal.) · L-011 settlement administrator page · L-019 legal-press timeline
- **V5 Known Issues & Defects** 🟢 82 — engineering root-cause reporting unmined.
  Leads: L-007 iFixit teardown of affected batch · L-013 technician failure-rate post
```

## Next-stage plan template

Always rendered last in the stage response, followed by the command hint:

```markdown
NEXT STAGE (default, awaiting approval)
  1. [V7] Fetch class-action docket + settlement administrator page (2 fetches)
  2. [V5] Pull iFixit teardown + failure-rate post; corroborate with press (1 search, 2 fetches)
  3. [V9] Sweep owner-forum threads for battery-swap program outcomes (2 searches)
  Est. budget: 5–7 searches, 5–6 fetches. Targets the two 🟢 High-relevance veins.

Reply "go" to run this plan · describe a different direction to customize · "stop" to consolidate the final report.
```

Plan construction rules: 2–4 target veins; actions are concrete (a query or a named fetch, never "research more about X"); ordered by relevance × yield; budget stated; if overall is 🟠/🔴 the plan is replaced by a consolidation recommendation with the one remaining targeted option (if any).

## Ledger formats (Appendices A–D of the master file)

**A. Query log** — every search ever run; check before every new query.

`| # | Stage | Vein | Query | Notable results |`

**B. Harvested-claims index** — the dedupe backbone; new claims get new IDs; repeats attach as corroboration to the existing ID (never a second row for the same claim).

`| ID | Claim (one line) | Source | Pub. date | Vein | Confidence | Corroborated by |`

Confidence: `[Verified — 2+ independent credible sources]` · `[Partial — one credible source]` · `[Unverified — community/single secondary]`.

**C. Lead pool** — the gauge's evidence base and the preview's content; status kept current at every stage close.

`| ID | Vein | Lead (URL / docket / thread) | Why promising | Tier est. | Added (stage) | Status (open/fetched/dead-end) |`

**D. Score history** — the decay curve, visible.

`| Vein | S1 (prospect) | S2 | S3 | … | Trend note |`

Example row: `| V6 Recalls & Safety | 🟢 88* | 🟡 71 | 🟠 41 | primaries pulled by S2; S3 mostly corroboration |` (*prospect estimate)

## Worked scoring micro-examples

1. **Stage 1, legal vein for a recalled phone.** Search surfaced three press articles about a class action; no docket pulled. Signals: tier gap open (tier-2 docket confirmed to exist via press), 2 leads pooled, no novelty baseline. Score: 🟢 80 — anchor "confirmed tier-ceiling gap". Justification names the docket.
2. **Stage 3, defects vein for a quiet dishwasher.** Two stages mined technician forums; last stage ran 4 searches, 1 new claim (novelty 25%); 2 open leads, both deep forum threads. Score: 🟠 30 — "primaries reached, novelty 25%, niche corners only".
3. **Rich but done.** A vein with 14 harvested claims, empty pool, last novelty 5%, slop dominating. Richness 80; yield 🔴 12 with note "rich vein, fully harvested in stages 2–3" — richness and yield disagreeing is exactly the honest state.
