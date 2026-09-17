---
type: workflow
domain: ai
task: context-selection
status: draft
tags:
  - ai
  - claude
  - retrieval
---

# Claude Context Selection Policy

## Purpose

Select only the minimum useful set of Vault content and operational evidence needed for a task.

## Retrieval priority

1. Current incident or task record
2. Directly linked troubleshooting/runbook notes
3. Technology and architecture notes
4. Relevant checklists and ADRs
5. Historical incidents with materially similar symptoms
6. General background knowledge

## Context exclusion

Exclude:

- unrelated notes
- duplicate content
- secrets and credentials
- unsupported assumptions
- stale operational evidence unless clearly labeled historical
- large documents that add no task-relevant information

## Conflict handling

When two notes disagree:

```text
identify conflict
      ↓
compare timestamps / sources
      ↓
retain both statements
      ↓
label uncertainty
      ↓
request validation where required
```

## Context budget principle

More context is not automatically better. Prefer a small, high-signal context set over a large undifferentiated dump.

## Output requirement

The AI must distinguish:

- Facts
- Observations
- Hypotheses
- Recommended diagnostics
- Proposed actions
- Unknowns

## Related

[[Claude-Integration-Architecture]]
[[Context-Packet-Template]]
[[Evidence-Quality-Matrix]]
