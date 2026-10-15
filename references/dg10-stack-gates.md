# DG10 stack gates (G1–G12)

Only what `production-readiness-audit`, `deployment-readiness`, and the
ReleaseGuard catalog miss. Tables only — procedure lives in SKILL.md.
Each gate ends PASS / FAIL / NOT ASSESSED with file:line or command output.

| # | Gate | How (exact command / grep) | Pass = |
|---|---|---|---|
| G1 | tsc zero-errors, both workspaces | `terminal`: `npx tsc --noEmit` at repo root AND at `apps/mobile/` | both exit 0; zero errors each |
| G2 | No template-literal SQL | Phase 1: resolve routes location (dir or file glob, e.g. backend/src/routes or server/*.routes.ts); if none exists, NOT ASSESSED; `search_files(pattern="query(`", path="<routes-dir>")` | zero hits |
| G3 | Auth on every route | Phase 1: resolve routes location (dir or file glob, e.g. backend/src/routes or server/*.routes.ts); if none exists, NOT ASSESSED; `grep -n 'router\.(get\|post\|put\|delete)' <routes-dir>/*.{js,ts} \| grep -v 'authenticate\|requirePipelineKey\|optionalAuth'` | zero hits (every route carries auth middleware) |
| G4 | Keyset pagination tiebreaker | Phase 1: resolve actual backend source dir (example: `backend/src`); `search_files(pattern="ORDER BY created_at", path="<backend-src-dir>")` then confirm `id DESC` tiebreaker + `WHERE ... id < $N` clause at each site; if no backend source dir exists, NOT ASSESSED | present at every paginated query |
| G5 | Supabase RLS + GoTrue | Phase 1: resolve actual app dir (example: `apps/`); list RLS policies per user table via Supabase dashboard/SQL; `search_files(pattern="service_role\\|service-role", path="<app-dir>")` for client-side leaks; if no app dir exists, NOT ASSESSED | policy exists on every user table AND zero client-side service-role hits |
| G6 | Expo EAS build flags | Phase 1: resolve actual build workflow (example: `.github/workflows/build-apk.yml`); read it: `assembleRelease --no-daemon --no-parallel`, reanimated/worklets pinned in `overrides`, JVM heap 4096m + Metaspace 1024m; if no build workflow exists, NOT ASSESSED | workflow matches all three |
| G7 | Stale-bundle guard | `terminal`: hash served `index.html`/bundle vs fresh export hash; confirm server ROOT serves the export dir; libraries with no bundle/export dir -> NOT ASSESSED | hashes equal AND ROOT == export dir |
| G8 | Cron has a caller | `terminal`: `grep -rn "schedule:" .github/workflows/` per cron route, or crontab/timer entry over SSH; `CRON_SECRET` in secrets store AND deploy env; handler has sent-flag / generate-only-if-due | schedule + both-side secret + idempotent handler, all three present |
| G9 | Migration clean | `terminal`: `prisma migrate status` on target DB; backend logs free of `P2022`; new endpoints return 401 (auth, live) not 404 (missing) | `migrate status` clean AND zero P2022 AND 401-not-404 |
| G10 | Stripe webhook replay | staging: replay a captured `checkout.session.completed` / `invoice.paid` event twice against the webhook endpoint | second delivery is a no-op (idempotency key hit), exactly one side effect |
| G11 | Contabo via CI only | `terminal`: `gh run list` deploy workflow green for this SHA; `git status` on server shows no manual edits; `systemctl --user list-units` shows supervised unit, not bare proc | green CI + zero manual edits + supervised unit |
| G12 | WP Plugin Check | `terminal`: run `Plugin Check via Docker` per wp-plugin-testing-lab before submission | report attached to release evidence, zero errors |

Rules: unknown is NOT ASSESSED, never PASS. Any gate that cannot run
(no SSH, no staging, no Docker) is NOT ASSESSED with reason + consequence.
