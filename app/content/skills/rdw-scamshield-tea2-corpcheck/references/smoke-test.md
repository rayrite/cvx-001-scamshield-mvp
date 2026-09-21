# Smoke Test — fast identity, authenticity, and register checks before any research

The smoke test answers three questions in under a minute with **at most 2 network calls**: ① *who is the entity, really?* ② *if a URL was supplied, is it actually theirs?* ③ *is the company in the documented dark-patterns register?* A seasoned reader resolves "Tide → Procter & Gamble", spots `siriusxm-billing-payments[.]com` as not-siriusxm, and remembers the CFPB action — in seconds. This checklist makes that instinct explicit, fast, and rubric-anchored. It is modeled on the scamshield-check-v2 smoke architecture (static tells before external research) adapted for companies: the "material" is the user's input plus major-brand knowledge plus the corporate register.

## Rules

1. **≤2 network calls, total.** Identity searches for unfamiliar entities, or one passive fetch of a supplied URL — never both in quantity. No WHOIS, no subagents, no regulator sweeps. Anything needing more is not a smoke item — fall through to Stage 1. Zero calls is the norm for major brands.
2. **Three outcomes, two snap classes.** A **final snap** (impersonation tell — the supplied site is not the company's) ends the check early with a 🔴. A **register hit** produces a *snap preview* — never a final verdict, because the register is cutoff-dated, records no positives, and cannot show remediation. **Fall-through** proceeds to Stage 1 in the same turn.
3. **Major-brand knowledge only.** Website-authenticity items fire only when the claimed company is a major brand whose official domain is common knowledge (amazon.com, siriusxm.com, pg.com…). An unfamiliar company's "real" domain cannot be smoke-judged — resolve by search if the budget allows, otherwise fall through.
4. **Observed, not inferred.** An item fires only on content actually visible in the input or a fetched page. A blocked or unfetched page is a gap, never evidence.
5. **FP guards are part of the item.** An item fired without its guard satisfied is a false positive, not caution.
6. **Register lookups follow the register's own rules** (exact-entity match, parent chain, defunct flags, cutoff discipline) — see `corp-register.md`.

## Outcomes

- **Decisive authenticity item fires** → final snap verdict: **🔴 Not the company's real site — High confidence, labeled `snap`**. Deliver the ultra-short snap response (below). No searches, no report file; `document` offered at the gate.
- **Register hit** → snap preview response (below): identity line + register row + band preview labeled `register` + the not-current-status caveat + fast-path plan. Then the gate.
- **Neither** → one line in the Stage-1 response: "no documented record in the dark-patterns register — absence ≠ clean", then the full sweep. The smoke test must never make a thin record feel like an all-clear.

## Snap response shape — impersonation (the whole reply, ~10 lines)

```
> ## ⚠️ VERDICT: 🔴 Not <Company>'s real site — High confidence (snap)
> **Basis:** <item ID(s)> — <the domain fact, one line>
> **Do/don't:** type <official domain> yourself · never pay/log in via the link · report to <company abuse channel> + FTC (reportfraud.ftc.gov)

Checked in <N> seconds, zero searches — the domain itself settles it.
Say "document" for the archived report · "stop" to finish here.
```

## Snap preview shape — register hit (the whole reply, ~12 lines + plan)

```
> ## 📋 REGISTER PREVIEW: 🟠/🔴 zone — <Tier> documented record *(register, as of KB cutoff 2026-09-19)*
> **Entity:** <resolved company + parent chain + official domain>
> **On record:** <DP-IDs + one-line notes from the register row>
> **Caveat:** documented as of the cutoff — not current status. Remediation, newer actions, and positives are unchecked until Stage 1 runs.

NEXT STAGE (fast path, awaiting approval)
  1. [C2/C4] Current status of the documented matter(s) + anything newer than the cutoff
  2. [C8] Positives & reputation sweep (balance)
  3. [<line>] <one angle-priority line for the user's stated goal>

Reply "go" to run this plan · describe a different direction to customize · "stop" to consolidate the final report.
```

## Identity resolution items

- **C-I1 Known-major resolution** · zero calls — the entity is major-brand knowledge: canonical company, official domain, parent chain stated from knowledge (Tide → Procter & Gamble; Instagram → Meta). *Guard:* if two same-named majors could plausibly be meant ("Delta"), ask once or state the assumption — do not guess silently.
- **C-I2 Unfamiliar entity** · ≤2 searches — resolve `<name> company official site` and/or `<brand> parent company`; take the official domain from the company's own pages, not an aggregator's guess. If two calls don't settle it, state the best resolution as an assumption and let Stage 1's C1 confirm.
- **C-I3 Product/brand subject** — the brand names the product; the check targets the **parent company**, with brand-level findings attributed to the brand. Run the register lookup on both (lookup rule 2).

## Website authenticity items (only when the user supplied a URL)

- **C-W1 Brand-in-domain-but-not-the-brand** · **[Decisive]** — the domain contains a major brand's name but is not that brand's official domain (`<brand>-billing-payments.com`, `<brand>-account[.]net`). Anchor: brand-clone confirmation. *FP guards:* official domains and their country/support subdomains pass; regional official domains pass (verify by one search if genuinely uncertain — then it is not smoke-decisive); a domain with generic words only (shop, deals, billing) and no major-brand name is not this item.
- **C-W2 Lookalike/typosquat of a major domain** · **[Decisive]** — one-letter-off, hyphenated, or TLD-swapped variant of a major brand's domain (`amazor.com`, `sirius-xm.com`). Same anchor and same guards as C-W1.
- **C-W3 Identity-claim mismatch on fetch** · **[Decisive]** — one passive fetch of the supplied page shows it *claims* to be company B while the legal/footer/contact/checkout links point at an unrelated entity. *FP guards:* third-party resellers and authorized dealers exist — a page *selling* brand goods while honestly identifying itself is not this item (that's a Stage-1 reseller question); payment-processor domains at checkout are normal; only a claimed-identity ≠ actual-identity mismatch fires.
- **C-W4 Template-and-nothing-else storefront** · **[Corroborating]** — fetched page shows no legal entity, no physical address, template lorem content. Alone it caps at 🟡 and hands off to Stage 1 — honest small businesses run thin sites too.

## Register lookup procedure (zero calls — it reads the reference file)

1. Read `corp-register.md`; match the resolved entity (and its parent chain) against the table per the lookup rules.
2. Hit → snapshot the row: DP-IDs, tier, note; apply the preview band (T1/T2 → 🔴 zone · T3/T4 → 🟠 zone); add defunct/non-monetary flags when the note carries them.
3. No hit → the honest line is "no documented record — absence ≠ clean", and Stage 1 runs the full sweep. **Never** render a register miss as reassurance, and never treat a near-name as a hit.

## Why the register preview is not a snap verdict

An impersonation snap rests on a decisive tell observed directly — its basis is complete at zero searches, so it is final. A register preview rests on a *cutoff-dated catalog entry*: the company may have remediated, the matter may have resolved or been vacated, and the register deliberately records no positives — so a final band from it alone would be both stale and unbalanced. The preview buys speed (the user learns in seconds what's on the documented record) while the fast-path plan buys honesty (current status + balance, one `go` away).
