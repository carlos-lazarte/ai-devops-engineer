---
type: prompt
domain: kubernetes
task: incident-analysis
difficulty: advanced
status: active
tags: [prompt, kubernetes, ai]
---
# Prompt-Kubernetes-Incident-Analysis

## Objective
Produce a structured, evidence-grounded analysis.

## Required input
Provide the relevant logs, metrics, configuration, timestamps, and operational context.

## Prompt
```text
Analyze the supplied Kubernetes evidence. Separate facts, symptoms, hypotheses, and validation steps. Prioritize by blast radius and reversibility. Consider Pod, Deployment, Node, Service, Ingress, configuration, image/registry, resources, and dependencies only where evidence supports them. Do not assume the most common cause is the actual cause.
```

## Expected output
Facts → symptoms → hypotheses → evidence → missing information → validation plan.
