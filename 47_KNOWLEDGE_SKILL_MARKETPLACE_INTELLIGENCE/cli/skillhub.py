#!/usr/bin/env python3
from pathlib import Path
import sys, argparse, json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from discovery.discover import discover
from resolver.plan import build_plan

ap=argparse.ArgumentParser(prog='skillhub'); sp=ap.add_subparsers(dest='cmd',required=True)
d=sp.add_parser('discover'); d.add_argument('--query',required=True); d.add_argument('--environment'); d.add_argument('--limit',type=int,default=8)
p=sp.add_parser('plan'); p.add_argument('--query',required=True); p.add_argument('--environment')
a=sp.add_parser('explain'); a.add_argument('--query',required=True); a.add_argument('--environment')
args=ap.parse_args()
if args.cmd=='discover': print(json.dumps(discover(args.query,args.environment,args.limit),indent=2))
elif args.cmd=='plan': print(json.dumps(build_plan(args.query,args.environment),indent=2))
else:
    rows=discover(args.query,args.environment,8)
    print(json.dumps({'query':args.query,'environment':args.environment,'explanation':rows},indent=2))
