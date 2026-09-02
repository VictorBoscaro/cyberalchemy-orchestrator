"""Pinned, versioned agent-role registry resolution."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .errors import GateBlockedError, ValidationError


SELECTION_PATH = Path("implementations/contracts/agent-role-registry-selection.json")
ROLE_ID_RE = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
REF_FIELDS = {"name", "version", "digest"}


class AgentRoleError(ValidationError):
    def __init__(self, code: str, path: str, detail: str = "") -> None:
        self.code = code
        self.path = path
        self.detail = detail
        super().__init__(f"{code} at {path}" + (f": {detail}" if detail else ""))


def _fail(code: str, path: str, detail: str = "") -> None:
    raise AgentRoleError(code, path, detail)


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            _fail("DG_DUPLICATE_JSON_KEY", "$", key)
        result[key] = value
    return result


def _load(path: Path, code: str) -> tuple[dict[str, Any], bytes]:
    try:
        raw = path.read_bytes()
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs)
    except AgentRoleError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        _fail(code, "$", str(exc))
    if not isinstance(value, dict):
        _fail(code, "$", "root must be an object")
    return value, raw


def digest_bytes(raw: bytes) -> str:
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def _contained(root: Path, relative: object, path: str) -> Path:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        _fail("DG_ROLE_REGISTRY_SELECTION_INVALID", path)
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        _fail("DG_ROLE_REGISTRY_SELECTION_INVALID", path)
    return candidate


def _load_selection(root: Path) -> dict[str, Any]:
    selection, _ = _load(root / SELECTION_PATH, "DG_ROLE_REGISTRY_SELECTION_INVALID")
    if set(selection) != {"schema", "selected_ref", "registry_path", "authority_path", "host_routing_path"} or selection.get("schema") != "aci.role-registry-selection@1":
        _fail("DG_ROLE_REGISTRY_SELECTION_INVALID", "$")
    selection["selected_ref"] = validate_ref(selection.get("selected_ref"), "$.selected_ref")
    for field in ("registry_path", "authority_path", "host_routing_path"):
        _contained(root, selection.get(field), f"$.{field}")
    return selection


def validate_ref(value: Any, path: str = "agent_role_registry_ref") -> dict[str, str]:
    if not isinstance(value, dict) or set(value) != REF_FIELDS:
        _fail("DG_ROLE_REGISTRY_REF_INVALID", path, "closed name/version/digest object required")
    if any(not isinstance(value[key], str) or not value[key] for key in ("name", "version")):
        _fail("DG_ROLE_REGISTRY_REF_INVALID", path)
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", value.get("digest", "")):
        _fail("DG_ROLE_REGISTRY_REF_INVALID", path + ".digest")
    return dict(value)


@dataclass(frozen=True, slots=True)
class AcceptedRoleRegistry:
    value: dict[str, Any]
    ref: dict[str, str]
    roles: frozenset[str]

    def require(self, role: object, path: str = "role") -> str:
        if not isinstance(role, str) or role not in self.roles:
            _fail("DG_ROLE_UNKNOWN", path, repr(role))
        return role


def load_accepted_role_registry(
    repo_root: Path,
    *,
    expected_ref: Any | None = None,
) -> AcceptedRoleRegistry:
    root = Path(repo_root).resolve()
    selection = _load_selection(root)
    selected_ref = selection["selected_ref"]
    if expected_ref is not None and validate_ref(expected_ref) != selected_ref:
        _fail("DG_ROLE_REGISTRY_REF_DRIFT", "agent_role_registry_ref")
    registry, raw = _load(_contained(root, selection["registry_path"], "$.registry_path"), "DG_ROLE_REGISTRY_SCHEMA_INVALID")
    authority, _ = _load(_contained(root, selection["authority_path"], "$.authority_path"), "DG_ROLE_REGISTRY_AUTHORITY_INVALID")
    if set(registry) != {"schema", "name", "version", "roles"} or registry.get("schema") != "aci.role-registry@1":
        _fail("DG_ROLE_REGISTRY_SCHEMA_INVALID", "$")
    roles = registry.get("roles")
    if not isinstance(roles, list) or not roles:
        _fail("DG_ROLE_REGISTRY_SCHEMA_INVALID", "$.roles")
    ids: list[str] = []
    for index, row in enumerate(roles):
        path = f"$.roles[{index}]"
        if not isinstance(row, dict) or set(row) != {"role_id", "enabled", "purpose"}:
            _fail("DG_ROLE_REGISTRY_SCHEMA_INVALID", path)
        role_id = row.get("role_id")
        if not isinstance(role_id, str) or not ROLE_ID_RE.fullmatch(role_id):
            _fail("DG_ROLE_REGISTRY_SCHEMA_INVALID", path + ".role_id")
        if role_id in ids:
            _fail("DG_ROLE_REGISTRY_DUPLICATE", path + ".role_id")
        if row.get("enabled") is not True:
            _fail("DG_ROLE_REGISTRY_DISABLED", path + ".enabled")
        if not isinstance(row.get("purpose"), str) or not row["purpose"].strip():
            _fail("DG_ROLE_REGISTRY_SCHEMA_INVALID", path + ".purpose")
        ids.append(role_id)
    if set(authority) != {"schema", "accepted"} or authority.get("schema") != "aci.role-registry-authority@1" or not isinstance(authority.get("accepted"), list):
        _fail("DG_ROLE_REGISTRY_AUTHORITY_INVALID", "$")
    actual = {"name": registry.get("name"), "version": registry.get("version"), "digest": digest_bytes(raw)}
    matches = [row for row in authority["accepted"] if isinstance(row, dict) and row.get("name") == actual["name"] and row.get("version") == actual["version"]]
    if len(matches) != 1:
        _fail("DG_ROLE_REGISTRY_UNTRUSTED", "$.name")
    if matches[0].get("digest") != actual["digest"]:
        _fail("DG_ROLE_REGISTRY_SUBSTITUTED", "$.digest")
    if actual != selected_ref:
        _fail("DG_ROLE_REGISTRY_SELECTION_DRIFT", "$.selected_ref")
    return AcceptedRoleRegistry(registry, actual, frozenset(ids))


def load_host_role_routing(repo_root: Path, registry: AcceptedRoleRegistry | None = None) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    accepted = registry or load_accepted_role_registry(root)
    selection = _load_selection(root)
    value, _ = _load(_contained(root, selection["host_routing_path"], "$.host_routing_path"), "DG_ROLE_ROUTING_INVALID")
    if set(value) != {"schema", "role_registry_ref", "fallback_role", "routes"} or value.get("schema") != "aci.agent-role-host-routing@1":
        _fail("DG_ROLE_ROUTING_INVALID", "$")
    if validate_ref(value.get("role_registry_ref")) != accepted.ref:
        _fail("DG_ROLE_REGISTRY_REF_DRIFT", "$.role_registry_ref")
    accepted.require(value.get("fallback_role"), "$.fallback_role")
    if not isinstance(value.get("routes"), list):
        _fail("DG_ROLE_ROUTING_INVALID", "$.routes")
    for index, route in enumerate(value["routes"]):
        if not isinstance(route, dict) or set(route) != {"role", "keywords"}:
            _fail("DG_ROLE_ROUTING_INVALID", f"$.routes[{index}]")
        accepted.require(route.get("role"), f"$.routes[{index}].role")
        if not isinstance(route.get("keywords"), list) or not route["keywords"] or any(not isinstance(word, str) or not word for word in route["keywords"]):
            _fail("DG_ROLE_ROUTING_INVALID", f"$.routes[{index}].keywords")
    return value
