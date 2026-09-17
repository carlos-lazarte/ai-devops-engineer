from __future__ import annotations

from typing import Dict


def assess(likelihood: float, impact: float, confidence: float) -> Dict:
    score = max(0.0, min(1.0, likelihood)) * max(0.0, min(1.0, impact))
    if score >= 0.75:
        level = "critical"
    elif score >= 0.50:
        level = "high"
    elif score >= 0.25:
        level = "medium"
    else:
        level = "low"
    return {
        "risk_level": level,
        "risk_score": round(score, 4),
        "confidence": confidence,
        "human_review_required": level in {"high", "critical"},
    }
