# Operational Dashboard Architecture

```text
Browser
  |
  | REST/JSON
  v
Product Runtime HTTP API
  |
  +--> Dashboard Summary
  +--> Incidents
  +--> Telemetry
  +--> Investigations
  +--> Connector Health
  |
  v
Existing v3.8-v3.11 services
  |
  +--> Store
  +--> Telemetry Ingestion
  +--> Production Connectors
  +--> Event Correlation
  +--> Automated Investigation
```

The browser does not talk to Prometheus, Kubernetes or host APIs directly. All infrastructure observations remain behind the connector boundary.
