from __future__ import annotations

import json
import shutil
import sqlite3
import tempfile
import threading
import unittest
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from implementations.server.runtime.api import create_router
from implementations.server.runtime.canonical import (
    canonical_bytes,
    canonical_bytes_for_schema,
    canonical_digest,
    parse_strict_json,
)
from implementations.server.runtime.cli import run as run_cli
from implementations.server.runtime.errors import (
    AuthorizationError,
    ConflictError,
    IdempotencyConflict,
    IntegrityError,
    GateBlockedError,
    ValidationError,
)
from implementations.server.runtime.journal import RuntimeCommand
from implementations.server.runtime.projections import ProjectionRegistration
from implementations.server.runtime.service import RuntimeService, RuntimeSettings

REPO = Path(__file__).resolve().parents[3]
GOLDEN_LEDGER = (
    REPO
    / "docs/features/agents-communication-infra/adrs/fixtures/"
    "golden-opening-v0.6.1.yaml"
)
DISPATCH_ID = "2026-07-23-local-probe-fixture"


class RuntimeFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.ledger = self.root / "ledger.yaml"
        shutil.copyfile(GOLDEN_LEDGER, self.ledger)
        self.service = RuntimeService(
            RuntimeSettings(self.root / "runtime.db", REPO, self.ledger)
        )
        self.service.open()
        self.service.register_profiles()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def activate(self):
        session = self.service.ensure_session(
            origin_digest="sha256:" + "1" * 64,
            name="fixture",
            actor_ref="test-host",
            actor_authentication_ref="test-auth:fixture",
            actor_authentication_digest="sha256:" + "a" * 64,
        )["session"]["session_id"]
        self.service.link_session_dispatch(
            session_id=session,
            dispatch_id=DISPATCH_ID,
            actor_ref="test-host",
            authorization_policy_ref="test.link@1",
            authorization_policy_digest="sha256:" + "b" * 64,
            authorization_evidence_ref="test-evidence:link",
            authorization_evidence_digest="sha256:" + "c" * 64,
        )
        activation = self.service.activate_local_probe(
            session_id=session,
            dispatch_id=DISPATCH_ID,
            probe_id="probe-1",
            group_aggregate_id="group-1",
            seat_id="seat-1",
            attempt_id="attempt-1",
            operation_id="operation-1",
        )
        return session, activation

    @staticmethod
    def intent(key: str = "pub-1", payload=None):
        return {
            "idempotency_key": key,
            "operation_id": "operation-1",
            "round_id": "probe",
            "message_type": "reference_probe",
            "reply_to_message_ids": [],
            "payload": payload or {"answer": "grounded"},
        }


class CanonicalMigrationTests(RuntimeFixture):
    def test_canonical_contract(self) -> None:
        self.assertEqual(canonical_bytes({"é": "e\u0301"}), b'{"\xc3\xa9":"\xc3\xa9"}')
        with self.assertRaises(ValidationError):
            canonical_bytes({"x": 1.5})
        with self.assertRaises(ValidationError):
            parse_strict_json('{"x":1,"x":2}')
        self.assertRegex(canonical_digest({"x": 1}), r"^sha256:[0-9a-f]{64}$")
        with self.assertRaises(ValidationError):
            canonical_bytes({"x": 2**63})

    def test_frozen_canonical_golden_vectors(self) -> None:
        fixture = json.loads(
            (
                REPO
                / "docs/features/agents-communication-infra/adrs/fixtures/"
                "canonical-contract-vectors.json"
            ).read_text(encoding="utf-8")
        )
        for vector in fixture["vectors"]:
            values = vector.get("equivalent_inputs")
            if values is None:
                values = [
                    parse_strict_json(raw)
                    for raw in vector["equivalent_raw_inputs"]
                ]
            for value in values:
                actual = canonical_bytes_for_schema(value, vector["target_schema"])
                self.assertEqual(actual.decode(), vector["canonical_utf8"], vector["id"])
                self.assertEqual(len(actual), vector["byte_length"], vector["id"])
                self.assertEqual(
                    "sha256:"
                    + __import__("hashlib").sha256(actual).hexdigest(),
                    vector["digest"],
                    vector["id"],
                )
        for rejected in fixture["rejection_vectors"]:
            with self.assertRaises(ValidationError, msg=rejected["id"]):
                canonical_bytes_for_schema(
                    parse_strict_json(rejected["raw_json"]),
                    rejected["target_schema"],
                )

    def test_policy_migrations_and_checksum_drift_fail_closed(self) -> None:
        self.assertEqual(self.service.database.verify_policy()["synchronous"], 2)
        with self.service.database.write() as conn:
            conn.execute(
                "UPDATE schema_migrations SET checksum='sha256:bad' WHERE version=1"
            )
        with self.assertRaises(IntegrityError):
            self.service.database.migrate()

    def test_profile_set_is_one_group_and_exact_four_rows(self) -> None:
        retry = self.service.register_profiles()
        self.assertEqual(retry["first_offset"], retry["last_offset"])
        with self.service.database.connect() as conn:
            self.assertEqual(
                conn.execute("SELECT count(*) FROM protocol_profiles").fetchone()[0], 4
            )


class LegacyCapabilityTests(RuntimeFixture):
    def test_strict_snapshot_and_ledger_unchanged(self) -> None:
        before = self.ledger.read_bytes()
        snapshot = self.service.legacy.resolve(self.ledger, DISPATCH_ID)
        self.service.legacy.verify_unchanged(snapshot)
        self.assertEqual(before, self.ledger.read_bytes())
        self.ledger.write_bytes(before + b"# mutation\n")
        with self.assertRaises(IntegrityError):
            self.service.legacy.verify_unchanged(snapshot)

    def test_strict_snapshot_rejects_duplicate_opening_and_bom(self) -> None:
        raw = self.ledger.read_bytes()
        self.ledger.write_bytes(raw + raw.split(b"dispatches:\n", 1)[1])
        with self.assertRaises(IntegrityError):
            self.service.legacy.resolve(self.ledger, DISPATCH_ID)
        self.ledger.write_bytes(b"\xef\xbb\xbf" + raw)
        with self.assertRaises(IntegrityError):
            self.service.legacy.resolve(self.ledger, DISPATCH_ID)

    def test_capability_is_opaque_scoped_and_rejects_body_authority(self) -> None:
        issued = self.service.issue_capability(
            principal_id="p",
            action="events.read",
            phase="observe",
            context={"scope": "local"},
        )
        raw_db = (self.root / "runtime.db").read_bytes()
        self.assertNotIn(issued["token"].encode(), raw_db)
        self.service.capabilities.resolve(
            issued["token"], action="events.read", phase="observe"
        )
        with self.assertRaises(AuthorizationError):
            self.service.capabilities.resolve(
                issued["token"], action="bus.publish", phase="collect"
            )
        with self.assertRaises(AuthorizationError):
            self.service.capabilities.reject_authority_fields(
                {"dispatch_id": "forged"}
            )
        self.service.capabilities.revoke(issued["capability_id"])
        with self.assertRaises(AuthorizationError):
            self.service.capabilities.resolve(
                issued["token"], action="events.read", phase="observe"
            )


class PublicationFlowTests(RuntimeFixture):
    def test_full_flow_candidate_then_exactly_one_official_and_restart(self) -> None:
        ledger_before = self.ledger.read_bytes()
        session, activation = self.activate()
        agent = activation["issued_capabilities_once"]["agent"]["token"]
        parent = activation["issued_capabilities_once"]["parent"]["token"]
        published = self.service.publish(agent, self.intent())
        with self.service.database.connect() as conn:
            self.assertEqual(conn.execute("SELECT count(*) FROM messages").fetchone()[0], 0)
        official = self.service.verify_publication(
            parent, published["publication_receipt"]
        )
        retry = self.service.verify_publication(
            parent, published["publication_receipt"]
        )
        self.assertEqual(
            canonical_bytes(official),
            canonical_bytes(retry),
        )
        restarted = RuntimeService(
            RuntimeSettings(self.root / "runtime.db", REPO, self.ledger)
        )
        restarted.open()
        self.assertEqual(
            restarted.journal.verify_store()["effective_as_of"],
            official["last_offset"],
        )
        with restarted.database.connect() as conn:
            self.assertEqual(conn.execute("SELECT count(*) FROM messages").fetchone()[0], 1)
        self.assertEqual(ledger_before, self.ledger.read_bytes())
        self.assertEqual(self.service.get_session(session)["session"]["name"], "fixture")

    def test_publish_retry_is_byte_stable_and_changed_digest_conflicts(self) -> None:
        _, activation = self.activate()
        token = activation["issued_capabilities_once"]["agent"]["token"]
        first = self.service.publish(token, self.intent())
        second = self.service.publish(token, self.intent())
        self.assertEqual(canonical_bytes(first), canonical_bytes(second))
        with self.assertRaises(IdempotencyConflict):
            self.service.publish(token, self.intent(payload={"answer": "changed"}))
        changed_intent = self.intent()
        changed_intent["message_type"] = "different"
        with self.assertRaises(IdempotencyConflict):
            self.service.publish(token, changed_intent)

    def test_receipt_tampering_and_wrong_parent_scope_fail(self) -> None:
        _, activation = self.activate()
        published = self.service.publish(
            activation["issued_capabilities_once"]["agent"]["token"], self.intent()
        )
        tampered = dict(published["publication_receipt"])
        tampered["payload_hash"] = "sha256:" + "0" * 64
        with self.assertRaises(ConflictError):
            self.service.verify_publication(
                activation["issued_capabilities_once"]["parent"]["token"], tampered
            )
        wrong = self.service.issue_capability(
            principal_id="parent",
            action="bus.verify",
            phase="collect",
            context={
                **self.service.capabilities.resolve(
                    activation["issued_capabilities_once"]["parent"]["token"],
                    action="bus.verify",
                    phase="collect",
                ).context,
                "attempt_id": "wrong",
            },
        )
        with self.assertRaises(ConflictError):
            self.service.verify_publication(
                wrong["token"], published["publication_receipt"]
            )
        self.service.verify_publication(
            activation["issued_capabilities_once"]["parent"]["token"],
            published["publication_receipt"],
        )
        with self.assertRaises(ConflictError):
            self.service.verify_publication(
                wrong["token"], published["publication_receipt"]
            )

    def test_logical_publication_race_has_one_winner(self) -> None:
        _, activation = self.activate()
        token = activation["issued_capabilities_once"]["agent"]["token"]
        barrier = threading.Barrier(2)
        results: list[str] = []

        def publish(key):
            barrier.wait()
            try:
                self.service.publish(token, self.intent(key=key))
                results.append("accepted")
            except (ConflictError, sqlite3.IntegrityError):
                results.append("conflict")

        threads = [
            threading.Thread(target=publish, args=("race-a",)),
            threading.Thread(target=publish, args=("race-b",)),
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual(sorted(results), ["accepted", "conflict"])
        with self.service.database.connect() as conn:
            self.assertEqual(
                conn.execute(
                    "SELECT count(*) FROM publication_candidates WHERE status='active'"
                ).fetchone()[0],
                1,
            )

    def test_concurrent_parent_verification_converges_to_one_message(self) -> None:
        _, activation = self.activate()
        published = self.service.publish(
            activation["issued_capabilities_once"]["agent"]["token"], self.intent()
        )
        token = activation["issued_capabilities_once"]["parent"]["token"]
        barrier = threading.Barrier(2)
        results: list[dict] = []

        def verify():
            barrier.wait()
            results.append(
                self.service.verify_publication(token, published["publication_receipt"])
            )

        threads = [threading.Thread(target=verify), threading.Thread(target=verify)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual(len(results), 2)
        self.assertEqual(canonical_bytes(results[0]), canonical_bytes(results[1]))
        with self.service.database.connect() as conn:
            self.assertEqual(conn.execute("SELECT count(*) FROM messages").fetchone()[0], 1)


class JournalArtifactApiTests(RuntimeFixture):
    def test_fail_before_commit_rolls_back_and_after_commit_retry_converges(self) -> None:
        command = RuntimeCommand(
            command_id="cmd-fail",
            scope_key="fail",
            idempotency_key="one",
            aggregate_type="test",
            aggregate_id="test:fail",
            expected_version=0,
            causation_id="cmd-fail",
            correlation_id="fail",
            authority_context={"principal_id": "test"},
            semantic_intent={"kind": "failure-fixture"},
        )
        event = self.service._event(
            "aci.local_probe_context_activated@1", {"fixture": True}
        )

        def before_commit(label):
            if label == "before_commit":
                raise RuntimeError("crash")

        with self.assertRaises(RuntimeError):
            self.service.journal.accept(
                command,
                [event],
                next_state={"accepted": True},
                failpoint=before_commit,
            )
        self.assertEqual(self.service.journal.head("test:fail")["current_version"], 0)

        def after_commit(label):
            if label == "after_commit":
                raise RuntimeError("lost response")

        with self.assertRaises(RuntimeError):
            self.service.journal.accept(
                command,
                [event],
                next_state={"accepted": True},
                failpoint=after_commit,
            )
        retry = self.service.journal.accept(
            command, [event], next_state={"accepted": True}
        )
        self.assertEqual(retry["status"], "accepted")
        self.assertEqual(self.service.journal.head("test:fail")["current_version"], 1)

    def test_two_event_group_rolls_back_inside_group_read(self) -> None:
        head = self.service.journal.head("test:group")
        command = self.service._command(
            command_name="test.group@1",
            scope_key="test:group",
            idempotency_key="g1",
            aggregate_type="test",
            aggregate_id="test:group",
            expected_version=head["current_version"],
            authority={"principal_id": "test"},
            intent={"events": 2},
        )
        events = [
            self.service._event(
                "aci.local_probe_context_activated@1", {"ordinal": ordinal}
            )
            for ordinal in (0, 1)
        ]
        receipt = self.service.journal.accept(
            command, events, next_state={"count": 2}
        )
        inside = self.service.journal.read_complete_groups(
            through=receipt["first_offset"]
        )
        self.assertEqual(inside["effective_as_of"], receipt["first_offset"] - 1)
        exact = self.service.journal.read_complete_groups(
            through=receipt["last_offset"]
        )
        self.assertEqual(exact["groups"][-1]["event_count"], 2)

    def test_group_digest_tamper_fails_closed(self) -> None:
        with self.service.database.write() as conn:
            conn.execute(
                "UPDATE events SET group_digest='sha256:bad' WHERE journal_offset=1"
            )
        with self.assertRaises(IntegrityError):
            self.service.journal.read_complete_groups()

    def test_projection_registration_ownership_and_deterministic_apply(self) -> None:
        registration = ProjectionRegistration(
            name="aci.test-count",
            owner_namespace="agents-communication-infra",
            reducer_ref="aci.test-count@1",
            reducer_digest="sha256:" + "4" * 64,
            reducer=lambda state, event: {
                "count": state.get("count", 0) + 1,
                "last": event["event_id"],
            },
        )
        self.service.projections.register(registration)
        with self.assertRaises(ConflictError):
            self.service.projections.register(registration)
        with self.service.database.write() as conn:
            first = self.service.projections.apply_complete_group(
                conn,
                projection_name="aci.test-count",
                projection_key="one",
                events=[{"event_id": "e1"}, {"event_id": "e2"}],
                last_offset=2,
            )
        read = self.service.projections.get("aci.test-count", "one")
        self.assertEqual(read["value"], {"count": 2, "last": "e2"})
        self.assertEqual(first["state_hash"], read["state_hash"])

    def test_artifact_policy_conflict_and_authorized_read(self) -> None:
        prepared = self.service.artifacts.prepare(
            b"answer-sentinel",
            media_type="text/plain",
            schema_ref="test.answer@1",
            classification="sensitive-output",
        )
        ref = self.service.artifacts.commit(prepared)
        body = self.service.artifacts.get_authorized(
            ref["artifact_id"],
            principal_id="reader",
            action="artifact.read",
            authorizer=lambda *_: True,
        )
        self.assertEqual(body, b"answer-sentinel")
        weaker = self.service.artifacts.prepare(
            b"answer-sentinel",
            media_type="text/plain",
            schema_ref="test.answer@1",
            classification="public",
        )
        with self.assertRaises(ConflictError):
            self.service.artifacts.commit(weaker)

    def test_production_router_is_gated_and_test_router_rejects_authority(self) -> None:
        gated = FastAPI()
        gated.include_router(create_router(lambda: self.service, enabled=lambda: False))
        self.assertEqual(
            TestClient(gated).get(
                "/api/runtime/events",
                headers={"Authorization": "Bearer blocked-before-resolution"},
            ).status_code,
            503,
        )
        _, activation = self.activate()
        app = FastAPI()
        app.include_router(create_router(lambda: self.service, enabled=lambda: True))
        response = TestClient(app).post(
            "/api/runtime/bus/publications",
            headers={
                "Authorization": "Bearer "
                + activation["issued_capabilities_once"]["agent"]["token"]
            },
            json={**self.intent(), "dispatch_id": "forged"},
        )
        self.assertEqual(response.status_code, 403)

    def test_cli_serve_gate_has_zero_runtime_effect(self) -> None:
        blocked_db = self.root / "must-not-exist.db"
        import os

        previous = os.environ.get("ACI_RUNTIME_DB")
        os.environ["ACI_RUNTIME_DB"] = str(blocked_db)
        try:
            with self.assertRaises(GateBlockedError):
                run_cli(["serve", "--local-pilot"])
        finally:
            if previous is None:
                os.environ.pop("ACI_RUNTIME_DB", None)
            else:
                os.environ["ACI_RUNTIME_DB"] = previous
        self.assertFalse(blocked_db.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
