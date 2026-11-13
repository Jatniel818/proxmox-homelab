# Configuration examples

These files illustrate selected parts of the recovered design. They use replacement values and are not exact copies of the live environment.

**Do not apply them blindly.** Review interface names, addressing, disk identity, service paths, firewall behavior, and current configuration first. Network changes can remove remote access.

| File | Purpose |
|---|---|
| `interfaces.example` | Separate DHCP uplink from private VM bridge |
| `dnsmasq.conf.example` | DHCP reservations and DNS on the private bridge only |
| `guest-forwarding.conf.example` | Persistent IPv4 forwarding |
| `docker-cloud-storage.conf.example` | Require the cloud mount before starting Docker |
| `guest-nat-rule.example` | NAT rule and idempotent service pattern |

The example subnet is `192.168.50.0/24`. Example MAC addresses are locally administered placeholders. The physical cloud disk's serial, UUID, actual addresses, SSH identities, and personal Compose secrets are intentionally absent.

Use a stable `/dev/disk/by-id/<CLOUD_DISK_ID>` path in the Cloud VM definition and a filesystem UUID for its mount inside the guest. Do not add a competing host mount of that filesystem.
