"""Fixture digest helpers shared by the generator and contract tests."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def canonical_bytes(value: Any) -> bytes:
    """RFC 8785-compatible encoding for this corpus (objects, arrays, strings, ints)."""
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def fixture_digest(fixture: dict[str, Any]) -> str:
    unsigned = {key: value for key, value in fixture.items() if key != "sha256"}
    return hashlib.sha256(canonical_bytes(unsigned)).hexdigest()


def load_fixture(path: Path, *, expected_digest: str | None = None) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    actual = fixture_digest(fixture)
    if fixture.get("sha256") != actual:
        raise ValueError(f"{path.name}: embedded fixture digest mismatch")
    if expected_digest is not None and expected_digest != actual:
        raise ValueError(f"{path.name}: manifest fixture digest mismatch")
    return fixture
