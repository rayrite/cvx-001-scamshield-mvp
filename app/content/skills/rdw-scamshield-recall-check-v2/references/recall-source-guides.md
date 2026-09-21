# Recall Source Guides — routing, federal & state surfaces, retailer layer, scam appendix

The knowledge base for recall checks: which agency owns which product class, every source URL worth querying, how to handle access-limited sites, and the scam patterns that target recall anxiety. **Source vintage: page verifications dated 2026-09-19** (research deliverable `research-us-product-food-recall-resources-2026-09/`). URLs drift; if a routed fetch 404s, fall back to the site's own search or a `site:` query rather than assuming the source died. All statuses below ("verified live", "access-limited") are as of that date unless re-verified in-session — record your own access dates in the report's Sources section.

## §1. Routing matrix — what you're checking → where the record lives

| What you're checking | Go here first | Why | Report a problem to |
|---|---|---|---|
| Packaged food, produce, snacks, supplements, infant formula, seafood (non-catfish) | **FDA recalls** — fda.gov/safety/recalls | FDA regulates ~78% of the food supply | fda.gov/safety/report-problem-fda |
| Peanut butter, salad kits, frozen vegetables (outbreak-prone foods) | FDA recalls + **CDC outbreaks** | Outbreak link likely | same |
| Ground beef, chicken, turkey, hot dogs, deli meat, processed eggs, **catfish** | **FSIS recalls** — fsis.usda.gov/recalls (access-limited, see §3) | USDA-regulated | ask.fsis.usda.gov |
| Dog food, pet treats, livestock feed | **FDA animal recalls** — fda.gov/animal-veterinary/safety-health/recalls-withdrawals | FDA regulates animal food | FDA report form |
| Crib, toy, space heater, dresser, hoverboard, button-battery product, appliance | **CPSC** — cpsc.gov/recalls | CPSC-regulated | SaferProducts.gov |
| Car, truck, motorcycle | **NHTSA** — nhtsa.gov/recalls, VIN lookup (access-limited, see §3); campaign records via search | NHTSA-regulated; VIN lookup is the user's to run — give the link | nhtsa.gov/report-a-safety-problem |
| Car seat, booster, tires | NHTSA (seat registration drives direct notice) | NHTSA-regulated | same |
| Prescription drug, OTC medicine | **FDA drug recalls** — fda.gov/drugs/drug-safety-and-availability/drug-recalls | FDA-regulated | FDA report form |
| Insulin pump, pacemaker, CPAP, implant | **FDA device recalls + database** — fda.gov/medical-devices/medical-device-safety/medical-device-recalls-and-early-alerts + accessdata.fda.gov device-recall DB | FDA-regulated; the database is the record of fact | same |
| Cosmetic, shampoo, makeup | FDA recalls hub (cosmetics flow through the main list) | FDA-regulated | same |
| Boat, personal watercraft | **USCG** — uscgboating.org/content/recalls.php | USCG manufacturer-recall system | uscgboating.org/consumer-safety-defect-report.php |
| Pesticide, insecticide concern | **EPA** — epa.gov/safepestcontrol | EPA regulates; stop-sale notices are the analog | EPA |
| "Was it distributed/sold in my state / at my store?" | State layer (§4) + retailer hub (§6) | States re-filter by distribution; retailers know lot-level | state agency (§4) |
| "People got sick eating X" (no recall yet) | **CDC Current Outbreak List** — cdc.gov/outbreaks + cdc.gov/foodborne-outbreaks/outbreaks | Investigations precede recalls | local/state health dept (they trigger CDC) |
| Not sure / everything | **Recalls.gov** → pick the tab | Six-agency gateway (a signpost, not a database) | — |

## §2. Federal sources (full entries)

**F-01 · FDA Recalls, Market Withdrawals & Safety Alerts** — fda.gov/safety/recalls (canonical `/safety/recalls-market-withdrawals-safety-alerts`) · verified live · filterable current list + archive; GovDelivery email + RSS. **Start here for all non-FSIS food, drugs, devices, cosmetics.**

**F-02 · FDA Enforcement Reports** — fda.gov/safety/recalls-market-withdrawals-safety-alerts/enforcement-reports · verified live · weekly comprehensive listing including Class II/III actions that never get press releases. **The history-depth source: use when press and the current list are silent.**

**F-03 · FSIS Recalls & Public Health Alerts** — fsis.usda.gov/recalls · **access-limited** (Akamai blocks automated verifiers; corroborate via search extraction — §3) · meat, poultry, processed egg. Companions: /food-safety/alerts (Active Alerts), per-alert items under /recalls-alerts/.

**F-04 · CDC Current Outbreak List / Foodborne Outbreaks** — cdc.gov/outbreaks/index.html + cdc.gov/foodborne-outbreaks/outbreaks/index.html · both verified live · the "no recall yet but people are sick" layer. Investigation pages carry **case counts by state** — feed the location table at map time.

**F-05 · FoodSafety.gov (HHS)** — foodsafety.gov + /recalls-and-outbreaks · verified live · plain-language aggregation of FDA + FSIS + outbreak notices; good fallback when an agency page is hostile.

**F-06 · FDA Animal Food Recalls & Withdrawals** — fda.gov/animal-veterinary/safety-health/recalls-withdrawals · verified live · pet/animal food.

**F-07 · Recalls.gov** — recalls.gov · verified live · six-agency gateway; tabs route to CPSC/NHTSA/USCG/FoodSafety.gov/FDA/EPA. Use when routing is uncertain.

**F-08 · CPSC Recalls Index** — cpsc.gov/recalls · verified live · 1,000+ archive pages; **search-by-company**: cpsc.gov/Recalls/search-by-company; email chooser at cpsc.gov/Newsroom/Subscribe; RSS. The most open federal source — fetch freely.

**F-09 · SaferProducts.gov** — saferproducts.gov · verified live · CPSC's public **incident-report** database (read + file). Distinct from the recall list — this is where fire/burn/injury reports live before any recall exists.

**F-10 · NHTSA Recalls (VIN lookup)** — nhtsa.gov/recalls · **access-limited** (bot-wall; corroborate via search extraction) · vehicles, car seats, tires, equipment. Manufacturer portal recalls.portal.nhtsa.gov verified live. Report: nhtsa.gov/report-a-safety-problem.

**F-11 · FDA Medical Device Recalls and Early Alerts** — fda.gov/medical-devices/medical-device-safety/medical-device-recalls-and-early-alerts · verified live · ⚠️ the old `/medical-devices/medical-device-recalls` URL is 404 (moved here).

**F-12 · FDA Medical Device Recall Database** — accessdata.fda.gov/scripts/cdrh/cfdocs/cfres/res.cfm · verified live, searchable · the device-recall **database of record** — separate from F-11.

**F-13 · FDA Drug Recalls** — fda.gov/drugs/drug-safety-and-availability/drug-recalls · verified live.

**F-14 · FDA Cosmetics Recall Policy** — fda.gov/cosmetics/cosmetics-compliance-enforcement/fda-recall-policy-cosmetics · verified live · policy page; cosmetic recall *listings* flow through F-01.

**F-15 · EPA Pesticides / Safe Pest Control** — epa.gov/pesticides + epa.gov/safepestcontrol · both verified live · stop-sale/suspension = EPA's recall-analog.

**F-16 · USCG Boating Safety — Recalls** — uscgboating.org/content/recalls.php · verified live · recreational-boat manufacturer recalls.

**F-17 · FDA Report a Problem** — fda.gov/safety/report-problem-fda · verified live · the reporting counterpart to F-01.

**Key vocabulary** (use precisely in findings): **recall** (defect/law violation; usually firm-initiated, agency-classified) · **market withdrawal** (minor violation, no legal action) · **safety alert / public health alert** (warning without a recall) · **outbreak investigation** (CDC; may precede any recall) · **Class I / II / III** (I = reasonable probability of serious harm/death; II = possible temporary harm; III = unlikely to harm — grades of *expected-harm probability*, not defect ugliness).

## §3. Access-limited sources — corroboration protocol

Observed 2026-09-19 and expected to persist: **fsis.usda.gov** (Akamai "Access Denied") and **nhtsa.gov/recalls** (bot-wall) refuse automated fetchers; **lapublichealth.org** refuses some TLS clients; occasional CPSC subpages fail. Protocol:

1. Try the direct fetch **once or twice** — never more.
2. Corroborate via **search-engine extraction**: `site:fsis.usda.gov <brand>` — the search engine's own crawl serves the page title + snippet; press relays add the specifics.
3. Label the finding **`access-limited — corroborated via search extraction + <outlets>`** in the findings index and coverage map. Never mark such a page "verified live".
4. Give the user the URL to open in their own browser (browsers work fine; the wall is against automation) and say that's what you did.
5. A 🔴 recall-status verdict may rest on ≥2 independent confirmations when the agency page is unreachable — with the limitation named explicitly (SKILL.md source hierarchy).

## §4. State layer — distribution filtering

States re-filter federal recalls by **distribution** ("recalls known to affect Montana", "food alerts affecting Texas") and cover state-inspected products (grade-A dairy, local meat processors). ~30 states maintain dedicated recall lists; ~20 relay via press releases or have only program pages. When a recall is found, the state layer answers "was it shipped here?" — the question federal pages don't.

**Machine-readable table** (`name|agency|url|type`; type: list = dedicated recall list · portal = cross-agency · news = press/notice relay · program = program page only). Verified 2026-09-19:

```
AL|Alabama Ag & Industries + ADPH|https://agi.alabama.gov/foodsafety/recalls/|list
AK|Alaska DEC|https://dec.alaska.gov/eh/fss/recall-alerts|list
AZ|Arizona DHS|https://www.azdhs.gov/preparedness/epidemiology-disease-control/food-safety-environmental-services/index.php|program
AR|Arkansas DOH|https://healthy.arkansas.gov/programs-services/public-health-safety/food-protection-inspection-portal/foodborne-disease/|news
CA|CA DPH|https://www.cdph.ca.gov/Programs/CEH/DFDCS/Pages/FDBPrograms/FoodSafetyProgram/FoodRecalls.aspx|list
CO|CO CDPHE|https://cdphe.colorado.gov/dehs/rf/resources|program
CT|CT DPH|https://portal.ct.gov/dph/food-protection-program/food-protection-communications|news
DE|DE DHSS|https://dhss.delaware.gov/dph/homepage/about/sections/hsp/licenses-and-permits/food-protection/food-safety/|program
DC|DC Health|https://dchealth.dc.gov/service/division-food|program
FL|FL FDACS|https://www.fdacs.gov/Consumer-Resources/Product-Recalls|list
GA|GA Agriculture|https://www.agr.georgia.gov/recalls|list
HI|HI DOH|https://health.hawaii.gov/food-drug/recalls-guidance/|list
ID|ID H&W|https://healthandwelfare.idaho.gov/health-wellness/community-health/food-safety|program
IL|IL Agriculture|https://agr.illinois.gov/safety/recalls.html|list
IN|IN DOH|https://www.in.gov/health/food-protection/consumer-information/recalls-and-advisories/|list
IA|IA DIAL|https://dial.iowa.gov/contacts/food-safety|program
KS|KS Agriculture|https://www.agriculture.ks.gov/divisions-programs/food-safety-and-lodging/consumer-information|program
KY|KY CHFS|https://www.chfs.ky.gov/agencies/dph/dphps/fsb/Pages/default.aspx|program
LA|LA DOH|https://www.ldh.la.gov/bureau-of-sanitarian-services/food-safety|program
ME|ME CDC|https://www.maine.gov/dhhs/mecdc/health-professionals/health-advisory-notices|news
MD|MD DOH|https://health.maryland.gov/phpa/OEHFP/OFPCHS/Pages/GuidanceRecalls.aspx|list
MA|MA DPH|https://www.mass.gov/info-details/food-safety-recalls-news-alerts|list
MI|MI MDARD|https://www.michigan.gov/mdard/food-dairy/food-safety/recalls|list
MN|MN MDA + MDH|https://www.mda.state.mn.us/food-feed/food-recalls-consumer-advisories-minnesota|list
MS|MS MSDH|https://msdh.ms.gov/msdhsite/_static/41,0,176,322.html|list
MO|MO DHSS|https://health.mo.gov/citizens/food-drug-recalls|list
MT|MT DPHHS|https://www.dphhs.mt.gov/publichealth/EHFS/recalls|list
NE|NE Agriculture|https://nda.nebraska.gov/fscp/foods/recalls|list
NV|NV DPBH/Nutrition|https://nutrition.nv.gov/Resources/Food_Recall/|list
NH|NH DHHS|https://www.dhhs.nh.gov/programs-services/environmental-health-and-you/food-protection|news
NJ|NJ DOH|https://www.nj.gov/health/ceohs/phfpp/retailfood/consumer.shtml|program
NM|NM ENV|https://www.env.nm.gov/foodprogram/|program
NY|NY Ag&Markets + DOH|https://agriculture.ny.gov/food-safety-alerts|list
NC|NC NCDHHS + NCDA|https://www.dph.ncdhhs.gov/programs/environmental-health/emergency-preparedness-and-response/food-product-recalls|list
ND|ND HHS|https://www.health.nd.gov/news/|news
OH|Ohio portal + ODA + ODH|https://ohio.gov/recalls|portal
OK|OK ODAFF|https://ag.ok.gov/disease-alerts/|news
OR|OR OHA|https://www.oregon.gov/oha/PH/newsadvisories/Pages/FoodSafetyAlerts.aspx|list
PA|PA PDA|https://www.pa.gov/agencies/pda/food/food-safety/consumer-protection|program
RI|RI RIDOH|https://health.ri.gov/press-releases|news
SC|SC Consumer Affairs + Ag|https://consumer.sc.gov/consumer-resources/recalls|list
SD|SD DOH|https://doh.sd.gov/topics/food-lodging-safety/food-lodging-safety-news/|news
TN|TN Agriculture|https://www.tn.gov/agriculture/consumers/food-safety/recalls.html|list
TX|TX DSHS|https://www.dshs.texas.gov/food-manufacturers-wholesalers-warehouses/food-alerts-recalls-affecting-texas|list
UT|UT UDAF|https://ag.utah.gov/tag/food-recall/|news
VT|VT AAFM|https://agriculture.vermont.gov/food-safety|program
VA|VA VDH + VDACS|https://www.vdh.virginia.gov/environmental-health/food-safety-in-virginia/food-recalls/|list
WA|WA DOH + WSDA|https://doh.wa.gov/you-and-your-family/food-safety/recalls|list
WV|WV Agriculture|https://agriculture.wv.gov/divisions/regulatory-and-environmental-affairs/recalls/|list
WI|WI DATCP|https://datcp.wi.gov/Pages/Programs_Services/FoodRecalls.aspx|list
WY|WY Agriculture|https://agriculture.wy.gov/food-safety|program
PR|PR Salud|https://www.salud.pr.gov/|news
GU|Guam DPHSS|https://dphss.guam.gov/services/food-establishments|program
VI|VI DOH|https://doh.vi.gov/|program
```

Usage: only query the specific state(s) relevant to the user's location or the recall's distribution list — never sweep all 54. `list` rows are fetchable targets; `news`/`program` rows mean the state relays via press — search `<state> <brand> recall` instead of fetching.

**Local layer** (below state): NACCHO directory (naccho.org/membership/lhd-directory) finds the user's county health department; big metros run real infrastructure (Philadelphia hip.phila.gov/health-alerts; Chicago CDPH alerts; NYC DOH food-safety; LA County's dedicated recalls page — access-limited). For illness reports this is the reporting layer, not usually a recall-record layer.

## §5. Retailer & manufacturer layer (lot-level, non-authoritative)

| Resource | URL | Notes |
|---|---|---|
| Walmart Product Recalls | corporate.walmart.com/recalls | verified live; lot-level for items sold by Walmart |
| Kroger Recall Alerts | kroger.com/i/recall-alerts | verified live; the old /i/recalls is 404 |
| Costco Product Recalls | costco.com/f/-/recalls | verified live; + customerservice.costco.com recall answer page |
| Manufacturer newsrooms | `<brand>.com` /news or /recalls | legitimate but slow; recalls usually announced by the firm first, then agency-posted |

Best lot-level match source ("was MY package affected"); confirm anything that matters at the agency page — retailer hubs are convenience tier, not the record.

## §6. Convenience tier (leads only) and §7 slop (never cite)

**Aggregators** (recall-named private sites/apps): useful discovery, never the endpoint — anything they surface gets confirmed at the agency page. **SEO recall-list content farms — never cite, never trust their dates**: walmartdesk.com, costcoguides.com, eatlikefit.com, menuswithprice.com, moneypilot.com, financebuzz.com class pages ("recall list 2026" auto-generated, frequently stale or wrong). **Media/local TV**: fine for awareness and often the fastest relay of new notices; not the source of record. The universal tier rule: **every authoritative source ends in .gov** (plus uscgboating.org for USCG, salud.pr.gov for PR). Everything else = convenience or caution.

## §8. Scam appendix — fake-recall patterns (the smoke test's evidence base)

1. **Fake recall-alert texts/emails — documented, active.** Press documentation Feb–Mar 2026: fake "Amazon recall alert" texts harvesting payment details (ConsumerAffairs 2026-02-18; NY Post 2026-03-23; thecooldown.com). **The rule: no legitimate recall notice asks for payment or a card "to process your refund."**
2. **Look-alike aggregator domains** with official-sounding branding (recallalert.app, recallradar.company, recallbench.com, getrecalls.com) — private; some fine, none official; verify anything they surface at the agency page.
3. **Call-center phone funnels** — real notices direct to agency/retailer sites, not phone-based refund processing.
4. **Why recalls make good lures** — real notices arrive unexpectedly, carry authority, and promise money back (refund/remedy): the exact emotional profile scammers want. This is why the two-readout design exists: authenticity of the content and recall status of the product are independent facts.

## §9. Query recipes (per surface)

- **Agency list sweep:** `site:fda.gov <brand> recall` · `site:fsis.usda.gov <brand>` · `site:cpsc.gov <brand> recall` · `site:nhtsa.gov <make> <model> recall` — routed per §1. Follow with the agency page fetch when the sweep hits.
- **History depth:** `site:fda.gov <brand> enforcement report` · `<brand> recall <year-1>` · CPSC search-by-company for the manufacturer's full record.
- **Outbreak layer:** `site:cdc.gov <food> outbreak <year>` · fetch cdc.gov/foodborne-outbreaks/outbreaks when the food matches an active investigation.
- **Distribution:** `<state> <brand> recall site:<state-agency-domain>` (from §4) · `<retailer> <brand> recall site:<retailer-domain>`.
- **Scam campaigns (R6/R7):** `<sender domain> phishing` · `fake <brand/retailer> recall text` · `<exact subject phrase> scam`.
- **Lot codes:** `"<lot code>" <brand>` quoted exact-match, then the agency notice's affected-lot table — the table is the record, not the snippet.
