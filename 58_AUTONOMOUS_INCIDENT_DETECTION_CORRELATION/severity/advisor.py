from __future__ import annotations

from typing import Dict, List

_ORDER = {'info': 0, 'warning': 1, 'high': 2, 'critical': 3}

def advise(events: List[Dict], confidence: float) -> str:
    hints = [e.get('severity_hint', 'info') for e in events]
    highest = max(hints, key=lambda x: _ORDER.get(x, 0), default='info')
    if highest == 'critical' and confidence >= 0.60:
        return 'critical'
    if highest in {'critical', 'high'} and confidence >= 0.55:
        return 'high'
    if highest == 'warning' or confidence >= 0.70:
        return 'medium'
    return 'low'
