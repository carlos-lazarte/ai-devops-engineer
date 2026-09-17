from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "65_PUBLIC_DEMO_GITHUB_COMMUNITY_EDITION"

def test_public_release_manifest_exists():
    assert (PUBLIC / "release-manifest.json").exists()

def test_demo_script_is_executable():
    p = PUBLIC / "demo" / "run_demo.sh"
    assert p.exists() and p.stat().st_mode & 0o111

def test_public_manifest_declares_safe_defaults():
    data = json.loads((PUBLIC / "release-manifest.json").read_text())
    assert data["version"] == "3.13.0"
    assert data["execution"]["production_enabled"] is False
    assert data["demo"]["uses_synthetic_data"] is True
    assert data["demo"]["requires_model_api_key"] is False

def test_community_controls_present():
    for name in ["README.md", "LICENSE", "NOTICE", "SECURITY.md", "COMMUNITY.md", "SUPPORT.md"]:
        assert (ROOT / name).exists(), name
