---
type: workflow
domain: ai
technology: llm
status: active
tags:
  - ai
  - incident
  - sre
---
# AI Incident Analysis Workflow

## Goal

Use an AI model as an analysis assistant without allowing model output to silently become operational truth.

## Workflow

```text
Incident
  ↓
Define scope + time window
  ↓
Collect evidence
  ↓
Build Context Packet
  ↓
Retrieve relevant Vault notes
  ↓
Ask AI for structured analysis
  ↓
Separate facts / hypotheses
  ↓
Validate hypotheses against evidence
  ↓
Choose human-approved action
  ↓
Execute / observe
  ↓
Verify result
  ↓
Document outcome
  ↓
Update Vault
```

## AI task sequence

### Step 1 — Summarize

Create a concise incident timeline without adding facts.

### Step 2 — Correlate

Relate events by time, component and dependency.

### Step 3 — Hypothesize

Generate a bounded set of plausible causes.

### Step 4 — Discriminate

For each hypothesis, identify evidence for, evidence against and the cheapest diagnostic that can distinguish it.

### Step 5 — Recommend

Suggest non-disruptive diagnostics first, then remediation options with risks.

## Human checkpoints

The engineer must validate:

- factual accuracy;
- version applicability;
- production impact;
- command safety;
- rollback feasibility;
- final remediation choice.

## Related

[[../AI-DevOps-Context-Protocol]]
[[../context/Context-Packet-Template]]
[[../../17_RUNBOOKS/Runbook-Incident-Triage]]
