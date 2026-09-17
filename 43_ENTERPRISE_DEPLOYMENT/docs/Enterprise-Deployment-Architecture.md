---
type: architecture
domain: platform
difficulty: advanced
status: active
tags:
  - kubernetes
  - helm
  - enterprise
---
# Enterprise Deployment Architecture

## Reference topology

```text
                           Enterprise Identity
                                  │
                              OIDC / SSO
                                  │
                                  ▼
                       ┌────────────────────┐
                       │ Ingress / Gateway  │
                       └─────────┬──────────┘
                                 │
                                 ▼
                     ┌─────────────────────────┐
                     │ AI DevOps Runtime       │
                     │ Deployment               │
                     └───────┬──────┬──────────┘
                             │      │
                  ┌──────────┘      └──────────┐
                  ▼                            ▼
             Knowledge/RAG                 Claude API
                  │                            │
                  ▼                            ▼
             Vault / Index                 External API
                  │
                  ▼
              Audit Store
                  │
                  ▼
        Observability / SRE Control Plane
```

## Boundaries

- The runtime container is stateless from the platform perspective. The reference deployment mounts the knowledge source read-only from a PersistentVolumeClaim; enterprise installations may replace this with an immutable artifact, CSI-backed source, object-store sync, or another approved distribution mechanism.
- Secrets are referenced from Kubernetes Secret objects or an external secret manager; plaintext credentials are not committed to Git.
- Production change execution remains disabled by the platform baseline unless separately designed, authorized, tested, and approved.

## Availability baseline

The reference production overlay uses two runtime replicas, a PodDisruptionBudget, topology spread constraints, resource requests/limits, and readiness/liveness/startup probes. These are starting points, not universal sizing values.
