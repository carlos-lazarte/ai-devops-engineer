from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Dict, Iterable, List, Tuple

import yaml

TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9_.-]*", re.I)


def tokens(text: str) -> set[str]:
    return {t.lower() for t in TOKEN_RE.findall(text)}


def parse_version(v: str) -> Tuple[int, int, int]:
    m = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", v)
    if not m:
        raise ValueError(f"Invalid semantic version: {v}")
    return tuple(map(int, m.groups()))


def satisfies(version: str, constraint: str) -> bool:
    v = parse_version(version)
    if constraint == version:
        return True
    m = re.fullmatch(r"(\d+)\.x", constraint)
    if m:
        return v[0] == int(m.group(1))
    m = re.fullmatch(r"\^(\d+)\.(\d+)\.(\d+)", constraint)
    if m:
        base = tuple(map(int, m.groups()))
        return v[0] == base[0] and v >= base
    raise ValueError(f"Unsupported version constraint: {constraint}")


@dataclass
class Skill: 
    skill_id: str
    name: str
    version: str
    platform_api: str
    contract_version: str
    domain: str
    risk: str
    autonomy_level: str
    capabilities: list[str] = field(default_factory=list)
    required_tools: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    environments: list[str] = field(default_factory=list)
    dependencies: list[dict] = field(default_factory=list)
    status: str = "draft"


def load_skills(base: Path) -> list[Skill]:
    out=[]
    for p in sorted((base/'skills').glob('*/skill.yaml')):
        d=yaml.safe_load(p.read_text(encoding='utf-8')) or {}
        out.append(Skill(
            skill_id=d['skill_id'], name=d['name'], version=str(d['version']),
            platform_api=str(d['platform_api']), contract_version=str(d['contract_version']),
            domain=str(d.get('domain','')), risk=str(d.get('risk','')),
            autonomy_level=str(d.get('autonomy_level','L0')),
            capabilities=list(d.get('capabilities') or []), required_tools=list(d.get('required_tools') or []),
            keywords=list(d.get('keywords') or []), environments=list(d.get('environments') or []),
            dependencies=list(d.get('dependencies') or []), status=str(d.get('status','draft'))
        ))
    return out


def rank_candidates(query: str, skills: Iterable[Skill], environment: str | None = None) -> list[dict]:
    q=tokens(query)
    rows=[]
    for s in skills:
        corpus=tokens(' '.join([s.name,s.domain,*s.capabilities,*s.keywords]))
        overlap=q & corpus
        score=(len(overlap) / max(1,len(q))) * 0.75
        reasons=[f"term_overlap={sorted(overlap)}"] if overlap else []
        if environment and environment in s.environments:
            score += 0.20; reasons.append(f"environment={environment}")
        if s.status == 'published':
            score += 0.05; reasons.append('status=published')
        rows.append({'skill_id':s.skill_id,'version':s.version,'score':round(score,6),'status':s.status,'reasons':reasons,'overlap':sorted(overlap)})
    return sorted(rows,key=lambda x:(-x['score'],x['skill_id']))


def resolve_dependencies(skill_map: Dict[str, Skill], selected: Iterable[str]) -> list[str]:
    order=[]; visiting=set(); visited=set()
    def dfs(sid: str):
        if sid in visiting:
            raise ValueError(f"Dependency cycle detected at {sid}")
        if sid in visited:
            return
        if sid not in skill_map:
            raise KeyError(f"Missing skill dependency: {sid}")
        visiting.add(sid)
        for dep in skill_map[sid].dependencies:
            depid=dep['skill_id']; constraint=str(dep['version_constraint'])
            dep_skill=skill_map.get(depid)
            if not dep_skill: raise KeyError(f"Missing skill dependency: {depid}")
            if not satisfies(dep_skill.version,constraint):
                raise ValueError(f"Unsatisfied dependency {depid} {constraint}; found {dep_skill.version}")
            dfs(depid)
        visiting.remove(sid); visited.add(sid); order.append(sid)
    for sid in selected: dfs(sid)
    return order


def policy_decision(skill: Skill, environment: str | None = None) -> tuple[str,str]:
    if skill.status != 'published': return 'blocked','skill status is not published'
    if environment and skill.environments and environment not in skill.environments:
        return 'incompatible', f'environment {environment} not declared'
    if skill.autonomy_level == 'L4': return 'blocked','critical autonomy is disabled'
    return 'eligible','policy baseline allows discovery'
