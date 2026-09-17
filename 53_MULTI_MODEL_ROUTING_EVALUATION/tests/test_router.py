import sys
from pathlib import Path
HERE = Path(__file__).resolve()
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "router"))

from router import ModelRouter, ModelProfile

def profiles():
    return [
        ModelProfile("standard","local","standard",["structured-output"],0.0,1500),
        ModelProfile("advanced","provider","advanced",["reasoning"],0.01,3500),
        ModelProfile("critical","provider","critical",["reasoning"],0.015,7000),
    ]

def test_critical_routes_to_critical():
    r = ModelRouter(profiles()).route(
        "t1","critical incident","critical","lab",
        min_quality_tier="standard"
    )
    assert r["decision"] == "selected"
    assert r["selected_model"] == "critical"

def test_standard_prefers_lower_tier_when_eligible():
    r = ModelRouter(profiles()).route(
        "t2","summarize evidence","standard","lab"
    )
    assert r["selected_model"] == "standard"

def test_no_eligible_model_blocks():
    r = ModelRouter(profiles()).route(
        "t3","critical incident","critical","lab",
        max_latency_ms=5000
    )
    assert r["decision"] == "blocked"
