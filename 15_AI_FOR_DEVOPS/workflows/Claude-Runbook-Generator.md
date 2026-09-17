---
type: workflow
domain: ai
task: runbook-generation
status: draft
tags:
  - ai
  - claude
  - runbook
---

# Claude Runbook Generator

## Source material

Generate a draft runbook only from validated sources such as:

- known procedures
- verified commands
- incident records
- architecture documentation
- vendor documentation

## Transformation

```text
Evidence / source notes
       ↓
Procedure extraction
       ↓
Preconditions
       ↓
Risk classification
       ↓
Steps
       ↓
Validation
       ↓
Rollback
       ↓
Human review
```

## Quality gate

The resulting runbook must be reviewed for:

- command correctness
- environment assumptions
- destructive operations
- rollback completeness
- permissions
- observability
- post-change verification

AI-generated procedures are drafts until validated.
