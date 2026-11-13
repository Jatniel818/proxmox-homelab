# Validation record

The following results were recorded during recovery on November 8 and 9, 2026. This repository does not poll the live environment or assert current uptime.

| Check | Recorded result | Limit |
|---|---|---|
| Host access from another network | SSH and Proxmox worked from a phone hotspot | Depends on power, internet, and valid Tailscale authentication |
| Proxmox web TLS | HTTP 200; certificate verified against the host CA retrieved through authenticated SSH | Browser trust configuration is separate |
| Host and guest services | No failed systemd units listed after restart | Not an exhaustive log or security audit |
| Cloud filesystem repair | Complete read-only filesystem check passed offline | Not proof of every file's historical integrity |
| Directory comparison | 99,071 path entries matched between original and repaired copy | Compared metadata and names, not all file-content hashes |
| Cloud root capacity | Approximately 19 GiB free after LVM expansion | Snapshot of capacity at the time |
| Nextcloud | Installed; maintenance off; no database upgrade needed; status endpoint responded through Tailscale | User login, upload/download, and sync still need acceptance tests |
| MariaDB | Startup recovery completed and server became ready | Not a full consistency audit of every application record |
| Redis | PONG | Basic service check |
| Database backup | All-databases dump saved and gzip integrity check passed | No full restore drill performed |
| NVIDIA passthrough | GTX 1650 and 4096 MiB detected; NVIDIA tools worked in AI VM | No comprehensive GPU benchmark |
| Ollama | Model discovery and a completed `gemma3:1b` inference returning READY | Other models and cloud-backed tags not all tested |
| Open WebUI | HTTP 200 and healthy, including after reboot | Startup takes longer than initial VM boot |
| Existing FFmpeg worker | Container running after recovery and reboot | End-to-end media processing not tested |
| Controlled host restart | Host, private network, both guests, and applications returned automatically | Not a power-loss stress test or uptime SLA |

Recorded application versions included Nextcloud 33.0.2, MariaDB 11.8.6, and Open WebUI 0.8.12. The installed host's recovered kernel was 6.17.13-2-pve and Tailscale was 1.104.5. These are historical observations, not version recommendations or upgrade instructions.

## Deliberately unclaimed

- A completed Lightroom library migration.
- A completed autonomous administration assistant.
- Independent, offsite, or scheduled backups with a tested restore.
- A fully enforced Proxmox firewall policy.
- Performance or functionality of every model listed by Ollama.
- Production availability, enterprise security, or continuous monitoring.
