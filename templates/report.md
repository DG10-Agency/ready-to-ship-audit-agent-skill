# Release report: <app> @ <sha> (<channel>)

> Fill every slot. Delete nothing. Unknown stays NOT VERIFIED — never PASS.
> Verdict used once; put ReleaseGuard equiv in parentheses on the VERDICT line.

VERDICT: <BLOCKED | READY WITH WARNINGS | READY> (<BLOCK | SHIP WITH ACCEPTED RISK | SHIP>)
RE-SCORE DATE: <YYYY-MM-DD — next re-run due: next release or quarterly, whichever first>

## Why (3 lines max)

1. <strongest reason for the verdict>
2. <second reason, or second blocker>
3. <third reason, or owner decision needed>

## Gap table (every FAIL + NOT ASSESSED — zero orphan rows)
<!-- maturity band per Fix: now (P0) / 30-day (P1) / 90-day (P2) — put band in fix task ref, e.g. <Fix 2, 30-day> -->

| check | severity | evidence (file:line or cmd) | impact | fix task |
|---|---|---|---|---|
| <G#/catalog id> | <Critical/High/Medium/Low> | <path/file:line OR exact cmd + output digest> | <what breaks if shipped> | <fix-plan.md Fix N> |
| <example: G3 auth-on-routes> | <High> | <backend/src/routes/x.ts:12 — no authenticate> | <unauth access to pipeline data> | <Fix 1> |

## Passed (one line each, with proof pointer)

- <check id + one-line what passed> — proof: <file:line OR cmd + output digest>
- <example: G1 tsc clean — proof: `npx tsc --noEmit` exit 0, web+mobile>

## NOT VERIFIED (what couldn't run + why + consequence)

- <check/area> — why: <no access / tool missing / out of scope> — consequence: <risk carried if shipped>
- <example: DAST staging scan — why: no authorized staging target — consequence: reflected-XSS class unverified>

## Coverage

- attempted: <n> / passed: <n> / failed: <n> / unassessed: <n> / NA: <n> / denominator: <n total applicable>
- envs: <e.g. staging API + web export> | devices: <e.g. Pixel 6a API 34, desktop Chrome> | roles sampled: <e.g. owner, member, anon>

## Rollback plan

- <how to revert this release: exact command / deploy step / migration downgrade>
- <example: revert to tag v1.2.3 via deploy workflow re-run; `prisma migrate resolve --rolled-back <migration>`>

## Secrets statement

- Secrets redacted in all evidence above (hashes/artifact IDs only, no values). No client-side service-role keys observed: <yes/no/NOT VERIFIED>.
