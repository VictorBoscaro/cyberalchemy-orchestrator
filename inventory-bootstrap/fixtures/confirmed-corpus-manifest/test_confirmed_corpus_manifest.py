from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import confirmed_corpus_manifest as subject


ROOT = Path(__file__).resolve().parents[3]
MANIFEST_PATH = (
    "internal-tools/composition-lab/orchestration/milestone-1-strategy/"
    "d1-readiness/runtime-blocker/inventory-bootstrap/runs/test-run/"
    "confirmed-corpus-manifest.json"
)
GOLDEN_ROWS = [
    ("internal-tools/composition-lab/README.md", "1d2ef9cae7b41028e0a53bf9ec1efc3a3970385c75f2943f2a175a6a3266e806"),
    ("internal-tools/composition-lab/research/milestone-1/01-repository-inventory/research-initial-definitions.md", "2183ce096aa33224ef94cf00f56aa1c42e69ae2dc630cde4ecddae7eaf098932"),
    ("telemetry/agents/subagents-dispatch.yaml", "e28aad64545131ac684731213eefa38b865f4807f439578950514eb3f9b9062c"),
    (".claude/skills/domainspec-subagents-strategy/SKILL.md", "335987a8684f4672d644054ad3def4ef107d616a689edd84fe30e9652e73eb91"),
    (".claude/skills/research/SKILL.md", "56ce56d0b8ac779455ee6f76b999f9c84e7bce0a3af14791b575f17b5ee6f4a9"),
    (".claude/skills/review/SKILL.md", "60dbcb97707949aa7fe102479dbcd712e491bb833362f54b285a536365abd4be"),
    (".claude/skills/robot-talks/SKILL.md", "a9dfd079ad9351c4bdb4b50d06b8755f31dda7d216cdc9774780e35af6805a39"),
    (".codex/dispatch-proposals/2026-08-06-irreducible-research-team-design.json", "53c630b51db9c7224eb317b93c6d553921f2b3cc6771dec3b2af8cb02b382426"),
    (".codex/dispatch-proposals/2026-08-06-irreducible-research-team-design-close.json", "9d3792ab905525ffde03f9c5da587052b5a692f1536d5d692247535f930aaecb"),
    (".codex/workflow-inputs/2026-07-25-work-context-technical-detail-research/abramsky-manifest.json", "0040566b149d49e135d96dd363d3a3959de8091def79c339569183725d1dbb82"),
    (".codex/workflow-inputs/2026-07-25-work-context-technical-detail-research/rittel-manifest.json", "ea9ecf2414d45bdc3b79d1a6959025f273c1e8b0ef14de8dc396b89136a9c418"),
    ("plans/governed-agent-work-infrastructure/essays/robot-talks/2026-08-12-work-overview-composition/dialogue.md", "491482947fcf2064c8d8078125e51162f0b73ecf1af431225c205316eada0672"),
    ("plans/governed-agent-work-infrastructure/essays/robot-talks/2026-08-12-work-overview-composition/findings.md", "be10623815ecbd8b5ac48d8505cb8aef93b13188f1fa3e52e43b5258c6d83cf5"),
    ("plans/governed-agent-work-infrastructure/essays/robot-talks/2026-08-12-work-overview-composition/reports/01-reader-journey.md", "d7e7a35bd37293a0c2b55763575e1051b2721915ffa5e1ed0df2d70198528a54"),
    ("plans/governed-agent-work-infrastructure/essays/robot-talks/2026-08-12-work-overview-composition/reports/02-system-composition.md", "ab1b5e57f38b2c362f9eee65cf27cb7ba61be34130ecc0dd841a6272aa346d8d"),
    ("plans/governed-agent-work-infrastructure/essays/robot-talks/2026-08-12-work-overview-composition/reports/03-product-fidelity.md", "046df6f3509e7b209fd156c45c04f33bea1fc41615ca3c97b5aa90ffb4690250"),
    ("docs/temps/operational-knowledge-language/robot-talks/2026-08-11-editorial-next-step/dialogue.md", "b6ebe1092e2c58250796d52aed91168c431bd5cc014bb3126c0a1ca9752743ee"),
    ("docs/temps/operational-knowledge-language/robot-talks/2026-08-11-editorial-next-step/findings.md", "b8bffbf658a1414b35fdeb133e99c7b422c540863c430bd2ffeb146dddf76b8a"),
    ("docs/features/agent-provenance-telemetry/reviews/2026-07-22-system-tags-and-lens-review.md", "5cadf61c8b19096229fa8b022a54de77ce2514417df748d6a45487f89b6949a7"),
    ("docs/features/agent-provenance-telemetry/probes/APT-P007-emergent-lens.md", "d3d77c7a55d1a4bb38d689434e9c25f656cd10f5e4eb90a99a866e881f57e4ce"),
    ("docs/features/agent-provenance-telemetry/probes/lenses/README.md", "dd6a05eef436f97fbf412855de766350de99c380d41cb363b357314c7337763f"),
    ("docs/features/agent-provenance-telemetry/probes/lenses/agent-pool-scientist-tags@1.json", "3cd34692e30b06708e7f790c0bd83d009f969d02b651447105b44f4ba0116e0f"),
    ("projects/domainspec-v2/README.md", "ca5cfbc0a467e3f14e459236d373db4c046f428930c0fae7571246bfe0aeefff"),
    ("projects/domainspec-v2/research/TWO-LANE-DISCIPLINE.md", "cb09d2412e53288ae891ad6d1f03ff5d56c10808824bf0d7e025fc233cd93557"),
    ("projects/domainspec-v2/research/domainspec-v2-research-towers.dispatch.json", "83206a57f4ed8d05a1c623ede6db17ae058e74fcfdc184150d20f2f7096147fd"),
    ("projects/domainspec-v2/research/target-state/2026-07-02-comprehension-narrative-model/lens-narrative.md", "8b58ef34e0ce95ee5dc76757a963bc3512f53fc97fadc6e460608d00bb23f11c"),
    ("projects/domainspec-v2/research/target-state/2026-07-02-comprehension-narrative-model/lens-example.md", "d0885fe8899d245dcee081974d4551e9797f332b33afcfb399b031e3852ac20b"),
    ("projects/domainspec-v2/research/target-state/2026-07-02-comprehension-narrative-model/lens-distillation.md", "c96a7366c8bf67d263def4ec1358feb08b55aa6acb5ded10535557f8a109eec5"),
    ("projects/domainspec-v2/research/target-state/2026-07-02-comprehension-narrative-model/findings.md", "774c37b64ae35c9536ebb0fdc2442b052a578187f663f2ff39bece335639e3f4"),
    ("projects/domainspec-v2/research/2026-07-01-composability-edges-taxonomy-synthesis.md", "bf2a5a45f7214e36eda2048251315571a6d8d27be7a1e59c1c8f0ce23963fc0d"),
    ("projects/domainspec-v2/research/typed-artifacts-precedent/findings.md", "597bdf17b876b2d4ab68b91e6c748cdb849214cd36cec011d3e83b75dc59606f"),
    ("projects/domainspec-v2/research/spec-ontology-unification/DESIGN.md", "e5410e893314d0c000d291e02a527b4535e5f689f9862ab0b1259e1d78138432"),
    ("projects/domainspec-v2/development/ds-d1-improvement-plan/WORK-PACK.md", "c70bca7310ac0e3e06046f88a978e85edb82b6ba8fbe4d40f29f3f8526029d81"),
    ("projects/domainspec-v2/impl/spec/meta-types/ui/component.schema.yml", "46540796103bac845fc78aee3deceb8fe905a85968b76f7edb7d987efc8deca0"),
    ("projects/domainspec-v2/definitions/relationships/relationships.yml", "7757884f599bb18707f105add8b9de92fb2ea58d78e216d3aa228b0ad25ea013"),
]
GOLDEN_CONTROLS = [
    ("C1", "file/source partition only"),
    ("C2", "nominally different instructions seeking equivalent judgment"),
    ("C3", "isolated `lens` language in single-agent prose"),
    ("C4", "merely concatenated returns"),
    ("C5", "unexecuted proposal"),
    ("C6", "close without output demonstrating relations"),
    ("C7", "duplicate proposal/manifest/ledger/report representations"),
    ("C8", "prescribed mechanism without linked instance"),
]


class ConfirmedCorpusManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = subject.materialize(ROOT, MANIFEST_PATH)

    def test_materialization_is_canonical_and_deterministic(self) -> None:
        first = subject.canonical_json(self.manifest)
        second = subject.canonical_json(subject.materialize(ROOT, MANIFEST_PATH))
        self.assertEqual(first, second)
        self.assertEqual(self.manifest["repository_revision"], subject.EXPECTED_REVISION)
        self.assertEqual(len(self.manifest["sources"]), 35)
        self.assertEqual(len(self.manifest["controls"]), 8)

    def test_materialization_matches_independent_literal_golden(self) -> None:
        rows = [(row["path"], row["sha256"]) for row in self.manifest["sources"]]
        controls = [(control["id"], control["description"]) for control in self.manifest["controls"]]
        self.assertEqual(rows, GOLDEN_ROWS)
        self.assertEqual(controls, GOLDEN_CONTROLS)

    def test_exact_manifest_verifies(self) -> None:
        subject.verify(copy.deepcopy(self.manifest), ROOT, ROOT / MANIFEST_PATH)

    def test_omitted_source_fails(self) -> None:
        changed = copy.deepcopy(self.manifest)
        changed["sources"].pop()
        with self.assertRaisesRegex(subject.ManifestError, "source-cardinality"):
            subject.verify(changed, ROOT, ROOT / MANIFEST_PATH)

    def test_extra_source_fails(self) -> None:
        changed = copy.deepcopy(self.manifest)
        changed["sources"].append(copy.deepcopy(changed["sources"][-1]))
        with self.assertRaisesRegex(subject.ManifestError, "source-cardinality"):
            subject.verify(changed, ROOT, ROOT / MANIFEST_PATH)

    def test_reordered_sources_fail(self) -> None:
        changed = copy.deepcopy(self.manifest)
        changed["sources"][0], changed["sources"][1] = changed["sources"][1], changed["sources"][0]
        with self.assertRaisesRegex(subject.ManifestError, "source-order"):
            subject.verify(changed, ROOT, ROOT / MANIFEST_PATH)

    def test_semantically_changed_source_fails(self) -> None:
        changed = copy.deepcopy(self.manifest)
        changed["sources"][0]["selector"] = "heading:# Composition Lab"
        with self.assertRaisesRegex(subject.ManifestError, "order-or-selector"):
            subject.verify(changed, ROOT, ROOT / MANIFEST_PATH)

    def test_reordered_controls_fail(self) -> None:
        changed = copy.deepcopy(self.manifest)
        changed["controls"][0], changed["controls"][1] = changed["controls"][1], changed["controls"][0]
        with self.assertRaisesRegex(subject.ManifestError, "control-order"):
            subject.verify(changed, ROOT, ROOT / MANIFEST_PATH)

    def test_semantically_changed_control_fails_equivalence(self) -> None:
        changed = copy.deepcopy(self.manifest)
        changed["controls"][0]["description"] += " changed"
        with self.assertRaisesRegex(subject.ManifestError, "MANIFEST_DIVERGENCE"):
            subject.verify(changed, ROOT, ROOT / MANIFEST_PATH)

    def test_extra_field_fails_closed(self) -> None:
        changed = copy.deepcopy(self.manifest)
        changed["unexpected"] = True
        with self.assertRaisesRegex(subject.ManifestError, "manifest-shape"):
            subject.verify(changed, ROOT, ROOT / MANIFEST_PATH)

    def test_external_row_reordering_is_detected(self) -> None:
        table = subject.parse_frozen_table(
            (ROOT / subject.SEMANTIC_AUTHORITY).read_text(encoding="utf-8")
        )
        external = subject.parse_external_rows(
            (ROOT / subject.EXTERNAL_ROW_SOURCE).read_text(encoding="utf-8")
        )
        external[0], external[1] = external[1], external[0]
        normalized_table = [{"path": row["path"], "sha256": row["sha256"]} for row in table]
        self.assertNotEqual(normalized_table, external)

    def test_manifest_path_outside_repository_fails(self) -> None:
        outside = Path(tempfile.gettempdir()) / "confirmed-corpus-manifest.json"
        with self.assertRaisesRegex(subject.ManifestError, "outside-repository"):
            subject.normalize_manifest_path(ROOT, str(outside))

    def test_manifest_at_wrong_physical_path_fails(self) -> None:
        wrong = ROOT / "inventory-bootstrap/fixtures/confirmed-corpus-manifest/wrong.json"
        with self.assertRaisesRegex(subject.ManifestError, "MANIFEST_PATH_DIVERGENCE"):
            subject.verify(copy.deepcopy(self.manifest), ROOT, wrong)

    def test_inventory_projection_is_deterministic_and_equivalent(self) -> None:
        projection = subject.project_inventory_manifest(self.manifest, ROOT / MANIFEST_PATH, ROOT)
        second = subject.project_inventory_manifest(self.manifest, ROOT / MANIFEST_PATH, ROOT)
        self.assertEqual(subject.canonical_json(projection), subject.canonical_json(second))
        self.assertEqual(projection["denominator"]["cell_count"], 280)
        subject.verify_inventory_projection(self.manifest, ROOT / MANIFEST_PATH, projection, ROOT)

    def test_inventory_projection_omission_fails(self) -> None:
        projection = subject.project_inventory_manifest(self.manifest, ROOT / MANIFEST_PATH, ROOT)
        projection["sources"].pop()
        with self.assertRaisesRegex(subject.ManifestError, "projection-sources"):
            subject.verify_inventory_projection(self.manifest, ROOT / MANIFEST_PATH, projection, ROOT)

    def test_inventory_projection_extra_fails(self) -> None:
        projection = subject.project_inventory_manifest(self.manifest, ROOT / MANIFEST_PATH, ROOT)
        projection["unexpected"] = True
        with self.assertRaisesRegex(subject.ManifestError, "projection-shape"):
            subject.verify_inventory_projection(self.manifest, ROOT / MANIFEST_PATH, projection, ROOT)

    def test_inventory_projection_reordering_fails(self) -> None:
        projection = subject.project_inventory_manifest(self.manifest, ROOT / MANIFEST_PATH, ROOT)
        projection["sources"][0], projection["sources"][1] = projection["sources"][1], projection["sources"][0]
        with self.assertRaisesRegex(subject.ManifestError, "PROJECTION_DIVERGENCE"):
            subject.verify_inventory_projection(self.manifest, ROOT / MANIFEST_PATH, projection, ROOT)

    def test_inventory_projection_semantic_change_fails(self) -> None:
        projection = subject.project_inventory_manifest(self.manifest, ROOT / MANIFEST_PATH, ROOT)
        projection["controls"][0]["description"] += " changed"
        with self.assertRaisesRegex(subject.ManifestError, "PROJECTION_DIVERGENCE"):
            subject.verify_inventory_projection(self.manifest, ROOT / MANIFEST_PATH, projection, ROOT)


if __name__ == "__main__":
    unittest.main()
