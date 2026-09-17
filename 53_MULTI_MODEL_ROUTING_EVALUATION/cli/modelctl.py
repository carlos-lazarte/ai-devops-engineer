import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "router"))

from router import ModelRouter, ModelProfile

PROFILES = [
    ModelProfile("claude-reference-advanced","anthropic","advanced",["reasoning","technical-analysis"],0.01,3500),
    ModelProfile("local-reference-standard","local","standard",["summarization"],0.0,1500),
    ModelProfile("critical-reference","reference","critical",["reasoning","critical-evaluation"],0.015,7000),
]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--task", required=True)
    p.add_argument("--task-class", choices=["standard","critical"], default="standard")
    p.add_argument("--max-latency-ms", type=float, default=12000)
    args = p.parse_args()
    result = ModelRouter(PROFILES).route(
        "CLI-ROUTE-001", args.task, args.task_class, "lab",
        max_latency_ms=args.max_latency_ms
    )
    print(json.dumps(result, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
