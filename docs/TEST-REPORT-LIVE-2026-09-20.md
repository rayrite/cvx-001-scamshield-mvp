# Live test report — two-stage image decode + web research (2026-09-20)

**Purpose.** Locally exercise, with the live z.ai key, (A) the staged
**rdw-scamshield-check-v2** pipeline (vision intake → snap smoke test → gates →
documentation + verify web-research stages → consolidation) and (B) the
single-pass quick check driven by
`app/content/prompts/system-prompt-scamshield-check.md`, using
`testing/email_test01.png` as input.

**Result: PASS — 37/38 checks passed in the automated run; the single FAIL was
a bug in the test's own regex (it rejected an emoji-prefixed label), corrected
and re-verified offline against the saved output: 38/38 effective.**

| | |
|---|---|
| Server | `http://127.0.0.1:8000`, LIVE mode (`demo_mode: false`, key configured) |
| Models | intake `glm-5.3-flash` (vision) · research `glm-5.3` (`reasoning_effort=low`) |
| Input | `testing/email_test01.png` — 90,277 bytes → 120,394-char data-URI (cap 7,340,032) |
| Job id | `j_6d79636b0977` |
| Wall clock | 15:24:42 → 15:26:40 (Test A ≈ 91 s, Test A2 ≈ 4 s, Test B ≈ 23 s) |
| Raw artifacts | `testing/live-test-results/live-test-results-2026-09-20.json`, `testA_report_j_6d79636b0977.md` |
| Test script | `testing/live_test_2026-09-20.py` |

---

## Ground truth (independently established)

The image is a screenshot of a **Sam's Club “Your Membership Has Ended”
account-renewal phishing email**:

- **From:** `Festaslots <noreply@Fiestaslotspromo.com>` **on behalf of** “Sam's
  Club” `<UT0OG5GK@TWZCT38S2JNPFMOTV2MLGKVIL1XC>` — a spoofed send-through;
  the real Sam's Club domain appears nowhere in the sender chain.
- **Subject:** none · **Date:** Sun 9/20/2026 1:42 PM
- Webmail junk banner (“This message was identified as junk…”).
- Body: renewal lure — “90 additional days of benefits at no extra cost”, a
  member-details table cropped/illegible below the fold, no URLs visible.

Ground truth was cross-established by **two independent vision passes**
(the pipeline's own intake and a strict second-pass QA transcription, Test A2
below) plus the quick-prompt analysis. Both passes independently extracted the
same sender address (`noreply@fiestaslotspromo.com`); token-level agreement
Jaccard = **0.536** (high for two free transcriptions of the same image).

---

## Test A — staged Check v2 (`rdw-scamshield-check-v2`)

Flow driven exactly as a user would: `POST /api/jobs` (caption + image, worry
`legitimacy`) → poll → gate **document** → gate **go** (verify) → gate **stop**
→ `done` → `GET /api/jobs/{id}/report`.

| Check | Result |
|---|---|
| Job accepted (202) + poll to first gate | **PASS** — `awaiting_gate` in **15.1 s** |
| Gate presented correctly | **PASS** — kind `post_snap`, options `[document, stop]` |
| Vision transcript produced | **PASS** — 996 chars, structured (From/Reply-To/Subject/Date/Body), URLs defanged convention respected (none visible), illegible regions marked |
| Intake model + usage logged | **PASS** — `glm-5.3-flash`, 2,093 in / 276 out tokens |
| Smoke test (snap verdict) | **PASS** — `glm-5.3`, 🔴 **Scam pattern match — confidence High** in 5.1 s |
| Gate `document` → web research | **PASS** — 10 search results, 22.5 s, 23,486 tokens |
| Gate `go` → verify stage | **PASS** — 4 more search results, 17.6 s |
| Gate `stop` → consolidate → `done` | **PASS** — final 🔴 **Scam pattern match — High** |
| Report file | **PASS** — served at `/api/jobs/{id}/report`, copy saved |

**Verdict history (all four entries):**

| Stage | Verdict | Confidence | Label |
|---|---|---|---|
| Stage 0/½ — Smoke Test | 🔴 Scam pattern match | High | snap |
| Stage 1 — Documentation Pass | 🔴 Scam pattern match | High | snap |
| Stage 2 — Domain Check | 🔴 Scam pattern match | High | final |
| Final Report — Consolidated | 🔴 Scam pattern match | High | final |

**Job budget:** 5 model calls · 14 search results · 59,086 tokens in ·
6,042 tokens out.

**Research quality (fairness mandate).** The web-research stages surfaced
real, dated, on-point sources — the Sam's Club help/security page, a KY3
"On Your Side" news report (Oct 7, 2024) confirming this exact
membership-renewal scam wave, and an AARP report (Nov 5, 2021) on Sam's
Club-name phishing. Inferences below the fold are labeled as inferred, and
the output recommends not clicking to verify — balanced, grounded, no
unsubstantiated claims.

## Test A2 — decode stability (second independent pass)

A second `glm-5.3-flash` call with a strict "verbatim transcription" prompt,
compared against the pipeline's transcript:

- **PASS** — decode non-empty and structured.
- **PASS** — token Jaccard 0.536 between passes.
- **PASS** — sender e-mail identical in both passes (1/1 matched).
- Money amounts: none visible in either pass (consistent — the lure is
  "no extra cost", and the pricing table is cropped).

## Test B — quick single-pass (`system-prompt-scamshield-check.md`)

`POST /api/chat` `{"mode": "quick:scamshield", text, images}` — the same
screenshot through the quick prompt (this path runs its own vision intake,
appends the transcript, then one `glm-5.3` call with `web_search`).

| Check | Result |
|---|---|
| 200 + `demo: false` (genuinely live) | **PASS** |
| Not demo-canned ("Demo mode" absent) | **PASS** |
| **Three separate indicator lines** | **PASS** — see below |
| Sources attached | **PASS** — 3 sources |
| Substantive reply | **PASS** — 2,316 chars |
| Conversation deleted after test | **PASS** |

The reply opens with the mandate's three independent indicators, each on its
own line:

```
**🔴 Verdict:** Scam pattern match — account-renewal phishing impersonating
               Sam's Club (sender domain ≠ samsclub.com)
**Confidence:** High — decisive tell observed directly in the message
**Ripeness:** LOW — case closed by direct observation; nothing left worth digging
```

Sources cited: help.samsclub.com (security page), KY3 Oct 7 2024, AARP
Nov 5 2021. Caveats section correctly separates observed facts from inference.

## The one FAIL, and its resolution

`indicator on its own line: Verdict` failed because the test regex
(`^\s*\**Verdict`) did not tolerate the emoji glyph inside the bold label
(`**🔴 Verdict:**`). Confidence/Ripeness (no emoji) matched fine. The regex
was corrected in `live_test_2026-09-20.py` and re-run offline against the
saved reply: all three indicators on their own lines — **the model output was
compliant; the checker was not.** No additional API calls were spent.

## Cost of this test (estimate)

Test A: 59,086 in × $1.40/MTok ≈ $0.083 + 6,042 out × $4.40/MTok ≈ $0.027
+ 2 web-search calls ≈ $0.02. Test A2: ≈ $0.001 (flash). Test B: ≈ $0.06
(vision + research + 1 search). **Total ≈ $0.19.**

## Observations (not defects)

1. `verdict_history` shows two entries labeled *final* (Stage 2 — Domain
   Check, and the Consolidated report). This is the state machine's design —
   the last research stage may self-label `final` and consolidation always
   appends one — but a UI consumer should take the **last** entry as final.
2. `elapsed_s` is logged for research stages but not intake/consolidate
   (0 in the ledger); timing above comes from wall-clock.
3. Cleanup verified: job JSON + report MD removed from `app/data/jobs` and
   `app/data/reports`; Test B conversation deleted — the app's data dirs are
   exactly as they were before the test.
