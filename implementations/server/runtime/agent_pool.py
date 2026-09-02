"""Strict canonical v0.7 agent-pool loading and one-time v0.6 migration support."""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .agent_roles import AcceptedRoleRegistry, load_accepted_role_registry
from .errors import ValidationError


POOL_PATH = Path("telemetry/agents/agent-pool.yaml")
AUTHORITY_PATH = Path("implementations/contracts/agent-pool-authority.v1.json")
METADATA_FIELDS = {
    "profile", "name", "description", "node_type", "layer", "nature", "status",
    "version", "last_updated", "source", "notes",
}
ENTRY_FIELDS = {"agent_name", "field", "era", "role_fit", "cited", "tags", "note"}
REQUIRED_ENTRY_FIELDS = {"agent_name", "field", "era", "role_fit", "cited", "tags"}


class AgentPoolError(ValidationError):
    def __init__(self, code: str, path: str, detail: str = "") -> None:
        self.code = code
        self.path = path
        self.detail = detail
        super().__init__(f"{code} at {path}" + (f": {detail}" if detail else ""))


def _fail(code: str, path: str, detail: str = "") -> None:
    raise AgentPoolError(code, path, detail)


class _StrictLoader(yaml.SafeLoader):
    pass


def _construct_mapping(loader: _StrictLoader, node: yaml.MappingNode, deep: bool = False) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            _fail("DG_DUPLICATE_YAML_KEY", "$.yaml", str(key))
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


_StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping)
_StrictLoader.add_constructor("tag:yaml.org,2002:timestamp", lambda loader, node: loader.construct_scalar(node))


def parse_pool_stream(raw: bytes | str) -> list[Any]:
    try:
        text = raw.decode("utf-8") if isinstance(raw, bytes) else raw
    except UnicodeDecodeError as exc:
        _fail("DG_POOL_SCHEMA_INVALID", "$.yaml", str(exc))
    if not isinstance(text, str):
        _fail("DG_POOL_SCHEMA_INVALID", "$.yaml")
    try:
        docs = list(yaml.load_all(text, Loader=_StrictLoader))
    except AgentPoolError:
        raise
    except yaml.YAMLError as exc:
        _fail("DG_POOL_SCHEMA_INVALID", "$.yaml", str(exc))
    if len(docs) != 2:
        _fail("DG_POOL_DOCUMENT_COUNT", "$.documents")
    if not isinstance(docs[0], dict) or not isinstance(docs[1], dict) or set(docs[1]) != {"scientists"}:
        _fail("DG_POOL_DOCUMENT_ORDER", "$.documents")
    return docs


def _canonical_digest(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True, slots=True)
class NormalizedAgentPool:
    value: dict[str, Any]
    ref: dict[str, str]
    by_name: dict[str, dict[str, Any]]


def normalize_pool_documents(docs: list[Any], registry: AcceptedRoleRegistry) -> NormalizedAgentPool:
    metadata, roster = docs
    if set(metadata) != METADATA_FIELDS:
        _fail("DG_POOL_METADATA_DRIFT", "$.documents[0]")
    expected_meta = {
        "profile": "subagents-strategy", "node_type": "agent-pool", "layer": "meta",
        "nature": "reference", "status": "active", "version": "0.7.0",
    }
    for key, expected in expected_meta.items():
        if metadata.get(key) != expected:
            _fail("DG_POOL_METADATA_DRIFT", f"$.documents[0].{key}")
    for key in ("name", "description", "last_updated", "source"):
        if not isinstance(metadata.get(key), str) or not metadata[key].strip():
            _fail("DG_POOL_METADATA_DRIFT", f"$.documents[0].{key}")
    if not isinstance(metadata.get("notes"), list) or not metadata["notes"] or any(not isinstance(note, str) or not note.strip() for note in metadata["notes"]):
        _fail("DG_POOL_METADATA_DRIFT", "$.documents[0].notes")
    rows = roster.get("scientists")
    if not isinstance(rows, list) or not rows:
        _fail("DG_POOL_SCHEMA_INVALID", "$.documents[1].scientists")
    agents: list[dict[str, Any]] = []
    names: set[str] = set()
    for index, row in enumerate(rows):
        path = f"$.documents[1].scientists[{index}]"
        if not isinstance(row, dict):
            _fail("DG_POOL_SCHEMA_INVALID", path)
        present_identity = [key for key in ("agent_name", "name", "agent-name") if key in row]
        if not present_identity:
            _fail("DG_POOL_NAME_MISSING", path)
        if len(present_identity) != 1:
            _fail("DG_POOL_NAME_AMBIGUOUS", path)
        identity_key = present_identity[0]
        if identity_key == "name":
            _fail("DG_POOL_LEGACY_NAME_FORBIDDEN", path + ".name")
        if identity_key == "agent-name":
            _fail("DG_POOL_NAME_KEY_INVALID", path + ".agent-name")
        unknown = set(row) - ENTRY_FIELDS
        if unknown:
            _fail("DG_POOL_UNKNOWN_KEY", path + "." + sorted(unknown)[0])
        if not REQUIRED_ENTRY_FIELDS <= set(row):
            _fail("DG_POOL_SCHEMA_INVALID", path)
        name = row["agent_name"]
        if not isinstance(name, str):
            _fail("DG_POOL_NAME_TYPE", path + ".agent_name")
        if not name.strip():
            _fail("DG_POOL_NAME_EMPTY", path + ".agent_name")
        if name in names:
            _fail("DG_POOL_DUPLICATE_NAME", path + ".agent_name")
        names.add(name)
        for field in ("field", "era"):
            if not isinstance(row[field], str) or not row[field].strip():
                _fail("DG_POOL_SCHEMA_INVALID", path + "." + field)
        if not isinstance(row["cited"], bool):
            _fail("DG_POOL_SCHEMA_INVALID", path + ".cited")
        if not isinstance(row["tags"], list) or not row["tags"] or len(row["tags"]) != len(set(row["tags"])) or any(not isinstance(tag, str) or not tag for tag in row["tags"]):
            _fail("DG_POOL_SCHEMA_INVALID", path + ".tags")
        role_fit = row["role_fit"]
        if not isinstance(role_fit, list) or not role_fit or len(role_fit) != len(set(role_fit)):
            _fail("DG_POOL_SCHEMA_INVALID", path + ".role_fit")
        for role_index, role in enumerate(role_fit):
            registry.require(role, f"{path}.role_fit[{role_index}]")
        if "note" in row and (not isinstance(row["note"], str) or not row["note"].strip()):
            _fail("DG_POOL_SCHEMA_INVALID", path + ".note")
        agents.append({"display_name": name, "role_fit": list(role_fit)})
    normalized = {
        "schema": "aci.normalized-agent-pool@1",
        "name": metadata["name"],
        "version": metadata["version"],
        "agents": agents,
    }
    ref = {"name": metadata["name"], "version": metadata["version"], "digest": _canonical_digest(normalized)}
    return NormalizedAgentPool(normalized, ref, {row["display_name"]: row for row in agents})


def load_agent_pool(repo_root: Path, registry: AcceptedRoleRegistry | None = None) -> NormalizedAgentPool:
    root = Path(repo_root).resolve()
    accepted = registry or load_accepted_role_registry(root)
    path = (root / POOL_PATH).resolve()
    try:
        raw = path.read_bytes()
    except OSError as exc:
        _fail("DG_POOL_SCHEMA_INVALID", "$.yaml", str(exc))
    authority_path = root / AUTHORITY_PATH
    if authority_path.is_file():
        try:
            authority = json.loads(authority_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            _fail("DG_POOL_AUTHORITY_INVALID", "$", str(exc))
        if not isinstance(authority, dict) or authority.get("schema") != "aci.agent-pool-authority@1":
            _fail("DG_POOL_AUTHORITY_INVALID", "$")
        actual = "sha256:" + hashlib.sha256(raw).hexdigest()
        if authority.get("source_raw_digest") != actual:
            _fail("DG_POOL_SOURCE_SUBSTITUTION", "$.yaml")
    result = normalize_pool_documents(parse_pool_stream(raw), accepted)
    if authority_path.is_file():
        if authority.get("agent_pool_ref") != result.ref:
            _fail("DG_POOL_METADATA_DRIFT", "$.documents[0]")
        if authority.get("entry_count") != len(result.value["agents"]):
            _fail("DG_POOL_METADATA_DRIFT", "$.documents[1].scientists")
    return result


def migrate_legacy_pool(raw: bytes, authority: dict[str, Any], registry: AcceptedRoleRegistry) -> list[Any]:
    actual = "sha256:" + hashlib.sha256(raw).hexdigest()
    if actual != authority.get("source_raw_digest"):
        _fail("DG_POOL_SOURCE_SUBSTITUTION", "$.yaml")
    docs = parse_pool_stream(raw)
    metadata, roster = docs
    if metadata.get("version") != authority.get("source_version") or len(roster.get("scientists", [])) != authority.get("source_entry_count"):
        _fail("DG_POOL_METADATA_DRIFT", "$.documents[0]")
    migrated = copy.deepcopy(docs)
    target_meta = migrated[0]
    changes = authority["metadata_changes"]
    target_meta["version"] = authority["target_version"]
    target_meta["last_updated"] = changes["last_updated"]
    target_meta["notes"].insert(0, changes["prepend_note"])
    for index, row in enumerate(migrated[1]["scientists"]):
        if "name" not in row or "agent_name" in row or "agent-name" in row:
            _fail("DG_POOL_NAME_MISSING", f"$.documents[1].scientists[{index}]")
        replacement = {}
        for key, value in row.items():
            replacement["agent_name" if key == "name" else key] = value
        migrated[1]["scientists"][index] = replacement
    normalize_pool_documents(migrated, registry)
    return migrated
