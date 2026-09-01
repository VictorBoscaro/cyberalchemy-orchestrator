from __future__ import annotations

import ast
import json
import re
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[3]
MANIFEST = Path(__file__).with_name("aci-test-traceability.json")
REQUIRED_BOUNDED_IDS = {
    "T-ACI-R3",
    "T-ACI-R5",
    "T-ACI-R6",
    "T-ACI-R7",
    "T-ACI-R8",
    "T-ACI-R15",
    "T-ACI-R16",
    "T-ACI-R20",
    "T-ACI-C1",
    "T-ACI-C2",
    "T-ACI-C4",
    "T-ACI-ETA2",
    "T-ACI-R22",
    "T-ACI-AUTH1",
    "T-ACI-AUTH2",
    "T-ACI-AUTH3",
    "T-ACI-AUTH4",
    "T-ACI-AUTH5",
    "T-ACI-AUTH6",
    "T-ACI-AUTH7",
    "T-ACI-AUTH8",
    "T-ACI-CONT1",
    "T-ACI-CONT9",
    "T-ACI-ARD1",
    "T-ACI-ARD2",
    "T-ACI-ARD3",
    "T-ACI-ARD4",
    "T-ACI-ARD5",
    "T-ACI-PEER1",
    "T-ACI-PEER2",
    "T-ACI-PEER3",
    "T-ACI-PEER4",
    "T-ACI-PEER5",
    "T-ACI-PEER6",
    "T-ACI-PEER7",
    "T-ACI-PC1",
    "T-ACI-PC2",
    "T-ACI-PC3",
    "T-ACI-PC4",
    "T-ACI-PC5",
    "T-ACI-PC6",
    "T-ACI-PC7",
    "T-ACI-PC8",
    "T-ACI-PC9",
    "T-ACI-PC10",
    "T-ACI-PC11",
    "T-ACI-PC12",
    "T-ACI-S1",
    "T-ACI-S2",
}


def _test_methods(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    selectors: set[str] = set()
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        for child in node.body:
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) and child.name.startswith(
                "test_"
            ):
                selectors.add(f"{node.name}::{child.name}")
    return selectors


class AciTestTraceabilityTests(unittest.TestCase):
    def test_bounded_manifest_references_real_spec_ids_and_test_selectors(self) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["feature"], "agents-communication-infra")
        self.assertEqual(manifest["coverage_claim"], "bounded")

        spec_path = REPO / manifest["test_spec"]
        spec_ids = set(
            re.findall(
                r"^#{3,4} (T-(?:ACI|CVR)-[A-Z0-9]+)\s",
                spec_path.read_text(encoding="utf-8"),
                re.M,
            )
        )
        entries = manifest["entries"]
        mapped_ids = {entry["test_spec_id"] for entry in entries}
        self.assertEqual(mapped_ids, REQUIRED_BOUNDED_IDS)
        self.assertEqual(len(entries), len(mapped_ids), "duplicate test-spec mapping")

        methods_by_path: dict[Path, set[str]] = {}
        for entry in entries:
            self.assertEqual(entry["coverage_level"], "bounded")
            self.assertIn(entry["test_spec_id"], spec_ids)
            self.assertTrue(entry["selectors"])
            for selector in entry["selectors"]:
                relative_path, class_name, method_name = selector.split("::")
                path = REPO / relative_path
                self.assertTrue(path.is_file(), selector)
                methods = methods_by_path.setdefault(path, _test_methods(path))
                self.assertIn(f"{class_name}::{method_name}", methods, selector)


if __name__ == "__main__":
    unittest.main()
