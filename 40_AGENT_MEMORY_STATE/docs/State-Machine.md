# Stateful Agent State Machine

Allowed states:

```text
CREATED
CONTEXT_BUILT
ANALYZING
PROPOSAL_READY
AWAITING_APPROVAL
APPROVED
REJECTED
EXECUTED
VERIFIED
CLOSED
FAILED
EXPIRED
```

## Key invariants

- `EXECUTED` requires an explicit approved transition and an external execution capability.
- `VERIFIED` requires a verification event; the model cannot self-attest execution.
- `CLOSED` must retain a final outcome summary and provenance.
- `EXPIRED` is terminal for working-memory tasks and cannot be used as authorization.
