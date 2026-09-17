from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'48_KNOWLEDGE_GRAPH_CONTEXT_INTELLIGENCE'))
from graph.build_graph import build
from context.context_planner import plan

def test_k8s_context_contains_operational_material():
    data=plan('Kubernetes node not ready incident',build(ROOT),max_items=20,max_hops=2)
    paths=[x['path'] for x in data['items']]
    assert any('K8S-NOTREADY-001' in p for p in paths)
    assert 'kubernetes-troubleshooting' in {s['skill_id'] for s in data.get('skills',[])}

def test_context_packet_has_provenance():
    data=plan('Terraform drift review',build(ROOT),max_items=10)
    assert data['items']
    assert all('provenance' in item for item in data['items'])
