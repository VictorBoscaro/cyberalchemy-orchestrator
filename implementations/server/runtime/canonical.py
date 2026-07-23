"""The frozen ``aci-cjson-1`` projection and digest boundary."""

from __future__ import annotations

import hashlib
import json
import math
import unicodedata
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from collections.abc import Mapping, Sequence
from typing import Any

from .errors import ValidationError


def _project(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, str)):
        if isinstance(value, int) and not isinstance(value, bool):
            if value < -(2**63) or value > 2**63 - 1:
                raise ValidationError("integer is outside signed int64")
        if isinstance(value, str):
            return unicodedata.normalize("NFC", value)
        return value
    if isinstance(value, float):
        # This bounded slice rejects binary floats instead of allowing a
        # language serializer to define semantic identity.
        if not math.isfinite(value):
            raise ValidationError("non-finite numbers are forbidden")
        raise ValidationError("binary floats are not admitted by aci-cjson-1")
    if isinstance(value, Mapping):
        projected: dict[str, Any] = {}
        for key, member in value.items():
            if not isinstance(key, str):
                raise ValidationError("canonical object keys must be strings")
            normalized = unicodedata.normalize("NFC", key)
            if normalized in projected:
                raise ValidationError("object keys collide after NFC normalization")
            projected[normalized] = _project(member)
        return {key: projected[key] for key in sorted(projected)}
    if isinstance(value, Sequence) and not isinstance(
        value, (str, bytes, bytearray, memoryview)
    ):
        return [_project(member) for member in value]
    raise ValidationError(f"unsupported canonical value: {type(value).__name__}")


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        _project(value),
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
    ).encode("utf-8")


def digest_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def canonical_digest(value: Any) -> str:
    return digest_bytes(canonical_bytes(value))


def canonical_text(value: Any) -> str:
    return canonical_bytes(value).decode("utf-8")


_FIXTURE_SCHEMAS = {
    "aci.fixture.contract@1": (
        {"schema_version", "label", "items", "count", "amount", "occurred_at"},
        {"metadata"},
        "aci.contract@1",
    ),
    "aci.fixture.contract@2": (
        {"schema_version", "label", "items", "count", "amount", "occurred_at"},
        {"metadata"},
        "aci.contract@2",
    ),
    "aci.fixture.integer@1": (
        {"schema_version", "value"},
        set(),
        "aci.integer@1",
    ),
    "aci.fixture.timestamp@1": (
        {"schema_version", "occurred_at"},
        set(),
        "aci.timestamp@1",
    ),
    "aci.fixture.decimal@1": (
        {"schema_version", "amount"},
        set(),
        "aci.decimal@1",
    ),
    "aci.fixture.numeric-boundaries@1": (
        {"schema_version", "minimum", "maximum", "amount", "occurred_at"},
        set(),
        "aci.contract@1",
    ),
}


def project_for_schema(value: Any, schema_ref: str) -> Any:
    """Frozen Stage-A fixture projections used to prove the canonical boundary."""
    if schema_ref == "aci.fixture.unicode-object@1":
        if not isinstance(value, dict) or "schema_version" not in value:
            raise ValidationError("unicode fixture requires schema_version")
        return _project(value)
    try:
        required, optional, schema_version = _FIXTURE_SCHEMAS[schema_ref]
    except KeyError as exc:
        raise ValidationError(f"unknown canonical projection schema: {schema_ref}") from exc
    if not isinstance(value, dict):
        raise ValidationError("schema projection requires an object")
    fields = set(value)
    if not required.issubset(fields) or fields - required - optional:
        raise ValidationError("schema has missing or unknown fields")
    if value["schema_version"] != schema_version:
        raise ValidationError("schema_version does not match target schema")
    result = dict(value)
    for name in ("count", "value", "minimum", "maximum"):
        if name in result:
            member = result[name]
            if isinstance(member, bool) or not isinstance(member, int):
                raise ValidationError(f"{name} must be int64")
            if member < -(2**63) or member > 2**63 - 1:
                raise ValidationError(f"{name} is outside signed int64")
    if "amount" in result:
        result["amount"] = _canonical_decimal(result["amount"])
    if "occurred_at" in result:
        result["occurred_at"] = _canonical_timestamp(result["occurred_at"])
    return _project(result)


def canonical_bytes_for_schema(value: Any, schema_ref: str) -> bytes:
    return canonical_bytes(project_for_schema(value, schema_ref))


def _canonical_decimal(value: Any) -> str:
    if not isinstance(value, str):
        raise ValidationError("decimal contract fields must be strings")
    if "e" in value.lower():
        raise ValidationError("decimal exponent notation is forbidden")
    try:
        number = Decimal(value)
    except InvalidOperation as exc:
        raise ValidationError("invalid decimal string") from exc
    if not number.is_finite():
        raise ValidationError("non-finite decimal is forbidden")
    if number == 0:
        return "0"
    rendered = format(number, "f")
    if "." in rendered:
        rendered = rendered.rstrip("0").rstrip(".")
    if rendered.startswith("+"):
        rendered = rendered[1:]
    negative = rendered.startswith("-")
    body = rendered[1:] if negative else rendered
    integer, dot, fraction = body.partition(".")
    integer = integer.lstrip("0") or "0"
    return ("-" if negative else "") + integer + (dot + fraction if dot else "")


def _canonical_timestamp(value: Any) -> str:
    if not isinstance(value, str):
        raise ValidationError("timestamp must be a string")
    if value.endswith("Z"):
        parsed_text = value[:-1] + "+00:00"
    else:
        parsed_text = value
    try:
        parsed = datetime.fromisoformat(parsed_text)
    except ValueError as exc:
        raise ValidationError("invalid RFC3339 timestamp") from exc
    if parsed.tzinfo is None:
        raise ValidationError("timestamp timezone is required")
    if "." in value:
        fraction = value.split(".", 1)[1].split("Z", 1)[0].split("+", 1)[0]
        if len(fraction.split("-", 1)[0]) > 3:
            raise ValidationError("timestamp precision would be lost")
    utc = parsed.astimezone(timezone.utc)
    if utc.microsecond % 1000:
        raise ValidationError("timestamp precision would be lost")
    return utc.strftime("%Y-%m-%dT%H:%M:%S.") + f"{utc.microsecond // 1000:03d}Z"


def parse_strict_json(data: bytes | str) -> Any:
    def reject_duplicate(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValidationError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    text = data.decode("utf-8") if isinstance(data, bytes) else data
    try:
        value = json.loads(
            text,
            object_pairs_hook=reject_duplicate,
            parse_constant=lambda token: (_ for _ in ()).throw(
                ValidationError(f"invalid numeric constant: {token}")
            ),
        )
    except UnicodeDecodeError as exc:
        raise ValidationError("JSON is not valid UTF-8") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(f"invalid JSON: {exc.msg}") from exc
    _project(value)
    return value
