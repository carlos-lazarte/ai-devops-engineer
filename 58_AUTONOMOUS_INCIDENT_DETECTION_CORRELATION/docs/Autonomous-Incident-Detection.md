---
type: architecture
domain: ai-devops
status: active
version: "3.6.0"
tags:
  - incident-detection
  - event-correlation
  - autonomous-sre
  - event-driven
---
# Autonomous Incident Detection & Event Correlation

## Objective

Detect operational signals automatically, normalize them into events, remove duplicates, correlate related events, and create an **Incident Candidate** suitable for triage and AI-assisted investigation.

## Event-driven SRE flow

```text
Telemetry / Logs / Traces / Digital Twin
                 ↓
             Ingestion
                 ↓
        Event Normalization
                 ↓
       Deduplication / Suppression
                 ↓
          Event Correlation
                 ↓
       Incident Candidate
                 ↓
      Severity / Confidence
                 ↓
      Topology + Knowledge Graph
                 ↓
        Skill Discovery / Plan
                 ↓
          Human Review
```

## Incident Candidate versus confirmed incident

Correlation produces a **candidate**, not a fact. A candidate can be promoted to `TRIAGED` only after a defined triage condition is satisfied. The pipeline must preserve provenance for every signal used in correlation.

## Safety boundary

Detection and correlation may create advisory incident candidates. They must not:
- grant authorization;
- alter IAM/RBAC or secrets;
- execute production remediation;
- bypass policy or approval;
- treat predicted or correlated state as ground truth.

## v3.6 hand-off

`Incident Candidate → Context Intelligence → Skill Discovery → Planner`.
The planner remains subject to the existing Policy + Identity + Approval controls.
