from __future__ import annotations
from typing import Dict
from trigger.engine import build_trigger_request
from commander.session import open_session, transition
from handoff.planner import build_handoff

def trigger_to_commander(incident: Dict) -> Dict:
    trigger = build_trigger_request(incident)
    if trigger["policy_decision"] == "DENY":
        return {"trigger": trigger, "session": None, "handoff": None}
    session = open_session(incident, trigger)
    session["state"] = transition(session["state"], "TRIAGE")
    session["state"] = transition(session["state"], "INVESTIGATING")
    if trigger["approval_required"]:
        session["state"] = transition(session["state"], "AWAITING_HUMAN")
        handoff = None
    else:
        session["state"] = transition(session["state"], "PLANNING")
        handoff = build_handoff(session)
        session["planner_handoff_id"] = handoff["handoff_id"]
    return {"trigger": trigger, "session": session, "handoff": handoff}
