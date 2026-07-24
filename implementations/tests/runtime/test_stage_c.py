from __future__ import annotations

import os
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from implementations.server.runtime.cli import run
from implementations.server.runtime.errors import GateBlockedError
from implementations.server.runtime.local_pilot import (
    DEFAULT_RUNTIME_DB,
    STRICT_LEDGER,
    preflight_local_pilot,
)

REPO = Path(__file__).resolve().parents[3]
LEDGER = REPO / STRICT_LEDGER


class StageCLocalPilotTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.database = Path(self.temp.name) / "dedicated-local-pilot.sqlite3"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def preflight(self, **overrides):
        values = {
            "repo_root": REPO,
            "database_path": self.database,
            "ledger_path": LEDGER,
            "host": "127.0.0.1",
            "opted_in": True,
        }
        values.update(overrides)
        return preflight_local_pilot(**values)

    def test_missing_local_pilot_flag_is_rejected_before_side_effects(self) -> None:
        with self.assertRaises(SystemExit):
            run(["serve"])
        self.assertFalse(self.database.exists())

    def test_missing_environment_opt_in_never_calls_uvicorn(self) -> None:
        with patch.dict(os.environ, {"ACI_REPO_ROOT": str(REPO)}, clear=True), patch(
            "uvicorn.run"
        ) as server:
            with self.assertRaisesRegex(GateBlockedError, "ACI_LOCAL_PILOT_ENABLED"):
                run(
                    [
                        "serve",
                        "--local-pilot",
                        "--database",
                        str(self.database),
                        "--ledger",
                        str(LEDGER),
                    ]
                )
        server.assert_not_called()
        self.assertFalse(self.database.exists())

    def test_stage_c_receipt_drift_fails_before_database(self) -> None:
        with patch(
            "implementations.server.runtime.local_pilot.STAGE_C_RECEIPT_SHA256",
            "0" * 64,
        ):
            with self.assertRaisesRegex(GateBlockedError, "Stage-C receipt digest"):
                self.preflight()
        self.assertFalse(self.database.exists())

    def test_shared_default_database_is_forbidden(self) -> None:
        with self.assertRaisesRegex(GateBlockedError, "shared/default"):
            self.preflight(database_path=REPO / DEFAULT_RUNTIME_DB)

    def test_non_loopback_host_is_forbidden_before_database(self) -> None:
        with self.assertRaisesRegex(GateBlockedError, "127.0.0.1"):
            self.preflight(host="0.0.0.0")
        self.assertFalse(self.database.exists())

    def test_failed_preflight_never_calls_uvicorn(self) -> None:
        env = {
            "ACI_REPO_ROOT": str(REPO),
            "ACI_LOCAL_PILOT_ENABLED": "1",
        }
        with patch.dict(os.environ, env, clear=False), patch(
            "uvicorn.run"
        ) as server:
            with self.assertRaisesRegex(GateBlockedError, "strict dispatch ledger"):
                run(
                    [
                        "serve",
                        "--local-pilot",
                        "--host",
                        "127.0.0.1",
                        "--database",
                        str(self.database),
                        "--ledger",
                        str(Path(self.temp.name) / "missing-ledger.yaml"),
                    ]
                )
        server.assert_not_called()
        self.assertFalse(self.database.exists())

    def test_successful_preflight_passes_exact_loopback_app_to_uvicorn(self) -> None:
        env = {
            "ACI_REPO_ROOT": str(REPO),
            "ACI_LOCAL_PILOT_ENABLED": "1",
        }
        with patch.dict(os.environ, env, clear=False), patch(
            "uvicorn.run"
        ) as server:
            result = run(
                [
                    "serve",
                    "--local-pilot",
                    "--host",
                    "127.0.0.1",
                    "--port",
                    "8877",
                    "--database",
                    str(self.database),
                    "--ledger",
                    str(LEDGER),
                ]
            )
        self.assertEqual(result["status"], "stopped")
        self.assertTrue(result["preflight"]["health"]["ready"])
        server.assert_called_once()
        _, kwargs = server.call_args
        self.assertEqual(kwargs["host"], "127.0.0.1")
        self.assertEqual(kwargs["port"], 8877)
        paths = set(server.call_args.args[0].openapi()["paths"])
        self.assertIn("/api/runtime/events", paths)
        self.assertIn("/api/provenance/research/{capture_id}", paths)
        self.assertIn("/api/health", paths)
        self.assertTrue(
            all(
                path == "/api/health"
                or path.startswith("/api/runtime/")
                or path.startswith("/api/provenance/")
                for path in paths
            )
        )

    def test_tampered_registered_profile_fails_closed_on_restart(self) -> None:
        self.preflight()
        conn = sqlite3.connect(self.database)
        try:
            conn.execute(
                """
                UPDATE protocol_profiles SET canonical_digest=?
                WHERE profile_id=(SELECT profile_id FROM protocol_profiles LIMIT 1)
                """,
                ("sha256:" + "0" * 64,),
            )
            conn.commit()
        finally:
            conn.close()
        with self.assertRaisesRegex(GateBlockedError, "registered profile set"):
            self.preflight()


if __name__ == "__main__":
    unittest.main(verbosity=2)
