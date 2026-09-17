from pathlib import Path
import yaml, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from discovery.discover import discover

def test_golden_cases():
    cases=yaml.safe_load((ROOT/'evaluation/golden-discovery.yaml').read_text(encoding='utf-8'))
    for c in cases:
        rows=discover(c['query'],c['environment'],5)
        assert rows[0]['skill_id']==c['expected_top_skill']
