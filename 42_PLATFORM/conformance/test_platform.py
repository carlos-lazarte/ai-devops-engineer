from pathlib import Path
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_stable_api_contract_exists():
    p = ROOT / "api/v1/runtime-openapi.yaml"
    spec = yaml.safe_load(p.read_text(encoding="utf-8"))
    assert spec["openapi"].startswith("3.")
    for path in ["/api/v1/health", "/api/v1/ready", "/api/v1/version", "/api/v1/search", "/api/v1/incidents/analyze"]:
        assert path in spec["paths"]


def test_platform_config_is_fail_closed():
    p = ROOT / "config/platform.yaml"
    cfg = yaml.safe_load(p.read_text(encoding="utf-8"))
    assert cfg["policy"]["default_decision"] == "deny"
    assert cfg["policy"]["human_approval_required_for_actions"] is True
    assert cfg["platform"]["production_execution_enabled"] is False


def test_runtime_contract_is_documented():
    assert (ROOT.parent / "35_RUNTIME/schemas/runtime-response.json").is_file()
    data = json.loads((ROOT.parent / "35_RUNTIME/schemas/runtime-response.json").read_text(encoding="utf-8"))
    assert "request_id" in data["required"]
