# Category Vein Guides — automobile · consumer electronics · appliance

Use these as **checklists, not scripts**. After classifying the product (Stage 0), read only the matching guide. Not every vein applies to every product — but skipping a vein *silently* is worse than writing "not applicable." Each guide gives: the veins that matter most for the category, the category's gold-standard sources per vein, and query patterns that actually reach those sources. The universal vein definitions (V1–V12) live in the SKILL.md; these guides tell you what each vein *means for this category*.

## How to read a guide

Each vein entry: **[Vn] Name** — what to look for · *Sources*: where the quality content lives (tiered) · *Queries*: search patterns that reach them. When a source name appears here, treat it as a **lead pool seed** — a Stage-1 search that never touches the category's gold-standard sources has not actually scanned that vein, and the vein's gauge score must reflect the gap (tier-ceiling signal, see the ripeness rubric).

---

## Automobile guide

Products: a specific model, generation, or powertrain ("2021–2024 Ford Bronco", "Toyota RAV4 2019–2024, 2.5L"). Generations matter enormously — defects, recalls, and reliability scores are generation- and engine-specific, so pin model years in every query.

**[V1] Identity & Lineage** — generation boundaries, trim ladder, mid-cycle refreshes, platform sharing, model-year changes. *Sources:* manufacturer archives, enthusiast wikis and generation guides, Wikipedia (orientation only). *Queries:* `<model> generations guide`, `<model> <year> changes vs <year>`.

**[V2] Specs & Features** — powertrain options, tow ratings, dimension/weight class, option packages, standard-equipment shifts by year. *Sources:* official spec pages, spec-database sites, launch reviews. *Queries:* `<model> <year> specs towing`, `<model> trim comparison <year>`.

**[V3] Pricing & Market** — MSRP by year, incentives, current used-market bands, depreciation vs segment, resale-value awards. *Sources:* KBB, Edmunds, resale/auction data, enthusiast market trackers. *Queries:* `<model> <year> used price`, `<model> depreciation <year>`.

**[V4] Reception & Ratings** — road-test verdicts, IIHS/TSP ratings by year, Consumer Reports reliability scores by year, JD Power dependability, owner-survey scores. *Sources:* Consumer Reports, JD Power, IIHS/HLDI, major outlet road tests. *Queries:* `<model> <year> Consumer Reports reliability`, `<model> IIHS rating <year>`.

**[V5] Known Issues & Defects** ⛩ *the usually-richest vein for autos* — failure modes by engine/transmission/chassis, symptom threads, affected model-year and VIN ranges, "common problems" lists cross-checked against complaints data. *Sources:* NHTSA Office of Defects Investigation complaints, model-specific owner forums, mechanic subreddits, technical service journalism (CarComplaints-style aggregators are leads, not endpoints). *Queries:* `<model> <engine> common problems`, `<model> <year> <symptom>`, `site:carcomplaints.com <model>` (lead only).

**[V6] Recalls & Safety** — NHTSA recalls (number, date, defect, remedy), open investigations (EQ/PE/RQ numbers), TSBs distinct from recalls, airbag/crash-part actions. *Sources:* NHTSA recall and complaints databases (gold standard), manufacturer recall lookup by VIN, IIHS, Transport Canada / EU equivalents for non-US scope. *Queries:* `<model> NHTSA recall <year>`, `NHTSA investigation <model> <defect>`, `<model> technical service bulletin`.

**[V7] Legal & Liability** — auto-defect class actions (which court, which defect, settlement terms, buyback offers), lemon-law patterns, attorney-general/consumer-protection actions. *Sources:* court dockets, class-action news sites (leads), legal press, settlement administration pages (primary!). *Queries:* `<model> class action settlement`, `<model> lawsuit <defect> <year>`.

**[V8] Manufacturer Response & Support** — warranty-extension campaigns ("customer satisfaction programs"), silent part revisions by model year, dealer-service guidance, parts availability for known failures. *Sources:* manufacturer owner sites and campaign lookups, TSB databases, dealer communications quoted in forums (corroborate). *Queries:* `<model> warranty extension <defect>`, `<model> customer satisfaction program`.

**[V9] Community & Sentiment** — model-specific forums and subreddits, megathreads on known issues, sentiment arc across generations, nicknames. *Sources:* model forums, r/<model> subreddits, long-term-owner threads. *Queries:* `<model> forum owners thread`, `reddit <model> <year> problems`.

**[V10] Repairability & Longevity** — DIY-friendliness, parts cost and availability, specialty-tool needs, high-mileage longevity reports, rust/durability patterns. *Sources:* repair-trade forums, parts retailers (what sells = what fails), long-term owner threads. *Queries:* `<model> high mileage problems`, `<model> repair cost <part>`.

**[V11] Technical Analysis & Teardowns** — engineer/technician root-cause write-ups of known defects, engine-teardown videos, engineering-explainer journalism. *Sources:* technical YouTube channels, technician forums, engineering-explainer articles. *Queries:* `<model> <engine> failure analysis`, `<model> <defect> teardown`.

**[V12] Market Impact & Legacy** — sales trends, discontinuation/replacement, "worst/best year" retrospective lists, collector trajectory. *Sources:* business press, sales-data trackers, retrospectives. *Queries:* `<model> sales <year>`, `<model> discontinued why`.

**Category notes:** always distinguish **recall (safety, regulator) vs TSB (repair guidance, not a recall) vs class action (legal)** — the same defect usually appears in all three veins with different facts. Pin model years in every defect claim. VIN-range specificity is a credibility marker.

---

## Consumer electronics guide

Products: phones, laptops, consoles and controllers, headphones, tablets, wearables, smart-home devices. Batch/serial ranges and hardware revisions matter — "revision B fixed it" is a recurring plotline.

**[V1] Identity & Lineage** — model numbers vs marketing names, storage/color variants, carrier/regional variants, hardware revisions (rev A/B, "2nd gen quietly fixed"), serial-date decoding. *Sources:* manufacturer spec pages, enthusiast wikis, regulatory-filing databases (FCC IDs reveal internal revisions). *Queries:* `<product> model numbers explained`, `<product> revision differences`.

**[V2] Specs & Features** — headline specs, chip/config variants, what changed generation-over-generation. *Sources:* official spec sheets, spec databases, launch reviews. *Queries:* `<product> specs vs <predecessor>`.

**[V3] Pricing & Market** — launch pricing, price cuts cadence, current new/refurb/used bands, trade-in values. *Sources:* price trackers, resale platforms, deal-history sites. *Queries:* `<product> price history`, `<product> used value <year>`.

**[V4] Reception & Ratings** — launch reviews, review aggregators, user ratings over time (score decay after defect news is itself a finding), editor's-choice awards. *Sources:* major tech-press reviews, review aggregators, retail review sections (community tier). *Queries:* `<product> review <year>`, `<product> user rating drop`.

**[V5] Known Issues & Defects** ⛩ *usually the richest vein* — failure modes (batteries, keyboards, sticks, screens, hinges), affected batch/serial ranges, symptom threads, failure-rate estimates, "gate" nicknames ("-gate" suffixes are a search goldmine). *Sources:* owner forums, Reddit megathreads, tech-press defect coverage, iFixit, regulator complaints where applicable. *Queries:* `<product> <symptom>`, `<product>gate`, `<product> serial number check defect`.

**[V6] Recalls & Safety** — CPSC recalls (consumer products), battery-safety actions, aviation/transport authority restrictions (the Note 7 airline-ban pattern), burn/fire incident reporting. *Sources:* CPSC recall database (gold standard), regulator press releases, airline/authority directives, FAA safety advisories where relevant. *Queries:* `<product> CPSC recall`, `<product> banned airlines`, `<product> battery fire report`.

**[V7] Legal & Liability** — class actions (keyboard, stick-drift, battery, throttling are the classics), settlement terms and claim deadlines, warranty litigation, small-claims patterns. *Sources:* court dockets, settlement administration pages (primary), class-action trackers (leads), legal press. *Queries:* `<product> class action settlement`, `<product> lawsuit payout`.

**[V8] Manufacturer Response & Support** — official service/repair programs, extended warranties on known defects, free-repair campaigns, silent revisions in later production runs, software fixes for hardware issues, end-of-support dates. *Sources:* manufacturer service-program pages (primary), support forums with staff replies, press coverage of program launches. *Queries:* `<product> repair program`, `<product> free repair <defect>`, `<product> end of support`.

**[V9] Community & Sentiment** — megathreads on defects, nicknames and memes, sentiment arc (launch hype → defect backlash → nostalgia), moderator-compiled issue wikis. *Sources:* Reddit, enthusiast forums, community wikis/FAQs. *Queries:* `reddit <product> megathread <issue>`, `<product> owners thread`.

**[V10] Repairability & Longevity** — repairability scores, parts availability, battery-replaceability, planned-obsolescence accusations, longevity/retro status. *Sources:* iFixit (teardowns + scores, primary technical), repair-trade forums, parts marketplaces. *Queries:* `<product> iFixit teardown`, `<product> repairability score`.

**[V11] Technical Analysis & Teardowns** — root-cause engineering analyses (battery cell design, stick-drift potentiometer wear, keyboard mechanism failure), teardowns, failure statistics from repair shops. *Sources:* iFixit teardowns, technical YouTube, repair-shop data posts, engineering-explainer journalism. *Queries:* `<product> teardown <defect> cause`, `why <product> <failure mode>`.

**[V12] Market Impact & Legacy** — sales impact, discontinuation, product-line consequences, later products' fixes ("the Note 8's battery validation story"), collector/retro status. *Sources:* business press, analyst notes, retrospectives. *Queries:* `<product> sales impact <issue>`, `<successor> battery safety changes`.

**Category notes:** the same defect story usually spans V5 (what breaks) → V11 (why it breaks) → V8 (what the maker did) → V7 (what courts did) → V12 (what it cost). Rich-vein flags in one of these usually mean the others have unfetched primary sources — feed the lead pool across all five.

---

## Appliance guide

Products: refrigerators, washers/dryers, dishwashers, ovens/ranges, HVAC, water heaters, vacuums. Model numbers (not marketing names) are the real identity; serial-date decoding tells you which production run a unit belongs to.

**[V1] Identity & Lineage** — model-number families, series within brands, manufacturer consolidation (one factory, many brands — a recurring plotline), serial-date decoding, which "brand" actually made it. *Sources:* manufacturer model-locator pages, appliance-part retailers' model databases, enthusiast/technician references. *Queries:* `<model number> manufacture date`, `who makes <brand> appliances <year>`.

**[V2] Specs & Features** — capacity/efficiency ratings, feature tiers, configuration variants. *Sources:* official spec pages, Energy Star database, retailer spec listings. *Queries:* `<model> specs capacity`.

**[V3] Pricing & Market** — street price bands, frequent sale cycles, expected-life cost of ownership. *Sources:* price trackers, retailer history, Consumer Reports cost data. *Queries:* `<model> price history`.

**[V4] Reception & Ratings** — Consumer Reports reliability scores (brand + model tier), owner-satisfaction surveys, retail review distributions (read the 1-stars — defect clusters hide there). *Sources:* Consumer Reports, JD Power appliance studies, retail review sections. *Queries:* `<brand> refrigerator reliability <year>`, `<model> reviews 1-star`.

**[V5] Known Issues & Defects** ⛩ — failure modes (compressors, control boards, door seals, mold issues), affected model ranges and production dates, symptom threads. *Sources:* appliance-repair forums (technician posts are gold), Reddit appliance subs, parts retailers' best-seller data (what sells = what fails — a genuinely strong signal), defect press coverage. *Queries:* `<model> <symptom>`, `<model> compressor failure`, `<model> most replaced part`.

**[V6] Recalls & Safety** — CPSC recalls (fire hazards dominate: control boards, wiring, dryers), recall remedy status, incident/injury counts in CPSC notices. *Sources:* CPSC recall database (gold standard), manufacturer recall pages, recall aggregator sites (leads). *Queries:* `<model> CPSC recall`, `<brand> <appliance type> recall fire`.

**[V7] Legal & Liability** — class actions (compressor and mold lawsuits are classics), settlement terms, repair/reimbursement programs ordered or negotiated. *Sources:* court dockets, settlement administration pages (primary), class-action trackers (leads). *Queries:* `<brand> <appliance> class action`, `<model> lawsuit settlement`.

**[V8] Manufacturer Response & Support** — service bulletins to technicians, extended-warranty/recognition programs for known failures, parts-availability horizon, authorized-repair network behavior. *Sources:* manufacturer service portals, technician forums quoting bulletins (corroborate), parts retailers. *Queries:* `<model> service bulletin`, `<brand> extended warranty <defect>`.

**[V9] Community & Sentiment** — owner threads on symptom/fix outcomes, repair-vs-replace debates, brand-sentiment arcs. *Sources:* appliance subreddits, repair forums, homeowner forums. *Queries:* `reddit <model> problems`, `<model> repair or replace`.

**[V10] Repairability & Longevity** — repairability in practice (parts cost vs unit cost), expected lifespan by category, common wear parts, DIY difficulty. *Sources:* repair-trade forums, parts retailers, iFixit where applicable, lifespan surveys. *Queries:* `<model> expected life`, `<model> parts diagram cost`.

**[V11] Technical Analysis & Teardowns** — technician failure explanations (why compressors fail, board failure modes), teardown/diagnostic posts, failure statistics from repair services. *Sources:* repair technician forums and YouTube channels, manufacturer technical documentation where leaked/quoted. *Queries:* `<model> <part> failure cause technician`.

**[V12] Market Impact & Legacy** — brand reliability reputation shifts, model-line discontinuations, "don't buy year X" lore. *Sources:* Consumer Reports trend coverage, appliance-trade press, retrospectives. *Queries:* `<brand> reliability reputation <year>`.

**Category notes:** appliances have weaker single-product press coverage than electronics — the richest veins are usually V5/V8/V11 via technician communities and parts data, plus V6/V7 for safety/legal stories. A product with no CPSC hits and quiet forums is likely genuinely boring; report that honestly rather than padding.

---

## Cross-category notes

- **Regional variants**: recalls, warranties, and lawsuits are region-scoped. Keep the Stage-0 region pinned in defect/legal claims; note when a story is US-only.
- **Model numbers > marketing names** for appliances and electronics variants; model years + engine/trim for autos. Every defect claim should carry the identifier precision the evidence supports.
- **"-gate" nicknames, megathreads, and best-selling replacement parts** are three of the cheapest rich-vein detectors — teach them to your Stage-1 queries.
- **Aggregators are leads, not endpoints** (CarComplaints-style sites, class-action trackers, recall aggregators): use them to find the docket/recall/program, then cite the primary.
