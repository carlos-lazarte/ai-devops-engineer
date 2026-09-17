from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from resolver.intelligence import load_skills, rank_candidates, resolve_dependencies, policy_decision, satisfies
from resolver.plan import build_plan

def test_discovery_top_skill():
    skills=load_skills(ROOT)
    ranked=rank_candidates('diagnose Kubernetes node not ready incident',skills,'lab')
    assert ranked[0]['skill_id']=='kubernetes-troubleshooting'

def test_environment_and_status_policy():
    skills={s.skill_id:s for s in load_skills(ROOT)}
    decision,_=policy_decision(skills['kubernetes-troubleshooting'],'lab')
    assert decision=='eligible'
    assert policy_decision(type('S',(),{'status':'draft','environments':['lab'],'autonomy_level':'L1'})(),'lab')[0]=='blocked'

def test_dependency_resolution_order_empty_graph():
    skills={s.skill_id:s for s in load_skills(ROOT)}
    assert resolve_dependencies(skills,['terraform-review'])==['terraform-review']

def test_version_constraints():
    assert satisfies('1.2.3','1.2.3')
    assert satisfies('1.4.0','1.x')
    assert satisfies('1.4.0','^1.2.0')
    assert not satisfies('2.0.0','^1.2.0')

def test_plan_is_plan_only_and_approval_aware():
    plan=build_plan('diagnose Kubernetes node not ready incident','lab',max_selected=1)
    assert plan['execution_mode']=='plan_only'
    assert plan['selected_skills']==['kubernetes-troubleshooting']
    assert plan['requires_human_approval'] is True
