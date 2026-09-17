from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from memory_quality import run

def test_memory_quality(tmp_path):
    result = run(tmp_path/'memory.db')
    assert result['pass']
