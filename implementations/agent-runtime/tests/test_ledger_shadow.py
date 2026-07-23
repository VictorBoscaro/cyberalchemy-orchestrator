from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from agent_runtime import Runtime, ShadowLedgerReconciler


def _row(first_key: str, first_value: object, rest: dict[str, object] | None = None) -> str:
    lines = [f"  - {first_key}: {json.dumps(first_value, separators=(',', ':'))}"]
    for key, value in (rest or {}).items():
        lines.append(f"    {key}: {json.dumps(value, separators=(',', ':'))}")
    return "\n".join(lines)


class ShadowLedgerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.runtime = Runtime(self.root / "runtime.sqlite3")
        self.runtime.ensure_session(
            "op-session",
            session_id="ses-1",
            ensure_key="host:opaque",
            origin_kind="codex",
            origin_ref="conversation:opaque",
        )
        self.runtime.link_session_dispatch(
            "op-link",
            session_dispatch_link_id="link-1",
            session_id="ses-1",
            dispatch_id="dispatch-1",
        )
        self.reconciler = ShadowLedgerReconciler(self.runtime)

    def tearDown(self) -> None:
        self.runtime.close()
        self.temp.cleanup()

    def write(self, body: str) -> Path:
        path = self.root / "subagents-dispatch.yaml"
        path.write_text("dispatches:\n" + body + "\n", encoding="utf-8")
        return path

    @staticmethod
    def digest(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def test_classifies_all_states_and_never_mutates_ledger(self) -> None:
        candidate = self.runtime.shadow_runtime_refs("dispatch-1")
        cases = {
            "identical": _row(
                "dispatch_id", "dispatch-1", {"runtime_refs": candidate}
            ),
            "divergent": _row(
                "dispatch_id", "dispatch-1", {"runtime_refs": {"session_id": "wrong"}}
            ),
            "absent": _row("dispatch_id", "another"),
            "orphan_close": _row("close_of", "dispatch-1", {"outcome": "done"}),
            "malformed": "  - dispatch_id: not-json",
        }
        for expected, body in cases.items():
            with self.subTest(expected=expected):
                path = self.write(body)
                before = self.digest(path)
                result = self.reconciler.reconcile(path, "dispatch-1")
                after = self.digest(path)
                self.assertEqual(result["classification"], expected)
                self.assertEqual(after, before)

    def test_missing_file_is_absent_and_no_file_is_created(self) -> None:
        path = self.root / "missing.yaml"
        result = self.reconciler.reconcile(path, "dispatch-1")
        self.assertEqual(result["classification"], "absent")
        self.assertFalse(path.exists())


if __name__ == "__main__":
    unittest.main()
