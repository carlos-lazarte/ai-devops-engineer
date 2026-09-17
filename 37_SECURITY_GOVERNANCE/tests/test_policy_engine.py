from pathlib import Path

from policy_engine.policy_engine import PolicyEngine

POLICY = Path(__file__).parents[1] / "policies" / "policy.yaml"


def engine():
    return PolicyEngine(POLICY)


def test_viewer_can_read():
    d = engine().authorize({"request_id": "1", "role": "viewer", "tool": "read_note", "operation": "read_note"})
    assert d.decision == "allow"
    assert d.risk == "low"


def test_viewer_cannot_propose_change():
    d = engine().authorize({"request_id": "2", "role": "viewer", "tool": "propose_change", "operation": "propose_change"})
    assert d.decision == "deny"


def test_operator_needs_approval():
    d = engine().authorize({"request_id": "3", "role": "operator", "tool": "propose_change", "operation": "propose_change"})
    assert d.decision == "deny"
    assert d.approval_required is True


def test_operator_with_approval_is_allowed():
    d = engine().authorize({"request_id": "4", "role": "operator", "tool": "propose_change", "operation": "propose_change", "approval_id": "APR-4"})
    assert d.decision == "allow"


def test_execute_change_disabled():
    d = engine().authorize({"request_id": "5", "role": "operator", "tool": "execute_change", "operation": "execute_change", "approval_id": "APR-5"})
    assert d.decision == "deny"
