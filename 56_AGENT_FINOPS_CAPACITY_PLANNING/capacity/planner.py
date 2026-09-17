from __future__ import annotations

from typing import Dict


def plan(demand: Dict, capacity: Dict, minimum_headroom_ratio: float = 0.20) -> Dict:
    headroom = {}
    shortfalls = []

    for metric, cap in capacity.items():
        d = float(demand.get(metric, 0))
        c = float(cap)
        if c <= 0:
            headroom[metric] = 0.0
            if d > 0:
                shortfalls.append(metric)
            continue
        headroom[metric] = (c - d) / c
        if d > c:
            shortfalls.append(metric)

    recommendations = []
    if shortfalls:
        recommendations.append("capacity-review-required")
    if any(v < minimum_headroom_ratio for v in headroom.values()):
        recommendations.append("low-headroom-review")

    return {
        "demand": demand,
        "capacity": capacity,
        "headroom": headroom,
        "shortfalls": shortfalls,
        "recommendations": recommendations,
    }
