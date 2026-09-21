# zai-demo-app-2026-09

The full ScamShield **demo web app** — a copy of the staged-agent service from
`../zai-deep-research-railway-2026-09/` (kept untouched as the backup/PRIMER
track) extended into a complete product-shaped demo: SaaS front door, chat
surfaces for the research skills, Learning Center, dynamic app library, and a
centralized design system.

Runs **demo-first**: with no `ZAI_API_KEY` every surface works end-to-end with
canned, honestly-labeled responses. Set the key and the same flows call z.ai
GLM models with live web search.

## Quick start (local)

```bash
cd app
python -m venv .venv && .venv/Scripts/pip install -r requirements.txt
.venv/Scripts/python -m uvicorn main:app --port 8000
```

Open **http://127.0.0.1:8000** — that URL is the "front door" (landing page)
to hand out; all end-user functions hang off its nav.

Go live: copy `.env.example` → set `ZAI_API_KEY` (see the railway track's
[PRIMER](../zai-deep-research-railway-2026-09/PRIMER.md) for hosting + cost
notes; the operating characteristics are the same, plus the new surfaces).

## The surfaces

| Route | What it is |
|---|---|
| `/` | SaaS landing: sticky header, hero, auto-rotating phone-mockup carousel (4s, pause on hover, dots + arrows + keys), features, how-it-works, illustrative-labeled testimonials, email waitlist → flat file |
| `/check` | The staged **rdw-scamshield-check-v2** agent (backup track's UI, now UDL-themed): vision intake → snap smoke test → triage/verify with gates as buttons |
| `/chat` | **Multi-turn skill chat** — the three remaining skills (`rdw-product-dig`, `rdw-scamshield-recall-check-v2`, `rdw-scamshield-tea2-corpcheck`) with SKILL.md + references as the system prompt; replies drive the gates (`go` / direction / `stop`); conversation list, per-reply sources, turn cap |
| `/quick` | **Single-pass quick research** from the paste-ready prompts in `../zai-scamshield-prompts-2026-09/` (4 modes; verdict/confidence/ripeness as independent lines) |
| `/learn` | **Learning Center** — menu of the research wikis (`research-us-consumer-dark-patterns-2026-09/wiki`, `research-ecommerce-seller-scam-wiki-2026-09/wiki`), served from `content/wikis/`. Wikis open in the same window inside the app frame (site nav + footer) and are themed by the UDL via a token bridge — `/theme` restyles them like every other page |
| `/apps` | **Dynamic App Library** — menu built at request time from `content/spas/*.html`; drop in or remove any single-page app and the menu reflects it on next load (no restart) |
| `/video` | **Sample video players** — two MP4 placeholders (`demo1.mp4`, `demo2.mp4`) with native controls, Range-streamed (`206 Partial Content`) from `data/videos/` (the volume on Railway); a 1-byte probe per player reports streaming + size, missing, or won't-decode (codec) |
| `/theme` | **Universal Design Language editor** — edit `udl.json` (colors, fonts, radius, shadow, light/dark/auto) with live preview; every page restyles on next load |

Verdict, confidence, and ripeness are **three separate, independent
indicators** everywhere (standing mandate), and all research output keeps the
fairness mandate: balanced, no unsubstantiated claims, favorable findings
reported like adverse ones.

## Feature flags

`app/features.json` — `check · chat · quick · learning · apps · video · theme ·
waitlist`. A flag is only *effective* when its content exists (e.g. `learning`
needs ≥1 wiki in `content/wikis/`; `video` has no content dependency — the
placeholders are the point). `GET /api/features` reports set vs. effective;
`python cli.py status` prints the same in the terminal; the nav and landing
feature cards hide disabled surfaces.

## Layout

```
app/
  main.py          FastAPI: jobs API + chat + modes + wikis/spas menus + UDL
                   + waitlist + pretty routes; mounts /learn/wiki, /apps/spa,
                   /videos (data volume), then static/ LAST
  agents.py        mode registry: 3 skill modes + 4 quick modes, system-prompt
                   builder, honestly-labeled demo replies
  chatstore.py     conversations (JSON on DATA_DIR/chats), MAX_CHAT_TURNS cap
  features.py      flags + content-aware effectiveness + inventory
  udl.py/udl.json  the design language: config → /udl.css + /udl.js
  orchestrator.py  staged check state machine (unchanged from backup track)
  skillkit.py      skill files → per-stage prompts (now under content/skills/)
  zai.py           thin z.ai client (glm-5.3-flash intake, glm-5.3 research)
  jobs.py          job store + cumulative report files
  cli.py           status + the 64-check expected-vs-actual verify suite
  smoke_test.py    the staged-agent API suite (27 checks)
  static/          landing, check, chat, quick, learn, apps, theme + shared
                   app.css/app.js (nav, flags, markdown via marked+DOMPurify
                   SRI-pinned, canvas image downscale)
  content/
    skills/        4 rdw-* skills (check-v2 feeds the staged track; the other
                   3 feed chat)
    prompts/       4 single-pass system prompts
    wikis/         2 wiki HTMLs bridged onto the UDL (aliased tokens →
                   /udl.css custom properties; app chrome via /app.js)
    spas/          single-page apps — the dynamic menu's folder
```

## Testing (no blind faith)

```bash
# with the server running on :8000
PYTHONIOENCODING=utf-8 .venv/Scripts/python cli.py verify
# staged-agent suite expects :8111
.venv/Scripts/python -m uvicorn main:app --port 8111 &
PYTHONIOENCODING=utf-8 .venv/Scripts/python -c "import smoke_test; smoke_test.main()"
```

- `cli.py verify` — **71 checks, expected vs. actual, exit 1 on any FAIL**:
  health, flags/inventory, all 7 modes, every page + marker, UDL round-trip
  (POST → GET → /udl.css → restore), wiki menu + titles parsed from files
  + UDL hook & app-frame wiring per wiki + same-frame links, **dynamic SPA
  add/remove without restart**, demo chat (quick + skill + turn counting +
  error paths), waitlist (append/dedupe/reject/flat-file/cleanup), staged
  check end-to-end (gate → stop → done → final verdict → report).
  Cleans up its own demo data. On a LIVE server the credit-spending
  sections report SKIP instead of running.
- `smoke_test.py` — the original 27-check staged-agent API suite.

Status (2026-09-20): `cli.py verify` **71/71 PASS** (demo server; 50/50 of
the non-credit checks against a live server), `smoke_test.py`
**ALL PASS**, all pages browser-verified (carousel rotation/wrap/arrows,
waitlist, chat turns, theme edit propagating across pages **including the
wikis — accent, fonts, and forced light/dark all follow /theme**, staged
check to `done`, learn/apps menus, wikis opening in the app frame). /video
Range-verified live: `206 Partial Content` + exact `content-range` on both
clips, seek past the 1.1 MB mark confirmed.
