#!/usr/bin/env python3
"""Repository launcher for the shared host input-lineage hook."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from implementations.server.runtime.host_ingestion_hook import main


if __name__ == "__main__":
    main()
