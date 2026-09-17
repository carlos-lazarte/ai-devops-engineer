from __future__ import annotations
from typing import Dict

def build_handoff(session: Dict, objective: str = "investigate incident candidate") -> Dict:
    return {
        "handoff_id": f"handoff-{session['session_id']}",
        "incident_id": session["incident_id"],
        "objective": objective,
        "constraints": ["read-only evidence first", "preserve provenance", "do not execute production mutation"],
        "skill": "incident-triage",
        "policy_context": {"policy_decision": session["policy_decision"], "production_execution_enabled": False},
        "execution_mode": "PLAN_ONLY",
    }
