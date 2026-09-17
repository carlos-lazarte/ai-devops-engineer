---
type: procedure
domain: devops
technology: kubernetes
status: active
tags:
  - gitops
  - drift
---

# GitOps Drift Management

## Desired behavior

Detected drift should be visible, attributable and handled through the approved reconciliation process.

## AI rule

The AI agent may explain drift, correlate it with change records, and prepare a proposed remediation. It must not silently mutate cluster state to hide drift.

## Verification

After reconciliation, compare the cluster state with the expected revision and confirm alerts have cleared.
