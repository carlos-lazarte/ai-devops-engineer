from enum import Enum


class LoopState(str, Enum):
    PLANNED = "PLANNED"
    AWAITING_APPROVAL = "AWAITING_APPROVAL"
    APPROVED = "APPROVED"
    EXECUTING = "EXECUTING"
    OBSERVING = "OBSERVING"
    VERIFIED = "VERIFIED"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"
    REPLANNING = "REPLANNING"
    CLOSED = "CLOSED"


_ALLOWED = {
    LoopState.PLANNED: {LoopState.AWAITING_APPROVAL},
    LoopState.AWAITING_APPROVAL: {LoopState.APPROVED},
    LoopState.APPROVED: {LoopState.EXECUTING},
    LoopState.EXECUTING: {LoopState.OBSERVING, LoopState.FAILED},
    LoopState.OBSERVING: {LoopState.VERIFIED, LoopState.FAILED, LoopState.UNKNOWN},
    LoopState.VERIFIED: {LoopState.CLOSED},
    LoopState.FAILED: {LoopState.REPLANNING},
    LoopState.UNKNOWN: {LoopState.REPLANNING},
    LoopState.REPLANNING: {LoopState.PLANNED, LoopState.CLOSED},
    LoopState.CLOSED: set(),
}


def transition(current: LoopState, target: LoopState) -> LoopState:
    if target not in _ALLOWED[current]:
        raise ValueError(f"invalid transition: {current.value} -> {target.value}")
    return target
