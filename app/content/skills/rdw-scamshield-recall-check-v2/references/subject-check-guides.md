# Subject Check Guides — product name · SKU/lot · website · social post · news article · recall message

Use as **checklists, not scripts**. After classifying the subject (Stage 0), read only the matching guide. Each guide gives: what to extract from the input, which check lines apply and in what priority, query patterns that actually reach the evidence, subject-specific verification moves, and the pitfalls that cause false verdicts. Universal check-line definitions (R1–R8) live in the SKILL.md; the agency routing matrix and all source URLs live in `recall-source-guides.md`. When a source named here is never touched in Stage 1, the coverage map must show the line as ⚪ — an unscanned line is a gap, not a clean result.

## Product / food name guide

Subjects: "was <brand> <product> recalled?", "is <food> part of the outbreak?", "any recalls on <brand> dog food?". The subject is the **brand + product**, not the category.

**Extract:** exact brand and product name (and sub-line/flavor/variety — recalls attach to varieties, not brands wholesale); package size; if available: UPC, lot/batch code, best-by date; where purchased (sets the R5 retailer surface); when purchased (a 2019 purchase has a different recall window than last week's).

**Check lines, priority order:** **R1 agency recall list (routed by product class)** · **R3 CDC outbreak layer** (food + illness angle) · **R6 press & news record** · R4 state distribution layer (if a recall is found — "was it distributed here?") · R5 retailer hub (if purchase-linked) · R2 agency databases (history depth: Enforcement Reports for Class II/III actions that never got press) · R8 community (last, for unreported-illness signals).

**Queries:** `site:fda.gov <brand> <product> recall` (or `site:fsis.usda.gov` / `site:cpsc.gov` per routing) · `<brand> <product> recall <current year>` · `<brand> <product> recall <year -1>` (history) · `<food> outbreak site:cdc.gov` · `<brand> recall site:<retailer>.com` · `<brand> <product> salmonella OR listeria OR E. coli OR cyclospora OR undeclared`.

**Verification moves:** route FIRST — the meat/dairy/produce/ supplement classification decides which agency page is the source of record (routing matrix, source guide §1); fetch the agency list page and search it for the brand; when a hit surfaces, capture the notice's specifics — announcement date, class (I/II/III), reason, lot codes/date ranges, distribution scope, remedy, conclusion status; for the outbreak angle, the CDC investigation page names states and case counts even when no recall exists; for old events, Enforcement Reports and the CPSC archive go deeper than press pages.

**Pitfalls:** brands share names across markets (US vs international) — confirm the jurisdiction; a *past, concluded* recall is not a current danger but IS the answer to "has it ever been recalled" — separate current from past by date, always; aggregator "recall list" pages are frequently stale or wrong (source guide §7) — a recall seen there is a lead, not a finding, until confirmed at the agency page; supplements and "natural" products are FDA-regulated food — don't misroute them to CPSC.

## SKU / lot / UPC code guide

Subjects: "check lot 24-081", "UPC 0 12345 67890 1 — is this the recalled one?", "best-by Aug 2026, plant code P-123". The subject is a **specific manufactured batch** — the most precise recall question there is.

**Extract:** the code(s) verbatim (lot, batch, UPC, model, serial, plant code, best-by/use-by date); product name + brand (routing); where the code is printed (package clues help the user re-find it); photo/date context if given.

**Check lines, priority order:** **R1 agency recall list (routed)** · **R5 retailer hub** (lot-level matching is exactly what retailers do best — non-authoritative but fastest) · R2 agency database detail (the full notice carries the lot list) · R6 press (lot lists often reprinted) · R3 CDC (illness-linked lots) · R4 state layer (distribution).

**Queries:** `"<lot code>" <brand> recall` (quote it — lot codes are exact-match strings) · `site:fda.gov <brand> recall` + scan the notice for the lot table · `<brand> recall lot codes list` · `site:corporate.walmart.com OR site:costco.com <brand> recall` (retailer lot-level posts) · for vehicles: `site:nhtsa.gov <make> <model> <year> recall` (campaign records by year/model; VIN-level lookup is the user's to do at nhtsa.gov/recalls — give them the link).

**Verification moves:** compare the user's code against the notice's affected-lot table character by character — an "O" vs "0" or transposed digit changes the answer; when the code doesn't appear in the affected table, say exactly that ("your lot is not in the affected range per the notice dated X") rather than "you're safe" — production runs after the fix exist; check whether the recall was **expanded** later (follow-up notices add lots — search the brand + "expanded recall").

**Pitfalls:** lot-code formats vary by manufacturer (some embed the plant and date — decode only if the notice explains its own format, never guess); a code found on an aggregator page must match the agency notice before driving a verdict; absence of the code from press summaries is not absence from the official table — the agency notice is the lot list of record.

## Product website guide

Subjects: a product/brand site the user is evaluating — "is this supplement site legit, and has their stuff been recalled?", a DTC brand's storefront. Two questions in one: the site's authenticity (family expertise) and the products' recall record.

**Extract:** full registrable domain; claimed manufacturer/distributor; product names + claims; contact info (real address/phone?); any "recall" or "news" page on their own site; cert/seal claims (USDA, GMP, third-party) — note whether they link to the issuer.

**Check lines, priority order:** **R1 agency recall list (routed)** · **R7 content authenticity** (the site's own claims: clone/impersonation tells, seal fraud) · **R6 press record** (investigations, FDA warning letters) · R2 agency enforcement history (FDA warning letters are searchable and often name the domain) · R8 community.

**Queries:** `<brand> recall site:fda.gov` · `<brand> FDA warning letter` · `<domain> scam` · `<brand> site:reddit.com` · `<brand> complaints` · `"<brand>" lawsuit OR FDA OR recall <year>`.

**Verification moves:** passive fetch of the site's own pages is allowed — check that contact info resolves to a real business, seals link to issuers, claims match the label reality; search FDA warning letters (fda.gov has a searchable index) — a warning letter is a regulator record that predates most recalls; if the site impersonates a known brand, that is the smoke test's domain (S-W2) and the authenticity readout takes over.

**Pitfalls:** a polished site is not evidence; https means nothing; absence of a recall record for a small DTC brand is expected, not reassuring — thin coverage is 🟡, not 🟢; gray-market/gray-label supplement sellers are a policy/quality gray zone, not automatically fraud.

**Safety:** passive reads only — never start checkout, never enter data, never download their files.

## Social post guide (TikTok / Facebook / Instagram)

Subjects: a post/video/ad claiming a recall, an outbreak, or a "recall refund" — "a TikTok says air fryers are catching fire", "this FB post says our formula was recalled". The subject is the **claim + its product**, and the two readouts split cleanly: authenticity of the post/claim, recall status of the product.

**Extract:** platform, account handle; the exact claim (what product, what hazard, what action it pushes); where the funnel points (link-in-bio domain, DM instruction); comment state (others reporting the same? "did yours too?"); account signals (age, content coherence); screenshots the user can paste.

**Check lines, priority order:** **R1 agency recall list (routed)** (the claim's truth is checked here) · **R3 CDC layer** (illness claims) · **R6 press record** (did any outlet cover it?) · **R7 content authenticity** (funnel, payment asks, impersonation — smoke items S-P1..S-P4) · R8 community (other users' reports).

**Queries:** `<brand> <product> recall site:cpsc.gov` (or routed agency) · `<brand> recall 2026` · `<brand> site:cdc.gov outbreak` · `<handle> scam` · `site:reddit.com <brand> recall TikTok` · `<claim keywords> hoax OR debunked OR confirmed`.

**Verification moves:** the claim is checked exactly like a product-name subject — routed agency sweep; the post's authenticity is separate: does it link to the agency page or to somewhere that wants something? Platforms amplify both genuine consumer warnings (often EARLIER than official notices — a real signal worth recording as community evidence) and engagement-bait panic (corroborating tell S-P3); when the agency record is silent, the honest pair is: authenticity 🟡 unverifiable + recall status 🟢 no record found (with dates), plus the R8 cluster reported for what it is.

**Pitfalls:** don't verdict the platform, verdict the post; a deleted or vanished post is a finding, not exoneration; virality is not verification in either direction; comment sections are curated — their *absence* (disabled comments on a recall claim) is itself a signal.

**Safety:** never engage with the post, account, or DMs from the check; never click tracked links directly — note the landing domain and apply the website guide's passive-fetch rules if it needs inspection.

## News article guide

Subjects: an article the user found or was sent — "this says my spinach brand was recalled, is it current?", a press piece claiming an outbreak link. Articles are evidence, not subjects, EXCEPT when they are the only thing being checked ("is this article real/current?").

**Extract:** outlet name + URL; publication date (critical — recall articles live for years and get re-crawled); the specific claim (brand, product, lots, hazard, agency named); whether it links the agency notice; whether it's an original report or syndicated/aggregated copy.

**Check lines, priority order:** **R1 agency recall list (routed)** (confirm the claim at the source of record) · **R6 press record corroboration** (did the named agency/other outlets report it?) · R3 CDC (illness claims) · R4 state layer (distribution claims) · R7 authenticity only if the "article" shows farm markers (S-A1) or funnel behavior.

**Queries:** `<brand> recall site:fda.gov` (routed) · `"<article headline key phrase>"` (find syndication + the original) · `<brand> recall <article's year>` + `<brand> recall <current year>` (is it still current?) · `<brand> recall concluded OR ended OR expanded`.

**Verification moves:** date-discriminate ruthlessly — a 2024 recall article surfacing in 2026 search results is archaeology unless the recall was never resolved; confirm at the agency page that the notice exists and check its **conclusion status** (ongoing vs completed — agency pages mark this); trace syndicated copies to the original outlet; if the article names lots/states, those feed the location table at map time.

**Pitfalls:** local-TV recall stories are usually legitimate but shallow (syndicated wire copy with the agency's specifics stripped) — use them as leads to the notice, not as the record; "expanded recall" follow-ups often outrank the original in search — read dates; a paywalled outlet's headline + date may be all that's visible — that's enough to route the agency check, which is the real answer anyway.

## Recall message guide (text / email / DM)

Subjects: a recall ALERT the user received — "is this recall text real?", "an email about my pressure cooker". The message is the claim-bearing subject; the product named in it is the routed sub-check.

**Extract (as text, defanged, user PII redacted):** sender address or number (the actual domain after @, not the display name) · reply-to if known · the specific ask (fee? card? call? click? "register"?) · any URL text (defanged: `gp-refund[.]net`) · claimed agency/brand/retailer · product named · any order/reference numbers.

**Check lines — narrow set:** **R7 content authenticity** (the smoke test's home turf: S-M1..S-M7) · **R1 agency recall list** (does the claimed recall exist at all?) · R6 press (documented scam campaigns get covered) · R5 retailer hub (if the message claims to be a retailer).

**Queries:** `<sender domain> phishing OR scam` · `<exact subject/keyword phrase> scam` (campaign reports) · `<brand> recall site:fda.gov` (routed — is the claimed recall real?) · `fake <retailer> recall text <year>` (documented campaigns).

**Verification moves — static first.** The institution test: real agencies and retailers (a) never ask for payment or a card to process a recall refund, (b) never run refunds through gift cards/wire/crypto, (c) don't funnel recall claims through call centers, (d) send from their own real domains. The verify-instead rule to give the user: open the agency's recall page or the retailer's own app/site yourself — typed, never the message's link — and look for the product there; no record there = the message's premise is fiction. Then the routed sweep answers whether the product has any real, unrelated recall record.

**Pitfalls:** retailers DO legitimately text real recall alerts — sender-domain match + no ask = fall through, check the claim at the retailer's hub; a real recall existing does NOT legitimize the message (scammers piggyback on real events — the message still fails the institution test); grammatical errors are not required (AI-written lures read clean); short-code senders can't be domain-checked — fall through, don't fire.

**Safety (hard rules):** never click, never reply, never call the numbers, never visit the URLs — reputation-check domains via search only; never open attachments; defang all URLs when writing them into the report.
