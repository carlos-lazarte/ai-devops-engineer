---
type: architecture
domain: ai
task: claude-integration
status: draft
tags:
  - ai
  - claude
  - devops
  - context
---

# Claude Integration Architecture

## Objective

Define a provider-neutral integration pattern for using Claude as a reasoning layer over the Vault without treating model output as authoritative operational truth.

## Logical flow

```text
Obsidian Vault
     |
     | select relevant notes
     v
Context Builder
     |
     | normalize facts/evidence
     v
Context Packet
     |
     v
Claude
     |
     | structured response
     v
Human Validation
     |
     +----> action / remediation
     |
     +----> new note / postmortem / knowledge update
```

## Design rules

1. Retrieval happens before reasoning.
2. Facts and observations are preserved verbatim where practical.
3. Hypotheses are explicitly labeled as hypotheses.
4. Commands with production impact require human review.
5. Secrets, credentials and unnecessary personal data must be excluded from context.
6. Responses should use a predictable schema when consumed by automation.
7. The Vault remains the durable knowledge source; the model is a reasoning component.

## Integration modes

### Manual

Copy a Context Packet into Claude and paste the validated result back into the Vault.

### Semi-automated

A script selects notes, builds a Context Packet and sends it through an approved model interface.

### Retrieval-Augmented

A retrieval layer selects relevant Vault content and constructs the Context Packet automatically.

### MCP-oriented

A controlled tool layer exposes specific read/write capabilities to an AI client. Tool permissions must be least-privilege and explicitly scoped.

## Failure boundaries

```text
Retrieval failure      -> do not invent context
Context loss           -> stop and request missing evidence
Model uncertainty      -> label uncertainty
Tool failure           -> preserve evidence; do not retry destructive actions blindly
Human rejection        -> no operational action
```

## Related

[[AI-DevOps-Context-Protocol]]
[[Context-Packet-Template]]
[[Claude-Context-Selection-Policy]]
[[AI-Structured-Response-Contract]]
