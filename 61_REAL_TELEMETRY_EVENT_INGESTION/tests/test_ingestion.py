import json
import tempfile
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "35_RUNTIME"))
sys.path.insert(0, str(ROOT / "61_REAL_TELEMETRY_EVENT_INGESTION"))

from app.store import IncidentStore
from service.ingest import TelemetryIngestionService
from adapters.otlp import parse_metrics
from adapters.prometheus import PrometheusClient


def mk():
    td = tempfile.TemporaryDirectory()
    store = IncidentStore(sqlite_path=Path(td.name) / "test.db")
    return td, store, TelemetryIngestionService(store)


def test_generic_event_creates_candidate_and_persists():
    td, store, svc = mk()
    try:
        base = 1_900_000_000.0
        events = [
            {"event_id":"e1","timestamp":base,"tenant_id":"t1","environment":"prod","component":"node-a","metric_family":"cpu","condition":"high","severity_hint":"high","value":95,"source":"test"},
            {"event_id":"e2","timestamp":base+20,"tenant_id":"t1","environment":"prod","component":"node-a","metric_family":"memory","condition":"high","severity_hint":"high","value":92,"source":"test"},
        ]
        out = svc.ingest_events(events)
        assert out["accepted"] == 2
        assert out["candidates"]
        assert store.list_telemetry_events("t1", 10)[0]["tenant_id"] == "t1"
    finally:
        td.cleanup()


def test_otlp_subset_maps_metric_to_event():
    payload = {"resourceMetrics":[{"resource":{"attributes":[{"key":"service.name","value":{"stringValue":"payments"}}]},"scopeMetrics":[{"metrics":[{"name":"cpu.utilization","gauge":{"dataPoints":[{"timeUnixNano":"1900000000000000000","asDouble":0.95}]}}]}]}]}
    events = parse_metrics(payload, "t1", "prod", "warning")
    assert len(events) == 1
    assert events[0]["component"] == "payments"
    assert events[0]["metric_family"] == "cpu.utilization"
    assert events[0]["value"] == 0.95


def test_prometheus_vector_mapping():
    payload = {"status":"success","data":{"resultType":"vector","result":[{"metric":{"instance":"node-a","job":"node"},"value":[1900000000,"95"]}]}}
    events = PrometheusClient.result_to_events(payload, "t1", "prod", severity_hint="high")
    assert len(events) == 1
    assert events[0]["component"] == "node-a"
    assert events[0]["value"] == 95.0


def test_tenant_isolation():
    td, store, svc = mk()
    try:
        event = {"event_id":"e1","timestamp":1900000000,"tenant_id":"tenant-a","environment":"prod","component":"n1","metric_family":"cpu","condition":"high"}
        svc.ingest_event(event)
        assert store.list_telemetry_events("tenant-b", 10) == []
        assert store.list_telemetry_events("tenant-a", 10)[0]["tenant_id"] == "tenant-a"
    finally:
        td.cleanup()
