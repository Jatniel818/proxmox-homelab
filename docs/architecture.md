# Architecture

## Host and network

The Proxmox host uses DHCP on its onboard Ethernet port. A private Linux bridge connects the VMs without bridging their MAC addresses onto the physical uplink. The host supplies IPv4 forwarding and source NAT for outbound guest traffic.

For documentation, the examples use `192.168.50.0/24`. These addresses are replacements, not the live environment:

| Example role | Address |
|---|---|
| Host identity on the private bridge | 192.168.50.100 |
| Guest gateway and DNS | 192.168.50.1 |
| Cloud VM | 192.168.50.32 |
| AI VM | 192.168.50.6 |

A dedicated dnsmasq instance binds only to the private bridge and supplies DHCP reservations. Its upstream DNS follows the host resolver. A systemd oneshot service adds an idempotent NAT rule without flushing Tailscale's existing chains.

Tailscale runs on the host and both guests. Administrators reach the host directly for Proxmox or SSH and reach applications through the relevant guest's Tailscale address. Application port 8080 is used independently on both VMs; the guest addresses distinguish Nextcloud from Open WebUI.

At the last check, the Proxmox firewall was disabled, although both VM NIC configurations retained `firewall=1`. This should not be represented as a fully enforced firewall policy. Enabling enforcement later requires checking guest forwarding and NAT deliberately.

## Storage ownership

The system SSD holds Proxmox root storage and the LVM thin pool containing the VM system disks. The Cloud VM receives the whole dedicated data disk through a stable `/dev/disk/by-id/` path. Inside that guest, its ext4 partition mounts at `/mnt/cloud` using a filesystem UUID.

**Only the Cloud VM mounts this data filesystem.** Mounting the same ext4 filesystem read-write on the host and guest can corrupt it. A stable device path protects against drive-name changes; it does not make simultaneous ownership safe.

The Cloud VM's Docker service requires `/mnt/cloud` and checks that the path is an actual mountpoint before starting. This prevents a missing mount from silently redirecting data writes into the guest root filesystem.

The thin-pool OS snapshots do not include the raw physical cloud drive. Restoring a system disk must be coordinated with the application and database state on that drive.

## Cloud VM

- Two virtual CPU cores and 4032 MiB memory.
- A 50 GiB SCSI virtual system disk with the VirtIO SCSI single controller and I/O thread enabled.
- The dedicated data disk attached through VirtIO.
- Ubuntu root volume expanded from about 24 GiB to 44 GiB using existing free space in its volume group.
- Nextcloud, MariaDB, and Redis managed through Docker Compose.

| Guest path | Container path | Purpose |
|---|---|---|
| /mnt/cloud/nextcloud/db | /var/lib/mysql | MariaDB data |
| /mnt/cloud/nextcloud/redis | /data | Redis data |
| /mnt/cloud/nextcloud/app | /var/www/html | Nextcloud application and configuration |
| /mnt/cloud/nextcloud/data | /var/www/html/data | Nextcloud file data |

The Nextcloud container publishes guest port 8080 to container port 80. The database and Redis are not individually published to the guest's external interfaces. A separate FFmpeg worker container was observed running; its full workflow was not validated.

## AI VM

- Four virtual CPU cores using the host CPU model and 16 GiB memory.
- An 82 GiB virtual system disk, OVMF firmware, and q35 machine type.
- NVIDIA GTX 1650 passed through as a PCIe device; 4 GiB VRAM recognized inside the guest.
- Ollama runs as a service on port 11434.
- Open WebUI runs in Docker using host networking on port 8080.

The recorded NVIDIA driver was 535.309.01. GPU recognition was tested separately from a successful small-model inference. The inference test alone is not a GPU throughput benchmark or evidence that every listed model uses GPU acceleration.

## Startup

Cloud starts before AI, with a 30-second startup delay assigned to each VM and a 120-second shutdown allowance. Both retain Proxmox automatic startup. The host's separate Ollama service stays disabled; the verified Ollama installation runs in the AI guest.

A controlled host restart verified that the uplink, private bridge, Tailscale, both VMs, data mount, Docker workloads, and application interfaces returned. Open WebUI took additional time to finish initializing after the VM itself was running.
