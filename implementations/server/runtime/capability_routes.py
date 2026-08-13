"""Immutable capability-route receipts for specialized and generic dispatch types."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .canonical import canonical_digest, digest_bytes
from .errors import GateBlockedError, ValidationError


ROUTE_SCHEMA = "aci-capability-route/v1"
_CAPABILITY_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_FRONTMATTER_NAME = re.compile(r"(?m)^name:\s*[\"']?([^\s\"']+)[\"']?\s*$")


def registry_digest(repo_root: Path, registry_path: Path) -> str:
    path = (Path(repo_root).resolve() / registry_path).resolve()
    return digest_bytes(path.read_bytes())


def installed_capability(
    repo_root: Path, *, capability_ref: str, capability_roots: list[str]
) -> tuple[str, str]:
    """Return the exact installed skill path and digest, or fail closed."""
    if not isinstance(capability_ref, str) or not _CAPABILITY_ID.fullmatch(capability_ref):
        raise ValidationError(f"capability {capability_ref!r} is not an exact capability id")
    root = Path(repo_root).resolve()
    matches: list[Path] = []
    for relative_root in capability_roots:
        candidate = (root / relative_root / capability_ref / "SKILL.md").resolve()
        try:
            candidate.relative_to(root)
        except ValueError as exc:
            raise GateBlockedError("capability root escapes the repository") from exc
        if candidate.is_file():
            matches.append(candidate)
    if len(matches) != 1:
        raise ValidationError(
            f"capability {capability_ref!r} is not uniquely installed in canonical roots"
        )
    path = matches[0]
    body = path.read_bytes()
    try:
        text = body.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise GateBlockedError("installed capability is not UTF-8") from exc
    match = _FRONTMATTER_NAME.search(text)
    if match is None or match.group(1) != capability_ref:
        raise ValidationError("installed capability name does not match its exact identity")
    return path.relative_to(root).as_posix(), digest_bytes(body)


def build_route_receipt(
    *,
    repo_root: Path,
    registry_path: Path,
    registry_schema: str,
    dispatch_type_ref: str,
    ledger_dispatch_type: str,
    capability_ref: str,
    capability_path: str,
    capability_digest: str,
    authority_mode: str,
    tool_profile_ref: str,
) -> dict[str, Any]:
    body: dict[str, Any] = {
        "schema": ROUTE_SCHEMA,
        "registry_schema": registry_schema,
        "registry_digest": registry_digest(repo_root, registry_path),
        "dispatch_type_ref": dispatch_type_ref,
        "ledger_dispatch_type": ledger_dispatch_type,
        "capability_ref": capability_ref,
        "capability_path": capability_path,
        "capability_digest": capability_digest,
        "execution_authority_mode": authority_mode,
        "tool_profile_ref": tool_profile_ref,
    }
    return {**body, "route_digest": canonical_digest(body)}

