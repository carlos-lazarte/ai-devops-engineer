---
type: runbook
domain: kubernetes
technology: kubernetes
status: active
risk: high
tags:
  - kubernetes
  - capacity
---

# Runbook — Node Capacity Pressure

## Symptoms

Pending pods, high node utilization, eviction pressure, or scheduling failures.

## Diagnostics

```bash
kubectl get nodes
kubectl describe node <node>
kubectl get pods -A --field-selector=status.phase=Pending
```

## Reasoning

Separate workload request pressure from actual usage. Inspect taints, affinity, topology constraints and available allocatable capacity.

## Remediation

Use approved node scaling or capacity changes. Do not bypass admission, change-management or cloud identity controls.

## Verification

Pending pods return to zero or an approved baseline; scheduling events stop; SLOs remain within objective.
