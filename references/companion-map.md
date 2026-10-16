# Companion map (route outward, never vendor)

Prefer maintained specialists for depth; DG10 owns only the gap column.
Strategy follows ReleaseGuard `coverage-ownership.md` (reuse → wrap →
build-only-for-gap → NOT ASSESSED). Zero copied check text below.

| Aspect | Prefer | DG10-owned gap | Evidence gate |
|---|---|---|---|
| App security / DAST | Cloudflare security skill; OWASP ASVS + ZAP on authorized staging | DG10 gates G2/G3 (SQL/auth) as pre-screen | Companion report + mapped check IDs, or NOT ASSESSED |
| Breadth / second opinion | Viaknox | DG10 stack gates G1–G15 it doesn't cover | Its findings mapped to ledger; gaps stay ours |
| Mobile security | OWASP MASVS-MASTG; MobSF | EAS flag gate G6; stale-bundle G7 | Static + device/dynamic output, or NOT ASSESSED |
| Dependency vulns | OSV + GHSA + CISA KEV | Exact version + lockfile + reachability call | Advisory range + fix release confirmed; no single feed = clean |
| Supply chain / provenance | OpenSSF Scorecard; Syft/CycloneDX SBOM | CI-permissions + artifact-hash binding (G11) | Hashes + attestation on shipped artifact |
| Browser E2E | Playwright | Critical-journey ↔ route ↔ screen gap table | Authored journeys green on release artifact |
| Web performance | Lighthouse CI | SLO + field metrics, not one lab score | Controlled repeats vs declared SLO |
| Load / capacity | k6 (bounded, staging only) | Traffic profile + headroom + cost under stress | Measured numbers, estimates labeled |
| Android build/packaging | MobSF; store publishing guidance | Signed binary == intended release (G6/G7) | Compare actual artifact, not source |

Safety rules: verify upstream revision + license + prereqs live
before running anything. OSV batch queries need `--allow-public-query`
consent (package names leave the box). DAST/load only against
authorized staging, bounded workload. Never upload a private repo
or prod artifact to an external scanner without owner approval.
