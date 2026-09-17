# Human Approval Model

Approval is explicit and action-specific.

An approval record contains:

`approval_id`, `request_id`, `approver_identity`, `decision`, `scope`, `expires_at`, `reason`, `timestamp`.

Rules:

1. No approval means no gated action.
2. Approval is scoped to the requested action, tenant and environment.
3. Expired approval is invalid.
4. A planner handoff does not imply approval.
5. Rejection is terminal for that request, but the commander may create a different request after new evidence.
6. Emergency/production changes remain disabled in this reference implementation.
