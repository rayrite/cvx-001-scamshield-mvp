# Design: `rdw-product-dig`

Created 2026-09-19, retroactively — this skill predates the workspace's DESIGN.md convention, so its original rationale lives implicitly in SKILL.md's structure: staged prospect → dig → consolidate research over 12 product veins, the ripeness gauge as the gate's price tag (later ported to the whole scamshield/corpcheck family), and the research ledger as the multi-session state container. This file is the landing spot for changes from here on.

## Output modes (2026-09-19)

**Trigger:** user requirement — the staged-research skills will roll into a chat-GPT-style app where an end-user prompt triggers research. The app needs each stage's full content printable to the chat output (not just highlights), the end user gets to choose, and the backend developer must be able to flip the default on demand (file for a debugging session, chat for a production release) without editing skill prose.

1. **Three modes, one knob.** `file` (default — current behavior untouched: highlight summaries in chat, full cumulative report in the markdown file) · `chat` (complete stage content prints to the chat response; no file unless requested) · `both` (chat content + file maintained). Applied identically across all four staged skills (this one, rdw-scamshield-check-v2, rdw-scamshield-recall-check-v2, rdw-scamshield-tea2-corpcheck).
2. **Three precedence levels.** The user's in-chat choice (any time, sticks for the check, noted in report meta) > the per-skill config file (`product-dig.config.json` here; `"output_mode"` field; absent file/field = default) > the one-line default baked into SKILL.md's Inputs bullet — so embedding the prompt in an app and editing that line is also a valid default flip. This mirrors and generalizes recall-check's `overview_map` config precedent.
3. **"Full stage content" defined once, family-wide:** stage banner; *every* finding recorded that stage with its complete citation (no 3–6 highlight cap); executive overview/verdict box(es); vein/coverage map; ripeness gauge with legend; the stage's **ledger delta** (queries run, new finding IDs, lead-pool changes — the cumulative ledger is never reprinted per stage); the plan. Consolidation in `chat`/`both` delivers the full final report to chat.
4. **The `chat` trade-off is named, not hidden:** no file = no ledger to resume from after a session break. Surfaced at intake when the user picks `chat`; `both` is the long-dig-safe option.

**Files changed:** SKILL.md (key-concepts bullet, Inputs bullet, steps 5/7/12/13, output-contract modes block, session-resume failure rule). No config file is shipped — the developer writes `product-dig.config.json` into the working directory when they want a non-default mode; absent = `file`.

**Untested live** — first exercised when the app integration runs or a user says "in chat" on a real dig.
