# Security policy

This is an early community starter without a security-maintenance SLA. Only the
current main branch is considered for fixes; no released-version support matrix
or security audit is claimed. Review upstream image advisories independently.

## Report privately

Use the repository's **Security → Report a vulnerability** form when available:
[private vulnerability report](https://github.com/Fogbose/HomeServer/security/advisories/new).
Do not open a public issue containing exploit details, credentials or private
configuration. If private reporting is unavailable, do not post those details;
ask the maintainer for a private channel using a minimal public issue with no
sensitive content. There is no guaranteed response time.

Include affected revision, a minimal sanitized reproduction, impact and suggested
mitigation. Do not scan or attack anyone's home server to demonstrate a flaw.
This repository does not authorize tests against the maintainer's infrastructure.

If a real secret is leaked, revocation/rotation is required; removing a file in
the latest commit cannot invalidate copies already made. Never attach .env,
config.php, private keys, raw backups, packet captures or unredacted logs.
