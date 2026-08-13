"""Strict, read-only resolver for validated-appender dispatch rows."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .canonical import canonical_digest, digest_bytes, parse_strict_json
from .errors import IntegrityError, NotFoundError

ROW_RE = re.compile(rb"^(  - |    )([A-Za-z_][A-Za-z0-9_]*): (.*)$")
SUPPORTED_OPENING_CONTRACTS = {"0.6.1", "0.6.2", "0.6.3", "0.6.4"}


@dataclass(frozen=True)
class LegacyDispatchSnapshot:
    dispatch_id: str
    ledger_path: str
    ledger_digest: str
    row_bytes_digest: str
    row_digest: str
    row: dict[str, Any]
    appender_identity: str = "register-dispatch/append-dispatch.cjs"
    contract_version: str = "0.6.1"
    row_kind: str = "opening"


class StrictLegacySnapshotResolver:
    def _rows(self, path: Path) -> tuple[Path, bytes, list[tuple[dict[str, Any], bytes]]]:
        path = Path(path).resolve()
        raw = path.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            raise IntegrityError("legacy ledger BOM is forbidden")
        try:
            raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise IntegrityError("legacy ledger is not UTF-8") from exc
        rows: list[tuple[dict[str, Any], bytes]] = []
        current: dict[str, Any] | None = None
        current_lines: list[bytes] = []
        root_seen = 0
        for line in raw.splitlines(keepends=True):
            bare = line.rstrip(b"\r\n")
            if not bare or bare.startswith(b"#"):
                continue
            if bare == b"dispatches:":
                root_seen += 1
                if root_seen != 1 or current is not None or rows:
                    raise IntegrityError("legacy ledger root is duplicated or misplaced")
                continue
            match = ROW_RE.fullmatch(bare)
            if not match or root_seen != 1:
                raise IntegrityError("legacy ledger line violates appender grammar")
            prefix, key_bytes, json_bytes = match.groups()
            key = key_bytes.decode("ascii")
            try:
                value = parse_strict_json(json_bytes)
            except Exception as exc:
                raise IntegrityError(f"invalid legacy JSON column: {key}") from exc
            if prefix == b"  - ":
                if current is not None:
                    rows.append((current, b"".join(current_lines)))
                if key not in {"dispatch_id", "close_of"}:
                    raise IntegrityError("legacy row must begin with dispatch_id or close_of")
                current = {}
                current_lines = []
            elif current is None:
                raise IntegrityError("orphan legacy continuation")
            assert current is not None
            if key in current:
                raise IntegrityError(f"duplicate legacy row field: {key}")
            current[key] = value
            current_lines.append(line)
        if current is not None:
            rows.append((current, b"".join(current_lines)))
        if root_seen != 1:
            raise IntegrityError("legacy ledger must contain one dispatches root")
        return path, raw, rows

    def _resolve(
        self, path: Path, dispatch_id: str, *, identity_field: str, row_kind: str
    ) -> LegacyDispatchSnapshot:
        path, raw, rows = self._rows(path)
        matches = [
            (row, row_bytes)
            for row, row_bytes in rows
            if row.get(identity_field) == dispatch_id
        ]
        if len(matches) != 1:
            if not matches:
                raise NotFoundError(f"dispatch {row_kind} not found")
            raise IntegrityError(f"ambiguous duplicate dispatch {row_kind}")
        row, row_bytes = matches[0]
        contract_version = self._opening_contract_version(row, row_kind=row_kind)
        return LegacyDispatchSnapshot(
            dispatch_id=dispatch_id,
            ledger_path=str(path),
            ledger_digest=digest_bytes(raw),
            row_bytes_digest=digest_bytes(row_bytes),
            row_digest=canonical_digest(row),
            row=row,
            contract_version=contract_version,
            row_kind=row_kind,
        )

    @staticmethod
    def _opening_contract_version(row: dict[str, Any], *, row_kind: str) -> str:
        if row_kind != "opening":
            return "0.6.1"
        contract_version = row.get("schema_version")
        if contract_version not in SUPPORTED_OPENING_CONTRACTS:
            raise IntegrityError(
                "dispatch opening is not a supported 0.6.1, 0.6.2, 0.6.3, or 0.6.4 contract"
            )
        return contract_version

    def resolve(self, path: Path, dispatch_id: str) -> LegacyDispatchSnapshot:
        return self._resolve(
            path,
            dispatch_id,
            identity_field="dispatch_id",
            row_kind="opening",
        )

    def resolve_close(self, path: Path, dispatch_id: str) -> LegacyDispatchSnapshot:
        return self._resolve(
            path,
            dispatch_id,
            identity_field="close_of",
            row_kind="close",
        )

    def verify_unchanged(self, snapshot: LegacyDispatchSnapshot) -> None:
        current = Path(snapshot.ledger_path).read_bytes()
        if digest_bytes(current) != snapshot.ledger_digest:
            raise IntegrityError("legacy ledger changed after snapshot resolution")
