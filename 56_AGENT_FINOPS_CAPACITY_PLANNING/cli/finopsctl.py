import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT))

from anomaly.detector import detect
from forecasting.simple_forecast import forecast_cost
from capacity.planner import plan


def main():
    p = argparse.ArgumentParser(description="AI Agent FinOps reference CLI")
    p.add_argument("--baseline", type=float, default=100.0)
    p.add_argument("--observed", type=float, default=100.0)
    p.add_argument("--capacity", type=float, default=1000.0)
    p.add_argument("--demand", type=float, default=800.0)
    args = p.parse_args()

    anomaly = detect(args.observed, args.baseline)
    capacity = plan({"cost": args.demand}, {"cost": args.capacity})
    forecast = forecast_cost([args.baseline], 1)

    print(json.dumps({
        "anomaly": anomaly,
        "capacity": capacity,
        "forecast": forecast,
        "budget_auto_increase": False,
        "production_execution_enabled": False,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
