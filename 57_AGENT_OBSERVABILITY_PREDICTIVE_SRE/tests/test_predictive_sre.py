import sys
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT))

from anomaly.detector import detect
from correlation.engine import correlate
from prediction.predictor import predict
from risk.assessor import assess


def test_correlation_and_prediction():
    events = [
        {**detect(180, 100), "metric": "latency"},
        {**detect(180, 100), "metric": "tool_calls"},
        {**detect(180, 100), "metric": "cost"},
    ]
    corr = correlate(events)
    pred = predict(corr, min_confidence=0.66)
    assert corr["correlated"] is True
    assert pred["state"] == "PREDICTED"


def test_low_signal_is_not_prediction():
    event = detect(120, 100)
    corr = correlate([{**event, "metric": "latency"}])
    pred = predict(corr)
    assert pred["state"] == "OBSERVED"


def test_high_risk_requires_review():
    out = assess(0.9, 0.9, 0.9)
    assert out["risk_level"] == "critical"
    assert out["human_review_required"] is True
