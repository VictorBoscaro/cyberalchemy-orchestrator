"""The frozen ``aci-cjson-1`` projection and digest boundary."""

from __future__ import annotations

import hashlib
import json
import math
import unicodedata
from collections.abc import Mapping, Sequence
from typing import Any

from .errors import ValidationError


def _project(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, str)):
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
