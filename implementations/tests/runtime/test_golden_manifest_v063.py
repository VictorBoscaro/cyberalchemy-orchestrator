from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[3]
FIXTURES = REPO / "docs/features/agents-communication-infra/adrs/fixtures"
CURRENT_MANIFEST = FIXTURES / "SWU-ACI-002-GOLDEN-MANIFEST-v0.6.3.json"


class GoldenManifestV063Tests(unittest.TestCase):
    def test_manifest_preserves_frozen_baseline_and_binds_extension_bytes(self) -> None:
        manifest = json.loads(CURRENT_MANIFEST.read_text(encoding="utf-8"))

        baseline = manifest["frozen_baseline"]
        self.assertEqual(baseline["path"], "SWU-ACI-002-GOLDEN-MANIFEST.json")
        self._assert_binding(baseline)

        fixture_paths = {entry["path"] for entry in manifest["fixtures"]}
        self.assertEqual(
            fixture_paths,
            {
                "golden-opening-input-v0.6.2-disabled.json",
                "golden-opening-input-v0.6.2-enabled.json",
                "golden-opening-v0.6.2-disabled.yaml",
                "golden-opening-v0.6.2-enabled.yaml",
                "golden-opening-input-v0.6.3-disabled.json",
                "golden-opening-input-v0.6.3-enabled.json",
                "golden-opening-v0.6.3-disabled.yaml",
                "golden-opening-v0.6.3-enabled.yaml",
            },
        )
        for entry in manifest["fixtures"]:
            self._assert_binding(entry)

    def _assert_binding(self, entry: dict[str, object]) -> None:
        artifact = FIXTURES / str(entry["path"])
        content = artifact.read_bytes()
        self.assertEqual(len(content), entry["size_bytes"], artifact.name)
        self.assertEqual(
            f"sha256:{hashlib.sha256(content).hexdigest()}",
            entry["sha256"],
            artifact.name,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
