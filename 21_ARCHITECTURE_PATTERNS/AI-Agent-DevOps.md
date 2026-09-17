---
type: architecture
domain: ai
difficulty: advanced
status: active
tags: [architecture, ai]
---
# Architecture — AI-Agent-DevOps

## Objective
Describe the pattern and its main operational boundaries.

## Flow
```text
User/Event → Agent Orchestrator → Retrieval/Tools/Policy → Human Approval for risky actions → Execution → Verification → Audit
```

## Design notes
Read-only diagnostics can generally be automated more broadly than production mutations. Define permissions, allowlists, timeouts, and auditability.

## Failure considerations
Document dependency failures, degraded modes, recovery, and observability for the real environment.
