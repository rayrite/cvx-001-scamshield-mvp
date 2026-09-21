# Corporate Register — documented dark-pattern companies + pattern quick index

The knowledge base for company lookups and finding classification. Distilled from the U.S. Consumer Dark Patterns knowledge base (`research-us-consumer-dark-patterns-2026-09`, corpus verified 2026-09-19 against regulator, court, and investigative primary sources). **Use in three ways:** (1) Stage ½ register lookup — company (or parent) in the table → snap preview; (2) classify observed signals → DP pattern IDs for verdict mapping; (3) mine pattern names for search vocabulary. **The register is a preview, never a verdict**: it records what was documented as of the cutoff — companies remediate, cases resolve, and statuses move. Current status always comes from live verification.

## Lookup rules

1. **Exact-entity match.** The company names in the table match the catalog entries. A similar name is not a hit — "Match Group" (register) ≠ a local "Match Productions". When in doubt, it is not a register hit; fall through.
2. **Parent-chain lookup.** Look up *both* the named entity *and* its parent/owner. "Tide" hits its own row (parent noted); "Facebook"/"Instagram"/"WhatsApp" → **Meta**; "YouTube" → **Google**; "Amazon Prime" → **Amazon**; "Genshin Impact" → **Cognosphere**; "ABCmouse" → **Age of Learning**; "Disney+" type brands need their own resolution (not all majors are in the register — absence ≠ clean).
3. **Defunct ≠ irrelevant.** Four register primaries are defunct (Columbia House, Machinima, Devumi, LeanSpa) — retained because the legal architecture those cases built still governs live patterns. Flag defunct status in any preview.
4. **Non-monetary ≠ minor.** Twelve primaries are non-monetary (warning letters, pending suits, investigations, documented-but-unenforced patterns). Their tiers run T3–T4 accordingly — preview band 🟠, not 🔴.
5. **Cutoff discipline.** Every preview cites the cutoff date (`as of 2026-09-19`) and the not-current-status caveat. The register cannot firm a verdict — only live tier 1–3 sources can.

## Evidence tiers (as used in the register)

| Tier | Meaning |
|---|---|
| T1 | Adjudicated: court finding or fully litigated agency decision establishing the conduct |
| T2 | Formal charge + resolution: agency complaint plus consent order/settlement, or well-documented class settlement (no-admission clauses noted) |
| T3 | Formal charge pending: agency complaint or major litigation, unresolved as of cutoff |
| T4 | Investigative/documentary: reputable investigation or academic study with primary artifacts |
| T5 | Illustrative only: complaint volume, anecdotes — never sufficient to name a company (excluded from the register) |

Preview band from a register row: **T1/T2 → 🔴 preview · T3/T4 → 🟠 preview** — always labeled `register`.

## The register (63 companies)

| Company | HQ | Pattern IDs | Note |
| --- | --- | --- | --- |
| Adobe | San Jose, CA | DP-SUB-05 | Hidden early-termination fees; $150M DOJ-filed settlement (2024/25) |
| Age of Learning | Glendale, CA | DP-SUB-02 | ABCmouse cancellation redesign ($3M class companion) |
| Air Canada | Montreal, Canada | DP-EMR-01 | Chatbot held liable for its own stated policy (Moffatt, 2024 BCCRT 149) — non-U.S. tribunal |
| Amazon | Seattle, WA | DP-SUB-01, DP-INT-01, DP-GAM-02, DP-QTY-06 | Four primaries — the catalog's most-documented company: Prime ($2.5B, 2025), decline-button design, child IAPs (adjudicated 2016), CPSC distributor holding (2025) |
| American Beverage | Washington, DC | DP-HLT-02 | Trade association; 2023 FTC/FDA warning letters (non-monetary) |
| Apple | Cupertino, CA | DP-QTY-04 | Battery throttling: €25M France + $500M class + $113M/34 states |
| Asbury Automotive Group | Duluth, GA | DP-FIN-07 | Discriminatory markups and no-consent add-ons — pending (allegations) |
| AT&T | Dallas, TX | DP-TEL-01, DP-TEL-03 | Cramming ($105M) and "unlimited" throttling ($60M) |
| B.E.S.T. GDR | Illinois | DP-REV-01 | First federal Consumer Review Rule case — pending (allegations) |
| Bank of America | Charlotte, NC | DP-FIN-03 | ~$250M over junk-fee architecture and fake accounts (2023) |
| Big Fish Games | Seattle, WA (at the time) | DP-GAM-03 | Social-casino line; ~$155M genre settlements |
| Capital One | McLean, VA | DP-FIN-02 | CFPB's first action (2012, $210M) |
| Cerebral | San Francisco, CA | DP-HLT-03 | Telehealth data + cancellation (2024) |
| Character.AI | San Francisco Bay Area | DP-EMR-02 | Teen-harm suits; settlements in principle (Jan 2026) |
| Chegg | Santa Clara, CA | DP-SUB-06 | Billing-interference cancellation ($7.5M) |
| Cognosphere | Singapore (Cognosphere Pte. Ltd.) | DP-GAM-01 | Genshin Impact loot boxes — first U.S. loot-box order ($20M) |
| Columbia House | New York, NY (defunct) | DP-SUB-11 | Historical negative-option anchor |
| Comcast | Philadelphia, PA | DP-TEL-02 | Broadcast TV Fee lineage — contested, unresolved |
| Credit Karma | Charlotte, NC (current; SF at order) | DP-FIN-04 | Phantom "pre-approved" offers ($3M) |
| Devumi | Florida (defunct) | DP-REV-04 | Fake followers sold to ~30,000 customers (NY AG, 2019) |
| DirecTV | El Segundo, CA | DP-SUB-08 | Adjudicated cancellation deception (2018) |
| doxo | Bellevue, WA | DP-HOM-02 | Bill-pay lookalike fees ($21M, 2026) |
| DoorDash | San Francisco, CA | DP-PRV-03 | Tips sold as income to ad platforms ($375K) |
| Encore Capital Group | San Diego, CA | DP-FIN-05 | Robosigned collections ($52M) |
| Epic Games | Cary, NC | DP-SUB-07, DP-INT-02, DP-INT-03 | Three primaries: purchase-flow dark patterns ($245M+520M), defaults, button configs |
| Fashion Nova | Vernon, CA | DP-REV-02 | Sub-4-star review suppression ($4.2M) |
| Financial Education Services | Farmington Hills, MI | DP-SUB-04 | Credit-repair negative option ($213M+) |
| Gatorade | Purchase, NY (PepsiCo) | DP-QTY-01 | 32→28 oz waistline redesign (documented, no enforcement) |
| GoodRx | Santa Monica, CA | DP-PRV-04 | First Health Breach Notification action ($1.5M) |
| Google | Mountain View, CA | DP-PRV-05, DP-PRV-06 | YouTube COPPA ($170M) + location-data order ($391.5M suite) |
| Greystar | Charleston, SC | DP-HOM-01 | Rental fee laundering ($23M + $1M CO, 2025) |
| Harley-Davidson | Milwaukee, WI | DP-R2R-01 | Magnuson-Moss anti-tying order (2022) |
| Hopper | Montreal, Canada | DP-PRC-05 | Fee-without-consent ($35M, 2026) |
| HP | Palo Alto, CA | DP-QTY-05 | Dynamic Security: AGCM €10M + 2022 class settlement |
| Imperial margarine | Flora Food Group (Amsterdam) | DP-QTY-02 | 80%→48% oil, water first (documented, no enforcement) |
| John Deere | Moline, IL | DP-R2R-02 | Repair access: 10-yr order (2025) + $99M class |
| Kroger | Cincinnati, OH | DP-EMR-06 | Shelf-tag/register mismatch (CR investigation, 2025) |
| LA Fitness | Irvine, CA | DP-SUB-03 | Cancellation friction — current FTC action (pending) |
| LeanSpa | — | DP-REV-06 | Fake-news acai network; 2d Cir. affiliate liability |
| Machinima | Los Angeles, CA (defunct) | DP-REV-03 | Paid Xbox One videos without disclosure |
| Marriott | Bethesda, MD | DP-PRC-01, DP-PRC-04 | Resort-fee deception (DC AG suit; fee-naming order) |
| Match Group | Dallas, TX | DP-INT-04 | Guaranteed-message ads (adjudicated line, 2019) |
| Meta | Menlo Park, CA | DP-GAM-04 | Youth design litigation; settlement reported up to ~$18B (final docs pending) |
| OTG Management | New York, NY | DP-EMR-05 | Tip-prompt wage settlement ($1.58M, 2024) |
| Overstock.com | Salt Lake City, UT | DP-PRC-03 | Former-price comparison deception ($6.82M affirmed 2017) |
| Progressive Leasing | Draper, UT | DP-FIN-06 | Rent-to-own cost obscuring ($175M, 2020) |
| Publishers Clearing House | Jericho, NY | DP-SUB-12, DP-URG-02 | Sweepstakes urgency and negative option ($18.5M era) |
| Sephora | San Francisco, CA (US operations) | DP-PRV-01 | First public CCPA dark-patterns action ($1.2M) |
| SiriusXM | New York, NY | DP-SUB-10 | Cancellation gauntlet (NY AG + CFPB, 2024/25) |
| Starion Energy | — | DP-TEL-05 | ESCO teaser rates ($10M MA AG, 2020) |
| StubHub | San Francisco, CA | DP-PRC-02, DP-URG-01 | Drip pricing ($10M refunds, 2026) + urgency countdown warnings |
| Sunday Riley Modern Skincare | — | DP-REV-05 | CEO-directed employee reviews (no-money order, 2020) |
| The New York Times | New York, NY | DP-SUB-09 | Hard-cancel subscription flow ($275K, Canada line) |
| Tide | Cincinnati, OH (Procter & Gamble) | DP-QTY-03 | 100→80 oz with "64 loads" and unchanged dosing cap (documented) |
| Tractor Supply | Brentwood, TN | DP-PRV-02 | DNC-list spam before merger ($1.35M) |
| TruHeight | — | DP-HLT-01 | "Clinically proven" growth claims; $4M suspended to $750K (2026) |
| Uber | San Francisco, CA | DP-EMR-04 | Algorithmic pricing differentials (CR investigation, 2026) |
| U.S. major airlines | n/a — American, Delta, United, Southwest (DOT probe) | DP-EMR-03 | Group target of DOT rewards-program investigation (2024) |
| University of Phoenix | Phoenix, AZ | DP-FIN-08 | Record $191M outcome-deception settlement (2019) |
| Verizon | New York, NY | DP-TEL-04 | Disney+ promo conversion (documented, no enforcement) |
| Wells Fargo | San Francisco, CA | DP-FIN-01 | Phantom accounts: $185M (2016) + $3.7B (2022) |
| Wendy's | Dublin, OH | DP-PRC-06 | Surge-pricing representations (state investigations) |
| X-Mode Labs | Northern Virginia | DP-PRV-07 | Sensitive-location broker order (2024) |

**Reading notes.** Amazon, Epic Games, and AT&T carry multiple primaries — repeated conduct findings *and* regulator attention concentration. The register is a map of enforcement, not of industry-wide incidence: a company's absence means no documented primary case study, not virtue. Settlements with no-admission clauses are resolutions, not findings of wrongdoing; pending matters are allegations.

## Pattern quick index (14 families, 73 patterns)

For classifying findings and mining search vocabulary. Full mechanism, harm pathway, legal hooks, and case studies live in the knowledge base; this index is the mapping layer.

**SUB — Subscription, negative-option, cancellation obstruction:** DP-SUB-01 cancellation labyrinth · 02 silent trial-to-paid conversion · 03 channel asymmetry (can't cancel where you signed up) · 04 hidden enrollment / piggyback programs · 05 buried terms & hidden early-termination fees · 06 zombie billing · 07 chargeback retaliation · 08 teaser-price step-up & surprise renewal increases · 09 refund obstruction scripts · 10 service doom loops · 11 prenotification & continuity plans · 12 sweepstakes paid-entry harvesting.

**PRC — Pricing, fees, discount architecture:** DP-PRC-01 drip pricing · 02 ticketing checkout fee stacking · 03 fictitious reference prices · 04 fee laundering by label · 05 un-bundling of included attributes · 06 surge framing & drip-priced dynamics.

**URG — Urgency & scarcity:** DP-URG-01 baseless countdown timers · 02 manufactured scarcity & false activity signals.

**INT — Interface interference & steering:** DP-INT-01 confirmshaming · 02 preselection & default exploitation · 03 trick wording & button misdirection · 04 nagging & engagement bait.

**PRV — Privacy, consent, data:** DP-PRV-01 consent asymmetry / notice-and-choice theater · 02 opt-out signal ignoring · 03 the privacy maze · 04 sensitive-data monetization · 05 age-gate theater · 06 location deception · 07 vulnerability-targeted data brokering.

**GAM — Gaming, apps, virtual economies:** DP-GAM-01 loot boxes & intermediate currency · 02 unauthorized child purchases · 03 social casino & pseudo-gambling · 04 attention & compulsion loops.

**TEL — Telecom & utilities:** DP-TEL-01 cramming · 02 below-the-line fee relabeling · 03 "unlimited" that isn't · 04 bundle promo conversion · 05 energy-supplier teaser rates.

**REV — Reviews & social proof:** DP-REV-01 fabricated & purchased reviews · 02 review suppression · 03 undisclosed endorsements · 04 fake social-media indicators · 05 insider reviews · 06 disguised advertising & fake news.

**FIN — Finance & debt:** DP-FIN-01 phantom account origination · 02 add-on packing · 03 overdraft fee architecture · 04 pre-approval & score deception · 05 robosigned & zombie debt · 06 rent-to-own cost obscuring · 07 auto add-on packing & discriminatory markups · 08 for-profit education outcome inflation.

**HLT — Health & supplements:** DP-HLT-01 unsubstantiated health claims · 02 undisclosed expert testimonials · 03 telehealth data & cancellation abuse.

**HOM — Housing & home services:** DP-HOM-01 rental fee laundering · 02 bill-payment lookalike fees.

**QTY — Quality, counterfeits, durability:** DP-QTY-01 shrinkflation · 02 skimpflation · 03 serving-count & dose manipulation · 04 software-imposed obsolescence · 05 consumable gating & printer DRM · 06 counterfeit commingling.

**EMR — Emerging & platform-native:** DP-EMR-01 seller-agent chatbot deception · 02 companion-AI engagement manipulation · 03 loyalty-currency devaluation · 04 algorithmic personalized pricing · 05 tip-prompt architecture · 06 shelf-tag & sale-price mismatch.

**R2R — Repair restriction:** DP-R2R-01 warranty-void intimidation · 02 parts pairing & diagnostic lockout.

## Gray zones (documented-but-not-deception — never map these to DP IDs)

Disclosed fees and restocking charges · inflation-driven price increases (vs. shrinkflation's *undisclosed* reduction) · unpopular-but-disclosed policies · gray-market genuine goods · slow-but-honest support (vs. *engineered* doom loops, DP-SUB-10) · legitimate dynamic pricing with disclosure (vs. DP-PRC-06 misrepresentation). The boundary: dark patterns obtain outcomes the consumer would likely have declined had things been presented neutrally. When the boundary is arguable, say so and score it down.
