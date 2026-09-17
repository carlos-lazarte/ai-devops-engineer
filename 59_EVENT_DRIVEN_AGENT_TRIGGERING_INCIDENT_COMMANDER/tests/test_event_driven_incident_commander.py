import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from trigger.engine import evaluate_trigger, build_trigger_request
from commander.session import open_session, transition
from commander.orchestrator import trigger_to_commander
from approval.gate import request_approval, apply_approval, is_usable
from handoff.planner import build_handoff


def incident(severity="warning", confidence=0.8, tenant="t1", env="prod"):
    return {"incident_id":"inc-1","tenant_id":tenant,"environment":env,"state":"CANDIDATE","severity":severity,"confidence":confidence,"signals":["e1","e2"],"candidate_reason":"correlated signals"}

def test_trigger_allows_analysis_for_normal_candidate():
    r = evaluate_trigger(incident())
    assert r["policy_decision"] == "ALLOW_ANALYSIS"
    assert r["approval_required"] is False

def test_critical_requires_human_gate():
    r = build_trigger_request(incident("critical", 0.9))
    assert r["policy_decision"] == "REQUIRE_HUMAN"
    assert r["approval_required"] is True

def test_low_confidence_is_denied():
    assert evaluate_trigger(incident("high", 0.4))["policy_decision"] == "DENY"

def test_orchestrator_opens_human_gated_session():
    out = trigger_to_commander(incident("critical", 0.9))
    assert out["session"]["state"] == "AWAITING_HUMAN"
    assert out["handoff"] is None
    assert out["session"]["production_execution_enabled"] is False

def test_approval_is_scoped():
    s = open_session(incident(), build_trigger_request(incident()))
    req = request_approval(s, "restart_service", {"tenant_id":"t1","environment":"prod"})
    approved = apply_approval(req, "human-1", "APPROVED", "bounded remediation")
    assert is_usable(approved, "t1", "prod") is True
    assert is_usable(approved, "t2", "prod") is False

def test_planner_handoff_is_plan_only():
    s = open_session(incident(), build_trigger_request(incident()))
    h = build_handoff(s)
    assert h["execution_mode"] == "PLAN_ONLY"
    assert h["policy_context"]["production_execution_enabled"] is False

def test_invalid_state_transition_rejected():
    try:
        transition("OPENED", "PLANNING")
    except ValueError:
        pass
    else:
        raise AssertionError("invalid transition accepted")
