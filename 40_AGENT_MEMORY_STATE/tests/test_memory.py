import sys
from pathlib import Path
from tempfile import TemporaryDirectory

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1]))

from store.memory_store import MemoryStore
from memory.state_machine import StatefulTask


def test_memory_tenant_and_environment_isolation():
    with TemporaryDirectory() as d:
        store = MemoryStore(Path(d) / "memory.db")
        m = store.add(
            memory_class="episodic", tenant_id="t1", environment="lab",
            content="node notready", correlation_id="c1"
        )
        assert store.get(m.memory_id, tenant_id="t1", environment="lab") is not None
        assert store.get(m.memory_id, tenant_id="t2", environment="lab") is None
        assert store.search("node", tenant_id="t2", environment="lab") == []


def test_episodic_requires_review_for_promotion():
    with TemporaryDirectory() as d:
        store = MemoryStore(Path(d) / "memory.db")
        m = store.add(
            memory_class="episodic", tenant_id="t1", environment="lab",
            content="verified pattern", correlation_id="c1"
        )
        promoted = store.promote(m.memory_id, tenant_id="t1", environment="lab", reviewer="engineer")
        assert promoted.status == "verified"
        assert promoted.reviewed_by == "engineer"


def test_state_machine_requires_approval_for_execution():
    task = StatefulTask()
    task.transition("CONTEXT_BUILT", actor="agent", reason="context assembled")
    task.transition("ANALYZING", actor="agent", reason="analysis started")
    task.transition("PROPOSAL_READY", actor="agent", reason="proposal generated")
    task.transition("AWAITING_APPROVAL", actor="agent", reason="approval requested")
    task.transition("APPROVED", actor="human", reason="approved", approval_id="appr-1")
    try:
        task.transition("EXECUTED", actor="executor", reason="execution")
    except ValueError as exc:
        assert str(exc) == "approval_required_for_execution"
    else:
        raise AssertionError("execution must require approval_id")
