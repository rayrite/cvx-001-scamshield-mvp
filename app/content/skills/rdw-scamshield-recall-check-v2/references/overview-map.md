# Overview Map — geocode-accurate U.S. location mapping (optional post-processing)

Post-processing at consolidation: when findings name U.S. locations (outbreak case counts by city/state, distribution states, incident reports, manufacturing sites), build a location table, geocode it, and render an interactive map. **Default ON during beta testing** (`overview_map: true`); toggle via `recall-check.config.json`. In-chat override ("no map this run" / "map this run") always honored for that run and recorded in the report meta.

**v2 layer:** the rendered artifact is a **modular, embeddable component** — one self-contained HTML file that works standalone (double-click) AND drops into a host app (chat-style UI) three ways: iframe, custom element, or direct API. All styles are scoped; the data contract is the location-table JSON schema (unchanged); layout is responsive across desktop and mobile. Rendering logic depends on nothing from the skill, the report, or the sibling CSV/JSON files.

## Binding requirements (the feature spec — follow verbatim)

1. **Real coordinates on a real basemap, never a generated illustration.** Rendering is Plotly `scattergeo` with `scope:"usa"` (pinned plotly.js 2.35.2 from CDN in the hand-authored HTML file) — Leaflet/OpenStreetMap or Mapbox are acceptable equivalents; **image-generation models are never used for maps.**
2. **Location table first.** The map is a rendering of the table, nothing more. Schema, one row per location:

   | Column | Content |
   |---|---|
   | `raw_text` | The location exactly as the source stated it ("Detroit, MI", "statewide Michigan", "Fresno plant") |
   | `locality` | Normalized city/place name, or empty for state-only rows |
   | `admin1` | State (2-letter code or name) |
   | `county` | County when known (geocoder or source) |
   | `lat`, `lon` | Numeric, or **null** on geocode failure — the row stays, the pin doesn't exist |
   | `geocode_method` | `source_stated` · `nominatim` · `census` · `model_knowledge` · `state_centroid` · `failed` · `ambiguous` |
   | `geocode_precision` | `address` · `place` · `county` · `metro` · `state` · `non_us` |
   | `event_type` | `confirmed_case` · `suspected_case`/`probable_case` · `distribution` · `manufacturing`/`origin` · `retail` · `other` |
   | `n_cases` | Integer case count when stated, else null |
   | `source_citation` | Which finding/URL supplied this row |
   | `confidence` | `high` (T1–T3 geocode) · `medium` (T4) · `low` (ambiguous/failed) |
   | `notes` | Merge history, ambiguity flags, anything the reader needs |

3. **Normalization rules.** A city mention ("Detroit, MI") pins **on the city**, never the state centroid. A state-only mention ("cases in Michigan") gets a **state-level marker — never a fake city pin**. Metro mentions ("Detroit metro area") stay **metro precision** (city-center pin, `geocode_precision: metro`, noted). **Non-U.S. sites are listed separately in the table and never plotted.** Duplicate mentions of the same locality+state+event_type **dedupe into one marker sized by summed case count** (raw variants preserved in `notes`). **Ambiguous place names** (multi-state cities with no state context) are **omitted from the map and flagged** in the table (`geocode_method: ambiguous`, lat/lon null).
4. **Rendering — modular, decoupled, responsive.** The HTML artifact is a **dual-mode component**:
   - **Standalone mode:** opening the file directly renders the map from the inline `<script type="application/json" id="recall-map-data">` payload. Zero setup, any browser.
   - **Embed modes (host app):** (a) `<iframe src="..._map.html">` — optionally with `?src=<url>` to fetch the location JSON at runtime instead of the inline copy; (b) custom element `<recall-overview-map data-json="…">` or `<recall-overview-map src="…json">` after including the file's script; (c) imperative API `RecallOverviewMap.create(container, rows, options)`.
   - **Scoped styles:** every rule lives under the `.recall-map-embed` root class; no bare `body`/`h3`/`p` selectors leak into the host. Theming via CSS custom properties (`--rm-surface`, `--rm-text`, `--rm-muted`, `--rm-border`, `--rm-accent`, `--rm-chip-bg`, `--rm-plot-land`, `--rm-plot-subunit`, `--rm-plot-lake`) with `prefers-color-scheme: dark` defaults; a host overrides the properties (or pins `.recall-map-embed--light` / `--dark`) to match its own chat theme.
   - **Responsive:** width 100% of container; plot height derives from `aspect-ratio` (clamped 320–640px); a `ResizeObserver` keeps Plotly sized; text labels default OFF below ~700px container width (a "Labels" toggle restores them) because dense state labels collide on small plots; markers get larger minimum sizes on coarse pointers (touch).
   - Marker **size by case count**; **color by event_type**; shape distinguishes precision (circles = place-level, diamonds = state-level, label suffixed `*`). **Hover** shows locality/state, n_cases, event_type. **Title**: `<product/recall name> · reported U.S. locations · as of YYYY-MM-DD`. **Caption, verbatim**: `Markers are plotted from geocoded coordinates in the location table, not from a generated illustration.`
5. **Outputs: BOTH** the interactive HTML map **AND** the location table in **CSV and JSON**. All three artifacts, always together. The HTML's inline JSON and the `_locations.json` file carry identical rows — the file pair is the decoupling seam (a host can re-render the component from the JSON alone, without the generated HTML).
6. **Geocode failure is a kept row**: lat/lon null, no pin, never an invented coordinate. CDN failure is a **disclosed error card**, never a blank div: the component states that the map library failed to load and that the data remains available in the CSV/JSON table.

## Configuration

`recall-check.config.json` (JSON; looked up in the working directory first, then the skill directory):

```json
{ "overview_map": true }
```

Absent file → default `true` (beta behavior; intended long-term default may flip to off — the config file is the stable interface). In-chat override wins for the current run only.

## Pipeline

1. **Extract** every U.S. location the findings name, with its event_type, n_cases (when stated), and source_citation. Sources that carry geography: CDC investigation pages (case counts by state, sometimes city), agency notices (distribution lists), state pages, press reports. A distribution-state list with no counts is still mappable (diamonds, n_cases null).
2. **Normalize + dedupe** into table rows (rules above).
3. **Geocode** in tier order (below). One request per unique locality per run — cache; Nominatim max 1 request/second.
4. **Render** HTML + CSV + JSON (templates below). The generated HTML gets `{{TITLE}}`/`{{AS_OF}}` baked into `data-title`/`data-as-of` attributes on the root element and the same rows inlined into `#recall-map-data`.
5. **Verify** the render (below) at **both a desktop and a mobile viewport**. Fix and re-render on failure — never ship an unverified map silently.
6. **Reference all three artifacts** in the report's Overview Map section: paths, row counts, geocode-method summary, and every flagged/omitted row.

## Geocode tiers (in order)

- **T1 `source_stated`** — coordinates printed in the source. Use as-is; confidence high.
- **T2 `nominatim`** — live place geocode, the default for cities/counties:
  `GET https://nominatim.openstreetmap.org/search?q=<urlencoded "locality, admin1">&format=json&limit=1&addressdetails=1&countrycodes=us` with header `User-Agent: rdw-scamshield-recall-check/1.0 (research skill; contact: local)` (Nominatim requires a meaningful UA; without it requests are refused). Take `lat`/`lon`; `county` from `address.county`; precision from `addresstype` (city/town/village → `place`; municipality/county → `county`). A city pin lands on the city, not the state centroid — verified: Detroit, MI → 42.3316, -83.0466, Wayne County.
- **T3 `census`** — street addresses (plants, facilities):
  `GET https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress?benchmark=Public_AR_Current&format=json&address=<urlencoded address>` (the `benchmark` parameter is **required** — omitting it returns HTTP 400). Precision `address`. Verified: 4600 Silver Hill Rd, Suitland MD → -76.9284, 38.8451.
- **T4 `model_knowledge`** — fallback ONLY when live lookup fails, ONLY for major unambiguous cities (top-100 US, state context present). `geocode_method: model_knowledge`, confidence **medium max**, noted in `notes`. An ambiguous name without state context is NOT T4-eligible → `ambiguous`, null, no pin.
- **State-only mentions** → `state_centroid` from a fixed state-centroid lookup (Census centers of population). Rendered as the **diamond** marker with an asterisk-suffixed label; `geocode_precision: state`; **never** dressed up as a city.
- **Failure** → `geocode_method: failed`, lat/lon null, `notes: geocode_failed: <reason>`, confidence low, row kept, no pin.

## HTML template (v2 component)

Emit this file as `recall-check_<slug>_<YYYY-MM-DD>_map.html`, replacing `{{TITLE}}`, `{{AS_OF}}`, and `{{LOCATIONS_JSON}}` (a JSON array of table rows; only rows with non-null lat/lon and `geocode_precision` ≠ `non_us` are plotted — the rest live in the CSV/JSON table and the on-card count line). The script tag's integrity hash is computed for plotly-2.35.2.min.js exactly (sha384, base64) — if the pinned version ever changes, recompute the hash; a stale hash silently breaks every map.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{TITLE}} — reported U.S. locations</title>
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"
        integrity="sha384-cCVCZkAjYNxaYKbM8lsArLznDF/SvMFr1jcZrvOpSTCa0W40ZAdLzHCEulnUa5i7"
        crossorigin="anonymous"></script>
<style>
  /* Page shell — standalone mode only; inert when the component is embedded. */
  html { height: 100%; }
  body {
    margin: 0; min-height: 100%; padding: clamp(8px, 2vw, 16px);
    background: #f6f7f9; display: flex; align-items: flex-start; justify-content: center;
  }
  @media (prefers-color-scheme: dark) { body { background: #0f1115; } }

  /* ============================================================
     recall-map-embed — self-contained component styles.
     Everything is scoped under .recall-map-embed; hosts can restyle
     by overriding the --rm-* custom properties on the root.
     ============================================================ */
  .recall-map-embed {
    /* theme tokens (light defaults) */
    --rm-surface: #ffffff;
    --rm-text: #1c2430;
    --rm-muted: #5b6470;
    --rm-border: #d9dee5;
    --rm-accent: #2c7fb8;
    --rm-chip-bg: #eef1f5;
    --rm-plot-land: #f0f0f0;
    --rm-plot-subunit: #c8cdd4;
    --rm-plot-lake: #e8f4fb;
    --rm-focus: #2c7fb8;
    /* layout tokens */
    --rm-radius: 10px;
    --rm-pad: clamp(10px, 2vw, 16px);
    box-sizing: border-box;
    display: block;
    width: 100%;
    max-width: 1040px;
    margin-inline: auto;
    padding: var(--rm-pad);
    background: var(--rm-surface);
    color: var(--rm-text);
    border: 1px solid var(--rm-border);
    border-radius: var(--rm-radius);
    font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    -webkit-text-size-adjust: 100%;
  }
  @media (prefers-color-scheme: dark) {
    .recall-map-embed:not(.recall-map-embed--light) {
      --rm-surface: #16181d;
      --rm-text: #e8eaee;
      --rm-muted: #9aa2ad;
      --rm-border: #2c313a;
      --rm-accent: #66b0da;
      --rm-chip-bg: #22262e;
      --rm-plot-land: #242932;
      --rm-plot-subunit: #3c434f;
      --rm-plot-lake: #1d242c;
      --rm-focus: #66b0da;
    }
  }
  .recall-map-embed * { box-sizing: border-box; }

  .recall-map-embed__head {
    display: flex; flex-wrap: wrap; gap: 4px 12px;
    align-items: baseline; justify-content: space-between;
    margin-bottom: 8px;
  }
  .recall-map-embed__title {
    margin: 0;
    font-size: clamp(14px, 2.4vw, 17px);
    font-weight: 650; line-height: 1.35;
    overflow-wrap: anywhere;
  }
  .recall-map-embed__count {
    color: var(--rm-muted);
    font-size: clamp(12px, 1.8vw, 13px);
    white-space: nowrap;
  }

  /* Responsive plot area: width-driven height, clamped for chat cards. */
  .recall-map-embed__plot {
    width: 100%;
    aspect-ratio: 4 / 3;
    min-height: 320px;
    max-height: 640px;
    border-radius: 6px;
    overflow: hidden;
  }
  @media (max-width: 480px) {
    .recall-map-embed__plot { aspect-ratio: 1 / 1; min-height: 300px; }
  }

  .recall-map-embed__foot {
    display: flex; flex-wrap: wrap; gap: 6px 12px;
    align-items: center; margin-top: 8px;
  }
  .recall-map-embed__toggle {
    appearance: none; -webkit-appearance: none;
    font: inherit; font-size: 12.5px;
    color: var(--rm-text); background: var(--rm-chip-bg);
    border: 1px solid var(--rm-border); border-radius: 999px;
    padding: 5px 12px; cursor: pointer;
    min-height: 32px; /* touch target */
  }
  .recall-map-embed__toggle[aria-pressed="true"] {
    border-color: var(--rm-accent); color: var(--rm-accent);
  }
  .recall-map-embed__toggle:focus-visible { outline: 2px solid var(--rm-focus); outline-offset: 2px; }
  .recall-map-embed__caption {
    flex: 1 1 260px; margin: 0;
    color: var(--rm-muted); font-size: 12.5px; line-height: 1.45;
  }
  .recall-map-embed__error {
    margin: 8px 0 0; padding: 10px 12px;
    border: 1px solid var(--rm-border); border-radius: 6px;
    background: var(--rm-chip-bg); color: var(--rm-muted);
    font-size: 13px; line-height: 1.5;
  }
</style>
</head>
<body>
<!-- Component root. data-title / data-as-of drive the card heading;
     data-json is only read by the auto-mount in standalone mode. -->
<div class="recall-map-embed" id="recall-map-auto" role="region"
     aria-label="{{TITLE}} — reported U.S. locations map"
     data-title="{{TITLE}}" data-as-of="{{AS_OF}}"></div>

<script type="application/json" id="recall-map-data">{{LOCATIONS_JSON}}</script>

<script>
/* ============================================================
   recall-overview-map component (framework-free, no build step).
   Mount paths:
     1. Standalone: auto-mounts into #recall-map-auto from
        #recall-map-data (inline JSON) or ?src=<url> (fetched JSON).
     2. Custom element: <recall-overview-map data-json="…"
        title="…" as-of="…"> or <recall-overview-map src="…json">.
     3. Imperative: RecallOverviewMap.create(el, rows, opts)
        → returns { setData, setLabels, destroy }.
   Requires window.Plotly (the standalone page loads it; hosts
   embedding the element must include plotly.js themselves or
   use the iframe path). Data contract: the _locations.json row
   schema in overview-map.md.
   ============================================================ */
(() => {
  "use strict";

  const EVENT_COLORS = {
    confirmed_case: "#c0392b", suspected_case: "#e67e22", probable_case: "#e67e22",
    distribution: "#2c7fb8", manufacturing: "#7d3c98", origin: "#7d3c98",
    retail: "#16a085", other: "#5d6d7e"
  };
  const CAPTION = "Markers are plotted from geocoded coordinates in the location table, not from a generated illustration.";
  const LABEL_BREAKPOINT = 700; // px of container width

  const coarse = typeof matchMedia === "function" &&
    matchMedia("(pointer: coarse)").matches;

  const clampSize = n => {
    const base = n == null ? (coarse ? 13 : 10) : NaN;
    const min = coarse ? 11 : 8;
    return n == null ? base : Math.max(min, Math.min(30, 6 + Math.sqrt(n) * 4));
  };

  const label = r => (r.locality ? r.locality : r.admin1) +
    (r.geocode_precision === "state" ? "*" : "");

  const hover = r => [
    r.raw_text,
    r.n_cases == null ? "count not stated" : r.n_cases + " case(s)",
    r.event_type, r.geocode_precision
  ].join("<br>");

  const cssVar = (root, name, fallback) => {
    const v = getComputedStyle(root).getPropertyValue(name).trim();
    return v || fallback;
  };

  const debounce = (fn, ms) => {
    let t; return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); };
  };

  function buildDom(root, opts) {
    root.innerHTML = "";
    const head = document.createElement("div");
    head.className = "recall-map-embed__head";
    const h = document.createElement("h3");
    h.className = "recall-map-embed__title";
    h.textContent = opts.title + " · reported U.S. locations · as of " + opts.asOf;
    const count = document.createElement("span");
    count.className = "recall-map-embed__count";
    head.append(h, count);
    const plot = document.createElement("div");
    plot.className = "recall-map-embed__plot";
    const foot = document.createElement("div");
    foot.className = "recall-map-embed__foot";
    const toggle = document.createElement("button");
    toggle.type = "button";
    toggle.className = "recall-map-embed__toggle";
    toggle.setAttribute("aria-pressed", "true");
    const cap = document.createElement("p");
    cap.className = "recall-map-embed__caption";
    cap.textContent = CAPTION;
    foot.append(toggle, cap);
    root.append(head, plot, foot);
    return { count, plot, toggle };
  }

  function create(container, rows, options = {}) {
    if (!container) throw new Error("RecallOverviewMap.create: container required");
    const root = container.classList && container.classList.contains("recall-map-embed")
      ? container
      : wrap(container);
    const opts = {
      title: options.title || root.dataset.title || "Recall check",
      asOf: options.asOf || root.dataset.asOf || "",
      showLabels: options.showLabels
    };
    const ui = buildDom(root, opts);
    let current = Array.isArray(rows) ? rows.slice() : [];
    let showLabels = opts.showLabels != null ? !!opts.showLabels
      : (root.clientWidth || 800) >= LABEL_BREAKPOINT;
    let userToggled = opts.showLabels != null;

    function plotRows() {
      return current.filter(r => r.lat != null && r.lon != null &&
        r.geocode_precision !== "non_us");
    }

    function render() {
      if (typeof window.Plotly === "undefined") { renderCdnError(); return; }
      const plotted = plotRows();
      const traces = [];
      for (const et of [...new Set(plotted.map(r => r.event_type))]) {
        const rs = plotted.filter(r => r.event_type === et);
        traces.push({
          type: "scattergeo",
          mode: showLabels ? "markers+text" : "markers",
          name: et,
          textposition: "top center", textfont: { size: 9 },
          lat: rs.map(r => r.lat), lon: rs.map(r => r.lon),
          text: rs.map(label), hovertext: rs.map(hover), hoverinfo: "text",
          marker: {
            size: rs.map(r => clampSize(r.n_cases)),
            symbol: rs.map(r => r.geocode_precision === "state" ? "diamond" : "circle"),
            color: EVENT_COLORS[et] || EVENT_COLORS.other,
            line: { color: "#ffffff", width: 1 }
          }
        });
      }
      const listed = current.length - plotted.length;
      ui.count.textContent = plotted.length + " plotted location" +
        (plotted.length === 1 ? "" : "s") +
        (listed > 0 ? " · " + listed + " listed without coordinates" : "");
      ui.toggle.hidden = false;
      ui.toggle.textContent = "Labels: " + (showLabels ? "on" : "off");
      ui.toggle.setAttribute("aria-pressed", String(showLabels));
      Plotly.react(ui.plot, traces, {
        font: { color: cssVar(root, "--rm-text", "#1c2430"), size: 12 },
        paper_bgcolor: "transparent", plot_bgcolor: "transparent",
        margin: { t: 30, l: 6, r: 6, b: 6 },
        legend: { orientation: "h", font: { size: 11 } },
        hoverlabel: {
          bgcolor: cssVar(root, "--rm-surface", "#ffffff"),
          bordercolor: cssVar(root, "--rm-border", "#d9dee5"),
          font: { color: cssVar(root, "--rm-text", "#1c2430") }
        },
        geo: {
          scope: "usa", projection: { type: "albers usa" },
          showland: true, landcolor: cssVar(root, "--rm-plot-land", "#f0f0f0"),
          subunitcolor: cssVar(root, "--rm-plot-subunit", "#c8cdd4"),
          countrycolor: cssVar(root, "--rm-plot-subunit", "#c8cdd4"),
          showlakes: true, lakecolor: cssVar(root, "--rm-plot-lake", "#e8f4fb")
        }
      }, { responsive: true });
    }

    function renderCdnError() {
      ui.plot.style.display = "none";
      ui.toggle.hidden = true;
      ui.count.textContent = "";
      const err = document.createElement("p");
      err.className = "recall-map-embed__error";
      err.textContent = "The map library (plotly.js) could not be loaded from its CDN. " +
        "No coordinates were invented to compensate — the full location table remains " +
        "available in the _locations.csv and _locations.json artifacts.";
      root.querySelector(".recall-map-embed__foot").before(err);
    }

    ui.toggle.addEventListener("click", () => {
      userToggled = true;
      showLabels = !showLabels;
      render();
    });

    const onResize = debounce(() => {
      if (typeof window.Plotly !== "undefined" && ui.plot.style.display !== "none") {
        Plotly.Plots.resize(ui.plot);
      }
      if (!userToggled) {
        const want = (root.clientWidth || 800) >= LABEL_BREAKPOINT;
        if (want !== showLabels) { showLabels = want; render(); }
      }
    }, 150);
    let ro = null;
    if (typeof ResizeObserver === "function") {
      ro = new ResizeObserver(onResize);
      ro.observe(root);
    } else if (typeof window.addEventListener === "function") {
      window.addEventListener("resize", onResize);
    }

    render();

    return {
      setData(rows2) { current = Array.isArray(rows2) ? rows2.slice() : []; render(); },
      setLabels(on) { userToggled = true; showLabels = !!on; render(); },
      destroy() {
        if (ro) ro.disconnect();
        else window.removeEventListener("resize", onResize);
        if (typeof window.Plotly !== "undefined") Plotly.purge(ui.plot);
        root.innerHTML = "";
      }
    };
  }

  function wrap(container) {
    const el = document.createElement("div");
    el.className = "recall-map-embed";
    if (container.dataset && container.dataset.title) el.dataset.title = container.dataset.title;
    if (container.dataset && container.dataset.asOf) el.dataset.asOf = container.dataset.asOf;
    container.innerHTML = "";
    container.appendChild(el);
    return el;
  }

  function showError(target, message) {
    const root = target || document.body;
    const p = document.createElement("p");
    p.className = "recall-map-embed__error";
    p.style.maxWidth = "1040px";
    p.textContent = message;
    root.appendChild(p);
  }

  /* Custom element: <recall-overview-map src="…json" | data-json="…"
     title="…" as-of="…"></recall-overview-map> */
  class RecallOverviewMapElement extends HTMLElement {
    connectedCallback() {
      if (this._api) return;
      this.style.display = "block";
      const inline = this.getAttribute("data-json");
      const src = this.getAttribute("src");
      const mount = rows => {
        this._api = create(this, rows, {
          title: this.getAttribute("title"),
          asOf: this.getAttribute("as-of")
        });
      };
      if (inline) {
        try { mount(JSON.parse(inline)); }
        catch (e) { showError(this, "recall-overview-map: invalid data-json — " + e.message); }
      } else if (src) {
        fetch(src).then(r => {
          if (!r.ok) throw new Error("HTTP " + r.status);
          return r.json();
        }).then(mount).catch(e =>
          showError(this, "recall-overview-map: could not load " + src + " — " + e.message));
      } else {
        showError(this, "recall-overview-map: provide data-json or src");
      }
    }
    disconnectedCallback() {
      if (this._api) { this._api.destroy(); this._api = null; }
    }
  }
  if (typeof customElements !== "undefined" &&
      !customElements.get("recall-overview-map")) {
    customElements.define("recall-overview-map", RecallOverviewMapElement);
  }

  /* Standalone auto-mount: inline #recall-map-data, else ?src=<url>. */
  function autoMount() {
    const root = document.getElementById("recall-map-auto");
    if (!root) return;
    const dataEl = document.getElementById("recall-map-data");
    if (dataEl) {
      try { create(root, JSON.parse(dataEl.textContent)); }
      catch (e) { showError(root, "Invalid inline location JSON — " + e.message); }
      return;
    }
    const src = new URLSearchParams(location.search).get("src");
    if (src) {
      fetch(src).then(r => {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.json();
      }).then(rows => create(root, rows))
        .catch(e => showError(root, "Could not load location table from " + src + " — " + e.message));
    }
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", autoMount);
  } else {
    autoMount();
  }

  window.RecallOverviewMap = { create };
})();
</script>
</body>
</html>
```

Design notes: one trace per event_type (legend = event types, fixed colors); per-point `symbol` arrays distinguish state-level diamonds (asterisk-suffixed labels) from place-level circles; `albers usa` insets AK/HI natively. The plot container's height comes from `aspect-ratio` (4/3 desktop, 1/1 under 480px) so it derives from actual rendered width in any host column — fixed heights cropped viewports in v1 testing; `min/max-height` clamp it for chat cards. `ResizeObserver` (window-resize fallback) re-syncs Plotly and auto-flips the label default across the 700px breakpoint until the user toggles manually (`userToggled` latches). Coarse-pointer media query bumps minimum marker sizes for touch. `Plotly.react` (not `newPlot`) so `setData` re-renders in place for host apps. If per-point symbol arrays ever fail to render (verify step catches it), fallback: split each event_type into two traces (place/state) with fixed symbols — same data, legend names suffixed "(state)".

## Embedding guide (for the host app)

The component is decoupled from the skill and from the sibling artifacts; the data contract is the `_locations.json` row schema alone.

| Path | How | Notes |
|---|---|---|
| iframe | `<iframe src="…_map.html" style="width:100%;height:640px;border:0" title="…"></iframe>` | strongest isolation; the file is self-sufficient. For live data, serve `…_map.html?src=…_locations.json` and drop the inline JSON payload at generation time |
| custom element | include the component script + plotly.js, then `<recall-overview-map src="…_locations.json" title="…" as-of="…"></recall-overview-map>` | `data-json="<escaped json>"` works without a fetch; element cleans up on disconnect |
| imperative | `const api = RecallOverviewMap.create(el, rows, {title, asOf, showLabels})` | `api.setData(rows)`, `api.setLabels(bool)`, `api.destroy()` — fits React/Vue/Svelte effects |

Theming: set the `--rm-*` custom properties on `.recall-map-embed` (or a wrapper) to match the host chat theme; force light with the `recall-map-embed--light` class. The component never loads fonts or makes network requests beyond Plotly (CDN, SRI-pinned) and an optional `src` fetch — safe behind a CSP that allows `cdn.plot.ly`.

## CSV and JSON outputs

`_locations.csv` — header row + all table rows (including null-lat/lon, ambiguous, and non-US rows), UTF-8, comma-separated, quoting as needed.
`_locations.json` — a JSON array of row objects with the exact schema above. These are outputs of record: the CSV/JSON is the data; the HTML is its rendering.

## Render verification (mandatory before delivery)

1. Open the generated HTML in browser tooling: **chrome-devtools MCP `new_page` with the `file:///` URL**. (Do NOT use agent-browser MCP for local file URLs — it hangs in this environment.)
2. **Desktop pass:** resize to ≥1300×800, reload, confirm: basemap renders, AK/HI insets present, expected markers visible, diamond/circle distinction where applicable, legend lists event types, caption verbatim, count line matches row math.
3. **Mobile pass:** resize to ~390×844, reload, confirm: no horizontal page scroll, card fits the viewport, plot visible at the 1/1 aspect, labels default OFF (when >~10 short labels would collide), the Labels toggle flips them on and re-renders, legend and caption still visible.
4. Confirm the component API is live: `RecallOverviewMap.create` exists and `customElements.get("recall-overview-map")` is defined (hosts depend on both).
5. On any failure: fix (payload or template), re-render, re-verify.
6. If no browser tooling is available in the session: verify statically (JSON parses; schema conforms; coordinates in plausible US ranges; every plotted row has non-null lat/lon; caption and title exact) and **say in the report that visual verification was not performed**.

## Skips and honesty

- No U.S. locations in the findings → report states "no mappable U.S. locations surfaced; map not rendered" — never a map with nothing to plot, never a decorative pin.
- Map disabled by config/override → report states that, and that the run can be re-done with it on.
- Rows with null lat/lon, ambiguous flags, and non-US rows are summarized in the report's Overview Map section, not silently dropped.
- Case counts are only what sources state — `n_cases` is never estimated, and marker size flows from it (or defaults when null).
