---
name: secret-backup
description: "Back up or restore secret files with an existing encrypted provider and locally configured manifest."
---

# Secret Backup

## Inventory and authorization

Use the user's approved encrypted provider, its actual available tooling and locally configured manifest. List intended file paths, destination and operation statuses without printing, quoting or summarizing secret values. Never ask for a pasted credential; use the provider’s normal interactive login or secure local configuration. Do not assume a bundled script, provider quota or storage format.

Check the exact scope, overwrite behavior and applicable authorization before a backup or restore. A request to back up does not imply permission to overwrite local files during restore. Exclude unrelated sensitive data. If no suitable provider tool is available, offer manual provider-native steps rather than inventing integration.

## Execute and verify

Use a paths-only manifest when supported; preserve binary data and line endings. Transfer changed files through the approved provider, without leaking contents through commands or logs. Track per-file success and failure and do not report an incomplete batch as complete. Verify recoverability and integrity with provider-supported checks or exact-byte hashes without exposing contents. Avoid insecure temporary files; if required, restrict access and clean up according to the system policy.

On restore, inventory destination conflicts first and skip existing files unless overwriting is specifically authorized. Verify restored bytes and report paths and statuses only. Authentication and encryption remain under the user’s control.
