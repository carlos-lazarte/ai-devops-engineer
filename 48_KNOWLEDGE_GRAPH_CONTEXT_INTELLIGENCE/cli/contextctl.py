from __future__ import annotations
import argparse,json
from pathlib import Path
import sys
BASE=Path(__file__).resolve().parents[1]
ROOT=BASE.parent
sys.path.insert(0,str(BASE))
from graph.build_graph import build
from context.context_planner import plan

def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='cmd',required=True)
    bp=sub.add_parser('build-graph'); bp.add_argument('--root',default='.'); bp.add_argument('--output',default='.knowledge-graph/graph.json')
    pp=sub.add_parser('plan'); pp.add_argument('--root',default='.'); pp.add_argument('--query',required=True); pp.add_argument('--max-items',type=int,default=16); pp.add_argument('--max-hops',type=int,default=2)
    a=ap.parse_args()
    if a.cmd=='build-graph':
        data=build(Path(a.root).resolve()); out=Path(a.root).resolve()/a.output; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8'); print(json.dumps({'nodes':len(data['nodes']),'edges':len(data['edges']),'output':str(out)},indent=2))
    else:
        root=Path(a.root).resolve(); graph_path=root/'.knowledge-graph/graph.json'
        if not graph_path.exists():
            data=build(root); graph_path.parent.mkdir(parents=True,exist_ok=True); graph_path.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8')
        else: data=json.loads(graph_path.read_text(encoding='utf-8'))
        print(json.dumps(plan(a.query,data,a.max_items,a.max_hops),indent=2,ensure_ascii=False))
if __name__=='__main__': main()
