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
from .projections import ProjectionManager

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
        self._profiles = self.profile_importer.load_manifest(
            self.settings.repo_root / PROFILE_MANIFEST
        )
        bindings = ProfileImporter.event_bindings(self._profiles)
        bindings.update(ACI_SCHEMAS)
        self.journal.bind_event_schemas(bindings)
        return {"applied_migrations": applied, "policy": self.database.verify_policy()}

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
            scope_key=f"{aggregate_id}:publish",
            idempotency_key=intent["idempotency_key"],
            aggregate_type="aci.local-probe",
            aggregate_id=aggregate_id,
            expected_version=head["current_version"],
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
                    f"{aggregate_id}:publish",
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
                "SELECT * FROM publication_candidates WHERE publication_event_id=?",
                (publication_receipt["event_id"],),
            ).fetchone()
            if candidate and candidate["status"] == "officially_accepted":
                row = conn.execute(
                    """
                    SELECT cr.result_receipt_json FROM events e
                    JOIN command_receipts cr ON cr.command_id=e.command_id
                    WHERE e.event_id=?
                    """,
                    (candidate["official_accepted_event_id"],),
                ).fetchone()
                if row and bytes(candidate["receipt_bytes"]) == canonical_bytes(
                    publication_receipt
                ):
                    return json.loads(row["result_receipt_json"])
        if not candidate or candidate["status"] != "active":
            raise ConflictError("publication candidate is not active")
        stored_receipt = parse_strict_json(bytes(candidate["receipt_bytes"]))
        if stored_receipt != publication_receipt:
            raise ConflictError("publication receipt does not match committed evidence")
        if (
            candidate["group_aggregate_id"] != bound["group_aggregate_id"]
            or candidate["seat_id"] != bound["seat_id"]
            or candidate["attempt_id"] != bound["attempt_id"]
            or candidate["operation_id"] != bound["operation_id"]
        ):
            raise ConflictError("parent capability scope does not own candidate")
        aggregate_id = bound["aggregate_id"]
        head = self.journal.head(aggregate_id)
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
            expected_version=head["current_version"],
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
                capture = payload["research_capture"]
                conn.execute(
                    """
                    INSERT INTO apt_capture_keys(
                      research_capture_id,dispatch_id,expected_contribution_id,
                      capture_digest,accepted_event_id
                    ) VALUES(?,?,?,?,?)
                    """,
                    (
                        capture["research_capture_id"],
                        capture["dispatch_id"],
                        capture["expected_contribution_id"],
                        capture["capture_digest"],
                        records[0].event_id,
                    ),
                )
            elif command_name == "apt.append-research-fact@1":
                entity = payload["payload"]
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
                      fact_id,research_capture_id,subject_id,supersedes_fact_id,
                      canonical_payload_digest,accepted_event_id,is_current
                    ) VALUES(?,?,?,?,?,?,1)
                    """,
                    (
                        envelope["fact_id"],
                        entity["research_capture_id"],
                        envelope["subject_id"],
                        predecessor,
                        canonical_digest(entity),
                        records[0].event_id,
                    ),
                )
            conn.execute(
                """
                INSERT INTO apt_semantic_request_results(
                  request_key,request_digest,result_json,accepted_event_id
                ) VALUES(?,?,?,?)
                """,
                (
                    f"{aggregate_id}:{idempotency_key}",
                    command.digest,
                    canonical_text(result),
                    records[0].event_id,
                ),
            )

        return self.journal.accept(
            command, [event], next_state={"last_payload_digest": canonical_digest(payload)}, mutate=mutate
        )

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
