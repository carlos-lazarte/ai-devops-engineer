---
type: procedure
domain: platform
difficulty: advanced
status: active
tags:
  - kustomize
  - deployment
---
# Kustomize Deployment

Render first:

```bash
kubectl kustomize 43_ENTERPRISE_DEPLOYMENT/kubernetes/overlays/staging
```

Apply only after review:

```bash
kubectl apply -k 43_ENTERPRISE_DEPLOYMENT/kubernetes/overlays/staging
```

The `prod` overlay adds topology spread constraints and retains the baseline PDB and security posture. Replace the placeholder image and secret strategy before use.
