---
type: knowledge
domain: kubernetes
technology: kubernetes
status: active
tags:
  - kubernetes
  - hpa
  - resilience
---

# Autoscaling and Resilience

## Horizontal Pod Autoscaler

Use HPA for stateless runtime workloads when CPU, memory or application metrics correlate with load.

## Pod distribution

Use topology spread constraints and anti-affinity where losing a single node or zone should not remove all replicas.

## Capacity

HPA changes replica count but does not create cluster capacity. Node autoscaling and workload requests must be considered together.

## Verification

After enabling autoscaling, validate:

- request rate
- p95 latency
- replica count
- pending pods
- node capacity
- error rate
- SLO impact
