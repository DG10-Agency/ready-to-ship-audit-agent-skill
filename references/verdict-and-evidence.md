# Verdict and evidence

One verdict language. Parents: ReleaseGuard `release-gate.md`
(SHIP/FIX/BLOCK) and `deployment-readiness` verdict section — mapped,
not copied. Severity wording follows ReleaseGuard `evidence-and-severity.md`.

| Ours | Means | ReleaseGuard equiv |
|---|---|---|
| BLOCKED | Do not ship; ≥1 hard blocker open | BLOCK |
| READY WITH WARNINGS | May ship with owner sign-off; warnings tracked as required changes | SHIP WITH ACCEPTED RISK (non-blocking only) |
| READY | Ship; zero blockers, zero untracked warnings | SHIP |

Mapping rule: never emit two verdicts. Write ours; put the
ReleaseGuard equiv in parentheses once in the report header.

Triangulation rule: a PASS needs two of three — (a) repo/config
evidence, (b) live-command output (build log, curl, `gh run`),
(c) current vendor/official doc for behavior claims. Three model
opinions with no artifact are zero evidence, not triangulation.

Severity: Critical (ship-killer: RCE, cross-tenant, live secret,
irreversible loss) / High (exploitable auth bypass, reachable
injection, reachable vuln dep) / Medium (constrained exploit or
reliability risk with mitigation) / Low (narrow hygiene).
Keep severity separate from confidence (high/medium/low).

NOT VERIFIED rule: anything not run goes under report.md
`NOT VERIFIED` with what + why + consequence. Missing capability
is never converted to PASS. Coverage line needs an explicit
denominator (attempted/passed/failed/unassessed/NA).

Kanban mapping: BLOCKED → `kanban_block` with blocker list.
READY / READY WITH WARNINGS → `kanban_request_review`, warnings
attached as required changes. No silent absorption.
Redact secrets in all evidence (hash or artifact ID, never values).
`scripts/gate_check.py` checks ledger shape only, never truth — a GATE PASS is not evidence a gate actually ran. Floor rule: any High-severity NOT ASSESSED forbids READY; zero FAILs + open High unassessed floors at READY WITH WARNINGS.

Readiness bands: BLOCKED = any P0 open (ship-killer, must close now); READY WITH WARNINGS = zero P0 + open P1 (ship with owner sign-off, P1 closes within 30 days); READY = zero P0/P1 + open P2 only (P2 hardens within 90 days, tracked in Sustain/blind-spots).

Re-score rule: re-run every release + quarterly; report carries a re-score date; trend (band movement + gap aging) beats absolute score — cite prior band + date when re-scoring.

<!-- last_verified: 2026-10-18 — verdict language vs ReleaseGuard mapping; no vendor doc dependency. -->
