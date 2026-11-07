# Operations and troubleshooting

## Read-only checks on Linux

```sh
hostname
docker compose ps --all
python3 tools/homeserver.py check
docker compose exec -T -u www-data app php occ status
df -h
```

Use sudo for Docker if needed; in that case run the Python check with the same
authorized Docker access. The helper executes only Compose process queries,
Nextcloud status and Redis ping. It does not repair, restart, restore, inspect
secrets, measure disk health or establish that a backup is recoverable.

| Symptom | First checks | Avoid |
| --- | --- | --- |
| Cannot reach web UI | Host on, SSH tunnel, correct local port, app health | Publishing all interfaces as a workaround |
| Remote DNS/HTTPS fails | Client VPN, DNS, exact certificate hostname, access policy, Serve | Disabling TLS checks or firewall |
| Missing/unhealthy db | Free space, service state, targeted local logs | Deleting a volume or changing a secret at random |
| Maintenance persists | Backup/update owner, cron/writers state, application status | Blindly disabling maintenance during a migration |
| Cron running but jobs overdue | Last execution in Nextcloud admin page and job logs | Treating a running scheduler as proof of completion |
| Disk fills | Volumes, versions/trash, logs, backup staging and restore tests | Automated prune or deletion without a retention decision |

Logs can contain personal filenames, URLs and identities. Inspect locally and
redact before sharing. Do not paste `config.php`, .env or a complete environment.

## Updates

1. Read current upstream advisories, supported upgrade paths and compatibility.
2. Record images/digests and local overrides. Test a recoverable external backup.
3. Choose a maintenance window and rollback/recovery plan including migrations.
4. Change pins in a reviewable commit. Validate Compose and exercise the new
   version against a disposable copy before production.
5. Verify login/data, proxy/WebDAV, cron and a new coherent backup after deployment.

Do not jump Nextcloud major versions against its supported path. Do not revert
only an image after an incompatible database migration. PostgreSQL major upgrades
need their own migration procedure; replacing the image tag is not a migration.
Dependency-update PRs must be reviewed, not automatically merged into a live host.

## Stopping

`docker compose stop` requests graceful service stops, but still interrupts users
and background work. Plan the operation; inspect exit states and allow sufficient
time. This starter does not guarantee arbitrary active jobs complete on shutdown.
Never disconnect power as an application shutdown mechanism. No destructive cleanup
command is included in the normal operating procedure.
