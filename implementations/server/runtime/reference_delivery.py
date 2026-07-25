"""Pure contracts for ACI target-agent reference delivery."""

from __future__ import annotations

from typing import Any

from .canonical import canonical_bytes, canonical_digest, digest_bytes, parse_strict_json
from .errors import IntegrityError, ValidationError

TARGET_RESOLUTION_SCHEMA = "aci.agent-reference-target-resolution/v1"
DELIVERY_EVIDENCE_SCHEMA = "aci.agent-reference-delivery-evidence/v1"
EFFECTIVE_INPUT_SCHEMA = "aci.effective-input-artifact/v1"


def derive_target_identity(binding: dict[str, Any]) -> dict[str, str]:
    required = {
        "binding_id",
        "dispatch_id",
        "group_id",
        "seat_index",
        "attempt_id",
        "host",
        "prompt_template_digest",
    }
    if not required.issubset(binding):
        raise IntegrityError("host workflow binding is incomplete")
    seed = {
        "dispatch_id": binding["dispatch_id"],
        "group_id": binding["group_id"],
        "seat_index": binding["seat_index"],
    }
    instance_seed = {
        **seed,
        "host": binding["host"],
        "prompt_template_digest": binding["prompt_template_digest"],
    }
    return {
        "dispatch_id": binding["dispatch_id"],
        "target_attempt_id": binding["attempt_id"],
        "target_seat_id": "seat_" + canonical_digest(seed)[7:39],
        "target_agent_instance_id": "agi_" + canonical_digest(instance_seed)[7:39],
    }


def decode_reference_bundle(
    body: bytes, *, expected_digest: str
) -> tuple[dict[str, Any], list[str]]:
    if digest_bytes(body) != expected_digest:
        raise IntegrityError("reference bundle bytes do not match committed digest")
    bundle = parse_strict_json(body)
    if (
        not isinstance(bundle, dict)
        or set(bundle) != {"schema", "scout_run_id", "probe_id", "recommendations"}
        or bundle["schema"] != "aci.reference-scout-bundle/v1"
        or not isinstance(bundle["recommendations"], list)
    ):
        raise IntegrityError("reference bundle shape is invalid")
    recommendation_ids: list[str] = []
    for recommendation in bundle["recommendations"]:
        if (
            not isinstance(recommendation, dict)
            or not isinstance(recommendation.get("recommendation_id"), str)
            or not recommendation["recommendation_id"]
        ):
            raise IntegrityError("reference bundle recommendation identity is invalid")
        recommendation_ids.append(recommendation["recommendation_id"])
    if len(recommendation_ids) != len(set(recommendation_ids)):
        raise IntegrityError("reference bundle recommendation identities are duplicated")
    return bundle, recommendation_ids


def build_effective_input(
    *,
    attempt_id: str,
    base_entries: list[dict[str, Any]],
    entry_ordinal: int,
    bundle_artifact_id: str,
    bundle_digest: str,
    agent_reference_delivery_id: str,
    visibility_policy_ref: str,
) -> tuple[dict[str, Any], bytes]:
    if (
        not isinstance(base_entries, list)
        or not isinstance(entry_ordinal, int)
        or entry_ordinal < 0
        or entry_ordinal > len(base_entries)
    ):
        raise ValidationError("effective-input entry ordinal is invalid")
    if any(
        not isinstance(entry, dict) or not isinstance(entry.get("entry_type"), str)
        for entry in base_entries
    ):
        raise ValidationError("effective-input base entry is invalid")
    if any(entry["entry_type"] == "reference_bundle" for entry in base_entries):
        raise ValidationError("effective input already contains a reference bundle")
    reference_entry = {
        "entry_type": "reference_bundle",
        "artifact_ref": bundle_artifact_id,
        "content_hash": bundle_digest,
        "agent_reference_delivery_id": agent_reference_delivery_id,
        "visibility_policy_ref": visibility_policy_ref,
    }
    entries = [dict(entry) for entry in base_entries]
    entries.insert(entry_ordinal, reference_entry)
    manifest = {
        "schema": EFFECTIVE_INPUT_SCHEMA,
        "attempt_id": attempt_id,
        "entries": entries,
    }
    return manifest, canonical_bytes(manifest)


def verify_reference_bundle_entry(
    delivery: dict[str, Any], effective_input: dict[str, Any]
) -> dict[str, Any]:
    required_delivery = {
        "agent_reference_delivery_id",
        "bundle_artifact_id",
        "bundle_digest",
        "target_attempt_id",
        "effective_input_entry_ordinal",
        "effective_input_manifest_hash",
        "visibility_policy_ref",
    }
    if not required_delivery.issubset(delivery):
        raise IntegrityError("agent reference delivery is incomplete")
    if (
        not isinstance(effective_input, dict)
        or set(effective_input) != {"schema", "attempt_id", "entries"}
        or effective_input["schema"] != EFFECTIVE_INPUT_SCHEMA
        or effective_input["attempt_id"] != delivery["target_attempt_id"]
        or canonical_digest(effective_input)
        != delivery["effective_input_manifest_hash"]
    ):
        raise IntegrityError("effective-input manifest binding is invalid")
    entries = effective_input["entries"]
    ordinal = delivery["effective_input_entry_ordinal"]
    if not isinstance(entries, list) or not 0 <= ordinal < len(entries):
        raise IntegrityError("reference-bundle entry ordinal is invalid")
    matching = [
        entry
        for entry in entries
        if isinstance(entry, dict)
        and entry.get("entry_type") == "reference_bundle"
        and entry.get("agent_reference_delivery_id")
        == delivery["agent_reference_delivery_id"]
    ]
    expected = {
        "entry_type": "reference_bundle",
        "artifact_ref": delivery["bundle_artifact_id"],
        "content_hash": delivery["bundle_digest"],
        "agent_reference_delivery_id": delivery["agent_reference_delivery_id"],
        "visibility_policy_ref": delivery["visibility_policy_ref"],
    }
    if len(matching) != 1 or entries[ordinal] != expected:
        raise IntegrityError("reference-bundle entry is absent, duplicated, or divergent")
    return expected


def wrap_target_resolution(
    target: dict[str, Any], *, binding_id: str, effective_as_of: int
) -> dict[str, Any]:
    body = {
        "schema": TARGET_RESOLUTION_SCHEMA,
        "owner": "agents-communication-infra",
        "owner_version": "1",
        "binding_id": binding_id,
        "effective_as_of": effective_as_of,
        "target": target,
    }
    return {**body, "wrapper_digest": canonical_digest(body)}


def wrap_delivery_evidence(
    *,
    delivery: dict[str, Any],
    effective_input: dict[str, Any],
    accepted_group: dict[str, Any],
) -> dict[str, Any]:
    verified_entry = verify_reference_bundle_entry(delivery, effective_input)
    body = {
        "schema": DELIVERY_EVIDENCE_SCHEMA,
        "owner": "agents-communication-infra",
        "owner_version": "1",
        "effective_as_of": delivery["journal_offset"],
        "delivery": delivery,
        "effective_input": effective_input,
        "verified_reference_bundle_entry": verified_entry,
        "accepted_group": accepted_group,
        "evidence_boundary": {
            "included_in_effective_input": True,
            "access_observed": False,
            "declared_used": False,
            "claim_support": False,
        },
    }
    return {**body, "wrapper_digest": canonical_digest(body)}


def verify_wrapper(wrapper: dict[str, Any], *, schema: str) -> dict[str, Any]:
    if not isinstance(wrapper, dict) or wrapper.get("schema") != schema:
        raise IntegrityError("reference evidence wrapper schema is invalid")
    required = (
        {
            "schema",
            "owner",
            "owner_version",
            "binding_id",
            "effective_as_of",
            "target",
            "wrapper_digest",
        }
        if schema == TARGET_RESOLUTION_SCHEMA
        else {
            "schema",
            "owner",
            "owner_version",
            "effective_as_of",
            "delivery",
            "effective_input",
            "verified_reference_bundle_entry",
            "accepted_group",
            "evidence_boundary",
            "wrapper_digest",
        }
    )
    if set(wrapper) != required:
        raise IntegrityError("reference evidence wrapper fields are incomplete or extra")
    if wrapper.get("owner") != "agents-communication-infra":
        raise IntegrityError("reference evidence wrapper owner is invalid")
    digest = wrapper.get("wrapper_digest")
    body = {key: value for key, value in wrapper.items() if key != "wrapper_digest"}
    if not isinstance(digest, str) or canonical_digest(body) != digest:
        raise IntegrityError("reference evidence wrapper digest is invalid")
    return body
