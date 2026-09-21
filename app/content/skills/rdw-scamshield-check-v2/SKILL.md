---
name: rdw-scamshield-check-v2
description: Staged background-check research on e-commerce content — a product listing, an online store or website URL, a TikTok/Facebook/Instagram post or ad, a suspicious email, or an online seller's name/handle. Use when the user asks to verify, vet, or check whether something for sale online is legit, fake, counterfeit, a clone, or a known scam pattern; whether a store, marketplace offer, seller, or fishy order/invoice/delivery/Zelle email can be trusted; or when screening a product for imitations and counterfeits before buying. Checks consumer advisory portals (FTC, BBB, IC3), complaint boards, review sites, seller feedback, forums, domain forensics, and counterfeit/clone signals. Opens with a zero-search smoke test that snaps decisive tells to an instant verdict; every staged response ends with an evidence-coverage map, a color-coded risk verdict, and a ready-to-approve next-stage plan.
---

# ScamShield Check v2 — smoke test first, then staged background checks

Background checks fail in two familiar ways: a single-pass "looks fine to me" that misses the BBB Scam Tracker reports, the three-week-old WHOIS record, or the Reddit thread where forty people never got their order — or an exhaustive forensic deep-dive the user never asked to pay for. This skill splits the difference in **three tiers**. **Stage ½ smoke test**: a zero-search, zero-fetch pass over the material itself — a seasoned reader flips to the sender line, the payment ask, or the funnel domain and knows in seconds; if a decisive tell fires, the verdict is delivered **immediately** (snap verdict) and all research becomes optional documentation. **Stage 1 triage**: a light snippet-first sweep across ten standard check lines, for subjects the smoke test can't settle. **Verify stages**: dig the flagged lines — but only when the user orders them, one bounded stage at a time. Findings map to documented scam-technique IDs (T-0xxx) from the technique catalog, so a verdict says *"matches T-0401 off-platform payment pressure — FTC-documented"*, not a vibe.

## When to scope down

Not every question needs the machinery. A single factual ask ("does Zelle have buyer protection?") gets a search and an answer — no stages, no file. An education ask ("what are common puppy scams?") gets an answer straight from the technique catalog. The full workflow is for vetting a **specific subject**: "is this store legit", "check this seller before I buy", "is this email a scam", "is this product a counterfeit". One subject = one check; if the user drops a bundle (an email pointing to a store run by a seller), treat it as ONE investigation — pick the primary subject (usually the store or seller), treat the rest as evidence. Comparisons ("which of these three sellers is safer") = separate checks, one file each.

## Key concepts

- **Smoke test (Stage ½)** — zero-search checklist of decisive static tells (sender-identity failure, near-diagnostic asks, brand-clone domains, funnel mismatches…) with inline false-positive guards. Any decisive tell → **snap verdict** (🔴, High, labeled `snap`), no research, no report file. Full checklist and rules: `references/smoke-test.md`.
- **Subject types** — the five things this skill vets: `product listing`, `website/store`, `social post/ad` (TikTok, Facebook, Instagram), `suspicious email`, `online seller`. Stage 0 classifies the subject and loads **only the matching guide** from `references/subject-check-guides.md`.
- **Check lines** — the 10 standard verification dimensions: C1 Advisory portals & scam databases · C2 Review & complaint boards · C3 Domain & identity forensics · C4 Counterfeit, clone & imitation check · C5 Platform standing & enforcement record · C6 Price & listing plausibility · C7 Payment & checkout behavior · C8 Impersonation & contact-initiation analysis · C9 Community & social sentiment · C10 Official records & enforcement. Not all apply to every subject — the guides give the priority order.
- **Technique catalog** — 13 families / 57 documented seller-scam techniques with stable IDs (T-0401 off-platform payment pressure, T-0302 brand-impersonation clone store, T-0603 invoice phishing…). Findings map observed signals to these IDs. Full catalog, signal library, payment-rail table, and reporting directory: `references/technique-catalog.md`.
- **Risk verdict** — 🟢 no adverse findings · 🟡 caution · 🟠 multiple red flags · 🔴 scam pattern match. Always with confidence (High/Medium/Low) and named evidence. Scoring anchors and honesty rules: `references/verdict-rubric.md`.
- **Coverage map** — per-check-line status: ⚪ unchecked · 🔵 checked, clean · 🚩 checked, flagged · 🔴 checked, hit · ➖ not applicable. The honesty device: a verdict is only as strong as its coverage.
- **Ripeness & relevance gauge** — per-line and overall readout of how much *new* decision-relevant evidence one more verify stage would surface: 🟢 75–100 fresh · 🟡 50–74 yielding · 🟠 25–49 thinning · 🔴 0–24 exhausted, each scored from ledger signals (novelty rate, lead-pool depth, tier-ceiling gap) and each line rated for relevance to the user's worry. Stage-1 scores are prospect estimates. The gate's price tag, kept strictly separate from the verdict. Full rubric and formats: `references/ripeness-rubric.md`.
- **Research ledger** — query log, findings index, lead pool, verdict history, gauge history, persisted in the report file. What makes multi-stage checks work without repeating searches.
- **Output mode** — where the full stage content goes: `file` (default — highlights in chat, full cumulative report in the report file) · `chat` (the complete content of every stage prints to the chat response; no file unless requested) · `both`. Default set by `scamshield-check.config.json` (`"output_mode"`; absent file = `file`); the user's in-chat choice always wins and is noted in the report meta. Formats: output contract.

## Safety rules (read before any check)

- **Suspicious email = static analysis only.** Never click links, never reply, never visit URL(s) from the email, never open attachments. Extract domains/URLs as *text* and reputation-check them via search queries (`<domain> phishing`, `<domain> scam`), not by fetching.
- **Suspect stores = passive inspection only.** Fetching public pages to inspect them is fine. Never enter payment data, create accounts, message the seller, or download files from a subject under investigation.
- **Verdict discipline.** Evidence-linked language: "domain registered 3 weeks ago (WHOIS)" not "obviously run by criminals". Distinguish *documented* (regulator action, BBB/FTC reports, named complainants) from *inferred* (signal cluster). Never call a business a scam beyond what the evidence shows; honor gray zones (disclosed replicas, gray-market goods, dropship delays are not fraud).
- **No fabrication.** Every cited complaint, review, or report must actually exist in fetched/snippet-verified results. Never invent URLs, dates, or complaint counts. Absence of hits is recorded as "no adverse record found", never as "verified safe".
- **Defense-only posture.** Findings describe recognition and avoidance. Never produce how-to-commit guidance, even when the mechanics are documented in the catalog.
- **Redact the user's PII** (their name, address, order numbers) when quoting their material into the report file.

## Inputs to collect

- **Subject + exact identifiers** — URL (store, listing, or post), seller name + platform + handle, product brand + model + seller line, or the full email text pasted verbatim. If the user names a category ("some TikTok shop"), ask once for the specific shop/link; one clarification round max, then commit.
- **Region / market** — default US / English-language sources; scam-report coverage differs by country.
- **User's situation** — *screening* (deciding whether to buy — the default) or *already paid / already clicked* (→ victim path below). This changes the whole response shape.
- **User's angle** — what specifically worries them (counterfeit? non-delivery? seller reputation?). Sets check-line relevance.
- **Output location** — default `scam-check_<slug>_<YYYY-MM-DD>.md` in the working directory; use the user's path if given.
- **Output mode** — `file` / `chat` / `both` (default `file`, from `scamshield-check.config.json`; editing the default in this bullet changes the skill's baked-in default). State the active mode once at intake — e.g. *"Full report → file (default). Say 'in chat' to print full stages here, 'both' for both."* — and honor any-time switches for the rest of the check.
- **Today's date** — anchor time-sensitive queries to it (`<store> scam 2026`, `<seller> complaints <year>`).

## Procedure

### Stage 0 — Intake (no searching)

1. Capture today's date as `YYYY-MM-DD` and the subject's exact identifiers. Reason: scam infrastructure churns fast — a store's record from 18 months ago is archaeology; date-anchored queries catch current reports and current *absence*.
2. Classify the subject type (product / store / post / email / seller; bundle rule above) and read **only the matching guide** in `references/subject-check-guides.md`. Load the technique catalog's signal library at the same time.
3. **Victim-path check:** if the user already paid, clicked, or shared data — run the smoke test and Stage 1 triage, but center the first response on damage control: preserve evidence (screenshot listing, order, emails, payments), the escalation ladder (seller in writing → platform claim *inside its deadline* → card-issuer dispute → reports), the reporting directory (catalog §6), and the recovery-fraud warning (nobody legitimate contacts victims first or charges a fee to recover money). The background check then documents the pattern for their claim.

### Stage ½ — Smoke test (zero searches, target: seconds)

4. Run the smoke checklist for the subject type from `references/smoke-test.md` over the supplied material — sender line, payment ask, funnel/landing domain, visible payment rails. **Zero network calls.** Reason: a decisive tell observed directly is already a 🔴 rubric anchor (near-diagnostic signal or brand-clone confirmation) — searching first adds minutes to a verdict the material itself settles, and delays the do/don't advice the user actually needs.
5. **If any [Decisive] item fires:** deliver the snap response immediately — verdict box (🔴, High, labeled `snap`), the fired tells with item IDs + T-ID mapping, 2–3 do/don't bullets, and the gate with the `document` option. **No searches, no report file.** Reason: the user asked "is this a scam?"; the fastest correct complete answer is the product. The archived report is documentation, not verification — it is offered, not forced.
6. **If only [Corroborating] items fire:** carry them into Stage 1 as opening findings (the sweep starts smarter). **If nothing fires:** Stage 1 unchanged. Most honest-but-odd subjects live here — the smoke test must never make thin evidence feel decisive.

### Stage 1 — Triage (light and fast)

7. Run **10–14 parallel web searches**, snippet-first, spread across the subject's applicable check lines per its guide. Include the standard sweeps: `<identifier> scam`, `<identifier> complaint`, `<identifier> reviews`, plus the guide's subject-specific queries. **Fetch at most 3–5 pages** — WHOIS/domain-age lookup, the advisory-portal hit worth confirming, or a passive look at the store's own page. **No subagents.** Reason: Stage 1's promise is a fast verdict preview; every fetch it skips is time saved deciding whether to dig.
8. Map every observed signal to the catalog's technique IDs where one fits. Write the **coverage map** and the provisional **risk verdict** per the rubric — Stage-1 verdicts are always labeled provisional (snap verdicts, which precede this stage, are labeled `snap` instead). Reason: "matches T-0301 disposable storefront (domain 22 days old + no contact info + 85%-off pricing)" is checkable and defensible; "seems scammy" is neither. Score the initial **ripeness gauge** per `references/ripeness-rubric.md` — a prospect estimate, labeled as such. Reason: the go/stop decision needs both what the record shows (verdict) and whether digging further pays (yield).
9. Create the **report file** now — meta header, subject profile, verdict box, evidence by check line, coverage map, recommended actions, and the full ledger (query log, findings index, lead pool, verdict history, gauge history). In `chat` output mode, skip the file — the Stage-1 response carries the full stage content per the output contract; a file requested mid-check catches up at the next stage boundary. Reason: the file is the state container; a later session resumes from the ledger without re-searching.
10. Deliver the Stage-1 chat response: verdict box, key findings with T-ID mapping, coverage map, ripeness gauge + overall line, recommended actions (if the user is about to transact, the do/don't from the catalog applies *now*), default Stage-2 plan, command hint — in `chat`/`both` output mode, this response carries the full stage content instead (output contract). Reason: chat is the decision surface; the file is the archive — and in `chat` mode, chat is also the archive.

### Between stages — the gate

11. End every stage response with the plan and this hint, verbatim in spirit: `Reply "go" to run this plan · describe a different direction to customize · "stop" to finalize the background-check report.` After a **snap verdict**, the gate reads: `Say "document" for the full archived report (pattern documentation, sources, ledger) · describe a different direction to customize · "stop" to finish here.`
   - `go` / `check` / `next` / `continue` / `dig` / `yes` → execute the default plan verbatim. Do not re-plan, do not re-ask.
   - `document` (after a snap verdict) → run the documentation pass: the Stage-1 search sweep (7) against the pattern that fired, write the full report file with the snap verdict's evidence chain, deliver the Stage-1-style response. The band is not expected to change; if documentation contradicts the snap, show the movement per the rubric.
   - Substantive text → custom stage: restate your interpretation in one line, plan to match, execute. Ask one question only if genuinely ambiguous.
   - `stop` / `done` / `enough` / `finish` → consolidate (step 16). After a snap verdict with no documentation requested, consolidation = a final one-paragraph verdict confirmation; the file was never created, so none is needed.
   - `go` when coverage is already complete on all applicable lines, **or when the overall ripeness gauge reads 🔴** → push back **once** with the evidence (last stage's novelty rate, empty lead pool), offer the single most-targeted option; if the user insists, run a minimal stage.

### Stage N (N ≥ 2) — Verify

12. Execute the approved plan. Default budget: 8–12 searches + 4–8 fetches; one subagent per target check line, spawned in parallel when available, serial otherwise. Reason: parallelism makes a multi-line dig affordable; serial fallback keeps the skill portable.
13. Enforce ledger discipline — **never re-run a logged query**; check the findings index before recording (a repeat is corroboration attached to the existing finding ID); park promising unfetched results in the **lead pool** instead of chasing them mid-stage.
14. Record findings as: one-line finding + source name + URL + date + check line + confidence tag (`[Documented]` regulator/press/official record · `[Reported]` consumer complaints/reviews, multiple or single labeled · `[Inferred]` signal-cluster match, no external record yet). Contradictions (praise on one board, reports on another) are surfaced explicitly, never silently resolved.
15. Close the stage: update the report file, **re-score the verdict, coverage, and ripeness gauge** for every touched line, then deliver the stage response: banner, 3–6 new findings (🆕) with T-ID mapping, verdict box, coverage map, ripeness gauge + overall, next default plan (ordered by relevance × yield), command hint. In `chat`/`both` mode the stage response carries the full stage content (every finding, full citations) per the output contract, and the report-file update is skipped in `chat` mode.

### Consolidate

16. On stop: restructure the report file (if one exists) into the final background check — verdict with confidence and its evidence chain; findings grouped by theme; red flags → technique mapping; gray-zone and mitigating evidence; what was checked vs not; recommended actions (avoid / proceed-with-precautions / recovery ladder if victim); where to report; gaps & caveats; tiered sources. Chat response: verdict box, one-paragraph basis, final gauge statement (why further stages would not pay — or what remains open), file path (or "no file was needed — snap verdict stood on direct observation") — in `chat`/`both` mode the full final report is delivered in the chat response instead (or in addition). The consolidated file must stand alone for a reader who never saw the stages — in `chat` mode, that reader reads the chat.

## Output contract

- **Snap verdicts:** ultra-short chat response per `references/smoke-test.md`; **no report file** unless `document` is requested. When requested, the file is the Stage-1 file with the snap verdict as its verdict box and the smoke items recorded as findings.
- **One cumulative report file** for staged checks, `scam-check_<slug>_<YYYY-MM-DD>.md` (creation date; collision → `-v2`), updated every stage, finalized on stop. In `file` mode (the default), never paste the full file into chat — link it and summarize.
- **Output modes** (default `file`; precedence: the user's in-chat choice > `scamshield-check.config.json` → `"output_mode": "file" | "chat" | "both"`, absent file/field = `file` > this contract's default):
  - `file` — chat responses are highlight summaries (verdict box, key findings, coverage map, gauge, plan); the full cumulative report lives in the report file.
  - `chat` — the complete content of each stage prints to the chat response: stage banner, **every** finding recorded this stage with its full citation (finding + source + URL + date + check line + T-ID where one fits + confidence tag — no 3–6 cap), verdict box, coverage map, ripeness gauge with legend, the stage's **ledger delta** (queries run, new finding IDs, lead-pool changes — the cumulative ledger is not reprinted, only the delta), then the plan. No report file is written unless requested; consolidation delivers the full final report in chat.
  - `both` — full stage content in chat **and** the report file maintained as in `file` mode.
  - Snap responses are unchanged in every mode (nothing exists yet to expand); the `document` pass follows the active mode.
- **File sections, in order:** meta header (subject · type · region · created · last updated · stage count · status) · Verdict Box · Subject Profile · Evidence by Check Line (H3 per line; findings cited; 🆕 marks current-stage additions) · Red Flags → Technique Mapping · Coverage Map · Ripeness Gauge (current table + overall line) · Recommended Actions · If Victim: Recovery Ladder · Where to Report · Gaps & Caveats · Sources (tiered, with access dates) · Appendices A–E: the ledger (A queries · B findings · C leads · D verdict history · E gauge history).
- **Every stage's chat response ends with the verdict block, then the ripeness gauge (with legend), then the plan block.** Verdict and gauge legends rendered every time — a reader joining at Stage 3 must understand 🟠 without archaeology.
- **Citations:** inline Markdown links with the source name visible and access date; every non-trivial finding cited. Review-site entries are cited as the platform + reviewer date, not as verified fact.
- **No fabricated anything.** If a check line came back empty, that's the finding — recorded in coverage, echoed in Gaps & Caveats.

## Source hierarchy (use in this order of preference)

1. **Regulator & law-enforcement** — FTC alerts/actions, IC3, state AG, USPIS, CPSC, court records
2. **Official platform & payment-rail policy** — marketplace guarantee pages, Zelle/PayPal official terms
3. **Consumer-advocacy & NGO** — BBB (Scam Tracker + business profiles), Consumer Reports
4. **Reputable journalism** — named-outlet scam/fraud investigations
5. **Review & complaint platforms** — Trustpilot, Sitejabber, ResellerRatings: evidence of *reports*, not proof of guilt; note review-manipulation risk (a wall of 5-stars is a signal, not an all-clear)
6. **Community** — Reddit, niche forums, ad comments: discovery and corroboration, labeled as community-sourced
7. **Aggregators** — ScamAdviser-class site scorers: leads, never endpoints
8. **Slop** — SEO farms, AI mills, undated blogs: never cited

A 🔴 verdict requires tier 1–4 documentation OR a near-diagnostic signal from the catalog (the five in §2 of the technique catalog) observed directly — **or** the smoke-test equivalent: a decisive item from `references/smoke-test.md`, which is one of those two anchors observed in static material. Clusters of tier-5/6 signals alone cap at 🟠. Lack of evidence is not evidence of safety — and one batch of complaints is not proof of fraud; weigh recency, volume, and specificity.

## Failure handling

- **Thin or no record** — report honestly: "no adverse record found across C1/C2/C9; absence is not verification" (🟡 or 🟢 per the rubric, never 🔴 without evidence). New honest sellers exist; the rubric's false-positive rules apply.
- **Smoke-test false-positive guard** — if a decisive item's guard says fall through (unknown brand, possibly-legitimate ESP pattern, blocked images), it falls through; never fire a snap verdict on guarded-out evidence.
- **Mixed record** — both sides in the findings; state which looks weightier and why; reflect it in confidence.
- **Bot-walled or paywalled source** — record as a dead-end lead, note the gap, continue. Never invent contents.
- **Subject vanished mid-check** (store goes dark, listing removed) — that is itself a finding (T-0106 pattern); note date/time observed.
- **User asks for perpetrator detail** ("how do these fake stores get away with it") — answer at recognition level from the catalog; no operational guidance.
- **Session ended mid-check** — on return, read the report file, rebuild state from the ledger, resume at the next stage. In `chat` mode there is no file to rebuild from — the check restarts; surface that trade-off when the user picks `chat` (`both` keeps the file).
- **User pivots to a new subject** — mini-consolidate, start a new check file.

## Examples

**Example 1 — email, smoke test snaps it.**
Input: "got an email: 'Your USPS package is on hold — pay $1.99 redelivery fee: usps-delivery-fee[.]net'. Real?"
Stage ½ (seconds, zero searches): sender domain not usps.com → S-E1 sender-identity failure [Decisive]; carrier fee-by-link → S-E3 [Decisive] (T-0504). Snap verdict: **🔴 scam pattern match, High (snap)**. Response: don't click, track only at usps.com, report to USPIS + FTC — with `document` offered. No searches, no file. If the user says `document`: the sweep confirms the pattern in phishing reports (C1), full report file written.

**Example 2 — email with no visible ask, smoke falls through.**
Input: a "McAfee Total Security Team" renewal notice whose body is image-hosted and blocked.
Stage ½: sender is a random-string domain, not mcafee.com → S-E1 [Decisive] fires on the brand claim alone; reply-to on a newsletter ESP → S-E4/S-E6 corroborating. Snap verdict: **🔴 (snap)**, with the blocked-body ask honestly noted as unobserved. This is the case v1 spent minutes searching for — the material's own headers settle it.

**Example 3 — store via social ad, smoke partial, triage finishes it.**
Input: "is dealznike-outlet.shop legit? saw their ad on Instagram — Jordans 80% off."
Stage ½: S-W1 brand-in-domain-but-not-the-brand [Decisive] fires (nike.com is major-brand knowledge; this domain is not it) → snap 🔴 (snap) with T-0302. If instead the store were "kicks4less.shop" (no brand name), S-W3 is only corroborating → Stage 1 sweep: WHOIS 19 days old (C3), 80%-off pricing (C6), BBB + Reddit non-delivery reports on near-identical domains (C1/C9) → **🔴 High, provisional** — Stage 2 unnecessary; consolidation recommended.

**Example 4 — honest thinness, verdict restraint.**
Input: "check this Etsy seller, bohomade-ceramics — 12 sales, no reviews yet, I love the pieces."
Stage ½: nothing (no static tells exist for a clean new seller). Stage 1: no scam-database hits, no complaints, no reviews (C1/C2/C9 all clean), shop opened 2 months ago, listings show actual-item photos and shop policies are specific (C3/C6 clean). Verdict: **🟡 caution, Medium** — zero adverse findings, but a 2-month-old shop with no transaction history is unverifiable, not verified-safe. Proceed with protections only. The smoke test must not rush this case into a verdict.

**Example 5 — product counterfeit screen.**
Input: "is this $14 'Anker 100W' charger on a Walmart Marketplace seller real?"
Stage ½: S-T2 spec absurdity is corroborating only → fall through. Stage 1 flags C4 (price ~3× under Anker MSRP; seller not on Anker's authorized-seller page; stock photos), C5 (marketplace listing surface vs third-party counterparty), C1 (safety-counterfeit documentation — catalog notes 99% of counterfeit chargers failed UL safety testing). Verdict: **🟠 multiple red flags, Medium-High** — no scam report on this specific seller, but counterfeit risk on safety-critical electronics is documented category-wide. Default Stage 2: authorized-seller verification + seller review sweep.
