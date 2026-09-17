from __future__ import annotations

from typing import Dict, List
from dedup.deduplicator import deduplicate
from correlator.engine import correlate
from incident.builder import build_candidates


def build_incident_candidates(events: List[Dict], dedup_window: float = 300.0,
                              correlation_window: float = 300.0,
                              threshold: float = 0.55) -> Dict:
    unique, suppressed = deduplicate(events, dedup_window)
    groups = correlate(unique, correlation_window, threshold)
    candidates = build_candidates(groups)
    return {'candidates': candidates, 'suppressed_event_ids': suppressed}
