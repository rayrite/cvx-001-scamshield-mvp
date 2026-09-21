# Smoke Test — zero-search snap checks on recall-claiming content

The smoke test answers one question in under a minute with **zero searches and zero fetches**: *does the supplied material itself contain a decisive fake-recall-scam tell?* A seasoned reader flips to the payment ask, the sender domain, or the phone number and knows immediately. This checklist makes that instinct explicit, fast, and rubric-anchored. It is modeled on the recall-scam patterns documented in the 2026-09 source research (§21 of the recall-resources guide: fake Amazon recall texts Feb–Mar 2026, refund-fee asks, call-center funnels, look-alike "official" domains) and on the consumer-protection consensus rule they all violate: **no legitimate recall notice asks for payment or a card "to process your refund."**

## Rules

1. **Zero network calls.** No searches, no fetches, no WHOIS, no subagents. The smoke test reads only what the user supplied (message text/screenshot, URL, post description, article text). If a check would need the network, it is not a smoke item — fall through to Stage 1.
2. **Claim-bearing content only.** The smoke test runs on material that *asserts* a recall or refund: a text/email/DM, a social post, a website, an article. A bare product question ("is my almond milk recalled?") has nothing to smoke-test — fall through immediately and run the routed sweep. **The recall-status readout can never be snap-answered**: whether a product has a real recall record is a database fact, not a content tell, and "I don't recall hearing about it" is worth nothing.
3. **Decisive vs corroborating.** Every item below is labeled **[Decisive]** (fires a snap verdict alone — it maps to a 🔴 authenticity anchor: near-diagnostic scam ask observed directly, or agency/brand impersonation confirmed in the material itself) or **[Corroborating]** (a strong tell that alone caps at 🟠; it either joins a decisive item or is handed to Stage 1 as a head start).
4. **FP guards are part of the item.** Each item states when NOT to fire. An item fired without its guard satisfied is a false positive, not caution.
5. **Major-brand/agency knowledge only.** Domain-identity items fire only when the impersonated institution is common knowledge (fda.gov, usda.gov, cpsc.gov, amazon.com, walmart.com, costco.com, kroger.com, target.com, and major consumer brands). An unfamiliar sender's domain proves nothing — fall through.
6. **Observed, not inferred.** An item fires only on text/content actually visible in the material. Blocked images = unknown, not clean: unobservable asks are recorded as a gap, never guessed.

## Outcomes

- **Any [Decisive] item fires** → snap verdict on **content authenticity**: **🔴 scam/impersonation pattern — High confidence, labeled `snap`**. Deliver the ultra-short snap response (below). Do NOT search, do NOT create the report file. The **recall-status readout is marked "not checked"** and `document` is offered — the documentation pass is also the honest way to answer "is the product *actually* recalled".
- **Only [Corroborating] items fire** → proceed to Stage 1 triage normally, opening with the observed tells (the sweep starts smarter, not from zero).
- **Nothing fires** → Stage 1 triage unchanged. A scary-but-tell-free post and a legitimate retailer recall text both live here — the smoke test must never make thin evidence feel decisive.

## Snap response shape (the whole reply, ~10 lines)

```
> ## ⚠️ CONTENT AUTHENTICITY: 🔴 Scam/impersonation pattern — High confidence (snap)
> **Basis:** <decisive tell(s) with item IDs, one line>
> **Do/don't:** <2–3 bullets — don't click/pay/call; where to verify instead; report it>

**Recall status: not checked** — a fake message doesn't tell us whether <product> has a real recall record.
Checked in <N> seconds, zero searches — the material itself settles the authenticity question.
Say "document" for the full archived report — which also checks <product>'s actual recall record ·
"stop" to finish here.
```

## Message smoke list (recall texts / emails / DMs)

- **S-M1 Pay-to-refund ask** · **[Decisive]** — the message's visible ask is a payment or card entry "to process your recall refund": a processing fee, a card-on-file update, an overpayment you must return, or "verify your card to receive compensation". Near-diagnostic — the documented rule is that no legitimate recall notice asks for payment or a card to deliver a refund. *FP guards:* the ask must be visible in the material (blocked-image buttons = gap, not evidence); real remedies exist that involve the *retailer crediting your account* or a refund *initiated by them* — an ask where the consumer sends money or card data first is the tell, not the existence of a refund.
- **S-M2 Sender/link domain ≠ claimed institution** · **[Decisive]** — the message claims to be an agency (FDA/USDA/CPSC) or brand/retailer B, but the actual @-domain or link domain is not B's official domain. Rubric anchor: impersonation confirmed in the material. *FP guards:* display names and logos prove nothing — only the @-domain and link domains count; **retailers legitimately send real recall texts** (Walmart, Costco, Kroger all run alert channels) — if the sender is a short code or the domain genuinely matches the retailer's, do NOT fire, fall through; brands do send some mail from legitimate corporate-ESP subdomains — if in doubt, it is NOT smoke-decisive.
- **S-M3 Call-center number as the action** · **[Decisive]** — "call this number to process your recall/refund/claim". Real recall notices direct you to the agency page or retailer site/app, not a call center; phone-based refund flows are the documented scam signature. *FP guard:* a published customer-service number on the brand's own official recall page is legitimate contact info — the tell is an unsolicited message whose *action* is calling to process money.
- **S-M4 Non-recoverable refund rails** · **[Decisive]** — refund flow demands gift card, wire transfer, crypto, or P2P app to "release" recall compensation. Near-diagnostic family; no real recall remediation runs on these rails.
- **S-M5 Unsolicited first contact** · **[Corroborating]** — you don't own the product, didn't shop at that retailer, or never opted into alerts, yet received a "recall notice" about your purchase. Targeted-lead behavior; alone it caps at 🟠 (lists get bought; some error is possible).
- **S-M6 Urgency/deadline pressure** · **[Corroborating]** — "respond within 24 hours or forfeit your refund", "final notice". Real recalls run for weeks-to-months with published remedy deadlines. *FP guard:* genuine notices do state claim deadlines — the tell is pressure replacing specifics, not the existence of a date.
- **S-M7 Missing recall specifics** · **[Corroborating]** — no product name/brand, no lot or model numbers, no dates, no agency reference. Real recall notices are specific to a fault (lot codes, date ranges, UPCs). *FP guard:* a legitimate retailer text may be short and link out for specifics — pair this with where the link points; alone it corroborates.

## Post smoke list (TikTok / Facebook / Instagram)

- **S-P1 Claimed authority + non-official funnel** · **[Decisive]** — post claims an agency or major brand announced a recall, and its link/bio funnel points to a domain that is not the agency's (.gov) or brand's official domain. The landing domain is the fact. *FP guards:* major-brand/agency knowledge only; in-app platform shops fall through (platform standing is a Stage-1 question); a link to a news outlet's coverage is not this item — fall through and let Stage 1 check the coverage.
- **S-P2 Visible payment/claim instruction** · **[Decisive]** — "DM to claim your refund", comment-to-register, payment-app or gift-card instructions visible in the post or its pinned comment. Near-diagnostic ask family.
- **S-P3 Panic + vague product** · **[Corroborating]** — high-urgency recall claim with no brand/lot/agency specifics ("they're recalling lettuce NOW, check yours!"). Recall-panic engagement bait is real but not inherently fraudulent — it hands Stage 1 the job of checking the claim.
- **S-P4 Impersonated account identity** · **[Corroborating]** — account handle/name mimics an agency or major brand ("@FDA_recalls_official") without being it. Platform identity verification is Stage-1 work, but the mimicry observed in the handle text is a head-start finding.

## Website smoke list

- **S-W1 Look-alike "official recall registry" + data ask** · **[Decisive]** — non-.gov domain presenting as an official recall service ("National Recall Registry", "Recall Compensation Center") with a form asking for card numbers, SSN, or account credentials to "check eligibility / process your refund". Impersonation + near-diagnostic ask, both observed in the page itself. *FP guard:* the data ask must be visible in supplied material.
- **S-W2 Brand-in-domain-but-not-the-brand** · **[Decisive]** — domain contains a major brand's name but is not the brand's official domain (`<brand>-recall-refund.com`). Same rule as the family's other skills: official recall microsites live on the brand's OWN domain (`brand.com/recalls`) or an agency's (.gov). *FP guard:* authorized-reseller and brand-partner questions can't be smoke-judged — fall through.
- **S-W3 Aggregator breadth** · **[not a tell]** — a private site that lists many recalls, asks for nothing, and links out: that is the convenience tier (non-authoritative), not a scam. Never fires; Stage 1 simply never treats it as the source of record. Recorded here so it isn't mistaken for a smoke item.

## Article smoke list (thin by design)

News articles are rarely smoke-decidable — their failure mode is sloppiness or staleness, not fraud.

- **S-A1 Content-farm markers** · **[Corroborating]** — undated, no agency link, no author, generic stock imagery, "recall list 2026" SEO title patterns. Corroborating only: the article's *claim* still gets checked at the agency page in Stage 1; the farm markers downgrade its evidentiary weight to zero.
- Default: fall through to Stage 1.

## Why the snap label replaces "provisional"

A Stage-1 verdict is labeled *provisional* because a partial sweep might be revised by later stages. A snap verdict rests on a decisive tell **observed directly in the material** — an existing 🔴 authenticity anchor — so it is labeled `snap` instead: the basis is complete at zero searches. The documentation pass can strengthen the writeup (and in rare cases surface a contradiction — e.g., the "random" domain turns out to be the retailer's documented alert sender — which is then shown as verdict movement per the rubric's honest-verdict rules), but it is not needed to justify the band. What the snap verdict never covers is the **recall-status readout**: that stays "not checked" until a routed sweep runs, full stop.
