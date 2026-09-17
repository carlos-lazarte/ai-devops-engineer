---
type: procedure
domain: platform
difficulty: advanced
status: active
tags:
  - helm
  - deployment
---
# Helm Deployment

## Render before applying

```bash
helm lint 43_ENTERPRISE_DEPLOYMENT/helm/ai-devops-platform
helm template ai-devops ./43_ENTERPRISE_DEPLOYMENT/helm/ai-devops-platform \
  -n ai-devops \
  --values 43_ENTERPRISE_DEPLOYMENT/config/platform-values.yaml
```

## Install/upgrade

Use an immutable image digest and an approved secret-management path:

```bash
helm upgrade --install ai-devops \
  ./43_ENTERPRISE_DEPLOYMENT/helm/ai-devops-platform \
  -n ai-devops --create-namespace \
  --values 43_ENTERPRISE_DEPLOYMENT/config/platform-values.yaml
```

## Verify

```bash
kubectl -n ai-devops rollout status deploy/ai-devops-runtime
kubectl -n ai-devops get pods -o wide
```
