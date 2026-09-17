# v2.6.0 — Knowledge Graph & Context Intelligence

## Added

- Derived graph index from Markdown wikilinks and metadata.
- Graph-aware context retrieval with bounded neighbor expansion.
- Context packet builder that merges knowledge, evidence and Skill candidates.
- Explainable retrieval reasons and provenance fields.
- Graph-aware evaluation fixtures and deterministic tests.

## Safety

- The graph is a derived index; Markdown remains the source of truth.
- Retrieval does not grant tool authorization.
- Graph expansion is bounded.
- No infrastructure mutation is performed by the graph or context planner.
