from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from implementations.server.runtime.canonical import canonical_digest
from implementations.server.runtime.legacy import StrictLegacySnapshotResolver


REPO = Path(__file__).resolve().parents[3]
APPENDER = REPO / ".claude/skills/register-dispatch/append-dispatch.cjs"
REGISTRY = Path("implementations/contracts/dispatch-type-registry.v1.json")


class AntiBiasModeAppenderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        destination = self.root / REGISTRY
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REPO / REGISTRY, destination)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _record(self, *, mode: str | None) -> dict:
        record = {
            "dispatch_id": "2026-08-03-anti-bias-mode-test",
            "schema_version": "0.6.2",
            "dispatch_type": "review",
            "goal": "Verify explicit anti-bias mode enforcement.",
            "context": "Two reviewers exercise the appender boundary.",
            "max_loops": 1,
            "final_approver": "parent",
            "output_mode": "inline",
            "invoked_by": "test@example.invalid",
            "project_dir": str(self.root),
            "groups": [
                {
                    "group_id": "reviewers",
                    "agents": [
                        {
                            "role": "auditor",
                            "model": "test-model",
                            "token_budget": 100,
                            "initial_prompt": "Review from the first perspective.",
                        },
                        {
                            "role": "skeptic",
                            "model": "test-model",
                            "token_budget": 100,
                            "initial_prompt": "Review from the second perspective.",
                        },
                    ],
                }
            ],
        }
        if mode is not None:
            record["anti_bias_mode"] = mode
        return record

    def _append(self, record: dict) -> subprocess.CompletedProcess[str]:
        record_path = self.root / "record.json"
        record_path.write_text(json.dumps(record), encoding="utf-8")
        return subprocess.run(
            ["node", str(APPENDER), str(record_path)],
            cwd=self.root,
            text=True,
            capture_output=True,
            check=False,
        )

    @staticmethod
    def _with_receipt(record: dict) -> dict:
        subject = {
            key: value
            for key, value in record.items()
            if key not in {"entry_validation_receipt", "project_dir"}
        }
        return {
            **record,
            "entry_validation_receipt": {
                "schema": "entry-validation-receipt/v1",
                "subject_digest": canonical_digest(subject),
                "checks": [
                    {"checker_id": "entry-check-a", "verdict": "PASS"},
                    {"checker_id": "entry-check-b", "verdict": "PASS"},
                ],
            },
        }

    def test_mode_is_required_in_v062(self) -> None:
        result = self._append(self._record(mode=None))
        self.assertEqual(result.returncode, 2)
        self.assertIn("anti_bias_mode is required", result.stderr)

    def test_invalid_mode_is_rejected(self) -> None:
        result = self._append(self._record(mode="automatic"))
        self.assertEqual(result.returncode, 2)
        self.assertIn("anti_bias_mode is required", result.stderr)

    def test_disabled_accepts_fanout_without_tension_fields(self) -> None:
        result = self._append(self._record(mode="disabled"))
        self.assertEqual(result.returncode, 0, result.stderr)
        ledger = self.root / "telemetry/agents/subagents-dispatch.yaml"
        self.assertIn('    anti_bias_mode: "disabled"', ledger.read_text(encoding="utf-8"))

    def test_disabled_rejects_tension_fields(self) -> None:
        record = self._record(mode="disabled")
        record["anti_bias_global"] = "global axis"
        record["groups"][0]["anti_bias"] = "group axis"
        record["groups"][0]["agents"][0]["angle"] = "first side"
        result = self._append(record)
        self.assertEqual(result.returncode, 2)
        self.assertIn('anti_bias_global is forbidden', result.stderr)
        self.assertIn('.anti_bias is forbidden', result.stderr)
        self.assertIn('.angle is forbidden', result.stderr)

    def test_disabled_rejects_entry_validation_receipt(self) -> None:
        record = self._record(mode="disabled")
        record["entry_validation_receipt"] = {
            "schema": "entry-validation-receipt/v1",
            "subject_digest": "sha256:" + "0" * 64,
            "checks": [],
        }
        result = self._append(record)
        self.assertEqual(result.returncode, 2)
        self.assertIn("entry_validation_receipt is forbidden", result.stderr)

    def test_enabled_preserves_fanout_requirements(self) -> None:
        missing = self._append(self._record(mode="enabled"))
        self.assertEqual(missing.returncode, 2)
        self.assertIn('.anti_bias is required', missing.stderr)
        self.assertIn('.angle is required', missing.stderr)

        record = self._record(mode="enabled")
        record["groups"][0]["anti_bias"] = "constructive vs adversarial"
        record["groups"][0]["agents"][0]["angle"] = "constructive"
        record["groups"][0]["agents"][1]["angle"] = "adversarial"
        record = self._with_receipt(record)
        accepted = self._append(record)
        self.assertEqual(accepted.returncode, 0, accepted.stderr)

    def test_enabled_requires_valid_entry_validation_receipt(self) -> None:
        record = self._record(mode="enabled")
        record["groups"][0]["anti_bias"] = "constructive vs adversarial"
        record["groups"][0]["agents"][0]["angle"] = "constructive"
        record["groups"][0]["agents"][1]["angle"] = "adversarial"

        missing = self._append(record)
        self.assertEqual(missing.returncode, 2)
        self.assertIn("entry_validation_receipt is required", missing.stderr)

        mismatched = self._with_receipt(record)
        mismatched["entry_validation_receipt"]["subject_digest"] = "sha256:" + "0" * 64
        result = self._append(mismatched)
        self.assertEqual(result.returncode, 2)
        self.assertIn("subject_digest does not match", result.stderr)

        duplicate = self._with_receipt(record)
        duplicate["entry_validation_receipt"]["checks"][1]["checker_id"] = "entry-check-a"
        result = self._append(duplicate)
        self.assertEqual(result.returncode, 2)
        self.assertIn("checker_id values must be distinct", result.stderr)

        failed = self._with_receipt(record)
        failed["entry_validation_receipt"]["checks"][1]["verdict"] = "FAIL"
        result = self._append(failed)
        self.assertEqual(result.returncode, 2)
        self.assertIn('verdict must be exactly "PASS"', result.stderr)

    def test_reader_preserves_v061_and_accepts_v062(self) -> None:
        historical = (
            REPO
            / "docs/features/agents-communication-infra/adrs/fixtures/"
            "golden-opening-v0.6.1.yaml"
        )
        old = StrictLegacySnapshotResolver().resolve(
            historical, "2026-07-23-local-probe-fixture"
        )
        self.assertEqual(old.contract_version, "0.6.1")

        result = self._append(self._record(mode="disabled"))
        self.assertEqual(result.returncode, 0, result.stderr)
        current = StrictLegacySnapshotResolver().resolve(
            self.root / "telemetry/agents/subagents-dispatch.yaml",
            "2026-08-03-anti-bias-mode-test",
        )
        self.assertEqual(current.contract_version, "0.6.2")


if __name__ == "__main__":
    unittest.main(verbosity=2)
