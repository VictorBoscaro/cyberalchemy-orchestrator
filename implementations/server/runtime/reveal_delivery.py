"""Pure contracts for the bounded ACI reveal-to-attempt delivery proof."""

from __future__ import annotations

from typing import Any

from .canonical import canonical_bytes, canonical_digest
from .errors import IntegrityError, ValidationError

VISIBILITY_POLICY_REF = "aci.fixed-two-seat-peer-reveal@1"
EFFECTIVE_INPUT_SCHEMA = "aci.effective-input-artifact/v1"
MATERIALIZER_REF = "aci.fixed-local-peer-input-materializer@1"

PLAN_FIELDS = {
    "attempt_id",
    "operation_id",
    "seat_id",
    "group_aggregate_id",
    "binding_id",
    "provider_ref",
    "adapter_ref",
    "model_ref",
    "role_contract_ref",
    "task_ref",
    "base_snapshot_ref",
    "role_delta_ref",
    "response_schema_ref",
    "tool_profile_ref",
    "deadline",
    "resource_budget",
    "sandbox_policy",
    "authority_fence",
}


def validate_invocation_plan(plan: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(plan, dict) or set(plan) != PLAN_FIELDS:
        raise ValidationError("agent invocation plan shape is invalid")
    structured = {"resource_budget", "sandbox_policy", "authority_fence"}
    required_text = PLAN_FIELDS - {"role_delta_ref"} - structured
    if any(not isinstance(plan[name], str) or not plan[name] for name in required_text):
        raise ValidationError("agent invocation plan text identity is invalid")
    if plan["role_delta_ref"] is not None and (
        not isinstance(plan["role_delta_ref"], str) or not plan["role_delta_ref"]
    ):
        raise ValidationError("agent invocation plan role delta is invalid")
    if any(not isinstance(plan[name], dict) for name in structured):
        raise ValidationError("agent invocation plan structured control is invalid")
    return plan


def build_peer_entries(
    *,
    reveal_manifest_id: str,
    manifest_entries: list[dict[str, Any]],
    official_messages: list[dict[str, Any]],
    target_seat_id: str,
    visibility_policy_ref: str,
) -> list[dict[str, Any]]:
    if visibility_policy_ref != VISIBILITY_POLICY_REF:
        raise ValidationError("peer visibility policy is not admitted")
    by_id = {row["message_id"]: row for row in official_messages}
    if len(by_id) != len(official_messages):
        raise IntegrityError("official contribution identity is duplicated")
    peer_entries: list[dict[str, Any]] = []
    for entry in manifest_entries:
        if set(entry) != {"message_id", "payload_hash"}:
            raise IntegrityError("reveal manifest entry shape is invalid")
        contribution = by_id.get(entry["message_id"])
        if not contribution:
            raise IntegrityError("reveal entry is not an official contribution")
        if (
            contribution["payload_hash"] != entry["payload_hash"]
            or contribution["artifact_content_hash"] != entry["payload_hash"]
        ):
            raise IntegrityError("reveal contribution artifact binding differs")
        if contribution["seat_id"] == target_seat_id:
            continue
        peer_entries.append(
            {
                "entry_type": "reveal_message",
                "artifact_ref": contribution["payload_ref"],
                "content_hash": entry["payload_hash"],
                "author_principal_id": contribution["seat_id"],
                "message_id": entry["message_id"],
                "reveal_manifest_id": reveal_manifest_id,
                "visibility_policy_ref": visibility_policy_ref,
            }
        )
    return peer_entries


def preallocate_effective_input_id(
    *, plan_digest: str, reveal_manifest_id: str, target_attempt_id: str
) -> str:
    digest = canonical_digest(
        {
            "plan_digest": plan_digest,
            "reveal_manifest_id": reveal_manifest_id,
            "target_attempt_id": target_attempt_id,
        }
    )
    return "art_eia_" + digest.removeprefix("sha256:")[:32]


def deterministic_materialize(
    *,
    plan: dict[str, Any],
    plan_digest: str,
    effective_input_artifact_id: str,
    prepared_entries: list[dict[str, Any]],
) -> tuple[dict[str, Any], bytes]:
    validate_invocation_plan(plan)
    if canonical_digest(plan) != plan_digest:
        raise IntegrityError("agent invocation plan digest differs")
    wrapper = {
        "schema": "aci.fixed-provider-invocation/v1",
        "attempt_id": plan["attempt_id"],
        "effective_input_ref": effective_input_artifact_id,
        "entry_hashes": [canonical_digest(entry) for entry in prepared_entries],
        "tool_profile_ref": plan["tool_profile_ref"],
        "response_schema_ref": plan["response_schema_ref"],
    }
    wrapper_bytes = canonical_bytes(wrapper)
    wrapper_hash = canonical_digest(wrapper)
    provider_invocation_ref = "art_" + wrapper_hash.removeprefix("sha256:")[:32]
    materialized_body = {
        "plan_digest": plan_digest,
        "effective_input_ref": effective_input_artifact_id,
        "provider_invocation_ref": provider_invocation_ref,
        "materializer_ref": MATERIALIZER_REF,
    }
    materialized = {
        **materialized_body,
        "materialization_digest": canonical_digest(materialized_body),
    }
    return materialized, wrapper_bytes


def build_effective_input_manifest(
    *,
    plan: dict[str, Any],
    effective_input_artifact_id: str,
    base_entries: list[dict[str, Any]],
    peer_entries: list[dict[str, Any]],
    reveal_manifest_entries: list[dict[str, Any]],
    provider_invocation_ref: str,
    provider_invocation_hash: str,
) -> tuple[dict[str, Any], bytes]:
    manifest_positions = {
        entry["message_id"]: (position, entry["payload_hash"])
        for position, entry in enumerate(reveal_manifest_entries)
    }
    positions: list[int] = []
    for entry in peer_entries:
        source = manifest_positions.get(entry.get("message_id"))
        if (
            entry.get("entry_type") != "reveal_message"
            or entry.get("author_principal_id") == plan["seat_id"]
            or entry.get("visibility_policy_ref") != VISIBILITY_POLICY_REF
            or source is None
            or entry.get("content_hash") != source[1]
        ):
            raise IntegrityError("final peer entry violates reveal authority")
        positions.append(source[0])
    if len(positions) != len(set(positions)) or positions != sorted(positions):
        raise IntegrityError("final peer entry order or identity differs from reveal")
    entries = [dict(entry) for entry in base_entries] + [dict(entry) for entry in peer_entries]
    entries.append(
        {
            "entry_type": "adapter_wrapper",
            "artifact_ref": provider_invocation_ref,
            "content_hash": provider_invocation_hash,
            "author_principal_id": None,
            "message_id": None,
            "reveal_manifest_id": None,
            "visibility_policy_ref": MATERIALIZER_REF,
        }
    )
    manifest = {
        "schema": EFFECTIVE_INPUT_SCHEMA,
        "artifact_id": effective_input_artifact_id,
        "attempt_id": plan["attempt_id"],
        "base_snapshot_ref": plan["base_snapshot_ref"],
        "role_delta_ref": plan["role_delta_ref"],
        "entries": entries,
        "tool_contract_refs": [plan["tool_profile_ref"]],
        "response_schema_ref": plan["response_schema_ref"],
        "context_artifact_refs": [
            ref
            for ref in (plan["base_snapshot_ref"], plan["role_delta_ref"])
            if ref is not None
        ],
        "adapter_wrapper_refs": [provider_invocation_ref],
    }
    return manifest, canonical_bytes(manifest)
