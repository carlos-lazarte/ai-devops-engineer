---
type: runbook
domain: sre
technology: kubernetes
status: active
risk: medium
tags:
  - kubernetes
  - latency
  - sre
---

# Runbook — Runtime High Latency

## Trigger

Alert on p95/p99 latency or a defined SLO burn rate.

## First checks

1. Confirm alert window and affected endpoint.
2. Compare request rate and in-flight requests.
3. Inspect pod readiness and restarts.
4. Check CPU/memory throttling and saturation.
5. Compare RAG and Claude dependency latency.

## Evidence

Collect request metrics, deployment revision, pod events and dependency timings.

## Actions

Do not scale blindly. Determine whether latency is caused by application CPU, downstream dependency, RAG retrieval, model latency, or node pressure.

## Verification

Confirm recovery in metrics and SLOs for a sustained observation window.
