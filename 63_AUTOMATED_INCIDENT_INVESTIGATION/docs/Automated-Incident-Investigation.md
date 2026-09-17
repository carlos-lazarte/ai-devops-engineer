---
type: architecture
domain: incident-management
technology: python, rag, knowledge-graph, skills, planner, claude
status: active
---
# v3.11.0 — Automated Incident Investigation

v3.11 connects the Incident Candidate from v3.6/v3.7/v3.9/v3.10 to an evidence-first investigation loop.

```text
Incident Candidate
      ↓
Trigger Eligibility
      ↓
Telemetry + Read-only Connector Evidence
      ↓
RAG + Knowledge Graph
      ↓
Skill Discovery
      ↓
Plan-only Planner
      ↓
Deterministic Hypotheses + Unknowns
      ↓
Optional Claude Analysis
      ↓
Human Review
```

The investigator never executes remediation. A root cause remains a hypothesis unless the supplied evidence independently establishes it.

## Investigation object

The persisted investigation keeps:

- source incident and signal provenance;
- telemetry summary;
- evidence items;
- hypotheses and confidence;
- unknowns / missing evidence;
- requested diagnostics;
- proposed actions;
- RAG hits;
- graph-aware context;
- selected skills;
- planner output;
- optional model result;
- safety flags.

## Modes

`dry-run` is deterministic and requires no model key. `claude` adds model-assisted synthesis but does not change authorization or execution boundaries.
