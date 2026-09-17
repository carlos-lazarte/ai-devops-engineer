from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4

ALLOWED = {
    "CREATED": {"CONTEXT_BUILT", "FAILED", "EXPIRED"},
    "CONTEXT_BUILT": {"ANALYZING", "FAILED", "EXPIRED"},
    "ANALYZING": {"PROPOSAL_READY", "FAILED", "EXPIRED"},
    "PROPOSAL_READY": {"AWAITING_APPROVAL", "REJECTED", "FAILED", "EXPIRED"},
    "AWAITING_APPROVAL": {"APPROVED", "REJECTED", "EXPIRED"},
    "APPROVED": {"EXECUTED", "FAILED"},
    "REJECTED": {"CLOSED"},
    "EXECUTED": {"VERIFIED", "FAILED"},
    "VERIFIED": {"CLOSED"},
    "CLOSED": set(),
    "FAILED": {"CLOSED"},
    "EXPIRED": set(),
}


@dataclass
class StateEvent:
    event_id: str
    task_id: str
    from_state: str
    to_state: str
    actor: str
    reason: str
    approval_id: str | None
    timestamp: str


@dataclass
class StatefulTask:
    task_id: str = field(default_factory=lambda: f"task-{uuid4().hex[:12]}")
    state: str = "CREATED"
    history: list[StateEvent] = field(default_factory=list)

    def transition(self, to_state: str, *, actor: str, reason: str, approval_id: str | None = None) -> StateEvent:
        if to_state not in ALLOWED.get(self.state, set()):
            raise ValueError(f"invalid_transition:{self.state}->{to_state}")
        if to_state == "EXECUTED" and not approval_id:
            raise ValueError("approval_required_for_execution")
        event = StateEvent(
            event_id=f"evt-{uuid4().hex[:12]}", task_id=self.task_id, from_state=self.state,
            to_state=to_state, actor=actor, reason=reason, approval_id=approval_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.history.append(event)
        self.state = to_state
        return event
