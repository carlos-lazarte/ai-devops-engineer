---
type: architecture
domain: ai
difficulty: advanced
status: active
tags:
  - agents
  - skills
  - devops
  - autonomy
---
# Agent Skills Architecture

## Purpose

Provide bounded, reusable and independently evaluated capabilities for an AI DevOps agent.

## Skill contract

Every skill defines:

1. Goal and scope
2. Required inputs
3. Evidence requirements
4. Allowed tools
5. Prohibited tools
6. Risk classification
7. Output schema
8. Verification procedure
9. Escalation conditions
10. Evaluation cases

## Control flow

```text
User Task
  ↓
Router
  ↓
Skill Selection
  ↓
Input Validation
  ↓
Evidence Gate
  ↓
Policy Check
  ↓
Plan
  ↓
Approval Gate
  ↓
Execution Adapter
  ↓
Verification
  ↓
Result + Provenance
```

## Safety boundary

The skill layer can propose an operational action, but the platform policy engine remains authoritative for authorization. v2.3.0 execution adapters are simulation-only.
