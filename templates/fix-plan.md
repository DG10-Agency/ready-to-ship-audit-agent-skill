# Fix plan: <app> @ <sha>

> Order: P0 blockers → P1 warnings → P2 hardening. Every Gap-table FAIL has ≥1 Fix here.
> Every NOT ASSESSED has either a verification Fix or an entry under Blind spots.

## P0 — Blockers (must close before SHIP)

### Fix 1: <title> [blocks SHIP]

- Check: <G#/catalog id> | Severity: <Critical/High>
- Files: <exact path 1>, <exact path 2>
- Commands:
  - `<exact command>` — expected: <exact expected output / exit code>
- Acceptance: <runnable check that FAILS before the fix and PASSES after>
  - `<exact command or test invocation>`
- Verify: <tsc / tests / curl / screenshot — exact command + what to look at>

## P1 — Warnings + 30-day (ship only with owner sign-off, tracked as required changes; close within 30 days)

### Fix 2: <title>

- Check: <id> | Severity: <Medium>
- Files: <exact paths>
- Commands:
  - `<exact command>` — expected: <expected output>
- Acceptance: <runnable check failing-before / passing-after>
- Verify: <exact command + expected result>

## P2 — Hardening + 90-day (post-release OK; harden within 90 days)

### Fix 3: <title>

- Check: <id> | Severity: <Low>
- Files: <exact paths>
- Commands:
  - `<exact command>` — expected: <expected output>
- Acceptance: <runnable check failing-before / passing-after>
- Verify: <exact command + expected result>

## Sustain (fill ONLY when verdict is READY; otherwise write N/A)

- <observe/schedule task: what to watch, threshold, who owns it>
- <example: alert on Stripe webhook 5xx > 1% over 1h — owner: on-call>

## Blind spots carried forward

- <NOT ASSESSED item with no verification Fix> — consequence: <risk> — next step: <when/how it gets verified>
