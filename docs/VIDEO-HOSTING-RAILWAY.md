# Hosting and streaming a video on Railway — ScamShield demo

> **Audience.** You have (or are about to deploy) the ScamShield service
> from [DEPLOY-RAILWAY.md](DEPLOY-RAILWAY.md) and want to add one video
> file, served from a simple HTML page, playable and seekable in the
> browser.
>
> **Verified.** Railway-specific claims were checked against
> docs.railway.com on **2026-09-20**. The streaming behavior itself was
> verified **empirically** against this app's actual installed packages
> (fastapi 0.141.1 · starlette 1.6.0 · uvicorn 0.53.0): 11/11 checks
> passed — HTTP `Range` requests answered with `206 Partial Content`,
> correct `Content-Range` headers, `video/mp4` MIME type, proper 404/416.
> The test script ships at `testing/video_range_check_2026-09-20.py`.

**Short answer: yes.** Railway has no video-specific feature and doesn't
need one — an ordinary web server that answers HTTP **Range requests**
gives browsers everything they need to stream and seek a `<video>` element.
Your FastAPI service does this out of the box. The work is: put a
browser-compatible MP4 on the volume, expose it through a static mount,
and add one HTML page.

---

## 0. How HTTP video "streaming" actually works (60 seconds)

There is no magic protocol here for demo-scale video:

1. The browser loads your HTML page, which contains a `<video>` element.
2. The browser requests the video URL. Playback starts as data arrives —
   it does **not** wait for the whole file.
3. When you **seek** (click the middle of the timeline), the browser sends
   a new request with a `Range: bytes=N-M` header, and the server replies
   `206 Partial Content` with just that slice.
4. If the server ignored `Range`, every seek would restart the download
   from byte 0 — the symptom would be "seeking doesn't work".

FastAPI/Starlette's `StaticFiles` and `FileResponse` answer Range requests
correctly (support added in Starlette 0.39.0; a Range-handling security
patch landed in 0.49.1 — your install, 1.6.0, is far past both). The
response is streamed in chunks, so a 400 MB video does **not** load 400 MB
into the service's RAM.

```
browser ── GET /video.html ─────────► static mount (app/static/)
        ── GET /videos/demo.mp4 ────► /videos mount ──► volume /data/videos/
           (Range: bytes=…  → 206)        (served by FileResponse)
```

The video file lives on the **volume**, never in the git repo — see §2.

---

## 1. Railway constraints that specifically matter for video

All verified 2026-09-20 (details in [DEPLOY-RAILWAY.md](DEPLOY-RAILWAY.md)):

| Constraint | Value | Practical meaning for video |
|---|---|---|
| Volume size | **0.5 GB** Trial / **5 GB** Hobby (one volume per service) | Keep the video comfortably under ~450 MB on Trial, or move to Hobby |
| Edge request caps | requests closed after **5 min with no data** / **15 min max** even with data flowing | One continuous transfer can't exceed ~15 minutes wall-clock. A 100–300 MB file transfers in well under that on normal connections; a half-gigabyte file on a slow connection may stall near the end. Seeking recovers (each seek is a fresh request). |
| Egress | **$0.05/GB**, counts against usage credit | A 100 MB video watched 10 times = 1 GB ≈ $0.05. Trivial at demo scale. |
| GitHub file limit | **100 MB hard block** per file (warning at 50 MB) | The other reason the video must not live in the repo — push would be rejected outright. |
| RAM/CPU billing | usage-based; streaming is chunked, not whole-file | Serving video does not spike memory; idle cost unchanged. |

> **Trial bonus warning** (from the deploy guide): volumes created by
> Trial accounts are deleted 30 days after trial credits expire — another
> reason to keep the master copy of the video on your machine.

---

## 2. Prepare the video file (ffmpeg — you have 9.0.1 installed)

Two things quietly break browser playback, and both are about the *file*,
not the server:

1. **Codec.** Browsers universally play **H.264 video + AAC audio in an
   MP4 container**. iPhones record **HEVC/H.265** by default — those files
   play in Safari but often not in Chrome/Edge on Windows.
2. **"Faststart" / moov atom position.** MP4s keep their index (the *moov*
   atom) at the end by default; the browser wants it up front or it can't
   start playing until the whole file has arrived. Remuxing moves it —
   seconds of work, zero quality loss.

**Inspect what you have** (read the `Stream #…` lines — `hevc` = problem,
`h264` = good):

```bash
ffmpeg -i input.mov
```

**If it's already H.264 but plays only after a full download** — remux
only (fast, no re-encode):

```bash
ffmpeg -i input.mp4 -c copy -movflags +faststart demo.mp4
```

**Full universal re-encode** (HEVC source, or anything exotic):

```bash
ffmpeg -i input.mov -c:v libx264 -preset medium -crf 23 -c:a aac -b:a 128k -movflags +faststart demo.mp4
```

Optional shrink for big files (720p is plenty for a demo):

```bash
ffmpeg -i input.mp4 -vf scale=-2:720 -c:v libx264 -crf 24 -c:a aac -movflags +faststart demo.mp4
```

Sanity-check the result plays locally (double-click it) before going
further — if your local browser can't play it, Railway won't fix that.

---

## 3. Path A — add video to the existing ScamShield service (recommended)

Reuses the service, volume, and domain you already have; costs nothing
extra. Three additions, then one upload.

> **Already shipped (2026-09-20).** This section is now part of the app:
> the `/videos` mount is in `app/main.py`, the `video` feature flag gates
> it, and the **`/video`** page serves two UDL-themed placeholder players
> (`demo1.mp4`, `demo2.mp4`) with a 1-byte Range probe that reports
> *streaming + size*, *not found*, or *found-but-won't-decode* per file.
> Verified live locally: `206` + exact `content-range` on both clips,
> including a high-offset request near the end of the 1.1 MB file (the
> seek path). The code below stays as the walkthrough of what was added;
> §3.2's plain HTML page remains the **minimal standalone example** if you
> ever want a video page without the app's design language around it.

### 3.1 Serve the videos folder (two lines + one guard)

In `app/main.py`, **above the catch-all static mount** (mounts match in
order — if `app.mount("/", …)` came first it would shadow `/videos`):

```python
# ── video demo: serve /data/videos with Range support ──────────────
VIDEOS_DIR = jobs.DATA_DIR / "videos"
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)   # StaticFiles crashes at boot if missing
app.mount("/videos", StaticFiles(directory=VIDEOS_DIR), name="videos")
```

(`jobs.DATA_DIR` is the app's existing data root — locally `app/data`, on
Railway `/data` from `DATA_DIR=/data`. The `mkdir` matters: `StaticFiles`
checks the directory exists when the app starts, and a missing folder
would crash the deployment rather than 404.)

Place this next to the existing `/learn/wiki` and `/apps/spa` mounts,
before `app.mount("/", StaticFiles(directory=STATIC, html=True), …)`.

### 3.2 The HTML page

Create `app/static/video.html` — the existing static mount serves it at
**`/video.html`**:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Video — ScamShield demo</title>
  <style>
    :root { color-scheme: dark; }
    body { margin: 0; min-height: 100vh; display: grid; place-items: center;
           background: #0f1115; color: #e6e8ee;
           font: 16px/1.6 system-ui, "Segoe UI", Roboto, sans-serif; }
    main { width: min(920px, 94vw); padding: 24px 0 48px; }
    h1 { font-size: 1.35rem; margin: 0 0 4px; }
    p.sub { margin: 0 0 20px; color: #9aa3b2; font-size: .95rem; }
    video { width: 100%; border-radius: 12px; background: #000;
            box-shadow: 0 12px 40px rgba(0,0,0,.45); }
    p.note { color: #9aa3b2; font-size: .88rem; }
  </style>
</head>
<body>
  <main>
    <h1>Video demo</h1>
    <p class="sub">Served from the service volume with HTTP Range streaming.</p>
    <video controls preload="metadata" playsinline>
      <source src="/videos/demo.mp4" type="video/mp4">
      Your browser does not support HTML5 video.
    </video>
    <p class="note">If playback stalls near the end of a very large file,
    click slightly ahead on the timeline — each seek opens a fresh request.</p>
  </main>
</body>
</html>
```

`controls` gives the native play/seek/volume UI; `preload="metadata"`
fetches just enough to show duration before the user presses play;
`playsinline` avoids fullscreen-forcing on iOS. (The app's real page —
**`/video`**, at `app/static/video.html` — is this plus the UDL: it links
`/udl.css` + `/app.js` and consumes only the design tokens, so `/theme`
restyles it like every other page, and it renders two players with the
placeholder probe instead of one hardcoded file.)

### 3.3 Test locally before touching Railway

1. Put the prepared file where the local server looks for it:

   ```bash
   mkdir -p app/data/videos
   cp demo.mp4 app/data/videos/demo.mp4
   ```

2. Start the server as usual and open **http://127.0.0.1:8000/video.html**
   — the video should play immediately and the timeline should seek
   instantly anywhere.

3. Confirm Range handling from a terminal (PowerShell/Git Bash — `curl.exe`
   ships with Windows):

   ```bash
   curl.exe -s -o NUL -D - -H "Range: bytes=0-1023" http://127.0.0.1:8000/videos/demo.mp4
   ```

   You want **`HTTP/1.1 206 Partial Content`**, a
   **`content-range: bytes 0-1023/<file size>`** header, and
   **`content-type: video/mp4`**. (A `200` here instead of `206` means
   Range isn't being honored — seeking would misbehave. The 11/11 offline
   check with this app's packages confirms it will be 206.)

### 3.4 Deploy the code change

Exactly as in the deploy guide: commit + push (autodeploy picks it up), or
`railway up ./app`. Nothing video-specific here.

### 3.5 Upload the video to the Railway volume

The file never goes through git. With the CLI (install/link steps in
Part 8 of the deploy guide):

```bash
railway login
railway link                 # pick workspace → project → environment → scamshield
railway volume files upload ./app/data/videos/demo.mp4 /videos/demo.mp4 --overwrite
railway volume files list /videos      # confirm it landed
```

Path semantics: `volume files` paths are **inside the volume** — leading
`/` is the volume root, which the container sees at your mount point
(`/data`). So `/videos/demo.mp4` on the volume = `/data/videos/demo.mp4`
in the container = exactly where the mount from §3.1 looks. The `list`
command above is the confirmation. (`--overwrite` lets you re-upload an
updated cut; drop it for first upload.) Prefer a terminal UI?
`railway volume browse` opens an interactive browser with
upload/download/rename/delete. Note there is **no dashboard file browser**
— volume file management is CLI-only.

Uploading a file does **not** restart the service — the mount serves
whatever is in the folder, so no redeploy is needed for new videos.

### 3.6 Verify in production

Open `https://<your-app>.up.railway.app/video.html`:

| Step | Expect | Verifies |
|---|---|---|
| 1 | Page renders with the player frame | static page deployed |
| 2 | Press play — starts within seconds | file on volume, MIME correct |
| 3 | Click the middle of the timeline — jumps instantly | Range/206 in production |
| 4 | `curl.exe -s -o NUL -D - -H "Range: bytes=0-1023" https://<app>.up.railway.app/videos/demo.mp4` → `206` | edge → service path intact |

---

## 4. Path B — a standalone mini-service (if you don't want to touch ScamShield)

A second, tiny service in the same project (Trial allows 5 services per
project; idle cost roughly $1–1.5/month of usage credit). Four files:

**`main.py`**

```python
"""Minimal video host: static page + Range-streamed /videos from the volume."""
from pathlib import Path
import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

DATA_DIR = Path(os.getenv("DATA_DIR", "/data"))
VIDEOS_DIR = DATA_DIR / "videos"
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI()
app.mount("/videos", StaticFiles(directory=VIDEOS_DIR), name="videos")
app.mount("/", StaticFiles(directory=Path(__file__).parent / "static", html=True), name="site")
```

**`static/index.html`** — reuse the page from §3.2 as-is.

**`requirements.txt`**

```text
fastapi
uvicorn
```

**`Procfile`**

```text
web: uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
```

Deploy it with the same procedure as the main guide (Parts 2–6), with two
differences: the files sit at the **repo root** (so no Root Directory
setting is needed), and the only variable is `DATA_DIR=/data` with a
volume mounted at `/data`. Then upload the video exactly as in §3.5
(`-s`/`--service` picks this service instead). Optional belt-and-suspenders:
pin `starlette>=0.49.1` in `requirements.txt` so the Range support (and its
security patch) can never be resolved away.

---

## 5. Troubleshooting

| Symptom | Cause → Fix |
|---|---|
| Video only starts after the *entire* file downloads | moov atom at end → remux: `ffmpeg -i in.mp4 -c copy -movflags +faststart demo.mp4` (§2) |
| Plays in Safari, "no video" / error in Chrome or Edge | HEVC source → full re-encode with `libx264` + `aac` (§2) |
| `404 Not Found` on `/videos/demo.mp4` | File not uploaded, or uploaded to the wrong remote path → `railway volume files list /videos`; also confirm the `app.mount("/videos", …)` line deployed |
| Service **crashes at boot** right after adding the mount | The videos directory didn't exist at startup → the `VIDEOS_DIR.mkdir(...)` guard in §3.1 exists precisely for this; make sure it runs before the mount |
| Seeking always restarts from 0:00 / never lands where clicked | Server not honoring Range (stale Starlette) → this stack returns 206 (verified); if you ever see `200` on a Range request, update dependencies (`starlette>=0.49.1`) |
| Playback stalls near the end of a very large file | Railway edge caps a request at 15 min even with data flowing (§1) → click ahead on the timeline (fresh Range request), or use a smaller file |
| Video downloads instead of playing | Wrong MIME — don't rename the file to a non-`.mp4` extension; `StaticFiles` sets `video/mp4` from the extension (verified) |
| Works locally, 404 in production | The code deployed but the video didn't — the file is **not** in git by design; run the §3.5 upload |
| Slow start for viewers far from the region | No CDN in front of Railway — expected at demo scale; see §6 |

---

## 6. When to outgrow this setup

This approach is comfortably good for demo-scale: a handful of videos,
file sizes into the low hundreds of MB, tens of viewers. Beyond that
(many concurrent viewers, long-form content, global audience), the
standard architecture is object storage + CDN — e.g. Railway's own
S3-compatible **Buckets** (billed ≈ $0.015/GB-month per the 2026-09-20
pricing page) or S3/Cloudflare R2 in front of a CDN, with your HTML page
simply pointing its `<source>` at the public/pre-signed URL. That changes
nothing about the player — Range streaming still does the work; only the
URL origin moves.

---

## 7. Sources and verification log (2026-09-20)

- **Empirical (this machine, this app's venv):** fastapi 0.141.1 /
  starlette 1.6.0 / uvicorn 0.53.0 — `StaticFiles` mount and `FileResponse`
  route both return `206 Partial Content` with exact `Content-Range`
  headers, `accept-ranges: bytes`, `video/mp4` MIME, `416` on past-end
  ranges, `404` on missing files. 11/11 checks —
  `testing/video_range_check_2026-09-20.py` (rerunnable, offline, no key).
- **ffmpeg 9.0.1-essentials** present locally; commands in §2 are standard
  libx264/aac/faststart invocations.
- docs.railway.com — CLI volume reference: `railway volume files upload
  <LOCAL_PATH> <REMOTE_PATH>` with `--overwrite`; `volume files
  list/download/delete`; `railway volume browse` interactive TUI.
- docs.railway.com — volumes guide: file management is CLI-only ("Use the
  Railway CLI to inspect and manage files stored on a volume"); live
  resize available on paid plans.
- docs.railway.com — CLI link reference: `railway link` interactively
  selects workspace/project/environment/service; stores the link in a
  `.railway` directory (usually gitignored).
- Starlette version history (web-search sourced, flagged as such): Range
  support in `FileResponse` added in 0.39.0; O(n²) Range-header DoS
  patched in 0.49.1.
- Cross-referenced from [DEPLOY-RAILWAY.md](DEPLOY-RAILWAY.md) (verified
  same day): edge request caps (5 min no-data / 15 min max), egress
  $0.05/GB, volume sizes 0.5 GB Trial / 5 GB Hobby, one volume per
  service, trial-volume deletion 30 days after credit expiry, GitHub
  100 MB per-file limit.

**Open items (⚠️):** the CLI docs don't explicitly define whether
`volume files` remote paths are volume-rooted or container-absolute —
this guide states volume-rooted (consistent with the docs' `/backup.tar`
examples) and includes a `files list` self-check after upload; Railway
Buckets' public-serving details were not researched here (pricing only).

---

*Companion documents: `DEPLOY-RAILWAY.md` (full deploy guide) ·
`TEST-REPORT-LIVE-2026-09-20.md` (live z.ai test). A responsive standalone
HTML version of this guide will be created on request after review.*
