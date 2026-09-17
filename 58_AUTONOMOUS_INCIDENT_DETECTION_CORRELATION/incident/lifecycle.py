from __future__ import annotations

_ALLOWED = {
    'NEW': {'CORRELATING', 'SUPPRESSED'},
    'CORRELATING': {'CANDIDATE', 'SUPPRESSED', 'MERGED'},
    'CANDIDATE': {'TRIAGED', 'SUPPRESSED', 'MERGED'},
    'TRIAGED': {'INVESTIGATING', 'CLOSED'},
    'INVESTIGATING': {'CLOSED'},
    'SUPPRESSED': set(),
    'MERGED': set(),
    'CLOSED': set(),
}


def transition(state: str, target: str) -> str:
    if target not in _ALLOWED.get(state, set()):
        raise ValueError(f'invalid transition: {state} -> {target}')
    return target
