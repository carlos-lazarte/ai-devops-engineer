---
type: prompt
domain: sre
task: postmortem
difficulty: intermediate
status: active
tags: [prompt, sre, ai]
---
# Prompt-Postmortem-Draft

## Objective
Produce a structured, evidence-grounded analysis.

## Required input
Provide the relevant logs, metrics, configuration, timestamps, and operational context.

## Prompt
```text
Draft a blameless technical postmortem from the supplied timeline and evidence. Separate confirmed facts from inferred explanations. Include impact, timeline, detection, contributing factors, mitigation, recovery, lessons, and follow-up actions. Do not invent facts or assign individual blame.
```

## Expected output
Facts → symptoms → hypotheses → evidence → missing information → validation plan.
