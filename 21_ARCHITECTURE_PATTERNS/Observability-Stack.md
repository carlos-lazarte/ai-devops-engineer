---
type: architecture
domain: observability
difficulty: intermediate
status: active
tags: [architecture, observability]
---
# Architecture — Observability-Stack

## Objective
Describe the pattern and its main operational boundaries.

## Flow
```text
Applications/Hosts → Collectors → Metrics | Logs | Traces → Storage/Query → Dashboards/Alerts/Investigation
```

## Design notes
Design for retention, cardinality, cost, access control, buffering, and correlation.

## Failure considerations
Document dependency failures, degraded modes, recovery, and observability for the real environment.
