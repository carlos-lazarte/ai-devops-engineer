from __future__ import annotations
import argparse, json, re
from pathlib import Path

WIKILINK_RE=re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")

def parse_frontmatter(text: str):
    if not text.startswith('---\n'): return {}
    parts=text.split('\n---\n',1)
    if len(parts)!=2: return {}
    raw=parts[0][4:]
    try:
        import yaml
        return yaml.safe_load(raw) or {}
    except Exception:
        return {}

def title_from(path, text):
    fm=parse_frontmatter(text)
    if fm.get('title'): return str(fm['title'])
    for line in text.splitlines():
        if line.startswith('# '): return line[2:].strip()
    return path.stem

def build(root: Path):
    nodes={}; title_to_ids={}
    for p in sorted([*root.rglob('*.md'), *root.glob('26_OPERATIONAL_AGENT_LAB/fixtures/**/*.txt'), *root.glob('26_OPERATIONAL_AGENT_LAB/fixtures/**/*.log')]):
        if any(part in {'.git','.venv','dist','.rag-index','.knowledge-graph'} for part in p.parts):
            continue
        text=p.read_text(encoding='utf-8',errors='ignore')
        rel=p.relative_to(root).as_posix(); fm=parse_frontmatter(text); title=title_from(p,text)
        node_id=rel
        if rel.endswith('.md'): node_id=rel[:-3]
        links=[x.strip() for x in WIKILINK_RE.findall(text) if x.strip()]
        node_type=fm.get('type')
        domain=fm.get('domain')
        if '26_OPERATIONAL_AGENT_LAB/fixtures/' in rel:
            node_type=node_type or 'evidence'; domain=domain or 'incident'
        n={'node_id':node_id,'path':rel,'title':title,'type':node_type,'domain':domain,'technology':fm.get('technology'),'tags':fm.get('tags') or [],'links':links}
        nodes[node_id]=n; title_to_ids.setdefault(title.lower(),[]).append(node_id); title_to_ids.setdefault(p.stem.lower(),[]).append(node_id)
    edges=[]
    for nid,n in nodes.items():
        for target in n['links']:
            candidates=title_to_ids.get(target.lower(),[])
            if candidates:
                target_id=candidates[0]
                edges.append({'source':nid,'target':target_id,'type':'wikilink'})
    return {'version':'1.0','nodes':list(nodes.values()),'edges':edges}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); ap.add_argument('--output',required=True)
    a=ap.parse_args(); data=build(Path(a.root).resolve()); out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8'); print(json.dumps({'nodes':len(data['nodes']),'edges':len(data['edges']),'output':str(out)},indent=2))
if __name__=='__main__': main()
