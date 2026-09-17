---
type: security
domain: kubernetes
status: active
tags:
  - policy
  - admission
  - security
---

# Kubernetes Admission and Policy

Recommended policy categories:

- disallow privileged containers
- require non-root execution
- restrict hostPath usage
- require resource requests/limits
- restrict image registries
- require approved labels and ownership metadata
- prevent unsafe capabilities

Admission policy is a cluster control. It complements, but does not replace, the platform's application-level policy engine.
