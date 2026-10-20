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
Self-contained inputs (v0.8.1):                   │                                 - coverage line with
no external skills required.                      ▼                                   explicit denominator
- references/core-procedure.md                    ┌───────────────────────────────┐       - rollback plan
  (structure discovery,                           │ §1 PROFILE + ROUTE            │       - secrets statement
  auth-surface read,                              │ map languages/platforms/      │         (redacted)
  CI-artifact proof)                              │ layers → cut tracks A–E on   │
- ReleaseGuard catalog (optional)                 │ one commit, non-overlapping   │       fix-plan.md
  (172 checks; checklist,                         │ files, max 7 subagents        │       - P0 blockers (must close
  not proof)                                      └───────────────┬───────────────┘         before SHIP)
                                                  │                       - P1 warnings + 30-day (ship only
                                                  ▼                         with owner sign-off)
                                  ┌───────────────────────────────┐       - P2 hardening + 90-day
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
                                  │ §3 DG10 SWEEP (G1–G17,        │
                                  │ references/dg10-stack-gates)  │
                                  │ G1 tsc workspaces · G2        │
                                  │ no-template SQL · G3 auth     │
                                  │ per-handler table · G4        │
                                  │ keyset/offset rule · G5       │
                                  │ RLS/split/N/A · G6 EAS/       │
                                  │ Gradle flags · G7 bundle/     │
                                  │ artifact hash · G8 cron +     │
                                  │ scheduler variant · G9        │
                                  │ migration/raw-SQL split ·     │
                                  │ G10 PSP replay · G11 CI       │
                                  │ triggers · G12 WP Check ·     │
                                  │ G13 desktop packaging ·       │
                                  │ G14 SLO/cost/PII/registry     │
                                  │ · G15 rate-limit/license/     │
                                  │ a11y · G16 service liveness   │
                                  │ + restart policy · G17 boot  │
                                  │ smoke — each ends PASS /      │
                                  │ FAIL / NOT ASSESSED / N/A     │
                                  │ with file:line or cmd out     │
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

This skill is self-contained as of v0.9.0 (procedure vendored in `references/core-procedure.md`; the sibling columns above are routing context, not dependencies) and references the ReleaseGuard catalog by path instead of vendoring it. It adds only what breadth scans miss: DG10 stack gates (G1–G17) plus the verdict-to-fix-plan finish.

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

**How do I install it?**
Run `npx skills add DG10-Agency/ready-to-ship-audit-agent-skill`, or clone the repo and load `SKILL.md` in your agent harness.

## Executing fix-plans at scale

This skill audits and plans; for **executing** a fix-plan across dozens or
thousands of items (files, records, URLs) without losing progress on weak
models or long runs, use the separate-but-linked
**agentic-batch-loop-engine** — checkpointed resume, retries, timeouts,
and per-item evidence logs:

- Engine repo: <https://github.com/DG10-Agency/Agentic-Batch-Loop-Engine-by-DG10.Agency>
- Install: `npx skills add DG10-Agency/Agentic-Batch-Loop-Engine-by-DG10.Agency`
- Typical flow: this skill emits `fix-plan.md` → feed each finding as a batch
  item into the engine → verify with `scripts/gate_check.py` → ship.

## Install

```bash
npx skills add DG10-Agency/ready-to-ship-audit-agent-skill
git clone https://github.com/DG10-Agency/ready-to-ship-audit-agent-skill.git ready-to-ship-audit-agent-skill
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
- `references/core-procedure.md` — self-contained run procedure (no external skills needed).
- `references/dg10-stack-gates.md` — gates G1–G17 (DG10 stack + desktop + observability + hygiene + live liveness + boot smoke).
- `references/verdict-and-evidence.md` — verdict vocabulary, evidence rules, maturity bands.
- `references/companion-map.md` — breadth-scan routing and coexistence.
- `scripts/gate_check.py` — ledger checker; `scripts/test_gate_check.py` — unit tests.
- `templates/report.md`, `templates/fix-plan.md` — output shapes.
- `.claude-plugin/plugin.json` — install manifest (`npx skills add`); `CALIBRATION.md` — self-audit proving a non-BLOCKED verdict.

## Freshness and limits

Battle-tested across four real app audits (Academy mobile → v0.4.0, PIB auth shell → v0.5.0, MicStudio web → v0.6.0, VakilOne monorepo → v0.7.0; every version tagged) plus a published self-audit (`CALIBRATION.md`, verdict READY WITH WARNINGS). Honest note: still no fixed-corpus benchmark — no measured precision, recall, or ship-decision success rate. It cannot see production secrets, live traffic, or uninstrumented failure modes; anything unverifiable is reported as a blind spot, not a pass. Re-verify `last_verified` dates in `references/` before launch claims.

## Versioning

The version lives in the `SKILL.md` frontmatter (currently `0.8.1`). History is tracked through git tags and GitHub Releases — `git tag v0.8.1 && git push origin v0.8.1`.

## License

MIT © 2026 [shubham-dg10](https://github.com/shubham-dg10) — see [`LICENSE`](LICENSE).
