from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

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


if __name__ == "__main__":
    unittest.main()

