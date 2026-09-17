---
type: example
domain: ai
status: active
---

# Incident Agent Session

## User request

Analyze a Kubernetes node reported as `NotReady`.

## Agent sequence

1. Search relevant troubleshooting notes.
2. Read Kubernetes node and incident procedures.
3. Request or retrieve evidence.
4. Assemble Context Packet.
5. Ask Claude for structured analysis.
6. Return facts, observations, hypotheses, diagnostics, and proposed actions.
7. Require human review before any change.

## Desired behavior

The agent should be able to say:

> The current evidence is insufficient to determine root cause. The next diagnostic is to inspect kubelet health and node conditions.

It should not claim a root cause without supporting evidence.
