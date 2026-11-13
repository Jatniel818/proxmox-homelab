# Operations and troubleshooting

Examples use placeholders. They are reference commands, not a deployment script.

## Connect and inspect

Connect the client to Tailscale before opening the Proxmox interface or SSH:

```sh
ssh root@<HOST_TAILSCALE_IP>
qm list
systemctl --failed
systemctl is-active tailscaled pveproxy homelab-guest-dns homelab-guest-nat
ip -br address
ip route
```

Host Tailscale SSH may require account verification. An unexpected SSH host key should be verified against a trusted record before changing known-hosts entries. Proxmox's web interface uses its private certificate authority; browser certificate trust should be reviewed separately.

If applications fail while Proxmox is reachable, inspect the relevant VM first. A frozen local monitor alone is not a reason to force a power-off, especially when a display GPU is passed through to a guest.

## Cloud VM

```sh
findmnt /mnt/cloud
df -h / /mnt/cloud
systemctl --failed
cd /home/<USER>/nextcloud-stack
docker compose ps
docker exec -u www-data <NEXTCLOUD_CONTAINER> php occ status
```

Check that the data filesystem is actually mounted before restarting Docker or writing application data. If a direct private-IP request returns an untrusted-domain response, test the intended hostname or Tailscale address rather than treating it immediately as a database failure.

## AI VM

```sh
nvidia-smi
systemctl is-active ollama docker tailscaled
docker inspect open-webui --format '{{.State.Health.Status}}'
curl http://127.0.0.1:11434/api/tags
```

Allow Open WebUI to finish initialization after reboot. Check its health and recent logs before repeatedly restarting it. Model discovery alone does not validate inference for every model.

## Storage rules

- Do not mount the cloud filesystem on the host while the Cloud VM owns it.
- Do not run filesystem repair against a mounted filesystem or a disk in use by a VM.
- Verify disk identity with stable paths before any disk operation.
- Do not delete Docker volumes, Nextcloud directories, or `lost+found` simply to free space.
- Coordinate system-disk rollback with database and application data on the physical drive.
- Keep external backups and validate a restore before treating the recovery design as complete.

## If the host is unreachable

Check client Tailscale, host power, Ethernet link, and the uplink connection. DHCP leases can change. Expired Tailscale keys can interrupt access even when the machine is otherwise healthy.

If physical recovery is required, inspect the existing installation from a recovery environment before reinstalling. A GRUB prompt is not a Linux login, and a clean root-filesystem message does not establish that all later mounts and services succeeded.
