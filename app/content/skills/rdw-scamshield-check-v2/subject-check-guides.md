# Subject Check Guides — product · store · social post · email · seller

Use as **checklists, not scripts**. After classifying the subject (Stage 0), read only the matching guide. Each guide gives: what to extract from the input, which check lines apply and in what priority, query patterns that actually reach the evidence, subject-specific verification moves, and the pitfalls that cause false verdicts. Universal check-line definitions (C1–C10) live in the SKILL.md. When a source named here is never touched in Stage 1, the coverage map must show the line as ⚪ — an unscanned line is a gap, not a clean result.

## Product listing guide

Subjects: a specific item for sale — "this Anker charger from a Walmart Marketplace seller", "a Dyson Airwrap for $39 on TikTok Shop", "a 1TB SD card for $8 on Amazon". The subject is the **listing + its seller line**, not the product category.

**Extract:** brand, model/part number, claimed specs, price, seller line ("Sold by / Ships from"), platform, listing photos (note whether actual-item or stock), condition language, listing age if visible.

**Check lines, priority order:** **C4 counterfeit/clone** (the heart of a product check) · **C6 price & listing plausibility** · **C5 platform standing** · **C1 advisory portals** · **C9 community** · C10 official records (recalls/seizures for the category) · C2/C3/C7 only when the listing links off-platform.

**Queries:** `<brand> <model> counterfeit` · `<brand> <model> fake vs real` · `<brand> authorized sellers` / `site:<brand>.com authorized resellers` · `<brand> <model> price` (market baseline — compare against brand store + major retail) · `<brand> <model> scam OR complaint` · `<seller name> reviews` · category-specific: `<model> serial number check`, `counterfeit <category>` (chargers, cards, sneakers, cosmetics…).

**Verification moves:** compare price against brand MSRP and major-retail range — 50%+ under market on current-season brand goods is the classic counterfeit-risk zone; check the seller against the brand's authorized-seller page; reverse-image-search the listing photos (stock/photo-shoot images on a "used" listing → T-0206); spec plausibility (capacity/weight/wattage far beyond market at a fraction of price → T-0202); on marketplaces, read the *recent* review texts on the listing, not the aggregate — a trusted old page with recent "received a fake" reviews is the T-1001 hijack signature.

**Pitfalls:** legitimate clearance/refurb pricing exists (gray zone — catalog §9); "ships from brand, sold by third-party" is still third-party; gray-market ≠ counterfeit (real item, voided warranty); safety-critical electronics (chargers, batteries, helmets, car seats, cosmetics) deserve a stricter read — the documented failure mode is physical harm, not just money loss.

## Website / store guide

Subjects: a store URL the user is contemplating buying from — "is dealz-outlet.shop legit", "this Shopify store my aunt found".

**Extract:** full domain (not the logo — the actual registrable domain), claimed brand affiliation, prices, payment methods offered, contact info (phone, address, email), return-policy text, trust badges shown, page structure tells (countdown timers, "liquidation" banners).

**Check lines, priority order:** **C3 domain & identity forensics** · **C1 advisory portals** · **C2 review & complaint boards** · **C6 price plausibility** · **C7 payment behavior** · C9 community · C5 (if it's a storefront on a hosted platform) · C10 (enforcement/seizures).

**Queries:** `<domain> scam` · `<domain> reviews` · `<domain> complaint` · `<store name> BBB` · `whois <domain>` / fetch a WHOIS lookup (domain age is a top-tier signal: weeks-old + national-brand discounts = T-0301 signature) · `<phone number>` and `<address>` if listed (do they resolve to a real business?) · if brand impersonation suspected: compare against the brand's **official** domain typed directly — one-letter-off/hyphen-suffix variants = T-0302 · `<domain> site:reddit.com`.

**Verification moves:** passive fetch of the store's own pages is allowed (landing, about, contact, policy, checkout-facing pages) — look for: physical address & phone that exist, return policy that is specific vs lorem-generic, checkout URL domain changes, payment rails offered (gift-card logos in the footer = red flag), trust badges that link nowhere or to lookalike verifier pages (T-1302 — real seals verify at the issuer). Domain age vs claimed company history is a hard tell: "family business since 1987" on a 3-week-old domain is a finding.

**Pitfalls:** a polished site is not evidence (catalog §3 trust table); https means nothing; Trustpilot pages for small stores can be gamed in both directions — read review *content and dates*, count one-star non-delivery patterns; **absence of complaints on a young store is expected, not reassuring** — no record ≠ safe.

**Safety:** passive reads only — never start checkout, never enter any data, never message the store from the check, never download their files.

## Social post / ad guide (TikTok, Facebook, Instagram)

Subjects: a post, ad, live, or shop the user saw — "this Instagram ad for 90%-off Ray-Bans", "a TikTok Shop live selling phones", "Facebook Marketplace listing for a truck, seller wants Zelle".

**Extract:** platform, account/shop handle, what's claimed (product, price, urgency mechanics), where the funnel points (in-app checkout vs link-out domain), comment state (enabled? full of "did it arrive?"), account signals (age, other content, follower pattern), any DM/screenshot content the user can paste.

**Check lines, priority order:** **C3 domain forensics** (where the funnel lands — the single most decisive fact) · **C6 price plausibility** · **C1 advisory portals** · **C9 community/social sentiment** · **C7 payment behavior** (whatever the seller asks for in comments/DMs) · C2 · C5 (shop verification badges on TikTok/FB).

**Queries:** `<handle> scam` · `<handle> reviews` · `<brand advertised> fake ad` · `<landing domain> scam` · `site:reddit.com <brand or product> instagram ad` · `<platform> <shop name> not delivered` · FTC/press: `FTC social media shopping scams` (context for the ad-funnel pattern).

**Verification moves:** the ad is not vetting — the **landing domain is the fact** (T-0303: FTC-documented top pattern — >40% of social-scam money-losers ordered from an ad). Compare the landing domain against the brand's official domain. Read the ad's comments for "did it arrive?" / "never got mine" clusters. On TikTok Shop: check the shop badge and the return policy on the product page; note TikTok's own policy states it "is not a party to your transaction". On Facebook Marketplace local listings: any move toward shipping/Zelle/deposit = classifieds pattern (T-0401/T-1203), treat as near-diagnostic per catalog §2 item 3.

**Pitfalls:** a hijacked or imposter *account* (warm profile, borrowed content) is common — the account's apparent age is not the seller's; comment sections can be curated/deleted — their *absence* (disabled comments on a shopping ad) is itself a signal; don't verdict on the platform's brand (TikTok/Instagram) — the subject is this post/shop/funnel.

**Safety:** never engage with the post, seller, or DMs from the check; never click tracked ad links directly — if the landing domain needs inspection, note it and apply the store guide's passive-fetch rules; never paste the user's own account activity into the report beyond what's needed.

## Suspicious email guide

Subjects: an order/invoice/"problem" email the user received — "verify your order", "your package is on hold", "your Zelle account needs upgrading", a fake invoice PDF. Includes carrier texts described to you (same patterns).

**Extract (as text, in the report with user PII redacted):** sender address — the actual domain after @, not the display name · reply-to if known · subject line · the specific ask (click? pay a fee? verify a card? enter credentials? call a number?) · any URL text (write it defanged: `usps-fee[.]net`, never auto-link) · impersonated institution · order/invoice references.

**Check lines — narrow set:** **C8 impersonation & contact-initiation analysis** (the core) · **C1 advisory portals/reputation** · **C3 domain forensics** (sender/landing domain vs the institution's official domain) · C9 (has anyone else reported this campaign?).

**Queries:** `<sender domain> phishing` · `<sender domain> scam` · `<landing domain> phishing` · `<exact subject line> scam` (campaign reports surface this way) · `FTC <impersonated brand> phishing email` · for carrier texts: `USPS text scam`, `FedEx delivery problem text`.

**Verification moves — static only.** The institution test: real marketplaces, banks, payment apps, and carriers (a) never need your password, a just-received code, or an upfront payment to give you money, (b) never invoice redelivery/customs/release fees via external links, (c) don't require "account upgrades" to receive payments. Map to pattern: fake order + cancel/verify button → T-0603 · "support contacted me first" + portal/remote-access → T-0601 · refund-fee → T-0602 · carrier problem/fee → T-0504 · customs fee → T-0503 · Zelle/P2P upgrade → T-0402. The verify-instead rule to give the user: open the institution's **official app/site yourself** (typed, never the link) and look for the order/refund there; no order = the email is fiction.

**Pitfalls:** display names and even logos prove nothing — only the @domain does; grammatical errors are *not* required (AI-written lures read clean); a real order existing does NOT legitimize the email (data-breach follow-on targeting); never verdict from "it looks phishy" — name the domain mismatch or the pattern violation.

**Safety (hard rules):** never click, never reply, never call numbers in the mail, never visit the URLs — reputation-check domains via search only; never open attachments; defang all URLs when writing them into the report.

## Online seller guide

Subjects: a named seller or handle the user is about to buy from — "check this eBay seller, 99.8% feedback", "someone called PineTreeDeals on Mercari", "a Facebook seller named Dana Smith".

**Extract:** exact seller name/handle, platform(s), feedback score and count, account age if visible, what they sell (coherent specialty vs random high-demand mix), listing prices vs market, recent feedback *content*.

**Check lines, priority order:** **C2 review & complaint boards** · **C9 community & forums** · **C5 platform standing** (feedback forensics) · **C1 advisory portals** · **C6 price plausibility across their listings** · C10 (enforcement naming them) · C3/C4 when they run their own store too.

**Queries:** `"<seller name>" scam` · `"<seller name>" complaint` · `"<seller name>" reviews` · `<seller name> site:reddit.com` · `<seller name> BBB` · platform-specific: `site:reddit.com <platform> seller <seller name>` · if a phone/address is public: search it directly.

**Verification moves:** read the seller's *recent* feedback text, not the aggregate — the Krebs-documented pattern (T-0705) is aged high-feedback accounts recruited into triangulation rings: watch for feedback content that stops matching current inventory, or sudden category shifts. On Amazon, check whether "Sold by" on the target listing differs from the listing's original seller (T-1001). Random high-demand goods (consoles, GPUs, air fryers) consistently under market from a new account is the classic non-delivery/triangulation storefront. Cross-platform: the same handle with reports on one platform is evidence for all.

**Pitfalls (the false-positive guards):** low-feedback new sellers are usually honest people starting out — no record = unverifiable, not scam; a handful of old negatives on a high-volume seller is normal commerce; competitor-planted negatives exist (T-0702) — weigh specificity and recency, not counts alone; a seller's *one* overpriced listing is not a scam pattern.
