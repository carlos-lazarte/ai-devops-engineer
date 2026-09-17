from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "30_AUTOMATION"))
from validate_vault import validate  # noqa: E402


def test_current_vault_is_valid():
    errors = validate(ROOT)
    assert errors == []
