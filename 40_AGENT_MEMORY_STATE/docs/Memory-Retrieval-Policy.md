# Memory Retrieval Policy

Memory retrieval should use the following filters before ranking content:

1. `tenant_id`
2. `environment`
3. `memory_class`
4. `status`
5. `provenance`
6. time window / retention eligibility

Recommended ranking inputs:

- semantic relevance
- incident recency
- same service/technology
- verified outcome
- provenance quality

A memory item marked `unverified`, `redacted`, or `superseded` should not be presented as authoritative without that status attached.
