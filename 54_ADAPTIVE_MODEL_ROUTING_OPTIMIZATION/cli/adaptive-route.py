import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "router"))

from adaptive_router import AdaptiveRouter, Profile

PROFILES = [
    Profile("local-reference-standard","local","standard",0.0,1500,["summarization"]),
    Profile("claude-reference-advanced","anthropic","advanced",0.01,3500,["reasoning"]),
    Profile("critical-reference","reference","critical",0.015,7000,["reasoning","critical-evaluation"]),
]

HISTORY = [
    {"model_id":"local-reference-standard","task_class":"standard","observations":12,"success_rate":0.97,"grounding_rate":0.98,"safety_pass_rate":1.0,"mean_latency_ms":1500,"mean_cost_per_1k_tokens":0.0},
    {"model_id":"claude-reference-advanced","task_class":"advanced","observations":10,"success_rate":0.98,"grounding_rate":0.99,"safety_pass_rate":1.0,"mean_latency_ms":3600,"mean_cost_per_1k_tokens":0.01},
    {"model_id":"critical-reference","task_class":"critical","observations":8,"success_rate":0.99,"grounding_rate":1.0,"safety_pass_rate":1.0,"mean_latency_ms":7000,"mean_cost_per_1k_tokens":0.015},
]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--task", required=True)
    p.add_argument("--task-class", choices=["standard","advanced","critical"], default="standard")
    p.add_argument("--max-cost", type=float, default=0.02)
    p.add_argument("--max-latency-ms", type=float, default=12000)
    a = p.parse_args()

    result = AdaptiveRouter(PROFILES, HISTORY).route(
        "ADAPTIVE-CLI-001", a.task, a.task_class, "lab",
        max_cost_per_1k_tokens=a.max_cost,
        max_latency_ms=a.max_latency_ms,
    )
    print(json.dumps(result, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
