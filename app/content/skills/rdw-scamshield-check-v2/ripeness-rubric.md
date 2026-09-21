# Ripeness & Relevance Gauge — pricing the next stage, honestly

The gauge answers one question: **will another verify stage surface new decision-relevant evidence not already in the findings index?** Search results behave like result pages: pages 1–2 hold the quality sources; by pages 5–6 you're reading repeats, re-reported reports, and slop. The gauge tells the user — per check line, and overall — which page of the check they're on, so the go/stop gate is a priced decision, not a vibe. Ported from rdw-product-dig's ripeness rubric (via rdw-scamshield-tea2-corpcheck), adapted from product veins to this skill's check lines, subject types, and source hierarchy.

## The three components

Every line row shows three components. The **headline** is the composite color + score; the other columns explain it.

| Component | Question it answers | Scale |
|---|---|---|
| **Richness** | How much quality evidence *exists* in this line? (recorded + confirmed-unfetched) | 0–100 |
| **Marginal yield** (headline) | How much *new* decision-relevant evidence would one more stage surface? | 🟢🟡🟠🔴 + 0–100 |
| **Relevance** | How much does this line matter to *this user's worry*? | High / Medium / Low |

Richness ≠ yield — and in this skill richness is structurally capped by subject age: scam subjects are often *young* (a three-week-old domain, a two-month-old shop) and have a small record because little time has passed, not because the sweep was lazy. Low richness on a young subject is the truth, not a scoring failure. What the yield column prices is whether any unexplored **surface** remains — an unfetched advisory-portal entry, an unmined board thread, an unqueried agency database — not whether deep archives exist.

## Relevance defaults by worry

Set at Stage 1 from the user's stated worry (the intake "angle"); revise only when the user redirects. Never inflate a convenient line to High to justify a stage.

| Worry / angle | High | Medium | Low |
|---|---|---|---|
| Legitimacy (default — "is this a scam?") | C1, C2, C9 | C3, C5, C10 | C4, C6, C7, C8 |
| Counterfeit / fake goods | C4, C5, C6 | C1, C2 | C3, C7, C8, C9, C10 |
| Non-delivery / order never came | C1, C2, C9 | C5, C10 | C3, C4, C6, C7, C8 |
| Payment & checkout safety | C7, C3 | C1, C2, C5 | C4, C6, C8, C9, C10 |

Subject-type overrides: **suspicious email** → C8 and C1 lead whenever research runs at all (the smoke test usually settles emails; a corroborating-only fall-through or a `document` pass is when this row matters); **product listing** → C4/C5/C6 lead; **online seller** → C2/C5/C9 lead. **Victim-path runs** re-rate toward whatever documents the user's claim (advisory-portal reports, payment-rail records) — the background check is documenting the pattern for their dispute.

## Color bands and observable anchors

Match the line's observable signals to these anchors; pick the band, then place the score within it. Bands carry the meaning; the numeric score is a communication device, not a measurement.

### 🟢 Fresh · 75–100 · "pages 1–2"
Any of:
- ≥3 concrete **unfetched leads** in the pool, at least one a **tier 1–4 primary** (an advisory-portal report page, an agency action, an official platform-policy page, a named-outlet investigation), **or**
- A confirmed **tier-ceiling gap**: the best source type the hierarchy says should exist hasn't been reached, and evidence shows it exists (press covered the enforcement action ⇒ an agency record exists; every board repeats the same story ⇒ the advisory-portal entry or platform-action page is the unfetched ceiling), **or**
- (Stage 2+) last stage's **novelty rate > 50%** with the lead pool still populated.

### 🟡 Yielding · 50–74 · "pages 2–3"
Any of:
- 1–2 concrete unfetched leads, or ≥3 leads all tier 5+ (boards, community, aggregators), **or**
- Tier 1–4 primaries largely in, but the board-thread / review-trajectory / community digging hasn't been done and the line's story clearly runs through it, **or**
- Last stage's novelty rate 25–50%.

### 🟠 Thinning · 25–49 · "pages 4–5"
All of:
- Tier 1–4 sources reached or confirmed absent; boards and community substantially mined, **and**
- Last stage's novelty rate 10–25% — new results mostly corroborate or re-report known findings, **and**
- Remaining leads are niche corners only: deep pagination, foreign-language boards, archived threads.

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
| **Lead-pool depth** | count of `open` leads for that line | ≥3 strong · 2–4 moderate · ≤1 weak. Leads must be **concrete** (URL, portal entry, thread) — "more complaints probably exist" is not a lead |
| **Tier-ceiling gap** | best tier harvested vs. best tier the source hierarchy says should exist for that finding type | The strongest gold-left signal. "Boards are full of it" + "no advisory-portal or platform-action page pulled" = at least 🟡, whatever else is true |
| **Repeat rate** | share of results already covered by the findings index | Rising repeat rate across stages is the decay curve made visible |
| **Slop rate** | share of results from tier 8 | Never cited; counts only toward the exhaustion signal |

Aggregator note: tier-7 site scorers (ScamAdviser-class) are **leads, never endpoints**. A line whose only open leads are aggregators is thinning at best — aggregator agreement is a pointer to check elsewhere, not a harvest target.

## Clean-line shortcut

A 🔵 line whose absence-check reached its proper tier (advisory portals + boards + community, per the subject guide) is exhausted **by completion**: score 🔴 with the note "confirmed absence — harvest complete" (richness records how much absence-proof was gathered; it is not nothing). On a young subject, pair this with the verdict rubric's honesty rule: absence of reports on a two-month-old shop is *thin* absence-proof — the line is still exhausted (there is genuinely nothing more to find), and that is exactly why the verdict floors at 🟡 caution rather than 🟢. **Exhaustion ≠ safety.** Never score a clean line 🟢 without named leads — "maybe reports exist" is not a lead, and absence of hits is already the finding.

## When the gauge renders

Not on snap responses — no research has run, there is no coverage to gauge, and the snap verdict stands on direct observation. From the first Stage-1-shaped response on (the sweep, a corroborating-only fall-through, or a `document` pass), the gauge renders every stage.

## Scoring procedure

1. Gather the line's signals — they come free from the ledger.
2. Match to a band's anchors — conjunctive/disjunctive as written; when a line sits between bands, take the **lower** band (optimism bias is the failure mode this rubric exists to prevent).
3. Place the score within the band: top if the anchor conditions are exceeded, bottom if barely met.
4. Write a one-line justification naming the evidence ("🟡 58 — BBB Scam Tracker entries snippet-seen, unfetched (tier-3 gap); 2 open board leads; novelty 35%"). **A score without a named-evidence justification is invalid.**

## Overall gauge

Deterministic aggregation:

1. If any **High-relevance** line ≥ 50 (🟢/🟡): overall = the score of the highest-yielding High-relevance line.
2. Else if any **Medium-relevance** line ≥ 50: overall = that line's score − 15.
3. Else: overall = the lowest band present among remaining lines → recommend consolidation.

Render as one line: `OVERALL: 🟡 58/100 — targeted stage on C2 recommended (1 High-relevance line still yielding; C3 thinning).`

Recommendation mapping: 🟢 → next stage strongly recommended · 🟡 → targeted stage on the listed lines · 🟠 → only for a specific named question · 🔴 → stop, consolidate.

## Honest-scoring rules (anti-gaming)

- 🟢/🟡 **requires named leads or a named tier gap.** An empty lead pool cannot justify green or yellow, no matter how the search "felt".
- Never score 🔴 to avoid work; never score 🟢 to seem thorough. Both are auditable against the ledger — that's the point of the ledger.
- Relevance comes from the user's actual worry, set at Stage 1 and revised only on redirect. On a custom-redirect stage, re-rate that stage's lines — the gauge serves *their* question, not the skill's convenience.
- Prospect estimates (Stage 1) may drop sharply once Stage 2 measures novelty. That's the system working, not a mistake — surface it in gauge history.
- The gauge never touches the verdict. This skill's most tempting confusion is "nothing left to find" drifting into "verified safe". A 🔴-yield C1 on a young store pairs honestly with a 🟡 caution verdict — neither upgrades the other.

## Gauge output format (rendered every stage with the legend; not on snap responses — research coverage not yet run)

```markdown
## Ripeness Gauge — after Stage 2

| Line | Richness | Yield (headline) | Relevance | Evidence |
|---|---|---|---|---|
| C2 Review boards | 70 | 🟡 58 | High | Trustpilot arc characterized; 2 Reddit threads unfetched; novelty 35% |
| C3 Domain forensics | 45 | 🟠 30 | Medium | WHOIS + history pulled; 1 marginal archived-thread lead; novelty 12% |
| C9 Community | 55 | 🟠 35 | High | both named threads mined; repeats only on re-query; novelty 10% |
| C1 Advisory portals | 25 | 🔴 15 | High | confirmed absence at portal-query level — clean by completion |

**OVERALL: 🟡 58/100** — targeted stage on C2 recommended (1 High-relevance line still yielding).

Legend: 🟢 75–100 fresh (pages 1–2 — new quality evidence confirmed waiting) · 🟡 50–74 yielding (pages 2–3 — targeted digging still pays) · 🟠 25–49 thinning (pages 4–5 — only named questions worth a dig) · 🔴 0–24 exhausted (pages 6+ — repeats and slop; stop).
```

## Plan integration

The next-stage plan (verdict-rubric template) is ordered by **relevance × yield** and names its target lines' gauge scores. When the overall gauge reads 🟠/🔴 — or coverage is already complete on all applicable lines — the plan is replaced by a consolidation recommendation, with at most one targeted option offered. This formalizes the gate's push-back rule: `go` against a 🔴 overall gets exactly one evidence-backed push-back.

## Appendix E — Gauge history (report-file ledger)

The report body's gauge table is overwritten each stage; the history preserves the decay curve:

`| Line | S1 (prospect) | S2 | S3 | … | Trend note |`

Example row: `| C2 Review boards | 🟢 75* | 🟡 58 | 🟠 38 | BBB + Trustpilot + both threads mined by S2; S3 repeats only |` (*prospect estimate)

## Worked micro-examples

1. **Stage 1, store, non-delivery worry.** Sweep surfaced BBB Scam Tracker entries (snippet-seen, unfetched) and a Reddit thread naming the same domain family; the FTC/IC3 report-level query hasn't been run. Signals: named tier-3 gap, 2 concrete leads, no novelty baseline. Score: 🟡 60 — anchor "1–2 concrete leads" plus the named ceiling gap; labeled prospect estimate.
2. **Stage 3, community line.** Last stage: 4 searches, 0 new findings (novelty 0%), 0 open leads, fresh queries return the same two threads plus SEO-farm pages. Score: 🔴 10 — "repeats and slop; nothing left."
3. **Clean young seller.** All boards and portals swept clean at the tier the guide demands; shop two months old. C1/C2/C9 all 🔴 "confirmed absence — harvest complete"; verdict stays **🟡 caution** (unverifiable is not verified-safe). Gauge and verdict disagree *by design* — the gauge says more searching won't help, the verdict says the absence-proof is thin. Both render; neither repairs the other.
