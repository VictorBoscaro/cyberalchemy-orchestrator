"""Deterministic canonical bytes and typed digests for the RWO profile.

This module is deliberately pure and standard-library only.  It owns neither
schema admission nor any orchestration behavior.
"""

from __future__ import annotations

import hashlib
import json
import re
import struct
from collections.abc import Mapping, Sequence
from typing import Any


SAFE_INTEGER_MINIMUM = -9_007_199_254_740_991
SAFE_INTEGER_MAXIMUM = 9_007_199_254_740_991
_IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9._/-]*\Z")


class CanonicalizationError(ValueError):
    """The value cannot be represented by the pinned canonical profile."""


class DuplicateSemanticIdentity(CanonicalizationError):
    """Two order-insensitive elements have one identical semantic identity."""


def utf16_sort_key(value: str) -> bytes:
    """Return unsigned UTF-16 code units in their comparison byte order."""

    if not isinstance(value, str):
        raise CanonicalizationError("object names must be strings")
    try:
        return value.encode("utf-16-be")
    except UnicodeEncodeError as error:
        raise CanonicalizationError("surrogate code points are forbidden") from error


def _encode_string(value: str) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
        ).encode("utf-8")
    except (UnicodeEncodeError, ValueError) as error:
        raise CanonicalizationError("string is outside the canonical profile") from error


def canonical_payload_bytes(value: Any) -> bytes:
    """Serialize one already-admitted value as RFC 8785-compatible JSON bytes."""

    if value is None:
        return b"null"
    if value is True:
        return b"true"
    if value is False:
        return b"false"
    if isinstance(value, int):
        if value < SAFE_INTEGER_MINIMUM or value > SAFE_INTEGER_MAXIMUM:
            raise CanonicalizationError("integer is outside the safe profile")
        return str(value).encode("ascii")
    if isinstance(value, float):
        raise CanonicalizationError("binary floats are not admitted")
    if isinstance(value, str):
        return _encode_string(value)
    if isinstance(value, Mapping):
        members: list[bytes] = []
        for key in sorted(value, key=utf16_sort_key):
            if not isinstance(key, str):
                raise CanonicalizationError("object names must be strings")
            members.append(
                _encode_string(key) + b":" + canonical_payload_bytes(value[key])
            )
        return b"{" + b",".join(members) + b"}"
    if isinstance(value, Sequence) and not isinstance(
        value, (str, bytes, bytearray, memoryview)
    ):
        return b"[" + b",".join(canonical_payload_bytes(item) for item in value) + b"]"
    raise CanonicalizationError(f"unsupported canonical value: {type(value).__name__}")


def _resolve_key_path(value: Any, path: str) -> Any:
    if path == "$":
        return value
    current = value
    for segment in path.split("."):
        if not isinstance(current, Mapping) or segment not in current:
            raise CanonicalizationError(f"primary-key path is absent: {path}")
        current = current[segment]
    return current


def _component_key(value: Any) -> tuple[int, Any]:
    if isinstance(value, bool):
        raise CanonicalizationError("boolean primary-key components are unsupported")
    if isinstance(value, int):
        return (0, value)
    if isinstance(value, str):
        return (1, utf16_sort_key(value))
    if isinstance(value, (bytes, bytearray, memoryview)):
        return (2, bytes(value))
    raise CanonicalizationError(
        f"unsupported primary-key component: {type(value).__name__}"
    )


def normalize_semantic_collection(
    elements: Sequence[Any],
    primary_key_paths: Sequence[str],
    *,
    duplicate_policy: str = "reject",
) -> list[Any]:
    """Normalize an order-insensitive collection under the version-one rule."""

    if duplicate_policy != "reject":
        raise CanonicalizationError("only duplicatePolicy=reject is supported")
    if not primary_key_paths:
        raise CanonicalizationError("at least one primary-key path is required")

    decorated: list[tuple[tuple[tuple[int, Any], ...], bytes, Any]] = []
    for element in elements:
        primary = tuple(
            _component_key(_resolve_key_path(element, path))
            for path in primary_key_paths
        )
        payload = canonical_payload_bytes(element)
        decorated.append((primary, payload, element))
    decorated.sort(key=lambda item: (item[0], item[1]))

    previous: tuple[tuple[tuple[int, Any], ...], bytes] | None = None
    for primary, payload, _ in decorated:
        identity = (primary, payload)
        if identity == previous:
            raise DuplicateSemanticIdentity("duplicate semantic identity")
        previous = identity
    return [element for _, _, element in decorated]


def _framed_text(value: str) -> bytes:
    if not isinstance(value, str) or not _IDENTIFIER.fullmatch(value):
        raise CanonicalizationError("digest tuple identifiers use the closed grammar")
    encoded = value.encode("utf-8")
    if len(encoded) > 0xFFFF_FFFF:
        raise CanonicalizationError("digest tuple text is too large")
    return struct.pack(">I", len(encoded)) + encoded


def _framed_blob(value: bytes) -> bytes:
    if not isinstance(value, bytes):
        raise CanonicalizationError("payload bytes must be immutable bytes")
    if len(value) > 0xFFFF_FFFF_FFFF_FFFF:
        raise CanonicalizationError("payload is too large")
    return struct.pack(">Q", len(value)) + value


def semantic_digest(
    contract_id: str,
    contract_version: str,
    profile_id: str,
    profile_version: str,
    schema_id: str,
    schema_version: str,
    value_type: str,
    payload_bytes: bytes,
) -> str:
    """Derive the length-framed RWO semantic digest."""

    preimage = b"RWO-SEMANTIC-DIGEST\x00" + b"".join(
        _framed_text(value)
        for value in (
            contract_id,
            contract_version,
            profile_id,
            profile_version,
            schema_id,
            schema_version,
            value_type,
        )
    )
    preimage += _framed_blob(payload_bytes)
    return "sha256:" + hashlib.sha256(preimage).hexdigest()
