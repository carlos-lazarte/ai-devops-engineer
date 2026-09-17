---
type: policy
domain: ai-devops
status: active
tags:
  - memory
  - governance
---
# Memory Quality Policy

Memory is evaluated on four axes:

## Provenance

Every episodic or semantic record must identify its source references and correlation context.

## Isolation

Records are queryable only within the same tenant and environment boundary defined by the contract.

## Freshness

Expired working memory must not be presented as active state.

## Promotion

Episodic memory becomes durable knowledge only through explicit review. AI-generated memory is a candidate, not an authority.
