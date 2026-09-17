---
type: reference
domain: ai
technology: llm
status: active
tags:
  - ai
  - context
  - llm
  - devops
  - retrieval
---
# AI DevOps Context Protocol

## Purpose

Define a repeatable way to prepare evidence and Vault knowledge before asking an AI model to analyze a DevOps problem.

The protocol separates **facts**, **observations**, **hypotheses**, **actions**, and **model-generated suggestions**.

## Core principle

> Context is evidence packaged for reasoning; it is not permission to act.

## Context layers

```text
Layer 0  Identity
         Environment, service, cluster, host, technology, version

Layer 1  Time
         Incident start, relevant window, timezone, sequence of events

Layer 2  Evidence
         Logs, metrics, events, commands, manifests, traces, screenshots

Layer 3  Knowledge
         Relevant Vault notes, runbooks, troubleshooting guides, ADRs

Layer 4  Constraints
         Change window, risk, access, rollback requirements, business impact

Layer 5  Task
         Exact question the model must answer
```

## Evidence classes

### FACT
A directly observed or source-supported statement.

Example:

```text
The Kubernetes node reports Ready=False at 14:32 UTC.
```

### OBSERVATION
A pattern derived from one or more facts.

```text
The node became NotReady shortly after the container runtime errors began.
```

### HYPOTHESIS
A possible explanation that still requires validation.

```text
The container runtime failure may be contributing to the node state.
```

### ACTION
A human-approved operational step.

```text
Collect journal logs from containerd before restarting the service.
```

### AI-SUGGESTION
An output proposed by an AI model. It must not be treated as a fact until validated.

## Evidence priority

Use this default order when sources disagree:

1. Direct command output from the target system.
2. System/application logs from the relevant time window.
3. Monitoring data and traces.
4. Version-specific vendor documentation.
5. Approved internal runbooks and architecture records.
6. General technical references.
7. Model knowledge without supplied evidence.

This is a reasoning preference, not an absolute rule; source quality and freshness still need human review.

## Minimum context packet

For an operational incident, provide:

- target environment
- exact time window
- observed symptoms
- business/technical impact
- commands already executed
- relevant output
- logs or metrics
- recent changes
- known constraints
- explicit question

## Required AI behavior

The model should:

1. Separate facts from hypotheses.
2. Cite or identify the evidence used for each major inference.
3. State what is missing.
4. Avoid inventing system state.
5. Prefer diagnostic steps before disruptive actions.
6. Flag commands that can change production state.
7. Ask for version-specific context when it materially affects the answer.

## Forbidden assumptions

Do not assume:

- a version that was not supplied;
- a component exists because it is common in similar systems;
- a command succeeded because it was suggested;
- a log line has causal meaning without temporal/contextual support;
- a remediation is safe merely because it is reversible in theory.

## Output contract

For incident analysis, prefer:

```text
FACTS
OBSERVATIONS
HYPOTHESES
EVIDENCE FOR
EVIDENCE AGAINST
MISSING DATA
DIAGNOSTIC NEXT STEPS
RISK NOTES
POSSIBLE REMEDIATIONS
VERIFICATION
```

## Related

[[AI-Evidence-Handling]]
[[AI-Assisted-Change-Review]]
[[../17_RUNBOOKS/Runbook-Incident-Triage]]
