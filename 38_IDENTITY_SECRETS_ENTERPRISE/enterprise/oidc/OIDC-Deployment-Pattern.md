# OIDC Deployment Pattern

```text
User / Workload
      ↓
Identity Provider
      ↓
OIDC token
      ↓
AI DevOps Runtime
      ↓
JWT/OIDC validation
      ↓
Normalized Principal
      ↓
Policy Engine
```

The authorization decision must use the normalized principal rather than trusting an unverified claim supplied by the caller.
