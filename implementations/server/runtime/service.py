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
from .canonical import canonical_bytes, canonical_digest, canonical_text, parse_strict_json
from .capabilities import CapabilityManager
from .database import RuntimeDatabase
from .errors import ConflictError, IntegrityError, NotFoundError, ValidationError
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
        return {"applied_migrations": applied, "policy": self.database.verify_policy()}

    def _register_projection_ports(self) -> None:
        def session_reducer(state, event):
            result = dict(state)
            if event["event_type"] == "apt.session_started":
                result["session"] = event["payload"]
                result.setdefault("dispatch_ids", [])
            elif event["event_type"] == "apt.session_dispatch_linked":
                dispatch_id = event["payload"]["dispatch_id"]
                result["dispatch_ids"] = sorted(
                    set(result.get("dispatch_ids", [])) | {dispatch_id}
                )
            result["effective_as_of"] = event["journal_offset"]
            return result

        def dispatch_reducer(state, event):
            return {
                **state,
                "dispatch_link": event["payload"],
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
        self, *, origin_digest: str, name: str, idempotency_key: str = "ensure"
    ) -> dict[str, Any]:
        if not origin_digest.startswith("sha256:") or not name:
            raise ValidationError("session origin digest and name are required")
        session_id = self._stable_id("ses_", origin_digest)
        aggregate_id = f"apt.session-binding:{origin_digest}"
        started_at = self.now().isoformat()
        payload = {
            "session_id": session_id,
            "origin_digest": origin_digest,
            "name": name,
            "started_at": started_at,
        }
        command = self._command(
            command_name="apt.ensure-session@1",
            scope_key=aggregate_id,
            idempotency_key=idempotency_key,
            aggregate_type="apt.session-binding",
            aggregate_id=aggregate_id,
            expected_version=0,
            authority={"principal_id": "runtime-bootstrap", "action": "session.ensure"},
            intent={"origin_digest": origin_digest, "name": name},
        )
        event = self._event("apt.session_started", payload)

        def result(records, base):
            return {**base, "session": payload}

        def mutate(conn, records, _result):
            conn.execute(
                """
                INSERT INTO sessions(session_id,origin_digest,name,started_at,event_id)
                VALUES(?,?,?,?,?)
                """,
                (session_id, origin_digest, name, started_at, records[0].event_id),
            )
            self.projections.apply_complete_group(
                conn,
                projection_name="apt.session-record",
                projection_key=session_id,
                events=[
                    {
                        "event_type": "apt.session_started",
                        "payload": payload,
                        "event_id": records[0].event_id,
                        "journal_offset": records[0].journal_offset,
                    }
                ],
                last_offset=records[0].journal_offset,
            )

        return self.journal.accept(
            command, [event], next_state=payload, result_builder=result, mutate=mutate
        )

    def link_session_dispatch(
        self,
        *,
        session_id: str,
        dispatch_id: str,
        idempotency_key: str = "link",
    ) -> dict[str, Any]:
        snapshot = self.legacy.resolve(self.settings.ledger_path, dispatch_id)
        with self.database.connect() as conn:
            session = conn.execute(
                "SELECT * FROM sessions WHERE session_id=?", (session_id,)
            ).fetchone()
        if not session:
            raise NotFoundError("session not found")
        session_head = self.journal.head(
            f"apt.session-binding:{session['origin_digest']}"
        )
        aggregate_id = f"apt.dispatch-link:{dispatch_id}"
        payload = {
            "session_dispatch_link_id": self._stable_id(
                "lnk_", [session_id, dispatch_id, snapshot.row_digest]
            ),
            "session_id": session_id,
            "dispatch_id": dispatch_id,
            "snapshot": {
                "kind": "legacy_ledger",
                "ledger_row_identity": {
                    "dispatch_id": dispatch_id,
                    "row_kind": snapshot.row_kind,
                    "appender_identity": snapshot.appender_identity,
                    "contract_version": snapshot.contract_version,
                },
                "row_digest": snapshot.row_digest,
            },
        }
        command = self._command(
            command_name="apt.link-session-dispatch@1",
            scope_key=aggregate_id,
            idempotency_key=idempotency_key,
            aggregate_type="apt.dispatch-link",
            aggregate_id=aggregate_id,
            expected_version=0,
            authority={"principal_id": "runtime-bootstrap", "action": "dispatch.link"},
            intent={
                "session_id": session_id,
                "dispatch_id": dispatch_id,
                "row_digest": snapshot.row_digest,
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
            return {**base, "dispatch_link": payload}

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
                    self.now().isoformat(),
                ),
            )
            projected = {
                "event_type": "apt.session_dispatch_linked",
                "payload": payload,
                "event_id": records[0].event_id,
                "journal_offset": records[0].journal_offset,
            }
            self.projections.apply_complete_group(
                conn,
                projection_name="apt.session-record",
                projection_key=session_id,
                events=[projected],
                last_offset=records[0].journal_offset,
            )
            self.projections.apply_complete_group(
                conn,
                projection_name="apt.dispatch-scope",
                projection_key=dispatch_id,
                events=[projected],
                last_offset=records[0].journal_offset,
            )

        return self.journal.accept(
            command, [event], next_state=payload, result_builder=result, mutate=mutate
        )

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
        if intent.get("round_id") != "probe":
            raise ValidationError("local probe round must be 'probe'")
        if not intent.get("message_type") or not intent.get("idempotency_key"):
            raise ValidationError("message type and idempotency key are required")
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
            aggregate_type="aci.local-probe",
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
        command = self._command(
            command_name="aci.verify-publication-receipt@1",
            scope_key=f"{aggregate_id}:verify",
            idempotency_key="verify:" + candidate["publication_event_id"],
            aggregate_type="aci.local-probe",
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
        event = self._event("reference_probe.accepted@1", payload)

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
                    if (
                        existing["canonical_payload_digest"] != semantic
                        or existing["expected_head_event_id"]
                        != item["expected_head_event_id"]
                    ):
                        raise ConflictError("delivery semantic identity conflict")
                    status = "existing_exact"
                    accepted_event_id = existing["accepted_event_id"]
                else:
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
            return {
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
            return {**base, "semantic_results": results}

        def mutate(conn, records, result_receipt):
            record_iter = iter(records)
            projected_by_capture: dict[str, list[dict[str, Any]]] = {}
            new_delivery_events: dict[str, dict[str, Any]] = {}
            for member in prepared:
                if member["status"] == "submitted_new":
                    record = next(record_iter)
                    event_id = record.event_id
                    if member["rank"] == 0:
                        conn.execute(
                            """
                            INSERT INTO apt_delivery_keys(
                              delivery_subject_key,canonical_payload_digest,
                              expected_head_event_id,accepted_event_id
                            ) VALUES(?,?,?,?)
                            """,
                            (
                                member["key"],
                                member["semantic_digest"],
                                member["event_payload"]["expected_head_event_id"],
                                event_id,
                            ),
                        )
                        new_delivery_events[member["key"]] = {
                            "event_type": member["event_type"],
                            "payload": member["event_payload"],
                            "event_id": event_id,
                            "journal_offset": record.journal_offset,
                        }
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
                        projected_by_capture.setdefault(
                            entity["research_capture_id"], []
                        ).append(
                            {
                                "event_type": member["event_type"],
                                "payload": member["event_payload"],
                                "event_id": event_id,
                                "journal_offset": record.journal_offset,
                            }
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
            # A delivery has no capture key of its own.  Materialize it into
            # every newly dependent research record, ahead of the reference
            # use, so readback retains the official probe origin.
            for member in prepared:
                if member["rank"] != 1 or member["status"] != "submitted_new":
                    continue
                ref = member["entity"]["probe_recommendation_ref"]
                subject = canonical_digest(
                    {
                        "probe_id": ref["probe_id"],
                        "bundle_digest": ref["bundle_digest"],
                        "recommendation_id": ref["recommendation_id"],
                    }
                )
                delivery_event = new_delivery_events.get(subject)
                if delivery_event:
                    capture_id = member["entity"]["research_capture_id"]
                    projected_by_capture[capture_id].insert(0, delivery_event)
            for capture_id, projected in projected_by_capture.items():
                self.projections.apply_complete_group(
                    conn,
                    projection_name="apt.research-record",
                    projection_key=capture_id,
                    events=projected,
                    last_offset=records[-1].journal_offset,
                )

        return self.journal.accept(
            command,
            events,
            next_state={
                "accepted_subjects": [member["key"] for member in new_items]
            },
            result_builder=result,
            mutate=mutate,
        )

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
        if (
            publication_receipt.get("event_id") != message["publication_event_id"]
            or publication_receipt.get("message_id") != message["message_id"]
            or publication_receipt.get("payload_hash") != message["payload_hash"]
            or publication_receipt.get("journal_offset")
            != message["publication_offset"]
            or publication_receipt.get("status") != "persisted_candidate"
        ):
            raise ConflictError("publication receipt identity mismatch")
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
        return {"session": dict(session), "dispatch_links": [dict(row) for row in links]}
