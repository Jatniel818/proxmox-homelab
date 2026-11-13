# Recovering the homelab without reinstalling

## Problem

The PC appeared stuck after LVM activation and a message that the Proxmox root filesystem was clean. Remote administration was unavailable. Early physical checks included no-signal displays and later static boot output. These symptoms did not establish whether the kernel had crashed or identify the damaged filesystem.

Moving the PC from the home network to a dorm introduced a separate network mismatch: the host still had a home-network bridge and default gateway configuration.

## Diagnosis

A Proxmox installer USB was used in debug mode as a recovery environment. The existing Proxmox installation and data disks were preserved.

Offline inspection established that:

- The host root filesystem passed its read-only check after clean unmounting.
- The separate cloud-data ext4 filesystem had an invalid HTREE directory index for inode 11, `lost+found`.
- The host's automatic mount and filesystem check of that data partition could block normal startup.
- The Cloud VM had raw access to the same physical disk that the host was configured to mount.
- Recovery Ethernet interfaces initially appeared administratively DOWN. Bringing up the correct motherboard NIC produced a 1 Gbps link and a working DHCP lease.

The conflicting mounts were a plausible contributing corruption risk. The evidence did not prove exactly when or how the corruption began.

## Stage one Restore host access

Original host configuration and the Proxmox cluster database were backed up. The cloud mount was temporarily changed to manual, read-only mounting so its failed check would not block host startup. VM autostart was masked while storage remained unresolved.

The physical uplink moved to DHCP. The old home gateway was removed from the private bridge, and the physical NIC was detached from that bridge. Tailscale was installed in the existing host and enabled persistently.

Temporary recovery access had required troubleshooting missing utilities, BusyBox wget options, and SSH host-key availability. Persistent installed-host access replaced that RAM-backed recovery session. SSH host-key changes were checked against the saved configuration rather than accepted blindly.

Host SSH and Proxmox web access were then verified from a phone hotspot. The machine was moved to its permanent dorm position and access was checked again.

## Stage two Protect and repair cloud storage

Both VMs were stopped and the cloud partition remained unmounted. A new 120 GiB logical volume was created on the system SSD for recovery material. No existing data device was formatted.

`e2image -rap` created a sparse image of allocated filesystem blocks, including file contents. The image had approximately 2 TB apparent size and approximately 33 GB of allocated storage. Copying it later requires preserving sparse allocation.

A QCOW2 overlay backed by the unchanged image provided a repair test target. Initial repair and directory rebuild attempts did not pass a subsequent read-only check. A targeted directory-index repair was developed on the copy first, retaining the directory data and preserving the inode's extents flag.

After the test copy passed, directory inventories of the original and repaired copy were compared. The comparison covered relative paths, modes, ownership, regular-file sizes, and symlink targets. The inventories matched across **99,071 path entries**. The populated `lost+found` directory remained present.

Only then was the tested repair applied to the unmounted original, with undo files and logs retained. A complete read-only filesystem check passed, and the filesystem's inode count remained 99,082.

These are structural and inventory checks. They do not prove every file's contents were intact before recovery. The pre-repair image remains important evidence.

## Stage three Restore guests and applications

The host's active data-disk mount was removed. The Cloud VM received exclusive ownership through a stable disk path, and its own data mount moved to a filesystem UUID.

Private DHCP, DNS, IPv4 forwarding, and NAT were configured so guests could use the dorm uplink without bridging directly onto it. DHCP reservations preserved guest addresses within the private network. Both guest Tailscale logins were renewed.

When Cloud booted, its operating-system filesystem was 100 percent full. Its LVM group still had free capacity. Extending the root logical volume by 20 GiB and resizing ext4 online produced a roughly 44 GiB filesystem with about 19 GiB available, without deleting user data.

Docker was started only after the data mount was verified. A systemd mount dependency and explicit mountpoint check were added before enabling normal startup. Nextcloud, MariaDB, Redis, and the existing video worker returned. A fresh logical database dump was saved.

The AI guest detected its GPU, Ollama listed saved models and completed a test inference, and Open WebUI became healthy.

## Verification and lessons

Both guests were shut down cleanly and the host was restarted. Remote access, the private network, automatic VM startup, mounted cloud storage, and applications returned. See [the validation record](validation.md).

The main lessons were to separate a frozen display from verified host state, investigate the filesystem actually blocking startup, maintain one owner for a raw filesystem, back up and test a repair before changing the original, and test restart behavior before relying on remote access.

The backup volume and snapshots still share the host SSD. Independent backups and tested restoration remain unfinished work.
