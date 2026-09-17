---
type: procedure
domain: sre
status: active
tags:
  - kubernetes
  - operations
  - gitops
---

# Operating Model

## Desired state

The production platform should converge toward a declarative desired state stored in version control.

## Operational loop

1. Observe health, saturation, errors and latency.
2. Correlate alerts with deployment and change history.
3. Retrieve the relevant runbook and evidence.
4. Propose a change through Git or an approved automation pathway.
5. Validate in staging.
6. Promote through the environment overlays.
7. Verify rollout, SLOs and audit events.
8. Record the result and update knowledge when a durable lesson is discovered.

## Safety

Production execution remains subject to identity, policy, approval and change-management controls. Kubernetes access is not granted merely because an AI agent can generate a manifest.
