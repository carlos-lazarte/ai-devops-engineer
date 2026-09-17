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
