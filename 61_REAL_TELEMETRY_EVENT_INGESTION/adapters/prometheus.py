from __future__ import annotations

import json
import os
import time
import urllib.parse
import urllib.request
from typing import Any


class PrometheusClient:
    """Small read-only Prometheus HTTP API client using the Python standard library."""

    def __init__(self, base_url: str | None = None, timeout: float = 5.0, max_response_bytes: int = 2_000_000):
        self.base_url = (base_url or os.getenv("PROMETHEUS_URL", "http://127.0.0.1:9090")).rstrip("/")
        self.timeout = timeout
        self.max_response_bytes = max_response_bytes

    def query(self, promql: str, *, ts: float | None = None) -> dict[str, Any]:
        if not promql or len(promql) > 4096:
            raise ValueError("invalid_promql")
        query = {"query": promql}
        if ts is not None:
            query["time"] = str(ts)
        url = self.base_url + "/api/v1/query?" + urllib.parse.urlencode(query)
        req = urllib.request.Request(url, headers={"Accept": "application/json"}, method="GET")
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            raw = resp.read(self.max_response_bytes + 1)
        if len(raw) > self.max_response_bytes:
            raise ValueError("prometheus_response_too_large")
        payload = json.loads(raw.decode("utf-8"))
        if payload.get("status") != "success":
            raise RuntimeError("prometheus_query_failed")
        return payload

    @staticmethod
    def result_to_events(payload: dict[str, Any], tenant_id: str, environment: str,
                         component_label: str = "instance", metric_family: str = "prometheus",
                         condition: str = "observed", severity_hint: str = "info",
                         source: str = "prometheus") -> list[dict[str, Any]]:
        data = payload.get("data", {})
        result = data.get("result", [])
        events: list[dict[str, Any]] = []
        now = time.time()
        for idx, item in enumerate(result):
            labels = item.get("metric", {}) or {}
            component = labels.get(component_label) or labels.get("job") or "unknown"
            sample = item.get("value")
            if sample is None and item.get("values"):
                sample = item["values"][-1]
            value = None
            ts = now
            if isinstance(sample, list) and len(sample) >= 2:
                ts = float(sample[0])
                try:
                    value = float(sample[1])
                except (TypeError, ValueError):
                    value = sample[1]
            event_id = f"prom-{int(ts*1000)}-{idx}-{abs(hash(json.dumps(labels, sort_keys=True))) & 0xfffffff:x}"
            events.append({
                "event_id": event_id,
                "timestamp": ts,
                "tenant_id": tenant_id,
                "environment": environment,
                "component": component,
                "metric_family": metric_family,
                "condition": condition,
                "severity_hint": severity_hint,
                "value": value,
                "source": source,
                "labels": labels,
                "topology_neighbors": [],
                "provenance": {"source": source, "query": payload.get("data", {}).get("resultType", "vector")},
            })
        return events
