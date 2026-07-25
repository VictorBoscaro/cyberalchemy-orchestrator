from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from server.control_center.sources import DispatchSource


class DispatchSourceTest(unittest.TestCase):
    def test_lineage_uses_only_explicit_parent_id(self):
        with tempfile.TemporaryDirectory() as folder:
            repo = Path(folder)
            ledger = repo / "telemetry" / "agents" / "subagents-dispatch.yaml"
            ledger.parent.mkdir(parents=True)
            rows = [
                {
                    "dispatch_id": "root",
                    "schema_version": "0.6.1",
                    "created": "2026-07-25T10:00:00Z",
                    "dispatch_type": "research",
                    "goal": "root",
                    "groups": [],
                },
                {
                    "dispatch_id": "child",
                    "schema_version": "0.6.1",
                    "created": "2026-07-25T10:01:00Z",
                    "dispatch_type": "review",
                    "goal": "child",
                    "parent_dispatch_id": "root",
                    "groups": [],
                },
                {
                    "dispatch_id": "looks-like-child-of-root",
                    "schema_version": "0.6.1",
                    "created": "2026-07-25T10:02:00Z",
                    "dispatch_type": "review",
                    "goal": "name similarity is not parentage",
                    "groups": [],
                },
            ]
            text = "dispatches:\n"
            for row in rows:
                first = True
                for key, value in row.items():
                    prefix = "  - " if first else "    "
                    text += f"{prefix}{key}: {json.dumps(value)}\n"
                    first = False
            ledger.write_text(text, encoding="utf-8")
            snapshot = DispatchSource([repo]).read()
            self.assertEqual(len(snapshot.edges), 1)
            self.assertEqual(
                (snapshot.edges[0]["source"], snapshot.edges[0]["target"]),
                (f"{repo.name}:root", f"{repo.name}:child"),
            )


if __name__ == "__main__":
    unittest.main()
