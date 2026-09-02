"""Strict, read-only resolver for validated-appender dispatch rows."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .canonical import canonical_digest, digest_bytes, parse_strict_json
from .errors import IntegrityError, NotFoundError

ROW_RE = re.compile(rb"^(  - |    )([A-Za-z_][A-Za-z0-9_]*): (.*)$")
SUPPORTED_OPENING_CONTRACTS = {"0.6.1", "0.6.2", "0.6.3", "0.6.4", "0.7.0"}


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
    agent_role_registry_ref: dict[str, str] | None = None


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
        role_ref = row.get("agent_role_registry_ref")
        if contract_version == "0.7.0":
            if (
                not isinstance(role_ref, dict)
                or set(role_ref) != {"name", "version", "digest"}
                or any(not isinstance(role_ref.get(key), str) or not role_ref[key] for key in ("name", "version"))
                or not isinstance(role_ref.get("digest"), str)
                or not re.fullmatch(r"sha256:[0-9a-f]{64}", role_ref["digest"])
            ):
                raise IntegrityError("0.7.0 dispatch row has no valid agent role registry ref")
        elif role_ref is not None:
            raise IntegrityError("legacy dispatch row must not retrofit an agent role registry ref")
        return LegacyDispatchSnapshot(
            dispatch_id=dispatch_id,
            ledger_path=str(path),
            ledger_digest=digest_bytes(raw),
            row_bytes_digest=digest_bytes(row_bytes),
            row_digest=canonical_digest(row),
            row=row,
            contract_version=contract_version,
            row_kind=row_kind,
            agent_role_registry_ref=role_ref,
        )

    @staticmethod
    def _opening_contract_version(row: dict[str, Any], *, row_kind: str) -> str:
        if row_kind != "opening":
            contract_version = row.get("schema_version")
            if contract_version is None:
                return "0.6.1"
            if contract_version != "0.7.0":
                raise IntegrityError("dispatch close is neither legacy nor supported 0.7.0")
            return contract_version
        contract_version = row.get("schema_version")
        if contract_version not in SUPPORTED_OPENING_CONTRACTS:
            raise IntegrityError(
                "dispatch opening is not a supported 0.6.1, 0.6.2, 0.6.3, 0.6.4, or 0.7.0 contract"
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
        closing = self._resolve(
            path,
            dispatch_id,
            identity_field="close_of",
            row_kind="close",
        )
        opening = self.resolve(path, dispatch_id)
        if "0.7.0" in {opening.contract_version, closing.contract_version}:
            if opening.contract_version != closing.contract_version:
                raise IntegrityError("mixed legacy/0.7.0 opening and close are forbidden")
            if opening.agent_role_registry_ref != closing.agent_role_registry_ref:
                raise IntegrityError("opening/close agent role registry refs differ")
        return closing

    def verify_unchanged(self, snapshot: LegacyDispatchSnapshot) -> None:
        current = Path(snapshot.ledger_path).read_bytes()
        if digest_bytes(current) != snapshot.ledger_digest:
            raise IntegrityError("legacy ledger changed after snapshot resolution")
