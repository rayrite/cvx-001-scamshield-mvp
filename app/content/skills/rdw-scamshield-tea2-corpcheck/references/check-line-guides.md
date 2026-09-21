# Check Line Guides — C1 Identity through C10 Sector overlay

Use as **checklists, not scripts**. After Stage 0 classifies the subject and the angle, these guides set each line's queries, what counts as a hit, and the pitfalls that cause false verdicts. Universal line definitions (C1–C10) live in the SKILL.md. When a line is never touched in a stage, the coverage map must show it ⚪ — an unscanned line is a gap, not a clean result. **C8 is never skipped in Stage 1.**

## C1 — Identity & ownership

**Purpose:** the canonical entity: legal parent, HQ, major brands/subsidiaries, M&A and rename lineage, defunct status. Every other line's findings attach to *this* entity.

**Queries:** `<company> parent company` · `who owns <brand>` · `<company> subsidiaries brands` · `<company> Wikipedia` (orientation only — never cite as primary) · `<company> acquired OR renamed <old name>` · `<company> SEC EDGAR CIK` (public companies).

**What counts as a hit:** a confirmed parent/ownership chain; a rename or acquisition that resets name-recognition; a defunct or dissolved status.

**Pitfalls:** the brand on the box is not the legal entity; an old scandal belongs to the entity that existed then (attribute, don't anoint); conglomerates own hundreds of brands — a subsidiary's finding does not automatically indict the parent (say which entity the documentation names); Wikipedia is orientation, not evidence.

## C2 — Regulator & enforcement record

**Purpose:** formal actions by FTC, CFPB, SEC, FCC, DOJ, state AGs, and sector regulators — resolved and pending.

**Queries:** `<company> FTC action OR complaint` · `<company> CFPB consent order` · `<company> SEC enforcement` · `<company> state attorney general settlement` · `<company> DOJ` · `<company> FTC returnon refund` (redress programs) · `<company> <sector> regulator fine`.

**What counts as a hit:** an agency press release, docket, consent order, or redress page naming the entity. Verify at the agency's own domain when fetched; press coverage is corroboration.

**Pitfalls:** an agency *complaint* is an allegation, a *consent order/settlement* is a resolution without admission, an *adjudicated finding* is the strongest of the three — label which; matters get dismissed and rules get vacated (date-check everything); warning letters and non-monetary actions are real but minor — tier them honestly; enforcement maps attention, not incidence (absence of actions ≠ cleanest company in the sector).

## C3 — Litigation & class actions

**Purpose:** current and past lawsuits naming the entity — class actions, MDLs, AG suits, notable individual suits.

**Queries:** `<company> class action <year>` · `<company> lawsuit settlement` · `<company> MDL` · `<company> pending litigation` · `site:<settlementadministrator> <company>` · `<company> settlement claims file`.

**What counts as a hit:** a docket, court order, or official settlement-administration page. Class-action tracker sites are **leads, not endpoints** — corroborate at a primary source before citing.

**Pitfalls:** filed suits are allegations until resolved — never phrase as findings; individual suits ≠ a pattern (look for MDLs and certified classes for pattern weight); companies this size are *always* in litigation somewhere — volume alone is not a signal; settlement with no admission is a resolution, not a confession; statutory exclusion deadlines matter for users ("claims file by …") — surface them when live; Stage-1 snippet mode cannot corroborate *status* at primary, and tracker pages routinely present closed matters as live — record litigation/enforcement status from trackers or snippets as `[Reported — status unverified]` and verify before any finding relies on it (live-run evidence: an undated tracker page showed a suit dismissed in 2018 as pending).

## C4 — Dark-pattern & deception record

**Purpose:** documented deceptive-practice conduct — the skill's signature line. Findings map to DP-IDs from `corp-register.md`.

**Queries:** `<company> dark patterns` · `<company> deceptive practices FTC` · `<company> cancellation difficult OR complaint` · `<company> hidden fees` · `<company> fake reviews` · `<company> shrinkflation` · pattern-name mining from the register's quick index (`<company> drip pricing`, `<company> subscription trap`…).

**What counts as a hit:** documented conduct (tier 1–4 sources) that fits a DP pattern's mechanism; clusters of specific, consistent consumer reports matching a pattern's detection cues (label `[Reported]` or `[Inferred]` accordingly).

**Pitfalls:** the pattern vocabulary is reserved for mechanism matches, not any bad experience; gray zones (disclosed fees, honest-but-slow support, inflation pricing) never map to DP IDs — the register's gray-zone list governs; EU/foreign actions count as documentation with jurisdiction labeled (AGCM, EU DSA…); a register row already found in Stage ½ enters here as its finding, then gets *current-status* verification.

## C5 — Complaints & review standings

**Purpose:** what customers report: BBB profile (grade, complaint volume, response pattern), Trustpilot/Sitejabber, app-store ratings, complaint-board arcs.

**Queries:** `<company> BBB profile` · `<company> Trustpilot` · `<company> site:reddit.com` · `<company> complaints <year>` · `<company> app store rating` · `<company> site:sitejabber.com`.

**What counts as a hit:** specific, dated, consistent failure modes across multiple reporters — not aggregate star counts.

**Pitfalls:** volume scales with customer base — normalize mentally for size before calling anything a pattern; a BBB grade measures responsiveness more than conduct; review platforms are manipulable in both directions (a wall of 5-stars is a signal worth noting, not an all-clear); one-star archives on old policies may not reflect current flows — date-check; this line alone caps at 🟡 no matter the volume.

## C6 — Scandals & controversies

**Purpose:** investigative-journalism arcs and public controversies beyond formal enforcement — safety cover-ups, exposés, viral harm events.

**Queries:** `<company> scandal` · `<company> investigation <year>` · `<company> controversy` · `<company> exposé OR whistleblower` · `<company> Reuters OR Bloomberg OR WSJ investigation`.

**What counts as a hit:** named-outlet investigations with primary artifacts; sustained multi-outlet coverage of one documented event.

**Pitfalls:** consumer-relevance boundary — labor/ESG/political controversies belong only when they are the *mechanism* of consumer deception or direct consumer harm; old scandals under different management deserve a staleness label; viral pile-ons without documentation are T5 — never primary; balance discipline cuts both ways — a scandal arc may also contain the company's remediation story.

## C7 — Pricing history & practices

**Purpose:** how the company prices and how that has moved: price-change chronology, fee architecture, shrinkflation/skimpflation, surge behavior. Applicability varies (consumer products/services: yes; pure B2B: often ➖).

**Queries:** `<company> price increase <year>` · `<product> price history` · `<company> shrinkflation` · `<company> new fee OR surcharge` · price-tracker pages for specific SKUs (camelcamelcamel-class) · `<company> junk fees`.

**What counts as a hit:** dated price or fee changes with sources (build the chronological table: Date | Change | Product/tier | Region | Source); documented undisclosed reductions in size/quality; new below-the-line fees.

**Pitfalls:** inflation-driven increases are not deception — only *undisclosed* quality/quantity reduction or *misrepresented* prices map to patterns; regional and tier pricing differ (one row per region); compare like tiers; "price history" without dates is not a finding.

## C8 — Positives & reputation balance (mandatory every Stage 1)

**Purpose:** the balance mandate's evidence base: awards and accolades, expert ratings (Consumer Reports, JD Power), trust standings (BBB responsiveness, app-store trajectory), documented remediation and compliance programs, settlement performance, long clean-record stretches, consumer-satisfaction surveys.

**Queries:** `<company> Consumer Reports rating` · `<company> JD Power award` · `<company> customer satisfaction survey` · `<company> remediation OR compliance program` · `<company> award <year>` · `<company> BBB response to complaints` · `<company> improved cancellation OR refund`.

**What counts as a hit:** expert/consumer-advocacy recognition with a named source and date; documented remediation (post-order product changes, refund programs, published compliance commitments); a verifiable stretch without adverse findings.

**Pitfalls:** manufacturer-claimed awards are labeled `company-claimed` until the awarding body confirms; astroturfed positives exist — same skepticism as astroturfed negatives; positives do not erase a documented record and vice versa — they feed the *balance readout*, not a band discount; "no positives found" after a real sweep is itself reportable (and rare at this scale).

## C9 — Privacy & data record

**Purpose:** data breaches, privacy enforcement (FTC, COPPA, state privacy laws), data-selling/broker conduct, security posture.

**Queries:** `<company> data breach <year>` · `<company> FTC privacy` · `<company> COPPA OR children privacy` · `<company> selling data` · `<company> GDPR fine` · `Have I Been Pwned <company domain>` (lead).

**What counts as a hit:** documented breaches with scope; privacy enforcement actions; documented data-monetization practices that drew regulatory or investigative findings.

**Pitfalls:** a breach is a fact about attackers as much as the company — the response (notification speed, remediation, credit monitoring) is the conduct dimension; old breaches with completed remediation get staleness labels; privacy-maze UX (DP-PRV-03) is a C4 pattern, breach volume is C9 — keep the lines straight.

## C10 — Sector-specific overlay

**Purpose:** the sector's own regulator and record pools. Load **only the matching overlay** after C1 establishes the sector.

| Sector | Regulator pools | One probe query |
|---|---|---|
| Auto / dealers | NHTSA (recalls, investigations), FTC dealer practices, state DMV/AG | `<company> NHTSA investigation` |
| Food / beverage / supplements | FDA, FTC health-claims, USDA | `<company> FDA warning letter` |
| Telecom / streaming | FCC, FTC, state AG | `<company> FCC fine` |
| Banking / fintech / credit | CFPB, OCC, Fed, state regulators | `<company> CFPB enforcement` |
| Health / telehealth | FTC health claims, HHS/OCR (HIPAA), state medical boards | `<company> HIPAA penalty` |
| Travel / ticketing / lodging | DOT, FTC, state AG | `<company> DOT penalty` |
| Gaming / apps / kids | FTC (COPPA), ESRB, state AG | `<company> COPPA` |
| Housing / rentals | HUD, state AG, local tenant enforcement | `<company> tenant settlement` |
| CPG / retail | CPSC, FTC, weights-and-measures | `<company> CPSC recall` |
| Energy / utilities | state PUC, state AG | `<company> utility commission complaint` |

**Pitfalls:** the overlay supplements C2, never replaces it; sector complaints (PUC-style) skew grievance-heavy by nature — note the instrument's bias; recalls are not wrongdoing per se (response and scope are the dimensions).
