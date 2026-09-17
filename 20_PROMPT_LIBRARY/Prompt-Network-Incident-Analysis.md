---
type: prompt
domain: networking
task: incident-analysis
difficulty: advanced
status: active
tags: [prompt, networking, ai]
---
# Prompt-Network-Incident-Analysis

## Objective
Produce a structured, evidence-grounded analysis.

## Required input
Provide the relevant logs, metrics, configuration, timestamps, and operational context.

## Prompt
```text
Analyze only the supplied network evidence. Separate facts, observed symptoms, hypotheses, evidence for/against each hypothesis, missing evidence, and safe validation steps. Do not invent counters, packets, timestamps, or root causes. Do not recommend disruptive changes without stating risk and rollback.
```

## Expected output
Facts → symptoms → hypotheses → evidence → missing information → validation plan.
