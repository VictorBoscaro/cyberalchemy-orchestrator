from __future__ import annotations

import base64
import hashlib
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
    ROOT_V080_APPENDER,
    ROOT_V080_RECORD_AUTHORITY,
    compile_bound_launch_plan,
    run as dispatch_workflow_run,
)
from implementations.server.runtime.errors import GateBlockedError, ValidationError


REPO = Path(__file__).resolve().parents[3]
WORKSPACE = REPO.parents[1]
ROOT_APPENDER = WORKSPACE / ROOT_V080_APPENDER


class DispatchWorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.project = Path(self.temp.name)
        registry_relative = "implementations/contracts/dispatch-type-registry.v2.json"
        registry = json.loads((REPO / registry_relative).read_text(encoding="utf-8"))
        paths = [
            registry_relative,
            "implementations/contracts/dispatch-ledger-row.v0.7.0.schema.json",
            "implementations/contracts/agent-role-registry.v1.json",
            "implementations/contracts/agent-role-registry-authority.v1.json",
            "implementations/contracts/agent-role-registry-selection.json",
            ".claude/skills/register-dispatch/append-dispatch.cjs",
        ]
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
            "schema_version": registry["ledger_schema_version"],
            "agent_role_registry_ref": registry["agent_role_registry_ref"],
            "dispatch_type": "review",
            "capability_route": resolve_dispatch_capability(
                self.project, capability_ref="review", authority_mode="legacy-managed"
            ),
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

    def _stage_root_v080_authority(
        self, *, closed: bool = False
    ) -> tuple[Path, dict[str, object], Path]:
        governance_root = self.project / "governance-root"
        appender = governance_root / ROOT_V080_APPENDER
        appender.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT_APPENDER, appender)
        pool = governance_root / "telemetry/agents/agent-pool.yaml"
        pool.parent.mkdir(parents=True, exist_ok=True)
        pool.write_text(
            'schema_version: "0.7"\nversion: "fixture"\nlast_updated: "2026-09-01"\n'
            'sources: []\nnotes: "fixture"\n---\nscientists:\n'
            '  - agent_name: "Fixture, Reviewer"\n    field: testing\n'
            '    subfield: workflow\n    historical_period: present\n'
            '    geographical_focus: global\n    role_fit: [auditor]\n'
            '    tags: [testing]\n    prompt_style: fixture\n',
            encoding="utf-8",
        )
        record: dict[str, object] = {
            "dispatch_id": "2026-08-10-root-v080-review",
            "schema_version": "0.8.0",
            "dispatch_type": "review",
            "goal": "Compile one root-authoritative review seat.",
            "context": "The root registry has already accepted this review.",
            "max_loops": 1,
            "final_approver": "parent",
            "working_folder": "reviews/root-v080/",
            "groups": [
                {
                    "group_id": "reviewers",
                    "agents": [
                        {
                            "agent_name": None,
                            "role": "skeptic",
                            "model": "gpt-5.6",
                            "token_budget": 1000,
                            "initial_prompt": "Review without changing files.",
                        }
                    ],
                }
            ],
        }
        sheet = governance_root / "dispatch-sheets/root-v080-review.json"
        sheet.parent.mkdir(parents=True, exist_ok=True)
        sheet_value = dict(record)
        sheet_body = json.dumps(sheet_value, indent=2) + "\n"
        sheet.write_text(sheet_body, encoding="utf-8")
        sheet_digest = hashlib.sha256(sheet_body.encode("utf-8")).hexdigest()
        record["evidence_binding"] = {
            "sheet_path": "dispatch-sheets/root-v080-review.json",
            "sheet_sha256": sheet_digest,
            "tension_verdicts": [
                {
                    "handle": "root-v080:tension:one",
                    "verdict": "pass",
                    "sheet_sha256": sheet_digest,
                },
                {
                    "handle": "root-v080:tension:two",
                    "verdict": "pass",
                    "sheet_sha256": sheet_digest,
                },
            ],
            "confirmation": {
                "handle": "root-v080:confirmation",
                "confirmed": True,
                "sheet_sha256": sheet_digest,
            },
        }
        row = {
            "dispatch_id": record["dispatch_id"],
            "schema_version": record["schema_version"],
            "created": "2026-08-10T00:00:00.000Z",
            "invoked_by": None,
            **{
                key: value
                for key, value in record.items()
                if key not in {"dispatch_id", "schema_version"}
            },
        }
        lines = ["dispatches:"]
        for index, (key, value) in enumerate(row.items()):
            prefix = "  - " if index == 0 else "    "
            lines.append(f"{prefix}{key}: {json.dumps(value, separators=(',', ':'))}")
        if closed:
            lines.extend(
                [
                    f"  - close_of: {json.dumps(record['dispatch_id'])}",
                    '    closed: "2026-08-10T00:01:00.000Z"',
                    '    invoked_by: null',
                    '    exit_reason: "error"',
                    '    agents_spawned: {"total":0,"tree":{"helpers":0},"loops_used":0}',
                ]
            )
        ledger = governance_root / "telemetry/agents/subagents-dispatch.yaml"
        ledger.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return governance_root, record, ledger

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

    def test_resolve_does_not_import_the_optional_http_host_hook(self) -> None:
        route = dispatch_workflow_run(
            [
                "--project-dir",
                str(self.project),
                "resolve",
                "--capability-ref",
                "review",
            ]
        )
        self.assertEqual(route["ledger_dispatch_type"], "review")

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
        with self.assertRaisesRegex(ValidationError, "dispatch_type must be"):
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

    def test_compile_accepts_explicit_root_v080_authority_without_mutation(self) -> None:
        governance_root, record, ledger = self._stage_root_v080_authority()
        before = ledger.read_bytes()
        compiled = compile_bound_launch_plan(
            repo_root=self.project,
            record=record,
            capability_ref="review",
            output_dir=Path("workflow-root-v080"),
            record_authority=ROOT_V080_RECORD_AUTHORITY,
            governance_root=governance_root,
        )
        self.assertEqual(compiled["record_authority"], ROOT_V080_RECORD_AUTHORITY)
        self.assertEqual(len(compiled["launches"]), 1)
        self.assertEqual(ledger.read_bytes(), before)

    def test_compile_rejects_root_v080_without_explicit_authority(self) -> None:
        _, record, _ = self._stage_root_v080_authority()
        with self.assertRaises(ValidationError):
            compile_bound_launch_plan(
                repo_root=self.project,
                record=record,
                capability_ref="review",
                output_dir=Path("workflow-root-v080-default"),
            )
        self.assertFalse((self.project / "workflow-root-v080-default").exists())

    def test_compile_rejects_stale_or_closed_root_v080_dispatch_before_writing(self) -> None:
        governance_root, record, _ = self._stage_root_v080_authority()
        sheet = governance_root / "dispatch-sheets/root-v080-review.json"
        sheet.write_text(sheet.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        with self.assertRaisesRegex(ValidationError, "sheet digest"):
            compile_bound_launch_plan(
                repo_root=self.project,
                record=record,
                capability_ref="review",
                output_dir=Path("workflow-root-v080-stale"),
                record_authority=ROOT_V080_RECORD_AUTHORITY,
                governance_root=governance_root,
            )
        self.assertFalse((self.project / "workflow-root-v080-stale").exists())

        governance_root, record, _ = self._stage_root_v080_authority(closed=True)
        with self.assertRaisesRegex(GateBlockedError, "is closed"):
            compile_bound_launch_plan(
                repo_root=self.project,
                record=record,
                capability_ref="review",
                output_dir=Path("workflow-root-v080-closed"),
                record_authority=ROOT_V080_RECORD_AUTHORITY,
                governance_root=governance_root,
            )
        self.assertFalse((self.project / "workflow-root-v080-closed").exists())

    def test_runtime_managed_route_is_not_advertised(self) -> None:
        with self.assertRaises(GateBlockedError):
            resolve_dispatch_capability(
                self.project,
                capability_ref="review",
                authority_mode="runtime-managed",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
