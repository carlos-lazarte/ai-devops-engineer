from __future__ import annotations
from typing import Dict, List

_TRANSITIONS = {
    "OPENED": {"TRIAGE", "PAUSED"},
    "TRIAGE": {"INVESTIGATING", "AWAITING_HUMAN", "PAUSED"},
    "INVESTIGATING": {"AWAITING_HUMAN", "PLANNING", "PAUSED", "CLOSED"},
    "AWAITING_HUMAN": {"APPROVED", "REJECTED", "EXPIRED", "INVESTIGATING"},
    "APPROVED": {"PLANNING", "INVESTIGATING"},
    "REJECTED": {"INVESTIGATING", "CLOSED"},
    "EXPIRED": {"INVESTIGATING", "CLOSED"},
    "PLANNING": {"VERIFIED", "CLOSED", "PAUSED"},
    "VERIFIED": {"CLOSED"},
    "PAUSED": {"TRIAGE", "INVESTIGATING", "CLOSED"},
    "CLOSED": set(),
}

def transition(state: str, target: str) -> str:
    if target not in _TRANSITIONS.get(state, set()):
        raise ValueError(f"invalid transition: {state} -> {target}")
    return target

def open_session(incident: Dict, trigger: Dict, session_id: str = "session-0001") -> Dict:
    return {
        "session_id": session_id,
        "incident_id": incident["incident_id"],
        "state": "OPENED",
        "tenant_id": incident["tenant_id"],
        "environment": incident["environment"],
        "evidence": [{"event_id": e, "type": "source-signal"} for e in incident.get("signals", [])],
        "hypotheses": [{"id": "h1", "statement": incident.get("candidate_reason", "correlated operational signals"), "confidence": incident.get("confidence", 0.0)}],
        "unknowns": ["root_cause_not_yet_confirmed"],
        "requested_actions": [{"action": "collect_read_only_evidence", "scope": {"tenant_id": incident["tenant_id"], "environment": incident["environment"]}, "gated": False}],
        "approval_ids": [],
        "planner_handoff_id": None,
        "trigger_id": trigger["trigger_id"],
        "policy_decision": trigger["policy_decision"],
        "production_execution_enabled": False,
    }

def add_hypothesis(session: Dict, statement: str, confidence: float) -> None:
    session["hypotheses"].append({"id": f"h{len(session['hypotheses'])+1}", "statement": statement, "confidence": max(0.0, min(1.0, confidence))})
