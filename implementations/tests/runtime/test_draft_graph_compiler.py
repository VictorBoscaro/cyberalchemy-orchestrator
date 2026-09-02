from __future__ import annotations

import base64
import copy
import hashlib
import json
import os
import pickle
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from jsonschema import Draft202012Validator
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from implementations.server.runtime.draft_graph_compiler import (
    DraftGraphCompileError,
    DraftGraphCompiler,
    TrustedAllocatorContextGate,
    VerifiedCompilationContext,
    bundled_contract_schema_digests,
    canonicalize_execution_graph,
    validate_compilation_match,
    validate_execution_graph,
)


REPO = Path(__file__).resolve().parents[3]
IMPL = REPO / "docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/followups/IMPL-ACI-AGENT-IDENTITY-ROLE-001"
SPEC = IMPL
EG_SCHEMA = IMPL.parents[1] / "stages/06-invoke-design/execution-graph-v2.proposed.schema.json"


def load(relative: str) -> dict:
    return json.loads((SPEC / relative).read_text(encoding="utf-8"))


def encode(value: dict) -> bytes:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


class DraftGraphCompilerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.context = load("fixtures/compilation-context.json")
        self.draft = load("fixtures/review-correct-verify.draft.json")
        self.policy = load("fixtures/policy.json")
        self.catalog = load("fixtures/catalog.json")
        self.resources = load("fixtures/resources.json")
        self.expected = load("fixtures/review-correct-verify.expected.execution.json")
        self.evidence = json.loads((IMPL / "fixtures/allocator-evidence.json").read_text(encoding="utf-8"))
        self.nonlatest_evidence = json.loads((IMPL / "fixtures/allocator-evidence-nonlatest.json").read_text(encoding="utf-8"))
        self.bound_evidence = json.loads((IMPL / "fixtures/allocator-evidence-bound.json").read_text(encoding="utf-8"))
        self.trust = load("fixtures/allocator-trust.json")
        self.role_registry = load("fixtures/role-registry.json")
        self.role_registry_raw = (IMPL / "fixtures/role-registry.json").read_bytes()
        self.agent_pool = load("fixtures/normalized-agent-pool.json")
        self.verified = TrustedAllocatorContextGate.verify(encode(self.context), encode(self.evidence), encode(self.trust))

    def _authority_for(self, draft: dict) -> tuple[VerifiedCompilationContext, dict]:
        try:
            node_keys = [node["key"] for node in draft["nodes"]]
        except (KeyError, TypeError):
            return self.verified, self.agent_pool
        if any(not isinstance(key, str) for key in node_keys):
            return self.verified, self.agent_pool
        if node_keys == [row["node_key"] for row in self.context["agent_assignments"]]:
            return self.verified, self.agent_pool
        context = copy.deepcopy(self.context)
        pool = copy.deepcopy(self.agent_pool)
        existing = {row["node_key"]: row for row in context["agent_assignments"]}
        used: set[str] = set()
        assignments = []
        for index, node in enumerate(draft["nodes"]):
            key = node["key"]
            assignment = copy.deepcopy(existing.get(key))
            if assignment is None or assignment["display_name"] in used:
                name = f"Fixture Agent {index + 1}"
                pool["agents"].append({"display_name": name, "role_fit": [node["agent_request"]["role"]]})
                assignment = {"node_key": key, "display_name": name, "role_fit_override": False, "role_fit_override_reason": None}
            used.add(assignment["display_name"])
            assignments.append(assignment)
        context["agent_assignments"] = assignments
        pool_bytes = json.dumps(pool, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
        context["agent_pool_ref"] = {"name": pool["name"], "version": pool["version"], "digest": "sha256:" + hashlib.sha256(pool_bytes).hexdigest()}
        evidence = copy.deepcopy(self.evidence)
        context_bytes = json.dumps(context, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
        evidence["context_digest"] = "sha256:" + hashlib.sha256(context_bytes).hexdigest()
        payload = {key: evidence[key] for key in ("schema", "evidence_id", "key_id", "context_digest", "is_latest", "pair_is_unbound")}
        evidence["signature"] = base64.b64encode(Ed25519PrivateKey.from_private_bytes(bytes(range(32))).sign(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode())).decode()
        return TrustedAllocatorContextGate.verify(encode(context), encode(evidence), encode(self.trust)), pool

    def compile(self, *, draft=None, policy=None, catalog=None, resources=None):
        draft_value = self.draft if draft is None else draft
        verified, pool = self._authority_for(draft_value)
        return DraftGraphCompiler().compile(
            verified,
            encode(draft_value),
            encode(self.policy if policy is None else policy),
            encode(self.catalog if catalog is None else catalog),
            encode(self.resources if resources is None else resources),
            self.role_registry_raw,
            encode(pool),
        )

    def failure(self, code: str, path: str, **inputs) -> DraftGraphCompileError:
        with self.assertRaises(DraftGraphCompileError) as caught:
            self.compile(**inputs)
        self.assertEqual((caught.exception.code, caught.exception.path), (code, path))
        return caught.exception

    def test_positive_exact_schema_digest_and_external_report(self) -> None:
        result = self.compile()
        self.assertEqual(result.graph, self.expected)
        Draft202012Validator(json.loads(EG_SCHEMA.read_text(encoding="utf-8"))).validate(result.graph)
        self.assertEqual(result.canonical_bytes, canonicalize_execution_graph(self.expected))
        self.assertEqual(result.digest, "sha256:" + hashlib.sha256(result.canonical_bytes).hexdigest())
        self.assertEqual(result.report, ())
        self.assertNotIn("execution_graph_digest", result.graph)

    def test_result_authority_is_bytes_and_graph_views_are_defensive(self) -> None:
        result = self.compile()
        first = result.graph; second = result.graph
        self.assertIsNot(first, second)
        self.assertIsNot(first["nodes"][0]["agent"]["provider_ref"], first["nodes"][1]["agent"]["provider_ref"])
        first["nodes"][0]["agent"]["provider_ref"]["name"] = "attacker"
        first["nodes"].append(copy.deepcopy(first["nodes"][-1]))
        self.assertEqual(result.graph, self.expected)
        self.assertEqual(result.digest, "sha256:" + hashlib.sha256(result.canonical_bytes).hexdigest())
        self.assertEqual(canonicalize_execution_graph(result.graph), result.canonical_bytes)

    def test_bounded_jcs_order_preserves_unicode_and_uri_resources_fail_closed(self) -> None:
        value = {"דּ": 7, "😀": 6, "€": 5, "ö": 4, "\u0080": 3, "1": 2, "\r": 1}
        self.assertEqual(
            canonicalize_execution_graph(value),
            '{"\\r":1,"1":2,"\u0080":3,"ö":4,"€":5,"😀":6,"דּ":7}'.encode("utf-8"),
        )
        self.assertNotEqual(canonicalize_execution_graph({"é": 1}), canonicalize_execution_graph({"e\u0301": 1}))
        for uri in ("urn:sha256:44d90d18d91d79fbae7e1ca43c47a1657f6e0a644e9fe9ae63119f79c2f20186", "https://example.invalid/latest"):
            resources = copy.deepcopy(self.resources)
            source = next(row for row in resources["resources"] if row["resource_key"] == "result_x")
            source.clear(); source.update({"resource_key": "result_x", "kind": "input", "media_type": "text/plain", "immutable_uri": uri, "digest": "sha256:44d90d18d91d79fbae7e1ca43c47a1657f6e0a644e9fe9ae63119f79c2f20186"})
            self.failure("DG_RESOURCE_SCHEMA_INVALID", "resources.resources[0]", resources=resources)

    def test_closed_input_schemas_and_duplicate_keys(self) -> None:
        fixtures = {
            "compilation-context.schema.json": self.context,
            "allocator-evidence.schema.json": self.evidence,
            "policy.schema.json": self.policy,
            "catalog.schema.json": self.catalog,
            "resources.schema.json": self.resources,
        }
        for name, value in fixtures.items():
            schema = json.loads((IMPL / "schemas" / name).read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            Draft202012Validator(schema).validate(value)
            hostile = dict(value); hostile["unknown"] = True
            self.assertTrue(list(Draft202012Validator(schema).iter_errors(hostile)))
        duplicate = encode(self.draft).decode().replace('"schema":"aci.draft-graph@1"', '"schema":"aci.draft-graph@1","schema":"aci.draft-graph@1"', 1)
        with self.assertRaises(DraftGraphCompileError) as caught:
            DraftGraphCompiler().compile(self.verified, duplicate, encode(self.policy), encode(self.catalog), encode(self.resources), self.role_registry_raw, encode(self.agent_pool))
        self.assertEqual((caught.exception.code, caught.exception.path), ("DG_DUPLICATE_JSON_KEY", "draft"))
        vectors = (SPEC / "NEGATIVE-VECTORS.md").read_text(encoding="utf-8")
        for number in range(1, 25):
            self.assertIn(f"`DG-N{number:02d}-", vectors)

    def test_failure_emits_no_result_and_mutates_no_compiler_state(self) -> None:
        compiler = DraftGraphCompiler()
        hostile = copy.deepcopy(self.draft); hostile["nodes"][1]["capability_requests"].append({"capability_key": "shell_exec", "operations": ["run"]})
        with self.assertRaises(DraftGraphCompileError):
            compiler.compile(self.verified, encode(hostile), encode(self.policy), encode(self.catalog), encode(self.resources), self.role_registry_raw, encode(self.agent_pool))
        self.assertEqual(vars(compiler), {})

    def test_allocator_gate_stale_conflict_and_author_identity_injection(self) -> None:
        stale = copy.deepcopy(self.context); stale["allocation_status"] = "released"
        for raw, evidence, code, path in (
            (stale, self.evidence, "DG_IDENTITY_CONTEXT_STALE", "compilation_context"),
            (self.context, self.nonlatest_evidence, "DG_IDENTITY_CONTEXT_STALE", "allocator_evidence.is_latest"),
            (self.context, self.bound_evidence, "DG_AUTHORITY_CONFLICT", "allocator_evidence.pair_is_unbound"),
        ):
            with self.subTest(code=code), self.assertRaises(DraftGraphCompileError) as caught:
                TrustedAllocatorContextGate.verify(encode(raw), encode(evidence))
            self.assertEqual((caught.exception.code, caught.exception.path), (code, path))
        forged_evidence = copy.deepcopy(self.evidence); forged_evidence["signature"] = base64.b64encode(b"0" * 64).decode()
        with self.assertRaises(DraftGraphCompileError) as forged:
            TrustedAllocatorContextGate.verify(encode(self.context), encode(forged_evidence))
        self.assertEqual(forged.exception.code, "DG_ALLOCATOR_EVIDENCE_INVALID")
        with self.assertRaises(TypeError): VerifiedCompilationContext()
        raw_object = object.__new__(VerifiedCompilationContext)
        object.__setattr__(raw_object, "_context_bytes", encode(self.context)); object.__setattr__(raw_object, "_evidence_bytes", encode(self.evidence))
        with self.assertRaises(DraftGraphCompileError) as direct:
            DraftGraphCompiler().compile(raw_object, encode(self.draft), encode(self.policy), encode(self.catalog), encode(self.resources), self.role_registry_raw, encode(self.agent_pool))
        self.assertEqual(direct.exception.code, "DG_IDENTITY_CONTEXT_STALE")
        for operation in (copy.copy, copy.deepcopy, pickle.dumps):
            with self.subTest(operation=operation.__name__), self.assertRaises(TypeError): operation(self.verified)
        for field, value in (("graph_key", "model_choice"), ("draft_revision", 9)):
            hostile = copy.deepcopy(self.draft); hostile[field] = value
            self.failure("DG_DRAFT_SCHEMA_INVALID", "draft", draft=hostile)

    def test_n01_through_n11_exact_results(self) -> None:
        value = copy.deepcopy(self.draft); value["nodes"][1]["capability_requests"].append({"capability_key": "shell_exec", "operations": ["run"]})
        self.failure("DG_UNKNOWN_REFERENCE", "nodes[correct].capability_requests[shell_exec]", draft=value)
        value = copy.deepcopy(self.draft); value["nodes"][2]["agent_request"]["model_key"] = "unlisted_model"
        self.failure("DG_UNKNOWN_REFERENCE", "nodes[verify].agent_request.model_key", draft=value)
        value = copy.deepcopy(self.draft); value["nodes"][1]["access_request"]["write_paths"].append("workspace:/secrets")
        self.failure("DG_PERMISSION_DENIED", "nodes[correct].access_request.write_paths[1]", draft=value)
        value = copy.deepcopy(self.draft); value["nodes"][2]["inputs"][1]["source"]["node_key"] = "missing_reviewer"
        self.failure("DG_INPUT_WITHOUT_PRODUCER", "nodes[verify].inputs[review_findings]", draft=value)
        resources = copy.deepcopy(self.resources); resource = next(row for row in resources["resources"] if row["resource_key"] == "correction_schema")
        resource["content"] = '{"type":"object","required":["patch"],"properties":{},"additionalProperties":false}'
        resource["digest"] = "sha256:" + hashlib.sha256(resource["content"].encode()).hexdigest()
        self.failure("DG_OUTPUT_CONTRACT_INVALID", "resources[correction_schema]", resources=resources)
        value = copy.deepcopy(self.draft); value["nodes"][2]["success_condition"] = {"kind": "free_text", "expression": "looks good"}
        self.failure("DG_DRAFT_SCHEMA_INVALID", "draft.nodes[2].success_condition", draft=value)
        expanded = copy.deepcopy(self.expected); expanded["nodes"][2]["isolation"]["network"] = {"mode": "allowlist", "allow": ["internet"]}
        with self.assertRaises(DraftGraphCompileError) as caught: validate_compilation_match(self.expected, expanded)
        self.assertEqual((caught.exception.code, caught.exception.path), ("DG_AUTHORITY_EXPANSION", "execution_graph"))
        value = copy.deepcopy(self.draft); value["nodes"][0]["validation"][0]["validator_key"] = "best_effort_review"
        self.failure("DG_UNKNOWN_REFERENCE", "nodes[review].validation[review_has_evidence].validator_key", draft=value)
        value = copy.deepcopy(self.draft); value["nodes"][0]["requested_limits"]["max_tokens"] = 13000
        self.failure("DG_GLOBAL_BUDGET_EXCEEDED", "global_limits.max_tokens", draft=value)
        resources = copy.deepcopy(self.resources); next(row for row in resources["resources"] if row["resource_key"] == "result_x")["content"] += "!"
        self.failure("DG_RESOURCE_DIGEST_MISMATCH", "resources[result_x]", resources=resources)
        value = copy.deepcopy(self.draft); value["nodes"][1]["requested_limits"]["max_tokens"] = 13000
        result = self.compile(draft=value)
        self.assertEqual(result.graph, self.expected)
        self.assertEqual(result.report, ({"kind": "numeric_limit_restriction", "path": "nodes[correct].limits.max_tokens", "requested": 13000, "effective": 12000, "policy_ceiling": 12000},))

    def test_n12_through_n20_exact_results(self) -> None:
        for predicate in ({"kind": "attempts_exhausted"}, {"kind": "input_unavailable", "input_key": "target"}):
            value = copy.deepcopy(self.draft); value["nodes"][0]["success_condition"] = predicate
            self.failure("DG_DRAFT_SCHEMA_INVALID", "draft.nodes[0].success_condition", draft=value)
        value = copy.deepcopy(self.draft); value["nodes"][1]["access_request"]["commands"] = {"mode": "allowlist", "grants": [{"command_key": "shell", "argv": ["-c", "work"], "cwd": "workspace:/target", "environment_resource_alias": None}]}
        self.failure("DG_DRAFT_SCHEMA_INVALID", "draft.nodes[1].access_request.commands.grants", draft=value)
        additions = []
        unique_node = copy.deepcopy(self.expected["nodes"][-1]); unique_node["node_id"] = "node:extra"
        additions.append(lambda graph: graph["nodes"].append(copy.deepcopy(unique_node)))
        additions.append(lambda graph: graph["nodes"].append(copy.deepcopy(graph["nodes"][-1])))
        additions.append(lambda graph: graph["nodes"][0]["tools"].append(copy.deepcopy(graph["nodes"][1]["tools"][0])))
        for field in ("inputs", "outputs", "validation", "stop_conditions"):
            additions.append(lambda graph, field=field: graph["nodes"][0][field].append(copy.deepcopy(graph["nodes"][0][field][0])))
        additions.append(lambda graph: graph["nodes"][0]["isolation"]["commands"]["grants"].append({"argv": ["x"]}))
        for position, mutation in enumerate(additions):
            candidate = copy.deepcopy(self.expected); mutation(candidate)
            with self.subTest(vector="N17", position=position), self.assertRaises(DraftGraphCompileError) as caught: validate_compilation_match(self.expected, candidate)
            self.assertEqual((caught.exception.code, caught.exception.path), ("DG_AUTHORITY_EXPANSION", "execution_graph"))
        removals = [lambda graph: graph["nodes"].pop()]
        for field, node_index in (("tools", 1), ("inputs", 0), ("outputs", 0), ("validation", 0), ("stop_conditions", 0)):
            removals.append(lambda graph, field=field, node_index=node_index: graph["nodes"][node_index][field].pop())
        for position, mutation in enumerate(removals):
            candidate = copy.deepcopy(self.expected); mutation(candidate)
            with self.subTest(vector="N18", position=position), self.assertRaises(DraftGraphCompileError) as caught: validate_compilation_match(self.expected, candidate)
            self.assertEqual((caught.exception.code, caught.exception.path), ("DG_COMPILATION_MISMATCH", "execution_graph"))
        for pointer, scalar, code, path in (("/does_not_exist", "pass", "DG_PREDICATE_POINTER_INVALID", "nodes[verify].success_condition.json_pointer"), ("/verdict", "bogus", "DG_PREDICATE_VALUE_INVALID", "nodes[verify].success_condition.value")):
            value = copy.deepcopy(self.draft); value["nodes"][2]["success_condition"]["json_pointer"] = pointer; value["nodes"][2]["success_condition"]["value"] = scalar
            self.failure(code, path, draft=value)

    def test_n21_through_n24_reject_unproved_ancestor_types_on_both_paths(self) -> None:
        attacks = (
            ("nested", {"properties": {"leaf": {"type": "string"}}, "required": ["leaf"]}, "/nested/leaf"),
            ("nested", {"type": ["object", "null"], "properties": {"leaf": {"type": "string"}}, "required": ["leaf"]}, "/nested/leaf"),
            ("arr", {"items": {"type": "string"}, "minItems": 1}, "/arr/0"),
            ("arr", {"type": ["array", "null"], "items": {"type": "string"}, "minItems": 1}, "/arr/0"),
        )
        for field, ancestor, pointer in attacks:
            resources = copy.deepcopy(self.resources)
            resource = next(row for row in resources["resources"] if row["resource_key"] == "verification_schema")
            schema = {"type": "object", "required": ["verdict", field], "properties": {"verdict": {"enum": ["pass", "flag", "block"]}, field: ancestor}, "additionalProperties": False}
            resource["content"] = json.dumps(schema, separators=(",", ":")); resource["digest"] = "sha256:" + hashlib.sha256(resource["content"].encode()).hexdigest()
            draft = copy.deepcopy(self.draft); draft["nodes"][2]["success_condition"] = {"kind": "output_field_equals", "output_key": "verification", "json_pointer": pointer, "value": "ok"}
            self.failure("DG_PREDICATE_POINTER_UNPROVABLE", "nodes[verify].success_condition.json_pointer", draft=draft, resources=resources)
            candidate = copy.deepcopy(self.expected); member = next(row for row in candidate["content_members"] if row["member_id"] == "member:verification_schema")
            member["content"] = resource["content"]; member["digest"] = resource["digest"]; candidate["nodes"][2]["success_condition"] = {"kind": "output_field_equals", "output_id": "output:verification", "json_pointer": pointer, "value": "ok"}
            with self.assertRaises(DraftGraphCompileError) as caught: validate_execution_graph(candidate)
            self.assertEqual(caught.exception.code, "DG_PREDICATE_POINTER_UNPROVABLE")

    def test_f3_strict_and_satisfiable_output_contracts_on_both_paths(self) -> None:
        contents = (
            '{"type":"object","required":["patch"],"properties":{"patch":{"const":NaN}},"additionalProperties":false}',
            '{"type":"object","required":["patch"],"properties":{"patch":false},"additionalProperties":false}',
        )
        for content in contents:
            resources = copy.deepcopy(self.resources)
            resource = next(row for row in resources["resources"] if row["resource_key"] == "correction_schema")
            resource["content"] = content; resource["digest"] = "sha256:" + hashlib.sha256(content.encode()).hexdigest()
            expected_path = "resources[correction_schema]" if "NaN" in content else "resources[correction_schema].properties.patch"
            self.failure("DG_OUTPUT_CONTRACT_INVALID", expected_path, resources=resources)
            candidate = copy.deepcopy(self.expected)
            member = next(row for row in candidate["content_members"] if row["member_id"] == "member:correction_schema")
            member["content"] = content; member["digest"] = resource["digest"]
            with self.assertRaises(DraftGraphCompileError) as caught: validate_execution_graph(candidate)
            expected_path = "member:correction_schema" if "NaN" in content else "member:correction_schema.properties.patch"
            self.assertEqual((caught.exception.code, caught.exception.path), ("DG_OUTPUT_CONTRACT_INVALID", expected_path))

    def test_f4_selector_language_is_literal_root_only(self) -> None:
        for selector in ("runtime://guess/free-form?x=../secret", "$.field", "", "/field"):
            draft = copy.deepcopy(self.draft); draft["nodes"][0]["inputs"][0]["source"]["selector"] = selector
            code = "DG_DRAFT_SCHEMA_INVALID" if selector == "" else "DG_SELECTOR_UNSUPPORTED"
            path = "draft.nodes[0].inputs[0].source" if selector == "" else "nodes[review].inputs[target].source.selector"
            self.failure(code, path, draft=draft)

    def test_f6_condition_aware_joins_and_feedback(self) -> None:
        failure_only = copy.deepcopy(self.draft)
        failure_only["nodes"][1]["inputs"][1]["source"] = {"kind": "resource", "resource_alias": "result_x", "selector": "$"}
        failure_only["edges"].append({"key": "review_failed", "from_node_key": "review", "to_node_key": "correct", "kind": "control", "condition": "on_failure"})
        self.failure("DG_TOPOLOGY_INVALID", "nodes[verify].start_when", draft=failure_only)
        feedback = copy.deepcopy(self.draft)
        feedback["nodes"][0]["inputs"].append({"key": "verification_feedback", "required": False, "source": {"kind": "node_output", "node_key": "verify", "output_key": "verification"}})
        feedback["edges"].append({"key": "verification_feedback", "from_node_key": "verify", "to_node_key": "review", "kind": "feedback", "condition": "always"})
        result = self.compile(draft=feedback)
        self.assertEqual(result.graph["lifecycle"]["entry_nodes"], ["node:review"])
        self.assertIn("edge:verify:review:data", {edge["edge_id"] for edge in result.graph["edges"]})
        required_feedback = copy.deepcopy(feedback)
        required_feedback["nodes"][0]["inputs"][-1]["required"] = True
        self.failure("DG_TOPOLOGY_INVALID", "nodes[review].inputs[verification_feedback].required", draft=required_feedback)
        unsafe_feedback_target = copy.deepcopy(self.draft)
        unsafe_feedback_target["edges"].append({"key": "correct_verify_feedback", "from_node_key": "correct", "to_node_key": "verify", "kind": "feedback", "condition": "on_success"})
        self.failure("DG_TOPOLOGY_INVALID", "nodes[verify].start_when", draft=unsafe_feedback_target)
        self.assertEqual(self.compile().graph["nodes"][2]["start_when"], "all_predecessors_succeeded")

    def test_r1_any_join_requires_all_required_inputs_ready(self) -> None:
        single_required = copy.deepcopy(self.draft)
        single_required["nodes"][1]["start_when"] = "any_predecessor_succeeded"
        self.assertEqual(self.compile(draft=single_required).graph["nodes"][1]["start_when"], "any_predecessor_succeeded")

        multiple_required = copy.deepcopy(self.draft)
        multiple_required["nodes"][2]["start_when"] = "any_predecessor_succeeded"
        self.failure("DG_TOPOLOGY_INVALID", "nodes[verify].start_when", draft=multiple_required)

        optional_multiple = copy.deepcopy(self.draft)
        optional_multiple["nodes"][2]["start_when"] = "any_predecessor_succeeded"
        optional_multiple["nodes"][2]["inputs"][1]["required"] = False
        optional_multiple["nodes"][2]["inputs"][2]["required"] = False
        self.assertEqual(self.compile(draft=optional_multiple).graph["nodes"][2]["start_when"], "any_predecessor_succeeded")

        ancestor_guaranteed = copy.deepcopy(self.draft)
        ancestor_guaranteed["nodes"][2]["start_when"] = "any_predecessor_succeeded"
        ancestor_guaranteed["nodes"][2]["inputs"][2]["required"] = False
        self.assertEqual(self.compile(draft=ancestor_guaranteed).graph["nodes"][2]["start_when"], "any_predecessor_succeeded")

        early_optional_trigger = copy.deepcopy(self.draft)
        early_optional_trigger["nodes"][2]["start_when"] = "any_predecessor_succeeded"
        early_optional_trigger["nodes"][2]["inputs"][1]["required"] = False
        self.failure("DG_TOPOLOGY_INVALID", "nodes[verify].start_when", draft=early_optional_trigger)

        optional_output = copy.deepcopy(self.draft)
        optional_output["nodes"][0]["outputs"].append({"key": "optional_findings", "contract_resource_alias": "review_report_schema", "required": False})
        optional_output["nodes"][1]["inputs"][1]["source"]["output_key"] = "optional_findings"
        self.failure("DG_TOPOLOGY_INVALID", "nodes[correct].inputs[review_findings].required", draft=optional_output)

    def test_r1_conditional_must_availability_matrix(self) -> None:
        def routed(condition: str):
            graph = copy.deepcopy(self.draft)
            graph["nodes"][1]["inputs"][1]["source"] = {"kind": "resource", "resource_alias": "result_x", "selector": "$"}
            graph["edges"].append({"key": "review_route", "from_node_key": "review", "to_node_key": "correct", "kind": "control", "condition": condition})
            graph["nodes"][2]["start_when"] = "any_predecessor_succeeded"
            graph["nodes"][2]["inputs"][2]["required"] = False
            return graph

        always_after_failure = routed("always")
        self.failure("DG_TOPOLOGY_INVALID", "nodes[verify].start_when", draft=always_after_failure)

        success_only = routed("on_success")
        self.assertEqual(self.compile(draft=success_only).graph["nodes"][2]["start_when"], "any_predecessor_succeeded")

        mixed_narrowing = routed("on_success")
        mixed_narrowing["edges"].append({"key": "review_always", "from_node_key": "review", "to_node_key": "correct", "kind": "control", "condition": "always"})
        self.assertEqual(self.compile(draft=mixed_narrowing).graph["nodes"][2]["start_when"], "any_predecessor_succeeded")

        repair = copy.deepcopy(self.draft)
        repair["nodes"][1]["inputs"][1]["source"] = {"kind": "resource", "resource_alias": "result_x", "selector": "$"}
        repair["edges"].append({"key": "review_failed", "from_node_key": "review", "to_node_key": "correct", "kind": "control", "condition": "on_failure"})
        del repair["nodes"][2]["inputs"][1]
        repair["nodes"][2]["start_when"] = "any_predecessor_succeeded"
        repair["lifecycle"]["terminal_node_keys"] = ["review", "verify"]
        repair["lifecycle"]["completion"] = "any_terminal_succeeded"
        repair_result = self.compile(draft=repair)
        self.assertIn("on_failure", {edge["condition"] for edge in repair_result.graph["edges"]})

        diamond = copy.deepcopy(self.draft)
        alternative = copy.deepcopy(diamond["nodes"][1])
        alternative["key"] = "correct_alt"
        for node in (diamond["nodes"][1], alternative):
            node["requested_limits"] = {"max_attempts": 1, "max_tokens": 6000, "wall_clock_seconds": 300}
        diamond["nodes"].insert(2, alternative)
        diamond["nodes"][3]["inputs"].append({"key": "candidate_alternative", "required": True, "source": {"kind": "node_output", "node_key": "correct_alt", "output_key": "correction"}})
        self.assertEqual(self.compile(draft=diamond).graph["nodes"][3]["start_when"], "all_predecessors_succeeded")
        diamond["nodes"][3]["start_when"] = "any_predecessor_succeeded"
        self.failure("DG_TOPOLOGY_INVALID", "nodes[verify].start_when", draft=diamond)

    def test_f7_schema_gate_typed_paths_and_hash_seed_independence(self) -> None:
        policy = copy.deepcopy(self.policy); policy["access_ceiling"]["network"]["allow"] = [[]]
        self.failure("DG_POLICY_SCHEMA_INVALID", "policy.access_ceiling.network.allow[0]", policy=policy)
        malformed = (
            ("draft", {**self.draft, "unknown": True}, "DG_DRAFT_SCHEMA_INVALID"),
            ("policy", {**self.policy, "unknown": True}, "DG_POLICY_SCHEMA_INVALID"),
            ("catalog", {**self.catalog, "unknown": True}, "DG_CATALOG_SCHEMA_INVALID"),
            ("resources", {**self.resources, "unknown": True}, "DG_RESOURCE_SCHEMA_INVALID"),
        )
        for name, value, code in malformed:
            with self.subTest(name=name), self.assertRaises(DraftGraphCompileError) as caught:
                self.compile(**{name: value})
            self.assertEqual(caught.exception.code, code)
        script = f"""import json\nfrom pathlib import Path\nfrom implementations.server.runtime.draft_graph_compiler import *\nb=Path({str(SPEC)!r}); r=lambda p:(b/p).read_bytes()\nc=json.loads(r('fixtures/catalog.json')); c['providers'][0]['key']=[]; c['models'][0]['provider_key']=[]\nv=TrustedAllocatorContextGate.verify(r('fixtures/compilation-context.json'),r('fixtures/allocator-evidence.json'),r('fixtures/allocator-trust.json'))\ntry: DraftGraphCompiler().compile(v,r('fixtures/review-correct-verify.draft.json'),r('fixtures/policy.json'),json.dumps(c,separators=(',',':')).encode(),r('fixtures/resources.json'),r('fixtures/role-registry.json'),r('fixtures/normalized-agent-pool.json'))\nexcept DraftGraphCompileError as x: print(x.code+'|'+x.path)"""
        outputs = []
        for seed in range(1, 9):
            completed = subprocess.run([sys.executable, "-c", script], cwd=REPO, env={**os.environ, "PYTHONHASHSEED": str(seed)}, check=True, capture_output=True, text=True)
            outputs.append(completed.stdout.strip())
        self.assertEqual(len(set(outputs)), 1, outputs)
        self.assertTrue(outputs[0].startswith("DG_CATALOG_SCHEMA_INVALID|catalog."), outputs[0])

    def test_f7_all_boundary_shapes_fail_typed_without_partial_result(self) -> None:
        attacks = []
        value = copy.deepcopy(self.draft); del value["objective"]; attacks.append(("draft", value, "DG_DRAFT_SCHEMA_INVALID"))
        value = copy.deepcopy(self.draft); value["nodes"][0]["key"] = []; attacks.append(("draft", value, "DG_DRAFT_SCHEMA_INVALID"))
        value = copy.deepcopy(self.policy); del value["access_ceiling"]; attacks.append(("policy", value, "DG_POLICY_SCHEMA_INVALID"))
        value = copy.deepcopy(self.catalog); value["providers"][0]["ref"]["digest"] = 7; attacks.append(("catalog", value, "DG_CATALOG_SCHEMA_INVALID"))
        value = copy.deepcopy(self.resources); value["resources"][0]["content"] = {}; attacks.append(("resources", value, "DG_RESOURCE_SCHEMA_INVALID"))
        value = copy.deepcopy(self.catalog); value["providers"].append(copy.deepcopy(value["providers"][0])); attacks.append(("catalog", value, "DG_AMBIGUOUS_REFERENCE"))
        value = copy.deepcopy(self.resources); value["resources"].append(copy.deepcopy(value["resources"][0])); attacks.append(("resources", value, "DG_AMBIGUOUS_REFERENCE"))
        for name, value, code in attacks:
            with self.subTest(name=name, code=code), self.assertRaises(DraftGraphCompileError) as caught:
                self.compile(**{name: value})
            self.assertEqual(caught.exception.code, code)
        bad_context = copy.deepcopy(self.context); del bad_context["revision"]
        with self.assertRaises(DraftGraphCompileError) as caught: TrustedAllocatorContextGate.verify(encode(bad_context), encode(self.evidence))
        self.assertEqual(caught.exception.code, "DG_COMPILATION_CONTEXT_INVALID")
        bad_evidence = copy.deepcopy(self.evidence); bad_evidence["unknown"] = True
        with self.assertRaises(DraftGraphCompileError) as caught: TrustedAllocatorContextGate.verify(encode(self.context), encode(bad_evidence))
        self.assertEqual(caught.exception.code, "DG_ALLOCATOR_EVIDENCE_INVALID")

    def test_r2_lone_surrogates_fail_typed_at_every_boundary(self) -> None:
        def ascii_json(value) -> bytes:
            return json.dumps(value, ensure_ascii=True, separators=(",", ":")).encode("ascii")

        context = copy.deepcopy(self.context); context["dispatch_id"] = "\ud800"
        with self.assertRaises(DraftGraphCompileError) as caught:
            TrustedAllocatorContextGate.verify(ascii_json(context), encode(self.evidence))
        self.assertEqual((caught.exception.code, caught.exception.path), ("DG_COMPILATION_CONTEXT_INVALID", "compilation_context.dispatch_id"))
        context = copy.deepcopy(self.context); context["\ud800"] = True
        with self.assertRaises(DraftGraphCompileError) as caught:
            TrustedAllocatorContextGate.verify(ascii_json(context), encode(self.evidence))
        self.assertEqual((caught.exception.code, caught.exception.path), ("DG_COMPILATION_CONTEXT_INVALID", "compilation_context.<member-name>"))

        evidence = copy.deepcopy(self.evidence); evidence["key_id"] = "\ud800"
        with self.assertRaises(DraftGraphCompileError) as caught:
            TrustedAllocatorContextGate.verify(encode(self.context), ascii_json(evidence))
        self.assertEqual((caught.exception.code, caught.exception.path), ("DG_ALLOCATOR_EVIDENCE_INVALID", "allocator_evidence.key_id"))

        attacks = []
        draft = copy.deepcopy(self.draft); draft["objective"]["statement"] = "\ud800"; attacks.append(("draft", draft, "DG_DRAFT_SCHEMA_INVALID", "draft.objective.statement"))
        policy = copy.deepcopy(self.policy); policy["semantics_key"] = "\ud800"; attacks.append(("policy", policy, "DG_POLICY_SCHEMA_INVALID", "policy.semantics_key"))
        catalog = copy.deepcopy(self.catalog); catalog["providers"][0]["digest_source"] = "\ud800"; attacks.append(("catalog", catalog, "DG_CATALOG_SCHEMA_INVALID", "catalog.providers[0].digest_source"))
        resources = copy.deepcopy(self.resources); resources["resources"][0]["content"] = "\ud800"; attacks.append(("resources", resources, "DG_RESOURCE_SCHEMA_INVALID", "resources.resources[0].content"))
        good = {"draft": encode(self.draft), "policy": encode(self.policy), "catalog": encode(self.catalog), "resources": encode(self.resources)}
        for name, value, code, path in attacks:
            raw = dict(good); raw[name] = ascii_json(value)
            with self.subTest(name=name), self.assertRaises(DraftGraphCompileError) as caught:
                DraftGraphCompiler().compile(self.verified, raw["draft"], raw["policy"], raw["catalog"], raw["resources"], self.role_registry_raw, encode(self.agent_pool))
            self.assertEqual((caught.exception.code, caught.exception.path), (code, path))

        resources = copy.deepcopy(self.resources)
        schema_resource = next(row for row in resources["resources"] if row["resource_key"] == "correction_schema")
        schema_resource["content"] = r'{"type":"object","required":["patch"],"properties":{"patch":{"const":"\ud800"}},"additionalProperties":false}'
        schema_resource["digest"] = "sha256:" + hashlib.sha256(schema_resource["content"].encode("utf-8")).hexdigest()
        self.failure("DG_OUTPUT_CONTRACT_INVALID", "resources[correction_schema].properties.patch.const", resources=resources)

        with self.assertRaises(DraftGraphCompileError) as caught:
            canonicalize_execution_graph({"\ud800": 1})
        self.assertEqual((caught.exception.code, caught.exception.path), ("DG_CANONICALIZATION_ERROR", "execution_graph.<member-name>"))

    def test_r2_unicode_failures_are_hash_seed_stable_in_clean_processes(self) -> None:
        payloads = {
            "context": base64.b64encode(encode(self.context)).decode(),
            "evidence": base64.b64encode(encode(self.evidence)).decode(),
            "draft": base64.b64encode(encode(self.draft)).decode(),
            "policy": base64.b64encode(encode(self.policy)).decode(),
            "catalog": base64.b64encode(encode(self.catalog)).decode(),
            "resources": base64.b64encode(encode(self.resources)).decode(),
            "trust": base64.b64encode(encode(self.trust)).decode(),
            "registry": base64.b64encode(self.role_registry_raw).decode(),
            "pool": base64.b64encode(encode(self.agent_pool)).decode(),
        }
        script = f'''import base64, copy, json
from implementations.server.runtime.draft_graph_compiler import DraftGraphCompileError, DraftGraphCompiler, TrustedAllocatorContextGate
p={{k:base64.b64decode(v) for k,v in {payloads!r}.items()}}
j={{k:json.loads(v) for k,v in p.items()}}
raw=lambda v:json.dumps(v,ensure_ascii=True,separators=(",",":")).encode("ascii")
results=[]
c=copy.deepcopy(j["context"]); c["dispatch_id"]="\\ud800"
try: TrustedAllocatorContextGate.verify(raw(c),p["evidence"],p["trust"])
except DraftGraphCompileError as e: results.append(e.code+"|"+e.path)
e=copy.deepcopy(j["evidence"]); e["key_id"]="\\ud800"
try: TrustedAllocatorContextGate.verify(p["context"],raw(e),p["trust"])
except DraftGraphCompileError as x: results.append(x.code+"|"+x.path)
v=TrustedAllocatorContextGate.verify(p["context"],p["evidence"],p["trust"])
for name,path in (("draft",("objective","statement")),("policy",("semantics_key",)),("catalog",("providers",0,"digest_source")),("resources",("resources",0,"content"))):
    values={{k:p[k] for k in ("draft","policy","catalog","resources")}}; hostile=copy.deepcopy(j[name]); cursor=hostile
    for part in path[:-1]: cursor=cursor[part]
    cursor[path[-1]]="\\ud800"; values[name]=raw(hostile)
    try: DraftGraphCompiler().compile(v,values["draft"],values["policy"],values["catalog"],values["resources"],p["registry"],p["pool"])
    except DraftGraphCompileError as x: results.append(x.code+"|"+x.path)
print(";".join(results))'''
        outputs = [subprocess.run([sys.executable, "-c", script], cwd=REPO, env={**os.environ, "PYTHONHASHSEED": str(seed)}, check=True, capture_output=True, text=True).stdout.strip() for seed in range(1, 5)]
        self.assertEqual(len(set(outputs)), 1, outputs)
        self.assertEqual(len(outputs[0].split(";")), 6)

    def test_f8_non_toy_single_node_and_base64_inline_forms(self) -> None:
        node = copy.deepcopy(self.draft["nodes"][0]); node["key"] = "analyze"; node["objective"] = "Analyze one pinned input."; node["instructions"] = "Return a closed findings report."
        graph = {"schema": "aci.draft-graph@1", "objective": {"statement": "Analyze a pinned document.", "done_when": ["A findings report exists."]}, "resources": copy.deepcopy(self.draft["resources"]), "requested_global_limits": {"max_attempts": 1, "max_tokens": 6000, "wall_clock_seconds": 300}, "nodes": [node], "edges": [], "lifecycle": {"entry_node_keys": ["analyze"], "terminal_node_keys": ["analyze"], "completion": "all_terminal_succeeded", "failure": "fail_fast", "cancellation": "cancel_running_nodes", "max_parallel_nodes": 1}}
        result = self.compile(draft=graph)
        self.assertEqual([item["node_id"] for item in result.graph["nodes"]], ["node:analyze"])
        resources = copy.deepcopy(self.resources); resource = next(row for row in resources["resources"] if row["resource_key"] == "result_x")
        raw = resource["content"].encode(); resource["encoding"] = "base64"; resource["content"] = base64.b64encode(raw).decode()
        base64_result = self.compile(resources=resources)
        member = next(row for row in base64_result.graph["content_members"] if row["member_id"] == "member:result_x")
        self.assertEqual((member["encoding"], member["content"]), ("base64", resource["content"]))

    def test_determinism_across_key_order_and_clean_processes(self) -> None:
        def reverse_objects(value):
            if isinstance(value, dict): return {key: reverse_objects(value[key]) for key in reversed(value)}
            if isinstance(value, list): return [reverse_objects(item) for item in value]
            return value
        shuffled = DraftGraphCompiler().compile(self.verified, encode(reverse_objects(self.draft)), encode(reverse_objects(self.policy)), encode(reverse_objects(self.catalog)), encode(reverse_objects(self.resources)), self.role_registry_raw, encode(reverse_objects(self.agent_pool)))
        baseline = self.compile()
        self.assertEqual((shuffled.graph, shuffled.canonical_bytes, shuffled.digest), (baseline.graph, baseline.canonical_bytes, baseline.digest))
        script = f"""from pathlib import Path\nimport base64\nfrom implementations.server.runtime.draft_graph_compiler import *\nb=Path({str(SPEC)!r})\nr=lambda p:(b/p).read_bytes()\nv=TrustedAllocatorContextGate.verify(r('fixtures/compilation-context.json'),r('fixtures/allocator-evidence.json'),r('fixtures/allocator-trust.json'))\no=DraftGraphCompiler().compile(v,r('fixtures/review-correct-verify.draft.json'),r('fixtures/policy.json'),r('fixtures/catalog.json'),r('fixtures/resources.json'),r('fixtures/role-registry.json'),r('fixtures/normalized-agent-pool.json'))\nprint(base64.b64encode(o.canonical_bytes).decode())"""
        outputs = [subprocess.run([sys.executable, "-c", script], cwd=REPO, env={**os.environ, "PYTHONHASHSEED": str(seed)}, check=True, capture_output=True, text=True).stdout.strip() for seed in range(1, 7)]
        self.assertEqual(len(set(outputs)), 1); self.assertEqual(base64.b64decode(outputs[0]), baseline.canonical_bytes)

    def test_pure_compiler_has_no_effects_or_runtime_actions(self) -> None:
        sentinel = Mock(side_effect=AssertionError("forbidden effect"))
        with patch("builtins.open", sentinel), patch("time.time", sentinel), patch("random.random", sentinel), patch("socket.socket", sentinel), patch("os.getenv", sentinel):
            self.compile()
        sentinel.assert_not_called()
        self.assertFalse(any(hasattr(DraftGraphCompiler, name) for name in ("confirm", "store", "schedule", "run", "launch", "execute")))

    def test_r3_embedded_contracts_match_artifacts_and_clean_import_needs_no_filesystem(self) -> None:
        schema_files = {
            "compilation_context": IMPL / "schemas/compilation-context.schema.json",
            "allocator_evidence": IMPL / "schemas/allocator-evidence.schema.json",
            "draft": IMPL / "schemas/draft-graph-v1.proposed.schema.json",
            "policy": IMPL / "schemas/policy.schema.json",
            "catalog": IMPL / "schemas/catalog.schema.json",
            "resources": IMPL / "schemas/resources.schema.json",
            "execution_graph": EG_SCHEMA,
        }
        self.assertEqual(
            bundled_contract_schema_digests(),
            {name: "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest() for name, path in schema_files.items()},
        )
        payloads = [
            base64.b64encode(encode(self.context)).decode(),
            base64.b64encode(encode(self.evidence)).decode(),
            base64.b64encode(encode(self.draft)).decode(),
            base64.b64encode(encode(self.policy)).decode(),
            base64.b64encode(encode(self.catalog)).decode(),
            base64.b64encode(encode(self.resources)).decode(),
            base64.b64encode(encode(self.trust)).decode(),
            base64.b64encode(self.role_registry_raw).decode(),
            base64.b64encode(encode(self.agent_pool)).decode(),
        ]
        script = f'''import base64, builtins, pathlib
import cryptography, jsonschema
p=[base64.b64decode(v) for v in {payloads!r}]
def blocked(*args,**kwargs): raise AssertionError("filesystem access")
builtins.open=blocked
pathlib.Path.open=blocked
pathlib.Path.read_text=blocked
pathlib.Path.read_bytes=blocked
from implementations.server.runtime.draft_graph_compiler import DraftGraphCompiler, TrustedAllocatorContextGate
v=TrustedAllocatorContextGate.verify(p[0],p[1],p[6])
print(DraftGraphCompiler().compile(v,p[2],p[3],p[4],p[5],p[7],p[8]).digest)'''
        completed = subprocess.run([sys.executable, "-c", script], cwd=REPO, check=True, capture_output=True, text=True)
        self.assertEqual(completed.stdout.strip(), self.compile().digest)


if __name__ == "__main__":
    unittest.main()
