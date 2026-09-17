---
type: workflow
domain: ai
task: incident-analysis
status: active
tags:
  - claude
  - incident
  - e2e
---

# Claude End-to-End Incident Workflow

## Scenario

`K8S-NOTREADY-001`

## Flow

```text
Scenario
  ↓
Evidence loader
  ↓
MCP gateway retrieval
  ↓
Context packet
  ↓
Claude client
  ↓
JSON response
  ↓
Schema validation
  ↓
Human approval
```

## Expected output

- summary
- confidence
- facts
- observations
- hypotheses
- recommended diagnostics
- proposed actions
- unknowns
- references

## Stop conditions

Stop before operational action when:

- context is missing;
- provenance cannot be established;
- response validation fails;
- a proposed action lacks an explicit human-approval flag;
- the model claims an action was executed without execution evidence.
