# Contributor automation instructions

- Inspect existing files and preserve user work. Keep this repository generic:
  no private hostnames, addresses, credentials, snapshots or personal diagnostics.
- Linux is the deployment target; distinguish Windows administration commands.
- Never modify a live host to test a documentation change. Use disposable data.
- No volume deletion, partitioning, restore, network/security changes, force push
  or publication beyond the explicitly authorized scope.
- Keep image versions and digests explicit; read upstream compatibility/advisories.
- Do not claim hardware WOL, recovery, HTTPS or security is verified by unit tests.
- Run meaningful helper tests and Compose validation; document untested behavior.
- Update public docs with implementation changes. No API spending or services
  with charges without explicit authorization.
