---
type: workflow
domain: ai
task: change-review
difficulty: intermediate
risk: high
status: active
tags: [ai, workflow, change, review]
---
# AI-Assisted Change Review

## Flow
```text
Change plan → Context → AI review → Risks/assumptions → Human review → Approved execution → Verification
```

## Questions
- What assumptions are unstated?
- Which dependencies can fail?
- What telemetry should detect regression?
- What is the rollback trigger?
- Which actions are destructive or irreversible?

Related: [[Checklist-AI-Generated-Change]], [[AI-Evidence-Handling]]
