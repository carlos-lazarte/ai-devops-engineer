---
type: policy
domain: ai
status: active
tags:
  - retrieval
  - knowledge-graph
  - policy
---
# Graph-Aware Retrieval Policy

## Rules

1. Direct task matches have priority over distant graph neighbors.
2. Graph expansion is bounded and deterministic.
3. Every selected item must retain provenance.
4. Cross-tenant isolation remains mandatory when runtime context contains tenant metadata.
5. A Skill recommendation never implies authorization.
6. Evidence is not promoted to permanent knowledge automatically.
7. When the context budget is exceeded, lower-relevance items are removed first.

## Default limits

```yaml
max_graph_hops: 2
max_knowledge_items: 12
max_skill_candidates: 4
max_evidence_items: 8
```

These are baseline values for evaluation and may be tuned per deployment.
