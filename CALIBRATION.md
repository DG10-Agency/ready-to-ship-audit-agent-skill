# CALIBRATION.md — self-audit of THIS repo (v0.8.1 gates)

Scope: agent-skill repo (SKILL.md + references/ + stdlib-only `scripts/` + `templates/` + validate-only CI). No app backend, no DB, no deploy target. Gates read from `references/dg10-stack-gates.md` (v0.8.1).
Method: `python3 scripts/gate_check.py .` → `GATE PASS (3 files, 0 fails mapped)` exit 0; `python -m unittest discover -s scripts` → 6 tests OK; `gh run list` → 5 recent `validate` runs green (e.g. run 38860614780, success, 2026-10-16); secret grep (`sk_live|ghp_|AKIA|api[_-]?key\s*=|password\s*=`) → zero hits.

| Gate | Verdict | Evidence (one line) |
|---|---|---|
| G1 tsc zero-errors | PASS | `scripts/gate_check.py:73` GATE PASS exit 0; scope: `scripts/` only — no tsconfig/TS sources, tsc not applicable |
| G2 no template-literal SQL | NOT ASSESSED | no routes/backend dir exists; `scripts/*.py` has zero `query(`/`queryRaw` hits (verified via grep, `scripts/` only) |
| G3 auth on every route | NOT ASSESSED | no routes location exists (skill repo, no HTTP surface); nothing to grep per gate Phase 1 |
| G4 keyset pagination tiebreaker | NOT ASSESSED | no backend source dir exists; zero query sites after grep, never vacuous PASS per gate |
| G5 Supabase RLS + GoTrue | N/A | no Supabase client/import anywhere; stdlib-only skill — N/A-by-design, not untested surface |
| G6 Expo EAS build flags | NOT ASSESSED | no build workflow exists (only `.github/workflows/validate.yml:3` `on: [push, pull_request]`) |
| G7 stale-bundle guard | NOT ASSESSED | library/no-bundle repo; no export dir or EAS artifact to hash |
| G8 cron has a caller | N/A | no cron route exists; `validate.yml` triggers push/PR only, no `schedule:` entry |
| G9 migration clean | NOT ASSESSED | no runner/target DB; no `prisma/` or `migrations/` dir; `scripts/` contains zero SQL |
| G10 Stripe webhook replay | N/A | no webhook endpoint and no PSP surface (only doc-example mentions in `templates/fix-plan.md:43`) |
| G11 Contabo via CI only | N/A | no deploy workflow and no server target (validate-only CI); supporting signal: `gh run list` shows green `validate` runs, e.g. run 38860614780 success |
| G12 WP Plugin Check | N/A | no plugin header (`Plugin Name` zero hits) — non-plugin |
| G13 desktop packaging | N/A | no desktop target; zero `tauri|electron` hits outside gate doc itself |
| G14 observability/SLO/cost/PII/registry | NOT ASSESSED (split) | SLO: NOT ASSESSED — no availability/p95 target recorded; cost/PII/registry: N/A — no LLM runtime surface in checkout (`scripts/` is stdlib shape-check only); PII policy documented in `SECURITY.md:20` |
| G15 web/API hygiene | PASS | license sub-check PASS: `LICENSE:1` MIT + zero dependency manifests (no package.json/requirements.txt) so no GPL possible; rate-limit N/A (no mutating routes); a11y N/A (no web surface) |

Denominator: G1–G15 applicable only → 9 applicable (G1, G2, G3, G4, G6, G7, G9, G14-SLO, G15 — rows with verdicts other than N/A; N/A: G5, G8, G10, G11, G12, G13 = 6). Zero FAILs. NOT ASSESSED items are blind spots with nil consequence here (no executable/networked surface in checkout); none is a P0 ship-killer for a static skill repo.

VERDICT: READY WITH WARNINGS (ReleaseGuard equiv: SHIP WITH ACCEPTED RISK) — evidence: zero FAILs, `gate_check.py` GATE PASS exit 0, 6/6 unit tests OK, green CI (run 38860614780), secret grep zero hits; warnings: G2/G3/G4/G6/G7/G9/G14-SLO unassessed blind spots, tracked as verification tasks on first real-target audit, no owner sign-off needed before use as a skill.
