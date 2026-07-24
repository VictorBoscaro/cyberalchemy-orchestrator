from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from implementations.server.runtime.api import create_provenance_router
from implementations.server.runtime.canonical import canonical_digest
from implementations.server.runtime.projections import ProjectionLagError
from implementations.server.runtime.provenance import ProvenanceService
from implementations.server.runtime.service import RuntimeService, RuntimeSettings
from implementations.tests.runtime.test_apt_stage_b import (
    DISPATCH_ID,
    GOLDEN_LEDGER,
    REPO,
)


class AptIndependentProjectorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.ledger = self.root / "ledger.yaml"
        shutil.copyfile(GOLDEN_LEDGER, self.ledger)
        self.settings = RuntimeSettings(self.root / "runtime.db", REPO, self.ledger)
        self.runtime = RuntimeService(self.settings)
        self.runtime.open()
        self.runtime.register_profiles()
        self.session_id = self.runtime.ensure_session(
            origin_digest="sha256:" + "7" * 64,
            name="APT projector",
            actor_ref="apt-projector",
            actor_authentication_ref="test-auth:projector",
            actor_authentication_digest="sha256:" + "2" * 64,
        )["session"]["session_id"]
        self.runtime.link_session_dispatch(
            session_id=self.session_id,
            dispatch_id=DISPATCH_ID,
            actor_ref="apt-projector",
            authorization_policy_ref="test.link@1",
            authorization_policy_digest="sha256:" + "3" * 64,
            authorization_evidence_ref="test-evidence:projector-link",
            authorization_evidence_digest="sha256:" + "4" * 64,
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def token(self, action: str, phase: str, context: dict[str, str]) -> str:
        return self.runtime.issue_capability(
            principal_id="apt-projector",
            action=action,
            phase=phase,
            context=context,
        )["token"]

    def _intent(self, contribution: str) -> dict:
        return {
            "session_id": self.session_id,
            "expected_contribution_id": contribution,
            "question": "What survives a projector failure?",
            "final_answer": "The authoritative command receipt.",
            "references": [],
            "problems": [],
            "formalizations": [],
        }

    def test_authoritative_receipt_survives_projector_failure_and_catches_up(self):
        provenance = ProvenanceService(self.runtime)
        scope = {"session_id": self.session_id, "dispatch_id": DISPATCH_ID}
        original = self.runtime.projections.apply_apt_group

        def fail_projection(_conn, _events):
            raise RuntimeError("injected projector failure")

        self.runtime.projections.apply_apt_group = fail_projection
        receipt = provenance.append_research_submission(
            token=self.token("apt.append", "capture", scope),
            dispatch_id=DISPATCH_ID,
            idempotency_key="projector-failure",
            intent=self._intent("projector-failure"),
        )
        self.assertEqual(receipt["status"], "accepted")
        self.assertEqual(receipt["projection_status"], "pending")
        with self.runtime.database.connect() as conn:
            durable = conn.execute(
                "SELECT result_receipt_json FROM command_receipts WHERE command_id=?",
                (receipt["command_id"],),
            ).fetchone()
            projected = conn.execute(
                "SELECT count(*) FROM apt_research_captures_projection"
            ).fetchone()[0]
        self.assertIsNotNone(durable)
        self.assertEqual(json.loads(durable[0])["projection_status"], "pending")
        self.assertEqual(projected, 0)
        pending_state = self.runtime.projections.apt_state()
        self.assertGreaterEqual(
            pending_state["source_through_offset"], receipt["last_offset"]
        )
        self.assertLess(
            pending_state["apt_source_through_offset"], receipt["last_offset"]
        )
        self.assertFalse(pending_state["current"])
        with self.assertRaises(ProjectionLagError):
            provenance.get_research(
                token=self.token("projection.read", "observe", scope),
                capture_id=receipt["research_capture_id"],
            )
        with self.assertRaises(ProjectionLagError):
            provenance.get_answer(
                token=self.token(
                    "artifact.read",
                    "collect",
                    {
                        **scope,
                        "research_capture_id": receipt["research_capture_id"],
                    },
                ),
                capture_id=receipt["research_capture_id"],
            )
        with self.runtime.database.connect() as conn:
            conn.execute(
                """UPDATE apt_projection_state SET apt_source_through_offset=0
                   WHERE projection_name='apt.granular'"""
            )
            conn.commit()
        app = FastAPI()
        app.include_router(
            create_provenance_router(lambda: self.runtime, enabled=lambda: True)
        )
        client = TestClient(app)
        session_response = client.get(
            f"/api/provenance/sessions/{self.session_id}",
            headers={
                "Authorization": "Bearer "
                + self.token(
                    "session.read",
                    "observe",
                    {"session_id": self.session_id},
                )
            },
        )
        research_response = client.get(
            f"/api/provenance/research/{receipt['research_capture_id']}",
            headers={
                "Authorization": "Bearer "
                + self.token("projection.read", "observe", scope)
            },
        )
        answer_response = client.get(
            f"/api/provenance/research/{receipt['research_capture_id']}/answer",
            headers={
                "Authorization": "Bearer "
                + self.token(
                    "artifact.read",
                    "collect",
                    {
                        **scope,
                        "research_capture_id": receipt["research_capture_id"],
                    },
                )
            },
        )
        for response in (session_response, research_response, answer_response):
            self.assertEqual(response.status_code, 503)
            self.assertEqual(response.json()["detail"]["code"], "PROJECTION_LAG")
        with self.runtime.database.connect() as conn:
            conn.execute(
                """UPDATE apt_projection_state SET apt_source_through_offset=?
                   WHERE projection_name='apt.granular'""",
                (pending_state["apt_source_through_offset"],),
            )
            conn.commit()

        self.runtime.projections.apply_apt_group = original
        state = self.runtime.projections.catch_up_apt(self.runtime.journal)
        self.assertTrue(state["current"])
        self.assertGreaterEqual(
            state["apt_source_through_offset"], receipt["last_offset"]
        )
        projected = provenance.get_research(
            token=self.token("projection.read", "observe", scope),
            capture_id=receipt["research_capture_id"],
        )
        self.assertEqual(
            projected["questions"][0]["question_text"],
            self._intent("projector-failure")["question"],
        )

    def test_rebuild_from_zero_is_deterministic(self):
        provenance = ProvenanceService(self.runtime)
        scope = {"session_id": self.session_id, "dispatch_id": DISPATCH_ID}
        receipt = provenance.append_research_submission(
            token=self.token("apt.append", "capture", scope),
            dispatch_id=DISPATCH_ID,
            idempotency_key="projector-rebuild",
            intent=self._intent("projector-rebuild"),
        )
        self.assertEqual(receipt["projection_status"], "current")

        def snapshot() -> str:
            with self.runtime.database.connect() as conn:
                value = {}
                for table in (
                    "apt_research_captures_projection",
                    "apt_research_facts_projection",
                    "apt_research_questions_projection",
                    "apt_research_answers_projection",
                    "runtime_projections",
                ):
                    rows = [
                        dict(row)
                        for row in conn.execute(
                            f"SELECT * FROM {table} ORDER BY rowid"
                        ).fetchall()
                    ]
                    if table == "runtime_projections":
                        rows = [
                            row
                            for row in rows
                            if row["projection_name"]
                            in {
                                "apt.session-record",
                                "apt.dispatch-scope",
                                "apt.research-record",
                            }
                        ]
                    value[table] = rows
            return canonical_digest(value)

        before = snapshot()
        state = self.runtime.projections.rebuild_apt(self.runtime.journal)
        after = snapshot()
        self.assertTrue(state["current"])
        self.assertEqual(before, after)
        self.assertEqual(
            state["apt_source_through_offset"], state["source_through_offset"]
        )


if __name__ == "__main__":
    unittest.main()
