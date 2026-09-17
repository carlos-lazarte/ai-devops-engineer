---
type: runbook
domain: linux
technology: linux
difficulty: intermediate
risk: medium
environment: production
status: active
tags:
  - linux
  - cpu
  - runbook
---

# Runbook — Linux High CPU

## Purpose

Identify the process or workload responsible for sustained CPU pressure and determine whether the condition is expected, transient or anomalous.

## Preconditions

- Access to the affected host.
- Permission to inspect processes and system metrics.
- Change window approval before modifying production workloads.

## Step 1 — Confirm the condition

```bash
top
uptime
mpstat -P ALL 1 5
```

## Step 2 — Identify top consumers

```bash
ps -eo pid,ppid,user,stat,pcpu,pmem,etime,cmd --sort=-pcpu | head -n 20
```

## Step 3 — Correlate with recent changes

Check deployments, scheduled jobs, configuration changes and workload volume.

## Step 4 — Analyze

Use logs and application metrics to determine whether CPU consumption is caused by expected load, a runaway process, retry loop, inefficient workload or another system dependency.

## Verification

Confirm CPU returns to the expected operating envelope and that application health remains normal.

## Rollback

If a workload was changed, restore the documented previous configuration or deployment according to the service's rollback procedure.
