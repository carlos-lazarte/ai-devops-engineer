---
type: runbook
domain: linux
technology: Linux
difficulty: intermediate
risk: high
status: active
tags: [runbook, linux]
---
# Runbook-Linux-Disk-Recovery

## Purpose
Restore filesystem headroom while preserving evidence and avoiding unsafe deletion.

## Procedure
1. Confirm affected filesystem and service owner.
2. Check `df -h` and `df -i`.
3. Identify top consumers and growth.
4. Check for deleted-open files.
5. Apply the least disruptive approved remediation.

## Verification
Recheck filesystem usage and application health.

Related: [[Troubleshooting-Linux-Disk-Full]]
