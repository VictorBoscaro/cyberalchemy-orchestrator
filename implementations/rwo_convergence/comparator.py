"""Data-only comparison of independently produced observation envelopes."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from .provenance import (
    ProvenanceError,
    require_identical_source_lock,
    validate_expectation_binding,
    validate_observation_envelope,
)


def _ordered_vectors(
    observation: Mapping[str, Any], frozen_corpus_order: Sequence[str]
) -> list[Mapping[str, Any]]:
    vectors = observation["result"]["vectors"]
    actual_order = [vector["vector_id"] for vector in vectors]
    if actual_order != list(frozen_corpus_order):
        raise ProvenanceError(
            "frozen-corpus-order",
            "observation vectors must exactly match the complete frozen corpus order",
        )
    return vectors


def _validate_frozen_order(value: Any) -> tuple[str, ...]:
    if not isinstance(value, list) or not value:
        raise ProvenanceError(
            "frozen-corpus-order", "frozen corpus order must be a non-empty array"
        )
    if any(not isinstance(member, str) or not member for member in value):
        raise ProvenanceError(
            "frozen-corpus-order", "frozen corpus members must be non-empty strings"
        )
    if len(set(value)) != len(value):
        raise ProvenanceError(
            "frozen-corpus-order", "frozen corpus order contains a duplicate member"
        )
    return tuple(value)


def compare_cross_language(
    python_observation: Mapping[str, Any],
    rust_observation: Mapping[str, Any],
    *,
    corpus_binding: Mapping[str, Any],
    corpus_binding_sha256: str,
    oracle_binding: Mapping[str, Any],
    oracle_binding_sha256: str,
    frozen_corpus_order: Sequence[str],
) -> dict[str, Any]:
    """Compare Python and Rust observations in exact frozen-corpus order.

    Agreement is a bounded current observation.  It is never converted into
    semantic acceptance or ownership of either producer.
    """

    python_document = validate_observation_envelope(python_observation)
    rust_document = validate_observation_envelope(rust_observation)
    if python_document["axis_id"] != "AX-PYTHON":
        raise ProvenanceError("python-axis", "Python observation must name AX-PYTHON")
    if rust_document["axis_id"] != "AX-RUST":
        raise ProvenanceError("rust-axis", "Rust observation must name AX-RUST")
    source_lock_sha256 = require_identical_source_lock(python_document, rust_document)

    corpus = validate_expectation_binding(
        corpus_binding,
        expected_binding_id="EXP-FROZEN-CORPUS",
        expected_sha256=corpus_binding_sha256,
        consuming_axis="AX-CROSS-LANGUAGE",
        implementation_owner=rust_document["implementation_owner"],
    )
    oracle = validate_expectation_binding(
        oracle_binding,
        expected_binding_id="EXP-PYTHON-PRODUCER",
        expected_sha256=oracle_binding_sha256,
        consuming_axis="AX-CROSS-LANGUAGE",
        implementation_owner=rust_document["implementation_owner"],
    )
    if oracle["producer"] != python_document["producer"]:
        raise ProvenanceError(
            "oracle-producer", "Python observation producer does not match the oracle binding"
        )
    if oracle["accountable_owner"] != python_document["accountable_owner"]:
        raise ProvenanceError(
            "oracle-owner", "Python observation accountable owner does not match the oracle binding"
        )
    for document in (python_document, rust_document):
        result = document["result"]
        if result["corpus_binding_id"] != corpus["binding_id"]:
            raise ProvenanceError(
                "corpus-binding", "observation names a different frozen corpus binding"
            )
        if result["corpus_sha256"] != corpus["sha256"]:
            raise ProvenanceError(
                "corpus-digest", "observation names a different frozen corpus digest"
            )

    order = _validate_frozen_order(frozen_corpus_order)
    python_vectors = _ordered_vectors(python_document, order)
    rust_vectors = _ordered_vectors(rust_document, order)
    vector_results: list[dict[str, Any]] = []
    all_equivalent = True
    for vector_id, python_vector, rust_vector in zip(
        order, python_vectors, rust_vectors, strict=True
    ):
        python_fields = python_vector["fields"]
        rust_fields = rust_vector["fields"]
        fields: list[dict[str, Any]] = []
        vector_equivalent = True
        for field_name in sorted(set(python_fields) | set(rust_fields)):
            python_present = field_name in python_fields
            rust_present = field_name in rust_fields
            equivalent = (
                python_present
                and rust_present
                and python_fields[field_name] == rust_fields[field_name]
            )
            vector_equivalent = vector_equivalent and equivalent
            fields.append(
                {
                    "field": field_name,
                    "python_present": python_present,
                    "rust_present": rust_present,
                    "equivalent": equivalent,
                }
            )
        all_equivalent = all_equivalent and vector_equivalent
        vector_results.append(
            {
                "vector_id": vector_id,
                "equivalent": vector_equivalent,
                "field_comparisons": fields,
            }
        )

    return {
        "schema_version": "rwo.cross-language-comparison/v1",
        "axis_id": "AX-CROSS-LANGUAGE",
        "source_lock_sha256": source_lock_sha256,
        "corpus_binding_id": corpus["binding_id"],
        "corpus_sha256": corpus["sha256"],
        "oracle_binding_id": oracle["binding_id"],
        "oracle_sha256": oracle["sha256"],
        "implementation_owner": rust_document["implementation_owner"],
        "provenance_verdict": "independent",
        "frozen_corpus_order": list(order),
        "vector_results": vector_results,
        "all_equivalent": all_equivalent,
        "disposition": (
            "selected-parity-observed"
            if all_equivalent
            else "selected-mismatch-observed"
        ),
        "claim_id": "CLAIM-CROSS-LANGUAGE-SELECTED-PARITY",
        "claim_supported": all_equivalent,
        "claim_ceiling": (
            "independently produced observations agree only for the selected frozen corpus"
            if all_equivalent
            else "independently produced observations differ within the selected frozen corpus"
        ),
        "semantic_acceptance": False,
        "authority_effect": "none",
    }
