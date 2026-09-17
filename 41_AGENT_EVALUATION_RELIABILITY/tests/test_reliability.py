import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_fault_harness():
    p = subprocess.run([sys.executable, str(ROOT/'reliability/fault_harness.py')], capture_output=True, text=True, check=False)
    assert p.returncode == 0, p.stdout + p.stderr
    assert '"pass": true' in p.stdout.lower()
