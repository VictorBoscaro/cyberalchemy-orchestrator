from __future__ import annotations

import base64
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import jsonschema
import yaml
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey


ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[7]
SCHEMAS = ROOT / "schemas"
FIXTURES = ROOT / "fixtures"
REAL_POOL = REPO_ROOT / "telemetry" / "agents" / "agent-pool.yaml"
ROLE_IDS = ["explorer", "synthesizer", "skeptic", "writer", "auditor", "planner", "coder", "other"]
FIXTURE_PRIVATE_SEED = bytes(range(32))


class ContractError(Exception):
    def __init__(self, code: str, path: str):
        super().__init__(f"{code} at {path}")
        self.code = code
        self.path = path


class UniqueKeyLoader(yaml.SafeLoader):
    pass


# Dates are data in this contract, not Python datetime objects.
UniqueKeyLoader.yaml_implicit_resolvers = copy.deepcopy(yaml.SafeLoader.yaml_implicit_resolvers)
for first_char, resolvers in list(UniqueKeyLoader.yaml_implicit_resolvers.items()):
    UniqueKeyLoader.yaml_implicit_resolvers[first_char] = [
        pair for pair in resolvers if pair[0] != "tag:yaml.org,2002:timestamp"
    ]


def _construct_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ContractError("DG_POOL_YAML_DUPLICATE_KEY", "$.yaml")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping)


def load_json(path: Path) -> Any:
    def exact_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ContractError("DG_DUPLICATE_JSON_KEY", "$.json")
            result[key] = value
        return result

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=exact_pairs)


def load_yaml_stream_text(text: str) -> dict[str, Any]:
    try:
        documents = list(yaml.load_all(text, Loader=UniqueKeyLoader))
    except ContractError:
        raise
    except yaml.YAMLError as exc:
        raise ContractError("DG_POOL_YAML_INVALID", "$.yaml") from exc
    return {"documents": documents}


def load_yaml_stream(path: Path) -> dict[str, Any]:
    return load_yaml_stream_text(path.read_text(encoding="utf-8"))


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()


def raw_digest(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def json_path(parts: Any) -> str:
    result = "$"
    for part in parts:
        result += f"[{part}]" if isinstance(part, int) else f".{part}"
    return result


def schema_validate(instance: Any, schema_name: str, code: str) -> None:
    schema = load_json(SCHEMAS / schema_name)
    jsonschema.Draft202012Validator.check_schema(schema)
    errors = sorted(jsonschema.Draft202012Validator(schema).iter_errors(instance), key=lambda e: list(e.absolute_path))
    if errors:
        raise ContractError(code, json_path(errors[0].absolute_path))


def check_pool_topology(stream: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    documents = stream.get("documents")
    if not isinstance(documents, list) or len(documents) != 2:
        raise ContractError("DG_POOL_DOCUMENT_COUNT", "$.documents")
    if not isinstance(documents[0], dict) or not isinstance(documents[1], dict):
        raise ContractError("DG_POOL_DOCUMENT_ORDER", "$.documents")
    if "profile" not in documents[0] or set(documents[1]) != {"scientists"}:
        raise ContractError("DG_POOL_DOCUMENT_ORDER", "$.documents")
    return documents[0], documents[1]


def normalize_canonical_pool(stream: dict[str, Any], allowed_roles: set[str]) -> dict[str, Any]:
    metadata, roster = check_pool_topology(stream)
    if metadata.get("version") != "0.7.0":
        raise ContractError("DG_POOL_VERSION_UNSUPPORTED", "$.documents[0].version")
    entries = roster.get("scientists")
    if not isinstance(entries, list):
        raise ContractError("DG_POOL_SCHEMA_INVALID", "$.documents[1].scientists")

    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    allowed_entry_keys = {"agent_name", "field", "era", "role_fit", "cited", "tags", "note"}
    for index, entry in enumerate(entries):
        base = f"$.documents[1].scientists[{index}]"
        if not isinstance(entry, dict):
            raise ContractError("DG_POOL_SCHEMA_INVALID", base)
        identity_keys = [key for key in ("name", "agent_name", "agent-name") if key in entry]
        if not identity_keys:
            raise ContractError("DG_POOL_NAME_MISSING", base)
        if len(identity_keys) > 1:
            raise ContractError("DG_POOL_NAME_AMBIGUOUS", base)
        if identity_keys[0] == "name":
            raise ContractError("DG_POOL_LEGACY_NAME_FORBIDDEN", f"{base}.name")
        if identity_keys[0] == "agent-name":
            raise ContractError("DG_POOL_NAME_KEY_INVALID", f"{base}.agent-name")
        name = entry["agent_name"]
        if not isinstance(name, str):
            raise ContractError("DG_POOL_NAME_TYPE", f"{base}.agent_name")
        if not name:
            raise ContractError("DG_POOL_NAME_EMPTY", f"{base}.agent_name")
        unknown = set(entry) - allowed_entry_keys
        if unknown:
            key = sorted(unknown)[0]
            raise ContractError("DG_POOL_UNKNOWN_KEY", f"{base}.{key}")
        if name in seen:
            raise ContractError("DG_POOL_IDENTITY_DUPLICATE", f"{base}.agent_name")
        seen.add(name)
        role_fit = entry.get("role_fit")
        if isinstance(role_fit, list):
            for role_index, role in enumerate(role_fit):
                if role not in allowed_roles:
                    raise ContractError("DG_ROLE_UNKNOWN", f"{base}.role_fit[{role_index}]")
        normalized.append({"display_name": name, "role_fit": role_fit})

    schema_validate(stream, "source-agent-pool.schema.json", "DG_POOL_SCHEMA_INVALID")
    result = {
        "schema": "aci.normalized-agent-pool@1",
        "name": metadata["name"],
        "version": metadata["version"],
        "agents": normalized,
    }
    schema_validate(result, "normalized-agent-pool.schema.json", "DG_POOL_SCHEMA_INVALID")
    return result


def validate_registry(registry: dict[str, Any], authority: dict[str, Any]) -> set[str]:
    schema_validate(authority, "role-registry-authority.schema.json", "DG_ROLE_AUTHORITY_SCHEMA_INVALID")
    accepted = authority["accepted"]
    accepted_pairs = [(row["name"], row["version"]) for row in accepted]
    if len(accepted_pairs) != len(set(accepted_pairs)):
        raise ContractError("DG_ROLE_AUTHORITY_DUPLICATE", "$.accepted")

    name = registry.get("name")
    version = registry.get("version")
    match = next((row for row in accepted if (row["name"], row["version"]) == (name, version)), None)
    if match is None:
        path = "$.version" if name == "aci.agent-roles" else "$.name"
        raise ContractError("DG_ROLE_REGISTRY_UNTRUSTED", path)
    rows = registry.get("roles")
    if not isinstance(rows, list):
        raise ContractError("DG_ROLE_REGISTRY_SCHEMA_INVALID", "$.roles")
    ids = [row.get("role_id") for row in rows if isinstance(row, dict)]
    seen: set[Any] = set()
    for index, role_id in enumerate(ids):
        if role_id in seen:
            raise ContractError("DG_ROLE_REGISTRY_DUPLICATE", f"$.roles[{index}].role_id")
        seen.add(role_id)
    for index, row in enumerate(rows):
        if isinstance(row, dict) and row.get("role_id") in ROLE_IDS and row.get("enabled") is False:
            raise ContractError("DG_ROLE_REGISTRY_DISABLED", f"$.roles[{index}].enabled")
    missing = set(ROLE_IDS) - set(ids)
    extra = set(ids) - set(ROLE_IDS)
    if extra:
        index = next(index for index, role_id in enumerate(ids) if role_id in extra)
        raise ContractError("DG_ROLE_REGISTRY_EXTRA_ROLE", f"$.roles[{index}].role_id")
    if missing:
        raise ContractError("DG_ROLE_REGISTRY_MISSING_ROLE", "$.roles")
    schema_validate(registry, "role-registry.schema.json", "DG_ROLE_REGISTRY_SCHEMA_INVALID")
    if digest(registry) != match["digest"]:
        raise ContractError("DG_ROLE_REGISTRY_SUBSTITUTION", "$.role_registry")
    return set(ROLE_IDS)


def evidence_payload(evidence: dict[str, Any]) -> dict[str, Any]:
    return {key: evidence[key] for key in (
        "schema", "evidence_id", "key_id", "context_digest", "is_latest", "pair_is_unbound"
    )}


def sign_fixture_evidence(evidence: dict[str, Any], context: dict[str, Any]) -> None:
    evidence["context_digest"] = digest(context)
    private_key = Ed25519PrivateKey.from_private_bytes(FIXTURE_PRIVATE_SEED)
    evidence["signature"] = base64.b64encode(private_key.sign(canonical_bytes(evidence_payload(evidence)))).decode("ascii")


def verify_evidence(
    evidence: dict[str, Any], context: dict[str, Any], trust: dict[str, Any], consumed_ids: set[str]
) -> None:
    schema_validate(evidence, "allocator-evidence.schema.json", "DG_ALLOCATOR_EVIDENCE_SCHEMA_INVALID")
    schema_validate(trust, "allocator-trust.schema.json", "DG_ALLOCATOR_TRUST_SCHEMA_INVALID")
    if evidence["context_digest"] != digest(context):
        raise ContractError("DG_IDENTITY_CONTEXT_TAMPERED", "$.context_digest")
    key = next((row for row in trust["keys"] if row["key_id"] == evidence["key_id"]), None)
    if key is None:
        raise ContractError("DG_ALLOCATOR_KEY_UNTRUSTED", "$.key_id")
    try:
        public_key = Ed25519PublicKey.from_public_bytes(base64.b64decode(key["public_key_base64"], validate=True))
        public_key.verify(base64.b64decode(evidence["signature"], validate=True), canonical_bytes(evidence_payload(evidence)))
    except (InvalidSignature, ValueError) as exc:
        raise ContractError("DG_ALLOCATOR_SIGNATURE_INVALID", "$.signature") from exc
    if evidence["evidence_id"] in consumed_ids:
        raise ContractError("DG_ALLOCATOR_EVIDENCE_REPLAY", "$.evidence_id")
    if not evidence["is_latest"]:
        raise ContractError("DG_IDENTITY_CONTEXT_STALE", "$.is_latest")
    if not evidence["pair_is_unbound"]:
        raise ContractError("DG_AUTHORITY_CONFLICT", "$.pair_is_unbound")


def verify_and_migrate_real_pool(
    raw: bytes, authority: dict[str, Any], allowed_roles: set[str]
) -> dict[str, Any]:
    schema_validate(authority, "pool-migration-authority.schema.json", "DG_POOL_MIGRATION_AUTHORITY_INVALID")
    stream = load_yaml_stream_text(raw.decode("utf-8"))
    metadata, roster = check_pool_topology(stream)
    schema_validate(stream, "source-agent-pool.schema.json", "DG_POOL_SCHEMA_INVALID")
    if digest(metadata) != authority["source_metadata_digest"]:
        raise ContractError("DG_POOL_METADATA_DRIFT", "$.documents[0]")
    if raw_digest(raw) != authority["source_raw_digest"]:
        raise ContractError("DG_POOL_SOURCE_SUBSTITUTION", "$.yaml")
    entries = roster["scientists"]
    if metadata["version"] != authority["source_version"] or len(entries) != authority["source_entry_count"]:
        raise ContractError("DG_POOL_SOURCE_SUBSTITUTION", "$.documents")
    seen: set[str] = set()
    for index, entry in enumerate(entries):
        base = f"$.documents[1].scientists[{index}]"
        identity_keys = [key for key in ("name", "agent_name", "agent-name") if key in entry]
        if identity_keys != ["name"]:
            raise ContractError("DG_POOL_LEGACY_SHAPE_INVALID", base)
        if entry["name"] in seen:
            raise ContractError("DG_POOL_IDENTITY_DUPLICATE", f"{base}.name")
        seen.add(entry["name"])

    migrated = copy.deepcopy(stream)
    target_metadata = migrated["documents"][0]
    changes = authority["metadata_changes"]
    target_metadata["version"] = changes["version"]
    target_metadata["last_updated"] = changes["last_updated"]
    target_metadata["notes"].insert(0, changes["prepend_note"])
    for old, new in zip(entries, migrated["documents"][1]["scientists"], strict=True):
        value = new.pop("name")
        new[authority["canonical_name_key"]] = value
        old_rest = {key: item for key, item in old.items() if key != "name"}
        new_rest = {key: item for key, item in new.items() if key != "agent_name"}
        if old_rest != new_rest:
            raise ContractError("DG_POOL_MIGRATION_LOSS", "$.documents[1].scientists")
    normalized = normalize_canonical_pool(migrated, allowed_roles)
    if len(normalized["agents"]) != authority["source_entry_count"]:
        raise ContractError("DG_POOL_MIGRATION_LOSS", "$.documents[1].scientists")
    return migrated


def validate_contract(
    draft: dict[str, Any],
    source_stream: dict[str, Any],
    normalized_fixture: dict[str, Any],
    registry: dict[str, Any],
    registry_authority: dict[str, Any],
    context: dict[str, Any],
    evidence: dict[str, Any],
    trust: dict[str, Any],
    consumed_ids: set[str] | None = None,
) -> list[dict[str, str]]:
    schema_validate(draft, "draft-graph-v1.proposed.schema.json", "DG_DRAFT_SCHEMA_INVALID")
    allowed_roles = validate_registry(registry, registry_authority)
    normalized = normalize_canonical_pool(source_stream, allowed_roles)
    if normalized != normalized_fixture:
        raise ContractError("DG_AGENT_POOL_NORMALIZATION_MISMATCH", "$.normalized_agent_pool")
    schema_validate(context, "compilation-context.schema.json", "DG_IDENTITY_CONTEXT_SCHEMA_INVALID")
    verify_evidence(evidence, context, trust, consumed_ids or set())

    expected_registry_ref = {"name": registry["name"], "version": registry["version"], "digest": digest(registry)}
    if context["role_registry_ref"] != expected_registry_ref:
        raise ContractError("DG_ROLE_REGISTRY_DRIFT", "$.role_registry_ref.digest")
    expected_pool_ref = {"name": normalized["name"], "version": normalized["version"], "digest": digest(normalized)}
    if context["agent_pool_ref"] != expected_pool_ref:
        raise ContractError("DG_AGENT_POOL_DRIFT", "$.agent_pool_ref.digest")

    nodes = {node["key"]: node for node in draft["nodes"]}
    assignments = context["agent_assignments"]
    assignment_keys = [row["node_key"] for row in assignments]
    seen_keys: set[str] = set()
    for row in assignments:
        if row["node_key"] in seen_keys:
            raise ContractError("DG_AGENT_ASSIGNMENT_DUPLICATE", f"$.agent_assignments.{row['node_key']}")
        seen_keys.add(row["node_key"])
    extras = set(assignment_keys) - set(nodes)
    if extras:
        extra = sorted(extras)[0]
        raise ContractError("DG_AGENT_ASSIGNMENT_EXTRA", f"$.agent_assignments.{extra}")
    if set(nodes) - set(assignment_keys):
        raise ContractError("DG_AGENT_ASSIGNMENT_MISSING", "$.agent_assignments")
    names = [row["display_name"] for row in assignments]
    if len(names) != len(set(names)):
        duplicate = next(name for name in names if names.count(name) > 1)
        node_key = next(row["node_key"] for row in assignments[1:] if row["display_name"] == duplicate)
        raise ContractError("DG_AGENT_REUSED", f"$.agent_assignments.{node_key}.display_name")

    pool_by_name = {row["display_name"]: row for row in normalized["agents"]}
    projection: list[dict[str, str]] = []
    for assignment in assignments:
        node = nodes[assignment["node_key"]]
        role = node["agent_request"]["role"]
        if role not in allowed_roles:
            raise ContractError("DG_ROLE_UNKNOWN", f"$.nodes.{assignment['node_key']}.agent_request.role")
        if assignment["display_name"] not in pool_by_name:
            raise ContractError("DG_AGENT_ASSIGNMENT_UNKNOWN", f"$.agent_assignments.{assignment['node_key']}.display_name")
        matches = role in pool_by_name[assignment["display_name"]]["role_fit"]
        override = assignment["role_fit_override"]
        reason = assignment["role_fit_override_reason"]
        if not matches and (not override or not isinstance(reason, str) or not reason):
            raise ContractError("DG_ROLE_FIT_MISMATCH", f"$.agent_assignments.{assignment['node_key']}")
        if matches and (override or reason is not None):
            raise ContractError("DG_ROLE_FIT_OVERRIDE_INVALID", f"$.agent_assignments.{assignment['node_key']}")
        projection.append({
            "node_id": "node:" + assignment["node_key"],
            "display_name": assignment["display_name"],
            "role": role,
        })
    return projection


def mutate_vector(
    vector: dict[str, Any], draft: dict[str, Any], source: dict[str, Any], registry: dict[str, Any],
    context: dict[str, Any], evidence: dict[str, Any], real_stream: dict[str, Any]
) -> None:
    op = vector["operation"]
    entries = source["documents"][1]["scientists"]
    assignments = context["agent_assignments"]
    if op == "pool_remove_name":
        entries[0].pop("agent_name")
    elif op == "pool_add_hyphen_name":
        entries[0]["agent-name"] = vector["value"]
    elif op == "pool_set_name":
        entries[0]["agent_name"] = vector["value"]
    elif op == "pool_use_legacy_name":
        entries[0]["name"] = entries[0].pop("agent_name")
    elif op == "pool_use_hyphen_name":
        entries[0]["agent-name"] = entries[0].pop("agent_name")
    elif op == "pool_duplicate_name":
        entries[1]["agent_name"] = entries[0]["agent_name"]
    elif op == "pool_unknown_key":
        entries[0]["nickname"] = "Karl"
    elif op == "pool_drop_document":
        source["documents"].pop()
    elif op == "pool_reverse_documents":
        source["documents"].reverse()
    elif op == "real_pool_metadata_drift":
        real_stream["documents"][0]["description"] += " tampered"
    elif op == "draft_set_role":
        draft["nodes"][0]["agent_request"]["role"] = vector["value"]
    elif op == "assignment_disable_override":
        assignments[1]["role_fit_override"] = False
        assignments[1]["role_fit_override_reason"] = None
    elif op == "assignment_empty_override_reason":
        assignments[1]["role_fit_override_reason"] = ""
    elif op == "assignment_reuse_name":
        assignments[2]["display_name"] = assignments[0]["display_name"]
    elif op == "assignment_remove":
        assignments.pop()
    elif op == "assignment_add_unknown_node":
        assignments.append({"node_key": "ghost", "display_name": "Popper, Karl", "role_fit_override": False, "role_fit_override_reason": None})
    elif op == "assignment_duplicate_node_key":
        assignments[1]["node_key"] = "review"
    elif op == "assignment_unknown_pool_name":
        assignments[0]["display_name"] = "Unknown, Agent"
    elif op == "context_registry_ref_drift":
        context["role_registry_ref"]["digest"] = "sha256:" + "f" * 64
    elif op == "context_pool_ref_drift":
        context["agent_pool_ref"]["digest"] = "sha256:" + "f" * 64
    elif op == "assignment_tamper_without_evidence":
        assignments[0]["display_name"] = "Unknown, Agent"
    elif op == "forge_signature":
        evidence["signature"] = base64.b64encode(b"0" * 64).decode("ascii")
    elif op == "evidence_mark_stale":
        evidence["is_latest"] = False
    elif op == "evidence_mark_bound":
        evidence["pair_is_unbound"] = False
    elif op == "evidence_replay":
        pass
    elif op == "registry_mutate_purpose_and_repin_context":
        registry["roles"][5]["purpose"] = "Mutated in place."
        context["role_registry_ref"]["digest"] = digest(registry)
    elif op == "registry_duplicate_role":
        registry["roles"][5]["role_id"] = "skeptic"
    elif op == "registry_disable_requested_role":
        registry["roles"][2]["enabled"] = False
    elif op == "registry_remove_role":
        registry["roles"].pop()
    elif op == "registry_add_role":
        registry["roles"].append({"role_id": "hacker", "enabled": True, "purpose": "Unauthorized role."})
    elif op == "registry_unknown_version":
        registry["version"] = "2"
    elif op == "registry_reorder_roles":
        registry["roles"][0], registry["roles"][1] = registry["roles"][1], registry["roles"][0]
    elif op == "registry_substitute_name":
        registry["name"] = "aci.substituted-agent-roles"
    elif op == "draft_add_display_name":
        draft["nodes"][0]["agent_request"]["display_name"] = "LLM name"
    elif op == "pool_unknown_role_fit":
        entries[0]["role_fit"][0] = "hacker"
    elif op == "pool_role_only_in_future_registry":
        entries[0]["role_fit"][0] = "researcher"
    elif op in {"pool_duplicate_yaml_key", "real_pool_raw_substitution"}:
        return
    else:
        raise AssertionError(f"unsupported vector operation: {op}")


def validate_vector(
    vector: dict[str, Any], base: dict[str, Any], real_stream: dict[str, Any], migration_authority: dict[str, Any]
) -> None:
    d = copy.deepcopy(base["draft"])
    s = copy.deepcopy(base["source"])
    n = copy.deepcopy(base["normalized"])
    r = copy.deepcopy(base["registry"])
    c = copy.deepcopy(base["context"])
    e = copy.deepcopy(base["evidence"])
    rs = copy.deepcopy(real_stream)
    mutate_vector(vector, d, s, r, c, e, rs)
    if vector.get("resign"):
        sign_fixture_evidence(e, c)
    try:
        if vector["operation"] == "pool_duplicate_yaml_key":
            load_yaml_stream_text("profile: one\nprofile: two\n---\nscientists: []\n")
        elif vector["operation"] == "real_pool_raw_substitution":
            verify_and_migrate_real_pool(
                REAL_POOL.read_bytes() + b"\n# raw-only substitution\n",
                migration_authority,
                set(ROLE_IDS),
            )
        elif vector["operation"] == "real_pool_metadata_drift":
            metadata, _ = check_pool_topology(rs)
            if digest(metadata) != migration_authority["source_metadata_digest"]:
                raise ContractError("DG_POOL_METADATA_DRIFT", "$.documents[0]")
        else:
            consumed = {e["evidence_id"]} if vector["operation"] == "evidence_replay" else set()
            validate_contract(d, s, n, r, base["registry_authority"], c, e, base["trust"], consumed)
    except ContractError as exc:
        assert exc.code == vector["expected"], f"{vector['id']}: {exc.code} != {vector['expected']}"
        assert exc.path == vector["path"], f"{vector['id']}: {exc.path} != {vector['path']}"
    else:
        raise AssertionError(f"{vector['id']}: invalid vector passed")


def main() -> None:
    base = {
        "draft": load_json(FIXTURES / "review-correct-verify.draft.json"),
        "source": load_yaml_stream(FIXTURES / "source-agent-pool.yaml"),
        "normalized": load_json(FIXTURES / "normalized-agent-pool.json"),
        "registry": load_json(FIXTURES / "role-registry.json"),
        "registry_authority": load_json(FIXTURES / "role-registry-authority.json"),
        "context": load_json(FIXTURES / "compilation-context.json"),
        "evidence": load_json(FIXTURES / "allocator-evidence.json"),
        "trust": load_json(FIXTURES / "allocator-trust.json"),
    }
    policy = load_json(FIXTURES / "policy.json")
    expected = load_json(FIXTURES / "review-correct-verify.expected-agent-projection.json")
    migration_authority = load_json(FIXTURES / "pool-migration-authority.json")
    illustrative_v2 = load_json(FIXTURES / "role-registry-v2-illustrative.json")

    projection = validate_contract(
        base["draft"], base["source"], base["normalized"], base["registry"],
        base["registry_authority"], base["context"], base["evidence"], base["trust"]
    )
    assert expected == {"schema": "aci.execution-agent-identity-projection@1", "nodes": projection}

    allowed_bindings = {
        tuple(row[field] for field in ("role", "provider_key", "model_key", "profile_key", "credential_key"))
        for row in policy["allowed_agent_bindings"]
    }
    requested_bindings = {
        tuple(node["agent_request"][field] for field in ("role", "provider_key", "model_key", "profile_key", "credential_key"))
        for node in base["draft"]["nodes"]
    }
    assert requested_bindings <= allowed_bindings

    other_draft = copy.deepcopy(base["draft"])
    other_context = copy.deepcopy(base["context"])
    other_evidence = copy.deepcopy(base["evidence"])
    other_draft["nodes"][0]["agent_request"]["role"] = "other"
    other_context["agent_assignments"][0]["role_fit_override"] = True
    other_context["agent_assignments"][0]["role_fit_override_reason"] = "No narrower configured role describes this fixture assignment."
    sign_fixture_evidence(other_evidence, other_context)
    other_projection = validate_contract(
        other_draft, base["source"], base["normalized"], base["registry"], base["registry_authority"],
        other_context, other_evidence, base["trust"]
    )
    assert other_projection[0]["role"] == "other"
    other_request = other_draft["nodes"][0]["agent_request"]
    assert tuple(other_request[field] for field in ("role", "provider_key", "model_key", "profile_key", "credential_key")) in allowed_bindings

    # This registry is deliberately not admitted by the v1 authority. It proves only that the
    # structural pool schema can carry a future accepted role without a source-schema enum edit.
    schema_validate(illustrative_v2, "role-registry-envelope.schema.json", "DG_ROLE_REGISTRY_SCHEMA_INVALID")
    illustrative_ids = [row["role_id"] for row in illustrative_v2["roles"] if row["enabled"]]
    assert len(illustrative_ids) == len(set(illustrative_ids)) and "researcher" in illustrative_ids
    future_source = copy.deepcopy(base["source"])
    future_source["documents"][1]["scientists"][0]["role_fit"][0] = "researcher"
    future_normalized = normalize_canonical_pool(future_source, set(illustrative_ids))
    assert future_normalized["agents"][0]["role_fit"][0] == "researcher"

    real_raw = REAL_POOL.read_bytes()
    migrated = verify_and_migrate_real_pool(real_raw, migration_authority, set(ROLE_IDS))
    assert migrated["documents"][0]["version"] == "0.7.0"
    assert len(migrated["documents"][1]["scientists"]) == 414
    assert all("agent_name" in row and "name" not in row for row in migrated["documents"][1]["scientists"])
    real_stream = load_yaml_stream_text(real_raw.decode("utf-8"))

    vectors = load_json(FIXTURES / "negative-vectors.json")["vectors"]
    for vector in vectors:
        validate_vector(vector, base, real_stream, migration_authority)

    print("PASS: schemas, positive identity projection, Ed25519 evidence, singular other, and structural future role")
    print("PASS: real two-document pool v0.6 verified and losslessly projected to canonical v0.7 shape (414 entries)")
    print(f"PASS: {len(vectors)}/{len(vectors)} typed negative vectors with exact paths")
    print("LIMIT: specification fixtures only; production pool, consumers, registrar, compiler, and telemetry are unchanged")


if __name__ == "__main__":
    main()
