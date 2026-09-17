---
type: reference
domain: kubernetes
difficulty: beginner
status: active
tags: [cheatsheet, kubernetes]
---
# Cheatsheet-Kubernetes-First-Response

```bash
kubectl get nodes
kubectl get pods -A
kubectl get events -A --sort-by=.lastTimestamp
kubectl describe pod <pod>
kubectl logs <pod>
kubectl logs <pod> --previous
```

Always review context and impact before running commands in production.
