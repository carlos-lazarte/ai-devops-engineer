---
type: troubleshooting
domain: linux
technology: Linux
difficulty: intermediate
severity: medium
status: active
tags: [linux, troubleshooting]
---
# Troubleshooting-Linux-Disk-Full

Capacity exhaustion may be filesystem blocks, inodes, or space retained by deleted-open files.

## First checks
```bash
df -h
df -i
findmnt
```

## Evidence
Identify the affected filesystem, top consumers, growth pattern, and application symptoms.

## Branches
- Blocks exhausted: inspect large paths.
- Inodes exhausted: inspect file count/small-file workloads.
- Deleted-open files: identify processes holding removed files.

## Verification
Recheck usage and service health after the approved remediation.

Related: [[Runbook-Linux-Disk-Recovery]]
