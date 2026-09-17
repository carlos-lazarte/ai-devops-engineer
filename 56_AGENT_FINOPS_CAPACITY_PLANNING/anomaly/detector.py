from __future__ import annotations

from typing import Dict


def detect(observed: float, baseline: float, warning_ratio: float = 1.5, critical_ratio: float = 2.0) -> Dict:
    if baseline <= 0:
        severity = "critical" if observed > 0 else "info"
        ratio = float("inf") if observed > 0 else 1.0
    else:
        ratio = observed / baseline
        if ratio >= critical_ratio:
            severity = "critical"
        elif ratio >= warning_ratio:
            severity = "warning"
        else:
            severity = "info"

    return {
        "observed": observed,
        "baseline": baseline,
        "deviation_ratio": ratio,
        "severity": severity,
    }
