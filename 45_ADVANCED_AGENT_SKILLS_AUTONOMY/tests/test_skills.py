from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from skill_runtime.skill_registry import SkillRegistry
from skill_runtime.autonomy_policy import AutonomyPolicy
from skill_runtime.skill_executor import SkillExecutor, SkillTask
from evaluation.skill_quality import evaluate_skill


def test_all_skill_contracts_are_valid():
    errors = []
    for path in (ROOT / "skills").glob("*.yaml"):
        errors.extend([f"{path.name}:{e}" for e in evaluate_skill(path)])
    assert errors == []


def test_high_risk_needs_approval():
    registry = SkillRegistry(ROOT)
    registry.load()
    executor = SkillExecutor(registry, AutonomyPolicy())
    result = executor.run(SkillTask("t1", "kubernetes-troubleshooting", "tenant-a", "lab", ("task_context", "relevant_operational_evidence")))
    assert result["status"] == "needs_approval"


def test_approved_skill_is_simulation_only():
    registry = SkillRegistry(ROOT)
    registry.load()
    executor = SkillExecutor(registry, AutonomyPolicy())
    result = executor.run(SkillTask("t2", "kubernetes-troubleshooting", "tenant-a", "lab", ("task_context", "relevant_operational_evidence"), approved=True))
    assert result["status"] == "simulated"
    assert "mutation" in result["proposed_actions"][0].lower()


def test_missing_evidence_blocks():
    registry = SkillRegistry(ROOT)
    registry.load()
    executor = SkillExecutor(registry, AutonomyPolicy())
    result = executor.run(SkillTask("t3", "linux-performance-analysis", "tenant-a", "lab", ("task_context",)))
    assert result["status"] == "blocked"
