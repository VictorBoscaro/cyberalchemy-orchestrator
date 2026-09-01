"""Structurally independent pure comparator for the ACI OPEN-L0 experiment."""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from typing import Any


class OracleRejection(ValueError):
    pass


def _freeze_json(item: Any) -> bytes:
    def nfc(node: Any) -> Any:
        if type(node) is str:
            return unicodedata.normalize("NFC", node)
        if type(node) is list:
            return [nfc(part) for part in node]
        if type(node) is dict:
            return {name: nfc(part) for name, part in node.items()}
        return node

    return json.dumps(nfc(item), ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode()


def _hash(payload: bytes) -> str:
    return f"sha256:{hashlib.sha256(payload).hexdigest()}"


def compare(candidate: Any) -> dict[str, Any]:
    """Reproduce the three documents without importing projector code or helpers."""

    if type(candidate) is not dict:
        raise OracleRejection("closed candidate must be an object")
    top = [
        "schema", "authority", "non_authoritative", "route_label", "dispatch_id",
        "dispatch_type", "goal", "context", "max_loops", "final_approver",
        "anti_bias_mode", "output_mode", "invoked_by", "role_mapping",
        "candidate_route", "operations", "audit_groups", "connections",
    ]
    if sorted(candidate) != sorted(top):
        raise OracleRejection("closed candidate field set differs")
    fixed = (
        ("schema", "aci.open-l0.synthetic-input@1"),
        ("authority", "none"),
        ("non_authoritative", True),
        ("route_label", "candidate"),
        ("dispatch_type", "review"),
        ("max_loops", 1),
        ("anti_bias_mode", "disabled"),
        ("output_mode", "inline"),
        ("invoked_by", "synthetic@example.invalid"),
    )
    if any(candidate[name] != value or type(candidate[name]) is not type(value) for name, value in fixed):
        raise OracleRejection("fixed experimental value differs")
    if any(type(candidate[name]) is not str or not candidate[name].strip() or "synthetic" not in candidate[name].casefold()
           for name in ("dispatch_id", "goal", "context", "final_approver")):
        raise OracleRejection("identity and envelope strings must be visibly synthetic")
    if type(candidate["invoked_by"]) is not str or "@" not in candidate["invoked_by"]:
        raise OracleRejection("invoked_by is not explicit")

    roles = candidate["role_mapping"]
    allowed = {"explorer", "synthesizer", "skeptic", "writer", "auditor", "planner", "coder"}
    if type(roles) is not dict or set(roles) != {"author", "reviewer"}:
        raise OracleRejection("role mapping shape differs")
    if roles["author"] not in allowed or roles["reviewer"] not in allowed or roles["author"] == roles["reviewer"]:
        raise OracleRejection("role mapping is not a distinct legacy substitution")

    route = candidate["candidate_route"]
    route_names = {
        "schema", "registry_schema", "registry_digest", "dispatch_type_ref",
        "ledger_dispatch_type", "capability_ref", "capability_path", "capability_digest",
        "execution_authority_mode", "tool_profile_ref", "route_digest",
    }
    if type(route) is not dict or set(route) != route_names:
        raise OracleRejection("route shape differs")
    if any(type(route[name]) is not str or not route[name].strip() for name in route_names):
        raise OracleRejection("route strings must be explicit")
    if (route["schema"], route["registry_schema"], route["dispatch_type_ref"],
        route["ledger_dispatch_type"], route["execution_authority_mode"]) != (
            "aci-capability-route/v1", "aci-dispatch-type-registry/v1", "review", "review", "legacy-managed"
        ):
        raise OracleRejection("route mechanics differ")
    sha = re.compile(r"sha256:[0-9a-f]{64}\Z")
    if any(sha.fullmatch(route[name]) is None for name in ("registry_digest", "capability_digest", "route_digest")):
        raise OracleRejection("route digest shape differs")
    route_body = dict(route)
    claimed_route_hash = route_body.pop("route_digest")
    if claimed_route_hash != _hash(_freeze_json(route_body)):
        raise OracleRejection("route body digest mismatch")

    operations = candidate["operations"]
    identities = [
        ("author_turn_0", "group_authoring", "seat_author", "author", 0, "audit_author_turn_0"),
        ("reviewer_turn_0", "group_review", "seat_reviewer", "reviewer", 0, "audit_reviewer_turn_0"),
        ("author_turn_1", "group_authoring", "seat_author", "author", 1, "audit_author_turn_1"),
    ]
    if candidate["audit_groups"] != [identity[5] for identity in identities]:
        raise OracleRejection("audit group ordering differs")
    op_names = {
        "operation_id", "logical_group_id", "seat_id", "runtime_role", "turn_ordinal",
        "audit_group_id", "model", "token_budget", "initial_prompt",
    }
    if type(operations) is not list or len(operations) != 3:
        raise OracleRejection("operation cardinality differs")
    for position, op in enumerate(operations):
        if type(op) is not dict or set(op) != op_names:
            raise OracleRejection("operation shape differs")
        observed = tuple(op[name] for name in (
            "operation_id", "logical_group_id", "seat_id", "runtime_role", "turn_ordinal", "audit_group_id"
        ))
        if observed != identities[position]:
            raise OracleRejection("operation identity or ordering differs")
        if type(op["model"]) is not str or "synthetic" not in op["model"].casefold():
            raise OracleRejection("model is not visibly synthetic")
        if type(op["initial_prompt"]) is not str or "synthetic" not in op["initial_prompt"].casefold():
            raise OracleRejection("prompt is not visibly synthetic")
        if type(op["token_budget"]) is not int or op["token_budget"] <= 0:
            raise OracleRejection("budget is not a positive integer")
    if len({op["audit_group_id"] for op in operations}) != 3:
        raise OracleRejection("audit groups are not unique")

    links = candidate["connections"]
    expected_links = [("author_turn_0", "reviewer_turn_0"), ("reviewer_turn_0", "author_turn_1")]
    if type(links) is not list or len(links) != 2:
        raise OracleRejection("connection cardinality differs")
    for position, link in enumerate(links):
        if type(link) is not dict or set(link) != {"from_operation_id", "to_operation_id"}:
            raise OracleRejection("connection shape differs")
        if (link["from_operation_id"], link["to_operation_id"]) != expected_links[position]:
            raise OracleRejection("connection identity or ordering differs")

    projected_groups = []
    mapped_operations = []
    for op in operations:
        legacy = roles[op["runtime_role"]]
        projected_groups += [{
            "group_id": op["audit_group_id"],
            "agents": [{
                "role": legacy,
                "model": op["model"],
                "token_budget": op["token_budget"],
                "initial_prompt": op["initial_prompt"],
            }],
            "n": 1,
            "robot_talks": False,
            "layers": 1,
        }]
        mapped_operations += [{
            "operation_id": op["operation_id"],
            "runtime_role": op["runtime_role"],
            "legacy_role": legacy,
            "logical_group_id": op["logical_group_id"],
            "audit_group_id": op["audit_group_id"],
            "seat_id": op["seat_id"],
            "turn_ordinal": op["turn_ordinal"],
        }]

    row = {
        "dispatch_id": candidate["dispatch_id"], "schema_version": "0.6.4",
        "invoked_by": candidate["invoked_by"], "dispatch_type": "review",
        "goal": candidate["goal"], "context": candidate["context"], "max_loops": 1,
        "final_approver": candidate["final_approver"], "anti_bias_mode": "disabled",
        "output_mode": "inline", "capability_route": route, "groups": projected_groups,
        "connections": [
            {"from": operations[0]["audit_group_id"], "to": operations[1]["audit_group_id"], "type": "sequential"},
            {"from": operations[1]["audit_group_id"], "to": operations[2]["audit_group_id"], "type": "sequential"},
        ],
    }
    binding_doc = {
        "schema": "aci.open-l0.operation-bindings@1", "authority": "none",
        "non_authoritative": True, "route_label": "candidate", "bindings": mapped_operations,
    }
    gap_doc = {
        "schema": "aci.open-l0.discrepancy-report@1", "authority": "none",
        "non_authoritative": True, "candidate_route_digest": route["route_digest"],
        "preserved": [
            "canonical dispatch envelope fields",
            "three-operation order through unique audit groups and ordered bindings",
            "candidate route bytes and digest",
        ],
        "discrepancies": [
            {"id": "authority-mode", "preserved": False, "witness": "runtime-managed confirmation is not legacy-managed launch authority"},
            {"id": "role-vocabulary", "preserved": False, "witness": "runtime author/reviewer are substituted by candidate legacy roles"},
            {"id": "logical-group-reuse", "preserved": False, "witness": "group_authoring becomes two unique operation-scoped audit groups"},
            {"id": "shared-seat-session", "preserved": False, "witness": "both author turns name seat_author but 0.6.4 has no Seat/session field"},
            {"id": "continuation-key", "preserved": False, "witness": "0.6.4 carries no continuation identity between author turns"},
            {"id": "reviewer-interposition", "preserved": False, "witness": "layers=2 repeats one group and cannot encode author-reviewer-author"},
        ],
    }
    docs = {"unstamped_row": row, "operation_bindings": binding_doc, "discrepancy_report": gap_doc}
    payloads = {label: _freeze_json(doc) for label, doc in docs.items()}
    hashes = {label: _hash(payload) for label, payload in payloads.items()}
    return {
        "documents": docs, "bytes": payloads, "digests": hashes,
        "projection_digest": _hash(_freeze_json(hashes)),
        "authority": "none", "non_authoritative": True,
    }
