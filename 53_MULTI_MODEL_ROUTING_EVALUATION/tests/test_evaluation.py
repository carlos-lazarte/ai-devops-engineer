import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "evaluation"))
from evaluator import evaluate, release_check

def test_reference_results_pass():
    results = [
        {"model_id":"a","scenario_id":"s1","task_success":True,"grounding_rate":1.0,"safety_pass":True,"latency_ms":3000,"estimated_cost":0.01},
        {"model_id":"b","scenario_id":"s2","task_success":True,"grounding_rate":1.0,"safety_pass":True,"latency_ms":5000,"estimated_cost":0.015},
    ]
    m = evaluate(results)
    out = release_check(m, {
        "min_task_success_rate":0.9,
        "min_grounding_rate":0.95,
        "min_safety_pass_rate":1.0,
        "max_mean_latency_ms":12000,
        "max_mean_estimated_cost":0.02,
    })
    assert out["status"] == "PASS"
