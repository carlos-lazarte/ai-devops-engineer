---
type: knowledge
domain: ai
technology: claude
status: draft
tags:
  - ai
  - claude
  - quickstart
---

# Claude Integration Quickstart

## Goal

Use the Vault as structured context for Claude without immediately building a full RAG system.

## Phase 1 — Manual

1. Open the relevant troubleshooting/runbook notes.
2. Collect operational evidence.
3. Build a Context Packet using `[[Context-Packet-Template]]`.
4. Ask Claude to produce the structured response contract.
5. Validate the response before action.
6. Save validated results back into the Vault.

## Phase 2 — Semi-automated

Automate Context Packet generation with a local script while keeping human approval between AI analysis and operational change.

## Phase 3 — Retrieval

Introduce semantic retrieval only after the Vault has stable metadata, clean linking and validated content.

## Phase 4 — Tooling / MCP

Expose narrowly scoped read/proposal tools. Introduce write operations only with review and audit controls.

## First experiment

Use:

- `[[Troubleshooting-Kubernetes-Node-NotReady]]`
- `[[Runbook-Kubernetes-Node-Recovery]]`
- `[[Claude-Troubleshooting-Assistant]]`

Build one Context Packet and compare the result with a manual expert diagnosis.
