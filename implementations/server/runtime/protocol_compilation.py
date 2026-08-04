"""Pure bounded compiler for ACI protocol-candidate fixture package v1."""

from __future__ import annotations

import heapq
import re
from typing import Any

from .canonical import canonical_bytes, canonical_text, digest_bytes, parse_strict_json
from .errors import RuntimeContractError, ValidationError


COMPILER_CONTRACT_DIGEST = "sha256:9fd10473647a5ea5a7f03df6370773fab2af911cca9d37ffc1e2b7912a009543"
ADMITTED_TUPLES = {
    (
        "sha256:43229944b101d12c6d14008d1db17f40c41277b7b441417c7ca5cd38006d7d17",
        "sha256:26d7a8a3fb4955a9442d5807b7c27c1c1f204b394e3862437c49a4aae5b14c7b",
        "sha256:92fbf20eebbe5ba490bcd1969eed86e3ae91e4e643d7f448a1a089d3be2b50e3",
        "sha256:469dff24fc67a048a0f5f7040704c3601861beb386b9713dc3eb4e3b233de77b",
    ),
    (
        "sha256:43ec4c29eca01a6786ec9fff2723c2623828af286e80c67f2b320672d002fa1e",
        "sha256:10bc707b787041d8b3327a1f3096b5635fae56d75975b0ffbf81f82fa2b00f8a",
        "sha256:16ce0d514a5b1b42d1c2170d0c4eb8b04a72d150adb4f7bb7b0ef91796c8aaa1",
        "sha256:0fdbd75e214f91a0ad53cec35849d43208af1d51dfa1f1c0300cfa0be3a11c17",
    ),
}

_DIGEST = re.compile(r"sha256:[0-9a-f]{64}\Z")
_PLACEHOLDER = re.compile(r"\{\{parameter:([^{}]+)\}\}")
_REQUEST_FIELDS = {
    "schema", "profile_document", "profile_digest", "binding_document", "binding_digest",
    "recipe_document", "recipe_digest", "invocation_document", "invocation_digest",
    "compiler_contract_digest",
}


class ProtocolCompileFailure(RuntimeContractError):
    """Stable typed rejection from protocol compilation or its storage seam."""

    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(detail or code)
        self.code = code
        self.detail = detail


def _fail(code: str, detail: str) -> None:
    raise ProtocolCompileFailure(code, detail)


def _exact(obj: Any, fields: set[str], name: str) -> dict[str, Any]:
    if not isinstance(obj, dict) or set(obj) != fields:
        raise ValueError(f"{name} must contain exactly {sorted(fields)}")
    return obj


def _text(value: Any, name: str, *, maximum: int = 128) -> str:
    if not isinstance(value, str) or not value or len(value.encode("utf-8")) > maximum:
        raise ValueError(f"{name} must be non-empty bounded text")
    return value


def _digest(value: Any, name: str) -> str:
    if not isinstance(value, str) or not _DIGEST.fullmatch(value):
        raise ValueError(f"{name} must be a qualified lowercase SHA-256 digest")
    return value


def _boolean(value: Any, name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{name} must be boolean")
    return value


def _sorted_unique(items: Any, key, name: str, maximum: int, *, nonempty: bool = False) -> list[Any]:
    if not isinstance(items, list) or len(items) > maximum or (nonempty and not items):
        raise ValueError(f"{name} has invalid cardinality")
    keys = [key(item) for item in items]
    if keys != sorted(keys) or len(keys) != len(set(keys)):
        raise ValueError(f"{name} must be sorted and unique")
    return items


def _scalar_schema(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be object")
    allowed = {"type", "enum_values", "min_length", "max_length"}
    if "type" not in value or set(value) - allowed:
        raise ValueError(f"{name} has invalid fields")
    kind = value["type"]
    if kind not in {"string", "integer", "boolean"}:
        raise ValueError(f"{name}.type is invalid")
    if kind != "string" and ({"min_length", "max_length"} & set(value)):
        raise ValueError(f"{name} length bounds require string")
    lower = value.get("min_length", 0)
    upper = value.get("max_length", 65536)
    if any(isinstance(v, bool) or not isinstance(v, int) or not 0 <= v <= 65536 for v in (lower, upper)) or lower > upper:
        raise ValueError(f"{name} length bounds are invalid")
    if "enum_values" in value:
        enum = value["enum_values"]
        if not isinstance(enum, list) or not enum:
            raise ValueError(f"{name}.enum_values must be non-empty")
        for member in enum:
            _validate_scalar(member, {"type": kind}, name)
        if enum != sorted(enum) or len({canonical_text(x) for x in enum}) != len(enum):
            raise ValueError(f"{name}.enum_values must be sorted and unique")
    return value


def _validate_scalar(value: Any, schema: dict[str, Any], name: str) -> None:
    kind = schema["type"]
    valid = ((kind == "string" and isinstance(value, str)) or
             (kind == "integer" and isinstance(value, int) and not isinstance(value, bool)) or
             (kind == "boolean" and isinstance(value, bool)))
    if not valid:
        raise ValueError(f"{name} has wrong scalar type")
    if kind == "integer" and not -(2**63) <= value <= 2**63 - 1:
        raise ValueError(f"{name} is outside int64")
    if kind == "string" and not schema.get("min_length", 0) <= len(value) <= schema.get("max_length", 65536):
        raise ValueError(f"{name} violates length bounds")
    if "enum_values" in schema and value not in schema["enum_values"]:
        raise ValueError(f"{name} is outside enum")


def _validate_profile(value: Any) -> None:
    p = _exact(value, {"schema", "skill_id", "skill_revision_digest", "profile_revision", "obligations", "parameters", "capability_requirements", "outputs"}, "profile")
    if p["schema"] != "aci.skill-execution-profile@1": raise ValueError("profile schema")
    _text(p["skill_id"], "skill_id"); _digest(p["skill_revision_digest"], "skill_revision_digest"); _text(p["profile_revision"], "profile_revision")
    for item in _sorted_unique(p["obligations"], lambda x: x.get("obligation_id") if isinstance(x, dict) else None, "obligations", 256, nonempty=True):
        _exact(item, {"obligation_id", "statement", "required"}, "obligation"); _text(item["obligation_id"], "obligation_id"); _text(item["statement"], "statement", maximum=8192); _boolean(item["required"], "required")
    for item in _sorted_unique(p["parameters"], lambda x: x.get("parameter_id") if isinstance(x, dict) else None, "parameters", 128):
        _exact(item, {"parameter_id", "value_schema", "required"}, "parameter"); _text(item["parameter_id"], "parameter_id"); _scalar_schema(item["value_schema"], "value_schema"); _boolean(item["required"], "required")
    for item in _sorted_unique(p["capability_requirements"], lambda x: x.get("capability_id") if isinstance(x, dict) else None, "capabilities", 128):
        _exact(item, {"capability_id", "requirement", "required"}, "capability"); _text(item["capability_id"], "capability_id"); _text(item["requirement"], "requirement", maximum=8192); _boolean(item["required"], "required")
    for item in _sorted_unique(p["outputs"], lambda x: x.get("output_id") if isinstance(x, dict) else None, "outputs", 128, nonempty=True):
        _exact(item, {"output_id", "content_schema", "required"}, "output"); _text(item["output_id"], "output_id"); _scalar_schema(item["content_schema"], "content_schema"); _boolean(item["required"], "required")


def _validate_binding(value: Any) -> None:
    b = _exact(value, {"schema", "status", "skill_id", "skill_revision_digest", "profile_digest", "recipe_digest", "binding_revision"}, "binding")
    if b["schema"] != "aci.skill-protocol-binding@1" or b["status"] not in {"active", "stale", "superseded", "revoked"}: raise ValueError("binding schema/status")
    _text(b["skill_id"], "skill_id"); _digest(b["skill_revision_digest"], "skill_revision_digest"); _digest(b["profile_digest"], "profile_digest"); _digest(b["recipe_digest"], "recipe_digest"); _text(b["binding_revision"], "binding_revision")


def _validate_recipe(value: Any) -> None:
    r = _exact(value, {"schema", "recipe_id", "recipe_revision", "mode", "profile_digest", "nodes", "edges", "terminal_node_ids", "obligation_rules"}, "recipe")
    if r["schema"] != "aci.protocol-recipe@1" or r["mode"] != "read_only": raise ValueError("recipe schema/mode")
    _text(r["recipe_id"], "recipe_id"); _text(r["recipe_revision"], "recipe_revision"); _digest(r["profile_digest"], "profile_digest")
    for node in _sorted_unique(r["nodes"], lambda x: x.get("node_id") if isinstance(x, dict) else None, "nodes", 128, nonempty=True):
        _exact(node, {"node_id", "node_kind", "prompt_template", "parameter_ids", "capability_ids", "output_ids"}, "node")
        _text(node["node_id"], "node_id"); _text(node["prompt_template"], "prompt_template", maximum=65536)
        if node["node_kind"] not in {"work", "review", "decision", "integration", "projection", "terminal"}: raise ValueError("node_kind")
        for field in ("parameter_ids", "capability_ids", "output_ids"):
            _sorted_unique(node[field], lambda x: x, field, 128)
            for member in node[field]: _text(member, field)
    for edge in _sorted_unique(r["edges"], lambda x: (x.get("from_node_id"), x.get("to_node_id"), x.get("edge_id")) if isinstance(x, dict) else None, "edges", 512):
        _exact(edge, {"edge_id", "from_node_id", "to_node_id", "edge_kind"}, "edge")
        for field in ("edge_id", "from_node_id", "to_node_id"): _text(edge[field], field)
        if edge["edge_kind"] not in {"depends_on", "review_of", "feeds", "gates"}: raise ValueError("edge_kind")
    _sorted_unique(r["terminal_node_ids"], lambda x: x, "terminal_node_ids", 128, nonempty=True)
    for terminal_node_id in r["terminal_node_ids"]:
        _text(terminal_node_id, "terminal_node_id")
    for rule in _sorted_unique(r["obligation_rules"], lambda x: x.get("obligation_id") if isinstance(x, dict) else None, "obligation_rules", 256):
        if not isinstance(rule, dict) or set(rule) not in ({"obligation_id", "disposition", "target_refs"}, {"obligation_id", "disposition", "target_refs", "authority_ref"}): raise ValueError("obligation rule fields")
        _text(rule["obligation_id"], "obligation_id")
        if rule["disposition"] not in {"preserved", "compiled", "superseded", "unsupported"}: raise ValueError("disposition")
        _sorted_unique(rule["target_refs"], lambda x: x, "target_refs", 256)
        for target_ref in rule["target_refs"]:
            _text(target_ref, "target_ref", maximum=135)
        if "authority_ref" in rule:
            a = _exact(rule["authority_ref"], {"authority_kind", "authority_digest"}, "authority_ref"); _text(a["authority_kind"], "authority_kind"); _digest(a["authority_digest"], "authority_digest")


def _validate_invocation(value: Any) -> None:
    i = _exact(value, {"schema", "skill_id", "skill_revision_digest", "profile_digest", "binding_digest", "recipe_digest", "values"}, "invocation")
    if i["schema"] != "aci.skill-protocol-invocation@1": raise ValueError("invocation schema")
    _text(i["skill_id"], "skill_id"); _digest(i["skill_revision_digest"], "skill_revision_digest"); _digest(i["profile_digest"], "profile_digest"); _digest(i["binding_digest"], "binding_digest"); _digest(i["recipe_digest"], "recipe_digest")
    for item in _sorted_unique(i["values"], lambda x: x.get("parameter_id") if isinstance(x, dict) else None, "values", 128):
        _exact(item, {"parameter_id", "value"}, "value"); _text(item["parameter_id"], "parameter_id")
        if item["value"] is None or isinstance(item["value"], (dict, list, float)): raise ValueError("value must be scalar")


def _validate_candidate(value: Any) -> None:
    """Validate the complete closed candidate output before serialization."""
    candidate = _exact(
        value,
        {
            "schema", "source_binding", "invocation_values", "nodes", "edges",
            "terminal_node_ids", "obligation_dispositions",
            "capability_requirements", "outputs",
        },
        "candidate",
    )
    if candidate["schema"] != "aci.dispatch-candidate@1":
        raise ValueError("candidate schema")
    source = _exact(
        candidate["source_binding"],
        {
            "skill_id", "skill_revision_digest", "profile_digest", "binding_digest",
            "recipe_digest", "invocation_digest", "compiler_contract_digest",
        },
        "candidate source_binding",
    )
    _text(source["skill_id"], "candidate skill_id")
    for field in (
        "skill_revision_digest", "profile_digest", "binding_digest", "recipe_digest",
        "invocation_digest", "compiler_contract_digest",
    ):
        _digest(source[field], f"candidate {field}")

    for item in _sorted_unique(
        candidate["invocation_values"],
        lambda x: x.get("parameter_id") if isinstance(x, dict) else None,
        "candidate invocation_values",
        128,
    ):
        _exact(item, {"parameter_id", "value"}, "candidate invocation value")
        _text(item["parameter_id"], "candidate parameter_id")
        if item["value"] is None or isinstance(item["value"], (dict, list, float)):
            raise ValueError("candidate invocation value must be scalar")

    for node in _sorted_unique(
        candidate["nodes"],
        lambda x: x.get("node_id") if isinstance(x, dict) else None,
        "candidate nodes",
        128,
        nonempty=True,
    ):
        _exact(
            node,
            {"node_id", "node_kind", "prompt_template", "parameter_ids", "capability_ids", "output_ids"},
            "candidate node",
        )
        _text(node["node_id"], "candidate node_id")
        _text(node["prompt_template"], "candidate prompt_template", maximum=65536)
        if node["node_kind"] not in {"work", "review", "decision", "integration", "projection", "terminal"}:
            raise ValueError("candidate node_kind")
        for field in ("parameter_ids", "capability_ids", "output_ids"):
            _sorted_unique(node[field], lambda x: x, f"candidate {field}", 128)
            for member in node[field]:
                _text(member, f"candidate {field}")

    for edge in _sorted_unique(
        candidate["edges"],
        lambda x: (x.get("from_node_id"), x.get("to_node_id"), x.get("edge_id")) if isinstance(x, dict) else None,
        "candidate edges",
        512,
    ):
        _exact(edge, {"edge_id", "from_node_id", "to_node_id", "edge_kind"}, "candidate edge")
        for field in ("edge_id", "from_node_id", "to_node_id"):
            _text(edge[field], f"candidate {field}")
        if edge["edge_kind"] not in {"depends_on", "review_of", "feeds", "gates"}:
            raise ValueError("candidate edge_kind")

    _sorted_unique(candidate["terminal_node_ids"], lambda x: x, "candidate terminal_node_ids", 128, nonempty=True)
    for member in candidate["terminal_node_ids"]:
        _text(member, "candidate terminal_node_id")

    for rule in _sorted_unique(
        candidate["obligation_dispositions"],
        lambda x: x.get("obligation_id") if isinstance(x, dict) else None,
        "candidate obligation_dispositions",
        256,
    ):
        if not isinstance(rule, dict) or set(rule) not in (
            {"obligation_id", "disposition", "target_refs"},
            {"obligation_id", "disposition", "target_refs", "authority_ref"},
        ):
            raise ValueError("candidate obligation disposition fields")
        _text(rule["obligation_id"], "candidate obligation_id")
        if rule["disposition"] not in {"preserved", "compiled", "superseded", "unsupported"}:
            raise ValueError("candidate disposition")
        _sorted_unique(rule["target_refs"], lambda x: x, "candidate target_refs", 256)
        for ref in rule["target_refs"]:
            _text(ref, "candidate target_ref", maximum=135)
        if "authority_ref" in rule:
            authority = _exact(rule["authority_ref"], {"authority_kind", "authority_digest"}, "candidate authority_ref")
            _text(authority["authority_kind"], "candidate authority_kind")
            _digest(authority["authority_digest"], "candidate authority_digest")

    for capability in _sorted_unique(
        candidate["capability_requirements"],
        lambda x: x.get("capability_id") if isinstance(x, dict) else None,
        "candidate capability_requirements",
        128,
    ):
        _exact(capability, {"capability_id", "requirement", "required"}, "candidate capability")
        _text(capability["capability_id"], "candidate capability_id")
        _text(capability["requirement"], "candidate requirement", maximum=8192)
        _boolean(capability["required"], "candidate capability required")

    for output in _sorted_unique(
        candidate["outputs"],
        lambda x: x.get("output_id") if isinstance(x, dict) else None,
        "candidate outputs",
        128,
        nonempty=True,
    ):
        _exact(output, {"output_id", "content_schema", "required"}, "candidate output")
        _text(output["output_id"], "candidate output_id")
        _scalar_schema(output["content_schema"], "candidate content_schema")
        _boolean(output["required"], "candidate output required")


def _serialize_unsupported_result(unsupported_ids: list[str]) -> bytes:
    result = {
        "schema": "aci.compiled-dispatch-candidate-result@1",
        "outcome": "unsupported",
        "unsupported_obligation_ids": unsupported_ids,
    }
    _exact(result, {"schema", "outcome", "unsupported_obligation_ids"}, "unsupported result")
    if result["schema"] != "aci.compiled-dispatch-candidate-result@1" or result["outcome"] != "unsupported":
        raise ValueError("unsupported result tag")
    _sorted_unique(result["unsupported_obligation_ids"], lambda x: x, "unsupported result ids", 256, nonempty=True)
    for obligation_id in result["unsupported_obligation_ids"]:
        _text(obligation_id, "unsupported result obligation_id")
    return canonical_bytes(result)


def _serialize_compiled_result(candidate: dict[str, Any]) -> bytes:
    _validate_candidate(candidate)
    candidate_document = canonical_text(candidate)
    candidate_digest = digest_bytes(candidate_document.encode("utf-8"))
    result = {
        "schema": "aci.compiled-dispatch-candidate-result@1",
        "outcome": "compiled",
        "candidate_document": candidate_document,
        "candidate_digest": candidate_digest,
    }
    _exact(result, {"schema", "outcome", "candidate_document", "candidate_digest"}, "compiled result")
    if result["schema"] != "aci.compiled-dispatch-candidate-result@1" or result["outcome"] != "compiled":
        raise ValueError("compiled result tag")
    if not isinstance(result["candidate_document"], str):
        raise ValueError("compiled result candidate_document")
    _digest(result["candidate_digest"], "compiled result candidate_digest")
    parsed_candidate = parse_strict_json(result["candidate_document"].encode("utf-8"))
    _validate_candidate(parsed_candidate)
    if canonical_text(parsed_candidate) != result["candidate_document"]:
        raise ValueError("compiled result candidate_document is noncanonical")
    if digest_bytes(result["candidate_document"].encode("utf-8")) != result["candidate_digest"]:
        raise ValueError("compiled result candidate_digest mismatch")
    return canonical_bytes(result)


def _topological_order(node_ids: set[str], outgoing: dict[str, list[str]], incoming: dict[str, int]) -> list[str]:
    ready = [node_id for node_id in node_ids if incoming[node_id] == 0]
    heapq.heapify(ready)
    order: list[str] = []
    while ready:
        node_id = heapq.heappop(ready)
        order.append(node_id)
        for target_id in sorted(outgoing[node_id]):
            incoming[target_id] -= 1
            if incoming[target_id] == 0:
                heapq.heappush(ready, target_id)
    return order


_DOCS = (
    ("profile", _validate_profile), ("binding", _validate_binding),
    ("recipe", _validate_recipe), ("invocation", _validate_invocation),
)


class ProtocolCompiler:
    """Effect-free compiler. It receives every byte and identity explicitly."""

    def compile_candidate(self, request_bytes: bytes) -> bytes:
        try:
            request = parse_strict_json(request_bytes)
            _exact(request, _REQUEST_FIELDS, "request")
            if request["schema"] != "aci.compile-dispatch-candidate-request@1": raise ValueError("request schema")
            for name, _ in _DOCS:
                if not isinstance(request[f"{name}_document"], str): raise ValueError(f"{name}_document")
                _digest(request[f"{name}_digest"], f"{name}_digest")
            _digest(request["compiler_contract_digest"], "compiler_contract_digest")
            if canonical_bytes(request) != request_bytes: raise ValueError("outer request is noncanonical")
        except (ValidationError, ValueError, TypeError) as exc:
            _fail("invalid_request_schema", str(exc))

        documents: dict[str, dict[str, Any]] = {}
        document_bytes: dict[str, bytes] = {}
        for name, validator in _DOCS:
            raw = request[f"{name}_document"].encode("utf-8")
            document_bytes[name] = raw
            try:
                value = parse_strict_json(raw)
                validator(value)
                documents[name] = value
            except (ValidationError, ValueError, TypeError) as exc:
                _fail("invalid_document_schema", f"{name}: {exc}")
        for name, _ in _DOCS:
            if canonical_bytes(documents[name]) != document_bytes[name]:
                _fail("noncanonical_bytes", name)
        for name, _ in _DOCS:
            if digest_bytes(document_bytes[name]) != request[f"{name}_digest"]:
                _fail("digest_mismatch", name)
        if request["compiler_contract_digest"] != COMPILER_CONTRACT_DIGEST:
            _fail("compiler_identity_mismatch", "compiler contract identity is not V1")

        p, b, r, i = (documents[n] for n, _ in _DOCS)
        if b["status"] != "active": _fail("inactive_binding", b["status"])
        if (b["skill_id"] != p["skill_id"] or b["skill_revision_digest"] != p["skill_revision_digest"] or b["profile_digest"] != request["profile_digest"] or b["recipe_digest"] != request["recipe_digest"] or r["profile_digest"] != request["profile_digest"]):
            _fail("binding_mismatch", "binding/profile/recipe identities differ")
        if (i["skill_id"] != p["skill_id"] or i["skill_revision_digest"] != p["skill_revision_digest"] or i["profile_digest"] != request["profile_digest"] or i["binding_digest"] != request["binding_digest"] or i["recipe_digest"] != request["recipe_digest"]):
            _fail("invocation_mismatch", "invocation identities differ")

        parameters = {x["parameter_id"]: x for x in p["parameters"]}
        values = {x["parameter_id"]: x["value"] for x in i["values"]}
        if set(values) - set(parameters) or any(x["required"] and x["parameter_id"] not in values for x in p["parameters"]):
            _fail("invalid_parameter_value", "missing or undeclared parameter")
        try:
            for key, value in values.items():
                _validate_scalar(value, parameters[key]["value_schema"], key)
                if isinstance(value, str) and ("{{" in value or "}}" in value):
                    raise ValueError("invocation string contains a template delimiter")
            for node in r["nodes"]:
                placeholders = set(_PLACEHOLDER.findall(node["prompt_template"]))
                if not placeholders.issubset(set(node["parameter_ids"])):
                    raise ValueError("placeholder is not declared by node")
                if not placeholders.issubset(set(values)):
                    raise ValueError("placeholder has no explicit invocation value")
                remainder = _PLACEHOLDER.sub("", node["prompt_template"])
                if "{{" in remainder or "}}" in remainder: raise ValueError("malformed placeholder")
        except ValueError as exc:
            _fail("invalid_parameter_value", str(exc))

        obligation_ids = {x["obligation_id"] for x in p["obligations"]}
        node_ids = {x["node_id"] for x in r["nodes"]}; output_ids = {x["output_id"] for x in p["outputs"]}
        try:
            if {x["obligation_id"] for x in r["obligation_rules"]} != obligation_ids: raise ValueError("obligation coverage")
            for rule in r["obligation_rules"]:
                disp, refs, has_auth = rule["disposition"], rule["target_refs"], "authority_ref" in rule
                if disp in {"preserved", "compiled"} and (not refs or has_auth): raise ValueError("preserved/compiled shape")
                if disp == "unsupported" and (refs or has_auth): raise ValueError("unsupported shape")
                if disp == "superseded" and (refs or not has_auth): raise ValueError("superseded shape")
                for ref in refs:
                    if not isinstance(ref, str) or not ref:
                        raise ValueError("target ref")
                    kind, sep, ident = ref.partition(":")
                    _text(ident, "target ref identifier")
                    if not sep or (kind == "node" and ident not in node_ids) or (kind == "output" and ident not in output_ids) or kind not in {"node", "output"}: raise ValueError("target ref")
        except ValueError as exc:
            _fail("invalid_obligation_mapping", str(exc))

        try:
            param_ids = set(parameters); cap_ids = {x["capability_id"] for x in p["capability_requirements"]}
            terminal = set(r["terminal_node_ids"]); outgoing = {n: [] for n in node_ids}; incoming = {n: 0 for n in node_ids}
            edge_ids = [edge["edge_id"] for edge in r["edges"]]
            if len(edge_ids) != len(set(edge_ids)): raise ValueError("duplicate edge id")
            for node in r["nodes"]:
                if not set(node["parameter_ids"]) <= param_ids or not set(node["capability_ids"]) <= cap_ids or not set(node["output_ids"]) <= output_ids: raise ValueError("node reference")
                if (node["node_kind"] == "terminal") != (node["node_id"] in terminal): raise ValueError("terminal kind")
            for edge in r["edges"]:
                a, z = edge["from_node_id"], edge["to_node_id"]
                if a not in node_ids or z not in node_ids or a == z: raise ValueError("edge endpoint")
                outgoing[a].append(z); incoming[z] += 1
            if any(outgoing[n] for n in terminal): raise ValueError("terminal outgoing edge")
            seen = _topological_order(node_ids, outgoing, incoming)
            if len(seen) != len(node_ids): raise ValueError("cycle")
            reachable=set(terminal)
            for n in reversed(seen):
                if any(z in reachable for z in outgoing[n]): reachable.add(n)
            if reachable != node_ids: raise ValueError("terminal unreachable")
        except ValueError as exc:
            _fail("invalid_graph", str(exc))

        key = tuple(request[f"{name}_digest"] for name in ("profile", "binding", "recipe", "invocation"))
        if key not in ADMITTED_TUPLES: _fail("fixture_not_admitted", "input tuple is not admitted")
        required = {x["obligation_id"] for x in p["obligations"] if x["required"]}
        unsupported = sorted(x["obligation_id"] for x in r["obligation_rules"] if x["disposition"] == "unsupported" and x["obligation_id"] in required)
        if unsupported:
            return _serialize_unsupported_result(unsupported)

        rendered_nodes=[]
        for node in r["nodes"]:
            rendered=dict(node); prompt=node["prompt_template"]
            for parameter_id in _PLACEHOLDER.findall(prompt):
                prompt=prompt.replace("{{parameter:"+parameter_id+"}}", canonical_text(values[parameter_id]))
            rendered["prompt_template"]=prompt; rendered_nodes.append(rendered)
        candidate={
            "schema":"aci.dispatch-candidate@1",
            "source_binding":{"skill_id":p["skill_id"],"skill_revision_digest":p["skill_revision_digest"],"profile_digest":request["profile_digest"],"binding_digest":request["binding_digest"],"recipe_digest":request["recipe_digest"],"invocation_digest":request["invocation_digest"],"compiler_contract_digest":request["compiler_contract_digest"]},
            "invocation_values":i["values"],"nodes":rendered_nodes,"edges":r["edges"],"terminal_node_ids":r["terminal_node_ids"],"obligation_dispositions":r["obligation_rules"],"capability_requirements":p["capability_requirements"],"outputs":p["outputs"],
        }
        return _serialize_compiled_result(candidate)


def compile_dispatch_candidate(request_bytes: bytes) -> bytes:
    return ProtocolCompiler().compile_candidate(request_bytes)
