# Kubernetes Closed-Loop Demo

Synthetic example only.

```text
PLAN
 ↓
Approval
 ↓
Simulated remediation
 ↓
Observe kubelet / node health
 ↓
Verify
```

### Successful verification

```text
VERIFIED
 ↓
CLOSED
```

### Failed verification

```text
FAILED
 ↓
REPLANNING
```

No Kubernetes API is contacted by the reference implementation.
