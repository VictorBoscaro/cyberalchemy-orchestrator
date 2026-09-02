from __future__ import annotations

import json
import sqlite3
import tempfile
import threading
import unittest
from copy import deepcopy
from pathlib import Path

from implementations.server.runtime.canonical import (
    canonical_bytes,
    canonical_digest,
    digest_bytes,
)
from implementations.server.runtime.confirmed_bus import (
    ConfirmedBusProjection,
    derive_group_aggregate_id,
    project_confirmed_bus_acceptance,
    reduce_confirmed_bus_group_pair,
    require_attempt_journal_chain,
    require_group_journal_chain,
)
from implementations.server.runtime.errors import (
    IdempotencyConflict,
    ValidationError,
    VersionConflict,
)
from implementations.server.runtime.journal import RuntimeCommand
from implementations.server.runtime.run_group import GroupProjection
from implementations.server.runtime.service import RuntimeService, RuntimeSettings


REPO = Path(__file__).resolve().parents[3]
FIXTURE = REPO / "docs/features/agents-communication-infra/specs/fixtures/confirmed-dispatch-v2"


def _required_row(row, label: str) -> dict:
    if row is None:
        raise ValidationError(f"{label} is missing")
    return dict(row)


class ConfirmedBusComponentTests(unittest.TestCase):
    """Test-only writer for the bounded BUS-001 component proof."""

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
        self.service.confirm_runtime_dispatch(
            pending_sheet_bytes=self.documents["pending-sheet.json"],
            capability_resolution_bytes=self.documents["capability-resolution.json"],
            capability_resolution_artifact_id=preview.artifact_id,
            trusted_issuer_context_bytes=self.documents["trusted-issuer-context.json"],
            confirmation_observation_bytes=self.documents["confirmation-observation.json"],
            identity_derivation_bytes=self.documents["identity-derivation.json"],
            payload_schema_bundle_bytes=self.documents["confirmation-payload-schemas.json"],
            command_bytes=self.documents["confirmation-command.json"],
        )
        self._bind_harness_events()
        with self.service.database.connect() as conn:
            self.graph = dict(conn.execute("SELECT * FROM confirmed_turn_graphs").fetchone())
            self.run = dict(conn.execute("SELECT * FROM runs").fetchone())

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _bind_harness_events(self) -> None:
        event_types = (
            "attempt.requested",
            "attempt.starting",
            "attempt.running",
            "attempt.completed",
            "group.started",
            "collection.closed",
            "reveal.published",
            "publication.persisted",
            "attempt.result_accepted",
            "position.accepted",
            "critique.accepted",
        )
        bindings = dict(self.service.journal._schema_bindings)
        validators = dict(self.service.journal._payload_validators)
        for event_type in event_types:
            schema_ref = "aci." + event_type.replace(".", "-") + "@1"
            bindings[event_type] = (schema_ref, canonical_digest({"schema_ref": schema_ref}))
            validators[event_type] = lambda _payload: None
        self.service.journal.bind_event_schemas(bindings)
        self.service.journal.bind_payload_validators(validators)

    def _mapping(self, ordinal: int) -> dict:
        with self.service.database.connect() as conn:
            return dict(
                conn.execute(
                    "SELECT * FROM continuation_input_mappings WHERE slot_ordinal=?",
                    (ordinal,),
                ).fetchone()
            )

    def _create_completed_attempt(self, ordinal: int, suffix: str = "") -> dict:
        mapping = self._mapping(ordinal)
        attempt_id = f"attempt_bus_{ordinal}{suffix}"
        aggregate_id = f"aci.agent-attempt:{attempt_id}"
        state_events = (
            ("attempt.requested", "requested"),
            ("attempt.starting", "starting"),
            ("attempt.running", "running"),
            ("attempt.completed", "completed"),
        )
        requested_event_id = f"evt_bus_attempt_{ordinal}{suffix}_requested"
        for version, (event_type, state) in enumerate(state_events, start=1):
            event = self.service._event(
                event_type,
                {"attempt_id": attempt_id, "state": state, "version": version},
                event_id=f"evt_bus_attempt_{ordinal}{suffix}_{state}",
            )
            command = self.service._command(
                command_name=f"test.bus-attempt-{state}@1",
                scope_key=aggregate_id,
                idempotency_key=f"{state}@1",
                aggregate_type="aci.agent-attempt",
                aggregate_id=aggregate_id,
                expected_version=version - 1,
                authority={"principal_id": "test-bus-harness"},
                intent={"attempt_id": attempt_id, "state": state, "version": version},
            )

            def mutate(conn, records, _receipt, current_state=state, current_version=version):
                record = records[0]
                if current_version == 1:
                    conn.execute(
                        """
                        INSERT INTO runtime_agent_attempts(
                          attempt_id,dispatch_id,graph_id,aggregate_id,operation_id,seat_id,
                          agent_instance_id,turn_ordinal,state,version,requested_event_id,
                          last_event_id,last_offset
                        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
                        """,
                        (
                            attempt_id,
                            mapping["dispatch_id"],
                            self.graph["graph_id"],
                            aggregate_id,
                            mapping["source_operation_id"],
                            mapping["source_seat_id"],
                            f"agent_instance_bus_{ordinal}{suffix}",
                            mapping["source_turn_ordinal"],
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
                            attempt_id,
                            current_version - 1,
                        ),
                    )
                    if changed.rowcount != 1:
                        raise VersionConflict("test attempt lifecycle CAS lost")

            self.service.journal.accept(
                command,
                [event],
                next_state={"attempt_id": attempt_id, "state": state, "version": version},
                mutate=mutate,
            )
        with self.service.database.connect() as conn:
            return dict(
                conn.execute(
                    "SELECT * FROM runtime_agent_attempts WHERE attempt_id=?", (attempt_id,)
                ).fetchone()
            )

    def _create_group_phase(self, ordinal: int) -> dict:
        mapping = self._mapping(ordinal)
        group_id = mapping["source_group_id"]
        aggregate_id = derive_group_aggregate_id(
            run_id=self.run["run_id"],
            graph_id=self.graph["graph_id"],
            group_id=group_id,
            group_version=1,
        )
        transitions = [("group.started", "collecting")]
        if ordinal == 1:
            transitions.extend(
                (("collection.closed", "revealing"), ("reveal.published", "deliberating"))
            )
        for version, (event_type, state) in enumerate(transitions, start=1):
            event = self.service._event(
                event_type,
                {
                    "graph_id": self.graph["graph_id"],
                    "group_id": group_id,
                    "harness_only": True,
                    "state": state,
                    "version": version,
                },
                event_id=f"evt_bus_group_{ordinal}_{state}",
            )
            command = self.service._command(
                command_name=f"test.bus-group-{state}@1",
                scope_key=aggregate_id,
                idempotency_key=f"{state}@1",
                aggregate_type="aci.runtime-group",
                aggregate_id=aggregate_id,
                expected_version=version - 1,
                authority={"principal_id": "test-bus-harness", "harness_only": True},
                intent={
                    "graph_id": self.graph["graph_id"],
                    "group_id": group_id,
                    "state": state,
                },
            )

            def mutate(conn, records, _receipt, current_state=state, current_version=version):
                record = records[0]
                if current_version == 1:
                    conn.execute(
                        """
                        INSERT INTO runtime_group_heads(
                          graph_id,group_id,group_version,state,version,last_event_id,last_offset
                        ) VALUES(?,?,?,?,?,?,?)
                        """,
                        (
                            self.graph["graph_id"],
                            group_id,
                            1,
                            current_state,
                            current_version,
                            record.event_id,
                            record.journal_offset,
                        ),
                    )
                else:
                    changed = conn.execute(
                        """
                        UPDATE runtime_group_heads
                        SET state=?,version=?,last_event_id=?,last_offset=?
                        WHERE graph_id=? AND group_id=? AND group_version=1 AND version=?
                        """,
                        (
                            current_state,
                            current_version,
                            record.event_id,
                            record.journal_offset,
                            self.graph["graph_id"],
                            group_id,
                            current_version - 1,
                        ),
                    )
                    if changed.rowcount != 1:
                        raise VersionConflict("test Group phase CAS lost")

            self.service.journal.accept(
                command,
                [event],
                next_state={"group_id": group_id, "state": state, "version": version},
                mutate=mutate,
            )
        with self.service.database.connect() as conn:
            return dict(
                conn.execute(
                    """
                    SELECT * FROM runtime_group_heads
                    WHERE graph_id=? AND group_id=? AND group_version=1
                    """,
                    (self.graph["graph_id"], group_id),
                ).fetchone()
            )

    def _create_candidate(
        self,
        ordinal: int,
        attempt: dict,
        suffix: str = "",
        replies: tuple[str, ...] = (),
    ) -> dict:
        mapping = self._mapping(ordinal)
        message_id = mapping["source_message_id"]
        group_aggregate_id = derive_group_aggregate_id(
            run_id=self.run["run_id"],
            graph_id=self.graph["graph_id"],
            group_id=mapping["source_group_id"],
            group_version=1,
        )
        candidate_id = f"candidate_bus_{ordinal}{suffix}"
        publication_key = f"publish-{ordinal}{suffix}@1"
        aggregate_id = attempt["aggregate_id"]
        event_id = f"evt_bus_publication_{ordinal}{suffix}"
        payload_artifact = self.service.artifacts.prepare(
            canonical_bytes({"content": f"bus payload {ordinal}{suffix}"}),
            media_type="application/json",
            schema_ref="aci.bus-contribution@1",
            classification="sensitive-output",
            created_event_id=event_id,
        )
        payload_ref = payload_artifact.artifact_id
        payload_hash = payload_artifact.content_hash
        event = self.service._event(
            "publication.persisted",
            {
                "attempt_id": attempt["attempt_id"],
                "candidate_id": candidate_id,
                "group_aggregate_id": group_aggregate_id,
                "idempotency_key": publication_key,
                "message_id": message_id,
                "message_type": mapping["source_message_type"],
                "operation_id": mapping["source_operation_id"],
                "payload_hash": payload_hash,
                "payload_ref": payload_ref,
                "receipt_version": "1",
                "reply_to_message_ids": list(replies),
                "round_id": mapping["source_round_id"],
                "schema": "aci.publication-persisted@1",
                "seat_id": mapping["source_seat_id"],
                "status": "persisted_candidate",
            },
            event_id=event_id,
        )
        command = self.service._command(
            command_name="test.bus-publication-candidate@1",
            scope_key=aggregate_id,
            idempotency_key=publication_key,
            aggregate_type="aci.agent-attempt",
            aggregate_id=aggregate_id,
            expected_version=attempt["version"],
            authority={"principal_id": "test-bus-harness", "harness_only": True},
            intent={"candidate_id": candidate_id, "message_id": message_id},
        )

        def result_builder(records, _base):
            return {
                "event_id": records[0].event_id,
                "idempotency_key": publication_key,
                "journal_offset": records[0].journal_offset,
                "message_id": message_id,
                "payload_hash": payload_hash,
                "receipt_version": "1",
                "status": "persisted_candidate",
            }

        def mutate(conn, records, receipt_document):
            record = records[0]
            receipt_bytes = canonical_bytes(receipt_document)
            receipt_digest = digest_bytes(receipt_bytes)
            conn.execute(
                """
                INSERT INTO publication_candidates(
                  candidate_id,message_id,publication_event_id,group_aggregate_id,
                  seat_id,round_id,message_type,attempt_id,operation_id,payload_ref,
                  payload_hash,idempotency_key,receipt_bytes,receipt_digest,journal_offset,
                  status,candidate_version,official_accepted_event_id,abandoned_event_id
                ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    candidate_id,
                    message_id,
                    record.event_id,
                    group_aggregate_id,
                    mapping["source_seat_id"],
                    mapping["source_round_id"],
                    mapping["source_message_type"],
                    attempt["attempt_id"],
                    mapping["source_operation_id"],
                    payload_ref,
                    payload_hash,
                    publication_key,
                    receipt_bytes,
                    receipt_digest,
                    record.journal_offset,
                    "active",
                    1,
                    None,
                    None,
                ),
            )
            conn.execute(
                """
                INSERT INTO publication_receipts(
                  event_id,message_id,scope_key,idempotency_key,payload_hash,
                  receipt_bytes,receipt_digest,journal_offset
                ) VALUES(?,?,?,?,?,?,?,?)
                """,
                (
                    record.event_id,
                    message_id,
                    aggregate_id,
                    publication_key,
                    payload_hash,
                    receipt_bytes,
                    receipt_digest,
                    record.journal_offset,
                ),
            )

        self.service.journal.accept(
            command,
            [event],
            next_state={"candidate_id": candidate_id, "state": "active"},
            additional_artifacts=(payload_artifact,),
            result_builder=result_builder,
            mutate=mutate,
        )
        with self.service.database.connect() as conn:
            return dict(
                conn.execute(
                    "SELECT * FROM publication_candidates WHERE candidate_id=?", (candidate_id,)
                ).fetchone()
            )

    def _read_projection(
        self,
        ordinal: int,
        replies: tuple[str, ...] = (),
        *,
        attempt_id: str | None = None,
    ) -> ConfirmedBusProjection:
        mapping = self._mapping(ordinal)
        with self.service.database.connect() as conn:
            if attempt_id is None:
                attempt_row = conn.execute(
                    """
                    SELECT * FROM runtime_agent_attempts
                    WHERE graph_id=? AND seat_id=? AND turn_ordinal=?
                    ORDER BY rowid DESC LIMIT 1
                    """,
                    (
                        self.graph["graph_id"],
                        mapping["source_seat_id"],
                        mapping["source_turn_ordinal"],
                    ),
                ).fetchone()
            else:
                attempt_row = conn.execute(
                    "SELECT * FROM runtime_agent_attempts WHERE attempt_id=?", (attempt_id,)
                ).fetchone()
            attempt = dict(attempt_row)
            candidate = dict(
                conn.execute(
                    "SELECT * FROM publication_candidates WHERE attempt_id=?", (attempt["attempt_id"],)
                ).fetchone()
            )
            receipt = dict(
                conn.execute(
                    "SELECT * FROM publication_receipts WHERE event_id=?",
                    (candidate["publication_event_id"],),
                ).fetchone()
            )
            publication_event = dict(
                conn.execute(
                    "SELECT * FROM events WHERE event_id=?", (candidate["publication_event_id"],)
                ).fetchone()
            )
            publication_command_receipt = dict(
                conn.execute(
                    "SELECT * FROM command_receipts WHERE command_id=?",
                    (publication_event["command_id"],),
                ).fetchone()
            )
            publication_event_payload_artifact = _required_row(
                conn.execute(
                    "SELECT * FROM artifacts WHERE artifact_id=?",
                    (publication_event["payload_ref"],),
                ).fetchone(),
                "publication event payload artifact",
            )
            contribution_artifact = _required_row(
                conn.execute(
                    "SELECT * FROM artifacts WHERE artifact_id=?", (candidate["payload_ref"],)
                ).fetchone(),
                "contribution artifact",
            )
            group_head = dict(
                conn.execute(
                    """
                    SELECT * FROM runtime_group_heads
                    WHERE graph_id=? AND group_id=? AND group_version=1
                    """,
                    (self.graph["graph_id"], mapping["source_group_id"]),
                ).fetchone()
            )
        return project_confirmed_bus_acceptance(
            mapping=mapping,
            graph=self.graph,
            run=self.run,
            attempt=attempt,
            candidate=candidate,
            publication_receipt=receipt,
            publication_event=publication_event,
            publication_command_receipt=publication_command_receipt,
            publication_event_payload_artifact=publication_event_payload_artifact,
            contribution_artifact=contribution_artifact,
            group_head=group_head,
            parent_principal_id="principal_test_parent",
            reply_to_message_ids=replies,
        )

    def _prepare(self, ordinal: int, *, replies: tuple[str, ...] = ()) -> ConfirmedBusProjection:
        attempt = self._create_completed_attempt(ordinal)
        self._create_group_phase(ordinal)
        self._create_candidate(ordinal, attempt, replies=replies)
        return self._read_projection(ordinal, replies)

    @staticmethod
    def _result_builder(projection: ConfirmedBusProjection):
        def build(records, base):
            return {
                **base,
                "acceptance_id": projection.acceptance_id,
                "mapping_id": projection.mapping_id,
                "message_id": projection.source_message_id,
                "ordered_event_types": [record.event_type for record in records],
                "schema": "aci.confirmed-attempt-result-acceptance-receipt@1",
                "semantic_digest": projection.semantic_digest,
            }

        return build

    def _accept(
        self,
        projection: ConfirmedBusProjection,
        *,
        failpoint=None,
        command_override: RuntimeCommand | None = None,
    ) -> dict:
        command = command_override or RuntimeCommand(
            command_id=projection.command_id,
            scope_key=projection.scope_key,
            idempotency_key=projection.idempotency_key,
            aggregate_type="aci.runtime-group",
            aggregate_id=projection.group_aggregate_id,
            expected_version=projection.group_head_version,
            causation_id=projection.publication_event_id,
            correlation_id=projection.dispatch_id,
            authority_context=projection.authority_context(),
            semantic_intent=projection.semantic_intent(),
        )
        events = [
            self.service._event(
                "attempt.result_accepted",
                projection.attempt_result_payload(),
                event_id=projection.attempt_result_event_id,
            ),
            self.service._event(
                projection.official_event_type,
                projection.official_payload(),
                event_id=projection.official_event_id,
            ),
        ]

        def mutate(conn, records, _receipt):
            mapping = dict(
                conn.execute(
                    "SELECT * FROM continuation_input_mappings WHERE mapping_id=?",
                    (projection.mapping_id,),
                ).fetchone()
            )
            graph = dict(
                conn.execute(
                    "SELECT * FROM confirmed_turn_graphs WHERE graph_id=?", (projection.graph_id,)
                ).fetchone()
            )
            run = dict(
                conn.execute("SELECT * FROM runs WHERE run_id=?", (projection.run_id,)).fetchone()
            )
            attempt = dict(
                conn.execute(
                    "SELECT * FROM runtime_agent_attempts WHERE attempt_id=?",
                    (projection.attempt_id,),
                ).fetchone()
            )
            candidate = dict(
                conn.execute(
                    "SELECT * FROM publication_candidates WHERE candidate_id=?",
                    (projection.candidate_id,),
                ).fetchone()
            )
            publication_receipt = dict(
                conn.execute(
                    "SELECT * FROM publication_receipts WHERE event_id=?",
                    (projection.publication_receipt_event_id,),
                ).fetchone()
            )
            publication_event = dict(
                conn.execute(
                    "SELECT * FROM events WHERE event_id=?",
                    (projection.publication_event_id,),
                ).fetchone()
            )
            publication_command_receipt = dict(
                conn.execute(
                    "SELECT * FROM command_receipts WHERE command_id=?",
                    (publication_event["command_id"],),
                ).fetchone()
            )
            publication_event_payload_artifact = _required_row(
                conn.execute(
                    "SELECT * FROM artifacts WHERE artifact_id=?",
                    (publication_event["payload_ref"],),
                ).fetchone(),
                "publication event payload artifact",
            )
            contribution_artifact = _required_row(
                conn.execute(
                    "SELECT * FROM artifacts WHERE artifact_id=?",
                    (candidate["payload_ref"],),
                ).fetchone(),
                "contribution artifact",
            )
            group_head = dict(
                conn.execute(
                    """
                    SELECT * FROM runtime_group_heads
                    WHERE graph_id=? AND group_id=? AND group_version=?
                    """,
                    (projection.graph_id, projection.group_id, projection.group_version),
                ).fetchone()
            )
            current = project_confirmed_bus_acceptance(
                mapping=mapping,
                graph=graph,
                run=run,
                attempt=attempt,
                candidate=candidate,
                publication_receipt=publication_receipt,
                publication_event=publication_event,
                publication_command_receipt=publication_command_receipt,
                publication_event_payload_artifact=publication_event_payload_artifact,
                contribution_artifact=contribution_artifact,
                group_head=group_head,
                parent_principal_id=projection.parent_principal_id,
                reply_to_message_ids=projection.reply_to_message_ids,
            )
            if current != projection:
                raise ValidationError("transactional authority differs from prepared projection")
            reduced_group = reduce_confirmed_bus_group_pair(
                GroupProjection(projection.required_group_state),
                (records[0].event_type, records[1].event_type),
            )
            if reduced_group.state != projection.required_group_state:
                raise ValidationError("confirmed BUS pair unexpectedly changes Group semantic state")
            attempt_chain = [
                dict(row)
                for row in conn.execute(
                    """
                    SELECT e.event_type,e.aggregate_id,e.aggregate_version,e.event_id,
                           e.journal_offset,e.event_count,e.command_id,r.first_offset,
                           r.last_offset,r.event_count AS receipt_event_count,
                           r.aggregate_id AS receipt_aggregate_id,
                           r.expected_version AS receipt_expected_version
                    FROM events e
                    JOIN command_receipts r ON r.command_id=e.command_id
                    WHERE e.aggregate_id=? AND e.aggregate_version BETWEEN 1 AND 4
                    ORDER BY e.aggregate_version
                    """,
                    (projection.attempt_aggregate_id,),
                )
            ]
            require_attempt_journal_chain(attempt, attempt_chain)
            group_chain = [
                dict(row)
                for row in conn.execute(
                    """
                    SELECT e.event_type,e.aggregate_id,e.aggregate_version,e.event_id,
                           e.journal_offset,e.event_count,e.command_id,r.first_offset,
                           r.last_offset,r.event_count AS receipt_event_count,
                           r.aggregate_id AS receipt_aggregate_id,
                           r.expected_version AS receipt_expected_version
                    FROM events e
                    JOIN command_receipts r ON r.command_id=e.command_id
                    WHERE e.aggregate_id=? AND e.aggregate_version<=?
                    ORDER BY e.aggregate_version
                    """,
                    (projection.group_aggregate_id, projection.group_head_version),
                )
            ]
            require_group_journal_chain(group_head, projection.group_aggregate_id, group_chain)
            if projection.source_message_type == "reviewer.output":
                expected_reply = conn.execute(
                    """
                    SELECT source_message_id FROM continuation_input_mappings
                    WHERE dispatch_id=? AND slot_ordinal=0
                    """,
                    (projection.dispatch_id,),
                ).fetchone()
                if expected_reply is None or projection.reply_to_message_ids != (
                    expected_reply["source_message_id"],
                ):
                    raise ValidationError("review reply differs from exact confirmed author source")
                visible = {
                    row["message_id"]
                    for row in conn.execute(
                        "SELECT message_id FROM messages WHERE message_id IN ({})".format(
                            ",".join("?" for _ in projection.reply_to_message_ids)
                        ),
                        projection.reply_to_message_ids,
                    )
                }
                if visible != set(projection.reply_to_message_ids):
                    raise ValidationError("review reply is not an official visible message")

            changed = conn.execute(
                """
                UPDATE publication_candidates
                SET status='officially_accepted',candidate_version=2,
                    official_accepted_event_id=?
                WHERE candidate_id=? AND status='active' AND candidate_version=1
                  AND official_accepted_event_id IS NULL AND abandoned_event_id IS NULL
                """,
                (records[1].event_id, projection.candidate_id),
            )
            if changed.rowcount != 1:
                raise VersionConflict("publication candidate CAS lost")
            if failpoint:
                failpoint("bus.after_candidate_cas")
            conn.execute(
                """
                INSERT INTO messages(
                  message_id,group_aggregate_id,seat_id,round_id,message_type,payload_ref,
                  payload_hash,source_candidate_id,official_event_id,accepted_offset
                ) VALUES(?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    projection.source_message_id,
                    projection.group_aggregate_id,
                    projection.seat_id,
                    projection.round_id,
                    projection.source_message_type,
                    projection.payload_ref,
                    projection.payload_hash,
                    projection.candidate_id,
                    records[1].event_id,
                    records[1].journal_offset,
                ),
            )
            if failpoint:
                failpoint("bus.after_message")
            conn.execute(
                """
                INSERT INTO runtime_attempt_result_acceptances(
                  acceptance_id,mapping_id,source_message_id,dispatch_id,run_id,graph_id,
                  group_id,group_version,group_aggregate_id,attempt_id,candidate_id,
                  publication_event_id,publication_receipt_event_id,official_message_id,
                  attempt_result_event_id,official_event_id,accepted_offset,
                  parent_principal_id,semantic_digest
                ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    projection.acceptance_id,
                    projection.mapping_id,
                    projection.source_message_id,
                    projection.dispatch_id,
                    projection.run_id,
                    projection.graph_id,
                    projection.group_id,
                    projection.group_version,
                    projection.group_aggregate_id,
                    projection.attempt_id,
                    projection.candidate_id,
                    projection.publication_event_id,
                    projection.publication_receipt_event_id,
                    projection.source_message_id,
                    records[0].event_id,
                    records[1].event_id,
                    records[1].journal_offset,
                    projection.parent_principal_id,
                    projection.semantic_digest,
                ),
            )
            if failpoint:
                failpoint("bus.after_acceptance")
            changed = conn.execute(
                """
                UPDATE runtime_group_heads
                SET version=?,last_event_id=?,last_offset=?
                WHERE graph_id=? AND group_id=? AND group_version=?
                  AND state=? AND version=?
                """,
                (
                    projection.group_head_version + 2,
                    records[1].event_id,
                    records[1].journal_offset,
                    projection.graph_id,
                    projection.group_id,
                    projection.group_version,
                    projection.required_group_state,
                    projection.group_head_version,
                ),
            )
            if changed.rowcount != 1:
                raise VersionConflict("runtime Group head CAS lost")
            generic_group_head = conn.execute(
                "SELECT * FROM aggregate_heads WHERE aggregate_id=?",
                (projection.group_aggregate_id,),
            ).fetchone()
            if (
                generic_group_head is None
                or generic_group_head["aggregate_type"] != "aci.runtime-group"
                or generic_group_head["current_version"] != projection.group_head_version + 2
                or generic_group_head["last_event_id"] != records[1].event_id
                or generic_group_head["last_offset"] != records[1].journal_offset
            ):
                raise ValidationError("generic and composite Group heads differ")
            if failpoint:
                failpoint("bus.after_group_head")

        return self.service.journal.accept(
            command,
            events,
            next_state={
                "group_id": projection.group_id,
                "official_message_id": projection.source_message_id,
                "result": "accepted",
            },
            result_builder=self._result_builder(projection),
            mutate=mutate,
            failpoint=failpoint,
        )

    def _surface(self) -> dict[str, list[tuple]]:
        tables = (
            "events",
            "aggregate_heads",
            "command_receipts",
            "publication_candidates",
            "messages",
            "runtime_attempt_result_acceptances",
            "runtime_group_heads",
            "effect_intents",
        )
        with self.service.database.connect() as conn:
            return {
                table: [tuple(row) for row in conn.execute(f"SELECT * FROM {table} ORDER BY rowid")]
                for table in tables
            }

    def test_migration_015_isolated_and_reopen_idempotent(self) -> None:
        migration_dir = REPO / "implementations/server/runtime/migrations"
        proof_path = self.root / "migration-isolation.sqlite3"
        proof = sqlite3.connect(proof_path)
        proof.row_factory = sqlite3.Row
        proof.execute("PRAGMA foreign_keys=ON")
        try:
            for version in range(1, 15):
                name = sorted(migration_dir.glob(f"{version:03d}_*.sql"))
                self.assertEqual(len(name), 1)
                for statement in name[0].read_text(encoding="utf-8").split(";"):
                    if statement.strip():
                        proof.execute(statement)
            legacy_schema = {
                (row["type"], row["name"]): row["sql"]
                for row in proof.execute(
                    """
                    SELECT type,name,sql FROM sqlite_master
                    WHERE name NOT LIKE 'sqlite_%' ORDER BY type,name
                    """
                )
            }
            legacy_counts = {
                row["name"]: proof.execute(f'SELECT COUNT(*) FROM "{row["name"]}"').fetchone()[0]
                for row in proof.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
                )
            }
            body = (migration_dir / "015_runtime_attempt_result_bus.sql").read_text(
                encoding="utf-8"
            )
            self.assertEqual(body.upper().count("CREATE TABLE "), 1)
            self.assertNotRegex(body.upper(), r"\b(ALTER|DROP|UPDATE|DELETE|INSERT)\b")
            for statement in body.split(";"):
                if statement.strip():
                    proof.execute(statement)
            current_schema = {
                (row["type"], row["name"]): row["sql"]
                for row in proof.execute(
                    """
                    SELECT type,name,sql FROM sqlite_master
                    WHERE name NOT LIKE 'sqlite_%' ORDER BY type,name
                    """
                )
            }
            self.assertEqual(
                set(current_schema) - set(legacy_schema),
                {("table", "runtime_attempt_result_acceptances")},
            )
            self.assertEqual(
                {key: current_schema[key] for key in legacy_schema}, legacy_schema
            )
            self.assertEqual(
                {
                    table: proof.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
                    for table in legacy_counts
                },
                legacy_counts,
            )
            self.assertEqual(
                proof.execute("SELECT COUNT(*) FROM runtime_attempt_result_acceptances").fetchone()[0],
                0,
            )
        finally:
            proof.close()

        with self.service.database.connect() as conn:
            self.assertEqual(conn.execute("PRAGMA user_version").fetchone()[0], 16)
            foreign_keys = {
                (row["from"], row["table"], row["to"])
                for row in conn.execute(
                    "PRAGMA foreign_key_list(runtime_attempt_result_acceptances)"
                )
            }
            self.assertEqual(
                foreign_keys,
                {
                    ("mapping_id", "continuation_input_mappings", "mapping_id"),
                    ("source_message_id", "continuation_input_mappings", "source_message_id"),
                    ("dispatch_id", "confirmed_dispatches", "dispatch_id"),
                    ("run_id", "runs", "run_id"),
                    ("graph_id", "confirmed_turn_graphs", "graph_id"),
                    ("graph_id", "runtime_group_heads", "graph_id"),
                    ("group_id", "runtime_group_heads", "group_id"),
                    ("group_version", "runtime_group_heads", "group_version"),
                    ("attempt_id", "runtime_agent_attempts", "attempt_id"),
                    ("candidate_id", "publication_candidates", "candidate_id"),
                    ("publication_event_id", "events", "event_id"),
                    ("publication_receipt_event_id", "publication_receipts", "event_id"),
                    ("official_message_id", "messages", "message_id"),
                    ("attempt_result_event_id", "events", "event_id"),
                    ("official_event_id", "events", "event_id"),
                    ("accepted_offset", "events", "journal_offset"),
                },
            )
            unique_sets = set()
            for index in conn.execute(
                "PRAGMA index_list(runtime_attempt_result_acceptances)"
            ):
                if index["unique"]:
                    unique_sets.add(
                        tuple(
                            row["name"]
                            for row in conn.execute(f'PRAGMA index_info("{index["name"]}")')
                        )
                    )
            self.assertEqual(
                unique_sets,
                {
                    ("acceptance_id",),
                    ("mapping_id",),
                    ("source_message_id",),
                    ("attempt_id",),
                    ("candidate_id",),
                    ("publication_event_id",),
                    ("publication_receipt_event_id",),
                    ("official_message_id",),
                    ("attempt_result_event_id",),
                    ("official_event_id",),
                    ("accepted_offset",),
                    ("semantic_digest",),
                },
            )
        self.assertEqual(self.service.database.migrate(), [])

    def test_group_aggregate_goldens(self) -> None:
        self.assertEqual(
            derive_group_aggregate_id(
                run_id=self.run["run_id"],
                graph_id=self.graph["graph_id"],
                group_id="group_authoring",
                group_version=1,
            ),
            "grp_d8d509256e173e4ea73eaab30cc26444",
        )
        self.assertEqual(
            derive_group_aggregate_id(
                run_id=self.run["run_id"],
                graph_id=self.graph["graph_id"],
                group_id="group_review",
                group_version=1,
            ),
            "grp_a3dcb826909707df51d640c654835aaa",
        )

    def test_source_identity_and_event_type_derive_from_confirmed_mapping(self) -> None:
        author = self._prepare(0)
        self.assertEqual(author.source_message_id, self._mapping(0)["source_message_id"])
        self.assertEqual(author.official_event_type, "position.accepted")
        self.assertEqual(author.required_group_state, "collecting")
        self.tearDown()
        self.setUp()
        attempt = self._create_completed_attempt(1)
        self._create_group_phase(1)
        reply = self._mapping(0)["source_message_id"]
        self._create_candidate(1, attempt, replies=(reply,))
        reviewer = self._read_projection(1, (reply,))
        self.assertEqual(reviewer.source_message_id, self._mapping(1)["source_message_id"])
        self.assertEqual(reviewer.official_event_type, "critique.accepted")
        self.assertEqual(reviewer.required_group_state, "deliberating")

    def test_attempt_result_link_does_not_reduce_group_before_official_self_transition(self) -> None:
        for state, official in (
            ("collecting", "position.accepted"),
            ("deliberating", "critique.accepted"),
        ):
            with self.subTest(state=state):
                current = GroupProjection(state)
                self.assertEqual(
                    reduce_confirmed_bus_group_pair(
                        current, ("attempt.result_accepted", official)
                    ),
                    current,
                )
        for pair in (
            ("position.accepted", "attempt.result_accepted"),
            ("attempt.result_accepted", "collection.closed"),
            ("attempt.result_accepted",),
        ):
            with self.subTest(pair=pair), self.assertRaises(ValidationError):
                reduce_confirmed_bus_group_pair(GroupProjection("collecting"), pair)

    def test_every_named_authority_discriminator_fails_closed(self) -> None:
        projection = self._prepare(0)
        with self.service.database.connect() as conn:
            mapping = dict(
                conn.execute(
                    "SELECT * FROM continuation_input_mappings WHERE mapping_id=?",
                    (projection.mapping_id,),
                ).fetchone()
            )
            graph = dict(conn.execute("SELECT * FROM confirmed_turn_graphs").fetchone())
            run = dict(conn.execute("SELECT * FROM runs").fetchone())
            attempt = dict(
                conn.execute(
                    "SELECT * FROM runtime_agent_attempts WHERE attempt_id=?",
                    (projection.attempt_id,),
                ).fetchone()
            )
            candidate = dict(
                conn.execute(
                    "SELECT * FROM publication_candidates WHERE candidate_id=?",
                    (projection.candidate_id,),
                ).fetchone()
            )
            publication_receipt = dict(
                conn.execute(
                    "SELECT * FROM publication_receipts WHERE event_id=?",
                    (projection.publication_event_id,),
                ).fetchone()
            )
            publication_event = dict(
                conn.execute(
                    "SELECT * FROM events WHERE event_id=?", (projection.publication_event_id,)
                ).fetchone()
            )
            publication_command_receipt = dict(
                conn.execute(
                    "SELECT * FROM command_receipts WHERE command_id=?",
                    (publication_event["command_id"],),
                ).fetchone()
            )
            publication_event_payload_artifact = dict(
                conn.execute(
                    "SELECT * FROM artifacts WHERE artifact_id=?",
                    (publication_event["payload_ref"],),
                ).fetchone()
            )
            contribution_artifact = dict(
                conn.execute(
                    "SELECT * FROM artifacts WHERE artifact_id=?", (projection.payload_ref,)
                ).fetchone()
            )
            group_head = dict(
                conn.execute(
                    "SELECT * FROM runtime_group_heads WHERE graph_id=? AND group_id=?",
                    (projection.graph_id, projection.group_id),
                ).fetchone()
            )
        base = {
            "mapping": mapping,
            "graph": graph,
            "run": run,
            "attempt": attempt,
            "candidate": candidate,
            "publication_receipt": publication_receipt,
            "publication_event": publication_event,
            "publication_command_receipt": publication_command_receipt,
            "publication_event_payload_artifact": publication_event_payload_artifact,
            "contribution_artifact": contribution_artifact,
            "group_head": group_head,
            "parent_principal_id": "principal_test_parent",
            "reply_to_message_ids": (),
        }
        cases = (
            ("mapping_identity", "mapping", "mapping_id", self._mapping(1)["mapping_id"]),
            ("mapping_version", "mapping", "mapping_version", 2),
            ("mapping_digest", "mapping", "confirmed_binding_digest", "sha256:" + "9" * 64),
            ("target_seat", "mapping", "target_seat_id", "seat_wrong"),
            ("target_turn", "mapping", "target_turn_ordinal", 99),
            ("slot_name", "mapping", "slot_name", "slot_wrong"),
            ("visibility_policy", "mapping", "visibility_policy_ref_json", "{}"),
            ("source_message", "mapping", "source_message_id", "msg_wrong"),
            ("run", "run", "run_id", "run_wrong"),
            ("graph", "graph", "graph_id", "graph_wrong"),
            ("group", "mapping", "source_group_id", "group_wrong"),
            ("group_version", "group_head", "group_version", 2),
            ("group_aggregate", "candidate", "group_aggregate_id", "grp_wrong"),
            ("attempt_state", "attempt", "state", "requested"),
            ("attempt_seat", "attempt", "seat_id", "seat_wrong"),
            ("attempt_turn", "attempt", "turn_ordinal", 99),
            ("attempt_operation", "attempt", "operation_id", "operation_wrong"),
            ("candidate_identity", "candidate", "candidate_id", "candidate_wrong"),
            ("receipt_identity", "publication_receipt", "event_id", "evt_wrong"),
            ("publication_aggregate_type", "publication_event", "aggregate_type", "wrong"),
            ("publication_aggregate_id", "publication_event", "aggregate_id", "agg_wrong"),
            ("publication_aggregate_version", "publication_event", "aggregate_version", 99),
            ("publication_command_aggregate", "publication_command_receipt", "aggregate_id", "agg_wrong"),
            ("publication_command_version", "publication_command_receipt", "expected_version", 99),
            ("payload", "candidate", "payload_hash", "sha256:" + "8" * 64),
            ("message_type", "mapping", "source_message_type", "unknown.output"),
            ("round", "mapping", "source_round_id", "round_wrong"),
            ("phase", "group_head", "state", "pending"),
        )
        before = self._surface()
        for label, member, field, value in cases:
            with self.subTest(label=label):
                inputs = deepcopy(base)
                inputs[member][field] = value
                if label == "attempt_state":
                    inputs["attempt"]["version"] = 1
                with self.assertRaises(ValidationError):
                    project_confirmed_bus_acceptance(**inputs)
                self.assertEqual(before, self._surface())

        reviewer_mapping = self._mapping(1)
        reviewer_inputs = deepcopy(base)
        reviewer_inputs["mapping"] = reviewer_mapping
        with self.assertRaises(ValidationError):
            project_confirmed_bus_acceptance(**reviewer_inputs)

    def test_candidate_only_is_not_official_or_continuation_visible(self) -> None:
        self._prepare(0)
        with self.service.database.connect() as conn:
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM messages").fetchone()[0], 0)
            self.assertEqual(
                conn.execute("SELECT COUNT(*) FROM runtime_attempt_result_acceptances").fetchone()[0],
                0,
            )
            source_ids = [row["source_message_id"] for row in conn.execute("SELECT * FROM continuation_input_mappings")]
            visible = conn.execute(
                "SELECT COUNT(*) FROM messages WHERE message_id IN (?,?)", source_ids
            ).fetchone()[0]
            self.assertEqual(visible, 0)

    def test_author_official_pair_and_zero_effects(self) -> None:
        projection = self._prepare(0)
        with self.service.database.connect() as conn:
            attempt_head_before = dict(
                conn.execute(
                    "SELECT * FROM aggregate_heads WHERE aggregate_id=?",
                    (projection.attempt_aggregate_id,),
                ).fetchone()
            )
        receipt = self._accept(projection)
        self.assertEqual(
            receipt["ordered_event_types"], ["attempt.result_accepted", "position.accepted"]
        )
        with self.service.database.connect() as conn:
            self.assertEqual(
                conn.execute("SELECT message_id FROM messages").fetchone()[0],
                projection.source_message_id,
            )
            row = dict(conn.execute("SELECT * FROM runtime_attempt_result_acceptances").fetchone())
            self.assertEqual(row["mapping_id"], projection.mapping_id)
            group_head = dict(
                conn.execute(
                    "SELECT * FROM runtime_group_heads WHERE graph_id=? AND group_id=?",
                    (projection.graph_id, projection.group_id),
                ).fetchone()
            )
            generic_group_head = dict(
                conn.execute(
                    "SELECT * FROM aggregate_heads WHERE aggregate_id=?",
                    (projection.group_aggregate_id,),
                ).fetchone()
            )
            accepted_events = [
                dict(row)
                for row in conn.execute(
                    "SELECT * FROM events WHERE command_id=? ORDER BY event_ordinal",
                    (projection.command_id,),
                )
            ]
            self.assertEqual(
                [event["aggregate_type"] for event in accepted_events],
                ["aci.runtime-group", "aci.runtime-group"],
            )
            self.assertEqual(
                [event["aggregate_id"] for event in accepted_events],
                [projection.group_aggregate_id, projection.group_aggregate_id],
            )
            self.assertEqual(
                [event["aggregate_version"] for event in accepted_events],
                [projection.group_head_version + 1, projection.group_head_version + 2],
            )
            self.assertEqual(group_head["state"], projection.required_group_state)
            self.assertEqual(group_head["version"], projection.group_head_version + 2)
            self.assertEqual(group_head["last_event_id"], accepted_events[1]["event_id"])
            self.assertEqual(group_head["last_offset"], accepted_events[1]["journal_offset"])
            self.assertEqual(generic_group_head["current_version"], group_head["version"])
            self.assertEqual(generic_group_head["last_event_id"], group_head["last_event_id"])
            self.assertEqual(generic_group_head["last_offset"], group_head["last_offset"])
            attempt_head_after = dict(
                conn.execute(
                    "SELECT * FROM aggregate_heads WHERE aggregate_id=?",
                    (projection.attempt_aggregate_id,),
                ).fetchone()
            )
            self.assertEqual(attempt_head_after, attempt_head_before)
            self.assertEqual(attempt_head_after["current_version"], 5)
            self.assertEqual(
                conn.execute(
                    "SELECT version FROM runtime_agent_attempts WHERE attempt_id=?",
                    (projection.attempt_id,),
                ).fetchone()[0],
                4,
            )
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM effect_intents").fetchone()[0], 1)
            self.assertEqual(
                conn.execute(
                    "SELECT COUNT(*) FROM effect_intents WHERE effect_type!='audit_opening'"
                ).fetchone()[0],
                0,
            )

    def test_reviewer_official_pair_requires_visible_author(self) -> None:
        author = self._prepare(0)
        self._accept(author)
        reviewer = self._prepare(1, replies=(author.source_message_id,))
        receipt = self._accept(reviewer)
        self.assertEqual(
            receipt["ordered_event_types"], ["attempt.result_accepted", "critique.accepted"]
        )
        with self.service.database.connect() as conn:
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM messages").fetchone()[0], 2)
            self.assertEqual(
                [row[0] for row in conn.execute("SELECT source_message_id FROM runtime_attempt_result_acceptances ORDER BY accepted_offset")],
                [author.source_message_id, reviewer.source_message_id],
            )

    def test_reviewer_without_visible_reply_rejects_before_acceptance(self) -> None:
        attempt = self._create_completed_attempt(1)
        self._create_group_phase(1)
        self._create_candidate(1, attempt)
        with self.assertRaises(ValidationError):
            self._read_projection(1)

    def test_field_by_field_authority_drift_rejects(self) -> None:
        projection = self._prepare(0)
        cases = (
            ("continuation_input_mappings", "mapping_id", projection.mapping_id, "source_round_id", "wrong"),
            ("runtime_agent_attempts", "attempt_id", projection.attempt_id, "operation_id", "wrong"),
            ("publication_candidates", "candidate_id", projection.candidate_id, "payload_hash", "sha256:" + "0" * 64),
            ("runtime_group_heads", "group_id", projection.group_id, "state", "pending"),
        )
        for table, key, identity, field, value in cases:
            with self.subTest(field=field):
                with self.service.database.write() as conn:
                    conn.execute(f"UPDATE {table} SET {field}=? WHERE {key}=?", (value, identity))
                with self.assertRaises(ValidationError):
                    self._read_projection(0)
                # Restore the exact prepared value without accepting anything.
                original = {
                    "source_round_id": projection.round_id,
                    "operation_id": projection.operation_id,
                    "state": "collecting",
                    "payload_hash": projection.payload_hash,
                }[field]
                with self.service.database.write() as conn:
                    conn.execute(f"UPDATE {table} SET {field}=? WHERE {key}=?", (original, identity))
        with self.service.database.connect() as conn:
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM messages").fetchone()[0], 0)

    def test_receipt_bytes_fields_scope_and_digest_fail_closed(self) -> None:
        projection = self._prepare(0)
        with self.service.database.connect() as conn:
            candidate = dict(
                conn.execute(
                    "SELECT * FROM publication_candidates WHERE candidate_id=?",
                    (projection.candidate_id,),
                ).fetchone()
            )
            receipt = dict(
                conn.execute(
                    "SELECT * FROM publication_receipts WHERE event_id=?",
                    (projection.publication_receipt_event_id,),
                ).fetchone()
            )
        original_document = json.loads(candidate["receipt_bytes"])
        cases = []
        for field in (
            "event_id",
            "message_id",
            "journal_offset",
            "payload_hash",
            "idempotency_key",
        ):
            changed = dict(original_document)
            changed[field] = changed[field] + "_drift" if isinstance(changed[field], str) else changed[field] + 1
            cases.append((f"field:{field}", canonical_bytes(changed), None, None))
        missing = dict(original_document)
        missing.pop("event_id")
        cases.append(("missing", canonical_bytes(missing), None, None))
        extra = {**original_document, "transport_replayed": True}
        cases.append(("extra", canonical_bytes(extra), None, None))
        version = {**original_document, "receipt_version": "2"}
        cases.append(("version", canonical_bytes(version), None, None))
        status = {**original_document, "status": "officially_accepted"}
        cases.append(("status", canonical_bytes(status), None, None))
        cases.append(("noncanonical", b" " + candidate["receipt_bytes"], None, None))
        cases.append(("digest", candidate["receipt_bytes"], "sha256:" + "0" * 64, None))
        cases.append(("scope", candidate["receipt_bytes"], None, "scope:drift"))

        for label, changed_bytes, digest_override, scope_override in cases:
            with self.subTest(label=label):
                changed_digest = digest_override or digest_bytes(changed_bytes)
                with self.service.database.write() as conn:
                    conn.execute(
                        """
                        UPDATE publication_candidates SET receipt_bytes=?,receipt_digest=?
                        WHERE candidate_id=?
                        """,
                        (changed_bytes, changed_digest, projection.candidate_id),
                    )
                    conn.execute(
                        """
                        UPDATE publication_receipts
                        SET receipt_bytes=?,receipt_digest=?,scope_key=? WHERE event_id=?
                        """,
                        (
                            changed_bytes,
                            changed_digest,
                            scope_override or receipt["scope_key"],
                            projection.publication_receipt_event_id,
                        ),
                    )

                before = self._surface()
                with self.assertRaises(ValidationError):
                    self._read_projection(0)
                self.assertEqual(before, self._surface())
                with self.service.database.write() as conn:
                    conn.execute(
                        """
                        UPDATE publication_candidates SET receipt_bytes=?,receipt_digest=?
                        WHERE candidate_id=?
                        """,
                        (
                            candidate["receipt_bytes"],
                            candidate["receipt_digest"],
                            projection.candidate_id,
                        ),
                    )
                    conn.execute(
                        """
                        UPDATE publication_receipts
                        SET receipt_bytes=?,receipt_digest=?,scope_key=? WHERE event_id=?
                        """,
                        (
                            receipt["receipt_bytes"],
                            receipt["receipt_digest"],
                            receipt["scope_key"],
                            projection.publication_receipt_event_id,
                        ),
                    )

    def test_coherent_publication_scope_drift_fails_closed(self) -> None:
        projection = self._prepare(0)
        with self.service.database.connect() as conn:
            command_id = conn.execute(
                "SELECT command_id FROM events WHERE event_id=?",
                (projection.publication_event_id,),
            ).fetchone()[0]
        before = self._surface()
        with self.service.database.write() as conn:
            conn.execute(
                "UPDATE publication_receipts SET scope_key='scope:coherent-drift' WHERE event_id=?",
                (projection.publication_receipt_event_id,),
            )
            conn.execute(
                "UPDATE command_receipts SET scope_key='scope:coherent-drift' WHERE command_id=?",
                (command_id,),
            )
        drifted = self._surface()
        self.assertNotEqual(before, drifted)
        with self.assertRaises(ValidationError):
            self._read_projection(0)
        self.assertEqual(drifted, self._surface())

    def test_attempt_journal_chain_mutations_reject_with_zero_acceptance(self) -> None:
        projection = self._prepare(0)
        with self.service.database.connect() as conn:
            attempt = dict(
                conn.execute(
                    "SELECT * FROM runtime_agent_attempts WHERE attempt_id=?",
                    (projection.attempt_id,),
                ).fetchone()
            )
            lifecycle = [
                dict(row)
                for row in conn.execute(
                    "SELECT * FROM events WHERE aggregate_id=? ORDER BY aggregate_version",
                    (projection.attempt_aggregate_id,),
                )
            ]
            receipts = {
                row["command_id"]: dict(row)
                for row in conn.execute(
                    "SELECT * FROM command_receipts WHERE aggregate_id=?",
                    (projection.attempt_aggregate_id,),
                )
            }
        publication_offset = None
        publication_event_id = projection.publication_event_id
        with self.service.database.connect() as conn:
            publication_offset = conn.execute(
                "SELECT journal_offset FROM events WHERE event_id=?", (publication_event_id,)
            ).fetchone()[0]

        mutations = (
            ("requested_event_id", "attempt", "requested_event_id", publication_event_id),
            ("last_event_id", "attempt", "last_event_id", publication_event_id),
            ("last_offset", "attempt", "last_offset", publication_offset),
            ("gapped", "event", "aggregate_version", 9),
            ("wrong_type", "event", "event_type", "publication.persisted"),
            ("wrong_aggregate", "event", "aggregate_id", "aci.agent-attempt:wrong"),
            ("receipt_aggregate", "receipt", "aggregate_id", "aci.agent-attempt:wrong"),
            ("receipt_version", "receipt", "expected_version", 99),
        )
        for label, target, field, value in mutations:
            with self.subTest(label=label):
                event = lifecycle[1]
                receipt_row = receipts[event["command_id"]]
                with self.service.database.write() as conn:
                    if target == "attempt":
                        conn.execute(
                            f"UPDATE runtime_agent_attempts SET {field}=? WHERE attempt_id=?",
                            (value, projection.attempt_id),
                        )
                    elif target == "event":
                        conn.execute(
                            f"UPDATE events SET {field}=? WHERE event_id=?",
                            (value, event["event_id"]),
                        )
                    else:
                        conn.execute(
                            f"UPDATE command_receipts SET {field}=? WHERE command_id=?",
                            (value, event["command_id"]),
                        )
                before = self._surface()
                with self.assertRaises(ValidationError):
                    self._accept(projection)
                self.assertEqual(before, self._surface())
                with self.service.database.write() as conn:
                    if target == "attempt":
                        conn.execute(
                            f"UPDATE runtime_agent_attempts SET {field}=? WHERE attempt_id=?",
                            (attempt[field], projection.attempt_id),
                        )
                    elif target == "event":
                        conn.execute(
                            f"UPDATE events SET {field}=? WHERE event_id=?",
                            (event[field], event["event_id"]),
                        )
                    else:
                        conn.execute(
                            f"UPDATE command_receipts SET {field}=? WHERE command_id=?",
                            (receipt_row[field], event["command_id"]),
                        )

    def test_immutable_publication_event_and_command_result_anchor_candidate(self) -> None:
        projection = self._prepare(0)
        changed_hash = "sha256:" + "7" * 64
        with self.service.database.connect() as conn:
            candidate = dict(
                conn.execute(
                    "SELECT * FROM publication_candidates WHERE candidate_id=?",
                    (projection.candidate_id,),
                ).fetchone()
            )
            publication_receipt = dict(
                conn.execute(
                    "SELECT * FROM publication_receipts WHERE event_id=?",
                    (projection.publication_event_id,),
                ).fetchone()
            )
            publication_event = dict(
                conn.execute(
                    "SELECT * FROM events WHERE event_id=?", (projection.publication_event_id,)
                ).fetchone()
            )
            command_receipt = dict(
                conn.execute(
                    "SELECT * FROM command_receipts WHERE command_id=?",
                    (publication_event["command_id"],),
                ).fetchone()
            )
        changed_document = json.loads(candidate["receipt_bytes"])
        changed_document["payload_hash"] = changed_hash
        changed_bytes = canonical_bytes(changed_document)
        changed_digest = digest_bytes(changed_bytes)
        with self.service.database.write() as conn:
            conn.execute(
                """
                UPDATE publication_candidates
                SET payload_hash=?,receipt_bytes=?,receipt_digest=? WHERE candidate_id=?
                """,
                (changed_hash, changed_bytes, changed_digest, projection.candidate_id),
            )
            conn.execute(
                """
                UPDATE publication_receipts
                SET payload_hash=?,receipt_bytes=?,receipt_digest=? WHERE event_id=?
                """,
                (changed_hash, changed_bytes, changed_digest, projection.publication_event_id),
            )
            conn.execute(
                "UPDATE command_receipts SET result_receipt_json=? WHERE command_id=?",
                (changed_bytes.decode("utf-8"), publication_event["command_id"]),
            )
        before = self._surface()
        with self.assertRaises(ValidationError):
            self._read_projection(0)
        self.assertEqual(before, self._surface())
        with self.service.database.connect() as conn:
            event_artifact = dict(
                conn.execute(
                    "SELECT * FROM artifacts WHERE artifact_id=?",
                    (publication_event["payload_ref"],),
                ).fetchone()
            )
        self.assertEqual(digest_bytes(bytes(event_artifact["body"])), publication_event["payload_hash"])
        self.assertEqual(
            json.loads(command_receipt["result_receipt_json"])["payload_hash"],
            candidate["payload_hash"],
        )
        self.assertEqual(publication_receipt["payload_hash"], candidate["payload_hash"])

    def test_contribution_artifact_missing_tampered_or_tombstoned_rejects(self) -> None:
        cases = ("missing", "body", "hash", "ref", "tombstone")
        for label in cases:
            with self.subTest(label=label):
                if label != cases[0]:
                    self.tearDown()
                    self.setUp()
                projection = self._prepare(0)
                with self.service.database.connect() as conn:
                    artifact = dict(
                        conn.execute(
                            "SELECT * FROM artifacts WHERE artifact_id=?",
                            (projection.payload_ref,),
                        ).fetchone()
                    )
                    event_artifact_id = conn.execute(
                        "SELECT payload_ref FROM events WHERE event_id=?",
                        (projection.publication_event_id,),
                    ).fetchone()[0]
                with self.service.database.write() as conn:
                    if label == "missing":
                        conn.execute("DELETE FROM artifacts WHERE artifact_id=?", (projection.payload_ref,))
                    elif label == "body":
                        conn.execute(
                            "UPDATE artifacts SET body=?,size_bytes=? WHERE artifact_id=?",
                            (b"tampered", len(b"tampered"), projection.payload_ref),
                        )
                    elif label == "hash":
                        conn.execute(
                            "UPDATE artifacts SET content_hash=? WHERE artifact_id=?",
                            ("sha256:" + "9" * 64, projection.payload_ref),
                        )
                    elif label == "ref":
                        conn.execute(
                            "UPDATE publication_candidates SET payload_ref=? WHERE candidate_id=?",
                            (event_artifact_id, projection.candidate_id),
                        )
                    else:
                        conn.execute(
                            """
                            UPDATE artifacts SET tombstoned_at=?,tombstone_reason=?
                            WHERE artifact_id=?
                            """,
                            ("2026-09-01T00:00:00Z", "test", projection.payload_ref),
                        )
                before = self._surface()
                with self.assertRaises(ValidationError):
                    self._read_projection(0)
                self.assertEqual(before, self._surface())
                self.assertEqual(artifact["classification"], "sensitive-output")

    def test_group_phase_chain_and_prepare_accept_swap_fail_closed(self) -> None:
        cases = ("last_event", "last_offset", "event_type", "aggregate", "receipt")
        for label in cases:
            with self.subTest(label=label):
                if label != cases[0]:
                    self.tearDown()
                    self.setUp()
                projection = self._prepare(0)
                with self.service.database.connect() as conn:
                    publication = dict(
                        conn.execute(
                            "SELECT * FROM events WHERE event_id=?",
                            (projection.publication_event_id,),
                        ).fetchone()
                    )
                    group_event = dict(
                        conn.execute(
                            "SELECT * FROM events WHERE event_id=?",
                            (projection.group_head_last_event_id,),
                        ).fetchone()
                    )
                with self.service.database.write() as conn:
                    if label == "last_event":
                        conn.execute(
                            """
                            UPDATE runtime_group_heads SET last_event_id=?
                            WHERE graph_id=? AND group_id=? AND group_version=1
                            """,
                            (publication["event_id"], projection.graph_id, projection.group_id),
                        )
                    elif label == "last_offset":
                        conn.execute(
                            """
                            UPDATE runtime_group_heads SET last_offset=?
                            WHERE graph_id=? AND group_id=? AND group_version=1
                            """,
                            (publication["journal_offset"], projection.graph_id, projection.group_id),
                        )
                    elif label == "event_type":
                        conn.execute(
                            "UPDATE events SET event_type='publication.persisted' WHERE event_id=?",
                            (group_event["event_id"],),
                        )
                    elif label == "aggregate":
                        conn.execute(
                            "UPDATE events SET aggregate_id='aci.runtime-group:wrong' WHERE event_id=?",
                            (group_event["event_id"],),
                        )
                    else:
                        conn.execute(
                            "UPDATE command_receipts SET expected_version=99 WHERE command_id=?",
                            (group_event["command_id"],),
                        )
                before = self._surface()
                with self.assertRaises(ValidationError):
                    self._accept(projection)
                self.assertEqual(before, self._surface())

    def test_replay_and_reopen_return_identical_receipt(self) -> None:
        projection = self._prepare(0)
        first = self._accept(projection)
        before = self._surface()
        replay = self._accept(projection)
        self.assertEqual(first, replay)
        self.assertEqual(before, self._surface())
        reopened = RuntimeService(self.service.settings)
        reopened.open()
        old = self.service
        self.service = reopened
        try:
            self._bind_harness_events()
            self.assertEqual(first, self._accept(projection))
        finally:
            self.service = old

    def test_same_key_semantic_drift_conflicts(self) -> None:
        projection = self._prepare(0)
        self._accept(projection)
        command = RuntimeCommand(
            command_id=projection.command_id,
            scope_key=projection.scope_key,
            idempotency_key=projection.idempotency_key,
            aggregate_type="aci.runtime-group",
            aggregate_id=projection.group_aggregate_id,
            expected_version=projection.group_head_version,
            causation_id=projection.publication_event_id,
            correlation_id=projection.dispatch_id,
            authority_context=projection.authority_context(),
            semantic_intent={**projection.semantic_intent(), "candidate_id": "candidate_drift"},
        )
        with self.assertRaises(IdempotencyConflict):
            self._accept(projection, command_override=command)

    def test_failpoints_roll_back_every_acceptance_boundary(self) -> None:
        labels = (
            "after_event:1",
            "after_event:2",
            "bus.after_candidate_cas",
            "bus.after_message",
            "bus.after_acceptance",
            "bus.after_group_head",
            "after_receipt",
            "before_commit",
        )
        for label in labels:
            with self.subTest(label=label):
                self.tearDown()
                self.setUp()
                projection = self._prepare(0)
                before = self._surface()
                count = 0

                def failpoint(current):
                    nonlocal count
                    if current == "after_event":
                        count += 1
                        current = f"after_event:{count}"
                    if current == label:
                        raise RuntimeError(label)

                with self.assertRaisesRegex(RuntimeError, label.replace(".", r"\.")):
                    self._accept(projection, failpoint=failpoint)
                self.assertEqual(before, self._surface())

    def test_lost_response_retry_returns_original(self) -> None:
        projection = self._prepare(0)
        captured = None

        def failpoint(label):
            nonlocal captured
            if label == "after_commit":
                with self.service.database.connect() as conn:
                    captured = json.loads(
                        conn.execute(
                            "SELECT result_receipt_json FROM command_receipts WHERE scope_key=? AND idempotency_key=?",
                            (projection.scope_key, projection.idempotency_key),
                        ).fetchone()[0]
                    )
                raise RuntimeError("lost response")

        with self.assertRaisesRegex(RuntimeError, "lost response"):
            self._accept(projection, failpoint=failpoint)
        self.assertEqual(captured, self._accept(projection))

    def test_equal_concurrency_converges(self) -> None:
        projection = self._prepare(0)
        barrier = threading.Barrier(2)
        results = []
        failures = []

        def run():
            try:
                barrier.wait()
                results.append(self._accept(projection))
            except Exception as exc:  # pragma: no cover - diagnostic capture
                failures.append(exc)

        threads = [threading.Thread(target=run) for _ in range(2)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual(failures, [])
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], results[1])
        with self.service.database.connect() as conn:
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM runtime_attempt_result_acceptances").fetchone()[0], 1)

    def test_distinct_attempt_candidate_race_has_one_confirmed_winner(self) -> None:
        first_attempt = self._create_completed_attempt(0, "_a")
        second_attempt = self._create_completed_attempt(0, "_b")
        self._create_group_phase(0)
        barrier = threading.Barrier(2)
        winners = []
        failures = []

        def create(attempt, suffix):
            try:
                barrier.wait()
                winners.append(self._create_candidate(0, attempt, suffix))
            except sqlite3.IntegrityError as exc:
                failures.append(exc)

        threads = [
            threading.Thread(target=create, args=(first_attempt, "_a")),
            threading.Thread(target=create, args=(second_attempt, "_b")),
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual(len(winners), 1)
        self.assertEqual(len(failures), 1)
        winner = winners[0]
        projection = self._read_projection(0, attempt_id=winner["attempt_id"])
        self._accept(projection)
        with self.service.database.connect() as conn:
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM publication_candidates").fetchone()[0], 1)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM messages").fetchone()[0], 1)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM runtime_attempt_result_acceptances").fetchone()[0], 1)

    def test_continuation_sources_become_visible_only_as_exact_pair(self) -> None:
        with self.service.database.connect() as conn:
            source_ids = tuple(
                row["source_message_id"]
                for row in conn.execute("SELECT * FROM continuation_input_mappings ORDER BY slot_ordinal")
            )
            self.assertEqual(self.service._continuation_official_facts(conn, source_ids), [])
        author = self._prepare(0)
        self._accept(author)
        with self.service.database.connect() as conn:
            self.assertEqual(
                self.service._continuation_official_facts(conn, source_ids),
                [
                    {
                        "message_id": author.source_message_id,
                        "group_aggregate_id": author.group_aggregate_id,
                        "seat_id": author.seat_id,
                        "round_id": author.round_id,
                        "message_type": author.source_message_type,
                        "operation_id": author.operation_id,
                        "candidate_id": author.candidate_id,
                    }
                ],
            )
        reviewer = self._prepare(1, replies=(author.source_message_id,))
        self._accept(reviewer)
        with self.service.database.connect() as conn:
            expected = sorted(
                [
                    {
                        "message_id": projection.source_message_id,
                        "group_aggregate_id": projection.group_aggregate_id,
                        "seat_id": projection.seat_id,
                        "round_id": projection.round_id,
                        "message_type": projection.source_message_type,
                        "operation_id": projection.operation_id,
                        "candidate_id": projection.candidate_id,
                    }
                    for projection in (author, reviewer)
                ],
                key=lambda fact: (fact["message_id"], fact["candidate_id"]),
            )
            self.assertEqual(self.service._continuation_official_facts(conn, source_ids), expected)
            message_rows = [
                dict(row)
                for row in conn.execute(
                    """
                    SELECT message_id,message_type,payload_ref,payload_hash
                    FROM messages WHERE message_id IN (?,?) ORDER BY message_id
                    """,
                    source_ids,
                )
            ]
            self.assertEqual(
                message_rows,
                sorted(
                    [
                        {
                            "message_id": projection.source_message_id,
                            "message_type": projection.source_message_type,
                            "payload_ref": projection.payload_ref,
                            "payload_hash": projection.payload_hash,
                        }
                        for projection in (author, reviewer)
                    ],
                    key=lambda message: message["message_id"],
                ),
            )
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM agent_continuations").fetchone()[0], 0)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM effective_input_artifacts").fetchone()[0], 0)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM sandbox_launch_effects").fetchone()[0], 0)


if __name__ == "__main__":
    unittest.main()
