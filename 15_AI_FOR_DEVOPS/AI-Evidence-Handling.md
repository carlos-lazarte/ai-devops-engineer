---
type: knowledge
domain: ai
difficulty: intermediate
status: active
tags: [ai, devops, evidence, llm]
---
# AI Evidence Handling

LLMs can organize and reason about operational evidence, but generated hypotheses are not evidence.

## Evidence chain

```text
Telemetry / logs / config
        ↓
Observed facts
        ↓
Hypotheses
        ↓
Validation tests
        ↓
Conclusion
```

Ask the model to separate facts, observations, hypotheses, supporting evidence, contradictory evidence, missing evidence, and validation steps.

Related: [[AI-DevOps-Workflow]], [[Prompt-Incident-Analysis]]
