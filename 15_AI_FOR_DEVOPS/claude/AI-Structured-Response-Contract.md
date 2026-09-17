---
type: schema
domain: ai
task: response-contract
status: draft
tags:
  - ai
  - structured-output
  - devops
---

# AI Structured Response Contract

## Purpose

Define a stable response shape for Claude outputs used in DevOps analysis.

## Contract

```yaml
summary: string
confidence: low|medium|high
facts:
  - string
observations:
  - string
hypotheses:
  - statement: string
    supporting_evidence:
      - string
    contradicting_evidence:
      - string
    validation_needed:
      - string
recommended_diagnostics:
  - step: string
    rationale: string
    risk: low|medium|high
proposed_actions:
  - action: string
    risk: low|medium|high
    requires_human_approval: true
unknowns:
  - string
references:
  - string
```

## Rules

- `facts` should be directly supported by supplied evidence.
- `hypotheses` are not conclusions.
- `proposed_actions` must indicate risk.
- Production-changing actions require human approval.
- Low confidence should be used whenever evidence is incomplete or conflicting.

## Related

[[AI-Evidence-Handling]]
[[AI-DevOps-Context-Protocol]]
