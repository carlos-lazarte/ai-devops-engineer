---
type: troubleshooting
domain: kubernetes
technology: kubernetes
difficulty: intermediate
severity: high
status: active
tags:
  - kubernetes
  - crashloopbackoff
---

# Troubleshooting — Kubernetes CrashLoopBackOff

## Symptom

A pod repeatedly starts and terminates, and Kubernetes reports `CrashLoopBackOff`.

## First checks

```bash
kubectl get pod -n <namespace>
kubectl describe pod <pod> -n <namespace>
kubectl logs <pod> -n <namespace>
kubectl logs <pod> -n <namespace> --previous
kubectl get events -n <namespace> --sort-by=.lastTimestamp
```

## Possible causes

- Application exits during startup.
- Invalid configuration.
- Missing secret/config map.
- Image or command problem.
- Resource constraints.
- Probe configuration causes restarts.
- External dependency unavailable.

## Decision tree

1. Does the container log show an application error?
2. Does `--previous` reveal the failure before restart?
3. Do pod events show image, mount or probe errors?
4. Are configuration or secrets present and correct?
5. Are resource limits or node conditions involved?

## Verification

The pod reaches `Running`/`Ready` and remains stable while application metrics and logs are healthy.

## Related

- [[../05_KUBERNETES/]]
- [[../10_OBSERVABILITY/]]
- [[../20_PROMPT_LIBRARY/Prompt-Incident-Analysis]]
