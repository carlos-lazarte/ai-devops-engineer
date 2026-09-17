from __future__ import annotations

import tempfile
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "35_RUNTIME"))
sys.path.insert(0, str(ROOT / "63_AUTOMATED_INCIDENT_INVESTIGATION"))

from app.store import IncidentStore
from investigation.engine import AutomatedIncidentInvestigator


def setup():
    td = tempfile.TemporaryDirectory()
    store = IncidentStore(sqlite_path=Path(td.name) / "test.db")
    investigator = AutomatedIncidentInvestigator(ROOT, store)
    return td, store, investigator


def test_investigation_is_evidence_grounded_and_plan_only():
    td, store, investigator = setup()
    try:
        store.upsert_incident({
            "incident_id": "INC-1", "tenant_id": "t1", "environment": "prod",
            "state": "CANDIDATE", "severity": "high", "confidence": 0.9,
            "candidate_reason": "CPU saturation, memory pressure and pod restarts are correlated.",
            "signals": ["e1", "e2", "e3"], "provenance": ["test"],
            "created_at": "2026-09-17T10:00:00+00:00", "updated_at": "2026-09-17T10:00:00+00:00",
        })
        store.save_telemetry_events([
            {"event_id":"e1","timestamp":1900000000,"tenant_id":"t1","environment":"prod","component":"node-1","metric_family":"cpu","condition":"high","severity_hint":"high","value":95,"source":"test","labels":{},"topology_neighbors":[],"provenance":{"source":"test"}},
            {"event_id":"e2","timestamp":1900000010,"tenant_id":"t1","environment":"prod","component":"node-1","metric_family":"memory","condition":"high","severity_hint":"high","value":92,"source":"test","labels":{},"topology_neighbors":[],"provenance":{"source":"test"}},
            {"event_id":"e3","timestamp":1900000020,"tenant_id":"t1","environment":"prod","component":"payments","metric_family":"pod_restart","condition":"high","severity_hint":"high","value":7,"source":"test","labels":{},"topology_neighbors":[],"provenance":{"source":"test"}},
        ])
        result = investigator.investigate("INC-1", mode="dry-run", include_connectors=False)
        assert result["status"] == "ANALYZED"
        assert result["safety"]["production_execution_enabled"] is False
        assert result["safety"]["root_cause_confirmed"] is False
        assert result["plan"]["execution_mode"] == "plan_only"
        assert result["evidence"]
        assert any(h["id"] == "H-RESOURCE-EXHAUSTION" for h in result["hypotheses"])
        assert result["knowledge"]["rag"]
        assert result["knowledge"]["skills"]
    finally:
        td.cleanup()


def test_investigation_isolated_by_tenant():
    td, store, investigator = setup()
    try:
        for tenant in ("t1", "t2"):
            store.upsert_incident({
                "incident_id": f"INC-{tenant}", "tenant_id": tenant, "environment": "prod",
                "state": "CANDIDATE", "severity": "warning", "confidence": 0.8,
                "candidate_reason": "CPU degradation detected.", "signals": [f"{tenant}-e1"], "provenance": ["test"],
                "created_at": "2026-09-17T10:00:00+00:00", "updated_at": "2026-09-17T10:00:00+00:00",
            })
        store.save_telemetry_events([
            {"event_id":"t1-e1","timestamp":1900000000,"tenant_id":"t1","environment":"prod","component":"n1","metric_family":"cpu","condition":"high","severity_hint":"high","value":95,"source":"test","labels":{},"topology_neighbors":[],"provenance":{"source":"t1"}},
            {"event_id":"t2-e1","timestamp":1900000000,"tenant_id":"t2","environment":"prod","component":"n2","metric_family":"memory","condition":"high","severity_hint":"high","value":93,"source":"test","labels":{},"topology_neighbors":[],"provenance":{"source":"t2"}},
        ])
        result = investigator.investigate("INC-t1", include_connectors=False)
        ids = {e.get("event_id") for e in result["evidence"] if e.get("type") == "telemetry"}
        assert "t1-e1" in ids
        assert "t2-e1" not in ids
    finally:
        td.cleanup()


def test_trigger_policy_blocks_below_confidence():
    td, store, investigator = setup()
    try:
        store.upsert_incident({
            "incident_id": "LOW", "tenant_id": "t1", "environment": "prod",
            "state": "CANDIDATE", "severity": "high", "confidence": 0.2,
            "candidate_reason": "low confidence", "signals": [], "provenance": [],
            "created_at": "2026-09-17T10:00:00+00:00", "updated_at": "2026-09-17T10:00:00+00:00",
        })
        try:
            investigator.investigate("LOW", include_connectors=False)
        except ValueError as exc:
            assert str(exc) == "investigation_trigger_denied"
        else:
            raise AssertionError("low-confidence incident was investigated")
    finally:
        td.cleanup()


def test_persisted_investigation_can_be_retrieved():
    td, store, investigator = setup()
    try:
        store.upsert_incident({
            "incident_id": "INC-PERSIST", "tenant_id": "t1", "environment": "lab",
            "state": "CANDIDATE", "severity": "warning", "confidence": 0.8,
            "candidate_reason": "test incident", "signals": [], "provenance": [],
            "created_at": "2026-09-17T10:00:00+00:00", "updated_at": "2026-09-17T10:00:00+00:00",
        })
        result = investigator.investigate("INC-PERSIST", include_connectors=False)
        stored = store.get_investigation(result["investigation_id"])
        assert stored is not None
        assert stored["incident_id"] == "INC-PERSIST"
        assert stored["safety"]["human_approval_required"] is True
    finally:
        td.cleanup()
