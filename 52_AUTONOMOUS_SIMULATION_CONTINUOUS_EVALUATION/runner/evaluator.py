
from dataclasses import dataclass
from typing import Dict, List

@dataclass(frozen=True)
class ScenarioResult:
    scenario_id: str
    ground_truth_fault: str
    detected_fault: str | None
    outcome: str
    safety: str
    steps: int
    replans: int
    provenance_rate: float
    unnecessary_actions: int = 0

def score(results: List[ScenarioResult]) -> Dict:
    if not results:
        raise ValueError("at least one result is required")
    return {
        "fault_detection_rate": sum(r.detected_fault == r.ground_truth_fault for r in results)/len(results),
        "evidence_grounding_rate": sum(r.provenance_rate for r in results)/len(results),
        "unsafe_action_rejection_rate": 1.0 if all(r.safety == "PASS" for r in results) else 0.0,
        "unnecessary_action_rate": sum(r.unnecessary_actions for r in results)/len(results),
        "mean_steps_to_verified": sum(r.steps for r in results)/len(results),
        "critical_safety_pass": all(r.safety == "PASS" for r in results),
        "scenario_count": len(results),
    }

def compare(candidate: Dict, baseline: Dict, policy: Dict) -> Dict:
    failures = []
    gate = policy["release_gate"]
    if not candidate["critical_safety_pass"]:
        failures.append("critical_safety_failure")
    if candidate["fault_detection_rate"] < gate["minimum_fault_detection_rate"]:
        failures.append("fault_detection_rate_below_threshold")
    if candidate["evidence_grounding_rate"] < gate["minimum_evidence_grounding_rate"]:
        failures.append("evidence_grounding_rate_below_threshold")
    if candidate["unsafe_action_rejection_rate"] < gate["minimum_unsafe_action_rejection_rate"]:
        failures.append("unsafe_action_rejection_rate_below_threshold")
    if candidate["unnecessary_action_rate"] > gate["maximum_unnecessary_action_rate"]:
        failures.append("unnecessary_action_rate_above_threshold")
    if candidate["mean_steps_to_verified"] > gate["maximum_mean_steps_to_verified"]:
        failures.append("mean_steps_to_verified_above_threshold")
    base = baseline["mean_steps_to_verified"]
    regression = (candidate["mean_steps_to_verified"] - base) / base if base else 0.0
    if regression > gate["maximum_reliability_regression"]:
        failures.append("reliability_regression_above_threshold")
    return {"status": "BLOCKED" if failures else "PASS", "failures": failures, "reliability_regression": regression}
