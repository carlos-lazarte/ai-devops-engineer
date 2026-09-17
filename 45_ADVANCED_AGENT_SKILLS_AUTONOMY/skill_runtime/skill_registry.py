from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import yaml

@dataclass(frozen=True)
class SkillSpec:
    skill_id: str
    risk: str
    autonomy_level: str
    allowed_tools: tuple[str, ...]
    forbidden_actions: tuple[str, ...]
    required_evidence: tuple[str, ...]

class SkillRegistry:
    def __init__(self, root: Path):
        self.root = root
        self.skills: dict[str, SkillSpec] = {}

    def load(self) -> None:
        self.skills.clear()
        for path in sorted((self.root / "skills").glob("*.yaml")):
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            self.skills[data["skill_id"]] = SkillSpec(
                skill_id=data["skill_id"],
                risk=data["risk"],
                autonomy_level=data["autonomy_level"],
                allowed_tools=tuple(data["allowed_tools"]),
                forbidden_actions=tuple(data["forbidden_actions"]),
                required_evidence=tuple(data["required_evidence"]),
            )

    def get(self, skill_id: str) -> SkillSpec:
        return self.skills[skill_id]
