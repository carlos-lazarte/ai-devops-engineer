from __future__ import annotations

from typing import Dict, List
from topology.graph import related_components
from severity.advisor import advise


def _reason(group: Dict) -> str:
    events = group['events']
    components = sorted({e['component'] for e in events})
    families = sorted({e['metric_family'] for e in events})
    if len(events) >= 2:
        return f"{len(events)} signals correlated across {len(components)} component(s) and {len(families)} metric family(ies) within the configured time window."
    return 'Single signal retained as an incident candidate because it crossed the candidate creation threshold for the source/policy.'


def build_candidates(groups: List[Dict]) -> List[Dict]:
    out = []
    for idx, group in enumerate(groups, start=1):
        events = group['events']
        severity = advise(events, group['confidence'])
        out.append({
            'incident_id': f"inc-candidate-{idx:04d}",
            'correlation_id': group['correlation_id'],
            'state': 'CANDIDATE',
            'tenant_id': group['tenant_id'],
            'environment': group['environment'],
            'signals': group['event_ids'],
            'severity': severity,
            'confidence': group['confidence'],
            'candidate_reason': _reason(group),
            'first_seen': min(e['timestamp'] for e in events),
            'last_seen': max(e['timestamp'] for e in events),
            'related_components': related_components(events),
            'recommended_skill': 'incident-triage',
            'plan_reference': None,
            'provenance': [e.get('provenance', {}) for e in events],
            'human_review_required': severity in {'high', 'critical'},
            'production_execution_enabled': False,
        })
    return out
