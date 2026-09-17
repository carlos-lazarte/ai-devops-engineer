---
type: design
domain: ai-devops
status: active
version: "3.6.0"
---
# Event Correlation Model

## Correlation dimensions

The reference engine correlates events using bounded deterministic signals:

1. Temporal proximity within a configurable window.
2. Same tenant and environment.
3. Same or related component scope.
4. Shared metric family or causal hint.
5. Optional topology adjacency.

A correlation is stronger when multiple independent dimensions agree.

## Candidate key

A canonical key is derived from:
`tenant_id + environment + normalized_component + metric_family + condition`.

The key is used for duplicate detection, not incident identity.

## Merge rule

Events may be merged into the same candidate only when tenant/environment boundaries match and the correlation score reaches the configured threshold. Cross-tenant events are never merged.
