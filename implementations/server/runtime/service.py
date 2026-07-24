"""Composition root and descriptor-bounded ACI/APT vertical-slice commands."""

from __future__ import annotations

import json
import secrets
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .artifacts import ArtifactStore
from .canonical import (
    canonical_bytes,
    canonical_digest,
    canonical_text,
    digest_bytes,
    parse_strict_json,
)
from .capabilities import CapabilityManager
from .database import RuntimeDatabase
from .errors import (
    AuthorizationError,
    ConflictError,
    IdempotencyConflict,
    IntegrityError,
    NotFoundError,
    ValidationError,
)
from .journal import EventDraft, PrerequisiteHead, RuntimeCommand, RuntimeJournal
from .legacy import StrictLegacySnapshotResolver
from .profiles import ProfileImporter, VerifiedProfile
from .projections import ProjectionManager, ProjectionRegistration

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
        "reference_scout.terminated@1": "aci.reference-scout-terminated@1",
        "dispatch.ingestion_recorded@1": "aci.dispatch-ingestion-recorded@1",
    }.items()
}


@dataclass(frozen=True)
class RuntimeSettings:
    database_path: Path
    repo_root: Path
    ledger_path: Path
    local_pilot_serve_enabled: bool = False
    repo_id: str = "cyberalchemy-orchestrator"


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
                "reference_scout.terminated@1": (
                    self._validate_scout_terminated_event
                ),
                "dispatch.ingestion_recorded@1": (
                    self._validate_dispatch_ingestion_event
                ),
            }
        )
        return {"applied_migrations": applied, "policy": self.database.verify_policy()}

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
            },
            "LegacyLedgerRowIdentity",
        )
        if identity["dispatch_id"] != payload["link"]["dispatch_id"]:
            raise IntegrityError("legacy ledger identity dispatch does not match link")
        for field in ("row_kind", "appender_identity", "contract_version"):
            if not isinstance(identity[field], str) or not identity[field]:
                raise IntegrityError(f"legacy ledger identity {field} is malformed")
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
    ) -> EventDraft:
        binding = dict(self.journal._schema_bindings).get(event_type)
        if not binding:
            raise IntegrityError(f"event type is not registered: {event_type}")
        schema_ref, schema_digest = binding
        event_id = self._stable_id(
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
        if not link:
            raise NotFoundError("linked Session and dispatch are required before close")
        if unfinished_scout:
            raise ConflictError(
                "dispatch cannot close with unfinished Reference Scout "
                f"{unfinished_scout['scout_run_id']} ({unfinished_scout['state']})"
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
