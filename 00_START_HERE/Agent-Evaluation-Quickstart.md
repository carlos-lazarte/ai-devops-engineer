---
type: procedure
domain: ai-devops
status: active
tags:
  - evaluation
  - reliability
---
# Agent Evaluation Quickstart

Run the deterministic evaluation stack locally:

```bash
make agent-eval
make memory-quality
make reliability-test
make test
```

The evaluation report is written under `41_AGENT_EVALUATION_RELIABILITY/reports/`. Treat results as evidence for the current build and fixtures, not as proof of general model performance.
