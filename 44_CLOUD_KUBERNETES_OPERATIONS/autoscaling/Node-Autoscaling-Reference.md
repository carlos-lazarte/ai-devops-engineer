---
type: architecture
domain: kubernetes
status: active
tags:
  - autoscaling
  - cluster
  - kubernetes
---

# Node Autoscaling Reference

Node autoscaling supplies cluster capacity when workloads cannot be scheduled with the current node pool.

## Interaction with HPA

```text
HPA increases replicas
        ↓
unschedulable pods
        ↓
node autoscaler increases capacity
        ↓
pods schedule
```

This is a coordination problem: HPA, pod requests, scheduler constraints and node autoscaling policy must be evaluated together.

## Guardrails

- define maximum node limits
- use approved node pools
- respect topology requirements
- preserve disruption budgets
- verify cloud IAM and quota availability
- monitor cost and capacity
