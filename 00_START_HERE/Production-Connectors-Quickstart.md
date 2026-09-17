# Production Connectors Quickstart — v3.10.0

## 1. Start the product

```bash
cd 35_RUNTIME
python3 product_server.py --vault .. --host 127.0.0.1 --port 8080
```

## 2. Inspect connectors

```bash
curl -s http://127.0.0.1:8080/api/v1/connectors
curl -s http://127.0.0.1:8080/api/v1/connectors/health
```

## 3. Linux read-only snapshot

```bash
curl -s http://127.0.0.1:8080/api/v1/connectors/linux/snapshot
```

The connector reads `/proc` and `/sys` only. It does not execute shell commands.

## 4. Prometheus

Set:

```bash
export PROMETHEUS_URL=http://127.0.0.1:9090
export PROMETHEUS_BEARER_TOKEN=''
```

Then query through the existing telemetry boundary:

```bash
curl -s http://127.0.0.1:8080/api/v1/telemetry/prometheus/query \\
  -H 'content-type: application/json' \\
  -d '{"query":"up"}'
```

## 5. Kubernetes

Configure a read-only API endpoint and credential:

```bash
export K8S_API_SERVER='https://kubernetes.example:6443'
export K8S_BEARER_TOKEN='REDACTED'
export K8S_CA_FILE='/path/to/cluster-ca.crt'
```

Then:

```bash
curl -s http://127.0.0.1:8080/api/v1/connectors/kubernetes/pods?namespace=default
```

Do not provide a credential with mutation or exec privileges.

## 6. OpenTelemetry Collector

`62_PRODUCTION_OBSERVABILITY_CONNECTORS/otel/config.yaml` is a reference configuration. In production, pin a tested collector image version and place the collector behind your normal network policy and authentication boundary.

The v3.9 runtime currently accepts a deliberately bounded JSON metrics subset at `/api/v1/telemetry/otlp`; it is not a claim of complete OTLP protocol coverage. Use the collector as a protocol gateway only after validating the exact exporter/encoding mapping used in your deployment.
