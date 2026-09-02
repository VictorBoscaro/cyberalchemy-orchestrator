"""Composition root and descriptor-bounded ACI/APT vertical-slice commands."""

from __future__ import annotations

import json
import secrets
import sqlite3
from dataclasses import dataclass
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .artifacts import ArtifactStore, PreparedArtifact
from .canonical import (
    canonical_bytes,
    canonical_digest,
    canonical_text,
    digest_bytes,
    parse_strict_json,
)
from .capabilities import CapabilityManager
from .confirmation import (
    AUDIT_OPENING_REQUESTED_SCHEMA_DIGEST,
    RUN_CREATED_SCHEMA_DIGEST,
    build_confirmation_batch,
    decode_confirmation_command,
    derive_id as derive_confirmation_id,
    require_effect_ceiling,
)
from .continuation import (
    SuspensionProjection,
    project_suspension,
    require_exact_zero_official_facts,
    restore_suspension,
)
from .database import RuntimeDatabase
from .errors import (
    AuthorizationError,
    ConflictError,
    ContinuationAuthorityError,
    ContinuationPrerequisiteError,
    IdempotencyConflict,
    IntegrityError,
    NotFoundError,
    UntrustedConfirmationIssuer,
    UntrustedConfirmationObservation,
    ValidationError,
)
from .journal import EventDraft, PrerequisiteHead, RuntimeCommand, RuntimeJournal
from .legacy import StrictLegacySnapshotResolver
from .profiles import ProfileImporter, VerifiedProfile
from .protocol_compilation import ProtocolCompileFailure, ProtocolCompiler
from .projections import ProjectionManager, ProjectionRegistration
from .reference_delivery import (
    DELIVERY_EVIDENCE_SCHEMA,
    TARGET_RESOLUTION_SCHEMA,
    build_effective_input,
    decode_reference_bundle,
    derive_target_identity,
    verify_wrapper,
    wrap_delivery_evidence,
    wrap_target_resolution,
)
from .reveal_delivery import (
    VISIBILITY_POLICY_REF,
    build_effective_input_manifest as build_peer_effective_input_manifest,
    build_peer_entries,
    deterministic_materialize,
    preallocate_effective_input_id,
    validate_invocation_plan,
)

PROFILE_MANIFEST = Path(
    "docs/features/agents-communication-infra/reviews/"
    "2026-07-23-stage-a-freeze/profile-registry-manifest.json"
)

ACI_SCHEMAS = {
    name: (schema, canonical_digest({"schema_ref": schema}))
    for name, schema in {
        "aci.protocol_profile_registered@1": "aci.protocol-profile-registered@1",
        "aci.local_probe_context_activated@1": "aci.local-probe-context-activated@1",
        "publication.persisted": "aci.publication-persisted@1",
        "reference_probe.accepted@1": "aci.reference-probe-accepted@1",
        "publication.candidate_abandoned": "aci.publication-candidate-abandoned@1",
        "orchestration.dispatch_opened@1": "aci.orchestration-dispatch-opened@1",
        "orchestration.dispatch_closed@1": "aci.orchestration-dispatch-closed@1",
        "reference_scout.run_requested@1": "aci.reference-scout-run-requested@1",
        "reference_scout.recommendation_accepted@1": (
            "aci.reference-scout-recommendation-accepted@1"
        ),
        "reference_scout.bundle_committed@1": (
            "aci.reference-scout-bundle-committed@1"
        ),
        "reference_scout.bundle_delivered@1": (
            "aci.reference-scout-bundle-delivered@1"
        ),
        "reference_scout.bundle_delivered_to_agent@1": (
            "aci.reference-scout-bundle-delivered-to-agent@1"
        ),
        "attempt.requested": "aci.attempt-requested@1",
        "collection.closed": "aci.collection-closed@1",
        "reveal.published": "aci.reveal-published@1",
        "peer_input.materialized": "aci.peer-input-materialized@1",
        "reference_scout.terminated@1": "aci.reference-scout-terminated@1",
        "dispatch.ingestion_recorded@1": "aci.dispatch-ingestion-recorded@1",
        "host_workflow.turn_bound@1": "aci.host-workflow-turn-bound@1",
        "host_workflow.turn_terminal@1": "aci.host-workflow-turn-terminal@1",
    }.items()
}
ACI_SCHEMAS.update(
    {
        "run.created": ("aci.run-created@1", RUN_CREATED_SCHEMA_DIGEST),
        "audit_opening.requested": (
            "aci.audit-opening-requested@1",
            AUDIT_OPENING_REQUESTED_SCHEMA_DIGEST,
        ),
        "continuation.suspended": (
            "aci.continuation-suspended@1",
            canonical_digest({"schema_ref": "aci.continuation-suspended@1"}),
        ),
    }
)


@dataclass(frozen=True)
class RuntimeSettings:
    database_path: Path
    repo_root: Path
    ledger_path: Path
    local_pilot_serve_enabled: bool = False
    repo_id: str = "cyberalchemy-orchestrator"
    confirmation_issuer_ref: dict[str, Any] | None = None
    confirmation_host_context: dict[str, Any] | None = None


def _runtime_confirmation_command(value: dict[str, Any]) -> RuntimeCommand:
    """Preserve the complete decoded command in its canonical replay digest."""

    return RuntimeCommand(
        command_id=value["command_id"],
        scope_key=value["scope_key"],
        idempotency_key=value["idempotency_key"],
        aggregate_type=value["aggregate_type"],
        aggregate_id=value["aggregate_id"],
        expected_version=value["expected_version"],
        causation_id=value["causation_id"],
        correlation_id=value["correlation_id"],
        authority_context=value["authority_context"],
        semantic_intent=value["semantic_intent"],
        prerequisites=tuple(
            PrerequisiteHead(
                aggregate_id=prerequisite["aggregate_id"],
                expected_version=prerequisite["expected_version"],
                state_hash=prerequisite["state_hash"],
            )
            for prerequisite in value["prerequisites"]
        ),
    )


class RuntimeService:
    def __init__(
        self,
        settings: RuntimeSettings,
        *,
        now: Callable[[], datetime] | None = None,
        token_factory: Callable[[], str] | None = None,
    ) -> None:
        self.settings = settings
        self.now = now or (lambda: datetime.now(timezone.utc))
        self.database = RuntimeDatabase(settings.database_path)
        self.artifacts = ArtifactStore(self.database, now=self.now)
        self.journal = RuntimeJournal(self.database, self.artifacts, now=self.now)
        self.capabilities = CapabilityManager(
            self.database, now=self.now, token_factory=token_factory
        )
        self.projections = ProjectionManager(self.database)
        self.legacy = StrictLegacySnapshotResolver()
        self.profile_importer = ProfileImporter(settings.repo_root)
        self._profiles: list[VerifiedProfile] = []

    def open(self) -> dict[str, Any]:
        applied = self.database.migrate()
        self._register_projection_ports()
        self._profiles = self.profile_importer.load_manifest(
            self.settings.repo_root / PROFILE_MANIFEST
        )
        bindings = ProfileImporter.event_bindings(self._profiles)
        bindings.update(ACI_SCHEMAS)
        self.journal.bind_event_schemas(bindings)
        self.journal.bind_payload_validators(
            {
                "apt.session_started": self._validate_session_started_event,
                "apt.session_context_rebound": self._validate_session_rebound_event,
                "apt.session_dispatch_linked": self._validate_session_linked_event,
                "orchestration.dispatch_opened@1": self._validate_dispatch_opened_event,
                "orchestration.dispatch_closed@1": self._validate_dispatch_closed_event,
                "reference_scout.run_requested@1": (
                    self._validate_scout_requested_event
                ),
                "reference_scout.recommendation_accepted@1": (
                    self._validate_scout_recommendation_event
                ),
                "reference_scout.bundle_committed@1": (
                    self._validate_scout_bundle_event
                ),
                "reference_scout.bundle_delivered@1": (
                    self._validate_scout_delivery_event
                ),
                "reference_scout.bundle_delivered_to_agent@1": (
                    self._validate_scout_target_delivery_event
                ),
                "attempt.requested": self._validate_attempt_requested_event,
                "reference_scout.terminated@1": (
                    self._validate_scout_terminated_event
                ),
                "dispatch.ingestion_recorded@1": (
                    self._validate_dispatch_ingestion_event
                ),
                "host_workflow.turn_bound@1": (
                    self._validate_host_workflow_turn_bound_event
                ),
                "host_workflow.turn_terminal@1": (
                    self._validate_host_workflow_turn_terminal_event
                ),
            }
        )
        return {"applied_migrations": applied, "policy": self.database.verify_policy()}

    def compile_and_store_dispatch_candidate(self, request_bytes: bytes) -> dict[str, Any]:
        """Compile proposal bytes and optionally persist only an admitted candidate."""

        compiled = ProtocolCompiler().compile_candidate(request_bytes)
        result = parse_strict_json(compiled)
        if result["outcome"] != "compiled":
            return {"compiled_result": result, "artifact_ref": None}
        body = result["candidate_document"].encode("utf-8")
        prepared = self.artifacts.prepare(
            body,
            media_type="application/json",
            schema_ref="aci.dispatch-candidate@1",
            classification="runtime-internal",
        )
        if prepared.content_hash != result["candidate_digest"]:
            raise ProtocolCompileFailure("artifact_content_conflict")
        try:
            artifact_ref = self.artifacts.commit(prepared)
        except ConflictError as exc:
            raise ProtocolCompileFailure("artifact_content_conflict") from exc
        return {"compiled_result": result, "artifact_ref": artifact_ref}

    def confirm_runtime_dispatch(
        self,
        *,
        pending_sheet_bytes: bytes,
        capability_resolution_bytes: bytes,
        capability_resolution_artifact_id: str,
        trusted_issuer_context_bytes: bytes,
        confirmation_observation_bytes: bytes,
        identity_derivation_bytes: bytes,
        payload_schema_bundle_bytes: bytes,
        command_bytes: bytes,
        failpoint: Callable[[str], None] | None = None,
    ) -> dict[str, Any]:
        """Prepare and atomically accept the closed runtime confirmation v1 unit."""

        command_value = decode_confirmation_command(command_bytes)
        preliminary_command = _runtime_confirmation_command(command_value)
        replay = self.journal.replay_confirmed_dispatch_key(preliminary_command)
        if replay is not None:
            return replay

        trusted_context = parse_strict_json(trusted_issuer_context_bytes)
        if not isinstance(trusted_context, dict):
            raise UntrustedConfirmationIssuer("trusted issuer context must be an object")
        if (
            self.settings.confirmation_issuer_ref is None
            or trusted_context.get("admitted_issuer_ref")
            != self.settings.confirmation_issuer_ref
        ):
            raise UntrustedConfirmationIssuer("confirmation issuer is not configured")
        if (
            self.settings.confirmation_host_context is None
            or trusted_context.get("authenticated_host_context")
            != self.settings.confirmation_host_context
        ):
            raise UntrustedConfirmationObservation(
                "confirmation host evidence is not the authenticated configured tuple"
            )

        preview, preview_ref = self.artifacts.get_authorized_with_reference(
            capability_resolution_artifact_id,
            principal_id="runtime-confirmation",
            action="artifact.read",
            authorizer=lambda _principal, _action, classification: (
                classification == "runtime-internal"
            ),
        )
        if preview != capability_resolution_bytes:
            raise IntegrityError("finalized capability preview bytes differ")
        expected_preview_id = "art_" + digest_bytes(preview).removeprefix("sha256:")[:32]
        if capability_resolution_artifact_id != expected_preview_id:
            raise IntegrityError("finalized capability preview reference differs")
        preview_policy = {
            "classification": "runtime-internal",
            "redaction_policy_ref": "aci.redaction.none@1",
            "retention_policy_ref": "aci.retention.local-proof@1",
            "tombstone_policy_ref": "aci.tombstone.retain-digest@1",
            "authorization_policy_ref": "aci.artifact.runtime-operator@1",
        }
        expected_preview_ref = {
            "artifact_id": capability_resolution_artifact_id,
            "content_hash": digest_bytes(capability_resolution_bytes),
            "media_type": "application/json",
            "schema_ref": "aci.capability-resolution@1",
            "classification": "runtime-internal",
            "size_bytes": len(capability_resolution_bytes),
            **preview_policy,
            "policy_bundle_digest": canonical_digest(preview_policy),
        }
        if any(
            preview_ref.get(field) != expected
            for field, expected in expected_preview_ref.items()
        ):
            raise IntegrityError("finalized capability preview metadata differs")
        if not str(preview_ref.get("finalization_receipt_ref", "")).startswith("afr_"):
            raise IntegrityError("finalized capability preview receipt differs")

        batch = build_confirmation_batch(
            repo_root=self.settings.repo_root,
            pending_sheet_bytes=pending_sheet_bytes,
            capability_resolution_bytes=capability_resolution_bytes,
            capability_resolution_artifact_id=capability_resolution_artifact_id,
            trusted_issuer_context_bytes=trusted_issuer_context_bytes,
            confirmation_observation_bytes=confirmation_observation_bytes,
            identity_derivation_bytes=identity_derivation_bytes,
            payload_schema_bundle_bytes=payload_schema_bundle_bytes,
            command_bytes=command_bytes,
        )
        prepared = tuple(
            self.artifacts.prepare(
                body,
                media_type="application/json",
                schema_ref=schema_ref,
                classification="runtime-internal",
            )
            for _, schema_ref, body in batch.artifact_documents
        )
        prepared_by_schema = {artifact.schema_ref: artifact for artifact in prepared}
        command_value = batch.command
        command = _runtime_confirmation_command(command_value)
        dispatch_id = batch.pending_sheet["dispatch_id"]
        dispatch_spec_digest = canonical_digest(batch.dispatch_spec)
        events = [
            EventDraft(
                event_id=derive_confirmation_id(
                    "event",
                    ["run.created", 1],
                    dispatch_id=dispatch_id,
                    dispatch_spec_digest=dispatch_spec_digest,
                ),
                event_type="run.created",
                schema_ref="aci.run-created@1",
                schema_digest=RUN_CREATED_SCHEMA_DIGEST,
                payload=prepared_by_schema["aci.run-created@1"],
            ),
            EventDraft(
                event_id=derive_confirmation_id(
                    "event",
                    ["audit_opening.requested", 2],
                    dispatch_id=dispatch_id,
                    dispatch_spec_digest=dispatch_spec_digest,
                ),
                event_type="audit_opening.requested",
                schema_ref="aci.audit-opening-requested@1",
                schema_digest=AUDIT_OPENING_REQUESTED_SCHEMA_DIGEST,
                payload=prepared_by_schema["aci.audit-opening-requested@1"],
            ),
        ]
        require_effect_ceiling([batch.effect_intent], batch.effect_intent)
        return self.journal.accept_confirmed_dispatch(
            command,
            events,
            batch=batch,
            artifacts=prepared,
            failpoint=failpoint,
        )

    @staticmethod
    def _continuation_json_artifact(
        conn: sqlite3.Connection,
        *,
        artifact_id: str,
        content_hash: str,
        schema_ref: str,
    ) -> dict[str, Any]:
        row = conn.execute(
            "SELECT * FROM artifacts WHERE artifact_id=?", (artifact_id,)
        ).fetchone()
        if not row:
            raise ContinuationAuthorityError("continuation authority artifact is absent")
        body = bytes(row["body"])
        if (
            row["content_hash"] != content_hash
            or digest_bytes(body) != content_hash
            or row["schema_ref"] != schema_ref
            or row["media_type"] != "application/json"
            or row["classification"] != "runtime-internal"
            or row["tombstoned_at"] is not None
        ):
            raise ContinuationAuthorityError("continuation authority artifact differs")
        value = parse_strict_json(body)
        if not isinstance(value, dict):
            raise ContinuationAuthorityError("continuation authority artifact is not an object")
        return value

    @staticmethod
    def _continuation_mapping_rows(
        conn: sqlite3.Connection, continuation_id: str
    ) -> list[dict[str, Any]]:
        rows = [
            dict(row)
            for row in conn.execute(
                """
                SELECT * FROM continuation_input_mappings
                WHERE continuation_id=? ORDER BY slot_ordinal
                """,
                (continuation_id,),
            )
        ]
        for row in rows:
            try:
                row["visibility_policy_ref"] = json.loads(
                    row.pop("visibility_policy_ref_json")
                )
            except (KeyError, json.JSONDecodeError) as exc:
                raise ContinuationAuthorityError(
                    "confirmed continuation mapping policy is invalid"
                ) from exc
        return rows

    @staticmethod
    def _continuation_official_facts(
        conn: sqlite3.Connection, source_message_ids: tuple[str, str]
    ) -> list[dict[str, Any]]:
        return [
            dict(row)
            for row in conn.execute(
                """
                SELECT m.message_id,m.group_aggregate_id,m.seat_id,m.round_id,
                       m.message_type,c.operation_id,c.candidate_id
                FROM messages m
                JOIN publication_candidates c
                  ON c.candidate_id=m.source_candidate_id
                WHERE m.message_id IN (?,?)
                ORDER BY m.message_id,c.candidate_id
                """,
                source_message_ids,
            )
        ]

    @staticmethod
    def _require_attempt_journal_chain(
        conn: sqlite3.Connection, attempt: dict[str, Any]
    ) -> None:
        rows = conn.execute(
            """
            SELECT e.event_type,e.aggregate_version,e.event_id,e.journal_offset,
                   e.event_count,e.command_id,r.first_offset,r.last_offset,r.event_count
                   AS receipt_event_count
            FROM events e
            JOIN command_receipts r ON r.command_id=e.command_id
            WHERE e.aggregate_id=?
            ORDER BY e.aggregate_version
            """,
            (attempt["aggregate_id"],),
        ).fetchall()
        if [row["event_type"] for row in rows] != [
            "attempt.requested",
            "attempt.starting",
            "attempt.running",
            "attempt.completed",
        ]:
            raise ContinuationPrerequisiteError(
                "source attempt does not have the complete journal lifecycle"
            )
        for version, row in enumerate(rows, start=1):
            if (
                row["aggregate_version"] != version
                or row["event_count"] != 1
                or row["receipt_event_count"] != 1
                or row["first_offset"] != row["journal_offset"]
                or row["last_offset"] != row["journal_offset"]
            ):
                raise ContinuationPrerequisiteError(
                    "source attempt lifecycle receipt is incomplete"
                )
        terminal = rows[-1]
        if (
            attempt["version"] != 4
            or attempt["state"] != "completed"
            or attempt["requested_event_id"] != rows[0]["event_id"]
            or attempt["last_event_id"] != terminal["event_id"]
            or attempt["last_offset"] != terminal["journal_offset"]
        ):
            raise ContinuationPrerequisiteError(
                "source attempt terminal projection differs from the journal"
            )

    def _load_new_suspension_projection(
        self,
        conn: sqlite3.Connection,
        *,
        dispatch_id: str,
        continuation_id: str,
        provider_continuation_ref_digest: str | None,
    ) -> tuple[
        SuspensionProjection,
        tuple[str, str],
        str,
        dict[str, Any],
        dict[str, Any],
        str,
    ]:
        authority = conn.execute(
            """
            SELECT d.*,g.graph_id,g.graph_artifact_id,g.graph_digest,g.continuation_id,
                   g.source_operation_id,g.source_seat_id,g.source_turn_ordinal,
                   g.target_operation_id,g.target_seat_id,g.target_turn_ordinal,
                   g.source_messages_json,g.nodes_json,g.mapping_set_artifact_id,
                   g.mapping_set_digest
            FROM confirmed_dispatches d
            JOIN confirmed_turn_graphs g ON g.dispatch_id=d.dispatch_id
            WHERE d.dispatch_id=? AND g.continuation_id=?
            """,
            (dispatch_id, continuation_id),
        ).fetchone()
        if not authority or authority["execution_authority_mode"] != "runtime-managed":
            raise ContinuationAuthorityError("confirmed continuation authority is absent")
        authority = dict(authority)
        dispatch_spec = self._continuation_json_artifact(
            conn,
            artifact_id=authority["dispatch_spec_artifact_id"],
            content_hash=authority["dispatch_spec_digest"],
            schema_ref="aci.dispatch-spec@1",
        )
        authority_document = self._continuation_json_artifact(
            conn,
            artifact_id=authority["confirmed_authority_artifact_id"],
            content_hash=authority["confirmed_authority_digest"],
            schema_ref="aci.confirmed-authority@1",
        )
        graph_document = self._continuation_json_artifact(
            conn,
            artifact_id=authority["graph_artifact_id"],
            content_hash=authority["graph_digest"],
            schema_ref="aci.confirmed-turn-graph@1",
        )
        mapping_document = self._continuation_json_artifact(
            conn,
            artifact_id=authority["mapping_set_artifact_id"],
            content_hash=authority["mapping_set_digest"],
            schema_ref="aci.continuation-input-mapping-set@1",
        )
        if (
            authority_document.get("dispatch_id") != dispatch_id
            or authority_document.get("confirmed_turn_graph_digest")
            != authority["graph_digest"]
            or authority_document.get("mapping_set_digest")
            != authority["mapping_set_digest"]
            or graph_document.get("dispatch_id") != dispatch_id
            or graph_document.get("continuation_bindings", [{}])[0].get(
                "continuation_id"
            )
            != continuation_id
        ):
            raise ContinuationAuthorityError("confirmed continuation documents disagree")

        mappings = self._continuation_mapping_rows(conn, continuation_id)
        if mapping_document.get("mappings") != mappings:
            raise ContinuationAuthorityError("confirmed continuation mapping rows differ")
        try:
            source_messages = tuple(graph_document["source_messages"])
            source_message_ids = tuple(
                message["source_message_id"] for message in source_messages
            )
            nodes = tuple(graph_document["nodes"])
        except (KeyError, TypeError) as exc:
            raise ContinuationAuthorityError("confirmed turn graph is invalid") from exc
        if (
            len(source_message_ids) != 2
            or len(set(source_message_ids)) != 2
            or list(source_messages) != json.loads(authority["source_messages_json"])
            or list(nodes) != json.loads(authority["nodes_json"])
        ):
            raise ContinuationAuthorityError("confirmed turn graph projection differs")
        source_nodes = [
            node
            for node in nodes
            if node.get("operation_id") == authority["source_operation_id"]
        ]
        target_nodes = [
            node
            for node in nodes
            if node.get("operation_id") == authority["target_operation_id"]
        ]
        if (
            len(source_nodes) != 1
            or source_nodes[0].get("role") != "author"
            or source_nodes[0].get("seat_id") != authority["source_seat_id"]
            or source_nodes[0].get("turn_ordinal") != authority["source_turn_ordinal"]
            or len(target_nodes) != 1
            or target_nodes[0].get("role") != "author"
            or target_nodes[0].get("seat_id") != authority["target_seat_id"]
            or target_nodes[0].get("turn_ordinal") != authority["target_turn_ordinal"]
        ):
            raise ContinuationAuthorityError("confirmed author turn binding differs")

        attempts = [
            dict(row)
            for row in conn.execute(
                """
                SELECT * FROM runtime_agent_attempts
                WHERE dispatch_id=? AND graph_id=? AND operation_id=?
                  AND seat_id=? AND turn_ordinal=?
                """,
                (
                    dispatch_id,
                    authority["graph_id"],
                    authority["source_operation_id"],
                    authority["source_seat_id"],
                    authority["source_turn_ordinal"],
                ),
            )
        ]
        if len(attempts) != 1 or attempts[0]["state"] != "completed":
            raise ContinuationPrerequisiteError(
                "exactly one completed confirmed source attempt is required"
            )
        attempt = attempts[0]
        self._require_attempt_journal_chain(conn, attempt)
        target_count = conn.execute(
            """
            SELECT COUNT(*) FROM runtime_agent_attempts
            WHERE dispatch_id=? AND graph_id=? AND operation_id=?
              AND seat_id=? AND turn_ordinal=?
            """,
            (
                dispatch_id,
                authority["graph_id"],
                authority["target_operation_id"],
                authority["target_seat_id"],
                authority["target_turn_ordinal"],
            ),
        ).fetchone()[0]
        if target_count:
            raise ContinuationPrerequisiteError("target attempt already exists")
        snapshot = conn.execute(
            """
            SELECT b.*,a.body,a.schema_ref,a.classification,a.tombstoned_at
            FROM runtime_attempt_snapshot_bindings b
            JOIN artifacts a ON a.artifact_id=b.artifact_id
            WHERE b.attempt_id=?
            """,
            (attempt["attempt_id"],),
        ).fetchone()
        if not snapshot:
            raise ContinuationPrerequisiteError("source reconstruction snapshot is absent")
        snapshot = dict(snapshot)
        if (
            snapshot["terminal_event_id"] != attempt["last_event_id"]
            or snapshot["terminal_offset"] != attempt["last_offset"]
            or digest_bytes(bytes(snapshot["body"])) != snapshot["content_hash"]
            or snapshot["classification"] != "runtime-internal"
            or snapshot["tombstoned_at"] is not None
        ):
            raise ContinuationPrerequisiteError(
                "source reconstruction snapshot binding differs"
            )
        try:
            resume_policy_ref = dispatch_spec["decision_policies"]["reconstruction"][
                "policy_ref"
            ]
            wall_clock_seconds = dispatch_spec["budgets"]["wall_clock_seconds"]
        except (KeyError, TypeError) as exc:
            raise ContinuationAuthorityError(
                "confirmed continuation policy or budget is absent"
            ) from exc
        projection = project_suspension(
            confirmed_authority_digest=authority["confirmed_authority_digest"],
            dispatch_id=dispatch_id,
            continuation_id=continuation_id,
            source_attempt_id=attempt["attempt_id"],
            source_turn_ordinal=authority["source_turn_ordinal"],
            target_turn_ordinal=authority["target_turn_ordinal"],
            seat_id=authority["target_seat_id"],
            agent_instance_id=attempt["agent_instance_id"],
            mappings=mappings,
            context_snapshot_artifact_id=snapshot["artifact_id"],
            context_snapshot_content_hash=snapshot["content_hash"],
            provider_continuation_ref_digest=provider_continuation_ref_digest,
            resume_policy_ref=resume_policy_ref,
            confirmed_at=authority["confirmed_at"],
            wall_clock_seconds=wall_clock_seconds,
        )
        return (
            projection,
            source_message_ids,
            authority["graph_id"],
            attempt,
            snapshot,
            authority["target_operation_id"],
        )

    def _load_persisted_suspension_projection(
        self,
        conn: sqlite3.Connection,
        *,
        dispatch_id: str,
        continuation_id: str,
        provider_continuation_ref_digest: str | None,
    ) -> tuple[SuspensionProjection, str] | None:
        row = conn.execute(
            """
            SELECT c.*
            FROM agent_continuations c
            WHERE c.dispatch_id=? AND c.continuation_id=?
            """,
            (dispatch_id, continuation_id),
        ).fetchone()
        if not row:
            return None
        row = dict(row)
        mappings = [
            {
                "mapping_id": mapping["mapping_id"],
                "slot_ordinal": mapping["member_ordinal"],
                "dispatch_id": row["dispatch_id"],
                "continuation_id": row["continuation_id"],
                "target_seat_id": row["seat_id"],
                "target_turn_ordinal": row["target_turn_ordinal"],
                "confirmed_binding_digest": mapping[
                    "confirmed_binding_digest"
                ],
            }
            for mapping in conn.execute(
                """
                SELECT mapping_id,member_ordinal,confirmed_binding_digest
                FROM agent_continuation_mapping_members
                WHERE continuation_id=?
                ORDER BY member_ordinal
                """,
                (continuation_id,),
            )
        ]
        projection = restore_suspension(
            confirmed_authority_digest=row["confirmed_authority_digest"],
            dispatch_id=row["dispatch_id"],
            continuation_id=row["continuation_id"],
            source_attempt_id=row["source_attempt_id"],
            source_turn_ordinal=row["source_turn_ordinal"],
            target_turn_ordinal=row["target_turn_ordinal"],
            seat_id=row["seat_id"],
            agent_instance_id=row["agent_instance_id"],
            mappings=mappings,
            context_snapshot_artifact_id=row["context_snapshot_artifact_id"],
            context_snapshot_content_hash=row["context_snapshot_content_hash"],
            provider_continuation_ref_digest=provider_continuation_ref_digest,
            resume_policy_ref=json.loads(row["resume_policy_ref_json"]),
            deadline_utc=row["deadline_utc"],
        )
        return projection, row["graph_id"]

    def suspend_agent_continuation(
        self,
        *,
        dispatch_id: str,
        continuation_id: str,
        provider_continuation_ref_digest: str | None = None,
        failpoint: Callable[[str], None] | None = None,
    ) -> dict[str, Any]:
        """Accept one CONF-001-backed, effect-free continuation suspension."""

        fp = failpoint or (lambda _name: None)
        with self.database.connect() as conn:
            persisted = self._load_persisted_suspension_projection(
                conn,
                dispatch_id=dispatch_id,
                continuation_id=continuation_id,
                provider_continuation_ref_digest=provider_continuation_ref_digest,
            )
            if persisted:
                projection, graph_id = persisted
                source_message_ids: tuple[str, str] | None = None
                source_attempt_authority: dict[str, Any] | None = None
                source_snapshot_authority: dict[str, Any] | None = None
                target_operation_id: str | None = None
            else:
                (
                    projection,
                    source_message_ids,
                    graph_id,
                    source_attempt_authority,
                    source_snapshot_authority,
                    target_operation_id,
                ) = (
                    self._load_new_suspension_projection(
                        conn,
                        dispatch_id=dispatch_id,
                        continuation_id=continuation_id,
                        provider_continuation_ref_digest=(
                            provider_continuation_ref_digest
                        ),
                    )
                )
                require_exact_zero_official_facts(
                    self._continuation_official_facts(conn, source_message_ids),
                    source_message_ids,
                )
        if source_message_ids is not None:
            fp("continuation.after_official_precheck")

        scope_key = f"aci.agent-continuation:{projection.continuation_id}"
        command = self._command(
            command_name="aci.suspend-agent-continuation@1",
            scope_key=scope_key,
            idempotency_key="suspend@1",
            aggregate_type="aci.agent-continuation",
            aggregate_id=scope_key,
            expected_version=0,
            authority={
                "confirmed_authority_digest": projection.confirmed_authority_digest,
                "dispatch_id": projection.dispatch_id,
            },
            intent=projection.semantic_intent(),
        )
        event = self._event(
            "continuation.suspended",
            projection.event_payload(),
            event_id=self._stable_id(
                "evt_", ["continuation.suspended", projection.continuation_id]
            ),
        )

        def result_builder(records, base):
            return {
                **base,
                "agent_instance_id": projection.agent_instance_id,
                "confirmed_authority_digest": projection.confirmed_authority_digest,
                "context_snapshot_artifact_id": (
                    projection.context_snapshot_artifact_id
                ),
                "context_snapshot_content_hash": (
                    projection.context_snapshot_content_hash
                ),
                "continuation_id": projection.continuation_id,
                "deadline_utc": projection.deadline_utc,
                "dispatch_id": projection.dispatch_id,
                "ordered_awaited_mapping_ids": list(
                    projection.ordered_mapping_ids
                ),
                "ordered_input_mapping_ids": list(projection.ordered_mapping_ids),
                "provider_continuation_ref_digest": (
                    projection.provider_continuation_ref_digest
                ),
                "resume_policy_ref": projection.resume_policy_ref,
                "schema": "aci.continuation-suspension-receipt@1",
                "seat_id": projection.seat_id,
                "source_attempt_id": projection.source_attempt_id,
                "source_turn_ordinal": projection.source_turn_ordinal,
                "state": "suspended",
                "target_turn_ordinal": projection.target_turn_ordinal,
            }

        def mutate(conn, records, _receipt):
            if source_message_ids is None:
                raise ContinuationAuthorityError(
                    "persisted replay unexpectedly reached continuation mutation"
                )
            if (
                source_attempt_authority is None
                or source_snapshot_authority is None
                or target_operation_id is None
            ):
                raise ContinuationAuthorityError(
                    "source continuation authority was not frozen"
                )
            require_exact_zero_official_facts(
                self._continuation_official_facts(conn, source_message_ids),
                source_message_ids,
            )
            attempt_row = conn.execute(
                """
                SELECT * FROM runtime_agent_attempts
                WHERE attempt_id=?
                """,
                (projection.source_attempt_id,),
            ).fetchone()
            snapshot_row = conn.execute(
                """
                SELECT b.*,a.body,a.schema_ref,a.classification,a.tombstoned_at
                FROM runtime_attempt_snapshot_bindings b
                JOIN artifacts a ON a.artifact_id=b.artifact_id
                WHERE b.attempt_id=?
                """,
                (projection.source_attempt_id,),
            ).fetchone()
            if not attempt_row or not snapshot_row:
                raise ContinuationPrerequisiteError(
                    "source attempt or snapshot changed before acceptance"
                )
            attempt = dict(attempt_row)
            snapshot = dict(snapshot_row)
            if (
                attempt != source_attempt_authority
                or snapshot != source_snapshot_authority
                or attempt["dispatch_id"] != projection.dispatch_id
                or attempt["graph_id"] != graph_id
                or attempt["agent_instance_id"] != projection.agent_instance_id
                or attempt["turn_ordinal"] != projection.source_turn_ordinal
                or snapshot["artifact_id"]
                != projection.context_snapshot_artifact_id
                or snapshot["content_hash"]
                != projection.context_snapshot_content_hash
            ):
                raise ContinuationPrerequisiteError(
                    "source attempt or snapshot authority drifted before acceptance"
                )
            self._require_attempt_journal_chain(conn, attempt)
            if (
                snapshot["terminal_event_id"] != attempt["last_event_id"]
                or snapshot["terminal_offset"] != attempt["last_offset"]
                or digest_bytes(bytes(snapshot["body"])) != snapshot["content_hash"]
                or snapshot["classification"] != "runtime-internal"
                or snapshot["tombstoned_at"] is not None
            ):
                raise ContinuationPrerequisiteError(
                    "source snapshot terminal linkage drifted before acceptance"
                )
            target_count = conn.execute(
                """
                SELECT COUNT(*) FROM runtime_agent_attempts
                WHERE dispatch_id=? AND graph_id=? AND operation_id=?
                  AND seat_id=? AND turn_ordinal=?
                """,
                (
                    projection.dispatch_id,
                    graph_id,
                    target_operation_id,
                    projection.seat_id,
                    projection.target_turn_ordinal,
                ),
            ).fetchone()[0]
            if target_count:
                raise ContinuationPrerequisiteError("target attempt already exists")
            conn.execute(
                """
                INSERT INTO agent_continuations(
                  continuation_id,dispatch_id,graph_id,confirmed_authority_digest,
                  source_attempt_id,source_turn_ordinal,target_turn_ordinal,seat_id,
                  agent_instance_id,context_snapshot_artifact_id,
                  context_snapshot_content_hash,provider_continuation_ref_digest,
                  resume_policy_ref_json,deadline_utc,state,version,
                  suspended_event_id,suspended_offset
                ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    projection.continuation_id,
                    projection.dispatch_id,
                    graph_id,
                    projection.confirmed_authority_digest,
                    projection.source_attempt_id,
                    projection.source_turn_ordinal,
                    projection.target_turn_ordinal,
                    projection.seat_id,
                    projection.agent_instance_id,
                    projection.context_snapshot_artifact_id,
                    projection.context_snapshot_content_hash,
                    projection.provider_continuation_ref_digest,
                    canonical_text(projection.resume_policy_ref),
                    projection.deadline_utc,
                    "suspended",
                    1,
                    records[0].event_id,
                    records[0].journal_offset,
                ),
            )
            fp("continuation.after_continuation")
            for ordinal, mapping in enumerate(projection.ordered_mappings):
                conn.execute(
                    """
                    INSERT INTO agent_continuation_mapping_members(
                      continuation_id,mapping_id,member_ordinal,awaited,
                      confirmed_binding_digest
                    ) VALUES(?,?,?,?,?)
                    """,
                    (
                        projection.continuation_id,
                        mapping["mapping_id"],
                        ordinal,
                        1,
                        mapping["confirmed_binding_digest"],
                    ),
                )
                fp(f"continuation.after_mapping_{ordinal}")

        return self.journal.accept(
            command,
            [event],
            next_state=projection.next_state(),
            result_builder=result_builder,
            mutate=mutate,
            failpoint=fp,
        )

    @staticmethod
    def _require_exact_fields(
        value: Any, fields: set[str], label: str
    ) -> dict[str, Any]:
        if not isinstance(value, dict) or set(value) != fields:
            raise IntegrityError(f"{label} payload shape is invalid")
        return value

    @classmethod
    def _validate_session_started_event(cls, payload: dict[str, Any]) -> None:
        cls._require_exact_fields(
            payload,
            {
                "session",
                "actor_ref",
                "actor_authentication_ref",
                "actor_authentication_digest",
                "rollover_authorization",
            },
            "SessionStarted",
        )
        cls._require_exact_fields(
            payload["session"],
            {
                "session_id",
                "origin_kind",
                "origin_ref",
                "ensure_key",
                "start_operation_id",
                "started_at",
                "initial_name",
            },
            "Session",
        )
        rollover = payload["rollover_authorization"]
        if rollover is None:
            if (
                payload["actor_authentication_ref"] is None
                or payload["actor_authentication_digest"] is None
            ):
                raise IntegrityError("ensure authentication evidence is required")
        else:
            cls._require_exact_fields(
                rollover,
                {
                    "authorization_policy_ref",
                    "authorization_policy_digest",
                    "authorization_evidence_ref",
                    "authorization_evidence_digest",
                },
                "rollover authorization",
            )
            if (
                payload["actor_authentication_ref"] is not None
                or payload["actor_authentication_digest"] is not None
            ):
                raise IntegrityError("rollover authentication slots must be null")

    @classmethod
    def _validate_session_rebound_event(cls, payload: dict[str, Any]) -> None:
        cls._require_exact_fields(
            payload,
            {
                "origin_kind",
                "origin_ref",
                "predecessor_session_id",
                "successor_session_id",
                "rebound_at",
                "actor_ref",
                "authorization_policy_ref",
                "authorization_policy_digest",
                "authorization_evidence_ref",
                "authorization_evidence_digest",
            },
            "SessionContextRebound",
        )

    @classmethod
    def _validate_session_linked_event(cls, payload: dict[str, Any]) -> None:
        cls._require_exact_fields(
            payload,
            {
                "link",
                "origin_kind",
                "origin_ref",
                "dispatch_snapshot_ref",
                "actor_ref",
                "authorization_policy_ref",
                "authorization_policy_digest",
                "authorization_evidence_ref",
                "authorization_evidence_digest",
            },
            "SessionDispatchLinked",
        )
        cls._require_exact_fields(
            payload["link"],
            {
                "session_dispatch_link_id",
                "session_id",
                "dispatch_id",
                "link_operation_id",
                "linked_at",
            },
            "SessionDispatchLink",
        )
        snapshot = cls._require_exact_fields(
            payload["dispatch_snapshot_ref"],
            {"kind", "ledger_row_identity", "row_digest"},
            "DispatchAuthoritySnapshotRef",
        )
        if snapshot["kind"] != "legacy_ledger":
            raise IntegrityError("local link requires legacy_ledger snapshot")
        identity = cls._require_exact_fields(
            snapshot["ledger_row_identity"],
            {
                "dispatch_id",
                "row_kind",
                "appender_identity",
                "contract_version",
                "agent_role_registry_ref",
            },
            "LegacyLedgerRowIdentity",
        )
        if identity["dispatch_id"] != payload["link"]["dispatch_id"]:
            raise IntegrityError("legacy ledger identity dispatch does not match link")
        for field in ("row_kind", "appender_identity", "contract_version"):
            if not isinstance(identity[field], str) or not identity[field]:
                raise IntegrityError(f"legacy ledger identity {field} is malformed")
        role_ref = identity["agent_role_registry_ref"]
        if identity["contract_version"] == "0.7.0":
            if not isinstance(role_ref, dict) or set(role_ref) != {"name", "version", "digest"}:
                raise IntegrityError("0.7.0 ledger identity role registry ref is malformed")
        elif role_ref is not None:
            raise IntegrityError("legacy ledger identity cannot retrofit a role registry ref")
        digest = snapshot["row_digest"]
        if not (
            isinstance(digest, str)
            and digest.startswith("sha256:")
            and len(digest) == 71
            and all(character in "0123456789abcdef" for character in digest[7:])
        ):
            raise IntegrityError("legacy ledger row digest is malformed")

    @classmethod
    def _validate_dispatch_opened_event(cls, payload: dict[str, Any]) -> None:
        cls._require_exact_fields(
            payload,
            {
                "dispatch_id",
                "session_id",
                "opened_at",
                "actor_ref",
                "authority_mode",
                "ledger_path",
                "ledger_digest",
                "row_digest",
                "row_bytes_digest",
                "link_event_id",
                "authorization_evidence_ref",
                "authorization_evidence_digest",
            },
            "OrchestrationDispatchOpened",
        )
        if payload["authority_mode"] != "legacy-managed":
            raise IntegrityError("orchestration bridge authority mode must be legacy-managed")

    @classmethod
    def _validate_host_workflow_turn_bound_event(
        cls, payload: dict[str, Any]
    ) -> None:
        cls._require_exact_fields(
            payload,
            {
                "binding_id",
                "dispatch_id",
                "session_id",
                "parent_row_digest",
                "group_id",
                "seat_index",
                "turn_ordinal",
                "attempt_id",
                "host",
                "operation_kind",
                "prompt_template_digest",
                "workflow_manifest_artifact_id",
                "workflow_manifest_hash",
                "source_artifact_ids",
                "tool_input_digest",
                "host_session_id",
                "tool_use_id",
                "bound_at",
                "actor_ref",
            },
            "HostWorkflowTurnBound",
        )
        if payload["host"] not in {"claude", "codex"}:
            raise IntegrityError("host workflow host is invalid")
        if payload["operation_kind"] not in {"spawn", "followup"}:
            raise IntegrityError("host workflow operation kind is invalid")
        if (
            not isinstance(payload["seat_index"], int)
            or payload["seat_index"] < 0
            or not isinstance(payload["turn_ordinal"], int)
            or payload["turn_ordinal"] < 0
        ):
            raise IntegrityError("host workflow seat/turn is invalid")
        if not isinstance(payload["source_artifact_ids"], list):
            raise IntegrityError("host workflow source artifacts are invalid")

    @classmethod
    def _validate_host_workflow_turn_terminal_event(
        cls, payload: dict[str, Any]
    ) -> None:
        cls._require_exact_fields(
            payload,
            {
                "binding_id",
                "dispatch_id",
                "group_id",
                "seat_index",
                "turn_ordinal",
                "attempt_id",
                "host",
                "state",
                "agent_id",
                "terminal_at",
                "actor_ref",
            },
            "HostWorkflowTurnTerminal",
        )
        if payload["state"] not in {"resolved", "error", "cancelled"}:
            raise IntegrityError("host workflow terminal state is invalid")

    @classmethod
    def _validate_dispatch_closed_event(cls, payload: dict[str, Any]) -> None:
        cls._require_exact_fields(
            payload,
            {
                "dispatch_id",
                "session_id",
                "closed_at",
                "actor_ref",
                "exit_reason",
                "agents_spawned",
                "feedback_prompts",
                "ledger_path",
                "ledger_digest",
                "row_digest",
                "row_bytes_digest",
                "authorization_evidence_ref",
                "authorization_evidence_digest",
            },
            "OrchestrationDispatchClosed",
        )

    @classmethod
    def _validate_scout_requested_event(cls, payload: dict[str, Any]) -> None:
        cls._require_exact_fields(
            payload,
            {
                "scout_run_id",
                "probe_id",
                "session_id",
                "dispatch_id",
                "launch_mode",
                "objective_ref",
                "shape",
                "source_mode",
                "profile_binding",
                "group_aggregate_id",
                "seat_id",
                "attempt_id",
                "operation_id",
                "requested_at",
                "actor_ref",
            },
            "ReferenceScoutRunRequested",
        )
        cls._require_exact_fields(
            payload["profile_binding"],
            {"profile_id", "profile_version", "profile_digest"},
            "ReferenceScoutProfileBinding",
        )
        if (
            payload["launch_mode"] != "dispatch_bound"
            or payload["shape"] not in {"small", "tensioned"}
            or payload["source_mode"]
            not in {"internal", "external", "internal-and-external"}
        ):
            raise IntegrityError("Reference Scout request enum is invalid")

    @classmethod
    def _validate_scout_recommendation_event(
        cls, payload: dict[str, Any]
    ) -> None:
        cls._require_exact_fields(
            payload,
            {
                "scout_run_id",
                "probe_id",
                "recommendation",
                "message_id",
                "publication_event_id",
                "payload_ref",
                "payload_hash",
                "accepted_at",
            },
            "ReferenceScoutRecommendationAccepted",
        )
        cls._require_exact_fields(
            payload["recommendation"],
            {
                "recommendation_id",
                "reference_id",
                "source_class",
                "locator_observed",
                "access_state",
                "found_by_seat_id",
                "evaluated_by_seat_id",
                "evaluation",
                "why_inspect",
                "comparability_state",
            },
            "ReferenceScoutRecommendation",
        )

    @classmethod
    def _validate_scout_bundle_event(cls, payload: dict[str, Any]) -> None:
        cls._require_exact_fields(
            payload,
            {
                "scout_run_id",
                "probe_id",
                "bundle_artifact_id",
                "bundle_digest",
                "recommendation_ids",
                "committed_at",
                "actor_ref",
            },
            "ReferenceScoutBundleCommitted",
        )

    @classmethod
    def _validate_scout_delivery_event(cls, payload: dict[str, Any]) -> None:
        cls._require_exact_fields(
            payload,
            {
                "scout_run_id",
                "probe_id",
                "bundle_artifact_id",
                "bundle_digest",
                "delivered_at",
                "actor_ref",
            },
            "ReferenceScoutBundleDelivered",
        )

    @classmethod
    def _validate_scout_target_delivery_event(
        cls, payload: dict[str, Any]
    ) -> None:
        cls._require_exact_fields(
            payload,
            {
                "agent_reference_delivery_id",
                "dispatch_id",
                "scout_run_id",
                "source_bundle_delivered_event_id",
                "bundle_artifact_id",
                "bundle_digest",
                "recommendation_ids",
                "target_attempt_id",
                "target_seat_id",
                "target_agent_instance_id",
                "effective_input_artifact_id",
                "effective_input_entry_ordinal",
                "effective_input_manifest_hash",
                "visibility_policy_ref",
                "idempotency_key",
            },
            "ReferenceScoutBundleDeliveredToAgent",
        )

    @classmethod
    def _validate_attempt_requested_event(cls, payload: dict[str, Any]) -> None:
        cls._require_exact_fields(
            payload,
            {
                "attempt_id",
                "dispatch_id",
                "operation_id",
                "seat_id",
                "agent_instance_id",
                "provider_ref",
                "adapter_ref",
                "model_ref",
                "effective_input_artifact_id",
                "request_id",
                "request_digest",
                "sandbox_launch_effect_id",
            },
            "AttemptRequested",
        )

    @classmethod
    def _validate_scout_terminated_event(cls, payload: dict[str, Any]) -> None:
        cls._require_exact_fields(
            payload,
            {
                "scout_run_id",
                "probe_id",
                "outcome",
                "reason",
                "terminated_at",
                "actor_ref",
            },
            "ReferenceScoutTerminated",
        )
        if payload["outcome"] not in {"failed", "cancelled"}:
            raise IntegrityError("Reference Scout termination outcome is invalid")

    @classmethod
    def _validate_dispatch_ingestion_event(
        cls, payload: dict[str, Any]
    ) -> None:
        cls._require_exact_fields(
            payload,
            {
                "ingestion_id",
                "session_id",
                "dispatch_id",
                "host",
                "agent_id",
                "tool_use_id",
                "tool_name",
                "source_kind",
                "locator",
                "repo_relative_path",
                "content_digest",
                "artifact_id",
                "media_type",
                "size_bytes",
                "coverage",
                "purpose",
                "observed_at",
            },
            "DispatchIngestionRecorded",
        )
        if payload["host"] not in {"claude", "codex"}:
            raise IntegrityError("dispatch ingestion host is invalid")
        if payload["coverage"] not in {"exact", "metadata_only", "opaque"}:
            raise IntegrityError("dispatch ingestion coverage is invalid")

    def _register_projection_ports(self) -> None:
        def session_reducer(state, event):
            result = dict(state)
            if event["event_type"] == "apt.session_started":
                result["session"] = event["payload"]["session"]
                result.setdefault("dispatch_ids", [])
            elif event["event_type"] == "apt.session_context_rebound":
                result["current_session_id"] = event["payload"]["successor_session_id"]
            elif event["event_type"] == "apt.session_dispatch_linked":
                dispatch_id = event["payload"]["link"]["dispatch_id"]
                result["dispatch_ids"] = sorted(
                    set(result.get("dispatch_ids", [])) | {dispatch_id}
                )
            result["effective_as_of"] = event["journal_offset"]
            return result

        def dispatch_reducer(state, event):
            return {
                **state,
                "dispatch_link": event["payload"]["link"],
                "dispatch_snapshot_ref": event["payload"]["dispatch_snapshot_ref"],
                "effective_as_of": event["journal_offset"],
            }

        def research_reducer(state, event):
            result = dict(state)
            if event["event_type"] == "apt.research_capture_appended":
                result["capture"] = event["payload"]["research_capture"]
            elif event["event_type"] == "apt.research_fact_appended":
                variant = event["payload"]["payload_variant"]
                bucket = {
                    "research_question": "questions",
                    "research_answer": "answers",
                    "reference_use": "reference_uses",
                    "research_problem": "problems",
                    "research_claim": "claims",
                    "formalization_candidate": "formalizations",
                }.get(variant, "other_facts")
                values = dict(result.get(bucket, {}))
                entity = event["payload"]["payload"]
                values[entity["fact"]["subject_id"]] = entity
                result[bucket] = values
            elif event["event_type"] == "apt.reference_probe_lineage_appended":
                values = dict(result.get("delivery_origins", {}))
                values[event["payload"]["delivery_subject_key"]] = event["payload"]
                result["delivery_origins"] = values
            result["effective_as_of"] = event["journal_offset"]
            return result

        registrations = (
            ("apt.session-record", session_reducer),
            ("apt.dispatch-scope", dispatch_reducer),
            ("apt.research-record", research_reducer),
        )
        for name, reducer in registrations:
            self.projections.register(
                ProjectionRegistration(
                    name=name,
                    owner_namespace="agent-provenance-telemetry",
                    reducer_ref=f"{name}-projection@1",
                    reducer_digest=canonical_digest({"reducer_ref": f"{name}-projection@1"}),
                    reducer=reducer,
                )
            )

    @staticmethod
    def _stable_id(prefix: str, value: Any) -> str:
        return prefix + canonical_digest(value).removeprefix("sha256:")[:32]

    def _catch_up_apt_status(self, receipt: dict[str, Any]) -> dict[str, Any]:
        result = dict(receipt)
        try:
            state = self.projections.catch_up_apt(self.journal)
            result["projection_status"] = (
                "current"
                if state["current"]
                and int(state["apt_source_through_offset"])
                >= int(receipt["last_offset"])
                else "pending"
            )
        except Exception:
            result["projection_status"] = "pending"
        return result

    def _event(
        self,
        event_type: str,
        payload: dict[str, Any],
        *,
        classification: str = "runtime-internal",
        event_id: str | None = None,
    ) -> EventDraft:
        binding = dict(self.journal._schema_bindings).get(event_type)
        if not binding:
            raise IntegrityError(f"event type is not registered: {event_type}")
        schema_ref, schema_digest = binding
        event_id = event_id or self._stable_id(
            "evt_", {"event_type": event_type, "payload": payload, "nonce": secrets.token_hex(8)}
        )
        prepared = self.artifacts.prepare(
            canonical_bytes(payload),
            media_type="application/json",
            schema_ref=schema_ref,
            classification=classification,
        )
        return EventDraft(
            event_id=event_id,
            event_type=event_type,
            schema_ref=schema_ref,
            schema_digest=schema_digest,
            payload=prepared,
        )

    def _command(
        self,
        *,
        command_name: str,
        scope_key: str,
        idempotency_key: str,
        aggregate_type: str,
        aggregate_id: str,
        expected_version: int,
        authority: dict[str, Any],
        intent: dict[str, Any],
        prerequisites: tuple[PrerequisiteHead, ...] = (),
    ) -> RuntimeCommand:
        command_id = self._stable_id(
            "cmd_",
            {
                "command_name": command_name,
                "scope_key": scope_key,
                "idempotency_key": idempotency_key,
            },
        )
        return RuntimeCommand(
            command_id=command_id,
            scope_key=scope_key,
            idempotency_key=idempotency_key,
            aggregate_type=aggregate_type,
            aggregate_id=aggregate_id,
            expected_version=expected_version,
            causation_id=command_id,
            correlation_id=scope_key,
            authority_context=authority,
            semantic_intent={"command_name": command_name, **intent},
            prerequisites=prerequisites,
        )

    def register_profiles(self) -> dict[str, Any]:
        if not self._profiles:
            self.open()
        profile_projection = [
            {
                "profile_id": p.profile_id,
                "profile_version": p.profile_version,
                "authoritative_path": p.authoritative_path,
                "authoritative_file_digest": p.authoritative_file_digest,
                "canonical_digest": p.canonical_digest,
                "canonical_size_bytes": p.canonical_size_bytes,
            }
            for p in self._profiles
        ]
        command = self._command(
            command_name="aci.register-protocol-profile@1",
            scope_key="aci.protocol-registry",
            idempotency_key="required-profile-set@1",
            aggregate_type="aci.protocol-registry",
            aggregate_id="aci.protocol-registry",
            expected_version=0,
            authority={"principal_id": "trusted-cli", "action": "profile.register"},
            intent={"profiles": profile_projection},
        )
        event = self._event(
            "aci.protocol_profile_registered@1", {"profiles": profile_projection}
        )

        def mutate(conn, records, _result):
            event_id = records[0].event_id
            for profile in self._profiles:
                conn.execute(
                    """
                    INSERT INTO protocol_profiles(
                      profile_id,profile_version,authoritative_path,
                      authoritative_file_digest,canonical_digest,canonical_size_bytes,
                      registration_event_id,registered_at
                    ) VALUES(?,?,?,?,?,?,?,?)
                    """,
                    (
                        profile.profile_id,
                        profile.profile_version,
                        profile.authoritative_path,
                        profile.authoritative_file_digest,
                        profile.canonical_digest,
                        profile.canonical_size_bytes,
                        event_id,
                        self.now().isoformat(),
                    ),
                )

        return self.journal.accept(
            command,
            [event],
            next_state={"registered_profiles": profile_projection},
            mutate=mutate,
        )

    def ensure_session(
        self,
        *,
        origin_digest: str,
        name: str,
        actor_ref: str,
        actor_authentication_ref: str,
        actor_authentication_digest: str,
        idempotency_key: str = "ensure",
    ) -> dict[str, Any]:
        self._require_authority_evidence(
            actor_ref=actor_ref,
            references=(actor_authentication_ref,),
            digests=(actor_authentication_digest,),
        )
        if not origin_digest.startswith("sha256:") or not name:
            raise ValidationError("session origin digest and name are required")
        session_id = self._stable_id("ses_", origin_digest)
        aggregate_id = f"apt.session-binding:{origin_digest}"
        started_at = self.now().isoformat()
        session_entity = {
            "session_id": session_id,
            "origin_kind": "host_context",
            "origin_ref": origin_digest,
            "ensure_key": self._stable_id("ensure_", origin_digest),
            "start_operation_id": idempotency_key,
            "started_at": started_at,
            "initial_name": name,
        }
        payload = {
            "session": session_entity,
            "actor_ref": actor_ref,
            "actor_authentication_ref": actor_authentication_ref,
            "actor_authentication_digest": actor_authentication_digest,
            "rollover_authorization": None,
        }
        command = self._command(
            command_name="apt.ensure-session@1",
            scope_key=aggregate_id,
            idempotency_key=idempotency_key,
            aggregate_type="apt.session-binding",
            aggregate_id=aggregate_id,
            expected_version=0,
            authority={
                "principal_id": actor_ref,
                "action": "session.ensure",
                "authentication_ref": actor_authentication_ref,
                "authentication_digest": actor_authentication_digest,
            },
            intent={
                "origin_digest": origin_digest,
                "name": name,
                "actor_ref": actor_ref,
                "actor_authentication_ref": actor_authentication_ref,
                "actor_authentication_digest": actor_authentication_digest,
            },
        )
        event = self._event("apt.session_started", payload)

        def result(records, base):
            return {
                **base,
                "session": {
                    "session_id": session_id,
                    "origin_digest": origin_digest,
                    "name": name,
                    "started_at": started_at,
                },
            }

        def mutate(conn, records, _result):
            conn.execute(
                """
                INSERT INTO sessions(session_id,origin_digest,name,started_at,event_id)
                VALUES(?,?,?,?,?)
                """,
                (session_id, origin_digest, name, started_at, records[0].event_id),
            )
            conn.execute(
                """
                INSERT INTO session_origin_heads(
                  origin_digest,current_session_id,head_version,rebound_event_id
                ) VALUES(?,?,1,NULL)
                ON CONFLICT(origin_digest) DO NOTHING
                """,
                (origin_digest, session_id),
            )
        receipt = self.journal.accept(
            command, [event], next_state=payload, result_builder=result, mutate=mutate
        )
        return self._catch_up_apt_status(receipt)

    def start_new_session(
        self,
        *,
        token: str,
        name: str,
        expected_current_session_id: str,
        idempotency_key: str,
    ) -> dict[str, Any]:
        context = self.capabilities.resolve(
            token, action="session.start-new", phase="bootstrap"
        )
        required_context = {
            "origin_digest",
            "authorization_policy_ref",
            "authorization_policy_digest",
            "authorization_evidence_ref",
            "authorization_evidence_digest",
            "expected_current_session_id",
            "nonce",
        }
        if not required_context.issubset(context.context) or not name or not idempotency_key:
            raise ValidationError("start-new authorization/name/idempotency is incomplete")
        origin_digest = context.context["origin_digest"]
        aggregate_id = f"apt.session-binding:{origin_digest}"
        with self.database.connect() as conn:
            prior = conn.execute(
                """SELECT result_receipt_json FROM command_receipts
                   WHERE scope_key=? AND idempotency_key=?""",
                (aggregate_id, idempotency_key),
            ).fetchone()
            if prior:
                result = json.loads(prior["result_receipt_json"])
                if (
                    result.get("session", {}).get("origin_digest") != origin_digest
                    or result.get("session", {}).get("name") != name
                    or result.get("expected_current_session_id")
                    != expected_current_session_id
                    or context.context["expected_current_session_id"]
                    != expected_current_session_id
                    or result.get("authorization_nonce")
                    != context.context["nonce"]
                    or result.get("capability_id") != context.capability_id
                ):
                    raise IdempotencyConflict(
                        "start-new key reused with different intent"
                    )
                return self._catch_up_apt_status(result)
            head = conn.execute(
                "SELECT * FROM session_origin_heads WHERE origin_digest=?",
                (origin_digest,),
            ).fetchone()
        if not head:
            raise NotFoundError("session origin binding does not exist")
        predecessor = head["current_session_id"]
        if (
            expected_current_session_id != predecessor
            or context.context["expected_current_session_id"] != predecessor
        ):
            raise ConflictError("expected current Session CAS is stale")
        successor = self._stable_id(
            "ses_", [origin_digest, predecessor, idempotency_key]
        )
        rebound_at = self.now().isoformat()
        session_entity = {
            "session_id": successor,
            "origin_kind": "host_context",
            "origin_ref": origin_digest,
            "ensure_key": self._stable_id(
                "ensure_", [origin_digest, predecessor, idempotency_key]
            ),
            "start_operation_id": idempotency_key,
            "started_at": rebound_at,
            "initial_name": name,
        }
        session_payload = {
            "session": session_entity,
            "actor_ref": context.principal_id,
            "actor_authentication_ref": None,
            "actor_authentication_digest": None,
            "rollover_authorization": {
                "authorization_policy_ref": context.context[
                    "authorization_policy_ref"
                ],
                "authorization_policy_digest": context.context[
                    "authorization_policy_digest"
                ],
                "authorization_evidence_ref": context.context[
                    "authorization_evidence_ref"
                ],
                "authorization_evidence_digest": context.context[
                    "authorization_evidence_digest"
                ],
            },
        }
        rebound_payload = {
            "origin_kind": "host_context",
            "origin_ref": origin_digest,
            "predecessor_session_id": predecessor,
            "successor_session_id": successor,
            "rebound_at": rebound_at,
            "actor_ref": context.principal_id,
            "authorization_policy_ref": context.context["authorization_policy_ref"],
            "authorization_policy_digest": context.context[
                "authorization_policy_digest"
            ],
            "authorization_evidence_ref": context.context[
                "authorization_evidence_ref"
            ],
            "authorization_evidence_digest": context.context[
                "authorization_evidence_digest"
            ],
        }
        aggregate_head = self.journal.head(aggregate_id)
        command = self._command(
            command_name="apt.start-new-session@1",
            scope_key=aggregate_id,
            idempotency_key=idempotency_key,
            aggregate_type="apt.session-binding",
            aggregate_id=aggregate_id,
            expected_version=aggregate_head["current_version"],
            authority={
                "capability_id": context.capability_id,
                "principal_id": context.principal_id,
                "action": "session.start-new",
                "nonce": context.context["nonce"],
                "authorization_evidence_digest": context.context[
                    "authorization_evidence_digest"
                ],
            },
            intent={
                "origin_digest": origin_digest,
                "expected_current_session_id": expected_current_session_id,
                "predecessor_session_id": predecessor,
                "successor_session_id": successor,
                "name": name,
                "expected_head_version": int(head["head_version"]),
            },
        )
        events = [
            self._event("apt.session_started", session_payload),
            self._event("apt.session_context_rebound", rebound_payload),
        ]

        def result(records, base):
            return {
                **base,
                "session": {
                    "session_id": successor,
                    "origin_digest": origin_digest,
                    "name": name,
                    "started_at": rebound_at,
                },
                "expected_current_session_id": predecessor,
                "authorization_nonce": context.context["nonce"],
                "capability_id": context.capability_id,
                "predecessor_session_id": predecessor,
                "rebound_event_id": records[1].event_id,
            }

        def mutate(conn, records, _result):
            conn.execute(
                """INSERT INTO sessions(session_id,origin_digest,name,started_at,event_id)
                   VALUES(?,?,?,?,?)""",
                (
                    successor,
                    origin_digest,
                    name,
                    rebound_at,
                    records[0].event_id,
                ),
            )
            updated = conn.execute(
                """
                UPDATE session_origin_heads
                SET current_session_id=?,head_version=head_version+1,
                    rebound_event_id=?
                WHERE origin_digest=? AND current_session_id=? AND head_version=?
                """,
                (
                    successor,
                    records[1].event_id,
                    origin_digest,
                    predecessor,
                    head["head_version"],
                ),
            )
            if updated.rowcount != 1:
                raise ConflictError("session origin head CAS lost")
            conn.execute(
                """INSERT INTO session_context_rebounds(
                     predecessor_session_id,successor_session_id,origin_digest,
                     rebound_event_id,rebound_at
                   ) VALUES(?,?,?,?,?)""",
                (
                    predecessor,
                    successor,
                    origin_digest,
                    records[1].event_id,
                    rebound_at,
                ),
            )
        receipt = self.journal.accept(
            command,
            events,
            next_state={
                "current_session_id": successor,
                "head_version": int(head["head_version"]) + 1,
            },
            result_builder=result,
            mutate=mutate,
        )
        return self._catch_up_apt_status(receipt)

    def link_session_dispatch(
        self,
        *,
        session_id: str,
        dispatch_id: str,
        actor_ref: str,
        authorization_policy_ref: str,
        authorization_policy_digest: str,
        authorization_evidence_ref: str,
        authorization_evidence_digest: str,
        idempotency_key: str = "link",
    ) -> dict[str, Any]:
        self._require_authority_evidence(
            actor_ref=actor_ref,
            references=(authorization_policy_ref, authorization_evidence_ref),
            digests=(
                authorization_policy_digest,
                authorization_evidence_digest,
            ),
        )
        snapshot = self.legacy.resolve(self.settings.ledger_path, dispatch_id)
        with self.database.connect() as conn:
            session = conn.execute(
                "SELECT * FROM sessions WHERE session_id=?", (session_id,)
            ).fetchone()
            current = (
                conn.execute(
                    """SELECT * FROM session_origin_heads
                       WHERE origin_digest=? AND current_session_id=?""",
                    (session["origin_digest"], session_id),
                ).fetchone()
                if session
                else None
            )
        if not session or not current:
            raise ConflictError("Session is not the current origin binding")
        session_head = self.journal.head(
            f"apt.session-binding:{session['origin_digest']}"
        )
        aggregate_id = f"apt.dispatch-link:{dispatch_id}"
        link_entity = {
            "session_dispatch_link_id": self._stable_id(
                "lnk_", [session_id, dispatch_id, snapshot.row_digest]
            ),
            "session_id": session_id,
            "dispatch_id": dispatch_id,
            "link_operation_id": idempotency_key,
            "linked_at": self.now().isoformat(),
        }
        dispatch_snapshot_ref = {
                "kind": "legacy_ledger",
                "ledger_row_identity": {
                    "dispatch_id": dispatch_id,
                    "row_kind": snapshot.row_kind,
                    "appender_identity": snapshot.appender_identity,
                    "contract_version": snapshot.contract_version,
                    "agent_role_registry_ref": snapshot.agent_role_registry_ref,
                },
                "row_digest": snapshot.row_digest,
        }
        payload = {
            "link": link_entity,
            "origin_kind": "host_context",
            "origin_ref": session["origin_digest"],
            "dispatch_snapshot_ref": dispatch_snapshot_ref,
            "actor_ref": actor_ref,
            "authorization_policy_ref": authorization_policy_ref,
            "authorization_policy_digest": authorization_policy_digest,
            "authorization_evidence_ref": authorization_evidence_ref,
            "authorization_evidence_digest": authorization_evidence_digest,
        }
        command = self._command(
            command_name="apt.link-session-dispatch@1",
            scope_key=aggregate_id,
            idempotency_key=idempotency_key,
            aggregate_type="apt.dispatch-link",
            aggregate_id=aggregate_id,
            expected_version=0,
            authority={
                "principal_id": actor_ref,
                "action": "dispatch.link",
                "authorization_policy_ref": authorization_policy_ref,
                "authorization_policy_digest": authorization_policy_digest,
                "authorization_evidence_ref": authorization_evidence_ref,
                "authorization_evidence_digest": authorization_evidence_digest,
            },
            intent={
                "session_id": session_id,
                "dispatch_id": dispatch_id,
                "actor_ref": actor_ref,
                "dispatch_snapshot_ref": dispatch_snapshot_ref,
                "authorization_policy_ref": authorization_policy_ref,
                "authorization_policy_digest": authorization_policy_digest,
                "authorization_evidence_ref": authorization_evidence_ref,
                "authorization_evidence_digest": authorization_evidence_digest,
            },
            prerequisites=(
                PrerequisiteHead(
                    aggregate_id=session_head["aggregate_id"],
                    expected_version=session_head["current_version"],
                    state_hash=session_head["state_hash"],
                ),
            ),
        )
        event = self._event("apt.session_dispatch_linked", payload)

        def result(records, base):
            return {
                **base,
                "dispatch_link": {
                    **link_entity,
                    "snapshot": dispatch_snapshot_ref,
                },
            }

        def mutate(conn, records, _result):
            self.legacy.verify_unchanged(snapshot)
            conn.execute(
                """
                INSERT INTO dispatch_links(
                  dispatch_id,session_id,ledger_path,ledger_digest,row_digest,row_json,
                  event_id,linked_at
                ) VALUES(?,?,?,?,?,?,?,?)
                """,
                (
                    dispatch_id,
                    session_id,
                    snapshot.ledger_path,
                    snapshot.ledger_digest,
                    snapshot.row_digest,
                    canonical_text(snapshot.row),
                    records[0].event_id,
                    link_entity["linked_at"],
                ),
            )
        receipt = self.journal.accept(
            command, [event], next_state=payload, result_builder=result, mutate=mutate
        )
        return self._catch_up_apt_status(receipt)

    def record_orchestration_dispatch_opened(
        self,
        *,
        session_id: str,
        dispatch_id: str,
        actor_ref: str,
        authorization_evidence_ref: str,
        authorization_evidence_digest: str,
        idempotency_key: str = "orchestration-open",
    ) -> dict[str, Any]:
        """Accept the launch gate only after the YAML opening is linked in ACI."""
        self._require_authority_evidence(
            actor_ref=actor_ref,
            references=(authorization_evidence_ref,),
            digests=(authorization_evidence_digest,),
        )
        snapshot = self.legacy.resolve(self.settings.ledger_path, dispatch_id)
        with self.database.connect() as conn:
            link = conn.execute(
                "SELECT * FROM dispatch_links WHERE dispatch_id=? AND session_id=?",
                (dispatch_id, session_id),
            ).fetchone()
        if not link:
            raise NotFoundError("linked Session and dispatch are required before launch")
        if link["row_digest"] != snapshot.row_digest:
            raise IntegrityError("linked opening digest differs from current YAML row")
        opened_at = snapshot.row.get("created")
        if not isinstance(opened_at, str) or not opened_at:
            raise IntegrityError("validated YAML opening has no created timestamp")
        aggregate_id = f"aci.orchestration-dispatch:{dispatch_id}"
        link_head = self.journal.head(f"apt.dispatch-link:{dispatch_id}")
        payload = {
            "dispatch_id": dispatch_id,
            "session_id": session_id,
            "opened_at": opened_at,
            "actor_ref": actor_ref,
            "authority_mode": "legacy-managed",
            "ledger_path": link["ledger_path"],
            "ledger_digest": link["ledger_digest"],
            "row_digest": snapshot.row_digest,
            "row_bytes_digest": snapshot.row_bytes_digest,
            "link_event_id": link["event_id"],
            "authorization_evidence_ref": authorization_evidence_ref,
            "authorization_evidence_digest": authorization_evidence_digest,
        }
        command = self._command(
            command_name="aci.record-orchestration-dispatch-opened@1",
            scope_key=aggregate_id,
            idempotency_key=idempotency_key,
            aggregate_type="aci.orchestration-dispatch",
            aggregate_id=aggregate_id,
            expected_version=0,
            authority={
                "principal_id": actor_ref,
                "action": "orchestration.dispatch.open",
                "authorization_evidence_ref": authorization_evidence_ref,
                "authorization_evidence_digest": authorization_evidence_digest,
            },
            intent=payload,
            prerequisites=(
                PrerequisiteHead(
                    aggregate_id=link_head["aggregate_id"],
                    expected_version=link_head["current_version"],
                    state_hash=link_head["state_hash"],
                ),
            ),
        )
        event = self._event("orchestration.dispatch_opened@1", payload)

        def result(records, base):
            return {
                **base,
                "orchestration_dispatch": {
                    "dispatch_id": dispatch_id,
                    "session_id": session_id,
                    "status": "opened",
                    "authority_mode": "legacy-managed",
                    "event_id": records[0].event_id,
                    "yaml_row_digest": snapshot.row_digest,
                },
            }

        receipt = self.journal.accept(
            command, [event], next_state=payload, result_builder=result
        )
        return self._catch_up_apt_status(receipt)

    def record_orchestration_dispatch_closed(
        self,
        *,
        session_id: str,
        dispatch_id: str,
        actor_ref: str,
        authorization_evidence_ref: str,
        authorization_evidence_digest: str,
        idempotency_key: str = "orchestration-close",
    ) -> dict[str, Any]:
        """Accept the durable outcome only after the validated YAML close exists."""
        self._require_authority_evidence(
            actor_ref=actor_ref,
            references=(authorization_evidence_ref,),
            digests=(authorization_evidence_digest,),
        )
        snapshot = self.legacy.resolve_close(self.settings.ledger_path, dispatch_id)
        with self.database.connect() as conn:
            link = conn.execute(
                "SELECT * FROM dispatch_links WHERE dispatch_id=? AND session_id=?",
                (dispatch_id, session_id),
            ).fetchone()
            unfinished_scout = conn.execute(
                """
                SELECT scout_run_id,state FROM reference_scout_runs
                WHERE dispatch_id=? AND state NOT IN ('delivered','failed','cancelled')
                ORDER BY requested_at LIMIT 1
                """,
                (dispatch_id,),
            ).fetchone()
            running_binding = conn.execute(
                """
                SELECT binding_id,group_id,seat_index,turn_ordinal
                FROM host_workflow_turn_bindings
                WHERE dispatch_id=? AND state='running'
                ORDER BY group_id,seat_index,turn_ordinal LIMIT 1
                """,
                (dispatch_id,),
            ).fetchone()
        if not link:
            raise NotFoundError("linked Session and dispatch are required before close")
        if unfinished_scout:
            raise ConflictError(
                "dispatch cannot close with unfinished Reference Scout "
                f"{unfinished_scout['scout_run_id']} ({unfinished_scout['state']})"
            )
        if running_binding:
            raise ConflictError(
                "dispatch cannot close with running host workflow binding "
                f"{running_binding['binding_id']} "
                f"({running_binding['group_id']}[{running_binding['seat_index']}] "
                f"turn {running_binding['turn_ordinal']})"
            )
        aggregate_id = f"aci.orchestration-dispatch:{dispatch_id}"
        head = self.journal.head(aggregate_id)
        if head["current_version"] == 0:
            raise ConflictError("orchestration opening must be accepted before close")
        closed_at = snapshot.row.get("closed")
        exit_reason = snapshot.row.get("exit_reason")
        agents_spawned = snapshot.row.get("agents_spawned")
        feedback_prompts = snapshot.row.get("feedback_prompts", [])
        if (
            not isinstance(closed_at, str)
            or not closed_at
            or not isinstance(exit_reason, str)
            or not isinstance(agents_spawned, dict)
            or not isinstance(feedback_prompts, list)
        ):
            raise IntegrityError("validated YAML close payload is incomplete")
        payload = {
            "dispatch_id": dispatch_id,
            "session_id": session_id,
            "closed_at": closed_at,
            "actor_ref": actor_ref,
            "exit_reason": exit_reason,
            "agents_spawned": agents_spawned,
            "feedback_prompts": feedback_prompts,
            "ledger_path": snapshot.ledger_path,
            "ledger_digest": snapshot.ledger_digest,
            "row_digest": snapshot.row_digest,
            "row_bytes_digest": snapshot.row_bytes_digest,
            "authorization_evidence_ref": authorization_evidence_ref,
            "authorization_evidence_digest": authorization_evidence_digest,
        }
        command = self._command(
            command_name="aci.record-orchestration-dispatch-closed@1",
            scope_key=aggregate_id,
            idempotency_key=idempotency_key,
            aggregate_type="aci.orchestration-dispatch",
            aggregate_id=aggregate_id,
            expected_version=1,
            authority={
                "principal_id": actor_ref,
                "action": "orchestration.dispatch.close",
                "authorization_evidence_ref": authorization_evidence_ref,
                "authorization_evidence_digest": authorization_evidence_digest,
            },
            intent=payload,
        )
        event = self._event("orchestration.dispatch_closed@1", payload)

        def result(records, base):
            return {
                **base,
                "orchestration_dispatch": {
                    "dispatch_id": dispatch_id,
                    "session_id": session_id,
                    "status": "closed",
                    "exit_reason": exit_reason,
                    "event_id": records[0].event_id,
                    "yaml_row_digest": snapshot.row_digest,
                },
            }

        receipt = self.journal.accept(
            command, [event], next_state=payload, result_builder=result
        )
        return self._catch_up_apt_status(receipt)

    def require_orchestration_dispatch_can_close(
        self,
        *,
        session_id: str,
        dispatch_id: str,
        actor_ref: str,
        authorization_evidence_ref: str,
        authorization_evidence_digest: str,
    ) -> dict[str, Any]:
        """Read-only guard that must pass before the YAML close side effect."""
        self._require_authority_evidence(
            actor_ref=actor_ref,
            references=(authorization_evidence_ref,),
            digests=(authorization_evidence_digest,),
        )
        with self.database.connect() as conn:
            link = conn.execute(
                "SELECT event_id,row_digest FROM dispatch_links "
                "WHERE dispatch_id=? AND session_id=?",
                (dispatch_id, session_id),
            ).fetchone()
            unfinished_scout = conn.execute(
                """
                SELECT scout_run_id,state FROM reference_scout_runs
                WHERE dispatch_id=? AND state NOT IN ('delivered','failed','cancelled')
                ORDER BY requested_at LIMIT 1
                """,
                (dispatch_id,),
            ).fetchone()
        if not link:
            raise NotFoundError("linked Session and dispatch are required before close")
        if unfinished_scout:
            raise ConflictError(
                "dispatch cannot close with unfinished Reference Scout "
                f"{unfinished_scout['scout_run_id']} ({unfinished_scout['state']})"
            )
        head = self.journal.head(f"aci.orchestration-dispatch:{dispatch_id}")
        if head["current_version"] not in {1, 2}:
            raise ConflictError("accepted orchestration opening is required before close")
        return {
            "dispatch_id": dispatch_id,
            "session_id": session_id,
            "current_version": head["current_version"],
            "current_event_id": head["last_event_id"],
            "link_event_id": link["event_id"],
            "opening_row_digest": link["row_digest"],
        }

    def get_orchestration_dispatch_log(
        self, *, dispatch_id: str
    ) -> dict[str, Any]:
        """Return an integrity-checked YAML/ACI lifecycle view for one dispatch."""
        if not isinstance(dispatch_id, str) or not dispatch_id.strip():
            raise ValidationError("dispatch_id is required")
        verification = self.journal.verify_store()
        aggregate_id = f"aci.orchestration-dispatch:{dispatch_id}"
        with self.database.connect() as conn:
            rows = conn.execute(
                """
                SELECT e.journal_offset,e.event_id,e.aggregate_version,e.event_type,
                       e.command_id,e.recorded_at,e.payload_ref,e.payload_hash,
                       a.body,a.size_bytes,a.content_hash
                FROM events e
                JOIN artifacts a ON a.artifact_id=e.payload_ref
                WHERE e.aggregate_id=?
                ORDER BY e.aggregate_version
                """,
                (aggregate_id,),
            ).fetchall()
            link = conn.execute(
                """
                SELECT dispatch_id,session_id,ledger_path,ledger_digest,row_digest,
                       event_id,linked_at
                FROM dispatch_links WHERE dispatch_id=?
                """,
                (dispatch_id,),
            ).fetchone()
            bindings = conn.execute(
                """
                SELECT b.binding_id,b.dispatch_id,b.session_id,b.group_id,
                       b.seat_index,b.turn_ordinal,b.attempt_id,b.host,
                       b.operation_kind,b.workflow_manifest_artifact_id,
                       b.workflow_manifest_hash,b.source_artifact_ids_json,
                       b.state,b.bound_event_id,b.terminal_event_id,
                       b.bound_at,b.terminal_at,r.result_receipt_json
                FROM host_workflow_turn_bindings b
                LEFT JOIN command_receipts r
                  ON r.scope_key='aci.host-workflow-turn:'||b.binding_id
                 AND r.idempotency_key='bind'
                WHERE b.dispatch_id=?
                ORDER BY b.bound_at
                """,
                (dispatch_id,),
            ).fetchall()
        if not rows or not link:
            raise NotFoundError("orchestration dispatch log not found")
        events: list[dict[str, Any]] = []
        for row in rows:
            body = bytes(row["body"])
            if (
                len(body) != row["size_bytes"]
                or digest_bytes(body) != row["content_hash"]
                or row["payload_hash"] != row["content_hash"]
            ):
                raise IntegrityError("orchestration event artifact integrity mismatch")
            payload = parse_strict_json(body)
            if not isinstance(payload, dict) or payload.get("dispatch_id") != dispatch_id:
                raise IntegrityError("orchestration event payload identity mismatch")
            events.append(
                {
                    "journal_offset": row["journal_offset"],
                    "event_id": row["event_id"],
                    "aggregate_version": row["aggregate_version"],
                    "event_type": row["event_type"],
                    "command_id": row["command_id"],
                    "recorded_at": row["recorded_at"],
                    "payload_ref": row["payload_ref"],
                    "payload_hash": row["payload_hash"],
                    "payload": payload,
                }
            )
        opening = self.legacy.resolve(self.settings.ledger_path, dispatch_id)
        try:
            closing = self.legacy.resolve_close(self.settings.ledger_path, dispatch_id)
        except NotFoundError:
            closing = None
        host_workflow_turn_bindings = [
            {
                "binding_id": binding["binding_id"],
                "dispatch_id": binding["dispatch_id"],
                "session_id": binding["session_id"],
                "group_id": binding["group_id"],
                "seat_index": binding["seat_index"],
                "turn_ordinal": binding["turn_ordinal"],
                "attempt_id": binding["attempt_id"],
                "host": binding["host"],
                "operation_kind": binding["operation_kind"],
                "workflow_manifest_artifact_id": binding["workflow_manifest_artifact_id"],
                "workflow_manifest_hash": binding["workflow_manifest_hash"],
                "source_artifact_ids_json": binding["source_artifact_ids_json"],
                "state": binding["state"],
                "bound_event_id": binding["bound_event_id"],
                "terminal_event_id": binding["terminal_event_id"],
                "bound_at": binding["bound_at"],
                "terminal_at": binding["terminal_at"],
                "command_receipt": json.loads(binding["result_receipt_json"])
                if binding["result_receipt_json"]
                else None,
            }
            for binding in bindings
        ]
        return {
            "dispatch_id": dispatch_id,
            "status": "closed"
            if events[-1]["event_type"] == "orchestration.dispatch_closed@1"
            else "opened",
            "database": str(self.settings.database_path.resolve()),
            "journal_verification": verification,
            "session_dispatch_link": dict(link),
            "yaml": {
                "ledger_path": opening.ledger_path,
                "opening": {
                    "row_digest": opening.row_digest,
                    "row_bytes_digest": opening.row_bytes_digest,
                    "record": opening.row,
                },
                "closing": (
                    {
                        "row_digest": closing.row_digest,
                        "row_bytes_digest": closing.row_bytes_digest,
                        "record": closing.row,
                    }
                    if closing
                    else None
                ),
            },
            "events": events,
            "host_workflow_turn_bindings": host_workflow_turn_bindings,
        }

    def activate_local_probe(
        self,
        *,
        session_id: str,
        dispatch_id: str,
        probe_id: str,
        group_aggregate_id: str,
        seat_id: str,
        attempt_id: str,
        operation_id: str,
        idempotency_key: str = "activate",
    ) -> dict[str, Any]:
        """Activate the frozen v1 reference-probe lineage publication context.

        This compatibility operation does not launch a ``ScoutRun`` and is not
        the future lens-bound ``ProbeTool``/``ProbeRun`` agent capability.
        Its names remain stable because registered Stage-B profiles and receipts
        already bind them.
        """
        with self.database.connect() as conn:
            link = conn.execute(
                "SELECT * FROM dispatch_links WHERE dispatch_id=? AND session_id=?",
                (dispatch_id, session_id),
            ).fetchone()
            profile = conn.execute(
                """
                SELECT * FROM protocol_profiles
                WHERE profile_id='apt.reference-probe-lineage' AND profile_version='1'
                """
            ).fetchone()
        if not link or not profile:
            raise NotFoundError("linked dispatch and registered probe profile are required")
        aggregate_id = (
            f"aci.local-probe:{session_id}:{dispatch_id}:{probe_id}:"
            f"{profile['canonical_digest']}"
        )
        context_id = self._stable_id("prb_", aggregate_id)
        payload = {
            "probe_context_id": context_id,
            "session_id": session_id,
            "dispatch_id": dispatch_id,
            "probe_id": probe_id,
            "profile_binding": {
                "profile_id": profile["profile_id"],
                "profile_version": profile["profile_version"],
                "profile_digest": profile["canonical_digest"],
            },
            "group_aggregate_id": group_aggregate_id,
            "seat_id": seat_id,
            "attempt_id": attempt_id,
            "operation_id": operation_id,
            "phase": "collect",
        }
        link_head = self.journal.head(f"apt.dispatch-link:{dispatch_id}")
        command = self._command(
            command_name="aci.activate-local-probe-context@1",
            scope_key=aggregate_id,
            idempotency_key=idempotency_key,
            aggregate_type="aci.local-probe",
            aggregate_id=aggregate_id,
            expected_version=0,
            authority={"principal_id": "trusted-cli", "action": "probe.activate"},
            intent=payload,
            prerequisites=(
                PrerequisiteHead(
                    link_head["aggregate_id"],
                    link_head["current_version"],
                    link_head["state_hash"],
                ),
            ),
        )
        event = self._event("aci.local_probe_context_activated@1", payload)
        issued: dict[str, dict[str, str]] = {}

        def mutate(conn, records, _result):
            conn.execute(
                """
                INSERT INTO local_probe_contexts(
                  probe_context_id,session_id,dispatch_id,probe_id,profile_id,
                  profile_version,profile_digest,group_aggregate_id,seat_id,
                  attempt_id,operation_id,phase,event_id
                ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    context_id,
                    session_id,
                    dispatch_id,
                    probe_id,
                    profile["profile_id"],
                    profile["profile_version"],
                    profile["canonical_digest"],
                    group_aggregate_id,
                    seat_id,
                    attempt_id,
                    operation_id,
                    "collect",
                    records[0].event_id,
                ),
            )
            capability_context = {**payload, "aggregate_id": aggregate_id}
            issued["agent"] = self.capabilities.issue(
                principal_id=f"agent:{attempt_id}",
                action="bus.publish",
                phase="collect",
                context=capability_context,
                conn=conn,
            )
            issued["parent"] = self.capabilities.issue(
                principal_id="parent-runtime",
                action="bus.verify",
                phase="collect",
                context=capability_context,
                conn=conn,
            )
            issued["reader"] = self.capabilities.issue(
                principal_id="research-reader",
                action="artifact.read",
                phase="collect",
                context=capability_context,
                conn=conn,
            )

        receipt = self.journal.accept(
            command, [event], next_state=payload, mutate=mutate
        )
        return {**receipt, "issued_capabilities_once": issued}

    def start_reference_scout(
        self,
        *,
        token: str,
        session_id: str,
        dispatch_id: str,
        objective_ref: str,
        shape: str,
        source_mode: str,
        seat_id: str,
        attempt_id: str,
        operation_id: str,
        idempotency_key: str = "start",
    ) -> dict[str, Any]:
        """Start one dispatch-bound ScoutRun and atomically issue its bus authority."""
        context = self.capabilities.resolve(
            token, action="scout.start", phase="bootstrap"
        )
        bound = context.context
        expected = {
            "session_id": session_id,
            "dispatch_id": dispatch_id,
            "objective_ref": objective_ref,
            "shape": shape,
            "source_mode": source_mode,
            "seat_id": seat_id,
            "attempt_id": attempt_id,
            "operation_id": operation_id,
        }
        if any(bound.get(key) != value for key, value in expected.items()):
            raise AuthorizationError("Scout start intent differs from capability")
        if shape != "small":
            raise ValidationError(
                "only the small single-seat Scout shape is operational"
            )
        if source_mode not in {"internal", "external", "internal-and-external"}:
            raise ValidationError("Scout source mode is invalid")
        for field, value in expected.items():
            if not isinstance(value, str) or not value:
                raise ValidationError(f"Scout {field} is required")
        with self.database.connect() as conn:
            link = conn.execute(
                "SELECT * FROM dispatch_links WHERE dispatch_id=? AND session_id=?",
                (dispatch_id, session_id),
            ).fetchone()
            profile = conn.execute(
                """
                SELECT * FROM protocol_profiles
                WHERE profile_id='apt.reference-probe-lineage' AND profile_version='1'
                """
            ).fetchone()
        if not link or not profile:
            raise NotFoundError(
                "linked dispatch and registered Scout compatibility profile are required"
            )
        orchestration_head = self.journal.head(
            f"aci.orchestration-dispatch:{dispatch_id}"
        )
        if orchestration_head["current_version"] != 1:
            raise ConflictError(
                "Reference Scout may start only while orchestration is open"
            )
        scout_run_id = self._stable_id(
            "sct_", [session_id, dispatch_id, operation_id]
        )
        probe_id = self._stable_id("probe_", scout_run_id)
        group_aggregate_id = f"aci.reference-scout:{scout_run_id}"
        payload = {
            "scout_run_id": scout_run_id,
            "probe_id": probe_id,
            "session_id": session_id,
            "dispatch_id": dispatch_id,
            "launch_mode": "dispatch_bound",
            "objective_ref": objective_ref,
            "shape": shape,
            "source_mode": source_mode,
            "profile_binding": {
                "profile_id": profile["profile_id"],
                "profile_version": profile["profile_version"],
                "profile_digest": profile["canonical_digest"],
            },
            "group_aggregate_id": group_aggregate_id,
            "seat_id": seat_id,
            "attempt_id": attempt_id,
            "operation_id": operation_id,
            "requested_at": self.now().isoformat(),
            "actor_ref": context.principal_id,
        }
        capability_context = {
            **payload,
            "aggregate_id": group_aggregate_id,
            "aggregate_type": "aci.reference-scout",
            "bus_kind": "reference_scout",
            "expected_round_id": "scout",
        }

        def issue_run_capabilities(conn=None):
            return {
                "agent": self.capabilities.issue(
                    principal_id=f"agent:{attempt_id}",
                    action="bus.publish",
                    phase="collect",
                    context=capability_context,
                    conn=conn,
                ),
                "parent": self.capabilities.issue(
                    principal_id=context.principal_id,
                    action="bus.verify",
                    phase="collect",
                    context=capability_context,
                    conn=conn,
                ),
                "committer": self.capabilities.issue(
                    principal_id=context.principal_id,
                    action="scout.commit",
                    phase="finalize",
                    context=capability_context,
                    conn=conn,
                ),
                "deliverer": self.capabilities.issue(
                    principal_id=context.principal_id,
                    action="scout.deliver",
                    phase="deliver",
                    context=capability_context,
                    conn=conn,
                ),
                "terminator": self.capabilities.issue(
                    principal_id=context.principal_id,
                    action="scout.terminate",
                    phase="control",
                    context=capability_context,
                    conn=conn,
                ),
            }

        with self.database.connect() as conn:
            prior = conn.execute(
                """
                SELECT result_receipt_json FROM command_receipts
                WHERE scope_key=? AND idempotency_key=?
                """,
                (group_aggregate_id, idempotency_key),
            ).fetchone()
            existing_run = conn.execute(
                "SELECT * FROM reference_scout_runs WHERE scout_run_id=?",
                (scout_run_id,),
            ).fetchone()
        if prior:
            if not existing_run or any(
                existing_run[field] != value
                for field, value in {
                    "session_id": session_id,
                    "dispatch_id": dispatch_id,
                    "objective_ref": objective_ref,
                    "shape": shape,
                    "source_mode": source_mode,
                    "seat_id": seat_id,
                    "attempt_id": attempt_id,
                    "operation_id": operation_id,
                }.items()
            ):
                raise IdempotencyConflict(
                    "Scout start key reused with different intent"
                )
            return {
                **json.loads(prior["result_receipt_json"]),
                "issued_capabilities_once": issue_run_capabilities(),
                "capabilities_reissued": True,
            }
        link_head = self.journal.head(f"apt.dispatch-link:{dispatch_id}")
        command = self._command(
            command_name="aci.start-reference-scout@1",
            scope_key=group_aggregate_id,
            idempotency_key=idempotency_key,
            aggregate_type="aci.reference-scout",
            aggregate_id=group_aggregate_id,
            expected_version=0,
            authority={
                "capability_id": context.capability_id,
                "principal_id": context.principal_id,
                "action": "scout.start",
                "phase": "bootstrap",
            },
            intent=payload,
            prerequisites=(
                PrerequisiteHead(
                    link_head["aggregate_id"],
                    link_head["current_version"],
                    link_head["state_hash"],
                ),
                PrerequisiteHead(
                    orchestration_head["aggregate_id"],
                    orchestration_head["current_version"],
                    orchestration_head["state_hash"],
                ),
            ),
        )
        event = self._event("reference_scout.run_requested@1", payload)
        issued: dict[str, dict[str, str]] = {}

        def mutate(conn, records, _result):
            conn.execute(
                """
                INSERT INTO reference_scout_runs(
                  scout_run_id,probe_id,session_id,dispatch_id,launch_mode,
                  objective_ref,shape,source_mode,profile_id,profile_version,
                  profile_digest,group_aggregate_id,seat_id,attempt_id,operation_id,
                  state,requested_at,start_event_id,last_event_id,source_through_offset
                ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,'requested',?,?,?,?)
                """,
                (
                    scout_run_id,
                    probe_id,
                    session_id,
                    dispatch_id,
                    "dispatch_bound",
                    objective_ref,
                    shape,
                    source_mode,
                    profile["profile_id"],
                    profile["profile_version"],
                    profile["canonical_digest"],
                    group_aggregate_id,
                    seat_id,
                    attempt_id,
                    operation_id,
                    payload["requested_at"],
                    records[0].event_id,
                    records[0].event_id,
                    records[0].journal_offset,
                ),
            )
            issued.update(issue_run_capabilities(conn))

        def result(records, base):
            return {
                **base,
                "scout_run": {
                    "scout_run_id": scout_run_id,
                    "probe_id": probe_id,
                    "session_id": session_id,
                    "dispatch_id": dispatch_id,
                    "state": "requested",
                    "event_id": records[0].event_id,
                },
            }

        receipt = self.journal.accept(
            command,
            [event],
            next_state=payload,
            result_builder=result,
            mutate=mutate,
        )
        return {**receipt, "issued_capabilities_once": issued}

    def publish(self, token: str, intent: dict[str, Any]) -> dict[str, Any]:
        self.capabilities.reject_authority_fields(intent)
        allowed = {
            "idempotency_key",
            "operation_id",
            "round_id",
            "message_type",
            "reply_to_message_ids",
            "payload",
            "payload_ref",
        }
        if set(intent) - allowed:
            raise ValidationError("unknown publication intent fields")
        if ("payload" in intent) == ("payload_ref" in intent):
            raise ValidationError("exactly one payload or payload_ref is required")
        context = self.capabilities.resolve(token, action="bus.publish", phase="collect")
        bound = context.context
        if intent.get("operation_id") != bound["operation_id"]:
            raise ConflictError("operation does not match capability")
        expected_round = bound.get("expected_round_id", "probe")
        if intent.get("round_id") != expected_round:
            raise ValidationError("bus round does not match capability")
        if not intent.get("message_type") or not intent.get("idempotency_key"):
            raise ValidationError("message type and idempotency key are required")
        if bound.get("bus_kind") == "reference_scout" and not intent[
            "message_type"
        ].startswith("reference_scout:"):
            raise ValidationError(
                "Scout publication message type must bind a recommendation identity"
            )
        if intent.get("reply_to_message_ids", []) != []:
            raise ValidationError("local probe publication has no visible peer replies")
        with self.database.connect() as conn:
            sealed = conn.execute(
                """
                SELECT 1 FROM collection_closures
                WHERE group_aggregate_id=? AND round_id=?
                """,
                (bound["group_aggregate_id"], intent["round_id"]),
            ).fetchone()
        if sealed:
            raise ConflictError("collection is sealed")

        if "payload" in intent:
            message_artifact = self.artifacts.prepare(
                canonical_bytes(intent["payload"]),
                media_type="application/json",
                schema_ref="aci.bus-publication-payload@1",
                classification="sensitive-output",
            )
        else:
            with self.database.connect() as conn:
                row = conn.execute(
                    "SELECT * FROM artifacts WHERE artifact_id=?",
                    (intent["payload_ref"],),
                ).fetchone()
            if not row:
                raise NotFoundError("payload artifact not found")
            message_artifact = self.artifacts.prepare(
                bytes(row["body"]),
                media_type=row["media_type"],
                schema_ref=row["schema_ref"],
                classification=row["classification"],
                redaction_policy_ref=row["redaction_policy_ref"],
                retention_policy_ref=row["retention_policy_ref"],
                tombstone_policy_ref=row["tombstone_policy_ref"],
                authorization_policy_ref=row["authorization_policy_ref"],
            )
        aggregate_id = bound["aggregate_id"]
        publication_scope = f"{aggregate_id}:publish"
        with self.database.connect() as conn:
            existing = conn.execute(
                """
                SELECT result_receipt_json,expected_version FROM command_receipts
                WHERE scope_key=? AND idempotency_key=?
                """,
                (publication_scope, intent["idempotency_key"]),
            ).fetchone()
        head = self.journal.head(aggregate_id)
        logical = {
            "group_aggregate_id": bound["group_aggregate_id"],
            "seat_id": bound["seat_id"],
            "round_id": intent["round_id"],
            "message_type": intent["message_type"],
        }
        candidate_id = self._stable_id(
            "cand_", [aggregate_id, intent["idempotency_key"]]
        )
        message_id = self._stable_id("msg_", logical)
        event_payload = {
            "candidate_id": candidate_id,
            "message_id": message_id,
            "logical_key": logical,
            "attempt_id": bound["attempt_id"],
            "operation_id": bound["operation_id"],
            "payload_ref": message_artifact.artifact_id,
            "payload_hash": message_artifact.content_hash,
            "idempotency_key": intent["idempotency_key"],
        }
        command = self._command(
            command_name="aci.publish-bus-contribution@1",
            scope_key=publication_scope,
            idempotency_key=intent["idempotency_key"],
            aggregate_type=bound.get("aggregate_type", "aci.local-probe"),
            aggregate_id=aggregate_id,
            expected_version=(
                int(existing["expected_version"])
                if existing
                else head["current_version"]
            ),
            authority={
                "capability_id": context.capability_id,
                "principal_id": context.principal_id,
                **logical,
                "attempt_id": bound["attempt_id"],
                "operation_id": bound["operation_id"],
                "phase": "collect",
            },
            intent={key: intent[key] for key in intent if key != "payload"}
            | {"payload_hash": message_artifact.content_hash},
        )
        event = self._event("publication.persisted", event_payload)

        def result(records, base):
            publication_receipt = {
                "receipt_version": "1",
                "status": "persisted_candidate",
                "event_id": records[0].event_id,
                "message_id": message_id,
                "payload_hash": message_artifact.content_hash,
                "idempotency_key": intent["idempotency_key"],
                "journal_offset": records[0].journal_offset,
            }
            return {**base, "publication_receipt": publication_receipt}

        def mutate(conn, records, result_receipt):
            publication = result_receipt["publication_receipt"]
            receipt_bytes = canonical_bytes(publication)
            conn.execute(
                """
                INSERT INTO publication_candidates(
                  candidate_id,message_id,publication_event_id,group_aggregate_id,
                  seat_id,round_id,message_type,attempt_id,operation_id,payload_ref,
                  payload_hash,idempotency_key,receipt_bytes,receipt_digest,
                  journal_offset,status,candidate_version
                ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,1)
                """,
                (
                    candidate_id,
                    message_id,
                    records[0].event_id,
                    logical["group_aggregate_id"],
                    logical["seat_id"],
                    logical["round_id"],
                    logical["message_type"],
                    bound["attempt_id"],
                    bound["operation_id"],
                    message_artifact.artifact_id,
                    message_artifact.content_hash,
                    intent["idempotency_key"],
                    receipt_bytes,
                    canonical_digest(publication),
                    records[0].journal_offset,
                    "active",
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
                    records[0].event_id,
                    message_id,
                    publication_scope,
                    intent["idempotency_key"],
                    message_artifact.content_hash,
                    receipt_bytes,
                    canonical_digest(publication),
                    records[0].journal_offset,
                ),
            )

        try:
            return self.journal.accept(
                command,
                [event],
                next_state={"phase": "collect", "candidate_id": candidate_id},
                additional_artifacts=(message_artifact,),
                result_builder=result,
                mutate=mutate,
            )
        except sqlite3.IntegrityError as exc:
            raise ConflictError("logical publication already reserved or official") from exc

    def verify_publication(
        self, token: str, publication_receipt: dict[str, Any]
    ) -> dict[str, Any]:
        context = self.capabilities.resolve(token, action="bus.verify", phase="collect")
        bound = context.context
        expected_fields = {
            "receipt_version",
            "status",
            "event_id",
            "message_id",
            "payload_hash",
            "idempotency_key",
            "journal_offset",
        }
        if set(publication_receipt) != expected_fields:
            raise ValidationError("publication receipt has an invalid field set")
        with self.database.connect() as conn:
            candidate = conn.execute(
                """
                SELECT c.*,e.aggregate_version AS publication_aggregate_version
                FROM publication_candidates c
                JOIN events e ON e.event_id=c.publication_event_id
                WHERE c.publication_event_id=?
                """,
                (publication_receipt["event_id"],),
            ).fetchone()
        if not candidate or candidate["status"] != "active":
            if not candidate or candidate["status"] != "officially_accepted":
                raise ConflictError("publication candidate is not active")
        if (
            candidate["group_aggregate_id"] != bound["group_aggregate_id"]
            or candidate["seat_id"] != bound["seat_id"]
            or candidate["attempt_id"] != bound["attempt_id"]
            or candidate["operation_id"] != bound["operation_id"]
        ):
            raise ConflictError("parent capability scope does not own candidate")
        stored_receipt = parse_strict_json(bytes(candidate["receipt_bytes"]))
        if stored_receipt != publication_receipt:
            raise ConflictError("publication receipt does not match committed evidence")
        if candidate["status"] == "officially_accepted":
            with self.database.connect() as conn:
                row = conn.execute(
                    """
                    SELECT cr.result_receipt_json FROM events e
                    JOIN command_receipts cr ON cr.command_id=e.command_id
                    WHERE e.event_id=?
                    """,
                    (candidate["official_accepted_event_id"],),
                ).fetchone()
            if row:
                return json.loads(row["result_receipt_json"])
            raise IntegrityError("official candidate lacks stored command receipt")
        aggregate_id = bound["aggregate_id"]
        is_scout = bound.get("bus_kind") == "reference_scout"
        recommendation: dict[str, Any] | None = None
        if is_scout:
            with self.database.connect() as conn:
                artifact = conn.execute(
                    "SELECT body,content_hash FROM artifacts WHERE artifact_id=?",
                    (candidate["payload_ref"],),
                ).fetchone()
                run = conn.execute(
                    "SELECT * FROM reference_scout_runs WHERE scout_run_id=?",
                    (bound.get("scout_run_id"),),
                ).fetchone()
            if (
                not artifact
                or artifact["content_hash"] != candidate["payload_hash"]
                or not run
                or run["state"] not in {"requested", "collecting"}
            ):
                raise ConflictError("Scout publication authority is no longer current")
            recommendation = parse_strict_json(bytes(artifact["body"]))
            expected_recommendation_fields = {
                "recommendation_id",
                "reference_id",
                "source_class",
                "locator_observed",
                "access_state",
                "found_by_seat_id",
                "evaluated_by_seat_id",
                "evaluation",
                "why_inspect",
                "comparability_state",
            }
            if (
                not isinstance(recommendation, dict)
                or set(recommendation) != expected_recommendation_fields
            ):
                raise ValidationError("Scout recommendation payload shape is invalid")
            required_recommendation_fields = (
                "recommendation_id",
                "reference_id",
                "source_class",
                "locator_observed",
                "access_state",
                "found_by_seat_id",
                "why_inspect",
            )
            if any(
                not isinstance(recommendation[field], str)
                or not recommendation[field]
                for field in required_recommendation_fields
            ):
                raise ValidationError("Scout recommendation text field is invalid")
            if recommendation["found_by_seat_id"] != bound["seat_id"]:
                raise AuthorizationError(
                    "Scout recommendation seat differs from capability"
                )
            comparability = recommendation["comparability_state"]
            if comparability not in {
                None,
                "comparable",
                "incommensurable",
                "count_capped",
            }:
                raise ValidationError("Scout comparability state is invalid")
            expected_message_type = (
                "reference_scout:" + recommendation["recommendation_id"]
            )
            if candidate["message_type"] != expected_message_type:
                raise ConflictError(
                    "Scout message type does not bind recommendation identity"
                )
            payload = {
                "scout_run_id": bound["scout_run_id"],
                "probe_id": bound["probe_id"],
                "recommendation": recommendation,
                "message_id": candidate["message_id"],
                "publication_event_id": candidate["publication_event_id"],
                "payload_ref": candidate["payload_ref"],
                "payload_hash": candidate["payload_hash"],
                "accepted_at": self.now().isoformat(),
            }
            event_type = "reference_scout.recommendation_accepted@1"
        else:
            payload = {
                "candidate_id": candidate["candidate_id"],
                "message_id": candidate["message_id"],
                "publication_event_id": candidate["publication_event_id"],
                "profile_binding": {
                    "profile_id": bound["profile_binding"]["profile_id"],
                    "profile_version": bound["profile_binding"]["profile_version"],
                    "profile_digest": bound["profile_binding"]["profile_digest"],
                },
            }
            event_type = "reference_probe.accepted@1"
        command = self._command(
            command_name="aci.verify-publication-receipt@1",
            scope_key=f"{aggregate_id}:verify",
            idempotency_key="verify:" + candidate["publication_event_id"],
            aggregate_type=bound.get("aggregate_type", "aci.local-probe"),
            aggregate_id=aggregate_id,
            # Both concurrent verifiers must seal the same semantic command.
            # Reading the mutable current head here made the losing verifier
            # compute a different command digest after the winner committed,
            # turning an exact retry into an idempotency conflict.  The
            # candidate's accepted publication version is the immutable CAS
            # predecessor for this transition.
            expected_version=candidate["publication_aggregate_version"],
            authority={
                "capability_id": context.capability_id,
                "principal_id": context.principal_id,
                "action": "bus.verify",
                "phase": "collect",
            },
            intent={"publication_receipt": publication_receipt},
        )
        event = self._event(event_type, payload)

        def result(records, base):
            return {
                **base,
                "official_message": {
                    "message_id": candidate["message_id"],
                    "accepted_event_id": records[0].event_id,
                    "accepted_offset": records[0].journal_offset,
                    "payload_ref": candidate["payload_ref"],
                    "payload_hash": candidate["payload_hash"],
                },
            }

        def mutate(conn, records, _result):
            updated = conn.execute(
                """
                UPDATE publication_candidates
                SET status='officially_accepted',candidate_version=candidate_version+1,
                    official_accepted_event_id=?
                WHERE candidate_id=? AND status='active' AND candidate_version=?
                """,
                (
                    records[0].event_id,
                    candidate["candidate_id"],
                    candidate["candidate_version"],
                ),
            )
            if updated.rowcount != 1:
                raise ConflictError("candidate verification CAS lost")
            conn.execute(
                """
                INSERT INTO messages(
                  message_id,group_aggregate_id,seat_id,round_id,message_type,
                  payload_ref,payload_hash,source_candidate_id,official_event_id,
                  accepted_offset
                ) VALUES(?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    candidate["message_id"],
                    candidate["group_aggregate_id"],
                    candidate["seat_id"],
                    candidate["round_id"],
                    candidate["message_type"],
                    candidate["payload_ref"],
                    candidate["payload_hash"],
                    candidate["candidate_id"],
                    records[0].event_id,
                    records[0].journal_offset,
                ),
            )
            if is_scout:
                assert recommendation is not None
                conn.execute(
                    """
                    INSERT INTO reference_recommendations(
                      recommendation_id,scout_run_id,reference_id,source_class,
                      locator_observed,access_state,found_by_seat_id,
                      evaluated_by_seat_id,evaluation,why_inspect,
                      comparability_state,message_id,payload_ref,payload_hash,
                      source_event_id,source_through_offset
                    ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    """,
                    (
                        recommendation["recommendation_id"],
                        bound["scout_run_id"],
                        recommendation["reference_id"],
                        recommendation["source_class"],
                        recommendation["locator_observed"],
                        recommendation["access_state"],
                        recommendation["found_by_seat_id"],
                        recommendation["evaluated_by_seat_id"],
                        recommendation["evaluation"],
                        recommendation["why_inspect"],
                        recommendation["comparability_state"],
                        candidate["message_id"],
                        candidate["payload_ref"],
                        candidate["payload_hash"],
                        records[0].event_id,
                        records[0].journal_offset,
                    ),
                )
                updated_run = conn.execute(
                    """
                    UPDATE reference_scout_runs
                    SET state='collecting',last_event_id=?,source_through_offset=?
                    WHERE scout_run_id=? AND state IN ('requested','collecting')
                    """,
                    (
                        records[0].event_id,
                        records[0].journal_offset,
                        bound["scout_run_id"],
                    ),
                )
                if updated_run.rowcount != 1:
                    raise ConflictError("Scout recommendation state CAS lost")

        return self.journal.accept(
            command,
            [event],
            next_state={
                "phase": "official",
                "official_message_id": candidate["message_id"],
            },
            result_builder=result,
            mutate=mutate,
        )

    def commit_reference_scout(
        self,
        *,
        token: str,
        scout_run_id: str,
        idempotency_key: str = "commit",
    ) -> dict[str, Any]:
        context = self.capabilities.resolve(
            token, action="scout.commit", phase="finalize"
        )
        bound = context.context
        if bound.get("scout_run_id") != scout_run_id:
            raise AuthorizationError("Scout commit scope mismatch")
        aggregate_id = bound["aggregate_id"]
        with self.database.connect() as conn:
            prior = conn.execute(
                """
                SELECT result_receipt_json FROM command_receipts
                WHERE scope_key=? AND idempotency_key=?
                """,
                (f"{aggregate_id}:commit", idempotency_key),
            ).fetchone()
            run = conn.execute(
                "SELECT * FROM reference_scout_runs WHERE scout_run_id=?",
                (scout_run_id,),
            ).fetchone()
            recommendations = conn.execute(
                """
                SELECT recommendation_id,reference_id,source_class,locator_observed,
                       access_state,found_by_seat_id,evaluated_by_seat_id,evaluation,
                       why_inspect,comparability_state,message_id,payload_ref,payload_hash
                FROM reference_recommendations
                WHERE scout_run_id=? ORDER BY recommendation_id
                """,
                (scout_run_id,),
            ).fetchall()
        if prior:
            return json.loads(prior["result_receipt_json"])
        if not run or run["state"] not in {"requested", "collecting"}:
            raise ConflictError("only an uncommitted Scout can be committed")
        bundle = {
            "schema": "aci.reference-scout-bundle/v1",
            "scout_run_id": scout_run_id,
            "probe_id": run["probe_id"],
            "recommendations": [dict(row) for row in recommendations],
        }
        bundle_artifact = self.artifacts.prepare(
            canonical_bytes(bundle),
            media_type="application/json",
            schema_ref="aci.reference-scout-bundle@1",
            classification="sensitive-output",
        )
        committed_at = self.now().isoformat()
        payload = {
            "scout_run_id": scout_run_id,
            "probe_id": run["probe_id"],
            "bundle_artifact_id": bundle_artifact.artifact_id,
            "bundle_digest": bundle_artifact.content_hash,
            "recommendation_ids": [
                row["recommendation_id"] for row in recommendations
            ],
            "committed_at": committed_at,
            "actor_ref": context.principal_id,
        }
        head = self.journal.head(aggregate_id)
        command = self._command(
            command_name="aci.commit-reference-scout-bundle@1",
            scope_key=f"{aggregate_id}:commit",
            idempotency_key=idempotency_key,
            aggregate_type="aci.reference-scout",
            aggregate_id=aggregate_id,
            expected_version=head["current_version"],
            authority={
                "capability_id": context.capability_id,
                "principal_id": context.principal_id,
                "action": "scout.commit",
                "phase": "finalize",
            },
            intent=payload,
        )
        event = self._event("reference_scout.bundle_committed@1", payload)

        def mutate(conn, records, _result):
            updated = conn.execute(
                """
                UPDATE reference_scout_runs
                SET state='committed',bundle_artifact_id=?,bundle_digest=?,
                    committed_at=?,last_event_id=?,source_through_offset=?
                WHERE scout_run_id=? AND state IN ('requested','collecting')
                """,
                (
                    bundle_artifact.artifact_id,
                    bundle_artifact.content_hash,
                    committed_at,
                    records[0].event_id,
                    records[0].journal_offset,
                    scout_run_id,
                ),
            )
            if updated.rowcount != 1:
                raise ConflictError("Scout commit state CAS lost")

        def result(records, base):
            return {
                **base,
                "scout_bundle": {
                    "scout_run_id": scout_run_id,
                    "state": "committed",
                    "bundle_artifact_id": bundle_artifact.artifact_id,
                    "bundle_digest": bundle_artifact.content_hash,
                    "recommendation_count": len(recommendations),
                    "event_id": records[0].event_id,
                },
            }

        return self.journal.accept(
            command,
            [event],
            next_state=payload,
            additional_artifacts=(bundle_artifact,),
            result_builder=result,
            mutate=mutate,
        )

    def deliver_reference_scout(
        self,
        *,
        token: str,
        scout_run_id: str,
        idempotency_key: str = "deliver",
    ) -> dict[str, Any]:
        context = self.capabilities.resolve(
            token, action="scout.deliver", phase="deliver"
        )
        bound = context.context
        if bound.get("scout_run_id") != scout_run_id:
            raise AuthorizationError("Scout delivery scope mismatch")
        aggregate_id = bound["aggregate_id"]
        with self.database.connect() as conn:
            prior = conn.execute(
                """
                SELECT result_receipt_json FROM command_receipts
                WHERE scope_key=? AND idempotency_key=?
                """,
                (f"{aggregate_id}:deliver", idempotency_key),
            ).fetchone()
            run = conn.execute(
                "SELECT * FROM reference_scout_runs WHERE scout_run_id=?",
                (scout_run_id,),
            ).fetchone()
        if prior:
            return json.loads(prior["result_receipt_json"])
        if not run or run["state"] != "committed":
            raise ConflictError("only a committed Scout can be delivered")
        delivered_at = self.now().isoformat()
        payload = {
            "scout_run_id": scout_run_id,
            "probe_id": run["probe_id"],
            "bundle_artifact_id": run["bundle_artifact_id"],
            "bundle_digest": run["bundle_digest"],
            "delivered_at": delivered_at,
            "actor_ref": context.principal_id,
        }
        head = self.journal.head(aggregate_id)
        command = self._command(
            command_name="aci.deliver-reference-scout-bundle@1",
            scope_key=f"{aggregate_id}:deliver",
            idempotency_key=idempotency_key,
            aggregate_type="aci.reference-scout",
            aggregate_id=aggregate_id,
            expected_version=head["current_version"],
            authority={
                "capability_id": context.capability_id,
                "principal_id": context.principal_id,
                "action": "scout.deliver",
                "phase": "deliver",
            },
            intent=payload,
        )
        event = self._event("reference_scout.bundle_delivered@1", payload)

        def mutate(conn, records, _result):
            updated = conn.execute(
                """
                UPDATE reference_scout_runs
                SET state='delivered',delivered_at=?,last_event_id=?,
                    source_through_offset=?
                WHERE scout_run_id=? AND state='committed'
                """,
                (
                    delivered_at,
                    records[0].event_id,
                    records[0].journal_offset,
                    scout_run_id,
                ),
            )
            if updated.rowcount != 1:
                raise ConflictError("Scout delivery state CAS lost")

        def result(records, base):
            return {
                **base,
                "scout_bundle": {
                    "scout_run_id": scout_run_id,
                    "state": "delivered",
                    "bundle_artifact_id": run["bundle_artifact_id"],
                    "bundle_digest": run["bundle_digest"],
                    "event_id": records[0].event_id,
                },
            }

        return self.journal.accept(
            command,
            [event],
            next_state=payload,
            result_builder=result,
            mutate=mutate,
        )

    def close_collection(
        self,
        *,
        token: str,
        group_aggregate_id: str,
        round_id: str,
        idempotency_key: str = "close",
        failpoint: Callable[[str], None] | None = None,
    ) -> dict[str, Any]:
        """Freeze only receipt-verified official contributions; visibility stays sealed."""
        context = self.capabilities.resolve(token, action="bus.close", phase="collect")
        if context.context != {
            "group_aggregate_id": group_aggregate_id,
            "round_id": round_id,
        }:
            raise AuthorizationError("collection close capability scope mismatch")
        scope_key = f"{group_aggregate_id}:{round_id}:close"
        with self.database.connect() as conn:
            prior = conn.execute(
                "SELECT result_receipt_json FROM command_receipts "
                "WHERE scope_key=? AND idempotency_key=?",
                (scope_key, idempotency_key),
            ).fetchone()
            messages = conn.execute(
                """
                SELECT message_id,payload_hash FROM messages
                WHERE group_aggregate_id=? AND round_id=?
                ORDER BY accepted_offset,message_id
                """,
                (group_aggregate_id, round_id),
            ).fetchall()
        if prior:
            return json.loads(prior["result_receipt_json"])
        entries = [dict(row) for row in messages]
        closure_id = self._stable_id("cls_", [group_aggregate_id, round_id])
        frozen_set_hash = canonical_digest(entries)
        payload = {
            "collection_closure_id": closure_id,
            "group_aggregate_id": group_aggregate_id,
            "round_id": round_id,
            "message_entries": entries,
            "frozen_set_hash": frozen_set_hash,
            "expected_seat_count": 2,
            "received_seat_count": len(entries),
            "quorum_status": "quorum" if len(entries) == 2 else "no_quorum",
        }
        head = self.journal.head(group_aggregate_id)
        command = self._command(
            command_name="aci.close-collection@1",
            scope_key=scope_key,
            idempotency_key=idempotency_key,
            aggregate_type="aci.group",
            aggregate_id=group_aggregate_id,
            expected_version=head["current_version"],
            authority={
                "capability_id": context.capability_id,
                "principal_id": context.principal_id,
                "action": "bus.close",
                "phase": "collect",
            },
            intent=payload,
        )
        event = self._event("collection.closed", payload)

        def mutate(conn, records, _result):
            conn.execute(
                """
                INSERT INTO collection_closures(
                  collection_closure_id,group_aggregate_id,round_id,
                  message_entries_json,frozen_set_hash,expected_seat_count,
                  received_seat_count,quorum_status,closed_event_id,closed_offset
                ) VALUES(?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    closure_id,
                    group_aggregate_id,
                    round_id,
                    canonical_text(entries),
                    frozen_set_hash,
                    2,
                    len(entries),
                    payload["quorum_status"],
                    records[0].event_id,
                    records[0].journal_offset,
                ),
            )

        def result(records, base):
            return {
                **base,
                "collection_closure": {
                    **payload,
                    "closed_event_id": records[0].event_id,
                    "closed_offset": records[0].journal_offset,
                    "peer_visibility": "sealed",
                },
            }

        return self.journal.accept(
            command,
            [event],
            next_state={"phase": "revealing", "closure": payload},
            result_builder=result,
            mutate=mutate,
            failpoint=failpoint,
        )

    def publish_reveal_manifest(
        self,
        *,
        token: str,
        group_aggregate_id: str,
        round_id: str,
        message_entries: list[dict[str, Any]],
        manifest_hash: str,
        idempotency_key: str = "reveal",
        failpoint: Callable[[str], None] | None = None,
    ) -> dict[str, Any]:
        """Publish the one reveal whose ordered bytes equal the sealed close."""
        context = self.capabilities.resolve(token, action="bus.reveal", phase="reveal")
        if context.context != {
            "group_aggregate_id": group_aggregate_id,
            "round_id": round_id,
        }:
            raise AuthorizationError("reveal capability scope mismatch")
        expected_hash = canonical_digest(
            {
                "group_aggregate_id": group_aggregate_id,
                "round_id": round_id,
                "message_entries": message_entries,
            }
        )
        if manifest_hash != expected_hash:
            raise ConflictError("reveal manifest hash differs from canonical content")
        with self.database.connect() as conn:
            closure = conn.execute(
                "SELECT * FROM collection_closures "
                "WHERE group_aggregate_id=? AND round_id=?",
                (group_aggregate_id, round_id),
            ).fetchone()
            existing = conn.execute(
                "SELECT * FROM reveal_manifests "
                "WHERE group_aggregate_id=? AND round_id=?",
                (group_aggregate_id, round_id),
            ).fetchone()
        if not closure:
            raise ConflictError("collection is not closed")
        frozen_entries = json.loads(closure["message_entries_json"])
        if message_entries != frozen_entries:
            raise ConflictError("reveal membership differs from sealed collection")
        if existing:
            if (
                existing["manifest_hash"] != manifest_hash
                or json.loads(existing["message_entries_json"]) != message_entries
            ):
                raise ConflictError("reveal manifest already exists with different bytes")
            with self.database.connect() as conn:
                row = conn.execute(
                    """
                    SELECT cr.result_receipt_json FROM events e
                    JOIN command_receipts cr ON cr.command_id=e.command_id
                    WHERE e.event_id=?
                    """,
                    (existing["reveal_event_id"],),
                ).fetchone()
            if row:
                return json.loads(row["result_receipt_json"])
            raise IntegrityError("reveal manifest lacks command receipt")
        reveal_manifest_id = self._stable_id(
            "rvl_", [group_aggregate_id, round_id]
        )
        payload = {
            "reveal_manifest_id": reveal_manifest_id,
            "manifest_hash": manifest_hash,
            "group_aggregate_id": group_aggregate_id,
            "group_version": self.journal.head(group_aggregate_id)["current_version"],
            "round_id": round_id,
            "message_entries": message_entries,
            "authorized_principals": ["fixed-seat-0", "fixed-seat-1"],
            "target_next_phase": "voting",
            "collection_closed_event_id": closure["closed_event_id"],
        }
        head = self.journal.head(group_aggregate_id)
        command = self._command(
            command_name="aci.publish-reveal-manifest@1",
            scope_key=f"{group_aggregate_id}:{round_id}:reveal",
            idempotency_key=idempotency_key,
            aggregate_type="aci.group",
            aggregate_id=group_aggregate_id,
            expected_version=head["current_version"],
            authority={
                "capability_id": context.capability_id,
                "principal_id": context.principal_id,
                "action": "bus.reveal",
                "phase": "reveal",
            },
            intent=payload,
        )
        event = self._event("reveal.published", payload)

        def mutate(conn, records, _result):
            conn.execute(
                """
                INSERT INTO reveal_manifests(
                  reveal_manifest_id,group_aggregate_id,round_id,
                  message_entries_json,manifest_hash,collection_closed_event_id,
                  reveal_event_id,reveal_offset
                ) VALUES(?,?,?,?,?,?,?,?)
                """,
                (
                    reveal_manifest_id,
                    group_aggregate_id,
                    round_id,
                    canonical_text(message_entries),
                    manifest_hash,
                    closure["closed_event_id"],
                    records[0].event_id,
                    records[0].journal_offset,
                ),
            )

        def result(records, base):
            return {
                **base,
                "reveal_manifest": {
                    **payload,
                    "reveal_event_id": records[0].event_id,
                    "reveal_offset": records[0].journal_offset,
                },
            }

        return self.journal.accept(
            command,
            [event],
            next_state={"phase": "voting", "reveal": payload},
            result_builder=result,
            mutate=mutate,
            failpoint=failpoint,
        )

    def authorize_agent_invocation_plan(
        self, *, token: str, binding_id: str, plan: dict[str, Any]
    ) -> dict[str, str]:
        """Persist a trusted scheduler plan before target-attempt acceptance."""
        context = self.capabilities.resolve(token, action="bus.plan", phase="plan")
        validate_invocation_plan(plan)
        if plan["binding_id"] != binding_id:
            raise ConflictError("invocation plan binding differs")
        plan_digest = canonical_digest(plan)
        plan_ref = "plan_" + plan_digest.removeprefix("sha256:")[:32]
        with self.database.write() as conn:
            binding = conn.execute(
                "SELECT * FROM host_workflow_turn_bindings WHERE binding_id=?",
                (binding_id,),
            ).fetchone()
            if not binding or binding["state"] != "running":
                raise ConflictError("target binding is not running")
            target = derive_target_identity(dict(binding))
            canonical_group = (
                f"aci.group:{binding['dispatch_id']}:{binding['group_id']}"
            )
            canonical_provider = f"aci.host.{binding['host']}@1"
            canonical_adapter = "aci.fixed-local-peer-input-materializer@1"
            expected_authority = {
                "binding_id": binding_id,
                "group_aggregate_id": canonical_group,
                "target_attempt_id": target["target_attempt_id"],
                "target_seat_id": target["target_seat_id"],
                "provider_ref": canonical_provider,
                "adapter_ref": canonical_adapter,
            }
            if context.context != expected_authority:
                raise AuthorizationError("invocation plan capability scope is not canonical")
            if (
                plan["attempt_id"] != target["target_attempt_id"]
                or plan["seat_id"] != target["target_seat_id"]
                or plan["group_aggregate_id"] != canonical_group
                or plan["provider_ref"] != canonical_provider
                or plan["adapter_ref"] != canonical_adapter
            ):
                raise AuthorizationError("invocation plan authority differs from binding")
            existing = conn.execute(
                "SELECT plan_digest FROM agent_invocation_plans WHERE plan_ref=?",
                (plan_ref,),
            ).fetchone()
            if existing and existing["plan_digest"] != plan_digest:
                raise IdempotencyConflict("invocation plan identity drift")
            if not existing:
                conn.execute(
                    """
                    INSERT INTO agent_invocation_plans(
                      plan_ref,plan_digest,binding_id,attempt_id,operation_id,
                      seat_id,group_aggregate_id,plan_json
                    ) VALUES(?,?,?,?,?,?,?,?)
                    """,
                    (
                        plan_ref,
                        plan_digest,
                        binding_id,
                        plan["attempt_id"],
                        plan["operation_id"],
                        plan["seat_id"],
                        plan["group_aggregate_id"],
                        canonical_text(plan),
                    ),
                )
        return {"plan_ref": plan_ref, "plan_digest": plan_digest}

    def materialize_authorized_peer_input(
        self,
        *,
        token: str,
        reveal_manifest_id: str,
        visibility_policy_ref: str,
        idempotency_key: str,
        failpoint: Callable[[str], None] | None = None,
    ) -> dict[str, Any]:
        """Atomically bind authorized reveal entries to a requested Attempt."""
        context = self.capabilities.resolve(
            token, action="bus.materialize", phase="reveal"
        )
        bound = context.context
        if set(bound) != {
            "agent_invocation_plan_ref",
            "agent_invocation_plan_digest",
            "target_attempt_id",
            "target_seat_id",
        }:
            raise AuthorizationError("peer materialization capability shape is invalid")
        if visibility_policy_ref != VISIBILITY_POLICY_REF:
            raise ValidationError("peer visibility policy is not admitted")
        with self.database.connect() as conn:
            plan_row = conn.execute(
                "SELECT * FROM agent_invocation_plans WHERE plan_ref=?",
                (bound["agent_invocation_plan_ref"],),
            ).fetchone()
            manifest_row = conn.execute(
                "SELECT * FROM reveal_manifests WHERE reveal_manifest_id=?",
                (reveal_manifest_id,),
            ).fetchone()
        if not plan_row or plan_row["plan_digest"] != bound["agent_invocation_plan_digest"]:
            raise ConflictError("invocation plan binding differs")
        plan = parse_strict_json(plan_row["plan_json"])
        validate_invocation_plan(plan)
        if (
            canonical_digest(plan) != plan_row["plan_digest"]
            or plan["attempt_id"] != bound["target_attempt_id"]
            or plan["seat_id"] != bound["target_seat_id"]
        ):
            raise AuthorizationError("target authority differs from invocation plan")
        if not manifest_row or plan["group_aggregate_id"] != manifest_row["group_aggregate_id"]:
            raise AuthorizationError("source and target groups differ")
        manifest_entries = json.loads(manifest_row["message_entries_json"])
        with self.database.connect() as conn:
            official_rows = conn.execute(
                """
                SELECT m.*,a.content_hash AS artifact_content_hash
                FROM messages m JOIN artifacts a ON a.artifact_id=m.payload_ref
                WHERE m.group_aggregate_id=? AND m.round_id=?
                ORDER BY m.accepted_offset,m.message_id
                """,
                (manifest_row["group_aggregate_id"], manifest_row["round_id"]),
            ).fetchall()
            base_rows = []
            for ref in (plan["base_snapshot_ref"], plan["role_delta_ref"]):
                if ref is None:
                    continue
                row = conn.execute(
                    "SELECT body,content_hash FROM artifacts WHERE artifact_id=?", (ref,)
                ).fetchone()
                if not row or digest_bytes(bytes(row["body"])) != row["content_hash"]:
                    raise IntegrityError("invocation plan input artifact is missing or corrupt")
                base_rows.extend(parse_strict_json(bytes(row["body"]))["entries"])
        peer_entries = build_peer_entries(
            reveal_manifest_id=reveal_manifest_id,
            manifest_entries=manifest_entries,
            official_messages=[dict(row) for row in official_rows],
            target_seat_id=plan["seat_id"],
            visibility_policy_ref=visibility_policy_ref,
        )
        effective_input_id = preallocate_effective_input_id(
            plan_digest=plan_row["plan_digest"],
            reveal_manifest_id=reveal_manifest_id,
            target_attempt_id=plan["attempt_id"],
        )
        prepared_entries = base_rows + peer_entries
        materialized, wrapper_bytes = deterministic_materialize(
            plan=plan,
            plan_digest=plan_row["plan_digest"],
            effective_input_artifact_id=effective_input_id,
            prepared_entries=prepared_entries,
        )
        wrapper = self.artifacts.prepare(
            wrapper_bytes,
            media_type="application/json",
            schema_ref="aci.fixed-provider-invocation@1",
            classification="sensitive-input",
        )
        if wrapper.artifact_id != materialized["provider_invocation_ref"]:
            raise IntegrityError("deterministic wrapper identity differs")
        manifest, manifest_bytes = build_peer_effective_input_manifest(
            plan=plan,
            effective_input_artifact_id=effective_input_id,
            base_entries=base_rows,
            peer_entries=peer_entries,
            reveal_manifest_entries=manifest_entries,
            provider_invocation_ref=wrapper.artifact_id,
            provider_invocation_hash=wrapper.content_hash,
        )
        event_id = self._stable_id(
            "evt_", ["peer-input", reveal_manifest_id, plan["attempt_id"]]
        )
        attempt_event_id = self._stable_id(
            "evt_", ["attempt-requested", plan["attempt_id"]]
        )
        effective_input = replace(
            self.artifacts.prepare(
                manifest_bytes,
                media_type="application/json",
                schema_ref="aci.effective-input-artifact@1",
                classification="sensitive-input",
                created_event_id=event_id,
            ),
            artifact_id=effective_input_id,
        )
        delivery_id = self._stable_id(
            "pid_", [reveal_manifest_id, plan["attempt_id"]]
        )
        request_id = self._stable_id("req_", plan["attempt_id"])
        request_binding_id = self._stable_id("rqb_", request_id)
        materialized_id = self._stable_id("mai_", [plan_row["plan_ref"], delivery_id])
        effect_id = self._stable_id("eff_", ["sandbox-launch", request_id])
        request_body = {
            "attempt_id": plan["attempt_id"],
            "operation_id": plan["operation_id"],
            "seat_id": plan["seat_id"],
            "provider_ref": plan["provider_ref"],
            "adapter_ref": plan["adapter_ref"],
            "model_ref": plan["model_ref"],
            "plan_digest": plan_row["plan_digest"],
            "materialization_digest": materialized["materialization_digest"],
            "effective_input_ref": effective_input.artifact_id,
            "provider_invocation_ref": wrapper.artifact_id,
            "response_schema_ref": plan["response_schema_ref"],
            "tool_profile_ref": plan["tool_profile_ref"],
            "deadline": plan["deadline"],
            "resource_budget": plan["resource_budget"],
            "sandbox_policy": plan["sandbox_policy"],
            "authority_fence": plan["authority_fence"],
        }
        request_digest = canonical_digest(request_body)
        semantic_digest = canonical_digest(
            {
                "reveal_manifest_id": reveal_manifest_id,
                "manifest_hash": manifest_row["manifest_hash"],
                "target_attempt_id": plan["attempt_id"],
                "target_seat_id": plan["seat_id"],
                "peer_message_entries": peer_entries,
                "effective_input_artifact_id": effective_input.artifact_id,
                "effective_input_manifest_hash": effective_input.content_hash,
                "visibility_policy_ref": visibility_policy_ref,
            }
        )
        with self.database.connect() as conn:
            existing_delivery = conn.execute(
                """
                SELECT d.*,e.command_id FROM peer_input_deliveries d
                JOIN events e ON e.event_id=d.accepted_event_id
                WHERE d.reveal_manifest_id=? AND d.target_attempt_id=?
                """,
                (reveal_manifest_id, plan["attempt_id"]),
            ).fetchone()
            existing_result = (
                conn.execute(
                    "SELECT result_receipt_json FROM command_receipts WHERE command_id=?",
                    (existing_delivery["command_id"],),
                ).fetchone()
                if existing_delivery
                else None
            )
        if existing_delivery:
            if (
                existing_delivery["idempotency_key"] != idempotency_key
                or existing_delivery["semantic_digest"] != semantic_digest
            ):
                raise IdempotencyConflict("peer input delivery semantic identity drift")
            if not existing_result:
                raise IntegrityError("peer input delivery lacks stored command receipt")
            return json.loads(existing_result["result_receipt_json"])
        delivery_payload = {
            "peer_input_delivery_id": delivery_id,
            "reveal_manifest_id": reveal_manifest_id,
            "reveal_manifest_hash": manifest_row["manifest_hash"],
            "reveal_event_id": manifest_row["reveal_event_id"],
            "source_group_aggregate_id": manifest_row["group_aggregate_id"],
            "source_round_id": manifest_row["round_id"],
            "target_attempt_id": plan["attempt_id"],
            "target_seat_id": plan["seat_id"],
            "peer_message_entries": peer_entries,
            "effective_input_artifact_id": effective_input.artifact_id,
            "effective_input_manifest_hash": effective_input.content_hash,
            "visibility_policy_ref": visibility_policy_ref,
            "idempotency_key": idempotency_key,
        }
        attempt_payload = {
            "attempt_id": plan["attempt_id"],
            "dispatch_id": self._binding_dispatch(plan["binding_id"]),
            "operation_id": plan["operation_id"],
            "seat_id": plan["seat_id"],
            "agent_instance_id": self._stable_id("agi_", [plan["binding_id"], plan["seat_id"]]),
            "provider_ref": plan["provider_ref"],
            "adapter_ref": plan["adapter_ref"],
            "model_ref": plan["model_ref"],
            "effective_input_artifact_id": effective_input.artifact_id,
            "request_id": request_id,
            "request_digest": request_digest,
            "sandbox_launch_effect_id": effect_id,
        }
        aggregate_id = f"aci.agent-attempt:{plan['attempt_id']}"
        reveal_head = self.journal.head(manifest_row["group_aggregate_id"])
        command = self._command(
            command_name="aci.materialize-authorized-peer-input@1",
            scope_key=f"{aggregate_id}:peer-input:{reveal_manifest_id}",
            idempotency_key=idempotency_key,
            aggregate_type="aci.agent-attempt",
            aggregate_id=aggregate_id,
            expected_version=0,
            authority={
                "capability_id": context.capability_id,
                "principal_id": context.principal_id,
                "action": "bus.materialize",
                "phase": "reveal",
                **bound,
            },
            intent={
                "delivery": delivery_payload,
                "plan_ref": plan_row["plan_ref"],
                "plan_digest": plan_row["plan_digest"],
                "materialized_invocation": materialized,
                "request_digest": request_digest,
                "semantic_digest": semantic_digest,
            },
            prerequisites=(
                PrerequisiteHead(
                    reveal_head["aggregate_id"],
                    reveal_head["current_version"],
                    reveal_head["state_hash"],
                ),
            ),
        )
        delivery_event = self._event(
            "peer_input.materialized", delivery_payload, event_id=event_id
        )
        attempt_event = self._event(
            "attempt.requested", attempt_payload, event_id=attempt_event_id
        )
        accepted_at = self.now().isoformat()
        fp = failpoint or (lambda _: None)

        def mutate(conn, records, result_receipt):
            conn.execute(
                """
                INSERT INTO agent_attempts(
                  attempt_id,host_workflow_binding_id,dispatch_id,operation_id,
                  seat_id,agent_instance_id,provider_ref,adapter_ref,model_ref,
                  effective_input_artifact_id,request_digest,state,
                  requested_event_id,requested_offset
                ) VALUES(?,?,?,?,?,?,?,?,?,?,?,'requested',?,?)
                """,
                (
                    plan["attempt_id"], plan["binding_id"], attempt_payload["dispatch_id"],
                    plan["operation_id"], plan["seat_id"],
                    attempt_payload["agent_instance_id"], plan["provider_ref"],
                    plan["adapter_ref"], plan["model_ref"], effective_input.artifact_id,
                    request_digest, records[1].event_id, records[1].journal_offset,
                ),
            )
            fp("after_attempt")
            conn.execute(
                """
                INSERT INTO effective_input_artifacts(
                  effective_input_artifact_id,attempt_id,manifest_hash,
                  entries_json,entry_count
                ) VALUES(?,?,?,?,?)
                """,
                (
                    effective_input.artifact_id, plan["attempt_id"],
                    effective_input.content_hash, canonical_text(manifest["entries"]),
                    len(manifest["entries"]),
                ),
            )
            fp("after_effective_input")
            conn.execute(
                """
                INSERT INTO materialized_agent_invocations(
                  materialized_invocation_id,attempt_id,plan_ref,plan_digest,
                  effective_input_artifact_id,provider_invocation_ref,
                  adapter_wrapper_refs_json,materialization_json,materialization_digest
                ) VALUES(?,?,?,?,?,?,?,?,?)
                """,
                (
                    materialized_id, plan["attempt_id"], plan_row["plan_ref"],
                    plan_row["plan_digest"], effective_input.artifact_id,
                    wrapper.artifact_id, canonical_text([wrapper.artifact_id]),
                    canonical_text(materialized), materialized["materialization_digest"],
                ),
            )
            fp("after_materialized_invocation")
            conn.execute(
                """
                INSERT INTO agent_execution_requests(
                  request_id,attempt_id,effective_input_artifact_id,
                  request_digest,sealed_at
                ) VALUES(?,?,?,?,?)
                """,
                (
                    request_id, plan["attempt_id"], effective_input.artifact_id,
                    request_digest, accepted_at,
                ),
            )
            fp("after_execution_request")
            conn.execute(
                """
                INSERT INTO agent_request_bindings(
                  request_binding_id,request_id,materialized_invocation_id,
                  effective_input_artifact_id
                ) VALUES(?,?,?,?)
                """,
                (request_binding_id, request_id, materialized_id, effective_input.artifact_id),
            )
            fp("after_request_binding")
            conn.execute(
                """
                INSERT INTO sandbox_launch_effects(
                  effect_id,attempt_id,request_id,state,created_at
                ) VALUES(?,?,?,'pending',?)
                """,
                (effect_id, plan["attempt_id"], request_id, accepted_at),
            )
            fp("after_effect")
            conn.execute(
                """
                INSERT INTO peer_input_deliveries(
                  peer_input_delivery_id,reveal_manifest_id,source_group_aggregate_id,
                  source_round_id,target_attempt_id,target_seat_id,
                  peer_message_entries_json,effective_input_artifact_id,
                  effective_input_manifest_hash,visibility_policy_ref,idempotency_key,
                  semantic_digest,accepted_event_id,journal_offset
                ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    delivery_id, reveal_manifest_id, manifest_row["group_aggregate_id"],
                    manifest_row["round_id"], plan["attempt_id"], plan["seat_id"],
                    canonical_text(peer_entries), effective_input.artifact_id,
                    effective_input.content_hash, visibility_policy_ref, idempotency_key,
                    semantic_digest, records[0].event_id, records[0].journal_offset,
                ),
            )
            fp("after_peer_delivery")
            receipt = result_receipt["peer_input_delivery_receipt"]
            conn.execute(
                """
                INSERT INTO peer_input_delivery_receipts(
                  peer_input_delivery_id,receipt_bytes,receipt_digest
                ) VALUES(?,?,?)
                """,
                (delivery_id, canonical_bytes(receipt), canonical_digest(receipt)),
            )
            fp("after_delivery_receipt")

        def result(records, base):
            receipt = {
                "receipt_version": "aci.peer-input-delivery-receipt/v1",
                "status": "materialized",
                "event_id": records[0].event_id,
                "peer_input_delivery_id": delivery_id,
                "reveal_manifest_id": reveal_manifest_id,
                "target_attempt_id": plan["attempt_id"],
                "target_seat_id": plan["seat_id"],
                "effective_input_artifact_id": effective_input.artifact_id,
                "effective_input_manifest_hash": effective_input.content_hash,
                "idempotency_key": idempotency_key,
                "journal_offset": records[0].journal_offset,
            }
            return {
                **base,
                "peer_input_delivery_receipt": receipt,
                "attempt_requested_event_id": records[1].event_id,
                "request_id": request_id,
                "request_digest": request_digest,
                "sandbox_launch_effect_id": effect_id,
                "effect_state": "pending",
                "provider_start_count": 0,
            }

        return self.journal.accept(
            command,
            [delivery_event, attempt_event],
            next_state={"state": "requested", "delivery": delivery_payload},
            additional_artifacts=(wrapper, effective_input),
            result_builder=result,
            mutate=mutate,
            failpoint=failpoint,
        )

    def _binding_dispatch(self, binding_id: str) -> str:
        with self.database.connect() as conn:
            row = conn.execute(
                "SELECT dispatch_id FROM host_workflow_turn_bindings WHERE binding_id=?",
                (binding_id,),
            ).fetchone()
        if not row:
            raise ConflictError("target binding does not exist")
        return str(row["dispatch_id"])

    def settle_agent_reference_delivery(
        self,
        *,
        token: str,
        binding_id: str,
        scout_run_id: str,
        source_bundle_delivered_event_id: str,
        base_entries: list[dict[str, Any]],
        entry_ordinal: int,
        idempotency_key: str = "reference-delivery",
        failpoint: Callable[[str], None] | None = None,
    ) -> dict[str, Any]:
        """Atomically accept one delivered Scout bundle into one host-bound Attempt."""
        context = self.capabilities.resolve(
            token, action="reference_delivery.accept", phase="start"
        )
        bound = context.context
        if set(bound) != {
            "binding_id",
            "scout_run_id",
            "source_bundle_delivered_event_id",
            "visibility_policy_ref",
        }:
            raise AuthorizationError("reference delivery capability shape is invalid")
        if (
            bound["binding_id"] != binding_id
            or bound["scout_run_id"] != scout_run_id
            or bound["source_bundle_delivered_event_id"]
            != source_bundle_delivered_event_id
        ):
            raise AuthorizationError("reference delivery capability scope mismatch")
        visibility_policy_ref = bound["visibility_policy_ref"]
        if not isinstance(visibility_policy_ref, str) or not visibility_policy_ref:
            raise AuthorizationError("reference delivery visibility policy is invalid")
        if not isinstance(idempotency_key, str) or not idempotency_key:
            raise ValidationError("reference delivery idempotency key is required")

        with self.database.connect() as conn:
            binding_row = conn.execute(
                "SELECT * FROM host_workflow_turn_bindings WHERE binding_id=?",
                (binding_id,),
            ).fetchone()
            run = conn.execute(
                "SELECT * FROM reference_scout_runs WHERE scout_run_id=?",
                (scout_run_id,),
            ).fetchone()
            delivered_row = conn.execute(
                """
                SELECT e.*,a.body FROM events e
                JOIN artifacts a ON a.artifact_id=e.payload_ref
                WHERE e.event_id=? AND e.event_type='reference_scout.bundle_delivered@1'
                """,
                (source_bundle_delivered_event_id,),
            ).fetchone()
            committed_row = conn.execute(
                """
                SELECT e.*,a.body FROM events e
                JOIN artifacts a ON a.artifact_id=e.payload_ref
                WHERE e.event_type='reference_scout.bundle_committed@1'
                  AND json_extract(CAST(a.body AS TEXT),'$.scout_run_id')=?
                ORDER BY e.journal_offset DESC LIMIT 1
                """,
                (scout_run_id,),
            ).fetchone()
            bundle_row = (
                conn.execute(
                    "SELECT * FROM artifacts WHERE artifact_id=?",
                    (run["bundle_artifact_id"],),
                ).fetchone()
                if run and run["bundle_artifact_id"]
                else None
            )
        if not binding_row or binding_row["state"] != "running":
            raise ConflictError("target host workflow binding is not running")
        if not run or run["state"] != "delivered":
            raise ConflictError("source Scout bundle is not lifecycle-delivered")
        if run["dispatch_id"] != binding_row["dispatch_id"]:
            raise AuthorizationError("source and target dispatch scopes differ")
        if not delivered_row or not committed_row or not bundle_row:
            raise IntegrityError("reference delivery source evidence is incomplete")

        delivered_payload = parse_strict_json(bytes(delivered_row["body"]))
        committed_payload = parse_strict_json(bytes(committed_row["body"]))
        if "recommendation_ids" in delivered_payload:
            raise IntegrityError("lifecycle delivery cannot own recommendation membership")
        source_tuple = (
            scout_run_id,
            run["bundle_artifact_id"],
            run["bundle_digest"],
        )
        if (
            (
                delivered_payload.get("scout_run_id"),
                delivered_payload.get("bundle_artifact_id"),
                delivered_payload.get("bundle_digest"),
            )
            != source_tuple
            or (
                committed_payload.get("scout_run_id"),
                committed_payload.get("bundle_artifact_id"),
                committed_payload.get("bundle_digest"),
            )
            != source_tuple
            or int(committed_row["journal_offset"])
            >= int(delivered_row["journal_offset"])
        ):
            raise IntegrityError("Scout commit and lifecycle delivery do not agree")
        bundle, recommendation_ids = decode_reference_bundle(
            bytes(bundle_row["body"]), expected_digest=run["bundle_digest"]
        )
        if bundle["scout_run_id"] != scout_run_id or recommendation_ids != committed_payload.get(
            "recommendation_ids"
        ):
            raise IntegrityError("committed recommendation membership differs from bundle bytes")

        binding = dict(binding_row)
        target = derive_target_identity(binding)
        delivery_id = self._stable_id(
            "ard_", [scout_run_id, target["target_attempt_id"]]
        )
        target_event_id = self._stable_id("evt_", ["reference-delivery", delivery_id])
        attempt_event_id = self._stable_id(
            "evt_", ["attempt-requested", target["target_attempt_id"]]
        )
        manifest, manifest_bytes = build_effective_input(
            attempt_id=target["target_attempt_id"],
            base_entries=base_entries,
            entry_ordinal=entry_ordinal,
            bundle_artifact_id=run["bundle_artifact_id"],
            bundle_digest=run["bundle_digest"],
            agent_reference_delivery_id=delivery_id,
            visibility_policy_ref=visibility_policy_ref,
        )
        effective_input = self.artifacts.prepare(
            manifest_bytes,
            media_type="application/json",
            schema_ref="aci.effective-input-artifact@1",
            classification="sensitive-input",
            created_event_id=attempt_event_id,
        )
        operation_id = self._stable_id("op_", ["host-attempt", binding_id])
        request_id = self._stable_id("req_", target["target_attempt_id"])
        effect_id = self._stable_id("eff_", ["sandbox-launch", request_id])
        provider_ref = f"aci.host.{binding['host']}@1"
        adapter_ref = "aci.host-workflow-bridge@1"
        model_ref = "aci.host-model.unobserved@1"
        request_digest = canonical_digest(
            {
                "request_id": request_id,
                "attempt_id": target["target_attempt_id"],
                "effective_input_artifact_id": effective_input.artifact_id,
                "effective_input_manifest_hash": effective_input.content_hash,
                "provider_ref": provider_ref,
                "adapter_ref": adapter_ref,
                "model_ref": model_ref,
            }
        )
        delivery_payload = {
            "agent_reference_delivery_id": delivery_id,
            "dispatch_id": target["dispatch_id"],
            "scout_run_id": scout_run_id,
            "source_bundle_delivered_event_id": source_bundle_delivered_event_id,
            "bundle_artifact_id": run["bundle_artifact_id"],
            "bundle_digest": run["bundle_digest"],
            "recommendation_ids": recommendation_ids,
            "target_attempt_id": target["target_attempt_id"],
            "target_seat_id": target["target_seat_id"],
            "target_agent_instance_id": target["target_agent_instance_id"],
            "effective_input_artifact_id": effective_input.artifact_id,
            "effective_input_entry_ordinal": entry_ordinal,
            "effective_input_manifest_hash": effective_input.content_hash,
            "visibility_policy_ref": visibility_policy_ref,
            "idempotency_key": idempotency_key,
        }
        attempt_payload = {
            "attempt_id": target["target_attempt_id"],
            "dispatch_id": target["dispatch_id"],
            "operation_id": operation_id,
            "seat_id": target["target_seat_id"],
            "agent_instance_id": target["target_agent_instance_id"],
            "provider_ref": provider_ref,
            "adapter_ref": adapter_ref,
            "model_ref": model_ref,
            "effective_input_artifact_id": effective_input.artifact_id,
            "request_id": request_id,
            "request_digest": request_digest,
            "sandbox_launch_effect_id": effect_id,
        }
        aggregate_id = f"aci.agent-attempt:{target['target_attempt_id']}"
        scout_head = self.journal.head(run["group_aggregate_id"])
        binding_head = self.journal.head(f"aci.host-workflow-turn:{binding_id}")
        command = self._command(
            command_name="aci.start-host-attempt-with-reference-bundle@1",
            scope_key=aggregate_id,
            idempotency_key=idempotency_key,
            aggregate_type="aci.agent-attempt",
            aggregate_id=aggregate_id,
            expected_version=0,
            authority={
                "capability_id": context.capability_id,
                "principal_id": context.principal_id,
                "action": "reference_delivery.accept",
                "phase": "start",
                **target,
            },
            intent={
                "binding_id": binding_id,
                "delivery": delivery_payload,
                "attempt": attempt_payload,
                "effective_input": manifest,
            },
            prerequisites=(
                PrerequisiteHead(
                    scout_head["aggregate_id"],
                    scout_head["current_version"],
                    scout_head["state_hash"],
                ),
                PrerequisiteHead(
                    binding_head["aggregate_id"],
                    binding_head["current_version"],
                    binding_head["state_hash"],
                ),
            ),
        )
        delivery_event = self._event(
            "reference_scout.bundle_delivered_to_agent@1",
            delivery_payload,
            event_id=target_event_id,
        )
        attempt_event = self._event(
            "attempt.requested", attempt_payload, event_id=attempt_event_id
        )
        accepted_at = self.now().isoformat()

        def mutate(conn, records, _result):
            conn.execute(
                """
                INSERT INTO agent_attempts(
                  attempt_id,host_workflow_binding_id,dispatch_id,operation_id,
                  seat_id,agent_instance_id,provider_ref,adapter_ref,model_ref,
                  effective_input_artifact_id,request_digest,state,
                  requested_event_id,requested_offset
                ) VALUES(?,?,?,?,?,?,?,?,?,?,?,'requested',?,?)
                """,
                (
                    target["target_attempt_id"],
                    binding_id,
                    target["dispatch_id"],
                    operation_id,
                    target["target_seat_id"],
                    target["target_agent_instance_id"],
                    provider_ref,
                    adapter_ref,
                    model_ref,
                    effective_input.artifact_id,
                    request_digest,
                    records[1].event_id,
                    records[1].journal_offset,
                ),
            )
            conn.execute(
                """
                INSERT INTO effective_input_artifacts(
                  effective_input_artifact_id,attempt_id,manifest_hash,
                  entries_json,entry_count
                ) VALUES(?,?,?,?,?)
                """,
                (
                    effective_input.artifact_id,
                    target["target_attempt_id"],
                    effective_input.content_hash,
                    canonical_text(manifest["entries"]),
                    len(manifest["entries"]),
                ),
            )
            conn.execute(
                """
                INSERT INTO agent_execution_requests(
                  request_id,attempt_id,effective_input_artifact_id,
                  request_digest,sealed_at
                ) VALUES(?,?,?,?,?)
                """,
                (
                    request_id,
                    target["target_attempt_id"],
                    effective_input.artifact_id,
                    request_digest,
                    accepted_at,
                ),
            )
            conn.execute(
                """
                INSERT INTO sandbox_launch_effects(
                  effect_id,attempt_id,request_id,state,created_at
                ) VALUES(?,?,?,'pending',?)
                """,
                (effect_id, target["target_attempt_id"], request_id, accepted_at),
            )
            conn.execute(
                """
                INSERT INTO agent_reference_deliveries(
                  agent_reference_delivery_id,dispatch_id,scout_run_id,
                  source_bundle_delivered_event_id,bundle_artifact_id,bundle_digest,
                  recommendation_ids_json,target_attempt_id,target_seat_id,
                  target_agent_instance_id,effective_input_artifact_id,
                  effective_input_entry_ordinal,effective_input_manifest_hash,
                  visibility_policy_ref,idempotency_key,accepted_event_id,journal_offset
                ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    delivery_id,
                    target["dispatch_id"],
                    scout_run_id,
                    source_bundle_delivered_event_id,
                    run["bundle_artifact_id"],
                    run["bundle_digest"],
                    canonical_text(recommendation_ids),
                    target["target_attempt_id"],
                    target["target_seat_id"],
                    target["target_agent_instance_id"],
                    effective_input.artifact_id,
                    entry_ordinal,
                    effective_input.content_hash,
                    visibility_policy_ref,
                    idempotency_key,
                    records[0].event_id,
                    records[0].journal_offset,
                ),
            )

        def result(records, base):
            return {
                **base,
                "status": "launch-authorized",
                "agent_reference_delivery_id": delivery_id,
                "accepted_event_id": records[0].event_id,
                "attempt_requested_event_id": records[1].event_id,
                "target": target,
                "effective_input_artifact_id": effective_input.artifact_id,
                "effective_input_manifest_hash": effective_input.content_hash,
                "effective_input_entry_ordinal": entry_ordinal,
                "request_id": request_id,
                "request_digest": request_digest,
                "sandbox_launch_effect_id": effect_id,
            }

        return self.journal.accept(
            command,
            [delivery_event, attempt_event],
            next_state={
                "state": "requested",
                "delivery": delivery_payload,
                "attempt": attempt_payload,
            },
            additional_artifacts=(effective_input,),
            result_builder=result,
            mutate=mutate,
            failpoint=failpoint,
        )

    def get_agent_reference_target(
        self, *, attempt_id: str
    ) -> dict[str, Any]:
        with self.database.connect() as conn:
            row = conn.execute(
                """
                SELECT a.*,b.group_id,b.seat_index,b.binding_id
                FROM agent_attempts a
                JOIN host_workflow_turn_bindings b
                  ON b.binding_id=a.host_workflow_binding_id
                WHERE a.attempt_id=?
                """,
                (attempt_id,),
            ).fetchone()
        if not row:
            raise NotFoundError("agent reference target is not found")
        target = {
            "dispatch_id": row["dispatch_id"],
            "target_attempt_id": row["attempt_id"],
            "target_seat_id": row["seat_id"],
            "target_agent_instance_id": row["agent_instance_id"],
        }
        return wrap_target_resolution(
            target,
            binding_id=row["binding_id"],
            effective_as_of=int(row["requested_offset"]),
        )

    def get_agent_reference_delivery_evidence(
        self, *, attempt_id: str
    ) -> dict[str, Any]:
        with self.database.connect() as conn:
            row = conn.execute(
                """
                SELECT d.*,a.body,t.requested_offset AS group_through_offset
                FROM agent_reference_deliveries d
                JOIN artifacts a
                  ON a.artifact_id=d.effective_input_artifact_id
                JOIN agent_attempts t ON t.attempt_id=d.target_attempt_id
                WHERE d.target_attempt_id=?
                """,
                (attempt_id,),
            ).fetchone()
        if not row:
            raise NotFoundError("agent reference delivery is not found")
        delivery = dict(row)
        delivery.pop("body")
        group_through_offset = int(delivery.pop("group_through_offset"))
        delivery["recommendation_ids"] = json.loads(
            delivery.pop("recommendation_ids_json")
        )
        effective_input = parse_strict_json(bytes(row["body"]))
        # The delivery event is the first member of a two-event atomic group.
        prefix = self.journal.read_complete_groups(through=group_through_offset)
        groups = [
            group
            for group in prefix["groups"]
            if row["accepted_event_id"] in group["ordered_event_ids"]
        ]
        if len(groups) != 1:
            raise IntegrityError("delivery event does not belong to one complete group")
        group = groups[0]
        if (
            group["event_count"] != 2
            or [event["event_type"] for event in group["events"]]
            != [
                "reference_scout.bundle_delivered_to_agent@1",
                "attempt.requested",
            ]
        ):
            raise IntegrityError("delivery acceptance group is incomplete or divergent")
        return wrap_delivery_evidence(
            delivery=delivery,
            effective_input=effective_input,
            accepted_group=group,
        )

    @staticmethod
    def verify_agent_reference_wrapper(
        wrapper: dict[str, Any], *, schema: str
    ) -> dict[str, Any]:
        if schema not in {TARGET_RESOLUTION_SCHEMA, DELIVERY_EVIDENCE_SCHEMA}:
            raise ValidationError("unsupported agent reference wrapper schema")
        return verify_wrapper(wrapper, schema=schema)

    def terminate_reference_scout(
        self,
        *,
        token: str,
        scout_run_id: str,
        outcome: str,
        reason: str,
        idempotency_key: str = "terminate",
    ) -> dict[str, Any]:
        context = self.capabilities.resolve(
            token, action="scout.terminate", phase="control"
        )
        if context.context.get("scout_run_id") != scout_run_id:
            raise AuthorizationError("Scout termination scope mismatch")
        if outcome not in {"failed", "cancelled"}:
            raise ValidationError("Scout termination outcome is invalid")
        if not isinstance(reason, str) or not reason.strip():
            raise ValidationError("Scout termination reason is required")
        aggregate_id = context.context["aggregate_id"]
        scope_key = f"{aggregate_id}:terminate"
        with self.database.connect() as conn:
            prior = conn.execute(
                """
                SELECT result_receipt_json FROM command_receipts
                WHERE scope_key=? AND idempotency_key=?
                """,
                (scope_key, idempotency_key),
            ).fetchone()
            run = conn.execute(
                "SELECT * FROM reference_scout_runs WHERE scout_run_id=?",
                (scout_run_id,),
            ).fetchone()
        if prior:
            return json.loads(prior["result_receipt_json"])
        if not run or run["state"] in {"delivered", "failed", "cancelled"}:
            raise ConflictError("Reference Scout is already terminal")
        payload = {
            "scout_run_id": scout_run_id,
            "probe_id": run["probe_id"],
            "outcome": outcome,
            "reason": reason.strip(),
            "terminated_at": self.now().isoformat(),
            "actor_ref": context.principal_id,
        }
        head = self.journal.head(aggregate_id)
        command = self._command(
            command_name="aci.terminate-reference-scout@1",
            scope_key=scope_key,
            idempotency_key=idempotency_key,
            aggregate_type="aci.reference-scout",
            aggregate_id=aggregate_id,
            expected_version=head["current_version"],
            authority={
                "capability_id": context.capability_id,
                "principal_id": context.principal_id,
                "action": "scout.terminate",
                "phase": "control",
            },
            intent=payload,
        )
        event = self._event("reference_scout.terminated@1", payload)

        def mutate(conn, records, _result):
            updated = conn.execute(
                """
                UPDATE reference_scout_runs
                SET state=?,last_event_id=?,source_through_offset=?
                WHERE scout_run_id=?
                  AND state NOT IN ('delivered','failed','cancelled')
                """,
                (
                    outcome,
                    records[0].event_id,
                    records[0].journal_offset,
                    scout_run_id,
                ),
            )
            if updated.rowcount != 1:
                raise ConflictError("Scout termination state CAS lost")

        def result(records, base):
            return {
                **base,
                "scout_run": {
                    "scout_run_id": scout_run_id,
                    "state": outcome,
                    "reason": reason.strip(),
                    "event_id": records[0].event_id,
                },
            }

        return self.journal.accept(
            command,
            [event],
            next_state=payload,
            result_builder=result,
            mutate=mutate,
        )

    def record_dispatch_ingestion(
        self,
        *,
        token: str,
        intent: dict[str, Any],
        content: bytes | None = None,
    ) -> dict[str, Any]:
        """Record one observable dispatch input or one explicitly opaque access."""
        fields = {
            "agent_id",
            "tool_use_id",
            "tool_name",
            "source_kind",
            "locator",
            "repo_relative_path",
            "media_type",
            "coverage",
            "purpose",
            "observed_at",
        }
        if set(intent) != fields:
            raise ValidationError("dispatch ingestion intent field set is invalid")
        context = self.capabilities.resolve(
            token, action="ingestion.record", phase="observe"
        )
        session_id = context.context.get("session_id")
        dispatch_id = context.context.get("dispatch_id")
        host = context.context.get("host")
        if (
            not isinstance(session_id, str)
            or not session_id
            or not isinstance(dispatch_id, str)
            or not dispatch_id
            or host not in {"claude", "codex"}
        ):
            raise AuthorizationError("dispatch ingestion capability scope is incomplete")
        if context.context.get("intent_digest") != canonical_digest(intent):
            raise AuthorizationError("dispatch ingestion differs from capability")
        if context.context.get("tool_use_id") != intent["tool_use_id"]:
            raise AuthorizationError("dispatch ingestion scope mismatch")
        source_kinds = {
            "repository_file",
            "repository_search",
            "external_url",
            "mcp_resource",
            "shell_opaque",
        }
        if intent["source_kind"] not in source_kinds:
            raise ValidationError("dispatch ingestion source kind is invalid")
        if intent["coverage"] not in {"exact", "metadata_only", "opaque"}:
            raise ValidationError("dispatch ingestion coverage is invalid")
        for field in (
            "tool_use_id",
            "tool_name",
            "source_kind",
            "locator",
            "purpose",
            "observed_at",
        ):
            if not isinstance(intent[field], str) or not intent[field]:
                raise ValidationError(f"dispatch ingestion {field} is required")
        if intent["source_kind"] == "repository_file" and (
            not isinstance(intent["repo_relative_path"], str)
            or not intent["repo_relative_path"]
        ):
            raise ValidationError("repository ingestion requires a relative path")
        if intent["coverage"] == "exact" and content is None:
            raise ValidationError("exact ingestion requires captured bytes")
        if intent["coverage"] != "exact" and content is not None:
            raise ValidationError("non-exact ingestion cannot carry captured bytes")
        with self.database.connect() as conn:
            link = conn.execute(
                "SELECT * FROM dispatch_links WHERE dispatch_id=? AND session_id=?",
                (dispatch_id, session_id),
            ).fetchone()
        if not link:
            raise NotFoundError("dispatch ingestion requires an exact Session link")
        orchestration_head = self.journal.head(
            f"aci.orchestration-dispatch:{dispatch_id}"
        )
        if orchestration_head["current_version"] != 1:
            raise ConflictError(
                "dispatch ingestion is accepted only while orchestration is open"
            )
        prepared = (
            self.artifacts.prepare(
                content,
                media_type=intent["media_type"] or "application/octet-stream",
                schema_ref="aci.dispatch-ingested-input@1",
                classification="sensitive-input",
            )
            if content is not None
            else None
        )
        ingestion_id = self._stable_id(
            "ing_",
            [
                host,
                session_id,
                dispatch_id,
                intent["tool_use_id"],
                intent["locator"],
            ],
        )
        payload = {
            "ingestion_id": ingestion_id,
            "session_id": session_id,
            "dispatch_id": dispatch_id,
            "host": host,
            **intent,
            "content_digest": prepared.content_hash if prepared else None,
            "artifact_id": prepared.artifact_id if prepared else None,
            "size_bytes": len(prepared.body) if prepared else None,
        }
        aggregate_id = f"aci.dispatch-ingestion:{ingestion_id}"
        record_digest = canonical_digest(payload)
        with self.database.connect() as conn:
            prior = conn.execute(
                """
                SELECT result_receipt_json FROM command_receipts
                WHERE scope_key=? AND idempotency_key='record'
                """,
                (aggregate_id,),
            ).fetchone()
        if prior:
            prior_result = json.loads(prior["result_receipt_json"])
            if prior_result.get("record_digest") != record_digest:
                raise IdempotencyConflict(
                    "ingestion identity reused with different evidence"
                )
            return prior_result
        command = self._command(
            command_name="aci.record-dispatch-ingestion@1",
            scope_key=aggregate_id,
            idempotency_key="record",
            aggregate_type="aci.dispatch-ingestion",
            aggregate_id=aggregate_id,
            expected_version=0,
            authority={
                "capability_id": context.capability_id,
                "principal_id": context.principal_id,
                "action": "ingestion.record",
                "phase": "observe",
            },
            intent=payload,
            prerequisites=(
                PrerequisiteHead(
                    aggregate_id=orchestration_head["aggregate_id"],
                    expected_version=orchestration_head["current_version"],
                    state_hash=orchestration_head["state_hash"],
                ),
            ),
        )
        event = self._event("dispatch.ingestion_recorded@1", payload)

        def mutate(conn, records, _result):
            conn.execute(
                """
                INSERT INTO dispatch_ingestions(
                  ingestion_id,session_id,dispatch_id,host,agent_id,tool_use_id,
                  tool_name,source_kind,locator,repo_relative_path,content_digest,
                  artifact_id,media_type,size_bytes,coverage,purpose,observed_at,
                  event_id,accepted_offset
                ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    ingestion_id,
                    session_id,
                    dispatch_id,
                    host,
                    intent["agent_id"],
                    intent["tool_use_id"],
                    intent["tool_name"],
                    intent["source_kind"],
                    intent["locator"],
                    intent["repo_relative_path"],
                    prepared.content_hash if prepared else None,
                    prepared.artifact_id if prepared else None,
                    intent["media_type"],
                    len(prepared.body) if prepared else None,
                    intent["coverage"],
                    intent["purpose"],
                    intent["observed_at"],
                    records[0].event_id,
                    records[0].journal_offset,
                ),
            )

        def result(records, base):
            return {
                **base,
                "record_digest": record_digest,
                "ingestion": {
                    "ingestion_id": ingestion_id,
                    "session_id": session_id,
                    "dispatch_id": dispatch_id,
                    "coverage": intent["coverage"],
                    "content_digest": prepared.content_hash if prepared else None,
                    "artifact_id": prepared.artifact_id if prepared else None,
                    "event_id": records[0].event_id,
                },
            }

        return self.journal.accept(
            command,
            [event],
            next_state=payload,
            additional_artifacts=((prepared,) if prepared else ()),
            result_builder=result,
            mutate=mutate,
        )

    def append_apt_event(
        self,
        *,
        token: str,
        command_name: str,
        aggregate_id: str,
        expected_version: int,
        idempotency_key: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        """Trusted APT port; no APT-owned route or raw research table is created."""
        context = self.capabilities.resolve(token, action="apt.append", phase="capture")
        mapping = {
            "apt.append-research-capture@1": "apt.research_capture_appended",
            "apt.append-research-fact@1": "apt.research_fact_appended",
            "apt.append-reference-probe-lineage@1": "apt.reference_probe_lineage_appended",
        }
        event_type = mapping.get(command_name)
        if not event_type:
            raise ValidationError("unsupported APT append command")
        if command_name == "apt.append-reference-probe-lineage@1":
            return self._append_reference_lineage(
                context=context,
                aggregate_id=aggregate_id,
                expected_version=expected_version,
                idempotency_key=idempotency_key,
                request=payload,
            )
        if payload.get("actor_ref") != context.principal_id:
            raise AuthorizationError("APT payload actor is not the capability principal")
        if command_name == "apt.append-research-capture@1":
            capture = self._validate_capture_payload(payload)
            item_key = capture["research_capture_id"]
            with self.database.connect() as conn:
                existing = conn.execute(
                    "SELECT * FROM apt_capture_keys WHERE research_capture_id=?",
                    (item_key,),
                ).fetchone()
            if existing:
                if existing["capture_digest"] != self._content_digest_string(
                    capture["capture_digest"]
                ):
                    raise ConflictError("research capture identity conflict")
                return {
                    "status": "existing_exact",
                    "accepted_event_id": existing["accepted_event_id"],
                    "research_capture_id": item_key,
                }
        else:
            entity = self._validate_fact_payload(payload)
            envelope = entity["fact"]
            item_key = envelope["fact_id"]
            semantic_digest = canonical_digest(entity)
            with self.database.connect() as conn:
                existing = conn.execute(
                    "SELECT * FROM apt_semantic_facts WHERE fact_id=?", (item_key,)
                ).fetchone()
            if existing:
                exact = (
                    existing["canonical_payload_digest"] == semantic_digest
                    and existing["subject_id"] == envelope["subject_id"]
                    and existing["supersedes_fact_id"]
                    == envelope["supersedes_fact_id"]
                )
                if not exact:
                    raise ConflictError("global fact identity collision")
                return {
                    "status": "existing_exact",
                    "accepted_event_id": existing["accepted_event_id"],
                    "fact_id": item_key,
                }
        event = self._event(event_type, payload, classification="sensitive-output")
        command = self._command(
            command_name=command_name,
            scope_key=aggregate_id,
            idempotency_key=idempotency_key,
            aggregate_type=aggregate_id.split(":", 1)[0],
            aggregate_id=aggregate_id,
            expected_version=expected_version,
            authority={
                "capability_id": context.capability_id,
                "principal_id": context.principal_id,
                "action": "apt.append",
            },
            intent={"payload_digest": canonical_digest(payload)},
        )

        def mutate(conn, records, result):
            if command_name == "apt.append-research-capture@1":
                if capture["supersedes_capture_id"]:
                    updated = conn.execute(
                        """
                        UPDATE apt_capture_keys SET is_current=0
                        WHERE research_capture_id=? AND is_current=1
                        """,
                        (capture["supersedes_capture_id"],),
                    )
                    if updated.rowcount != 1:
                        raise ConflictError("capture predecessor is not current")
                conn.execute(
                    """
                    INSERT INTO apt_capture_keys(
                      research_capture_id,dispatch_id,expected_contribution_id,
                      capture_operation_id,supersedes_capture_id,capture_digest,
                      accepted_event_id,is_current
                    ) VALUES(?,?,?,?,?,?,?,1)
                    """,
                    (
                        capture["research_capture_id"],
                        capture["dispatch_id"],
                        capture["expected_contribution_id"],
                        capture["capture_operation_id"],
                        capture["supersedes_capture_id"],
                        self._content_digest_string(capture["capture_digest"]),
                        records[0].event_id,
                    ),
                )
            elif command_name == "apt.append-research-fact@1":
                envelope = entity["fact"]
                predecessor = envelope["supersedes_fact_id"]
                if predecessor:
                    updated = conn.execute(
                        """
                        UPDATE apt_semantic_facts SET is_current=0
                        WHERE fact_id=? AND subject_id=? AND is_current=1
                        """,
                        (predecessor, envelope["subject_id"]),
                    )
                    if updated.rowcount != 1:
                        raise ConflictError("fact predecessor is not current")
                conn.execute(
                    """
                    INSERT INTO apt_semantic_facts(
                      fact_id,research_capture_id,subject_id,fact_kind,supersedes_fact_id,
                      canonical_payload_digest,accepted_event_id,is_current
                    ) VALUES(?,?,?,?,?,?,?,1)
                    """,
                    (
                        envelope["fact_id"],
                        entity["research_capture_id"],
                        envelope["subject_id"],
                        payload["payload_variant"],
                        predecessor,
                        canonical_digest(entity),
                        records[0].event_id,
                    ),
                )
            conn.execute(
                """
                INSERT INTO apt_semantic_request_results(
                  request_key,item_key,request_digest,result_status,result_json,
                  accepted_event_id
                ) VALUES(?,?,?,?,?,?)
                """,
                (
                    f"{aggregate_id}:{idempotency_key}",
                    item_key,
                    command.digest,
                    "accepted_new",
                    canonical_text(result),
                    records[0].event_id,
                ),
            )
            self.projections.apply_complete_group(
                conn,
                projection_name="apt.research-record",
                projection_key=(
                    capture["research_capture_id"]
                    if command_name == "apt.append-research-capture@1"
                    else entity["research_capture_id"]
                ),
                events=[
                    {
                        "event_type": event_type,
                        "payload": payload,
                        "event_id": records[0].event_id,
                        "journal_offset": records[0].journal_offset,
                    }
                ],
                last_offset=records[0].journal_offset,
            )

        return self.journal.accept(
            command, [event], next_state={"last_payload_digest": canonical_digest(payload)}, mutate=mutate
        )

    def _validate_capture_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        if set(payload) != {"research_capture", "session_dispatch_link_id", "actor_ref"}:
            raise ValidationError("research capture event field set is invalid")
        capture = payload["research_capture"]
        required = {
            "schema_ref",
            "research_capture_id",
            "expected_contribution_id",
            "capture_operation_id",
            "dispatch_id",
            "dispatch_snapshot_ref",
            "origin_refs",
            "producer_ref",
            "capture_status",
            "raw_return",
            "partial_reason",
            "failure_reason",
            "failure_evidence_ref",
            "supersedes_capture_id",
            "synthesizes",
            "captured_at",
            "capture_digest",
        }
        if not isinstance(capture, dict) or set(capture) != required:
            raise ValidationError("research capture entity field set is invalid")
        if capture["schema_ref"] != "apt.research-capture@1":
            raise ValidationError("research capture schema_ref is invalid")
        preimage = {key: capture[key] for key in capture if key != "capture_digest"}
        if canonical_digest(preimage) != self._content_digest_string(
            capture["capture_digest"]
        ):
            raise ValidationError("research capture digest mismatch")
        with self.database.connect() as conn:
            link = conn.execute(
                "SELECT * FROM dispatch_links WHERE dispatch_id=?",
                (capture["dispatch_id"],),
            ).fetchone()
            raw_ref = capture["raw_return"]
            artifact = (
                conn.execute(
                    "SELECT * FROM artifacts WHERE artifact_id=?",
                    (raw_ref["artifact_id"],),
                ).fetchone()
                if raw_ref
                else None
            )
        if (
            not link
            or payload["session_dispatch_link_id"]
            != self._stable_id(
                "lnk_",
                [link["session_id"], capture["dispatch_id"], link["row_digest"]],
            )
            or capture["dispatch_snapshot_ref"].get("kind") != "legacy_ledger"
            or self._content_digest_string(
                capture["dispatch_snapshot_ref"].get("row_digest")
            )
            != link["row_digest"]
        ):
            raise ConflictError("capture dispatch link is missing")
        status = capture["capture_status"]
        if status not in {"captured", "partial", "missing"}:
            raise ValidationError("capture status is invalid")
        if status == "captured":
            if (
                not artifact
                or raw_ref["content_digest"]
                != {
                    "algorithm": "sha256",
                    "value": artifact["content_hash"].removeprefix("sha256:"),
                }
                or raw_ref["charset"] != "utf-8"
            ):
                raise ValidationError("capture raw artifact evidence is invalid")
            if any(
                capture[key] is not None
                for key in ("partial_reason", "failure_reason", "failure_evidence_ref")
            ):
                raise ValidationError("captured status evidence matrix is invalid")
        elif status == "partial":
            if not artifact or not capture["partial_reason"] or capture["failure_reason"]:
                raise ValidationError("partial status evidence matrix is invalid")
        elif (
            artifact is not None
            or capture["raw_return"] is not None
            or not capture["failure_reason"]
            or capture["failure_evidence_ref"] is None
            or capture["partial_reason"] is not None
        ):
            raise ValidationError("missing status evidence matrix is invalid")
        with self.database.connect() as conn:
            current = conn.execute(
                """
                SELECT research_capture_id,capture_digest FROM apt_capture_keys
                WHERE dispatch_id=? AND expected_contribution_id=? AND is_current=1
                """,
                (capture["dispatch_id"], capture["expected_contribution_id"]),
            ).fetchone()
        expected_predecessor = current["research_capture_id"] if current else None
        if capture["supersedes_capture_id"] != expected_predecessor:
            raise ConflictError("capture predecessor is not the current contribution head")
        return capture

    def _validate_fact_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        if set(payload) != {
            "payload_variant",
            "payload",
            "actor_ref",
            "event_occurred_at",
        }:
            raise ValidationError("research fact event field set is invalid")
        variant = payload["payload_variant"]
        field_sets = {
            "research_question": {
                "research_question_id",
                "research_capture_id",
                "fact",
                "question_text",
                "derives_from",
                "extraction",
            },
            "research_answer": {
                "research_answer_id",
                "research_capture_id",
                "fact",
                "question_ids",
                "extraction",
            },
            "reference_use": {
                "reference_use_id",
                "research_capture_id",
                "fact",
                "reference_id",
                "reference_kind",
                "locator_observed",
                "source_observation_id",
                "probe_recommendation_ref",
                "use_kind",
                "anchor_quality",
                "extraction",
            },
            "research_problem": {
                "problem_id",
                "research_capture_id",
                "fact",
                "kind",
                "statement",
                "blocks",
                "evidence_refs",
                "extraction",
            },
            "research_claim": {
                "research_claim_id",
                "research_capture_id",
                "fact",
                "statement",
                "answer_ids",
                "extraction",
            },
            "formalization_candidate": {
                "formalization_id",
                "research_capture_id",
                "fact",
                "research_claim_id",
                "notation",
                "latex",
                "legend",
                "reading",
                "logic_family",
                "assumptions",
                "scope",
                "extraction",
            },
        }
        entity = payload["payload"]
        if variant not in field_sets or not isinstance(entity, dict) or set(entity) != field_sets[variant]:
            raise ValidationError("research fact entity field set is invalid")
        id_field = {
            "research_question": "research_question_id",
            "research_answer": "research_answer_id",
            "reference_use": "reference_use_id",
            "research_problem": "problem_id",
            "research_claim": "research_claim_id",
            "formalization_candidate": "formalization_id",
        }[variant]
        envelope = entity["fact"]
        if set(envelope) != {
            "fact_id",
            "subject_id",
            "operation_id",
            "occurred_at",
            "supersedes_fact_id",
        } or envelope["subject_id"] != entity[id_field]:
            raise ValidationError("fact envelope subject binding is invalid")
        if envelope["occurred_at"] != payload["event_occurred_at"]:
            raise ValidationError("fact/event occurrence time mismatch")
        extraction = entity["extraction"]
        if set(extraction) != {
            "mode",
            "actor_ref",
            "method_ref",
            "extracted_at",
            "source_capture_id",
            "source_capture_digest",
            "selector",
        } or extraction["source_capture_id"] != entity["research_capture_id"]:
            raise ValidationError("extraction provenance field set is invalid")
        with self.database.connect() as conn:
            capture_row = conn.execute(
                "SELECT * FROM apt_capture_keys WHERE research_capture_id=?",
                (entity["research_capture_id"],),
            ).fetchone()
            if not capture_row:
                raise ConflictError("owning research capture is missing")
            projection = conn.execute(
                """
                SELECT value_json FROM runtime_projections
                WHERE projection_name='apt.research-record' AND projection_key=?
                """,
                (entity["research_capture_id"],),
            ).fetchone()
            capture = json.loads(projection["value_json"])["capture"]
            artifact = conn.execute(
                "SELECT * FROM artifacts WHERE artifact_id=?",
                (capture["raw_return"]["artifact_id"],),
            ).fetchone()
        expected_capture_digest = {
            "algorithm": "sha256",
            "value": capture_row["capture_digest"].removeprefix("sha256:"),
        }
        if (
            extraction["source_capture_digest"] != capture_row["capture_digest"]
            and extraction["source_capture_digest"] != expected_capture_digest
        ):
            raise ValidationError("extraction capture digest mismatch")
        selector = extraction["selector"]
        if set(selector) != {
            "schema_ref",
            "unit",
            "start_inclusive",
            "end_exclusive",
            "selected_text_digest",
        } or selector["schema_ref"] != "apt.raw-selector@1" or selector["unit"] != "utf8-byte":
            raise ValidationError("raw selector field set is invalid")
        start, end = selector["start_inclusive"], selector["end_exclusive"]
        body = bytes(artifact["body"])
        if not (0 <= start < end <= len(body)):
            raise ValidationError("raw selector bounds are invalid")
        selected = body[start:end]
        selected.decode("utf-8")
        expected_digest = {
            "algorithm": "sha256",
            "value": __import__("hashlib").sha256(selected).hexdigest(),
        }
        if selector["selected_text_digest"] != expected_digest:
            raise ValidationError("selected text digest mismatch")
        # Semantic edges are capture-local.  The APT port therefore refuses
        # dangling or cross-capture links instead of leaving them to a later
        # projection repair.
        referenced_subjects: list[str] = []
        referenced_facts: list[str] = []
        if variant == "research_answer":
            referenced_subjects.extend(entity["question_ids"])
        elif variant == "research_claim":
            referenced_subjects.extend(entity["answer_ids"])
        elif variant == "formalization_candidate":
            referenced_subjects.append(entity["research_claim_id"])
        elif variant == "research_problem":
            referenced_subjects.extend(entity["blocks"])
            for evidence in entity["evidence_refs"]:
                if set(evidence) != {"kind", "fact_id"} or evidence["kind"] != "fact":
                    raise ValidationError("problem evidence reference is invalid")
                referenced_facts.append(evidence["fact_id"])
        with self.database.connect() as conn:
            for subject_id in referenced_subjects:
                edge = conn.execute(
                    """
                    SELECT 1 FROM apt_semantic_facts
                    WHERE research_capture_id=? AND subject_id=? AND is_current=1
                    """,
                    (entity["research_capture_id"], subject_id),
                ).fetchone()
                if not edge:
                    raise ConflictError("semantic edge is dangling or cross-capture")
            for fact_id in referenced_facts:
                edge = conn.execute(
                    """
                    SELECT 1 FROM apt_semantic_facts
                    WHERE research_capture_id=? AND fact_id=?
                    """,
                    (entity["research_capture_id"], fact_id),
                ).fetchone()
                if not edge:
                    raise ConflictError("evidence fact is dangling or cross-capture")
        return entity

    def _append_reference_lineage(
        self,
        *,
        context,
        aggregate_id: str,
        expected_version: int,
        idempotency_key: str,
        request: dict[str, Any],
    ) -> dict[str, Any]:
        if set(request) != {"operation_id", "actor_ref", "lineage_items"}:
            raise ValidationError("lineage request field set is invalid")
        if request["actor_ref"] != context.principal_id or not request["lineage_items"]:
            raise ValidationError("lineage actor/items are invalid")
        request_digest = canonical_digest(request)
        with self.database.connect() as conn:
            prior = conn.execute(
                """SELECT result_receipt_json FROM command_receipts
                   WHERE scope_key=? AND idempotency_key=?""",
                (aggregate_id, idempotency_key),
            ).fetchone()
        if prior:
            prior_result = json.loads(prior["result_receipt_json"])
            if prior_result.get("request_digest") != request_digest:
                raise IdempotencyConflict(
                    "lineage idempotency key reused with different request"
                )
            return prior_result
        prepared: list[dict[str, Any]] = []
        seen: set[tuple[int, str]] = set()
        delivery_refs: dict[str, dict[str, Any]] = {}
        for item in request["lineage_items"]:
            if item.get("kind") == "delivery_origin":
                if set(item) != {
                    "kind",
                    "delivery_subject_key",
                    "probe_recommendation_ref",
                    "expected_head_event_id",
                }:
                    raise ValidationError("delivery lineage item field set is invalid")
                ref = item["probe_recommendation_ref"]
                identity = {
                    "probe_id": ref["probe_id"],
                    "bundle_digest": ref["bundle_digest"],
                    "recommendation_id": ref["recommendation_id"],
                }
                if item["delivery_subject_key"] != canonical_digest(identity):
                    raise ValidationError("delivery subject key is not canonical identity")
                self._verify_probe_recommendation(ref)
                key = (0, item["delivery_subject_key"])
                delivery_refs[item["delivery_subject_key"]] = ref
                event_payload = {
                    "delivery_subject_key": item["delivery_subject_key"],
                    "probe_recommendation_ref": ref,
                    "expected_head_event_id": item["expected_head_event_id"],
                    "actor_ref": context.principal_id,
                    "event_occurred_at": self.now().isoformat(),
                }
                semantic = canonical_digest(
                    {
                        "delivery_subject_key": item["delivery_subject_key"],
                        "probe_recommendation_ref": ref,
                        "expected_head_event_id": item["expected_head_event_id"],
                    }
                )
                with self.database.connect() as conn:
                    existing = conn.execute(
                        "SELECT * FROM apt_delivery_keys WHERE delivery_subject_key=?",
                        (item["delivery_subject_key"],),
                    ).fetchone()
                if existing:
                    if item["expected_head_event_id"] != existing["accepted_event_id"]:
                        raise ConflictError("delivery head CAS is stale or arbitrary")
                    status = "submitted_new"
                    accepted_event_id = None
                else:
                    if item["expected_head_event_id"] is not None:
                        raise ConflictError("first delivery head must be null")
                    status = "submitted_new"
                    accepted_event_id = None
                prepared.append(
                    {
                        "rank": 0,
                        "key": item["delivery_subject_key"],
                        "status": status,
                        "accepted_event_id": accepted_event_id,
                        "event_type": "apt.reference_probe_lineage_appended",
                        "event_payload": event_payload,
                        "semantic_digest": semantic,
                        "entity": None,
                    }
                )
            elif item.get("kind") == "research_reference_use":
                if set(item) != {"kind", "payload"}:
                    raise ValidationError("reference-use lineage item field set is invalid")
                fact_payload = {
                    "payload_variant": "reference_use",
                    "payload": item["payload"],
                    "actor_ref": context.principal_id,
                    "event_occurred_at": item["payload"]["fact"]["occurred_at"],
                }
                entity = self._validate_fact_payload(fact_payload)
                ref = entity["probe_recommendation_ref"]
                self._verify_probe_recommendation(ref)
                subject = canonical_digest(
                    {
                        "probe_id": ref["probe_id"],
                        "bundle_digest": ref["bundle_digest"],
                        "recommendation_id": ref["recommendation_id"],
                    }
                )
                with self.database.connect() as conn:
                    delivery_exists = conn.execute(
                        "SELECT 1 FROM apt_delivery_keys WHERE delivery_subject_key=?",
                        (subject,),
                    ).fetchone()
                    existing = conn.execute(
                        "SELECT * FROM apt_semantic_facts WHERE fact_id=?",
                        (entity["fact"]["fact_id"],),
                    ).fetchone()
                if not delivery_exists and subject not in delivery_refs:
                    raise ConflictError("reference use lacks preceding/current delivery")
                semantic = canonical_digest(entity)
                if existing:
                    exact = (
                        existing["canonical_payload_digest"] == semantic
                        and existing["subject_id"] == entity["fact"]["subject_id"]
                        and existing["supersedes_fact_id"]
                        == entity["fact"]["supersedes_fact_id"]
                    )
                    if not exact:
                        raise ConflictError("reference-use fact identity conflict")
                    status = "existing_exact"
                    accepted_event_id = existing["accepted_event_id"]
                else:
                    status = "submitted_new"
                    accepted_event_id = None
                key = (1, entity["reference_use_id"])
                prepared.append(
                    {
                        "rank": 1,
                        "key": entity["reference_use_id"],
                        "status": status,
                        "accepted_event_id": accepted_event_id,
                        "event_type": "apt.research_fact_appended",
                        "event_payload": fact_payload,
                        "semantic_digest": semantic,
                        "entity": entity,
                    }
                )
            else:
                raise ValidationError("unknown lineage item kind")
            if key in seen:
                raise ValidationError("duplicate lineage member key")
            seen.add(key)
        prepared.sort(key=lambda member: (member["rank"], member["key"]))
        new_items = [member for member in prepared if member["status"] == "submitted_new"]
        if not new_items:
            existing_result = {
                "status": "existing_exact",
                "submitted": False,
                "results": [
                    {
                        "kind_rank": member["rank"],
                        "stable_subject_key": member["key"],
                        "status": "existing_exact",
                        "accepted_event_id": member["accepted_event_id"],
                    }
                    for member in prepared
                ],
            }
            try:
                state = self.projections.catch_up_apt(self.journal)
                existing_result["projection_status"] = (
                    "current" if state["current"] else "pending"
                )
            except Exception:
                existing_result["projection_status"] = "pending"
            return existing_result
        events = [
            self._event(
                member["event_type"],
                member["event_payload"],
                classification="sensitive-output",
            )
            for member in new_items
        ]
        command = self._command(
            command_name="apt.append-reference-probe-lineage@1",
            scope_key=aggregate_id,
            idempotency_key=idempotency_key,
            aggregate_type="apt.probe-lineage",
            aggregate_id=aggregate_id,
            expected_version=expected_version,
            authority={
                "capability_id": context.capability_id,
                "principal_id": context.principal_id,
                "action": "apt.append",
            },
            intent={
                "operation_id": request["operation_id"],
                "canonical_items": [
                    {
                        "rank": member["rank"],
                        "key": member["key"],
                        "semantic_digest": member["semantic_digest"],
                    }
                    for member in prepared
                ],
            },
        )

        def result(records, base):
            accepted = iter(records)
            results = []
            for member in prepared:
                if member["status"] == "submitted_new":
                    record = next(accepted)
                    event_id = record.event_id
                    status = "accepted_new"
                else:
                    event_id = member["accepted_event_id"]
                    status = "existing_exact"
                results.append(
                    {
                        "kind_rank": member["rank"],
                        "stable_subject_key": member["key"],
                        "status": status,
                        "accepted_event_id": event_id,
                    }
                )
            return {
                **base,
                "request_digest": request_digest,
                "semantic_results": results,
            }

        def mutate(conn, records, result_receipt):
            record_iter = iter(records)
            for member in prepared:
                if member["status"] == "submitted_new":
                    record = next(record_iter)
                    event_id = record.event_id
                    if member["rank"] == 0:
                        expected_head = member["event_payload"][
                            "expected_head_event_id"
                        ]
                        current = conn.execute(
                            """SELECT accepted_event_id FROM apt_delivery_keys
                               WHERE delivery_subject_key=?""",
                            (member["key"],),
                        ).fetchone()
                        if current:
                            if expected_head != current["accepted_event_id"]:
                                raise ConflictError("delivery head CAS lost")
                            updated = conn.execute(
                                """UPDATE apt_delivery_keys
                                   SET canonical_payload_digest=?,
                                       expected_head_event_id=?,accepted_event_id=?
                                   WHERE delivery_subject_key=? AND accepted_event_id=?""",
                                (
                                    member["semantic_digest"],
                                    expected_head,
                                    event_id,
                                    member["key"],
                                    expected_head,
                                ),
                            )
                            if updated.rowcount != 1:
                                raise ConflictError("delivery head CAS lost")
                        else:
                            if expected_head is not None:
                                raise ConflictError("first delivery head must be null")
                            conn.execute(
                                """INSERT INTO apt_delivery_keys(
                                     delivery_subject_key,canonical_payload_digest,
                                     expected_head_event_id,accepted_event_id
                                   ) VALUES(?,?,NULL,?)""",
                                (member["key"], member["semantic_digest"], event_id),
                            )
                    else:
                        entity = member["entity"]
                        envelope = entity["fact"]
                        conn.execute(
                            """
                            INSERT INTO apt_semantic_facts(
                              fact_id,research_capture_id,subject_id,fact_kind,supersedes_fact_id,
                              canonical_payload_digest,accepted_event_id,is_current
                            ) VALUES(?,?,?,?,?,?,?,1)
                            """,
                            (
                                envelope["fact_id"],
                                entity["research_capture_id"],
                                envelope["subject_id"],
                                "reference_use",
                                envelope["supersedes_fact_id"],
                                member["semantic_digest"],
                                event_id,
                            ),
                        )
                else:
                    event_id = member["accepted_event_id"]
                result_item = next(
                    item
                    for item in result_receipt["semantic_results"]
                    if item["stable_subject_key"] == member["key"]
                    and item["kind_rank"] == member["rank"]
                )
                conn.execute(
                    """
                    INSERT INTO apt_semantic_request_results(
                      request_key,item_key,request_digest,result_status,result_json,
                      accepted_event_id
                    ) VALUES(?,?,?,?,?,?)
                    """,
                    (
                        f"{aggregate_id}:{idempotency_key}",
                        f"{member['rank']}:{member['key']}",
                        command.digest,
                        result_item["status"],
                        canonical_text(result_item),
                        event_id,
                    ),
                )
        receipt = self.journal.accept(
            command,
            events,
            next_state={
                "accepted_subjects": [member["key"] for member in new_items]
            },
            result_builder=result,
            mutate=mutate,
        )
        result_receipt = dict(receipt)
        try:
            state = self.projections.catch_up_apt(self.journal)
            result_receipt["projection_status"] = (
                "current"
                if state["current"]
                and int(state["apt_source_through_offset"])
                >= int(receipt["last_offset"])
                else "pending"
            )
        except Exception:
            result_receipt["projection_status"] = "pending"
        return result_receipt

    def _verify_probe_recommendation(self, ref: dict[str, Any]) -> None:
        required = {
            "probe_id",
            "recommendation_id",
            "bundle_digest",
            "profile_binding",
            "bundle_acceptance_ref",
            "profile_registration_ref",
            "source_observation_ids",
        }
        if set(ref) != required:
            raise ValidationError("probe recommendation field set is invalid")
        profile = ref["profile_binding"]
        if set(profile) != {
            "protocol_profile_id",
            "protocol_profile_version",
            "protocol_profile_digest",
        }:
            raise ValidationError("probe profile binding field set is invalid")
        with self.database.connect() as conn:
            registered = conn.execute(
                """
                SELECT * FROM protocol_profiles
                WHERE profile_id=? AND profile_version=?
                """,
                (
                    profile["protocol_profile_id"],
                    profile["protocol_profile_version"],
                ),
            ).fetchone()
            acceptance = ref["bundle_acceptance_ref"]
            if (
                set(acceptance)
                != {
                    "kind",
                    "accepted_event_id",
                    "contract_version",
                    "evidence_digest",
                }
                or acceptance.get("kind") != "accepted_event"
            ):
                raise ValidationError("local slice requires accepted-event bundle evidence")
            message = conn.execute(
                """
                SELECT m.*,a.body,e.schema_ref,e.payload_hash AS acceptance_evidence_digest,
                       e.command_id,e.event_ordinal,e.event_count,
                       cr.first_offset,cr.last_offset,cr.event_count AS receipt_event_count,
                       cr.result_receipt_json AS official_result_receipt_json,
                       pc.publication_event_id,pe.journal_offset AS publication_offset,
                       pcr.first_offset AS publication_first_offset,
                       pcr.last_offset AS publication_last_offset,
                       pr.message_id AS receipt_message_id,
                       pr.payload_hash AS receipt_payload_hash,
                       pr.receipt_bytes AS publication_receipt_bytes,
                       pr.receipt_digest AS publication_receipt_digest,
                       pr.journal_offset AS receipt_journal_offset
                FROM messages m
                JOIN artifacts a ON a.artifact_id=m.payload_ref
                JOIN events e ON e.event_id=m.official_event_id
                JOIN command_receipts cr ON cr.command_id=e.command_id
                JOIN publication_candidates pc ON pc.candidate_id=m.source_candidate_id
                JOIN events pe ON pe.event_id=pc.publication_event_id
                JOIN command_receipts pcr ON pcr.command_id=pe.command_id
                JOIN publication_receipts pr ON pr.event_id=pc.publication_event_id
                WHERE m.official_event_id=?
                """,
                (acceptance["accepted_event_id"],),
            ).fetchone()
            registration_event = (
                conn.execute(
                    """
                    SELECT e.schema_ref,e.payload_hash,e.journal_offset,
                           cr.first_offset,cr.last_offset
                    FROM events e
                    JOIN command_receipts cr ON cr.command_id=e.command_id
                    WHERE e.event_id=?
                    """,
                    (registered["registration_event_id"],),
                ).fetchone()
                if registered
                else None
            )
        if (
            not registered
            or registered["canonical_digest"]
            != self._content_digest_string(profile["protocol_profile_digest"])
            or not message
            or message["accepted_offset"] < message["first_offset"]
            or message["accepted_offset"] > message["last_offset"]
            or message["event_count"] != message["receipt_event_count"]
            or message["event_ordinal"] >= message["event_count"]
            or not (
                message["publication_first_offset"]
                <= message["publication_offset"]
                <= message["publication_last_offset"]
                < message["accepted_offset"]
            )
            or message["receipt_message_id"] != message["message_id"]
            or message["receipt_payload_hash"] != message["payload_hash"]
            or message["receipt_journal_offset"] != message["publication_offset"]
            or canonical_digest(
                parse_strict_json(bytes(message["publication_receipt_bytes"]))
            )
            != message["publication_receipt_digest"]
            or acceptance["contract_version"] != message["schema_ref"]
            or self._content_digest_string(acceptance["evidence_digest"])
            != message["acceptance_evidence_digest"]
        ):
            raise ConflictError("profile or official bundle acceptance is invalid")
        publication_receipt = parse_strict_json(
            bytes(message["publication_receipt_bytes"])
        )
        official_receipt = parse_strict_json(
            message["official_result_receipt_json"]
        )
        official_message = official_receipt.get("official_message", {})
        if (
            publication_receipt.get("event_id") != message["publication_event_id"]
            or publication_receipt.get("message_id") != message["message_id"]
            or publication_receipt.get("payload_hash") != message["payload_hash"]
            or publication_receipt.get("journal_offset")
            != message["publication_offset"]
            or publication_receipt.get("status") != "persisted_candidate"
            or official_message.get("accepted_event_id")
            != acceptance["accepted_event_id"]
            or official_message.get("message_id") != message["message_id"]
            or official_message.get("payload_ref") != message["payload_ref"]
            or official_message.get("payload_hash") != message["payload_hash"]
            or official_message.get("accepted_offset") != message["accepted_offset"]
        ):
            raise ConflictError("official verification receipt identity mismatch")
        registry_ref = ref["profile_registration_ref"]
        if (
            set(registry_ref)
            != {
                "kind",
                "accepted_event_id",
                "protocol_profile_id",
                "protocol_profile_version",
                "protocol_profile_digest",
                "contract_version",
                "evidence_digest",
            }
            or registry_ref["kind"] != "registry_event"
            or registry_ref["accepted_event_id"] != registered["registration_event_id"]
            or registry_ref["protocol_profile_id"] != registered["profile_id"]
            or registry_ref["protocol_profile_version"] != registered["profile_version"]
            or self._content_digest_string(
                registry_ref["protocol_profile_digest"]
            )
            != registered["canonical_digest"]
            or not registration_event
            or registry_ref["contract_version"] != registration_event["schema_ref"]
            or self._content_digest_string(registry_ref["evidence_digest"])
            != registration_event["payload_hash"]
            or not (
                registration_event["first_offset"]
                <= registration_event["journal_offset"]
                <= registration_event["last_offset"]
            )
        ):
            raise ConflictError("profile registration evidence mismatch")
        prefix = self.journal.read_complete_groups(through=message["accepted_offset"])
        if prefix["effective_as_of"] != message["accepted_offset"]:
            raise ConflictError("official recommendation is outside verified prefix")
        if ref["source_observation_ids"] != sorted(set(ref["source_observation_ids"])):
            raise ValidationError("source observation IDs are not canonical unique")
        published = parse_strict_json(bytes(message["body"]))
        for field in ("probe_id", "recommendation_id", "bundle_digest"):
            if published.get(field) != ref[field]:
                raise ConflictError("official recommendation identity mismatch")

    @staticmethod
    def _require_authority_evidence(
        *,
        actor_ref: Any,
        references: tuple[Any, ...],
        digests: tuple[Any, ...],
    ) -> None:
        if not isinstance(actor_ref, str) or not actor_ref:
            raise AuthorizationError("authenticated actor reference is required")
        if any(not isinstance(value, str) or not value for value in references):
            raise AuthorizationError("authority evidence reference is required")
        if any(
            not (
                isinstance(value, str)
                and value.startswith("sha256:")
                and len(value) == 71
                and all(character in "0123456789abcdef" for character in value[7:])
            )
            for value in digests
        ):
            raise AuthorizationError("authority evidence digest must be qualified sha256")

    @staticmethod
    def _content_digest_string(value: Any) -> str:
        if isinstance(value, str) and value.startswith("sha256:"):
            return value
        if (
            isinstance(value, dict)
            and value.get("algorithm") == "sha256"
            and isinstance(value.get("value"), str)
        ):
            return "sha256:" + value["value"]
        raise ValidationError("invalid ContentDigest")

    def _host_workflow_source(self, relative: str) -> tuple[Path, bytes, str]:
        if (
            not isinstance(relative, str)
            or not relative
            or Path(relative).is_absolute()
            or "\\" in relative
            or ".." in Path(relative).parts
        ):
            raise ValidationError("workflow source path must be repository-relative")
        root = self.settings.repo_root.resolve()
        candidate = root / relative
        try:
            resolved = candidate.resolve(strict=True)
            resolved.relative_to(root)
        except (OSError, ValueError) as exc:
            raise ValidationError(
                "workflow source is unavailable or escapes repository"
            ) from exc
        cursor = candidate
        while cursor != root:
            if cursor.is_symlink():
                raise ValidationError("workflow source symlinks are forbidden")
            cursor = cursor.parent
        if not resolved.is_file():
            raise ValidationError("workflow source must be a regular file")
        body = resolved.read_bytes()
        return resolved, body, digest_bytes(body)

    def _validate_workflow_manifest(
        self,
        *,
        raw: bytes,
        expected_digest: str,
        opened_dispatch_route_digest: str,
        dispatch_id: str,
        group_id: str,
        seat_index: int,
        turn_ordinal: int,
        attempt_id: str,
    ) -> tuple[dict[str, Any], list[PreparedArtifact]]:
        if digest_bytes(raw) != self._content_digest_string(expected_digest):
            raise IntegrityError("workflow manifest digest mismatch")
        manifest = self._require_exact_fields(
            parse_strict_json(raw),
            {"schema", "dispatch_id", "route_digest", "target", "slots"},
            "WorkflowInputManifest",
        )
        if (
            manifest["schema"] != "aci-workflow-input-manifest/v1"
            or manifest["dispatch_id"] != dispatch_id
        ):
            raise IntegrityError("workflow manifest identity mismatch")
        manifest_route_digest = manifest["route_digest"]
        if (
            not isinstance(manifest_route_digest, str)
            or not manifest_route_digest.startswith("sha256:")
            or len(manifest_route_digest) != 71
            or any(
                character not in "0123456789abcdef"
                for character in manifest_route_digest[7:]
            )
            or manifest_route_digest != opened_dispatch_route_digest
        ):
            raise IntegrityError("workflow manifest route digest mismatch")
        target = self._require_exact_fields(
            manifest["target"],
            {"group_id", "seat_index", "turn_ordinal", "attempt_id"},
            "WorkflowInputManifest target",
        )
        if target != {
            "group_id": group_id,
            "seat_index": seat_index,
            "turn_ordinal": turn_ordinal,
            "attempt_id": attempt_id,
        }:
            raise IntegrityError("workflow manifest target mismatch")
        slots = manifest["slots"]
        if not isinstance(slots, list):
            raise IntegrityError("workflow manifest slots must be ordered")
        names: set[str] = set()
        source_artifacts: list[PreparedArtifact] = []
        for slot in slots:
            slot = self._require_exact_fields(
                slot,
                {
                    "name",
                    "data_schema_ref",
                    "cardinality",
                    "max_bytes",
                    "purpose",
                    "sources",
                },
                "WorkflowInputManifest slot",
            )
            name = slot["name"]
            if not isinstance(name, str) or not name or name in names:
                raise IntegrityError("workflow manifest slot names must be unique")
            names.add(name)
            if (
                not isinstance(slot["data_schema_ref"], str)
                or not slot["data_schema_ref"]
                or not isinstance(slot["purpose"], str)
                or not slot["purpose"]
                or not isinstance(slot["max_bytes"], int)
                or slot["max_bytes"] < 0
            ):
                raise IntegrityError("workflow manifest slot contract is invalid")
            cardinality = self._require_exact_fields(
                slot["cardinality"], {"min", "max"}, "slot cardinality"
            )
            if (
                not isinstance(cardinality["min"], int)
                or not isinstance(cardinality["max"], int)
                or cardinality["min"] < 0
                or cardinality["max"] < cardinality["min"]
            ):
                raise IntegrityError("workflow manifest cardinality is invalid")
            sources = slot["sources"]
            if not isinstance(sources, list) or not (
                cardinality["min"] <= len(sources) <= cardinality["max"]
            ):
                raise IntegrityError("workflow manifest source cardinality is invalid")
            total = 0
            for source in sources:
                if not isinstance(source, dict):
                    raise IntegrityError("WorkflowInputManifest source must be an object")
                source_kind = source.get("source_kind")
                if source_kind not in {"repository", "binding-output"}:
                    raise IntegrityError("workflow manifest source kind is invalid")
                if source_kind == "repository":
                    source_classification = "sensitive-input"
                    source = self._require_exact_fields(
                        source,
                        {
                            "source_kind",
                            "producer_binding_id",
                            "path",
                            "sha256",
                            "size_bytes",
                        },
                        "WorkflowInputManifest repository source",
                    )
                    _, body, actual_digest = self._host_workflow_source(source["path"])
                    if (
                        source["sha256"] != actual_digest
                        or source["size_bytes"] != len(body)
                    ):
                        raise IntegrityError("workflow source bytes differ from manifest")
                    if source["producer_binding_id"] is not None:
                        raise IntegrityError(
                            "repository source cannot claim a producer"
                        )
                else:
                    source_classification = "sensitive-output"
                    source = self._require_exact_fields(
                        source,
                        {"source_kind", "producer_output_receipt"},
                        "WorkflowInputManifest binding-output source",
                    )
                    output = self._require_exact_fields(
                        source["producer_output_receipt"],
                        {
                            "schema",
                            "dispatch_id",
                            "producer_binding_id",
                            "producer_agent_id",
                            "artifact_id",
                            "path",
                            "data_schema_ref",
                            "sha256",
                            "size_bytes",
                            "route_digest",
                            "receipt_digest",
                        },
                        "producer-output receipt",
                    )
                    receipt_body = dict(output)
                    receipt_digest = receipt_body.pop("receipt_digest")
                    if (
                        output["schema"]
                        != "aci-host-workflow-producer-output/v1"
                        or output["dispatch_id"] != dispatch_id
                        or output["route_digest"] != opened_dispatch_route_digest
                        or output["data_schema_ref"] != slot["data_schema_ref"]
                        or any(
                            not isinstance(output[field], str) or not output[field]
                            for field in (
                                "producer_binding_id",
                                "producer_agent_id",
                                "artifact_id",
                                "path",
                                "data_schema_ref",
                                "sha256",
                                "receipt_digest",
                            )
                        )
                        or isinstance(output["size_bytes"], bool)
                        or not isinstance(output["size_bytes"], int)
                        or output["size_bytes"] < 0
                        or canonical_digest(receipt_body) != receipt_digest
                    ):
                        raise IntegrityError("producer-output receipt is invalid")
                    producer_id = output["producer_binding_id"]
                    with self.database.connect() as conn:
                        producer = conn.execute(
                            """
                            SELECT b.dispatch_id,b.state,b.agent_id,
                                   r.result_receipt_json
                            FROM host_workflow_turn_bindings b
                            LEFT JOIN command_receipts r
                              ON r.scope_key='aci.host-workflow-turn:'||b.binding_id
                             AND r.idempotency_key='terminal'
                            WHERE b.binding_id=?
                            """,
                            (producer_id,),
                        ).fetchone()
                    if (
                        not producer
                        or producer["dispatch_id"] != dispatch_id
                        or producer["state"] != "resolved"
                        or producer["agent_id"] != output["producer_agent_id"]
                        or producer["result_receipt_json"] is None
                    ):
                        raise ConflictError(
                            "workflow source producer is absent or lacks a resolved identity"
                        )
                    terminal_result = parse_strict_json(
                        producer["result_receipt_json"].encode("utf-8")
                    )
                    if (
                        not isinstance(terminal_result, dict)
                        or terminal_result.get("binding_id") != producer_id
                        or terminal_result.get("dispatch_id") != dispatch_id
                        or terminal_result.get("state") != "resolved"
                        or terminal_result.get("agent_id")
                        != output["producer_agent_id"]
                        or terminal_result.get("producer_output_receipt") != output
                    ):
                        raise IntegrityError(
                            "workflow source differs from registered producer output"
                        )
                    _, body, actual_digest = self._host_workflow_source(output["path"])
                    if (
                        output["sha256"] != actual_digest
                        or output["size_bytes"] != len(body)
                        or output["artifact_id"]
                        != "art_" + actual_digest.removeprefix("sha256:")[:32]
                    ):
                        raise IntegrityError(
                            "producer-output bytes differ from immutable receipt"
                        )
                total += len(body)
                source_artifacts.append(
                    self.artifacts.prepare(
                        body,
                        media_type="application/octet-stream",
                        schema_ref=slot["data_schema_ref"],
                        classification=source_classification,
                    )
                )
            if total > slot["max_bytes"]:
                raise IntegrityError("workflow manifest slot exceeds byte ceiling")
        return manifest, source_artifacts

    def bind_host_workflow_turn(
        self,
        *,
        host: str,
        host_session_id: str,
        tool_use_id: str,
        tool_input: dict[str, Any],
        dispatch_id: str,
        group_id: str,
        seat_index: int,
        turn_ordinal: int,
        attempt_id: str,
        prompt_body: str,
        prompt_template_path: str | None,
        prompt_template_digest: str,
        workflow_manifest_path: str,
        workflow_manifest_digest: str,
        actor_ref: str,
    ) -> dict[str, Any]:
        if host not in {"claude", "codex"}:
            raise ValidationError("host workflow host is invalid")
        if not all(
            isinstance(value, str) and value
            for value in (
                host_session_id,
                tool_use_id,
                dispatch_id,
                group_id,
                attempt_id,
                prompt_body,
                workflow_manifest_path,
                actor_ref,
            )
        ):
            raise ValidationError("host workflow binding identity is incomplete")
        if (
            not isinstance(seat_index, int)
            or seat_index < 0
            or not isinstance(turn_ordinal, int)
            or turn_ordinal < 0
        ):
            raise ValidationError("host workflow seat/turn is invalid")
        operation_kind = "spawn" if turn_ordinal == 0 else "followup"
        snapshot = self.legacy.resolve(self.settings.ledger_path, dispatch_id)
        orchestration_head = self.journal.head(
            f"aci.orchestration-dispatch:{dispatch_id}"
        )
        if orchestration_head["current_version"] != 1:
            raise ConflictError("parent Dispatch is not open")
        with self.database.connect() as conn:
            link = conn.execute(
                "SELECT * FROM dispatch_links WHERE dispatch_id=?",
                (dispatch_id,),
            ).fetchone()
        if not link or link["row_digest"] != snapshot.row_digest:
            raise IntegrityError("parent Dispatch link is absent or stale")
        row = parse_strict_json(link["row_json"])
        capability_route = row.get("capability_route")
        if not isinstance(capability_route, dict):
            raise IntegrityError("parent Dispatch capability route is unavailable")
        opened_dispatch_route_digest = capability_route.get("route_digest")
        capability_route_body = dict(capability_route)
        capability_route_body.pop("route_digest", None)
        if (
            not isinstance(opened_dispatch_route_digest, str)
            or not opened_dispatch_route_digest.startswith("sha256:")
            or len(opened_dispatch_route_digest) != 71
            or any(
                character not in "0123456789abcdef"
                for character in opened_dispatch_route_digest[7:]
            )
            or canonical_digest(capability_route_body)
            != opened_dispatch_route_digest
        ):
            raise IntegrityError("parent Dispatch capability route is invalid")
        groups = row.get("groups")
        group = (
            next(
                (
                    candidate
                    for candidate in groups
                    if isinstance(candidate, dict)
                    and candidate.get("group_id") == group_id
                ),
                None,
            )
            if isinstance(groups, list)
            else None
        )
        agents = group.get("agents") if isinstance(group, dict) else None
        if (
            not isinstance(agents, list)
            or seat_index >= len(agents)
            or not isinstance(agents[seat_index], dict)
        ):
            raise NotFoundError("parent Dispatch group/seat is not declared")
        confirmed_prompt = agents[seat_index].get("initial_prompt")
        if not isinstance(confirmed_prompt, str) or not confirmed_prompt:
            raise IntegrityError("parent Dispatch seat prompt is unavailable")
        expected_template_digest = self._content_digest_string(
            prompt_template_digest
        )
        if turn_ordinal == 0:
            if prompt_template_path is not None or prompt_body != confirmed_prompt:
                raise IntegrityError("spawn prompt differs from confirmed seat prompt")
            if digest_bytes(prompt_body.encode("utf-8")) != expected_template_digest:
                raise IntegrityError("spawn prompt template digest mismatch")
        else:
            if not isinstance(prompt_template_path, str):
                raise IntegrityError("followup requires a declared prompt template")
            _, template_bytes, template_digest = self._host_workflow_source(
                prompt_template_path
            )
            try:
                template_text = template_bytes.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise IntegrityError(
                    "followup prompt template must be UTF-8"
                ) from exc
            if (
                template_digest != expected_template_digest
                or template_text != prompt_body
                or expected_template_digest not in confirmed_prompt
            ):
                raise IntegrityError(
                    "followup prompt is not bound by the confirmed seat prompt"
                )
            with self.database.connect() as conn:
                prior_turn = conn.execute(
                    """
                    SELECT state,agent_id FROM host_workflow_turn_bindings
                    WHERE dispatch_id=? AND group_id=? AND seat_index=?
                      AND turn_ordinal=?
                    """,
                    (dispatch_id, group_id, seat_index, turn_ordinal - 1),
                ).fetchone()
            if (
                not prior_turn
                or prior_turn["state"]
                not in {"resolved", "error", "cancelled"}
            ):
                raise ConflictError("previous seat turn is not terminal")
            target = tool_input.get("target")
            if (
                prior_turn["agent_id"] is not None
                and target != prior_turn["agent_id"]
            ):
                raise AuthorizationError(
                    "followup target differs from bound agent"
                )
        _, manifest_bytes, actual_manifest_digest = self._host_workflow_source(
            workflow_manifest_path
        )
        if actual_manifest_digest != workflow_manifest_digest:
            raise IntegrityError("workflow manifest file digest mismatch")
        _, source_artifacts = self._validate_workflow_manifest(
            raw=manifest_bytes,
            expected_digest=workflow_manifest_digest,
            opened_dispatch_route_digest=opened_dispatch_route_digest,
            dispatch_id=dispatch_id,
            group_id=group_id,
            seat_index=seat_index,
            turn_ordinal=turn_ordinal,
            attempt_id=attempt_id,
        )
        source_artifact_ids = [
            artifact.artifact_id for artifact in source_artifacts
        ]
        prepared_manifest = self.artifacts.prepare(
            manifest_bytes,
            media_type="application/json",
            schema_ref="aci.workflow-input-manifest@1",
            classification="sensitive-input",
        )
        tool_input_digest = canonical_digest(tool_input)
        binding_id = self._stable_id(
            "hwb_",
            [
                dispatch_id,
                group_id,
                str(seat_index),
                str(turn_ordinal),
                attempt_id,
            ],
        )
        aggregate_id = f"aci.host-workflow-turn:{binding_id}"
        with self.database.connect() as conn:
            existing = conn.execute(
                """
                SELECT b.*,r.result_receipt_json
                FROM host_workflow_turn_bindings b
                LEFT JOIN command_receipts r
                  ON r.scope_key=? AND r.idempotency_key='bind'
                WHERE b.binding_id=?
                """,
                (aggregate_id, binding_id),
            ).fetchone()
        if existing:
            accepted = {
                "dispatch_id": dispatch_id,
                "session_id": link["session_id"],
                "parent_row_digest": snapshot.row_digest,
                "group_id": group_id,
                "seat_index": seat_index,
                "turn_ordinal": turn_ordinal,
                "attempt_id": attempt_id,
                "host": host,
                "operation_kind": operation_kind,
                "prompt_template_digest": expected_template_digest,
                "workflow_manifest_artifact_id": prepared_manifest.artifact_id,
                "workflow_manifest_hash": prepared_manifest.content_hash,
                "source_artifact_ids_json": canonical_text(source_artifact_ids),
                "tool_input_digest": tool_input_digest,
                "host_session_id": host_session_id,
                "tool_use_id": tool_use_id,
            }
            if any(existing[key] != value for key, value in accepted.items()):
                raise IdempotencyConflict(
                    "host workflow binding retry differs from accepted launch"
                )
            if not existing["result_receipt_json"]:
                raise IntegrityError(
                    "host workflow binding exists without command receipt"
                )
            return json.loads(existing["result_receipt_json"])
        bound_at = self.now().isoformat()
        payload = {
            "binding_id": binding_id,
            "dispatch_id": dispatch_id,
            "session_id": link["session_id"],
            "parent_row_digest": snapshot.row_digest,
            "group_id": group_id,
            "seat_index": seat_index,
            "turn_ordinal": turn_ordinal,
            "attempt_id": attempt_id,
            "host": host,
            "operation_kind": operation_kind,
            "prompt_template_digest": expected_template_digest,
            "workflow_manifest_artifact_id": prepared_manifest.artifact_id,
            "workflow_manifest_hash": prepared_manifest.content_hash,
            "source_artifact_ids": source_artifact_ids,
            "tool_input_digest": tool_input_digest,
            "host_session_id": host_session_id,
            "tool_use_id": tool_use_id,
            "bound_at": bound_at,
            "actor_ref": actor_ref,
        }
        command = self._command(
            command_name="aci.bind-host-workflow-turn@1",
            scope_key=aggregate_id,
            idempotency_key="bind",
            aggregate_type="aci.host-workflow-turn",
            aggregate_id=aggregate_id,
            expected_version=0,
            authority={
                "principal_id": actor_ref,
                "action": "host_workflow.bind",
                "phase": "bootstrap",
            },
            intent=payload,
            prerequisites=(
                PrerequisiteHead(
                    aggregate_id=orchestration_head["aggregate_id"],
                    expected_version=orchestration_head["current_version"],
                    state_hash=orchestration_head["state_hash"],
                ),
            ),
        )
        event = self._event("host_workflow.turn_bound@1", payload)

        def mutate(conn, records, _result):
            conn.execute(
                """
                INSERT INTO host_workflow_turn_bindings(
                  binding_id,dispatch_id,session_id,parent_row_digest,group_id,
                  seat_index,turn_ordinal,attempt_id,host,operation_kind,
                  prompt_template_digest,workflow_manifest_artifact_id,
                  workflow_manifest_hash,source_artifact_ids_json,tool_input_digest,
                  host_session_id,tool_use_id,state,bound_event_id,bound_at
                ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,'running',?,?)
                """,
                (
                    binding_id,
                    dispatch_id,
                    link["session_id"],
                    snapshot.row_digest,
                    group_id,
                    seat_index,
                    turn_ordinal,
                    attempt_id,
                    host,
                    operation_kind,
                    expected_template_digest,
                    prepared_manifest.artifact_id,
                    prepared_manifest.content_hash,
                    canonical_text(source_artifact_ids),
                    tool_input_digest,
                    host_session_id,
                    tool_use_id,
                    records[0].event_id,
                    bound_at,
                ),
            )

        def result(records, base):
            return {
                **base,
                "status": "launch-authorized",
                "binding_id": binding_id,
                "dispatch_id": dispatch_id,
                "session_id": link["session_id"],
                "group_id": group_id,
                "seat_index": seat_index,
                "turn_ordinal": turn_ordinal,
                "attempt_id": attempt_id,
                "workflow_manifest_artifact_id": prepared_manifest.artifact_id,
                "bound_event_id": records[0].event_id,
            }

        return self.journal.accept(
            command,
            [event],
            next_state={**payload, "state": "running"},
            additional_artifacts=(prepared_manifest, *source_artifacts),
            result_builder=result,
            mutate=mutate,
        )

    def complete_host_workflow_turn(
        self,
        *,
        binding_id: str,
        state: str,
        agent_id: str | None,
        actor_ref: str,
        producer_output: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        if state not in {"resolved", "error", "cancelled"}:
            raise ValidationError("host workflow terminal state is invalid")
        aggregate_id = f"aci.host-workflow-turn:{binding_id}"
        with self.database.connect() as conn:
            binding = conn.execute(
                "SELECT * FROM host_workflow_turn_bindings WHERE binding_id=?",
                (binding_id,),
            ).fetchone()
            prior = conn.execute(
                """
                SELECT result_receipt_json FROM command_receipts
                WHERE scope_key=? AND idempotency_key='terminal'
                """,
                (aggregate_id,),
            ).fetchone()
        if not binding:
            raise NotFoundError("host workflow binding not found")
        prepared_output: PreparedArtifact | None = None
        producer_output_receipt: dict[str, Any] | None = None
        if producer_output is not None:
            output = self._require_exact_fields(
                producer_output,
                {"path", "data_schema_ref"},
                "host workflow producer output",
            )
            if (
                state != "resolved"
                or not isinstance(agent_id, str)
                or not agent_id
                or not isinstance(output["data_schema_ref"], str)
                or not output["data_schema_ref"]
            ):
                raise ValidationError(
                    "producer output requires a resolved turn, agent, and data schema"
                )
            resolved_output, output_body, output_digest = self._host_workflow_source(
                output["path"]
            )
            canonical_path = resolved_output.relative_to(
                self.settings.repo_root.resolve()
            ).as_posix()
            if output["path"] != canonical_path:
                raise ValidationError("producer output path must be canonical")
            with self.database.connect() as conn:
                link = conn.execute(
                    "SELECT row_digest,row_json FROM dispatch_links WHERE dispatch_id=?",
                    (binding["dispatch_id"],),
                ).fetchone()
            if not link or link["row_digest"] != binding["parent_row_digest"]:
                raise IntegrityError("producer output parent Dispatch is absent or stale")
            dispatch_row = parse_strict_json(link["row_json"])
            capability_route = dispatch_row.get("capability_route")
            if not isinstance(capability_route, dict):
                raise IntegrityError("producer output capability route is unavailable")
            route_digest = capability_route.get("route_digest")
            route_body = dict(capability_route)
            route_body.pop("route_digest", None)
            if (
                not isinstance(route_digest, str)
                or canonical_digest(route_body) != route_digest
            ):
                raise IntegrityError("producer output capability route is invalid")
            prepared_output = self.artifacts.prepare(
                output_body,
                media_type="application/octet-stream",
                schema_ref=output["data_schema_ref"],
                classification="sensitive-output",
            )
            receipt_body = {
                "schema": "aci-host-workflow-producer-output/v1",
                "dispatch_id": binding["dispatch_id"],
                "producer_binding_id": binding_id,
                "producer_agent_id": agent_id,
                "artifact_id": prepared_output.artifact_id,
                "path": canonical_path,
                "data_schema_ref": output["data_schema_ref"],
                "sha256": output_digest,
                "size_bytes": len(output_body),
                "route_digest": route_digest,
            }
            producer_output_receipt = {
                **receipt_body,
                "receipt_digest": canonical_digest(receipt_body),
            }
        if prior:
            result = json.loads(prior["result_receipt_json"])
            if (
                result.get("state") != state
                or result.get("agent_id") != agent_id
                or result.get("producer_output_receipt")
                != producer_output_receipt
            ):
                raise IdempotencyConflict(
                    "host workflow terminal retry differs from accepted result"
                )
            return result
        terminal_at = self.now().isoformat()
        payload = {
            "binding_id": binding_id,
            "dispatch_id": binding["dispatch_id"],
            "group_id": binding["group_id"],
            "seat_index": binding["seat_index"],
            "turn_ordinal": binding["turn_ordinal"],
            "attempt_id": binding["attempt_id"],
            "host": binding["host"],
            "state": state,
            "agent_id": agent_id,
            "terminal_at": terminal_at,
            "actor_ref": actor_ref,
        }
        command = self._command(
            command_name="aci.complete-host-workflow-turn@1",
            scope_key=aggregate_id,
            idempotency_key="terminal",
            aggregate_type="aci.host-workflow-turn",
            aggregate_id=aggregate_id,
            expected_version=1,
            authority={
                "principal_id": actor_ref,
                "action": "host_workflow.complete",
                "phase": "finalize",
            },
            intent=payload,
        )
        event = self._event("host_workflow.turn_terminal@1", payload)

        def mutate(conn, records, _result):
            updated = conn.execute(
                """
                UPDATE host_workflow_turn_bindings
                SET state=?,agent_id=COALESCE(?,agent_id),terminal_event_id=?,
                    terminal_at=?
                WHERE binding_id=? AND state='running'
                """,
                (state, agent_id, records[0].event_id, terminal_at, binding_id),
            )
            if updated.rowcount != 1:
                raise ConflictError("host workflow terminal state CAS lost")

        def result(records, base):
            return {
                **base,
                "binding_id": binding_id,
                "dispatch_id": binding["dispatch_id"],
                "state": state,
                "agent_id": agent_id,
                "terminal_event_id": records[0].event_id,
                "producer_output_receipt": producer_output_receipt,
            }

        return self.journal.accept(
            command,
            [event],
            next_state=payload,
            additional_artifacts=((prepared_output,) if prepared_output else ()),
            result_builder=result,
            mutate=mutate,
        )

    def get_host_workflow_binding(self, binding_id: str) -> dict[str, Any]:
        with self.database.connect() as conn:
            row = conn.execute(
                "SELECT * FROM host_workflow_turn_bindings WHERE binding_id=?",
                (binding_id,),
            ).fetchone()
        if not row:
            raise NotFoundError("host workflow binding not found")
        return dict(row)

    def issue_capability(
        self,
        *,
        principal_id: str,
        action: str,
        phase: str,
        context: dict[str, Any],
        expires_at: str | None = None,
    ) -> dict[str, str]:
        return self.capabilities.issue(
            principal_id=principal_id,
            action=action,
            phase=phase,
            context=context,
            expires_at=expires_at,
        )

    # ACI-owned read ports used by the APT application binder. They prevent
    # domain/application code from acquiring database handles or issuing SQL.
    def apt_command_result(
        self, scope_key: str, idempotency_key: str
    ) -> dict[str, Any] | None:
        with self.database.connect() as conn:
            row = conn.execute(
                """SELECT result_receipt_json FROM command_receipts
                   WHERE scope_key=? AND idempotency_key=?""",
                (scope_key, idempotency_key),
            ).fetchone()
        return json.loads(row["result_receipt_json"]) if row else None

    def apt_dispatch_link(
        self, dispatch_id: str, session_id: str | None = None
    ) -> dict[str, Any] | None:
        with self.database.connect() as conn:
            row = conn.execute(
                """SELECT * FROM dispatch_links WHERE dispatch_id=?
                   AND (? IS NULL OR session_id=?)""",
                (dispatch_id, session_id, session_id),
            ).fetchone()
        return dict(row) if row else None

    def apt_capture_projection_payload(self, capture_id: str) -> dict[str, Any] | None:
        with self.database.connect() as conn:
            row = conn.execute(
                """SELECT payload_json FROM apt_research_captures_projection
                   WHERE research_capture_id=?""",
                (capture_id,),
            ).fetchone()
        return parse_strict_json(row["payload_json"]) if row else None

    def apt_semantic_partition(
        self,
        capture_id: str,
        capture_digest: str,
        facts: list[dict[str, Any]],
    ) -> tuple[dict[str, Any] | None, dict[str, dict[str, Any]]]:
        with self.database.connect() as conn:
            capture = conn.execute(
                "SELECT * FROM apt_capture_keys WHERE research_capture_id=?",
                (capture_id,),
            ).fetchone()
            rows: dict[str, dict[str, Any]] = {}
            for fact in facts:
                row = conn.execute(
                    "SELECT * FROM apt_semantic_facts WHERE fact_id=?",
                    (fact["fact_id"],),
                ).fetchone()
                if row:
                    rows[fact["fact_id"]] = dict(row)
        return (dict(capture) if capture else None, rows)

    def apt_answer_binding(
        self, capture_id: str
    ) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
        with self.database.connect() as conn:
            capture = conn.execute(
                """SELECT c.*,l.session_id FROM apt_research_captures_projection c
                   JOIN dispatch_links l ON l.dispatch_id=c.dispatch_id
                   WHERE c.research_capture_id=?""",
                (capture_id,),
            ).fetchone()
            answer = conn.execute(
                """SELECT * FROM apt_research_answers_projection
                   WHERE research_capture_id=? ORDER BY research_answer_id LIMIT 1""",
                (capture_id,),
            ).fetchone()
        return (
            dict(capture) if capture else None,
            dict(answer) if answer else None,
        )

    def apt_research_mutation(self, plan: dict[str, Any]):
        """Return the ACI-owned transactional port for one bound APT batch."""

        def mutate(conn, committed, result):
            capture_payload = plan["capture_payload"]
            capture = capture_payload["research_capture"]
            raw = capture["raw_return"]
            link = conn.execute(
                "SELECT * FROM dispatch_links WHERE dispatch_id=?",
                (capture["dispatch_id"],),
            ).fetchone()
            artifact = conn.execute(
                "SELECT * FROM artifacts WHERE artifact_id=?",
                (raw["artifact_id"],),
            ).fetchone()
            if (
                not link
                or capture_payload["session_dispatch_link_id"]
                != self._stable_id(
                    "lnk_",
                    [
                        link["session_id"],
                        capture["dispatch_id"],
                        link["row_digest"],
                    ],
                )
                or not artifact
                or artifact["content_hash"]
                != self._content_digest_string(raw["content_digest"])
            ):
                raise ConflictError("APT batch authority/artifact changed in transaction")
            claim_statements: dict[str, str] = {}
            for item in plan["items"]:
                if item["kind"] == "capture":
                    continue
                entity = item["payload"]["payload"]
                selector = entity["extraction"]["selector"]
                start, end = (
                    selector["start_inclusive"],
                    selector["end_exclusive"],
                )
                body = bytes(artifact["body"])
                if not (0 <= start < end <= len(body)):
                    raise ValidationError("APT selector bounds changed")
                selected_bytes = body[start:end]
                if self._content_digest_string(
                    selector["selected_text_digest"]
                ) != digest_bytes(selected_bytes):
                    raise ValidationError("APT selector digest changed")
                frame = parse_strict_json(selected_bytes)
                kind = item["kind"]
                comparisons = {
                    "research_question": frame.get("question_text")
                    == entity.get("question_text"),
                    "research_answer": set(frame)
                    == {"mode", "type", "final_answer"},
                    "reference_use": all(
                        frame.get(key) == entity.get(key)
                        for key in (
                            "reference_kind",
                            "locator_observed",
                            "use_kind",
                        )
                    ),
                    "research_problem": all(
                        frame.get(key) == entity.get(key)
                        for key in ("kind", "statement")
                    ),
                    "research_claim": frame.get("statement")
                    == entity.get("statement"),
                    "formalization_candidate": (
                        frame.get("claim")
                        == claim_statements.get(entity.get("research_claim_id"))
                        and all(
                            frame.get(key) == entity.get(key)
                            for key in (
                                "notation",
                                "latex",
                                "legend",
                                "reading",
                                "logic_family",
                                "assumptions",
                                "scope",
                            )
                        )
                    ),
                }
                if frame.get("type") != {
                    "research_question": "question",
                    "research_answer": "answer",
                    "reference_use": "reference",
                    "research_problem": "problem",
                    "research_claim": "claim",
                    "formalization_candidate": "formalization",
                }.get(kind) or not comparisons.get(kind, False):
                    raise ValidationError("APT selected frame diverges from semantic entity")
                if kind == "research_claim":
                    claim_statements[entity["fact"]["subject_id"]] = entity["statement"]
            committed_iter = iter(committed)
            result_by_key = {
                row["item_key"]: row for row in result["semantic_results"]
            }
            for item in plan["items"]:
                if item["status"] == "submitted_new":
                    record = next(committed_iter)
                    accepted_event_id = record.event_id
                    if item["kind"] == "capture":
                        conn.execute(
                            """INSERT INTO apt_capture_keys(
                                 research_capture_id,dispatch_id,expected_contribution_id,
                                 capture_operation_id,supersedes_capture_id,capture_digest,
                                 accepted_event_id,is_current
                               ) VALUES(?,?,?,?,?,?,?,1)""",
                            (
                                capture["research_capture_id"],
                                capture["dispatch_id"],
                                capture["expected_contribution_id"],
                                capture["capture_operation_id"],
                                capture["supersedes_capture_id"],
                                self._content_digest_string(capture["capture_digest"]),
                                accepted_event_id,
                            ),
                        )
                    else:
                        entity = item["payload"]["payload"]
                        fact = entity["fact"]
                        conn.execute(
                            """INSERT INTO apt_semantic_facts(
                                 fact_id,research_capture_id,subject_id,fact_kind,
                                 supersedes_fact_id,canonical_payload_digest,
                                 accepted_event_id,is_current
                               ) VALUES(?,?,?,?,?,?,?,1)""",
                            (
                                fact["fact_id"],
                                entity["research_capture_id"],
                                fact["subject_id"],
                                item["kind"],
                                fact["supersedes_fact_id"],
                                item["semantic_digest"],
                                accepted_event_id,
                            ),
                        )
                else:
                    accepted_event_id = item["accepted_event_id"]
                mapped = result_by_key[item["item_key"]]
                conn.execute(
                    """INSERT INTO apt_semantic_request_results(
                         request_key,item_key,request_digest,result_status,result_json,
                         accepted_event_id
                       ) VALUES(?,?,?,?,?,?)""",
                    (
                        plan["request_key"],
                        item["item_key"],
                        plan["submission_digest"],
                        mapped["status"],
                        canonical_text(mapped),
                        accepted_event_id,
                    ),
                )

        return mutate

    def accept_apt_research(
        self,
        command: RuntimeCommand,
        events: list[EventDraft],
        *,
        next_state: dict[str, Any],
        additional_artifacts=(),
        result_builder=None,
        mutation_plan: dict[str, Any],
    ) -> dict[str, Any]:
        try:
            return self.journal.accept(
                command,
                events,
                next_state=next_state,
                additional_artifacts=additional_artifacts,
                result_builder=result_builder,
                mutate=self.apt_research_mutation(mutation_plan),
            )
        except sqlite3.IntegrityError as exc:
            raise ConflictError("research semantic currentness conflict") from exc

    def get_reference_scout(self, scout_run_id: str) -> dict[str, Any]:
        self.journal.verify_store()
        with self.database.connect() as conn:
            run = conn.execute(
                "SELECT * FROM reference_scout_runs WHERE scout_run_id=?",
                (scout_run_id,),
            ).fetchone()
            if not run:
                raise NotFoundError("Reference Scout run not found")
            recommendations = conn.execute(
                """
                SELECT * FROM reference_recommendations
                WHERE scout_run_id=? ORDER BY recommendation_id
                """,
                (scout_run_id,),
            ).fetchall()
            event_rows = {
                row["event_id"]: row
                for row in conn.execute(
                    """
                    SELECT e.event_id,e.payload_hash,a.body,a.content_hash
                    FROM events e JOIN artifacts a ON a.artifact_id=e.payload_ref
                    WHERE e.event_id IN (
                      SELECT start_event_id FROM reference_scout_runs
                      WHERE scout_run_id=?
                      UNION
                      SELECT source_event_id FROM reference_recommendations
                      WHERE scout_run_id=?
                    )
                    """,
                    (scout_run_id, scout_run_id),
                ).fetchall()
            }
            bundle = (
                conn.execute(
                    "SELECT * FROM artifacts WHERE artifact_id=?",
                    (run["bundle_artifact_id"],),
                ).fetchone()
                if run["bundle_artifact_id"]
                else None
            )
        start_event = event_rows.get(run["start_event_id"])
        if not start_event:
            raise IntegrityError("Reference Scout start event is missing")
        start_payload = parse_strict_json(bytes(start_event["body"]))
        if (
            start_event["payload_hash"] != start_event["content_hash"]
            or digest_bytes(bytes(start_event["body"])) != start_event["content_hash"]
            or start_payload.get("scout_run_id") != scout_run_id
        ):
            raise IntegrityError("Reference Scout start evidence is inconsistent")
        for recommendation in recommendations:
            evidence = event_rows.get(recommendation["source_event_id"])
            if not evidence:
                raise IntegrityError("Scout recommendation event is missing")
            payload = parse_strict_json(bytes(evidence["body"]))
            if (
                evidence["payload_hash"] != evidence["content_hash"]
                or digest_bytes(bytes(evidence["body"])) != evidence["content_hash"]
                or payload.get("recommendation", {}).get("recommendation_id")
                != recommendation["recommendation_id"]
                or payload.get("message_id") != recommendation["message_id"]
            ):
                raise IntegrityError("Scout recommendation evidence is inconsistent")
        if run["bundle_artifact_id"] and (
            not bundle
            or bundle["content_hash"] != run["bundle_digest"]
            or digest_bytes(bytes(bundle["body"])) != run["bundle_digest"]
        ):
            raise IntegrityError("Reference Scout bundle artifact is inconsistent")
        return {
            "scout_run": dict(run),
            "recommendations": [dict(row) for row in recommendations],
        }

    def get_dispatch_operational_lineage(
        self, dispatch_id: str
    ) -> dict[str, Any]:
        self.journal.verify_store()
        with self.database.connect() as conn:
            link = conn.execute(
                "SELECT * FROM dispatch_links WHERE dispatch_id=?", (dispatch_id,)
            ).fetchone()
            if not link:
                raise NotFoundError("dispatch lineage not found")
            scouts = conn.execute(
                """
                SELECT * FROM reference_scout_runs
                WHERE dispatch_id=? ORDER BY requested_at,scout_run_id
                """,
                (dispatch_id,),
            ).fetchall()
            recommendations = conn.execute(
                """
                SELECT rr.* FROM reference_recommendations rr
                JOIN reference_scout_runs sr
                  ON sr.scout_run_id=rr.scout_run_id
                WHERE sr.dispatch_id=?
                ORDER BY rr.scout_run_id,rr.recommendation_id
                """,
                (dispatch_id,),
            ).fetchall()
            ingestions = conn.execute(
                """
                SELECT * FROM dispatch_ingestions
                WHERE dispatch_id=? ORDER BY accepted_offset
                """,
                (dispatch_id,),
            ).fetchall()
            captures = conn.execute(
                """
                SELECT research_capture_id,expected_contribution_id,capture_status,
                       raw_artifact_id,capture_digest,accepted_event_id,
                       accepted_offset,is_current
                FROM apt_research_captures_projection
                WHERE dispatch_id=? ORDER BY accepted_offset
                """,
                (dispatch_id,),
            ).fetchall()
            ingestion_evidence = {
                row["ingestion_id"]: row
                for row in conn.execute(
                    """
                    SELECT di.ingestion_id,e.payload_hash,a.body,a.content_hash,
                           input.body AS input_body,input.content_hash AS input_hash,
                           input.size_bytes AS input_size
                    FROM dispatch_ingestions di
                    JOIN events e ON e.event_id=di.event_id
                    JOIN artifacts a ON a.artifact_id=e.payload_ref
                    LEFT JOIN artifacts input ON input.artifact_id=di.artifact_id
                    WHERE di.dispatch_id=?
                    """,
                    (dispatch_id,),
                ).fetchall()
            }
        for ingestion in ingestions:
            evidence = ingestion_evidence.get(ingestion["ingestion_id"])
            if not evidence:
                raise IntegrityError("dispatch ingestion event is missing")
            payload = parse_strict_json(bytes(evidence["body"]))
            if (
                evidence["payload_hash"] != evidence["content_hash"]
                or digest_bytes(bytes(evidence["body"])) != evidence["content_hash"]
                or payload.get("ingestion_id") != ingestion["ingestion_id"]
            ):
                raise IntegrityError("dispatch ingestion event is inconsistent")
            if ingestion["coverage"] == "exact" and (
                evidence["input_hash"] != ingestion["content_digest"]
                or digest_bytes(bytes(evidence["input_body"]))
                != ingestion["content_digest"]
                or evidence["input_size"] != ingestion["size_bytes"]
            ):
                raise IntegrityError("dispatch ingestion artifact is inconsistent")
        return {
            "session_dispatch_link": dict(link),
            "scout_runs": [dict(row) for row in scouts],
            "recommendations": [dict(row) for row in recommendations],
            "ingestions": [dict(row) for row in ingestions],
            "research_captures": [dict(row) for row in captures],
        }

    def health(self) -> dict[str, Any]:
        journal = self.journal.verify_store()
        with self.database.connect() as conn:
            profiles = int(
                conn.execute("SELECT count(*) FROM protocol_profiles").fetchone()[0]
            )
        projection = self.projections.apt_state()
        ready = profiles == 4 and bool(projection["current"])
        return {
            "status": "ready" if ready else "degraded",
            "ready": ready,
            "journal": journal,
            "profiles": {"registered": profiles, "required": 4},
            "projection": projection,
            "production_serve_enabled": False,
        }

    def get_session(self, session_id: str) -> dict[str, Any]:
        with self.database.connect() as conn:
            session = conn.execute(
                "SELECT * FROM sessions WHERE session_id=?", (session_id,)
            ).fetchone()
            if not session:
                raise NotFoundError("session not found")
            links = conn.execute(
                "SELECT dispatch_id,row_digest,event_id FROM dispatch_links WHERE session_id=? ORDER BY dispatch_id",
                (session_id,),
            ).fetchall()
            scouts = conn.execute(
                """
                SELECT scout_run_id,dispatch_id,state,bundle_digest,requested_at
                FROM reference_scout_runs
                WHERE session_id=? ORDER BY requested_at,scout_run_id
                """,
                (session_id,),
            ).fetchall()
            ingestions = conn.execute(
                """
                SELECT ingestion_id,dispatch_id,source_kind,locator,coverage,
                       content_digest,accepted_offset
                FROM dispatch_ingestions
                WHERE session_id=? ORDER BY accepted_offset
                """,
                (session_id,),
            ).fetchall()
        return {
            "session": dict(session),
            "dispatch_links": [dict(row) for row in links],
            "scout_runs": [dict(row) for row in scouts],
            "ingestions": [dict(row) for row in ingestions],
        }
