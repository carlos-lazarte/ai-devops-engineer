---
type: troubleshooting
domain: kubernetes
technology: Kubernetes
difficulty: intermediate
severity: high
status: active
tags: [kubernetes, troubleshooting]
---
# Troubleshooting-Kubernetes-Node-NotReady

A NotReady node requires checking conditions, kubelet/runtime, pressure, networking, and recent events.

## First checks
```bash
kubectl get nodes
kubectl describe node <node>
kubectl get events --sort-by=.lastTimestamp
```

## Evidence
Collect node conditions, events, kubelet/runtime state, disk/memory pressure, and connectivity to required endpoints.

## Validation
Do not drain/remove the node solely because it is NotReady; validate the failure domain first.

Related: [[Runbook-Kubernetes-Node-Recovery]]
