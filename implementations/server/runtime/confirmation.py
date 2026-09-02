"""Pure Runtime Confirmation Authority v1 compiler and verifier."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .canonical import canonical_bytes, canonical_digest, canonical_text, digest_bytes, parse_strict_json
from .errors import (
    ConfirmationObservationScopeMismatch,
    ConfirmationPayloadSchemaMismatch,
    ConfirmationProjectionMismatch,
    ConfirmationSchemaVersionsMismatch,
    DerivedIdentityMismatch,
    DispatchSpecDigestMismatch,
    ForbiddenEffectBoundary,
    IdentityDerivationMismatch,
    InvalidBoundedGraph,
    LegacyAuthorityMode,
    PendingSheetDigestMismatch,
    UntrustedConfirmationIssuer,
    UntrustedConfirmationObservation,
)
from .dispatch_types import load_dispatch_type_registry


IDENTITY_DERIVATION_DIGEST = (
    "sha256:e1d77f8e2e7eed4a94140d17ef05f10b227cba22727ed67d970244c8b910a3b5"
)
PAYLOAD_SCHEMA_BUNDLE_DIGEST = (
    "sha256:11e139bae3b1b6f8c9f21ac3d08f59f20828f61eb273604eb067b59ad53abe26"
)
PAYLOAD_SCHEMA_DIALECT_DIGEST = (
    "sha256:1fde625dc38238b2de389f1472ad993c580a076dcddf471e0066b54cc4a7ad26"
)
RUN_CREATED_SCHEMA_DIGEST = (
    "sha256:fcea3b5eb5942d744dc76fc9d8e0c36b9315063ae4fbcf9265dad1235985aacb"
)
AUDIT_OPENING_REQUESTED_SCHEMA_DIGEST = (
    "sha256:e5de962abcc0926d29858bc502c82af046c88a463726b55b45c6d8d02e5ca514"
)
AUDIT_OPENING_EFFECT_SCHEMA_DIGEST = (
    "sha256:bf3f56e03ca37db52ecd9049b36fa1a2c8e9af0af9c8d948f6f171e844fa6b98"
)
CONFIRMATION_RECEIPT_SCHEMA_DIGEST = (
    "sha256:996d5f440b8d2515484b6369d0f0b55c371bb6f3332940a284993479a12b2021"
)

SCHEMA_VERSIONS = {
    "command": "aci.confirm-runtime-dispatch-command@1",
    "event": "aci.runtime-event-envelope@1",
    "identity_derivation": "aci.confirmed-dispatch-id-preimage@1",
    "payload": "aci.runtime-confirmation-payloads@1",
    "recipe": "aci.author-reviewer-author@1",
}

_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
_MILLISECOND_UTC = re.compile(
    r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z$"
)
_KIND_PREFIX = {
    "run": "run_",
    "turn_graph": "graph_",
    "continuation": "cont_",
    "source_message": "msg_",
    "input_mapping": "map_",
    "effect": "effect_",
    "event": "event_",
    "receipt": "receipt_",
}


@dataclass(frozen=True)
class ConfirmationBatch:
    command: dict[str, Any]
    pending_sheet: dict[str, Any]
    dispatch_spec: dict[str, Any]
    observation: dict[str, Any]
    capability_resolution: dict[str, Any]
    graph: dict[str, Any]
    mapping_set: dict[str, Any]
    authority: dict[str, Any]
    effect_payload: dict[str, Any]
    run_created_payload: dict[str, Any]
    audit_opening_requested_payload: dict[str, Any]
    artifact_documents: tuple[tuple[str, str, bytes], ...]
    observation_record: dict[str, Any]
    confirmed_dispatch_record: dict[str, Any]
    run_record: dict[str, Any]
    graph_record: dict[str, Any]
    mapping_records: tuple[dict[str, Any], dict[str, Any]]
    effect_intent: dict[str, Any]
    next_state: dict[str, Any]
    receipt_id: str


def decode_confirmation_command(raw: bytes) -> dict[str, Any]:
    command = _decode(raw, error=ConfirmationProjectionMismatch)
    _fields(
        command,
        {
            "aggregate_id",
            "aggregate_type",
            "authority_context",
            "causation_id",
            "command_id",
            "correlation_id",
            "expected_version",
            "idempotency_key",
            "prerequisites",
            "scope_key",
            "semantic_intent",
        },
        ConfirmationProjectionMismatch,
        "confirmation command",
    )
    for name in (
        "aggregate_id",
        "aggregate_type",
        "causation_id",
        "command_id",
        "correlation_id",
        "idempotency_key",
        "scope_key",
    ):
        _string(command[name], ConfirmationProjectionMismatch, name)
    _integer(
        command["expected_version"],
        ConfirmationProjectionMismatch,
        "expected_version",
    )
    if (
        not isinstance(command["authority_context"], dict)
        or not isinstance(command["semantic_intent"], dict)
        or not isinstance(command["prerequisites"], list)
    ):
        raise ConfirmationProjectionMismatch("confirmation command object members are invalid")
    for index, prerequisite in enumerate(command["prerequisites"]):
        label = f"confirmation command prerequisite {index}"
        _fields(
            prerequisite,
            {"aggregate_id", "expected_version", "state_hash"},
            ConfirmationProjectionMismatch,
            label,
        )
        _string(
            prerequisite["aggregate_id"],
            ConfirmationProjectionMismatch,
            f"{label}.aggregate_id",
        )
        _integer(
            prerequisite["expected_version"],
            ConfirmationProjectionMismatch,
            f"{label}.expected_version",
        )
        _digest(
            prerequisite["state_hash"],
            ConfirmationProjectionMismatch,
            f"{label}.state_hash",
        )
    return command


def _decode(raw: bytes, *, error: type[Exception]) -> dict[str, Any]:
    try:
        value = parse_strict_json(raw)
        if not isinstance(value, dict) or canonical_bytes(value) != raw:
            raise error("document is not a canonical closed JSON object")
        return value
    except error:
        raise
    except Exception as exc:
        raise error("document is not valid canonical JSON") from exc


def _fields(value: Any, names: set[str], error: type[Exception], label: str) -> None:
    if not isinstance(value, dict) or set(value) != names:
        raise error(f"{label} has missing or unknown fields")


def _string(value: Any, error: type[Exception], label: str) -> str:
    if not isinstance(value, str) or not value:
        raise error(f"{label} must be a non-empty string")
    return value


def _digest(value: Any, error: type[Exception], label: str) -> str:
    if not isinstance(value, str) or _DIGEST.fullmatch(value) is None:
        raise error(f"{label} must be an algorithm-qualified digest")
    return value


def _integer(value: Any, error: type[Exception], label: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise error(f"{label} must be an integer >= {minimum}")
    return value


def _versioned_ref(value: Any, error: type[Exception], label: str) -> dict[str, Any]:
    _fields(value, {"name", "version", "digest"}, error, label)
    _string(value["name"], error, f"{label}.name")
    _string(value["version"], error, f"{label}.version")
    _digest(value["digest"], error, f"{label}.digest")
    return value


def artifact_id(digest: str) -> str:
    return "art_" + digest.removeprefix("sha256:")[:32]


def derive_id(
    kind: str,
    coordinates: list[str | int],
    *,
    dispatch_id: str,
    dispatch_spec_digest: str,
) -> str:
    try:
        prefix = _KIND_PREFIX[kind]
    except KeyError as exc:
        raise DerivedIdentityMismatch("unknown confirmed-dispatch identity kind") from exc
    encoded_coordinates = [str(value) for value in coordinates]
    preimage = {
        "coordinates": encoded_coordinates,
        "dispatch_id": dispatch_id,
        "dispatch_spec_digest": dispatch_spec_digest,
        "kind": kind,
        "schema": "aci.confirmed-dispatch-id-preimage@1",
    }
    return prefix + canonical_digest(preimage).removeprefix("sha256:")[:32]


def _validate_pending(pending: dict[str, Any]) -> None:
    _fields(
        pending,
        {
            "schema",
            "dispatch_id",
            "dispatch_revision",
            "execution_authority_mode",
            "recipe_ref",
            "schema_refs",
            "workflow",
            "decision_policy_refs",
            "prompt_snapshot_refs",
            "capability_requirements",
            "budgets",
        },
        InvalidBoundedGraph,
        "pending sheet",
    )
    if pending["schema"] != "aci.pending-runtime-dispatch@1":
        raise InvalidBoundedGraph("pending sheet schema is not admitted")
    _string(pending["dispatch_id"], InvalidBoundedGraph, "dispatch_id")
    _string(pending["dispatch_revision"], InvalidBoundedGraph, "dispatch_revision")
    if pending["execution_authority_mode"] != "runtime-managed":
        raise LegacyAuthorityMode("runtime confirmation rejects legacy-managed authority")
    recipe = _versioned_ref(pending["recipe_ref"], InvalidBoundedGraph, "recipe_ref")
    if recipe["name"] != "aci.author-reviewer-author" or recipe["version"] != "1":
        raise InvalidBoundedGraph("recipe is outside the bounded v1 projection")

    schema_refs = pending["schema_refs"]
    if not isinstance(schema_refs, list) or len(schema_refs) != 3:
        raise InvalidBoundedGraph("exactly three ordered schema refs are required")
    for index, ref in enumerate(schema_refs):
        _versioned_ref(ref, InvalidBoundedGraph, f"schema_refs[{index}]")
    if [ref["name"] for ref in schema_refs] != [
        "aci.author-output",
        "aci.reviewer-output",
        "aci.revision-instruction",
    ]:
        raise InvalidBoundedGraph("ordered schema refs are outside the bounded recipe")

    policy_refs = pending["decision_policy_refs"]
    _fields(policy_refs, {"reconstruction", "visibility"}, InvalidBoundedGraph, "policies")
    for name in ("reconstruction", "visibility"):
        _versioned_ref(policy_refs[name], InvalidBoundedGraph, f"policies.{name}")

    prompts = pending["prompt_snapshot_refs"]
    if not isinstance(prompts, list) or len(prompts) != 2:
        raise InvalidBoundedGraph("exactly two prompt snapshots are required")
    for prompt in prompts:
        _string(prompt, InvalidBoundedGraph, "prompt snapshot")

    requirements = pending["capability_requirements"]
    if not isinstance(requirements, list) or len(requirements) != 3:
        raise InvalidBoundedGraph("exactly three capability requirements are required")
    expected_capabilities = ["adapter.resume", "model.text", "tool.none"]
    for index, requirement in enumerate(requirements):
        _fields(requirement, {"capability_id", "required"}, InvalidBoundedGraph, "capability")
        if requirement != {"capability_id": expected_capabilities[index], "required": True}:
            raise InvalidBoundedGraph("capability requirement order/shape is invalid")

    budgets = pending["budgets"]
    _fields(
        budgets,
        {"max_attempts_per_turn", "max_total_turns", "wall_clock_seconds"},
        InvalidBoundedGraph,
        "budgets",
    )
    for name in budgets:
        _integer(budgets[name], InvalidBoundedGraph, f"budgets.{name}", minimum=1)

    workflow = pending["workflow"]
    _fields(workflow, {"nodes", "edges", "workflow_kind", "loop_ceiling"}, InvalidBoundedGraph, "workflow")
    expected_nodes = [
        {"group_id": "group_authoring", "operation_id": "author_turn_0", "role": "author", "round_id": "round_0", "seat_id": "seat_author", "turn_ordinal": 0},
        {"group_id": "group_review", "operation_id": "reviewer_turn_0", "role": "reviewer", "round_id": "round_0", "seat_id": "seat_reviewer", "turn_ordinal": 0},
        {"group_id": "group_authoring", "operation_id": "author_turn_1", "role": "author", "round_id": "round_1", "seat_id": "seat_author", "turn_ordinal": 1},
    ]
    expected_edges = [
        {"from_operation_id": "author_turn_0", "to_operation_id": "reviewer_turn_0"},
        {"from_operation_id": "reviewer_turn_0", "to_operation_id": "author_turn_1"},
    ]
    if (
        workflow["nodes"] != expected_nodes
        or workflow["edges"] != expected_edges
        or workflow["workflow_kind"] != "author-reviewer-author"
        or workflow["loop_ceiling"] != 1
    ):
        raise InvalidBoundedGraph("workflow must equal the admitted three-turn graph")


def _validate_resolution(resolution: dict[str, Any]) -> None:
    _fields(
        resolution,
        {"schema", "adapter_ref", "model_ref", "tool_profile_ref"},
        DispatchSpecDigestMismatch,
        "capability resolution",
    )
    if resolution["schema"] != "aci.capability-resolution@1":
        raise DispatchSpecDigestMismatch("capability resolution schema is invalid")
    for name in ("adapter_ref", "model_ref", "tool_profile_ref"):
        _versioned_ref(resolution[name], DispatchSpecDigestMismatch, name)


def project_dispatch_spec(pending: dict[str, Any], resolution: dict[str, Any]) -> dict[str, Any]:
    _validate_pending(pending)
    _validate_resolution(resolution)
    return {
        "budgets": pending["budgets"],
        "capability_resolution": resolution,
        "decision_policies": {
            "reconstruction": {
                "mode": "same_session_preferred",
                "policy_ref": pending["decision_policy_refs"]["reconstruction"],
            },
            "visibility": {
                "policy_ref": pending["decision_policy_refs"]["visibility"],
                "source_message_types": ["author.output", "reviewer.output"],
            },
        },
        "group_graph": {
            "edges": pending["workflow"]["edges"],
            "loop_ceiling": pending["workflow"]["loop_ceiling"],
            "nodes": pending["workflow"]["nodes"],
            "schema": "aci.logical-turn-graph@1",
            "workflow_kind": pending["workflow"]["workflow_kind"],
        },
        "prompt_snapshot_refs": pending["prompt_snapshot_refs"],
        "recipe_ref": pending["recipe_ref"],
        "schema": "aci.dispatch-spec@1",
        "schema_refs": pending["schema_refs"],
    }


def _validate_trust(
    trusted: dict[str, Any],
    observation: dict[str, Any],
    *,
    pending: dict[str, Any],
    pending_digest: str,
    spec_digest: str,
) -> None:
    _fields(
        trusted,
        {"schema", "admitted_issuer_ref", "authenticated_host_context", "observed_confirmation"},
        UntrustedConfirmationIssuer,
        "trusted issuer context",
    )
    if trusted["schema"] != "aci.trusted-confirmation-issuer-context@1":
        raise UntrustedConfirmationIssuer("trusted issuer context schema is invalid")
    _versioned_ref(trusted["admitted_issuer_ref"], UntrustedConfirmationIssuer, "admitted issuer")
    host = trusted["authenticated_host_context"]
    _fields(
        host,
        {"channel", "human_principal_id", "issuer_evidence_ref", "issuer_evidence_digest"},
        UntrustedConfirmationObservation,
        "host context",
    )
    if host["channel"] not in {"chat", "ui"}:
        raise UntrustedConfirmationObservation("confirmation channel is not admitted")
    _string(host["human_principal_id"], UntrustedConfirmationObservation, "human principal")
    _string(host["issuer_evidence_ref"], UntrustedConfirmationObservation, "issuer evidence ref")
    _digest(host["issuer_evidence_digest"], UntrustedConfirmationObservation, "issuer evidence digest")
    observed = trusted["observed_confirmation"]
    _fields(
        observed,
        {
            "action",
            "dispatch_id",
            "dispatch_revision",
            "observed_at",
            "presented_dispatch_spec_digest",
            "presented_pending_sheet_digest",
        },
        UntrustedConfirmationObservation,
        "observed confirmation",
    )
    if observed["action"] != "approve_runtime_dispatch" or _MILLISECOND_UTC.fullmatch(str(observed["observed_at"])) is None:
        raise UntrustedConfirmationObservation("confirmation action/time is invalid")
    if observed["dispatch_id"] != pending["dispatch_id"] or observed["dispatch_revision"] != pending["dispatch_revision"]:
        raise ConfirmationObservationScopeMismatch("observation scope differs from pending revision")
    if observed["presented_pending_sheet_digest"] != pending_digest:
        raise PendingSheetDigestMismatch("presented pending digest differs")
    if observed["presented_dispatch_spec_digest"] != spec_digest:
        raise DispatchSpecDigestMismatch("presented DispatchSpec digest differs")

    _fields(
        observation,
        {
            "schema",
            "observation_id",
            "issuer_ref",
            "issuer_evidence_ref",
            "issuer_evidence_digest",
            "human_principal_id",
            "channel",
            "observed_at",
            "dispatch_id",
            "dispatch_revision",
            "presented_pending_sheet_digest",
            "presented_dispatch_spec_digest",
            "action",
        },
        UntrustedConfirmationObservation,
        "confirmation observation",
    )
    if observation["schema"] != "aci.confirmation-observation@1":
        raise UntrustedConfirmationObservation("confirmation observation schema is invalid")
    _string(observation["observation_id"], UntrustedConfirmationObservation, "observation id")
    expected = {
        "action": observed["action"],
        "channel": host["channel"],
        "dispatch_id": observed["dispatch_id"],
        "dispatch_revision": observed["dispatch_revision"],
        "human_principal_id": host["human_principal_id"],
        "issuer_evidence_digest": host["issuer_evidence_digest"],
        "issuer_evidence_ref": host["issuer_evidence_ref"],
        "issuer_ref": trusted["admitted_issuer_ref"],
        "observed_at": observed["observed_at"],
        "presented_dispatch_spec_digest": observed["presented_dispatch_spec_digest"],
        "presented_pending_sheet_digest": observed["presented_pending_sheet_digest"],
    }
    if any(observation[name] != value for name, value in expected.items()):
        if observation["issuer_ref"] != trusted["admitted_issuer_ref"]:
            raise UntrustedConfirmationIssuer("confirmation issuer is not the admitted issuer")
        raise UntrustedConfirmationObservation("observation does not equal authenticated host evidence")


def _validate_derivation_contract(raw: bytes) -> None:
    value = _decode(raw, error=IdentityDerivationMismatch)
    if digest_bytes(raw) != IDENTITY_DERIVATION_DIGEST:
        raise IdentityDerivationMismatch("identity derivation contract digest differs")
    _fields(
        value,
        {"schema", "preimage_schema", "preimage_fields", "coordinates_encoding", "hash_algorithm", "output", "kinds"},
        IdentityDerivationMismatch,
        "identity derivation contract",
    )
    if value["schema"] != "aci.confirmed-dispatch-identity-derivation-contract@1":
        raise IdentityDerivationMismatch("identity derivation contract schema differs")


def _validate_payload_schemas(raw: bytes) -> None:
    value = _decode(raw, error=ConfirmationPayloadSchemaMismatch)
    if digest_bytes(raw) != PAYLOAD_SCHEMA_BUNDLE_DIGEST:
        raise ConfirmationPayloadSchemaMismatch("payload schema bundle digest differs")
    _fields(value, {"schema", "dialect", "members"}, ConfirmationPayloadSchemaMismatch, "payload schema bundle")
    if value["schema"] != "aci.runtime-confirmation-payload-schemas@1":
        raise ConfirmationPayloadSchemaMismatch("payload schema bundle schema differs")
    if canonical_digest(value["dialect"]) != PAYLOAD_SCHEMA_DIALECT_DIGEST:
        raise ConfirmationPayloadSchemaMismatch("payload schema dialect differs")
    expected = [
        ("aci.run-created@1", RUN_CREATED_SCHEMA_DIGEST),
        ("aci.audit-opening-requested@1", AUDIT_OPENING_REQUESTED_SCHEMA_DIGEST),
        ("aci.audit-opening-effect@1", AUDIT_OPENING_EFFECT_SCHEMA_DIGEST),
        ("aci.confirmed-dispatch-receipt@1", CONFIRMATION_RECEIPT_SCHEMA_DIGEST),
    ]
    members = value["members"]
    if not isinstance(members, list) or len(members) != len(expected):
        raise ConfirmationPayloadSchemaMismatch("payload schema member set differs")
    for member, (schema_ref, schema_digest) in zip(members, expected):
        _fields(member, {"schema_ref", "schema_digest", "definition"}, ConfirmationPayloadSchemaMismatch, "payload schema member")
        if (
            member["schema_ref"] != schema_ref
            or member["schema_digest"] != schema_digest
            or canonical_digest(member["definition"]) != schema_digest
        ):
            raise ConfirmationPayloadSchemaMismatch("payload schema member definition differs")


def _binding_digest(mapping: dict[str, Any]) -> str:
    return canonical_digest(
        {
            "schema": "aci.continuation-input-binding@1",
            **{
                name: mapping[name]
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
                    "visibility_policy_ref",
                )
            },
        }
    )


def build_confirmation_batch(
    *,
    repo_root: Path,
    pending_sheet_bytes: bytes,
    capability_resolution_bytes: bytes,
    capability_resolution_artifact_id: str,
    trusted_issuer_context_bytes: bytes,
    confirmation_observation_bytes: bytes,
    identity_derivation_bytes: bytes,
    payload_schema_bundle_bytes: bytes,
    command_bytes: bytes,
) -> ConfirmationBatch:
    dispatch_registry = load_dispatch_type_registry(repo_root)
    appender_contract_version = dispatch_registry["ledger_schema_version"]
    agent_role_registry_ref = dispatch_registry["agent_role_registry_ref"]
    pending = _decode(pending_sheet_bytes, error=InvalidBoundedGraph)
    _validate_pending(pending)
    pending_digest = digest_bytes(pending_sheet_bytes)
    resolution = _decode(capability_resolution_bytes, error=DispatchSpecDigestMismatch)
    dispatch_spec = project_dispatch_spec(pending, resolution)
    dispatch_spec_bytes = canonical_bytes(dispatch_spec)
    dispatch_spec_digest = digest_bytes(dispatch_spec_bytes)
    if capability_resolution_artifact_id != artifact_id(digest_bytes(capability_resolution_bytes)):
        raise DispatchSpecDigestMismatch("capability preview artifact identity differs")

    trusted = _decode(trusted_issuer_context_bytes, error=UntrustedConfirmationIssuer)
    observation = _decode(confirmation_observation_bytes, error=UntrustedConfirmationObservation)
    _validate_trust(
        trusted,
        observation,
        pending=pending,
        pending_digest=pending_digest,
        spec_digest=dispatch_spec_digest,
    )
    _validate_derivation_contract(identity_derivation_bytes)
    _validate_payload_schemas(payload_schema_bundle_bytes)

    dispatch_id = pending["dispatch_id"]
    run_id = derive_id("run", [], dispatch_id=dispatch_id, dispatch_spec_digest=dispatch_spec_digest)
    graph_id = derive_id("turn_graph", [], dispatch_id=dispatch_id, dispatch_spec_digest=dispatch_spec_digest)
    continuation_id = derive_id(
        "continuation",
        ["seat_author", 0, 1],
        dispatch_id=dispatch_id,
        dispatch_spec_digest=dispatch_spec_digest,
    )
    source_specs = [
        ("group_authoring", "seat_author", "author_turn_0", 0, "round_0", "author.output", "prior_author_output", 0),
        ("group_review", "seat_reviewer", "reviewer_turn_0", 0, "round_0", "reviewer.output", "review_feedback", 1),
    ]
    source_messages: list[dict[str, Any]] = []
    mappings: list[dict[str, Any]] = []
    for group, seat, operation, turn, round_id, message_type, slot_name, slot_ordinal in source_specs:
        message_id = derive_id(
            "source_message",
            [operation, round_id, message_type],
            dispatch_id=dispatch_id,
            dispatch_spec_digest=dispatch_spec_digest,
        )
        source_messages.append(
            {
                "group_id": group,
                "message_type": message_type,
                "operation_id": operation,
                "round_id": round_id,
                "seat_id": seat,
                "source_message_id": message_id,
                "turn_ordinal": turn,
            }
        )
        mapping = {
            "continuation_id": continuation_id,
            "dispatch_id": dispatch_id,
            "mapping_id": derive_id(
                "input_mapping",
                [slot_ordinal, operation, turn],
                dispatch_id=dispatch_id,
                dispatch_spec_digest=dispatch_spec_digest,
            ),
            "mapping_version": 1,
            "slot_name": slot_name,
            "slot_ordinal": slot_ordinal,
            "source_group_id": group,
            "source_message_id": message_id,
            "source_message_type": message_type,
            "source_operation_id": operation,
            "source_round_id": round_id,
            "source_seat_id": seat,
            "source_turn_ordinal": turn,
            "target_seat_id": "seat_author",
            "target_turn_ordinal": 1,
            "visibility_policy_ref": pending["decision_policy_refs"]["visibility"],
        }
        mapping["confirmed_binding_digest"] = _binding_digest(mapping)
        mappings.append(mapping)

    graph = {
        "continuation_bindings": [
            {
                "continuation_id": continuation_id,
                "source_operation_id": "author_turn_0",
                "source_seat_id": "seat_author",
                "source_turn_ordinal": 0,
                "target_operation_id": "author_turn_1",
                "target_seat_id": "seat_author",
                "target_turn_ordinal": 1,
            }
        ],
        "dispatch_id": dispatch_id,
        "dispatch_spec_digest": dispatch_spec_digest,
        "edges": pending["workflow"]["edges"],
        "graph_id": graph_id,
        "nodes": pending["workflow"]["nodes"],
        "schema": "aci.confirmed-turn-graph@1",
        "source_messages": source_messages,
    }
    graph_bytes = canonical_bytes(graph)
    graph_digest = digest_bytes(graph_bytes)
    mapping_set = {"mappings": mappings, "schema": "aci.continuation-input-mapping-set@1"}
    mapping_set_bytes = canonical_bytes(mapping_set)
    mapping_set_digest = digest_bytes(mapping_set_bytes)
    observation_digest = digest_bytes(confirmation_observation_bytes)
    capability_digest = digest_bytes(capability_resolution_bytes)
    authority = {
        "capability_resolution_digest": capability_digest,
        "confirmation_observation_digest": observation_digest,
        "confirmed_turn_graph_digest": graph_digest,
        "derivation_schema": "aci.confirmed-dispatch-id-preimage@1",
        "dispatch_id": dispatch_id,
        "dispatch_revision": pending["dispatch_revision"],
        "dispatch_spec_digest": dispatch_spec_digest,
        "execution_authority_mode": "runtime-managed",
        "identity_derivation_digest": IDENTITY_DERIVATION_DIGEST,
        "mapping_set_digest": mapping_set_digest,
        "payload_schema_bundle_digest": PAYLOAD_SCHEMA_BUNDLE_DIGEST,
        "pending_sheet_digest": pending_digest,
        "schema": "aci.confirmed-authority@1",
        "schema_versions": SCHEMA_VERSIONS,
    }
    authority_bytes = canonical_bytes(authority)
    authority_digest = digest_bytes(authority_bytes)

    effect_id = derive_id("effect", ["audit_opening"], dispatch_id=dispatch_id, dispatch_spec_digest=dispatch_spec_digest)
    run_event_id = derive_id("event", ["run.created", 1], dispatch_id=dispatch_id, dispatch_spec_digest=dispatch_spec_digest)
    audit_event_id = derive_id("event", ["audit_opening.requested", 2], dispatch_id=dispatch_id, dispatch_spec_digest=dispatch_spec_digest)
    receipt_id = derive_id("receipt", ["confirmation"], dispatch_id=dispatch_id, dispatch_spec_digest=dispatch_spec_digest)
    authority_ref = artifact_id(authority_digest)
    effect_payload = {
        "agent_role_registry_ref": agent_role_registry_ref,
        "appender_contract_version": appender_contract_version,
        "confirmed_authority_digest": authority_digest,
        "confirmed_authority_ref": authority_ref,
        "dispatch_id": dispatch_id,
        "run_id": run_id,
        "schema": "aci.audit-opening-effect@1",
    }
    effect_payload_bytes = canonical_bytes(effect_payload)
    effect_payload_digest = digest_bytes(effect_payload_bytes)
    effect_payload_ref = artifact_id(effect_payload_digest)
    run_created_payload = {
        "capability_resolution_digest": capability_digest,
        "capability_resolution_ref": capability_resolution_artifact_id,
        "confirmation_observation_digest": observation_digest,
        "confirmation_observation_ref": artifact_id(observation_digest),
        "confirmed_at": observation["observed_at"],
        "confirmed_authority_digest": authority_digest,
        "confirmed_authority_ref": authority_ref,
        "confirmed_by": observation["human_principal_id"],
        "confirmed_turn_graph_digest": graph_digest,
        "confirmed_turn_graph_ref": artifact_id(graph_digest),
        "continuation_id": continuation_id,
        "continuation_mapping_set_digest": mapping_set_digest,
        "continuation_mapping_set_ref": artifact_id(mapping_set_digest),
        "dispatch_id": dispatch_id,
        "dispatch_revision": pending["dispatch_revision"],
        "dispatch_spec_digest": dispatch_spec_digest,
        "dispatch_spec_ref": artifact_id(dispatch_spec_digest),
        "execution_authority_mode": "runtime-managed",
        "graph_id": graph_id,
        "identity_derivation_digest": IDENTITY_DERIVATION_DIGEST,
        "identity_derivation_ref": {
            "digest": IDENTITY_DERIVATION_DIGEST,
            "name": "aci.confirmed-dispatch-identity-derivation-contract",
            "version": "1",
        },
        "mapping_ids": [mapping["mapping_id"] for mapping in mappings],
        "payload_schema_bundle_digest": PAYLOAD_SCHEMA_BUNDLE_DIGEST,
        "pending_sheet_digest": pending_digest,
        "pending_sheet_ref": artifact_id(pending_digest),
        "run_id": run_id,
        "schema": "aci.run-created@1",
        "schema_versions": SCHEMA_VERSIONS,
        "source_message_ids": [message["source_message_id"] for message in source_messages],
    }
    run_payload_bytes = canonical_bytes(run_created_payload)
    run_payload_digest = digest_bytes(run_payload_bytes)
    audit_payload = {
        "agent_role_registry_ref": agent_role_registry_ref,
        "appender_contract_version": appender_contract_version,
        "confirmed_authority_digest": authority_digest,
        "confirmed_authority_ref": authority_ref,
        "dispatch_id": dispatch_id,
        "effect_id": effect_id,
        "effect_payload_digest": effect_payload_digest,
        "effect_payload_ref": effect_payload_ref,
        "effect_type": "audit_opening",
        "run_id": run_id,
        "schema": "aci.audit-opening-requested@1",
    }
    audit_payload_bytes = canonical_bytes(audit_payload)

    command = decode_confirmation_command(command_bytes)
    _validate_command(
        command,
        run_id=run_id,
        observation=observation,
        observation_digest=observation_digest,
        pending=pending,
        pending_digest=pending_digest,
        dispatch_spec_digest=dispatch_spec_digest,
        capability_digest=capability_digest,
        authority_digest=authority_digest,
    )
    next_state = {
        "dispatch_id": dispatch_id,
        "opening_state": "pending",
        "run_id": run_id,
        "state": "opening_pending",
    }
    state_hash = canonical_digest(next_state)
    observation_record = {
        **observation,
        "issuer_ref_json": canonical_text(observation["issuer_ref"]),
        "observation_artifact_id": artifact_id(observation_digest),
        "observation_digest": observation_digest,
    }
    confirmed_dispatch_record = {
        "dispatch_id": dispatch_id,
        "dispatch_revision": pending["dispatch_revision"],
        "pending_sheet_artifact_id": artifact_id(pending_digest),
        "pending_sheet_digest": pending_digest,
        "dispatch_spec_artifact_id": artifact_id(dispatch_spec_digest),
        "dispatch_spec_digest": dispatch_spec_digest,
        "confirmation_observation_artifact_id": artifact_id(observation_digest),
        "confirmation_observation_digest": observation_digest,
        "capability_resolution_artifact_id": capability_resolution_artifact_id,
        "capability_resolution_digest": capability_digest,
        "confirmed_turn_graph_artifact_id": artifact_id(graph_digest),
        "confirmed_turn_graph_digest": graph_digest,
        "continuation_mapping_set_artifact_id": artifact_id(mapping_set_digest),
        "continuation_mapping_set_digest": mapping_set_digest,
        "confirmed_authority_artifact_id": authority_ref,
        "confirmed_authority_digest": authority_digest,
        "execution_authority_mode": "runtime-managed",
        "confirmed_by": observation["human_principal_id"],
        "confirmed_at": observation["observed_at"],
        "accepted_command_id": command["command_id"],
    }
    run_record = {
        "run_id": run_id,
        "dispatch_id": dispatch_id,
        "dispatch_spec_digest": dispatch_spec_digest,
        "aggregate_version": 2,
        "state": "opening_pending",
        "state_hash": state_hash,
        "opening_state": "pending",
        "terminal_event_id": None,
    }
    binding = graph["continuation_bindings"][0]
    graph_record = {
        "graph_id": graph_id,
        "dispatch_id": dispatch_id,
        "run_id": run_id,
        "dispatch_spec_digest": dispatch_spec_digest,
        "graph_artifact_id": artifact_id(graph_digest),
        "graph_digest": graph_digest,
        "continuation_id": continuation_id,
        "mapping_set_artifact_id": artifact_id(mapping_set_digest),
        "mapping_set_digest": mapping_set_digest,
        "node_count": 3,
        "edge_count": 2,
        "mapping_count": 2,
        "nodes_json": canonical_text(graph["nodes"]),
        "edges_json": canonical_text(graph["edges"]),
        "source_messages_json": canonical_text(source_messages),
        **binding,
        "identity_derivation_ref_json": canonical_text(run_created_payload["identity_derivation_ref"]),
    }
    effect_intent = {
        "effect_id": effect_id,
        "command_id": command["command_id"],
        "requested_event_id": audit_event_id,
        "effect_type": "audit_opening",
        "payload_ref": effect_payload_ref,
        "payload_digest": effect_payload_digest,
        "retry_class": "retryable",
        "status": "pending",
        "claim_epoch": None,
        "claimed_by": None,
        "attempt_count": 0,
        "outcome_event_id": None,
        "outcome_digest": None,
    }
    artifacts = (
        ("pending", "aci.pending-runtime-dispatch@1", pending_sheet_bytes),
        ("dispatch_spec", "aci.dispatch-spec@1", dispatch_spec_bytes),
        ("observation", "aci.confirmation-observation@1", confirmation_observation_bytes),
        ("graph", "aci.confirmed-turn-graph@1", graph_bytes),
        ("mapping_set", "aci.continuation-input-mapping-set@1", mapping_set_bytes),
        ("authority", "aci.confirmed-authority@1", authority_bytes),
        ("audit_opening_effect_payload", "aci.audit-opening-effect@1", effect_payload_bytes),
        ("run_created_payload", "aci.run-created@1", run_payload_bytes),
        ("audit_opening_requested_payload", "aci.audit-opening-requested@1", audit_payload_bytes),
    )
    return ConfirmationBatch(
        command=command,
        pending_sheet=pending,
        dispatch_spec=dispatch_spec,
        observation=observation,
        capability_resolution=resolution,
        graph=graph,
        mapping_set=mapping_set,
        authority=authority,
        effect_payload=effect_payload,
        run_created_payload=run_created_payload,
        audit_opening_requested_payload=audit_payload,
        artifact_documents=artifacts,
        observation_record=observation_record,
        confirmed_dispatch_record=confirmed_dispatch_record,
        run_record=run_record,
        graph_record=graph_record,
        mapping_records=(mappings[0], mappings[1]),
        effect_intent=effect_intent,
        next_state=next_state,
        receipt_id=receipt_id,
    )


def _validate_command(
    command: dict[str, Any],
    *,
    run_id: str,
    observation: dict[str, Any],
    observation_digest: str,
    pending: dict[str, Any],
    pending_digest: str,
    dispatch_spec_digest: str,
    capability_digest: str,
    authority_digest: str,
) -> None:
    _fields(
        command,
        {
            "aggregate_id",
            "aggregate_type",
            "authority_context",
            "causation_id",
            "command_id",
            "correlation_id",
            "expected_version",
            "idempotency_key",
            "prerequisites",
            "scope_key",
            "semantic_intent",
        },
        ConfirmationProjectionMismatch,
        "confirmation command",
    )
    for name in ("command_id", "idempotency_key"):
        _string(command[name], ConfirmationProjectionMismatch, name)
    expected_authority = {
        "confirmation_observation_digest": observation_digest,
        "human_principal_id": observation["human_principal_id"],
        "issuer_ref": observation["issuer_ref"],
        "schema": "aci.confirmation-authority-context@1",
    }
    expected_intent = {
        "capability_resolution_digest": capability_digest,
        "confirmation_observation_digest": observation_digest,
        "confirmed_authority_digest": authority_digest,
        "dispatch_id": pending["dispatch_id"],
        "dispatch_revision": pending["dispatch_revision"],
        "dispatch_spec_digest": dispatch_spec_digest,
        "execution_authority_mode": "runtime-managed",
        "pending_sheet_digest": pending_digest,
        "schema": "aci.confirm-runtime-dispatch-intent@1",
    }
    if (
        command["aggregate_id"] != run_id
        or command["aggregate_type"] != "run"
        or command["authority_context"] != expected_authority
        or command["causation_id"] != observation["observation_id"]
        or command["correlation_id"] != pending["dispatch_id"]
        or command["expected_version"] != 0
        or command["prerequisites"] != []
        or command["scope_key"] != f"confirm-runtime-dispatch:{pending['dispatch_id']}"
        or command["semantic_intent"] != expected_intent
    ):
        raise ConfirmationProjectionMismatch("confirmation command is not bound to derived authority")


def require_derived_document(
    actual: dict[str, Any],
    expected: dict[str, Any],
    *,
    identity_fields: set[str] = frozenset(),
) -> None:
    if actual == expected:
        return
    def member(value: Any, path: str) -> Any:
        current = value
        for part in path.split("."):
            current = current[int(part)] if isinstance(current, list) else current.get(part)
        return current

    if any(member(actual, name) != member(expected, name) for name in identity_fields):
        raise DerivedIdentityMismatch("caller-supplied derived identity differs")
    raise ConfirmationProjectionMismatch("caller-supplied derived projection differs")


def require_authority_document(
    actual: dict[str, Any], expected: dict[str, Any]
) -> None:
    if actual == expected:
        return
    if actual.get("schema_versions") != expected.get("schema_versions"):
        raise ConfirmationSchemaVersionsMismatch(
            "confirmed authority schema version map differs"
        )
    raise ConfirmationProjectionMismatch("confirmed authority envelope differs")


def require_effect_ceiling(
    actual: list[dict[str, Any]], expected: dict[str, Any]
) -> None:
    if actual != [expected]:
        raise ForbiddenEffectBoundary(
            "confirmation permits exactly one pending audit-opening intent"
        )
