"""Canonical dispatch-type registry reader shared by routing and runtime adapters."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .errors import GateBlockedError, ValidationError


REGISTRY = Path("implementations/contracts/dispatch-type-registry.v1.json")
REGISTRY_SCHEMA = "aci-dispatch-type-registry/v1"
ENTRY_FIELDS = {
    "id",
    "status",
    "routable",
    "capability_ref",
    "capability_path",
    "authority_modes",
    "tool_profile_ref",
    "ledger_value",
}


def load_dispatch_type_registry(repo_root: Path) -> dict[str, Any]:
    path = (Path(repo_root).resolve() / REGISTRY).resolve()
    try:
        path.relative_to(Path(repo_root).resolve())
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise GateBlockedError("canonical dispatch-type registry is unavailable") from exc
    if (
        not isinstance(value, dict)
        or set(value) != {"schema", "ledger_schema_version", "types"}
        or value.get("schema") != REGISTRY_SCHEMA
        or not isinstance(value.get("ledger_schema_version"), str)
        or not isinstance(value.get("types"), list)
        or not value["types"]
    ):
        raise GateBlockedError("canonical dispatch-type registry shape is invalid")
    ids: set[str] = set()
    ledger_values: set[str] = set()
    capability_refs: set[str] = set()
    for entry in value["types"]:
        if not isinstance(entry, dict) or set(entry) != ENTRY_FIELDS:
            raise GateBlockedError("canonical dispatch-type entry shape is invalid")
        dispatch_type = entry["id"]
        ledger_value = entry["ledger_value"]
        capability_ref = entry["capability_ref"]
        capability_path = entry["capability_path"]
        authority_modes = entry["authority_modes"]
        if (
            not isinstance(dispatch_type, str)
            or not dispatch_type
            or dispatch_type in ids
            or not isinstance(ledger_value, str)
            or not ledger_value
            or ledger_value in ledger_values
            or entry["status"] not in {"live", "reserved"}
            or not isinstance(entry["routable"], bool)
            or not isinstance(authority_modes, list)
            or any(mode not in {"legacy-managed", "runtime-managed"} for mode in authority_modes)
        ):
            raise GateBlockedError("canonical dispatch-type entry is invalid")
        if entry["status"] == "reserved" and authority_modes:
            raise GateBlockedError("reserved dispatch types cannot declare authority modes")
        if entry["routable"]:
            if (
                entry["status"] != "live"
                or not isinstance(capability_ref, str)
                or not capability_ref
                or capability_ref in capability_refs
                or not isinstance(capability_path, str)
                or not capability_path
                or not (Path(repo_root) / capability_path).is_file()
                or not isinstance(entry["tool_profile_ref"], str)
                or not entry["tool_profile_ref"]
            ):
                raise GateBlockedError("routable dispatch type has no installed capability")
            capability_refs.add(capability_ref)
        elif capability_ref is not None or capability_path is not None:
            raise GateBlockedError("non-routable dispatch type cannot name a capability")
        ids.add(dispatch_type)
        ledger_values.add(ledger_value)
    return value


def dispatch_type_entries(repo_root: Path) -> list[dict[str, Any]]:
    return load_dispatch_type_registry(repo_root)["types"]


def live_dispatch_type_values(repo_root: Path) -> set[str]:
    return {
        entry["ledger_value"]
        for entry in dispatch_type_entries(repo_root)
        if entry["status"] == "live"
    }


def resolve_dispatch_capability(
    repo_root: Path,
    *,
    capability_ref: str,
    authority_mode: str,
) -> dict[str, Any]:
    matches = [
        entry
        for entry in dispatch_type_entries(repo_root)
        if entry["capability_ref"] == capability_ref
    ]
    if not matches:
        raise ValidationError(
            f"capability {capability_ref!r} has no routable dispatch type"
        )
    entry = matches[0]
    if authority_mode not in entry["authority_modes"]:
        raise GateBlockedError(
            f"capability {capability_ref!r} is unavailable in {authority_mode!r}"
        )
    return {
        "registry_schema": REGISTRY_SCHEMA,
        "dispatch_type_ref": entry["id"],
        "ledger_dispatch_type": entry["ledger_value"],
        "capability_ref": entry["capability_ref"],
        "capability_path": entry["capability_path"],
        "execution_authority_mode": authority_mode,
        "tool_profile_ref": entry["tool_profile_ref"],
    }
