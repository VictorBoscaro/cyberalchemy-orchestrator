from __future__ import annotations

import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from agent_runtime import CommandConflict, DomainConflict, InvalidCommand, Runtime


class RuntimeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.database = Path(self.temp.name) / "runtime.sqlite3"
        self.runtime = Runtime(self.database)

    def tearDown(self) -> None:
        self.runtime.close()
        self.temp.cleanup()

    def ensure_session(self, operation_id: str = "op-session") -> dict:
        return self.runtime.ensure_session(
            operation_id,
            session_id="ses-1",
            ensure_key="host:conversation-opaque-7",
            origin_kind="codex",
            origin_ref="conversation:opaque-7",
            initial_name="Telemetry slice",
        )

    def start_scout(self, operation_id: str = "op-scout") -> dict:
        return self.runtime.start_reference_scout(
            operation_id,
            scout_run_id="scout-1",
            probe_id="probe-1",
            session_id="ses-1",
            dispatch_id="dispatch-1",
            objective_ref="artifact:objective-sha256",
            shape="small",
            source_mode="internal",
            protocol_profile_id="apt-reference-scout-lineage",
            protocol_profile_version="1",
            protocol_profile_digest="sha256:profile",
        )

    def happy_path(self) -> list[dict]:
        receipts = [self.ensure_session()]
        receipts.append(
            self.runtime.link_session_dispatch(
                "op-link",
                session_dispatch_link_id="link-1",
                session_id="ses-1",
                dispatch_id="dispatch-1",
            )
        )
        receipts.append(self.start_scout())
        receipts.append(
            self.runtime.publish_scout_contribution(
                "op-publish",
                recommendation_id="rec-1",
                scout_run_id="scout-1",
                probe_id="probe-1",
                reference_id="ref-1",
                source_class="repository",
                locator_observed="repo:path#symbol",
                access_state="observed",
                found_by_seat_id="worker-1",
                evaluated_by_seat_id="reviewer-1",
                evaluation="inspect",
                why_inspect="Contains the relevant contract.",
                comparability_state="incommensurable",
            )
        )
        receipts.append(
            self.runtime.commit_reference_bundle(
                "op-commit",
                scout_run_id="scout-1",
                probe_id="probe-1",
                bundle_digest="sha256:bundle",
            )
        )
        receipts.append(
            self.runtime.deliver_reference_bundle(
                "op-deliver",
                scout_run_id="scout-1",
                probe_id="probe-1",
            )
        )
        return receipts

    def test_happy_path_persists_receipts_and_explicit_comparability(self) -> None:
        receipts = self.happy_path()

        self.assertEqual([receipt["committed_seq"] for receipt in receipts], list(range(1, 7)))
        self.assertTrue(all(not receipt["replayed"] for receipt in receipts))
        for receipt in receipts:
            verified = self.runtime.verify_receipt(receipt["receipt_id"])
            self.assertTrue(verified["verified"])
        run = self.runtime.projection("reference_scout_runs")[0]
        recommendation = self.runtime.projection("reference_recommendations")[0]
        self.assertEqual(run["state"], "delivered")
        self.assertEqual(run["bundle_digest"], "sha256:bundle")
        self.assertEqual(recommendation["comparability_state"], "incommensurable")

    def test_same_operation_and_payload_returns_original_receipt(self) -> None:
        first = self.ensure_session()
        second = self.ensure_session()

        self.assertEqual(first["receipt_id"], second["receipt_id"])
        self.assertFalse(first["replayed"])
        self.assertTrue(second["replayed"])
        self.assertEqual(len(self.runtime.projection("journal_events")), 1)
        self.assertEqual(len(self.runtime.projection("command_receipts")), 1)

    def test_same_ensure_identity_new_operation_does_not_duplicate_start_fact(self) -> None:
        self.ensure_session()
        second = self.ensure_session("op-session-semantic-reuse")
        events = self.runtime.projection("journal_events")
        self.assertEqual(
            [event["event_type"] for event in events],
            ["session.started", "session.ensure_reused"],
        )
        self.assertEqual(second["result"]["session_id"], "ses-1")
        self.assertEqual(len(self.runtime.projection("sessions")), 1)

    def test_operation_reuse_with_changed_payload_conflicts(self) -> None:
        self.ensure_session()
        with self.assertRaises(CommandConflict):
            self.runtime.ensure_session(
                "op-session",
                session_id="ses-2",
                ensure_key="other",
                origin_kind="codex",
                origin_ref="conversation:other",
            )
        self.assertEqual(len(self.runtime.projection("journal_events")), 1)

    def test_failed_projection_rolls_back_event_and_receipt_atomically(self) -> None:
        with self.assertRaises(DomainConflict):
            self.runtime.link_session_dispatch(
                "op-invalid-link",
                session_dispatch_link_id="link-1",
                session_id="missing",
                dispatch_id="dispatch-1",
            )

        self.assertEqual(self.runtime.projection("journal_events"), [])
        self.assertEqual(self.runtime.projection("command_receipts"), [])
        self.assertEqual(self.runtime.projection("session_dispatch_links"), [])

    def test_replay_rebuilds_identical_domain_projections(self) -> None:
        self.happy_path()
        tables = (
            "sessions",
            "session_dispatch_links",
            "reference_scout_runs",
            "reference_recommendations",
        )
        before = {table: self.runtime.projection(table) for table in tables}

        counts = self.runtime.replay()
        after = {table: self.runtime.projection(table) for table in tables}

        self.assertEqual(after, before)
        self.assertEqual(counts["sessions"], 1)
        self.assertEqual(counts["reference_recommendations"], 1)
        self.assertEqual(len(self.runtime.projection("command_receipts")), 6)

    def test_replay_detects_tampered_journal_and_rolls_back(self) -> None:
        self.happy_path()
        before = self.runtime.projection("sessions")
        connection = sqlite3.connect(self.database)
        try:
            connection.execute(
                "UPDATE journal_events SET payload_json = ? WHERE seq = 1",
                (json.dumps({"session_id": "tampered"}),),
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaises(DomainConflict):
            self.runtime.replay()
        self.assertEqual(self.runtime.projection("sessions"), before)

    def test_raw_conversation_and_privileged_residue_metric_are_rejected(self) -> None:
        forbidden_payloads = [
            {"transcript": "secret"},
            {"metadata": {"messages": [{"content": "secret"}]}},
            {"residue_score": 0.4},
            {"prompt": "secret"},
        ]
        for index, extra in enumerate(forbidden_payloads):
            payload = {
                "session_id": f"ses-{index}",
                "ensure_key": f"key-{index}",
                "origin_kind": "codex",
                "origin_ref": f"opaque-{index}",
                **extra,
            }
            with self.subTest(extra=extra), self.assertRaises(InvalidCommand):
                self.runtime.ensure_session(f"op-{index}", **payload)
        self.assertEqual(self.runtime.projection("journal_events"), [])

    def test_session_is_not_conversation_and_schema_has_no_transcript_column(self) -> None:
        self.ensure_session()
        connection = sqlite3.connect(self.database)
        try:
            columns = {
                row[1] for row in connection.execute("PRAGMA table_info(sessions)").fetchall()
            }
        finally:
            connection.close()
        self.assertIn("origin_ref", columns)
        self.assertNotIn("conversation_id", columns)
        self.assertFalse(any("transcript" in column for column in columns))

    def test_state_machine_prevents_publish_after_commit_and_deliver_before_commit(self) -> None:
        self.ensure_session()
        self.runtime.link_session_dispatch(
            "op-link",
            session_dispatch_link_id="link-1",
            session_id="ses-1",
            dispatch_id="dispatch-1",
        )
        self.start_scout()
        with self.assertRaises(DomainConflict):
            self.runtime.deliver_reference_bundle(
                "op-early-deliver", scout_run_id="scout-1", probe_id="probe-1"
            )
        self.runtime.commit_reference_bundle(
            "op-commit", scout_run_id="scout-1", probe_id="probe-1",
            bundle_digest="sha256:empty"
        )
        with self.assertRaises(DomainConflict):
            self.runtime.publish_scout_contribution(
                "op-late-publish",
                recommendation_id="rec-late",
                scout_run_id="scout-1",
                probe_id="probe-1",
                reference_id="ref-late",
                source_class="repository",
                locator_observed="repo:path",
                access_state="observed",
                found_by_seat_id="worker",
                why_inspect="late",
            )
        self.assertEqual(len(self.runtime.projection("journal_events")), 4)

    def test_logical_dispatch_cannot_link_to_two_sessions(self) -> None:
        self.ensure_session()
        self.runtime.ensure_session(
            "op-session-2",
            session_id="ses-2",
            ensure_key="host:other",
            origin_kind="codex",
            origin_ref="conversation:other",
        )
        self.runtime.link_session_dispatch(
            "op-link-1",
            session_dispatch_link_id="link-1",
            session_id="ses-1",
            dispatch_id="dispatch-shared",
        )
        with self.assertRaises(DomainConflict):
            self.runtime.link_session_dispatch(
                "op-link-2",
                session_dispatch_link_id="link-2",
                session_id="ses-2",
                dispatch_id="dispatch-shared",
            )
        self.assertEqual(len(self.runtime.projection("session_dispatch_links")), 1)

    def test_scout_rejects_unlinked_or_cross_session_dispatch(self) -> None:
        self.ensure_session()
        with self.assertRaises(DomainConflict):
            self.runtime.start_reference_scout(
                "op-unlinked",
                scout_run_id="scout-unlinked",
                probe_id="probe-unlinked",
                session_id="ses-1",
                dispatch_id="not-linked",
                objective_ref="artifact:objective",
                shape="small",
                source_mode="internal",
                protocol_profile_id="apt.reference-probe-lineage",
                protocol_profile_version="1",
                protocol_profile_digest="sha256:profile",
            )
        self.assertEqual(len(self.runtime.projection("journal_events")), 1)

    def test_restart_preserves_idempotency_and_projections(self) -> None:
        first = self.ensure_session()
        self.runtime.close()
        self.runtime = Runtime(self.database)
        retry = self.ensure_session()
        self.assertEqual(retry["receipt_id"], first["receipt_id"])
        self.assertTrue(retry["replayed"])
        self.assertEqual(self.runtime.projection("sessions")[0]["start_operation_id"], "op-session")

    def test_structured_logs_are_allowlisted_and_never_contain_payload(self) -> None:
        self.runtime.close()
        records: list[dict] = []
        self.runtime = Runtime(self.database, log_sink=records.append)
        receipt = self.ensure_session()
        self.runtime.link_session_dispatch(
            "op-link",
            session_dispatch_link_id="link-1",
            session_id="ses-1",
            dispatch_id="dispatch-1",
        )
        self.start_scout()

        self.assertEqual(records[0]["operation_id"], receipt["operation_id"])
        self.assertEqual(records[0]["event_id"], receipt["event_id"])
        self.assertEqual(records[0]["receipt_id"], receipt["receipt_id"])
        self.assertEqual(records[2]["session_id"], "ses-1")
        self.assertEqual(records[2]["scout_run_id"], "scout-1")
        encoded = json.dumps(records)
        self.assertNotIn("conversation:opaque-7", encoded)
        self.assertNotIn("objective-sha256", encoded)
        self.assertEqual(
            set(records[0]),
            {
                "operation_id",
                "event_id",
                "receipt_id",
                "event_type",
                "journal_offset",
                "session_id",
                "dispatch_id",
                "scout_run_id",
                "state",
                "outcome",
                "error_code",
            },
        )

    def test_both_noncomparability_states_survive_replay(self) -> None:
        self.ensure_session()
        self.runtime.link_session_dispatch(
            "op-link",
            session_dispatch_link_id="link-1",
            session_id="ses-1",
            dispatch_id="dispatch-1",
        )
        self.start_scout()
        for suffix, state in (("a", "incommensurable"), ("b", "count_capped")):
            self.runtime.publish_scout_contribution(
                f"op-publish-{suffix}",
                recommendation_id=f"rec-{suffix}",
                scout_run_id="scout-1",
                probe_id="probe-1",
                reference_id=f"ref-{suffix}",
                source_class="repository",
                locator_observed=f"repo:path:{suffix}",
                access_state="observed",
                found_by_seat_id="worker",
                why_inspect="bounded navigation reason",
                comparability_state=state,
            )
        self.runtime.replay()
        states = {
            row["comparability_state"]
            for row in self.runtime.projection("reference_recommendations")
        }
        self.assertEqual(states, {"incommensurable", "count_capped"})


if __name__ == "__main__":
    unittest.main()
