from __future__ import annotations

import json
import unittest
from unittest.mock import patch

from implementations.server.runtime.canonical import canonical_bytes, canonical_digest
from implementations.server.runtime.errors import (
    AuthorizationError,
    ConflictError,
    IdempotencyConflict,
    IntegrityError,
    ValidationError,
)
from implementations.server.runtime.reference_delivery import derive_target_identity
from implementations.server.runtime.reveal_delivery import (
    VISIBILITY_POLICY_REF,
    build_effective_input_manifest,
    build_peer_entries,
)
from implementations.server.runtime.service import RuntimeService
from implementations.tests.runtime.test_agent_reference_delivery import (
    ReferenceDeliveryFixture,
)


class BusRevealDeliveryTests(ReferenceDeliveryFixture, unittest.TestCase):
    def setUp(self) -> None:
        self.build_fixture()
        with self.runtime.database.connect() as conn:
            binding = dict(
                conn.execute(
                    "SELECT * FROM host_workflow_turn_bindings WHERE binding_id=?",
                    (self.binding["binding_id"],),
                ).fetchone()
            )
        self.target = derive_target_identity(binding)
        self.group_id = (
            f"aci.group:{binding['dispatch_id']}:{binding['group_id']}"
        )
        self.target_seat_id = self.target["target_seat_id"]
        self.round_id = "round-1"

    def tearDown(self) -> None:
        self.cleanup_fixture()

    def _capability(self, action: str, phase: str, context: dict) -> str:
        return self.runtime.issue_capability(
            principal_id="kernel:test",
            action=action,
            phase=phase,
            context=context,
        )["token"]

    def _publish(self, seat: str, *, verify: bool) -> dict:
        operation_id = f"operation-{seat}"
        attempt_id = f"source-attempt-{seat}"
        common = {
            "aggregate_id": self.group_id,
            "aggregate_type": "aci.group",
            "group_aggregate_id": self.group_id,
            "seat_id": seat,
            "attempt_id": attempt_id,
            "operation_id": operation_id,
            "expected_round_id": self.round_id,
            "profile_binding": {
                "profile_id": "fixed-two-seat-proof",
                "profile_version": "1",
                "profile_digest": canonical_digest("fixed-two-seat-proof"),
            },
        }
        publication = self.runtime.publish(
            self._capability("bus.publish", "collect", common),
            {
                "idempotency_key": f"publish-{seat}",
                "operation_id": operation_id,
                "round_id": self.round_id,
                "message_type": "position",
                "reply_to_message_ids": [],
                "payload": {"seat": seat, "position": f"position-{seat}"},
            },
        )
        if verify:
            publication["verification"] = self.runtime.verify_publication(
                self._capability("bus.verify", "collect", common),
                publication["publication_receipt"],
            )
        return publication

    def _close(self) -> dict:
        return self.runtime.close_collection(
            token=self._capability(
                "bus.close",
                "collect",
                {
                    "group_aggregate_id": self.group_id,
                    "round_id": self.round_id,
                },
            ),
            group_aggregate_id=self.group_id,
            round_id=self.round_id,
        )

    def _reveal(self) -> dict:
        closure = self._close()["collection_closure"]
        entries = closure["message_entries"]
        manifest_hash = canonical_digest(
            {
                "group_aggregate_id": self.group_id,
                "round_id": self.round_id,
                "message_entries": entries,
            }
        )
        return self.runtime.publish_reveal_manifest(
            token=self._capability(
                "bus.reveal",
                "reveal",
                {
                    "group_aggregate_id": self.group_id,
                    "round_id": self.round_id,
                },
            ),
            group_aggregate_id=self.group_id,
            round_id=self.round_id,
            message_entries=entries,
            manifest_hash=manifest_hash,
        )

    def _plan_document(
        self, *, target_seat_id: str | None = None
    ) -> tuple[dict, dict]:
        target_seat_id = target_seat_id or self.target_seat_id
        base = self.runtime.artifacts.commit(
            self.runtime.artifacts.prepare(
                canonical_bytes(
                    {
                        "entries": [
                            {
                                "entry_type": "instruction",
                                "artifact_ref": "art_instruction",
                                "content_hash": canonical_digest("instruction"),
                                "author_principal_id": None,
                                "message_id": None,
                                "reveal_manifest_id": None,
                                "visibility_policy_ref": "aci.plan-base@1",
                            }
                        ]
                    }
                ),
                media_type="application/json",
                schema_ref="aci.effective-input-base@1",
                classification="sensitive-input",
            )
        )
        plan = {
            "attempt_id": self.binding["attempt_id"],
            "operation_id": "peer-target-operation",
            "seat_id": target_seat_id,
            "group_aggregate_id": self.group_id,
            "binding_id": self.binding["binding_id"],
            "provider_ref": "aci.host.codex@1",
            "adapter_ref": "aci.fixed-local-peer-input-materializer@1",
            "model_ref": "aci.model.fake@1",
            "role_contract_ref": "aci.role.peer-target@1",
            "task_ref": "aci.task.peer-review@1",
            "base_snapshot_ref": base["artifact_id"],
            "role_delta_ref": None,
            "response_schema_ref": "aci.response.position@1",
            "tool_profile_ref": "aci.tools.none@1",
            "deadline": "2099-01-01T00:00:00Z",
            "resource_budget": {"max_tokens": 1000},
            "sandbox_policy": {"network": "denied"},
            "authority_fence": {"mode": "runtime-managed"},
        }
        plan_authority = {
            "binding_id": self.binding["binding_id"],
            "group_aggregate_id": self.group_id,
            "target_attempt_id": plan["attempt_id"],
            "target_seat_id": plan["seat_id"],
            "provider_ref": plan["provider_ref"],
            "adapter_ref": plan["adapter_ref"],
        }
        return plan, plan_authority

    def _plan(self, *, target_seat_id: str | None = None) -> tuple[dict, dict]:
        plan, plan_authority = self._plan_document(target_seat_id=target_seat_id)
        registered = self.runtime.authorize_agent_invocation_plan(
            token=self._capability("bus.plan", "plan", plan_authority),
            binding_id=self.binding["binding_id"],
            plan=plan,
        )
        return plan, registered

    def _materialize(self, *, token: str | None = None, failpoint=None) -> dict:
        reveal = self._reveal()["reveal_manifest"]
        plan, registered = self._plan()
        capability_context = {
            "agent_invocation_plan_ref": registered["plan_ref"],
            "agent_invocation_plan_digest": registered["plan_digest"],
            "target_attempt_id": plan["attempt_id"],
            "target_seat_id": plan["seat_id"],
        }
        return self.runtime.materialize_authorized_peer_input(
            token=token
            or self._capability("bus.materialize", "reveal", capability_context),
            reveal_manifest_id=reveal["reveal_manifest_id"],
            visibility_policy_ref=VISIBILITY_POLICY_REF,
            idempotency_key="deliver-peer-input",
            failpoint=failpoint,
        )

    def test_peer1_close_freezes_only_official_and_keeps_read_surface_absent(self) -> None:
        official = self._publish("seat-a", verify=True)
        self._publish(self.target_seat_id, verify=False)
        close = self._close()["collection_closure"]
        self.assertEqual(
            close["message_entries"],
            [
                {
                    "message_id": official["publication_receipt"]["message_id"],
                    "payload_hash": official["publication_receipt"]["payload_hash"],
                }
            ],
        )
        self.assertEqual(close["peer_visibility"], "sealed")
        for name in ("list_peer_messages", "read_peer_message", "search_peer_messages"):
            self.assertFalse(hasattr(RuntimeService, name))

    def test_peer2_reveal_is_exact_and_restart_stable(self) -> None:
        self._publish("seat-a", verify=True)
        self._publish(self.target_seat_id, verify=False)
        closed = self._close()["collection_closure"]
        restarted = RuntimeService(self.runtime.settings)
        restarted.open()
        self.runtime = restarted
        self.assertEqual(
            self._close()["collection_closure"],
            closed,
        )
        with self.assertRaises(ConflictError):
            self._publish("seat-after-close", verify=False)
        first = self._reveal()
        second = self._reveal()
        self.assertEqual(first, second)
        entries = first["reveal_manifest"]["message_entries"] + [
            {"message_id": "forged", "payload_hash": canonical_digest("forged")}
        ]
        with self.assertRaises(ConflictError):
            self.runtime.publish_reveal_manifest(
                token=self._capability(
                    "bus.reveal",
                    "reveal",
                    {
                        "group_aggregate_id": self.group_id,
                        "round_id": self.round_id,
                    },
                ),
                group_aggregate_id=self.group_id,
                round_id=self.round_id,
                message_entries=entries,
                manifest_hash=canonical_digest(
                    {
                        "group_aggregate_id": self.group_id,
                        "round_id": self.round_id,
                        "message_entries": entries,
                    }
                ),
            )

    def test_peer3_recipient_authority_is_derived(self) -> None:
        self._publish("seat-a", verify=True)
        reveal = self._reveal()["reveal_manifest"]
        plan, canonical_authority = self._plan_document()
        with self.runtime.database.connect() as conn:
            plan_count = conn.execute(
                "SELECT COUNT(*) FROM agent_invocation_plans"
            ).fetchone()[0]
        for field, forged_value in (
            ("attempt_id", "attempt-forged"),
            ("seat_id", "seat-forged"),
            ("group_aggregate_id", "aci.group:cross-scope"),
            ("provider_ref", "aci.host.forged@1"),
            ("adapter_ref", "aci.adapter.forged@1"),
        ):
            with self.subTest(field=field):
                forged_plan = dict(plan)
                forged_plan[field] = forged_value
                with self.assertRaises(AuthorizationError):
                    self.runtime.authorize_agent_invocation_plan(
                        token=self._capability(
                            "bus.plan", "plan", canonical_authority
                        ),
                        binding_id=self.binding["binding_id"],
                        plan=forged_plan,
                    )
                with self.runtime.database.connect() as conn:
                    self.assertEqual(
                        conn.execute(
                            "SELECT COUNT(*) FROM agent_invocation_plans"
                        ).fetchone()[0],
                        plan_count,
                    )
        registered = self.runtime.authorize_agent_invocation_plan(
            token=self._capability("bus.plan", "plan", canonical_authority),
            binding_id=self.binding["binding_id"],
            plan=plan,
        )
        wrong = self._capability(
            "bus.materialize",
            "reveal",
            {
                "agent_invocation_plan_ref": registered["plan_ref"],
                "agent_invocation_plan_digest": registered["plan_digest"],
                "target_attempt_id": plan["attempt_id"],
                "target_seat_id": "seat-forged",
            },
        )
        with self.assertRaises(AuthorizationError):
            self.runtime.materialize_authorized_peer_input(
                token=wrong,
                reveal_manifest_id=reveal["reveal_manifest_id"],
                visibility_policy_ref=VISIBILITY_POLICY_REF,
                idempotency_key="deliver-peer-input",
            )
        with self.runtime.database.connect() as conn:
            self.assertEqual(
                conn.execute("SELECT COUNT(*) FROM agent_attempts").fetchone()[0], 0
            )

    def test_peer4_filter_and_wrapper_complete_artifact_binding(self) -> None:
        seat_a = "seat-a"
        seat_b = self.target_seat_id
        official_a = self._publish(seat_a, verify=True)
        official_b = self._publish(seat_b, verify=True)
        unaccepted = self._publish("seat-candidate", verify=False)
        official = [
            {
                "message_id": official_a["publication_receipt"]["message_id"],
                "payload_hash": official_a["publication_receipt"]["payload_hash"],
                "artifact_content_hash": official_a["publication_receipt"]["payload_hash"],
                "payload_ref": official_a["verification"]["official_message"]["payload_ref"],
                "seat_id": seat_a,
            },
            {
                "message_id": official_b["publication_receipt"]["message_id"],
                "payload_hash": official_b["publication_receipt"]["payload_hash"],
                "artifact_content_hash": official_b["publication_receipt"]["payload_hash"],
                "payload_ref": official_b["verification"]["official_message"]["payload_ref"],
                "seat_id": seat_b,
            },
        ]
        manifest_entries = [
            {"message_id": row["message_id"], "payload_hash": row["payload_hash"]}
            for row in official
        ]
        delivered_to_a = build_peer_entries(
            reveal_manifest_id="reveal-fixture",
            manifest_entries=manifest_entries,
            official_messages=official,
            target_seat_id=seat_a,
            visibility_policy_ref=VISIBILITY_POLICY_REF,
        )
        delivered_to_b = build_peer_entries(
            reveal_manifest_id="reveal-fixture",
            manifest_entries=manifest_entries,
            official_messages=official,
            target_seat_id=seat_b,
            visibility_policy_ref=VISIBILITY_POLICY_REF,
        )
        self.assertEqual(
            [entry["author_principal_id"] for entry in delivered_to_a], [seat_b]
        )
        self.assertEqual(
            [entry["author_principal_id"] for entry in delivered_to_b], [seat_a]
        )
        finalized_self = dict(delivered_to_a[0])
        finalized_self["author_principal_id"] = seat_a
        with self.assertRaises(IntegrityError):
            build_effective_input_manifest(
                plan={
                    "attempt_id": "attempt-self-negative",
                    "seat_id": seat_a,
                    "base_snapshot_ref": "base-self-negative",
                    "role_delta_ref": None,
                    "tool_profile_ref": "aci.tools.none@1",
                    "response_schema_ref": "aci.response.position@1",
                },
                effective_input_artifact_id="artifact-self-negative",
                base_entries=[],
                peer_entries=[finalized_self],
                reveal_manifest_entries=manifest_entries,
                provider_invocation_ref="wrapper-self-negative",
                provider_invocation_hash=canonical_digest("wrapper-self-negative"),
            )
        with self.assertRaises(ValidationError):
            build_peer_entries(
                reveal_manifest_id="reveal-fixture",
                manifest_entries=manifest_entries,
                official_messages=official,
                target_seat_id=seat_b,
                visibility_policy_ref="aci.denied@1",
            )
        with self.assertRaises(IntegrityError):
            build_peer_entries(
                reveal_manifest_id="reveal-fixture",
                manifest_entries=manifest_entries
                + [{"message_id": "absent", "payload_hash": canonical_digest("absent")}],
                official_messages=official,
                target_seat_id=seat_b,
                visibility_policy_ref=VISIBILITY_POLICY_REF,
            )
        with self.assertRaises(IntegrityError):
            build_peer_entries(
                reveal_manifest_id="reveal-fixture",
                manifest_entries=manifest_entries
                + [
                    {
                        "message_id": unaccepted["publication_receipt"]["message_id"],
                        "payload_hash": unaccepted["publication_receipt"]["payload_hash"],
                    }
                ],
                official_messages=official,
                target_seat_id=seat_b,
                visibility_policy_ref=VISIBILITY_POLICY_REF,
            )
        altered = [dict(entry) for entry in manifest_entries]
        altered[0]["payload_hash"] = canonical_digest("altered")
        with self.assertRaises(IntegrityError):
            build_peer_entries(
                reveal_manifest_id="reveal-fixture",
                manifest_entries=altered,
                official_messages=official,
                target_seat_id=seat_b,
                visibility_policy_ref=VISIBILITY_POLICY_REF,
            )
        third = {
            "message_id": "message-third",
            "payload_hash": canonical_digest("third"),
            "artifact_content_hash": canonical_digest("third"),
            "payload_ref": "artifact-third",
            "seat_id": seat_a,
        }
        ordered_official = [third, official[1], official[0]]
        ordered_entries = [
            {"message_id": row["message_id"], "payload_hash": row["payload_hash"]}
            for row in ordered_official
        ]
        ordered_result = build_peer_entries(
            reveal_manifest_id="reveal-fixture",
            manifest_entries=ordered_entries,
            official_messages=ordered_official,
            target_seat_id=seat_b,
            visibility_policy_ref=VISIBILITY_POLICY_REF,
        )
        self.assertEqual(
            [entry["message_id"] for entry in ordered_result],
            [third["message_id"], official[0]["message_id"]],
        )
        closure = self._close()["collection_closure"]
        reversed_entries = list(reversed(closure["message_entries"]))
        with self.assertRaises(ConflictError):
            self.runtime.publish_reveal_manifest(
                token=self._capability(
                    "bus.reveal",
                    "reveal",
                    {
                        "group_aggregate_id": self.group_id,
                        "round_id": self.round_id,
                    },
                ),
                group_aggregate_id=self.group_id,
                round_id=self.round_id,
                message_entries=reversed_entries,
                manifest_hash=canonical_digest(
                    {
                        "group_aggregate_id": self.group_id,
                        "round_id": self.round_id,
                        "message_entries": reversed_entries,
                    }
                ),
            )
        result = self._materialize()
        receipt = result["peer_input_delivery_receipt"]
        with self.runtime.database.connect() as conn:
            delivery = conn.execute("SELECT * FROM peer_input_deliveries").fetchone()
            artifact = conn.execute(
                "SELECT * FROM artifacts WHERE artifact_id=?",
                (receipt["effective_input_artifact_id"],),
            ).fetchone()
        entries = json.loads(delivery["peer_message_entries_json"])
        self.assertEqual([entry["author_principal_id"] for entry in entries], ["seat-a"])
        manifest = json.loads(bytes(artifact["body"]))
        self.assertEqual(manifest["adapter_wrapper_refs"], [manifest["entries"][-1]["artifact_ref"]])
        self.assertEqual(artifact["content_hash"], receipt["effective_input_manifest_hash"])

    def test_peer5_atomic_acceptance_rolls_back_each_internal_failpoint(self) -> None:
        for point, occurrence in (
            ("after_artifact", 1),
            ("after_artifact", 2),
            ("after_artifact", 3),
            ("after_artifact", 4),
            ("after_event", 1),
            ("after_event", 2),
            ("after_head", 1),
            ("after_attempt", 1),
            ("after_effective_input", 1),
            ("after_materialized_invocation", 1),
            ("after_execution_request", 1),
            ("after_request_binding", 1),
            ("after_effect", 1),
            ("after_peer_delivery", 1),
            ("after_delivery_receipt", 1),
            ("after_mutation", 1),
            ("after_receipt", 1),
            ("before_commit", 1),
        ):
            with self.subTest(point=point, occurrence=occurrence):
                self.cleanup_fixture()
                self.build_fixture()
                with self.runtime.database.connect() as conn:
                    binding = dict(
                        conn.execute(
                            "SELECT * FROM host_workflow_turn_bindings WHERE binding_id=?",
                            (self.binding["binding_id"],),
                        ).fetchone()
                    )
                self.target = derive_target_identity(binding)
                self.group_id = (
                    f"aci.group:{binding['dispatch_id']}:{binding['group_id']}"
                )
                self.target_seat_id = self.target["target_seat_id"]
                self.round_id = "round-1"
                self._publish("seat-a", verify=True)
                self._reveal()
                self._plan()
                all_tables = (
                    "artifacts",
                    "events",
                    "aggregate_heads",
                    "command_receipts",
                    "agent_attempts",
                    "effective_input_artifacts",
                    "materialized_agent_invocations",
                    "agent_execution_requests",
                    "agent_request_bindings",
                    "sandbox_launch_effects",
                    "peer_input_deliveries",
                    "peer_input_delivery_receipts",
                )
                with self.runtime.database.connect() as conn:
                    baseline = {
                        table: conn.execute(
                            f"SELECT COUNT(*) FROM {table}"
                        ).fetchone()[0]
                        for table in all_tables
                    }
                seen = 0

                def failpoint(name: str) -> None:
                    nonlocal seen
                    if name == point:
                        seen += 1
                    if name == point and seen == occurrence:
                        raise RuntimeError(point)

                with self.assertRaisesRegex(RuntimeError, point):
                    self._materialize(failpoint=failpoint)
                with self.runtime.database.connect() as conn:
                    for table in all_tables:
                        self.assertEqual(
                            conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0],
                            baseline[table],
                        )

    def test_peer6_retry_receipt_is_stable_and_semantic_drift_conflicts(self) -> None:
        self._publish("seat-a", verify=True)
        first = self._materialize()
        second = self._materialize()
        self.assertEqual(first, second)
        with self.runtime.database.connect() as conn:
            plan_row = conn.execute("SELECT * FROM agent_invocation_plans").fetchone()
            baseline = {
                table: conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                for table in (
                    "artifacts",
                    "events",
                    "aggregate_heads",
                    "command_receipts",
                    "agent_attempts",
                    "peer_input_deliveries",
                    "peer_input_delivery_receipts",
                )
            }
        with self.runtime.database.write() as conn:
            conn.execute(
                "UPDATE reveal_manifests SET manifest_hash=? WHERE reveal_manifest_id=?",
                (
                    canonical_digest("semantic-drift"),
                    first["peer_input_delivery_receipt"]["reveal_manifest_id"],
                ),
            )
        authority = {
            "agent_invocation_plan_ref": plan_row["plan_ref"],
            "agent_invocation_plan_digest": plan_row["plan_digest"],
            "target_attempt_id": plan_row["attempt_id"],
            "target_seat_id": plan_row["seat_id"],
        }
        for _ in range(2):
            with self.assertRaises(IdempotencyConflict):
                self.runtime.materialize_authorized_peer_input(
                    token=self._capability("bus.materialize", "reveal", authority),
                    reveal_manifest_id=first["peer_input_delivery_receipt"][
                        "reveal_manifest_id"
                    ],
                    visibility_policy_ref=VISIBILITY_POLICY_REF,
                    idempotency_key="deliver-peer-input",
                )
            with self.runtime.database.connect() as conn:
                for table, count in baseline.items():
                    self.assertEqual(
                        conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0],
                        count,
                    )

    def test_peer7_effect_remains_pending_and_no_provider_surface_runs(self) -> None:
        self._publish("seat-a", verify=True)
        reveal = self._reveal()["reveal_manifest"]
        plan, registered = self._plan()
        authority = {
            "agent_invocation_plan_ref": registered["plan_ref"],
            "agent_invocation_plan_digest": registered["plan_digest"],
            "target_attempt_id": plan["attempt_id"],
            "target_seat_id": plan["seat_id"],
        }
        token = self._capability("bus.materialize", "reveal", authority)
        before_methods = set(dir(self.runtime))
        with self.runtime.database.connect() as conn:
            before_actions = {
                row["action"] for row in conn.execute("SELECT action FROM capabilities")
            }
        with patch("subprocess.run") as process_run, patch(
            "subprocess.Popen"
        ) as process_popen:
            result = self.runtime.materialize_authorized_peer_input(
                token=token,
                reveal_manifest_id=reveal["reveal_manifest_id"],
                visibility_policy_ref=VISIBILITY_POLICY_REF,
                idempotency_key="deliver-peer-input",
            )
        process_run.assert_not_called()
        process_popen.assert_not_called()
        after_methods = set(dir(self.runtime))
        with self.runtime.database.connect() as conn:
            effect = conn.execute("SELECT * FROM sandbox_launch_effects").fetchone()
            after_actions = {
                row["action"] for row in conn.execute("SELECT action FROM capabilities")
            }
        self.assertEqual(before_methods, after_methods)
        self.assertEqual(before_actions, after_actions)
        for forbidden in ("peer.read", "peer.list", "peer.search", "effect.claim", "provider.start", "tool.start"):
            self.assertNotIn(forbidden, after_actions)
        self.assertEqual(effect["state"], "pending")
        self.assertNotIn("claim_id", effect.keys())


if __name__ == "__main__":
    unittest.main()
