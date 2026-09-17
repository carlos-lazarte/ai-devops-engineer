from __future__ import annotations

from pathlib import Path
import sys, json, argparse

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from resolver.intelligence import load_skills, rank_candidates, policy_decision

def discover(query: str, environment: str|None=None, limit: int=8):
    skills=load_skills(ROOT)
    by={s.skill_id:s for s in skills}
    rows=[]
    for row in rank_candidates(query,skills,environment)[:limit]:
        decision,reason=policy_decision(by[row['skill_id']],environment)
        row['policy_decision']=decision
        row['policy_reason']=reason
        rows.append(row)
    return rows

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--query',required=True); ap.add_argument('--environment'); ap.add_argument('--limit',type=int,default=8)
    args=ap.parse_args(); print(json.dumps({'query':args.query,'environment':args.environment,'candidates':discover(args.query,args.environment,args.limit)},indent=2))
