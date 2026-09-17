---
type: architecture
domain: cloud
title: Cloud & Kubernetes Operations
status: active
tags:
  - cloud
  - kubernetes
  - sre
  - operations
---

# Cloud & Kubernetes Operations

This layer describes operational patterns for running the AI DevOps Platform on Kubernetes and integrating it with cloud-native operations.

## Scope

- workload scheduling and resilience
- autoscaling
- topology-aware placement
- Prometheus Operator / ServiceMonitor integration
- OpenTelemetry patterns
- backup and restore of stateful stores
- GitOps deployment
- admission and policy controls
- operational runbooks

## Non-goals

These manifests are reference artifacts. They do not assert that a particular cloud, Kubernetes distribution, storage class, ingress controller, or policy engine is installed.

## Operational principle

Prefer immutable, declarative changes through GitOps; keep secrets external to the Vault and use environment-specific overlays.
