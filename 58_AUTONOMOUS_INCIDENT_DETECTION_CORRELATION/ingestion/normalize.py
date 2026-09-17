from __future__ import annotations

from typing import Any, Dict
import re


def _norm(value: Any) -> str:
    value = '' if value is None else str(value).strip().lower()
    value = re.sub(r'[^a-z0-9_.:-]+', '-', value)
    return value.strip('-')


def normalize(raw: Dict[str, Any]) -> Dict[str, Any]:
    required = ['event_id', 'timestamp', 'tenant_id', 'environment', 'component', 'metric_family', 'condition']
    missing = [k for k in required if not raw.get(k)]
    if missing:
        raise ValueError(f'missing required fields: {missing}')
    return {
        'event_id': str(raw['event_id']),
        'timestamp': float(raw['timestamp']),
        'tenant_id': _norm(raw['tenant_id']),
        'environment': _norm(raw['environment']),
        'component': _norm(raw['component']),
        'metric_family': _norm(raw['metric_family']),
        'condition': _norm(raw['condition']),
        'severity_hint': _norm(raw.get('severity_hint', 'info')),
        'value': raw.get('value'),
        'source': _norm(raw.get('source', 'unknown')),
        'topology_neighbors': [_norm(x) for x in raw.get('topology_neighbors', [])],
        'provenance': raw.get('provenance', {}),
    }
