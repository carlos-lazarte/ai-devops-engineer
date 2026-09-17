---
type: checklist
domain: platform
difficulty: advanced
status: active
tags:
  - verification
  - deployment
---
# Enterprise Deployment Verification

## Kubernetes

- [ ] Namespace exists.
- [ ] ServiceAccount exists.
- [ ] Deployment available replicas match the intended count.
- [ ] No unexpected CrashLoopBackOff or ImagePullBackOff.
- [ ] Readiness probes are green.
- [ ] PDB exists for the production profile.
- [ ] NetworkPolicy is present where supported.

## Runtime

- [ ] `/api/v1/health` returns success.
- [ ] `/api/v1/ready` returns success.
- [ ] `/api/v1/version` reports the expected release.
- [ ] `/api/v1/metrics` is reachable from the metrics path.
- [ ] Search smoke test succeeds against the mounted/remote knowledge source.

## Security

- [ ] No credential values are present in manifests.
- [ ] TLS termination is configured according to the platform standard.
- [ ] ServiceAccount token automount is disabled unless needed.
- [ ] Pod security baseline is enforced by cluster policy.

## Rollout completion

- [ ] Audit trail verified.
- [ ] Alerting/monitoring verified.
- [ ] Release artifact and checksum recorded.
