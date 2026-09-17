# Prometheus Integration

The runtime uses the Prometheus HTTP API in read-only mode.

## Data flow

```text
PromQL
  |
  v
Prometheus /api/v1/query
  |
  v
PrometheusClient
  |
  v
Normalized Telemetry Event
  |
  v
v3.6 Correlation
```

## Label mapping

By default `instance` is used as the component label, then `job`, then `unknown`.

The caller must provide `tenant_id` and `environment`; the runtime does not infer tenant boundaries from arbitrary labels.

## Operational controls

- query size is bounded;
- HTTP response size is bounded;
- requests are read-only;
- credentials should be supplied through the deployment environment or a secret manager;
- outbound egress should be allow-listed to approved telemetry endpoints.
