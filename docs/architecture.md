# Architecture and configuration

The host provides Linux, Docker, SSH and optional VPN/TLS. Compose provides four
services: app (Apache/Nextcloud), cron, db (PostgreSQL), redis. There is no host
firewall installer, no socket Docker mount in the application and no privileged
container. Docker access itself is powerful; do not grant it casually.

## Persistent storage

The `html` volume contains the complete `/var/www/html` including config, custom
apps and user files. The `postgres` volume contains active database files. Named
volumes are managed by Docker on its storage filesystem; verify the physical
disk and capacity before deployment. This baseline does not relocate a HDD, create
partitions or configure encryption. A second disk in the same PC is not an
external backup. Never use `docker compose down -v` for troubleshooting.

The project name defaults to `homeserver`. To run another independent instance,
use a separate checkout/configuration and an explicit distinct Compose project
name consistently, including diagnostics (`COMPOSE_PROJECT_NAME`). Do not point
two instances at the same data. This repository has no automated restore launcher.

## Variables in .env

| Variable | Default | Meaning |
| --- | --- | --- |
| NC_TRUSTED_DOMAINS | localhost 127.0.0.1 | Space-separated accepted hostnames; add the actual private hostname |
| NC_ADMIN_USER | ncadmin | First-install bootstrap account, not a later rename mechanism |
| HTTP_PORT | 8080 | Host loopback port; adjust tunnel/proxy accordingly |
| TZ | Etc/UTC | Container time zone; set a real IANA zone if needed |
| PHP_UPLOAD_LIMIT | 2G | PHP upload configuration; other proxy/client limits still apply |

Image tags/digests are literal in compose.yaml for auditable updates. Pins are the
baseline from the originating deployment; review current advisories before use.
Version pinning provides reproducibility, not immunity to vulnerabilities.

## Secret files

`init` creates `db_name`, `db_user`, `db_password`, `admin_password` beneath
`secrets/`. The directory uses mode 0700 on POSIX; files are read-only and readable
by container users through individual Compose secret mounts. The private parent
prevents unrelated host accounts from traversing to them. Keep the checkout on a
local POSIX filesystem with working permissions; Windows initialization does not
establish equivalent Linux permissions and is for development tests only.

Compose secrets are mounted files, not encrypted storage. Protect the host,
Docker access, config.php and backups. The existing database has independent
credentials after initialization: replacing a secret file is not a database
password rotation. Rotations need a coordinated application/database procedure.
If initialization is interrupted, inspect the partial files; the tool refuses
to guess what can safely be overwritten.

## Background work

Cron shares html, backend and outbound networks with app, uses init and SIGTERM,
and starts only after app is healthy. Configure `background:cron` explicitly.
Its process being running does not prove the last job succeeded. Check the
Nextcloud administration page and application logs after at least one cron cycle.
There is no automatic power-off policy or backup scheduler in this baseline.

## Optional modules

See [repository boundaries and interfaces](modules.md) and [Talk services](talk.md).
The core stack does not automatically install software or provision TURN/HPB.
