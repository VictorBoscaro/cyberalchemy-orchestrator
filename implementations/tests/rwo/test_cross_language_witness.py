"""Differential structural witness between the Python oracle and Rust kernel.

This intentionally covers only the frozen compiler/reducer/defect/retry corpus.
Raw JSON admission and transport behavior remain separately bounded work.
"""

from __future__ import annotations

import base64
import copy
import hashlib
import json
import os
import subprocess
import unittest
from pathlib import Path

from implementations.rwo.canonical import semantic_digest
from implementations.rwo.contract import admit_canonical_decimal, admit_json
from implementations.rwo.kernel import (
    StructuralDefect,
    compile_work_graph,
    derive_command_intent,
    order_defects,
    reduce_event,
)
from implementations.rwo.retry import classify_retry


REPOSITORY = Path(__file__).resolve().parents[3]
RUST_MANIFEST = REPOSITORY / "implementations/rwo-rust/Cargo.toml"
CONFORMANCE_MANIFEST = REPOSITORY / (
    "docs/features/recursive-work-orchestrator/development/decision-gates/"
    "20260807T173437Z-rwo-language-contract-v2/vectors/CONFORMANCE-MANIFEST.json"
)


def _replace_at(value: dict[str, object], path: list[str | int], replacement: object) -> None:
    target: object = value
    for segment in path[:-1]:
        target = target[segment]  # type: ignore[index]
    target[path[-1]] = replacement  # type: ignore[index]


def _retry_kwargs(value: dict[str, object]) -> dict[str, object]:
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


class CrossLanguageStructuralWitnessTests(unittest.TestCase):
    """Compare live Rust observations with independently calculated Python facts."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest_bytes = CONFORMANCE_MANIFEST.read_bytes()
        cls.manifest = json.loads(cls.manifest_bytes)
        cls.fixtures = cls.manifest["fixtures"]
        cls.vectors = {item["vectorId"]: item for item in cls.manifest["vectors"]}

    def _rust_observations(self) -> dict[str, object]:
        environment = dict(os.environ)
        environment.update(
            {
                "CARGO_NET_OFFLINE": "true",
                "CARGO_TARGET_DIR": "/tmp/rwo-rust-target",
                "PYTHONDONTWRITEBYTECODE": "1",
            }
        )
        completed = subprocess.run(
            [
                "cargo",
                "run",
                "--quiet",
                "--offline",
                "--manifest-path",
                str(RUST_MANIFEST.relative_to(REPOSITORY)),
                "--bin",
                "rwo_fixture_observations",
            ],
            cwd=REPOSITORY,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(
            completed.returncode,
            0,
            f"Rust witness failed:\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
        )
        return json.loads(completed.stdout)

    def _python_observations(self) -> dict[str, object]:
        compiled = compile_work_graph(copy.deepcopy(self.fixtures["explicitComposition"]))
        self.assertEqual(compiled.kind, "Compiled")
        self.assertIsNotNone(compiled.compiled)
        graph = compiled.compiled
        assert graph is not None

        matching_event = copy.deepcopy(self.fixtures["matchingEvent"])
        applied = reduce_event(
            graph, copy.deepcopy(self.fixtures["initialCursor"]), matching_event
        )
        derived = derive_command_intent(graph, matching_event, graph.graph["edges"][0])
        self.assertTrue(derived.admitted, derived.defects)
        self.assertEqual(derived.command, applied.command)
        self.assertEqual(
            derived.command_intent_identity, applied.command_intent_identity
        )
        self.assertEqual(
            derived.command_payload_digest, applied.command_payload_digest
        )
        duplicate = reduce_event(
            graph, copy.deepcopy(self.fixtures["nextCursor"]), matching_event
        )
        divergent_event = copy.deepcopy(matching_event)
        mutation = self.vectors["RED-003"]["typedInput"]["mutation"]["replace"]
        _replace_at(divergent_event, mutation["path"], mutation["value"])
        divergent = reduce_event(
            graph, copy.deepcopy(self.fixtures["nextCursor"]), divergent_event
        )

        defects = []
        for item in self.vectors["DEF-001"]["typedInput"]["discoveryOrder"]:
            path = tuple(
                segment["name"] if segment["kind"] == "field" else segment["index"]
                for segment in item["path"]
            )
            defects.append(
                StructuralDefect(item["phase"], item["code"], path, item["detail_digest"])
            )

        retry: dict[str, object] = {}
        for index in range(1, 12):
            vector = self.vectors[f"RTY-{index:03d}"]
            retry[vector["vectorId"]] = classify_retry(
                **_retry_kwargs(vector["typedInput"])
            ).treatment
        semantic_retry: dict[str, str] = {}
        for case in self.vectors["RTY-012"]["cases"]:
            reference = case["typedInput"]["semanticVectorRef"]
            outcome = "Duplicate" if reference == "RED-002" else "DivergentDuplicate"
            semantic_retry[outcome] = classify_retry(kernel_outcome=outcome).treatment
        retry["RTY-012"] = semantic_retry

        def admission_observation(result: object) -> dict[str, object]:
            payload = getattr(result, "payload_bytes")
            return {
                "admitted": getattr(result, "admitted"),
                "payload_base64": (
                    None
                    if payload is None
                    else base64.b64encode(payload).decode("ascii")
                ),
                "defect_codes": [
                    defect.code for defect in getattr(result, "defects")
                ],
            }

        raw_json: dict[str, list[dict[str, object]]] = {}
        for index in range(1, 14):
            vector_id = f"ADM-{index:03d}"
            raw_json[vector_id] = [
                admission_observation(
                    admit_json(base64.b64decode(case["rawUtf8JsonBase64"]))
                )
                for case in self.vectors[vector_id]["cases"]
            ]
        decimal: dict[str, list[dict[str, object]]] = {}
        for index in range(1, 3):
            vector_id = f"DEC-{index:03d}"
            decimal[vector_id] = [
                admission_observation(
                    admit_canonical_decimal(
                        base64.b64decode(case["rawUtf8JsonBase64"])
                    )
                )
                for case in self.vectors[vector_id]["cases"]
            ]
        ordinary_strings = [
            admission_observation(
                admit_json(base64.b64decode(case["rawUtf8JsonBase64"]))
            )
            for case in self.vectors["DEC-003"]["cases"]
        ]
        digest_tuple = self.manifest["digestTupleFixture"]
        digests: dict[str, str] = {}
        for vector_id in ("DIG-001", "DIG-002"):
            typed = self.vectors[vector_id]["typedInput"]
            digests[vector_id] = semantic_digest(
                digest_tuple["contract_id"],
                digest_tuple["contract_version"],
                digest_tuple["profile_id"],
                digest_tuple["profile_version"],
                digest_tuple["schema_id"],
                digest_tuple["schema_version"],
                typed["valueType"],
                base64.b64decode(typed["payloadBase64"]),
            )
        digests["DIG-003"] = digests["DIG-001"]

        return {
            "schema_version": "rwo.fixture-observations/v1",
            "manifest_sha256": hashlib.sha256(self.manifest_bytes).hexdigest(),
            "compile": {
                "kind": compiled.kind,
                "graph_identity": graph.graph_identity,
                "canonical_payload_base64": base64.b64encode(graph.canonical_bytes).decode(
                    "ascii"
                ),
            },
            "reduce": {
                "applied": {
                    "kind": applied.kind,
                    "cursor": applied.cursor,
                    "command": applied.command,
                    "accepted_event_identity": applied.accepted_event_identity,
                    "event_payload_digest": applied.event_payload_digest,
                    "command_intent_identity": applied.command_intent_identity,
                    "command_payload_digest": applied.command_payload_digest,
                },
                "duplicate": {
                    "kind": duplicate.kind,
                    "cursor": duplicate.cursor,
                },
                "divergent": {
                    "kind": divergent.kind,
                    "defect_codes": [defect.code for defect in divergent.defects],
                    "cursor": divergent.cursor,
                },
            },
            "admission": {
                "unicode_runtime_version": [15, 1, 0, 0],
                "raw_json": raw_json,
                "canonical_decimal": decimal,
                "ordinary_strings": ordinary_strings,
            },
            "digests": digests,
            "defects": {
                "ordered_codes": [defect.code for defect in order_defects(defects)]
            },
            "retry": retry,
        }

    def test_rust_observation_matches_python_structural_oracle(self) -> None:
        self.assertEqual(self._rust_observations(), self._python_observations())


if __name__ == "__main__":
    unittest.main()
