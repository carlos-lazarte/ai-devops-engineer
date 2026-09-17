---
type: workflow
domain: ai
task: troubleshooting
status: draft
tags:
  - ai
  - claude
  - troubleshooting
---

# Claude Troubleshooting Assistant

## Workflow

```text
Problem statement
      ↓
Select relevant Vault notes
      ↓
Collect evidence
      ↓
Redact secrets
      ↓
Build Context Packet
      ↓
Claude analysis
      ↓
Structured response
      ↓
Human validation
      ↓
Execute diagnostics
      ↓
Update evidence
      ↓
Repeat if needed
```

## Prompt contract

Ask Claude to:

1. Restate the problem using only supplied facts.
2. Separate facts from observations.
3. Generate bounded hypotheses.
4. Map each hypothesis to supporting and contradicting evidence.
5. Recommend low-risk diagnostics first.
6. Identify missing evidence.
7. Avoid claiming a root cause until evidence supports it.

## Operational guardrail

The workflow is diagnostic by default. Remediation commands must be presented as proposals until explicitly approved by a human operator.

## Output destination

Validated results may update:

- incident note
- troubleshooting note
- runbook
- postmortem
- ADR
