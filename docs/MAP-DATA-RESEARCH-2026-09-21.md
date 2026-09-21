# Threat Radar — real-data research for the three map scenarios

Research date: 2026-09-21. Purpose: source verifiable, plottable real data for
the `/map` page's three scenarios (vehicle recall · food recall · disease
outbreak), prioritizing Detroit / Tri-County (Wayne, Oakland, Macomb,
Washtenaw) connections. Every row plotted on the map carries the citation in
the location table; this file is the full audit trail.

Scope statement: pick ONE well-sourced event per scenario, recent (2025–2026),
with geography accurate enough to plot — dates, counts, and place names must
trace to a fetched primary source, not memory.

---

## Scenario B — Food recall: Salmonella Enteritidis / shell eggs (CHOSEN)

**Event:** Midwest Poultry Services, L.P. (dba MPS Egg Farms) recalled
1,589,577 dozen white + brown cage-free shell eggs (~19 million eggs) on
**July 22, 2026**, produced/distributed from its Texas farms June 6–July 3,
2026. FDA classified it **Class I on Aug 12, 2026** (enforcement report
Aug 19): entries **H-1230-2026** (white, 27 configs incl. Kroger, Brookshire's
Farm Fresh, Super 1 Foods, Cal-Maine Sunups) and **H-1229-2026** (brown,
Simple Truth – Kroger). CDC investigation **closed Sept 3, 2026**.

**Illness geography (CDC final, as of Sept 3, 2026):** 134 cases · 18 states ·
34 hospitalized · 0 deaths; onsets Nov 21, 2025 – Aug 12, 2026; 85% of 54
interviewed ate shell eggs; strain resistant to nalidixic acid.

| State | Cases | | State | Cases |
|---|---|---|---|---|
| TX | 99 | | CO, IL, **MI**, MO, MS, NC, NV, NY, SC, WV | 1 each |
| LA | 8 | | | |
| AR | 5 | | | |
| AZ | 4 | | | |
| NM | 3 | | | |
| GA, OK | 2 each | | | |

**Distribution (FDA enforcement report, verbatim):** Arkansas, Louisiana,
Mississippi, New Mexico, Oklahoma, Texas. Retail: Kroger (TX, LA);
Brookshire's banners (TX, OK, AR, LA).

**Plottable sites:** farms at Kurten, TX (Brazos Co.) and Center, TX (Shelby
Co.) — *single source (Marler Clark)*; recalling-firm HQ North Manchester, IN
(openFDA). Michigan angle: 1 reported case (residence state; no county detail
exists).

**Caveats (load-bearing):** per-state counts are CDC's final update as
compiled by Marler Clark / Food Poison Journal — CDC/FDA publish only totals +
the state list. Farm cities single-sourced. The Hill / Detroit Free Press
items seen via search summaries only.

**Sources:**
- CDC investigation page (upd. 9/3/26): https://www.cdc.gov/salmonella/outbreaks/shell-eggs-07-26/investigation.html
- FDA outbreak page (upd. 9/3/26): https://www.fda.gov/food/outbreaks-foodborne-illness/outbreak-investigation-salmonella-eggs-july-2026
- FDA recall notice (7/22/26): https://www.fda.gov/safety/recalls-market-withdrawals-safety-alerts/midwest-poultry-services-lp-recalls-shell-eggs-due-possible-salmonella-enteritidis-contamination
- openFDA enforcement entries (8/19/26): https://api.fda.gov/food/enforcement.json?search=%22Midwest+Poultry%22&limit=5
- Marler Clark per-state table (9/4/26): https://marlerclark.com/egg-salmonella-outbreak-sickens-98-in-17-states

---

## Scenario A — Vehicle recall: Ram 1500 rearview camera, Stellantis/FCA (CHOSEN)

**Event:** FCA US LLC (Stellantis) recall **NHTSA 26V-560000** / FCA campaign
**83D**, filed with NHTSA **Sept 1, 2026**. Certain 2025–2026 Ram 1500 (DT)
pickups built **Oct 6, 2023 – Feb 23, 2026**; **239,131 U.S. vehicles**,
100% estimated with defect. Suspect radio software may prevent the rearview
image from displaying while backing — FMVSS 571.111 S6.2.6 noncompliance, no
driver warning, no crashes/injuries disclosed in the Part 573 report.

**Remedy/status:** free software update (OTA or dealer), estimated Q3 2026 —
"not currently available" per the Sep 2, 2026 dealer letter; dealer notice
+ VIN search on nhtsa.gov from ~Sep 9, 2026; owner letters Sep 24 – Oct 2,
2026.

**The Metro Detroit chain (all plottable, all cited):**
- **Novi, MI** (Oakland Co.) — Harman Becker Automotive Systems, 30001 Cabot
  Dr — radio supplier (Part 573 report)
- **Sterling Heights, MI** (Macomb Co.) — Sterling Heights Assembly Plant,
  where the 2025–26 Ram 1500 (DT) is built (Stellantis release 4/17/25;
  ⚠ the Part 573 report does not name the plant — single fetched source)
- **Auburn Hills, MI** (Oakland Co.) — FCA US HQ, 800 Chrysler Dr (Part 573)

**Negative finding:** no per-state registration/distribution data exists for
this recall in any source — the map plots the chain sites + a nationwide
scope row (239,131) and invents nothing.

**Alternates kept on file:** 26V-495000 (Ram 1500 seat-belt anchor, ~1.27M
US units — count search-level only, verify the Part 573 PDF before use) and
the ~Jun 30, 2026 Ford park/rollaway recall (~741k, Expedition/Navigator/
Explorer/Aviator/F-150; Dearborn Rouge F-150 tie — search-level only).

**Evidence files:** `recall-evidence/RCLRPT-26V560.pdf` (+.txt) and
`recall-evidence/RCMN-26V560.pdf` (+.txt) — downloaded primary sources
(untracked).

**Sources:**
- NHTSA Part 573 report (9/1/26): https://static.nhtsa.gov/odi/rcl/2026/RCLRPT-26V560-9456.pdf
- FCA dealer letter 83D (9/2/26): https://static.nhtsa.gov/odi/rcl/2026/RCMN-26V560-5489.pdf
- Stellantis SHAP press release (4/17/25): https://blog.stellantisnorthamerica.com/2025/04/17/2-million-strong-and-counting-stellantis-sterling-heights-assembly-plant-celebrates-ram-1500-milestone/
- USA Today (9/4/26): https://www.usatoday.com/story/cars/recalls/2026/09/04/ram-1500-vehicles-recalled/91609746007/

---

## Scenario C — Disease outbreak: COVID-19 late-summer wave, variant SW.2, CDC NWSS wastewater (CHOSEN)

**Why not flu:** CDC FluView week 36 (ending Sep 12, 2026) shows **every
jurisdiction at Minimal ILI activity** — 1.8% positivity, 1.6% ILI, 1,486
hospitalizations, 95.9% influenza A. An all-flat map is honest but useless as a
demo, so the scenario shows the respiratory signal that IS moving. (Michigan
Flu Focus, wk ending 9/11/26: ILI 0.5% wks 32–35, 0 outbreaks, 68 flu
admissions. 2026–27 season starts MMWR week 40.) The rejection is disclosed on
the map itself (caption + chip) — the negative finding is part of the demo.

**Event (plotted):** CDC National Wastewater Surveillance System (NWSS)
**wastewater viral activity level (WVAL)** for COVID-19, **week ending Sep 12,
2026** — 49 jurisdictions with data. National level **2.85 (Low)**, climbing
from ~1.0 in mid-July; for scale, the summer-2025 XFG wave peaked at 9.13.

**Per-state values (48 plotted + USVI listed):** tiers are CDC's own cut
points; the map unfolds hottest tier first. Very high: **TX 16.42** (prior
14.87; ED visits the only Moderate in the U.S.; Rt 0.88 Declining — peak may be
passing), USVI 13.81 (listed, not plotted — outside the albers-usa projection).
High: CA 8.98, FL 8.79 (prior 5.38 — largest climb in tier), WA 8.42 (Rt 1.12
— fastest sustained growth). Moderate (8 states): HI 7.35, MS 6.77, NV 6.06,
NC/SC 5.77, AL 5.08, KY 5.00, MA 4.99 (prior 1.67 — tripled, sharpest rise).
Low (14): NM 4.83 … GA 2.85 (down from 8.12) … CO 2.69. Very low (22): NH
2.34 … **MI 1.41** … WV 0.30. Full value table with prior-week comparisons in
`map.html` rows / `covid_wastewater_by_state_2026-09-12.csv` (evidence file,
untracked). No data this week (listed, amber): AZ (had 14 sites the prior month
— a one-week gap, not zero activity), GU, MT, ND.

**Michigan / Tri-County detail (the local angle):** statewide **1.41 Very Low
across 28 sites (~4.2M covered), Rt 1.05 "Likely Growing"** — but NWSS site
data (dataset atcp-73re) shows the sewershed **serving Washtenaw County (incl.
Ann Arbor, pop 150,000) at 6.86 Moderate** (prior week 10.54 High, easing), and
the Tri-County sites at 3.48–4.15 Low, declining week-over-week: Macomb+Oakland
(1,482,000) 4.15, Macomb+Wayne (492,000) 3.85, Oakland+Wayne (840,600) 3.48,
plus a small Oakland-only site (13,900) at 1.44. **These five rows are listed,
not plotted**: the state feed publishes served counties and populations, not
site coordinates — plotting a county centroid would fake precision the data
doesn't have. This is the same restraint as the recall scenarios' "ambiguous —
listed, not plotted" rows.

**Variant SW.2 (context, in caption):** SW.2 leads at **20.7% of estimated
infections** (95% PI 16.4–25.8) for the 4-week period **ending Aug 1, 2026** —
CDC's newest published estimate, which lags ~7 weeks (posted Aug 28). XFG.1.1
15.8%, RW.1.1 9.2%. SW.2 trajectory: 0.8% (period ending 6/6) → 6.7% (7/4) →
20.7% (8/1). Regionally: **Region 10 (PNW) 40%**, Region 6 (South-Central)
25%, Region 9 23%, Region 5 (Great Lakes incl. MI) 14.3%, Region 2 (NY/NJ)
7.1%. WHO variants under monitoring as of 7/27/26: XFG, NB.1.8.1, PQ.16.1.1,
BA.3.2.

**Caveats (load-bearing):**
- USA Today described the national picture as "high" while CDC's own WVAL is
  2.85 Low — CDC is primary; the map plots CDC numbers only.
- Stale 2025 articles still claim XFG.1.1 at 22–39% — recycled from last
  summer's wave; do not use.
- NWSS low-coverage states (MS/TN/LA: 2 sites; WV: 1) swing week-to-week on
  noise — flagged in row notes.
- The research agent's population-weighted aggregation of MI site data
  disagreed with the official state value (3.55 vs 1.41) — **only official
  state values are plotted**; site rows are shown as reported.
- covid.cdc.gov/covid-data-tracker is retired — all citations use the current
  cdc.gov/data.cdc.gov URLs below.
- ED-visit activity (only TX Moderate) and ARI activity (all Very Low except
  AL/OH/WY Low) were checked and left out of the map — one metric per card
  keeps the legend honest.

**Sources:**
- CDC NWSS state wastewater levels (wk ending 9/12/26): https://www.cdc.gov/wastewater/respiratory-viruses/state.html
- CDC respiratory activity levels (national 2.85 Low; updated 9/18/26): https://www.cdc.gov/respiratory-viruses/data/activity-levels.html
- CDC SARS-CoV-2 variant proportions (jr58-6ysp; SW.2 20.7%, period ending 8/1/26): https://data.cdc.gov/Laboratory-Surveillance/SARS-CoV-2-Variant-Proportions/jr58-6ysp
- CDC NWSS site-level data (atcp-73re; MI sewershed values): https://data.cdc.gov/Public-Health-Surveillance/NWSS-public-SARS-CoV-2-wastewater-metric-data/atcp-73re
- CDC FluView week 36 (flu rejection): https://cdc.gov/fluview/surveillance/2026-week-36.html · MDHHS Michigan Flu Focus: https://www.michigan.gov/flu/surveillance
- WHO SARS-CoV-2 variant tracking (VUM list): https://www.who.int/activities/tracking-SARS-CoV-2-variants
