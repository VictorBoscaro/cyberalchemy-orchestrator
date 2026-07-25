"""Repository-root launcher shared by Claude and Codex lifecycle hooks."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from implementations.server.runtime.host_dispatch_hook import main


if __name__ == "__main__":
    main()
