from pathlib import Path
import tempfile

from app.product import ProductService
from app.store import IncidentStore


def service():
    td = tempfile.TemporaryDirectory()
    db = IncidentStore(sqlite_path=Path(td.name)/"test.db")
    s = ProductService(Path(__file__).resolve().parents[2], db)
    return td, s


def test_seed_and_list_incident():
    td, s = service()
    try:
        inc = s.seed_demo()
        out = s.list_incidents()
        assert out["results"][0]["incident_id"] == inc["incident_id"]
        assert out["results"][0]["environment"] == "lab"
    finally:
        td.cleanup()


def test_create_rejects_bad_confidence():
    td, s = service()
    try:
        try:
            s.create_incident({"incident_id":"x","tenant_id":"t","environment":"lab","confidence":1.2})
        except ValueError as exc:
            assert str(exc) == "confidence_out_of_range"
        else:
            raise AssertionError("invalid confidence accepted")
    finally:
        td.cleanup()


def test_tenant_filter():
    td, s = service()
    try:
        s.create_incident({"incident_id":"a","tenant_id":"t1","environment":"lab","confidence":.8})
        s.create_incident({"incident_id":"b","tenant_id":"t2","environment":"lab","confidence":.8})
        assert [x["incident_id"] for x in s.list_incidents("t1")["results"]] == ["a"]
    finally:
        td.cleanup()


def test_product_and_dashboard_versions_match_repository_version():
    td, s = service()
    try:
        expected = (Path(__file__).resolve().parents[2] / "VERSION").read_text(encoding="utf-8").strip()
        assert s.product_info()["version"] == expected
        assert s.product_info()["dashboard"]["version"] == expected
        assert s.dashboard_summary()["version"] == expected
    finally:
        td.cleanup()


def test_dashboard_counts_human_approval_requirement():
    td, s = service()
    try:
        s.db.save_investigation({
            "investigation_id": "inv-test-001",
            "incident_id": "incident-test-001",
            "tenant_id": "demo-tenant",
            "environment": "lab",
            "status": "ANALYZED",
            "mode": "dry-run",
            "trigger": {},
            "telemetry": {},
            "evidence": [],
            "hypotheses": [],
            "unknowns": [],
            "requested_diagnostics": [],
            "proposed_actions": [],
            "knowledge": {},
            "plan": {},
            "agent": None,
            "safety": {
                "production_execution_enabled": False,
                "human_approval_required": True,
                "connector_mode": "read-only",
                "root_cause_confirmed": False,
            },
            "provenance": {},
            "created_at": "2026-09-17T00:00:00+00:00",
            "updated_at": "2026-09-17T00:00:00+00:00",
        })
        out = s.dashboard_summary("demo-tenant")
        assert out["investigations"]["human_review_required"] == 1
    finally:
        td.cleanup()
