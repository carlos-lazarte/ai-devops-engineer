---
type: reference
domain: ai
topic: agent-adapter
status: active
tags:
  - multi-agent
  - adapter
---

# Agent Adapter Contract

A specialized agent adapter receives a bounded task and returns a structured result.

The adapter must not silently broaden scope, change tenant, change environment or inherit another agent's permissions.
