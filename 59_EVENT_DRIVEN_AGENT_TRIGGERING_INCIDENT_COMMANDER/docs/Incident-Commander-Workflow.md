# Human-in-the-Loop Incident Commander Workflow

The commander session is a coordination object, not an autonomous production operator.

### Lifecycle

```text
OPENED
  → TRIAGE
  → INVESTIGATING
  → AWAITING_HUMAN
  → APPROVED / REJECTED / EXPIRED
  → PLANNING
  → VERIFIED / CLOSED
```

`PAUSED` may be used when evidence quality is insufficient or a policy check is unresolved.

### Commander packet

Each session records:

- incident candidate reference
- evidence references and provenance
- current hypotheses with confidence
- unknowns / missing evidence
- requested actions
- policy decision
- approval record
- planner handoff reference
- verification status

The commander should explicitly distinguish **fact**, **observation**, **hypothesis**, **proposed action**, and **unknown**.
