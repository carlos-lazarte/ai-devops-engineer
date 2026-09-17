---
type: architecture
domain: ai-devops
status: active
version: "2.7.0"
tags:
  - adaptive-context
  - agent-planning
  - rag
  - knowledge-graph
---
# Adaptive Context & Agent Planning

## Purpose
Define a planning layer that decomposes a task before retrieval and execution.

## Core flow
```text
Task
  ↓
Intent / Goal Decomposition
  ↓
Investigation Plan
  ↓
Knowledge Graph Exploration
  ↓
Evidence Retrieval
  ↓
Historical Context
  ↓
Skill Selection
  ↓
Tool Planning
  ↓
Policy Evaluation
  ↓
Execution Plan
  ↓
Human / Agent Review
```

## Design principles
- Planning does not grant authorization.
- Retrieval does not grant authorization.
- Memory does not grant authorization.
- Skills do not grant authorization.
- The planner must surface uncertainty and missing evidence.
- High-risk actions remain approval-gated.
- Critical execution remains disabled in the v2.7.0 reference implementation.
- Plans are deterministic for the same normalized input and registry state.

## Non-goals
This layer does not execute shell commands, SSH, cloud mutations, Kubernetes mutations, or production changes.
