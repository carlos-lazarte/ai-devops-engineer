# Connector Evidence

The reference investigator does not sample the investigator host by default. Set `INVESTIGATION_LOCAL_LINUX=true` to opt in to Linux procfs/sysfs evidence for the investigator host. Kubernetes is queried only when `K8S_API_SERVER` is explicitly configured.

Prometheus evidence is represented primarily through the telemetry already persisted by v3.9. This avoids generating unbounded or speculative PromQL from the investigator.

All connector observations carry provenance and are treated as observations, not proof of root cause.
