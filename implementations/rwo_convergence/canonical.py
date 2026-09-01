"""Closed canonical JSON and byte-tree primitives for RWO-CVG-001.

The format is deliberately smaller than generic JSON: duplicate names, floats,
unsafe integers, non-ASCII object names, non-NFC strings, and lone surrogates
are rejected.  Canonical documents are compact UTF-8 JSON followed by one LF.
"""

from __future__ import annotations

import hashlib
import json
import unicodedata
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

MAX_SAFE_INTEGER = 9_007_199_254_740_991
MIN_SAFE_INTEGER = -MAX_SAFE_INTEGER


class CanonicalizationError(ValueError):
    """Input cannot be represented by the closed canonical format."""


def _pairs_no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CanonicalizationError(f"duplicate object name: {key!r}")
        result[key] = value
    return result


def _reject_float(value: str) -> None:
    raise CanonicalizationError(f"floating-point number is forbidden: {value}")


def _parse_int(value: str) -> int:
    parsed = int(value, 10)
    if not MIN_SAFE_INTEGER <= parsed <= MAX_SAFE_INTEGER:
        raise CanonicalizationError(f"integer outside safe range: {value}")
    return parsed


def _reject_constant(value: str) -> None:
    raise CanonicalizationError(f"non-finite number is forbidden: {value}")


def load_json_bytes(data: bytes) -> Any:
    """Parse UTF-8 JSON while preserving every rejection invariant."""

    try:
        text = data.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise CanonicalizationError("input is not valid UTF-8") from exc
    try:
        value = json.loads(
            text,
            object_pairs_hook=_pairs_no_duplicates,
            parse_float=_reject_float,
            parse_int=_parse_int,
            parse_constant=_reject_constant,
        )
    except CanonicalizationError:
        raise
    except json.JSONDecodeError as exc:
        raise CanonicalizationError(f"invalid JSON: {exc.msg}") from exc
    validate_value(value)
    return value


def load_json_file(path: Path | str) -> Any:
    return load_json_bytes(Path(path).read_bytes())


def _validate_string(value: str, *, object_name: bool = False) -> None:
    if any(0xD800 <= ord(char) <= 0xDFFF for char in value):
        raise CanonicalizationError("lone UTF-16 surrogate is forbidden")
    if unicodedata.normalize("NFC", value) != value:
        raise CanonicalizationError("string is not Unicode NFC")
    if object_name and (not value.isascii()):
        raise CanonicalizationError(f"non-ASCII object name: {value!r}")


def validate_value(value: Any) -> None:
    """Validate a Python value before canonical encoding."""

    if value is None or isinstance(value, bool):
        return
    if isinstance(value, int):
        if not MIN_SAFE_INTEGER <= value <= MAX_SAFE_INTEGER:
            raise CanonicalizationError(f"integer outside safe range: {value}")
        return
    if isinstance(value, float):
        raise CanonicalizationError("floating-point numbers are forbidden")
    if isinstance(value, str):
        _validate_string(value)
        return
    if isinstance(value, list):
        for item in value:
            validate_value(item)
        return
    if isinstance(value, Mapping):
        for key, item in value.items():
            if not isinstance(key, str):
                raise CanonicalizationError("object names must be strings")
            _validate_string(key, object_name=True)
            validate_value(item)
        return
    raise CanonicalizationError(f"unsupported value type: {type(value).__name__}")


def canonical_json_bytes(value: Any) -> bytes:
    validate_value(value)
    try:
        encoded = json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise CanonicalizationError(str(exc)) from exc
    return encoded + b"\n"


def assert_canonical_json(data: bytes) -> Any:
    value = load_json_bytes(data)
    if canonical_json_bytes(value) != data:
        raise CanonicalizationError("JSON bytes are not canonical")
    return value


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path | str) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


@dataclass(frozen=True, slots=True)
class TreeMember:
    path: str
    size_bytes: int
    sha256: str

    def frame(self) -> bytes:
        path_bytes = self.path.encode("utf-8", "strict")
        return (
            path_bytes
            + b"\0"
            + str(self.size_bytes).encode("ascii")
            + b"\0"
            + self.sha256.encode("ascii")
            + b"\n"
        )


def tree_digest(members: Iterable[TreeMember]) -> str:
    ordered = sorted(members, key=lambda item: item.path.encode("utf-8"))
    seen: set[bytes] = set()
    digest = hashlib.sha256()
    for member in ordered:
        key = member.path.encode("utf-8", "strict")
        if key in seen:
            raise CanonicalizationError(f"duplicate tree path: {member.path}")
        seen.add(key)
        if member.size_bytes < 0:
            raise CanonicalizationError("negative tree member size")
        if len(member.sha256) != 64 or any(c not in "0123456789abcdef" for c in member.sha256):
            raise CanonicalizationError("invalid lowercase SHA-256")
        digest.update(member.frame())
    return digest.hexdigest()


def require_exact_fields(value: Mapping[str, Any], expected: set[str], *, where: str) -> None:
    actual = set(value)
    if actual != expected:
        missing = sorted(expected - actual)
        unknown = sorted(actual - expected)
        raise CanonicalizationError(f"{where}: missing={missing}, unknown={unknown}")
