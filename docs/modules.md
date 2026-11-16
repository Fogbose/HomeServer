# Module boundaries

Three independent MIT repositories separate host infrastructure, applications
and the monitoring control plane:

| Layer | Repository | Responsibility |
| --- | --- | --- |
| Infrastructure | [HomeServer](https://github.com/Fogbose/HomeServer) | Docker, persistence, private ingress, backups, media binaries and operational architecture |
| Software | [HomeServer-Software](https://github.com/Fogbose/HomeServer-Software) | Maison launcher, App Store catalogue, client-kit generator and client guides |
| Monitoring | [HomeServer-Monitoring](https://github.com/Fogbose/HomeServer-Monitoring) | Monitoring architecture, loopback console, telemetry, maintenance guards and isolated SSO lab |
| Upstream apps | Nextcloud App Store | Independently licensed/signed software; installed through Nextcloud, not vendored here |

The base remains usable without Maison, Talk, Memories or any selected app.
Maison can also run on a compatible Nextcloud not deployed with this starter.
Repositories have independent histories and validation; moving software does not
move or delete any deployed application or user data.

Monitoring is optional. This starter still launches four services and does not
install agents, Cockpit, an IdP, new VPN identities or root power helpers. The
monitoring repository owns those reference architectures and their validation
limits; its experimental SSO work is not a production-ready installation claim.
See [the monitoring boundary](monitoring.md).

## Interface contract

Infrastructure provides a supported Nextcloud/PHP runtime, writable persistent
`custom_apps`, working cron, database/Redis, a canonical verified HTTPS origin and
coherent backups. Software consumes Nextcloud's authenticated routes, navigation,
installed icons and user-specific app availability. It receives no Docker socket,
host privileges or VPN credentials. Clients receive the origin and authenticate
normally; no credentials are embedded in a generated kit.

Memories depends on persistent FFmpeg/ffprobe/ExifTool in **both** app and cron.
Talk adds independent [TURN and HPB infrastructure](talk.md). These services are
not PHP app extensions and must be operated, backed up and updated separately.

## Migrating an existing checkout

The catalogue, `tools/build_client_kit.py` and its Python tests moved to the
software repository. Clone it alongside this one, then run its generator there.
Existing `docs/applications.md` and `docs/clients.md` URLs remain as pointers.
No server migration is necessary for this source-code split. Never run a fresh
initializer against an existing production directory.
