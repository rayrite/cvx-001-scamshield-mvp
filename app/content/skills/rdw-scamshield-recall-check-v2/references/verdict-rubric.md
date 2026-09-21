# Verdict Rubric — two readouts, coverage, and honesty rules

Every check answers **two different questions** and renders them as separate readouts. Collapsing them is the classic failure this rubric exists to prevent: a scam text about a never-recalled product, and an authentic news article about a real recall, must not produce the same single verdict.

## The two readouts

| Readout | Question it answers | Rendered |
|---|---|---|
| **Recall status** (headline, always) | Does this product have a documented recall record — current or past — or an active investigation? | 🟢🟡🟠🔴 + confidence High/Medium/Low + current-vs-past separation |
| **Content authenticity** (only for claim-bearing subjects: message, post, site, article) | Is this material what it claims to be? | 🟢🟡🟠🔴 + confidence, same scale as the family's other skills |

A verdict without its coverage map is invalid. The Stage-1 version of either readout is always labeled *provisional*; it firms up (or changes — say so plainly) as stages add evidence. The **snap verdict** (Stage ½) applies to the authenticity readout only and is labeled `snap`.

## Readout 1 — Recall status bands

### 🔴 Recall record found · documented
**Any one** of:
- An **agency record** (FDA/FSIS/CPSC/NHTSA/USCG/EPA notice, or the FDA Enforcement Report / device database entry) fetched directly and naming specifics: date, class or reason, affected lots/scope — **or** snippet-verified with the same specifics while the agency fetch is flagged as the pending confirmation (upgrade on fetch; if the agency surface stays unreachable, the 🔴 stands on the corroboration with the access limitation named), **or**
- **CDC outbreak with a named product link** where an FDA/FSIS recall action is documented in the investigation record, or
- **≥2 independent tier-3/4 confirmations with matching specifics** (state pages and/or named press, same dates + lots + class) — the "press-reported, agency page not yet seen" case.

Rendered with: agency · announcement date · class (I/II/III) · reason/hazard · affected lots/date ranges · distribution scope · remedy · **conclusion status (ongoing vs terminated/completed)**. A past concluded recall still renders 🔴 as a *record* — the current-vs-past section carries the "is it still live" answer.

### 🟠 Recall-adjacent · official concern short of a recall
**Any one** of: a **market withdrawal** or **safety alert / public health alert** on the agency page for this product · an **active CDC outbreak investigation** linked to the product (or its category + brand) with no recall announced · a documented **agency investigation** (e.g., FDA inspection fallout, NHTSA defect investigation) reported by tier 1–4 sources. This band exists because "people are sick and the agency is investigating, but no recall has been announced" is a real, common, actionable state — and it is not a recall.

### 🟡 Unverified or ambiguous · record can't be established
**Any** of: **ambiguous product identity** (common name, no brand/lot to narrow, multiple same-name products) · **thin coverage** (routing unclear, primary surfaces unreachable, coverage map mostly ⚪) · **contradictory record** (press says recalled; agency page silent; no conclusion possible this stage). A 🟡 must name which condition holds and what would resolve it.

### 🟢 No recall record found · absence, stated as absence
**All** of: routing confirmed (right agency surface identified) · the applicable lines actually checked (R1 at minimum, R3 for food-illness angles, R6 for recency) · nothing found. Phrase as **"no recall record found across <lines> as of <date>"** — never "safe", never "not recalled" as an absolute. For a product with *some* history but no record, note the search window (e.g., "FDA list + Enforcement Reports back to <year>, press back to <year>").

## Readout 2 — Content authenticity bands (claim-bearing subjects)

### 🔴 Scam / impersonation pattern · 75–100
Any one of: a **near-diagnostic ask** observed directly (pay/card to receive a refund; gift card/wire/crypto rails; credential harvest behind an "official recall" claim) · **agency/brand impersonation confirmed in the material** (@-domain or link domain provably not the institution's, institution is common knowledge) · **documented scam campaign** matching this exact message (press/FTC coverage of the same campaign) · **≥3 independent victim reports** of the same message/domain.

### 🟠 Multiple red flags · 50–74
A cluster of ≥2 independent tells (urgency + missing specifics + unsolicited contact + look-alike domain) with no decisive ask and no impersonation of a provably-major domain. High-volume "is this real?" community threads with no victims yet may hold this band.

### 🟡 Unverifiable · 25–49
The claim can't be confirmed or condemned from available evidence: anonymous post making a recall claim the agency record neither confirms nor denies · an article whose specifics can't be traced to a notice · a short-code text with no visible ask. **This is the honest home of most recall-claiming social posts.**

### 🟢 No adverse findings · 0–24
Every applicable tell checked, nothing fired, and the material's claims **verify at the official record** (the retailer really did send this; the article matches the agency notice). Phrased as "no scam indicators found; claims consistent with the official record" — never "verified legitimate" as an institution-grade guarantee.

## Snap verdicts (Stage ½ — zero-search)

A snap verdict is a 🔴 **authenticity** verdict delivered before any research, when a decisive smoke-test item (`references/smoke-test.md`) fires on the material itself. It is not a new band — it is an existing 🔴 anchor (near-diagnostic ask, or impersonation confirmed in the material) reached without searching.

**Label rules:** labeled `snap`, never `provisional*. Coverage is stated as "smoke test: <items fired>"; research coverage does not exist yet and must not be implied. **The recall-status readout in a snap response is always "not checked"** — it is answered by the `document` pass or a fresh routed check, never by the content's fraudulence (a scam about product X tells us nothing about whether X has a real recall record, and vice versa).

**Documentation-pass expectations:** `document` runs the Stage-1 routed sweep — writing up the scam pattern AND honestly answering the recall-status question. Normal outcome: authenticity band unchanged (confidence wording gains named sources), recall status whatever the record shows. Rare outcome: documentation contradicts the snap (the "wrong" domain is the retailer's documented alert sender) — show the movement explicitly per the honest-verdict rules and record the smoke false-positive.

**Anti-gaming:** [Corroborating] items alone never snap. An item whose FP guard says fall through (short-code sender, aggregator breadth, brand's own recall microsite) has not fired. And the fastest fake-recall snap must still not leak authority over the recall-status readout — "the text is a scam" ≠ "the product is clean".

## Confidence

| Tag | Requires |
|---|---|
| **High** | Agency/CDC record fetched · or a decisive tell observed directly · or ≥2 independent documented confirmations with matching specifics |
| **Medium** | Snippet-verified agency record pending fetch · one credible press/state confirmation · strong tell cluster without documentation |
| **Low** | Community-only evidence · single anecdotal report · mostly-inference |

Confidence is about evidence quality, separate from the band: 🔴 Medium (press-confirmed recall, agency page not yet fetched) is a valid honest state. A snap verdict is High (decisive tell observed directly). Access-limited corroborations are Medium until the user (or a lucky re-fetch) sees the agency page.

## Aggregation procedure

1. Score each **flagged line** against the band anchors; each 🚩/🔴 line names its specifics (agency, date, lots) or tells (with smoke item IDs).
2. Each readout's verdict = the **highest band triggered** by an anchor met on its own side. Never let authenticity findings escalate recall status or vice versa — **cross-readout contamination is the rubric's cardinal sin**.
3. Attach the confidence of the strongest contributing evidence, per readout.
4. Write the one-line justification naming the evidence per readout: `🔴 High — FDA Class II notice 2026-08-12, undeclared milk, lots 24-081..24-084, remedy: return; ongoing`. **A verdict without a named-evidence justification is invalid.** Snap verdicts justify with smoke item IDs.
5. Downgrade/hold rules: press-only vague claims cap at 🟠 (recall status) · ambiguous identity caps at 🟡 · single anecdotal illness report caps at 🟡 (record it, don't band it) · a 🟢 recall-status requires routing confirmed + R1 checked, else 🟡 thin.

## Honest-verdict rules (anti-gaming)

- Never render 🔴 to seem decisive; never render 🟢 to seem reassuring. Both are auditable against the findings index.
- **Absence is not verification.** "No recall record found" is a statement about the search — dates, lines, routing — never about the product's safety. Say it exactly that way.
- **Current vs past is mandatory** for any 🔴: a 2023 terminated recall and a live Class I are different facts; dates and conclusion status carry the difference.
- **No defamation beyond evidence**: "scam" attaches to documented patterns and observed tells; inferred conclusions are labeled `[Inferred]`.
- **Access limitations are named**, never hidden: an FSIS-corroborated finding says so, in the verdict basis if it's load-bearing.
- Contradictions (agency silent, press loud) are surfaced, weighted by tier, and reflected in confidence — not silently resolved.
- Verdict movement between stages is displayed with its history (`Stage 1: 🟠 provisional → Stage 2: 🔴 after agency notice fetched`) — the movement is information. Same for a snap overturned by documentation.

## Coverage map (rendered every stage, with legend)

```markdown
## Coverage Map — after Stage 1

| Line | Status | What was checked / found |
|---|---|---|
| R1 Agency list (FDA) | 🔴 hit | FDA recalls page: Class II notice 2026-08-12, undeclared milk, lots listed |
| R3 CDC outbreak layer | 🔵 clean | No active investigation naming this brand/product |
| R6 Press & news | 🔴 hit | 2 outlets covered 2026-08-13, matching lots |
| R4 State distribution | ⚪ unchecked | Not yet — Stage 2 offers "was it distributed in <user's state>" |
| R5 Retailer hub | ⚪ unchecked | Not yet — user purchased at Kroger; kroger.com/i/recall-alerts queued |
| R7 Content authenticity | ➖ | Not applicable — subject is a bare product question |
| R8 Community | 🔵 clean | No illness-report threads found |

Legend: ⚪ unchecked · 🔵 checked, clean · 🚩 checked, flagged · 🔴 checked, hit · ➖ not applicable.
Unchecked applicable lines = verdict coverage gap, listed in Gaps & Caveats.
```

Snap responses replace the table with one line — `Smoke test: S-M1 + S-M2 [Decisive] fired; research coverage not run (offered via "document")` — because research coverage does not exist yet and must not be implied.

## Verdict boxes (rendered every stage, first thing the user reads)

Standard staged response — recall status first, authenticity below it only when applicable:

```markdown
> ## 🥫 RECALL STATUS: 🔴 Recall record found — High confidence *(provisional, Stage 1)*
> **Basis:** FDA Class II notice 2026-08-12 — undeclared milk; lots 24-081..24-084; distribution: 12 states (list pending fetch); remedy: return to store for refund. Status: ongoing.

> ## ⚠️ CONTENT AUTHENTICITY: 🟡 Unverifiable — Medium confidence *(provisional, Stage 1)*
> **Basis:** FB post claims the recall but links no agency source; no scam tells fired; agency record exists and is consistent with the claim — consistency is corroboration, not proof of the account's identity.
> **If you own it:** check your lot against the FDA notice before using.
```

Snap variant (authenticity only, recall status explicitly not checked):

```markdown
> ## ⚠️ CONTENT AUTHENTICITY: 🔴 Scam/impersonation pattern — High confidence *(snap, Stage ½ — zero searches)*
> **Basis:** S-M1 pay-to-refund ask ($0.99 "processing" for a $40 refund) + S-M2 link domain gp-refund[.]net ≠ any Coca-Cola/retailer domain — both observed in the text itself.
> **Recall status: not checked.** Do/don't: don't click or pay; verify any real recall at fda.gov/safety/recalls or your retailer's app; forward the text to 7726 and report to FTC.
```

Rules: emoji + band + confidence + provisional/snap marker in the header line; one-line basis with check-line or smoke-item refs; one actionable line. Identical in chat and file. The final (consolidated) verdict drops the provisional marker; a snap verdict keeps its `snap` label (it names its basis, not its tentativeness).

## Next-stage plan template (rendered last, followed by the command hint)

```markdown
NEXT STAGE (default, awaiting approval)
  1. [R1] Fetch the FDA notice page — full lot table, distribution states, remedy (1 fetch)
  2. [R4] Check <user's state> ag/health page for distribution confirmation (1 fetch)
  3. [R5] Check Kroger recall alerts for the lot-level entry (1 fetch)
  Est. budget: 1–2 searches, 3 fetches. Fills R4/R5 and upgrades the 🔴 from snippet-verified to fetched.
```

After a snap verdict, the plan block is replaced by the documentation offer: `Say "document" for the full archived report — which also checks <product>'s actual recall record · describe a different direction to customize · "stop" to finish here.`

Plan rules: 2–4 target lines; ordered by **relevance × yield** per the ripeness gauge (`references/ripeness-rubric.md`), naming each target line's gauge score; actions concrete (named fetch or query); budget stated; if all applicable lines are 🔵/➖ with a stable verdict, or the overall gauge reads 🟠/🔴, the plan is replaced by a consolidation recommendation (at most one targeted option offered; the overview map runs at consolidation if enabled — it is post-processing, not a stage).

## Ledger formats (report-file appendices)

**A. Query log** — `| # | Stage | Line | Query | Notable results |` — check before every new query.

**B. Findings index** — `| ID | Finding (one line) | Source | URL | Date | Line | Confidence | Corroborated by |` — repeats attach as corroboration, never a second row. Confidence: `[Documented]` agency/CDC/government record (or access-limited corroboration, labeled) · `[Reported]` press/retailer/state relay naming specifics · `[Inferred]` signal-cluster match. Smoke findings enter at documentation time with source "user-supplied material (static observation)".

**C. Lead pool** — `| ID | Line | Lead (URL/notice/thread) | Why promising | Tier est. | Added (stage) | Status (open/fetched/dead-end/access-limited) |`.

**D. Verdict history** — `| Stage | Readout | Verdict | Confidence | Trigger/justification |` — one row per readout per stage; a snap's row is Stage ½ (authenticity only; recall status row appears when the sweep runs).

**E. Gauge history** — `| Line | S1 (prospect) | S2 | S3 | … | Trend note |` — the ripeness decay curve per line (`references/ripeness-rubric.md`); the report body's gauge table is overwritten each stage, this preserves it.

## Worked micro-examples

1. **Snap, recall text.** "Pay $0.99 to receive your $40 refund" + non-brand link domain. S-M1 + S-M2 fire. Authenticity: `🔴 High (snap)`. Recall status: **not checked** — stated, with `document` offered. Zero searches.
2. **Documented hit.** Agency notice fetched: date, class, lots, remedy all captured. Recall status: `🔴 High — FDA notice <date>, Class II, <reason>, lots <range>, ongoing`. Current-vs-past section notes it's the only record.
3. **Recall-adjacent.** CDC investigation page names the product category + brand; no recall announced. `🟠 Medium — active CDC investigation (<date> update), <N> cases in <M> states; no recall record found (R1 clean)`. The map (if on) plots case locations from the investigation record.
4. **Honest green.** Routed correctly, R1+R3+R6 clean, routing confirmed. `🟢 Medium — no recall record found across R1/R3/R6 as of <date>; search window: FDA list + Enforcement Reports to <year>, press to <year>; absence is not verification`.
5. **Ambiguous yellow.** "Is there a recall on ranch dressing?" — no brand, no lot. `🟡 — ambiguous identity: no brand/lot to narrow; multiple same-name products. Resolve by: brand + lot code from the label`.
6. **Cross-readout discipline.** Authentic press article about a real recall: authenticity 🟢 (claims match the agency record), recall status 🔴 (the record) — both boxes, no merging. And the reverse: scam text about a never-recalled product: authenticity 🔴 snap, recall status 🟢 after the sweep — the scam's premise is fiction AND the product has no record; two boxes, two different answers.
