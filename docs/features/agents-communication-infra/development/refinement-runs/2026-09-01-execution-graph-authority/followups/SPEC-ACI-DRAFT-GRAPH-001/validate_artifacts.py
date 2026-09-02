"""Validate SWU artifacts and reviewer regressions without implementing compilation."""

from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, ValidationError


HERE = Path(__file__).resolve().parent
EG_SCHEMA_PATH = HERE.parents[1] / "stages/06-invoke-design/execution-graph-v2.proposed.schema.json"
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load(relative: str | Path) -> Any:
    path = relative if isinstance(relative, Path) else HERE / relative
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)


def index(items: list[dict[str, Any]], key: str = "key") -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for item in items:
        assert item[key] not in result, ("duplicate", key, item[key])
        result[item[key]] = item
    return result


draft_schema = load("draft-graph-v1.proposed.schema.json")
draft = load("review-correct-verify.draft.json")
context = load("fixtures/compilation-context.json")
execution_schema = load(EG_SCHEMA_PATH)
execution = load("review-correct-verify.expected.execution.json")
policy = load("fixtures/policy.json")
catalog = load("fixtures/catalog.json")
resource_set = load("fixtures/resources.json")
draft_validator = Draft202012Validator(draft_schema)
execution_validator = Draft202012Validator(execution_schema)

resources = index(resource_set["resources"], "resource_key")
providers = index(catalog["providers"])
models = index(catalog["models"])
profiles = index(catalog["profiles"])
capabilities = index(catalog["capabilities"])
validators = index(catalog["validators"])
semantics = index(catalog["semantics"])


def validate_context(value: dict[str, Any]) -> None:
    assert set(value) == {
        "schema",
        "dispatch_id",
        "revision",
        "allocation_id",
        "allocation_status",
        "prior_accepted_graph_digest",
    }
    assert value["schema"] == "aci.compilation-context-fixture@1"
    assert all(isinstance(value[key], str) and value[key] for key in ("dispatch_id", "revision", "allocation_id"))
    assert value["allocation_status"] == "reserved", "DG_IDENTITY_CONTEXT_STALE"
    prior = value["prior_accepted_graph_digest"]
    assert prior is None or DIGEST_RE.fullmatch(prior)
    revision_number = int(re.fullmatch(r"r([1-9][0-9]*)", value["revision"]).group(1))
    assert (revision_number == 1 and prior is None) or (revision_number > 1 and prior is not None)


def evaluate_limits(value: dict[str, Any]) -> tuple[dict[str, int], list[dict[str, int]], list[dict[str, Any]], str | None]:
    dimensions = ("max_attempts", "max_tokens", "wall_clock_seconds")
    effective_global: dict[str, int] = {}
    effective_nodes: list[dict[str, int]] = []
    report: list[dict[str, Any]] = []
    for dimension in dimensions:
        requested = value["requested_global_limits"][dimension]
        ceiling = policy["global_limit_ceiling"][dimension]
        effective_global[dimension] = min(requested, ceiling)
        if requested != effective_global[dimension]:
            report.append({
                "kind": "numeric_limit_restriction",
                "path": f"global_limits.{dimension}",
                "requested": requested,
                "effective": effective_global[dimension],
                "policy_ceiling": ceiling,
            })
    for node in value["nodes"]:
        effective: dict[str, int] = {}
        for dimension in dimensions:
            requested = node["requested_limits"][dimension]
            ceiling = policy["node_limit_ceiling"][dimension]
            effective[dimension] = min(requested, ceiling)
            if requested != effective[dimension]:
                report.append({
                    "kind": "numeric_limit_restriction",
                    "path": f"nodes[{node['key']}].limits.{dimension}",
                    "requested": requested,
                    "effective": effective[dimension],
                    "policy_ceiling": ceiling,
                })
        effective_nodes.append(effective)
    for dimension in dimensions:
        if sum(node[dimension] for node in effective_nodes) > effective_global[dimension]:
            return effective_global, effective_nodes, report, "DG_GLOBAL_BUDGET_EXCEEDED"
    return effective_global, effective_nodes, report, None


def decode_pointer_token(token: str) -> str:
    result = ""
    position = 0
    while position < len(token):
        if token[position] != "~":
            result += token[position]
            position += 1
            continue
        assert position + 1 < len(token) and token[position + 1] in {"0", "1"}, "DG_PREDICATE_POINTER_INVALID"
        result += "~" if token[position + 1] == "0" else "/"
        position += 2
    return result


def resolve_pointer_subschema(schema: dict[str, Any], pointer: str) -> dict[str, Any]:
    assert pointer.startswith("/"), "DG_PREDICATE_POINTER_INVALID"
    tokens = [decode_pointer_token(token) for token in pointer[1:].split("/")]
    current: Any = schema
    unsupported = {"$ref", "$dynamicRef", "allOf", "anyOf", "oneOf", "not", "if", "then", "else"}
    for token in tokens:
        assert isinstance(current, dict) and not (set(current) & unsupported), "DG_PREDICATE_POINTER_UNPROVABLE"
        if current.get("type") == "object":
            properties = current.get("properties")
            assert isinstance(properties, dict) and token in properties, "DG_PREDICATE_POINTER_INVALID"
            assert token in current.get("required", []), "DG_PREDICATE_POINTER_UNPROVABLE"
            current = properties[token]
        elif current.get("type") == "array":
            assert token.isdigit() and (token == "0" or not token.startswith("0")), "DG_PREDICATE_POINTER_INVALID"
            assert isinstance(current.get("items"), dict), "DG_PREDICATE_POINTER_UNPROVABLE"
            assert int(token) < current.get("minItems", 0), "DG_PREDICATE_POINTER_UNPROVABLE"
            current = current["items"]
        else:
            raise AssertionError("DG_PREDICATE_POINTER_UNPROVABLE")
    assert isinstance(current, dict) and not (set(current) & unsupported), "DG_PREDICATE_POINTER_UNPROVABLE"
    assert set(current) & {"type", "const", "enum"}, "DG_PREDICATE_POINTER_UNPROVABLE"
    Draft202012Validator.check_schema(current)
    return current


def validate_output_field_predicate(predicate: dict[str, Any], output_schema: dict[str, Any]) -> None:
    if predicate["kind"] != "output_field_equals":
        return
    subschema = resolve_pointer_subschema(output_schema, predicate["json_pointer"])
    try:
        Draft202012Validator(subschema).validate(predicate["value"])
    except ValidationError as error:
        raise AssertionError("DG_PREDICATE_VALUE_INVALID") from error


def validate_draft_semantics(value: dict[str, Any]) -> tuple[dict[str, int], list[dict[str, int]]]:
    draft_validator.validate(value)
    nodes = index(value["nodes"])
    bindings = index(value["resources"], "alias")
    assert len({item["resource_key"] for item in value["resources"]}) == len(value["resources"])
    for binding in value["resources"]:
        assert binding["resource_key"] in resources
    for node_position, node in enumerate(value["nodes"]):
        request = node["agent_request"]
        tuple_keys = ("role", "provider_key", "model_key", "profile_key", "credential_key")
        assert any(all(request[key] == row[key] for key in tuple_keys) for row in policy["allowed_agent_bindings"])
        assert request["provider_key"] in providers and request["model_key"] in models and request["profile_key"] in profiles
        assert models[request["model_key"]]["provider_key"] == request["provider_key"]
        assert profiles[request["profile_key"]]["provider_key"] == request["provider_key"]
        assert profiles[request["profile_key"]]["model_key"] == request["model_key"]
        inputs = index(node["inputs"])
        outputs = index(node["outputs"])
        index(node["validation"])
        index(node["capability_requests"], "capability_key")
        for capability in node["capability_requests"]:
            record = capabilities[capability["capability_key"]]
            grant = next(row for row in policy["capability_grants"] if row["capability_key"] == capability["capability_key"])
            assert set(capability["operations"]) <= set(record["operations"]) & set(grant["allowed_operations"])
        for item in node["inputs"]:
            source = item["source"]
            if source["kind"] == "resource":
                assert source["resource_alias"] in bindings
            else:
                assert source["node_key"] in nodes
                assert list(nodes).index(source["node_key"]) < node_position
                assert source["output_key"] in {output["key"] for output in nodes[source["node_key"]]["outputs"]}
        output_schemas: dict[str, dict[str, Any]] = {}
        for output in node["outputs"]:
            resource = resources[bindings[output["contract_resource_alias"]]["resource_key"]]
            schema = json.loads(resource["content"])
            assert resource["kind"] == "schema"
            assert schema.get("type") == "object" and schema.get("additionalProperties") is False
            Draft202012Validator.check_schema(schema)
            output_schemas[output["key"]] = schema
        for validation in node["validation"]:
            assert validation["validator_key"] in validators and validation["validator_key"] in policy["allowed_validator_keys"]
            if validation["configuration_resource_alias"] is not None:
                key = bindings[validation["configuration_resource_alias"]]["resource_key"]
                assert resources[key]["kind"] == "schema"
        success = node["success_condition"]
        assert success["kind"] in {"output_present", "output_field_equals"}
        assert success["output_key"] in outputs and outputs[success["output_key"]]["required"] is True
        validate_output_field_predicate(success, output_schemas[success["output_key"]])
        for stop in node["stop_conditions"]:
            predicate = stop["when"]
            if predicate["kind"] in {"output_present", "output_field_equals"}:
                assert predicate["output_key"] in outputs
                validate_output_field_predicate(predicate, output_schemas[predicate["output_key"]])
            if predicate["kind"] == "input_unavailable":
                assert predicate["input_key"] in inputs and inputs[predicate["input_key"]]["required"] is True
            if predicate["kind"] == "attempts_exhausted":
                assert stop["action"] in {"stop_node", "fail_graph"}
        access = node["access_request"]
        assert set(access["read_paths"]) <= set(policy["access_ceiling"]["read_paths"])
        assert set(access["write_paths"]) <= set(policy["access_ceiling"]["write_paths"])
        assert access["network"] == policy["access_ceiling"]["network"]
        assert access["external_effects"] == policy["access_ceiling"]["external_effects"]
        assert access["version_control"] == policy["access_ceiling"]["version_control"]
        assert access["commands"] == {"mode": "deny", "grants": []}
    effective_global, effective_nodes, _, error = evaluate_limits(value)
    assert error is None, error
    assert all(key in nodes for key in value["lifecycle"]["entry_node_keys"] + value["lifecycle"]["terminal_node_keys"])
    return effective_global, effective_nodes


def map_predicate(value: dict[str, Any]) -> dict[str, Any]:
    result = dict(value)
    if "output_key" in result:
        result["output_id"] = "output:" + result.pop("output_key")
    if "input_key" in result:
        result["input_id"] = "input:" + result.pop("input_key")
    return result


def expected_execution(value: dict[str, Any], frozen_context: dict[str, Any]) -> dict[str, Any]:
    effective_global, effective_nodes = validate_draft_semantics(value)
    bindings = index(value["resources"], "alias")
    member_aliases = [binding["alias"] for binding in value["resources"]] + ["receipt_schema"]
    members = []
    for alias in member_aliases:
        resource_key = bindings[alias]["resource_key"] if alias in bindings else alias
        resource = resources[resource_key]
        members.append({"member_id": "member:" + alias, **{key: resource[key] for key in ("kind", "media_type", "encoding", "content", "digest")}})
    emitted_nodes = []
    for node, limits in zip(value["nodes"], effective_nodes, strict=True):
        request = node["agent_request"]
        emitted_inputs = []
        for item in node["inputs"]:
            source = item["source"]
            if source["kind"] == "resource":
                mapped = {"kind": "content_member", "member_id": "member:" + source["resource_alias"], "selector": source["selector"]}
            else:
                mapped = {"kind": "node_output", "node_id": "node:" + source["node_key"], "output_id": "output:" + source["output_key"]}
            emitted_inputs.append({"input_id": "input:" + item["key"], "required": item["required"], "source": mapped})
        emitted_nodes.append({
            "node_id": "node:" + node["key"],
            "objective": node["objective"],
            "instructions": node["instructions"],
            "agent": {
                "display_name": request["display_name"],
                "role": request["role"],
                "provider_ref": providers[request["provider_key"]]["ref"],
                "model_ref": models[request["model_key"]]["ref"],
                "profile_ref": profiles[request["profile_key"]]["ref"],
                "credential_ref": None,
            },
            "tools": [{"tool_ref": capabilities[item["capability_key"]]["tool_ref"], "allowed_operations": item["operations"]} for item in node["capability_requests"]],
            "inputs": emitted_inputs,
            "outputs": [{"output_id": "output:" + item["key"], "schema_member_id": "member:" + item["contract_resource_alias"], "required": item["required"]} for item in node["outputs"]],
            "limits": limits,
            "isolation": node["access_request"],
            "start_when": node["start_when"],
            "validation": [{
                "rule_id": "rule:" + item["key"],
                "validator_ref": validators[item["validator_key"]]["ref"],
                "configuration_member_id": None if item["configuration_resource_alias"] is None else "member:" + item["configuration_resource_alias"],
                "on_fail": item["on_fail"],
            } for item in node["validation"]],
            "success_condition": map_predicate(node["success_condition"]),
            "stop_conditions": [{"when": map_predicate(item["when"]), "action": item["action"], "reason_code": item["reason_code"]} for item in node["stop_conditions"]],
        })
    edges: list[dict[str, str]] = []
    seen_pairs: set[tuple[str, str]] = set()
    for consumer in value["nodes"]:
        for item in consumer["inputs"]:
            source = item["source"]
            if source["kind"] == "node_output":
                pair = (source["node_key"], consumer["key"])
                if pair not in seen_pairs:
                    seen_pairs.add(pair)
                    edges.append({"edge_id": f"edge:{pair[0]}:{pair[1]}:data", "from_node_id": "node:" + pair[0], "to_node_id": "node:" + pair[1], "kind": "data", "condition": "on_success"})
    lifecycle = value["lifecycle"]
    audit = policy["audit_requirements"]
    return {
        "schema": "aci.execution-graph@2",
        "dispatch_id": frozen_context["dispatch_id"],
        "revision": frozen_context["revision"],
        "objective": value["objective"],
        "semantics_ref": semantics[policy["semantics_key"]]["ref"],
        "content_members": members,
        "global_limits": effective_global,
        "nodes": emitted_nodes,
        "edges": edges,
        "lifecycle": {
            "entry_nodes": ["node:" + key for key in lifecycle["entry_node_keys"]],
            "terminal_nodes": ["node:" + key for key in lifecycle["terminal_node_keys"]],
            "completion": lifecycle["completion"],
            "failure": lifecycle["failure"],
            "cancellation": lifecycle["cancellation"],
            "max_parallel_nodes": lifecycle["max_parallel_nodes"],
        },
        "audit_requirements": {
            "record_objective": audit["record_objective"],
            "record_agents": audit["record_agents"],
            "record_route": audit["record_route"],
            "record_results": audit["record_results"],
            "receipt_schema_member_id": "member:" + audit["receipt_schema_resource_key"],
        },
    }


def validate_execution_semantics(value: dict[str, Any]) -> None:
    execution_validator.validate(value)
    members = index(value["content_members"], "member_id")
    nodes = index(value["nodes"], "node_id")
    index(value["edges"], "edge_id")
    for node in value["nodes"]:
        inputs = index(node["inputs"], "input_id")
        outputs = index(node["outputs"], "output_id")
        index(node["validation"], "rule_id")
        for item in node["inputs"]:
            source = item["source"]
            if source["kind"] == "content_member":
                assert source["member_id"] in members
            else:
                assert source["node_id"] in nodes
                assert source["output_id"] in {output["output_id"] for output in nodes[source["node_id"]]["outputs"]}
        output_schemas: dict[str, dict[str, Any]] = {}
        for output in node["outputs"]:
            assert output["schema_member_id"] in members and members[output["schema_member_id"]]["kind"] == "schema"
            schema = json.loads(members[output["schema_member_id"]]["content"])
            Draft202012Validator.check_schema(schema)
            output_schemas[output["output_id"]] = schema
        success = node["success_condition"]
        assert success["kind"] in {"output_present", "output_field_equals"}
        assert success["output_id"] in outputs and outputs[success["output_id"]]["required"] is True
        validate_output_field_predicate(success, output_schemas[success["output_id"]])
        for stop in node["stop_conditions"]:
            predicate = stop["when"]
            if "input_id" in predicate:
                assert predicate["input_id"] in inputs
            if "output_id" in predicate:
                assert predicate["output_id"] in outputs
                validate_output_field_predicate(predicate, output_schemas[predicate["output_id"]])
            if predicate["kind"] == "attempts_exhausted":
                assert stop["action"] in {"stop_node", "fail_graph"}
    for edge in value["edges"]:
        assert edge["from_node_id"] in nodes and edge["to_node_id"] in nodes
    assert all(node_id in nodes for node_id in value["lifecycle"]["entry_nodes"] + value["lifecycle"]["terminal_nodes"])
    receipt = value["audit_requirements"]["receipt_schema_member_id"]
    assert receipt in members and members[receipt]["kind"] == "schema"


def validate_mapping(value: dict[str, Any]) -> None:
    validate_execution_semantics(value)
    assert value == expected_execution(draft, context), "DG_COMPILATION_MISMATCH"


def expect_mapping_rejection(value: dict[str, Any]) -> None:
    try:
        validate_mapping(value)
    except (AssertionError, StopIteration, ValidationError):
        return
    raise AssertionError("adversarial execution mutation was accepted")


all_json = list(HERE.rglob("*.json"))
for json_file in all_json:
    load(json_file)
Draft202012Validator.check_schema(draft_schema)
Draft202012Validator.check_schema(execution_schema)
validate_context(context)
validate_draft_semantics(draft)
validate_execution_semantics(execution)
print(f"PASS schemas, context and duplicate-key parsing: {len(all_json)} JSON files")

for item in resources.values():
    actual = "sha256:" + hashlib.sha256(item["content"].encode(item["encoding"])).hexdigest()
    assert actual == item["digest"], (item["resource_key"], actual, item["digest"])
for table in ("semantics", "providers", "models", "profiles", "capabilities", "validators"):
    for item in catalog[table]:
        actual = "sha256:" + hashlib.sha256(item["digest_source"].encode("utf-8")).hexdigest()
        expected = (item.get("ref") or item["tool_ref"])["digest"]
        assert actual == expected, (table, item["key"], actual, expected)
print("PASS fixture digests: 5 resources and 10 catalog records")

validate_mapping(execution)
print("PASS exact full-collection draft+context+fixtures to expected-EG mapping")

# F1: author input cannot select authority identity/revision; stale allocation fails closed.
for obsolete_key, obsolete_value in (("graph_key", "chosen_by_model"), ("draft_revision", 99)):
    mutation = copy.deepcopy(draft)
    mutation[obsolete_key] = obsolete_value
    assert list(draft_validator.iter_errors(mutation))
stale_context = copy.deepcopy(context)
stale_context["allocation_status"] = "released"
try:
    validate_context(stale_context)
except AssertionError as error:
    assert "DG_IDENTITY_CONTEXT_STALE" in str(error)
else:
    raise AssertionError("stale identity context accepted")
print("PASS F1 regressions: author identity/revision rejected; stale system context rejected")

# F2: the reviewed 30k case fails; the safe restriction has one exact report record.
overflow = copy.deepcopy(draft)
next(node for node in overflow["nodes"] if node["key"] == "review")["requested_limits"]["max_tokens"] = 13000
global_limits, node_limits, _, error = evaluate_limits(overflow)
assert [node["max_tokens"] for node in node_limits] == [12000, 12000, 6000]
assert sum(node["max_tokens"] for node in node_limits) == 30000 and global_limits["max_tokens"] == 24000
assert error == "DG_GLOBAL_BUDGET_EXCEEDED"
safe = copy.deepcopy(draft)
next(node for node in safe["nodes"] if node["key"] == "correct")["requested_limits"]["max_tokens"] = 13000
global_limits, node_limits, report, error = evaluate_limits(safe)
assert error is None and sum(node["max_tokens"] for node in node_limits) == global_limits["max_tokens"] == 24000
assert report == [{"kind": "numeric_limit_restriction", "path": "nodes[correct].limits.max_tokens", "requested": 13000, "effective": 12000, "policy_ceiling": 12000}]
print("PASS F2 regressions: 30k/24k rejected; safe restriction report exact")

# F3: extra/missing/duplicate executable collections cannot hide behind truncating comparisons.
mutations: list[dict[str, Any]] = []
extra_node = copy.deepcopy(execution)
node = copy.deepcopy(extra_node["nodes"][-1]); node["node_id"] = "node:extra"; extra_node["nodes"].append(node); mutations.append(extra_node)
duplicate_node = copy.deepcopy(execution); duplicate_node["nodes"].append(copy.deepcopy(duplicate_node["nodes"][-1])); mutations.append(duplicate_node)
missing_node = copy.deepcopy(execution); missing_node["nodes"].pop(); mutations.append(missing_node)
extra_tool = copy.deepcopy(execution); extra_tool["nodes"][0]["tools"].append(copy.deepcopy(execution["nodes"][1]["tools"][0])); mutations.append(extra_tool)
duplicate_tool = copy.deepcopy(execution); duplicate_tool["nodes"][1]["tools"].append(copy.deepcopy(duplicate_tool["nodes"][1]["tools"][0])); mutations.append(duplicate_tool)
missing_tool = copy.deepcopy(execution); missing_tool["nodes"][1]["tools"].clear(); mutations.append(missing_tool)
for collection, template in (
    ("inputs", execution["nodes"][0]["inputs"][0]),
    ("outputs", execution["nodes"][0]["outputs"][0]),
    ("validation", execution["nodes"][0]["validation"][0]),
    ("stop_conditions", execution["nodes"][0]["stop_conditions"][0]),
):
    extra = copy.deepcopy(execution); extra["nodes"][0][collection].append(copy.deepcopy(template)); mutations.append(extra)
    missing = copy.deepcopy(execution); missing["nodes"][0][collection].pop(); mutations.append(missing)
extra_command = copy.deepcopy(execution)
extra_command["nodes"][0]["isolation"]["commands"] = {
    "mode": "allowlist",
    "grants": [{"command_ref": catalog["capabilities"][0]["tool_ref"], "argv": ["x"], "cwd": "workspace:/target", "environment_member_id": None}],
}
mutations.append(extra_command)
lifecycle_drift = copy.deepcopy(execution); lifecycle_drift["lifecycle"]["max_parallel_nodes"] = 2; mutations.append(lifecycle_drift)
audit_drift = copy.deepcopy(execution); audit_drift["audit_requirements"]["record_route"] = False; mutations.append(audit_drift)
for mutation in mutations:
    expect_mapping_rejection(mutation)
print(f"PASS F3 regressions: {len(mutations)} extra/missing/duplicate authority mutations rejected")

# F4: failure predicates cannot become success, and success must target a required output.
for bad_success in ({"kind": "attempts_exhausted"}, {"kind": "input_unavailable", "input_key": "target"}):
    mutation = copy.deepcopy(draft)
    mutation["nodes"][0]["success_condition"] = bad_success
    assert list(draft_validator.iter_errors(mutation))
optional_success = copy.deepcopy(draft)
optional_success["nodes"][0]["outputs"][0]["required"] = False
draft_validator.validate(optional_success)
try:
    validate_draft_semantics(optional_success)
except AssertionError:
    pass
else:
    raise AssertionError("optional output accepted as success proof")
print("PASS F4 regressions: failure-as-success and optional-output success rejected")

# F5: DraftGraph v1 has no command allowlist/tuple branch.
command_draft = copy.deepcopy(draft)
command_draft["nodes"][1]["access_request"]["commands"] = {
    "mode": "allowlist",
    "grants": [{"command_key": "shell", "argv": ["-c", "work"], "cwd": "workspace:/target", "environment_resource_alias": None}],
}
assert list(draft_validator.iter_errors(command_draft))
print("PASS F5 regression: command allowlist/argv/cwd/environment tuple rejected structurally")

# R1: successor work pack stays synchronized with the repaired input/vector/review contract.
work_pack = (HERE / "WORK-PACK.md").read_text(encoding="utf-8")
for required_text in (
    "exactly five positive compiler inputs",
    "`DG-N01` through `DG-N24`",
    "`DG-N09` returns `DG_GLOBAL_BUDGET_EXCEEDED`",
    "`DG-N11` is the only safe numeric-restriction vector",
    "aggregate `KEEP`",
    "artifact `FIX`",
):
    assert required_text in work_pack, required_text
for stale_text in ("four input fixtures", "`DG-N01` through `DG-N10`", "`DG-N01` through `DG-N20`", "except `DG-N09`"):
    assert stale_text not in work_pack, stale_text
print("PASS R1 regression: work-pack inputs, N01-N24 outcomes and KEEP/FIX gate synchronized")

# R2: both draft and emitted-EG semantic paths reject unprovable pointers and inadmissible values.
for pointer, candidate_value, expected_error in (
    ("/does_not_exist", "pass", "DG_PREDICATE_POINTER_INVALID"),
    ("/verdict", "bogus", "DG_PREDICATE_VALUE_INVALID"),
):
    draft_attack = copy.deepcopy(draft)
    draft_attack["nodes"][2]["success_condition"]["json_pointer"] = pointer
    draft_attack["nodes"][2]["success_condition"]["value"] = candidate_value
    draft_validator.validate(draft_attack)
    try:
        validate_draft_semantics(draft_attack)
    except AssertionError as error:
        assert expected_error in str(error), (expected_error, str(error))
    else:
        raise AssertionError(f"draft predicate attack accepted: {expected_error}")
    execution_attack = copy.deepcopy(execution)
    execution_attack["nodes"][2]["success_condition"]["json_pointer"] = pointer
    execution_attack["nodes"][2]["success_condition"]["value"] = candidate_value
    execution_validator.validate(execution_attack)
    try:
        validate_execution_semantics(execution_attack)
    except AssertionError as error:
        assert expected_error in str(error), (expected_error, str(error))
    else:
        raise AssertionError(f"execution predicate attack accepted: {expected_error}")
print("PASS R2 regressions: missing pointer and enum-invalid value rejected in draft and emitted EG")

# S1: applicator keywords never prove ancestor type; typeless/nullable ancestors fail symmetrically.
verification_resource = resources["verification_schema"]
original_verification_content = verification_resource["content"]
ancestor_attacks = (
    ("nested", {"properties": {"leaf": {"type": "string"}}, "required": ["leaf"]}, 5, "/nested/leaf"),
    ("nested", {"type": ["object", "null"], "properties": {"leaf": {"type": "string"}}, "required": ["leaf"]}, None, "/nested/leaf"),
    ("arr", {"items": {"type": "string"}, "minItems": 1}, 5, "/arr/0"),
    ("arr", {"type": ["array", "null"], "items": {"type": "string"}, "minItems": 1}, None, "/arr/0"),
)
for field, ancestor_schema, counterexample_value, pointer in ancestor_attacks:
    hostile_schema = {
        "type": "object",
        "required": ["verdict", field],
        "properties": {
            "verdict": {"enum": ["pass", "flag", "block"]},
            field: ancestor_schema,
        },
        "additionalProperties": False,
    }
    Draft202012Validator.check_schema(hostile_schema)
    Draft202012Validator(hostile_schema).validate({"verdict": "pass", field: counterexample_value})
    hostile_content = json.dumps(hostile_schema, separators=(",", ":"))
    verification_resource["content"] = hostile_content
    draft_attack = copy.deepcopy(draft)
    draft_attack["nodes"][2]["success_condition"] = {
        "kind": "output_field_equals",
        "output_key": "verification",
        "json_pointer": pointer,
        "value": "ok",
    }
    draft_validator.validate(draft_attack)
    try:
        validate_draft_semantics(draft_attack)
    except AssertionError as error:
        assert "DG_PREDICATE_POINTER_UNPROVABLE" in str(error), str(error)
    else:
        raise AssertionError(f"draft S1 ancestor attack accepted: {ancestor_schema}")
    execution_attack = copy.deepcopy(execution)
    member = next(item for item in execution_attack["content_members"] if item["member_id"] == "member:verification_schema")
    member["content"] = hostile_content
    member["digest"] = "sha256:" + hashlib.sha256(hostile_content.encode()).hexdigest()
    execution_attack["nodes"][2]["success_condition"] = {
        "kind": "output_field_equals",
        "output_id": "output:verification",
        "json_pointer": pointer,
        "value": "ok",
    }
    execution_validator.validate(execution_attack)
    try:
        validate_execution_semantics(execution_attack)
    except AssertionError as error:
        assert "DG_PREDICATE_POINTER_UNPROVABLE" in str(error), str(error)
    else:
        raise AssertionError(f"execution S1 ancestor attack accepted: {ancestor_schema}")
verification_resource["content"] = original_verification_content
negative_vectors = (HERE / "NEGATIVE-VECTORS.md").read_text(encoding="utf-8")
for vector_id in (
    "DG-N21-PREDICATE-TYPELESS-OBJECT",
    "DG-N22-PREDICATE-NULLABLE-OBJECT",
    "DG-N23-PREDICATE-TYPELESS-ARRAY",
    "DG-N24-PREDICATE-NULLABLE-ARRAY",
):
    assert f"`{vector_id}`" in negative_vectors, vector_id
contract = (HERE / "COMPILATION-CONTRACT.md").read_text(encoding="utf-8")
assert 'literal `"type":"object"`' in contract and 'literal `"type":"array"`' in contract
ownership = (HERE / "FIELD-OWNERSHIP.md").read_text(encoding="utf-8")
pointer_row = next(line for line in ownership.splitlines() if "`.success_condition.json_pointer`" in line)
assert 'literal exact `type:"object"`' in pointer_row and 'literal exact `type:"array"`' in pointer_row
print("PASS S1 regressions: typeless/nullable object/array ancestors rejected symmetrically")

# Existing negative preconditions plus F6 claim discipline.
unknown = copy.deepcopy(draft); unknown["nodes"][1]["capability_requests"].append({"capability_key": "shell_exec", "operations": ["run"]}); draft_validator.validate(unknown); assert "shell_exec" not in capabilities
unknown = copy.deepcopy(draft); unknown["nodes"][2]["agent_request"]["model_key"] = "unlisted_model"; draft_validator.validate(unknown); assert "unlisted_model" not in models
unknown = copy.deepcopy(draft); unknown["nodes"][1]["access_request"]["write_paths"].append("workspace:/secrets"); draft_validator.validate(unknown); assert "workspace:/secrets" not in policy["access_ceiling"]["write_paths"]
unknown = copy.deepcopy(draft); unknown["nodes"][2]["inputs"][1]["source"]["node_key"] = "missing_reviewer"; draft_validator.validate(unknown)
try:
    validate_draft_semantics(unknown)
except AssertionError:
    pass
else:
    raise AssertionError("input without producer accepted")
bad_schema = {"type": "object", "required": ["patch"], "properties": {}, "additionalProperties": False}
bad_schema_bytes = json.dumps(bad_schema, separators=(",", ":")).encode()
assert set(bad_schema["required"]) - set(bad_schema["properties"])
assert "sha256:" + hashlib.sha256(bad_schema_bytes).hexdigest() == "sha256:9b7f66b69daca245218bd6af6d627fab7cebad36ff9766fe48987a84ccb0994a"
ambiguous = copy.deepcopy(draft); ambiguous["nodes"][2]["success_condition"] = {"kind": "free_text", "expression": "looks good"}; assert list(draft_validator.iter_errors(ambiguous))
unknown = copy.deepcopy(draft); unknown["nodes"][0]["validation"][0]["validator_key"] = "best_effort_review"; draft_validator.validate(unknown); assert "best_effort_review" not in validators
assert "sha256:" + hashlib.sha256((resources["result_x"]["content"] + "!").encode()).hexdigest() != resources["result_x"]["digest"]
expanded_network = copy.deepcopy(execution); expanded_network["nodes"][2]["isolation"]["network"] = {"mode": "allowlist", "allow": ["internet"]}; expect_mapping_rejection(expanded_network)
done_when_row = next(line for line in ownership.splitlines() if "`objective.done_when[]`" in line)
assert "validators" not in done_when_row and "non-controlling" in done_when_row
print("PASS remaining negative preconditions and F6 non-controlling done_when ownership")

leaf_paths: set[str] = set()


def walk_schema(value: dict[str, Any], path: str = "") -> None:
    if "$ref" in value:
        value = execution_schema["$defs"][value["$ref"].split("/")[-1]]
    if "oneOf" in value:
        for branch in value["oneOf"]:
            walk_schema(branch, path)
    elif value.get("type") == "object" or "properties" in value:
        for key, child in value.get("properties", {}).items():
            walk_schema(child, f"{path}.{key}" if path else key)
    elif value.get("type") == "array":
        walk_schema(value["items"], path + "[]")
    else:
        leaf_paths.add(path)


walk_schema(execution_schema)
missing = sorted(path for path in leaf_paths if f"\n{path}\n" not in ownership)
assert not missing, missing
print(f"PASS field-ownership inventory: {len(leaf_paths)} of {len(leaf_paths)} schema leaves")
print("EVIDENCE LIMIT: no compiler, live allocator or RFC 8785 canonicalizer executed")
