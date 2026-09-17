# Knowledge & Skill Marketplace Intelligence

Version 2.5.0 adds an intelligence layer above the Skill Marketplace. Its purpose is to identify candidate Skills for a task, resolve dependencies, check platform compatibility and policy constraints, and produce a deterministic execution plan.

```text
Task
  ↓
Intent / capability extraction
  ↓
Skill Discovery
  ↓
Candidate ranking
  ↓
Dependency resolution
  ↓
Compatibility gate
  ↓
Policy gate
  ↓
Selected Skill set
  ↓
Execution Plan
```

The intelligence layer is advisory. It does not grant authorization and it does not execute production changes.

## Design principles

- Discovery is separate from authorization.
- Ranking is explainable: every score has traceable signals.
- Dependency resolution is deterministic.
- Policy is evaluated after candidate discovery and before selection.
- A failed dependency or incompatible platform blocks the dependent plan.
- No skill is selected solely because an LLM suggested its name.

## Semantic retrieval boundary

The reference implementation in v2.5.0 uses a deterministic token/term scoring baseline so it can run offline. An embedding provider can be added behind the same discovery contract later; the ranking contract must continue to expose provenance and reasons for the match.
