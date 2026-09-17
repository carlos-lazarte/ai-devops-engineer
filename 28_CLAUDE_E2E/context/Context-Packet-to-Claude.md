---
type: workflow
domain: ai
task: context-handoff
status: active
tags:
  - claude
  - context
  - provenance
---

# Context Packet → Claude

## Required sections

1. Task definition
2. Evidence
3. Retrieved knowledge
4. Retrieved runbooks
5. Constraints
6. Provenance

## Ordering rule

Evidence is kept separate from durable knowledge. Retrieved knowledge provides guidance; incident evidence provides current-state observations.

## Prompting rule

Ask Claude to reason over the packet and return a structured response. Do not ask it to simulate tool execution or claim that remediation was performed.

## Validation rule

The structured result must be validated before downstream automation consumes it.
