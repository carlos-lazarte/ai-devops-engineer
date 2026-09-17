import sys
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "router"))

from adaptive_router import AdaptiveRouter, Profile


def profiles():
    return [
        Profile("standard","local","standard",0.0,1500,["summarization"]),
        Profile("advanced","provider","advanced",0.01,3500,["reasoning"]),
        Profile("critical","provider","critical",0.015,7000,["reasoning"]),
    ]


def test_adaptive_standard_prefers_local_reference():
    history = [
        {"model_id":"standard","task_class":"standard","observations":10,"success_rate":0.97,"grounding_rate":0.98,"safety_pass_rate":1.0,"mean_latency_ms":1500,"mean_cost_per_1k_tokens":0.0},
        {"model_id":"advanced","task_class":"standard","observations":10,"success_rate":0.98,"grounding_rate":0.99,"safety_pass_rate":1.0,"mean_latency_ms":3600,"mean_cost_per_1k_tokens":0.01},
    ]
    result = AdaptiveRouter(profiles(), history).route("t1","summarize","standard","lab")
    assert result["decision"] == "selected"
    assert result["selected_model"] == "standard"


def test_critical_quality_is_hard_constraint():
    history = [
        {"model_id":"advanced","task_class":"critical","observations":10,"success_rate":0.999,"grounding_rate":1.0,"safety_pass_rate":1.0,"mean_latency_ms":1000,"mean_cost_per_1k_tokens":0.001},
        {"model_id":"critical","task_class":"critical","observations":2,"success_rate":0.90,"grounding_rate":0.95,"safety_pass_rate":1.0,"mean_latency_ms":7000,"mean_cost_per_1k_tokens":0.015},
    ]
    result = AdaptiveRouter(profiles(), history).route("t2","critical incident","critical","lab")
    assert result["selected_model"] == "critical"


def test_budget_blocks_models():
    result = AdaptiveRouter(profiles(), []).route(
        "t3","advanced task","advanced","lab",max_latency_ms=1000
    )
    assert result["decision"] == "blocked"
