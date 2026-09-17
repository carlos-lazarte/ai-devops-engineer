---
type: procedure
domain: devops
status: active
tags:
  - gitops
  - kubernetes
  - deployment
---

# GitOps Operations

## Model

```text
Git change
   ↓
validation
   ↓
review / approval
   ↓
controller reconciliation
   ↓
cluster desired state
   ↓
rollout verification
```

## Rules

- production manifests are declarative
- image references should be immutable where feasible
- every production change has an auditable commit or approved change record
- drift is detected rather than silently corrected by an AI agent
- rollback is performed by reverting or promoting a known-good revision

## AI interaction

The agent may prepare a draft or pull request. The GitOps controller remains the deployment authority.
