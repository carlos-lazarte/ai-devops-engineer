from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
BASE = Path(__file__).resolve().parents[0].parent

def parse_top_level(path):
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line and not line.startswith(" ") and ":" in line:
            k, v = line.split(":", 1)
            out[k] = v.strip().strip('"')
    return out

def test_manifests_valid():
    for p in BASE.glob("skills/*/skill.yaml"):
        d = parse_top_level(p)
        for k in ["skill_id","name","version","platform_api","contract_version","risk","autonomy_level"]:
            assert k in d and d[k]
        assert re.match(r"^\d+\.\d+\.\d+$", d["version"])
        assert d["autonomy_level"] in {"L0","L1","L2","L3","L4"}

def test_critical_autonomy_blocked_by_policy():
    policy = (BASE / "policies/Marketplace-Policy.yaml").read_text(encoding="utf-8")
    assert "allow_critical_autonomy: false" in policy

def test_registry_has_three_reference_skills():
    registry = (BASE / "registry/skill-registry.yaml").read_text(encoding="utf-8")
    assert registry.count("skill_id:") == 3
