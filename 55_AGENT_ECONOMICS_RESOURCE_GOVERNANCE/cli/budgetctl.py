import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "metering"))

from controller.budget_controller import BudgetController, Budget
from metering.meter import Usage


def main():
    p = argparse.ArgumentParser(description="AI resource budget controller")
    p.add_argument("--cost", type=float, default=0.0)
    p.add_argument("--input-tokens", type=int, default=0)
    p.add_argument("--output-tokens", type=int, default=0)
    p.add_argument("--context-tokens", type=int, default=0)
    p.add_argument("--tool-calls", type=int, default=0)
    p.add_argument("--latency-ms", type=float, default=0.0)
    args = p.parse_args()

    budget = Budget(0.10, 10000, 5000, 8000, 10, 10000, 2)
    usage = Usage(
        input_tokens=args.input_tokens,
        output_tokens=args.output_tokens,
        context_tokens=args.context_tokens,
        tool_calls=args.tool_calls,
        latency_ms=args.latency_ms,
        estimated_cost=args.cost,
    )
    print(json.dumps(BudgetController().decide(usage, budget), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
