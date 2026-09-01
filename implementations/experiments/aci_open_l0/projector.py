"""Pure, non-authoritative 0.6.4-shaped audit-opening projection.

This experiment deliberately has no writer or production-runtime dependency.  Its
outputs are hypothesis bytes; they cannot authorize append, OPEN, or execution.
"""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from typing import Any


class ProjectionError(ValueError):
    """The synthetic candidate is outside the closed L0 experiment."""


_TOP_KEYS = {
    "schema",
    "authority",
    "non_authoritative",
    "route_label",
    "dispatch_id",
    "dispatch_type",
    "goal",
    "context",
    "max_loops",
    "final_approver",
    "anti_bias_mode",
    "output_mode",
    "invoked_by",
    "role_mapping",
    "candidate_route",
    "operations",
    "audit_groups",
    "connections",
}
_ROUTE_KEYS = {
    "schema",
    "registry_schema",
    "registry_digest",
    "dispatch_type_ref",
    "ledger_dispatch_type",
    "capability_ref",
    "capability_path",
    "capability_digest",
    "execution_authority_mode",
    "tool_profile_ref",
    "route_digest",
}
_OP_KEYS = {
    "operation_id",
    "logical_group_id",
    "seat_id",
    "runtime_role",
    "turn_ordinal",
    "audit_group_id",
    "model",
    "token_budget",
    "initial_prompt",
}
_CONNECTION_KEYS = {"from_operation_id", "to_operation_id"}
_LEGACY_ROLES = {
    "explorer",
    "synthesizer",
    "skeptic",
    "writer",
    "auditor",
    "planner",
    "coder",
}
_SHA256 = re.compile(r"sha256:[0-9a-f]{64}\Z")
_EXPECTED_OPERATIONS = (
    ("author_turn_0", "group_authoring", "seat_author", "author", 0, "audit_author_turn_0"),
    ("reviewer_turn_0", "group_review", "seat_reviewer", "reviewer", 0, "audit_reviewer_turn_0"),
    ("author_turn_1", "group_authoring", "seat_author", "author", 1, "audit_author_turn_1"),
)
_EXPECTED_CONNECTIONS = (
    ("author_turn_0", "reviewer_turn_0"),
    ("reviewer_turn_0", "author_turn_1"),
)


def _normalized(value: Any) -> Any:
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    if isinstance(value, list):
        return [_normalized(item) for item in value]
    if isinstance(value, dict):
        return {key: _normalized(item) for key, item in value.items()}
    return value


def canonical_bytes(value: Any) -> bytes:
    """Return canonical UTF-8 JSON bytes with no trailing newline."""

    return json.dumps(
        _normalized(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def digest_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def _exact_keys(value: Any, expected: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or isinstance(value, bool):
        raise ProjectionError(f"{label} must be an object")
    actual = set(value)
    if actual != expected:
        raise ProjectionError(
            f"{label} keys differ: missing={sorted(expected - actual)!r} "
            f"extra={sorted(actual - expected)!r}"
        )
    return value


def _nonempty_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ProjectionError(f"{label} must be a non-empty explicit string")
    return unicodedata.normalize("NFC", value)


def _synthetic_text(value: Any, label: str) -> str:
    text = _nonempty_text(value, label)
    if "synthetic" not in text.casefold():
        raise ProjectionError(f"{label} must be visibly synthetic")
    return text


def _validated_route(raw: Any) -> dict[str, Any]:
    route = _exact_keys(raw, _ROUTE_KEYS, "candidate_route")
    for key in _ROUTE_KEYS:
        _nonempty_text(route[key], f"candidate_route.{key}")
    for key in ("registry_digest", "capability_digest", "route_digest"):
        if not _SHA256.fullmatch(route[key]):
            raise ProjectionError(f"candidate_route.{key} must be lowercase sha256")
    required = {
        "schema": "aci-capability-route/v1",
        "registry_schema": "aci-dispatch-type-registry/v1",
        "dispatch_type_ref": "review",
        "ledger_dispatch_type": "review",
        "execution_authority_mode": "legacy-managed",
    }
    for key, expected in required.items():
        if route[key] != expected:
            raise ProjectionError(f"candidate_route.{key} must be {expected!r}")
    body = {key: value for key, value in route.items() if key != "route_digest"}
    if route["route_digest"] != digest_bytes(canonical_bytes(body)):
        raise ProjectionError("candidate_route.route_digest does not bind its route body")
    return _normalized(route)


def _validate_candidate(candidate: Any) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    source = _exact_keys(candidate, _TOP_KEYS, "input")
    constants = {
        "schema": "aci.open-l0.synthetic-input@1",
        "authority": "none",
        "non_authoritative": True,
        "route_label": "candidate",
        "dispatch_type": "review",
        "max_loops": 1,
        "anti_bias_mode": "disabled",
        "output_mode": "inline",
        "invoked_by": "synthetic@example.invalid",
    }
    for key, expected in constants.items():
        if source[key] != expected or isinstance(source[key], bool) != isinstance(expected, bool):
            raise ProjectionError(f"input.{key} must be {expected!r}")
    for key in ("dispatch_id", "goal", "context", "final_approver"):
        _synthetic_text(source[key], f"input.{key}")
    invoked_by = _nonempty_text(source["invoked_by"], "input.invoked_by")
    if "@" not in invoked_by or invoked_by.casefold() in {"ambient", "git", "auto"}:
        raise ProjectionError("input.invoked_by must be explicit, not ambient")

    mapping = _exact_keys(source["role_mapping"], {"author", "reviewer"}, "role_mapping")
    for runtime_role in ("author", "reviewer"):
        legacy_role = mapping[runtime_role]
        if legacy_role not in _LEGACY_ROLES or legacy_role in {"author", "reviewer"}:
            raise ProjectionError(f"role_mapping.{runtime_role} must be a legacy role")
    if mapping["author"] == mapping["reviewer"]:
        raise ProjectionError("candidate role mappings must remain distinct")

    route = _validated_route(source["candidate_route"])
    if source["audit_groups"] != [item[5] for item in _EXPECTED_OPERATIONS]:
        raise ProjectionError("audit_groups must preserve exact operation-scoped group order")
    operations = source["operations"]
    if not isinstance(operations, list) or len(operations) != 3:
        raise ProjectionError("operations must contain exactly three ordered entries")
    audit_ids: set[str] = set()
    normalized_operations: list[dict[str, Any]] = []
    for index, expected in enumerate(_EXPECTED_OPERATIONS):
        operation = _exact_keys(operations[index], _OP_KEYS, f"operations[{index}]")
        actual_identity = tuple(
            operation[key]
            for key in (
                "operation_id",
                "logical_group_id",
                "seat_id",
                "runtime_role",
                "turn_ordinal",
                "audit_group_id",
            )
        )
        if actual_identity != expected:
            raise ProjectionError(f"operations[{index}] identity/order differs")
        if operation["audit_group_id"] in audit_ids:
            raise ProjectionError("audit group ids must be unique")
        audit_ids.add(operation["audit_group_id"])
        _synthetic_text(operation["model"], f"operations[{index}].model")
        _synthetic_text(operation["initial_prompt"], f"operations[{index}].initial_prompt")
        budget = operation["token_budget"]
        if isinstance(budget, bool) or not isinstance(budget, int) or budget <= 0:
            raise ProjectionError(f"operations[{index}].token_budget must be a positive integer")
        normalized_operations.append(_normalized(operation))

    connections = source["connections"]
    if not isinstance(connections, list) or len(connections) != 2:
        raise ProjectionError("connections must contain exactly two ordered entries")
    for index, expected in enumerate(_EXPECTED_CONNECTIONS):
        connection = _exact_keys(connections[index], _CONNECTION_KEYS, f"connections[{index}]")
        actual = (connection["from_operation_id"], connection["to_operation_id"])
        if actual != expected:
            raise ProjectionError(f"connections[{index}] identity/order differs")
    normalized = _normalized(source)
    normalized["candidate_route"] = route
    normalized["operations"] = normalized_operations
    return normalized, normalized_operations


def _documents(candidate: Any) -> dict[str, Any]:
    source, operations = _validate_candidate(candidate)
    mapping = source["role_mapping"]
    groups = []
    bindings = []
    for operation in operations:
        groups.append(
            {
                "group_id": operation["audit_group_id"],
                "agents": [
                    {
                        "role": mapping[operation["runtime_role"]],
                        "model": operation["model"],
                        "token_budget": operation["token_budget"],
                        "initial_prompt": operation["initial_prompt"],
                    }
                ],
                "n": 1,
                "robot_talks": False,
                "layers": 1,
            }
        )
        bindings.append(
            {
                "operation_id": operation["operation_id"],
                "runtime_role": operation["runtime_role"],
                "legacy_role": mapping[operation["runtime_role"]],
                "logical_group_id": operation["logical_group_id"],
                "audit_group_id": operation["audit_group_id"],
                "seat_id": operation["seat_id"],
                "turn_ordinal": operation["turn_ordinal"],
            }
        )

    row = {
        "dispatch_id": source["dispatch_id"],
        "schema_version": "0.6.4",
        "invoked_by": source["invoked_by"],
        "dispatch_type": source["dispatch_type"],
        "goal": source["goal"],
        "context": source["context"],
        "max_loops": source["max_loops"],
        "final_approver": source["final_approver"],
        "anti_bias_mode": source["anti_bias_mode"],
        "output_mode": source["output_mode"],
        "capability_route": source["candidate_route"],
        "groups": groups,
        "connections": [
            {
                "from": operations[index]["audit_group_id"],
                "to": operations[index + 1]["audit_group_id"],
                "type": "sequential",
            }
            for index in range(2)
        ],
    }
    binding_document = {
        "schema": "aci.open-l0.operation-bindings@1",
        "authority": "none",
        "non_authoritative": True,
        "route_label": "candidate",
        "bindings": bindings,
    }
    report = {
        "schema": "aci.open-l0.discrepancy-report@1",
        "authority": "none",
        "non_authoritative": True,
        "candidate_route_digest": source["candidate_route"]["route_digest"],
        "preserved": [
            "canonical dispatch envelope fields",
            "three-operation order through unique audit groups and ordered bindings",
            "candidate route bytes and digest",
        ],
        "discrepancies": [
            {
                "id": "authority-mode",
                "preserved": False,
                "witness": "runtime-managed confirmation is not legacy-managed launch authority",
            },
            {
                "id": "role-vocabulary",
                "preserved": False,
                "witness": "runtime author/reviewer are substituted by candidate legacy roles",
            },
            {
                "id": "logical-group-reuse",
                "preserved": False,
                "witness": "group_authoring becomes two unique operation-scoped audit groups",
            },
            {
                "id": "shared-seat-session",
                "preserved": False,
                "witness": "both author turns name seat_author but 0.6.4 has no Seat/session field",
            },
            {
                "id": "continuation-key",
                "preserved": False,
                "witness": "0.6.4 carries no continuation identity between author turns",
            },
            {
                "id": "reviewer-interposition",
                "preserved": False,
                "witness": "layers=2 repeats one group and cannot encode author-reviewer-author",
            },
        ],
    }
    return {
        "unstamped_row": row,
        "operation_bindings": binding_document,
        "discrepancy_report": report,
    }


def project(candidate: Any) -> dict[str, Any]:
    """Validate and project one closed synthetic candidate without side effects."""

    documents = _documents(candidate)
    encoded = {name: canonical_bytes(value) for name, value in documents.items()}
    digests = {name: digest_bytes(value) for name, value in encoded.items()}
    projection_digest = digest_bytes(canonical_bytes(digests))
    return {
        "documents": documents,
        "bytes": encoded,
        "digests": digests,
        "projection_digest": projection_digest,
        "authority": "none",
        "non_authoritative": True,
    }
