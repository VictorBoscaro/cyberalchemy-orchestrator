"""Strict admission oracle for the RWO JSON and version profile."""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass
from typing import Any

from .canonical import (
    SAFE_INTEGER_MAXIMUM,
    SAFE_INTEGER_MINIMUM,
    CanonicalizationError,
    canonical_payload_bytes,
)


CONTRACT_ID = "RWO-SEMANTIC-CONTRACT"
CONTRACT_VERSION = "1.0.0"
PROFILE_ID = "RWO-JCS-IJSON-SAFEINT"
PROFILE_VERSION = "1.0.0"
UNICODE_VERSION = "15.1.0"
# CPython's bundled Unicode database may lag the contract profile. The host
# used by this prototype exposes 15.0.0, so carry the complete 15.1 assignment
# delta locally. These scalars are assigned in 15.1 and therefore must not be
# rejected merely because the host table still reports category Cn.
# Source: Unicode 15.1.0 UCD DerivedAge.txt, entries with age 15.1.
UNICODE_15_1_ASSIGNMENT_DELTA = (
    (0x2FFC, 0x2FFF),
    (0x31EF, 0x31EF),
    (0x2EBF0, 0x2EE5D),
)
INTEGER_TOKEN = re.compile(r"(?:0|-[1-9][0-9]*|[1-9][0-9]*)\Z")
CANONICAL_DECIMAL = re.compile(
    r"(?:0|-?(?:[1-9][0-9]*)(?:\.[0-9]*[1-9])?|-?0\.[0-9]*[1-9])\Z"
)
_PHASE_RANK = {
    "decode": 0,
    "admission": 1,
    "schema": 2,
    "normalization": 3,
}


@dataclass(frozen=True)
class Defect:
    phase: str
    code: str
    path: tuple[str | int, ...] = ()


@dataclass(frozen=True)
class AdmissionResult:
    value: Any | None
    payload_bytes: bytes | None
    defects: tuple[Defect, ...]

    @property
    def admitted(self) -> bool:
        return not self.defects


@dataclass(frozen=True)
class VersionTuple:
    contract_id: str
    contract_version: str
    profile_id: str
    profile_version: str
    schema_id: str
    schema_version: str
    value_type: str


@dataclass(frozen=True)
class VersionRegistry:
    contract_id: str
    contract_version: str
    profile_id: str
    profile_version: str
    schemas: dict[tuple[str, str], frozenset[str]]

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> "VersionRegistry":
        schemas: dict[tuple[str, str], frozenset[str]] = {}
        for schema in document.get("schemas", []):
            schemas[(schema["schemaId"], schema["schemaVersion"])] = frozenset(
                schema["valueTypes"]
            )
        return cls(
            contract_id=document["contract"]["id"],
            contract_version=document["contract"]["version"],
            profile_id=document["profile"]["id"],
            profile_version=document["profile"]["version"],
            schemas=schemas,
        )

    def admits(self, value: VersionTuple) -> bool:
        return (
            value.contract_id == self.contract_id
            and value.contract_version == self.contract_version
            and value.profile_id == self.profile_id
            and value.profile_version == self.profile_version
            and value.value_type
            in self.schemas.get((value.schema_id, value.schema_version), frozenset())
        )


@dataclass(frozen=True)
class _RawNumber:
    token: str


class _DuplicateName(ValueError):
    pass


class _NumericConstant(ValueError):
    pass


def _path_key(path: tuple[str | int, ...]) -> tuple[tuple[int, Any], ...]:
    return tuple((0, segment.encode("utf-16-be")) if isinstance(segment, str) else (1, segment) for segment in path)


def _ordered(defects: list[Defect]) -> tuple[Defect, ...]:
    return tuple(
        sorted(
            defects,
            key=lambda item: (
                _PHASE_RANK[item.phase],
                _path_key(item.path),
                item.code.encode("ascii"),
            ),
        )
    )


def _rejected(*defects: Defect) -> AdmissionResult:
    return AdmissionResult(None, None, _ordered(list(defects)))


def admit_version_tuple(
    value: VersionTuple, registry: VersionRegistry
) -> tuple[Defect, ...]:
    if registry.admits(value):
        return ()
    return (Defect("admission", "VERSION_TUPLE_UNSUPPORTED"),)


def _object_from_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateName(key)
        result[key] = value
    return result


def _parse(raw: bytes) -> tuple[Any | None, list[Defect]]:
    if raw.startswith(b"\xef\xbb\xbf"):
        return None, [Defect("decode", "UTF8_BOM_FORBIDDEN")]
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None, [Defect("decode", "INVALID_UTF8")]

    decoder = json.JSONDecoder(
        object_pairs_hook=_object_from_pairs,
        parse_int=_RawNumber,
        parse_float=_RawNumber,
        parse_constant=lambda token: (_ for _ in ()).throw(_NumericConstant(token)),
        strict=True,
    )
    try:
        start = len(text) - len(text.lstrip(" \t\r\n"))
        value, end = decoder.raw_decode(text, start)
    except _DuplicateName:
        return None, [Defect("admission", "DUPLICATE_OBJECT_NAME")]
    except _NumericConstant:
        return None, [Defect("admission", "NON_CANONICAL_INTEGER")]
    except json.JSONDecodeError:
        return None, [Defect("decode", "INVALID_JSON")]
    if any(character not in " \t\r\n" for character in text[end:]):
        return None, [Defect("decode", "TRAILING_TOKEN")]
    return value, []


def _is_noncharacter(codepoint: int) -> bool:
    return 0xFDD0 <= codepoint <= 0xFDEF or codepoint & 0xFFFF in (0xFFFE, 0xFFFF)


def _is_assigned_in_pinned_unicode(codepoint: int, character: str) -> bool:
    if any(start <= codepoint <= end for start, end in UNICODE_15_1_ASSIGNMENT_DELTA):
        return True
    return unicodedata.category(character) != "Cn"


def _check_string(value: str, path: tuple[str | int, ...]) -> list[Defect]:
    for character in value:
        codepoint = ord(character)
        if 0xD800 <= codepoint <= 0xDFFF:
            return [Defect("admission", "INVALID_UNICODE_SCALAR", path)]
        if _is_noncharacter(codepoint):
            return [Defect("admission", "UNICODE_NONCHARACTER", path)]
        if not _is_assigned_in_pinned_unicode(codepoint, character):
            return [Defect("admission", "UNICODE_UNASSIGNED", path)]
    if unicodedata.normalize("NFC", value) != value:
        return [Defect("admission", "NON_NFC_TEXT", path)]
    return []


def _admit_value(
    value: Any, path: tuple[str | int, ...] = ()
) -> tuple[Any, list[Defect]]:
    if isinstance(value, _RawNumber):
        if not INTEGER_TOKEN.fullmatch(value.token):
            return None, [Defect("admission", "NON_CANONICAL_INTEGER", path)]
        integer = int(value.token)
        if integer < SAFE_INTEGER_MINIMUM or integer > SAFE_INTEGER_MAXIMUM:
            return None, [Defect("admission", "INTEGER_OUT_OF_RANGE", path)]
        return integer, []
    if isinstance(value, str):
        return value, _check_string(value, path)
    if isinstance(value, list):
        result: list[Any] = []
        defects: list[Defect] = []
        for index, member in enumerate(value):
            admitted, member_defects = _admit_value(member, path + (index,))
            result.append(admitted)
            defects.extend(member_defects)
        return result, defects
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        defects: list[Defect] = []
        for key, member in value.items():
            defects.extend(_check_string(key, path + (key,)))
            admitted, member_defects = _admit_value(member, path + (key,))
            result[key] = admitted
            defects.extend(member_defects)
        return result, defects
    if value is None or isinstance(value, bool):
        return value, []
    return None, [Defect("admission", "UNSUPPORTED_JSON_VALUE", path)]


def _json_type_matches(value: Any, expected: str) -> bool:
    if expected == "null":
        return value is None
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "string":
        return isinstance(value, str)
    if expected == "array":
        return isinstance(value, list)
    if expected == "object":
        return isinstance(value, dict)
    return False


def _resolve_ref(root: dict[str, Any], reference: str) -> dict[str, Any] | None:
    if not reference.startswith("#/"):
        return None
    current: Any = root
    for raw_segment in reference[2:].split("/"):
        segment = raw_segment.replace("~1", "/").replace("~0", "~")
        if not isinstance(current, dict) or segment not in current:
            return None
        current = current[segment]
    return current if isinstance(current, dict) else None


def _validate_schema(
    value: Any,
    schema: dict[str, Any],
    root: dict[str, Any],
    path: tuple[str | int, ...] = (),
) -> list[Defect]:
    reference = schema.get("$ref")
    if reference is not None:
        resolved = _resolve_ref(root, reference)
        if resolved is None:
            return [Defect("schema", "SCHEMA_REFERENCE_UNRESOLVED", path)]
        return _validate_schema(value, resolved, root, path)

    branches = schema.get("oneOf")
    if branches is not None:
        results = [_validate_schema(value, branch, root, path) for branch in branches]
        if sum(not result for result in results) != 1:
            return [Defect("schema", "SCHEMA_ONE_OF_MISMATCH", path)]
        return []

    defects: list[Defect] = []
    expected = schema.get("type")
    if expected is not None:
        expected_types = [expected] if isinstance(expected, str) else expected
        if not any(_json_type_matches(value, item) for item in expected_types):
            return [Defect("schema", "SCHEMA_TYPE_MISMATCH", path)]
    if "const" in schema and value != schema["const"]:
        defects.append(Defect("schema", "INVALID_CONST", path))
    if "enum" in schema and value not in schema["enum"]:
        defects.append(Defect("schema", "INVALID_ENUM_VALUE", path))

    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for name in schema.get("required", []):
            if name not in value:
                defects.append(Defect("schema", "REQUIRED_FIELD_MISSING", path + (name,)))
        if schema.get("additionalProperties") is False:
            for name in value.keys() - properties.keys():
                defects.append(Defect("schema", "UNKNOWN_FIELD", path + (name,)))
        for name, member in value.items():
            if name in properties:
                defects.extend(
                    _validate_schema(member, properties[name], root, path + (name,))
                )
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            defects.append(Defect("schema", "ARRAY_TOO_SHORT", path))
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, member in enumerate(value):
                defects.extend(
                    _validate_schema(member, item_schema, root, path + (index,))
                )
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            defects.append(Defect("schema", "STRING_TOO_SHORT", path))
        pattern = schema.get("pattern")
        if pattern is not None and re.search(pattern, value) is None:
            defects.append(Defect("schema", "PATTERN_MISMATCH", path))
    if isinstance(value, int) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            defects.append(Defect("schema", "NUMBER_OUT_OF_RANGE", path))
        if "maximum" in schema and value > schema["maximum"]:
            defects.append(Defect("schema", "NUMBER_OUT_OF_RANGE", path))
    return defects


def admit_json(
    raw_utf8_json: bytes,
    *,
    version_tuple: VersionTuple | None = None,
    registry: VersionRegistry | None = None,
    schema: dict[str, Any] | None = None,
) -> AdmissionResult:
    """Admit raw JSON without losing duplicate names or raw number lexemes."""

    if not isinstance(raw_utf8_json, bytes):
        raise TypeError("raw_utf8_json must be bytes")
    if (version_tuple is None) != (registry is None):
        raise ValueError("version_tuple and registry must be supplied together")
    if version_tuple is not None and registry is not None:
        tuple_defects = admit_version_tuple(version_tuple, registry)
        if tuple_defects:
            return AdmissionResult(None, None, tuple_defects)

    parsed, defects = _parse(raw_utf8_json)
    if defects:
        return AdmissionResult(None, None, _ordered(defects))
    admitted, value_defects = _admit_value(parsed)
    defects.extend(value_defects)
    if not defects and schema is not None:
        defects.extend(_validate_schema(admitted, schema, schema))
    if defects:
        return AdmissionResult(None, None, _ordered(defects))
    try:
        payload = canonical_payload_bytes(admitted)
    except CanonicalizationError:
        return _rejected(Defect("admission", "CANONICALIZATION_FAILED"))
    return AdmissionResult(admitted, payload, ())


def admit_canonical_decimal(raw_utf8_json: bytes) -> AdmissionResult:
    """Admit one JSON string under the schema-owned canonical-decimal rule."""

    result = admit_json(raw_utf8_json)
    if not result.admitted:
        return result
    if not isinstance(result.value, str) or not CANONICAL_DECIMAL.fullmatch(result.value):
        return _rejected(Defect("schema", "NON_CANONICAL_DECIMAL"))
    return result
