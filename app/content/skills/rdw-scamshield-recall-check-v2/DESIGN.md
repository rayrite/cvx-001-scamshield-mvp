# Design: `rdw-scamshield-recall-check`

Staged recall background-check skill with a zero-search smoke test, product-class-routed agency research, two independent verdict readouts, and an optional geocode-accurate U.S. overview map. Designed 2026-09-19, built the same day. Base design approved in chat; the overview-map feature addition (rendering tech, geocode tiers, config, outputs, verification step) presented and approved separately before implementation.

## Why this skill exists

Recall questions get answered badly in two directions: vibes ("never heard of one, you're fine") that miss a three-week-old FDA notice, and unstructured trawls that land on undated aggregator SEO pages of unknown vintage. Meanwhile the recall-information landscape is a **routing problem** (which agency regulates the item determines where the record lives), and recall anxiety is an **active scam category** (fake recall texts documented Feb–Mar 2026). No single skill in the family covers either. This one routes the first and snaps the second, borrowing the staged structure proven in `rdw-scamshield-check-v2` and the breadth of `rdw-product-dig`.

## Research basis (2026-09)

`research-us-product-food-recall-resources-2026-09/us-product-and-food-recall-resources.md` — every source URL in `references/recall-source-guides.md` comes from it (page verifications dated 2026-09-19). Key findings baked into the design:

- **Jurisdiction split** (§10, §12): FDA ~78% of food ↔ FSIS meat/poultry/processed egg ↔ CPSC consumer products ↔ NHTSA vehicles ↔ FDA drugs/devices/cosmetics ↔ USCG ↔ EPA — the routing matrix is the skill's core lookup.
- **CDC outbreak layer** (§12, F-04): "no recall yet but people are sick" is a real state that needs its own band (🟠 recall-adjacent).
- **State layer** (§18, Appendix A): ~30 states with dedicated lists; unique value = distribution filtering. The full machine-readable table ships in the reference.
- **Bot-walls** (§24, §25): FSIS (Akamai) and NHTSA actively block automated verifiers → the corroboration protocol (§3 of the source guide) with `access-limited` labeling.
- **Fake-recall scams** (§21): refund-fee asks, look-alike domains, call-center funnels → the smoke test's decisive tells.
- **Retailer hubs** (§20): lot-level matching, non-authoritative → R5.

## Key decisions

1. **Two orthogonal verdict readouts.** Recall status (always) and content authenticity (claim-bearing subjects only). A scam text about a never-recalled product and an authentic article about a real recall must not collapse into one verdict; the rubric names cross-readout contamination its cardinal sin. The snap mechanism applies to authenticity ONLY — recall status is a database fact that can never be snapped, and a snap response says "recall status: not checked" with `document` offered (the documentation pass doubles as the honest way to answer the product question).
2. **Stage ½ scope honesty.** The scamshield v2 smoke test can snap whole cases; here most inputs are bare product questions with nothing to smoke-test — those fall through immediately, and the "quick preliminary return" the user asked for is the smoke test **plus** the light routed Stage-1 sweep (which runs automatically; gates guard Stage 2+).
3. **Product-class routing as Stage-0's job.** Routing fixes R1's target before any query is written; the meat/FDA/CPSC misroute is the single most common recall-research failure. Unclear class → class identification is the sweep's first job.
4. **Check lines R1–R8** (agency list · agency databases · CDC layer · state layer · retailer/manufacturer · press · authenticity · community) instead of scamshield's C1–C10 — recall research has a different shape: fewer reputation surfaces, more official-records layers.
5. **Access-limited corroboration protocol** instead of retry loops or giving up: one direct attempt, search-extraction corroboration, labeled, user given the URL. A 🔴 may rest on ≥2 independent confirmations with the limitation named.
6. **Current-vs-past separation is mandatory** in any 🔴 recall record — undated recall claims are exactly what aggregator slop produces.
7. **Overview map: real coordinates on a real basemap, never generated imagery.** Hand-authored HTML loading pinned plotly.js 2.35.2 from CDN (`scattergeo`, `scope:"usa"`, `albers usa` — AK/HI insets native), with **computed SRI hash** (`sha384-cCVCZkAjYNxaYKbM8lsArLznDF/SvMFr1jcZrvOpSTCa0W40ZAdLzHCEulnUa5i7`) on the script tag — computed from the exact CDN bytes, because a guessed hash breaks every map. Zero Python/package dependencies (no plotly/kaleido on the dev machine; the HTML runs in any browser).
8. **Geocode tiers with labeled fallback.** T1 source-stated → T2 Nominatim (User-Agent required; city pins on the city — verified: Detroit → 42.3316, -83.0466) → T3 Census for addresses (`benchmark=Public_AR_Current` required — verified) → T4 model-knowledge for major unambiguous cities only, labeled and confidence-capped. State-only mentions → state-centroid diamonds, never fake city pins. Ambiguous/failure → row kept, lat/lon null, flagged. Non-US → table only.
9. **Map config: `recall-check.config.json`, `overview_map` default ON** for beta per user instruction (absent file = defaults; in-chat override honored). The config file is the stable interface so the default can flip later without touching the skill.
10. **Map outputs are triplets** (interactive HTML + CSV + JSON) and the caption is verbatim: `Markers are plotted from geocoded coordinates in the location table, not from a generated illustration.` Mandatory render verification via chrome-devtools MCP (`new_page` with `file:///`, resize ≥1300×800 — smaller viewports crop the map; agent-browser MCP hangs on local file URLs in this environment), with a static-verification fallback that must disclose itself.

## Files

| File | Content |
|---|---|
| `SKILL.md` | Three-tier intro · scope-down rules · key concepts (subject types, routing, R1–R8, two readouts, coverage, ledger, map) · safety rules · inputs · Stage 0/½/1/gate/N/consolidate procedure (steps 1–18, map = step 18) · output contract · source hierarchy · failure handling · 5 examples |
| `references/smoke-test.md` | Rules (zero network; claim-bearing only; recall status never snap-answered) · snap response shape · S-M/S-P/S-W/S-A item lists with FP guards (retailer texts legitimate; short codes fall through; aggregator breadth is not a tell) |
| `references/subject-check-guides.md` | Six guides — product/food name · SKU/lot/UPC · product website · social post · news article · recall message — each with Extract / check-line priority / Queries / Verification moves / Pitfalls (+Safety where applicable) |
| `references/recall-source-guides.md` | §1 routing matrix · §2 federal sources F-01…F-17 · §3 access-limited protocol · §4 state layer + full 54-row machine-readable table · §5 retailer/manufacturer · §6–7 convenience tier & slop blocklist · §8 scam appendix · §9 query recipes |
| `references/verdict-rubric.md` | Two-readout bands and anchors · snap rules (authenticity only; "not checked" recall status) · confidence · aggregation with anti-contamination rule · honest-verdict rules · coverage map + verdict box formats · plan template · ledger formats · 6 worked micro-examples |
| `references/overview-map.md` | Binding spec (schema, normalization, caption verbatim, no image-gen) · config · pipeline · geocode tiers (Nominatim/Census usage verified) · HTML template with SRI hash + responsive width · CSV/JSON outputs · render verification · skip/honesty rules |

## Testing notes

- **RED (baseline):** the failures this skill exists for — an undirected "is X recalled" that cites a 2024 aggregator page as current; a scary recall text treated as a product fact (or a real recall treated as proof the text is real); an FDA search for a ground-beef recall (wrong agency); a fake recall text researched for minutes when the pay-to-refund ask settles it in seconds.
- **GREEN targets:**
  - Fake recall text (`Example 1` facts) → zero searches, snap 🔴 authenticity, recall status "not checked", `document` offered.
  - Documented recalled product (`Example 2` facts) → 🔴 recall status with agency/date/class/lots, current-vs-past separated, coverage map honest about ⚪ lines.
  - FSIS-routed subject (`Example 3` facts) → access-limited labeling, corroboration-based 🔴, user given the direct URL.
  - Social-post claim (`Example 4` facts) → authenticity 🟡 unverifiable + recall status driven by the record, two separate boxes.
  - Outbreak subject (`Example 5` facts) → 🟠 recall-adjacent, map renders with city pins on cities / state diamonds for statewide counts, size by case count, caption verbatim, CSV/JSON emitted, render verified.
  - Config `overview_map: false` → no map, skip stated in report; "no map this run" override honored and noted.
  - Ambiguous city (Springfield, no state) → row kept, null coordinates, flagged, no pin.
- **Regression targets from the family:** verdict discipline (absence ≠ verification, 🟢 phrasing "no recall record found"), gate compliance (every stage ends with plan + hint), ledger discipline (no repeated queries), honest thinness, victim/consumer-safety path first when the user already ate/used the product.
- **A/B note:** no prior version of this skill exists — v1 of a new line, not a fork; the scamshield lineage is structural, not behavioral, so no A/B against v2 is implied.

---

# v2 — modular, embeddable, responsive visual output (2026-09-19)

**Trigger:** user requirement that the skill's visual output be modular and decoupled for incorporation into another app (a ChatGPT-style chat UI), responsive and appropriate on desktop and mobile. Ships as a **versioned fork per workspace policy** (`rdw-scamshield-recall-check-v2`; v1 preserved in workspace and `~/.claude/skills/` for A/B). Only the visual-output layer changed: research procedure, rubric, smoke test, source guides, CSV/JSON schemas, and the caption/honesty rules are untouched.

## Decisions

11. **Dual-mode artifact, one file.** The generated `_map.html` is simultaneously a standalone page (inline JSON auto-mounts into `#recall-map-auto`) and a drop-in component for a host app, via three documented paths: iframe (with optional `?src=<locations.json>` for live data), custom element `<recall-overview-map data-json|src title as-of>`, and imperative `RecallOverviewMap.create(container, rows, options)` returning `{ setData, setLabels, destroy }`. Rationale: a chat UI can iframe today with zero integration work, while a deeper integration (React/Vue effect calling `create`/`destroy`) needs no fork of the artifact. `Plotly.react` (not `newPlot`) so hosts can stream updated row arrays into an existing card.
12. **Data contract = the location-table schema, nothing else.** The renderer consumes `_locations.json` rows only; it never reads the report file, the CSV, or skill internals. The JSON file pair is the decoupling seam: a host can re-render or re-style every map from the JSON alone. Inline HTML JSON and the `_locations.json` file stay byte-identical at generation.
13. **Scoped styles + theme tokens.** All component CSS lives under `.recall-map-embed` (no bare element selectors — a host page's own `body`/`h3`/`p` styles neither leak in nor get overridden). Theming through CSS custom properties (`--rm-surface`, `--rm-text`, `--rm-muted`, `--rm-border`, `--rm-accent`, `--rm-chip-bg`, `--rm-plot-*`, `--rm-focus`) with `prefers-color-scheme: dark` defaults and `--light`/`--dark` modifier classes — a chat app sets tokens once and every map matches its theme, including the Plotly layout (basemap/land/lake/hover colors read from computed tokens at render time). The standalone page shell (centering + page background) is the only unscoped CSS and is inert when embedded.
14. **Responsive by container, not viewport units.** Plot height derives from `aspect-ratio` (4/3; 1/1 under 480px) with 320–640px clamps, so the card sizes from its actual width in any chat column; `ResizeObserver` (window-resize fallback) keeps Plotly synced. v1's fixed `min-height: 620px` cropped and overflowed narrow cards. Dense state labels default OFF below a 700px container-width breakpoint (a "Labels" toggle restores them; `userToggled` latches so auto-flipping never fights the user) — 21+ size-9 labels collide illegibly on small plots. Coarse pointers (`pointer: coarse`) raise minimum marker sizes (11px vs 8px) for touch targets; the toggle button keeps a 32px min height.
15. **Verification now two viewports.** Desktop ≥1300×800 (as v1) **plus** mobile ~390×844: no horizontal scroll, plot visible, label default off, toggle works, legend/caption present; plus an API liveness check (`RecallOverviewMap.create` exists, custom element defined) — hosts depend on both. Static fallback still discloses itself.
16. **CDN failure is a disclosed error card, not a blank div:** an inline notice states plotly.js failed to load and points to the CSV/JSON as the data of record; no coordinates are invented to compensate. Consistent with the family rule that the table is primary and the map is a rendering.

## Files changed (v1 → v2)

| File | Change |
|---|---|
| `references/overview-map.md` | Rewritten: binding req. 4 (modular/dual-mode/responsive), req. 6 (CDN-failure card), new v2 component template (scoped CSS, tokens, custom element + API + auto-mount, aspect-ratio plot, label toggle, coarse-pointer sizing), "Embedding guide" section for host apps, two-viewport verification, design notes updated |
| `SKILL.md` | Key-concepts map bullet (embeddable component, theme tokens, responsive); step 18 (dual-viewport verification, host-chat-UI requirement); output-contract map-artifacts line (three embed paths, CSV/JSON as data of record) |
| `DESIGN.md` | This section |

Unchanged: `references/smoke-test.md`, `references/subject-check-guides.md`, `references/recall-source-guides.md`, `references/verdict-rubric.md`, all schemas and honesty rules.

## Testing additions (v2)

- Desktop 1300×800 and mobile 390×844 passes on the same generated artifact (Example 5 dataset): markers render at both, label default flips correctly, toggle works, no horizontal scroll at 390px.
- `?src=` fetch path loads the locations JSON at runtime (iframe integration path).
- Custom element + `RecallOverviewMap.create`/`setData`/`destroy` liveness check.
- Dark-mode spot check: `prefers-color-scheme: dark` flips card + basemap tokens.
- CDN-blocked run (script onerror simulated) renders the disclosure card, not a blank div.

---

# v2.1 — ripeness & relevance gauge (2026-09-19)

**Trigger:** user-requested family-wide port, following the same change in `rdw-scamshield-tea2-corpcheck` v1.1 (donor: `rdw-product-dig`). The go/stop gate now gets a priced menu, not just verdicts.

## Decisions

17. **Gauge adapted to R1–R8 and the two-readout discipline.** Per line, score the marginal yield of one more stage (🟢–🔴, 0–100) from ledger signals — novelty rate, lead-pool depth, tier-ceiling gap, repeat rate, slop rate — and rate each line's relevance to the user's situation. Overall aggregation is deterministic; 🟠/🔴 overall replaces the next-stage plan with a consolidation recommendation. The gauge is orthogonal to **both** verdict readouts (R7's yield says nothing about authenticity; an exhausted R1 under a 🔴 recall record is the system working — the finding is complete, not stale). Gauge history rides as ledger Appendix E.
18. **Access-limited ceilings are not yield.** An agency surface that is bot-walled (FSIS Akamai, NHTSA) and attempted per the documented protocol is a *reached-with-limitation* ceiling: search-extraction corroboration counts toward the harvest, the unfetchable page never keeps the gauge green, and the "open it yourself" URL is a user action, never a stage. This binds the gauge to key decision 5 instead of letting it reopen the retry question the corroboration protocol closed.
19. **Hits can be exhausted.** Once the agency notice is fetched with its specifics (date, class, lots, remedy), R1 is exhausted by completion — exhaustion prices *further research*, not the record's cleanliness. Recall space being finite and agency-held, exhaustion arrives sooner than in reputation skills, and the rubric says so up front rather than apologizing for it.
20. **Relevance keyed to situation × angle:** screening vs already-owns (lot-level R5/R4 weight) vs full history (R2) vs outbreak concern (R3) vs claim-bearing content (R7+R1); R7 is ➖ for non-claim-bearing subjects; the `document` pass re-rates as a screening run. The overview map is unaffected — rendering is not research yield and never moves the gauge.

## Files changed (v2 → v2.1)

| File | Change |
|---|---|
| `references/ripeness-rubric.md` | **New** — full gauge rubric: three components, situation/angle relevance defaults, band anchors, access-limited ceiling rule, clean-line + hit-exhaustion shortcuts, render rule (not on snaps; map unaffected), scoring procedure, overall aggregation, anti-gaming rules, output + Appendix E formats, 3 worked micro-examples (incl. the FSIS bot-wall case) |
| `SKILL.md` | Key-concepts gauge bullet + ledger bullet; step 9 (Stage-1 prospect gauge); step 10 (Appendix E in ledger); step 11 (gauge in Stage-1 chat response); step 12 gate (push-back on 🔴 overall); step 16 (re-score + gauge in stage response, plan ordered by relevance × yield); step 17 (final gauge statement); output contract (Ripeness Gauge file section, Appendices A–E, chat order verdicts → gauge → plan) |
| `references/verdict-rubric.md` | Plan rules (relevance × yield ordering, 🟠/🔴 → consolidation recommendation; map is post-processing, not a stage); ledger **E. Gauge history** format |
| `DESIGN.md` | This section |

Unchanged: `references/smoke-test.md`, `references/subject-check-guides.md`, `references/recall-source-guides.md`, `references/overview-map.md`, both readouts' bands and anchors, snap semantics, safety rules, map pipeline. Frontmatter description unchanged (triggering conditions didn't change; near the YAML length ceiling).

## Testing notes (v2.1)

- **Basis:** user-directed port; donor gauge family-proven; the corpcheck Planet Fitness live run demonstrated the gate behavior this formalizes.
- **Untested live in this skill** — first exercised on the next live recall check. Regression targets: snap responses stay gauge-free with recall status "not checked"; the FSIS case (Example 3 facts) must score R1 on the corroboration harvest with the user URL as an action, never as agent yield; a fetched-notice R1 must go 🔴 *by completion* without touching the 🔴 recall verdict's meaning.
- GREEN check to run: re-run Example 2 facts → expect the Stage-1 response to carry a gauge with R1 🟢 prospect (tier-1 gap named), and after the notice fetch + state/retailer fills, overall 🔴 → consolidation recommendation with the map still running (post-processing).

---

# v2.2 — output modes (2026-09-19)

**Trigger:** user requirement — the staged-research skills roll into a ChatGPT-style app where an end-user prompt triggers research; the app needs each stage's full content printable to chat (not just highlights), the end user gets the choice, and the backend developer must flip the default on demand (file for a debugging session, chat for production) without editing skill prose. Applied family-wide the same day (rdw-product-dig, rdw-scamshield-check-v2, rdw-scamshield-tea2-corpcheck).

## Decisions

21. **Three modes, one knob, on the existing config.** `file` (default — current behavior untouched) · `chat` (complete stage content prints to the chat response; no report file unless requested) · `both` (chat content + file maintained). The knob joins the config file this skill already has: `recall-check.config.json` gains `"output_mode"` alongside `"overview_map"` — the two fields are independent (map is post-processing; output mode governs stage responses and the report file).
22. **"Full stage content" defined once in the output contract:** banner, *every* finding with full citation (no 3–6 cap), both verdict boxes when applicable, coverage map, gauge with legend, the stage's **ledger delta** (not a cumulative ledger reprint), the plan. Consolidation in `chat`/`both` delivers the full final report to chat.
23. **Precedence mirrors the map precedent:** in-chat user choice (any time, sticks, noted in report meta) > config file > the default baked into SKILL.md's Inputs bullet (itself a developer lever — edit that one line in the embedded prompt to flip the default).
24. **Snaps exempt; maps always files.** Snap responses are unchanged in every mode. Map artifacts, when produced, are written as files regardless of mode — they are rendered components, linked from chat; `chat` mode removes the *report* file, never the map's data of record.

## Files changed (v2.1 → v2.2)

| File | Change |
|---|---|
| `SKILL.md` | Key-concepts output-mode bullet; Inputs output-mode bullet; steps 10/11 (chat-mode file skip + full-content Stage-1 response); step 16 (chat-mode stage close); step 17 (full final report in chat); output contract (file-scoped "never paste" rule + Output modes block with config schema, map-artifacts-always-files rule); failure handling (chat-mode session-restart caveat) |
| `DESIGN.md` | This section |

Unchanged: `references/smoke-test.md`, `references/subject-check-guides.md`, `references/recall-source-guides.md`, `references/verdict-rubric.md`, `references/ripeness-rubric.md`, `references/overview-map.md` (its config documentation names the file, not the field list — the SKILL.md modes block is the field's home), both readouts, snap semantics, map pipeline. No config file shipped (absent = defaults, as before). Frontmatter description unchanged.

## Testing notes (v2.2)

- **Untested live.** GREEN checks: (a) default run with no config file → behavior identical to v2.1, map still ON; (b) `{"output_mode": "chat", "overview_map": true}` → full stages in chat, no report file, map artifacts still written and linked at consolidation; (c) in-chat "in chat" → sticks for the check, noted in meta; (d) "no map this run" and output mode stay independent toggles.
- Regression targets: snap responses unchanged; two-readout separation intact in chat-mode full content (both boxes when applicable); access-limited labels survive into full chat citations.
