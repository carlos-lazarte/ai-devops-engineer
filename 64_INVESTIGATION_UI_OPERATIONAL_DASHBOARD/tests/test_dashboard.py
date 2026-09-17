from pathlib import Path
import tempfile

from app.product import ProductService
from app.store import IncidentStore
from app.ui import HTML


def make_service():
    td = tempfile.TemporaryDirectory()
    db = IncidentStore(sqlite_path=Path(td.name) / "test.db")
    service = ProductService(Path(__file__).resolve().parents[2], db)
    return td, service


def test_dashboard_summary_aggregates():
    td, service = make_service()
    try:
        service.create_incident({
            "incident_id": "i-1", "tenant_id": "t1", "environment": "prod",
            "severity": "critical", "confidence": 0.95,
        })
        service.create_incident({
            "incident_id": "i-2", "tenant_id": "t1", "environment": "lab",
            "severity": "high", "confidence": 0.8,
        })
        service.ingest_telemetry_event({
            "event_id": "e-1", "timestamp": 1, "tenant_id": "t1", "environment": "prod",
            "component": "node-1", "metric_family": "cpu", "condition": "high",
            "severity_hint": "high", "value": 95, "source": "test",
        })
        out = service.dashboard_summary("t1")
        assert out["totals"] == {"incidents": 3, "investigations": 0, "telemetry_events": 1}
        assert out["incidents"]["by_severity"]["critical"] == 1
        assert out["incidents"]["by_severity"]["high"] == 1
        assert out["incidents"]["by_severity"]["low"] == 1
        assert out["execution"]["production_enabled"] is False
    finally:
        td.cleanup()


def test_dashboard_summary_tenant_isolation():
    td, service = make_service()
    try:
        service.create_incident({"incident_id": "a", "tenant_id": "t1", "environment": "prod", "confidence": 0.8})
        service.create_incident({"incident_id": "b", "tenant_id": "t2", "environment": "prod", "confidence": 0.8})
        out = service.dashboard_summary("t1")
        assert out["totals"]["incidents"] == 1
    finally:
        td.cleanup()


def test_dashboard_ui_safety_and_version():
    assert "v3.14.0" in HTML
    assert "Production execution is disabled" in HTML
    assert "/api/v1/dashboard/summary" in HTML
    assert "innerHTML" in HTML  # dynamic rendering exists; escaped values are used at the DOM boundary.
