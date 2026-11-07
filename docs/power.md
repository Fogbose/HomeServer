# Sleep, shutdown and Wake-on-LAN

| State | What remains | Return to service |
| --- | --- | --- |
| S3 sleep | RAM and wake-capable hardware remain powered | Resume memory state, then verify network and applications |
| S5 soft off | Main OS stopped; standby power may feed NIC/motherboard | Full boot, then Docker and application readiness |
| AC disconnected | No standby power | Ordinary WOL cannot work |

Support depends on motherboard firmware, NIC, driver, BIOS settings, power state
and cabling. A chipset feature list is not a successful wake test. Some platforms
offer different sleep states; inspect the actual host rather than forcing S3.

The NIC recognizes a magic packet containing its MAC address and signals the
motherboard. Debian and Docker are not running in S5. Validate WOL configuration
and persistence after reboot/shutdown, then repeat wake/resume tests from the
chosen state. Inspect logs and verify Nextcloud, not just ping. Do not change BIOS
or power settings automatically from this project.

## Local sender — Windows or Linux, Python 3.10+

Replace every example with the physical LAN's actual target and sender settings:

```sh
python tools/homeserver.py wake --mac 02:11:22:33:44:55 --network 192.168.10.0/24 --source 192.168.10.2
```

This is a **preview**, not a network test. Add `--send` only after reviewing the
target; the sender binds to the selected local IPv4 and sends one UDP packet to
the subnet broadcast on port 9. Packet delivery and actual wake-up still require
observation. MAC addresses are not authentication; restrict who can trigger wake.

A sleeping/off server cannot receive requests through its own Tailscale client.
Remote wake-up requires a separate always-on, authenticated relay on the home
network. No relay, router port-forward or remote-wake guarantee is provided here.

## Automatic shutdown is deliberately absent

Before implementing it, design checks for active users/transfers, backups,
restores, updates and critical tasks; a shared inhibitor/lock; a configurable
idle period; an immediate pre-shutdown recheck; and graceful app/database stops.
Unknown state or a failed probe must block shutdown. No HTTP requests is not proof
that mobile clients or background jobs are idle. Persistent systemd timers can
catch up after boot but do not power up a machine in S5 by themselves.

Measure power at the wall before claiming savings. Change one setting at a time,
check storage/network/WOL/stability and document rollback. Never apply a blanket
powertop profile or force PCIe power options without testing the hardware impact.
