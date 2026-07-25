from __future__ import annotations

import json
import unittest
from pathlib import Path

from server.control_center.fixtures import fixture_digest


class FixtureContractTest(unittest.TestCase):
    def test_manifest_digests_and_scale_contracts(self):
        root = (
            Path(__file__).resolve().parents[2]
            / "fixtures"
            / "skill-control-center"
        )
        manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
        loaded = {}
        for row in manifest["fixtures"]:
            fixture = json.loads((root / row["path"]).read_text(encoding="utf-8"))
            self.assertEqual(fixture_digest(fixture), row["sha256"])
            self.assertEqual(fixture["sha256"], row["sha256"])
            self.assertEqual(fixture["fixture_id"], row["fixture_id"])
            loaded[row["fixture_id"]] = fixture
        skill = loaded["FX-SKILL-TOPOLOGY-v1"]
        self.assertEqual(len(skill["nodes"]), 70)
        self.assertEqual(len(skill["edges"]), 262)
        self.assertEqual(
            sum(edge["relation"] == "explicit_path" for edge in skill["edges"]), 15
        )
        self.assertEqual(
            sum(edge["relation"] == "named_reference" for edge in skill["edges"]), 247
        )
        self.assertEqual(len(loaded["FX-DISPATCH-CATALOG-v1"]["rows"]), 700)
        expected_states = {
            "state-loading",
            "state-empty",
            "state-no-match",
            "state-focal-lineage",
            "state-observed",
            "state-stale",
            "state-partial",
            "state-invalid-endpoint",
            "state-truncated",
            "state-draft-dirty",
            "state-draft-saved",
            "state-validating",
            "state-valid",
            "state-invalid",
            "state-save-failed",
            "state-local-conflict",
            "state-read-api-unavailable",
        }
        manifest_cases = {
            case["case_id"]: case["sha256"]
            for row in manifest["fixtures"]
            for case in row["cases"]
        }
        fixture_cases = {
            case["case_id"]: case
            for fixture in loaded.values()
            for case in fixture.get("state_cases", [])
        }
        self.assertEqual(set(manifest_cases), expected_states)
        self.assertEqual(set(fixture_cases), expected_states)
        for case_id, case in fixture_cases.items():
            self.assertEqual(fixture_digest(case), case["sha256"])
            self.assertEqual(manifest_cases[case_id], case["sha256"])

    def test_unavailable_evidence_is_null_not_zero(self):
        root = Path(__file__).resolve().parents[2] / "fixtures" / "skill-control-center"
        fixture = json.loads((root / "evidence-mixed.json").read_text(encoding="utf-8"))
        unavailable = next(
            case for case in fixture["cases"] if case["case_id"] == "unavailable-not-zero"
        )
        self.assertEqual(unavailable["evidence_classes"], ["unknown-or-unavailable"])
        self.assertIsNone(unavailable["logical_invocation_count"])
        self.assertFalse(unavailable["exhaustive"])


if __name__ == "__main__":
    unittest.main()
