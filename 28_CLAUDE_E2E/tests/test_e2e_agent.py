from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
CLIENT = ROOT / "28_CLAUDE_E2E" / "client"
sys.path.insert(0, str(CLIENT))

from e2e_agent import build_context, validate_response


def test_build_context_has_evidence_and_retrieval():
    packet = build_context("K8S-NOTREADY-001")
    assert packet["evidence"]
    assert packet["retrieved_notes"]
    assert packet["retrieved_runbooks"]


def test_response_validation_requires_human_approval():
    obj = {
        "summary": "x",
        "confidence": "medium",
        "facts": [],
        "observations": [],
        "hypotheses": [],
        "recommended_diagnostics": [],
        "proposed_actions": [{"action": "change", "requires_human_approval": False}],
        "unknowns": [],
        "references": [],
    }
    assert "action_0:human_approval_must_be_true" in validate_response(obj)
