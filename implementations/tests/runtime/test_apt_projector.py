from __future__ import annotations

import json
import unittest

from implementations.server.runtime.canonical import canonical_digest
from implementations.server.runtime.projections import ProjectionLagError
from implementations.server.runtime.provenance import ProvenanceService
from implementations.tests.runtime.test_apt_stage_b import (
    AptResearchEndToEndTests,
    DISPATCH_ID,
)


class AptIndependentProjectorTests(AptResearchEndToEndTests):
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
        with self.assertRaises(ProjectionLagError):
            provenance.get_research(
                token=self.token("projection.read", "observe", scope),
                capture_id=receipt["research_capture_id"],
            )

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
                            if row["projection_name"] == "apt.research-record"
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
