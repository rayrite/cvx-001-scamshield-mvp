# Price Spectrum — data audit for the two /price scenarios

Page shipped: 2026-09-21. Purpose: document where every number on the
`/price` page comes from. The page embeds its data as two
`<script type="application/json">` blocks (`price-data-gpu`,
`price-data-dress`) inside `static/price.html`; this file is the audit
trail for both. One scenario is a real capture, one is simulated — the
page labels which is which on-screen, and this doc explains the basis of
each.

---

## Scenario A — RTX 3090 on eBay (REAL CAPTURE)

**Product:** NVIDIA GeForce RTX 3090 · 24GB GDDR6X · search `rtx 3090`
on eBay.com · captured **2026-09-11**.

**Source of record:** `price-data-gpu.json` in the research workspace
(`price_spectrum_ebay/`, capture + analysis project that produced this
page). The page's embedded GPU JSON is a projection of that file: same
meta, same fences, same zones/histogram; `asks` was filtered to prices
≤ xmax (3200) with the best-deal flag set on the $809 Zotac
(heartlesscapitalist, 209 fb · 100.0%), and `cards`/`table` carry the
9-card strip and 26-row live-listing sample.

### Capture counts (all from meta.counts)

| Bucket | Total | Included | Excluded |
|---|---|---|---|
| Live listings | 886 (of 933 on site — coverage) | 509 | 377 |
| Sold listings | 2,997 raw | 2,132 | 865 |

Sold window: 2026-06-13 → 2026-09-11 (τ = 45 d; 2,070 in window, 51
stale, 11 ended, 75 relisted). The 2,132 included sold prices are what
the density silhouette and all statistics project.

### Exclusion reasons (machine-readable, from the capture)

Live (377): product_mismatch 136 · accessory_only 110 · ti_variant 68 ·
ambiguous_multivariant 44 · ambiguous_accessory 10 · bundle_multi 5 ·
ambiguous_bundle 2 · ambiguous_formfactor 1 · engineering_board 1 —
the "$30,000 engineering sample" is real and excluded.
Sold (865): product_mismatch 360 · ti_variant 331 · accessory_only 111 ·
ambiguous_accessory 35 · bundle_multi 13 · ambiguous_formfactor 7 ·
ambiguous_multivariant 6 · ambiguous_bundle 1 · bundle_system 1.

The funnel card on the page prints these live counts; the "evidence"
details list real excluded titles (RTX 5090s, 3090 **Ti**s, waterblocks,
eGPU boxes, dual-GPU servers).

### Statistics of record

| Value | Number | Derivation |
|---|---|---|
| p25 / p50 / p75 (sold) | $1,175.50 / $1,249.93 / $1,349.99 | included sold prices |
| IQR fences lf / uf | $913.76 / $1,611.72 | p25 − 1.5×IQR, p75 + 1.5×IQR |
| Sellers' ask median | $1,799 | included live asks |
| MSRP | $1,499 | reference pin on the chart |
| Deals under fence | 5 | verified live asks below lf |
| Zone counts (live) | bait 55 · street 4 · over 343 (+gap_lo 11, gap_hi 96) | price vs fences |
| Zone counts (sold) | street 1,084 · over 90 (+gap_lo 399, gap_hi 424, scam 135) | price vs fences |
| Fraud cluster | lunoviashop ×2 | seller-name dedupe in capture |

Verdict pill "● BUY ≤ $1,350" = upper edge of the street band (p75).
The story the chart tells: two-thirds of live sellers (343) ask above
$1,612 while 1,084 of 2,132 sales closed inside the street band.

### Honesty gaps (disclosed on-page via meta.honesty_gaps)

Seller account age, stock-photo/perceptual-hash forensics, seller-network
& template detection, sold-side shipping cost, and sponsored-placement
status are NOT recoverable from search-result captures. The capture
treats all listings as organic (eBay's hidden Sponsored label is a
0-point disclosure-only signal). "47 flagged bait, but 5 verified deals
hide here" — bait flags are heuristics, not fraud findings.

---

## Scenario B — "olive green bodycon dress in XL" (SIMULATED)

**Everything on this scenario is fabricated for illustration.** No
Amazon query was run; no real sellers, brands, or listings exist. The
card says so three ways: the tab ("simulated"), an amber SIMULATED DATA
chip, and the caption ("not affiliated with Amazon and not real
listings").

**Why simulated:** the scenario demonstrates search-relevance slop
filtering — 412 results → 38 that actually match → priced on their own
spectrum. A real capture would need logged-in Amazon search scraping
(out of scope for the demo), and the pain point is universally
recognizable without one.

**Design of the simulation — anchored, not invented from nothing:**

- The slop taxonomy mirrors the real eBay exclusion reasons: no-XL-in-
  stock ≈ ambiguous_variant, wrong-green ≈ product_mismatch,
  not-bodycon ≈ product_mismatch, accessories ≈ accessory_only, juniors'
  size runs ≈ product_mismatch, stock-photo resellers + bait pricing ≈
  the capture's bait heuristics, duplicate relists ≈ relisted 75.
- Counts: 412 results, 374 slop, 38 relevant. Funnel lines sum to 374
  (96+71+58+44+33+27+22+14+9).
- Price distribution shaped to be a believable mid-market apparel market:
  p25 $52 / p50 $61 / p75 $72, fences $22 / $102, ask median $74,
  xmax $175. Zones: live 3/11/5 (+6 gap_lo, 13 gap_hi), sold
  9/121/6 (+47 gap_lo, 31 gap_hi).
- Sellers/brands are fictional but carry realistic signal fields
  (feedback count/%), top-rated, ship cost, ships-from) so the BUY /
  WAIT / AVOID / OVER logic exercises the same way as the GPU card.
  AVOID rows are flash-sale bait ($9.99–$18.99, zero-history accounts,
  CN ships-from); OVER rows are "boutique edition" markups ($108–$160).
- The ★ best deal ($47, "Verdant Muse", 1,204 fb · 98.4%, top-rated,
  ships free) sits just under the street band — the same verified-deal-
  under-fence pattern the real GPU capture found 5 of.

**The pain point it demonstrates:** every result that isn't actually an
olive-green bodycon dress with XL in stock is filtered with a
machine-readable reason *before* it can waste a click — 374 product
pages the shopper never opens.

---

## Verdict vocabulary (both scenarios)

| Verdict | Meaning |
|---|---|
| BUY | ask inside the street band (p25–p75) |
| DEAL | verified ask below the lower fence, clean seller signals (★ best) |
| WAIT | above p75 but below the upper fence |
| AVOID | bait zone + weak seller signals (0-fb accounts, parts/bait) |
| OVER | above the upper fence — sold data says wait |

On the chart, dot color never carries verdict alone: every ask's verdict
also appears as chip text on the listing cards, in zone-card rows, and
in the data-of-record table.

---

## Verification (2026-09-21, pre-merge)

- `cli.py verify --base http://127.0.0.1:8135` — **93 passed, 0 failed**
  (includes `GET /price` 200 + marker check).
- Browser (Playwright, desktop + 390×844 mobile): both scenarios render,
  deep link `?s=dress` works, replay/zone/funnel/table interactions
  clean, minimap swaps in under 660px with zero horizontal overflow,
  console clean (0 errors/warnings).
- Visual checks confirmed: axis ticks unique, MSRP pin raised clear of
  fence label, ★ halo ring distinct from plain dots in both scenarios.
