# Private HTTPS and family access

Start with the loopback listener and an SSH tunnel. For regular private remote
access, Tailscale Serve is one option; any equivalent well-configured private
proxy can be used. This guide is a procedure to adapt, not an automatic installer.

## Tailscale option

1. Install/authenticate Tailscale on the server and client using its official
   instructions. Keep your existing verified SSH access while changing networking.
2. Decide which people/devices may reach the server. Preserve admin SSH rules;
   allow only HTTPS to ordinary users. Granting a user identity can cover several
   devices, while device-specific rules are narrower. Check the actual policy.
3. Enable the tailnet DNS/HTTPS features required by Serve. Obtain the actual
   server FQDN from Tailscale, not an example copied from another deployment.
4. Add that FQDN to `NC_TRUSTED_DOMAINS` in .env and recreate app/cron during an
   approved maintenance window. Keep the localhost entries if using tunnels.
5. On the server, after checking port/proxy conflicts, configure private Serve:

```sh
sudo tailscale serve --bg http://127.0.0.1:8080
tailscale serve status
```

Use Serve, **not Funnel**. Verify from an authorized remote client and a denied
client. A certificate's public transparency record does not make the endpoint
public, but it may reveal the hostname. Do not include personal names in it.

## Nextcloud proxy settings need an explicit deployment decision

The baseline intentionally does not trust an arbitrary proxy or force HTTPS.
Inspect the source address Nextcloud actually receives from your host proxy
(often a Docker bridge gateway), then configure the exact trusted proxy, external
host, protocol and CLI URL using Nextcloud's official reverse-proxy documentation.
Do not trust all of 0.0.0.0/0 or guess the gateway. A malicious trusted forwarder
can spoof client addresses and affect access controls.

Validate login, uploads, client IP handling, WebDAV and CalDAV/CardDAV discovery.
The `/.well-known/caldav` and carddav redirects must retain HTTPS and the real
host. Proxy-specific Apache changes from the original private deployment are not
automatically applied here. Keep them versioned in a local override if required;
never put private configuration in a public issue.

## Family onboarding

Share the server with a personal invitation or use another explicitly designed
tailnet membership policy; verify the resulting HTTPS access rules. Each person
uses their own Tailscale identity and a separate non-admin Nextcloud account.
Set quotas and sharing permissions deliberately. An invitation is not a Nextcloud
account, and an installer cannot replace the user's consent and authentication.

When the server is powered off its Tailscale endpoint is off too. Remote wake-up
needs another authorized always-on device at home; see [power](power.md).

Sources: [Serve](https://tailscale.com/docs/features/tailscale-serve),
[sharing](https://tailscale.com/docs/features/sharing),
[Nextcloud proxy settings](https://docs.nextcloud.com/server/stable/admin_manual/configuration_server/reverse_proxy_configuration.html).
