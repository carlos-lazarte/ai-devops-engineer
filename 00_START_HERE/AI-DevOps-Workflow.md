---
type: workflow
domain: ai
status: active
tags:
  - ai
  - incident-response
  - workflow
---

# AI DevOps Workflow

## Operational loop

```text
Incident
  ↓
Collect Evidence
  ↓
Normalize Context
  ↓
Retrieve Relevant Knowledge
  ↓
AI Analysis
  ↓
Generate Hypotheses
  ↓
Human Validation
  ↓
Action
  ↓
Verification
  ↓
Postmortem
  ↓
Knowledge Update
```

## Rules for production use

1. Never fabricate missing evidence.
2. Separate facts, observations, hypotheses and conclusions.
3. Require explicit validation before destructive or high-impact actions.
4. Include rollback or recovery considerations.
5. Preserve timestamps and source evidence.
6. Capture the final outcome so future incidents become easier.

## Suggested AI output structure

- Facts
- Symptoms
- Evidence
- Hypotheses
- Evidence supporting each hypothesis
- Evidence against each hypothesis
- Missing evidence
- Safe next diagnostics
- Potential actions
- Verification plan
