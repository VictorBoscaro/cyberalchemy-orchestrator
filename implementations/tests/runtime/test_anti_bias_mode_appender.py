from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from implementations.server.runtime.dispatch_types import load_dispatch_type_registry, resolve_dispatch_capability
from implementations.server.runtime.legacy import StrictLegacySnapshotResolver


REPO = Path(__file__).resolve().parents[3]
APPENDER = REPO / ".claude/skills/register-dispatch/append-dispatch.cjs"
REGISTRY = Path("implementations/contracts/dispatch-type-registry.v2.json")


class AntiBiasModeAppenderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        destination = self.root / REGISTRY
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REPO / REGISTRY, destination)
        registry = json.loads(destination.read_text(encoding="utf-8"))
        for relative in (
            "implementations/contracts/dispatch-ledger-row.v0.7.0.schema.json",
            "implementations/contracts/agent-role-registry.v1.json",
            "implementations/contracts/agent-role-registry-authority.v1.json",
            "implementations/contracts/agent-role-registry-selection.json",
        ):
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / relative, target)
        for entry in registry["types"]:
            capability_path = entry.get("capability_path")
            if capability_path is None:
                continue
            capability = self.root / capability_path
            capability.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / capability_path, capability)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _record(self, *, mode: str | None) -> dict:
        registry = load_dispatch_type_registry(self.root)
        record = {
            "dispatch_id": "2026-08-03-anti-bias-mode-test",
            "schema_version": registry["ledger_schema_version"],
            "agent_role_registry_ref": registry["agent_role_registry_ref"],
            "dispatch_type": "review",
            "capability_route": resolve_dispatch_capability(
                self.root,
                capability_ref="review",
                authority_mode="legacy-managed",
            ),
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
    def _enabled(record: dict) -> dict:
        group = record["groups"][0]
        group["anti_bias"] = "constructive vs adversarial"
        group["agents"][0]["angle"] = "constructive"
        group["agents"][1]["angle"] = "adversarial"
        group["anti_bias_pairs"] = [
            {
                "left_index": 0,
                "right_index": 1,
                "question": "Does the implementation satisfy the contract under attack?",
                "left_position": "constructive",
                "right_position": "adversarial",
                "evidence": "The prompts assign opposing review stances.",
            }
        ]
        return record

    def test_mode_is_required_in_v064(self) -> None:
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
        record["groups"][0]["anti_bias_pairs"] = []
        record["groups"][0]["agents"][0]["angle"] = "first side"
        result = self._append(record)
        self.assertEqual(result.returncode, 2)
        self.assertIn('anti_bias_global is forbidden', result.stderr)
        self.assertIn('.anti_bias is forbidden', result.stderr)
        self.assertIn('.anti_bias_pairs is forbidden', result.stderr)
        self.assertIn('.angle is forbidden', result.stderr)

    def test_enabled_requires_complete_pairwise_matrix(self) -> None:
        missing = self._append(self._record(mode="enabled"))
        self.assertEqual(missing.returncode, 2)
        self.assertIn('.anti_bias is required', missing.stderr)
        self.assertIn('.angle is required', missing.stderr)
        self.assertIn('.anti_bias_pairs must contain exactly 1 pair', missing.stderr)

        record = self._enabled(self._record(mode="enabled"))
        accepted = self._append(record)
        self.assertEqual(accepted.returncode, 0, accepted.stderr)

    def test_enabled_rejects_invalid_pairwise_evidence(self) -> None:
        duplicate_angles = self._enabled(self._record(mode="enabled"))
        duplicate_angles["groups"][0]["agents"][1]["angle"] = "constructive"
        result = self._append(duplicate_angles)
        self.assertEqual(result.returncode, 2)
        self.assertIn("angle values must be distinct", result.stderr)

        wrong_position = self._enabled(self._record(mode="enabled"))
        wrong_position["groups"][0]["anti_bias_pairs"][0]["left_position"] = "wrong"
        result = self._append(wrong_position)
        self.assertEqual(result.returncode, 2)
        self.assertIn("left_position must equal", result.stderr)

        empty_evidence = self._enabled(self._record(mode="enabled"))
        empty_evidence["groups"][0]["anti_bias_pairs"][0]["evidence"] = " "
        result = self._append(empty_evidence)
        self.assertEqual(result.returncode, 2)
        self.assertIn("evidence must be a non-empty string", result.stderr)

    def test_enabled_rejects_missing_duplicate_and_noncanonical_pairs(self) -> None:
        record = self._enabled(self._record(mode="enabled"))
        third = {
            "role": "explorer",
            "model": "test-model",
            "token_budget": 100,
            "initial_prompt": "Review from a third perspective.",
            "angle": "empirical",
        }
        record["groups"][0]["agents"].append(third)
        base_pair = record["groups"][0]["anti_bias_pairs"][0]
        record["groups"][0]["anti_bias_pairs"] = [base_pair, dict(base_pair), dict(base_pair)]
        result = self._append(record)
        self.assertEqual(result.returncode, 2)
        self.assertIn("duplicates pair", result.stderr)
        self.assertIn("missing pair", result.stderr)

        reversed_pair = self._enabled(self._record(mode="enabled"))
        pair = reversed_pair["groups"][0]["anti_bias_pairs"][0]
        pair["left_index"], pair["right_index"] = 1, 0
        result = self._append(reversed_pair)
        self.assertEqual(result.returncode, 2)
        self.assertIn("left_index < right_index", result.stderr)

    def test_reader_preserves_v061_v062_v063_and_accepts_v064(self) -> None:
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
        self.assertEqual(current.contract_version, "0.7.0")

        historical_062 = (
            REPO
            / "docs/features/agents-communication-infra/adrs/fixtures/"
            "golden-opening-v0.6.2-disabled.yaml"
        )
        old_062 = StrictLegacySnapshotResolver().resolve(
            historical_062, "2026-08-03-anti-bias-disabled-fixture"
        )
        self.assertEqual(old_062.contract_version, "0.6.2")

    def test_removed_receipt_is_rejected(self) -> None:
        record = self._enabled(self._record(mode="enabled"))
        record["entry_validation_receipt"] = {"checks": []}
        result = self._append(record)
        self.assertEqual(result.returncode, 2)
        self.assertIn('unknown key "entry_validation_receipt"', result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
