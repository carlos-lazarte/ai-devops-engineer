from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .core import request_id
from .store import IncidentStore

V39_ROOT = Path(__file__).resolve().parents[2] / "61_REAL_TELEMETRY_EVENT_INGESTION"
V310_ROOT = Path(__file__).resolve().parents[2] / "62_PRODUCTION_OBSERVABILITY_CONNECTORS"
V311_ROOT = Path(__file__).resolve().parents[2] / "63_AUTOMATED_INCIDENT_INVESTIGATION"
if str(V39_ROOT) not in sys.path:
    sys.path.insert(0, str(V39_ROOT))
if str(V310_ROOT) not in sys.path:
    sys.path.insert(0, str(V310_ROOT))
if str(V311_ROOT) not in sys.path:
    sys.path.insert(0, str(V311_ROOT))
from service.ingest import TelemetryIngestionService
from v310_service.registry import ConnectorRegistry
from investigation.engine import AutomatedIncidentInvestigator


class ProductService:
    def __init__(self, vault_root: Path, db: IncidentStore):
        self.vault_root = vault_root
        self.db = db
        self.telemetry = TelemetryIngestionService(db)
        self.connectors = ConnectorRegistry()
        self.investigator = AutomatedIncidentInvestigator(vault_root, db, self.connectors)

    @staticmethod
    def now() -> str:
        return datetime.now(timezone.utc).isoformat()

    def version(self) -> str:
        version_path = self.vault_root / "VERSION"
        try:
            version = version_path.read_text(encoding="utf-8").strip()
        except OSError:
            version = "unknown"
        return version or "unknown"

    def product_info(self) -> dict[str, Any]:
        version = self.version()
        return {
            "product": "AI DevOps Engineer",
            "edition": "Community Local Runtime",
            "dashboard": {"version": version, "features": ["summary", "incident_queue", "investigation_queue", "investigation_detail", "telemetry", "connector_health"]},
            "version": version,
            "api_version": "v1",
            "execution": {"production_enabled": False, "mode": "approval-gated"},
            "components": ["Knowledge", "RAG", "Telemetry Ingestion", "Incident Engine", "Agent Commander", "Automated Investigation", "Knowledge Graph", "Skill Discovery", "Planner", "Policy", "Audit"],
            "telemetry": {"prometheus": True, "otlp_http_json_subset": True},
            "connectors": ["prometheus", "opentelemetry", "kubernetes", "linux"],
        }

    def seed_demo(self) -> dict[str, Any]:
        incident = {
            "incident_id": f"DEMO-{request_id('inc')[-6:]}",
            "tenant_id": "demo-tenant",
            "environment": "lab",
            "state": "CANDIDATE",
            "severity": "high",
            "confidence": 0.91,
            "candidate_reason": "CPU saturation, memory pressure and repeated pod restarts are temporally correlated.",
            "signals": ["cpu-high-001", "memory-pressure-001", "pod-restart-001"],
            "provenance": ["demo/synthetic-telemetry.json"],
            "created_at": self.now(),
            "updated_at": self.now(),
        }
        self.db.upsert_incident(incident)
        return incident

    def create_incident(self, payload: dict[str, Any]) -> dict[str, Any]:
        required = ["incident_id", "tenant_id", "environment"]
        for field in required:
            if not str(payload.get(field, "")).strip():
                raise ValueError(f"missing_{field}")
        now = self.now()
        incident = {
            "incident_id": str(payload["incident_id"]),
            "tenant_id": str(payload["tenant_id"]),
            "environment": str(payload["environment"]),
            "state": str(payload.get("state", "CANDIDATE")),
            "severity": str(payload.get("severity", "warning")),
            "confidence": float(payload.get("confidence", 0.0)),
            "candidate_reason": str(payload.get("candidate_reason", "")),
            "signals": list(payload.get("signals", [])),
            "provenance": list(payload.get("provenance", [])),
            "created_at": str(payload.get("created_at", now)),
            "updated_at": now,
        }
        if not 0.0 <= incident["confidence"] <= 1.0:
            raise ValueError("confidence_out_of_range")
        self.db.upsert_incident(incident)
        return incident

    def dashboard_summary(self, tenant_id: str | None = None) -> dict[str, Any]:
        incidents = self.db.list_incidents(tenant_id)
        investigations = self.db.list_investigations(tenant_id, 500)
        telemetry = self.db.list_telemetry_events(tenant_id, 1000)
        severities = {k: 0 for k in ("critical", "high", "warning", "info")}
        states: dict[str, int] = {}
        inv_status: dict[str, int] = {}
        for item in incidents:
            sev = str(item.get("severity", "info"))
            severities[sev] = severities.get(sev, 0) + 1
            state = str(item.get("state", "UNKNOWN"))
            states[state] = states.get(state, 0) + 1
        human_review_required = 0
        for item in investigations:
            status = str(item.get("status", "UNKNOWN"))
            inv_status[status] = inv_status.get(status, 0) + 1
            safety = item.get("safety") or {}
            if bool(safety.get("human_approval_required") or safety.get("human_review_required")):
                human_review_required += 1
        return {
            "status": "ok",
            "version": self.version(),
            "tenant_id": tenant_id,
            "totals": {"incidents": len(incidents), "investigations": len(investigations), "telemetry_events": len(telemetry)},
            "incidents": {"by_severity": severities, "by_state": states},
            "investigations": {"by_status": inv_status, "human_review_required": human_review_required},
            "telemetry": {"recent": min(len(telemetry), 100)},
            "execution": {"production_enabled": False, "mode": "approval-gated"},
        }

    def connector_metadata(self) -> dict[str, Any]:
        return {"status": "ok", "connectors": self.connectors.metadata()}

    def connector_health(self) -> dict[str, Any]:
        return self.connectors.health()

    def k8s_pods(self, namespace: str = "") -> dict[str, Any]:
        return self.connectors.get("kubernetes").list_pods(namespace)

    def linux_snapshot(self) -> dict[str, Any]:
        linux = self.connectors.get("linux")
        return {"cpu": linux.cpu_snapshot(), "memory": linux.memory()}

    def list_incidents(self, tenant_id: str | None = None) -> dict[str, Any]:
        return {"status": "ok", "results": self.db.list_incidents(tenant_id)}

    def get_incident(self, incident_id: str) -> dict[str, Any]:
        result = self.db.get_incident(incident_id)
        if result is None:
            raise FileNotFoundError("incident_not_found")
        return result

    def ingest_telemetry_event(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.telemetry.ingest_event(payload)

    def ingest_telemetry_events(self, payload: dict[str, Any]) -> dict[str, Any]:
        events = payload.get("events") if isinstance(payload, dict) else None
        if not isinstance(events, list):
            raise ValueError("events_array_required")
        return self.telemetry.ingest_events(events)

    def ingest_otlp(self, payload: dict[str, Any], tenant_id: str, environment: str, severity_hint: str = "info") -> dict[str, Any]:
        return self.telemetry.ingest_otlp(payload, tenant_id, environment, severity_hint)

    def query_prometheus(self, query: str) -> dict[str, Any]:
        return self.telemetry.query_prometheus(query)

    def poll_prometheus(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.telemetry.poll_prometheus(
            query=str(payload.get("query", "")),
            tenant_id=str(payload.get("tenant_id", "")),
            environment=str(payload.get("environment", "")),
            component_label=str(payload.get("component_label", "instance")),
            metric_family=str(payload.get("metric_family", "prometheus")),
            condition=str(payload.get("condition", "observed")),
            severity_hint=str(payload.get("severity_hint", "info")),
        )

    def list_telemetry_events(self, tenant_id: str | None = None, limit: int = 100) -> dict[str, Any]:
        return {"status": "ok", "results": self.telemetry.recent_events(tenant_id, limit)}

    def investigate_incident(self, incident_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = payload or {}
        mode = str(payload.get("mode", "dry-run"))
        include_connectors = bool(payload.get("include_connectors", True))
        return self.investigator.investigate(incident_id, mode, include_connectors)

    def list_investigations(self, tenant_id: str | None = None, limit: int = 100) -> dict[str, Any]:
        return {"status": "ok", "results": self.db.list_investigations(tenant_id, limit)}

    def get_investigation(self, investigation_id: str) -> dict[str, Any]:
        result = self.db.get_investigation(investigation_id)
        if result is None:
            raise FileNotFoundError("investigation_not_found")
        return result
