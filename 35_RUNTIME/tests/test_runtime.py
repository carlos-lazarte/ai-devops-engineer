from pathlib import Path

from app.core import VaultReader, assemble_context, build_prompt


def test_vault_search_returns_kubernetes_note():
    root = Path(__file__).resolve().parents[2]
    vault = VaultReader(root)
    hits = vault.search("kubernetes node notready", 5)
    assert hits
    assert any("kubernetes" in h.title.lower() or "k8s" in h.note_id.lower() for h in hits)


def test_context_packet_contains_evidence():
    root = Path(__file__).resolve().parents[2]
    vault = VaultReader(root)
    ctx = assemble_context(vault, "K8S-NOTREADY-001", 5)
    assert ctx["incident_id"] == "K8S-NOTREADY-001"
    assert ctx["evidence"]
    assert ctx["policy"]["human_approval_required"] is True


def test_prompt_contains_safety_rules():
    root = Path(__file__).resolve().parents[2]
    vault = VaultReader(root)
    ctx = assemble_context(vault, "K8S-NOTREADY-001", 5)
    prompt = build_prompt(ctx)
    assert "Do not claim a command was executed" in prompt
    assert "human approval" in prompt.lower()
