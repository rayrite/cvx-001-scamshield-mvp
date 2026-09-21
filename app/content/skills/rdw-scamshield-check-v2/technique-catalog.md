# Technique Catalog — documented seller-scam patterns, signals, rails, and reporting

The knowledge base for mapping observed signals to documented scam techniques. Condensed from the E-commerce Seller Scam Wiki research (corpus verified 2026-09-18 against FTC, IC3, BBB, platform, and payment-rail primary sources). **Use in three ways:** (1) classify observed signals → technique IDs (T-xxxx) for verdict mapping; (2) mine the alias index for search vocabulary; (3) quote the rail/platform reality tables when advising the user. Policy claims drift — re-verify anything load-bearing that postdates the corpus.

## §1. The four load-bearing walls (orientation)

Every technique collapses into one of: **fictional sellers** (F3, F10) · **lying listings** (F2, F11) · **corrupted proof systems** (F1, F5, F7, F8) · **irreversible payments** (F4). The consumer's counter-move at each wall: verify the seller/store before paying · distrust perfection in listings · demand evidence quality in delivery and reviews · never leave rails with recourse (credit card + platform checkout).

## §2. The near-diagnostic five (§15.6 of the source corpus)

Each alone justifies walking away and anchors a 🔴 verdict when observed directly:

1. Gift card / wire / crypto / reload-card payment ask (T-0403–T-0405).
2. "Upgrade your Zelle/P2P account to complete the sale" (T-0402).
3. Off-platform checkout link from a classified/social seller (T-0304, T-0401).
4. A refund that requires paying a fee first (T-0602).
5. Seller/support demands your password, OTP code, ID images, or remote access (T-0601, T-1303).

## §3. Signal library — by where you observe them

Clusters are proof; single signals are not. (→ IDs = matching techniques.)

**Listing signals:** price far below market for brand/current-season goods (→ F2/F3/F11) · stock photos only, no actual-item photos (→ T-0206) · vague/buried condition words — as-is, close-out, unqualified refurbished (→ T-0205) · impossible or photo-avoidant spec sheet (→ T-0202) · "Sold by" differs from brand; established page with suddenly-soured recent reviews (→ T-1001 hijack) · countdown timers, perpetual "closing sale" (→ T-0301) · ad lands on a domain that isn't the advertised brand's (→ T-0302/T-0303).

**Seller signals:** no contact info in listing · account new + high volume, or aged with reviews that suddenly change character (→ T-0705/T-0801) · ratings resting on star average only; generic, date-clustered review text (→ T-0701) · pressure/urgency/sob-story backstories ("deployment," "divorce") · insists on moving to email/WhatsApp/SMS (→ T-1303).

**Payment signals (highest specificity):** wire/gift-card/reload/crypto ask (near-diagnostic, T-0403–0405) · "Zelle is instant and safe" / "upgrade your account" (near-diagnostic, T-0401/T-0402) · PayPal friends-&-family discount offer (→ T-0407) · off-platform checkout link "to save fees" (→ T-0304/T-0401) · refund requires paying first (diagnostic, T-0602).

**Fulfillment signals:** tracking number unrecognized/recycled/"delivered" before order date (→ T-0501/T-0105) · "label created" frozen for days while seller soothes you toward the deadline (→ T-0104) · parcel weight absurd vs. item; tiny envelope for big product (→ T-0102) · unexpected lightweight unordered parcel (→ T-0703 brushing) · customs/release fee demanded by non-carrier, payable by gift card (→ T-0503).

**Communication signals:** "support" initiated contact (rule of first contact — the real institution never needs your password, a just-received code, or upfront payment to give you money) · requests for password/OTP/remote access/ID documents (→ T-0601/T-1303) · invoice for something you didn't buy with a cancel button — the cancel path is the theft (→ T-0603) · reshipping instructions tied to an anomalous order (→ T-0802).

**Trust-signal reality table (what consumers assume vs. reality):**

| Signal | Assumed | Reality |
|---|---|---|
| https / padlock | Site is legitimate | Scammers encrypt too — zero legitimacy signal |
| Star rating | Quality score | Manufacturable (fake reviews, brushing) and attackable (fake negatives) |
| "Verified purchase" review | Buyer used it | Brushing creates verified reviews for people who never ordered |
| High feedback / old account | Established seller | Triangulation rings recruit/steal aged high-feedback accounts |
| Professional storefront | Real business | Templates are free; polish is not evidence |
| Ad on a big platform | Platform vetted the seller | Ads lead off-platform; >40% of social-scam money-losers ordered from an ad |
| "Buyer protection" wording | I'm covered | Etsy's program protects *sellers*; Zelle has none; PayPal F&F has none |

## §4. Family & technique index (13 families, 57 techniques)

**F1 Non-delivery & phantom fulfillment** — take payment, defeat proof systems. T-0101 pure non-delivery · T-0102 token-item "proof of delivery" · T-0103 empty/weighted box · T-0104 label-created-never-ships stall · T-0105 tracking-to-nearby-wrong-address · T-0106 hit-and-run storefront.

**F2 Misrepresentation & counterfeits** — item is not what was sold. T-0201 bait-and-switch · T-0202 spec/capacity misrepresentation (reflashed storage, fake mAh) · T-0203 counterfeit sale · T-0204 safety-hazard counterfeit (chargers, batteries, cosmetics — UL: 99% of counterfeit chargers failed safety tests) · T-0205 condition/origin misrepresentation (used-as-new, mass-as-handmade, repro-as-vintage) · T-0206 stock-photo listing (seller never had the item).

**F3 Fake stores & ad funnels** — the seller is fiction. T-0301 disposable fake storefront (countdown/"liquidation" urgency) · T-0302 brand-impersonation clone store (one-letter-off domains) · T-0303 social-ad fraud funnel (FTC 2025: shopping = most-reported social scam type) · T-0304 classifieds-to-fake-checkout jump.

**F4 Payment redirection** — onto irreversible rails; the engine room of most losses. T-0401 off-platform payment pressure · T-0402 "Zelle business account upgrade" (real Zelle mail only comes from @zelle.com/@zellepay.com; no upgrade is ever needed to *receive* money) · T-0403 gift-card demand · T-0404 crypto demand · T-0405 wire/transfer demand · T-0406 fake escrow service · T-0407 PayPal friends-&-family ask.

**F5 Shipping deception** — corrupt the delivery record. T-0501 fabricated tracking number · T-0502 wrong-address proof (cross-listed T-0105) · T-0503 fake customs/release fee · T-0504 order-linked carrier smishing ("reschedule/address problem/small fee" texts; track only in the carrier's official app).

**F6 Post-purchase impersonation** — a second scam riding the first. T-0601 fake marketplace support (marketplaces never initiate refund contact asking for credentials/codes/payments) · T-0602 fake refund portal / "protection fee" (refunds never require paying first) · T-0603 invoice / "verify your order" phishing · T-0604 fake delivery-problem contact · T-0605 fake recall/warranty contact.

**F7 Reputation manipulation** — manufacture trust signals. T-0701 fake positive reviews (tight date clusters, generic phrasing, one-brand reviewer profiles) · T-0702 fake negative reviews on competitors · T-0703 brushing (unordered parcels manufacture "verified purchases"; unordered merchandise is legally yours to keep) · T-0704 shill bidding · T-0705 aged-account feedback laundering.

**F8 Triangulation fraud.** T-0801 stolen-card fulfillment (your order arrives, paid for elsewhere with a stolen card; parcel comes from a big retailer you didn't buy from, someone else's name on the slip) · T-0802 wrong-party return demand (never reship on private instruction).

**F9 Subscription & fee traps.** T-0901 hidden subscription / negative option (screenshot checkbox states; check statements monthly) · T-0902 free-trial conversion trap · T-0903 drip pricing / hidden fees · T-0904 surprise membership charge.

**F10 Listing hijacking.** T-1001 hijack / counterfeit-under-listing ("Sold by" flips on an established page; recent reviews mention fakes on a trusted old listing).

**F11 Category clusters.** T-1101 pet scams incl. AI imagery (reverse-image-search pet photos; video-verify live; incremental "shipping fees" = scam) · T-1102 fake/speculative tickets (FTC BOTS Act cases) · T-1103 vehicle marketplace scams (fake escrow, shipper deposits) · T-1104 electronics counterfeits/gray swap · T-1105 discount gift-card resale · T-1106 digital goods/account resale · T-1107 collectibles "grail" fakes (verify cert numbers with the grader).

**F12 Local-pickup risks.** T-1201 meetup robbery (daylight, public/surveilled places, companion) · T-1202 handoff switch (power-on/serial-check before money moves) · T-1203 shipper/deposit fraud on classifieds ("I'm away, use this shipper").

**F13 AI-era & emerging.** T-1301 AI-generated imagery & deepfakes in listings · T-1302 fake trust badges/seals (click the seal — real ones verify at the issuer) · T-1303 off-platform comms PII harvest.

## §5. Alias index (search vocabulary)

When querying boards and forums, use the street names: account upgrade (Zelle) → T-0402 · bait and switch / switcheroo → T-0201 · brick in a box / empty box → T-0103 · brushing / mystery seeds → T-0703 · "closing sale" store → T-0301 · counterfeit chargers → T-0204 · customs fee text → T-0503 · deepfake puppy → T-1101/T-1301 · delivery problem text → T-0504 · escrow site (vehicle) → T-0406/T-1103 · fake breeder → T-1101 · fake reviews → T-0701 · fake store → T-0301 · FedEx/USPS text scam → T-0504 · friends and family (PayPal) → T-0407 · gift card payment → T-0403 · hijacked listing / ASIN hijack → T-1001 · invoice phishing → T-0603 · label created never shipped → T-0104 · marketplace support (fake) → T-0601 · off-eBay / off-platform payment → T-0401 · puppy scam → T-1101 · refund portal (fake) / buyer protection fee (fake) → T-0602 · seed packages → T-0703 · shill bidding → T-0704 · shipper deposit → T-1203 · speculative tickets → T-1102 · subscription trap / negative option → T-0901 · token item / tracking scam → T-0102 · triangulation → T-0801 · wire transfer ask → T-0405 · wrong-address tracking → T-0105/T-0502.

## §6. Payment-rail verdict table + reporting directory

**Rails** (what each actually owes you — quote when advising):

| Rail | Verdict for buyers |
|---|---|
| Credit card | Default rail — legal dispute rights |
| Debit card | Acceptable; act fast, bank-dependent rights |
| PayPal Goods & Services | Good — Purchase Protection applies |
| PayPal Friends & Family | Never for purchases — no protection by design |
| Zelle / Venmo / Cash App personal send | Never for marketplace purchases — Zelle's FAQ states flatly it offers no purchase protection |
| Wire (Western Union/MoneyGram) | Never — unrecoverable |
| Gift cards / reload cards | Never — the canonical no-recourse rail |
| Crypto | Never — no chargebacks |
| Cash in person | Local only, after inspection at a safe meetup |
| Platform checkout | The precondition for every platform guarantee |

**Reporting directory (US):** FTC — reportfraud.ftc.gov (all seller scams) · identitytheft.gov (if PII/credentials taken) · FBI IC3 — ic3.gov (non-delivery, triangulation) · state AG via naag.org · USPS Inspection — uspis.gov/report (carrier/mail fraud, smishing) · CPSC — saferproducts.gov (safety counterfeits) · BBB Scam Tracker — bbb.org/scamtracker · payment apps — dispute in-app and via the number on your card/statement, never a number from the message · card issuer — number on card (strongest single remedy) · platform fraud reports (Amazon A-to-z flow, eBay Report item, Meta report ad/seller, etc.).

**Recovery-fraud warning (give whenever the user lost money):** no legitimate refund processor, chargeback agent, or fund-recovery firm contacts victims first or charges an upfront fee; government agencies never charge to release refunds; anything asking for gift cards/crypto/"test transfers" to return money is the same scam with a new hat.

## §7. Platform protection matrix (what actually protects you, by venue)

**Your protection comes from where you PAID, not where you SAW the item.**

| Venue | What actually protects you | Dominant threats |
|---|---|---|
| Amazon (3P) | A-to-z Guarantee, only via Amazon checkout; read the "Sold by / Ships from" line | Counterfeit-under-listing, hijack |
| eBay | Money Back Guarantee — **void for off-eBay payments** | Shill bidding, triangulation, off-platform asks |
| Etsy | Case system + card chargeback; **"Purchase Protection" is a seller-side program** — do not rely on the name | Origin misrepresentation (mass-as-handmade) |
| Shopify-style stores | Only your card network — Shopify is store software, no buyer protection | Fake/clone storefronts (F3 native habitat) |
| Craigslist | Nothing — "deal locally, face-to-face"; never wire, never escrow | Every distance-transaction pattern |
| Facebook Marketplace | Purchase Protection only for "checkout and shipping" purchases; local/off-checkout = zero | Payment redirection, pets/vehicles, hacked-account sellers |
| TikTok Shop | Buyer Policy: "TikTok is not a party to your transaction" — disputes run buyer↔seller | Social-ad funnels, live-urgency selling |
| OfferUp / Mercari / Poshmark | In-app checkout protections (Posh Protect holds payment until you rate/accept — don't rate before inspecting) | Off-app payment asks, condition lies |
| Walmart Marketplace | Returns/customer-service flow; card backstop | Third-party counterfeits |
| Temu / AliExpress | Card chargeback; AliExpress Buyer Protection (delivery window + 15-day not-as-described) — check the flag is on for the listing | Expectation gap, token parcels |
| Generic fake stores | Only your payment rail | Everything (F3/F4/F9/F13) |

## §8. Headline statistics (use with their caveats, never without)

~$16B reported US fraud losses 2025, record (FTC Sentinel; under-counted) · $2.1B social-media-originated losses; shopping = most-reported social scam type; >40% of social-scam money-losers ordered from an ad (FTC) · IC3 2025: $20.877B internet-crime losses; Non-Payment/Non-Delivery #3 by count at 56,478 complaints (**merges buyers-not-paying and sellers-not-shipping — never quote as seller-scam-only**) · GAO test-buy: 20 of 47 brand-name items from third-party vendors were counterfeit · UL: 99% of counterfeit iPhone chargers failed safety tests · Largest US counterfeit seizure: ~$1B retail value, ~219,000 items (2024). FTC Sentinel and IC3 are different instruments — never sum or compare as one trendline.

## §9. Gray zones (bad experiences that are NOT scams — do not verdict 🔴 on these)

Slow dropship-from-faraway sellers (weeks-long genuine delivery; the 30-day/no-ship-date Mail-Order-Rule baseline is the line for *when*, not *if*) · disclosed replicas/knockoffs (platform-policy issue, not necessarily fraud) · gray-market genuine goods (real products, unauthorized channel — warranty risk only) · disclosed restocking fees and strict return windows · buyer-visible "buyer protection fee" line items (disclosed pricing, e.g., Poshmark). **False-positive guards:** new honest sellers match scam heuristics — score clusters, not single signals; legitimate clearance pricing exists; non-native-English listings are never a scam signal.
