# Roadmap

This file separates completed infrastructure from proposed work. Unchecked items are not claimed as implemented.

## Recovery completed

- [x] Restore persistent host access through Tailscale.
- [x] Verify host access from a separate network.
- [x] Back up cloud filesystem blocks before repair and test repairs on a copy.
- [x] Give the Cloud VM exclusive ownership of its data disk.
- [x] Restore private guest DHCP, DNS, and internet access.
- [x] Expand the Cloud VM's full root filesystem using its existing LVM space.
- [x] Restore Nextcloud, MariaDB, Redis, Ollama, and Open WebUI.
- [x] Verify automatic startup after a controlled host reboot.

## Reliability and acceptance

- [ ] Create an independent external or offsite backup.
- [ ] Test restoration of files, the Nextcloud database, configuration, and VM state.
- [ ] Establish a scheduled backup and retention policy.
- [ ] Complete Nextcloud login, upload/download, and sync acceptance tests.
- [ ] Track Tailscale key expiry and choose a deliberate server expiry policy.
- [ ] Review firewall enforcement and guest forwarding together.
- [ ] Review firmware variables storage and package updates in a maintenance window.
- [ ] Validate the existing video-processing worker end to end.

## Lightroom to Nextcloud

The goal is to preserve originals, visible edits, album organization, and search by album title. A previously discussed library estimate was about 631 GB; a new inventory is required before transferring it.

- [ ] Inventory albums, nesting, unique assets, videos, unfiled images, and multi-album membership.
- [ ] Confirm destination space, quota, staging location, and backup capacity.
- [ ] Test one representative album before choosing an export method.
- [ ] Map albums to named folders and preserve title mappings in a manifest.
- [ ] Preserve originals and metadata; export rendered versions where needed to retain edits outside Adobe.
- [ ] Transfer in logged, restartable batches through a supported Nextcloud interface.
- [ ] Reconcile counts and checksums and test search on computer and phone.
- [ ] Keep the original collection until the migrated copy has been verified and separately backed up.

Album-folder search and semantic photo search are different requirements. Finding a named folder does not automatically mean every image matches its parent's album title.

## AI learning project

A photography curator was proposed to connect the photo collection with the AI server. Other ideas were a homelab incident investigator, document intake system, or ticket-triage system. No completed implementation is claimed here.

The photography idea would use a small copied sample, compare ordinary metadata search with AI tags and semantic retrieval, and evaluate results with human approval. Learning goals include classification versus clustering, embeddings, model selection, inference, retrieval, hallucinations, precision and recall, privacy, latency, and cost. A small AWS comparison was proposed as part of AWS AI Practitioner preparation; no AWS deployment or certification outcome is claimed.

## Administration assistant

A future assistant could inspect health, check disks, request backups, and restart approved services. It should use restricted access, allowlisted actions, logs, and confirmation for destructive changes before adding broader computer or phone control. Existing AI chat services do not establish that this execution layer exists.
