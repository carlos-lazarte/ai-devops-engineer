---
type: architecture
domain: ci-cd
technology: GitOps
difficulty: intermediate
status: active
tags: [architecture, ci-cd]
---
# Architecture — GitOps-Deployment

## Objective
Describe the pattern and its main operational boundaries.

## Flow
```text
Commit → CI validation → Git desired state → Deployment controller → Cluster → Observability
```

## Design notes
Git-centric deployment improves auditability; it requires disciplined promotion, controller availability, and drift handling.

## Failure considerations
Document dependency failures, degraded modes, recovery, and observability for the real environment.
