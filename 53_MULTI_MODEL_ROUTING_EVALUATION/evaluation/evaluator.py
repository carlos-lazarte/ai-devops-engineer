from __future__ import annotations
from typing import Dict, List

def evaluate(results: List[Dict]) -> Dict:
    if not results:
        raise ValueError("results required")
    n = len(results)
    return {
        "task_success_rate": sum(bool(r["task_success"]) for r in results) / n,
        "grounding_rate": sum(float(r["grounding_rate"]) for r in results) / n,
        "safety_pass_rate": sum(bool(r["safety_pass"]) for r in results) / n,
        "mean_latency_ms": sum(float(r["latency_ms"]) for r in results) / n,
        "mean_estimated_cost": sum(float(r["estimated_cost"]) for r in results) / n,
        "model_count": len({r["model_id"] for r in results}),
        "scenario_count": len({r["scenario_id"] for r in results}),
    }

def release_check(metrics: Dict, thresholds: Dict) -> Dict:
    failures = []
    if metrics["task_success_rate"] < thresholds["min_task_success_rate"]:
        failures.append("task_success_rate_below_threshold")
    if metrics["grounding_rate"] < thresholds["min_grounding_rate"]:
        failures.append("grounding_rate_below_threshold")
    if metrics["safety_pass_rate"] < thresholds["min_safety_pass_rate"]:
        failures.append("safety_pass_rate_below_threshold")
    if metrics["mean_latency_ms"] > thresholds["max_mean_latency_ms"]:
        failures.append("latency_above_threshold")
    if metrics["mean_estimated_cost"] > thresholds["max_mean_estimated_cost"]:
        failures.append("cost_above_threshold")
    return {"status": "BLOCKED" if failures else "PASS", "failures": failures}
