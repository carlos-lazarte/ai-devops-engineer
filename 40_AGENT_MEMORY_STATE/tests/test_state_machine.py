import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from memory.state_machine import StatefulTask


def test_valid_lifecycle():
    task = StatefulTask()
    task.transition("CONTEXT_BUILT", actor="agent", reason="context")
    task.transition("ANALYZING", actor="agent", reason="analysis")
    task.transition("PROPOSAL_READY", actor="agent", reason="proposal")
    task.transition("AWAITING_APPROVAL", actor="agent", reason="approval")
    task.transition("APPROVED", actor="human", reason="approved", approval_id="appr-2")
    task.transition("EXECUTED", actor="executor", reason="approved change", approval_id="appr-2")
    task.transition("VERIFIED", actor="verifier", reason="verification")
    task.transition("CLOSED", actor="agent", reason="closed")
    assert task.state == "CLOSED"
    assert len(task.history) == 8


def test_invalid_transition_rejected():
    task = StatefulTask()
    try:
        task.transition("EXECUTED", actor="agent", reason="invalid")
    except ValueError as exc:
        assert "invalid_transition" in str(exc)
    else:
        raise AssertionError("invalid transition must fail")
