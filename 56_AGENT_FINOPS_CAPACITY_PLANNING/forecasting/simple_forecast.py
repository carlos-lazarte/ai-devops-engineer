from __future__ import annotations

from statistics import mean
from typing import List, Dict


def forecast_cost(history: List[float], periods: int = 1) -> Dict:
    if not history:
        raise ValueError("history required")
    baseline = mean(history)
    return {
        "method": "moving-average-reference",
        "baseline": baseline,
        "periods": periods,
        "forecast_cost": baseline * periods,
        "confidence": 0.50,
    }


def forecast_tokens(history: List[int], periods: int = 1) -> Dict:
    if not history:
        raise ValueError("history required")
    baseline = mean(history)
    return {
        "method": "moving-average-reference",
        "baseline": baseline,
        "periods": periods,
        "forecast_tokens": int(round(baseline * periods)),
        "confidence": 0.50,
    }
