---
type: runbook
domain: core
difficulty: intermediate
risk: high
status: active
tags: [runbook, core]
---
# Runbook-Production-Change-Validation

## Purpose
Validate a production change against explicit baseline and acceptance criteria.

## Procedure
1. Confirm scope, baseline, and rollback criteria.
2. Record start time and affected components.
3. Execute the smallest planned change.
4. Observe health, logs, metrics, and dependencies.
5. Compare with baseline.
6. Declare success only when acceptance criteria pass.

Related: [[Checklist-Production-Change-Validation]]
