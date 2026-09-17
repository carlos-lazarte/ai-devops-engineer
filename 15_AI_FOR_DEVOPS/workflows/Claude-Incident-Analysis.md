---
type: workflow
domain: ai
task: incident-analysis
status: draft
tags:
  - ai
  - claude
  - incident
---

# Claude Incident Analysis

## Inputs

- incident timeline
- alert details
- logs
- metrics
- traces where available
- deployment/change history
- relevant runbooks
- architecture notes

## Analysis sequence

```text
Timeline reconstruction
        ↓
Fact extraction
        ↓
Signal / noise separation
        ↓
Hypothesis generation
        ↓
Evidence mapping
        ↓
Missing evidence
        ↓
Next diagnostics
        ↓
Human validation
```

## Required behavior

Claude must not rewrite uncertain statements as facts. Time ordering should be explicit. Correlation must not automatically be treated as causation.

## Deliverables

- incident summary
- timeline
- hypotheses
- evidence matrix
- recommended diagnostics
- candidate contributing factors
- draft postmortem inputs
