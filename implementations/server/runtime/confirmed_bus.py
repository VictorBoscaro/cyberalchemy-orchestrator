"""Pure confirmed-mapping projection for official attempt-result publication."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence

from .canonical import canonical_bytes, canonical_digest, digest_bytes, parse_strict_json
from .confirmation import _binding_digest as derive_confirmed_binding_digest
from .confirmation import derive_id as derive_confirmation_id
from .errors import ConflictError, ValidationError
from .run_group import GroupProjection, reduce_group


_MESSAGE_EVENTS = {
    "author.output": "position.accepted",
    "reviewer.output": "critique.accepted",
}
_MESSAGE_PHASES = {
    "author.output": "collecting",
    "reviewer.output": "deliberating",
}
_RECEIPT_FIELDS = {
    "event_id",
    "idempotency_key",
    "journal_offset",
    "message_id",
    "payload_hash",
    "receipt_version",
    "status",
}
_ATTEMPT_EVENTS = (
    "attempt.requested",
    "attempt.starting",
    "attempt.running",
    "attempt.completed",
)
_PUBLICATION_EVENT_FIELDS = {
    "attempt_id",
    "candidate_id",
    "group_aggregate_id",
    "idempotency_key",
    "message_id",
    "message_type",
    "operation_id",
    "payload_hash",
    "payload_ref",
    "receipt_version",
    "reply_to_message_ids",
    "round_id",
    "schema",
    "seat_id",
    "status",
}


def reduce_confirmed_bus_group_pair(
    current: GroupProjection, ordered_event_types: Sequence[Any]
) -> GroupProjection:
    """Fold the BUS pair: the first event links an Attempt; only the second reduces Group state."""

    event_types = tuple(
        _text(event_type, "confirmed bus event type") for event_type in ordered_event_types
    )
    if len(event_types) != 2 or event_types[0] != "attempt.result_accepted":
        raise ValidationError("confirmed bus event pair/order differs")
    guards_by_event = {
        "position.accepted": {
            "parent_receipt_verified": True,
            "logical_key_unused": True,
        },
        "critique.accepted": {
            "reply_visible": True,
            "round_schema_valid": True,
        },
    }
    try:
        guards = guards_by_event[event_types[1]]
    except KeyError as exc:
        raise ValidationError("confirmed bus official event type is not admitted") from exc
    return reduce_group(current, event_types[1], guards)


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValidationError(f"{label} must be a non-empty string")
    return value


def _integer(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValidationError(f"{label} must be an integer")
    return value


def derive_group_aggregate_id(
    *, run_id: Any, graph_id: Any, group_id: Any, group_version: Any
) -> str:
    """Derive the exact graph-scoped Group aggregate identity frozen by TECH-D0."""

    run_id = _text(run_id, "run_id")
    graph_id = _text(graph_id, "graph_id")
    group_id = _text(group_id, "group_id")
    group_version = _integer(group_version, "group_version")
    if group_version != 1:
        raise ValidationError("group_version must equal 1")
    preimage = {
        "schema": "aci.runtime-group-aggregate-id-preimage@1",
        "run_id": run_id,
        "graph_id": graph_id,
        "group_id": group_id,
        "group_version": group_version,
    }
    return "grp_" + canonical_digest(preimage)[7:39]


def _derived_id(prefix: str, kind: str, semantic_digest: str) -> str:
    digest = canonical_digest(
        {
            "schema": "aci.confirmed-bus-identity-preimage@1",
            "kind": kind,
            "semantic_digest": semantic_digest,
        }
    )
    return prefix + digest[7:39]


def require_attempt_journal_chain(
    attempt: Mapping[str, Any], rows: Iterable[Mapping[str, Any]]
) -> None:
    """Require the exact four single-event Attempt lifecycle receipts."""

    chain = tuple(dict(row) for row in rows)
    if tuple(row.get("event_type") for row in chain) != _ATTEMPT_EVENTS:
        raise ValidationError("attempt does not have the complete journal lifecycle")
    aggregate_id = _text(attempt.get("aggregate_id"), "attempt.aggregate_id")
    for version, row in enumerate(chain, start=1):
        if (
            row.get("aggregate_id") != aggregate_id
            or row.get("aggregate_version") != version
            or row.get("event_count") != 1
            or row.get("receipt_event_count") != 1
            or row.get("first_offset") != row.get("journal_offset")
            or row.get("last_offset") != row.get("journal_offset")
            or row.get("receipt_aggregate_id") != aggregate_id
            or row.get("receipt_expected_version") != version - 1
        ):
            raise ValidationError("attempt lifecycle receipt is incomplete")
    if (
        attempt.get("version") != 4
        or attempt.get("state") != "completed"
        or attempt.get("requested_event_id") != chain[0].get("event_id")
        or attempt.get("last_event_id") != chain[-1].get("event_id")
        or attempt.get("last_offset") != chain[-1].get("journal_offset")
    ):
        raise ValidationError("attempt terminal projection differs from journal")


def require_group_journal_chain(
    group_head: Mapping[str, Any],
    group_aggregate_id: str,
    rows: Iterable[Mapping[str, Any]],
) -> None:
    """Require the exact harness-only phase chain behind one composite Group head."""

    expected = {
        "collecting": ("group.started",),
        "deliberating": ("group.started", "collection.closed", "reveal.published"),
    }.get(group_head.get("state"))
    chain = tuple(dict(row) for row in rows)
    if expected is None or tuple(row.get("event_type") for row in chain) != expected:
        raise ValidationError("group does not have the exact harness phase lifecycle")
    for version, row in enumerate(chain, start=1):
        if (
            row.get("aggregate_id") != group_aggregate_id
            or row.get("aggregate_version") != version
            or row.get("event_count") != 1
            or row.get("receipt_event_count") != 1
            or row.get("first_offset") != row.get("journal_offset")
            or row.get("last_offset") != row.get("journal_offset")
            or row.get("receipt_aggregate_id") != group_aggregate_id
            or row.get("receipt_expected_version") != version - 1
        ):
            raise ValidationError("group phase lifecycle receipt is incomplete")
    if (
        group_head.get("version") != len(chain)
        or group_head.get("last_event_id") != chain[-1].get("event_id")
        or group_head.get("last_offset") != chain[-1].get("journal_offset")
    ):
        raise ValidationError("group phase head differs from journal")


def _require_artifact(
    artifact: Mapping[str, Any],
    *,
    artifact_id: Any,
    content_hash: Any,
    classification: str,
) -> bytes:
    body = artifact.get("body")
    if not isinstance(body, bytes):
        raise ValidationError("artifact body must be an immutable blob")
    content_hash = _text(content_hash, "artifact content_hash")
    if (
        artifact.get("artifact_id") != artifact_id
        or artifact.get("content_hash") != content_hash
        or artifact.get("size_bytes") != len(body)
        or digest_bytes(body) != content_hash
        or artifact.get("artifact_id") != "art_" + content_hash[7:39]
        or artifact.get("classification") != classification
        or artifact.get("tombstoned_at") is not None
        or artifact.get("tombstone_reason") is not None
    ):
        raise ValidationError("artifact identity/content/policy differs")
    for field in (
        "media_type",
        "schema_ref",
        "redaction_policy_ref",
        "retention_policy_ref",
        "tombstone_policy_ref",
        "authorization_policy_ref",
        "policy_bundle_digest",
        "finalization_receipt_ref",
        "finalized_at",
    ):
        if not isinstance(artifact.get(field), str) or not artifact[field]:
            raise ValidationError("artifact finalized metadata is incomplete")
    return body


@dataclass(frozen=True)
class ConfirmedBusProjection:
    acceptance_id: str
    command_id: str
    attempt_result_event_id: str
    official_event_id: str
    scope_key: str
    idempotency_key: str
    semantic_digest: str
    dispatch_id: str
    run_id: str
    graph_id: str
    group_id: str
    group_version: int
    group_aggregate_id: str
    mapping_id: str
    source_message_id: str
    source_message_type: str
    operation_id: str
    seat_id: str
    turn_ordinal: int
    round_id: str
    attempt_id: str
    attempt_aggregate_id: str
    candidate_id: str
    publication_event_id: str
    publication_receipt_event_id: str
    publication_idempotency_key: str
    publication_journal_offset: int
    payload_ref: str
    payload_hash: str
    receipt_digest: str
    parent_principal_id: str
    official_event_type: str
    required_group_state: str
    group_head_version: int
    group_head_last_event_id: str
    group_head_last_offset: int
    reply_to_message_ids: tuple[str, ...]

    def authority_context(self) -> dict[str, Any]:
        return {
            "confirmed_mapping_id": self.mapping_id,
            "dispatch_id": self.dispatch_id,
            "graph_id": self.graph_id,
            "parent_principal_id": self.parent_principal_id,
            "schema": "aci.confirmed-bus-authority@1",
        }

    def semantic_intent(self) -> dict[str, Any]:
        return {
            "attempt_id": self.attempt_id,
            "candidate_id": self.candidate_id,
            "group_aggregate_id": self.group_aggregate_id,
            "mapping_id": self.mapping_id,
            "message_type": self.source_message_type,
            "publication_receipt_event_id": self.publication_receipt_event_id,
            "reply_to_message_ids": list(self.reply_to_message_ids),
            "schema": "aci.confirmed-attempt-result-acceptance-intent@1",
            "source_message_id": self.source_message_id,
        }

    def attempt_result_payload(self) -> dict[str, Any]:
        return {
            "attempt_id": self.attempt_id,
            "group_aggregate_id": self.group_aggregate_id,
            "logical_message_key": {
                "message_type": self.source_message_type,
                "round_id": self.round_id,
                "seat_id": self.seat_id,
            },
            "operation_id": self.operation_id,
            "parent_principal_id": self.parent_principal_id,
            "receipt": {
                "event_id": self.publication_receipt_event_id,
                "idempotency_key": self.publication_idempotency_key,
                "journal_offset": self.publication_journal_offset,
                "message_id": self.source_message_id,
                "payload_hash": self.payload_hash,
                "receipt_digest": self.receipt_digest,
                "receipt_version": "1",
                "status": "persisted_candidate",
            },
            "schema": "aci.attempt-result-accepted@1",
        }

    def official_payload(self) -> dict[str, Any]:
        return {
            "attempt_id": self.attempt_id,
            "group_aggregate_id": self.group_aggregate_id,
            "group_id": self.group_id,
            "group_version": self.group_version,
            "message_id": self.source_message_id,
            "message_type": self.source_message_type,
            "operation_id": self.operation_id,
            "payload_hash": self.payload_hash,
            "payload_ref": self.payload_ref,
            "publication_event_id": self.publication_event_id,
            "reply_to_message_ids": list(self.reply_to_message_ids),
            "round_id": self.round_id,
            "run_id": self.run_id,
            "schema": "aci.confirmed-official-contribution@1",
            "seat_id": self.seat_id,
        }


def project_confirmed_bus_acceptance(
    *,
    mapping: Mapping[str, Any],
    graph: Mapping[str, Any],
    run: Mapping[str, Any],
    attempt: Mapping[str, Any],
    candidate: Mapping[str, Any],
    publication_receipt: Mapping[str, Any],
    publication_event: Mapping[str, Any],
    publication_command_receipt: Mapping[str, Any],
    publication_event_payload_artifact: Mapping[str, Any],
    contribution_artifact: Mapping[str, Any],
    group_head: Mapping[str, Any],
    parent_principal_id: Any,
    reply_to_message_ids: Sequence[Any] = (),
) -> ConfirmedBusProjection:
    """Validate one closed authoritative chain and derive the atomic acceptance."""

    parent_principal_id = _text(parent_principal_id, "parent_principal_id")
    dispatch_id = _text(mapping.get("dispatch_id"), "mapping.dispatch_id")
    graph_id = _text(graph.get("graph_id"), "graph.graph_id")
    run_id = _text(graph.get("run_id"), "graph.run_id")
    dispatch_spec_digest = _text(run.get("dispatch_spec_digest"), "run.dispatch_spec_digest")
    group_id = _text(mapping.get("source_group_id"), "mapping.source_group_id")
    group_version = 1
    message_type = _text(mapping.get("source_message_type"), "mapping.source_message_type")
    try:
        official_event_type = _MESSAGE_EVENTS[message_type]
        required_group_state = _MESSAGE_PHASES[message_type]
    except KeyError as exc:
        raise ValidationError("confirmed source message type is not admitted") from exc

    if graph.get("dispatch_id") != dispatch_id or run.get("dispatch_id") != dispatch_id:
        raise ValidationError("confirmed run/graph dispatch differs from mapping")
    if run.get("run_id") != run_id:
        raise ValidationError("confirmed graph does not belong to run")
    if graph.get("dispatch_spec_digest") != dispatch_spec_digest:
        raise ValidationError("confirmed graph dispatch digest differs from run")
    if run_id != derive_confirmation_id(
        "run", [], dispatch_id=dispatch_id, dispatch_spec_digest=dispatch_spec_digest
    ) or graph_id != derive_confirmation_id(
        "turn_graph", [], dispatch_id=dispatch_id, dispatch_spec_digest=dispatch_spec_digest
    ):
        raise ValidationError("confirmed run/graph identity derivation differs")
    expected_message_id = derive_confirmation_id(
        "source_message",
        [
            mapping.get("source_operation_id"),
            mapping.get("source_round_id"),
            mapping.get("source_message_type"),
        ],
        dispatch_id=dispatch_id,
        dispatch_spec_digest=dispatch_spec_digest,
    )
    expected_mapping_id = derive_confirmation_id(
        "input_mapping",
        [
            mapping.get("slot_ordinal"),
            mapping.get("source_operation_id"),
            mapping.get("source_turn_ordinal"),
        ],
        dispatch_id=dispatch_id,
        dispatch_spec_digest=dispatch_spec_digest,
    )
    if (
        mapping.get("mapping_id") != expected_mapping_id
        or mapping.get("source_message_id") != expected_message_id
        or mapping.get("continuation_id") != graph.get("continuation_id")
    ):
        raise ValidationError("confirmed mapping/message identity derivation differs")
    if mapping.get("mapping_version") != 1:
        raise ValidationError("confirmed mapping version differs")
    visibility_policy_json = mapping.get("visibility_policy_ref_json")
    if not isinstance(visibility_policy_json, str):
        raise ValidationError("confirmed mapping visibility policy is not canonical JSON")
    visibility_policy_ref = parse_strict_json(visibility_policy_json)
    if (
        not isinstance(visibility_policy_ref, dict)
        or canonical_bytes(visibility_policy_ref) != visibility_policy_json.encode("utf-8")
    ):
        raise ValidationError("confirmed mapping visibility policy is not canonical JSON")
    frozen_mapping = {
        name: mapping.get(name)
        for name in (
            "dispatch_id",
            "continuation_id",
            "source_group_id",
            "source_seat_id",
            "source_operation_id",
            "source_turn_ordinal",
            "source_round_id",
            "source_message_id",
            "source_message_type",
            "target_seat_id",
            "target_turn_ordinal",
            "slot_name",
            "slot_ordinal",
        )
    }
    frozen_mapping["visibility_policy_ref"] = visibility_policy_ref
    if mapping.get("confirmed_binding_digest") != derive_confirmed_binding_digest(
        frozen_mapping
    ):
        raise ValidationError("confirmed mapping binding digest differs")
    if attempt.get("dispatch_id") != dispatch_id or attempt.get("graph_id") != graph_id:
        raise ValidationError("attempt confirmed parent differs")
    for field, expected in (
        ("operation_id", mapping.get("source_operation_id")),
        ("seat_id", mapping.get("source_seat_id")),
        ("turn_ordinal", mapping.get("source_turn_ordinal")),
    ):
        if attempt.get(field) != expected:
            raise ValidationError(f"attempt {field} differs from confirmed mapping")
    if attempt.get("state") != "completed" or attempt.get("version") != 4:
        raise ValidationError("attempt is not journal-backed completed version 4")
    attempt_aggregate_id = _text(attempt.get("aggregate_id"), "attempt.aggregate_id")

    group_aggregate_id = derive_group_aggregate_id(
        run_id=run_id,
        graph_id=graph_id,
        group_id=group_id,
        group_version=group_version,
    )
    for field, expected in (
        ("graph_id", graph_id),
        ("group_id", group_id),
        ("group_version", group_version),
        ("state", required_group_state),
    ):
        if group_head.get(field) != expected:
            raise ValidationError(f"group head {field} differs")
    group_head_version = _integer(group_head.get("version"), "group_head.version")

    source_message_id = _text(mapping.get("source_message_id"), "source_message_id")
    attempt_id = _text(attempt.get("attempt_id"), "attempt_id")
    candidate_checks = (
        ("message_id", source_message_id),
        ("group_aggregate_id", group_aggregate_id),
        ("seat_id", mapping.get("source_seat_id")),
        ("round_id", mapping.get("source_round_id")),
        ("message_type", message_type),
        ("attempt_id", attempt_id),
        ("operation_id", mapping.get("source_operation_id")),
        ("status", "active"),
        ("candidate_version", 1),
    )
    for field, expected in candidate_checks:
        if candidate.get(field) != expected:
            raise ValidationError(f"candidate {field} differs")
    if candidate.get("official_accepted_event_id") is not None or candidate.get(
        "abandoned_event_id"
    ) is not None:
        raise ConflictError("candidate is no longer exclusively active")

    receipt_checks = (
        ("event_id", candidate.get("publication_event_id")),
        ("message_id", source_message_id),
        ("idempotency_key", candidate.get("idempotency_key")),
        ("payload_hash", candidate.get("payload_hash")),
        ("receipt_bytes", candidate.get("receipt_bytes")),
        ("receipt_digest", candidate.get("receipt_digest")),
        ("journal_offset", candidate.get("journal_offset")),
    )
    for field, expected in receipt_checks:
        if publication_receipt.get(field) != expected:
            raise ValidationError(f"publication receipt {field} differs")

    if (
        publication_event.get("event_id") != candidate.get("publication_event_id")
        or publication_event.get("event_type") != "publication.persisted"
        or publication_event.get("aggregate_type") != "aci.agent-attempt"
        or publication_event.get("aggregate_id") != attempt_aggregate_id
        or publication_event.get("aggregate_version") != attempt.get("version") + 1
        or publication_event.get("journal_offset") != candidate.get("journal_offset")
        or publication_event.get("command_id") != publication_command_receipt.get("command_id")
    ):
        raise ValidationError("publication event lineage differs")
    if (
        publication_receipt.get("scope_key") != attempt_aggregate_id
        or publication_command_receipt.get("scope_key") != attempt_aggregate_id
        or publication_command_receipt.get("aggregate_id") != attempt_aggregate_id
        or publication_command_receipt.get("expected_version") != attempt.get("version")
        or publication_command_receipt.get("idempotency_key")
        != publication_receipt.get("idempotency_key")
        or publication_command_receipt.get("first_offset") != candidate.get("journal_offset")
        or publication_command_receipt.get("last_offset") != candidate.get("journal_offset")
        or publication_command_receipt.get("event_count") != 1
    ):
        raise ValidationError("publication command scope/receipt differs")

    event_payload_bytes = _require_artifact(
        publication_event_payload_artifact,
        artifact_id=publication_event.get("payload_ref"),
        content_hash=publication_event.get("payload_hash"),
        classification="runtime-internal",
    )
    event_payload = parse_strict_json(event_payload_bytes)
    if (
        not isinstance(event_payload, dict)
        or set(event_payload) != _PUBLICATION_EVENT_FIELDS
        or canonical_bytes(event_payload) != event_payload_bytes
    ):
        raise ValidationError("publication event payload is not the closed canonical schema")
    expected_event_payload = {
        "attempt_id": attempt_id,
        "candidate_id": candidate.get("candidate_id"),
        "group_aggregate_id": group_aggregate_id,
        "idempotency_key": candidate.get("idempotency_key"),
        "message_id": source_message_id,
        "message_type": message_type,
        "operation_id": mapping.get("source_operation_id"),
        "payload_hash": candidate.get("payload_hash"),
        "payload_ref": candidate.get("payload_ref"),
        "receipt_version": "1",
        "reply_to_message_ids": list(reply_to_message_ids),
        "round_id": mapping.get("source_round_id"),
        "schema": "aci.publication-persisted@1",
        "seat_id": mapping.get("source_seat_id"),
        "status": "persisted_candidate",
    }
    if event_payload != expected_event_payload:
        raise ValidationError("candidate differs from immutable publication event payload")

    _require_artifact(
        contribution_artifact,
        artifact_id=candidate.get("payload_ref"),
        content_hash=candidate.get("payload_hash"),
        classification="sensitive-output",
    )

    receipt_bytes = candidate.get("receipt_bytes")
    if not isinstance(receipt_bytes, bytes):
        raise ValidationError("publication receipt bytes must be an immutable blob")
    receipt_digest = _text(candidate.get("receipt_digest"), "candidate.receipt_digest")
    if digest_bytes(receipt_bytes) != receipt_digest:
        raise ValidationError("publication receipt digest differs from its bytes")
    receipt_document = parse_strict_json(receipt_bytes)
    if not isinstance(receipt_document, dict) or set(receipt_document) != _RECEIPT_FIELDS:
        raise ValidationError("publication receipt has missing or unknown fields")
    if canonical_bytes(receipt_document) != receipt_bytes:
        raise ValidationError("publication receipt bytes are not canonical")
    expected_receipt_document = {
        "event_id": candidate.get("publication_event_id"),
        "idempotency_key": candidate.get("idempotency_key"),
        "journal_offset": candidate.get("journal_offset"),
        "message_id": source_message_id,
        "payload_hash": candidate.get("payload_hash"),
        "receipt_version": "1",
        "status": "persisted_candidate",
    }
    if receipt_document != expected_receipt_document:
        raise ValidationError("publication receipt canonical fields differ")
    command_result_json = publication_command_receipt.get("result_receipt_json")
    if not isinstance(command_result_json, str):
        raise ValidationError("publication command result is not canonical JSON")
    command_result = parse_strict_json(command_result_json)
    if (
        not isinstance(command_result, dict)
        or set(command_result) != _RECEIPT_FIELDS
        or canonical_bytes(command_result) != command_result_json.encode("utf-8")
        or command_result != receipt_document
    ):
        raise ValidationError("publication command result differs from canonical receipt")

    replies = tuple(_text(value, "reply_to_message_id") for value in reply_to_message_ids)
    if len(replies) != len(set(replies)):
        raise ValidationError("reply identities must be unique")
    if message_type == "author.output" and replies:
        raise ValidationError("author output cannot carry peer reply identities")
    if message_type == "reviewer.output" and not replies:
        raise ValidationError("reviewer output requires visible reply identity")

    semantic = {
        "attempt_id": attempt_id,
        "candidate_id": candidate.get("candidate_id"),
        "graph_id": graph_id,
        "group_aggregate_id": group_aggregate_id,
        "group_head_version": group_head_version,
        "group_head_last_event_id": group_head.get("last_event_id"),
        "group_head_last_offset": group_head.get("last_offset"),
        "mapping_id": mapping.get("mapping_id"),
        "parent_principal_id": parent_principal_id,
        "publication_receipt_event_id": publication_receipt.get("event_id"),
        "reply_to_message_ids": list(replies),
        "schema": "aci.confirmed-attempt-result-acceptance@1",
        "source_message_id": source_message_id,
    }
    semantic_digest = canonical_digest(semantic)
    return ConfirmedBusProjection(
        acceptance_id=_derived_id("ara_", "acceptance", semantic_digest),
        command_id=_derived_id("cmd_", "command", semantic_digest),
        attempt_result_event_id=_derived_id("evt_", "attempt.result_accepted", semantic_digest),
        official_event_id=_derived_id("evt_", official_event_type, semantic_digest),
        scope_key=f"aci.confirmed-bus:{mapping['mapping_id']}",
        idempotency_key="accept@1",
        semantic_digest=semantic_digest,
        dispatch_id=dispatch_id,
        run_id=run_id,
        graph_id=graph_id,
        group_id=group_id,
        group_version=group_version,
        group_aggregate_id=group_aggregate_id,
        mapping_id=_text(mapping.get("mapping_id"), "mapping_id"),
        source_message_id=source_message_id,
        source_message_type=message_type,
        operation_id=_text(mapping.get("source_operation_id"), "source_operation_id"),
        seat_id=_text(mapping.get("source_seat_id"), "source_seat_id"),
        turn_ordinal=_integer(mapping.get("source_turn_ordinal"), "source_turn_ordinal"),
        round_id=_text(mapping.get("source_round_id"), "source_round_id"),
        attempt_id=attempt_id,
        attempt_aggregate_id=attempt_aggregate_id,
        candidate_id=_text(candidate.get("candidate_id"), "candidate_id"),
        publication_event_id=_text(candidate.get("publication_event_id"), "publication_event_id"),
        publication_receipt_event_id=_text(publication_receipt.get("event_id"), "receipt.event_id"),
        publication_idempotency_key=_text(
            publication_receipt.get("idempotency_key"), "receipt.idempotency_key"
        ),
        publication_journal_offset=_integer(
            publication_receipt.get("journal_offset"), "receipt.journal_offset"
        ),
        payload_ref=_text(candidate.get("payload_ref"), "candidate.payload_ref"),
        payload_hash=_text(candidate.get("payload_hash"), "candidate.payload_hash"),
        receipt_digest=_text(candidate.get("receipt_digest"), "candidate.receipt_digest"),
        parent_principal_id=parent_principal_id,
        official_event_type=official_event_type,
        required_group_state=required_group_state,
        group_head_version=group_head_version,
        group_head_last_event_id=_text(
            group_head.get("last_event_id"), "group_head.last_event_id"
        ),
        group_head_last_offset=_integer(
            group_head.get("last_offset"), "group_head.last_offset"
        ),
        reply_to_message_ids=replies,
    )
