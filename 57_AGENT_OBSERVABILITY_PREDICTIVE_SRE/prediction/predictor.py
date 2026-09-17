from __future__ import annotations

from typing import Dict


def predict(correlation: Dict, min_confidence: float = 0.8) -> Dict:
    if correlation.get("correlated") and correlation.get("confidence", 0.0) >= min_confidence:
        return {
            "state": "PREDICTED",
            "confidence": correlation["confidence"],
            "prediction": "possible_agent_performance_degradation",
        }
    return {
        "state": "OBSERVED",
        "confidence": correlation.get("confidence", 0.0),
        "prediction": None,
    }
