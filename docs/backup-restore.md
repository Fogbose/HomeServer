# Backup and recovery plan

**This starter does not include a backup scheduler or an automated restore.**
Build and test these before importing unique documents. The originating private
installation had a snapshot restored successfully, but its account-specific
scripts and proof do not validate a new community installation.

## What to retain

- The entire html volume (config, custom apps, themes and user data).
- A consistent PostgreSQL export and required roles/ownership information.
- Compose, local overrides, .env, image digests and the protected secret files.
- Host reconstruction instructions and separately protected recovery keys.

Do not copy running PostgreSQL data files as if they were a logical backup. The
Nextcloud application role can differ from the PostgreSQL bootstrap role:
`pg_dump` alone does not include global roles. Decide whether to export protected
role metadata or recreate only the required role in isolation. Never fix a test
restore by resetting production credentials.

## Coherent capture procedure to adapt

1. Confirm server identity, stack, volume identities, free space and destination.
   Take a lock shared by every backup/maintenance operation.
2. Check no migration or critical task is in progress. Enable Nextcloud maintenance.
3. Quiesce background work without killing an active job, then stop writers
   gracefully. Verify no container was killed with exit 137. Decide how to handle
   a timeout before starting; do not accept a partially interrupted task silently.
4. Export PostgreSQL with its matching tool version; verify the dump table of
   contents. Archive the html volume and configuration with ownership/metadata.
   Use approved temporary tooling or the host's known volume paths; do not copy
   arbitrary data from a guessed Docker path.
5. Verify archive structure and checksums; restore app/cron and disable maintenance
   with error handling. An interrupted script must not publish success.
6. Encrypt and copy to another physical machine/device. Verify both capture time
   and transfer time, integrity and recoverability with a separately held key.

A backup to the same SSD cannot protect against losing it. A laptop copy depends
on its power/session/network and may share theft/fire risks at home. Set retention
only after considering capacity and tested recovery; never delete all previous
copies before verifying new ones. Schedule health/failure notifications deliberately.

## Isolated restore acceptance test

Choose an explicit snapshot, checksums and empty target. Record images, keys and
permissions required. Do not reuse production volumes or overwrite active data.
Create a separate Compose project, distinct volumes, no cron, no exposed public
ports and no outgoing application traffic; **the default compose.yaml is not an
isolated restore configuration** because app/cron have outbound access.

Restore roles/database and html together, preserving ownership; adapt only the
test copy's host/proxy settings. Verify Nextcloud status, login, a user's file
download/upload, Redis, permissions and authenticated WebDAV. Compare recovered
files and record timings/errors. Shut down the test services after review without
deleting evidence or data unless explicitly approved.

Define recovery point/time objectives from measured tests and operational needs;
the mere existence of a daily schedule is not an RPO guarantee.

Sources: [Nextcloud backup](https://docs.nextcloud.com/server/stable/admin_manual/maintenance/backup.html),
[restore](https://docs.nextcloud.com/server/stable/admin_manual/maintenance/restore.html),
[PostgreSQL pg_dump](https://www.postgresql.org/docs/17/app-pgdump.html).
