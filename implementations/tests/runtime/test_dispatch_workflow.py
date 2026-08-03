from __future__ import annotations

import base64
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from implementations.server.runtime.canonical import digest_bytes
from implementations.server.runtime.dispatch_types import (
    live_dispatch_type_values,
    resolve_dispatch_capability,
)
from implementations.server.runtime.dispatch_workflow import (
    BINDING_MARKER,
    compile_bound_launch_plan,
)
from implementations.server.runtime.errors import GateBlockedError, ValidationError


REPO = Path(__file__).resolve().parents[3]


class DispatchWorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.project = Path(self.temp.name)
        registry_relative = "implementations/contracts/dispatch-type-registry.v1.json"
        registry = json.loads((REPO / registry_relative).read_text(encoding="utf-8"))
        paths = [registry_relative, ".claude/skills/register-dispatch/append-dispatch.cjs"]
        paths.extend(
            entry["capability_path"]
            for entry in registry["types"]
            if entry["capability_path"] is not None
        )
        for relative in paths:
            destination = self.project / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / relative, destination)
        self.record = {
            "dispatch_id": "2026-08-03-workflow-review",
            "schema_version": "0.6.3",
            "dispatch_type": "review",
            "goal": "Review the dispatch workflow.",
            "context": "One bound reviewer checks the compiled workflow.",
            "max_loops": 1,
            "final_approver": "parent",
            "anti_bias_mode": "disabled",
            "output_mode": "inline",
            "groups": [
                {
                    "group_id": "reviewers",
                    "agents": [
                        {
                            "role": "auditor",
                            "model": "gpt-5.6",
                            "token_budget": 1000,
                            "initial_prompt": "Review the workflow without changing files.",
                        }
                    ],
                }
            ],
        }

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_registry_resolves_one_canonical_type(self) -> None:
        route = resolve_dispatch_capability(
            self.project,
            capability_ref="review",
            authority_mode="legacy-managed",
        )
        self.assertEqual(route["dispatch_type_ref"], "review")
        self.assertEqual(route["ledger_dispatch_type"], "review")
        self.assertIn("review", live_dispatch_type_values(self.project))
        with self.assertRaises(ValidationError):
            resolve_dispatch_capability(
                self.project,
                capability_ref="others",
                authority_mode="legacy-managed",
            )

    def test_compile_produces_exact_bound_prompt_and_manifest(self) -> None:
        compiled = compile_bound_launch_plan(
            repo_root=self.project,
            record=self.record,
            capability_ref="review",
            output_dir=Path(".codex/workflow-inputs/workflow-review"),
        )
        self.assertEqual(len(compiled["launches"]), 1)
        launch = compiled["launches"][0]
        message = launch["spawn_arguments"]["message"]
        first, prompt = message.split("\n", 1)
        self.assertTrue(first.startswith(BINDING_MARKER))
        encoded = first[len(BINDING_MARKER) :]
        envelope = json.loads(
            base64.urlsafe_b64decode(encoded + "=" * (-len(encoded) % 4))
        )
        self.assertEqual(envelope["dispatch_id"], self.record["dispatch_id"])
        self.assertEqual(envelope["group_id"], "reviewers")
        self.assertEqual(prompt, self.record["groups"][0]["agents"][0]["initial_prompt"])
        manifest_path = self.project / envelope["workflow_manifest_path"]
        self.assertEqual(
            envelope["workflow_manifest_digest"],
            digest_bytes(manifest_path.read_bytes()),
        )
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["target"]["seat_index"], 0)
        self.assertEqual(manifest["slots"], [])

    def test_compile_rejects_capability_type_mismatch(self) -> None:
        mismatched = {
            key: value
            for key, value in {**self.record, "dispatch_type": "others"}.items()
            if key != "output_mode"
        }
        with self.assertRaisesRegex(ValidationError, "type differs"):
            compile_bound_launch_plan(
                repo_root=self.project,
                record=mismatched,
                capability_ref="review",
                output_dir=Path("workflow"),
            )

    def test_compile_rejects_invalid_opening_before_writing(self) -> None:
        invalid_records = [
            {key: value for key, value in self.record.items() if key != "anti_bias_mode"},
            {
                **self.record,
                "anti_bias_mode": "disabled",
                "groups": [
                    {
                        **self.record["groups"][0],
                        "anti_bias": "forbidden axis",
                    }
                ],
            },
            {
                **self.record,
                "anti_bias_mode": "enabled",
                "groups": [
                    {
                        **self.record["groups"][0],
                        "agents": [
                            self.record["groups"][0]["agents"][0],
                            {
                                **self.record["groups"][0]["agents"][0],
                                "agent_name": "second-reviewer",
                            },
                        ],
                    }
                ],
            },
        ]
        for index, record in enumerate(invalid_records):
            output = Path(f"workflow-invalid-{index}")
            with self.subTest(index=index), self.assertRaises(ValidationError):
                compile_bound_launch_plan(
                    repo_root=self.project,
                    record=record,
                    capability_ref="review",
                    output_dir=output,
                )
            self.assertFalse((self.project / output).exists())

    def test_runtime_managed_route_is_not_advertised(self) -> None:
        with self.assertRaises(GateBlockedError):
            resolve_dispatch_capability(
                self.project,
                capability_ref="review",
                authority_mode="runtime-managed",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
