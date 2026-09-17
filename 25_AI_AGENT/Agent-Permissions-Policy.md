---
type: policy
domain: ai
status: active
---

# Agent Permissions Policy

## Permission tiers

### Tier 0 — Observe

Allowed:

- search_notes
- read_note
- list_related_notes
- retrieve_runbook
- inspect_context_packet

No mutation or execution.

### Tier 1 — Draft

Allowed after retrieval:

- create_draft
- propose_patch
- generate_postmortem

Drafts remain uncommitted and require review.

### Tier 2 — Approved change

A human explicitly approves a previously generated proposal. The agent may invoke only the exact approved operation and arguments.

### Tier 3 — Production execution

Out of scope for the initial Vault. Production execution must remain behind an independent, authenticated automation system with its own authorization controls.

## Deny by default

Any operation not explicitly declared in the tool registry is denied.

## Safety rules

- Never expose secrets in prompts or tool results when avoidable.
- Redact tokens, passwords, private keys, and session cookies.
- Reject path traversal and arbitrary path access.
- Enforce maximum result sizes.
- Record tool invocation metadata.
- Preserve provenance for all retrieved content.
