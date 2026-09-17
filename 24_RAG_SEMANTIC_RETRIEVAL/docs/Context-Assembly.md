---
type: workflow
domain: ai
topic: context-assembly
difficulty: intermediate
status: active
tags:
  - ai
  - rag
  - context
---

# Context Assembly

## Goal

Convert retrieved chunks into a compact, auditable Context Packet for the LLM.

## Assembly order

```text
1. Task
2. User constraints
3. Relevant facts from evidence
4. Retrieved knowledge
5. Operational constraints
6. Required output contract
```

## Source block

Each retrieved item should look like:

```text
[SOURCE]
path: 16_TROUBLESHOOTING/Troubleshooting-Kubernetes-Node-NotReady.md
heading: First checks
chunk_id: <stable-id>
score: <numeric-score>
content:
...
[/SOURCE]
```

## Deduplication

When several chunks come from the same note:

- preserve the strongest source
- merge adjacent sections only when semantic continuity is obvious
- keep all unique source references

## Context budget

The assembler should prefer fewer high-value chunks to a large amount of weakly related text.

## Output contract

The final context packet should contain:

```yaml
request:
constraints:
evidence:
knowledge:
unknowns:
required_output:
provenance:
```

Use [[Context-Packet-Template]] and [[AI-Structured-Response-Contract]] as the integration contracts.
