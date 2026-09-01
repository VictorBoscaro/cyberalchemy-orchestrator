"""Atomic accepted-command journal and complete-group reader."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable

from .artifacts import ArtifactStore, PreparedArtifact
from .canonical import canonical_digest, canonical_text, digest_bytes, parse_strict_json
from .confirmation import ConfirmationBatch
from .database import RuntimeDatabase
from .errors import (
    ConfirmationObservationConflict,
    ConfirmedAuthorityConflict,
    IdempotencyConflict,
    IntegrityError,
    VersionConflict,
)

CANONICALIZER_PROFILE_ID = "aci.canonical-json"
CANONICALIZER_PROFILE_VERSION = "1"
CANONICALIZER_PROFILE_DIGEST = (
    "sha256:6ed22971449c8ea911f9b885d26b01e6eb2e77f208cd8bc6419dff31d97b7ade"
)


@dataclass(frozen=True)
class PrerequisiteHead:
    aggregate_id: str
    expected_version: int
    state_hash: str


@dataclass(frozen=True)
class EventDraft:
    event_id: str
    event_type: str
    schema_ref: str
    schema_digest: str
    payload: PreparedArtifact
    observed_at: str | None = None


@dataclass(frozen=True)
class RuntimeCommand:
    command_id: str
    scope_key: str
    idempotency_key: str
    aggregate_type: str
    aggregate_id: str
    expected_version: int
    causation_id: str
    correlation_id: str
    authority_context: dict[str, Any]
    semantic_intent: dict[str, Any]
    prerequisites: tuple[PrerequisiteHead, ...] = ()

    @property
    def digest(self) -> str:
        return canonical_digest(
            {
                "scope_key": self.scope_key,
                "idempotency_key": self.idempotency_key,
                "aggregate_type": self.aggregate_type,
                "aggregate_id": self.aggregate_id,
                "expected_version": self.expected_version,
                "causation_id": self.causation_id,
                "correlation_id": self.correlation_id,
                "authority_context": self.authority_context,
                "semantic_intent": self.semantic_intent,
                "prerequisites": [
                    {
                        "aggregate_id": p.aggregate_id,
                        "expected_version": p.expected_version,
                        "state_hash": p.state_hash,
                    }
                    for p in self.prerequisites
                ],
            }
        )


@dataclass(frozen=True)
class CommittedEvent:
    journal_offset: int
    event_id: str
    aggregate_id: str
    aggregate_version: int
    event_type: str
    schema_ref: str
    schema_digest: str
    payload_ref: str
    payload_hash: str
    command_id: str
    event_ordinal: int
    event_count: int


ResultBuilder = Callable[[list[CommittedEvent], dict[str, Any]], dict[str, Any]]
TransactionMutation = Callable[
    [sqlite3.Connection, list[CommittedEvent], dict[str, Any]], None
]
Failpoint = Callable[[str], None]


class RuntimeJournal:
    def __init__(
        self,
        database: RuntimeDatabase,
        artifacts: ArtifactStore,
        *,
        now: Callable[[], datetime] | None = None,
    ) -> None:
        self.database = database
        self.artifacts = artifacts
        self._now = now or (lambda: datetime.now(timezone.utc))
        self._schema_bindings: dict[str, tuple[str, str]] = {}
        self._payload_validators: dict[str, Callable[[dict[str, Any]], None]] = {}

    def bind_event_schemas(
        self, bindings: dict[str, tuple[str, str]]
    ) -> None:
        self._schema_bindings = dict(bindings)

    def bind_payload_validators(
        self, validators: dict[str, Callable[[dict[str, Any]], None]]
    ) -> None:
        self._payload_validators = dict(validators)

    def head(self, aggregate_id: str) -> dict[str, Any]:
        with self.database.connect() as conn:
            row = conn.execute(
                "SELECT * FROM aggregate_heads WHERE aggregate_id=?", (aggregate_id,)
            ).fetchone()
        if not row:
            return {
                "aggregate_id": aggregate_id,
                "current_version": 0,
                "state_hash": canonical_digest({}),
                "last_event_id": None,
                "last_offset": None,
            }
        return dict(row)

    def accept(
        self,
        command: RuntimeCommand,
        events: list[EventDraft],
        *,
        next_state: dict[str, Any],
        additional_artifacts: tuple[PreparedArtifact, ...] = (),
        result_builder: ResultBuilder | None = None,
        mutate: TransactionMutation | None = None,
        failpoint: Failpoint | None = None,
    ) -> dict[str, Any]:
        if not events:
            raise IntegrityError("an accepted command must emit at least one event")
        if command.expected_version < 0:
            raise VersionConflict("negative expected version")
        fp = failpoint or (lambda _: None)
        fp("before_begin")
        committed_result: dict[str, Any] | None = None
        with self.database.write() as conn:
            fp("after_begin")
            existing = conn.execute(
                """
                SELECT command_digest,result_receipt_json
                FROM command_receipts WHERE scope_key=? AND idempotency_key=?
                """,
                (command.scope_key, command.idempotency_key),
            ).fetchone()
            if existing:
                if existing["command_digest"] != command.digest:
                    raise IdempotencyConflict("idempotency key reused with different digest")
                committed_result = json.loads(existing["result_receipt_json"])
            else:
                self._verify_target(conn, command)
                self._verify_prerequisites(conn, command.prerequisites)
                self._verify_event_schemas(events)
                fp("after_validation")

                artifact_refs: list[dict[str, object]] = []
                for prepared in additional_artifacts:
                    artifact_refs.append(self.artifacts.finalize(conn, prepared))
                    fp("after_artifact")
                for draft in events:
                    artifact_refs.append(self.artifacts.finalize(conn, draft.payload))
                    fp("after_artifact")

                ordered_payload_digest = canonical_digest(
                    [draft.payload.content_hash for draft in events]
                )
                authority_json = canonical_text(command.authority_context)
                authority_digest = digest_bytes(authority_json.encode("utf-8"))
                recorded_at = self._now().isoformat()
                records: list[CommittedEvent] = []
                count = len(events)
                for ordinal, draft in enumerate(events):
                    version = command.expected_version + ordinal + 1
                    cursor = conn.execute(
                        """
                        INSERT INTO events(
                          event_id,aggregate_type,aggregate_id,aggregate_version,
                          event_type,schema_ref,schema_digest,
                          canonicalizer_profile_id,canonicalizer_profile_version,
                          canonicalizer_profile_digest,command_id,event_ordinal,event_count,
                          group_digest,causation_id,correlation_id,recorded_at,observed_at,
                          payload_ref,payload_hash,authority_context_json,
                          authority_context_digest
                        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                        """,
                        (
                            draft.event_id,
                            command.aggregate_type,
                            command.aggregate_id,
                            version,
                            draft.event_type,
                            draft.schema_ref,
                            draft.schema_digest,
                            CANONICALIZER_PROFILE_ID,
                            CANONICALIZER_PROFILE_VERSION,
                            CANONICALIZER_PROFILE_DIGEST,
                            command.command_id,
                            ordinal,
                            count,
                            ordered_payload_digest,
                            command.causation_id,
                            command.correlation_id,
                            recorded_at,
                            draft.observed_at,
                            draft.payload.artifact_id,
                            draft.payload.content_hash,
                            authority_json,
                            authority_digest,
                        ),
                    )
                    records.append(
                        CommittedEvent(
                            journal_offset=int(cursor.lastrowid),
                            event_id=draft.event_id,
                            aggregate_id=command.aggregate_id,
                            aggregate_version=version,
                            event_type=draft.event_type,
                            schema_ref=draft.schema_ref,
                            schema_digest=draft.schema_digest,
                            payload_ref=draft.payload.artifact_id,
                            payload_hash=draft.payload.content_hash,
                            command_id=command.command_id,
                            event_ordinal=ordinal,
                            event_count=count,
                        )
                    )
                    fp("after_event")

                state_hash = canonical_digest(next_state)
                final = records[-1]
                if command.expected_version == 0:
                    try:
                        conn.execute(
                            """
                            INSERT INTO aggregate_heads(
                              aggregate_id,aggregate_type,current_version,state_hash,
                              last_event_id,last_offset,reducer_version
                            ) VALUES(?,?,?,?,?,?,?)
                            """,
                            (
                                command.aggregate_id,
                                command.aggregate_type,
                                final.aggregate_version,
                                state_hash,
                                final.event_id,
                                final.journal_offset,
                                "aci.slice0-reducer@1",
                            ),
                        )
                    except sqlite3.IntegrityError as exc:
                        raise VersionConflict("aggregate creation race lost") from exc
                else:
                    updated = conn.execute(
                        """
                        UPDATE aggregate_heads
                        SET current_version=?,state_hash=?,last_event_id=?,last_offset=?
                        WHERE aggregate_id=? AND current_version=?
                        """,
                        (
                            final.aggregate_version,
                            state_hash,
                            final.event_id,
                            final.journal_offset,
                            command.aggregate_id,
                            command.expected_version,
                        ),
                    )
                    if updated.rowcount != 1:
                        raise VersionConflict("aggregate CAS lost")
                fp("after_head")

                base_receipt = {
                    "command_id": command.command_id,
                    "command_digest": command.digest,
                    "status": "accepted",
                    "first_offset": records[0].journal_offset,
                    "last_offset": records[-1].journal_offset,
                    "event_count": count,
                    "ordered_event_ids": [record.event_id for record in records],
                    "ordered_payload_digest": ordered_payload_digest,
                    "artifact_ids": [ref["artifact_id"] for ref in artifact_refs],
                    "recorded_at": recorded_at,
                    "head": {
                        "aggregate_id": command.aggregate_id,
                        "version": final.aggregate_version,
                        "state_hash": state_hash,
                    },
                }
                committed_result = (
                    result_builder(records, base_receipt)
                    if result_builder
                    else base_receipt
                )
                if mutate:
                    mutate(conn, records, committed_result)
                fp("after_mutation")
                result_json = canonical_text(committed_result)
                conn.execute(
                    """
                    INSERT INTO command_receipts(
                      command_id,scope_key,idempotency_key,command_digest,aggregate_id,
                      expected_version,status,result_receipt_json,first_offset,last_offset,
                      event_count,ordered_event_ids_json,ordered_payload_digest,
                      artifact_ids_json,recorded_at
                    ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    """,
                    (
                        command.command_id,
                        command.scope_key,
                        command.idempotency_key,
                        command.digest,
                        command.aggregate_id,
                        command.expected_version,
                        "accepted",
                        result_json,
                        records[0].journal_offset,
                        records[-1].journal_offset,
                        count,
                        canonical_text(base_receipt["ordered_event_ids"]),
                        ordered_payload_digest,
                        canonical_text(base_receipt["artifact_ids"]),
                        recorded_at,
                    ),
                )
                fp("after_receipt")
            fp("before_commit")
        fp("after_commit")
        assert committed_result is not None
        return committed_result

    def accept_confirmed_dispatch(
        self,
        command: RuntimeCommand,
        events: list[EventDraft],
        *,
        batch: ConfirmationBatch,
        artifacts: tuple[PreparedArtifact, ...],
        failpoint: Failpoint | None = None,
    ) -> dict[str, Any]:
        """Accept the closed confirmation unit with identity replay before creation CAS."""

        if command.expected_version != 0 or command.aggregate_type != "run":
            raise VersionConflict("confirmed dispatch must create a run at version zero")
        if len(events) != 2 or [event.event_type for event in events] != [
            "run.created",
            "audit_opening.requested",
        ]:
            raise IntegrityError("confirmed dispatch must emit its exact two-event group")
        if len(artifacts) != 9 or tuple(
            (prepared.schema_ref, prepared.body)
            for prepared in artifacts
        ) != tuple(
            (schema_ref, body)
            for _, schema_ref, body in batch.artifact_documents
        ):
            raise IntegrityError("confirmed dispatch artifact batch is not the closed nine-member unit")

        fp = failpoint or (lambda _: None)
        fp("confirmation.before_begin")
        committed_result: dict[str, Any] | None = None
        with self.database.write() as conn:
            fp("confirmation.after_begin")
            existing_key = conn.execute(
                """
                SELECT command_digest,result_receipt_json
                FROM command_receipts WHERE scope_key=? AND idempotency_key=?
                """,
                (command.scope_key, command.idempotency_key),
            ).fetchone()
            if existing_key:
                if existing_key["command_digest"] != command.digest:
                    raise IdempotencyConflict("idempotency key reused with different digest")
                committed_result = json.loads(existing_key["result_receipt_json"])
            else:
                observation = batch.observation_record
                existing_observation = conn.execute(
                    """
                    SELECT observation_digest FROM confirmation_observations
                    WHERE issuer_ref_json=? AND observation_id=?
                    """,
                    (observation["issuer_ref_json"], observation["observation_id"]),
                ).fetchone()
                if (
                    existing_observation
                    and existing_observation["observation_digest"]
                    != observation["observation_digest"]
                ):
                    raise ConfirmationObservationConflict(
                        "issuer-scoped observation identity has different canonical bytes"
                    )

                dispatch = batch.confirmed_dispatch_record
                existing_dispatch = conn.execute(
                    """
                    SELECT confirmed_authority_digest,accepted_command_id
                    FROM confirmed_dispatches WHERE dispatch_id=?
                    """,
                    (dispatch["dispatch_id"],),
                ).fetchone()
                if existing_dispatch:
                    if (
                        existing_dispatch["confirmed_authority_digest"]
                        != dispatch["confirmed_authority_digest"]
                    ):
                        raise ConfirmedAuthorityConflict(
                            "dispatch identity already has another confirmed authority"
                        )
                    first = conn.execute(
                        "SELECT result_receipt_json FROM command_receipts WHERE command_id=?",
                        (existing_dispatch["accepted_command_id"],),
                    ).fetchone()
                    if not first:
                        raise IntegrityError("confirmed dispatch first receipt is missing")
                    committed_result = json.loads(first["result_receipt_json"])
                else:
                    self._verify_target(conn, command)
                    self._verify_prerequisites(conn, command.prerequisites)
                    self._verify_event_schemas(events)

                    artifact_refs: list[dict[str, object]] = []
                    for (name, _, _), prepared in zip(batch.artifact_documents, artifacts):
                        artifact_refs.append(self.artifacts.finalize(conn, prepared))
                        fp(f"confirmation.after_{name}_artifact")

                    conn.execute(
                        """
                        INSERT INTO confirmation_observations(
                          issuer_ref_json,observation_id,observation_artifact_id,
                          observation_digest,issuer_evidence_ref,issuer_evidence_digest,
                          human_principal_id,channel,observed_at,dispatch_id,
                          dispatch_revision,presented_pending_sheet_digest,
                          presented_dispatch_spec_digest,action
                        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                        """,
                        (
                            observation["issuer_ref_json"], observation["observation_id"],
                            observation["observation_artifact_id"], observation["observation_digest"],
                            observation["issuer_evidence_ref"], observation["issuer_evidence_digest"],
                            observation["human_principal_id"], observation["channel"],
                            observation["observed_at"], observation["dispatch_id"],
                            observation["dispatch_revision"],
                            observation["presented_pending_sheet_digest"],
                            observation["presented_dispatch_spec_digest"], observation["action"],
                        ),
                    )
                    fp("confirmation.after_confirmation_observation")

                    conn.execute(
                        """
                        INSERT INTO confirmed_dispatches(
                          dispatch_id,dispatch_revision,pending_sheet_artifact_id,
                          pending_sheet_digest,dispatch_spec_artifact_id,dispatch_spec_digest,
                          confirmation_observation_artifact_id,confirmation_observation_digest,
                          capability_resolution_artifact_id,capability_resolution_digest,
                          confirmed_turn_graph_artifact_id,confirmed_turn_graph_digest,
                          continuation_mapping_set_artifact_id,continuation_mapping_set_digest,
                          confirmed_authority_artifact_id,confirmed_authority_digest,
                          execution_authority_mode,confirmed_by,confirmed_at,accepted_command_id
                        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                        """,
                        tuple(
                            dispatch[name]
                            for name in (
                                "dispatch_id", "dispatch_revision", "pending_sheet_artifact_id",
                                "pending_sheet_digest", "dispatch_spec_artifact_id", "dispatch_spec_digest",
                                "confirmation_observation_artifact_id", "confirmation_observation_digest",
                                "capability_resolution_artifact_id", "capability_resolution_digest",
                                "confirmed_turn_graph_artifact_id", "confirmed_turn_graph_digest",
                                "continuation_mapping_set_artifact_id", "continuation_mapping_set_digest",
                                "confirmed_authority_artifact_id", "confirmed_authority_digest",
                                "execution_authority_mode", "confirmed_by", "confirmed_at",
                                "accepted_command_id",
                            )
                        ),
                    )
                    fp("confirmation.after_confirmed_dispatch")

                    run = batch.run_record
                    conn.execute(
                        """
                        INSERT INTO runs(
                          run_id,dispatch_id,dispatch_spec_digest,aggregate_version,
                          state,state_hash,opening_state,terminal_event_id
                        ) VALUES(?,?,?,?,?,?,?,?)
                        """,
                        tuple(
                            run[name]
                            for name in (
                                "run_id", "dispatch_id", "dispatch_spec_digest", "aggregate_version",
                                "state", "state_hash", "opening_state", "terminal_event_id",
                            )
                        ),
                    )
                    fp("confirmation.after_run")

                    graph = batch.graph_record
                    conn.execute(
                        """
                        INSERT INTO confirmed_turn_graphs(
                          graph_id,dispatch_id,run_id,dispatch_spec_digest,graph_artifact_id,
                          graph_digest,continuation_id,mapping_set_artifact_id,mapping_set_digest,
                          node_count,edge_count,mapping_count,nodes_json,edges_json,
                          source_messages_json,source_operation_id,source_seat_id,
                          source_turn_ordinal,target_operation_id,target_seat_id,
                          target_turn_ordinal,identity_derivation_ref_json
                        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                        """,
                        tuple(
                            graph[name]
                            for name in (
                                "graph_id", "dispatch_id", "run_id", "dispatch_spec_digest",
                                "graph_artifact_id", "graph_digest", "continuation_id",
                                "mapping_set_artifact_id", "mapping_set_digest", "node_count",
                                "edge_count", "mapping_count", "nodes_json", "edges_json",
                                "source_messages_json", "source_operation_id", "source_seat_id",
                                "source_turn_ordinal", "target_operation_id", "target_seat_id",
                                "target_turn_ordinal", "identity_derivation_ref_json",
                            )
                        ),
                    )
                    fp("confirmation.after_turn_graph")

                    for index, mapping in enumerate(batch.mapping_records):
                        conn.execute(
                            """
                            INSERT INTO continuation_input_mappings(
                              mapping_id,mapping_version,dispatch_id,continuation_id,
                              source_group_id,source_seat_id,source_operation_id,
                              source_turn_ordinal,source_round_id,source_message_id,
                              source_message_type,target_seat_id,target_turn_ordinal,
                              slot_name,slot_ordinal,visibility_policy_ref_json,
                              confirmed_binding_digest
                            ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                            """,
                            (
                                mapping["mapping_id"], mapping["mapping_version"],
                                mapping["dispatch_id"], mapping["continuation_id"],
                                mapping["source_group_id"], mapping["source_seat_id"],
                                mapping["source_operation_id"], mapping["source_turn_ordinal"],
                                mapping["source_round_id"], mapping["source_message_id"],
                                mapping["source_message_type"], mapping["target_seat_id"],
                                mapping["target_turn_ordinal"], mapping["slot_name"],
                                mapping["slot_ordinal"], canonical_text(mapping["visibility_policy_ref"]),
                                mapping["confirmed_binding_digest"],
                            ),
                        )
                        fp(f"confirmation.after_mapping_{index}")

                    ordered_payload_digest = canonical_digest(
                        [event.payload.content_hash for event in events]
                    )
                    authority_json = canonical_text(command.authority_context)
                    authority_context_digest = digest_bytes(authority_json.encode("utf-8"))
                    recorded_at = self._now().isoformat()
                    records: list[CommittedEvent] = []
                    for ordinal, event in enumerate(events):
                        version = ordinal + 1
                        cursor = conn.execute(
                            """
                            INSERT INTO events(
                              event_id,aggregate_type,aggregate_id,aggregate_version,
                              event_type,schema_ref,schema_digest,
                              canonicalizer_profile_id,canonicalizer_profile_version,
                              canonicalizer_profile_digest,command_id,event_ordinal,event_count,
                              group_digest,causation_id,correlation_id,recorded_at,observed_at,
                              payload_ref,payload_hash,authority_context_json,
                              authority_context_digest
                            ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                            """,
                            (
                                event.event_id, command.aggregate_type, command.aggregate_id,
                                version, event.event_type, event.schema_ref, event.schema_digest,
                                CANONICALIZER_PROFILE_ID, CANONICALIZER_PROFILE_VERSION,
                                CANONICALIZER_PROFILE_DIGEST, command.command_id, ordinal, 2,
                                ordered_payload_digest, command.causation_id,
                                command.correlation_id, recorded_at, event.observed_at,
                                event.payload.artifact_id, event.payload.content_hash,
                                authority_json, authority_context_digest,
                            ),
                        )
                        records.append(
                            CommittedEvent(
                                journal_offset=int(cursor.lastrowid),
                                event_id=event.event_id,
                                aggregate_id=command.aggregate_id,
                                aggregate_version=version,
                                event_type=event.event_type,
                                schema_ref=event.schema_ref,
                                schema_digest=event.schema_digest,
                                payload_ref=event.payload.artifact_id,
                                payload_hash=event.payload.content_hash,
                                command_id=command.command_id,
                                event_ordinal=ordinal,
                                event_count=2,
                            )
                        )
                        fp(
                            "confirmation.after_run_created_event"
                            if ordinal == 0
                            else "confirmation.after_audit_opening_requested_event"
                        )

                    state_hash = canonical_digest(batch.next_state)
                    if state_hash != run["state_hash"]:
                        raise IntegrityError("confirmed run state hash differs from reduced state")
                    conn.execute(
                        """
                        INSERT INTO aggregate_heads(
                          aggregate_id,aggregate_type,current_version,state_hash,
                          last_event_id,last_offset,reducer_version
                        ) VALUES(?,?,?,?,?,?,?)
                        """,
                        (
                            command.aggregate_id, "run", 2, state_hash,
                            records[1].event_id, records[1].journal_offset,
                            "aci.confirmed-run-reducer@1",
                        ),
                    )
                    fp("confirmation.after_run_head")

                    effect = batch.effect_intent
                    conn.execute(
                        """
                        INSERT INTO effect_intents(
                          effect_id,command_id,requested_event_id,effect_type,payload_ref,
                          payload_digest,retry_class,status,claim_epoch,claimed_by,
                          attempt_count,outcome_event_id,outcome_digest
                        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
                        """,
                        tuple(
                            effect[name]
                            for name in (
                                "effect_id", "command_id", "requested_event_id", "effect_type",
                                "payload_ref", "payload_digest", "retry_class", "status",
                                "claim_epoch", "claimed_by", "attempt_count", "outcome_event_id",
                                "outcome_digest",
                            )
                        ),
                    )
                    fp("confirmation.after_effect_intent")

                    receipt = {
                        "artifact_ids": [ref["artifact_id"] for ref in artifact_refs],
                        "command_digest": command.digest,
                        "command_id": command.command_id,
                        "confirmed_authority_digest": dispatch["confirmed_authority_digest"],
                        "dispatch_id": dispatch["dispatch_id"],
                        "event_count": 2,
                        "first_offset": records[0].journal_offset,
                        "head": {
                            "aggregate_id": command.aggregate_id,
                            "state_hash": state_hash,
                            "version": 2,
                        },
                        "last_offset": records[1].journal_offset,
                        "ordered_event_ids": [record.event_id for record in records],
                        "ordered_payload_digest": ordered_payload_digest,
                        "receipt_id": batch.receipt_id,
                        "recorded_at": recorded_at,
                        "run_id": run["run_id"],
                        "schema": "aci.confirmed-dispatch-receipt@1",
                        "status": "accepted",
                    }
                    result_json = canonical_text(receipt)
                    conn.execute(
                        """
                        INSERT INTO command_receipts(
                          command_id,scope_key,idempotency_key,command_digest,aggregate_id,
                          expected_version,status,result_receipt_json,first_offset,last_offset,
                          event_count,ordered_event_ids_json,ordered_payload_digest,
                          artifact_ids_json,recorded_at
                        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                        """,
                        (
                            command.command_id, command.scope_key, command.idempotency_key,
                            command.digest, command.aggregate_id, 0, "accepted", result_json,
                            records[0].journal_offset, records[1].journal_offset, 2,
                            canonical_text(receipt["ordered_event_ids"]), ordered_payload_digest,
                            canonical_text(receipt["artifact_ids"]), recorded_at,
                        ),
                    )
                    fp("confirmation.after_receipt")
                    committed_result = receipt
            fp("confirmation.before_commit")
        fp("confirmation.after_commit")
        assert committed_result is not None
        return committed_result

    def replay_confirmed_dispatch_key(
        self, command: RuntimeCommand
    ) -> dict[str, Any] | None:
        """Resolve an already-accepted confirmation key before expensive pure preparation."""

        with self.database.write() as conn:
            existing = conn.execute(
                """
                SELECT command_digest,result_receipt_json
                FROM command_receipts WHERE scope_key=? AND idempotency_key=?
                """,
                (command.scope_key, command.idempotency_key),
            ).fetchone()
            if not existing:
                return None
            if existing["command_digest"] != command.digest:
                raise IdempotencyConflict("idempotency key reused with different digest")
            return json.loads(existing["result_receipt_json"])

    def _verify_target(self, conn: sqlite3.Connection, command: RuntimeCommand) -> None:
        row = conn.execute(
            "SELECT current_version FROM aggregate_heads WHERE aggregate_id=?",
            (command.aggregate_id,),
        ).fetchone()
        current = int(row["current_version"]) if row else 0
        if current != command.expected_version:
            raise VersionConflict(
                f"expected aggregate version {command.expected_version}, found {current}"
            )

    @staticmethod
    def _verify_prerequisites(
        conn: sqlite3.Connection, prerequisites: tuple[PrerequisiteHead, ...]
    ) -> None:
        for prerequisite in prerequisites:
            row = conn.execute(
                "SELECT current_version,state_hash FROM aggregate_heads WHERE aggregate_id=?",
                (prerequisite.aggregate_id,),
            ).fetchone()
            if (
                not row
                or row["current_version"] != prerequisite.expected_version
                or row["state_hash"] != prerequisite.state_hash
            ):
                raise VersionConflict(
                    f"prerequisite head changed: {prerequisite.aggregate_id}"
                )

    def _verify_event_schemas(self, events: list[EventDraft]) -> None:
        decoded: list[dict[str, Any]] = []
        for event in events:
            binding = self._schema_bindings.get(event.event_type)
            if binding is None:
                raise IntegrityError(f"event type is unregistered: {event.event_type}")
            if binding != (event.schema_ref, event.schema_digest):
                raise IntegrityError(f"event schema binding mismatch: {event.event_type}")
            if not event.schema_digest.startswith("sha256:"):
                raise IntegrityError("schema digest must be algorithm-qualified")
            payload = parse_strict_json(event.payload.body)
            decoded.append(payload)
            validator = self._payload_validators.get(event.event_type)
            if validator:
                if not isinstance(payload, dict):
                    raise IntegrityError("event payload must be a JSON object")
                validator(payload)
        types = [event.event_type for event in events]
        if "apt.session_context_rebound" in types:
            if types != ["apt.session_started", "apt.session_context_rebound"]:
                raise IntegrityError("session rollover group shape/order is invalid")
            started, rebound = decoded
            session = started["session"]
            authorization = started["rollover_authorization"]
            if (
                authorization is None
                or session["origin_kind"] != rebound["origin_kind"]
                or session["origin_ref"] != rebound["origin_ref"]
                or session["session_id"] != rebound["successor_session_id"]
                or started["actor_ref"] != rebound["actor_ref"]
                or any(
                    authorization[name] != rebound[name]
                    for name in authorization
                )
            ):
                raise IntegrityError("session rollover group bindings diverge")
        elif (
            "apt.session_started" in types
            and decoded[types.index("apt.session_started")][
                "rollover_authorization"
            ]
            is not None
        ):
            raise IntegrityError("rollover SessionStarted lacks rebound partner")

    def read_complete_groups(
        self, *, after: int = 0, through: int | None = None
    ) -> dict[str, Any]:
        with self.database.connect() as conn:
            receipts = conn.execute(
                "SELECT * FROM command_receipts ORDER BY first_offset"
            ).fetchall()
            verified = self._verify_groups(conn, receipts)
        max_boundary = verified[-1]["last_offset"] if verified else 0
        requested_through = max_boundary if through is None else through
        effective_after = max(
            (group["last_offset"] for group in verified if group["last_offset"] <= after),
            default=0,
        )
        effective_through = max(
            (
                group["last_offset"]
                for group in verified
                if group["last_offset"] <= requested_through
            ),
            default=0,
        )
        selected = [
            group
            for group in verified
            if group["first_offset"] > effective_after
            and group["last_offset"] <= effective_through
        ]
        return {
            "requested_after": after,
            "requested_through": through,
            "effective_after": effective_after,
            "effective_as_of": effective_through,
            "groups": selected,
        }

    def _verify_groups(
        self, conn: sqlite3.Connection, receipts: list[sqlite3.Row]
    ) -> list[dict[str, Any]]:
        groups: list[dict[str, Any]] = []
        expected_first = 1
        seen_event_ids: set[str] = set()
        for receipt in receipts:
            first, last, count = (
                int(receipt["first_offset"]),
                int(receipt["last_offset"]),
                int(receipt["event_count"]),
            )
            if first != expected_first or last - first + 1 != count:
                raise IntegrityError("accepted command groups have a gap or overlap")
            rows = conn.execute(
                """
                SELECT e.*,a.body,a.size_bytes,a.content_hash
                FROM events e JOIN artifacts a ON a.artifact_id=e.payload_ref
                WHERE e.journal_offset BETWEEN ? AND ? ORDER BY e.journal_offset
                """,
                (first, last),
            ).fetchall()
            if len(rows) != count:
                raise IntegrityError("incomplete accepted command group")
            ids = [row["event_id"] for row in rows]
            payload_hashes = [row["payload_hash"] for row in rows]
            if ids != json.loads(receipt["ordered_event_ids_json"]):
                raise IntegrityError("ordered event IDs do not match receipt")
            if len(set(ids)) != count or seen_event_ids.intersection(ids):
                raise IntegrityError("duplicate event identity")
            if [row["event_ordinal"] for row in rows] != list(range(count)):
                raise IntegrityError("event ordinals are not zero-based and contiguous")
            if any(
                row["command_id"] != receipt["command_id"]
                or row["event_count"] != count
                or row["group_digest"] != receipt["ordered_payload_digest"]
                for row in rows
            ):
                raise IntegrityError("event group membership mismatch")
            if canonical_digest(payload_hashes) != receipt["ordered_payload_digest"]:
                raise IntegrityError("ordered payload digest mismatch")
            for row in rows:
                body = bytes(row["body"])
                if (
                    len(body) != row["size_bytes"]
                    or digest_bytes(body) != row["content_hash"]
                    or row["payload_hash"] != row["content_hash"]
                ):
                    raise IntegrityError("event payload artifact digest mismatch")
                if (
                    row["canonicalizer_profile_id"] != CANONICALIZER_PROFILE_ID
                    or row["canonicalizer_profile_version"]
                    != CANONICALIZER_PROFILE_VERSION
                    or row["canonicalizer_profile_digest"]
                    != CANONICALIZER_PROFILE_DIGEST
                ):
                    raise IntegrityError("canonicalizer identity mismatch")
                binding = self._schema_bindings.get(row["event_type"])
                if binding is None:
                    raise IntegrityError("event type is unregistered")
                if binding != (row["schema_ref"], row["schema_digest"]):
                    raise IntegrityError("event schema registry mismatch")
            seen_event_ids.update(ids)
            groups.append(
                {
                    "command_id": receipt["command_id"],
                    "first_offset": first,
                    "last_offset": last,
                    "event_count": count,
                    "ordered_event_ids": ids,
                    "ordered_payload_digest": receipt["ordered_payload_digest"],
                    "events": [
                        {
                            "journal_offset": row["journal_offset"],
                            "event_id": row["event_id"],
                            "aggregate_id": row["aggregate_id"],
                            "aggregate_version": row["aggregate_version"],
                            "event_type": row["event_type"],
                            "schema_ref": row["schema_ref"],
                            "schema_digest": row["schema_digest"],
                            "payload_ref": row["payload_ref"],
                            "payload_hash": row["payload_hash"],
                        }
                        for row in rows
                    ],
                }
            )
            expected_first = last + 1
        event_count = int(conn.execute("SELECT count(*) FROM events").fetchone()[0])
        if event_count != sum(group["event_count"] for group in groups):
            raise IntegrityError("orphan event outside accepted command group")
        return groups

    def verify_store(self) -> dict[str, Any]:
        policy = self.database.verify_policy()
        prefix = self.read_complete_groups()
        with self.database.connect() as conn:
            heads = conn.execute("SELECT * FROM aggregate_heads").fetchall()
            for head in heads:
                event = conn.execute(
                    "SELECT aggregate_version,journal_offset,event_id FROM events WHERE aggregate_id=? ORDER BY aggregate_version DESC LIMIT 1",
                    (head["aggregate_id"],),
                ).fetchone()
                if (
                    not event
                    or event["aggregate_version"] != head["current_version"]
                    or event["journal_offset"] != head["last_offset"]
                    or event["event_id"] != head["last_event_id"]
                ):
                    raise IntegrityError("aggregate head does not match event stream")
        return {
            "policy": policy,
            "accepted_groups": len(prefix["groups"]),
            "effective_as_of": prefix["effective_as_of"],
            "aggregate_heads": len(heads),
        }
