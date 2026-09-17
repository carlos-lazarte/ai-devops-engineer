---
type: reference
domain: ai
status: active
---

# Agent Task Contract

## Input

```json
{
  "task_id": "string",
  "intent": "string",
  "scope": "string",
  "constraints": [],
  "evidence_refs": [],
  "requested_output": "string"
}
```

## Output

```json
{
  "task_id": "string",
  "status": "completed|needs_review|blocked|failed",
  "facts": [],
  "observations": [],
  "hypotheses": [],
  "recommended_diagnostics": [],
  "proposed_actions": [],
  "unknowns": [],
  "provenance": []
}
```

The contract intentionally separates facts from hypotheses and proposed actions.
