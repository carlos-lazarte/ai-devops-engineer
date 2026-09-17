---
type: runbook
domain: platform
difficulty: advanced
risk: high
status: active
tags:
  - deployment
  - kubernetes
---
# Runbook — Enterprise Deployment

## Preconditions

- Approved release artifact and checksum.
- Target Kubernetes cluster and namespace.
- Registry access and image policy satisfied.
- Secret references created through the approved secret-management path.
- Ingress/TLS requirements defined.
- Rollback version identified.

## Procedure

1. Apply the namespace and service account configuration.
2. Apply the selected Helm values or Kustomize overlay.
3. Confirm Deployment rollout status.
4. Verify `/health`, `/ready`, and `/api/v1/version` through an internal path.
5. Verify Prometheus scraping or the organization's telemetry path.
6. Verify audit events are written according to the selected storage design.
7. Perform the platform conformance and smoke checks.

## Rollback

Use the previous immutable image digest/release artifact. Confirm the rollback target before execution.

## Post-deployment verification

```bash
kubectl -n ai-devops get deploy,pods,svc
kubectl -n ai-devops rollout status deploy/ai-devops-runtime
kubectl -n ai-devops get events --sort-by=.lastTimestamp
```

Then run the API smoke test documented in `docs/Deployment-Verification.md`.
