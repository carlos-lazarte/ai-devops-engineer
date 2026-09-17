# Operations

## Prometheus
Set `PROMETHEUS_URL` and optionally `PROMETHEUS_BEARER_TOKEN`. Prefer internal DNS, TLS and an egress allow-list. Keep the service account/token read-only.

## Kubernetes
Set `K8S_API_SERVER`, `K8S_BEARER_TOKEN` and, for private clusters, `K8S_CA_FILE`. The reference connector calls only GET APIs.

## Linux
Mount `/proc` and `/sys` read-only into the runtime container if host-level metrics are required. For Kubernetes nodes, a DaemonSet or node-local collector is preferable to exposing host namespaces directly to the agent.

## OTEL Collector
Deploy the collector as the protocol gateway. Pin a tested collector image version and keep the collector-to-runtime path on an authenticated internal network in production.

## Failure handling
Connector failures are signals. They do not become implicit authorization. The caller should preserve `source`, `connector`, `endpoint`, timing and error provenance for audit and diagnosis.
