from __future__ import annotations

import base64
import copy
import json
import unittest
from pathlib import Path

from implementations.rwo.kernel import (
    CompiledGraph,
    StructuralDefect,
    compile_work_graph,
    derive_command_intent,
    order_defects,
    reduce_event,
)
from implementations.rwo.retry import classify_retry


REPOSITORY = Path(__file__).resolve().parents[3]
MANIFEST_PATH = REPOSITORY / (
    "docs/features/recursive-work-orchestrator/development/decision-gates/"
    "20260807T173437Z-rwo-language-contract-v2/vectors/CONFORMANCE-MANIFEST.json"
)


def replace_at(value: dict, path: list[str | int], replacement: object) -> None:
    target: object = value
    for segment in path[:-1]:
        target = target[segment]  # type: ignore[index]
    target[path[-1]] = replacement  # type: ignore[index]


def retry_kwargs(value: dict) -> dict:
    names = {
        "kernelOutcome": "kernel_outcome",
        "adapterOutcome": "adapter_outcome",
        "submissionState": "submission_state",
        "commandValidity": "command_validity",
        "attemptBudget": "attempt_budget",
        "budgetOpen": "budget_open",
        "frozenPolicy": "frozen_policy",
        "leaseState": "lease_state",
        "policyAllows": "policy_allows",
        "adapterCapabilities": "adapter_capabilities",
    }
    return {names[key]: item for key, item in value.items() if key in names}


class RwoKernelVectors(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        cls.fixtures = cls.manifest["fixtures"]
        cls.vectors = {item["vectorId"]: item for item in cls.manifest["vectors"]}
        cls.compiled = compile_work_graph(cls.fixtures["explicitComposition"]).compiled
        if cls.compiled is None:
            raise AssertionError("fixture composition did not compile")

    def test_full_semantic_vector_denominator(self) -> None:
        prefixes = {"ADM", "DEC", "NRM", "DIG", "VER", "CMP", "RED", "CMD", "DEF", "RTY", "FIX"}
        applicable = {
            vector_id
            for vector_id in self.vectors
            if vector_id.split("-", 1)[0] in prefixes
        }
        self.assertEqual(len(applicable), 54)
        self.assertEqual(
            {vector_id.split("-", 1)[0] for vector_id in applicable}, prefixes
        )

    def test_compile_vectors(self) -> None:
        vector = self.vectors["CMP-001"]
        first = compile_work_graph(self.fixtures["explicitComposition"])
        second = compile_work_graph(self.fixtures["explicitComposition"])
        self.assertEqual(first.kind, vector["expected"]["outcome"])
        self.assertEqual(first.graph, self.fixtures["compiledWorkGraph"])
        self.assertEqual(first.canonical_bytes, second.canonical_bytes)
        self.assertEqual(first.graph_identity, vector["expected"]["graphIdentity"])
        expected_payload = base64.b64decode(
            self.fixtures["compiledGraphPayload"]["base64"]
        )
        self.assertEqual(first.canonical_bytes, expected_payload)

        unknown = copy.deepcopy(self.fixtures["explicitComposition"])
        unknown["unknown"] = True
        unknown_result = compile_work_graph(unknown)
        self.assertEqual(unknown_result.kind, "Rejected")
        self.assertEqual(
            [defect.code for defect in unknown_result.defects],
            self.vectors["CMP-002"]["expected"]["defectCodes"],
        )

        missing = copy.deepcopy(self.fixtures["explicitComposition"])
        missing["edges"][0]["target_node_id"] = "missing"
        missing_result = compile_work_graph(missing)
        self.assertEqual(missing_result.kind, "Rejected")
        self.assertEqual(
            [defect.code for defect in missing_result.defects],
            self.vectors["CMP-003"]["expected"]["defectCodes"],
        )

    def test_reduce_and_command_vectors(self) -> None:
        initial = copy.deepcopy(self.fixtures["initialCursor"])
        event = copy.deepcopy(self.fixtures["matchingEvent"])
        applied = reduce_event(self.compiled, initial, event)
        expected = self.vectors["RED-001"]["expected"]
        self.assertEqual(applied.kind, expected["outcome"])
        self.assertEqual(applied.cursor, self.fixtures["nextCursor"])
        self.assertEqual(applied.command, self.fixtures["expectedCommand"])
        self.assertEqual(applied.accepted_event_identity, expected["acceptedEventIdentity"])
        self.assertEqual(applied.event_payload_digest, expected["eventPayloadDigest"])
        self.assertEqual(applied.command_intent_identity, expected["commandIntentIdentity"])
        self.assertEqual(applied.command_payload_digest, expected["commandPayloadDigest"])
        self.assertEqual(initial, self.fixtures["initialCursor"])

        duplicate_cursor = copy.deepcopy(self.fixtures["nextCursor"])
        duplicate = reduce_event(self.compiled, duplicate_cursor, event)
        self.assertEqual(duplicate.kind, "Duplicate")
        self.assertEqual(duplicate.cursor, duplicate_cursor)
        self.assertIsNone(duplicate.command)

        divergent_event = copy.deepcopy(event)
        divergent_event["payload"]["job_id"] = "job-2"
        divergent = reduce_event(self.compiled, duplicate_cursor, divergent_event)
        self.assertEqual(divergent.kind, "DivergentDuplicate")
        self.assertEqual(
            [defect.code for defect in divergent.defects],
            self.vectors["RED-003"]["expected"]["defectCodes"],
        )
        self.assertEqual(divergent.cursor, duplicate_cursor)

        no_match_event = copy.deepcopy(self.vectors["RED-004"]["typedInput"]["event"])
        no_match = reduce_event(self.compiled, self.fixtures["initialCursor"], no_match_event)
        self.assertEqual(no_match.kind, "Applied")
        self.assertEqual(len(no_match.cursor["accepted_events"]), 1)
        self.assertEqual(no_match.cursor["satisfied_edge_ids"], [])
        self.assertIsNone(no_match.command)

        for case in self.vectors["RED-005"]["cases"]:
            cursor = copy.deepcopy(self.fixtures["initialCursor"])
            mutation = case["typedInput"]["mutation"]["replace"]
            replace_at(cursor, mutation["path"], mutation["value"])
            result = reduce_event(self.compiled, cursor, event)
            self.assertEqual(result.kind, "Rejected")
            self.assertEqual(
                [defect.code for defect in result.defects],
                case["expected"]["defectCodes"],
            )
            self.assertEqual(result.cursor, cursor)

        malformed_graph = copy.deepcopy(self.fixtures["compiledWorkGraph"])
        malformed_graph["edges"].append(
            self.vectors["RED-006"]["typedInput"]["graphMutation"]["appendEdge"]
        )
        adversarial = CompiledGraph.bind(
            malformed_graph, graph_identity=self.fixtures["graphIdentity"]
        )
        ambiguous = reduce_event(adversarial, self.fixtures["initialCursor"], event)
        self.assertEqual(ambiguous.kind, "Rejected")
        self.assertEqual(
            [defect.code for defect in ambiguous.defects],
            self.vectors["RED-006"]["expected"]["defectCodes"],
        )

        derived = derive_command_intent(self.compiled, event, self.compiled.graph["edges"][0])
        command_expected = self.vectors["CMD-001"]["expected"]
        self.assertTrue(derived.admitted, derived.defects)
        self.assertEqual(derived.command, self.fixtures["expectedCommand"])
        self.assertEqual(derived.command_intent_identity, command_expected["commandIntentIdentity"])
        self.assertEqual(derived.command_payload_digest, command_expected["commandPayloadDigest"])

        corrupt_cursor = copy.deepcopy(self.fixtures["nextCursor"])
        corrupt_cursor["emitted_commands"][0]["command_payload_digest"] = "sha256:" + "0" * 64
        command_conflict = reduce_event(self.compiled, corrupt_cursor, event)
        self.assertEqual(command_conflict.kind, "Rejected")
        self.assertEqual(
            [defect.code for defect in command_conflict.defects],
            self.vectors["CMD-002"]["expected"]["defectCodes"],
        )
        self.assertEqual(command_conflict.cursor, corrupt_cursor)

    def test_structural_defect_order_vector(self) -> None:
        vector = self.vectors["DEF-001"]
        defects = []
        for item in vector["typedInput"]["discoveryOrder"]:
            path = tuple(
                segment["name"] if segment["kind"] == "field" else segment["index"]
                for segment in item["path"]
            )
            defects.append(
                StructuralDefect(
                    item["phase"], item["code"], path, item["detail_digest"]
                )
            )
        self.assertEqual(
            [defect.code for defect in order_defects(defects)],
            vector["expected"]["orderedCodes"],
        )
        with self.assertRaises(ValueError):
            order_defects([defects[0], defects[0]])

    def test_retry_vectors(self) -> None:
        for index in range(1, 12):
            vector = self.vectors[f"RTY-{index:03d}"]
            with self.subTest(vector=vector["vectorId"]):
                decision = classify_retry(**retry_kwargs(vector["typedInput"]))
                expected = vector["expected"]
                self.assertEqual(decision.treatment, expected["treatment"])
                if "identityAndPayloadUnchanged" in expected:
                    self.assertEqual(
                        decision.preserve_identity_and_payload,
                        expected["identityAndPayloadUnchanged"],
                    )
                if "semanticDisposition" in expected:
                    self.assertEqual(
                        decision.semantic_disposition, expected["semanticDisposition"]
                    )
                if "nextPolicyRoute" in expected:
                    self.assertEqual(
                        list(decision.next_policy_routes), expected["nextPolicyRoute"]
                    )
        semantic = self.vectors["RTY-012"]
        for case in semantic["cases"]:
            ref = case["typedInput"]["semanticVectorRef"]
            outcome = "Duplicate" if ref == "RED-002" else "DivergentDuplicate"
            decision = classify_retry(kernel_outcome=outcome)
            self.assertEqual(decision.treatment, case["expected"]["treatment"])


if __name__ == "__main__":
    unittest.main()
