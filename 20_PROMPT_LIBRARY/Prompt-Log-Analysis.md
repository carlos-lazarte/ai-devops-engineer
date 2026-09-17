---
type: prompt
domain: observability
task: log-analysis
model: vendor-neutral
status: active
tags:
  - ai
  - logs
  - troubleshooting
---

# Prompt — Log Analysis

## Objective

Turn raw logs into a structured diagnostic summary.

## Prompt

```text
Analyze the supplied logs.

Do not assume missing context.
Group messages by timestamp, component, severity and correlation identifier when available.
Identify repeated patterns, first occurrence, escalation points and likely causal sequences.
Distinguish direct evidence from interpretation.

Return:
- timeline
- recurring errors
- anomalies
- probable dependencies
- evidence gaps
- suggested next checks
```
