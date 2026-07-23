"""Test-only enabled provenance composition used by subprocess restart evidence."""

from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI

from implementations.server.runtime.api import create_provenance_router
from implementations.server.runtime.service import RuntimeService, RuntimeSettings


runtime = RuntimeService(
    RuntimeSettings(
        database_path=Path(os.environ["APT_TEST_DB"]),
        repo_root=Path(os.environ["APT_TEST_REPO"]),
        ledger_path=Path(os.environ["APT_TEST_LEDGER"]),
        repo_id=os.environ["APT_TEST_REPO_ID"],
    )
)
runtime.open()
app = FastAPI()
app.include_router(create_provenance_router(lambda: runtime, enabled=lambda: True))
