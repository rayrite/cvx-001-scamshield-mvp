---
name: rdw-product-dig
description: Staged deep-and-wide research on a single physical consumer product — automobile, consumer electronics device, or appliance. Use when the user asks to research, investigate, dig into, or look up a specific car, phone, laptop, console, appliance, or gadget ("research the Samsung Galaxy Note 7", "what's wrong with 2019 Toyota RAV4s", "look up LG refrigerator compressor issues"). Runs a fast Stage-1 overview that maps where rich content lives (defects, recalls, lawsuits, teardowns, community sentiment), then user-approved deeper dig stages. Every response ends with a color+score ripeness gauge showing whether another stage will surface new quality content, plus a ready-to-approve next-stage plan.
---

# Product Dig — staged research for cars, electronics, and appliances

Product research fails in two familiar ways: a single-pass lookup that misses the regulator docket, the class action, or the forum megathread where the real story lives — or an exhaustive deep-dive the user never asked to pay for. This skill splits the difference. Stage 1 is a light **prospect** pass: fast, snippet-first, mapping all the standard "veins" of a product's story and flagging where the rich content is (the exploding-battery mountains, the Joy-Con-drift sagas, the butterfly-keyboard settlements). Later **dig** stages mine the flagged veins — but only when the user orders them, one bounded stage at a time, with a honest gauge of how much quality content is left.

## When to scope down

Not every product question needs the staged machinery. A single fact ("does the 2024 Prius have a spare tire") gets a search and an answer — no stages, no gauge, no ledger. The full workflow is for requests where value accumulates across findings: "research this car before I buy it", "what's the deal with the Note 7 batteries", "is this fridge a lemon". If the request names a *category* rather than a product ("best EVs"), that's a comparison task — suggest the competitive-analysis workflow instead. One product = one dig; never mix products in one file.

## Key concepts

- **Veins** — the 12 standard research dimensions (V1 Identity & Lineage, V2 Specs & Features, V3 Pricing & Market, V4 Reception & Ratings, V5 Known Issues & Defects, V6 Recalls & Safety, V7 Legal & Liability, V8 Manufacturer Response & Support, V9 Community & Sentiment, V10 Repairability & Longevity, V11 Technical Analysis & Teardowns, V12 Market Impact & Legacy). V1–V4 are *context* veins; V5–V11 are *investigative* veins — that's where rich deposits form. Full definitions and per-category source pools: `references/category-vein-guides.md`.
- **Stages** — Stage 1 *prospect* (light scan of everything), Stage N *dig* (deep pass on 2–4 veins), *consolidate* (final report).
- **Ripeness gauge** — per-vein and overall color + 0–100 score for the marginal yield of another stage: 🟢 75–100 fresh, 🟡 50–74 yielding, 🟠 25–49 thinning, 🔴 0–24 exhausted. Scored from observable signals, never vibes. Full rubric: `references/ripeness-rubric.md`.
- **Research ledger** — query log, harvested-claims index, lead pool, and score history, persisted in the master file. The memory that makes multi-stage, multi-session research work without repeating itself.
- **Output mode** — where the full stage content goes: `file` (default — highlights in chat, full cumulative report in the markdown file) · `chat` (the complete content of every stage prints to the chat response; no file unless requested) · `both`. Default set by `product-dig.config.json` (`"output_mode"`; absent file = `file`); the user's in-chat choice always wins and is noted in the report meta. Formats: output contract.

## Inputs to collect

- **Product + variant/generation/model years** — "One product = one dig." If the user names a category ("a Tesla"), pick the most iconic current product, state the assumption, and proceed. At most **one round** of clarification questions, then commit.
- **Region / market** — default US / English-language sources. Pricing, recalls, and lawsuits differ by region; pin the scope up front.
- **User's angle** — what they actually care about (buying decision? defect history? curiosity?). Sets vein *relevance* ratings for the gauge.
- **Output location** — default `product-dig_<slug>_<YYYY-MM-DD>.md` in the working directory; use the user's path if given.
- **Output mode** — `file` / `chat` / `both` (default `file`, from `product-dig.config.json`; editing the default in this bullet changes the skill's baked-in default). State the active mode once at intake — e.g. *"Full report → file (default). Say 'in chat' to print full stages here, 'both' for both."* — and honor any-time switches for the rest of the dig.
- **Today's date** — anchor every time-sensitive query to it.

## Procedure

### Stage 0 — Intake (no searching)

1. Capture today's date as `YYYY-MM-DD` and the resolved product identity (name, generation/variant, region). Reason: stale training-data priors are the top failure mode in product research; date-anchored queries (`<product> recall 2016`, `<product> settlement 2026`) are the antidote.
2. Classify the category — automobile / consumer electronics / appliance — and read **only the matching section** of `references/category-vein-guides.md`. Reason: each category has different gold-standard sources (NHTSA vs CPSC vs repair-forums); loading only the relevant guide keeps context lean.

### Stage 1 — Prospect (light and fast)

3. Run **10–14 parallel web searches**, snippet-first: one per investigative vein (V5–V11), plus 2–3 covering the context veins (V1–V4, V12). Date-anchor time-sensitive queries. **Fetch at most 3–5 pages** — only to confirm identity or verify a rich-vein flag. **No subagents.** Reason: Stage 1's promise is speed; every fetch it skips is time the user saves deciding whether to dig at all.
4. Write the **vein map**: 2–4 sentences per vein on what exists there, flagging `⛏ RICH VEIN` where the scan saw signals of deep content (regulator action + press arc + community volume together = a mountain). Reason: the user's Stage-1 takeaway is *where the story is*, not the story itself.
5. Create the **master file** now — meta header, executive overview, vein map, first findings, initial gauge, and the full research ledger (query log from this stage, harvested claims, lead pool, score history). In `chat` output mode, skip the file — the Stage-1 response carries the full stage content per the output contract; a file requested mid-dig catches up at the next stage boundary. Reason: the file is the state container; if the session dies after Stage 1, a later session resumes from the ledger without re-searching.
6. Score the initial gauge (prospect estimate — see rubric) and prepare the **default Stage-2 plan**: 2–4 target veins chosen by highest relevance × yield, each with concrete actions. Reason: the plan must be ready so approval costs the user one word.
7. Deliver the Stage-1 chat response: overview, vein highlights, gauge table + overall line, discovery preview, default next-stage plan, command hint — in `chat`/`both` output mode, this response carries the full stage content instead (output contract). Reason: chat is the decision surface; the file is the archive — and in `chat` mode, chat is also the archive.

### Between stages — the gate

8. End every stage response with the plan and this hint, verbatim in spirit: `Reply "go" to run this plan · describe a different direction to customize · "stop" to consolidate the final report.`
   - `go` / `dig` / `next` / `continue` / `deeper` / `yes` → execute the default plan verbatim. Do not re-plan, do not re-ask.
   - Substantive text → custom stage: restate your interpretation in one line, plan to match, execute. Ask one question only if the direction is genuinely ambiguous.
   - `stop` / `done` / `enough` / `finish` → consolidate (step 13).
   - `go` while the overall gauge is 🔴 → push back **once** with evidence (last stage's novelty rate, the thin lead pool), offer the single most-targeted remaining option; if the user insists, run a minimal stage. Reason: silently running a dead stage wastes the user's money and the skill's credibility.

### Stage N (N ≥ 2) — Dig

9. Execute the approved plan. Default budget: 8–12 searches + 4–8 deep fetches; one subagent per target vein, spawned in parallel when available, serial otherwise. Reason: parallelism is what makes a multi-vein dig affordable; serial fallback keeps the skill portable.
10. Enforce ledger discipline on every action — **never re-run a logged query**; **check the harvested-claims index before recording** (a repeated claim is corroboration attached to the existing claim ID, not a new claim); add promising unfetched results to the **lead pool** instead of chasing them mid-stage. Reason: the whole value of staging is that stage N+1 starts where stage N ended; re-finding is the failure this prevents.
11. Record claims as: one-line claim + source name + URL + publication date + vein + confidence tag (`[Verified]` / `[Partial]` / `[Unverified]`). Surface contradictions explicitly — both positions, both sources; never silently pick a side. Reason: product stories attract conflicting numbers (failure rates, settlement amounts); hiding the conflict is worse than either number.
12. Close the stage: update the master file (findings grow, timeline grows, ledger updated), **re-score every touched vein** from the rubric's signals, then deliver the stage response: banner, 3–6 new findings (🆕), gauge + overall, discovery preview, next default plan, command hint. In `chat`/`both` mode the stage response carries the full stage content (every claim, full citations) per the output contract, and the master-file update is skipped in `chat` mode.

### Consolidate

13. On stop (or confirmed 🔴 overall): restructure the master file into the final report — findings by theme (not by stage), issue & event timeline with a date-precision ladder (`YYYY-MM-DD` → `YYYY-MM` → `c. YYYY` → `Date uncertain`), synthesis with overall confidence (high/medium/low) and why, adjacent digs worth ordering, gaps & caveats, tiered sources. Chat response: top-line findings, final gauge statement, file path — in `chat`/`both` mode the full final report is delivered in the chat response instead (or in addition). Reason: the consolidated report should stand alone for a reader who never saw the stages — in `chat` mode, that reader reads the chat.

## Output contract

- **One cumulative master file**, `product-dig_<slug>_<YYYY-MM-DD>.md` (creation date; collision → `-v2`), updated every stage, finalized on stop. In `file` mode (the default), never paste the full file into chat — link it and summarize.
- **Output modes** (default `file`; precedence: the user's in-chat choice > `product-dig.config.json` → `"output_mode": "file" | "chat" | "both"`, absent file/field = `file` > this contract's default):
  - `file` — chat responses are highlight summaries (overview, vein highlights, gauge, plan); the full cumulative report lives in the master file.
  - `chat` — the complete content of each stage prints to the chat response: stage banner, **every** claim recorded this stage with its full citation (claim + source + URL + publication date + vein + confidence tag — no highlight cap), executive overview, vein map, gauge with legend, the stage's **ledger delta** (queries run, new claim IDs, lead-pool changes — the cumulative ledger is not reprinted, only the delta), then the plan. No master file is written unless requested; consolidation delivers the full final report in chat.
  - `both` — full stage content in chat **and** the master file maintained as in `file` mode.
  - Scope-down single-fact asks are unaffected (no stages, no mode).
- **File sections, in order:** meta header (product · variant · region · category · created · last updated · stage count · status) · Executive Overview · Vein Map · Findings by Vein (H3 per vein; claims cited; 🆕 marks current-stage additions) · Issue & Event Timeline (`Date | Event | Significance | Sources`) · Ripeness Gauge (current table + score history) · Discovery Preview · Gaps & Caveats · Sources (tiered, with access dates) · Appendices A–D: the research ledger.
- **Every stage's chat response ends with the gauge block then the plan block** — the gauge is the final scored section; the plan + command hint is the last thing the user reads.
- **Gauge legend rendered every time** (colors, bands, meaning) — a reader joining at Stage 3 must understand the gauge without archaeology.
- **Citations:** inline Markdown links with the source name visible, publication date and access date; every non-trivial claim cited; slop-tier sources (SEO farms, AI content mills, undated blogs) are never cited — they count only toward the slop signal.
- **No fabricated anything:** no invented dates, docket numbers, statistics, or quotes. If a number can't be sourced, it goes in Gaps & Caveats.

## Source hierarchy (use in this order of preference)

1. **Regulator & official records** — NHTSA (autos), CPSC (consumer products), FCC, EPA, IIHS, court dockets, official recall pages
2. **Primary technical** — manufacturer service bulletins/TSBs and service-program pages, teardown reports, iFixit, failure analyses
3. **Expert & survey** — Consumer Reports, JD Power, published failure statistics
4. **Tier-1 press** — Reuters, WSJ, Bloomberg, major consumer/tech/automotive press, named authors
5. **Manufacturer claims** — marketing/press pages; always mark `manufacturer-claimed`
6. **Reputable community** — model forums, Reddit megathreads, repair-trade forums; cite as community-sourced
7. **Trackers & aggregators** — class-action/recall trackers: leads, not endpoints; corroborate before citing
8. **Slop** — never cite

Numeric and failure-rate claims require tiers 1–4. A higher tier contradicting a lower one: lead with the higher tier, record both. Lack of evidence is not evidence of absence — a quiet recall vein is a finding, not proof of safety.

## Failure handling

- **Ambiguous product** — resolve to the most iconic current product, state the assumption, proceed; one clarification round max.
- **Obscure/thin product** — Stage 1 reports honest low richness (mostly 🟠/🔴), recommends stopping after Stage 1. Never pad stages with slop to seem useful.
- **Brand-new product** — note that coverage hasn't formed yet; several veins are green-by-default; suggest re-running in N months.
- **Paywalled/blocked source** — record the lead as `dead-end` in the pool, note the gap, continue. Never invent contents.
- **Sources disagree** — both positions in the vein + Gaps; state which methodology looks stronger; reflect it in the synthesis confidence.
- **Session ended mid-dig** — on return, read the master file, rebuild state from the ledger, resume at the next stage. In `chat` mode there is no file to rebuild from — the dig restarts; surface that trade-off when the user picks `chat` (`both` keeps the file).
- **User pivots to a different product** — mini-consolidate the current file, start a new dig.

## Examples

**Example 1 — notorious product, rich veins.**
Input: "research the Samsung Galaxy Note 7".
Stage 1 (fast): overview — flagship phablet, Aug 2016 launch, two recalls, discontinued Oct 2016 after battery fires. Vein map flags `⛏ RICH VEIN` on V5 (battery defect), V6 (CPSC recall docket), V9 (airline-ban memes, megathreads), V12 (a product-killing failure with a long legacy). Gauge: overall 🟢 88 — prospect estimate; lead pool holds the CPSC docket, FAA safety advisory, teardown reports, class-action coverage, all unfetched. Default Stage-2 plan targets V5+V6+V7. User replies "go" → Stage 2 pulls the recall chronology, defect root-cause reporting, and the class-action record; V6 moves 🟢→🟡, overall 🟡 71. User replies "dig the airline ban angle" → custom Stage 3 on V6/V12 with the FAA angle. User replies "stop" → consolidated report with full timeline; final gauge 🟡 58 with remaining leads archived.

**Example 2 — quiet product, honest thinness.**
Input: "look up the 2019 Honda CR-V".
Stage 1 finds a healthy-reputation vehicle with one real story (oil dilution in 1.5T engines, V5/V8) and quiet veins elsewhere. Gauge: V5 🟡 64, V8 🟡 58, rest 🟠/🔴. Default Stage-2 plan targets only those two veins. If the user says "go" twice, by Stage 3 the overall gauge reads 🟠 38 — the skill proposes consolidation instead of a third dig.

**Example 3 — scope down.**
Input: "does the 2024 Prius come with a spare tire?" → one search, one answer, no stages, no file.
