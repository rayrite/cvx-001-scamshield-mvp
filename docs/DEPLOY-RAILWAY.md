# Deploying ScamShield (zai-demo-app) to Railway — greenfield guide

> **Audience.** You have never used Railway before. This guide takes you from a
> fresh Railway account to a public, HTTPS-backed ScamShield demo, in the
> correct order, with a troubleshooting chapter organized by blast radius.
>
> **Verified.** Every Railway-specific claim below was checked against the
> official docs (docs.railway.com, railpack.com, railway.com/pricing) on
> **2026-09-20**. Anything not independently verified is marked ⚠️. A source
> list with dates is at the end.

---

## 0. What you are deploying

ScamShield is **one web service** (a FastAPI app) plus **one persistent volume**
(for job/report/chat/waitlist files). There is no database, no worker, no
second service — if the web service is healthy, everything works.

```
GitHub repo (zai-demo-app-2026-09/)
        │  push (or Railway CLI up)
        ▼
┌────────────────────────── Railway project ─────────────────────────┐
│  service "scamshield"                                               │
│   • builds with Railpack: pip install from app/requirements.txt     │
│   • starts:  uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}   │
│     (already in app/Procfile — Railway reads it)                    │
│   • env:     ZAI_API_KEY + optional knobs                           │
│   • volume:  mounted at /data  ← DATA_DIR=/data                     │
│   • domain:  <something>.railway.app (auto SSL)                     │
└─────────────────────────────────────────────────────────────────────┘
        │  outbound HTTPS
        ▼
   z.ai API (glm-5.3-flash vision + glm-5.3 research w/ web_search)
```

**Time budget:** ≈ 45–60 minutes the first time (most of it is account/repo
setup). The deploy itself builds in a few minutes. Per task:

| Task (do them in this order) | Hands-on | Notes |
|---|---|---|
| Part 0 — code on GitHub | 10–15 min | the bulk of the total if your GitHub account is brand-new |
| Part 1 — Railway account | ~5 min | plus trial verification in the background — no duration published; near-instant with an established GitHub account (see Part 1, step 4) |
| Part 2 — create the service | ~5 min | 2–5 min of that is watching the first build go green |
| Part 3 — environment variables | 2–3 min | fastest via the Raw Editor bulk paste |
| Part 4 — the volume | 1–2 min | |
| Part 5 — public domain | ~1 min | |
| Part 4B — folder-hierarchy audit | ~1 min | two curl calls; the folders themselves need zero setup |
| Part 6 — verify the deployment | 2 min | the checklist in Part 6 |

Reading the table: **≈ 25–30 minutes is you actively working.** The rest of
the 45–60-minute total is *waiting, not working* — Railway building the app
after each deploy (2–5 min per build, you just watch the log), the automated
trial verification finishing in the background on a new account, and simple
first-time-through slowness (finding buttons, re-reading steps).

**You deploy one way, not both.** Parts 0–6 are the GitHub path
(recommended — pushes auto-redeploy). Part 8 is a complete *alternative*
route using the Railway CLI with no GitHub at all (≈ 10–15 min end-to-end).
Pick one and follow only that path.

**What it costs.** A brand-new Railway account starts on the **Free Trial**:
$5 one-time usage credit, valid 30 days, **no credit card required**
(railway.com/pricing, 2026-09-20). There is no fixed instance size — you pay
per minute of actual RAM/CPU use (RAM ≈ $10/GB-mo, CPU ≈ $20/vCPU-mo), and
the docs benchmark a "typical Node or Python web service" at **100–400 MB
idle RAM** (their worked example: 0.36 GB + 0.05 vCPU ≈ $5.60/month). This
app is in that class; with demo-level traffic the trial credit lasts weeks.
To keep it running long-term, move to the **Hobby** plan ($5/month, which
includes $5 of usage per month — "If your total usage at the end of your
billing period is $5 or less, you will not be charged extra for usage").
When the trial ends — 30 days or $5 spent, whichever comes first — the
account reverts to the **Free** plan ($1/month non-rolling credit, tighter
limits: 0.5 GB RAM per service, 3-day log retention). ⚠️ And critically:
**"Railway deletes stateful volumes created by Trial accounts 30 days
after the expiration of your credits"** — back up your job data (Part 4)
before the trial lapses, or upgrade to Hobby first.

> **Key facts this guide is built on (all doc-verified 2026-09-20):**
> - Railway injects a `PORT` environment variable at runtime; web servers
>   must bind `0.0.0.0` and listen on `$PORT`. Our Procfile already does
>   exactly this (`uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}` —
>   byte-for-byte the command Railpack itself generates for FastAPI+uvicorn
>   apps; the app object here is `main:app`, which is what it expects).
> - Railway builds with **Railpack** (it replaced Nixpacks, now in
>   maintenance mode). With `requirements.txt` present, dependencies install
>   with pip and the Procfile start command is honored.
> - Files outside a volume are **ephemeral**: "Files outside a volume are part
>   of the service's ephemeral filesystem and don't persist across
>   deployments." So the volume in Part 4 is not optional if you want job
>   history and the waitlist to survive redeploys.
> - Railway's edge closes a request after **5 minutes with no data
>   transferred** (15 minutes max if data keeps flowing). Staged-check gate
>   actions block server-side for up to `ZAI_RESEARCH_TIMEOUT` (300 s
>   default) with an empty response in flight — right at the edge limit. On
>   Railway, set `ZAI_RESEARCH_TIMEOUT=240` to stay safely inside it.
> - Generated domains look like `<name>.up.railway.app` with automatic SSL.

---

## 1. Prerequisites (do these first, in this order)

| # | What | Where / how | Check |
|---|------|-------------|-------|
| 1 | The app folder | `zai-demo-app-2026-09/` on your machine | `app/main.py`, `app/requirements.txt`, `app/Procfile` exist |
| 2 | A GitHub account | github.com (free) | you can log in |
| 3 | Your z.ai API key | from your z.ai console | 49-char key; keep it private |
| 4 | git installed | `git --version` works in a terminal | any recent version |
| 5 | (optional) Railway CLI | `npm i -g @railway/cli` or installer | `railway --version` — Part 8 is the CLI alternative |

---

## 2. Part 0 — Put the code on GitHub (Railway deploys from a repo) · ≈10–15 min

Railway's main deploy flow pulls from GitHub, so the repo comes first.

### 2.1 Check what will be committed (protect your API key)

The app already ships `app/.gitignore` covering the dangerous/local files:

```text
.env          ← your LIVE z.ai key — must never be pushed
.venv/
data/         ← local job/chat/waitlist files
demo-server.log
__pycache__/
```

Verify before the first commit (run from `zai-demo-app-2026-09/`):

```bash
git init
git add -A
git status --short          # nothing here should list app/.env
git check-ignore -v app/.env   # should print the .gitignore rule
```

If `app/.env` shows up in `git status`, **stop** — fix `.gitignore` before
committing. (It is already correct as shipped; this check is your seatbelt.)

### 2.2 Commit and push

```bash
git commit -m "ScamShield demo app — initial commit"
```

Then create an empty repo on github.com (say `scamshield-demo`) and push.
Easiest with the GitHub CLI if you have it authenticated:

```bash
gh repo create scamshield-demo --private --source . --push
```

or the classic way (GitHub → New repository → create empty → copy the URL):

```bash
git branch -M main
git remote add origin https://github.com/<you>/scamshield-demo.git
git push -u origin main
```

> **Private vs public:** private is fine — Railway gets access via its GitHub
> App integration, not by cloning a public URL.

---

## 3. Part 1 — Create the Railway account (greenfield) · ≈5 min

1. Go to **railway.com** → **Sign Up** / **Get Started** (the login page
   offers "Continue with GitHub" or email).
2. Sign up **with GitHub** — this pre-authorizes the Railway GitHub App, so
   Part 2 won't need extra OAuth gymnastics.
3. No credit card is required for the Free Trial; you get a **$5 one-time
   credit that expires after 30 days**.
4. **Let trial verification finish** (automated, GitHub-based): unverified
   accounts get a "Limited" trial — deploys still work, but with
   **restricted outbound network**, which would break this app's z.ai
   calls. Railway publishes **no duration** for the check; what it keys on
   is **"the age and activity of your GitHub account"** (the exact
   thresholds are deliberately unpublished — it's an anti-abuse check) —
   an established,
   active account typically clears during signup (effectively instant),
   while a brand-new or dormant GitHub account may stay Limited. Sign up
   with your existing GitHub account, not a fresh one. If z.ai requests
   fail on a brand-new account, go to **railway.com/verify** and retry
   (any time, no wait between attempts; fully automated — Railway takes no
   manual appeals). The escape hatch if it never clears: upgrade to Hobby.
5. You land on the **dashboard**. Create your workspace by clicking **New
   Project** — the docs quickstart shows exactly this path (dashboard → New
   Project → GitHub repo option).
6. One account per person (enforced through email, GitHub, and payment
   verification) — don't try to refresh the trial with a second account.

---

## 4. Part 2 — Create the service from your GitHub repo · ≈5 min incl. the first build

1. In the dashboard, click **New Project** and choose the **GitHub repo**
   option. (Adding to an existing project later: **New** button on the
   canvas or the command palette, then **Connect Repo**.)
2. First time: Railway prompts to link GitHub and install its **GitHub
   App** — grant it access to the `scamshield-demo` repo. Autodeploys need
   at least one project member with contributor access to the repo.
3. Search for and click the repo. Railway shows **Deploy Now** (build
   immediately) or **Add variables** first — either is fine; the next parts
   cover the variables you'll want.
4. **Set the Root Directory to `app`** — the single most important setting
   for this repo, because the Python code (and `requirements.txt`) live in
   the `app/` subfolder, not the repo root.
   - Select the service → **Settings** tab → **Root Directory** → `app`
   - Doc behavior: "Railway will only pull down files from that directory
     when creating new deployments" — install, start command, and Procfile
     lookup all run inside it.
5. Watch the first build: click the deployment → **Build Logs** tab.
   - Railpack detects Python via `requirements.txt`, installs with pip,
     and starts with the Procfile command (`web: uvicorn main:app …`).
   - Python version: Railpack defaults to 3.13 (any 3.10+ works with this
     codebase). To pin one, set `RAILPACK_PYTHON_VERSION` (e.g. `3.12`).
   - Reading build failures: "the actual error is rarely at the bottom!"
     — scan upward for the first Python/pip error.
6. The first deployment can go green on its own — the app starts fine with
   no env vars (it runs in demo mode) — but don't hand out the URL yet: do
   Part 3 next so you never confuse demo replies with live ones.

---

## 5. Part 3 — Environment variables · ≈2–3 min

Where: service → **Variables** tab → **New Variable** (name + value form,
with autocomplete). Faster: open the **Raw Editor** and paste the contents
of a `.env`-style file — plain `KEY=value` lines, imported in bulk. The
repo's `app/.env.example` is a ready-made template: copy it, fill in
`ZAI_API_KEY`, set `DATA_DIR=/data` and `ZAI_RESEARCH_TIMEOUT=240`, paste.

| Variable | Required? | Value / default | What it does |
|---|---|---|---|
| `ZAI_API_KEY` | **yes (for live mode)** | your 49-char z.ai key | Unset ⇒ app runs in **demo mode** (canned, honestly-labeled replies). Set ⇒ live z.ai calls. |
| `DATA_DIR` | **yes (with volume)** | `/data` | Points the app's file store (jobs, reports, chats, waitlist) at the volume from Part 4. |
| `ZAI_API_URL` | no | `https://api.z.ai/api/paas/v4/chat/completions` | Only change if z.ai moves the endpoint. |
| `ZAI_INTAKE_MODEL` | no | `glm-5.3-flash` | Vision transcriptionist (screenshots ≤5 MB). |
| `ZAI_RESEARCH_MODEL` | no | `glm-5.3` | Staged reasoning + web_search model. |
| `ZAI_REASONING_EFFORT` | no | `low` | Only depth/cost lever for GLM-5.x (`low\|high\|max`, API default `max`). |
| `ZAI_INTAKE_TIMEOUT` | no | `120` (s) | Vision call timeout. |
| `ZAI_RESEARCH_TIMEOUT` | no | `300` (s) — **set `240` on Railway** | Research-call timeout — also why staged checks legitimately take minutes. Railway's edge cuts requests with 5 min of no data; 240 keeps gate responses inside it. |
| `MAX_STAGE_CALLS` | no | `10` | Model-call cap per staged job before forced consolidation. |
| `MAX_IMAGES` | no | `5` | Max screenshots per request. |
| `MAX_CHAT_TURNS` | no | `12` | Turns per chat/quick conversation. |
| `AGENT_TOKEN` | no | unset | If set, all `/api/*` routes require `X-Auth-Token: <value>` — a cheap shared-secret gate for a public demo. |

Minimum viable live setup = exactly two variables: `ZAI_API_KEY` and
`DATA_DIR=/data`.

Notes:

- Variable changes are **staged**: "Adding, updating, or removing variables,
  results in a set of staged changes that you must review and deploy" —
  applying them creates the new deployment.
- Railway also injects its own variables at runtime (`PORT`,
  `RAILWAY_PUBLIC_DOMAIN`, `RAILWAY_SERVICE_NAME`, …) — don't define `PORT`
  yourself; Railway assigns it dynamically.
- z.ai billing is pay-per-use on your z.ai account and is **separate** from
  Railway billing. The app burns z.ai credits only when someone actually
  runs a check/chat (~$0.02–0.10 per staged check at 2026-09-20 z.ai
  prices).
- Optional hardening: a variable's ⋮ menu → **Seal** makes `ZAI_API_KEY`
  write-only — "never visible in the UI nor can it be retrieved via the
  API". Sealing is permanent and sealed values are **not** copied into
  duplicated environments/services, so store the key somewhere safe first.
- The app's optional local `.env` loading is a no-op on Railway — it reads
  plain environment variables at runtime, exactly what Railway supplies.

---

## 6. Part 4 — The volume (persistence) · ≈1–2 min

Without a volume, every redeploy wipes `data/` (job history, reports,
conversations, waitlist). One volume, 0.5 GB on the trial, is plenty for a
demo.

1. Create a volume and attach it to the `scamshield` service, with **mount
   path `/data`**.
   - 2026 UI: open the command palette (**Ctrl/Cmd+K**) → "Volume" (or
     right-click the service on the project canvas) → choose the service →
     set the mount path.
2. Make sure `DATA_DIR=/data` is set (Part 3) — the app creates its
   `jobs/`, `reports/`, `chats/`, `videos/` subfolders automatically on
   boot (full map in Part 4B; `waitlist.txt` appears on first signup).
3. Redeploy if prompted. Volume mounts happen at container start, not
   mid-run.

Doc-verified behavior (2026-09-20):

- "Files outside a volume are part of the service's ephemeral filesystem and
  don't persist across deployments."
- Trial: up to 3 volumes/project, 0.5 GB each (Hobby: 10 × 5 GB). Billed
  ≈ $0.15/GB-month against usage credit.
- A service can have **one volume**; **replicas cannot be used with
  volumes** — keep the service at 1 replica (the default).
- Redeploys of a volume-attached service briefly stop the service (the old
  deployment must release the volume) — expect seconds-to-a-minute of
  downtime per redeploy, even with healthchecks.
- Volume-attached services support **manual and scheduled backups**
  (service → Backups tab).
- ⚠️ Trial accounts: "Railway deletes stateful volumes created by Trial
  accounts 30 days after the expiration of your credits" — export or back
  up job data before the trial ends, or upgrade to Hobby first. Trial caps:
  1 GB RAM, 5 services.

---

## 6b. Part 4B — The folder hierarchy on the Railway server (the map) · ≈1 min audit

> Every path in this section was verified against the app's own code
> (`main.py`, `jobs.py`, `chatstore.py`, `features.py`, `agents.py`) on
> 2026-09-20 — nothing below is aspirational.

**The short version: you never create folders on the Railway server by
hand.** The hierarchy assembles itself from exactly two inputs:

1. **The deploy** copies the repo's `app/` folder to the service root
   (that is what **Root Directory = `app`** from Part 2 does). Code,
   `static/`, and `content/` arrive with it. This side is **ephemeral** —
   rebuilt from the repo on every deploy.
2. **The app itself** creates its data subfolders inside the volume at
   boot — `jobs/`, `reports/`, `chats/`, `videos/` each have an explicit
   `mkdir` that runs at import time. The volume is the only **persistent**
   part.

So the complete list of folder-related decisions in this deployment is:
**Root Directory = `app`** (Part 2, step 4) · **volume at `/data` +
`DATA_DIR=/data`** (Parts 3–4) · and only if you want the sample videos,
the CLI upload described in `VIDEO-HOSTING-RAILWAY.md`. There is no step
where you hand-build a directory tree on the server — if you find yourself
wanting one, something above went wrong.

### Tree 1 — service root: the repo's `app/` folder as deployed (ephemeral)

```text
<service root>          ← the app/ subfolder of the repo (Root Directory)
│
├── main.py             FastAPI app — "uvicorn main:app"
├── Procfile            start command Railway reads (0.0.0.0:$PORT)
├── requirements.txt    pip install list (build input)
├── agents.py           content registry: chat skills + quick prompts
├── chatstore.py        conversations → $DATA_DIR/chats/
├── cli.py              local verify tooling (not used at runtime)
├── features.py         feature flags + content-presence checks
├── jobs.py             jobs + reports under $DATA_DIR
├── orchestrator.py     staged-agent state machine
├── skillkit.py         skill-file parsing
├── udl.py              design tokens → /udl.css + /udl.js
├── zai.py              z.ai API client
├── features.json       feature flags (defaults all-on if absent)
├── udl.json            design tokens (house defaults if absent)
├── .env.example        template for Part 3 — ships; the real .env does NOT
├── .gitignore          what kept .env / data/ out of this tree
│
├── static/             the entire UI — mounted at / (LAST, so /api wins)
│   ├── index.html      /        landing (hero, carousel, waitlist)
│   ├── check.html      /check   staged agent
│   ├── chat.html       /chat    skills as multi-turn chat
│   ├── quick.html      /quick   single-pass prompts
│   ├── learn.html      /learn   Learning Center menu
│   ├── apps.html       /apps    dynamic SPA menu
│   ├── theme.html      /theme   UDL theme editor
│   ├── video.html      /video   sample video players
│   ├── app.css         page styling
│   └── app.js          site header/footer frame + wiki integration
│
└── content/            agent + learning content (presence = feature ON)
    ├── prompts/        /quick modes — 4 files
    │   ├── system-prompt-scamshield-check.md
    │   ├── system-prompt-recall-check.md
    │   ├── system-prompt-product-dig.md
    │   └── system-prompt-corpcheck.md
    ├── skills/         /chat modes — 4 skill folders
    │   ├── rdw-product-dig/                 SKILL.md · DESIGN.md · references/
    │   ├── rdw-scamshield-check-v2/         SKILL.md + 5 reference files
    │   ├── rdw-scamshield-recall-check-v2/  SKILL.md · DESIGN.md · references/
    │   └── rdw-scamshield-tea2-corpcheck/   SKILL.md · DESIGN.md · references/
    ├── spas/           /apps menu items — 1 file
    │   └── scamshield-full-spectrum.html
    └── wikis/          /learn menu items — 2 files
        ├── dark-patterns-wiki.html
        └── seller-scam-wiki.html
```

### Tree 2 — the volume at `/data`: everything the app writes (persistent)

```text
/data                   ← DATA_DIR=/data (Part 3) · volume mount path (Part 4)
│
├── jobs/               ← created automatically at boot (jobs.py)
│   └── <job-id>.json   one staged-check job each
├── reports/            ← created automatically at boot (jobs.py)
│   └── <job-id>.md     cumulative markdown report per job
├── chats/              ← created automatically at boot (chatstore.py)
│   └── c_*.json        chat + quick conversations
├── videos/             ← created automatically at boot (main.py mount guard)
│   ├── demo1.mp4       the ONLY manual upload: railway volume files
│   └── demo2.mp4       upload <local> /videos/<name>.mp4  (CLI-only)
└── waitlist.txt        ← created on the first signup (not at boot)
```

**Deliberately absent from the server:** `.env` (the key lives in Railway
Variables, Part 3 — never in a file on the deploy side), your local
`data/` contents (a fresh volume legitimately starts empty), `.venv/`,
`demo-server.log`, `__pycache__/`, and everything outside `app/`
(`README.md`, `docs/` — the Root Directory setting excludes them, so they
never deploy at all).

The CLI path (Part 8, `railway up ./app`) produces the **same tree**: the
uploaded folder becomes the service root directly, so Root Directory
juggling is a GitHub-path concern only.

### Why a broken link cannot appear silently

The app fails loud on the paths that matter, in tiers:

| If this is missing… | What happens | Where you'll see it |
|---|---|---|
| a whole `static/`, `content/wikis/`, or `content/spas/` folder | Deployment **crashes at startup** — the mounts verify the folder exists at import time (the `videos/` mount has a `mkdir` guard for exactly this) | deployment shows Crashed; runtime log (T-L2-1) |
| *every* skill (`SKILL.md` + declared references) or *every* `prompts/*.md` | No crash — that surface answers **503 "disabled or its content is missing"** | `/api/features` shows the flag set-but-not-effective |
| one skill folder or one prompt file | That one mode drops off the chat/quick menu (availability is checked per mode); the surface stays up as long as ≥1 mode remains | `/api/modes` shows `"available": false` for it |
| one wiki/SPA `.html` file | It drops off the `/learn` or `/apps` menu (menus scan the folder at request time) | shorter menu list |
| `features.json` / `udl.json` | No crash — defaults apply (all flags on / house theme) | `/theme` shows default tokens |
| `/videos/*.mp4` on the volume | `/video` page still loads; each player probes its file and reports `missing` instead of `streaming` | the player tile's status line |

### The 30-second structural audit (after Part 6's checks)

Two endpoints double as a folder-hierarchy audit:

```bash
curl https://<your-app>.up.railway.app/api/health
#   expect "data_dir": "/data"              → volume wiring correct

curl https://<your-app>.up.railway.app/api/features
#   expect every "effective" flag true, and
#   "inventory": {"skills": 4, "quick_prompts": 4, "wikis": 2, "spas": 1}
```

That single `/api/features` call proves the deploy carried the full
`content/` tree. Lower counts mean files were left out of the commit — fix
locally and push; the next deploy rebuilds the ephemeral side while the
volume is untouched.

### Before the first push: the hierarchy starts in git

What deploys is exactly what git tracks, so audit it once at Part 0 time
(right after `git add -A`):

```bash
git ls-files app | sort
```

Expected: the 16 root files from Tree 1 (12 `.py`/config files incl.
`Procfile` + `requirements.txt`, plus `features.json`, `udl.json`,
`.env.example`, `.gitignore`), the 10 `static/` files, and the full
`content/` tree (4 prompts, 4 skill folders with their `references/`,
1 SPA, 2 wikis) — and **no** `.env`, no `data/`, no `.venv/`, no logs.

---

## 7. Part 5 — Public domain + HTTPS · ≈1 min

1. Service → **Settings** → **Networking → Public Networking** →
   **Generate Domain**. (The button is hidden if a TCP proxy is assigned —
   delete the proxy first.)
2. You get `<name>.up.railway.app` with **automatic SSL** (free Let's
   Encrypt certs, auto-renewed).
3. No port configuration is needed: generated domains auto-detect
   single-port apps, and our app listens on the injected `PORT`.
4. **Recommended:** set a healthcheck path so traffic only cuts over once
   the app really answers — service settings → health endpoint →
   `/api/health` (returns 2xx). Default healthcheck timeout is 300 s.
5. (Optional) Custom domain: add it in the same panel; Railway shows the
   **CNAME + TXT** records to create at your DNS — both are required ("If
   the `TXT` record is missing, requests to your custom domain will return
   a `404` error"). Limits: 1 custom domain on Trial, 2 on Hobby.

---

## 8. Part 6 — Verify the deployment (2 minutes)

Open `https://<your-app>.up.railway.app` and confirm, in order:

| Step | Expect | Verifies |
|---|---|---|
| 1 | Landing page renders with header/hero/theme | service is up, static files served |
| 2 | `/api/health` returns `{"ok": true, ...}` | API layer healthy |
| 3 | `"demo_mode": false` in that JSON | `ZAI_API_KEY` was accepted |
| 4 | Header beacon turns green **GO** (auto-runs on load; click the pill to re-run — key · internet · one tiny ping) | live z.ai connectivity end-to-end, one glance |
| 5 | `/check` → submit any text → snap verdict arrives | live glm-5.3 works |
| 6 | After the check, the job still appears after a browser refresh | volume + `DATA_DIR` wired (job JSON on `/data`) |
| 7 | `/learn`, `/apps`, `/theme`, `/quick`, `/chat` all load | mounts intact |
| 8 | `/api/features` → all flags effective, inventory `skills 4 · quick_prompts 4 · wikis 2 · spas 1` | full `content/` hierarchy deployed (Part 4B) |

If the beacon is red **OFF**, open the pill's panel — each failed check names
its cause (missing key · outbound blocked · HTTP 401/429 from z.ai). Red OFF
with "out of credit" means the z.ai account needs a recharge; "outbound
blocked" on Railway means the trial plan hasn't been verified yet.

If step 3 says `"demo_mode": true`, the key variable isn't set on the
**deployment** you're hitting — see troubleshooting T-L4-2.

---

## 9. Part 7 — Everyday operations

- **Logs:** click a deployment → its panel shows runtime logs, with build
  output under the **Build Logs** tab; the environment-wide **Log
  Explorer** lives under the **Observability** tab (date filtering). CLI:
  `railway logs` (`--build` for build logs, `-n 100` for the last lines).
  Retention on Trial/Hobby: 7 days (Pro: 30). Anything the app prints to
  stdout/stderr is captured; rate limit 500 lines/sec per replica.
- **Deploys on push:** pushes to the connected branch rebuild
  automatically (on by default). Pushes from committers without a linked
  Railway account wait as a **Deployment Approval** you must Approve/Reject
  in the UI. Manual rebuild: command palette → **Deploy Latest Commit**.
  Limit triggers with watch paths (e.g. `app/**`) so README-only pushes
  don't rebuild.
- **Crash behavior:** restart policy defaults to **On Failure, max 10
  restarts**; a crashing deployment shows state **Crashed**. Railway does
  not health-poll after a deployment goes live — the healthcheck only
  gates the initial cutover.
- **Restart:** safe — data on the volume survives.
- **Rollback:** deployments list → an older healthy deployment → restore.
- **Stop spending:** stop or remove the service (service settings) —
  usage-based billing only burns while something runs. For a harder cap,
  set an account **usage limit**: at the limit all workloads go offline
  (warning emails at 75/90/100 %) and they auto-redeploy once the limit is
  raised.
- **Update the key:** Variables → edit `ZAI_API_KEY` → review & deploy the
  staged change.

---

## 10. Part 8 — Alternative: deploy with the Railway CLI (no GitHub) · ≈10–15 min

On Windows, install with npm (`npm i -g @railway/cli`) or
`scoop install railway` — the curl installer is macOS/Linux only.

```bash
railway login                          # opens the browser (or --browserless)
railway init                           # "Create a new project" (name: scamshield)
railway up ./app                       # upload just the app folder and stream the build
railway variable set ZAI_API_KEY --stdin   # paste key + Enter — stays out of shell history
railway variable set DATA_DIR=/data ZAI_RESEARCH_TIMEOUT=240   # batch pairs in one call
railway domain                         # generate the Railway domain
railway volume add                     # add the volume (choose service + mount path /data)
railway logs                           # stream runtime logs (--build for build logs)
```

CLI vs dashboard semantics: unlike the dashboard's staged review flow,
**`railway variable set` triggers a redeploy by default** — batch several
`KEY=value` pairs into one call (as above) or pass `--skip-deploys` and
deploy once at the end. `railway run <command>` executes a local command
with the service's variables injected (sealed values excluded) — handy for
testing the exact production environment.

Uploading `./app` directly means the service root already contains
`requirements.txt` and `main.py`, so no Root Directory juggling. Two
cautions: `railway up` respects `.gitignore` (good — `.env` stays home),
and **`railway deploy` is a different command** (pre-built templates like
Postgres) — for your own code it's `railway up`. GitHub remains the
recommended path (automatic redeploys + history); CLI is fine for
experiments, and CI pipelines can use `RAILWAY_TOKEN=xxx railway up`.

> Do **not** add a `railway.toml` — Config-as-Code is deprecated with a
> hard cutoff of 2026-12-01, and new services can't opt into it (Railway's
> newer code-driven path is `.railway/railway.ts` infrastructure-as-code —
> unnecessary here). Plain service settings (this guide's path) are the
> current way.

---

## 11. Troubleshooting — organized by blast radius

Start at the level that matches the symptom; each entry lists what you'll
see, the likely cause, and the fix. Levels are ordered from "nothing works
for anyone" to "one user's browser".

### Level 0 — Account / billing (nothing in the project will start)

**T-L0-1 · Everything offline: usage limit reached / trial exhausted**
- Verified behavior: when a hard usage limit or the trial credit is hit,
  "all your workloads will be taken offline" (warning emails arrive at
  75 / 90 / 100 %). Raising or removing the limit — or upgrading to Hobby
  after trial depletion — **automatically redeploys** the stopped services.
- Trial expiry (30 days or $5 spent) reverts the account to the Free plan
  ($1/month non-rolling credit) — and **trial-created volumes are deleted
  30 days after the credits expire** (back up first; see Part 4).
- On Hobby, a failed or expired card stops services until open invoices
  are paid (payment is retried over several days first; volumes are
  retained 60 days after a cancellation).
- Fix: upgrade to Hobby ($5/mo, includes $5 usage) or set a hard usage
  limit as a guardrail; check the account usage view for the burn
  breakdown (RAM ≈ $10/GB-mo, CPU ≈ $20/vCPU-mo).

### Level 1 — Build failures (deployment fails before the app ever runs)

**T-L1-1 · Build fails: "No start command could be found" / language not detected**
- Cause: Root Directory is not `app` — Railpack finds no `requirements.txt`
  or `main.py` where it looks, detects no language, and generates no start
  command (this is the official error string for that situation).
- Fix: Service → **Settings** tab → **Root Directory** → `app`, redeploy.
  (Alternative: set a Start Command in Service Settings — the docs' Python
  example is exactly ours: `uvicorn main:app --host 0.0.0.0 --port $PORT`.)

**T-L1-2 · pip install fails (package not found / resolver error)**
- Cause: `requirements.txt` edited with a typo, or a pinned version
  unavailable under the default Python (3.13).
- Fix: fix the file locally, push; or pin `RAILPACK_PYTHON_VERSION`.

**T-L1-3 · Build succeeds, deployment marked failed, "Application Failed
to Respond" (502)**
- Cause: the app is listening on the wrong host/port — Railway's edge
  proxy reports it "cannot communicate with your application". The app
  must bind `0.0.0.0` and the port from Railway-injected `$PORT` (docs'
  own Python fix: `uvicorn main:app --host 0.0.0.0 --port $PORT`).
- Fix: keep the shipped Procfile
  (`web: uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}`) or set
  the start command in service settings; if you use a *custom* domain,
  also check its target port matches what the app listens on.
- If a healthcheck is configured, it must return **2xx over HTTP** within
  300 s (default; `RAILWAY_HEALTHCHECK_TIMEOUT_SEC` to change) — `/` and
  `/api/health` both do.

**T-L1-4 · Pushes to GitHub never trigger a deploy**
- Official check order: (1) a project member has contributor access to the
  repo; (2) the Railway GitHub App includes the repo in its installation
  (GitHub → Settings → Applications → Railway — accept any pending
  permission update); (3) refresh Railway's repo cache from the project
  canvas; (4) disconnect/reconnect the GitHub integration as a last
  resort. Pushes from authors not linked to a Railway account arrive as a
  **Deployment Approval** waiting in the UI instead of deploying.
- Also verified to silently skip deploys: **watch paths** that exclude the
  pushed files (enable "Show Skipped" in deployment history to confirm),
  **empty commits** (use **Deploy Latest Commit**, Ctrl/Cmd+K), a
  **failed** GitHub Actions workflow when wait-for-CI is enabled, and the
  skipped-builds optimization (same source as the last build — force it
  with Redeploy or `railway up`).

**T-L1-5 · "your build took too long to complete and was timed out"**
- Free/Trial plans have a **5-minute build timeout** — Railway staff
  confirmed on the community forum (2025-08-13) that raising it requires a
  paid plan (the paid-plan ceiling itself is not published ⚠️). Normal
  builds for this app finish in a few minutes, so a timeout usually means
  a stuck pip download or a poisoned cache layer.
- Fix: retrigger; set `NO_CACHE=1` once to bypass the cache; check pip
  isn't fetching a huge pinned package. Free-tier deploys can also queue
  during regional high-traffic windows (8 AM–8 PM local).

### Level 2 — Runtime (deploys fine, app misbehaves)

**T-L2-1 · Container restarts repeatedly (deployment shows Crashed)**
- Restart policy defaults to **On Failure, max 10 restarts** — after that
  the deployment stays down until the next deploy.
- Read the **deployment logs** (not build logs) bottom-up to the first
  Python traceback. Common verified signatures:
  - `ModuleNotFoundError: No module named 'X'` — the build never saw
    `requirements.txt` (Root Directory wrong — see T-L1-1).
  - **Exit code 137** — the app was killed for running out of memory
    (SIGKILL/OOM); check the Metrics tab and simplify or accept higher
    usage.
  - A `SyntaxError` or traceback at import time — a bad edit shipped;
    fix and push.
  - Corrupted `data/` files after an unclean stop — delete the offending
    file via the CLI (`railway volume files delete /jobs/<id>.json`; or
    `railway volume browse` for an interactive file browser — volume file
    management is CLI-only, there is no dashboard file browser).

**T-L2-2 · 502/504 on staged-check gate clicks**
- Verified cause: Railway's edge closes requests after **5 minutes with
  no data transferred**. Gate actions block server-side for up to
  `ZAI_RESEARCH_TIMEOUT` (default 300 s) before responding — right at the
  limit, so long verify stages get cut.
- Fix: set `ZAI_RESEARCH_TIMEOUT=240` on Railway (recommended in Part 3).
  The quick surface (`/quick`, single pass) never hits this.

**T-L2-3 · Deploys succeed but never receive traffic / marked unhealthy**
- Log signature: "Attempt #1 failed with service unavailable. Continuing
  to retry for 4m59s" ending in "1/1 replicas never became healthy!
  Healthcheck failed".
- Causes (official): the healthcheck path returns non-2xx without auth;
  the app isn't listening on the injected `PORT` (or you defined `PORT`
  yourself); or the probe from `healthcheck.railway.app` is rejected by
  host filtering.
- Fixes: use `/api/health` (2xx, no auth), bind `0.0.0.0:$PORT` (our
  Procfile does), don't define `PORT` yourself, allow the probe origin.
  Slow boots: raise `RAILWAY_HEALTHCHECK_TIMEOUT_SEC` above the 300 s
  default.

**T-L2-4 · HTTP 544 on the public domain**
- 544 is Railway's **platform-side** proxy error, not your app — contact
  support and include the `X-Railway-Request-Id` response header.

### Level 3 — Data / volume (app runs, data vanishes or errors)

**T-L3-1 · Jobs/waitlist disappear after each redeploy**
- Cause: no volume, or volume not mounted where the app writes.
- Fix: attach volume at `/data` **and** set `DATA_DIR=/data`; verify with
  step 5 of the Part 6 checklist.

**T-L3-2 · "Permission denied" writing under /data**
- Cause: non-root runtime user vs volume mounted as root.
- Fix: set `RAILWAY_RUN_UID=0` on the service (doc-documented workaround).

**T-L3-3 · Redeploys are slow / brief downtime**
- Expected: only one deployment can mount the volume at a time; seconds
  to a minute.

**T-L3-4 · Need files off the volume**
- `railway volume files download /reports/<id>.md ./copy.md`, or the
  interactive `railway volume browse` (note: volume file management is
  CLI-only — there is no dashboard file browser); or service → Backups.

### Level 4 — External API (z.ai) (app up, model calls fail)

**T-L4-1 · Replies say demo/canned things**
- `demo_mode: true` in `/api/health` ⇒ `ZAI_API_KEY` unset on this
  deployment (typo in the name, set on the wrong environment, or the
  service hasn't redeployed since you added it).

**T-L4-2 · 502 from the app with "z.ai HTTP 401/403" in logs**
- Key invalid/revoked, or copied with whitespace. Re-paste exactly.

**T-L4-3 · "z.ai HTTP 429" / intermittent failures**
- z.ai rate limiting — the app surfaces it as a 502 with the upstream
  status; retry after a pause; check your z.ai console quotas.

**T-L4-4 · Image upload rejected (~5 MB)**
- The app enforces ≤5 MB per image (base64-adjusted) because that is
  z.ai's vision limit — shrink the screenshot first.

**T-L4-5 · Every z.ai call fails on a brand-new account**
- Fresh trials run "Limited" until the automated GitHub-based verification
  completes — the restriction is on **outbound network**, so the app can
  deploy and serve pages while all api.z.ai requests fail.
- Fix: visit **railway.com/verify**, complete verification, retry the
  check (verification is automated — no manual appeals).

### Level 5 — Client / browser (one visitor's problem)

**T-L5-1 · "This site can't be reached"**
- Domain not generated (Part 5), or the visitor is hitting an old URL
  after a rename — regenerate/re-check the domain. Custom domain showing
  **404**: the DNS TXT verification record is missing (CNAME alone is not
  enough).

**T-L5-2 · Page loads but styles/CDN fonts look wrong**
- The app is self-hosted (no CDN dependencies); a hard refresh clears
  stale cache.

**T-L5-3 · Staged check "stuck" at a gate**
- Gates intentionally wait for a human decision; and each gate click can
  take up to ~5 min of model time. Check the service logs to see the
  stage progressing.

---

## 12. Sources (all fetched 2026-09-20)

- docs.railway.com — volumes reference (sizes/limits, one-volume rule,
  replicas exclusion, backups, IOPS)
- docs.railway.com — services page (ephemeral-filesystem wording, storage
  caps)
- docs.railway.com — guides/volumes (mount timing, /app guidance,
  `RAILWAY_RUN_UID`)
- docs.railway.com — public-networking reference (Generate Domain flow,
  auto SSL, CNAME+TXT for custom domains)
- docs.railway.com — variables reference (injected `RAILWAY_*` list,
  `RAILWAY_PUBLIC_DOMAIN` form `example.up.railway.app`) and PORT-binding
  guidance via the "Application Failed to Respond" error doc
- docs.railway.com — build-configuration guide + builds reference (Railpack
  default, Root Directory, watch paths, Procfile note, Nixpacks
  maintenance mode, Dockerfile precedence)
- docs.railway.com — deployments reference + restart-policy guide (states,
  On-Failure/10 default, overlap & draining, zero-downtime behavior)
- docs.railway.com — healthchecks reference (HTTP 2xx, 300 s default,
  `healthcheck.railway.app` origin, PORT used for checks)
- docs.railway.com — networking: public-networking guide, working-with-
  domains (`*.up.railway.app`, target ports, CNAME+TXT), specs-and-limits
  (5-min no-data / 15-min request caps, connection limits), and the
  "Application Failed to Respond" troubleshooting page (0.0.0.0 + $PORT)
- docs.railway.com — observability/logs guide (Build Logs tab, Log
  Explorer, retention by plan, 500 lines/sec)
- docs.railway.com — right-size CPU/memory guide (usage rates, 100–400 MB
  idle benchmark, worked cost example)
- docs.railway.com — CLI guide (`up` incl. `[PATH]`, `variable set`,
  `volume add`, `domain`, `logs`, `RAILWAY_TOKEN`; npm/scoop on Windows)
- docs.railway.com — config-as-code reference (deprecated, 2026-12-01
  hard cutoff) and quick-start (New Project → GitHub repo flow)
- docs.railway.com — cost-control guide (usage limits: workloads taken
  offline at the cap, 75/90/100 % warning emails, auto-redeploy when
  raised) and free-trial reference (revert to Free plan after trial;
  trial-created volumes deleted 30 days after credits expire)
- docs.railway.com — "No start command could be found" troubleshooting
  page, exit-code 137/OOM guidance, staged-changes and skipped-builds
  references
- station.railway.com (community forum; staff-answered) — Free-plan
  5-minute build timeout (2025-08-13); healthcheck failure log wording
  (2026-08-06)
- docs.railway.com — variables guide + reference and managing-secrets
  guide (Raw Editor bulk paste, sealed write-only variables, `${{...}}`
  reference syntax, repo `.env` import suggestions); CLI variable/run
  pages (`--stdin`, `--skip-deploys`, batched `KEY=value` pairs)
- railway.com — pricing page (live: trial/Free/Hobby limits and usage
  rates) and login page; docs.railway.com/pricing/free-trial (Full vs
  Limited verification with outbound restriction; verification is
  automated against GitHub-account age/activity, no duration published —
  re-checked 2026-09-20), plans/pricing-FAQs
  (card-only payments, failed-card behavior, volume retention),
  quick-start (New Project paths)
- railpack.com — Python language page (detection, pip, FastAPI+uvicorn
  start command, `RAILPACK_PYTHON_VERSION`, 3.13 default) + railpack
  source `core/providers/python` (requirements.txt precedence, hardcoded
  `main:app` — verified in code, 2026-09-20)
- railway.com/pricing (plans, trial credit, Hobby included usage, rates)

**Known open items (⚠️):** the Free/Trial 5-minute build timeout is
staff-confirmed on the community forum (2025-08-13) but the paid-plan
ceiling is not published; no crash-loop alert text or threshold is
documented (only the On-Failure/10 restart policy is citable); `PORT` is
absent from the variables reference table even though the networking and
healthcheck pages document the injection (a docs inconsistency, not a
behavior doubt); the Free plan is listed as "0 custom domains" but the
docs are silent on whether `*.up.railway.app` traffic still works after a
trial lapses — untested here, so upgrade (or re-test) before relying on it.

---

*Companion documents: `TEST-REPORT-LIVE-2026-09-20.md` (live two-stage test
results) · `VIDEO-HOSTING-RAILWAY.md` (hosting/streaming a video on this
deployment). A responsive standalone HTML version of this guide will be
created on request after the Markdown is reviewed.*
