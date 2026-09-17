from __future__ import annotations

from collections import defaultdict
from typing import Dict, List


def allocate(events: List[Dict]) -> List[Dict]:
    totals = defaultdict(lambda: {"cost": 0.0, "tokens": 0, "tool_calls": 0})
    for e in events:
        key = (
            e["tenant_id"],
            e["environment"],
            e.get("model_id", "unknown"),
            e.get("skill_id", "unknown"),
            e.get("task_class", "unknown"),
        )
        totals[key]["cost"] += float(e.get("estimated_cost", 0.0))
        totals[key]["tokens"] += int(e.get("input_tokens", 0)) + int(e.get("output_tokens", 0))
        totals[key]["tool_calls"] += int(e.get("tool_calls", 0))

    result = []
    for key, value in sorted(totals.items()):
        result.append({
            "tenant_id": key[0],
            "environment": key[1],
            "model_id": key[2],
            "skill_id": key[3],
            "task_class": key[4],
            **value,
        })
    return result
