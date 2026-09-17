from __future__ import annotations

from collections import Counter
from typing import Any


def build_evidence(incident: dict[str, Any], events: list[dict[str, Any]], connector_observations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    evidence: list[dict[str, Any]] = []
    event_ids = set(incident.get("signals", []))
    matched = [e for e in events if e.get("event_id") in event_ids]
    if not matched and events:
        matched = events[:20]

    for event in matched[:30]:
        evidence.append({
            "evidence_id": f"telemetry:{event['event_id']}",
            "type": "telemetry",
            "source": event.get("source", "unknown"),
            "event_id": event.get("event_id"),
            "component": event.get("component"),
            "metric_family": event.get("metric_family"),
            "condition": event.get("condition"),
            "value": event.get("value"),
            "severity_hint": event.get("severity_hint"),
            "observed_at": event.get("timestamp"),
            "provenance": event.get("provenance", {}),
        })

    for observation in connector_observations:
        evidence.append(observation)

    return evidence


def summarize_telemetry(events: list[dict[str, Any]]) -> dict[str, Any]:
    families = Counter(str(e.get("metric_family", "unknown")) for e in events)
    conditions = Counter(str(e.get("condition", "unknown")) for e in events)
    components = sorted({str(e.get("component", "unknown")) for e in events})
    values = [e.get("value") for e in events if isinstance(e.get("value"), (int, float))]
    return {
        "event_count": len(events),
        "components": components,
        "metric_families": dict(families),
        "conditions": dict(conditions),
        "numeric_values": values[:50],
    }
