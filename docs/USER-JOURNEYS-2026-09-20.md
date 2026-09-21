# User journeys & ideal customer profiles — the ScamShield demo app

**Date:** 2026-09-20 · **Scope:** the app in `zai-demo-app-2026-09/` (all eight surfaces)
**Companion artifacts:**
[live journey simulation (hi-fi mockup)](mockups/recall-check-simulation.html) ·
[screenshots](mockups/screens/) (9 PNGs, listed in §5)

---

## 0. The app in one paragraph

ScamShield is a hosted deep-research assistant for scam, recall, and
dark-pattern questions. A visitor pastes something suspicious — an email, a
text, a listing, a lot code, a company name — and staged research agents
(`rdw-*` skills) check it against live web evidence: government records,
press, retailer data, community reports. Every research surface reports
**verdict, confidence, and ripeness as three separate, independent
indicators** (the app's UVP, §4), every finding is cited with source and
date, and multi-stage investigations advance **one gated stage at a time** —
the user decides whether each next stage is worth running. A centralized
Universal Design Language (`udl.json` → `/udl.css` + `/udl.js`) themes every
page, including the embedded research wikis.

---

## 1. Ideal customer profiles (ICPs)

| | Profile | Trigger moment | Primary surfaces | Success looks like |
|---|---|---|---|---|
| **ICP-1** | **The Cautious Consumer** — anyone active in email/text/marketplaces who lacks the time or background to vet what lands in their inbox | “Is this real? Should I click / pay / reply?” | `/quick` (e-commerce/email check), `/check` (with screenshots), `/chat` | A cited verdict **before** acting; avoided loss; zero jargon |
| **ICP-2** | **The Household Guardian** — parents, pet owners, caregivers, adult children helping older parents | “Was this recalled? Is the lot in my fridge affected?” | **`/chat` → RecallCheck v2** (§3), `/quick` (recall) | Agency-routed answer naming lots, dates, remedy; safety steps first |
| **ICP-3** | **The Micro-Seller / Reseller** — eBay/Etsy/Marketplace sellers and tiny e-commerce operators sourcing stock | “Is this supplier legit? Is this brand a counterfeit risk? Does this company have a dark-pattern record?” | `/chat` → TEA2 CorpCheck & ProductDig, `/quick` (company / reliability) | Sourcing decision backed by complaint history, registers, owner sentiment |
| **ICP-4** | **The AI-Product Evaluator** — product/UX teams studying agentic-research UX patterns (the demo's meta-audience) | “How should a gated multi-stage research agent present evidence, cost-of-more-research, and confidence?” | All surfaces, `/theme`, `/apps`, this document | A working reference implementation: staged gating, three-indicator contract, centralized theming |

**Anti-profile (stated honestly):** the app is research assistance, not legal,
financial, or medical advice; verdicts are evidence snapshots, not
certificates of safety (the footer says so on every page). It is not built
for high-volume/automated abuse — turn caps, image caps, and rate posture
reflect that.

---

## 2. The journey catalogue — every surface

### J1 · First touch → waitlist (landing `/`)
Hero (“deep-research checks for scams, recalls & dark patterns”) →
auto-rotating phone-mockup carousel (4 s, pause-on-hover, dots/arrows/keys) →
feature cards (flag-aware; hide disabled surfaces) → how-it-works →
testimonials **labeled illustrative** (fairness mandate) → email waitlist →
`POST /api/waitlist` appends to a flat file on the volume (dedup + validation;
count-only GET — addresses never leave the server). *Exit:* any nav item.

### J2 · Staged Check v2 (`/check` — skill `rdw-scamshield-check-v2`)
The button-driven staged agent for e-commerce/email legitimacy checks.
1. Submit: paste text, add up to 5 screenshots (`worry` = legitimacy /
   counterfeit / non-delivery / payment-safety; region) → `202` + job id.
2. **Stage 0 + ½:** vision intake (glm-5.3-flash) transcribes the screenshots;
   a zero-search **smoke test** snaps obvious scam tells to an instant verdict.
3. **Triage/verify stages** run; the job page polls `/api/jobs/{id}` and
   renders each stage; **gates are buttons** — `go` / custom direction / `stop`.
4. `done` → final verdict blocks + cumulative markdown report
   (`/api/jobs/{id}/report`).
Interrupted jobs (redeploy) are marked *interrupted* at boot, never left
hanging. Screenshot: [app-02-check.png](mockups/screens/app-02-check.png).

### J3 · Skill chat (`/chat` — 3 skills)
Multi-turn conversations bound to one skill: **ProductDig** (products),
**RecallCheck v2** (§3 — the highlighted journey), **TEA2 CorpCheck**
(companies). Each reply = one stage of that skill's contract; gates work by
replying `go` / a direction / `stop`; per-reply sources; conversation list in
the sidebar; **12-turn cap** per conversation (`MAX_CHAT_TURNS`, env-
overridable); live budget counters (model calls, tokens, search results).
Screenshot: [app-03-chat.png](mockups/screens/app-03-chat.png).

### J4 · Quick research (`/quick` — 4 single-pass modes)
The paste-ready prompts from the prompts track as one-pass checks:
e-commerce/email · recall · company · product reliability. No stages, no
gates — one research pass, then the reply with **verdict / confidence /
ripeness as three separate lines** + sources. Screenshot:
[app-04-quick.png](mockups/screens/app-04-quick.png).

### J5 · Learning Center (`/learn`)
Menu of the research wikis (US consumer dark patterns; e-commerce seller
scams). Wikis open **same-window inside the app frame** — site nav + footer
injected by `/app.js` — and are themed by the UDL through a token bridge, so
`/theme` restyles them like every other page. *Journey:* land → browse →
read in-frame → jump to a check surface from what was learned.

### J6 · App Library (`/apps`)
Dynamic menu built at request time from `content/spas/*.html` — drop in or
delete any single-page app and the menu reflects it on the next load, no
restart. *Journey:* the extensibility pitch — “new capability = one file.”

### J7 · Theme editor (`/theme`)
Edit the design language (colors, fonts, radius, shadow; auto/light/dark),
live preview; every page and both wikis restyle on next load. *Journey:*
ICP-4's playground; also the demo of “one config, whole product.”

### J8 · Video samples (`/video`)
Two placeholder MP4 players with native controls, Range-streamed
(`206 Partial Content`) from the data volume; a 1-byte probe per player
reports *streaming + size* / *not found* / *found-but-won't-decode*. A
standalone capability demo (see `VIDEO-HOSTING-RAILWAY.md`).

---

## 3. ★ Highlighted journey — multi-stage deep research with **RecallCheck v2**

> **Which surface:** `/chat`, mode **🥫 RecallCheck v2** (`skill:recall-check`,
> backed by `rdw-scamshield-recall-check-v2`). Not to be confused with (a)
> `/check`'s `rdw-scamshield-check-v2` (the e-commerce/email staged agent) or
> (b) `/quick`'s single-pass recall prompt. The full skill contract:
> `app/content/skills/rdw-scamshield-recall-check-v2/SKILL.md`.
> The scenario below is the one animated by the
> [live simulation](mockups/recall-check-simulation.html) — **illustrative:
> “Fjordline Smokehouse” is fictional and every finding/citation is simulated.**

### 3.1 The persona and the trigger

*ICP-2, the Household Guardian:* “Was **Fjordline Smokehouse cold-smoked
salmon** recalled? I have a packet in the fridge — **lot L-2417**, best-by
11/2026. I haven't opened it.” One message into a fresh RecallCheck v2
conversation. Safety posture starts immediately: the skill's consumer-safety
path applies because the user already owns the product.

### 3.2 Step-by-step

| # | Stage | What the user sees | Indicators after (verdict · confidence · ripeness) |
|---|---|---|---|
| 1 | **Stage 0 — intake** (no searching) | Agent confirms subject (product + lot), routes the product class (**fish → FDA**, not FSIS), notes “already owns” → keep packaging, don't eat until known; output mode `file`. | — · — · — (not yet run) |
| 2 | **Stage ½ — smoke test** (zero searches) | System note: input is *not claim-bearing content* (no message claiming a recall) → falls through instantly. *(If it were a “recall text” demanding a $0.99 fee, this is the 5-second 🔴 snap-verdict path.)* | — · — · — |
| 3 | **Stage 1 — routed triage** (10 searches, ≤3 fetches) | Key findings with cite chips: FDA Class I alert (Listeria, 2026-09-08, lots L-2415…L-2421, **access-limited** snippet), CDC outbreak investigation (14 cases / 6 states), 2 trade-press relays. Verdict boxes + coverage map + ripeness gauge + a **default Stage-2 plan** + gate hint. “Do not eat it while we verify.” | **🔴 recall record found** *(provisional)* · **Medium** (snippet-verified) · **🟢 fresh, 78/100** (4 lines unchecked, 9 leads pooled) |
| 4 | **Gate** | User replies: *“go — and check whether Montana is in the distribution list specifically.”* The described direction customizes the plan (Montana added as a named target). | unchanged |
| 5 | **Stage 2 — verify** (11 searches, 6 fetches) | 🆕 FDA notice **fetched in full** (Class I; 11 states; remedy: return for refund) · CDC updated 9 states/16 cases · **Montana list includes the lot range** ✅ · retailer hub: **L-2417 → affected**, refund without receipt · a press-vs-CDC discrepancy **surfaced, not silently resolved** (CDC wins on tier). Then a one-time **push-back**: coverage nearly complete, ripeness thinning — the one targeted option left is the past-recall archive sweep. | **🔴 documented** · **High** (tier-1 fetched + 3 independent layers agree) · **🟠 thinning, 34/100** (novelty 2/11; 2 low-relevance leads left) |
| 6 | **Gate** | User replies: *“stop — that's everything I needed.”* | unchanged |
| 7 | **Consolidation** | Final verdict boxes + one-paragraph basis + **final gauge statement** (“further stages would not pay — …”) + recommended actions (don't eat; return for refund; if consumed & symptomatic → clinician + report to state health dept; monitor the CDC page) + report file `recall-check_fjordline_2026-09-20.md` + **overview map** of the 9 outbreak states (default ON at beta). | **🔴 documented · final** · **High** · **🔴 exhausted, 8/100** |

Screenshots of steps 1, 3, 5, 7 (light) and 5 (dark):
[sim-01](mockups/screens/sim-01-intake.png) ·
[sim-02](mockups/screens/sim-02-stage1-triage.png) ·
[sim-03](mockups/screens/sim-03-stage2-verify.png) ·
[sim-04](mockups/screens/sim-04-final.png) ·
[sim-05](mockups/screens/sim-05-stage2-dark.png).

### 3.3 The indicator arc (why this journey is the demo of the UVP)

| Stage | Verdict (recall status) | Confidence | Ripeness |
|---|---|---|---|
| Stage 1 — triage | 🔴 record found — **provisional** | **Medium** (tier-1 snippet + 2 press confirmations) | **🟢 78 fresh** — lots left to verify |
| Stage 2 — verify | 🔴 record found — **documented** | **High** (fetched + 3 layers agree) | **🟠 34 thinning** — novelty falling |
| Final | 🔴 documented | **High** | **🔴 8 exhausted** — more digging wouldn't pay |

The verdict **pinned** at Stage 1; confidence **climbed** as the agency
record was fetched; ripeness **fell** as the remaining value of another
stage was spent. Three axes, three different trajectories, one check —
which is exactly why they are never merged (§4).

### 3.4 Guardrails the user experiences as UX (not rules text)

- **One stage per reply** — never bundled; the gate hint ends every stage.
- **Push-back, once** — if coverage is complete or ripeness 🔴, the agent
  shows its ledger math (novelty rate, empty lead pool) and offers the
  single most-targeted option instead of obediently burning another stage.
- **Ledger discipline** — no repeated queries; contradictions surfaced.
- **Coverage map** — the honesty device: a 🟢 “no record found” is only
  worth its coverage.
- **Verdict discipline** — “FDA recall notice dated 2026-09-08, Class I,
  undeclared allergen,” never “this product is dangerous garbage.”
- **Safety-first paths** — already-ate → safety steps lead; already-paid →
  victim path (dispute, report, recovery-fraud warning).

---

## 4. The three-indicator UVP — verdict · confidence · ripeness

**The standing contract** (from the chat preamble baked into every skill
mode): *“Verdict, confidence, and ripeness are three separate, independent
indicators — never merged, never derived from each other.”*

| Indicator | The question it answers | Grounded in | Moves when |
|---|---|---|---|
| **Verdict** (two readouts: recall status + content authenticity) | *What does the record show?* | Agency/CDC/government records, press, retailer, community — tiered sources with dates | A finding lands or is corrected |
| **Confidence** | *How solid is that reading?* | Tier of the best source, fetched vs snippet-verified, independent confirmations, open contradictions | Evidence firms up (snippet → fetched) or a contradiction opens |
| **Ripeness** | *Would one more stage pay?* | Novelty rate, lead-pool depth, tier-ceiling gap — “the gate's price tag” | Value is extracted: fresh 🟢 75–100 → yielding 🟡 50–74 → thinning 🟠 25–49 → exhausted 🔴 0–24 |

**Why separating them is the value:** each combination is a different
decision. 🔴 + Medium + 🟢 = *act on the warning now; verifying will pay* —
the Stage-1 moment above. 🔴 + High + 🟠 = *act; further digging is
optional* — Stage 2. 🟢 + Low + 🔴 = *no record found, but we've squeezed
what there is to find — “absence is not verification”* — the honest thin-
record case. Merge the three into one score and every one of those states
collapses into an ambiguous number that hides exactly the choice the user
faces: **act now, or pay for one more stage.**

---

## 5. The mockups & screenshots

| Artifact | What it shows |
|---|---|
| [mockups/recall-check-simulation.html](mockups/recall-check-simulation.html) | **The live simulation.** Open the file directly in any browser (UDL tokens from `udl.json` are inlined, auto light/dark + toggle). Press **▶ Run simulation** to watch the whole §3 journey animate — transcript, indicators, coverage map, ledger, history table — or click any stepper chip to jump to a stage. |
| [screens/sim-01-intake.png](mockups/screens/sim-01-intake.png) | Step 1 — intake & routing; indicators idle |
| [screens/sim-02-stage1-triage.png](mockups/screens/sim-02-stage1-triage.png) | Step 3 — Stage-1 triage; first indicator snapshot (🔴 provisional · Medium · 🟢 78) |
| [screens/sim-03-stage2-verify.png](mockups/screens/sim-03-stage2-verify.png) | Step 5 — Stage-2 verify (🔴 documented · High · 🟠 34) |
| [screens/sim-04-final.png](mockups/screens/sim-04-final.png) | Step 7 — consolidated final; full history table visible |
| [screens/sim-05-stage2-dark.png](mockups/screens/sim-05-stage2-dark.png) | Stage 2 in **dark mode** (UDL dark palette) |
| [screens/app-01-landing.png](mockups/screens/app-01-landing.png) | Real app — landing `/` |
| [screens/app-02-check.png](mockups/screens/app-02-check.png) | Real app — `/check` staged agent |
| [screens/app-03-chat.png](mockups/screens/app-03-chat.png) | Real app — `/chat` with the RecallCheck v2 mode selected |
| [screens/app-04-quick.png](mockups/screens/app-04-quick.png) | Real app — `/quick` single-pass |

The four `app-*` shots are the **live demo app** (2026-09-20, live mode);
the five `sim-*` shots are the mockup. The mockup exists because a real
multi-stage run spends research credits and takes minutes — the simulation
compresses the same contract into 15 seconds and is safe to demo offline.

---

## 6. Real vs. illustrative

- **Real:** every surface, the gating mechanics, the three-indicator
  contract, coverage-map and ripeness semantics, legends, UDL theming,
  waitlist, flags, the `/chat` mode registry — all running in this repo.
  With no `ZAI_API_KEY` the app runs in an honestly-labeled **demo mode**
  (canned replies marked as demo).
- **Illustrative:** the simulation's scenario content — “Fjordline
  Smokehouse,” its recall, dates, case counts, citations — is fictional
  mockup data, labeled as such on-screen and here. The landing page's
  testimonials are labeled illustrative for the same fairness-mandate reason.

## 7. Sources

- `app/content/skills/rdw-scamshield-recall-check-v2/SKILL.md` (stage
  contract, two-verdict readouts, ripeness bands, gates, guardrails)
- `app/agents.py` (chat preamble: indicator-independence rule, gate verbs,
  fairness/balance rules; mode registry)
- `app/main.py`, `app/features.py`, `app/chatstore.py` (surfaces, flags,
  12-turn cap), `app/udl.json` (design tokens mirrored into the mockup)
- Screenshots captured 2026-09-20 from the running app (live mode) and the
  mockup via Playwright.
