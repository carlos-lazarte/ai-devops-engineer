# Kubernetes Secret Reference Pattern

Prefer an external secret manager integration over embedding literal secret values in Git-managed manifests.

```text
Kubernetes workload
   ↓
Workload identity
   ↓
External secret manager
   ↓
Pod secret projection
```

This document is a pattern only. Provider-specific controllers and CRDs must be evaluated and secured independently.
