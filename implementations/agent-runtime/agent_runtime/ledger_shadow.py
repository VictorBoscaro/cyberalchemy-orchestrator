from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .runtime import Runtime


_ROW = re.compile(r"^(  - |    )([A-Za-z_][A-Za-z0-9_]*): (.+)$")


class ShadowLedgerReconciler:
    """Read/compare-only bridge to the append-only dispatch ledger.

    This class has no writer or appender dependency. It reads a complete
    snapshot, derives the E0 candidate from SQLite, and compares only the
    `runtime_refs` fragment. It never repairs or acknowledges ledger effects.
    """

    def __init__(self, runtime: Runtime):
        self.runtime = runtime

    @staticmethod
    def _read_rows(path: Path) -> tuple[list[dict[str, Any]], bool]:
        rows: list[dict[str, Any]] = []
        current: dict[str, Any] | None = None
        malformed = False
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            return [], True
        for line in text.splitlines():
            if not line or line.startswith("#") or line == "dispatches:":
                continue
            match = _ROW.match(line)
            if not match:
                malformed = True
                continue
            indent, key, encoded = match.groups()
            try:
                value = json.loads(encoded)
            except json.JSONDecodeError:
                malformed = True
                continue
            if indent == "  - ":
                if key not in ("dispatch_id", "close_of"):
                    malformed = True
                    current = None
                    continue
                current = {key: value}
                rows.append(current)
            elif current is None:
                malformed = True
            else:
                current[key] = value
        return rows, malformed

    def reconcile(self, ledger_path: str | Path, dispatch_id: str) -> dict[str, Any]:
        path = Path(ledger_path)
        candidate = self.runtime.shadow_runtime_refs(dispatch_id)
        if not path.exists():
            return {"classification": "absent", "dispatch_id": dispatch_id, "candidate": candidate}
        rows, malformed = self._read_rows(path)
        if malformed:
            return {
                "classification": "malformed",
                "dispatch_id": dispatch_id,
                "candidate": candidate,
            }
        opening = next((row for row in rows if row.get("dispatch_id") == dispatch_id), None)
        closing = next((row for row in rows if row.get("close_of") == dispatch_id), None)
        if opening is None and closing is not None:
            classification = "orphan_close"
        elif opening is None or candidate is None:
            classification = "absent"
        elif opening.get("runtime_refs") == candidate:
            classification = "identical"
        else:
            classification = "divergent"
        return {
            "classification": classification,
            "dispatch_id": dispatch_id,
            "candidate": candidate,
        }
