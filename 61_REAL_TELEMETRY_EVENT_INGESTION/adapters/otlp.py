from __future__ import annotations

from typing import Any


def _metric_family(name: str) -> str:
    return name.split("{")[0].strip().lower().replace("/", ":")


def _pick_component(resource: dict[str, Any], attrs: dict[str, Any]) -> str:
    for key in ("service.name", "host.name", "k8s.node.name", "k8s.pod.name", "instance"):
        if key in attrs:
            return str(attrs[key])
        if key in resource:
            return str(resource[key])
    return "unknown"


def _attrs(items: list[dict[str, Any]] | None) -> dict[str, Any]:
    out = {}
    for item in items or []:
        key = item.get("key")
        value = item.get("value", {})
        if not key:
            continue
        for k in ("stringValue", "intValue", "doubleValue", "boolValue"):
            if k in value:
                out[str(key)] = value[k]
                break
    return out


def parse_metrics(payload: dict[str, Any], tenant_id: str, environment: str,
                  severity_hint: str = "info") -> list[dict[str, Any]]:
    """Parse a bounded OTLP/HTTP JSON metrics subset."""
    events: list[dict[str, Any]] = []
    resource_metrics = payload.get("resourceMetrics", [])
    for r_idx, resource_metric in enumerate(resource_metrics):
        resource = _attrs(resource_metric.get("resource", {}).get("attributes"))
        for s_idx, scope_metric in enumerate(resource_metric.get("scopeMetrics", [])):
            for m_idx, metric in enumerate(scope_metric.get("metrics", [])):
                name = str(metric.get("name", "unknown"))
                family = _metric_family(name)
                data_block = next((metric.get(k) for k in ("gauge", "sum", "histogram", "exponentialHistogram") if metric.get(k)), None)
                if not data_block:
                    continue
                points = data_block.get("dataPoints", [])
                for p_idx, point in enumerate(points):
                    attrs = dict(resource)
                    attrs.update(_attrs(point.get("attributes")))
                    ts_ns = point.get("timeUnixNano") or point.get("startTimeUnixNano")
                    ts = float(ts_ns) / 1_000_000_000 if ts_ns else 0.0
                    if not ts:
                        continue
                    value = point.get("asDouble", point.get("asInt"))
                    component = _pick_component(resource, attrs)
                    event_id = f"otlp-{int(ts*1000)}-{r_idx}-{s_idx}-{m_idx}-{p_idx}"
                    events.append({
                        "event_id": event_id,
                        "timestamp": ts,
                        "tenant_id": tenant_id,
                        "environment": environment,
                        "component": component,
                        "metric_family": family,
                        "condition": "observed",
                        "severity_hint": severity_hint,
                        "value": value,
                        "source": "otlp-http",
                        "labels": attrs,
                        "topology_neighbors": [],
                        "provenance": {"source": "otlp-http", "metric_name": name},
                    })
    return events
