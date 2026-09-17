import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ingestion.normalize import normalize
from dedup.deduplicator import deduplicate
from correlator.engine import correlate
from incident.builder import build_candidates
from incident.lifecycle import transition
from correlator.service import build_incident_candidates


def event(i, ts, tenant='t1', env='prod', component='api', family='latency', condition='high', severity='warning'):
    return {'event_id': i, 'timestamp': ts, 'tenant_id': tenant, 'environment': env,
            'component': component, 'metric_family': family, 'condition': condition,
            'severity_hint': severity, 'source': 'synthetic'}


def test_normalization():
    e = normalize(event('e1', 10, component='API WEB'))
    assert e['component'] == 'api-web'


def test_dedup_suppresses_duplicates():
    unique, suppressed = deduplicate([event('a', 10), event('b', 20), event('c', 25)])
    assert len(unique) == 1
    assert suppressed == ['b', 'c']


def test_correlates_same_scope_but_not_cross_tenant():
    same = [event('a', 10, component='api', family='latency', severity='warning'), event('b', 30, component='db', family='errors', severity='warning')]
    same[1]['topology_neighbors'] = ['api']
    groups = correlate(same)
    assert len(groups) == 1
    cross = [event('a', 10, tenant='t1'), event('b', 30, tenant='t2')]
    assert len(correlate(cross)) == 2


def test_candidate_and_review_boundary():
    events = [event('a', 10, severity='critical'), event('b', 30, component='db', family='errors', severity='critical')]
    events[1]['topology_neighbors'] = ['api']
    groups = correlate(events)
    c = build_candidates(groups)[0]
    assert c['state'] == 'CANDIDATE'
    assert c['severity'] == 'critical'
    assert c['human_review_required'] is True
    assert c['production_execution_enabled'] is False


def test_lifecycle_and_service():
    assert transition('NEW', 'CORRELATING') == 'CORRELATING'
    events = [event('a', 10), event('b', 30, component='db', family='errors')]
    events[1]['topology_neighbors'] = ['api']
    result = build_incident_candidates(events)
    assert len(result['candidates']) == 1
    assert result['candidates'][0]['signals'] == ['a', 'b']
