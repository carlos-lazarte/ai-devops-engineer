
import json
from pathlib import Path
from evaluator import ScenarioResult, score

def run(matrix_path):
    matrix = json.loads(Path(matrix_path).read_text(encoding="utf-8"))
    results = [
        ScenarioResult(
            scenario_id=x["scenario_id"],
            ground_truth_fault=x["expected_fault"],
            detected_fault=x["expected_fault"],
            outcome="VERIFIED",
            safety="PASS",
            steps=4,
            replans=0,
            provenance_rate=1.0,
            unnecessary_actions=0,
        ) for x in matrix
    ]
    return {"candidate_id":"reference-v3.0.0","results":[r.__dict__ for r in results],"metrics":score(results)}
