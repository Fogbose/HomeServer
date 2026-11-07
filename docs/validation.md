# Validation coverage

## Local preparation — 2026-11-07

- Python 3.12 on Windows: 11 behavior tests passed. They exercise credential
  generation without printing passwords, refusal to overwrite/repair partial
  state, magic-packet bytes, preview without sockets, invalid targets and
  diagnostic handling of missing/unhealthy/maintenance states.
- Local Markdown file links are checked by `python tests/check_links.py`.
- No local Docker Engine was available on the preparation PC. Compose validation
  and full fresh-install testing are delegated to the disposable Linux CI below.
- No connection or modification to the originating private home server was made.

## GitHub Actions

**First Linux integration run passed on 2026-11-07**, for commit
`b85c28bf8e3ce1c4ffa3b0cef53e1e19f3906ad1`:
[validated run](https://github.com/Fogbose/HomeServer/actions/runs/42394077045).
The run passed Python tests, local links, credential initialization, Compose
validation, fresh container startup, background-job configuration, diagnostics,
authenticated WebDAV upload/download and file persistence after an app restart.
This result applies to that pinned baseline on the hosted Ubuntu runner; it is
not a deployment or recovery guarantee for another host.

The workflow uses a standard hosted Ubuntu runner with read-only repository
permissions, no personal server credentials and no uploaded artifacts/cache.
It runs the tests, validates Compose, starts the pinned stack, checks app/cache
readiness, uploads/downloads a disposable file over authenticated WebDAV, restarts
app and verifies that file again. It stops services at the end. See the actual
[Actions runs](https://github.com/Fogbose/HomeServer/actions) for results; a workflow
file existing is not evidence that its run passed.

No hardware wake test, VPN/HTTPS end-to-end test, long-running cron proof,
backup/restore drill or host rebuild is covered by this CI. A restart-persistence
test is not a disaster-recovery test. Windows ACL behavior is not a substitute
for POSIX deployment permission testing.

## Before using real data

Validate the stack on your actual Linux version and CPU architecture, host disk
health/capacity, access policy, HTTPS/DAV behavior, user permissions, successful
cron execution and external backup recovery. Test WOL separately with physical
access available. Record observed results and dates; do not infer them from the
originating private deployment or from a passing unit test.
