---
type: troubleshooting
domain: linux
technology: Linux
difficulty: intermediate
severity: medium
status: active
tags: [linux, troubleshooting]
---
# Troubleshooting-Linux-High-Memory

High memory utilization is not by itself proof of a memory fault; inspect pressure, swap, OOM events, and workload behavior.

## First checks
```bash
free -h
vmstat 1 5
ps -eo pid,ppid,comm,%mem,rss --sort=-rss | head
```

## Evidence
Capture memory usage, swap activity, top processes, timing, and application symptoms.

## Related
[[Prompt-Incident-Analysis]]
