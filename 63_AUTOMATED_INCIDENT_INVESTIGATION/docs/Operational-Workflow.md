# Operational Workflow

1. A candidate is retrieved from the incident store.
2. The v3.7 trigger policy is evaluated.
3. Recent telemetry is filtered by tenant/environment.
4. Read-only connector evidence is collected where configured.
5. RAG and graph-aware retrieval provide operational context.
6. Skill discovery selects eligible published skills.
7. The planner creates a plan-only investigation workflow.
8. Deterministic hypotheses and unknowns are generated.
9. Optionally, Claude synthesizes a structured analysis from the bounded context.
10. The result is persisted and audited.
11. Any remediation proposal remains approval-gated and execution-disabled.
