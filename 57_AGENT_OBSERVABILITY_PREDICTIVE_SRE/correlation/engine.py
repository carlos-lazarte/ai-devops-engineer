from __future__ import annotations

from typing import Dict, List


def correlate(events: List[Dict]) -> Dict:
    if not events:
        return {"correlated": False, "signals": [], "confidence": 0.0}
    anomalous = [e for e in events if e.get("severity") in ("warning", "critical")]
    confidence = min(1.0, len(anomalous) / max(3, len(events)))
    return {
        "correlated": len(anomalous) >= 2,
        "signals": [e["metric"] for e in anomalous],
        "confidence": round(confidence, 4),
    }
