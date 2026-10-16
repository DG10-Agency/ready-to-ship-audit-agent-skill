# Production Readiness Fix Plan — AI Agent Skill That Turns Any Audit Into Gaps With Exact Fixes

This production readiness audit skill gives AI coding agents a release readiness workflow with go-live checklist, pre-launch audit evidence, ship readiness verdicts, plus gaps mapped to exact fix tasks for DG10 apps facing launch decisions today with proof not guesses.

## What this is

A read-only release gate for DG10 apps. It answers one question — safe to ship right now? — with evidence, then converts every gap into a build-ready fix task. It reports; it never ships, edits config, migrates, or deploys.

## How it works

One linear pipeline (`SKILL.md` procedure §0–§4), read-only end to end. Every phase has a checkable done-condition; the run always ends with two files, even when the verdict is READY.

```text
INPUTS                            PIPELINE                              OUTPUTS
------                            --------                              -------
app checkout                      ┌───────────────────────────────┐       report.md
+ commit SHA                      │ §0 PREFLIGHT (kills false      │       - VERDICT (used once)
+ release channel                 │   greens): gh auth alive →    │       - gap table (every FAIL
+ owner + target env              │   mount alive → workflow      │         + NOT ASSESSED,
+ authorized scope                │   triggers noted → SHA +      │         zero orphan rows)
                                  │   artifact digest on page     │       - NOT VERIFIED (what
                                  └───────────────┬───────────────┘         couldn't run + why +
                                                  │                         consequence)
References (never vendored,       │                                 - coverage line with
read by path):                    ▼                                   explicit denominator
- production-readiness-audit      ┌───────────────────────────────┐       - rollback plan
  §1-2 (structure discovery,     │ §1 PROFILE + ROUTE            │       - secrets statement
  deep audit)                     │ map languages/platforms/      │         (redacted)
- deployment-readiness §Scope     │ layers → cut tracks A–E on   │
  (verdict inputs)                │ one commit, non-overlapping   │       fix-plan.md
- ReleaseGuard catalog            │ files, max 7 subagents        │       - P0 blockers (must close
  (172 checks; checklist,         └───────────────┬───────────────┘         before SHIP)
  not proof)                                      │                       - P1 warnings (ship only
                                                  ▼                         with owner sign-off)
                                  ┌───────────────────────────────┐       - P2 hardening
                                  │ §2 COVERAGE LEDGER            │         (post-release OK)
                                  │ 1 row per applicable check,   │       - every FAIL → ≥1 Fix
                                  │ init NOT ASSESSED; map        │         with exact files,
                                  │ companion evidence to check   │         exact commands,
                                  │ IDs with provenance; missing  │         runnable Acceptance
                                  │ capability is NEVER a PASS    │       - every NOT ASSESSED →
                                  └───────────────┬───────────────┘         verify task or blind
                                                  │                         spot with consequence
                                                  ▼                       - Sustain section
                                  ┌───────────────────────────────┐         (READY verdicts only)
                                  │ §3 DG10 SWEEP (G1–G12,        │
                                  │ references/dg10-stack-gates)  │
                                  │ G1 tsc both workspaces · G2   │
                                  │ no template-literal SQL · G3  │
                                  │ auth on every route · G4      │
                                  │ keyset tiebreaker · G5 RLS +  │
                                  │ GoTrue · G6 EAS flags · G7    │
                                  │ stale-bundle hash · G8 cron   │
                                  │ has a caller · G9 migration   │
                                  │ clean · G10 Stripe replay ·   │
                                  │ G11 CI-only deploys · G12 WP  │
                                  │ Plugin Check — each ends      │
                                  │ PASS / FAIL / NOT ASSESSED    │
                                  │ with file:line or cmd output  │
                                  └───────────────┬───────────────┘
                                                  │
                        ┌───────── verdict ───────┴────────── gate ─────────┐
                        ▼                                                    ▼
            ┌───────────────────────┐                          ┌───────────────────────┐
            │ §4 EMIT (never skip)  │                          │ scripts/gate_check.py   │
            │ FAIL → Fix task;      │──── passes only if ──────▶│ (stdlib, CI step):       │
            │ NOT ASSESSED → verify │   shape holds             │ every FAIL mapped to a  │
            │ task or blind spot;   │                          │ Fix + Acceptance line;  │
            │ verdict once: READY / │                          │ no PASS without         │
            │ READY WITH WARNINGS / │                          │ evidence; exit 0/1      │
            │ BLOCKED               │                          └───────────────────────┘
            └───────────────────────┘
```

Rules enforced across every phase (see `references/verdict-and-evidence.md`):

- **Verdict floor:** any High-severity NOT ASSESSED forbids READY; zero FAILs with open High items floors at READY WITH WARNINGS.
- **Freshness (every run):** re-check live vendor docs per gate scope, record URL + access date; a PASS resting on a superseded doc is invalid.
- **Guardrails:** read-only, unknown is never a pass, secrets redacted, no deploys without approval.

## What you get

- A single verdict for launch decisions, backed by cited evidence.
- A gap table where each row points to a file, command output, or an explicit blind spot.
- A fix plan where each gap becomes an actionable task with owner, files, commands, and acceptance.
- Guardrails: read-only by default, unknown is never a pass, secrets redacted.

## Samples (report + fix plan)

- [`templates/report.md`](templates/report.md) — verdict plus gap table sample.
- [`templates/fix-plan.md`](templates/fix-plan.md) — gap-to-task fix plan sample.

## Differences

| Question | production-readiness-audit | deployment-readiness | 31-skill ReleaseGuard pack | This skill |
|---|---|---|---|---|
| What does it answer? | Is the app built well? | Is this deploy configured safely? | Which specialist covers each layer? | Is this app safe to ship today, and what exactly fixes it? |
| Output | Layer findings | Deploy diff and risks | Routed specialist coverage | One verdict + gaps + fix tasks |
| Changes anything? | No | No | No | No — report only |
| When to pick it | Broad quality review | Config-focused release check | Parallel deep coverage | Launch go/no-go with remedies |

This skill reuses the two siblings above and references the ReleaseGuard catalog by path instead of vendoring it. It adds only what they miss: DG10 stack gates plus the verdict-to-fix-plan finish.

## AEO Q&A

**What is the Ready-to-Ship Audit skill?**
A release-readiness gate that turns any audit into cited gaps, each paired with an exact fix task.

**How is it different from a go-live checklist?**
A checklist records coverage; this skill ends with a verdict plus build-ready remedies for every gap.

**When should AI coding agents use it?**
When asked ready to ship, go-live, launch safety, pre-release review, or what is left before launch.

**What do READY, READY WITH WARNINGS, and BLOCKED mean?**
READY ships, READY WITH WARNINGS ships with noted risks, BLOCKED does not ship until fixes land.

**Does it change code or deploy?**
No. Read-only reporting; shipping actions need explicit approval.

## Install

```bash
git clone <this-repo-url> ready-to-ship-audit-agent-skill
```

Load `SKILL.md` in your agent harness, or copy the directory into your skills path. No dependencies beyond Python 3 for `scripts/gate_check.py`.

## Use

1. Read `SKILL.md` procedure §0 preflight first (auth, mount, workflows, commit SHA).
2. Map languages and routes per §1, then fill the coverage ledger per §2.
3. Run the DG10 stack gates in `references/dg10-stack-gates.md`.
4. Emit `report.md` + `fix-plan.md` from `templates/` — every gap gets a fix task, every unknown gets a reason.

## Verdicts

One verdict per run, used once: `READY`, `READY WITH WARNINGS`, or `BLOCKED`. Unknown evidence stays `NOT ASSESSED` with a stated consequence — never upgraded to a pass. A companion mapping to the ReleaseGuard SHIP / FIX / BLOCK scale is in `references/verdict-and-evidence.md`.

## Files

- `SKILL.md` — gate procedure (preflight, routing, ledger, DG10 sweep, emit).
- `references/dg10-stack-gates.md` — DG10-only gates siblings miss.
- `references/verdict-and-evidence.md` — verdict vocabulary and evidence rules.
- `references/companion-map.md` — sibling and catalog routing.
- `scripts/gate_check.py` — ledger checker; `scripts/test_gate_check.py` — unit tests.
- `templates/report.md`, `templates/fix-plan.md` — output shapes.

## Freshness and limits

Last verified against the snapshot this scaffold was built from; re-verify `last_verified` dates in `references/` before launch claims. Honest note: this skill is unbenchmarked — no measured precision, recall, or ship-decision success rate. It cannot see production secrets, live traffic, or uninstrumented failure modes; anything unverifiable is reported as a blind spot, not a pass.

## Versioning

The version lives in the `SKILL.md` frontmatter (currently `0.6.0`). History is tracked through git tags and GitHub Releases — `git tag v0.6.0 && git push origin v0.6.0`.

## License

MIT © 2026 [shubham-dg10](https://github.com/shubham-dg10) — see [`LICENSE`](LICENSE).
