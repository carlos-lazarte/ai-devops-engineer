import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent.parent))

from engine.executor import ClosedLoopExecutor


def test_verified_closes():
    result = ClosedLoopExecutor().run(
        task_id="LOOP-001",
        action_id="a1",
        tool_id="simulated-health-tool",
        approval_id="approval-1",
        environment="lab",
        verification_result="VERIFIED",
    )
    assert result["verification_status"] == "VERIFIED"
    assert result["state"] == "CLOSED"
    assert result["replanning_required"] is False


def test_failed_replans():
    result = ClosedLoopExecutor().run(
        task_id="LOOP-002",
        action_id="a2",
        tool_id="simulated-health-tool",
        approval_id="approval-2",
        environment="lab",
        verification_result="FAILED",
    )
    assert result["verification_status"] == "FAILED"
    assert result["state"] == "REPLANNING"
    assert result["replanning_required"] is True


def test_unknown_replans():
    result = ClosedLoopExecutor().run(
        task_id="LOOP-003",
        action_id="a3",
        tool_id="simulated-health-tool",
        approval_id="approval-3",
        environment="lab",
        verification_result="UNKNOWN",
    )
    assert result["verification_status"] == "UNKNOWN"
    assert result["state"] == "REPLANNING"


def test_approval_required():
    result = ClosedLoopExecutor().run(
        task_id="LOOP-004",
        action_id="a4",
        tool_id="simulated-health-tool",
        approval_id=None,
        environment="lab",
        verification_result="VERIFIED",
    )
    assert result["status"] == "rejected"
    assert result["reason"] == "explicit_approval_required"


def test_production_disabled():
    result = ClosedLoopExecutor().run(
        task_id="LOOP-005",
        action_id="a5",
        tool_id="simulated-health-tool",
        approval_id="approval-5",
        environment="prod",
        verification_result="VERIFIED",
        mode="approved_execution",
    )
    assert result["status"] == "rejected"
    assert result["reason"] == "production_execution_disabled"
