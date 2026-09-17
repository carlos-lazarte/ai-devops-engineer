# Event-Driven Agent Architecture

v3.7 introduces an event-driven entry point after v3.6 creates an Incident Candidate.

## Responsibilities

| Layer | Responsibility | Authority |
|---|---|---|
| Detection/Correlation | Create candidate | advisory |
| Trigger Engine | Decide whether a candidate may create a trigger request | policy-constrained |
| Policy | Enforce tenant, environment, safety and action rules | authoritative |
| Identity | Establish actor/service identity | authoritative |
| Budget/FinOps | Enforce resource/cost ceilings | authoritative |
| Incident Commander | Coordinate evidence, hypotheses, requests and state | coordination |
| Human Approval | Accept/reject requested action | authoritative for gated action |
| Planner | Produce bounded plan | advisory |
| Executor | Execute only where separately authorized | disabled in reference release |
| Verification | Determine whether outcome is verified | evidentiary |

## Key rule

An event may trigger analysis, but an event cannot self-authorize mutation. The trigger payload contains explicit authority metadata and a required policy decision.
