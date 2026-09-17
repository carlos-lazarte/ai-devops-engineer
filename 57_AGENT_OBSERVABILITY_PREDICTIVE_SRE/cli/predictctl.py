import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT))

from anomaly.detector import detect
from correlation.engine import correlate
from prediction.predictor import predict
from risk.assessor import assess


def main():
    p = argparse.ArgumentParser(description="Predictive SRE reference CLI")
    p.add_argument("--observed", type=float, default=180.0)
    p.add_argument("--baseline", type=float, default=100.0)
    p.add_argument("--signals", type=int, default=3)
    args = p.parse_args()

    events = [
        {**detect(args.observed, args.baseline), "metric": f"signal-{i+1}"}
        for i in range(args.signals)
    ]
    corr = correlate(events)
    pred = predict(corr)
    risk = assess(
        likelihood=min(1.0, args.observed / max(args.baseline * 2.0, 1.0)),
        impact=0.8 if args.signals >= 3 else 0.3,
        confidence=pred["confidence"],
    )
    print(json.dumps({
        "correlation": corr,
        "prediction": pred,
        "risk": risk,
        "automatic_remediation": False,
        "production_execution_enabled": False,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
