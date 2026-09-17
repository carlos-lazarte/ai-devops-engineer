---
type: reference
domain: platform
status: active
---
# v2.2.0 Release Notes

## Theme

Cloud & Kubernetes Operations.

## Added

- Kubernetes autoscaling and disruption reference manifests
- HPA and node-capacity guidance
- Prometheus Operator ServiceMonitor reference
- OpenTelemetry Collector reference
- GitOps and drift-management guidance
- backup/restore strategy and restore-drill runbook
- operational SLO schema
- pod-security and default-deny network policy references
- cloud-provider adapter model
- static manifest validation and tests

## Verification boundary

Reference manifests are statically validated. Cluster-side admission, CRD availability, cloud IAM, storage classes, CNI behavior, monitoring operators and controller reconciliation must be validated in the target environment.
