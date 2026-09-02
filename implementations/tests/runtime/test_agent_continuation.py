from __future__ import annotations

import json
import tempfile
import threading
import unittest
from pathlib import Path

from implementations.server.runtime.canonical import canonical_digest
from implementations.server.runtime.continuation import (
    CONTINUATION_EVENTS,
    CONTINUATION_STATES,
    derive_deadline_utc,
    reduce_continuation,
    require_exact_zero_official_facts,
)
from implementations.server.runtime.errors import (
    ContinuationAuthorityError,
    ContinuationMixedSourceState,
    ContinuationPrerequisiteError,
    IdempotencyConflict,
    InvalidContinuationTransition,
)
from implementations.server.runtime.service import RuntimeService, RuntimeSettings


REPO = Path(__file__).resolve().parents[3]
FIXTURE = (
    REPO
    / "docs/features/agents-communication-infra/specs/fixtures/confirmed-dispatch-v2"
)


class AgentContinuationTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.documents = {
            path.name: path.read_bytes()
            for path in FIXTURE.iterdir()
            if path.suffix == ".json"
        }
        trusted = json.loads(self.documents["trusted-issuer-context.json"])
        self.service = RuntimeService(
            RuntimeSettings(
                self.root / "runtime.sqlite3",
                REPO,
                self.root / "ledger.yaml",
                confirmation_issuer_ref=trusted["admitted_issuer_ref"],
                confirmation_host_context=trusted["authenticated_host_context"],
            )
        )
        self.service.open()
        preview = self.service.artifacts.prepare(
            self.documents["capability-resolution.json"],
            media_type="application/json",
            schema_ref="aci.capability-resolution@1",
            classification="runtime-internal",
        )
        self.service.artifacts.commit(preview)
        self.confirmation_receipt = self.service.confirm_runtime_dispatch(
            pending_sheet_bytes=self.documents["pending-sheet.json"],
            capability_resolution_bytes=self.documents["capability-resolution.json"],
            capability_resolution_artifact_id=preview.artifact_id,
            trusted_issuer_context_bytes=self.documents["trusted-issuer-context.json"],
            confirmation_observation_bytes=self.documents[
                "confirmation-observation.json"
            ],
            identity_derivation_bytes=self.documents["identity-derivation.json"],
            payload_schema_bundle_bytes=self.documents[
                "confirmation-payload-schemas.json"
            ],
            command_bytes=self.documents["confirmation-command.json"],
        )
        with self.service.database.connect() as conn:
            self.graph = dict(
                conn.execute("SELECT * FROM confirmed_turn_graphs").fetchone()
            )
        self._bind_test_attempt_events()
        self.source_attempt_id = "attempt_author_turn_0"
        self._accept_source_attempt_lifecycle()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _bind_test_attempt_events(self) -> None:
        bindings = dict(self.service.journal._schema_bindings)
        validators = dict(self.service.journal._payload_validators)
        for event_type in (
            "attempt.requested",
            "attempt.starting",
            "attempt.running",
            "attempt.completed",
            "test.publication.persisted",
            "test.publication.official",
        ):
            schema_ref = "aci." + event_type.replace(".", "-") + "@1"
            bindings[event_type] = (
                schema_ref,
                canonical_digest({"schema_ref": schema_ref}),
            )
            validators[event_type] = lambda payload: None
        self.service.journal.bind_event_schemas(bindings)
        self.service.journal.bind_payload_validators(validators)

    def _mapping(self, ordinal: int) -> dict:
        with self.service.database.connect() as conn:
            return dict(
                conn.execute(
                    """
                    SELECT * FROM continuation_input_mappings
                    WHERE continuation_id=? AND slot_ordinal=?
                    """,
                    (self.graph["continuation_id"], ordinal),
                ).fetchone()
            )

    def _accept_official_fact(self, ordinal: int) -> None:
        mapping = self._mapping(ordinal)
        message_id = mapping["source_message_id"]
        candidate_id = f"candidate_{ordinal}"
        aggregate_id = f"test.official-source:{message_id}"
        command = self.service._command(
            command_name="test.accept-official-source@1",
            scope_key=aggregate_id,
            idempotency_key="accept@1",
            aggregate_type="test.official-source",
            aggregate_id=aggregate_id,
            expected_version=0,
            authority={"principal_id": "test-continuation-harness"},
            intent={"message_id": message_id},
        )
        events = [
            self.service._event(
                "test.publication.persisted",
                {"message_id": message_id, "status": "candidate"},
                event_id=f"evt_test_candidate_{ordinal}",
            ),
            self.service._event(
                "test.publication.official",
                {"message_id": message_id, "status": "official"},
                event_id=f"evt_test_official_{ordinal}",
            ),
        ]

        def mutate(conn, records, _receipt):
            payload_hash = canonical_digest({"message_id": message_id})
            receipt_bytes = json.dumps(
                {"message_id": message_id}, separators=(",", ":")
            ).encode()
            conn.execute(
                """
                INSERT INTO publication_candidates(
                  candidate_id,message_id,publication_event_id,group_aggregate_id,
                  seat_id,round_id,message_type,attempt_id,operation_id,payload_ref,
                  payload_hash,idempotency_key,receipt_bytes,receipt_digest,
                  journal_offset,status,candidate_version,official_accepted_event_id,
                  abandoned_event_id
                ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    candidate_id,
                    message_id,
                    records[0].event_id,
                    mapping["source_group_id"],
                    mapping["source_seat_id"],
                    mapping["source_round_id"],
                    mapping["source_message_type"],
                    self.source_attempt_id if ordinal == 0 else "attempt_reviewer_0",
                    mapping["source_operation_id"],
                    f"test-payload-{ordinal}",
                    payload_hash,
                    "accept@1",
                    receipt_bytes,
                    canonical_digest({"receipt": message_id}),
                    records[0].journal_offset,
                    "officially_accepted",
                    1,
                    records[1].event_id,
                    None,
                ),
            )
            conn.execute(
                """
                INSERT INTO messages(
                  message_id,group_aggregate_id,seat_id,round_id,message_type,
                  payload_ref,payload_hash,source_candidate_id,official_event_id,
                  accepted_offset
                ) VALUES(?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    message_id,
                    mapping["source_group_id"],
                    mapping["source_seat_id"],
                    mapping["source_round_id"],
                    mapping["source_message_type"],
                    f"test-payload-{ordinal}",
                    payload_hash,
                    candidate_id,
                    records[1].event_id,
                    records[1].journal_offset,
                ),
            )

        self.service.journal.accept(
            command,
            events,
            next_state={"message_id": message_id, "state": "official"},
            mutate=mutate,
        )

    def _accept_source_attempt_lifecycle(self) -> None:
        aggregate_id = f"aci.agent-attempt:{self.source_attempt_id}"
        requested_event_id = "evt_test_attempt_requested"
        snapshot = None
        for version, (event_type, state) in enumerate(
            (
                ("attempt.requested", "requested"),
                ("attempt.starting", "starting"),
                ("attempt.running", "running"),
                ("attempt.completed", "completed"),
            ),
            start=1,
        ):
            event_id = f"evt_test_attempt_{state}"
            event = self.service._event(
                event_type,
                {
                    "attempt_id": self.source_attempt_id,
                    "state": state,
                    "version": version,
                },
                event_id=event_id,
            )
            command = self.service._command(
                command_name=f"test.accept-attempt-{state}@1",
                scope_key=aggregate_id,
                idempotency_key=f"{state}@1",
                aggregate_type="aci.agent-attempt",
                aggregate_id=aggregate_id,
                expected_version=version - 1,
                authority={"principal_id": "test-continuation-harness"},
                intent={"attempt_id": self.source_attempt_id, "state": state},
            )
            additional_artifacts = ()
            if state == "completed":
                snapshot = self.service.artifacts.prepare(
                    b'{"context":"author turn zero"}',
                    media_type="application/json",
                    schema_ref="test.reconstruction-snapshot@1",
                    classification="runtime-internal",
                    created_event_id=event_id,
                )
                additional_artifacts = (snapshot,)

            def mutate(conn, records, _receipt, current_state=state, current_version=version):
                record = records[0]
                if current_state == "requested":
                    conn.execute(
                        """
                        INSERT INTO runtime_agent_attempts(
                          attempt_id,dispatch_id,graph_id,aggregate_id,operation_id,
                          seat_id,agent_instance_id,turn_ordinal,state,version,
                          requested_event_id,last_event_id,last_offset
                        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
                        """,
                        (
                            self.source_attempt_id,
                            self.graph["dispatch_id"],
                            self.graph["graph_id"],
                            aggregate_id,
                            self.graph["source_operation_id"],
                            self.graph["source_seat_id"],
                            "agent_instance_author_0",
                            self.graph["source_turn_ordinal"],
                            current_state,
                            current_version,
                            requested_event_id,
                            record.event_id,
                            record.journal_offset,
                        ),
                    )
                else:
                    changed = conn.execute(
                        """
                        UPDATE runtime_agent_attempts
                        SET state=?,version=?,last_event_id=?,last_offset=?
                        WHERE attempt_id=? AND version=?
                        """,
                        (
                            current_state,
                            current_version,
                            record.event_id,
                            record.journal_offset,
                            self.source_attempt_id,
                            current_version - 1,
                        ),
                    )
                    self.assertEqual(changed.rowcount, 1)
                if current_state == "completed":
                    assert snapshot is not None
                    conn.execute(
                        """
                        INSERT INTO runtime_attempt_snapshot_bindings(
                          attempt_id,artifact_id,content_hash,terminal_event_id,
                          terminal_offset,bound_at
                        ) VALUES(?,?,?,?,?,?)
                        """,
                        (
                            self.source_attempt_id,
                            snapshot.artifact_id,
                            snapshot.content_hash,
                            record.event_id,
                            record.journal_offset,
                            snapshot.finalized_at,
                        ),
                    )

            self.service.journal.accept(
                command,
                [event],
                next_state={"attempt_id": self.source_attempt_id, "state": state},
                additional_artifacts=additional_artifacts,
                mutate=mutate,
            )

    def _suspend(self, **overrides):
        kwargs = {
            "dispatch_id": self.graph["dispatch_id"],
            "continuation_id": self.graph["continuation_id"],
        }
        kwargs.update(overrides)
        return self.service.suspend_agent_continuation(**kwargs)

    def _durable_surface(self) -> dict[str, list[tuple]]:
        tables = (
            "agent_continuations",
            "agent_continuation_mapping_members",
            "events",
            "aggregate_heads",
            "command_receipts",
            "artifacts",
            "effect_intents",
            "sandbox_launch_effects",
            "agent_attempts",
            "runtime_agent_attempts",
            "runtime_attempt_snapshot_bindings",
        )
        with self.service.database.connect() as conn:
            return {
                table: [
                    tuple(row)
                    for row in conn.execute(f"SELECT * FROM {table} ORDER BY rowid")
                ]
                for table in tables
            }

    def _assert_one_suspension_unit(self) -> None:
        aggregate_id = f"aci.agent-continuation:{self.graph['continuation_id']}"
        with self.service.database.connect() as conn:
            self.assertEqual(
                conn.execute("SELECT COUNT(*) FROM agent_continuations").fetchone()[0],
                1,
            )
            self.assertEqual(
                conn.execute(
                    "SELECT COUNT(*) FROM agent_continuation_mapping_members"
                ).fetchone()[0],
                2,
            )
            self.assertEqual(
                conn.execute(
                    "SELECT COUNT(*) FROM events WHERE aggregate_id=?",
                    (aggregate_id,),
                ).fetchone()[0],
                1,
            )
            self.assertEqual(
                conn.execute(
                    "SELECT COUNT(*) FROM aggregate_heads WHERE aggregate_id=?",
                    (aggregate_id,),
                ).fetchone()[0],
                1,
            )
            self.assertEqual(
                conn.execute(
                    "SELECT COUNT(*) FROM command_receipts WHERE scope_key=?",
                    (aggregate_id,),
                ).fetchone()[0],
                1,
            )

    def test_cont1_effect_free_suspension_replay_and_reopen(self) -> None:
        with self.service.database.connect() as conn:
            effect_before = conn.execute("SELECT COUNT(*) FROM effect_intents").fetchone()[0]
            sandbox_before = conn.execute(
                "SELECT COUNT(*) FROM sandbox_launch_effects"
            ).fetchone()[0]
        first = self._suspend()
        self.assertEqual(first["state"], "suspended")
        self.assertEqual(first["continuation_id"], self.graph["continuation_id"])
        self.assertEqual(len(first["ordered_input_mapping_ids"]), 2)
        self.assertEqual(
            first["ordered_awaited_mapping_ids"],
            first["ordered_input_mapping_ids"],
        )
        self.assertEqual(first, self._suspend())
        with self.service.database.connect() as conn:
            continuation = dict(
                conn.execute("SELECT * FROM agent_continuations").fetchone()
            )
            members = conn.execute(
                """
                SELECT * FROM agent_continuation_mapping_members
                ORDER BY member_ordinal
                """
            ).fetchall()
            self.assertEqual(continuation["state"], "suspended")
            self.assertEqual(len(members), 2)
            self.assertEqual(
                conn.execute("SELECT COUNT(*) FROM effect_intents").fetchone()[0],
                effect_before,
            )
            self.assertEqual(
                conn.execute("SELECT COUNT(*) FROM sandbox_launch_effects").fetchone()[0],
                sandbox_before,
            )
        reopened = RuntimeService(self.service.settings)
        reopened.open()
        self.assertEqual(
            reopened.suspend_agent_continuation(
                dispatch_id=self.graph["dispatch_id"],
                continuation_id=self.graph["continuation_id"],
            ),
            first,
        )

    def test_deadline_is_confirmation_relative_utc(self) -> None:
        self.assertEqual(
            derive_deadline_utc("2026-08-31T20:06:00.000Z", 900),
            "2026-08-31T20:21:00+00:00",
        )
        for timestamp in (
            "2026-08-31T20:06:00",
            "2026-08-31T17:06:00-03:00",
            "not-a-timestamp",
        ):
            with self.subTest(timestamp=timestamp):
                with self.assertRaises(Exception):
                    derive_deadline_utc(timestamp, 900)
        with self.assertRaises(Exception):
            derive_deadline_utc("9999-12-31T23:59:59Z", 900)

    def test_create_rechecks_official_facts_and_replay_precedes_new_facts(self) -> None:
        injected = False

        def inject(name: str) -> None:
            nonlocal injected
            if name == "continuation.after_official_precheck" and not injected:
                injected = True
                self._accept_official_fact(1)

        with self.assertRaises(ContinuationMixedSourceState):
            self._suspend(failpoint=inject)
        with self.service.database.connect() as conn:
            self.assertEqual(
                conn.execute("SELECT COUNT(*) FROM agent_continuations").fetchone()[0],
                0,
            )
            self.assertEqual(
                conn.execute(
                    "SELECT COUNT(*) FROM events WHERE event_type='continuation.suspended'"
                ).fetchone()[0],
                0,
            )

        self.tearDown()
        self.setUp()
        first = self._suspend()
        self._accept_official_fact(1)
        self.assertEqual(self._suspend(), first)
        with self.assertRaises(IdempotencyConflict):
            self._suspend(provider_continuation_ref_digest="sha256:" + "a" * 64)

    def test_replay_uses_persisted_projection_after_confirmed_mapping_drift(self) -> None:
        first = self._suspend()
        with self.service.database.connect() as conn:
            conn.execute(
                """
                UPDATE continuation_input_mappings
                SET target_seat_id=? WHERE continuation_id=?
                """,
                ("seat_after_commit_drift", self.graph["continuation_id"]),
            )
        self.assertEqual(self._suspend(), first)
        with self.assertRaises(IdempotencyConflict):
            self._suspend(provider_continuation_ref_digest="sha256:" + "a" * 64)

    def test_authority_and_snapshot_races_fail_typed_without_writer_changes(self) -> None:
        def update_attempt(conn, assignments: str, values: tuple) -> None:
            conn.execute(
                f"UPDATE runtime_agent_attempts SET {assignments} WHERE attempt_id=?",
                (*values, self.source_attempt_id),
            )

        cases = (
            (
                "agent-instance",
                lambda conn: update_attempt(
                    conn, "agent_instance_id=?", ("agent_instance_drift",)
                ),
            ),
            (
                "seat",
                lambda conn: update_attempt(conn, "seat_id=?", ("seat_drift",)),
            ),
            (
                "turn",
                lambda conn: update_attempt(conn, "turn_ordinal=?", (99,)),
            ),
            (
                "operation",
                lambda conn: update_attempt(
                    conn, "operation_id=?", ("operation_drift",)
                ),
            ),
            (
                "version",
                lambda conn: update_attempt(
                    conn, "state=?,version=?", ("running", 3)
                ),
            ),
            (
                "requested-event",
                lambda conn: update_attempt(
                    conn,
                    "requested_event_id=?",
                    ("evt_test_attempt_starting",),
                ),
            ),
            (
                "terminal-event-offset",
                lambda conn: update_attempt(
                    conn,
                    "last_event_id=?,last_offset=?",
                    (
                        "evt_test_attempt_running",
                        conn.execute(
                            "SELECT journal_offset FROM events WHERE event_id=?",
                            ("evt_test_attempt_running",),
                        ).fetchone()[0],
                    ),
                ),
            ),
            (
                "snapshot-terminal-link",
                lambda conn: conn.execute(
                    """
                    UPDATE runtime_attempt_snapshot_bindings
                    SET terminal_event_id=?,terminal_offset=? WHERE attempt_id=?
                    """,
                    (
                        "evt_test_attempt_running",
                        conn.execute(
                            "SELECT journal_offset FROM events WHERE event_id=?",
                            ("evt_test_attempt_running",),
                        ).fetchone()[0],
                        self.source_attempt_id,
                    ),
                ),
            ),
        )
        for index, (label, mutate_authority) in enumerate(cases):
            with self.subTest(label=label):
                if index:
                    self.tearDown()
                    self.setUp()
                post_injection_surface = None

                def inject(name: str) -> None:
                    nonlocal post_injection_surface
                    if name != "continuation.after_official_precheck":
                        return
                    with self.service.database.connect() as conn:
                        mutate_authority(conn)
                    post_injection_surface = self._durable_surface()

                with self.assertRaises(ContinuationPrerequisiteError):
                    self._suspend(failpoint=inject)
                self.assertIsNotNone(post_injection_surface)
                self.assertEqual(self._durable_surface(), post_injection_surface)

    def test_one_two_duplicate_and_ambiguous_official_states_fail_closed(self) -> None:
        for ordinal in (0, 1):
            self._accept_official_fact(ordinal)
            with self.assertRaises(ContinuationMixedSourceState):
                self._suspend()
        expected = ("message-author", "message-review")
        for facts in (
            [{"message_id": "message-author"}],
            [
                {"message_id": "message-author"},
                {"message_id": "message-author"},
            ],
            [{"message_id": "unexpected"}],
        ):
            with self.subTest(facts=facts):
                with self.assertRaises(ContinuationMixedSourceState):
                    require_exact_zero_official_facts(facts, expected)

    def test_migration_is_isolated_and_authority_substitutions_reject(self) -> None:
        expected_tables = {
            "runtime_agent_attempts",
            "runtime_attempt_snapshot_bindings",
            "agent_continuations",
            "agent_continuation_mapping_members",
        }
        with self.service.database.connect() as conn:
            tables = {
                row[0]
                for row in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
            }
            self.assertTrue(expected_tables <= tables)
            attempt_parents = {
                row["table"]
                for row in conn.execute(
                    "PRAGMA foreign_key_list(runtime_agent_attempts)"
                )
            }
            continuation_parents = {
                row["table"]
                for row in conn.execute(
                    "PRAGMA foreign_key_list(agent_continuations)"
                )
            }
            member_parents = {
                row["table"]
                for row in conn.execute(
                    "PRAGMA foreign_key_list(agent_continuation_mapping_members)"
                )
            }
        self.assertEqual(
            attempt_parents, {"confirmed_dispatches", "confirmed_turn_graphs", "events"}
        )
        self.assertTrue(
            {"confirmed_dispatches", "confirmed_turn_graphs", "runtime_agent_attempts"}
            <= continuation_parents
        )
        self.assertIn("continuation_input_mappings", member_parents)
        with self.assertRaises(ContinuationAuthorityError):
            self.service.suspend_agent_continuation(
                dispatch_id="legacy-dispatch",
                continuation_id=self.graph["continuation_id"],
            )
        with self.assertRaises(ContinuationAuthorityError):
            self.service.suspend_agent_continuation(
                dispatch_id=self.graph["dispatch_id"],
                continuation_id="cont_not_confirmed",
            )

    def test_every_suspension_failpoint_is_atomic_and_lost_response_replays(self) -> None:
        points = (
            "before_begin",
            "after_begin",
            "after_validation",
            "after_artifact",
            "after_event",
            "after_head",
            "continuation.after_continuation",
            "continuation.after_mapping_0",
            "continuation.after_mapping_1",
            "after_mutation",
            "after_receipt",
            "before_commit",
        )
        for point in points:
            with self.subTest(point=point):
                before = self._durable_surface()

                def fail(name: str, target=point) -> None:
                    if name == target:
                        raise RuntimeError(target)

                with self.assertRaisesRegex(RuntimeError, point):
                    self._suspend(failpoint=fail)
                self.assertEqual(self._durable_surface(), before)

        seen = False

        def lost_response(name: str) -> None:
            nonlocal seen
            if name == "after_commit" and not seen:
                seen = True
                raise RuntimeError("lost response")

        before_commit = self._durable_surface()
        with self.assertRaisesRegex(RuntimeError, "lost response"):
            self._suspend(failpoint=lost_response)
        committed = self._durable_surface()
        self.assertNotEqual(committed, before_commit)
        self._assert_one_suspension_unit()
        replay = self._suspend()
        with self.service.database.connect() as conn:
            persisted_receipt = json.loads(
                conn.execute(
                    """
                    SELECT result_receipt_json FROM command_receipts
                    WHERE scope_key=? AND idempotency_key='suspend@1'
                    """,
                    (f"aci.agent-continuation:{self.graph['continuation_id']}",),
                ).fetchone()[0]
            )
        self.assertEqual(replay, persisted_receipt)
        self.assertEqual(self._durable_surface(), committed)

    def test_concurrent_identical_and_divergent_suspensions_converge(self) -> None:
        def race(provider_digests: tuple[str | None, str | None]):
            barrier = threading.Barrier(2)
            results: list[dict] = []
            errors: list[Exception] = []

            def run(provider_digest: str | None) -> None:
                service = RuntimeService(self.service.settings)
                service.open()
                barrier.wait()
                try:
                    results.append(
                        service.suspend_agent_continuation(
                            dispatch_id=self.graph["dispatch_id"],
                            continuation_id=self.graph["continuation_id"],
                            provider_continuation_ref_digest=provider_digest,
                        )
                    )
                except Exception as exc:  # evidence collection for the race
                    errors.append(exc)

            threads = [
                threading.Thread(target=run, args=(provider_digest,))
                for provider_digest in provider_digests
            ]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
            return results, errors

        results, errors = race((None, None))
        self.assertEqual(errors, [])
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], results[1])
        self._assert_one_suspension_unit()

        self.tearDown()
        self.setUp()
        results, errors = race((None, "sha256:" + "a" * 64))
        self.assertEqual(len(results), 1)
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], IdempotencyConflict)
        self._assert_one_suspension_unit()

    def test_cont9_l2_base_reducer_rejects_every_unlisted_pair(self) -> None:
        admitted = {
            (None, "continuation.suspended"),
            ("suspended", "continuation.resume_requested"),
            ("resume_requested", "continuation.resuming"),
            ("resuming", "continuation.resumed"),
            ("resuming", "continuation.resume_unknown"),
            ("resume_unknown", "continuation.resumed"),
            ("suspended", "continuation.provider_lost"),
            ("resuming", "continuation.provider_lost"),
            ("resume_unknown", "continuation.provider_lost"),
            ("reconstruction_eligible", "continuation.reconstruction_requested"),
            ("suspended", "continuation.cancel_requested"),
            ("resume_requested", "continuation.cancel_requested"),
            ("resuming", "continuation.cancel_requested"),
            ("resume_unknown", "continuation.cancel_requested"),
            ("reconstruction_eligible", "continuation.cancel_requested"),
            ("cancel_requested", "continuation.cancelled"),
            ("suspended", "continuation.expired"),
            ("resume_requested", "continuation.expired"),
            ("reconstruction_eligible", "continuation.expired"),
        }
        for state in (None, *CONTINUATION_STATES):
            for event_type in CONTINUATION_EVENTS:
                with self.subTest(state=state, event_type=event_type):
                    if (state, event_type) in admitted:
                        self.assertIsInstance(
                            reduce_continuation(state, event_type), str
                        )
                    else:
                        with self.assertRaises(InvalidContinuationTransition):
                            reduce_continuation(state, event_type)


if __name__ == "__main__":
    unittest.main()
