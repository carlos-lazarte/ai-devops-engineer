---
type: troubleshooting
domain: kubernetes
technology: Kubernetes
difficulty: beginner
severity: medium
status: active
tags: [kubernetes, troubleshooting]
---
# Troubleshooting-Kubernetes-ImagePullBackOff

Repeated image pull failures require checking the image reference, registry access, network path, and credentials.

## First checks
```bash
kubectl describe pod <pod>
kubectl get events --sort-by=.lastTimestamp
```

## Common causes
- Wrong repository/tag
- Registry unreachable
- Authentication failure
- DNS/network issue
- Registry policy or rate limit

## Verification
Confirm the Pod becomes Running/Ready and health checks pass.
