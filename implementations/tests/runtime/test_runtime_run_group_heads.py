from __future__ import annotations

import json
import sqlite3
import tempfile
import threading
import unittest
from dataclasses import asdict
from pathlib import Path

from implementations.server.runtime.artifacts import ArtifactStore
from implementations.server.runtime.canonical import canonical_digest
from implementations.server.runtime.database import RuntimeDatabase
from implementations.server.runtime.errors import (
    IdempotencyConflict,
    InvalidGroupTransition,
    InvalidRunTransition,
    RunGroupFenceClosed,
    RunGroupGuardError,
    RunGroupHeadConflict,
)
from implementations.server.runtime.journal import EventDraft, RuntimeCommand, RuntimeJournal
from implementations.server.runtime.run_group import (
    GROUP_EVENTS,
    GROUP_STATES,
    RUN_EVENTS,
    RUN_STATES,
    GroupProjection,
    RunProjection,
    fixed_two_seat_decision,
    reduce_group,
    reduce_run,
    require_run_execution_eligible,
    run_execution_eligible,
)
from implementations.server.runtime.service import RuntimeService, RuntimeSettings


REPO = Path(__file__).resolve().parents[3]
FIXTURE = REPO / "docs/features/agents-communication-infra/specs/fixtures/confirmed-dispatch-v2"
HARNESS_EVENT = "test.run-group.harness-only-transition"
HARNESS_SCHEMA = "aci.test-run-group-harness-only-transition@1"
HARNESS_SCHEMA_DIGEST = canonical_digest({"schema_ref": HARNESS_SCHEMA})


class RuntimeRunGroupHeadsTests(unittest.TestCase):
    """Component evidence only; this harness is not an audit-opening materializer."""

    maxDiff = None

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        documents = {
            path.name: path.read_bytes()
            for path in FIXTURE.iterdir()
            if path.suffix == ".json"
        }
        trusted = json.loads(documents["trusted-issuer-context.json"])
        setup = RuntimeService(
            RuntimeSettings(
                self.root / "runtime.sqlite3",
                REPO,
                self.root / "ledger.yaml",
                confirmation_issuer_ref=trusted["admitted_issuer_ref"],
                confirmation_host_context=trusted["authenticated_host_context"],
            )
        )
        setup.open()
        preview = setup.artifacts.prepare(
            documents["capability-resolution.json"],
            media_type="application/json",
            schema_ref="aci.capability-resolution@1",
            classification="runtime-internal",
        )
        setup.artifacts.commit(preview)
        setup.confirm_runtime_dispatch(
            pending_sheet_bytes=documents["pending-sheet.json"],
            capability_resolution_bytes=documents["capability-resolution.json"],
            capability_resolution_artifact_id=preview.artifact_id,
            trusted_issuer_context_bytes=documents["trusted-issuer-context.json"],
            confirmation_observation_bytes=documents["confirmation-observation.json"],
            identity_derivation_bytes=documents["identity-derivation.json"],
            payload_schema_bundle_bytes=documents["confirmation-payload-schemas.json"],
            command_bytes=documents["confirmation-command.json"],
        )

        self.database = RuntimeDatabase(self.root / "runtime.sqlite3")
        self.artifacts = ArtifactStore(self.database)
        self.journal = RuntimeJournal(self.database, self.artifacts)
        self._bind_harness_schema(self.journal)
        with self.database.connect() as conn:
            self.run = dict(conn.execute("SELECT * FROM runs").fetchone())
            self.graph = dict(conn.execute("SELECT * FROM confirmed_turn_graphs").fetchone())
            nodes = json.loads(self.graph["nodes_json"])
            self.group_id = nodes[0]["group_id"]
            opening = conn.execute(
                """
                SELECT event_id,journal_offset FROM events
                WHERE aggregate_id=? AND event_type='audit_opening.requested'
                """,
                (self.run["run_id"],),
            ).fetchone()
        self.initial_run_event_id = opening["event_id"]
        with self.database.write() as conn:
            conn.execute(
                """
                INSERT INTO runtime_run_heads(
                  run_id,state,version,last_event_id,last_offset,opening_fence_status,
                  opening_verification_event_id,reconciliation_target
                ) VALUES(?,?,?,?,?,'closed',NULL,NULL)
                """,
                (
                    self.run["run_id"],
                    "opening_pending",
                    self.run["aggregate_version"],
                    opening["event_id"],
                    opening["journal_offset"],
                ),
            )
            conn.execute(
                """
                INSERT INTO runtime_group_heads(
                  graph_id,group_id,group_version,state,version,last_event_id,last_offset
                ) VALUES(?,?,1,'pending',0,NULL,NULL)
                """,
                (self.graph["graph_id"], self.group_id),
            )

    def tearDown(self) -> None:
        self.temp.cleanup()

    @staticmethod
    def _bind_harness_schema(journal: RuntimeJournal) -> None:
        journal.bind_event_schemas({HARNESS_EVENT: (HARNESS_SCHEMA, HARNESS_SCHEMA_DIGEST)})
        journal.bind_payload_validators({HARNESS_EVENT: lambda payload: None})

    def _seed_second_confirmed_graph(self) -> dict[str, str]:
        """Create a second confirmed parent tuple only inside the test harness."""

        command = RuntimeCommand(
            command_id="cmd_heads_second_parent",
            scope_key="aci.test-heads:second-parent",
            idempotency_key="accept@1",
            aggregate_type="test.run-group-parent",
            aggregate_id="aci.test-heads:second-parent",
            expected_version=0,
            causation_id="cause_heads_second_parent",
            correlation_id="run_heads_second",
            authority_context={"principal_id": "test-heads-harness-only"},
            semantic_intent={"harness_only": True, "purpose": "second-confirmed-graph"},
        )
        payload = self.artifacts.prepare(
            b'{"harness_only":true,"purpose":"second-confirmed-graph"}',
            media_type="application/json",
            schema_ref=HARNESS_SCHEMA,
            classification="runtime-internal",
        )
        receipt = self.journal.accept(
            command,
            [
                EventDraft(
                    event_id="evt_heads_second_parent",
                    event_type=HARNESS_EVENT,
                    schema_ref=HARNESS_SCHEMA,
                    schema_digest=HARNESS_SCHEMA_DIGEST,
                    payload=payload,
                )
            ],
            next_state={"harness_only": True, "state": "parent-seeded"},
        )
        graph_artifact = self.artifacts.prepare(
            b'{"harness_only":true,"parent":"graph-2"}',
            media_type="application/json",
            schema_ref="aci.test-confirmed-graph-parent@1",
            classification="runtime-internal",
        )
        mapping_artifact = self.artifacts.prepare(
            b'{"harness_only":true,"parent":"mapping-2"}',
            media_type="application/json",
            schema_ref="aci.test-confirmed-mapping-parent@1",
            classification="runtime-internal",
        )
        graph_ref = self.artifacts.commit(graph_artifact)
        mapping_ref = self.artifacts.commit(mapping_artifact)
        dispatch_id = "dispatch_heads_second"
        run_id = "run_heads_second"
        graph_id = "graph_heads_second"
        with self.database.write() as conn:
            source_dispatch = dict(conn.execute("SELECT * FROM confirmed_dispatches").fetchone())
            source_run = dict(
                conn.execute("SELECT * FROM runs WHERE run_id=?", (self.run["run_id"],)).fetchone()
            )
            source_graph = dict(
                conn.execute(
                    "SELECT * FROM confirmed_turn_graphs WHERE graph_id=?",
                    (self.graph["graph_id"],),
                ).fetchone()
            )
            source_dispatch.update(
                dispatch_id=dispatch_id,
                accepted_command_id=command.command_id,
            )
            columns = tuple(source_dispatch)
            conn.execute(
                f"INSERT INTO confirmed_dispatches({','.join(columns)}) VALUES({','.join('?' for _ in columns)})",
                tuple(source_dispatch[column] for column in columns),
            )
            source_run.update(run_id=run_id, dispatch_id=dispatch_id)
            columns = tuple(source_run)
            conn.execute(
                f"INSERT INTO runs({','.join(columns)}) VALUES({','.join('?' for _ in columns)})",
                tuple(source_run[column] for column in columns),
            )
            source_graph.update(
                graph_id=graph_id,
                dispatch_id=dispatch_id,
                run_id=run_id,
                graph_artifact_id=graph_ref["artifact_id"],
                graph_digest=graph_ref["content_hash"],
                continuation_id="cont_heads_second",
                mapping_set_artifact_id=mapping_ref["artifact_id"],
                mapping_set_digest=mapping_ref["content_hash"],
            )
            columns = tuple(source_graph)
            conn.execute(
                f"INSERT INTO confirmed_turn_graphs({','.join(columns)}) VALUES({','.join('?' for _ in columns)})",
                tuple(source_graph[column] for column in columns),
            )
            conn.execute(
                """
                INSERT INTO runtime_run_heads(
                  run_id,state,version,last_event_id,last_offset,opening_fence_status,
                  opening_verification_event_id,reconciliation_target
                ) VALUES(?,'opening_pending',2,?,?,'closed',NULL,NULL)
                """,
                (run_id, receipt["ordered_event_ids"][0], receipt["first_offset"]),
            )
            conn.execute(
                """
                INSERT INTO runtime_group_heads(
                  graph_id,group_id,group_version,state,version,last_event_id,last_offset
                ) VALUES(?,?,1,'pending',0,NULL,NULL)
                """,
                (graph_id, self.group_id),
            )
        return {
            "dispatch_id": dispatch_id,
            "run_id": run_id,
            "graph_id": graph_id,
            "run_last_event_id": receipt["ordered_event_ids"][0],
        }

    def _heads(
        self,
        *,
        run_id: str | None = None,
        graph_id: str | None = None,
        group_id: str | None = None,
    ) -> tuple[dict, dict]:
        run_id = run_id or self.run["run_id"]
        graph_id = graph_id or self.graph["graph_id"]
        group_id = group_id or self.group_id
        with self.database.connect() as conn:
            run = dict(
                conn.execute(
                    "SELECT * FROM runtime_run_heads WHERE run_id=?",
                    (run_id,),
                ).fetchone()
            )
            group = dict(
                conn.execute(
                    """
                    SELECT * FROM runtime_group_heads
                    WHERE graph_id=? AND group_id=? AND group_version=1
                    """,
                    (graph_id, group_id),
                ).fetchone()
            )
        return run, group

    def _surface(self) -> dict[str, list[tuple]]:
        tables = (
            "runtime_run_heads",
            "runtime_group_heads",
            "events",
            "aggregate_heads",
            "command_receipts",
            "artifacts",
            "effect_intents",
            "sandbox_launch_effects",
            "agent_attempts",
        )
        with self.database.connect() as conn:
            return {
                table: [tuple(row) for row in conn.execute(f"SELECT * FROM {table} ORDER BY rowid")]
                for table in tables
            }

    def _accept_heads(
        self,
        *,
        key: str,
        expected_run_version: int,
        expected_run_last_event_id: str | None = None,
        expected_group_version: int | None = None,
        expected_group_last_event_id: str | None = None,
        run_next: RunProjection | None = None,
        group_next: GroupProjection | None = None,
        run_transition: tuple[str, dict] | None = None,
        group_transition: tuple[str, dict] | None = None,
        run_id: str | None = None,
        graph_id: str | None = None,
        group_id: str | None = None,
        semantic_marker: str = "stable",
        journal: RuntimeJournal | None = None,
        failpoint=None,
    ) -> dict:
        journal = journal or self.journal
        run_id = run_id or self.run["run_id"]
        graph_id = graph_id or self.graph["graph_id"]
        group_id = group_id or self.group_id
        expected_run_head = {
            "run_id": run_id,
            "version": expected_run_version,
            "last_event_id": (
                self.initial_run_event_id
                if expected_run_version == 2 and expected_run_last_event_id is None
                else expected_run_last_event_id
            ),
        }
        expected_group_head = (
            {
                "graph_id": graph_id,
                "group_id": group_id,
                "group_version": 1,
                "version": expected_group_version,
                "last_event_id": expected_group_last_event_id,
            }
            if expected_group_version is not None
            else None
        )
        command = RuntimeCommand(
            command_id=f"cmd_heads_{key}_{semantic_marker}",
            scope_key=f"aci.test-heads:{key}",
            idempotency_key="accept@1",
            aggregate_type="test.run-group-heads",
            aggregate_id=f"aci.test-heads:{key}",
            expected_version=0,
            causation_id=f"cause_{key}",
            correlation_id=run_id,
            authority_context={"principal_id": "test-heads-harness-only"},
            semantic_intent={
                "expected_group_head": expected_group_head,
                "expected_run_head": expected_run_head,
                "graph_id": graph_id,
                "group_id": group_id,
                "group_projection": asdict(group_next) if group_next else None,
                "group_transition": group_transition,
                "group_version": 1,
                "harness_only": True,
                "marker": semantic_marker,
                "run_id": run_id,
                "run_projection": asdict(run_next) if run_next else None,
                "run_transition": run_transition,
            },
        )
        payload = self.artifacts.prepare(
            json.dumps(command.semantic_intent, sort_keys=True, separators=(",", ":")).encode(),
            media_type="application/json",
            schema_ref=HARNESS_SCHEMA,
            classification="runtime-internal",
        )
        event = EventDraft(
            event_id=f"evt_heads_{key}_{semantic_marker}",
            event_type=HARNESS_EVENT,
            schema_ref=HARNESS_SCHEMA,
            schema_digest=HARNESS_SCHEMA_DIGEST,
            payload=payload,
        )

        def mutate(conn, records, _receipt):
            record = records[0]
            graph_parent = conn.execute(
                """
                SELECT 1 FROM confirmed_turn_graphs
                WHERE graph_id=? AND run_id=?
                """,
                (graph_id, run_id),
            ).fetchone()
            if not graph_parent:
                raise RunGroupHeadConflict("confirmed graph/run parent binding changed")
            run_before = conn.execute(
                "SELECT * FROM runtime_run_heads WHERE run_id=?",
                (run_id,),
            ).fetchone()
            if not run_before or int(run_before["version"]) != expected_run_version:
                raise RunGroupHeadConflict("run prerequisite expected version changed")
            if run_before["last_event_id"] != expected_run_head["last_event_id"]:
                raise RunGroupHeadConflict("run prerequisite expected event changed")
            if run_next is not None:
                if run_transition is None:
                    raise RunGroupGuardError("run transition is required by the harness")
                current_run = RunProjection(
                    state=run_before["state"],
                    opening_verified=run_before["opening_verification_event_id"] is not None,
                    opening_verification_event_id=run_before["opening_verification_event_id"],
                    reconciliation_target=run_before["reconciliation_target"],
                )
                calculated_run = reduce_run(current_run, *run_transition)
                if calculated_run != run_next:
                    raise RunGroupGuardError("requested run projection differs from reducer output")
                opening_event_id = run_before["opening_verification_event_id"]
                if run_next.opening_verified and opening_event_id is None:
                    opening_event_id = record.event_id
                updated = conn.execute(
                    """
                    UPDATE runtime_run_heads
                    SET state=?,version=?,last_event_id=?,last_offset=?,
                        opening_fence_status=?,opening_verification_event_id=?,
                        reconciliation_target=?
                    WHERE run_id=? AND version=? AND last_event_id=?
                    """,
                    (
                        run_next.state,
                        expected_run_version + 1,
                        record.event_id,
                        record.journal_offset,
                        "verified" if run_execution_eligible(run_next) else "closed",
                        opening_event_id,
                        run_next.reconciliation_target,
                        run_id,
                        expected_run_version,
                        run_before["last_event_id"],
                    ),
                )
                if updated.rowcount != 1:
                    raise RunGroupHeadConflict("run head CAS lost")
                if failpoint:
                    failpoint("heads.after_run_head")
            if group_next is not None:
                group_before = conn.execute(
                    """
                    SELECT * FROM runtime_group_heads
                    WHERE graph_id=? AND group_id=? AND group_version=1
                    """,
                    (graph_id, group_id),
                ).fetchone()
                if not group_before or int(group_before["version"]) != expected_group_version:
                    raise RunGroupHeadConflict("group head expected version changed")
                if group_before["last_event_id"] != expected_group_head["last_event_id"]:
                    raise RunGroupHeadConflict("group head expected event changed")
                if group_transition is None:
                    raise RunGroupGuardError("group transition is required by the harness")
                calculated_group = reduce_group(
                    GroupProjection(group_before["state"]), *group_transition
                )
                if calculated_group != group_next:
                    raise RunGroupGuardError(
                        "requested group projection differs from reducer output"
                    )
                updated = conn.execute(
                    """
                    UPDATE runtime_group_heads
                    SET state=?,version=?,last_event_id=?,last_offset=?
                    WHERE graph_id=? AND group_id=? AND group_version=1 AND version=?
                      AND ((last_event_id IS NULL AND ? IS NULL) OR last_event_id=?)
                    """,
                    (
                        group_next.state,
                        expected_group_version + 1,
                        record.event_id,
                        record.journal_offset,
                        graph_id,
                        group_id,
                        expected_group_version,
                        group_before["last_event_id"],
                        group_before["last_event_id"],
                    ),
                )
                if updated.rowcount != 1:
                    raise RunGroupHeadConflict("group head CAS lost")
                if failpoint:
                    failpoint("heads.after_group_head")

        return journal.accept(
            command,
            [event],
            next_state={"harness_only": True, "semantic_intent": command.semantic_intent},
            mutate=mutate,
            failpoint=failpoint,
        )

    def _harness_verified_ready(self) -> RunProjection:
        return reduce_run(
            RunProjection("opening_pending"),
            "audit_opening.verified",
            {
                "exact_canonical_row": True,
                "evidence_event_id": "evt_test_harness_only_opening_verified",
            },
        )

    def test_migration_014_isolated_reopens_and_has_direct_confirmed_parents(self) -> None:
        with self.database.connect() as conn:
            self.assertEqual(conn.execute("PRAGMA user_version").fetchone()[0], 16)
            self.assertEqual(
                {
                    row[0]
                    for row in conn.execute(
                        """
                        SELECT name FROM sqlite_master
                        WHERE type='table' AND name IN ('runtime_run_heads','runtime_group_heads')
                        """
                    )
                },
                {"runtime_run_heads", "runtime_group_heads"},
            )
            self.assertEqual(
                {row["table"] for row in conn.execute("PRAGMA foreign_key_list(runtime_run_heads)")},
                {"runs", "events"},
            )
            self.assertEqual(
                {row["table"] for row in conn.execute("PRAGMA foreign_key_list(runtime_group_heads)")},
                {"confirmed_turn_graphs", "events"},
            )
            self.assertEqual(
                {
                    row["name"]: row["pk"]
                    for row in conn.execute("PRAGMA table_info(runtime_group_heads)")
                    if row["pk"]
                },
                {"graph_id": 1, "group_id": 2, "group_version": 3},
            )
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM runs").fetchone()[0], 1)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM confirmed_turn_graphs").fetchone()[0], 1)
        self.assertEqual(self.database.migrate(), [])
        self.assertEqual(self.database.verify_policy()["quick_check"], "ok")

    def test_group_identity_is_scoped_by_confirmed_graph_and_cas_reopens_independently(self) -> None:
        second = self._seed_second_confirmed_graph()
        with self.database.connect() as conn:
            rows = conn.execute(
                """
                SELECT graph_id,group_id,group_version,state,version
                FROM runtime_group_heads
                WHERE group_id=? AND group_version=1 ORDER BY graph_id
                """,
                (self.group_id,),
            ).fetchall()
        self.assertEqual(len(rows), 2)
        self.assertEqual({row["graph_id"] for row in rows}, {self.graph["graph_id"], second["graph_id"]})
        with self.assertRaises(sqlite3.IntegrityError):
            with self.database.write() as conn:
                conn.execute(
                    """
                    INSERT INTO runtime_group_heads(
                      graph_id,group_id,group_version,state,version,last_event_id,last_offset
                    ) VALUES(?,?,1,'pending',0,NULL,NULL)
                    """,
                    (second["graph_id"], self.group_id),
                )

        started = reduce_group(
            GroupProjection("pending"),
            "group.started",
            {"dependencies_delivered": True, "spec_valid": True},
        )
        start_transition = (
            "group.started",
            {"dependencies_delivered": True, "spec_valid": True},
        )
        for key, run_id, graph_id, last_event_id in (
            (
                "cross-parent-a-run-b-graph",
                self.run["run_id"],
                second["graph_id"],
                self.initial_run_event_id,
            ),
            (
                "cross-parent-b-run-a-graph",
                second["run_id"],
                self.graph["graph_id"],
                second["run_last_event_id"],
            ),
        ):
            with self.subTest(cross_parent=key):
                before = self._surface()
                with self.assertRaises(RunGroupHeadConflict):
                    self._accept_heads(
                        key=key,
                        expected_run_version=2,
                        expected_run_last_event_id=last_event_id,
                        expected_group_version=0,
                        group_next=started,
                        group_transition=start_transition,
                        run_id=run_id,
                        graph_id=graph_id,
                    )
                self.assertEqual(self._surface(), before)
        self._accept_heads(
            key="graph-a-start",
            expected_run_version=2,
            expected_group_version=0,
            group_next=started,
            group_transition=start_transition,
        )
        self._accept_heads(
            key="graph-b-start",
            expected_run_version=2,
            expected_run_last_event_id=second["run_last_event_id"],
            expected_group_version=0,
            group_next=started,
            group_transition=start_transition,
            run_id=second["run_id"],
            graph_id=second["graph_id"],
        )

        reopened_db = RuntimeDatabase(self.root / "runtime.sqlite3")
        self.assertEqual(reopened_db.migrate(), [])
        reopened_journal = RuntimeJournal(reopened_db, ArtifactStore(reopened_db))
        self._bind_harness_schema(reopened_journal)
        for run_id, graph_id in (
            (self.run["run_id"], self.graph["graph_id"]),
            (second["run_id"], second["graph_id"]),
        ):
            _, group = self._heads(run_id=run_id, graph_id=graph_id)
            self.assertEqual((group["state"], group["version"]), ("collecting", 1))

        revealing = reduce_group(
            GroupProjection("collecting"),
            "collection.closed",
            {"eligible_set_frozen": True, "quorum_or_deadline_policy": True},
        )
        close_transition = (
            "collection.closed",
            {"eligible_set_frozen": True, "quorum_or_deadline_policy": True},
        )
        self._accept_heads(
            key="graph-a-close",
            expected_run_version=2,
            expected_group_version=1,
            expected_group_last_event_id="evt_heads_graph-a-start_stable",
            group_next=revealing,
            group_transition=close_transition,
            journal=reopened_journal,
        )
        self._accept_heads(
            key="graph-b-close",
            expected_run_version=2,
            expected_run_last_event_id=second["run_last_event_id"],
            expected_group_version=1,
            expected_group_last_event_id="evt_heads_graph-b-start_stable",
            group_next=revealing,
            group_transition=close_transition,
            run_id=second["run_id"],
            graph_id=second["graph_id"],
            journal=reopened_journal,
        )
        stable = self._surface()
        with self.assertRaises(RunGroupHeadConflict):
            self._accept_heads(
                key="graph-b-stale",
                expected_run_version=2,
                expected_run_last_event_id=second["run_last_event_id"],
                expected_group_version=2,
                expected_group_last_event_id="evt_wrong_graph_b_prior",
                group_next=GroupProjection("voting"),
                group_transition=(
                    "reveal.published",
                    {"exact_manifest": True, "deliberation_enabled": False},
                ),
                run_id=second["run_id"],
                graph_id=second["graph_id"],
                journal=reopened_journal,
            )
        self.assertEqual(self._surface(), stable)
        final_db = RuntimeDatabase(self.root / "runtime.sqlite3")
        self.assertEqual(final_db.migrate(), [])
        for run_id, graph_id in (
            (self.run["run_id"], self.graph["graph_id"]),
            (second["run_id"], second["graph_id"]),
        ):
            _, group = self._heads(run_id=run_id, graph_id=graph_id)
            self.assertEqual((group["state"], group["version"]), ("revealing", 2))

    def test_run_reducer_is_total_terminal_mapping_and_fence_fail_closed(self) -> None:
        opening = RunProjection("opening_pending")
        reconciliation = reduce_run(
            opening,
            "audit_opening.reconciliation_required",
            {"same_identity_divergent": True},
        )
        ready = self._harness_verified_ready()
        for projection in (opening, reconciliation):
            self.assertFalse(run_execution_eligible(projection))
            with self.assertRaises(RunGroupFenceClosed):
                require_run_execution_eligible(projection)
        self.assertTrue(run_execution_eligible(ready))

        current_by_state = {
            "confirmed": RunProjection("confirmed"),
            "opening_pending": opening,
            "ready": ready,
            "running": RunProjection("running", True, "evt_open"),
            "execution_terminal": RunProjection(
                "execution_terminal", True, "evt_open", terminal_cause="committed_result", exit_reason="resolved"
            ),
            "close_pending": RunProjection(
                "close_pending", True, "evt_open", terminal_cause="committed_result", exit_reason="resolved"
            ),
            "reconciliation_required": reconciliation,
            "closed": RunProjection("closed", True, "evt_open"),
        }
        guards = {
            "run.created": {
                "execution_authority_mode": "runtime-managed",
                "frozen_digest_unique": True,
            },
            "audit_opening.requested": {"opening_intent_committed": True},
            "audit_opening.verified": {"exact_canonical_row": True, "evidence_event_id": "evt_open"},
            "audit_opening.reconciliation_required": {"same_identity_divergent": True},
            "reconciliation.retry_requested": {"target": "opening", "authorized_repair_disposition": True},
            "run.started": {"opening_remains_verified": True},
            "run.execution_terminal_elected": {"terminal_cause": "committed_result", "exit_reason": "resolved"},
            "audit_close.requested": {"close_derived_from_winner": True},
            "audit_close.verified": {"exact_canonical_row": True},
            "audit_close.reconciliation_required": {"same_identity_divergent": True},
        }
        admitted = {
            (None, "run.created"),
            ("confirmed", "audit_opening.requested"),
            ("opening_pending", "audit_opening.verified"),
            ("opening_pending", "audit_opening.reconciliation_required"),
            ("reconciliation_required", "reconciliation.retry_requested"),
            ("ready", "run.started"),
            ("running", "run.execution_terminal_elected"),
            ("execution_terminal", "audit_close.requested"),
            ("close_pending", "audit_close.verified"),
            ("close_pending", "audit_close.reconciliation_required"),
        }
        for state in (None, *RUN_STATES):
            for event_type in RUN_EVENTS:
                with self.subTest(state=state, event_type=event_type):
                    current = None if state is None else current_by_state[state]
                    if (state, event_type) in admitted:
                        self.assertIsInstance(reduce_run(current, event_type, guards[event_type]), RunProjection)
                    else:
                        with self.assertRaises(InvalidRunTransition):
                            reduce_run(current, event_type, guards[event_type])

        running = current_by_state["running"]
        expected = {
            "committed_result": "resolved",
            "committed_irreconcilable_dissent": "dissent_irreconcilable",
            "protocol_ceiling": "loop_ceiling_reached",
            "human_cancellation": "user_abort",
            "technical_prevention": "error",
        }
        for cause, exit_reason in expected.items():
            result = reduce_run(
                running,
                "run.execution_terminal_elected",
                {"terminal_cause": cause, "exit_reason": exit_reason},
            )
            self.assertEqual(result.exit_reason, exit_reason)
            with self.assertRaises(InvalidRunTransition):
                reduce_run(result, "run.execution_terminal_elected", {"terminal_cause": cause, "exit_reason": exit_reason})
        with self.assertRaises(RunGroupGuardError):
            reduce_run(running, "run.execution_terminal_elected", {"terminal_cause": "technical_prevention", "exit_reason": "loop_ceiling_reached"})
        with self.assertRaises(RunGroupGuardError):
            reduce_run(
                None,
                "run.created",
                {"execution_authority_mode": "runtime-managed"},
            )

    def test_group_reducer_is_total_fixed_two_seat_and_terminals_are_immutable(self) -> None:
        current_by_state = {
            state: GroupProjection(
                state,
                "dissent" if state in {"committing", "completed"} else None,
                ("msg_a", "msg_b") if state == "completed" else (),
            )
            for state in GROUP_STATES
        }
        guards = {
            "group.started": {"dependencies_delivered": True, "spec_valid": True},
            "position.accepted": {"parent_receipt_verified": True, "logical_key_unused": True},
            "collection.closed": {"eligible_set_frozen": True, "quorum_or_deadline_policy": True},
            "reveal.published": {"exact_manifest": True, "deliberation_enabled": False},
            "critique.accepted": {"reply_visible": True, "round_schema_valid": True},
            "round.closed": {"criterion_recorded": True},
            "vote.accepted": {"logical_vote_unused": True, "schema_valid": True},
            "verdict.computed": {"decision": "dissent", "quorum": True},
            "group.committed": {"typed_result": True, "persisted_verdict": True, "dissent_refs": ("msg_a", "msg_b")},
            "cancellation.requested": {"authorized": True},
            "group.cancelled": {"attempts_terminal_or_deadline": True},
            "group.failed": {"declared_retries_exhausted": True},
        }
        admitted = {
            ("pending", "group.started"),
            ("collecting", "position.accepted"),
            ("collecting", "collection.closed"),
            ("revealing", "reveal.published"),
            ("deliberating", "critique.accepted"),
            ("deliberating", "round.closed"),
            ("voting", "vote.accepted"),
            ("voting", "verdict.computed"),
            ("committing", "group.committed"),
            ("cancelling", "group.cancelled"),
        }
        nonterminal = set(GROUP_STATES) - {"completed", "cancelled", "failed"}
        admitted.update((state, "cancellation.requested") for state in nonterminal)
        admitted.update((state, "group.failed") for state in nonterminal - {"cancelling"})
        for state in GROUP_STATES:
            for event_type in GROUP_EVENTS:
                with self.subTest(state=state, event_type=event_type):
                    if (state, event_type) in admitted:
                        self.assertIsInstance(
                            reduce_group(current_by_state[state], event_type, guards[event_type]),
                            GroupProjection,
                        )
                    else:
                        with self.assertRaises(InvalidGroupTransition):
                            reduce_group(current_by_state[state], event_type, guards[event_type])
        self.assertEqual(fixed_two_seat_decision(("accept", "accept")), "consensus")
        self.assertEqual(fixed_two_seat_decision(("accept", "reject")), "dissent")
        self.assertEqual(fixed_two_seat_decision(("accept",)), "no_quorum")
        self.assertEqual(fixed_two_seat_decision(("", "accept")), "no_quorum")
        with self.assertRaises(RunGroupGuardError):
            reduce_group(
                GroupProjection("voting"),
                "verdict.computed",
                {"decision": "no_quorum", "quorum": True},
            )

    def test_exact_cas_replay_semantic_drift_and_stale_head_conflict(self) -> None:
        ready = self._harness_verified_ready()
        transition = (
            "audit_opening.verified",
            {
                "exact_canonical_row": True,
                "evidence_event_id": "evt_test_harness_only_opening_verified",
            },
        )
        first = self._accept_heads(
            key="ready", expected_run_version=2, run_next=ready, run_transition=transition
        )
        self.assertEqual(
            first,
            self._accept_heads(
                key="ready",
                expected_run_version=2,
                run_next=ready,
                run_transition=transition,
            ),
        )
        with self.assertRaises(IdempotencyConflict):
            self._accept_heads(
                key="ready",
                expected_run_version=2,
                run_next=RunProjection(
                    "ready", True, "evt_different_opening_evidence"
                ),
                run_transition=(
                    "audit_opening.verified",
                    {
                        "exact_canonical_row": True,
                        "evidence_event_id": "evt_different_opening_evidence",
                    },
                ),
            )
        before = self._surface()
        with self.assertRaises(RunGroupHeadConflict):
            self._accept_heads(
                key="stale",
                expected_run_version=2,
                run_next=ready,
                run_transition=transition,
            )
        self.assertEqual(self._surface(), before)

        with self.assertRaises(InvalidRunTransition):
            self._accept_heads(
                key="illegal-jump",
                expected_run_version=3,
                expected_run_last_event_id="evt_heads_ready_stable",
                run_next=RunProjection("closed", True, "evt_heads_ready_stable"),
                run_transition=("audit_close.verified", {"exact_canonical_row": True}),
            )

    def test_multi_head_failpoints_roll_back_both_and_reopen_replays(self) -> None:
        points = (
            "before_begin",
            "after_begin",
            "after_validation",
            "after_artifact",
            "after_event",
            "after_head",
            "heads.after_run_head",
            "heads.after_group_head",
            "after_mutation",
            "after_receipt",
            "before_commit",
        )
        for index, point in enumerate(points):
            with self.subTest(point=point):
                if index:
                    self.tearDown()
                    self.setUp()
                before = self._surface()

                def fail(name: str, target=point) -> None:
                    if name == target:
                        raise RuntimeError(target)

                with self.assertRaisesRegex(RuntimeError, point):
                    self._accept_heads(
                        key=f"atomic-{index}",
                        expected_run_version=2,
                        expected_group_version=0,
                        run_next=self._harness_verified_ready(),
                        run_transition=(
                            "audit_opening.verified",
                            {
                                "exact_canonical_row": True,
                                "evidence_event_id": "evt_test_harness_only_opening_verified",
                            },
                        ),
                        group_next=reduce_group(
                            GroupProjection("pending"),
                            "group.started",
                            {"dependencies_delivered": True, "spec_valid": True},
                        ),
                        group_transition=(
                            "group.started",
                            {"dependencies_delivered": True, "spec_valid": True},
                        ),
                        failpoint=fail,
                    )
                self.assertEqual(self._surface(), before)

        receipt = self._accept_heads(
            key="multi",
            expected_run_version=2,
            expected_group_version=0,
            run_next=self._harness_verified_ready(),
            run_transition=(
                "audit_opening.verified",
                {
                    "exact_canonical_row": True,
                    "evidence_event_id": "evt_test_harness_only_opening_verified",
                },
            ),
            group_next=GroupProjection("collecting"),
            group_transition=(
                "group.started",
                {"dependencies_delivered": True, "spec_valid": True},
            ),
        )
        run, group = self._heads()
        self.assertEqual((run["state"], run["version"]), ("ready", 3))
        self.assertEqual((group["state"], group["version"]), ("collecting", 1))
        reopened_db = RuntimeDatabase(self.root / "runtime.sqlite3")
        self.assertEqual(reopened_db.migrate(), [])
        reopened_journal = RuntimeJournal(reopened_db, ArtifactStore(reopened_db))
        self._bind_harness_schema(reopened_journal)
        self.assertEqual(
            self._accept_heads(
                key="multi",
                expected_run_version=2,
                expected_group_version=0,
                run_next=self._harness_verified_ready(),
                run_transition=(
                    "audit_opening.verified",
                    {
                        "exact_canonical_row": True,
                        "evidence_event_id": "evt_test_harness_only_opening_verified",
                    },
                ),
                group_next=GroupProjection("collecting"),
                group_transition=(
                    "group.started",
                    {"dependencies_delivered": True, "spec_valid": True},
                ),
                journal=reopened_journal,
            ),
            receipt,
        )
        revealing = reduce_group(
            GroupProjection("collecting"),
            "collection.closed",
            {"eligible_set_frozen": True, "quorum_or_deadline_policy": True},
        )
        before_bad_prerequisite = self._surface()
        with self.assertRaises(RunGroupHeadConflict):
            self._accept_heads(
                key="group-bad-run-prerequisite",
                expected_run_version=999,
                expected_run_last_event_id="evt_definitely_wrong",
                expected_group_version=1,
                expected_group_last_event_id="evt_heads_multi_stable",
                group_next=revealing,
                group_transition=(
                    "collection.closed",
                    {"eligible_set_frozen": True, "quorum_or_deadline_policy": True},
                ),
            )
        self.assertEqual(self._surface(), before_bad_prerequisite)
        self._accept_heads(
            key="group-progress",
            expected_run_version=3,
            expected_run_last_event_id="evt_heads_multi_stable",
            expected_group_version=1,
            expected_group_last_event_id="evt_heads_multi_stable",
            group_next=revealing,
            group_transition=(
                "collection.closed",
                {"eligible_set_frozen": True, "quorum_or_deadline_policy": True},
            ),
        )
        self.assertEqual(self._heads()[1]["version"], 2)
        before_stale = self._surface()
        with self.assertRaises(RunGroupHeadConflict):
            self._accept_heads(
                key="group-stale-event",
                expected_run_version=3,
                expected_run_last_event_id="evt_heads_multi_stable",
                expected_group_version=2,
                expected_group_last_event_id="evt_wrong_prior_group_event",
                group_next=GroupProjection("voting"),
                group_transition=(
                    "reveal.published",
                    {"exact_manifest": True, "deliberation_enabled": False},
                ),
            )
        self.assertEqual(self._surface(), before_stale)

    def test_concurrent_distinct_commands_have_one_runtime_head_winner(self) -> None:
        barrier = threading.Barrier(2)
        results: list[dict] = []
        errors: list[Exception] = []

        def race(key: str) -> None:
            database = RuntimeDatabase(self.root / "runtime.sqlite3")
            journal = RuntimeJournal(database, ArtifactStore(database))
            self._bind_harness_schema(journal)
            barrier.wait()
            try:
                results.append(
                    self._accept_heads(
                        key=key,
                        expected_run_version=2,
                        run_next=self._harness_verified_ready(),
                        run_transition=(
                            "audit_opening.verified",
                            {
                                "exact_canonical_row": True,
                                "evidence_event_id": "evt_test_harness_only_opening_verified",
                            },
                        ),
                        journal=journal,
                    )
                )
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=race, args=(key,)) for key in ("race-a", "race-b")]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual(len(results), 1)
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], RunGroupHeadConflict)
        self.assertEqual(self._heads()[0]["version"], 3)

    def test_harness_positive_setup_creates_no_effect_or_production_surface(self) -> None:
        before = self._surface()
        self._accept_heads(
            key="harness-only-positive",
            expected_run_version=2,
            run_next=self._harness_verified_ready(),
            run_transition=(
                "audit_opening.verified",
                {
                    "exact_canonical_row": True,
                    "evidence_event_id": "evt_test_harness_only_opening_verified",
                },
            ),
        )
        after = self._surface()
        self.assertEqual(after["effect_intents"], before["effect_intents"])
        self.assertEqual(after["sandbox_launch_effects"], before["sandbox_launch_effects"])
        self.assertEqual(after["agent_attempts"], before["agent_attempts"])
        service_source = (REPO / "implementations/server/runtime/service.py").read_text(encoding="utf-8")
        api_source = (REPO / "implementations/server/runtime/api.py").read_text(encoding="utf-8")
        for source in (service_source, api_source):
            self.assertNotIn("runtime_run_heads", source)
            self.assertNotIn("runtime_group_heads", source)
            self.assertNotIn("reduce_run", source)
            self.assertNotIn("reduce_group", source)


if __name__ == "__main__":
    unittest.main()
