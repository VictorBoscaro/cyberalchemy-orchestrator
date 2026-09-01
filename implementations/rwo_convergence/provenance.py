"""Pure provenance checks for convergence observations.

This layer deliberately accepts already-produced values only.  It does not
open paths, resolve executables, or invoke observation producers.
"""

from __future__ import annotations

import re
from typing import Any, Iterable, Mapping

from .canonical import CanonicalizationError, canonical_json_bytes, sha256_bytes


OBSERVATION_SCHEMA_VERSION = "rwo.cross-language-observation/v1"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class ProvenanceError(ValueError):
    """An input is malformed or cannot satisfy the provenance boundary."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def _fail(code: str, message: str) -> None:
    raise ProvenanceError(code, message)


def _closed_mapping(
    value: Any,
    *,
    required: Iterable[str],
    optional: Iterable[str] = (),
    label: str,
) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        _fail("not-object", f"{label} must be an object")
    required_set = set(required)
    allowed = required_set | set(optional)
    keys = set(value)
    missing = sorted(required_set - keys)
    extra = sorted(keys - allowed)
    if missing:
        _fail("missing-field", f"{label} is missing: {', '.join(missing)}")
    if extra:
        _fail("unknown-field", f"{label} has unknown fields: {', '.join(extra)}")
    return value


def _nonempty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        _fail("invalid-string", f"{label} must be a non-empty string")
    return value


def _sha256(value: Any, label: str) -> str:
    if not isinstance(value, str) or SHA256_RE.fullmatch(value) is None:
        _fail("invalid-sha256", f"{label} must be a lowercase SHA-256 digest")
    return value


def _json_value(value: Any, label: str) -> None:
    if value is None or isinstance(value, (str, bool)):
        return
    if isinstance(value, int) and not isinstance(value, bool):
        return
    if isinstance(value, list):
        for index, member in enumerate(value):
            _json_value(member, f"{label}[{index}]")
        return
    if isinstance(value, Mapping):
        for key, member in value.items():
            _nonempty_string(key, f"{label} key")
            _json_value(member, f"{label}.{key}")
        return
    _fail("non-json-value", f"{label} contains a non-JSON value")


def digest_json(value: Any) -> str:
    """Hash the shared closed canonical JSON bytes without external reads."""

    try:
        return sha256_bytes(canonical_json_bytes(value))
    except CanonicalizationError as exc:
        raise ProvenanceError("canonical-json", str(exc)) from exc


def validate_observation_envelope(value: Any) -> Mapping[str, Any]:
    """Validate one closed cross-language observation envelope."""

    observation = _closed_mapping(
        value,
        required=(
            "schema_version",
            "observation_id",
            "axis_id",
            "producer",
            "accountable_owner",
            "implementation_owner",
            "source_lock_sha256",
            "runner_receipt_sha256",
            "payload_sha256",
            "result",
        ),
        label="observation",
    )
    if observation["schema_version"] != OBSERVATION_SCHEMA_VERSION:
        _fail("schema-version", "observation schema_version is unsupported")
    for field in (
        "observation_id",
        "axis_id",
        "producer",
        "accountable_owner",
        "implementation_owner",
    ):
        _nonempty_string(observation[field], f"observation.{field}")
    _sha256(observation["source_lock_sha256"], "observation.source_lock_sha256")
    _sha256(
        observation["runner_receipt_sha256"],
        "observation.runner_receipt_sha256",
    )
    _sha256(observation["payload_sha256"], "observation.payload_sha256")

    result = _closed_mapping(
        observation["result"],
        required=("corpus_binding_id", "corpus_sha256", "vectors"),
        label="observation.result",
    )
    _nonempty_string(result["corpus_binding_id"], "observation.result.corpus_binding_id")
    _sha256(result["corpus_sha256"], "observation.result.corpus_sha256")
    vectors = result["vectors"]
    if not isinstance(vectors, list):
        _fail("invalid-vectors", "observation.result.vectors must be an array")
    seen: set[str] = set()
    for index, raw_vector in enumerate(vectors):
        vector = _closed_mapping(
            raw_vector,
            required=("vector_id", "fields"),
            label=f"observation.result.vectors[{index}]",
        )
        vector_id = _nonempty_string(
            vector["vector_id"], f"observation.result.vectors[{index}].vector_id"
        )
        if vector_id in seen:
            _fail("duplicate-vector", f"duplicate vector_id: {vector_id}")
        seen.add(vector_id)
        fields = vector["fields"]
        if not isinstance(fields, Mapping):
            _fail("invalid-fields", f"vector {vector_id} fields must be an object")
        _json_value(fields, f"vector {vector_id}.fields")

    if digest_json(result) != observation["payload_sha256"]:
        _fail("payload-digest", "observation payload digest does not match result")
    return observation


def validate_expectation_binding(
    value: Any,
    *,
    expected_binding_id: str,
    expected_sha256: str,
    consuming_axis: str,
    implementation_owner: str,
) -> Mapping[str, Any]:
    """Validate an exact, independent expectation binding.

    The digest argument is caller-bound evidence.  Merely supplying an object
    with a familiar identifier cannot cross this boundary.
    """

    binding = _closed_mapping(
        value,
        required=(
            "binding_id",
            "path",
            "sha256",
            "size_bytes",
            "producer",
            "accountable_owner",
            "authority_posture",
            "allowed_consuming_axes",
        ),
        optional=(
            "forbidden_as_acceptance_evidence",
            "implementation_under_review",
            "direct_runner_allowed",
            "may_issue_expectations",
            "derived_from_observation_id",
        ),
        label="expectation binding",
    )
    _nonempty_string(expected_binding_id, "expected_binding_id")
    _sha256(expected_sha256, "expected_sha256")
    _nonempty_string(consuming_axis, "consuming_axis")
    _nonempty_string(implementation_owner, "implementation_owner")
    if binding["binding_id"] != expected_binding_id:
        _fail("binding-id", "expectation binding ID does not match the bound ID")
    if binding["sha256"] != expected_sha256:
        _fail("binding-digest", "expectation binding digest does not match")
    _nonempty_string(binding["path"], "expectation binding.path")
    _sha256(binding["sha256"], "expectation binding.sha256")
    if (
        not isinstance(binding["size_bytes"], int)
        or isinstance(binding["size_bytes"], bool)
        or binding["size_bytes"] < 0
    ):
        _fail("binding-size", "expectation binding size_bytes is invalid")
    producer = _nonempty_string(binding["producer"], "expectation binding.producer")
    accountable_owner = _nonempty_string(
        binding["accountable_owner"], "expectation binding.accountable_owner"
    )
    _nonempty_string(binding["authority_posture"], "expectation binding.authority_posture")
    axes = binding["allowed_consuming_axes"]
    if (
        not isinstance(axes, list)
        or not axes
        or any(not isinstance(axis, str) or not axis for axis in axes)
        or len(set(axes)) != len(axes)
    ):
        _fail("binding-axes", "allowed_consuming_axes must be a unique non-empty array")
    if consuming_axis not in axes:
        _fail("binding-axis", "expectation binding does not permit the consuming axis")
    if producer == implementation_owner or accountable_owner == implementation_owner:
        _fail(
            "self-issued-expectation",
            "expectation producer and accountable owner must be disjoint from the implementation owner",
        )
    if binding.get("implementation_under_review") not in (None, implementation_owner):
        _fail("implementation-owner", "binding names a different implementation under review")
    if binding.get("may_issue_expectations") is False:
        _fail("observation-as-expectation", "this producer binding may not issue expectations")
    if binding.get("derived_from_observation_id") is not None:
        _fail("derived-expectation", "an observation-derived expectation is forbidden")
    if not binding["binding_id"].startswith("EXP-"):
        _fail("observation-as-expectation", "an observation binding cannot be relabeled as expectation")
    return binding


def require_identical_source_lock(*documents: Mapping[str, Any]) -> str:
    """Return the common lock digest or fail if inputs are not lock-identical."""

    if not documents:
        _fail("source-lock-empty", "at least one source-bound document is required")
    digests: list[str] = []
    for index, document in enumerate(documents):
        if not isinstance(document, Mapping):
            _fail("not-object", f"source-bound document {index} must be an object")
        if "source_lock_sha256" not in document:
            _fail("missing-source-lock", f"source-bound document {index} has no source lock")
        digests.append(_sha256(document["source_lock_sha256"], f"document {index} source lock"))
    if len(set(digests)) != 1:
        _fail("source-lock-mismatch", "all inputs must name the identical source lock")
    return digests[0]
