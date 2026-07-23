from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from agent_runtime.cli import main


class CliTest(unittest.TestCase):
    def test_init_command_show_and_replay(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "runtime.sqlite3"
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(main(["--database", str(database), "init"]), 0)
            self.assertTrue(json.loads(output.getvalue())["initialized"])

            payload = json.dumps(
                {
                    "session_id": "ses-cli",
                    "ensure_key": "cli:key",
                    "origin_kind": "cli",
                    "origin_ref": "opaque:cli",
                }
            )
            output = io.StringIO()
            with redirect_stdout(output):
                code = main(
                    [
                        "--database",
                        str(database),
                        "command",
                        "ensure_session",
                        "op-cli",
                        payload,
                    ]
                )
            self.assertEqual(code, 0)
            receipt = json.loads(output.getvalue())

            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(
                    main(
                        [
                            "--database",
                            str(database),
                            "verify-receipt",
                            receipt["receipt_id"],
                        ]
                    ),
                    0,
                )
            self.assertTrue(json.loads(output.getvalue())["verified"])

            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(
                    main(["--database", str(database), "show", "sessions"]), 0
                )
            self.assertEqual(json.loads(output.getvalue())[0]["session_id"], "ses-cli")

            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(main(["--database", str(database), "replay"]), 0)
            self.assertEqual(json.loads(output.getvalue())["sessions"], 1)

    def test_command_accepts_payload_from_stdin_for_powershell(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "runtime.sqlite3"
            payload = json.dumps(
                {
                    "session_id": "ses-stdin",
                    "ensure_key": "stdin:key",
                    "origin_kind": "cli",
                    "origin_ref": "opaque:stdin",
                }
            )
            output = io.StringIO()
            with patch("sys.stdin", io.StringIO(payload)), redirect_stdout(output):
                code = main(
                    [
                        "--database",
                        str(database),
                        "command",
                        "ensure_session",
                        "op-stdin",
                        "-",
                    ]
                )

            self.assertEqual(code, 0)
            self.assertEqual(
                json.loads(output.getvalue())["result"]["session_id"], "ses-stdin"
            )

    def test_show_accepts_observation_probe_projections(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "runtime.sqlite3"
            for table in ("observation_probe_runs", "probe_observations"):
                output = io.StringIO()
                with redirect_stdout(output):
                    code = main(["--database", str(database), "show", table])
                self.assertEqual(code, 0)
                self.assertEqual(json.loads(output.getvalue()), [])


if __name__ == "__main__":
    unittest.main()
