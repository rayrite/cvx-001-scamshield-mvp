"""Universal Design Language (UDL) — one config file themes every page.

udl.json (app root) holds the design tokens; every page links /udl.css and
loads /udl.js (both generated here from the config). Editing the file — or
POSTing to /api/udl from the /theme page — restyles the whole site on the
next page load. Tokens intentionally use the same custom-property names the
original pages already used, so adopting the UDL was a palette swap, not a
rewrite.

Light adjustments only: colors, fonts, radius, shadow strength, and the
light/dark/auto mode. Layout is not themeable from here.
"""
from __future__ import annotations

import json
import threading
from pathlib import Path

UDL_FILE = Path(__file__).parent / "udl.json"

DEFAULT: dict = {
    "name": "ScamShield House",
    "mode": "auto",                      # auto | light | dark
    "colors": {
        "light": {
            "bg": "#f4f6f9", "card": "#ffffff", "ink": "#1b2430",
            "muted": "#5a6675", "line": "#dde3ea",
            "accent": "#0b5cad", "accent_ink": "#084a8c", "accent_soft": "#e8f1fa",
            "good": "#0c7a43", "good_soft": "#e3f4ea",
            "warn": "#8a5a00", "warn_soft": "#fdf3df",
            "bad": "#a12b12", "bad_soft": "#fbe9e3",
        },
        "dark": {
            "bg": "#0f141b", "card": "#161d27", "ink": "#e8edf3",
            "muted": "#9aa7b6", "line": "#263140",
            "accent": "#6db3ff", "accent_ink": "#9cc9ff", "accent_soft": "#12253a",
            "good": "#5ec98d", "good_soft": "#122a1d",
            "warn": "#e5b45c", "warn_soft": "#2d2413",
            "bad": "#f0917a", "bad_soft": "#33201a",
        },
    },
    "fonts": {
        "body": "system-ui, 'Segoe UI', Roboto, Arial, sans-serif",
        "heading": "system-ui, 'Segoe UI', Roboto, Arial, sans-serif",
        "mono": "ui-monospace, 'Cascadia Mono', Consolas, monospace",
    },
    "radius": "14px",
    "shadow": "0 1px 2px rgba(16,24,40,.06), 0 4px 14px rgba(16,24,40,.06)",
}

_lock = threading.Lock()


def _merge(base: dict, over: dict) -> dict:
    out = dict(base)
    for k, v in over.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _merge(out[k], v)
        else:
            out[k] = v
    return out


def load() -> dict:
    with _lock:
        if UDL_FILE.exists():
            try:
                return _merge(DEFAULT, json.loads(UDL_FILE.read_text(encoding="utf-8")))
            except (json.JSONDecodeError, OSError):
                pass
        return json.loads(json.dumps(DEFAULT))   # deep copy


def save(cfg: dict) -> dict:
    merged = _merge(load(), cfg)
    with _lock:
        UDL_FILE.write_text(json.dumps(merged, indent=2, ensure_ascii=False) + "\n",
                            encoding="utf-8")
    return merged


def _vars(colors: dict, fonts: dict, radius: str, shadow: str) -> str:
    c = colors
    return (
        f"--bg:{c['bg']};--card:{c['card']};--ink:{c['ink']};--muted:{c['muted']};"
        f"--line:{c['line']};--accent:{c['accent']};--accent-ink:{c['accent-ink' if 'accent-ink' in c else 'accent_ink']};"
        f"--accent-soft:{c['accent_soft']};--good:{c['good']};--good-soft:{c['good_soft']};"
        f"--warn:{c['warn']};--warn-soft:{c['warn_soft']};--bad:{c['bad']};--bad-soft:{c['bad_soft']};"
        f"--font-body:{fonts['body']};--font-heading:{fonts['heading']};--font-mono:{fonts['mono']};"
        f"--radius:{radius};--shadow:{shadow};"
    )


def css() -> str:
    """The stylesheet every page links. Mode semantics:
    auto     → follow the visitor's prefers-color-scheme
    light    → force light for everyone
    dark     → force dark for everyone
    Pages set <html data-mode="…"> via /udl.js; the CSS below works even if
    that script never runs (auto falls back to the media query)."""
    u = load()
    light = _vars(u["colors"]["light"], u["fonts"], u["radius"], u["shadow"])
    dark = _vars(u["colors"]["dark"], u["fonts"], u["radius"], u["shadow"])
    return f"""/* UDL — {u['name']} — generated from udl.json; edit via /theme or /api/udl */
:root{{{light}}}
@media (prefers-color-scheme: dark){{:root:not([data-mode="light"]){{{dark}}}}}
:root[data-mode="dark"]{{{dark}}}
body{{font-family:var(--font-body)}}
h1,h2,h3,h4{{font-family:var(--font-heading)}}
code,pre,.mono{{font-family:var(--font-mono)}}
"""


def js() -> str:
    u = load()
    mode = u.get("mode", "auto")
    if mode not in ("auto", "light", "dark"):
        mode = "auto"
    return (
        "/* UDL boot — sets the configured light/dark mode before first paint. */\n"
        f'(function(){{document.documentElement.dataset.mode="{mode}";'
        'window.UDL_NAME=' + json.dumps(u.get("name", "")) + ';})();\n'
    )
