---
type: prompt
domain: iac
task: plan-analysis
difficulty: intermediate
status: active
tags: [prompt, iac, ai]
---
# Prompt-Terraform-Plan-Analysis

## Objective
Produce a structured, evidence-grounded analysis.

## Required input
Provide the relevant logs, metrics, configuration, timestamps, and operational context.

## Prompt
```text
Review this Terraform plan. Classify significant changes as create, update, replace, or destroy. Explain operational impact, dependencies, and rollback considerations. Flag destructive/replacement actions. Do not infer resource intent absent from the configuration.
```

## Expected output
Facts → symptoms → hypotheses → evidence → missing information → validation plan.
