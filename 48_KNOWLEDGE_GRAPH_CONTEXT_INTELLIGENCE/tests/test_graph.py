from pathlib import Path
import sys, json
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'48_KNOWLEDGE_GRAPH_CONTEXT_INTELLIGENCE'))
from graph.build_graph import build

def test_graph_contains_markdown_nodes():
    data=build(ROOT)
    assert len(data['nodes']) > 100
    assert any(n['path']=='00_START_HERE/DevOps-Knowledge-Map.md' for n in data['nodes'])

def test_graph_edges_are_deterministic():
    a=build(ROOT); b=build(ROOT)
    assert a==b
