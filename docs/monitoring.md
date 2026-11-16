# Optional monitoring module

Monitoring now has its own repository:
**[HomeServer-Monitoring](https://github.com/Fogbose/HomeServer-Monitoring)**.
Its architecture, dashboard, probes, guarded shutdown/recovery references and
synthetic SSO tests belong there rather than inside this Nextcloud starter.

No monitoring service or dependency is added by this documentation change.
The base Compose still runs Nextcloud, cron, PostgreSQL and Redis only. Deploy
an observation/control plane separately and register each additional service
with your own backup and shutdown policy before treating it as manageable.

The monitoring console can sleep with its admin PC. A missing network response
cannot distinguish off/sleep/failure without an independent observer. Do not add
automatic WOL or a sleep inhibitor to conceal telemetry gaps. Hardware/energy
claims require physical tests and measurements.

Review the module's [recovery guidance](https://github.com/Fogbose/HomeServer-Monitoring/blob/main/docs/operations.md)
before using privileged helpers: persist preparation ownership, refuse foreign
maintenance/migrations, preserve Compose overrides, use sufficiently long start
timeouts and provide a tested resume path. No automatic shutdown is enabled.

For shared login, a dedicated administration origin separates monitoring from
end-user Nextcloud apps. Keep MFA, strict TLS and independent SSH recovery.
Cockpit system elevation is distinct from an SSO browser session. The SSO module
is experimental and must not be described as deployed based solely on lab tests.
