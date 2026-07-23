"""D0 structural fixture verifier; not a runtime or canonical authority."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
FIXTURE_PATH = HERE / "fixtures" / "conformance-vectors.json"
CANDIDATE_PATH = HERE / "fixtures" / "seed-registry-candidates-v01.json"
REPO_ROOT = HERE.parents[3]
POOL_PATH = REPO_ROOT / "telemetry" / "agents" / "agent-pool.yaml"
ACI_VECTOR_PATH = (
    HERE.parent.parent
    / "agents-communication-infra"
    / "adrs"
    / "fixtures"
    / "canonical-contract-vectors.json"
)
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
INT64_MIN = -(2**63)
INT64_MAX = 2**63 - 1


class ContractError(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code


def _normalize(value: Any) -> Any:
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, int):
        if not INT64_MIN <= value <= INT64_MAX:
            raise ContractError("CANON_INTEGER_OUT_OF_RANGE")
        return value
    if isinstance(value, float):
        raise ContractError("CANON_FLOAT_FORBIDDEN")
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    if isinstance(value, list):
        return [_normalize(item) for item in value]
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        for raw_key, raw_value in value.items():
            if not isinstance(raw_key, str):
                raise ContractError("CANON_OBJECT_KEY_NOT_STRING")
            key = unicodedata.normalize("NFC", raw_key)
            if key in result:
                raise ContractError("CANON_DUPLICATE_KEY_AFTER_NFC", key)
            result[key] = _normalize(raw_value)
        return result
    raise ContractError("CANON_UNSUPPORTED_TYPE", type(value).__name__)


def canonical_bytes(projected: Any) -> bytes:
    normalized = _normalize(projected)
    return json.dumps(
        normalized,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def digest(projected: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(projected)).hexdigest()


REQUIRED: dict[str, set[str]] = {
    "topic.emission_observed@1": {
        "schema_version",
        "emission_id",
        "conversation_id",
        "turn_id",
        "dispatch_id",
        "group_id",
        "seat_id",
        "attempt_id",
        "activation_seq",
        "trigger",
        "capture_phase",
        "observed_terms",
        "selected_tag_ids",
        "writer_observed_at",
    },
    "tag.resolution_projected@1": {
        "schema_version",
        "resolution_id",
        "emission_ref",
        "registry_version",
        "resolver_version",
        "system_resolved_tag_ids",
        "unmapped_terms",
        "mapping_trace",
    },
    "tag.registry_snapshot@1": {"schema_version", "registry_version", "tags"},
    "lens.projected@1": {
        "schema_version",
        "lens_id",
        "scope",
        "resolution_refs",
        "registry_version",
        "projection_version",
        "shared_core",
        "perspectives",
        "residue_refs",
        "interpretation_limit",
    },
}

OPTIONAL: dict[str, set[str]] = {
    "topic.emission_observed@1": {"free_emission_ref", "registry_version"},
    "tag.resolution_projected@1": set(),
    "tag.registry_snapshot@1": set(),
    "lens.projected@1": set(),
}


def _require_unique_strings(values: Any, code: str) -> None:
    if not isinstance(values, list) or any(not isinstance(v, str) or not v for v in values):
        raise ContractError(code, "expected non-empty strings")
    if len(values) != len(set(values)):
        raise ContractError(code, "duplicates")


def _validate_shape(kind: str, record: dict[str, Any]) -> None:
    if kind not in REQUIRED:
        raise ContractError("UNKNOWN_KIND", kind)
    missing = REQUIRED[kind] - record.keys()
    if missing:
        raise ContractError("REQUIRED_FIELD_MISSING", ",".join(sorted(missing)))
    unknown = record.keys() - REQUIRED[kind] - OPTIONAL[kind]
    if unknown:
        raise ContractError("UNKNOWN_FIELD", ",".join(sorted(unknown)))


def validate_record(kind: str, record: dict[str, Any]) -> None:
    _validate_shape(kind, record)

    if kind == "topic.emission_observed@1":
        _require_unique_strings(record["observed_terms"], "OBSERVED_TERMS_INVALID")
        _require_unique_strings(record["selected_tag_ids"], "SELECTED_TAG_IDS_INVALID")
        phase = record["capture_phase"]
        if phase == "free":
            if record["selected_tag_ids"]:
                raise ContractError("FREE_EMISSION_SELECTS_TAGS")
            if "free_emission_ref" in record or "registry_version" in record:
                raise ContractError("FREE_EMISSION_HAS_ASSISTED_CONTEXT")
        elif phase == "assisted":
            if "free_emission_ref" not in record:
                raise ContractError("ASSISTED_FREE_REF_REQUIRED")
            if "registry_version" not in record:
                raise ContractError("ASSISTED_REGISTRY_REQUIRED")
            if record["observed_terms"]:
                raise ContractError("ASSISTED_EMISSION_HAS_FREE_TERMS")
            if not record["selected_tag_ids"]:
                raise ContractError("ASSISTED_SELECTION_REQUIRED")
        else:
            raise ContractError("CAPTURE_PHASE_INVALID")

    elif kind == "tag.resolution_projected@1":
        _require_unique_strings(record["system_resolved_tag_ids"], "RESOLVED_TAG_IDS_INVALID")
        _require_unique_strings(record["unmapped_terms"], "UNMAPPED_TERMS_INVALID")
        if not isinstance(record["mapping_trace"], list):
            raise ContractError("MAPPING_TRACE_INVALID")

    elif kind == "tag.registry_snapshot@1":
        if not isinstance(record["tags"], list) or not record["tags"]:
            raise ContractError("REGISTRY_TAGS_REQUIRED")
        seen_ids: set[str] = set()
        seen_labels: set[str] = set()
        allowed = {
            "tag_id",
            "canonical_label",
            "definition",
            "aliases",
            "status",
            "resolution_eligible",
            "provenance_refs",
        }
        for tag in record["tags"]:
            if not isinstance(tag, dict) or set(tag) != allowed:
                raise ContractError("REGISTRY_TAG_SHAPE_INVALID")
            if tag["tag_id"] in seen_ids or tag["canonical_label"] in seen_labels:
                raise ContractError("REGISTRY_TAG_DUPLICATE")
            seen_ids.add(tag["tag_id"])
            seen_labels.add(tag["canonical_label"])
            if tag["status"] == "accepted" and not tag["definition"].strip():
                raise ContractError("ACCEPTED_TAG_DEFINITION_REQUIRED")
            if tag["resolution_eligible"] and tag["status"] != "accepted":
                raise ContractError("NON_ACCEPTED_TAG_RESOLUTION_ELIGIBLE")
            _require_unique_strings(tag["aliases"], "TAG_ALIASES_INVALID")
            _require_unique_strings(tag["provenance_refs"], "TAG_PROVENANCE_INVALID")

    elif kind == "lens.projected@1":
        if record["interpretation_limit"] != "tag_presence_only":
            raise ContractError("LENS_INTERPRETATION_LIMIT_INVALID")
        _require_unique_strings(record["resolution_refs"], "LENS_RESOLUTION_REFS_INVALID")
        allowed_refs = set(record["resolution_refs"])
        for element in [*record["shared_core"], *record["perspectives"]]:
            refs = element.get("supporting_resolution_refs")
            _require_unique_strings(refs, "LENS_SUPPORT_REQUIRED")
            if not set(refs) <= allowed_refs:
                raise ContractError("LENS_SUPPORT_OUTSIDE_INPUT")


def _index_positive(fixture: dict[str, Any]) -> dict[str, dict[str, Any]]:
    vectors = fixture["vectors"]
    result = {vector["id"]: vector for vector in vectors}
    if len(result) != len(vectors):
        raise ContractError("VECTOR_ID_DUPLICATE")
    return result


def validate_cross_references(vectors: list[dict[str, Any]]) -> None:
    records = [vector["record_without_digest"] for vector in vectors]
    emissions = {r["emission_id"] for r in records if r.get("schema_version") == "apt.topic-emission@1"}
    registries = {
        r["registry_version"]: {
            tag["tag_id"]
            for tag in r["tags"]
            if tag["status"] == "accepted" and tag["resolution_eligible"]
        }
        for r in records
        if r.get("schema_version") == "apt.tag-registry@1"
    }
    resolutions = {r["resolution_id"]: r for r in records if r.get("schema_version") == "apt.tag-resolution@1"}

    for record in records:
        if record.get("capture_phase") == "assisted":
            if record["free_emission_ref"] not in emissions:
                raise ContractError("ASSISTED_FREE_REF_UNKNOWN")
            eligible = registries.get(record["registry_version"])
            if eligible is None:
                raise ContractError("ASSISTED_REGISTRY_UNKNOWN")
            if not set(record["selected_tag_ids"]) <= eligible:
                raise ContractError("ASSISTED_TAG_NOT_ELIGIBLE")
        if record.get("schema_version") == "apt.tag-resolution@1":
            if record["emission_ref"] not in emissions:
                raise ContractError("RESOLUTION_EMISSION_UNKNOWN")
            if record["registry_version"] not in registries:
                raise ContractError("RESOLUTION_REGISTRY_UNKNOWN")
            if not set(record["system_resolved_tag_ids"]) <= registries[record["registry_version"]]:
                raise ContractError("RESOLUTION_TAG_NOT_ELIGIBLE")
        if record.get("schema_version") == "apt.lens@1":
            if not set(record["resolution_refs"]) <= resolutions.keys():
                raise ContractError("LENS_RESOLUTION_UNKNOWN")
            if record["registry_version"] not in registries:
                raise ContractError("LENS_REGISTRY_UNKNOWN")
            inputs = [resolutions[ref] for ref in record["resolution_refs"]]
            if any(item["registry_version"] != record["registry_version"] for item in inputs):
                raise ContractError("LENS_REGISTRY_MISMATCH")
            input_tags = {tag for item in inputs for tag in item["system_resolved_tag_ids"]}
            lens_tags = {
                item["tag_id"] for item in record["shared_core"]
            } | {
                tag for item in record["perspectives"] for tag in item["tag_ids"]
            }
            if not lens_tags <= input_tags:
                raise ContractError("LENS_TAG_OUTSIDE_RESOLUTIONS")


def apply_rejection(vector: dict[str, Any], positives: dict[str, dict[str, Any]]) -> dict[str, Any]:
    source = positives.get(vector["mutate_from"])
    if source is None:
        raise ContractError("REJECTION_SOURCE_UNKNOWN", vector["mutate_from"])
    record = copy.deepcopy(source["record_without_digest"])
    for key, value in vector.get("patch", {}).items():
        record[key] = value
    for key in vector.get("remove", []):
        record.pop(key, None)
    if "patch_path" in vector:
        target: Any = record
        for segment in vector["patch_path"][:-1]:
            target = target[segment]
        target[vector["patch_path"][-1]] = vector["patch_value"]
    return record


def validate_aci_serializer_subset() -> None:
    corpus = json.loads(ACI_VECTOR_PATH.read_text(encoding="utf-8"))
    for vector in corpus["vectors"]:
        projected = json.loads(vector["canonical_utf8"])
        actual_bytes = canonical_bytes(projected)
        if actual_bytes.decode("utf-8") != vector["canonical_utf8"]:
            raise ContractError("ACI_CANONICAL_BYTES_MISMATCH", vector["id"])
        if "sha256:" + hashlib.sha256(actual_bytes).hexdigest() != vector["digest"]:
            raise ContractError("ACI_CANONICAL_DIGEST_MISMATCH", vector["id"])


def _pool_usage() -> tuple[Counter[str], dict[str, Counter[str]]]:
    counts: Counter[str] = Counter()
    fields: dict[str, Counter[str]] = defaultdict(Counter)
    current_field: str | None = None
    field_re = re.compile(r"\s+field:\s*(\S+)\s*$")
    tags_re = re.compile(r"\s+tags:\s*\[(.*)\]\s*$")
    for line in POOL_PATH.read_text(encoding="utf-8").splitlines():
        field_match = field_re.match(line)
        if field_match:
            current_field = field_match.group(1)
            continue
        tags_match = tags_re.match(line)
        if tags_match and current_field:
            tags = [item.strip().strip("\"'") for item in tags_match.group(1).split(",") if item.strip()]
            counts.update(tags)
            fields[current_field].update(tags)
    return counts, fields


def validate_candidate_batch() -> int:
    batch = json.loads(CANDIDATE_PATH.read_text(encoding="utf-8"))
    actual_pool_digest = "sha256:" + hashlib.sha256(POOL_PATH.read_bytes()).hexdigest()
    if batch["pool_snapshot"] != actual_pool_digest:
        raise ContractError(
            "CANDIDATE_POOL_SNAPSHOT_DRIFT",
            f'expected={batch["pool_snapshot"]} actual={actual_pool_digest}',
        )
    candidates = batch["candidates"]
    ids = [item["tag_id"] for item in candidates]
    labels = [item["canonical_label"] for item in candidates]
    if len(ids) != len(set(ids)) or len(labels) != len(set(labels)):
        raise ContractError("CANDIDATE_ID_OR_LABEL_DUPLICATE")

    counts, fields = _pool_usage()
    origin_counts: Counter[str] = Counter()
    for item in candidates:
        origin_counts[item["origin"]] += 1
        if item["status"] != "candidate" or item["resolution_eligible"] is not False:
            raise ContractError("CANDIDATE_PREMATURE_PROMOTION", item["canonical_label"])
        if item["definition_status"] != "missing":
            raise ContractError("CANDIDATE_DEFINITION_STATUS_UNEXPECTED", item["canonical_label"])
        label = item["canonical_label"]
        actual_count = counts[label]
        actual_fields = {name: field_counts[label] for name, field_counts in fields.items() if field_counts[label]}
        if item["pool_usage_count"] != actual_count or item["field_distribution"] != actual_fields:
            raise ContractError("CANDIDATE_POOL_FACT_DRIFT", label)
        if item["origin"] == "pool_present" and actual_count <= 0:
            raise ContractError("CANDIDATE_EXPECTED_POOL_PRESENCE", label)
        if item["origin"] == "runtime_exact_residue" and actual_count != 0:
            raise ContractError("CANDIDATE_RESIDUE_NOW_PRESENT", label)
        if item["origin"] not in {"pool_present", "runtime_exact_residue"}:
            raise ContractError("CANDIDATE_ORIGIN_INVALID", item["origin"])

    if origin_counts != Counter({"pool_present": 8, "runtime_exact_residue": 8}):
        raise ContractError("CANDIDATE_BATCH_COMPOSITION_INVALID", str(dict(origin_counts)))
    return len(candidates)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--print-digests", action="store_true")
    args = parser.parse_args()

    validate_aci_serializer_subset()
    candidate_count = validate_candidate_batch()
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    positives = _index_positive(fixture)

    for vector in fixture["vectors"]:
        record = vector["record_without_digest"]
        validate_record(vector["kind"], record)
        actual = digest(record)
        if args.print_digests:
            print(f'{vector["id"]} {actual}')
        elif not DIGEST_RE.fullmatch(vector["expected_digest"]) or actual != vector["expected_digest"]:
            raise ContractError("DIGEST_MISMATCH", f'{vector["id"]} expected={vector["expected_digest"]} actual={actual}')

    validate_cross_references(fixture["vectors"])

    for vector in fixture["rejection_vectors"]:
        mutated = apply_rejection(vector, positives)
        try:
            validate_record(vector["kind"], mutated)
            candidate_vectors = copy.deepcopy(fixture["vectors"])
            for candidate in candidate_vectors:
                if candidate["id"] == vector["mutate_from"]:
                    candidate["record_without_digest"] = mutated
                    break
            validate_cross_references(candidate_vectors)
        except ContractError as exc:
            if exc.code != vector["expected_error"]:
                raise ContractError(
                    "REJECTION_ERROR_MISMATCH",
                    f'{vector["id"]} expected={vector["expected_error"]} actual={exc.code}',
                ) from exc
        else:
            raise ContractError("REJECTION_ACCEPTED", vector["id"])

    if not args.print_digests:
        print(
            "PASS "
            f'aci_vectors={len(json.loads(ACI_VECTOR_PATH.read_text(encoding="utf-8"))["vectors"])} '
            f'positive={len(fixture["vectors"])} rejection={len(fixture["rejection_vectors"])} '
            f'candidates={candidate_count}'
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ContractError as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        raise SystemExit(1)
