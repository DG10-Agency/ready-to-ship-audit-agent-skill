# Core procedure (self-contained run path)

Run these three passes in order on the target repo. No outside
skill is needed; each pass names its own tools and stop rule.

## 1. Structure discovery

Walk the tree with `search_files` for manifests, entry points,
and platform markers (package.json, build.gradle, Podfile,
Dockerfile, .github/workflows). Group hits by runtime, client,
and backing service so every later check has an owner.

| Layer | Marker searched | Found at | Owner pass |
|---|---|---|---|
| runtime | manifest + lockfile | path noted | pass 3 |
| client | entry + bundle config | path noted | pass 2 |
| service | compose + workflow | path noted | pass 3 |

List gaps where a layer has code but no marker hit.
Done when: every layer row has a path or an explicit gap note.

## 2. Auth-pattern surface read

Open each route handler and record how identity is established:
session, token, key, or none. One table row per handler with
the file and line where the decision happens; shared guards
get one row pointing at the guard, not one row per caller.

Flag handlers with no identity step as open, and mark any
mixed-trust handler where one path skips the guard.
Done when: every handler has a row, and every open row is flagged.

## 3. CI-artifact proof

Run `gh run list` on the release branch and read each active
workflow file for its trigger branches. Tie the newest green run
to its commit SHA, then compare the run's bundle hash against
the artifact about to ship; names and tags alone do not match.

Record run id, branch, SHA, and hash side by side in the report.
Done when: SHA equals the audited commit and both hashes match.
