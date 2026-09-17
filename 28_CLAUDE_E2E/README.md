---
type: architecture
domain: ai
task: claude-e2e
status: active
tags:
  - ai
  - claude
  - agent
  - e2e
  - mcp
---

# v0.9.0 — Claude Client Integration & End-to-End Agent

## Objective

Connect the local MCP-style gateway and RAG/context layer to a Claude-compatible model client, while preserving provenance, structured responses and human approval boundaries.

## End-to-end path

```text
Incident / User Task
        |
        v
Agent Orchestrator
        |
        +--> MCP Gateway: search / read / related / runbook
        |
        v
Context Packet Builder
        |
        v
Claude Client Adapter
        |
        v
Structured Response Validator
        |
        +--> Human Approval Gate
        |
        +--> Draft Vault Update
        |
        v
Evaluation / Audit
```

## Integration modes

### Dry run

Builds the exact context and prompt that would be sent to Claude, but does not call an external model endpoint.

### Claude API mode

Uses the Anthropic Messages API through the local adapter. Credentials and model selection are supplied through environment variables; no secret is stored in the Vault.

### Future MCP-native client mode

A real MCP client can replace the local gateway adapter without changing the context packet or response contract.

## Safety boundary

This release remains read-oriented. The orchestrator can propose actions and draft changes, but it does not execute production commands.

## Primary demonstration

Run the `K8S-NOTREADY-001` scenario. The agent should retrieve:

- the incident evidence;
- relevant troubleshooting knowledge;
- a suitable runbook;
- related notes;

and return a structured analysis containing facts, observations, hypotheses, missing evidence, recommended diagnostics and proposed actions.
