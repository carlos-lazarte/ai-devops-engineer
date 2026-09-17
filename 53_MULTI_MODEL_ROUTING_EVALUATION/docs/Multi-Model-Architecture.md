---
type: architecture
domain: ai-devops
status: active
version: "3.1.0"
tags:
  - multi-model
  - model-routing
  - evaluation
  - llm
---
# Multi-Model Agent Evaluation & Model Routing

## Objective

Evaluate multiple model profiles against the same controlled DevOps scenarios and route a task to an explicitly registered model profile.

## Architecture

```text
Task
  ↓
Task Classifier
  ↓
Routing Policy
  ↓
Candidate Models
  ↓
Model Capability / Cost / Latency Constraints
  ↓
Selected Model
  ↓
Same Context + Same Scenario
  ↓
Evaluation
  ↓
Quality / Safety / Cost / Latency
```

## Important boundary

Model routing is not authorization.

```text
Model Selection ≠ Tool Authorization
Model Capability ≠ Operational Permission
```

The policy engine remains the authority for tools, actions and environments.

## Reference scope

The reference implementation is offline and deterministic. It uses model profiles rather than live provider calls.
