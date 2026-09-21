# Smoke Test — zero-search snap checks before any research

The smoke test answers one question in under a minute with **zero searches and zero fetches**: *does the subject material itself contain a decisive scam tell?* A seasoned reader flips to the sender line, the payment ask, or the funnel domain and knows immediately. This checklist makes that instinct explicit, fast, and rubric-anchored. It is modeled on the industry-standard triage order (SLAM: Sender → Links → Attachments → Message; SOC practice: sender & domain analysis before body/URL analysis) and on the FTC's first-line consumer indicators.

## Rules

1. **Zero network calls.** No searches, no fetches, no WHOIS, no subagents. The smoke test reads only what the user supplied (email text/screenshot, URL, listing page content, post description). If a check would need the network, it is not a smoke item — fall through to Stage 1.
2. **Decisive vs corroborating.** Every item below is labeled **[Decisive]** (fires a snap verdict alone — it maps to a 🔴 rubric anchor: near-diagnostic signal observed directly, or brand-clone confirmation) or **[Corroborating]** (a strong tell that alone caps at 🟠; it either joins a decisive item or is handed to Stage 1 as a head start).
3. **FP guards are part of the item.** Each item states when NOT to fire. An item fired without its guard satisfied is a false positive, not caution.
4. **Major-brand knowledge only.** Sender/funnel identity items fire only when the impersonated institution is a major brand/institution whose official domain is common knowledge (usps.com, mcafee.com, amazon.com, paypal.com, fedex.com, irs.gov, microsoft.com…). An unfamiliar sender's domain proves nothing — fall through.
5. **Observed, not inferred.** An item fires only on text/content actually visible in the material. Blocked images = unknown, not clean: unobservable asks (button text, phone numbers) are recorded as a gap, never guessed.

## Outcomes

- **Any [Decisive] item fires** → snap verdict: **🔴 scam pattern match — High confidence, labeled `snap`**. Deliver the ultra-short snap response (below). Do NOT search, do NOT create the report file. The documentation pass (searches + archived report + ledger) is offered at the gate via `document`.
- **Only [Corroborating] items fire** → proceed to Stage 1 triage normally, opening with the observed tells (Stage 1 starts smarter, not from zero).
- **Nothing fires** → Stage 1 triage exactly as in v1. Most honest-but-odd subjects live here; the smoke test must never make thin evidence feel decisive.

## Snap response shape (the whole reply, ~10 lines)

```
> ## ⚠️ VERDICT: 🔴 Scam pattern match — High confidence (snap)
> **Basis:** <decisive tell(s) with item IDs and T-ID mapping, one line>
> **Do/don't:** <2–3 bullets — report it, verify-instead move, ignore follow-ups>

Checked in <N> seconds, zero searches — the material itself settles it.
Say "document" for the full archived report (pattern documentation, sources, ledger) ·
"stop" to finish here.
```

## Email smoke list

- **S-E1 Sender-identity failure** · **[Decisive]** — the message claims to be major brand/institution B, but the actual @-domain (not the display name) is not B's official domain and not a known-legitimate sending pattern for B. Maps to T-0302/T-0603 impersonation; rubric anchor: brand-clone confirmation. *FP guards:* display names and logos prove nothing (only the @-domain counts); B must be major-brand knowledge; brands do send some mail from legitimate corporate-ESP subdomains — if in doubt whether a domain is B's, it is NOT smoke-decisive (fall through); a newsletter from an *expected* marketing sender is not this item.
- **S-E2 Near-diagnostic payment/credential ask** · **[Decisive]** — the email's visible ask is one of the catalog §2 five: pay by gift card / wire / crypto · "upgrade your Zelle/P2P account to receive payment" · a refund that requires paying first · enter password / just-received code / grant remote access · checkout on an off-platform link. Anchor: near-diagnostic observed directly. *FP guards:* the ask must be visible in the material (blocked-image buttons = gap, not evidence); legitimate 2FA prompts you *initiated* are not email-borne.
- **S-E3 Carrier/government fee-by-link** · **[Decisive]** — redelivery / customs / release / "address correction" fee invoiced via a link, for a carrier or agency. T-0504/T-0503. Real carriers and agencies never invoice small fees by external link. *FP guard:* tracking links inside genuine carrier mail point at the carrier's own domain and ask for no payment — links are fine, *fees by link* are the tell.
- **S-E4 Reply-to divergence** · **[Corroborating]** — reply-to on a domain unrelated to both sender and claimed brand (e.g., corporate billing notice with reply-to on a newsletter-ESP catcher domain). Legitimate corporate correspondence does not route replies through third-party marketing infrastructure. *FP guard:* small businesses legitimately reply via ESP addresses — this item corroborates corporate-brand claims, not small-sender mail.
- **S-E5 Machine-generated sender domain** · **[Corroborating]** — the @-domain is a random alphanumeric string, brand-incoherent (throwaway infrastructure). Together with any S-E1 brand claim, the cluster is decisive.
- **S-E6 Corporate-notice-via-marketing-ESP mismatch** · **[Corroborating]** — billing / security / renewal notices (trust-critical classes) sent through small-business marketing infrastructure. Marketing mail via ESP is normal; *billing and security notices* via a newsletter tool is a class mismatch.

## Store/website smoke list

- **S-W1 Brand-in-domain-but-not-the-brand** · **[Decisive]** — domain contains a major brand's name but is not the brand's official domain (`<brand>-outlet.shop`, `<brand>shoes.deals`). T-0302 brand clone; anchor: brand-clone confirmation. *FP guards:* official domains and their store/country subdomains pass; a domain merely *containing* generic words (shoe, deals) without a major-brand name is not this item; authorized-reseller questions can't be smoke-judged — fall through.
- **S-W2 Non-recoverable payment rails visible** · **[Decisive]** — gift-card payment logos, wire instructions, or crypto addresses in checkout/footer. Near-diagnostic family (catalog §2). *FP guard:* must be visible in supplied material, not assumed.
- **S-W3 Absurd pricing site-wide** · **[Corroborating]** — ≥70% under MSRP across current-season brand goods. Classic counterfeit/non-delivery zone (T-0301/T-0202) but clearance/refurb/gray-market exist — never decisive alone.

## Social post/ad smoke list

- **S-P1 Funnel mismatch** · **[Decisive]** — ad/post for major brand B points to a link-out domain that is not B's. T-0303/T-0302; the landing domain is the fact. *FP guards:* B must be major-brand knowledge; in-app checkout with the platform's own shop system falls through (platform standing is a Stage-1+ question).
- **S-P2 Off-platform payment pressure visible** · **[Decisive]** — "DM to order" plus payment-app/gift-card instruction in the post or its comments. T-0401/T-1203. *FP guard:* instructions must be visible in the supplied material.
- **S-P3 Marketplace shipping+deposit pattern** · **[Decisive]** — local-listings platform, but seller pushes shipping + Zelle/deposit/gift card. Near-diagnostic per catalog §2 item 3.

## Seller/product smoke list (thin by design)

Most seller and product questions need external records — the honest smoke result is usually "fall through."

- **S-T1 Off-platform payment instruction in the listing/DM** · **[Decisive]** — visible instruction to pay outside the platform's checkout. Near-diagnostic family.
- **S-T2 Spec absurdity** · **[Corroborating]** — claimed specs far beyond market at a fraction of price (1TB for $8, 100W charger for $3). T-0202 zone; corroborating only.
- Default: fall through to Stage 1.

## Why the snap label replaces "provisional"

A Stage-1 verdict is labeled *provisional* because a partial sweep might be revised by later stages. A snap verdict rests on a decisive tell **observed directly in the material** — an existing 🔴 anchor — so it is labeled `snap` instead: the basis is complete at zero searches. The documentation pass can strengthen the writeup (and in rare cases surface a contradiction, which is then shown as verdict movement per the rubric's honest-verdict rules), but it is not needed to justify the band.
