from __future__ import annotations

from typing import Dict, List, Tuple
from ingestion.normalize import normalize


def deduplicate(events: List[Dict], window_seconds: float = 300.0) -> Tuple[List[Dict], List[str]]:
    kept: List[Dict] = []
    suppressed: List[str] = []
    last_seen: Dict[tuple, float] = {}
    for raw in sorted(events, key=lambda x: float(x.get('timestamp', 0))):
        e = normalize(raw)
        key = (e['tenant_id'], e['environment'], e['component'], e['metric_family'], e['condition'])
        previous = last_seen.get(key)
        if previous is not None and e['timestamp'] - previous <= window_seconds:
            suppressed.append(e['event_id'])
            continue
        last_seen[key] = e['timestamp']
        kept.append(e)
    return kept, suppressed
