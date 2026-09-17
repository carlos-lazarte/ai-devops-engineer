from __future__ import annotations

from typing import Dict, Iterable, List


def related_components(events: Iterable[Dict]) -> List[str]:
    found = set()
    for e in events:
        found.add(e['component'])
        found.update(e.get('topology_neighbors', []))
    return sorted(x for x in found if x)
