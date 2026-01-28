# SSH Key Rotation Schedule

## Current Key
- **Created:** 2026-01-28 (assumed - check actual creation date)
- **Location:** `/root/.ssh/authorized_keys`
- **Next Rotation Due:** 2026-04-28 (90 days)

## Rotation Procedure
1. Generate new key pair on client machine: `ssh-keygen -t ed25519 -C "clarke@hetzner"`
2. Add new public key to authorized_keys (keep old one temporarily)
3. Test new key works
4. Remove old key from authorized_keys
5. Update this file with new creation date

## Automated Reminder
Clarke will remind about key rotation 7 days before due date.

## Last Rotation
- **Date:** Never (initial setup)
- **Reason:** N/A
