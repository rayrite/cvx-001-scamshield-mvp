/* Shared front-end helpers. Every page links /udl.css + /udl.js (the design
   language) and this file (nav, flags, markdown, image downscale). */
"use strict";

const $ = id => document.getElementById(id);
const esc = s => String(s ?? "").replace(/[&<>"']/g, c =>
  ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));

async function api(path, opts) {
  const resp = await fetch(path, opts);
  let data = null;
  try { data = await resp.json(); } catch { /* non-JSON error */ }
  if (!resp.ok) throw new Error((data && (data.detail || data.error)) || ("HTTP " + resp.status));
  return data;
}

// markdown → sanitized HTML (marked + DOMPurify are SRI-pinned CDN <script>s
// on the pages that need them; degrade to escaped <pre> if a CDN is blocked)
function md(text) {
  if (!window.marked) return "<pre>" + String(text).replace(/</g, "&lt;") + "</pre>";
  const html = marked.parse(String(text));
  return window.DOMPurify ? DOMPurify.sanitize(html) : html;
}

// --- client-side image downscale (canvas, never-grow, alpha→white) ------------
const MAX_EDGE = 1600, JPEG_Q = 0.9;
function loadImage(src) {
  return new Promise((res, rej) => {
    const img = new Image();
    img.onload = () => res(img);
    img.onerror = () => rej(new Error("unreadable image"));
    img.src = src;
  });
}
async function shrink(dataUrl) {
  const img = await loadImage(dataUrl);
  const scale = Math.min(1, MAX_EDGE / Math.max(img.width, img.height));
  if (scale === 1 && dataUrl.startsWith("data:image/jpeg")) return dataUrl;
  const c = document.createElement("canvas");
  c.width  = Math.max(1, Math.round(img.width  * scale));
  c.height = Math.max(1, Math.round(img.height * scale));
  const ctx = c.getContext("2d");
  ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, c.width, c.height);
  ctx.drawImage(img, 0, 0, c.width, c.height);
  const out = c.toDataURL("image/jpeg", JPEG_Q);
  return out.length < dataUrl.length ? out : dataUrl;
}
/* Reads up to `max` files from an input change event, downscaling each and
   returning data URLs. Alerts (and skips) files that fail the caps. */
async function readImages(fileList, max) {
  const out = [];
  for (const f of fileList) {
    if (out.length >= max) break;
    if (f.size > 25 * 1024 * 1024) { alert(f.name + " is too large for the browser to process."); continue; }
    try {
      const raw = await new Promise(res => {
        const r = new FileReader(); r.onload = () => res(r.result); r.readAsDataURL(f);
      });
      const small = await shrink(raw);
      if (small.length > 5 * 1024 * 1024 * 1.4) { alert(f.name + " is still over 5 MB after downscaling."); continue; }
      out.push(small);
    } catch { alert(f.name + " couldn't be read as an image."); }
  }
  return out;
}

// --- site header: one markup source, active link, flag-aware, demo chip -------
const NAV = [
  ["/",        "Home",    null],
  ["/check",   "Check",   "check"],
  ["/chat",    "Chat",    "chat"],
  ["/quick",   "Quick",   "quick"],
  ["/learn",   "Learn",   "learning"],
  ["/apps",    "Apps",    "apps"],
  ["/video",   "Video",   "video"],
  ["/map",     "Map",     null],
  ["/price",   "Price",   null],
  ["/models",  "Models",  null],
  ["/theme",   "Theme",   null],
];

// --- system-check beacon (header pill): GET /api/diagnostics -------------------
const DIAG_TITLES = { key: "API key configured", net: "Internet · z.ai host" };
const DIAG_NAMES = { key: "API key", net: "internet", ping: "z.ai ping" };
const DIAG_SUBS = {
  key: "presence only — the key itself is never returned",
  net: "the exact host the app depends on",
};
let diagRunning = false;

function diagPill(state, label) {
  const btn = $("diagBtn");
  if (!btn) return;
  btn.dataset.state = state;
  $("diagLabel").textContent = label;
}

function diagRow(status, title, why, ms) {
  const s = { pass: '<span class="s pass">✓</span>', fail: '<span class="s fail">✗</span>',
              skip: '<span class="s skip">–</span>', run: '<span class="spin"></span>' }[status];
  return `<div class="chk">${s}<span class="name"><b>${esc(title)}</b>` +
         (why ? `<span class="why">${esc(why)}</span>` : "") + `</span>` +
         (ms ? `<span class="ms">${esc(ms)}</span>` : "") + `</div>`;
}

/* One fetch → all three rows resolve together (the server runs the checks).
   Amber "···" while in flight, then GO/OFF. Click = re-run for fresh results. */
async function runDiag() {
  const btn = $("diagBtn"), panel = $("diagPanel"),
        rows = $("diagRows"), verdict = $("diagVerdict");
  if (!btn || !panel || diagRunning) return;
  diagRunning = true;
  diagPill("run", "···");
  rows.innerHTML = ["key", "net", "ping"].map(id =>
    diagRow("run", DIAG_TITLES[id] || "z.ai ping", "", "")).join("");
  verdict.style.display = "none";
  panel.classList.add("open");
  try {
    const d = await api("/api/diagnostics");
    rows.innerHTML = d.checks.map(c => {
      const title = DIAG_TITLES[c.id] || `z.ai ping · ${c.model || "glm-5.3-flash"}`;
      const why = c.status === "pass" ? (DIAG_SUBS[c.id] || c.detail) : c.detail;
      const ms = !c.ms ? "" : c.status === "fail" && c.ms >= 7500 ? "timeout" : `${c.ms} ms`;
      return diagRow(c.status, title, why, ms);
    }).join("");
    const failed = d.checks.find(c => c.status === "fail");
    verdict.className = "verdict " + (d.ok ? "go" : "off");
    verdict.innerHTML = d.ok ? "GO · all 3 checks passed"
      : `OFF · ${esc(DIAG_NAMES[failed?.id] || "check")} failed` +
        `<small>${esc(d.demo_mode && failed?.id === "key"
          ? "app still serves pages — replies are canned demo responses"
          : "fix the failing check before relying on live results")}</small>`;
    verdict.style.display = "";
    diagPill(d.ok ? "go" : "off", d.ok ? "GO" : "OFF");
  } catch {
    rows.innerHTML = "";
    verdict.className = "verdict off";
    verdict.innerHTML = "OFF · app server unreachable" +
      "<small>the app server itself did not answer — is it running?</small>";
    verdict.style.display = "";
    diagPill("off", "OFF");
  }
  diagRunning = false;
}

// --- live concurrency (the pill's trailing number): GET /api/metrics -----------
/* z.ai requests in flight right now, measured at the app's single HTTP
   choke point. Shows "n / limit" when ZAI_CONCURRENCY_LIMIT is configured;
   turns amber after a recent 429 or when the limit is reached. The same
   payload carries the current model pair, so the pull-down's context line
   (intake · research) follows swaps on every open page within one poll. */
let diagDataDir = "";

function paintCtx(intake, research) {
  const cx = $("diagCtx");
  if (cx && intake && research)
    cx.textContent = (diagDataDir ? `data dir: ${diagDataDir} · ` : "") +
                     `intake: ${intake} · research: ${research}`;
}

function applyHealthCtx(h) {
  if (h && h.data_dir) diagDataDir = h.data_dir;
  paintCtx(h && h.intake_model, h && h.research_model);
}

function paintConc(m) {
  const el = $("concLabel");
  if (!el) return;
  el.textContent = m.limit ? `${m.inflight} / ${m.limit}` : `${m.inflight}`;
  const hot = (m.last_limit_hit && m.last_limit_hit.ago_s < 30) ||
              (m.limit != null && m.inflight >= m.limit);
  el.classList.toggle("warn", !!hot);
  el.title = hot ? "AI service at capacity — new requests show a graceful retry notice"
                 : "z.ai requests in flight right now";
  paintCtx(m.intake_model, m.research_model);
}
async function pollConc() {
  try { paintConc(await api("/api/metrics")); } catch { /* transient */ }
}

async function siteHeader() {
  const host = $("sitenav");
  if (!host) return;
  let eff = {}, demo = null;
  try { eff = (await api("/api/features")).effective; } catch { /* show all */ }
  const links = NAV.filter(([, , flag]) => !flag || eff[flag] !== false)
    .map(([href, label]) => {
      const active = location.pathname === href ||
        (href !== "/" && location.pathname.startsWith(href)) ||
        (href === "/" && location.pathname === "/index.html") ? " class=\"active\"" : "";
      return `<a href="${href}"${active}>${label}</a>`;
    }).join("");
  host.innerHTML = `<header class="site"><div class="wrap">
    <a class="logo" href="/">🛡️ ScamShield</a>
    <nav>${links}</nav>
    <span class="spacer"></span>
    <span class="diagwrap">
      <button class="diag" id="diagBtn" data-state="idle"
              aria-label="System status and live AI call count — click to run diagnostics">
        <span class="beacon"></span><span id="diagLabel">···</span>
        <span class="diag-div" aria-hidden="true"></span><span id="concLabel" class="conc">–</span>
      </button>
      <div class="diag-panel" id="diagPanel" role="status">
        <h3>System check <button id="diagClose" aria-label="Close">✕</button></h3>
        <div id="diagRows"></div>
        <div class="verdict" id="diagVerdict" style="display:none"></div>
        <div class="ctx" id="diagCtx"></div>
      </div>
    </span>
    <span class="mode-chip" id="modeChip" style="display:none"></span>
  </div></header>`;
  const diagBtn = $("diagBtn");
  if (diagBtn) {
    diagBtn.addEventListener("click", runDiag);
    $("diagClose").addEventListener("click", e => {
      e.stopPropagation(); $("diagPanel").classList.remove("open");
    });
    document.addEventListener("click", e => {
      if (!e.target.closest(".diagwrap")) $("diagPanel").classList.remove("open");
    });
    runDiag();  // auto-run once per page load (approved default)
  }
  pollConc();                       // live concurrency number…
  setInterval(pollConc, 3000);      // …refreshed every 3 s
  try {
    const h = await api("/api/health");
    const chip = $("modeChip");
    if (chip) {
      chip.textContent = h.demo_mode ? "demo mode" : "live · z.ai";
      chip.className = "mode-chip" + (h.demo_mode ? " demo" : "");
      chip.style.display = "";
    }
    applyHealthCtx(h);
    document.dispatchEvent(new CustomEvent("health", {detail: h}));
  } catch { /* ignore */ }
}

document.addEventListener("DOMContentLoaded", siteHeader);

// --- footer -------------------------------------------------------------------
function siteFooter() {
  const host = $("sitefooter");
  if (!host) return;
  host.innerHTML = `<footer class="site"><div class="wrap">
    <span>ScamShield demo · research assistance, not legal or financial advice. Verdicts are evidence snapshots, not certificates of safety.</span>
    <span><a href="/">Home</a> · <a href="/models">Models</a> · <a href="/theme">Theme</a></span>
  </div></footer>`;
}
document.addEventListener("DOMContentLoaded", siteFooter);
