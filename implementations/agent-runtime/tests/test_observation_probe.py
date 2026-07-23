from __future__ import annotations

import sqlite3
import tempfile
import unittest
from pathlib import Path

from agent_runtime import CommandConflict, DomainConflict, InvalidCommand, Runtime


class ObservationProbeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.database = Path(self.temp.name) / "runtime.sqlite3"
        self.runtime = Runtime(self.database)
        self.runtime.ensure_session(
            "op-session",
            session_id="ses-1",
            ensure_key="probe-tests",
            origin_kind="test",
            origin_ref="opaque:probe-tests",
        )

    def tearDown(self) -> None:
        self.runtime.close()
        self.temp.cleanup()

    def start_probe(
        self,
        operation_id: str = "op-probe-start",
        *,
        probe_run_id: str = "probe-run-1",
        dispatch_id: str | None = None,
    ) -> dict:
        return self.runtime.start_observation_probe(
            operation_id,
            probe_run_id=probe_run_id,
            session_id="ses-1",
            dispatch_id=dispatch_id,
            target_ref="runtime:journal",
            question_ref="question:replay-integrity",
            lens_ref="lens:replay-integrity",
            lens_version="1",
            lens_digest="sha256:" + "a" * 64,
            observation_schema_ref="schema:replay-integrity@1",
        )

    def test_session_direct_probe_persists_normalized_observations_and_replays(self) -> None:
        started = self.start_probe()
        published = self.runtime.publish_probe_observation(
            "op-observe",
            observation_id="obs-1",
            probe_run_id="probe-run-1",
            observation_key="orphan_event_count",
            value=0,
            evidence_ref="receipt:verification-1",
            observed_by_seat_id="scientist:runtime",
        )
        self.runtime.commit_observation_probe(
            "op-probe-commit",
            probe_run_id="probe-run-1",
            observations_digest="sha256:" + "b" * 64,
        )
        self.runtime.deliver_observation_probe(
            "op-probe-deliver", probe_run_id="probe-run-1"
        )

        self.assertEqual(started["result"]["launch_mode"], "session_direct")
        self.assertEqual(published["result"]["observation_key"], "orphan_event_count")
        before_runs = self.runtime.projection("observation_probe_runs")
        before_observations = self.runtime.projection("probe_observations")
        self.assertEqual(before_runs[0]["state"], "delivered")
        self.assertEqual(before_observations[0]["value_json"], "0")

        counts = self.runtime.replay()
        self.assertEqual(self.runtime.projection("observation_probe_runs"), before_runs)
        self.assertEqual(self.runtime.projection("probe_observations"), before_observations)
        self.assertEqual(counts["observation_probe_runs"], 1)
        self.assertEqual(counts["probe_observations"], 1)

    def test_dispatch_bound_probe_requires_link_in_same_session(self) -> None:
        with self.assertRaises(DomainConflict):
            self.start_probe(dispatch_id="dispatch-1")
        self.runtime.link_session_dispatch(
            "op-link",
            session_dispatch_link_id="link-1",
            session_id="ses-1",
            dispatch_id="dispatch-1",
        )
        receipt = self.start_probe(
            "op-dispatch-probe",
            probe_run_id="probe-run-dispatch",
            dispatch_id="dispatch-1",
        )
        self.assertEqual(receipt["result"]["launch_mode"], "dispatch_bound")

    def test_probe_operation_is_idempotent_and_conflicting_retry_is_rejected(self) -> None:
        first = self.start_probe()
        retry = self.start_probe()
        self.assertEqual(retry["receipt_id"], first["receipt_id"])
        self.assertTrue(retry["replayed"])
        with self.assertRaises(CommandConflict):
            self.runtime.start_observation_probe(
                "op-probe-start",
                probe_run_id="probe-run-1",
                session_id="ses-1",
                dispatch_id=None,
                target_ref="runtime:different",
                question_ref="question:replay-integrity",
                lens_ref="lens:replay-integrity",
                lens_version="1",
                lens_digest="sha256:" + "a" * 64,
                observation_schema_ref="schema:replay-integrity@1",
            )

    def test_probe_and_legacy_scout_alias_are_separate_namespaces(self) -> None:
        self.runtime.start_reference_scout(
            "op-scout",
            scout_run_id="scout-1",
            probe_id="shared-id",
            session_id="ses-1",
            dispatch_id=None,
            objective_ref="artifact:references",
            shape="small",
            source_mode="internal",
            protocol_profile_id="apt-reference-scout-lineage",
            protocol_profile_version="1",
            protocol_profile_digest="sha256:profile",
        )
        self.start_probe(probe_run_id="shared-id")

        scout_event, probe_event = self.runtime.projection("journal_events")[-2:]
        self.assertEqual(scout_event["event_type"], "probe.requested")
        self.assertEqual(probe_event["event_type"], "observation_probe.requested")
        self.assertEqual(len(self.runtime.projection("reference_scout_runs")), 1)
        self.assertEqual(len(self.runtime.projection("observation_probe_runs")), 1)

    def test_lens_contract_is_required_and_observation_does_not_promote_fact(self) -> None:
        with self.assertRaises(InvalidCommand):
            self.runtime.start_observation_probe(
                "op-invalid",
                probe_run_id="probe-invalid",
                session_id="ses-1",
                dispatch_id=None,
                target_ref="runtime:journal",
                question_ref="question:integrity",
                lens_ref="lens:integrity",
                lens_version="1",
                lens_digest="",
                observation_schema_ref="schema:integrity@1",
            )
        self.assertEqual(self.runtime.projection("observation_probe_runs"), [])
        connection = sqlite3.connect(self.database)
        try:
            table_names = {
                row[0]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table'"
                )
            }
        finally:
            connection.close()
        self.assertNotIn("facts", table_names)
        self.assertNotIn("probe_facts", table_names)

    def test_probe_rejects_malformed_lens_and_observation_digests(self) -> None:
        with self.assertRaises(InvalidCommand):
            self.runtime.start_observation_probe(
                "op-bad-lens-digest",
                probe_run_id="probe-bad-lens-digest",
                session_id="ses-1",
                dispatch_id=None,
                target_ref="artifact:target",
                question_ref="question:one",
                lens_ref="lens:one",
                lens_version="1",
                lens_digest="sha256:",
                observation_schema_ref="schema:observation@1",
            )

        self.start_probe()
        with self.assertRaises(InvalidCommand):
            self.runtime.commit_observation_probe(
                "op-bad-observations-digest",
                probe_run_id="probe-run-1",
                observations_digest="sha256:",
            )

    def test_probe_state_machine_rejects_observation_after_commit(self) -> None:
        self.start_probe()
        self.runtime.commit_observation_probe(
            "op-commit-empty",
            probe_run_id="probe-run-1",
            observations_digest="sha256:" + "b" * 64,
        )
        with self.assertRaises(DomainConflict):
            self.runtime.publish_probe_observation(
                "op-late-observation",
                observation_id="obs-late",
                probe_run_id="probe-run-1",
                observation_key="late",
                value=True,
                observed_by_seat_id="scientist:runtime",
            )

    def test_schema_migration_three_is_recorded(self) -> None:
        connection = sqlite3.connect(self.database)
        try:
            versions = {
                row[0] for row in connection.execute("SELECT version FROM schema_migrations")
            }
        finally:
            connection.close()
        self.assertEqual(versions, {1, 2, 3})

    def test_existing_version_two_database_upgrades_additively(self) -> None:
        self.runtime.close()
        connection = sqlite3.connect(self.database)
        try:
            connection.execute("DROP TABLE probe_observations")
            connection.execute("DROP TABLE observation_probe_runs")
            connection.execute("DELETE FROM schema_migrations WHERE version = 3")
            connection.commit()
        finally:
            connection.close()

        self.runtime = Runtime(self.database)

        self.assertEqual(self.runtime.projection("observation_probe_runs"), [])
        connection = sqlite3.connect(self.database)
        try:
            migrated = connection.execute(
                "SELECT 1 FROM schema_migrations WHERE version = 3"
            ).fetchone()
            session_count = connection.execute(
                "SELECT COUNT(*) FROM sessions"
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertIsNotNone(migrated)
        self.assertEqual(session_count, 1)


if __name__ == "__main__":
    unittest.main()
