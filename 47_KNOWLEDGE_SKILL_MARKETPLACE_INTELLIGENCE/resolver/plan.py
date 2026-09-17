from __future__ import annotations
from pathlib import Path
import sys, json, argparse
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from resolver.intelligence import load_skills, rank_candidates, resolve_dependencies, policy_decision

def build_plan(query: str, environment: str|None=None, max_selected: int=4):
    skills=load_skills(ROOT); by={s.skill_id:s for s in skills}
    ranked=rank_candidates(query,skills,environment)
    selected=[]
    for row in ranked:
        d,_=policy_decision(by[row['skill_id']],environment)
        if d=='eligible': selected.append(row['skill_id'])
        if len(selected)>=max_selected: break
    ordered=resolve_dependencies(by,selected)
    for sid in ordered:
        d,reason=policy_decision(by[sid],environment)
        if d!='eligible': raise RuntimeError(f'{sid}: {d}: {reason}')
    return {'version':'1.0','query':query,'environment':environment,'selected_skills':ordered,'steps':[{'step':i+1,'skill_id':sid,'mode':'plan_only'} for i,sid in enumerate(ordered)],'policy_checked':True,'requires_human_approval':any(by[sid].risk in {'high','critical'} for sid in ordered),'execution_mode':'plan_only'}

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--query',required=True); ap.add_argument('--environment'); args=ap.parse_args(); print(json.dumps(build_plan(args.query,args.environment),indent=2))
