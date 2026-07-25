from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from implementations.server.runtime.api import create_router
from implementations.server.runtime.canonical import canonical_digest
from implementations.server.runtime.errors import (
    AuthorizationError,
    ConflictError,
    ValidationError,
)
from implementations.server.runtime.service import RuntimeService, RuntimeSettings

REPO = Path(__file__).resolve().parents[3]
GOLDEN_LEDGER = (
    REPO
    / "docs/features/agents-communication-infra/adrs/fixtures/"
    "golden-opening-v0.6.1.yaml"
)
DISPATCH_ID = "2026-07-23-local-probe-fixture"


class ReferenceScoutIngestionTests(unittest.TestCase):
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
        self.session_id = self.service.ensure_session(
            origin_digest="sha256:" + "9" * 64,
            name="Scout integration",
            actor_ref="host:test",
            actor_authentication_ref="auth:test",
            actor_authentication_digest="sha256:" + "a" * 64,
        )["session"]["session_id"]
        self.service.link_session_dispatch(
            session_id=self.session_id,
            dispatch_id=DISPATCH_ID,
            actor_ref="host:test",
            authorization_policy_ref="policy:test@1",
            authorization_policy_digest="sha256:" + "b" * 64,
            authorization_evidence_ref="evidence:test",
            authorization_evidence_digest="sha256:" + "c" * 64,
        )
        self.service.record_orchestration_dispatch_opened(
            session_id=self.session_id,
            dispatch_id=DISPATCH_ID,
            actor_ref="host:test",
            authorization_evidence_ref="evidence:test",
            authorization_evidence_digest="sha256:" + "c" * 64,
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _start(self):
        intent = {
            "session_id": self.session_id,
            "dispatch_id": DISPATCH_ID,
            "objective_ref": "objective:find-primary-source",
            "shape": "small",
            "source_mode": "internal-and-external",
            "seat_id": "scout-seat-1",
            "attempt_id": "scout-attempt-1",
            "operation_id": "scout-operation-1",
        }
        issued = self.service.issue_capability(
            principal_id="operator:test",
            action="scout.start",
            phase="bootstrap",
            context=intent,
        )
        return self.service.start_reference_scout(token=issued["token"], **intent)

    @staticmethod
    def _recommendation() -> dict:
        return {
            "recommendation_id": "rec-1",
            "reference_id": "ref-1",
            "source_class": "primary",
            "locator_observed": "https://example.test/primary",
            "access_state": "accessible",
            "found_by_seat_id": "scout-seat-1",
            "evaluated_by_seat_id": None,
            "evaluation": None,
            "why_inspect": "It is the primary source for the requested claim.",
            "comparability_state": "comparable",
        }

    def test_scout_bus_commit_delivery_and_restart_query(self) -> None:
        started = self._start()
        caps = started["issued_capabilities_once"]
        scout = started["scout_run"]
        publication = self.service.publish(
            caps["agent"]["token"],
            {
                "idempotency_key": "publish-rec-1",
                "operation_id": "scout-operation-1",
                "round_id": "scout",
                "message_type": "reference_scout:rec-1",
                "reply_to_message_ids": [],
                "payload": self._recommendation(),
            },
        )
        verified = self.service.verify_publication(
            caps["parent"]["token"], publication["publication_receipt"]
        )
        self.assertEqual(
            verified["official_message"]["message_id"],
            publication["publication_receipt"]["message_id"],
        )
        committed = self.service.commit_reference_scout(
            token=caps["committer"]["token"],
            scout_run_id=scout["scout_run_id"],
        )
        self.assertEqual(
            committed["scout_bundle"]["recommendation_count"], 1
        )
        delivered = self.service.deliver_reference_scout(
            token=caps["deliverer"]["token"],
            scout_run_id=scout["scout_run_id"],
        )
        self.assertEqual(delivered["scout_bundle"]["state"], "delivered")

        restarted = RuntimeService(
            RuntimeSettings(self.root / "runtime.db", REPO, self.ledger)
        )
        restarted.open()
        view = restarted.get_reference_scout(scout["scout_run_id"])
        self.assertEqual(view["scout_run"]["state"], "delivered")
        self.assertEqual(len(view["recommendations"]), 1)
        self.assertEqual(
            view["recommendations"][0]["locator_observed"],
            "https://example.test/primary",
        )
        self.assertEqual(
            restarted.journal.verify_store()["effective_as_of"],
            delivered["last_offset"],
        )

    def test_scout_http_surface_runs_complete_lifecycle(self) -> None:
        app = FastAPI()
        app.include_router(
            create_router(lambda: self.service, enabled=lambda: True)
        )
        client = TestClient(app)
        intent = {
            "session_id": self.session_id,
            "dispatch_id": DISPATCH_ID,
            "objective_ref": "objective:http-scout",
            "shape": "small",
            "source_mode": "external",
            "seat_id": "scout-seat-1",
            "attempt_id": "http-attempt",
            "operation_id": "http-operation",
        }
        start_token = self.service.issue_capability(
            principal_id="operator:http",
            action="scout.start",
            phase="bootstrap",
            context=intent,
        )["token"]
        started = client.post(
            "/api/runtime/scouts",
            json=intent,
            headers={
                "Authorization": f"Bearer {start_token}",
                "Idempotency-Key": "http-start",
            },
        )
        self.assertEqual(started.status_code, 200, started.text)
        body = started.json()
        scout_id = body["scout_run"]["scout_run_id"]
        caps = body["issued_capabilities_once"]
        publication = client.post(
            "/api/runtime/bus/publications",
            json={
                "idempotency_key": "http-publish",
                "operation_id": "http-operation",
                "round_id": "scout",
                "message_type": "reference_scout:rec-1",
                "reply_to_message_ids": [],
                "payload": self._recommendation(),
            },
            headers={"Authorization": f"Bearer {caps['agent']['token']}"},
        )
        self.assertEqual(publication.status_code, 200, publication.text)
        verified = client.post(
            "/api/runtime/bus/publications/verify",
            json={
                "publication_receipt": publication.json()["publication_receipt"]
            },
            headers={"Authorization": f"Bearer {caps['parent']['token']}"},
        )
        self.assertEqual(verified.status_code, 200, verified.text)
        committed = client.post(
            f"/api/runtime/scouts/{scout_id}/commit",
            json={},
            headers={
                "Authorization": f"Bearer {caps['committer']['token']}",
                "Idempotency-Key": "http-commit",
            },
        )
        self.assertEqual(committed.status_code, 200, committed.text)
        delivered = client.post(
            f"/api/runtime/scouts/{scout_id}/deliver",
            json={},
            headers={
                "Authorization": f"Bearer {caps['deliverer']['token']}",
                "Idempotency-Key": "http-deliver",
            },
        )
        self.assertEqual(delivered.status_code, 200, delivered.text)
        read_token = self.service.issue_capability(
            principal_id="reader:http",
            action="scout.read",
            phase="observe",
            context={"scout_run_id": scout_id},
        )["token"]
        view = client.get(
            f"/api/runtime/scouts/{scout_id}",
            headers={"Authorization": f"Bearer {read_token}"},
        )
        self.assertEqual(view.status_code, 200, view.text)
        self.assertEqual(view.json()["scout_run"]["state"], "delivered")

    def test_scout_capability_and_message_identity_fail_closed(self) -> None:
        started = self._start()
        caps = started["issued_capabilities_once"]
        with self.assertRaises(ConflictError):
            self.service.require_orchestration_dispatch_can_close(
                session_id=self.session_id,
                dispatch_id=DISPATCH_ID,
                actor_ref="host:test",
                authorization_evidence_ref="evidence:test",
                authorization_evidence_digest="sha256:" + "c" * 64,
            )
        with self.assertRaises(ValidationError):
            self.service.publish(
                caps["agent"]["token"],
                {
                    "idempotency_key": "bad-type",
                    "operation_id": "scout-operation-1",
                    "round_id": "scout",
                    "message_type": "wrong",
                    "reply_to_message_ids": [],
                    "payload": self._recommendation(),
                },
            )
        other = self.service.issue_capability(
            principal_id="operator:test",
            action="scout.start",
            phase="bootstrap",
            context={
                "session_id": self.session_id,
                "dispatch_id": DISPATCH_ID,
                "objective_ref": "different",
                "shape": "small",
                "source_mode": "internal",
                "seat_id": "seat",
                "attempt_id": "attempt",
                "operation_id": "operation",
            },
        )
        with self.assertRaises(AuthorizationError):
            self.service.start_reference_scout(
                token=other["token"],
                session_id=self.session_id,
                dispatch_id=DISPATCH_ID,
                objective_ref="not-different",
                shape="small",
                source_mode="internal",
                seat_id="seat",
                attempt_id="attempt",
                operation_id="operation",
            )

    def test_failed_scout_can_be_terminated_and_unblocks_close_guard(self) -> None:
        started = self._start()
        terminated = self.service.terminate_reference_scout(
            token=started["issued_capabilities_once"]["terminator"]["token"],
            scout_run_id=started["scout_run"]["scout_run_id"],
            outcome="failed",
            reason="provider execution failed",
        )
        self.assertEqual(terminated["scout_run"]["state"], "failed")
        guard = self.service.require_orchestration_dispatch_can_close(
            session_id=self.session_id,
            dispatch_id=DISPATCH_ID,
            actor_ref="host:test",
            authorization_evidence_ref="evidence:test",
            authorization_evidence_digest="sha256:" + "c" * 64,
        )
        self.assertEqual(guard["current_version"], 1)

    def test_exact_start_retry_reissues_lost_run_capabilities(self) -> None:
        first = self._start()
        retry = self._start()
        self.assertEqual(
            first["scout_run"]["scout_run_id"],
            retry["scout_run"]["scout_run_id"],
        )
        self.assertTrue(retry["capabilities_reissued"])
        self.assertNotEqual(
            first["issued_capabilities_once"]["agent"]["token"],
            retry["issued_capabilities_once"]["agent"]["token"],
        )

    def _ingestion_intent(self, **changes) -> dict:
        intent = {
            "agent_id": "agent-1",
            "tool_use_id": "read-1",
            "tool_name": "Read",
            "source_kind": "repository_file",
            "locator": "docs/input.md",
            "repo_relative_path": "docs/input.md",
            "media_type": "text/markdown",
            "coverage": "exact",
            "purpose": "Input observed by test.",
            "observed_at": "2026-07-24T16:00:00+00:00",
        }
        intent.update(changes)
        return intent

    def _ingestion_token(self, intent: dict) -> str:
        return self.service.issue_capability(
            principal_id="host:test",
            action="ingestion.record",
            phase="observe",
            context={
                "session_id": self.session_id,
                "dispatch_id": DISPATCH_ID,
                "host": "codex",
                "tool_use_id": intent["tool_use_id"],
                "intent_digest": canonical_digest(intent),
            },
        )["token"]

    def test_exact_and_opaque_ingestion_are_dispatch_queryable(self) -> None:
        exact = self._ingestion_intent()
        receipt = self.service.record_dispatch_ingestion(
            token=self._ingestion_token(exact),
            intent=exact,
            content=b"# captured input\n",
        )
        retry = self.service.record_dispatch_ingestion(
            token=self._ingestion_token(exact),
            intent=exact,
            content=b"# captured input\n",
        )
        self.assertEqual(
            receipt["ingestion"]["ingestion_id"],
            retry["ingestion"]["ingestion_id"],
        )
        opaque = self._ingestion_intent(
            tool_use_id="shell-1",
            tool_name="shell_command",
            source_kind="shell_opaque",
            locator="shell:" + "a" * 64,
            repo_relative_path=None,
            media_type=None,
            coverage="opaque",
        )
        self.service.record_dispatch_ingestion(
            token=self._ingestion_token(opaque), intent=opaque
        )
        lineage = self.service.get_dispatch_operational_lineage(DISPATCH_ID)
        self.assertEqual(len(lineage["ingestions"]), 2)
        self.assertEqual(
            [item["coverage"] for item in lineage["ingestions"]],
            ["exact", "opaque"],
        )
        self.assertEqual(len(lineage["scout_runs"]), 0)

    def test_ingestion_rejects_changed_content_and_closed_dispatch(self) -> None:
        exact = self._ingestion_intent()
        token = self._ingestion_token(exact)
        self.service.record_dispatch_ingestion(
            token=token, intent=exact, content=b"first"
        )
        with self.assertRaises(Exception):
            self.service.record_dispatch_ingestion(
                token=token, intent=exact, content=b"changed"
            )
        with self.service.database.write() as conn:
            conn.execute(
                """
                UPDATE aggregate_heads SET current_version=2
                WHERE aggregate_id=?
                """,
                (f"aci.orchestration-dispatch:{DISPATCH_ID}",),
            )
        later = self._ingestion_intent(tool_use_id="read-after-close")
        with self.assertRaises(ConflictError):
            self.service.record_dispatch_ingestion(
                token=self._ingestion_token(later),
                intent=later,
                content=b"late",
            )


if __name__ == "__main__":
    unittest.main()
