---
type: architecture
domain: cloud
status: active
tags:
  - aws
  - azure
  - oci
  - cloud
---

# Cloud Provider Adapter Model

Provider integrations should implement a common contract for:

- workload identity
- object storage references
- load balancer / ingress integration
- managed database connectivity
- metrics and logs export
- quotas and capacity

Keep cloud-specific identifiers out of reusable Markdown knowledge and reference manifests. Supply them via environment configuration and approved secret/reference mechanisms.
