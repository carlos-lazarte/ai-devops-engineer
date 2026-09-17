from __future__ import annotations

from typing import Dict, List
from math import exp


def _pair_score(a: Dict, b: Dict, window_seconds: float) -> float:
    if a['tenant_id'] != b['tenant_id'] or a['environment'] != b['environment']:
        return 0.0
    dt = abs(a['timestamp'] - b['timestamp'])
    if dt > window_seconds:
        return 0.0
    score = 0.0
    score += 0.35 * max(0.0, 1.0 - dt / window_seconds)
    if a['component'] == b['component']:
        score += 0.30
    elif b['component'] in a.get('topology_neighbors', []) or a['component'] in b.get('topology_neighbors', []):
        score += 0.20
    if a['metric_family'] == b['metric_family']:
        score += 0.15
    if a['condition'] == b['condition']:
        score += 0.10
    return min(1.0, score)


def correlate(events: List[Dict], window_seconds: float = 300.0, threshold: float = 0.55) -> List[Dict]:
    ordered = sorted(events, key=lambda e: e['timestamp'])
    groups: List[List[Dict]] = []
    for e in ordered:
        best = None
        best_score = 0.0
        for idx, group in enumerate(groups):
            score = max(_pair_score(e, prior, window_seconds) for prior in group)
            if score > best_score:
                best_score, best = score, idx
        if best is not None and best_score >= threshold:
            groups[best].append(e)
        else:
            groups.append([e])

    output = []
    for idx, group in enumerate(groups, start=1):
        pair_scores = [_pair_score(group[i], group[j], window_seconds)
                       for i in range(len(group)) for j in range(i + 1, len(group))]
        confidence = max(pair_scores, default=0.0)
        output.append({
            'correlation_id': f'corr-{idx:04d}',
            'events': group,
            'event_ids': [e['event_id'] for e in group],
            'confidence': round(confidence, 4),
            'tenant_id': group[0]['tenant_id'],
            'environment': group[0]['environment'],
        })
    return output
