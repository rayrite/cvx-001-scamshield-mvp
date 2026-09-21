"""CLI for the ScamShield demo app — status + an expected-vs-actual verify suite.

    python cli.py status              # flags, inventory, demo/live, models, data dir
    python cli.py verify [--base URL] # run every check against a running server

verify never takes "it responded" on faith: each check prints EXPECTED vs
ACTUAL and PASS/FAIL, exits 1 if anything failed. Run it against a server
started with demo defaults (no ZAI_API_KEY) — the suite exercises the demo
paths, which share all routing/rendering with the live ones.
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")   # so `status` reports the same mode the server would

import httpx

APP = Path(__file__).parent

PASS = 0
FAIL = 0
FAILURES: list[str] = []


def check(name: str, expected: str, actual, ok: bool | None = None):
    global PASS, FAIL
    if ok is None:
        ok = expected == actual
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"         expected: {expected}")
    print(f"         actual:   {actual}")
    if ok:
        PASS += 1
    else:
        FAIL += 1
        FAILURES.append(name)


def section(title: str):
    print(f"\n== {title} " + "=" * max(0, 66 - len(title)))


def rm_retry(p: Path) -> bool:
    """Windows: a just-served static file can still be held briefly — retry."""
    for _ in range(10):
        try:
            p.unlink(missing_ok=True)
            return True
        except PermissionError:
            time.sleep(0.3)
    return False


# ---------------------------------------------------------------------- status

def cmd_status():
    import agents
    import features
    import jobs
    import orchestrator
    import zai
    import udl
    import chatstore

    flags = features.load_flags()
    eff = features.effective()
    inv = features.inventory()
    cfg = udl.load()

    print("ScamShield demo app — status")
    print(f"  mode          : {'DEMO (canned, honestly labeled)' if orchestrator.DEMO else 'LIVE (z.ai key configured)'}")
    print(f"  models        : intake={zai.INTAKE_MODEL} research={zai.RESEARCH_MODEL} effort={zai.REASONING_EFFORT}")
    print(f"  data dir      : {jobs.DATA_DIR}")
    print(f"  max chat turns: {chatstore.MAX_TURNS}")
    print(f"  theme         : '{cfg['name']}' mode={cfg['mode']} radius={cfg['radius']}")
    print("\n  Feature flags (set → effective):")
    for k in features.DEFAULT_FLAGS:
        mark = lambda b: "on " if b else "OFF"
        note = "" if flags[k] == eff[k] else "  ← content missing!"
        print(f"    {k:<10} {mark(flags[k])} → {mark(eff[k])}{note}")
    print(f"\n  Inventory: {inv['skills']} skills · {inv['quick_prompts']} quick prompts · "
          f"{inv['wikis']} wikis · {inv['spas']} SPAs")
    avail = agents.modes_available()
    for mid, m in avail.items():
        print(f"    {mid:<22} {'✓' if m['available'] else '✗ MISSING'}  {m['label']}")
    if orchestrator.DEMO:
        print("\n  Start the server:  python -m uvicorn main:app --port 8000")
        print("  Then verify:       python cli.py verify")
    return 0


# ---------------------------------------------------------------------- verify

def cmd_verify(base: str) -> int:
    client = httpx.Client(base_url=base, timeout=30)

    def get(path):
        return client.get(path)

    def post(path, json_body=None):
        return client.post(path, json=json_body or {})

    # -- health -------------------------------------------------------------
    section("health")
    r = get("/api/health")
    check("GET /api/health status", 200, r.status_code)
    h = r.json()
    check("health.ok", True, h.get("ok"))
    check("health.demo_mode is bool", "bool", type(h.get("demo_mode")).__name__)
    registry = get("/api/models").json()["models"]
    check("health.models are registry ids", "both registered",
          f"{h.get('intake_model')} / {h.get('research_model')}",
          ok=h.get("intake_model") in registry and h.get("research_model") in registry)

    # -- diagnostics beacon ---------------------------------------------------
    section("diagnostics beacon")
    r = get("/api/diagnostics")
    check("GET /api/diagnostics status", 200, r.status_code)
    d = r.json()
    ids = [c.get("id") for c in d.get("checks", [])]
    check("check ids", "key/net/ping", "/".join(ids),
          ok=ids == ["key", "net", "ping"])
    stat = {c["id"]: c["status"] for c in d["checks"]}
    check("key + net statuses valid", "pass|fail", f"{stat['key']}|{stat['net']}",
          ok=stat["key"] in ("pass", "fail") and stat["net"] in ("pass", "fail"))
    check("ping skipped when a check fails", "consistent", stat["ping"],
          ok=(stat["key"] == "pass" and stat["net"] == "pass") or stat["ping"] == "skip")
    check("ok flag == all passed", all(s == "pass" for s in stat.values()), d.get("ok"))
    key_val = os.environ.get("ZAI_API_KEY", "")
    check("key value never in payload", "absent",
          "clean" if not key_val or key_val not in r.text else "LEAKED",
          ok=not key_val or key_val not in r.text)

    # -- features + modes -----------------------------------------------------
    section("feature flags + mode registry")
    r = get("/api/features")
    f = r.json()
    check("flags all on", True, all(f["flags"].values()))
    check("effective all on", True, all(f["effective"].values()),
          ok=all(f["effective"].values()))
    check("inventory skills", 3, f["inventory"]["skills"])
    check("inventory quick prompts", 4, f["inventory"]["quick_prompts"])
    check("inventory wikis >=2", ">=2", f['inventory']['wikis'], ok=f["inventory"]["wikis"] >= 2)
    check("inventory spas >=1", ">=1", f['inventory']['spas'], ok=f["inventory"]["spas"] >= 1)

    r = get("/api/modes")
    modes = r.json()["modes"]
    check("mode count", 7, len(modes))
    check("all modes available", True, all(m["available"] for m in modes.values()))

    # -- pages ----------------------------------------------------------------
    section("pages")
    PAGES = [
        ("/", "Coolyvision", "company splash"),
        ("/home", "ScamShield", "hero marker"),
        ("/check", "Start check", "staged check form"),
        ("/chat", "Skill chat", "chat surface"),
        ("/quick", "Quick research", "quick surface"),
        ("/learn", "Learning Center", "learn menu"),
        ("/apps", "App Library", "apps menu"),
        ("/video", "Video samples", "sample video players"),
        ("/models", "AI Models", "model switcher"),
        ("/map", "Threat Radar", "threat scenarios"),
        ("/price", "Price Spectrum", "is that price real"),
        ("/theme", "Universal Design Language", "theme editor"),
    ]
    for path, marker, label in PAGES:
        r = get(path)
        check(f"GET {path} ({label})", f"200 + '{marker}'",
              f"{r.status_code} + {'found' if marker in r.text else 'MISSING'}",
              ok=r.status_code == 200 and marker in r.text)
    r = get("/nope-404")
    check("unknown page 404s", 404, r.status_code)

    # -- UDL -------------------------------------------------------------------
    section("UDL (design language)")
    css = get("/udl.css").text
    check("/udl.css has tokens", "--accent + --radius + data-mode",
          "ok" if ("--accent:" in css and "--radius:" in css and "data-mode" in css) else "missing",
          ok="--accent:" in css and "--radius:" in css and "data-mode" in css)
    js = get("/udl.js").text
    check("/udl.js sets mode", "dataset.mode", "ok" if "dataset.mode" in js else "missing",
          ok="dataset.mode" in js)

    original = get("/api/udl").json()
    r = post("/api/udl", {"name": "CLI Verify Theme"})
    check("POST /api/udl accepted", 200, r.status_code)
    check("udl name round-trip", "CLI Verify Theme", get("/api/udl").json().get("name"))
    check("/udl.css reflects new name", "CLI Verify Theme",
          "found" if "CLI Verify Theme" in get("/udl.css").text else "missing",
          ok="CLI Verify Theme" in get("/udl.css").text)
    post("/api/udl", {"name": original["name"]})
    check("udl restored", original["name"], get("/api/udl").json().get("name"))

    # -- model switching (round-trip, credit-free: no call is placed) ------------
    section("model switching")
    m = get("/api/models").json()
    check("model registry count", 6, len(m["models"]))
    check("roles split 4 research / 2 intake", (4, 2),
          (sum("research" in v["roles"] for v in m["models"].values()),
           sum("intake" in v["roles"] for v in m["models"].values())))
    original_sel = m["selection"]
    check("selection matches health", "consistent",
          "ok" if m["selection"] == {"intake": h["intake_model"],
                                     "research": h["research_model"]} else "drift",
          ok=m["selection"] == {"intake": h["intake_model"],
                                "research": h["research_model"]})
    r = post("/api/models", {"intake": "glm-5.3", "research": "glm-5.3"})
    check("role violation rejected", 400, r.status_code)
    r = post("/api/models", {"research": "glm-4.6"})
    check("unknown model rejected", 400, r.status_code)
    r = post("/api/models", {})
    check("empty selection rejected", 400, r.status_code)
    r = post("/api/models", {"intake": "glm-5.3-flashx"})
    check("valid swap accepted", 200, r.status_code)
    check("swap applied", "glm-5.3-flashx",
          get("/api/models").json()["selection"]["intake"])
    check("health reflects swap", "glm-5.3-flashx",
          get("/api/health").json()["intake_model"])
    mm = get("/api/metrics").json()
    check("metrics follows selection", "glm-5.3-flashx", mm.get("intake_model"))
    check("metrics counters are ints", "int/int",
          f"{type(mm.get('inflight')).__name__}/{type(mm.get('max_seen')).__name__}",
          ok=isinstance(mm.get("inflight"), int) and isinstance(mm.get("max_seen"), int))
    check("metrics limit is int|null", True,
          mm.get("limit") is None or isinstance(mm.get("limit"), int),
          ok=mm.get("limit") is None or isinstance(mm.get("limit"), int))
    post("/api/models", original_sel)
    check("selection restored", original_sel, get("/api/models").json()["selection"])

    # -- wikis + dynamic SPA menu ---------------------------------------------
    section("Learning Center + dynamic App Library")
    r = get("/api/wikis").json()["wikis"]
    check("wikis listed", 2, len(r))
    import re as _re
    for w in r:
        raw = (APP / "content" / "wikis" / w["file"]).read_text(encoding="utf-8", errors="replace")
        m = _re.search(r"<title[^>]*>(.*?)</title>", raw, _re.S | _re.I)
        expected_title = (m.group(1).strip() if m else w["file"])[:60]
        check(f"wiki title parsed: {w['file']}", expected_title, w["title"][:60])
        udl_hook = all(s in raw for s in ('href="/udl.css"', 'src="/udl.js"', "UDL bridge"))
        check(f"wiki UDL hook: {w['file']}", "links /udl.css + /udl.js + bridge marker",
              "ok" if udl_hook else "missing", ok=udl_hook)
        framed = ('id="sitenav"' in raw and 'id="sitefooter"' in raw
                  and 'src="/app.js"' in raw and "--accent:#" not in raw)
        check(f"wiki in app frame: {w['file']}",
              "sitenav+sitefooter+/app.js, no hardcoded --accent:#",
              "ok" if framed else "missing", ok=framed)
    r = get("/learn/wiki/dark-patterns-wiki.html")
    check("wiki served via mount", "200 + <title>", f"{r.status_code}",
          ok=r.status_code == 200 and "<title" in r.text.lower())
    check("served wiki carries UDL link", 'href="/udl.css" in HTML',
          "ok" if 'href="/udl.css"' in r.text else "missing",
          ok='href="/udl.css"' in r.text)
    learn_html = (APP / "static" / "learn.html").read_text(encoding="utf-8")
    check("wikis open in same frame", 'no target="_blank" on /learn',
          "absent" if 'target="_blank"' not in learn_html else "present",
          ok='target="_blank"' not in learn_html)

    spa_files = sorted(p.name for p in (APP / "content" / "spas").glob("*.html"))
    spas = get("/api/spas").json()["spas"]
    check("spa menu matches folder contents", len(spa_files), len(spas))
    # dynamic add: drop an html file in the folder, menu must reflect it
    probe = APP / "content" / "spas" / "cli-verify-probe.html"
    probe.write_text("<!doctype html><html><head><title>CLI Dynamic Test</title></head>"
                     "<body>probe</body></html>", encoding="utf-8")
    try:
        spas = get("/api/spas").json()["spas"]
        check("spa appears after add (no restart)", len(spa_files) + 1, len(spas))
        check("probe title extracted", "CLI Dynamic Test",
              next((s["title"] for s in spas if s["file"] == probe.name), None))
        r = get("/apps/spa/cli-verify-probe.html")
        check("probe served via mount", 200, r.status_code)
    finally:
        removed = rm_retry(probe)
    spas = get("/api/spas").json()["spas"]
    check("probe file removed", True, removed)
    check("spa disappears after remove", len(spa_files), len(spas))

    # -- chat (demo) -----------------------------------------------------------
    section("chat API (demo mode)")
    if not h.get("demo_mode"):
        print("  [SKIP] server is LIVE — chat checks would spend real credits")
    else:
        r = post("/api/chat", {"mode": "quick:scamshield", "text": "cli verify quick"})
        check("quick chat status", 200, r.status_code)
        d = r.json()
        check("quick reply is demo-canned", "Demo mode", "found" if "Demo mode" in d["reply"] else "missing",
              ok="Demo mode" in d["reply"])
        check("quick reply shows 3 indicators", "Verdict+Confidence+Ripeness",
              "ok" if all(k in d["reply"] for k in ("Verdict", "Confidence", "Ripeness")) else "missing",
              ok=all(k in d["reply"] for k in ("Verdict", "Confidence", "Ripeness")))
        check("conversation id returned", True, bool(d.get("conversation_id")))

        r = post("/api/chat", {"mode": "skill:corpcheck", "text": "cli verify skill"})
        d2 = r.json()
        check("skill chat status", 200, r.status_code)
        check("skill reply demo-labeled + gated", "Demo mode + Next:",
              "ok" if "Demo mode" in d2["reply"] and "Next:" in d2["reply"] else "missing",
              ok="Demo mode" in d2["reply"] and "Next:" in d2["reply"])
        cid = d2["conversation_id"]
        r = post("/api/chat", {"mode": "skill:corpcheck", "text": "go", "conversation_id": cid})
        d3 = r.json()
        check("second turn turn-number", 2, d3.get("turn"))
        check("turns_left decremented", 10, d3.get("turns_left"))

        r = post("/api/chat", {"mode": "bogus:mode", "text": "x"})
        check("bad mode rejected", 400, r.status_code)
        r = post("/api/chat", {"mode": "quick:scamshield", "text": "x", "conversation_id": "c_deadbeef"})
        check("unknown conversation 404s", 404, r.status_code)

        convs = get("/api/conversations").json()["conversations"]
        check("conversation listed", True, any(c["id"] == cid for c in convs))
        r = client.delete("/api/conversations/" + cid)
        check("conversation deleted", 200, r.status_code)
        r = client.delete("/api/conversations/" + d["conversation_id"])
        check("quick conversation cleaned up", 200, r.status_code)
        convs = get("/api/conversations").json()["conversations"]
        check("conversation gone from list", False, any(c["id"] == cid for c in convs))

    # -- waitlist ---------------------------------------------------------------
    section("waitlist (flat file)")
    import jobs  # DATA_DIR
    wl_file = jobs.DATA_DIR / "waitlist.txt"
    before = get("/api/waitlist").json()["count"]
    test_email = "cli-verify@test.invalid"
    r = post("/api/waitlist", {"email": test_email})
    check("waitlist POST ok", 200, r.status_code)
    after1 = get("/api/waitlist").json()["count"]
    check("count incremented", before + 1, after1)
    r = post("/api/waitlist", {"email": test_email})
    check("duplicate flagged already", True, r.json().get("already"))
    check("count unchanged on duplicate", after1, get("/api/waitlist").json()["count"])
    r = post("/api/waitlist", {"email": "not-an-email"})
    check("bad email rejected", 400, r.status_code)
    flat_ok = wl_file.exists() and any(
        ln.endswith("\t" + test_email) for ln in wl_file.read_text(encoding="utf-8").splitlines())
    check("flat file has tab-separated line", True, flat_ok)
    # clean the probe line back out
    if wl_file.exists():
        lines = [ln for ln in wl_file.read_text(encoding="utf-8").splitlines()
                 if not ln.endswith("\t" + test_email)]
        wl_file.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    check("cleanup: count back to before", before, get("/api/waitlist").json()["count"])

    # -- staged check (demo end-to-end) ------------------------------------------
    section("staged Check v2 (demo end-to-end)")
    if not h.get("demo_mode"):
        print("  [SKIP] server is LIVE — job check would spend real credits")
    else:
        r = post("/api/jobs", {"text": "cli verify: usps redelivery fee text"})
        check("job created 202", 202, r.status_code)
        jid = r.json()["id"]
        job = {}
        for _ in range(30):
            job = get(f"/api/jobs/{jid}").json()
            if job["status"] not in ("queued", "running"):
                break
            time.sleep(0.3)
        check("demo reaches gate", "awaiting_gate", job.get("status"))
        r = post(f"/api/jobs/{jid}/gate", {"decision": "stop"})
        check("gate stop accepted", 200, r.status_code)
        job = r.json()
        for _ in range(20):
            job = get(f"/api/jobs/{jid}").json()
            if job["status"] in ("done", "error"):
                break
            time.sleep(0.3)
        check("job done after stop", "done", job.get("status"))
        check("final verdict in history", True,
              any(v.get("label") == "final" for v in job.get("verdict_history", [])),
              ok=any(v.get("label") == "final" for v in job.get("verdict_history", [])))
        r = get(f"/api/jobs/{jid}/report")
        check("report file exists", 200, r.status_code)
        # leave the demo data clean for the real demo
        (jobs.JOBS_DIR / f"{jid}.json").unlink(missing_ok=True)
        (jobs.REPORTS_DIR / f"{jid}.md").unlink(missing_ok=True)
        check("verify job cleaned up", False,
              any(j["id"] == jid for j in get("/api/jobs").json()["jobs"]))

    # -- summary -------------------------------------------------------------------
    print("\n" + "=" * 72)
    print(f"RESULT: {PASS} passed, {FAIL} failed" + (f" — {', '.join(FAILURES)}" if FAILURES else ""))
    return 1 if FAIL else 0


def main():
    ap = argparse.ArgumentParser(description="ScamShield demo app CLI")
    ap.add_argument("command", choices=["status", "verify"])
    ap.add_argument("--base", default="http://127.0.0.1:8000",
                    help="base URL of a running server (verify only)")
    args = ap.parse_args()
    try:
        if args.command == "status":
            sys.exit(cmd_status())
        sys.exit(cmd_verify(args.base))
    except httpx.ConnectError as e:
        print(f"✖ cannot reach {args.base} — start the server first:\n"
              f"    python -m uvicorn main:app --port 8000\n  ({e})")
        sys.exit(2)


if __name__ == "__main__":
    main()
