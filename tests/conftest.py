"""Shared test fixtures."""

import sys
from pathlib import Path

# Ensure smathpy is importable
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
