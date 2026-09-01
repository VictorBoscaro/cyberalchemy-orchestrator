from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import unittest
from pathlib import Path
from typing import Any, Mapping

from implementations.server.runtime import continuation


REPO = Path(__file__).resolve().parents[3]
BRIDGE_FIXTURE = Path(__file__).with_name(
    "agent_continuation_lean_manifest_v1.json"
)
LEAN_ROOT_ENV = "DOMAINSPEC_LEAN_ROOT"
BRIDGE_SCHEMA = "aci.agent-continuation-lean-bridge@1"


class ContinuationLeanBridgeError(ValueError):
    """The frozen Lean bridge is malformed or differs from the Python reducer."""


def _canonical_manifest_bytes(rows: list[dict[str, object]]) -> bytes:
    return json.dumps(rows, separators=(",", ":"), sort_keys=True).encode("utf-8")


def _normalized_source_digest(path: Path) -> str:
    content = path.read_bytes().replace(b"\r\n", b"\n")
    return "sha256:" + hashlib.sha256(content).hexdigest()


def _transition_key(row: Mapping[str, object]) -> tuple[str | None, str, str]:
    if set(row) != {"source", "event", "target"}:
        raise ContinuationLeanBridgeError("transition row fields differ")
    source = row["source"]
    event = row["event"]
    target = row["target"]
    if source is not None and not isinstance(source, str):
        raise ContinuationLeanBridgeError("transition source is invalid")
    if not isinstance(event, str) or not isinstance(target, str):
        raise ContinuationLeanBridgeError("transition event or target is invalid")
    return source, event, target


def _runtime_transition_keys(
    transitions: Mapping[tuple[str | None, str], str],
) -> set[tuple[str | None, str, str]]:
    return {(source, event, target) for (source, event), target in transitions.items()}


def validate_bridge(
    envelope: Mapping[str, Any],
    runtime_transitions: Mapping[tuple[str | None, str], str],
) -> list[dict[str, object]]:
    if envelope.get("schema") != BRIDGE_SCHEMA:
        raise ContinuationLeanBridgeError("bridge schema differs")
    manifest = envelope.get("manifest")
    if not isinstance(manifest, dict):
        raise ContinuationLeanBridgeError("bridge manifest is absent")
    rows = manifest.get("transitions")
    if not isinstance(rows, list) or not all(isinstance(row, dict) for row in rows):
        raise ContinuationLeanBridgeError("bridge transitions are invalid")
    if manifest.get("row_count") != len(rows):
        raise ContinuationLeanBridgeError("bridge row count differs")
    digest = "sha256:" + hashlib.sha256(_canonical_manifest_bytes(rows)).hexdigest()
    if manifest.get("sha256") != digest:
        raise ContinuationLeanBridgeError("bridge manifest digest differs")

    lean_keys = [_transition_key(row) for row in rows]
    if len(set(lean_keys)) != len(lean_keys):
        raise ContinuationLeanBridgeError("bridge manifest has duplicate transitions")
    if set(lean_keys) != _runtime_transition_keys(runtime_transitions):
        raise ContinuationLeanBridgeError("runtime transition set differs from Lean")
    return rows


class AgentContinuationLeanBridgeTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.envelope = json.loads(BRIDGE_FIXTURE.read_text(encoding="utf-8"))

    def test_frozen_lean_manifest_is_integral_and_matches_runtime(self) -> None:
        rows = validate_bridge(self.envelope, continuation._TRANSITIONS)
        self.assertEqual(len(rows), 19)

    def test_manifest_tampering_is_rejected(self) -> None:
        tampered = copy.deepcopy(self.envelope)
        tampered["manifest"]["transitions"][0]["target"] = "expired"
        with self.assertRaisesRegex(
            ContinuationLeanBridgeError, "manifest digest differs"
        ):
            validate_bridge(tampered, continuation._TRANSITIONS)

    def test_runtime_transition_drift_is_rejected(self) -> None:
        drifted = dict(continuation._TRANSITIONS)
        drifted[("resumed", "continuation.suspended")] = "suspended"
        with self.assertRaisesRegex(
            ContinuationLeanBridgeError, "runtime transition set differs from Lean"
        ):
            validate_bridge(self.envelope, drifted)

    def test_local_lean_emitter_reproduces_frozen_manifest_when_available(self) -> None:
        explicit_root = os.environ.get(LEAN_ROOT_ENV)
        lean_root = (
            Path(explicit_root).resolve()
            if explicit_root
            else (REPO.parent / "domainspec-lean-formalization").resolve()
        )
        if not lean_root.is_dir():
            if explicit_root:
                self.fail(f"{LEAN_ROOT_ENV} does not name a directory: {lean_root}")
            self.skipTest("domainspec-lean-formalization sibling is unavailable")

        source = self.envelope["source"]
        self.assertEqual(source["source_state"], "uncommitted")
        revision = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=lean_root,
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        ).stdout.strip()
        self.assertEqual(revision, source["base_revision"])
        toolchain = (engineer_root := lean_root / "lean-engineer") / "lean-toolchain"
        self.assertEqual(
            toolchain.read_text(encoding="utf-8").strip(), source["lean_toolchain"]
        )
        for key in ("lifecycle_source", "emitter_source"):
            binding = source[key]
            path = lean_root / binding["path"]
            self.assertTrue(path.is_file(), path)
            self.assertEqual(_normalized_source_digest(path), binding["sha256"], path)

        executable_name = (
            "agent-continuation-manifest.exe"
            if os.name == "nt"
            else "agent-continuation-manifest"
        )
        executable = engineer_root / ".lake" / "build" / "bin" / executable_name
        if executable.is_file():
            command = [str(executable)]
        elif explicit_root:
            command = ["lake", "exe", "agent-continuation-manifest"]
        else:
            self.skipTest(
                "Lean sibling is present but the emitter is not built; set "
                f"{LEAN_ROOT_ENV} to require regeneration"
            )

        completed = subprocess.run(
            command,
            cwd=engineer_root,
            check=True,
            capture_output=True,
            text=True,
            timeout=180,
        )
        emitted = json.loads(completed.stdout)
        self.assertEqual(emitted, self.envelope["manifest"]["transitions"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
