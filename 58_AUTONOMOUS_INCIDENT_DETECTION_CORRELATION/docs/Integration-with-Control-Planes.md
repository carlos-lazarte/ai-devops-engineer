# Integration with Existing Control Planes

## Upstream

- Prometheus / Alertmanager
- log pipelines
- tracing systems
- Digital Twin scenarios
- agent/model/tool telemetry
- FinOps telemetry

## Downstream

- Knowledge Graph / Context Intelligence
- Skill Discovery
- Adaptive Planner
- Agent Runtime
- Human review / incident workflow

## Control boundary

Event detection is **not** an authorization system. Identity, Policy and Approval remain authoritative.

Recommended payload hand-off:
`incident_id`, `correlation_id`, `tenant_id`, `environment`, `severity`, `confidence`, `candidate_reason`, `signals`, `related_components`, `recommended_skill`, `plan_reference`, `provenance`.
