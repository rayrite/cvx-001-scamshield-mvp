"""End-to-end smoke test for the hosted agent (demo mode, real uvicorn server).

Run with the server up:  uvicorn main:app --port 8111   then   python smoke_test.py
Exercises: health, job create → poll → snap gate → document → go → stop →
done/report, the list endpoint, and the 404/409 error paths.
"""
import sys
import time

import httpx

BASE = "http://127.0.0.1:8111"
FAILS: list[str] = []


def check(name: str, cond: bool, extra: str = ""):
    print(("PASS " if cond else "FAIL ") + name + (f"  [{extra}]" if extra else ""))
    if not cond:
        FAILS.append(name)


def wait_for(client, jid, statuses, timeout=30):
    t0 = time.time()
    while time.time() - t0 < timeout:
        j = client.get(f"{BASE}/api/jobs/{jid}").json()
        if j.get("status") in statuses:
            return j
        time.sleep(0.5)
    return j


def main():
    c = httpx.Client(timeout=15)

    h = c.get(f"{BASE}/api/health").json()
    check("health ok", h.get("ok") is True)
    check("demo mode on", h.get("demo_mode") is True)

    # 404 paths
    check("missing job 404", c.get(f"{BASE}/api/jobs/j_deadbeef00").status_code == 404)
    check("bad id rejected", c.get(f"{BASE}/api/jobs/../../etc").status_code in (400, 404))

    # bad create
    r = c.post(f"{BASE}/api/jobs", json={"text": "", "images": [], "worry": "legitimacy"})
    check("empty text rejected", r.status_code in (400, 422), str(r.status_code))
    r = c.post(f"{BASE}/api/jobs", json={"text": "x", "worry": "bogus"})
    check("bad worry rejected", r.status_code == 400)
    r = c.post(f"{BASE}/api/jobs", json={"text": "x", "images": ["javascript:alert(1)"]})
    check("non-image URI rejected", r.status_code == 400)

    # --- job 1: full happy path --------------------------------------------------
    r = c.post(f"{BASE}/api/jobs", json={
        "text": "got an email: 'Your USPS package is on hold — pay $1.99 redelivery "
                "fee: usps-delivery-fee.net'. Real?",
        "worry": "legitimacy",
    })
    check("create 202", r.status_code == 202 and "Location" in r.headers, r.text[:80])
    jid = r.json()["id"]

    j = wait_for(c, jid, {"awaiting_gate", "done", "error"})
    check("smoke snap → gate", j["status"] == "awaiting_gate", j["status"])
    check("gate is post_snap", j["gate"]["kind"] == "post_snap" and "document" in j["gate"]["options"])
    check("snap verdict in history", j["verdict_history"][-1]["label"] == "snap"
          and "🔴" in j["verdict_history"][-1]["verdict"])
    check("stage logged", len(j["stage_log"]) == 1 and "smoke" in j["stage_log"][0]["stage"])

    # gate on wrong decision
    r = c.post(f"{BASE}/api/jobs/{jid}/gate", json={"decision": "warp"})
    check("bad decision 400", r.status_code == 400)

    # document pass
    j = c.post(f"{BASE}/api/jobs/{jid}/gate", json={"decision": "document"}).json()
    j = wait_for(c, jid, {"awaiting_gate", "done", "error"})
    check("document → post_stage gate", j["status"] == "awaiting_gate" and j["gate"]["kind"] == "post_stage")
    check("doc stage labeled 1", j["stage_number"] == 1)
    check("verdict history grew", len(j["verdict_history"]) == 2)

    # go → verify (demo canned)
    j = c.post(f"{BASE}/api/jobs/{jid}/gate", json={"decision": "go"}).json()
    j = wait_for(c, jid, {"awaiting_gate", "done", "error"})
    check("verify stage ran", j["status"] == "awaiting_gate" and j["stage_number"] == 2
          and any(e["stage"] == "verify" for e in j["stage_log"]))

    # custom redirect
    j = c.post(f"{BASE}/api/jobs/{jid}/gate", json={"decision": "custom", "text": "check if this domain family recycles"}).json()
    j = wait_for(c, jid, {"awaiting_gate", "done", "error"})
    check("custom redirect ran", j["status"] == "awaiting_gate" and j["stage_number"] == 3)

    # stop → consolidate
    j = c.post(f"{BASE}/api/jobs/{jid}/gate", json={"decision": "stop"}).json()
    j = wait_for(c, jid, {"done", "error"})
    check("consolidated done", j["status"] == "done" and j["report"], j["status"])
    check("final label", j["verdict_history"][-1]["label"] == "final")
    check("budget counted", j["budget"]["model_calls"] >= 4 and j["budget"]["search_results"] >= 4,
          str(j["budget"]))

    rep = c.get(f"{BASE}/api/jobs/{jid}/report")
    check("report endpoint", rep.status_code == 200 and "VERDICT" in rep.text
          and rep.headers["content-type"].startswith("text/markdown"))

    # gate after done → 409
    r = c.post(f"{BASE}/api/jobs/{jid}/gate", json={"decision": "go"})
    check("gate after done 409", r.status_code == 409)

    # --- job 2: images path (demo transcript) ------------------------------------
    tiny_png = ("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFc"
                "SJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==")
    r = c.post(f"{BASE}/api/jobs", json={"text": "screenshot of the email attached", "images": [tiny_png]})
    check("image job created", r.status_code == 202, r.text[:80])
    j2 = wait_for(c, r.json()["id"], {"awaiting_gate", "done", "error"})
    check("transcript present", bool(j2.get("transcript")))

    # --- list endpoint -------------------------------------------------------------
    lst = c.get(f"{BASE}/api/jobs").json()["jobs"]
    check("list has jobs", len(lst) >= 2 and all("id" in x and "status" in x for x in lst))

    # --- static UI -----------------------------------------------------------------
    ui = c.get(f"{BASE}/")
    check("landing served", ui.status_code == 200 and "Before you click buy" in ui.text)
    ui2 = c.get(f"{BASE}/check")
    check("check page served", ui2.status_code == 200 and "Start check" in ui2.text)

    print()
    if FAILS:
        print(f"{len(FAILS)} FAILURES: " + ", ".join(FAILS))
        sys.exit(1)
    print("ALL PASS")


if __name__ == "__main__":
    main()
