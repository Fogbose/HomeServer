# Upstream references and provenance

Consulted during preparation on 2026-11-07. The project is an original community
adaptation of a personal deployment; private configurations, machine identities,
snapshots and operational history are not included. The four-service topology and
pinned baseline derive from that deployment; portability is tested separately.

- [Nextcloud Docker image documentation](https://github.com/nextcloud/docker)
- [Nextcloud requirements](https://docs.nextcloud.com/server/stable/admin_manual/installation/system_requirements.html)
- [Nextcloud backup](https://docs.nextcloud.com/server/stable/admin_manual/maintenance/backup.html)
- [Nextcloud restore](https://docs.nextcloud.com/server/stable/admin_manual/maintenance/restore.html)
- [Docker Engine on Debian](https://docs.docker.com/engine/install/debian/)
- [Compose secrets](https://docs.docker.com/compose/how-tos/use-secrets/)
- [PostgreSQL 17 dump reference](https://www.postgresql.org/docs/17/app-pgdump.html)
- [Tailscale Serve](https://tailscale.com/docs/features/tailscale-serve)
- [GitHub community practices](https://docs.github.com/en/repositories/creating-and-managing-repositories/best-practices-for-repositories)

No third-party binaries, container images, logos or license texts other than the
project's standard MIT license are vendored. Components fetched by Docker remain
under their own licenses; MIT applies to this repository's original material.
