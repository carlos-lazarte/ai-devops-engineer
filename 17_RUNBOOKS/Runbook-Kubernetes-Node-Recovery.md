---
type: runbook
domain: kubernetes
technology: Kubernetes
difficulty: advanced
risk: high
status: active
tags: [runbook, kubernetes]
---
# Runbook-Kubernetes-Node-Recovery

## Purpose
Recover a NotReady node while minimizing workload disruption.

## Procedure
1. Inspect node conditions and events.
2. Check kubelet and container runtime.
3. Check disk/memory pressure and network reachability.
4. Cordon/drain only when approved and appropriate for workload/PDB constraints.
5. Correct the underlying fault.
6. Restore services and verify readiness.

## Escalation
Escalate when control-plane connectivity, storage integrity, or host hardware is implicated.

Related: [[Troubleshooting-Kubernetes-Node-NotReady]]
