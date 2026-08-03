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
    IdempotencyConflict,
    IntegrityError,
)
from implementations.server.runtime.orchestration_bridge import (
    LocalOrchestrationLoggingBridge,
)
from implementations.server.runtime.service import RuntimeService, RuntimeSettings


REPO = Path(__file__).resolve().parents[3]
APPENDER = REPO / ".claude/skills/register-dispatch/append-dispatch.cjs"


class ReferenceDeliveryFixture:
    def build_fixture(self) -> None:
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
        registry = json.loads((REPO / registry_relative).read_text(encoding="utf-8"))
        paths = [registry_relative]
        paths.extend(profile["authoritative_profile_path"] for profile in registry["profiles"])
        paths.extend(
            "docs/features/agents-communication-infra/"
            + profile["local_review_mirror"]["path"]
            for profile in registry["profiles"]
        )
        for relative in paths:
            destination = self.project / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / relative, destination)
        self.ledger = self.project / "telemetry/agents/subagents-dispatch.yaml"
        self.runtime = RuntimeService(
            RuntimeSettings(
                self.project / "runtime.sqlite3",
                self.project,
                self.ledger,
                local_pilot_serve_enabled=True,
            )
        )
        self.bridge = LocalOrchestrationLoggingBridge(
            runtime=self.runtime,
            project_dir=self.project,
            appender_path=APPENDER,
        )
        self.dispatch_id = "2026-07-25-reference-delivery-test"
        self.prompt = "Consume the governed reference bundle."
        self.opening = {
            "dispatch_id": self.dispatch_id,
            "schema_version": "0.6.2",
            "dispatch_type": "review",
            "goal": "Exercise target-agent reference delivery.",
            "context": "Bounded local contract fixture.",
            "max_loops": 1,
            "final_approver": "parent",
            "anti_bias_mode": "disabled",
            "output_mode": "inline",
            "groups": [
                {
                    "group_id": "target",
                    "agents": [
                        {
                            "agent_name": None,
                            "role": "auditor",
                            "model": "gpt-test",
                            "token_budget": 1000,
                            "initial_prompt": self.prompt,
                        }
                    ],
                }
            ],
        }
        self.opened = self.bridge.open_dispatch(
            authority=self._bridge_authority(),
            record=self.opening,
            session_name="reference-delivery-test",
            origin_ref="codex:test",
        )
        self.binding = self._bind()
        self.scout = self._delivered_scout()
        self._delivery_token = self.delivery_token()

    def cleanup_fixture(self) -> None:
        self.temp.cleanup()

    def _bridge_authority(self):
        self.bridge.prepare()
        evidence_digest = canonical_digest({"confirmation": "reference-delivery-test"})
        context = {
            "operation": "open",
            "dispatch_id": self.dispatch_id,
            "record_digest": canonical_digest(self.opening),
            "authorization_evidence_ref": "codex-thread:reference-delivery-test",
            "authorization_evidence_digest": evidence_digest,
            "nonce": "open",
            "session_name": "reference-delivery-test",
            "origin_ref": "codex:test",
        }
        issued = self.runtime.issue_capability(
            principal_id="operator:test",
            action="orchestration.bridge.open",
            phase="bootstrap",
            context=context,
            expires_at="2099-01-01T00:00:00+00:00",
        )
        return self.runtime.capabilities.resolve(
            issued["token"],
            action="orchestration.bridge.open",
            phase="bootstrap",
        )

    def _bind(self) -> dict:
        manifest = {
            "schema": "aci-workflow-input-manifest/v1",
            "dispatch_id": self.dispatch_id,
            "target": {
                "group_id": "target",
                "seat_index": 0,
                "turn_ordinal": 0,
                "attempt_id": "attempt-target-1",
            },
            "slots": [],
        }
        path = self.project / "workflow/target.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        body = canonical_text(manifest).encode("utf-8")
        path.write_bytes(body)
        return self.runtime.bind_host_workflow_turn(
            host="codex",
            host_session_id="host-session",
            tool_use_id="tool-target",
            tool_input={"task_name": "target", "message": self.prompt},
            dispatch_id=self.dispatch_id,
            group_id="target",
            seat_index=0,
            turn_ordinal=0,
            attempt_id="attempt-target-1",
            prompt_body=self.prompt,
            prompt_template_path=None,
            prompt_template_digest=digest_bytes(self.prompt.encode("utf-8")),
            workflow_manifest_path="workflow/target.json",
            workflow_manifest_digest=digest_bytes(body),
            actor_ref="operator:test",
        )

    @staticmethod
    def recommendation() -> dict:
        return {
            "recommendation_id": "rec-1",
            "reference_id": "ref-1",
            "source_class": "primary",
            "locator_observed": "https://example.test/source",
            "access_state": "accessible",
            "found_by_seat_id": "scout-seat",
            "evaluated_by_seat_id": None,
            "evaluation": None,
            "why_inspect": "Primary evidence.",
            "comparability_state": "comparable",
        }

    def _delivered_scout(self) -> dict:
        intent = {
            "session_id": self.opened["session_id"],
            "dispatch_id": self.dispatch_id,
            "objective_ref": "objective:reference-delivery",
            "shape": "small",
            "source_mode": "external",
            "seat_id": "scout-seat",
            "attempt_id": "scout-attempt",
            "operation_id": "scout-operation",
        }
        start = self.runtime.issue_capability(
            principal_id="operator:test",
            action="scout.start",
            phase="bootstrap",
            context=intent,
        )
        started = self.runtime.start_reference_scout(token=start["token"], **intent)
        caps = started["issued_capabilities_once"]
        publication = self.runtime.publish(
            caps["agent"]["token"],
            {
                "idempotency_key": "publish-rec-1",
                "operation_id": "scout-operation",
                "round_id": "scout",
                "message_type": "reference_scout:rec-1",
                "reply_to_message_ids": [],
                "payload": self.recommendation(),
            },
        )
        self.runtime.verify_publication(
            caps["parent"]["token"], publication["publication_receipt"]
        )
        self.runtime.commit_reference_scout(
            token=caps["committer"]["token"],
            scout_run_id=started["scout_run"]["scout_run_id"],
        )
        delivered = self.runtime.deliver_reference_scout(
            token=caps["deliverer"]["token"],
            scout_run_id=started["scout_run"]["scout_run_id"],
        )
        return {
            "scout_run_id": started["scout_run"]["scout_run_id"],
            "source_event_id": delivered["scout_bundle"]["event_id"],
        }

    def delivery_token(self, **changes) -> str:
        context = {
            "binding_id": self.binding["binding_id"],
            "scout_run_id": self.scout["scout_run_id"],
            "source_bundle_delivered_event_id": self.scout["source_event_id"],
            "visibility_policy_ref": "aci.reference-visible-to-target@1",
        }
        context.update(changes)
        return self.runtime.issue_capability(
            principal_id="scheduler:test",
            action="reference_delivery.accept",
            phase="start",
            context=context,
        )["token"]

    def settle(self, **changes):
        values = {
            "token": self._delivery_token,
            "binding_id": self.binding["binding_id"],
            "scout_run_id": self.scout["scout_run_id"],
            "source_bundle_delivered_event_id": self.scout["source_event_id"],
            "base_entries": [
                {
                    "entry_type": "instruction",
                    "content_hash": canonical_digest("follow the task"),
                }
            ],
            "entry_ordinal": 1,
            "idempotency_key": "deliver-to-target",
        }
        values.update(changes)
        return self.runtime.settle_agent_reference_delivery(**values)


class AgentReferenceDeliveryTests(ReferenceDeliveryFixture, unittest.TestCase):
    def setUp(self) -> None:
        self.build_fixture()

    def tearDown(self) -> None:
        self.cleanup_fixture()

    def test_exact_delivery_commits_complete_attempt_unit_and_retry_is_stable(self) -> None:
        first = self.settle()
        second = self.settle()
        self.assertEqual(first, second)
        self.assertEqual(first["event_count"], 2)
        self.assertEqual(first["status"], "launch-authorized")
        with self.runtime.database.connect() as conn:
            counts = {
                table: conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                for table in (
                    "agent_attempts",
                    "effective_input_artifacts",
                    "agent_execution_requests",
                    "sandbox_launch_effects",
                    "agent_reference_deliveries",
                )
            }
        self.assertEqual(set(counts.values()), {1})
        self.assertTrue(first["target"]["target_agent_instance_id"].startswith("agi_"))

    def test_drift_and_cross_scope_capability_fail_closed(self) -> None:
        self.settle()
        with self.assertRaises(IdempotencyConflict):
            self.settle(entry_ordinal=0)
        wrong = self.delivery_token(binding_id="other-binding")
        with self.assertRaises(AuthorizationError):
            self.settle(token=wrong)
        wrong_source = self.delivery_token(
            source_bundle_delivered_event_id="evt_other"
        )
        with self.assertRaises(AuthorizationError):
            self.settle(token=wrong_source)

    def test_every_transaction_failpoint_rolls_back_all_members(self) -> None:
        for point in (
            "after_begin",
            "after_validation",
            "after_artifact",
            "after_event",
            "after_head",
            "after_mutation",
            "after_receipt",
            "before_commit",
        ):
            with self.subTest(point=point):
                self.cleanup_fixture()
                self.build_fixture()

                def failpoint(name: str) -> None:
                    if name == point:
                        raise RuntimeError(point)

                with self.assertRaisesRegex(RuntimeError, point):
                    self.settle(failpoint=failpoint)
                with self.runtime.database.connect() as conn:
                    for table in (
                        "agent_attempts",
                        "effective_input_artifacts",
                        "agent_execution_requests",
                        "sandbox_launch_effects",
                        "agent_reference_deliveries",
                    ):
                        self.assertEqual(
                            conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0],
                            0,
                        )

    def test_bundle_bytes_and_lifecycle_membership_are_verified(self) -> None:
        with self.runtime.database.write() as conn:
            row = conn.execute(
                """
                SELECT a.artifact_id,a.body FROM artifacts a
                JOIN reference_scout_runs r ON r.bundle_artifact_id=a.artifact_id
                WHERE r.scout_run_id=?
                """,
                (self.scout["scout_run_id"],),
            ).fetchone()
            conn.execute(
                "UPDATE artifacts SET body=? WHERE artifact_id=?",
                (bytes(row["body"]) + b" ", row["artifact_id"]),
            )
        with self.assertRaises(IntegrityError):
            self.settle()

    def test_after_commit_failure_converges_to_the_original_receipt(self) -> None:
        def fail_after_commit(name: str) -> None:
            if name == "after_commit":
                raise RuntimeError(name)

        with self.assertRaisesRegex(RuntimeError, "after_commit"):
            self.settle(failpoint=fail_after_commit)
        recovered = self.settle()
        self.assertEqual(recovered["event_count"], 2)
        with self.runtime.database.connect() as conn:
            self.assertEqual(
                conn.execute(
                    "SELECT COUNT(*) FROM agent_reference_deliveries"
                ).fetchone()[0],
                1,
            )


if __name__ == "__main__":
    unittest.main()
