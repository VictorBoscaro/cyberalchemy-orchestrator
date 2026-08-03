from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from implementations.server.runtime.canonical import (
    canonical_digest,
    canonical_text,
    digest_bytes,
)
from implementations.server.runtime.errors import (
    AuthorizationError,
    ConflictError,
    IdempotencyConflict,
    IntegrityError,
)
from implementations.server.runtime.orchestration_bridge import (
    LocalOrchestrationLoggingBridge,
)
from implementations.server.runtime.service import RuntimeService, RuntimeSettings


REPO = Path(__file__).resolve().parents[3]
APPENDER = REPO / ".claude/skills/register-dispatch/append-dispatch.cjs"
EVIDENCE_REF = "codex-thread:host-workflow-test"
EVIDENCE_DIGEST = canonical_digest({"confirmation": "host-workflow-test"})


class HostWorkflowBindingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.project = Path(self.temp.name)
        dispatch_registry_relative = (
            "implementations/contracts/dispatch-type-registry.v1.json"
        )
        dispatch_registry = json.loads(
            (REPO / dispatch_registry_relative).read_text(encoding="utf-8")
        )
        dispatch_paths = [dispatch_registry_relative]
        dispatch_paths.extend(
            entry["capability_path"]
            for entry in dispatch_registry["types"]
            if entry["capability_path"] is not None
        )
        for relative in dispatch_paths:
            destination = self.project / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / relative, destination)
        registry_relative = (
            "docs/features/agents-communication-infra/reviews/"
            "2026-07-23-stage-a-freeze/profile-registry-manifest.json"
        )
        registry = json.loads(
            (REPO / registry_relative).read_text(encoding="utf-8")
        )
        profile_files = [registry_relative]
        profile_files.extend(
            profile["authoritative_profile_path"]
            for profile in registry["profiles"]
        )
        profile_files.extend(
            "docs/features/agents-communication-infra/"
            + profile["local_review_mirror"]["path"]
            for profile in registry["profiles"]
        )
        for relative in profile_files:
            destination = self.project / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / relative, destination)
        self.ledger = self.project / "telemetry/agents/subagents-dispatch.yaml"
        self.database = self.project / "telemetry/runtime/runtime.sqlite3"
        self.runtime = RuntimeService(
            RuntimeSettings(
                database_path=self.database,
                repo_root=self.project,
                ledger_path=self.ledger,
                local_pilot_serve_enabled=True,
            )
        )
        self.bridge = LocalOrchestrationLoggingBridge(
            runtime=self.runtime,
            project_dir=self.project,
            appender_path=APPENDER,
        )
        self.followup_template = (
            "Challenge the findings and converge on a conclusion."
        )
        followup_path = self.project / "workflow/lean-followup.txt"
        followup_path.parent.mkdir(parents=True, exist_ok=True)
        followup_path.write_text(self.followup_template, encoding="utf-8")
        self.followup_digest = digest_bytes(
            self.followup_template.encode("utf-8")
        )
        self.prompts = {
            "kernel": "Investigate the kernel invariants.",
            "lean": (
                "Investigate Lean determinism. The confirmed follow-up template "
                f"digest is {self.followup_digest}."
            ),
            "runtime": "Investigate Lean runtime applicability.",
        }
        self.opening = {
            "dispatch_id": "2026-07-25-foundational-research",
            "schema_version": "0.6.3",
            "dispatch_type": "research",
            "goal": "Research a deterministic foundational kernel.",
            "context": (
                "Three independent researchers examine kernel invariants, Lean "
                "determinism, and runtime applicability under one parent Dispatch."
            ),
            "max_loops": 3,
            "final_approver": "parent",
            "anti_bias_mode": "disabled",
            "working_folder": "research/foundational-kernel-and-formalization",
            "groups": [
                {
                    "group_id": group_id,
                    "agents": [
                        {
                            "agent_name": None,
                            "role": "explorer",
                            "model": "gpt-5.6",
                            "token_budget": 1200,
                            "initial_prompt": prompt,
                        }
                    ],
                }
                for group_id, prompt in self.prompts.items()
            ],
        }
        self.opened = self._open()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _authority(
        self,
        operation: str,
        record: dict,
        *,
        session_id: str | None = None,
        nonce: str,
    ):
        self.bridge.prepare()
        context = {
            "operation": operation,
            "dispatch_id": record.get(
                "dispatch_id" if operation == "open" else "close_of"
            ),
            "record_digest": canonical_digest(record),
            "authorization_evidence_ref": EVIDENCE_REF,
            "authorization_evidence_digest": EVIDENCE_DIGEST,
            "nonce": nonce,
        }
        action = f"orchestration.bridge.{operation}"
        phase = "bootstrap" if operation == "open" else "finalize"
        if operation == "open":
            context.update(
                {
                    "session_name": "host-workflow-test",
                    "origin_ref": "codex:test",
                }
            )
        else:
            context["session_id"] = session_id
        issued = self.runtime.issue_capability(
            principal_id="operator:test",
            action=action,
            phase=phase,
            context=context,
            expires_at="2099-01-01T00:00:00+00:00",
        )
        return self.runtime.capabilities.resolve(
            issued["token"], action=action, phase=phase
        )

    def _open(self) -> dict:
        return self.bridge.open_dispatch(
            authority=self._authority("open", self.opening, nonce="open"),
            record=self.opening,
            session_name="host-workflow-test",
            origin_ref="codex:test",
        )

    def _write_json(self, relative: str, value: dict) -> tuple[str, str]:
        path = self.project / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        body = canonical_text(value).encode("utf-8")
        path.write_bytes(body)
        return relative, digest_bytes(body)

    def _manifest(
        self,
        *,
        group_id: str,
        attempt_id: str,
        turn_ordinal: int = 0,
        slots: list[dict] | None = None,
    ) -> tuple[str, str]:
        return self._write_json(
            f"workflow/{group_id}-{turn_ordinal}.json",
            {
                "schema": "aci-workflow-input-manifest/v1",
                "dispatch_id": self.opening["dispatch_id"],
                "target": {
                    "group_id": group_id,
                    "seat_index": 0,
                    "turn_ordinal": turn_ordinal,
                    "attempt_id": attempt_id,
                },
                "slots": slots or [],
            },
        )

    def _bind(
        self,
        *,
        group_id: str,
        attempt_id: str,
        tool_use_id: str,
        turn_ordinal: int = 0,
        prompt_body: str | None = None,
        prompt_template_path: str | None = None,
        prompt_template_digest: str | None = None,
        target: str | None = None,
        slots: list[dict] | None = None,
    ) -> dict:
        manifest_path, manifest_digest = self._manifest(
            group_id=group_id,
            attempt_id=attempt_id,
            turn_ordinal=turn_ordinal,
            slots=slots,
        )
        prompt = prompt_body or self.prompts[group_id]
        tool_input = {"message": prompt, "task_name": group_id}
        if target is not None:
            tool_input["target"] = target
        return self.runtime.bind_host_workflow_turn(
            host="codex",
            host_session_id="host-session",
            tool_use_id=tool_use_id,
            tool_input=tool_input,
            dispatch_id=self.opening["dispatch_id"],
            group_id=group_id,
            seat_index=0,
            turn_ordinal=turn_ordinal,
            attempt_id=attempt_id,
            prompt_body=prompt,
            prompt_template_path=prompt_template_path,
            prompt_template_digest=(
                prompt_template_digest
                or digest_bytes(prompt.encode("utf-8"))
            ),
            workflow_manifest_path=manifest_path,
            workflow_manifest_digest=manifest_digest,
            actor_ref="operator:test",
        )

    def test_three_seats_share_one_parent_dispatch(self) -> None:
        bindings = [
            self._bind(
                group_id=group_id,
                attempt_id=f"attempt-{group_id}",
                tool_use_id=f"tool-{group_id}",
            )
            for group_id in self.prompts
        ]
        self.assertEqual({item["dispatch_id"] for item in bindings}, {
            self.opening["dispatch_id"]
        })
        with self.runtime.database.connect() as conn:
            count = conn.execute(
                "SELECT COUNT(*) AS n FROM host_workflow_turn_bindings"
            ).fetchone()["n"]
        self.assertEqual(count, 3)
        ledger = self.ledger.read_text(encoding="utf-8")
        self.assertEqual(
            ledger.count(f'  - dispatch_id: "{self.opening["dispatch_id"]}"'),
            1,
        )

    def test_binding_is_idempotent_and_divergent_retry_is_rejected(self) -> None:
        first = self._bind(
            group_id="kernel",
            attempt_id="attempt-kernel",
            tool_use_id="tool-kernel",
        )
        second = self._bind(
            group_id="kernel",
            attempt_id="attempt-kernel",
            tool_use_id="tool-kernel",
        )
        self.assertEqual(first["binding_id"], second["binding_id"])
        with self.assertRaises(IdempotencyConflict):
            self._bind(
                group_id="kernel",
                attempt_id="attempt-kernel",
                tool_use_id="tool-kernel-different",
            )

    def test_parent_cannot_close_while_binding_runs(self) -> None:
        binding = self._bind(
            group_id="kernel",
            attempt_id="attempt-kernel",
            tool_use_id="tool-kernel",
        )
        closing = {
            "close_of": self.opening["dispatch_id"],
            "exit_reason": "resolved",
            "agents_spawned": {
                "total": 1,
                "tree": {"explorer": 1, "helpers": 0},
                "loops_used": 1,
            },
        }
        with self.assertRaises(ConflictError):
            self.bridge.close_dispatch(
                authority=self._authority(
                    "close",
                    closing,
                    session_id=self.opened["session_id"],
                    nonce="close-running",
                ),
                record=closing,
                session_id=self.opened["session_id"],
            )
        self.runtime.complete_host_workflow_turn(
            binding_id=binding["binding_id"],
            state="resolved",
            agent_id="agent-kernel",
            actor_ref="operator:test",
        )
        closed = self.bridge.close_dispatch(
            authority=self._authority(
                "close",
                closing,
                session_id=self.opened["session_id"],
                nonce="close-terminal",
            ),
            record=closing,
            session_id=self.opened["session_id"],
        )
        self.assertEqual(closed["status"], "closed")

    def test_followup_requires_terminal_bound_agent_and_frozen_template(self) -> None:
        first = self._bind(
            group_id="lean",
            attempt_id="attempt-lean-0",
            tool_use_id="tool-lean-0",
        )
        self.runtime.complete_host_workflow_turn(
            binding_id=first["binding_id"],
            state="resolved",
            agent_id="agent-lean",
            actor_ref="operator:test",
        )
        with self.assertRaises(AuthorizationError):
            self._bind(
                group_id="lean",
                attempt_id="attempt-lean-1",
                tool_use_id="tool-lean-1",
                turn_ordinal=1,
                prompt_body=self.followup_template,
                prompt_template_path="workflow/lean-followup.txt",
                prompt_template_digest=self.followup_digest,
                target="different-agent",
            )
        followed = self._bind(
            group_id="lean",
            attempt_id="attempt-lean-1",
            tool_use_id="tool-lean-1",
            turn_ordinal=1,
            prompt_body=self.followup_template,
            prompt_template_path="workflow/lean-followup.txt",
            prompt_template_digest=self.followup_digest,
            target="agent-lean",
        )
        self.assertEqual(followed["turn_ordinal"], 1)

    def test_binding_output_requires_terminal_producer_and_exact_bytes(self) -> None:
        producer = self._bind(
            group_id="kernel",
            attempt_id="attempt-kernel",
            tool_use_id="tool-kernel",
        )
        output = self.project / "workflow/kernel-output.md"
        output.write_text("kernel evidence", encoding="utf-8")
        output_body = output.read_bytes()
        slot = {
            "name": "kernel-result",
            "data_schema_ref": "text/markdown",
            "cardinality": {"min": 1, "max": 1},
            "max_bytes": 1024,
            "purpose": "Consume the upstream research result.",
            "sources": [
                {
                    "source_kind": "binding-output",
                    "producer_binding_id": producer["binding_id"],
                    "path": "workflow/kernel-output.md",
                    "sha256": digest_bytes(output_body),
                    "size_bytes": len(output_body),
                }
            ],
        }
        with self.assertRaises(ConflictError):
            self._bind(
                group_id="runtime",
                attempt_id="attempt-runtime",
                tool_use_id="tool-runtime",
                slots=[slot],
            )
        self.runtime.complete_host_workflow_turn(
            binding_id=producer["binding_id"],
            state="resolved",
            agent_id="agent-kernel",
            actor_ref="operator:test",
        )
        bound = self._bind(
            group_id="runtime",
            attempt_id="attempt-runtime",
            tool_use_id="tool-runtime",
            slots=[slot],
        )
        self.assertEqual(bound["status"], "launch-authorized")
        persisted = self.runtime.get_host_workflow_binding(bound["binding_id"])
        source_ids = json.loads(persisted["source_artifact_ids_json"])
        self.assertEqual(len(source_ids), 1)
        with self.runtime.database.connect() as conn:
            artifact = conn.execute(
                "SELECT content_hash FROM artifacts WHERE artifact_id=?",
                (source_ids[0],),
            ).fetchone()
        self.assertEqual(artifact["content_hash"], digest_bytes(output_body))
        slot["sources"][0]["sha256"] = digest_bytes(b"tampered")
        with self.assertRaises(IntegrityError):
            self._bind(
                group_id="lean",
                attempt_id="attempt-lean",
                tool_use_id="tool-lean",
                slots=[slot],
            )

if __name__ == "__main__":
    unittest.main(verbosity=2)
