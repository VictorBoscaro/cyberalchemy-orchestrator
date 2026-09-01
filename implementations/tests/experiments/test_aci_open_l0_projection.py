from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT = ROOT / "implementations" / "experiments" / "aci_open_l0"
FIXTURES = EXPERIMENT / "fixtures"


def load_module(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, EXPERIMENT / relative)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {relative}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PROJECTOR = load_module("aci_open_l0_projector", "projector.py")
ORACLE = load_module("aci_open_l0_independent_oracle", "independent_oracle.py")


def canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


class OpenL0ProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = json.loads((FIXTURES / "synthetic-input.json").read_text(encoding="utf-8"))
        cls.expected_row = json.loads((FIXTURES / "expected-unstamped-row.json").read_text(encoding="utf-8"))
        cls.expected_report = json.loads(
            (FIXTURES / "expected-discrepancy-report.json").read_text(encoding="utf-8")
        )

    def assert_rejected_by_both(self, candidate):
        with self.assertRaises((PROJECTOR.ProjectionError, ValueError)):
            PROJECTOR.project(copy.deepcopy(candidate))
        with self.assertRaises((ORACLE.OracleRejection, ValueError)):
            ORACLE.compare(copy.deepcopy(candidate))

    # OPEN-L0-T1
    def test_t1_independent_implementations_and_frozen_outputs_are_byte_identical(self):
        projected = PROJECTOR.project(copy.deepcopy(self.source))
        compared = ORACLE.compare(copy.deepcopy(self.source))
        self.assertEqual(projected["bytes"], compared["bytes"])
        self.assertEqual(projected["digests"], compared["digests"])
        self.assertEqual(projected["projection_digest"], compared["projection_digest"])
        self.assertEqual(projected["bytes"]["unstamped_row"], canonical(self.expected_row))
        self.assertEqual(projected["bytes"]["discrepancy_report"], canonical(self.expected_report))
        self.assertNotIn(b"created", projected["bytes"]["unstamped_row"])
        self.assertEqual(projected["authority"], "none")
        self.assertIs(projected["non_authoritative"], True)

    # OPEN-L0-T2
    def test_t2_closed_shapes_semantic_array_order_and_object_key_canonicalization(self):
        mutations = []
        missing = copy.deepcopy(self.source)
        missing.pop("context")
        mutations.append(missing)
        extra = copy.deepcopy(self.source)
        extra["unexpected"] = "synthetic"
        mutations.append(extra)
        nested_extra = copy.deepcopy(self.source)
        nested_extra["operations"][0]["unexpected"] = "synthetic"
        mutations.append(nested_extra)
        reordered_operations = copy.deepcopy(self.source)
        reordered_operations["operations"][0], reordered_operations["operations"][1] = (
            reordered_operations["operations"][1], reordered_operations["operations"][0]
        )
        mutations.append(reordered_operations)
        reordered_groups = copy.deepcopy(self.source)
        reordered_groups["audit_groups"].reverse()
        mutations.append(reordered_groups)
        reordered_connections = copy.deepcopy(self.source)
        reordered_connections["connections"].reverse()
        mutations.append(reordered_connections)
        for candidate in mutations:
            with self.subTest(candidate=list(candidate)):
                self.assert_rejected_by_both(candidate)

        reordered_keys = dict(reversed(list(copy.deepcopy(self.source).items())))
        reordered_keys["candidate_route"] = dict(
            reversed(list(reordered_keys["candidate_route"].items()))
        )
        self.assertEqual(
            PROJECTOR.project(self.source)["bytes"],
            PROJECTOR.project(reordered_keys)["bytes"],
        )
        self.assertEqual(
            ORACLE.compare(self.source)["bytes"],
            ORACLE.compare(reordered_keys)["bytes"],
        )

    # OPEN-L0-T3
    def test_t3_direct_runtime_roles_duplicate_groups_wrong_bindings_and_layers_two_reject(self):
        author_direct = copy.deepcopy(self.source)
        author_direct["role_mapping"]["author"] = "author"
        reviewer_direct = copy.deepcopy(self.source)
        reviewer_direct["role_mapping"]["reviewer"] = "reviewer"
        duplicate_group = copy.deepcopy(self.source)
        duplicate_group["operations"][2]["audit_group_id"] = "audit_author_turn_0"
        wrong_binding = copy.deepcopy(self.source)
        wrong_binding["connections"][0]["to_operation_id"] = "author_turn_1"
        layers_two = copy.deepcopy(self.source)
        layers_two["operations"][0]["layers"] = 2
        for candidate in (author_direct, reviewer_direct, duplicate_group, wrong_binding, layers_two):
            self.assert_rejected_by_both(candidate)

    # OPEN-L0-T4
    def test_t4_discrepancies_witness_every_declared_identity_and_order_loss(self):
        result = PROJECTOR.project(self.source)
        report = result["documents"]["discrepancy_report"]
        by_id = {item["id"]: item for item in report["discrepancies"]}
        self.assertEqual(
            set(by_id),
            {
                "authority-mode",
                "role-vocabulary",
                "logical-group-reuse",
                "shared-seat-session",
                "continuation-key",
                "reviewer-interposition",
            },
        )
        self.assertTrue(all(item["preserved"] is False and item["witness"] for item in by_id.values()))
        bindings = result["documents"]["operation_bindings"]["bindings"]
        self.assertEqual([item["operation_id"] for item in bindings], [
            "author_turn_0", "reviewer_turn_0", "author_turn_1"
        ])
        self.assertEqual(bindings[0]["seat_id"], bindings[2]["seat_id"])
        self.assertEqual(bindings[0]["logical_group_id"], bindings[2]["logical_group_id"])
        self.assertNotEqual(bindings[0]["audit_group_id"], bindings[2]["audit_group_id"])

    # OPEN-L0-T5
    def test_t5_inconsistent_route_rejects_and_consistent_drift_changes_only_hypothesis_digest(self):
        mismatched = copy.deepcopy(self.source)
        mismatched["candidate_route"]["tool_profile_ref"] = "synthetic/tool-profile@2"
        self.assert_rejected_by_both(mismatched)

        baseline = PROJECTOR.project(self.source)["projection_digest"]
        route_fields = {
            "registry_digest": "sha256:" + "1" * 64,
            "capability_digest": "sha256:" + "2" * 64,
            "tool_profile_ref": "synthetic/tool-profile@2",
        }
        for field, value in route_fields.items():
            candidate = copy.deepcopy(self.source)
            candidate["candidate_route"][field] = value
            body = dict(candidate["candidate_route"])
            body.pop("route_digest")
            candidate["candidate_route"]["route_digest"] = digest(canonical(body))
            projected = PROJECTOR.project(candidate)
            compared = ORACLE.compare(candidate)
            self.assertNotEqual(projected["projection_digest"], baseline)
            self.assertEqual(projected["projection_digest"], compared["projection_digest"])
            self.assertEqual(projected["authority"], "none")
            self.assertIs(projected["non_authoritative"], True)

        role_drift = copy.deepcopy(self.source)
        role_drift["role_mapping"] = {"author": "planner", "reviewer": "skeptic"}
        role_result = PROJECTOR.project(role_drift)
        self.assertNotEqual(role_result["projection_digest"], baseline)
        self.assertEqual(role_result["authority"], "none")

    # OPEN-L0-T6
    def test_t6_created_missing_empty_and_ambient_invoker_reject(self):
        created = copy.deepcopy(self.source)
        created["created"] = "synthetic-created-is-forbidden"
        missing = copy.deepcopy(self.source)
        missing.pop("invoked_by")
        empty = copy.deepcopy(self.source)
        empty["invoked_by"] = ""
        ambient = copy.deepcopy(self.source)
        ambient["invoked_by"] = "ambient"
        for candidate in (created, missing, empty, ambient):
            self.assert_rejected_by_both(candidate)

    # OPEN-L0-T7
    def test_t7_modules_are_independent_and_have_no_io_or_mutation_primitive(self):
        sources = {
            name: (EXPERIMENT / name).read_text(encoding="utf-8")
            for name in ("projector.py", "independent_oracle.py")
        }
        forbidden_import_roots = {
            "pathlib", "os", "subprocess", "socket", "sqlite3", "urllib", "requests",
            "http", "implementations",
        }
        forbidden_calls = {
            "open", "write", "run", "Popen", "connect", "request", "urlopen",
            "append_dispatch", "create_effect", "open_run", "launch_worker", "launch_provider",
        }
        for name, source in sources.items():
            tree = ast.parse(source, filename=name)
            imports = set()
            calls = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.update(alias.name.split(".")[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imports.add(node.module.split(".")[0])
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        calls.add(node.func.id)
                    elif isinstance(node.func, ast.Attribute):
                        calls.add(node.func.attr)
            self.assertFalse(imports & forbidden_import_roots, (name, imports & forbidden_import_roots))
            self.assertFalse(calls & forbidden_calls, (name, calls & forbidden_calls))
        self.assertNotIn("import independent_oracle", sources["projector.py"])
        self.assertNotIn("import projector", sources["independent_oracle.py"])

    # OPEN-L0-T8
    def test_t8_bounded_production_scan_finds_no_consumer_or_authority_path(self):
        roots = [ROOT / "implementations" / "server", ROOT / ".claude" / "skills" / "register-dispatch"]
        needles = (
            "aci_open_l0", "aci.open-l0", "expected-unstamped-row.json",
            "expected-discrepancy-report.json",
        )
        hits = []
        for root in roots:
            for path in root.rglob("*"):
                if path.is_file() and path.suffix in {".py", ".cjs", ".js", ".json", ".md"}:
                    text = path.read_text(encoding="utf-8", errors="replace")
                    if any(needle in text for needle in needles):
                        hits.append(str(path.relative_to(ROOT)))
        self.assertEqual(hits, [])

    # OPEN-L0-T9
    def test_t9_full_runtime_regression_command_is_part_of_the_pinned_readiness(self):
        readiness_path = ROOT / (
            "docs/features/agents-communication-infra/development/invoke-runs/"
            "20260831-resumable-feedback/plan/open-l0-work-pack/"
            "SWU-ACI-OPEN-AUDIT-PROJECTION-L0-001-code-readiness.json"
        )
        readiness = json.loads(readiness_path.read_text(encoding="utf-8"))
        self.assertIn(
            "python -B -m unittest discover -s implementations/tests/runtime -t .",
            readiness["validation_commands"],
        )
        self.assertEqual(readiness["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
