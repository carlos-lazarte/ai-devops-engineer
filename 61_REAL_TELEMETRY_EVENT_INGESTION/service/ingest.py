from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
V36 = ROOT / "58_AUTONOMOUS_INCIDENT_DETECTION_CORRELATION"
if str(V36) not in sys.path:
    sys.path.insert(0, str(V36))

from ingestion.normalize import normalize  # noqa: E402
from correlator.service import build_incident_candidates  # noqa: E402
from adapters.prometheus import PrometheusClient  # noqa: E402
from adapters.otlp import parse_metrics  # noqa: E402


class TelemetryIngestionService:
    def __init__(self, store, prometheus: PrometheusClient | None = None):
        self.store = store
        self.prometheus = prometheus or PrometheusClient()

    def ingest_events(self, raw_events: list[dict[str, Any]]) -> dict[str, Any]:
        normalized = [normalize(e) for e in raw_events]
        self.store.save_telemetry_events(normalized)
        candidates = build_incident_candidates(normalized)
        import datetime
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        for candidate in candidates["candidates"]:
            candidate["created_at"] = now
            candidate["updated_at"] = now
            self.store.upsert_incident(candidate)
        return {
            "accepted": len(normalized),
            "suppressed": len(candidates.get("suppressed_event_ids", [])),
            "candidates": candidates.get("candidates", []),
        }

    def ingest_event(self, raw_event: dict[str, Any]) -> dict[str, Any]:
        return self.ingest_events([raw_event])

    def ingest_otlp(self, payload: dict[str, Any], tenant_id: str, environment: str, severity_hint: str = "info") -> dict[str, Any]:
        if not tenant_id or not environment:
            raise ValueError("tenant_and_environment_required")
        events = parse_metrics(payload, tenant_id, environment, severity_hint)
        if not events:
            raise ValueError("no_supported_otlp_metrics")
        return self.ingest_events(events)

    def query_prometheus(self, query: str) -> dict[str, Any]:
        return self.prometheus.query(query)

    def poll_prometheus(self, query: str, tenant_id: str, environment: str,
                        component_label: str = "instance", metric_family: str = "prometheus",
                        condition: str = "observed", severity_hint: str = "info") -> dict[str, Any]:
        payload = self.prometheus.query(query)
        events = self.prometheus.result_to_events(payload, tenant_id, environment,
                                                   component_label, metric_family, condition, severity_hint)
        if not events:
            return {"accepted": 0, "suppressed": 0, "candidates": [], "prometheus_results": 0}
        result = self.ingest_events(events)
        result["prometheus_results"] = len(events)
        return result

    def recent_events(self, tenant_id: str | None = None, limit: int = 100) -> list[dict[str, Any]]:
        return self.store.list_telemetry_events(tenant_id, limit)
