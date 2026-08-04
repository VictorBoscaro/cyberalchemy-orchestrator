from __future__ import annotations

import copy
import ast
import base64
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock
from unittest.mock import patch

from implementations.server.runtime.canonical import canonical_bytes, canonical_text, digest_bytes
from implementations.server.runtime.protocol_compilation import (
    COMPILER_CONTRACT_DIGEST,
    ProtocolCompileFailure,
    ProtocolCompiler,
    _serialize_compiled_result,
    _serialize_unsupported_result,
    _topological_order,
)
from implementations.server.runtime.errors import ConflictError
from implementations.server.runtime.service import RuntimeService, RuntimeSettings


REPO = Path(__file__).resolve().parents[3]
FIXTURES = REPO / "docs/features/agents-communication-infra/specs/fixtures/protocol-compilation-v1"


def fixture(name: str):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def request(case: str = "compiled") -> tuple[dict, bytes]:
    prefix = "" if case == "compiled" else "unsupported-"
    value = {
        "schema": "aci.compile-dispatch-candidate-request@1",
        "compiler_contract_digest": COMPILER_CONTRACT_DIGEST,
    }
    for name in ("profile", "binding", "recipe", "invocation"):
        document = canonical_text(fixture(prefix + name + ".json"))
        value[name + "_document"] = document
        value[name + "_digest"] = digest_bytes(document.encode("utf-8"))
    return value, canonical_bytes(value)


def failure(data: bytes) -> str:
    with unittest.TestCase().assertRaises(ProtocolCompileFailure) as caught:
        ProtocolCompiler().compile_candidate(data)
    return caught.exception.code


def replace_documents(value: dict, profile: dict, binding: dict, recipe: dict, invocation: dict) -> bytes:
    for name, document in (("profile", profile), ("binding", binding), ("recipe", recipe), ("invocation", invocation)):
        text = canonical_text(document)
        value[name + "_document"] = text
        value[name + "_digest"] = digest_bytes(text.encode())
    return canonical_bytes(value)


def linked_request(profile: dict, binding: dict, recipe: dict, invocation: dict) -> bytes:
    """Rebind all content identities after a semantic test mutation."""
    recipe["profile_digest"] = digest_bytes(canonical_bytes(profile))
    binding["profile_digest"] = recipe["profile_digest"]
    binding["recipe_digest"] = digest_bytes(canonical_bytes(recipe))
    invocation["profile_digest"] = binding["profile_digest"]
    invocation["recipe_digest"] = binding["recipe_digest"]
    invocation["binding_digest"] = digest_bytes(canonical_bytes(binding))
    value, _ = request()
    return replace_documents(value, profile, binding, recipe, invocation)


class ProtocolCompilationTests(unittest.TestCase):
    def test_pc1_closed_schema_and_total_category_precedence(self) -> None:
        value, _ = request(); value["unknown"] = True
        self.assertEqual(failure(canonical_bytes(value)), "invalid_request_schema")
        value, _ = request(); profile = json.loads(value["profile_document"]); del profile["skill_id"]
        value["profile_document"] = json.dumps(profile, indent=2)
        value["profile_digest"] = "sha256:" + "0" * 64
        self.assertEqual(failure(canonical_bytes(value)), "invalid_document_schema")
        value, _ = request(); value["profile_document"] = " " + value["profile_document"]
        value["profile_digest"] = "sha256:" + "0" * 64
        self.assertEqual(failure(canonical_bytes(value)), "noncanonical_bytes")
        base, _ = request()
        for field in tuple(base):
            mutated = dict(base); del mutated[field]
            with self.subTest(request_missing=field):
                self.assertEqual(failure(canonical_bytes(mutated)), "invalid_request_schema")
        duplicate = canonical_bytes(base).replace(b'{"binding_digest"', b'{"schema":"duplicate","binding_digest"', 1)
        self.assertEqual(failure(duplicate), "invalid_request_schema")
        embedded, _ = request()
        embedded["profile_document"] = embedded["profile_document"].replace(
            '"skill_id":', '"skill_id":"duplicate","skill_id":', 1
        )
        embedded["profile_digest"] = digest_bytes(embedded["profile_document"].encode("utf-8"))
        self.assertEqual(failure(canonical_bytes(embedded)), "invalid_document_schema")
        for name in ("profile", "binding", "recipe", "invocation"):
            mutated, _ = request(); document = json.loads(mutated[name + "_document"])
            document["unknown"] = None
            text = canonical_text(document); mutated[name + "_document"] = text; mutated[name + "_digest"] = digest_bytes(text.encode())
            with self.subTest(document_unknown=name):
                self.assertEqual(failure(canonical_bytes(mutated)), "invalid_document_schema")
        nested = (
            ("profile", "obligations"), ("profile", "parameters"),
            ("profile", "capability_requirements"), ("profile", "outputs"),
            ("recipe", "nodes"), ("recipe", "edges"),
            ("recipe", "obligation_rules"), ("invocation", "values"),
        )
        for name, collection in nested:
            mutated, _ = request(); document = json.loads(mutated[name + "_document"])
            document[collection][0]["unknown"] = True
            text = canonical_text(document); mutated[name + "_document"] = text; mutated[name + "_digest"] = digest_bytes(text.encode())
            with self.subTest(nested_unknown=collection):
                self.assertEqual(failure(canonical_bytes(mutated)), "invalid_document_schema")
        # Every adjacent failure-category boundary is fixed and deterministic.
        value, _ = request(); value["unknown"] = True; value["profile_document"] = "not-json"
        self.assertEqual(failure(canonical_bytes(value)), "invalid_request_schema")
        value, _ = request(); profile=json.loads(value["profile_document"]); del profile["skill_id"]
        value["profile_document"] = " " + canonical_text(profile); value["profile_digest"] = "sha256:" + "0"*64
        self.assertEqual(failure(canonical_bytes(value)), "invalid_document_schema")
        value, _ = request(); value["profile_document"] = " " + value["profile_document"]; value["profile_digest"] = "sha256:" + "0"*64
        self.assertEqual(failure(canonical_bytes(value)), "noncanonical_bytes")
        p=fixture("profile.json"); b=fixture("binding.json"); r=fixture("recipe.json"); i=fixture("invocation.json"); b["status"]="stale"
        value=json.loads(linked_request(p,b,r,i)); value["compiler_contract_digest"]="sha256:"+"0"*64
        self.assertEqual(failure(canonical_bytes(value)), "compiler_identity_mismatch")
        self.assertEqual(failure(linked_request(p,b,r,i)), "inactive_binding")
        p=fixture("profile.json"); b=fixture("binding.json"); r=fixture("recipe.json"); i=fixture("invocation.json"); b["skill_id"]="wrong"; i["skill_id"]="wrong"; i["values"]=[]
        self.assertEqual(failure(linked_request(p,b,r,i)), "binding_mismatch")
        p=fixture("profile.json"); b=fixture("binding.json"); r=fixture("recipe.json"); i=fixture("invocation.json"); i["skill_id"]="wrong"; i["values"]=[]
        self.assertEqual(failure(linked_request(p,b,r,i)), "invocation_mismatch")
        p=fixture("profile.json"); b=fixture("binding.json"); r=fixture("recipe.json"); i=fixture("invocation.json")
        i["values"]=[]; r["obligation_rules"][0]["target_refs"]=[]
        self.assertEqual(failure(linked_request(p,b,r,i)), "invalid_parameter_value")
        p=fixture("profile.json"); b=fixture("binding.json"); r=fixture("recipe.json"); i=fixture("invocation.json")
        r["obligation_rules"][0]["target_refs"]=[]
        r["edges"].append({"edge_id":"done_to_work","edge_kind":"feeds","from_node_id":"done","to_node_id":"work"})
        r["edges"].sort(key=lambda edge:(edge["from_node_id"],edge["to_node_id"],edge["edge_id"]))
        self.assertEqual(failure(linked_request(p,b,r,i)), "invalid_obligation_mapping")
        p=fixture("profile.json"); b=fixture("binding.json"); r=fixture("recipe.json"); i=fixture("invocation.json")
        r["edges"][0]["to_node_id"]="missing"
        self.assertEqual(failure(linked_request(p,b,r,i)), "invalid_graph")

    def test_pc2_frozen_canonical_golden_vectors(self) -> None:
        _, data = request(); result = ProtocolCompiler().compile_candidate(data)
        self.assertEqual(result, canonical_bytes(fixture("result.json")))
        self.assertEqual(digest_bytes(canonical_bytes(fixture("candidate.json"))), fixture("result.json")["candidate_digest"])
        self.assertEqual((FIXTURES / "invocation.json").read_bytes()[-1:], b"\n")
        manifest = fixture("manifest.json")
        cases = {item["case_id"]: item for item in manifest["cases"]}
        for case_id, prefix, result_name in (
            ("compiled", "", "result.json"),
            ("required-unsupported", "unsupported-", "unsupported-result.json"),
        ):
            case = cases[case_id]
            for name in ("profile", "binding", "recipe", "invocation"):
                self.assertEqual(
                    case["input_digests"][name],
                    digest_bytes(canonical_bytes(fixture(prefix + name + ".json"))),
                )
            self.assertEqual(case["result_digest"], digest_bytes(canonical_bytes(fixture(result_name))))
        self.assertEqual(cases["compiled"]["candidate_digest"], digest_bytes(canonical_bytes(fixture("candidate.json"))))
        raw_hashes = {
            "skill-source.json":"1a1b13f817e88b9ab08f05c15ca33b709d75fa0cd153455cfe9cf35480e1a742",
            "profile.json":"da430d5f1cb0bc73c20f5722a5678c993983d70a6b3076f33021083dadd19ed5",
            "recipe.json":"05731f234c5a9aaada6b253c012219da33ae36301820b85bd7f5d55c2953d0bd",
            "binding.json":"e8e6a30e697b4bf0a646c1345a1c3a299b95fcd66dc8cc41f6fc7405936df681",
            "invocation.json":"d83595d04a3a4808dc8925aba6195561a37ffea75d7512e9d388749743be66ce",
            "compiler-contract.json":"6b15b4f6091058181cf7f32c9a8f155b5c0d8a6e6d4e9c35c6a36c716b2b947b",
            "candidate.json":"e05ae398a2f6111e3fff4620156b28320eeebbb835bee3a0c2f4a7d77a26f9b4",
            "result.json":"09714366cd3af0e3f965570b77c334bd3fc880ff38bb80b1ef379945039d0542",
            "unsupported-profile.json":"0db09987f24184a2e05aa7179f3017283a81f646afeb69d0d60035e6f597322b",
            "unsupported-recipe.json":"e89e07b4ad082a7cf00e00fe2eb3125e22fdc054a6e31a635dce9fd67d068da3",
            "unsupported-binding.json":"9e021be2fecd37b594d8d586086027d4a79413fe5f2b366dd2dd7a40a5ee114b",
            "unsupported-invocation.json":"ef06ac2d4cd7deaf59b9c570af1b638574caeefceed33d6592e5d001c68e7e5c",
            "unsupported-result.json":"61c7722659c8c152c35e6f8c0887b2b48e9862e202db70cdfd220ed1ece29ad4",
            "manifest.json":"8b902a972e7c605dc5df3ba51b35a0e1d0c0bfafb7d27d7e592f7bbcc49b7553",
        }
        for name, expected in raw_hashes.items():
            self.assertEqual(hashlib.sha256((FIXTURES / name).read_bytes()).hexdigest(), expected)
        canonical_hashes = {
            "skill-source.json":"13ea3dea6640fd553a56662c7efd4bc63480f82b07c49f6e3614b72f4201bc36",
            "profile.json":"43229944b101d12c6d14008d1db17f40c41277b7b441417c7ca5cd38006d7d17",
            "recipe.json":"92fbf20eebbe5ba490bcd1969eed86e3ae91e4e643d7f448a1a089d3be2b50e3",
            "binding.json":"26d7a8a3fb4955a9442d5807b7c27c1c1f204b394e3862437c49a4aae5b14c7b",
            "invocation.json":"469dff24fc67a048a0f5f7040704c3601861beb386b9713dc3eb4e3b233de77b",
            "compiler-contract.json":"9fd10473647a5ea5a7f03df6370773fab2af911cca9d37ffc1e2b7912a009543",
            "candidate.json":"9b829ca70a4717a133a8e42b18e7d95210d1bbfcd5c1e785b56b38778f6df795",
            "result.json":"1a38bb57cddfc8940c1ff19011f543b18e8844a2e2d68b12a340ded527aecb84",
            "unsupported-profile.json":"43ec4c29eca01a6786ec9fff2723c2623828af286e80c67f2b320672d002fa1e",
            "unsupported-recipe.json":"16ce0d514a5b1b42d1c2170d0c4eb8b04a72d150adb4f7bb7b0ef91796c8aaa1",
            "unsupported-binding.json":"10bc707b787041d8b3327a1f3096b5635fae56d75975b0ffbf81f82fa2b00f8a",
            "unsupported-invocation.json":"0fdbd75e214f91a0ad53cec35849d43208af1d51dfa1f1c0300cfa0be3a11c17",
            "unsupported-result.json":"9544a32ccf39309dc778d78623948675c9f80e73ecae52a0108458db35ae0578",
            "manifest.json":"e5cc329254ab8f748888f198ee004cba45f186b5ca21702612932f2c66ef0420",
        }
        for name, expected in canonical_hashes.items():
            self.assertEqual(digest_bytes(canonical_bytes(fixture(name))), "sha256:" + expected)
        self.assertEqual(canonical_text({"z":1,"a":[2,1],"text":"e\u0301"}), '{"a":[2,1],"text":"é","z":1}')
        with self.assertRaises(Exception): canonical_bytes({"float": 1.5})
        with self.assertRaises(Exception): canonical_bytes({"integer": 2**63})
        with self.assertRaises(Exception): canonical_bytes({"é":1,"e\u0301":2})
        for malformed in (b"\xef\xbb\xbf{}", b" {}", b"{}\n", b'{"n":NaN}', b'{"n":Infinity}'):
            self.assertEqual(failure(malformed), "invalid_request_schema")
        self.assertEqual(canonical_bytes({"array":[2,1],"boolean":True,"integer":1}), b'{"array":[2,1],"boolean":true,"integer":1}')
        self.assertEqual(canonical_text({"max":2**63-1,"min":-(2**63)}), '{"max":9223372036854775807,"min":-9223372036854775808}')

    def test_pc3_digest_and_compiler_identity_fail_closed(self) -> None:
        for name in ("profile", "binding", "recipe", "invocation"):
            value, _ = request(); value[name + "_digest"] = "sha256:" + "0" * 64
            with self.subTest(digest=name):
                self.assertEqual(failure(canonical_bytes(value)), "digest_mismatch")
        value, _ = request(); value["compiler_contract_digest"] = "sha256:" + "0" * 64
        self.assertEqual(failure(canonical_bytes(value)), "compiler_identity_mismatch")
        value, _ = request(); changed = json.loads(value["profile_document"]); changed["profile_revision"] = "v2"
        value["profile_document"] = canonical_text(changed)
        self.assertEqual(failure(canonical_bytes(value)), "digest_mismatch")
        dependent_failures = {
            "profile": "binding_mismatch",
            "binding": "invocation_mismatch",
            "recipe": "binding_mismatch",
            "invocation": "fixture_not_admitted",
        }
        for name, expected in dependent_failures.items():
            value, _ = request(); document = json.loads(value[name + "_document"])
            revision_field = {
                "profile": "profile_revision", "binding": "binding_revision",
                "recipe": "recipe_revision", "invocation": None,
            }[name]
            if revision_field is None:
                document["values"][0]["value"] = "changed topic"
            else:
                document[revision_field] = document[revision_field] + "-changed"
            text = canonical_text(document)
            value[name + "_document"] = text
            value[name + "_digest"] = digest_bytes(text.encode("utf-8"))
            with self.subTest(recomputed_document=name):
                self.assertEqual(failure(canonical_bytes(value)), expected)
        result = json.loads(ProtocolCompiler().compile_candidate(request()[1]))
        source_binding = json.loads(result["candidate_document"])["source_binding"]
        self.assertEqual(
            set(source_binding),
            {
                "skill_id", "skill_revision_digest", "profile_digest", "binding_digest",
                "recipe_digest", "invocation_digest", "compiler_contract_digest",
            },
        )

    def test_pc4_parameters_are_explicit_and_not_coerced(self) -> None:
        value, _ = request(); p=fixture("profile.json"); b=fixture("binding.json"); r=fixture("recipe.json"); i=fixture("invocation.json")
        i["values"] = []
        self.assertEqual(failure(replace_documents(value,p,b,r,i)), "invalid_parameter_value")
        for delimiter in ("{{not-a-template", "not-a-template}}"):
            value, _ = request(); p=fixture("profile.json"); b=fixture("binding.json"); r=fixture("recipe.json"); i=fixture("invocation.json")
            i["values"][0]["value"] = delimiter
            self.assertEqual(failure(replace_documents(value,p,b,r,i)), "invalid_parameter_value")
        for values in (
            [{"parameter_id":"extra","value":"x"},{"parameter_id":"topic","value":"x"}],
            [{"parameter_id":"topic","value":7}],
            [{"parameter_id":"topic","value":"x"},{"parameter_id":"topic","value":"y"}],
        ):
            value, _ = request(); p=fixture("profile.json"); b=fixture("binding.json"); r=fixture("recipe.json"); i=fixture("invocation.json"); i["values"] = values
            with self.subTest(values=values):
                self.assertIn(failure(replace_documents(value,p,b,r,i)), {"invalid_document_schema", "invalid_parameter_value"})
        p=fixture("profile.json"); b=fixture("binding.json"); r=fixture("recipe.json"); i=fixture("invocation.json")
        p["parameters"][0]["required"] = False; i["values"] = []
        self.assertEqual(failure(linked_request(p,b,r,i)), "invalid_parameter_value")
        p=fixture("profile.json"); b=fixture("binding.json"); r=fixture("recipe.json"); i=fixture("invocation.json")
        p["parameters"][0]["required"] = False; i["values"] = []
        r["nodes"][0]["prompt_template"] = "Finalize the report"
        r["nodes"][1]["prompt_template"] = "Analyze the supplied subject"
        self.assertEqual(failure(linked_request(p,b,r,i)), "fixture_not_admitted")
        for schema, scalar in (({"type":"integer"}, True), ({"type":"boolean"}, 1), ({"type":"string","enum_values":["allowed"]}, "denied"), ({"type":"string","max_length":1}, "xx")):
            p=fixture("profile.json"); b=fixture("binding.json"); r=fixture("recipe.json"); i=fixture("invocation.json")
            p["parameters"][0]["value_schema"] = schema; i["values"][0]["value"] = scalar
            with self.subTest(schema=schema, scalar=scalar):
                self.assertEqual(failure(linked_request(p,b,r,i)), "invalid_parameter_value")
        for scalar in (-(2**63), 2**63-1):
            p=fixture("profile.json"); b=fixture("binding.json"); r=fixture("recipe.json"); i=fixture("invocation.json")
            p["parameters"][0]["value_schema"]={"type":"integer"}; i["values"][0]["value"]=scalar
            with self.subTest(int64_endpoint=scalar):
                self.assertEqual(failure(linked_request(p,b,r,i)), "fixture_not_admitted")
        p=fixture("profile.json"); b=fixture("binding.json"); r=fixture("recipe.json"); i=fixture("invocation.json")
        p["parameters"][0]["value_schema"]["default"]="hidden"
        self.assertEqual(failure(linked_request(p,b,r,i)), "invalid_document_schema")
        p=fixture("profile.json"); b=fixture("binding.json"); r=fixture("recipe.json"); i=fixture("invocation.json")
        p["parameters"].insert(0,{"parameter_id":"alpha","required":False,"value_schema":{"type":"string"}})
        i["values"].append({"parameter_id":"alpha","value":"x"})
        self.assertEqual(failure(linked_request(p,b,r,i)), "invalid_document_schema")
        p=fixture("profile.json"); b=fixture("binding.json"); r=fixture("recipe.json"); i=fixture("invocation.json")
        r["nodes"][1]["prompt_template"] = "Analyze {{parameter:missing}}"
        self.assertEqual(failure(linked_request(p,b,r,i)), "invalid_parameter_value")
        p=fixture("profile.json"); b=fixture("binding.json"); r=fixture("recipe.json"); i=fixture("invocation.json")
        r["nodes"][1]["prompt_template"] = "Analyze {{parameter:topic"
        self.assertEqual(failure(linked_request(p,b,r,i)), "invalid_parameter_value")

    def test_pc5_required_unsupported_is_exact_and_never_candidate(self) -> None:
        _, data = request("unsupported")
        result = ProtocolCompiler().compile_candidate(data)
        self.assertEqual(result, canonical_bytes(fixture("unsupported-result.json")))
        self.assertEqual(set(json.loads(result)), {"schema", "outcome", "unsupported_obligation_ids"})
        p=fixture("unsupported-profile.json"); b=fixture("unsupported-binding.json"); r=fixture("unsupported-recipe.json"); i=fixture("unsupported-invocation.json")
        rule=r["obligation_rules"][0]; rule["disposition"]="superseded"; rule["authority_ref"]={"authority_kind":"policy","authority_digest":"sha256:"+"1"*64}
        self.assertEqual(failure(linked_request(p,b,r,i)), "fixture_not_admitted")
        invalid_rules = []
        r=fixture("recipe.json"); r["obligation_rules"][0]["target_refs"]=[]; invalid_rules.append(r)
        r=fixture("recipe.json"); r["obligation_rules"][0]["authority_ref"]={"authority_kind":"policy","authority_digest":"sha256:"+"1"*64}; invalid_rules.append(r)
        r=fixture("recipe.json"); r["obligation_rules"][0]["disposition"]="unsupported"; invalid_rules.append(r)
        r=fixture("recipe.json"); r["obligation_rules"]=[]; invalid_rules.append(r)
        for r in invalid_rules:
            with self.subTest(rule=r.get("obligation_rules")):
                self.assertEqual(failure(linked_request(fixture("profile.json"),fixture("binding.json"),r,fixture("invocation.json"))), "invalid_obligation_mapping")
        fake_store = Mock(); service = RuntimeService.__new__(RuntimeService); service.artifacts = fake_store
        _, unsupported_data = request("unsupported")
        self.assertIsNone(service.compile_and_store_dispatch_candidate(unsupported_data)["artifact_ref"])
        fake_store.assert_not_called()

    def test_pc6_invalid_dag_precedes_fixture_admission(self) -> None:
        value, _ = request(); p=fixture("profile.json"); b=fixture("binding.json"); r=fixture("recipe.json"); i=fixture("invocation.json")
        r["edges"].append({"edge_id":"done_to_work","edge_kind":"feeds","from_node_id":"done","to_node_id":"work"})
        r["edges"].sort(key=lambda x:(x["from_node_id"],x["to_node_id"],x["edge_id"]))
        r_text=canonical_text(r); r_digest=digest_bytes(r_text.encode()); b["recipe_digest"]=r_digest
        b_text=canonical_text(b); b_digest=digest_bytes(b_text.encode()); i["recipe_digest"]=r_digest; i["binding_digest"]=b_digest
        self.assertEqual(failure(replace_documents(value,p,b,r,i)), "invalid_graph")
        value, _ = request(); p=fixture("profile.json"); b=fixture("binding.json"); r=fixture("recipe.json"); i=fixture("invocation.json")
        duplicate = dict(r["edges"][0]); duplicate["from_node_id"] = "done"; duplicate["to_node_id"] = "work"
        r["edges"].append(duplicate)
        r["edges"].sort(key=lambda x:(x["from_node_id"],x["to_node_id"],x["edge_id"]))
        r_text=canonical_text(r); r_digest=digest_bytes(r_text.encode()); b["recipe_digest"]=r_digest
        b_text=canonical_text(b); b_digest=digest_bytes(b_text.encode()); i["recipe_digest"]=r_digest; i["binding_digest"]=b_digest
        self.assertEqual(failure(replace_documents(value,p,b,r,i)), "invalid_graph")
        graph_mutations = []
        r=fixture("recipe.json"); r["edges"][0]["to_node_id"]="missing"; graph_mutations.append(r)
        r=fixture("recipe.json"); r["edges"][0]["to_node_id"]="work"; graph_mutations.append(r)
        r=fixture("recipe.json"); r["terminal_node_ids"]=["work"]; graph_mutations.append(r)
        r=fixture("recipe.json"); r["edges"]=[]; graph_mutations.append(r)
        for r in graph_mutations:
            with self.subTest(graph=r):
                self.assertEqual(failure(linked_request(fixture("profile.json"),fixture("binding.json"),r,fixture("invocation.json"))), "invalid_graph")
        long_id = "w" * 124
        p=fixture("profile.json"); b=fixture("binding.json"); r=fixture("recipe.json"); i=fixture("invocation.json")
        r["nodes"][1]["node_id"] = long_id; r["edges"][0]["from_node_id"] = long_id
        r["obligation_rules"][0]["target_refs"] = ["node:" + long_id, "output:report"]
        self.assertEqual(failure(linked_request(p,b,r,i)), "fixture_not_admitted")
        self.assertEqual(
            _topological_order(
                {"m", "z", "a", "done"},
                {"m":["a"], "z":["done"], "a":["done"], "done":[]},
                {"m":0, "z":0, "a":1, "done":2},
            ),
            ["m", "a", "z", "done"],
        )

    def test_pc7_candidate_has_logical_requirements_only(self) -> None:
        _, data=request(); result=json.loads(ProtocolCompiler().compile_candidate(data)); candidate=json.loads(result["candidate_document"])
        self.assertEqual(candidate["capability_requirements"], fixture("profile.json")["capability_requirements"])
        forbidden={"provider","credential","permission","effective_grant","dispatch_spec_digest"}
        def keys(value):
            if isinstance(value, dict):
                return set(value).union(*(keys(member) for member in value.values()))
            if isinstance(value, list):
                return set().union(*(keys(member) for member in value)) if value else set()
            return set()
        self.assertFalse(forbidden & keys(candidate))
        closed_candidate = copy.deepcopy(candidate); closed_candidate["effective_grant"] = {}
        with self.assertRaises(ValueError):
            _serialize_compiled_result(closed_candidate)
        closed_candidate = copy.deepcopy(candidate); closed_candidate["source_binding"]["dispatch_spec_digest"] = "sha256:" + "0" * 64
        with self.assertRaises(ValueError):
            _serialize_compiled_result(closed_candidate)
        with self.assertRaises(ValueError):
            _serialize_unsupported_result([])
        with self.assertRaises(ValueError):
            _serialize_unsupported_result(["z", "a"])

    def test_pc8_equal_requests_are_restart_independent(self) -> None:
        _, data=request()
        encoded = base64.b64encode(data).decode("ascii")
        script = (
            "import base64; from implementations.server.runtime.protocol_compilation "
            "import ProtocolCompiler; print(base64.b64encode(ProtocolCompiler().compile_candidate("
            "base64.b64decode('" + encoded + "'))).decode('ascii'))"
        )
        outputs = [
            subprocess.run(
                [sys.executable, "-c", script],
                cwd=REPO,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            for _ in range(2)
        ]
        self.assertEqual(outputs[0], outputs[1])
        self.assertEqual(base64.b64decode(outputs[0]), ProtocolCompiler().compile_candidate(data))
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); settings = RuntimeSettings(root/"runtime.db", REPO, root/"ledger.yaml")
            first_service = RuntimeService(settings); first_service.database.migrate()
            first = first_service.compile_and_store_dispatch_candidate(data)
            restarted_service = RuntimeService(settings); restarted_service.database.migrate()
            second = restarted_service.compile_and_store_dispatch_candidate(data)
            self.assertEqual(first["artifact_ref"]["artifact_id"], second["artifact_ref"]["artifact_id"])
            self.assertEqual(first["artifact_ref"]["content_hash"], second["artifact_ref"]["content_hash"])

    def test_pc9_pure_compiler_has_no_effect_dependencies(self) -> None:
        source = REPO / "implementations/server/runtime/protocol_compilation.py"
        tree = ast.parse(source.read_text(encoding="utf-8"))
        imports = {
            alias.name.split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        }
        relative_imports = {
            node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)
        }
        self.assertEqual(imports, {"heapq", "re"})
        self.assertEqual(relative_imports, {"__future__", "typing", "canonical", "errors"})
        _, data=request()
        sentinels = Mock(side_effect=AssertionError("forbidden effect"))
        with patch("builtins.open", sentinels), patch("time.time", sentinels), patch("random.random", sentinels), patch("os.getenv", sentinels), patch("socket.socket", sentinels):
            ProtocolCompiler().compile_candidate(data)
            ProtocolCompiler().compile_candidate(request("unsupported")[1])
            malformed, _ = request(); malformed["profile_digest"] = "sha256:" + "0"*64
            self.assertEqual(failure(canonical_bytes(malformed)), "digest_mismatch")
        sentinels.assert_not_called()

    def test_pc10_storage_is_separate_idempotent_and_compiled_only(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); service=RuntimeService(RuntimeSettings(root/"runtime.db", REPO, root/"ledger.yaml"))
            service.database.migrate()
            _, compiled=request(); first=service.compile_and_store_dispatch_candidate(compiled); second=service.compile_and_store_dispatch_candidate(compiled)
            self.assertEqual(first["artifact_ref"]["artifact_id"], second["artifact_ref"]["artifact_id"])
            self.assertEqual(first["artifact_ref"]["classification"], "runtime-internal")
            self.assertEqual(first["artifact_ref"]["media_type"], "application/json")
            self.assertEqual(first["artifact_ref"]["schema_ref"], "aci.dispatch-candidate@1")
            self.assertEqual(first["artifact_ref"]["content_hash"], fixture("result.json")["candidate_digest"])
            with service.database.connect() as conn:
                self.assertEqual(conn.execute("SELECT COUNT(*) FROM events").fetchone()[0], 0)
                self.assertEqual(conn.execute("SELECT COUNT(*) FROM command_receipts").fetchone()[0], 0)
                self.assertEqual(conn.execute("SELECT COUNT(*) FROM publication_receipts").fetchone()[0], 0)
            _, unsupported=request("unsupported"); blocked=service.compile_and_store_dispatch_candidate(unsupported)
            self.assertIsNone(blocked["artifact_ref"])
            conflicting = Mock()
            conflicting.prepare.return_value = SimpleNamespace(content_hash="sha256:" + "0" * 64)
            service.artifacts = conflicting
            with self.assertRaisesRegex(ProtocolCompileFailure, "artifact_content_conflict"):
                service.compile_and_store_dispatch_candidate(compiled)
            no_store = Mock(); service.artifacts = no_store
            bad, _ = request(); bad["profile_digest"] = "sha256:" + "0"*64
            with self.assertRaises(ProtocolCompileFailure):
                service.compile_and_store_dispatch_candidate(canonical_bytes(bad))
            no_store.assert_not_called()
            conflicting.commit.assert_not_called()
            conflicting.prepare.return_value = SimpleNamespace(
                content_hash=fixture("result.json")["candidate_digest"]
            )
            conflicting.commit.side_effect = ConflictError("collision")
            with self.assertRaisesRegex(ProtocolCompileFailure, "artifact_content_conflict"):
                service.compile_and_store_dispatch_candidate(compiled)

    def test_pc11_both_admitted_cases_match_exact_outputs(self) -> None:
        for case, expected in (("compiled","result.json"),("unsupported","unsupported-result.json")):
            _, data=request(case)
            self.assertEqual(ProtocolCompiler().compile_candidate(data), canonical_bytes(fixture(expected)))
        _, data=request(); result=json.loads(ProtocolCompiler().compile_candidate(data)); candidate=json.loads(result["candidate_document"])
        recipe=fixture("recipe.json"); profile=fixture("profile.json"); invocation=fixture("invocation.json")
        self.assertEqual(candidate["edges"], recipe["edges"])
        self.assertEqual(candidate["terminal_node_ids"], recipe["terminal_node_ids"])
        self.assertEqual(candidate["invocation_values"], invocation["values"])
        self.assertEqual(candidate["capability_requirements"], profile["capability_requirements"])
        self.assertEqual(candidate["outputs"], profile["outputs"])
        self.assertEqual(candidate["nodes"], fixture("candidate.json")["nodes"])
        self.assertEqual(candidate, fixture("candidate.json"), "every candidate leaf must match the frozen provenance oracle")
        topic = canonical_text(invocation["values"][0]["value"])
        self.assertEqual(candidate["nodes"][0]["prompt_template"], "Finalize report for " + topic)
        self.assertEqual(candidate["nodes"][1]["prompt_template"], "Analyze " + topic)
        self.assertEqual(candidate["obligation_dispositions"], recipe["obligation_rules"])
        source = candidate["source_binding"]
        self.assertEqual(source["skill_id"], profile["skill_id"])
        self.assertEqual(source["skill_revision_digest"], profile["skill_revision_digest"])
        for name in ("profile", "binding", "recipe", "invocation"):
            self.assertEqual(source[name + "_digest"], request()[0][name + "_digest"])
        self.assertEqual(source["compiler_contract_digest"], COMPILER_CONTRACT_DIGEST)

    def test_pc12_candidate_is_not_runtime_authority(self) -> None:
        self.assertFalse(any(hasattr(ProtocolCompiler, name) for name in ("confirm","run","launch","schedule","activate","revoke")))
        _, data=request(); candidate=json.loads(json.loads(ProtocolCompiler().compile_candidate(data))["candidate_document"])
        self.assertEqual(candidate["schema"], "aci.dispatch-candidate@1")
        self.assertNotIn("dispatch_spec_digest", candidate)
        self.assertNotEqual(result_digest := digest_bytes(canonical_bytes(candidate)), "dispatch_spec_digest")
        self.assertEqual(result_digest, json.loads(ProtocolCompiler().compile_candidate(data))["candidate_digest"])
        api_source = (REPO / "implementations/server/runtime/api.py").read_text(encoding="utf-8")
        self.assertNotIn("compile_and_store_dispatch_candidate", api_source)


if __name__ == "__main__":
    unittest.main()
