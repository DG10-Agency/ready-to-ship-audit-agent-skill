---
name: ready-to-ship-audit-agent-skill
description: "Judge DG10 launch safety with evidence and remedies."
version: 0.6.0
author: shubham-dg10 (https://github.com/shubham-dg10), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [production-readiness, ready-to-ship, go-live, release-audit, fix-plan, ai-agents, agent-skill, ship-readiness]
    related_skills: [production-readiness-audit, deployment-readiness, systematic-debugging]
---

# Ready-to-Ship Audit Agent Skill

One gate for any DG10 app. Ends with gaps + fix plan, always.

## When to Use

- User asks: ready to ship, go-live, launch safety, pre-release audit, or "what is left".
- Release-sensitive work just finished and someone must answer: safe to ship right now?
- Don't use for: per-commit code review (use requesting-code-review), single-bug root cause (use systematic-debugging), pure deploy-config diff (use deployment-readiness alone).

## Reuse before create

Search repo + skills + MemPalace for prior art before writing new checks or scripts. Extend production-readiness-audit / deployment-readiness. Reference the ReleaseGuard catalog by configured path; never copy its files in.

## Boundaries

This skill reports; it does not change. No config edits, commits, tags, pushes, deploys, prod migrations, or CI alterations. Ask approval before any shipping action. Default read-only; unknown_is_not_pass; redact secrets.

## Procedure

### 0. Preflight (5 min, kills false greens)

1. `terminal` with `gh auth status` — fix auth before any CI claim.
2. `terminal` with `ls` on the project root — if the mount dropped, abort to a local clone.
3. `read_file` every `.github/workflows/*.yml`; note trigger branches and what actually deploys from this branch.
4. Record commit SHA + artifact digest. Branch name alone is not identity. For nested repos record inner SHA; libraries with no artifact record no-artifact instead of a digest. Done when: SHA + channel + owner on page.

### 1. Profile + route (reuse)

Load production-readiness-audit §1-2 and deployment-readiness §Scope. Map languages, platforms, and layers with `search_files`. Route tracks A-E per the ReleaseGuard skill-map: same base commit, non-overlapping files, max 7 subagents. If a sibling skill is absent, proceed without it and record the gap under NOT VERIFIED. Done when: track assignments + file ownership table written.

### 2. Coverage ledger (checklist, not proof)

Reference the ReleaseGuard catalog (`catalogs/production-checks.json`, path configured per machine — never vendored in). One row per applicable check, init NOT ASSESSED. Map companion evidence to check IDs with provenance. Never convert missing capability to PASS. If the catalog path is unavailable, ledger=G1-G12 only with an explicit omission note. Done when: every applicable check has status + evidence pointer, or NOT ASSESSED + reason.

### 3. DG10 gap sweep (only what siblings + catalog miss)

Run every gate in `references/dg10-stack-gates.md`; each ends PASS/FAIL/NOT ASSESSED with a `file:line` or command output. Done when: zero gates left un-attempted without a reason.

### 4. Emit gaps + fix plan (motive — never skip)

Write `report.md` + `fix-plan.md` from `templates/`. Every FAIL becomes at least one fix task with files, exact commands, and acceptance. Every NOT ASSESSED becomes either a verification task or an explicit blind-spot with consequence. Every Fix names its check id verbatim. Verdict vocabulary, used once: READY / READY WITH WARNINGS / BLOCKED (ReleaseGuard SHIP/FIX/BLOCK in parentheses). Done when: gap table has zero orphan rows and the fix plan is build-ready.

### Freshness (every run)

Refresh vendor/official docs per gate scope; record each URL + access date in the report. A local snapshot is never truth — re-check live before PASS. A PASS resting on a superseded doc is invalid; downgrade to NOT ASSESSED.
