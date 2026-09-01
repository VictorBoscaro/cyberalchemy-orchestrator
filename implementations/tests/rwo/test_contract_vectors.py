from __future__ import annotations

import ast
import base64
import copy
import hashlib
import json
import unittest
from pathlib import Path

from implementations.rwo.canonical import (
    DuplicateSemanticIdentity,
    canonical_payload_bytes,
    normalize_semantic_collection,
    semantic_digest,
)
from implementations.rwo.contract import (
    VersionRegistry,
    VersionTuple,
    admit_canonical_decimal,
    admit_json,
    admit_version_tuple,
)
from implementations.rwo.source_binding import (
    CONTRACT_SHA256,
    MANIFEST_SHA256,
    REVIEW_SHA256,
    verify_snapshot_bridge,
)


REPOSITORY = Path(__file__).resolve().parents[3]
CONTRACT_ROOT = REPOSITORY / (
    "docs/features/recursive-work-orchestrator/development/decision-gates/"
    "20260807T173437Z-rwo-language-contract-v2"
)
MANIFEST_PATH = CONTRACT_ROOT / "vectors/CONFORMANCE-MANIFEST.json"
REVIEW_PATH = CONTRACT_ROOT / "vectors/CONFORMANCE-MANIFEST-REVIEW.json"
REGISTRY_PATH = CONTRACT_ROOT / "schemas/registry.json"
CONTRACT_PATH = CONTRACT_ROOT / "RWO-SEMANTIC-CONTRACT-1.0.0.md"
POST_VALIDATION_PATH = REPOSITORY / (
    "docs/features/recursive-work-orchestrator/development/refinement-runs/"
    "20260807T173437Z-rwo-contract-kernel-refresh/refresh-runs/"
    "20260807T214631Z-rwo-contract-successor-repair-candidate/"
    "canonical-post-validation.json"
)
IMMUTABLE_HASHES = {
    CONTRACT_PATH: CONTRACT_SHA256,
    MANIFEST_PATH: MANIFEST_SHA256,
    REVIEW_PATH: REVIEW_SHA256,
    POST_VALIDATION_PATH: "98ae9aa2c3e7a0289e465a2c1c2b4d15223ed92234549cf728ec630aa5600bd7",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class RwoLanguageProfileVectors(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source_binding = verify_snapshot_bridge(REPOSITORY)
        cls.manifest_bytes = MANIFEST_PATH.read_bytes()
        cls.review_bytes = REVIEW_PATH.read_bytes()
        cls.manifest = json.loads(cls.manifest_bytes)
        cls.review = json.loads(cls.review_bytes)
        cls.registry = VersionRegistry.from_document(json.loads(REGISTRY_PATH.read_text()))
        cls.vectors = {item["vectorId"]: item for item in cls.manifest["vectors"]}
        for path, expected in IMMUTABLE_HASHES.items():
            if digest(path) != expected:
                raise AssertionError(f"immutable source drift: {path}")

    @classmethod
    def tearDownClass(cls) -> None:
        if verify_snapshot_bridge(REPOSITORY) != cls.source_binding:
            raise AssertionError("test mutated snapshot-bridge source evidence")
        for path, expected in IMMUTABLE_HASHES.items():
            if digest(path) != expected:
                raise AssertionError(f"test mutated immutable source: {path}")

    def test_applicable_vector_denominator(self) -> None:
        prefixes = {"ADM", "DEC", "NRM", "DIG", "VER", "FIX"}
        applicable = {
            vector_id
            for vector_id in self.vectors
            if vector_id.split("-", 1)[0] in prefixes
        }
        expected = {
            *(f"ADM-{index:03d}" for index in range(1, 14)),
            *(f"DEC-{index:03d}" for index in range(1, 4)),
            *(f"NRM-{index:03d}" for index in range(1, 4)),
            *(f"DIG-{index:03d}" for index in range(1, 4)),
            *(f"VER-{index:03d}" for index in range(1, 3)),
            *(f"FIX-{index:03d}" for index in range(1, 7)),
        }
        self.assertEqual(applicable, expected)

    def test_admission_vectors(self) -> None:
        for vector_id in [f"ADM-{index:03d}" for index in range(1, 14)]:
            vector = self.vectors[vector_id]
            with self.subTest(vector=vector_id):
                for case in vector["cases"]:
                    raw = base64.b64decode(case["rawUtf8JsonBase64"])
                    result = admit_json(raw)
                    expected = case["expected"]
                    if expected["outcome"] == "Admitted":
                        self.assertTrue(result.admitted, result.defects)
                        self.assertEqual(
                            base64.b64encode(result.payload_bytes).decode(),
                            expected["payloadBase64"],
                        )
                        if "payloadSha256" in expected:
                            self.assertEqual(
                                hashlib.sha256(result.payload_bytes).hexdigest(),
                                expected["payloadSha256"],
                            )
                        if "payloadSizeBytes" in expected:
                            self.assertEqual(len(result.payload_bytes), expected["payloadSizeBytes"])
                        if "firstKey" in expected:
                            pairs = json.loads(
                                result.payload_bytes,
                                object_pairs_hook=lambda values: values,
                            )
                            self.assertEqual(ord(pairs[0][0]), 0x10000)
                    else:
                        self.assertFalse(result.admitted)
                        self.assertEqual(
                            [defect.code for defect in result.defects],
                            expected["defectCodes"],
                        )

    def test_decimal_vectors(self) -> None:
        for vector_id in ("DEC-001", "DEC-002"):
            vector = self.vectors[vector_id]
            for case in vector["cases"]:
                with self.subTest(vector=vector_id, raw=case["rawUtf8JsonBase64"]):
                    result = admit_canonical_decimal(
                        base64.b64decode(case["rawUtf8JsonBase64"])
                    )
                    expected = case["expected"]
                    self.assertEqual(result.admitted, expected["outcome"] == "Admitted")
                    if not result.admitted:
                        self.assertEqual(
                            [defect.code for defect in result.defects],
                            expected["defectCodes"],
                        )

        ordinary = self.vectors["DEC-003"]["cases"][0]
        result = admit_json(base64.b64decode(ordinary["rawUtf8JsonBase64"]))
        self.assertTrue(result.admitted)
        self.assertEqual(result.value, ordinary["expected"]["value"])

    def test_normalization_vectors(self) -> None:
        tie_break = self.vectors["NRM-001"]
        normalized = normalize_semantic_collection(
            tie_break["typedInput"]["elements"],
            tie_break["typedInput"]["declaration"]["primaryKeyPaths"],
        )
        self.assertEqual(normalized, tie_break["expected"]["elements"])

        duplicate = self.vectors["NRM-002"]
        with self.assertRaises(DuplicateSemanticIdentity):
            normalize_semantic_collection(
                duplicate["typedInput"]["elements"],
                duplicate["typedInput"]["declaration"]["primaryKeyPaths"],
            )

        ordered = self.vectors["NRM-003"]
        payloads = [
            base64.b64encode(canonical_payload_bytes(value)).decode()
            for value in ordered["typedInput"]["orderedCases"]
        ]
        self.assertEqual(payloads, ordered["expected"]["payloadBase64Cases"])
        self.assertNotEqual(*payloads)

    def test_typed_digest_vectors(self) -> None:
        tuple_fixture = self.manifest["digestTupleFixture"]
        observed: dict[str, str] = {}
        for vector_id in ("DIG-001", "DIG-002"):
            vector = self.vectors[vector_id]
            typed = vector["typedInput"]
            observed[vector_id] = semantic_digest(
                tuple_fixture["contract_id"],
                tuple_fixture["contract_version"],
                tuple_fixture["profile_id"],
                tuple_fixture["profile_version"],
                tuple_fixture["schema_id"],
                tuple_fixture["schema_version"],
                typed["valueType"],
                base64.b64decode(typed["payloadBase64"]),
            )
            self.assertEqual(observed[vector_id], vector["expected"]["semanticDigest"])
        self.assertNotEqual(observed["DIG-001"], observed["DIG-002"])
        self.assertEqual(
            observed["DIG-001"],
            self.vectors["DIG-003"]["expected"]["semanticDigest"],
        )

    def test_version_tuple_vectors(self) -> None:
        accepted = self.vectors["VER-002"]["typedInput"]
        accepted_tuple = VersionTuple(**accepted)
        self.assertEqual(admit_version_tuple(accepted_tuple, self.registry), ())

        for case in self.vectors["VER-001"]["cases"]:
            changed = dict(accepted)
            changed.update(case["typedInput"])
            defects = admit_version_tuple(VersionTuple(**changed), self.registry)
            self.assertEqual([item.code for item in defects], ["VERSION_TUPLE_UNSUPPORTED"])

    def test_closed_schema_admission(self) -> None:
        payload_schema = next(
            item["schema"]
            for item in json.loads(REGISTRY_PATH.read_text())["inlinePayloadSchemas"]
            if item["schemaId"] == "FixtureEventPayload"
        )
        accepted = admit_json(b'{"job_id":"job-1"}', schema=payload_schema)
        self.assertTrue(accepted.admitted, accepted.defects)
        unknown = admit_json(
            b'{"job_id":"job-1","extra":true}', schema=payload_schema
        )
        self.assertEqual([item.code for item in unknown.defects], ["UNKNOWN_FIELD"])
        missing = admit_json(b"{}", schema=payload_schema)
        self.assertEqual([item.code for item in missing.defects], ["REQUIRED_FIELD_MISSING"])

    def test_repeatability_and_input_immutability(self) -> None:
        raw = b' \n {"z":[2,1],"a":"value"}\t '
        before = bytes(raw)
        first = admit_json(raw)
        second = admit_json(raw)
        self.assertTrue(first.admitted, first.defects)
        self.assertEqual(first, second)
        self.assertEqual(first.payload_bytes, b'{"a":"value","z":[2,1]}')
        self.assertEqual(raw, before)

        invalid_utf8 = admit_json(b'"\xff"')
        self.assertEqual([item.code for item in invalid_utf8.defects], ["INVALID_UTF8"])
        non_json_whitespace = admit_json(b"0\xc2\xa0")
        self.assertEqual(
            [item.code for item in non_json_whitespace.defects], ["TRAILING_TOKEN"]
        )

    def test_unicode_15_1_assignment_delta_is_not_host_version_dependent(self) -> None:
        # The contract pins Unicode 15.1 while this CPython exposes Unicode
        # 15.0. The local 15.1 assignment delta makes newly assigned scalars
        # admissible without changing immutable contract inputs.
        for codepoint in (0x2FFC, 0x31EF, 0x2EBF0, 0x2EE5D):
            with self.subTest(codepoint=hex(codepoint)):
                raw = json.dumps(chr(codepoint), ensure_ascii=False).encode("utf-8")
                self.assertTrue(admit_json(raw).admitted)
        unassigned = json.dumps(chr(0x2EE5E), ensure_ascii=False).encode("utf-8")
        self.assertEqual(
            [item.code for item in admit_json(unassigned).defects],
            ["UNICODE_UNASSIGNED"],
        )

    def test_fixture_governance_vectors_read_only(self) -> None:
        self.assertEqual(
            hashlib.sha256(self.manifest_bytes).hexdigest(),
            self.review["manifest"]["sha256"],
        )
        self.assertEqual(len(self.manifest_bytes), self.review["manifest"]["sizeBytes"])

        changed_manifest = self.manifest_bytes + b" "
        self.assertNotEqual(
            hashlib.sha256(changed_manifest).digest(),
            hashlib.sha256(self.manifest_bytes).digest(),
        )
        changed_review = self.review_bytes + b" "
        self.assertNotEqual(
            hashlib.sha256(changed_review).digest(),
            hashlib.sha256(self.review_bytes).digest(),
        )

        mutated = copy.deepcopy(self.manifest)
        digest_vector = next(
            item for item in mutated["vectors"] if item["vectorId"] == "DIG-001"
        )
        digest_vector["expected"]["semanticDigest"] = "sha256:" + "0" * 64
        mutated_bytes = json.dumps(
            mutated, sort_keys=True, separators=(",", ":")
        ).encode()
        self.assertNotEqual(hashlib.sha256(mutated_bytes).hexdigest(), self.review["manifest"]["sha256"])

        fixture_vectors = {key: self.vectors[key] for key in [f"FIX-{i:03d}" for i in range(1, 7)]}
        self.assertEqual(fixture_vectors["FIX-001"]["expected"]["writes"], [])
        self.assertEqual(fixture_vectors["FIX-005"]["expected"]["admission"], "block")
        self.assertEqual(self.manifest["status"], fixture_vectors["FIX-006"]["expected"]["status"])

    def test_implementation_import_boundary(self) -> None:
        banned = {
            "adapter",
            "are",
            "compiler",
            "go",
            "grpc",
            "queue",
            "reducer",
            "redis",
            "requests",
            "retry",
            "rust",
            "socket",
            "storage",
            "subprocess",
        }
        for name in ("contract.py", "canonical.py"):
            path = REPOSITORY / "implementations/rwo" / name
            tree = ast.parse(path.read_text())
            imports: set[str] = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.update(alias.name.split(".")[0].lower() for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imports.add(node.module.split(".")[0].lower())
            self.assertFalse(imports & banned, f"{name}: {imports & banned}")


if __name__ == "__main__":
    unittest.main()
