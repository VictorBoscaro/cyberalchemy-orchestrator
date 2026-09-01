"""Verify the accepted RWO source-snapshot bridge for local prototypes.

The vector manifest and its detached review deliberately remain bound to the
pre-repair registry.  The registry itself was later repaired under an accepted
snapshot bridge so that its embedded contract tuple matches the live contract.
This module makes that distinction executable: it proves the bridge path, but
never claims that the immutable manifest directly binds the repaired registry.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping


CONTRACT_ROOT = Path(
    "docs/features/recursive-work-orchestrator/development/decision-gates/"
    "20260807T173437Z-rwo-language-contract-v2"
)
BRIDGE_ROOT = Path(
    "docs/features/recursive-work-orchestrator/development/refinement-runs/"
    "20260809T192552Z-rwo-fdn-source-binding-bridge"
)
CONTRACT_PATH = CONTRACT_ROOT / "RWO-SEMANTIC-CONTRACT-1.0.0.md"
REGISTRY_PATH = CONTRACT_ROOT / "schemas/registry.json"
MANIFEST_PATH = CONTRACT_ROOT / "vectors/CONFORMANCE-MANIFEST.json"
REVIEW_PATH = CONTRACT_ROOT / "vectors/CONFORMANCE-MANIFEST-REVIEW.json"

CONTRACT_SHA256 = "8da8959770733ac4a3f0936f5cb2a8175a0786c909822a141f10670409610740"
BASELINE_REGISTRY_SHA256 = "5c8801a0587fabfbdfbf12686f49b943dac986def111a66af9fff90daf71bf51"
LIVE_REGISTRY_SHA256 = "6dd223bd5b8e16b0db574d140d442f1b924cb7cb305fe47aed4bbafddedd9cdc"
MANIFEST_SHA256 = "5fa9f516c88b4e7e85a1d7b7f751301e31f41493b51dd62bc0f0ea7a901d2b0c"
REVIEW_SHA256 = "170f7cae649a18adcfcf5c8e4155e516782a1453df6a0590269f390d891c49f2"

BRIDGE_ARTIFACTS = {
    BRIDGE_ROOT / "SOURCE-SNAPSHOT.json": "754ee27b61c04a031164e19ddfb31d40e44d51cf268982caaa367993705e768e",
    BRIDGE_ROOT / "OWNER-ACCEPTANCE-RECEIPT.json": "6c2acf92ffce1d285bc6589caaf747256760c3412c759b641524f850b09bdd01",
    BRIDGE_ROOT / "CANONICAL-REPLACEMENT-RECEIPT.json": "445f82e9e008f304454e7ba0e562fc92c115d55905de17d230c276c80fce1b46",
    BRIDGE_ROOT / "POST-REPLACEMENT-VALIDATION.json": "542ac3ebe29e332d9d95c84e33ffbfd4c924f212f92b85adba405ccf4b289aed",
}


class SourceBindingError(AssertionError):
    """Raised when a local prototype source no longer matches its declared bridge."""


@dataclass(frozen=True)
class SourceBindingEvidence:
    """The distinct source identities protected by snapshot-bridge mode."""

    mode: str
    contract_sha256: str
    registry_sha256: str
    manifest_sha256: str
    review_sha256: str


def _repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _document(path: Path) -> Mapping[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _expect(actual: object, expected: object, label: str) -> None:
    if actual != expected:
        raise SourceBindingError(
            f"snapshot-bridge mismatch for {label}: expected {expected!r}, got {actual!r}"
        )


def verify_snapshot_bridge(repository: Path | None = None) -> SourceBindingEvidence:
    """Return evidence for the accepted bridge or fail closed on any drift.

    This is intentionally a verifier, not a migration or acceptance mechanism.
    It preserves the three independent relationships:

    * the immutable manifest and review bind one another and the baseline;
    * the live registry binds the live semantic contract; and
    * owner acceptance and post-replacement evidence authorize only that
      registry repair under ``snapshot-bridge`` mode.
    """

    root = repository or _repository_root()
    contract = root / CONTRACT_PATH
    registry = root / REGISTRY_PATH
    manifest = root / MANIFEST_PATH
    review = root / REVIEW_PATH

    _expect(_digest(contract), CONTRACT_SHA256, "semantic contract")
    _expect(_digest(registry), LIVE_REGISTRY_SHA256, "live repaired registry")
    _expect(_digest(manifest), MANIFEST_SHA256, "immutable conformance manifest")
    _expect(_digest(review), REVIEW_SHA256, "immutable detached review")

    for relative_path, expected in BRIDGE_ARTIFACTS.items():
        _expect(_digest(root / relative_path), expected, str(relative_path))

    snapshot = _document(root / (BRIDGE_ROOT / "SOURCE-SNAPSHOT.json"))
    baseline = snapshot["baseline"]
    candidate = snapshot["registryRepairCandidate"]
    _expect(baseline["contract"]["sha256"], CONTRACT_SHA256, "snapshot contract digest")
    _expect(baseline["registry"]["sha256"], BASELINE_REGISTRY_SHA256, "snapshot baseline registry")
    _expect(candidate["sha256"], LIVE_REGISTRY_SHA256, "snapshot registry candidate")
    _expect(baseline["manifest"]["sha256"], MANIFEST_SHA256, "snapshot manifest")
    _expect(baseline["review"]["sha256"], REVIEW_SHA256, "snapshot review")
    _expect(
        snapshot["relations"]["bridgeRule"],
        "The source snapshot, not the immutable manifest, is the re-bound L0 authority for a successor after exact owner acceptance. A consumer must not infer that the baseline manifest binds the candidate registry.",
        "snapshot bridge rule",
    )

    acceptance = _document(root / (BRIDGE_ROOT / "OWNER-ACCEPTANCE-RECEIPT.json"))
    _expect(acceptance["status"], "accepted", "owner acceptance status")
    _expect(
        acceptance["constraints"]["sourceBindingMode"],
        "snapshot-bridge",
        "owner acceptance mode",
    )
    _expect(
        acceptance["authorizedReplacement"]["baseline"]["sha256"],
        BASELINE_REGISTRY_SHA256,
        "owner acceptance baseline registry",
    )
    _expect(
        acceptance["authorizedReplacement"]["candidate"]["sha256"],
        LIVE_REGISTRY_SHA256,
        "owner acceptance candidate registry",
    )
    _expect(
        acceptance["constraints"]["immutableManifestSha256"],
        MANIFEST_SHA256,
        "owner acceptance immutable manifest",
    )
    _expect(
        acceptance["constraints"]["immutableDetachedReviewSha256"],
        REVIEW_SHA256,
        "owner acceptance immutable review",
    )

    replacement = _document(root / (BRIDGE_ROOT / "CANONICAL-REPLACEMENT-RECEIPT.json"))
    _expect(replacement["status"], "pass", "canonical replacement status")
    _expect(
        replacement["canonicalReplacement"]["candidate"]["sha256"],
        LIVE_REGISTRY_SHA256,
        "canonical replacement candidate registry",
    )
    _expect(
        replacement["canonicalReplacement"]["baseline"]["sha256"],
        BASELINE_REGISTRY_SHA256,
        "canonical replacement baseline registry",
    )

    post_validation = _document(root / (BRIDGE_ROOT / "POST-REPLACEMENT-VALIDATION.json"))
    _expect(post_validation["status"], "pass", "post-replacement validation")
    _expect(post_validation["targetIsCanonical"], True, "post-replacement target flag")
    _expect(post_validation["target"]["sha256"], LIVE_REGISTRY_SHA256, "post-replacement target")

    live_registry = _document(registry)
    _expect(live_registry["contract"]["sha256"], CONTRACT_SHA256, "registry contract digest")
    _expect(live_registry["contract"]["sizeBytes"], contract.stat().st_size, "registry contract size")

    return SourceBindingEvidence(
        mode="snapshot-bridge",
        contract_sha256=CONTRACT_SHA256,
        registry_sha256=LIVE_REGISTRY_SHA256,
        manifest_sha256=MANIFEST_SHA256,
        review_sha256=REVIEW_SHA256,
    )
