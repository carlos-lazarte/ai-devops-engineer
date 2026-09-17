# Demo — Kubernetes NodeNotReady

## Objective

Demonstrate the complete product flow without connecting to a live cluster.

## Inputs

Scenario:

- `K8S-NOTREADY-001`
- node description
- kubelet logs
- network observation
- change record

## Flow

```text
Scenario
  ↓
Evidence
  ↓
Retrieval
  ↓
Context Packet
  ↓
Claude analysis
  ↓
Structured result
  ↓
Human review
```

## Expected behavior

The assistant should identify only evidence-supported facts, keep hypotheses explicit, list missing evidence, and propose diagnostics before recommending a change.

## Safety

This demo is offline and contains no production credentials or cluster access.
