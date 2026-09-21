---
name: rdw-scamshield-tea2-corpcheck
description: Staged background-check research on a company or brand — input is a company name, a company website URL, or a product/brand name (resolved to its parent company). Use when the user asks to vet, background-check, screen, or look into a company, brand, maker, or seller before buying from, subscribing to, or trusting it; to find what dark patterns, deceptive practices, hidden fees, scandals, controversies, lawsuits, class actions, verified customer complaints, or price/shrinkflation history a company has on its record; or to verify a website really belongs to the company it claims. Checks regulator actions (FTC, CFPB, SEC, state AGs), litigation, complaint boards, review standings, and documented positives for balance. Opens with a fast smoke test (entity resolution + website authenticity + dark-patterns register lookup) that returns a preview in under a minute; every staged response ends with an evidence-coverage map, a color-coded deception-record verdict with a balance readout, and a ready-to-approve next-stage plan.
---

# CorpCheck — smoke test first, then staged company background checks

Company background checks fail in three familiar ways: a single-pass "seems reputable" that misses the CFPB consent order, the pending class action, or the shrinkflation investigation — an exhaustive dossier the user never asked to pay for — or a one-sided hit job that buries the company's documented positives under its rap sheet. This skill splits the difference in **three tiers**. **Stage ½ smoke test**: a near-zero-search pass that resolves the entity (company name / website / product → parent), verifies a supplied website's authenticity, and looks the company up in the **corporate register** (63 companies with documented dark-pattern records, distilled from the U.S. consumer dark-patterns knowledge base) — returning in under a minute with either a preview of the documented record or a clean fall-through. **Stage 1 triage**: a light snippet-first sweep across ten standard check lines. **Verify stages**: dig the flagged lines — but only when the user orders them, one bounded stage at a time. Findings map to documented dark-pattern IDs (`DP-xxx-nn`), so a finding says *"matches DP-SUB-10 service doom loops — CFPB-documented"*, not a vibe — and every verdict carries a **balance readout** so positives and negatives are weighed, not sorted.

## When to scope down

Not every question needs the machinery. A single factual ask ("who owns Tide") gets a search and an answer — no stages, no file. An education ask ("what is drip pricing") gets an answer from the register's pattern index. An individual online seller, one-off store, or suspicious email is **rdw-scamshield-check-v2** territory — this skill vets *companies and brands*, not sellers. Deep quality research on one physical product is **rdw-product-dig**. The full workflow is for vetting a **specific company**: "background-check SiriusXM before I subscribe", "what's <company>'s track record", "is this website really <company>'s". One company = one check; if the user drops a bundle (a product + its maker + a website), treat it as ONE investigation — resolve to the parent company as the subject, keep the rest as evidence. Comparisons ("Anker vs Belkin") = separate checks, one file each.

## Key concepts

- **Smoke test (Stage ½)** — under a minute, ≤2 network calls: resolve the canonical entity + official domain, verify website authenticity when a URL is supplied (brand-clone and identity-mismatch tells with FP guards), and look the entity up in the corporate register. A decisive impersonation tell → **final snap verdict** (🔴, High, labeled `snap`); a register hit → **snap preview** (band + DP-IDs + tier, labeled `register`); neither → fall through to Stage 1. Full checklist and rules: `references/smoke-test.md`.
- **Subject types** — the three inputs this skill vets: `company name`, `company website`, `product or brand name`. Stage 0 classifies and resolves the product's **parent company** — the check runs on the legal parent, with brand-level findings attributed to the brand.
- **Check lines** — the 10 standard dimensions: C1 Identity & ownership · C2 Regulator & enforcement record · C3 Litigation & class actions · C4 Dark-pattern & deception record · C5 Complaints & review standings · C6 Scandals & controversies · C7 Pricing history & practices · C8 Positives & reputation balance · C9 Privacy & data record · C10 Sector-specific overlay. Line-by-line guides: `references/check-line-guides.md`.
- **Corporate register** — 63 companies with documented dark-pattern records, each with pattern IDs, evidence tier, and a one-line note; distilled from the U.S. consumer dark-patterns knowledge base (research cutoff 2026-09-19). Plus the 73-pattern quick index (`DP-` IDs across 14 families) for classifying findings. Lookup rules, tiers, and the full table: `references/corp-register.md`.
- **Deception-record verdict** — 🟢 no adverse documented record · 🟡 consumer-friction signals · 🟠 documented concerns (pending charges / documented patterns) · 🔴 documented deception record (adjudicated or formally resolved). Always with confidence (High/Medium/Low), named evidence, and the **balance readout** (Adverse-leaning / Mixed / Favorable). Scoring anchors and honesty rules: `references/verdict-rubric.md`.
- **Coverage map** — per-check-line status: ⚪ unchecked · 🔵 checked, clean · 🚩 checked, flagged · 🔴 checked, hit · ➖ not applicable. The honesty device: a verdict is only as strong as its coverage.
- **Ripeness & relevance gauge** — per-line and overall readout of how much *new* decision-relevant evidence one more verify stage would surface: 🟢 75–100 fresh · 🟡 50–74 yielding · 🟠 25–49 thinning · 🔴 0–24 exhausted, each scored from ledger signals (novelty rate, lead-pool depth, tier-ceiling gap) and each line rated for relevance to the user's angle. Stage-1 scores are prospect estimates. The gate's price tag, kept strictly separate from the verdict. Full rubric and formats: `references/ripeness-rubric.md`.
- **Research ledger** — query log, findings index, lead pool, verdict history, gauge history, persisted in the report file. What makes multi-stage checks work without repeating searches.
- **Output mode** — where the full stage content goes: `file` (default — highlights in chat, full cumulative report in the report file) · `chat` (the complete content of every stage prints to the chat response; no file unless requested) · `both`. Default set by `corpcheck.config.json` (`"output_mode"`; absent file = `file`); the user's in-chat choice always wins and is noted in the report meta. Formats: output contract.

## Safety rules (read before any check)

- **Balanced-reporting mandate.** Positives and negatives are both evidence. C8 (positives) is swept in Stage 1 **always** — a report with adverse findings and an unchecked C8 is invalid. Distinguish *documented* (regulator action, adjudication, settlement) from *alleged* (pending suits are allegations, not findings) from *reported* (complaint volume) from *inferred* (signal clusters). Settlements with no-admission clauses are labeled as such. Big companies attract both complaints and regulator attention — complaint volume scales with customer base; weigh specificity and recency, never raw counts.
- **Supplied websites = passive inspection only.** Fetching public pages to verify identity is fine. Never enter data, create accounts, start checkouts, message the company, or download files from a site under verification.
- **Verdict discipline.** Evidence-linked language: "CFPB consent order (2025, $M relief)" not "predatory criminals". Never call conduct "deception" beyond what the documentation shows; honor gray zones (disclosed fees, inflation-driven price increases, and unpopular-but-disclosed policies are not dark patterns).
- **No fabrication.** Every cited action, docket, complaint, or rating must actually exist in fetched/snippet-verified results. Never invent URLs, dates, docket numbers, or dollar amounts. Absence of hits is recorded as "no adverse documented record found", never as "verified trustworthy".
- **Not legal or investment advice; defense-only posture.** Findings describe recognition and consumer protection. Never produce guidance for designing deceptive practices.
- **Redact the user's PII** when quoting their material into the report file.

## Inputs to collect

- **Subject + exact identifiers** — company name (legal or common), website URL, or product/brand name (+ maker if known). If ambiguous ("Delta"), ask once; one clarification round max, then commit with the stated assumption.
- **Region / market** — default US / English-language sources; enforcement and complaint coverage differ by country. Foreign-parent companies: HQ labeled, U.S.-facing conduct in scope.
- **User's angle** — buying decision, subscription, already a customer with a problem, research/writing, general curiosity. Sets check-line priority (a pre-purchase check weights C5/C7; a due-diligence dig weights C2/C3).
- **Output location** — default `corp-check_<slug>_<YYYY-MM-DD>.md` in the working directory; use the user's path if given.
- **Output mode** — `file` / `chat` / `both` (default `file`, from `corpcheck.config.json`; editing the default in this bullet changes the skill's baked-in default). State the active mode once at intake — e.g. *"Full report → file (default). Say 'in chat' to print full stages here, 'both' for both."* — and honor any-time switches for the rest of the check.
- **Today's date** — anchor time-sensitive queries to it (`<company> lawsuit 2026`, `<company> FTC action <year>`).

## Procedure

### Stage 0 — Intake (no searching)

1. Capture today's date as `YYYY-MM-DD` and the subject's exact identifiers. Reason: enforcement records churn — a company's posture from two years ago may be pre- or post-consent-order; date-anchored queries catch current status, not stale priors.
2. Classify the subject type (company / website / product-brand) and identify the angle. Load the corporate register's pattern index at the same time. Reason: every downstream line keys off the resolved legal parent, not the brand on the box.

### Stage ½ — Smoke test (≤2 network calls, target: under a minute)

3. Run the smoke checklist from `references/smoke-test.md`: ① **resolve the entity** — canonical company + official domain from major-brand knowledge; if unfamiliar, spend the ≤2 network calls on identity searches (`<name> company official site`, `<brand> parent company`); ② **verify website authenticity** when a URL was supplied (one passive fetch allowed — footer legal name, contact, checkout domain); ③ **register lookup** on the resolved entity *and* its parent chain, per the register's lookup rules. Reason: identity + register are the two things knowable in seconds, and impersonation is decidable from the material itself — searching first adds minutes to conclusions the input settles.
4. **If a decisive impersonation tell fires on a supplied URL** (brand-in-domain-but-not-the-brand, lookalike domain, fetched page claiming the brand but pointing elsewhere): deliver the **final snap verdict** — 🔴 High, labeled `snap`, "this is not <company>'s real site" — with the do/don't (typed official domain, report path) and the `document` offer. No further research, no report file. Reason: an impersonation verdict is about the *site*, and the site's own domain settles it.
5. **If the register hits** (the entity or its parent is a register company): deliver the **snap preview** — identity line, the register row's DP-IDs + tier + notes, a band preview labeled `register — as of knowledge-base cutoff 2026-09-19`, the explicit caveat (*documented record, not current status — remediation, newer actions, and positives unchecked*), and a **fast-path Stage-1 plan** targeting the documented lines plus a currency sweep (has anything changed since the cutoff?) plus C8. Then the gate. Reason: the user asked "what's on this company's record" — the register answers in seconds, but companies remediate, statuses move, and balance requires evidence the register doesn't carry; so it's a preview with a fast path, never a final verdict.
6. **If nothing fires** (no impersonation tell, no register hit): state "no documented record in the dark-patterns register — absence ≠ clean" and **continue directly into Stage 1 in the same turn**. Most honest companies live here; the smoke test must never make a thin record feel like an all-clear.

### Stage 1 — Triage (light and fast)

7. Run **10–14 parallel web searches**, snippet-first, spread across the applicable check lines per the guides — **C8 is always in the sweep**. Standard batteries: `<company> FTC action`, `<company> lawsuit`, `<company> class action`, `<company> complaints`, `<company> scandal`, `<company> reviews`, plus the angle-priority queries from the guides. Date-anchor time-sensitive queries. **Fetch at most 3–5 pages** — the regulator action worth confirming, the BBB profile, one settlement or press page. **No subagents.** Reason: Stage 1's promise is a fast, broad first read; every fetch it skips is time saved deciding whether to dig.
8. Map every observed signal to the register's DP-IDs where one fits, and record findings with confidence tags (`[Documented]` / `[Reported]` / `[Inferred]`). Write the **coverage map** and the provisional **verdict + balance readout** per the rubric — Stage-1 verdicts are always labeled *provisional* (register previews keep their `register` label; snap verdicts keep `snap`). Reason: "matches DP-SUB-01 cancellation labyrinth — FTC v. <company>, consent order 2025" is checkable and defensible; "has lawsuits" is neither. Score the initial **ripeness gauge** per `references/ripeness-rubric.md` — a prospect estimate, labeled as such. Reason: the go/stop decision needs both what the record shows (verdict) and whether digging further pays (yield).
9. Create the **report file** now — meta header, entity profile, verdict box, evidence by check line, coverage map, consumer takeaways, and the full ledger (query log, findings index, lead pool, verdict history — the register row enters the findings index as its first entries when applicable). In `chat` output mode, skip the file — the Stage-1 response carries the full stage content per the output contract; a file requested mid-check catches up at the next stage boundary. Reason: the file is the state container; a later session resumes from the ledger without re-searching.
10. Deliver the Stage-1 chat response: verdict box, key findings with DP-ID mapping, coverage map, ripeness gauge + overall line, consumer takeaways (if the user is mid-decision, what matters *now*), default Stage-2 plan, command hint — in `chat`/`both` output mode, this response carries the full stage content instead (output contract). Reason: chat is the decision surface; the file is the archive — and in `chat` mode, chat is also the archive.

### Between stages — the gate

11. End every stage response with the plan and this hint, verbatim in spirit: `Reply "go" to run this plan · describe a different direction to customize · "stop" to consolidate the final report.` After a **snap verdict** (impersonation), the gate reads: `Say "document" for the archived report (pattern documentation, sources) · describe a different direction to customize · "stop" to finish here.`
   - `go` / `check` / `next` / `continue` / `dig` / `yes` → execute the default plan verbatim. Do not re-plan, do not re-ask.
   - `document` (after a snap verdict) → write the archived report on the impersonation finding with its evidence chain. The band is not expected to move.
   - Substantive text → custom stage: restate your interpretation in one line, plan to match, execute. Ask one question only if genuinely ambiguous.
   - `stop` / `done` / `enough` / `finish` → consolidate (step 16).
   - `go` when every applicable line is already 🔵/➖ with a stable verdict, **or when the overall ripeness gauge reads 🔴** → push back **once** with the evidence (last stage's novelty rate, empty lead pool), offer the single most-targeted option; if the user insists, run a minimal stage.

### Stage N (N ≥ 2) — Verify

12. Execute the approved plan. Default budget: 8–12 searches + 4–8 fetches; one subagent per target check line, spawned in parallel when available, serial otherwise. Reason: parallelism makes a multi-line dig affordable; serial fallback keeps the skill portable.
13. Enforce ledger discipline — **never re-run a logged query**; check the findings index before recording (a repeat is corroboration attached to the existing finding ID); park promising unfetched results in the **lead pool** instead of chasing them mid-stage.
14. Record findings as: one-line finding + source name + URL + date + check line + DP-ID (where one fits) + confidence tag. Contradictions (stellar ratings + damning docket) are surfaced explicitly, never silently resolved — the balance readout is where they get weighed.
15. Close the stage: update the report file, **re-score the verdict, coverage, balance, and ripeness gauge** for every touched line, then deliver the stage response: banner, 3–6 new findings (🆕) with DP-ID mapping, verdict box, coverage map, ripeness gauge + overall, next default plan (ordered by relevance × yield), command hint. In `chat`/`both` mode the stage response carries the full stage content (every finding, full citations) per the output contract, and the report-file update is skipped in `chat` mode.

### Consolidate

16. On stop: restructure the report file into the final **company dossier** — verdict with confidence and evidence chain + balance readout; entity profile & ownership lineage; the record by theme (enforcement, litigation, dark patterns with DP-IDs, complaints, scandals, pricing history table if applicable, privacy, sector); **positives & reputation** as a first-class section; balanced synthesis (what the total picture supports, what it doesn't); event timeline with a date-precision ladder (`YYYY-MM-DD` → `YYYY-MM` → `c. YYYY` → `Date uncertain`); consumer takeaways; what was checked vs not; gaps & caveats; tiered sources. Chat response: verdict box, one-paragraph basis, final gauge statement (why further stages would not pay — or what remains open), file path — in `chat`/`both` mode the full final report is delivered in the chat response instead (or in addition). The consolidated file must stand alone for a reader who never saw the stages — in `chat` mode, that reader reads the chat.

## Output contract

- **Snap verdicts (impersonation):** ultra-short chat response per `references/smoke-test.md`; **no report file** unless `document` is requested.
- **One cumulative report file** for staged checks, `corp-check_<slug>_<YYYY-MM-DD>.md` (creation date; collision → `-v2`), updated every stage, finalized on stop. In `file` mode (the default), never paste the full file into chat — link it and summarize.
- **Output modes** (default `file`; precedence: the user's in-chat choice > `corpcheck.config.json` → `"output_mode": "file" | "chat" | "both"`, absent file/field = `file` > this contract's default):
  - `file` — chat responses are highlight summaries (verdict box, key findings, coverage map, gauge, plan); the full cumulative report lives in the report file.
  - `chat` — the complete content of each stage prints to the chat response: stage banner, **every** finding recorded this stage with its full citation (finding + source + URL + date + check line + DP-ID where one fits + confidence tag — no 3–6 cap), verdict box with balance readout, coverage map, ripeness gauge with legend, the stage's **ledger delta** (queries run, new finding IDs, lead-pool changes — the cumulative ledger is not reprinted, only the delta), then the plan. No report file is written unless requested; consolidation delivers the full final report in chat.
  - `both` — full stage content in chat **and** the report file maintained as in `file` mode.
  - Snap verdicts and register previews are unchanged in every mode (they are already complete responses); the `document` pass follows the active mode.
- **File sections, in order:** meta header (entity · legal parent · subject type · region · created · last updated · stage count · status) · Verdict Box (band + balance) · Entity Profile & Ownership · The Record by Theme (H3 per theme; findings cited; 🆕 marks current-stage additions) · Positives & Reputation · Balanced Synthesis · Event Timeline · Coverage Map · Ripeness Gauge (current table + overall line) · Consumer Takeaways · Gaps & Caveats · Sources (tiered, with access dates) · Appendices A–E: the ledger (A queries · B findings · C leads · D verdict history · E gauge history).
- **Every stage's chat response ends with the verdict block, then the ripeness gauge (with legend), then the plan block.** Verdict, coverage, and gauge legends rendered every time — a reader joining at Stage 3 must understand 🟠 and 🟡 without archaeology.
- **Citations:** inline Markdown links with the source name visible and access date; every non-trivial finding cited. Review-site entries are cited as the platform + date, not as verified fact.
- **No fabricated anything.** If a check line came back empty, that's the finding — recorded in coverage, echoed in Gaps & Caveats.

## Source hierarchy (use in this order of preference)

1. **Regulator & law-enforcement** — FTC, CFPB, SEC, FCC, DOJ, state AGs, CPSC, NHTSA, DOT, court records
2. **Primary corporate** — SEC filings, official settlement/administrator pages, court-ordered remediation program pages
3. **Litigation records** — dockets and class-action administration sites (trackers are leads, not endpoints)
4. **Consumer-advocacy & expert** — BBB business profiles, Consumer Reports, JD Power
5. **Reputable journalism** — Reuters, WSJ, Bloomberg, major consumer/tech/business press, named authors
6. **Review & complaint platforms** — Trustpilot, Sitejabber, app stores: evidence of *reports*, not proof of conduct; note review-manipulation risk in both directions
7. **Community** — Reddit, niche forums: discovery and corroboration, labeled as community-sourced
8. **Slop** — SEO farms, AI mills, undated blogs: never cited

A 🔴 verdict requires tier 1–3 documentation of an adjudicated or formally resolved matter naming the entity (or its subsidiary/brand). Tier-5/6 complaint volume alone caps at 🟡. The corporate register may *preview* 🔴/🟠 (labeled `register`) but only current tier 1–3 verification firms it. Lack of evidence is not evidence of virtue — and complaint volume is not proof of deception; weigh recency, volume, specificity, and company size.

## Failure handling

- **Ambiguous entity** — resolve to the most prominent same-named company, state the assumption, proceed; one clarification round max.
- **Private or thin-record company** — report honestly: "no adverse documented record across C1/C2/C3; absence is not verification" (🟡 unverifiable or 🟢 per the rubric). Private companies have no SEC line; note the reduced visibility as a gap.
- **Register vs. current record contradiction** — current sources show remediation, dismissal, or vacatur where the register shows action: show the movement per the rubric ("register preview 🟠 → Stage 2: action dismissed 2026-04, 🟡"), and say what changed. The register is a preview, never a verdict.
- **Defunct / renamed / acquired entity** — the register flags defunct primaries; renames and acquisitions reset name-recognition but not the record — check the lineage under old names (C1) and attribute findings to the entity that existed at the time.
- **Foreign parent** — HQ labeled; U.S.-facing conduct in scope per the knowledge base's geographic rule.
- **Mixed record** — both sides in the findings; the balance readout states which way the documented evidence leans and why; confidence reflects the tension.
- **Paywalled or bot-walled source** — dead-end lead, note the gap, continue. One Wayback Machine snapshot fetch of the specific page is permitted as a secondary source, labeled with its archive date (an archived page evidences past state, not current state — say which). Never invent contents.
- **Corrupted or garbled search output** — discard the corrupt portion, use only clean source-attributed results; if an entire result was unusable, one rephrased query (logged as new). Never cite from garbled text.
- **Session ended mid-check** — on return, read the report file, rebuild state from the ledger, resume at the next stage. In `chat` mode there is no file to rebuild from — the check restarts; surface that trade-off when the user picks `chat` (`both` keeps the file).
- **User pivots to a new company** — mini-consolidate, start a new check file.

## Examples

**Example 1 — register hit, snap preview, fast path.**
Input: "background check on SiriusXM before I resubscribe."
Stage ½ (under a minute, zero searches — major brand, no URL): entity = Sirius XM Holdings, official siriusxm.com; register hit: **DP-SUB-10 service doom loops, tier T2 — NY AG + CFPB cancellation actions (2024/25)**. Snap preview: **🔴 zone (T1/T2 → red-zone preview), labeled `register`** with the not-current-status caveat. Fast-path plan: verify current status of the CFPB/NY AG resolutions + whether cancellation flow changed + C5 complaint sweep + **C8 positives**. User replies "go" → Stage 1 confirms the consent order's terms and relief, the post-order cancellation-flow coverage, mixed-but-improving complaint boards, and SiriusXM's content-service reputation (C8). Verdict: **🔴 documented deception record, High — remediation noted in balance: Mixed**. One more verify stage on C3 (pending class actions) if ordered; consolidation on stop.

**Example 2 — no register hit, clean record, balance works.**
Input: "vet Anker — the charger brand. Worth trusting?"
Stage ½: Anker Innovations → not in the register; no URL to verify. "No documented record — absence ≠ clean" → straight into Stage 1: C2 clean (no FTC/CPSC actions found), C5 normal-scale complaint noise with responsive handling, C8 strong (Consumer Reports recommendations, tech-press standing, warranty reputation). Verdict: **🟢 no adverse documented record found across C1/C2/C3/C5/C8/C9 — Medium-High, balance: Favorable (with normal at-scale friction)**. Never "verified trustworthy".

**Example 3 — product → parent chain.**
Input: "is Tide involved in shady stuff? Saw something about bottle sizes."
Stage ½: Tide → **Procter & Gamble** (parent chain); register hit on the Tide row: **DP-QTY-03 serving-count/dose manipulation — documented (T4, no enforcement)**. Snap preview: **🟠 (register)** + note. Fast path: C4/C7 (shrinkflation documentation, packaging/price history table) + C8. The check file is `corp-check_tide-pg_…` with findings attributed to the brand, entity attributed to the parent.

**Example 4 — impersonation snap.**
Input: "is siriusxm-billing-payments[.]com their real billing site?"
Stage ½ (zero fetches needed): C-W1 brand-in-domain-but-not-the-brand [Decisive] — the domain is not siriusxm.com (major-brand knowledge). Final snap: **🔴 this is not SiriusXM's site — High (snap)**; do/don't: type the official domain yourself, never pay/log in via the link, report to SiriusXM's abuse channel + FTC. `document` offered; done.
