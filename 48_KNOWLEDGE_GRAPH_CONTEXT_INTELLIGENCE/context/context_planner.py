from __future__ import annotations
import json,re,sys
from collections import defaultdict, deque
from pathlib import Path

TOKEN_RE=re.compile(r"[a-z0-9][a-z0-9._/-]*",re.I)

def load_graph(path: Path): return json.loads(path.read_text(encoding='utf-8'))

def tokens(s): return set(TOKEN_RE.findall(s.lower()))

def build_indexes(graph):
    nodes={n['node_id']:n for n in graph['nodes']}
    by_title={n['title'].lower():n['node_id'] for n in graph['nodes']}
    adj=defaultdict(set)
    for e in graph['edges']:
        adj[e['source']].add(e['target']); adj[e['target']].add(e['source'])
    return nodes,by_title,adj

def lexical_score(query,n):
    q=tokens(query); text=' '.join([n.get('title',''),str(n.get('type') or ''),str(n.get('domain') or ''),str(n.get('technology') or ''),' '.join(map(str,n.get('tags') or []))])
    nt=tokens(text)
    if not q or not nt: return 0.0
    return len(q&nt)/len(q)

def graph_distance(seeds,adj,max_hops=2):
    dist={sid:0 for sid in seeds}; q=deque(seeds)
    while q:
        cur=q.popleft(); d=dist[cur]
        if d>=max_hops: continue
        for nxt in adj[cur]:
            if nxt not in dist:
                dist[nxt]=d+1; q.append(nxt)
    return dist

def classify(n):
    t=(n.get('type') or '').lower()
    if t in {'incident','evidence'}: return 'evidence'
    if t in {'runbook','procedure','checklist'}: return 'procedure'
    if t in {'workflow','architecture'}: return 'architecture'
    return 'knowledge'

def plan(query, graph, max_items=16, max_hops=2):
    nodes,_,adj=build_indexes(graph)
    direct=sorted(((lexical_score(query,n),nid) for nid,n in nodes.items()),reverse=True)
    seeds=[nid for score,nid in direct if score>0][:8]
    dist=graph_distance(seeds,adj,max_hops)
    rows=[]
    for nid,n in nodes.items():
        score=lexical_score(query,n)
        if nid in dist and dist[nid]>0:
            score=max(score,0.65/(dist[nid]+1))
            reason=f'graph_neighbor_h{dist[nid]}'
        elif score>0:
            reason='lexical_match'
        else:
            continue
        provenance={'path':n['path'],'node_id':nid,'retrieval':'knowledge_graph'}
        rows.append({'path':n['path'],'title':n['title'],'kind':classify(n),'relevance':round(score,4),'reason':reason,'provenance':provenance})
    rows.sort(key=lambda r:(r['relevance'],r['kind']=='evidence'),reverse=True)
    selected=[]; seen=set()
    for r in rows:
        if r['path'] not in seen:
            seen.add(r['path']); selected.append(r)
        if len(selected)>=max_items: break
    skills=[]
    try:
        sys.path.insert(0,str(Path('47_KNOWLEDGE_SKILL_MARKETPLACE_INTELLIGENCE').resolve()))
        from discovery.discover import discover
        skills=discover(query,None,4)
    except Exception:
        pass
    return {'version':'1.0','query':query,'items':selected,'skills':skills,'limits':{'max_items':max_items,'max_graph_hops':max_hops}}
