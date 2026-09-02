from __future__ import annotations

import base64
import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from implementations.server.runtime.agent_pool import AgentPoolError, migrate_legacy_pool, normalize_pool_documents, parse_pool_stream
from implementations.server.runtime.agent_roles import AgentRoleError, load_accepted_role_registry
from implementations.server.runtime.draft_graph_compiler import DraftGraphCompileError, DraftGraphCompiler, TrustedAllocatorContextGate


REPO = Path(__file__).resolve().parents[3]
SPEC = REPO / "docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/followups/SPEC-ACI-AGENT-IDENTITY-ROLE-001"
IMPL = REPO / "docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/followups/IMPL-ACI-AGENT-IDENTITY-ROLE-001"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def encode(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def resign(context: dict, evidence: dict) -> None:
    context_bytes = json.dumps(context, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    evidence["context_digest"] = "sha256:" + hashlib.sha256(context_bytes).hexdigest()
    payload = {key: evidence[key] for key in ("schema", "evidence_id", "key_id", "context_digest", "is_latest", "pair_is_unbound")}
    message = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    evidence["signature"] = base64.b64encode(Ed25519PrivateKey.from_private_bytes(bytes(range(32))).sign(message)).decode("ascii")


class AgentIdentityRoleVectorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.vectors = load(SPEC / "fixtures/negative-vectors.json")["vectors"]
        self.registry = load_accepted_role_registry(REPO)
        self.pool_docs = parse_pool_stream((REPO / "telemetry/agents/agent-pool.yaml").read_bytes())
        self.draft = load(IMPL / "fixtures/review-correct-verify.draft.json")
        self.policy = load(IMPL / "fixtures/policy.json")
        self.catalog = load(IMPL / "fixtures/catalog.json")
        self.resources = load(IMPL / "fixtures/resources.json")
        self.context = load(IMPL / "fixtures/compilation-context.json")
        self.evidence = load(IMPL / "fixtures/allocator-evidence.json")
        self.trust = load(IMPL / "fixtures/allocator-trust.json")
        self.compiler_registry_raw = (IMPL / "fixtures/role-registry.json").read_bytes()
        self.compiler_pool = load(IMPL / "fixtures/normalized-agent-pool.json")

    def pool_failure(self, vector: dict) -> None:
        docs = copy.deepcopy(self.pool_docs)
        entries = docs[1]["scientists"]
        op = vector["operation"]
        if op == "pool_remove_name": entries[0].pop("agent_name")
        elif op == "pool_add_hyphen_name": entries[0]["agent-name"] = vector["value"]
        elif op == "pool_set_name": entries[0]["agent_name"] = vector["value"]
        elif op == "pool_use_legacy_name": entries[0]["name"] = entries[0].pop("agent_name")
        elif op == "pool_use_hyphen_name": entries[0]["agent-name"] = entries[0].pop("agent_name")
        elif op == "pool_duplicate_name": entries[1]["agent_name"] = entries[0]["agent_name"]
        elif op == "pool_unknown_key": entries[0]["nickname"] = "Karl"
        elif op == "pool_drop_document": docs.pop()
        elif op == "pool_reverse_documents": docs.reverse()
        elif op == "real_pool_metadata_drift": docs[0]["description"] += " tampered"
        elif op in {"pool_unknown_role_fit", "pool_role_only_in_future_registry"}: entries[0]["role_fit"][0] = "hacker" if op == "pool_unknown_role_fit" else "researcher"
        else: raise AssertionError(op)
        normalize_pool_documents(docs, self.registry)

    def compile_failure(self, vector: dict) -> None:
        draft = copy.deepcopy(self.draft)
        context = copy.deepcopy(self.context)
        evidence = copy.deepcopy(self.evidence)
        op = vector["operation"]
        assignments = context["agent_assignments"]
        if op == "draft_set_role": draft["nodes"][0]["agent_request"]["role"] = vector["value"]
        elif op == "draft_add_display_name": draft["nodes"][0]["agent_request"]["display_name"] = "LLM name"
        elif op == "assignment_disable_override": assignments[1].update(role_fit_override=False, role_fit_override_reason=None)
        elif op == "assignment_empty_override_reason": assignments[1]["role_fit_override_reason"] = ""
        elif op == "assignment_reuse_name": assignments[2]["display_name"] = assignments[0]["display_name"]
        elif op == "assignment_remove": assignments.pop()
        elif op == "assignment_add_unknown_node": assignments.append({"node_key": "ghost", "display_name": "Popper, Karl", "role_fit_override": False, "role_fit_override_reason": None})
        elif op == "assignment_unknown_pool_name": assignments[0]["display_name"] = "Unknown, Agent"
        elif op == "context_registry_ref_drift": context["role_registry_ref"]["digest"] = "sha256:" + "f" * 64
        elif op == "context_pool_ref_drift": context["agent_pool_ref"]["digest"] = "sha256:" + "f" * 64
        elif op == "assignment_tamper_without_evidence": assignments[0]["display_name"] = "Unknown, Agent"
        elif op == "forge_signature": evidence["signature"] = base64.b64encode(b"0" * 64).decode("ascii")
        elif op == "evidence_mark_stale": evidence["is_latest"] = False
        elif op == "evidence_mark_bound": evidence["pair_is_unbound"] = False
        elif op == "evidence_replay": pass
        elif op == "assignment_duplicate_node_key": assignments[1]["node_key"] = "review"
        else: raise AssertionError(op)
        if vector.get("resign"): resign(context, evidence)
        consumed = {evidence["evidence_id"]} if op == "evidence_replay" else None
        verified = TrustedAllocatorContextGate.verify(encode(context), encode(evidence), encode(self.trust), consumed)
        DraftGraphCompiler().compile(verified, encode(draft), encode(self.policy), encode(self.catalog), encode(self.resources), self.compiler_registry_raw, encode(self.compiler_pool))

    def registry_failure(self, vector: dict) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            contracts = root / "implementations/contracts"
            contracts.mkdir(parents=True)
            for name in ("agent-role-registry.v1.json", "agent-role-registry-authority.v1.json", "agent-role-host-routing.v1.json", "agent-role-registry-selection.json"):
                (contracts / name).write_bytes((REPO / "implementations/contracts" / name).read_bytes())
            path = contracts / "agent-role-registry.v1.json"
            registry = load(path)
            op = vector["operation"]
            if op == "registry_mutate_purpose_and_repin_context": registry["roles"][5]["purpose"] = "Mutated in place."
            elif op == "registry_duplicate_role": registry["roles"][5]["role_id"] = "skeptic"
            elif op == "registry_disable_requested_role": registry["roles"][2]["enabled"] = False
            elif op == "registry_remove_role": registry["roles"].pop()
            elif op == "registry_add_role": registry["roles"].append({"role_id": "hacker", "enabled": True, "purpose": "Unauthorized role."})
            elif op == "registry_unknown_version": registry["version"] = "2"
            elif op == "registry_reorder_roles": registry["roles"][0], registry["roles"][1] = registry["roles"][1], registry["roles"][0]
            elif op == "registry_substitute_name": registry["name"] = "aci.substituted-agent-roles"
            else: raise AssertionError(op)
            path.write_text(json.dumps(registry), encoding="utf-8")
            load_accepted_role_registry(root)

    def execute(self, vector: dict) -> None:
        op = vector["operation"]
        if op == "pool_duplicate_yaml_key":
            parse_pool_stream("profile: one\nprofile: two\n---\nscientists: []\n")
        elif op == "real_pool_raw_substitution":
            authority = load(SPEC / "fixtures/pool-migration-authority.json")
            raw = (SPEC / authority["source_fixture_path"]).read_bytes() + b"\n# substitution\n"
            migrate_legacy_pool(raw, authority, self.registry)
        elif op == "real_pool_metadata_drift":
            authority = load(SPEC / "fixtures/pool-migration-authority.json")
            source = parse_pool_stream((SPEC / authority["source_fixture_path"]).read_bytes())
            source[0]["description"] += " tampered"
            import yaml
            raw = yaml.safe_dump_all(source, allow_unicode=True, sort_keys=False).encode("utf-8")
            migrate_legacy_pool(raw, authority, self.registry)
        elif op.startswith("registry_"):
            self.registry_failure(vector)
        elif op.startswith(("draft_", "assignment_", "context_", "evidence_", "forge_")):
            self.compile_failure(vector)
        else:
            self.pool_failure(vector)

    def test_all_41_manifest_vectors_execute_against_runtime_and_emit_no_result(self) -> None:
        expected = {
            "AIR-N08": ("DG_POOL_DUPLICATE_NAME", "$.documents[1].scientists[1].agent_name"),
            "AIR-N09": ("DG_DUPLICATE_YAML_KEY", "$.yaml"),
            "AIR-N14": ("DG_ROLE_UNKNOWN", "nodes[review].agent_request.role"),
            "AIR-N15": ("DG_ROLE_UNKNOWN", "nodes[review].agent_request.role"),
            "AIR-N16": ("DG_ROLE_FIT_MISMATCH", "compilation_context.agent_assignments.correct"),
            "AIR-N17": ("DG_COMPILATION_CONTEXT_INVALID", "compilation_context.agent_assignments[1].role_fit_override_reason"),
            "AIR-N18": ("DG_AGENT_REUSED", "compilation_context.agent_assignments.verify.display_name"),
            "AIR-N19": ("DG_AGENT_ASSIGNMENT_MISSING", "compilation_context.agent_assignments"),
            "AIR-N20": ("DG_AGENT_ASSIGNMENT_EXTRA", "compilation_context.agent_assignments.ghost"),
            "AIR-N21": ("DG_AGENT_ASSIGNMENT_UNKNOWN", "compilation_context.agent_assignments.review.display_name"),
            "AIR-N22": ("DG_ROLE_REGISTRY_REF_DRIFT", "compilation_context.role_registry_ref"),
            "AIR-N23": ("DG_AGENT_POOL_REF_DRIFT", "compilation_context.agent_pool_ref"),
            "AIR-N24": ("DG_IDENTITY_CONTEXT_STALE", "compilation_context"),
            "AIR-N25": ("DG_ALLOCATOR_EVIDENCE_INVALID", "allocator_evidence.signature"),
            "AIR-N26": ("DG_IDENTITY_CONTEXT_STALE", "allocator_evidence.is_latest"),
            "AIR-N27": ("DG_AUTHORITY_CONFLICT", "allocator_evidence.pair_is_unbound"),
            "AIR-N28": ("DG_ALLOCATOR_EVIDENCE_REPLAY", "allocator_evidence.evidence_id"),
            "AIR-N29": ("DG_ROLE_REGISTRY_SUBSTITUTED", "$.digest"),
            "AIR-N30": ("DG_ROLE_REGISTRY_DUPLICATE", "$.roles[5].role_id"),
            "AIR-N31": ("DG_ROLE_REGISTRY_DISABLED", "$.roles[2].enabled"),
            "AIR-N32": ("DG_ROLE_REGISTRY_SUBSTITUTED", "$.digest"),
            "AIR-N33": ("DG_ROLE_REGISTRY_SUBSTITUTED", "$.digest"),
            "AIR-N34": ("DG_ROLE_REGISTRY_UNTRUSTED", "$.name"),
            "AIR-N35": ("DG_DRAFT_SCHEMA_INVALID", "draft.nodes[0].agent_request"),
            "AIR-N37": ("DG_AGENT_ASSIGNMENT_DUPLICATE", "compilation_context.agent_assignments.review"),
            "AIR-N40": ("DG_ROLE_REGISTRY_SUBSTITUTED", "$.digest"),
            "AIR-N41": ("DG_ROLE_REGISTRY_UNTRUSTED", "$.name"),
        }
        self.assertEqual([row["id"] for row in self.vectors], [f"AIR-N{index:02d}" for index in range(1, 42)])
        for vector in self.vectors:
            result = None
            with self.subTest(vector=vector["id"]):
                try:
                    result = self.execute(vector)
                except (AgentPoolError, AgentRoleError, DraftGraphCompileError) as exc:
                    actual = (exc.code, exc.path)
                else:
                    self.fail(f"{vector['id']} produced a result")
                self.assertIsNone(result)
                self.assertEqual(actual, expected.get(vector["id"], (vector["expected"], vector["path"])))


if __name__ == "__main__":
    unittest.main()
