from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from implementations.rwo.adapters import InMemoryCommandDeliveryPort
from implementations.rwo.kernel import load_default_registry
from implementations.rwo.runtime import InMemoryRwoPrototype


REPOSITORY = Path(__file__).resolve().parents[3]
MANIFEST_PATH = REPOSITORY / (
    "docs/features/recursive-work-orchestrator/development/decision-gates/"
    "20260807T173437Z-rwo-language-contract-v2/vectors/CONFORMANCE-MANIFEST.json"
)


class InMemoryPrototypeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixtures = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))["fixtures"]

    def make_prototype(self) -> InMemoryRwoPrototype:
        return InMemoryRwoPrototype.from_composition(
            copy.deepcopy(self.fixtures["explicitComposition"]),
            copy.deepcopy(self.fixtures["initialCursor"]),
        )

    def test_end_to_end_local_step_and_ingress_deduplication(self) -> None:
        prototype = self.make_prototype()
        event = copy.deepcopy(self.fixtures["matchingEvent"])
        first = prototype.offer_accepted_event(event)
        self.assertEqual(first.ingress.status, "accepted_in_memory")
        self.assertIsNotNone(first.reduction)
        self.assertEqual(first.reduction.kind, "Applied")
        self.assertEqual(first.reduction.command, self.fixtures["expectedCommand"])
        self.assertEqual(first.delivery.status, "accepted_by_transport")
        self.assertEqual(prototype.cursor, self.fixtures["nextCursor"])

        duplicate = prototype.offer_accepted_event(event)
        self.assertEqual(duplicate.ingress.status, "identical_duplicate")
        self.assertIsNone(duplicate.reduction)
        self.assertIsNone(duplicate.delivery)
        self.assertEqual(prototype.cursor, self.fixtures["nextCursor"])

        conflicting = copy.deepcopy(event)
        conflicting["payload"]["job_id"] = "job-2"
        conflict = prototype.offer_accepted_event(conflicting)
        self.assertEqual(conflict.ingress.status, "conflict")
        self.assertIsNone(conflict.reduction)
        self.assertEqual(prototype.cursor, self.fixtures["nextCursor"])

    def test_in_memory_delivery_preserves_logical_identity_on_redelivery(self) -> None:
        delivery = InMemoryCommandDeliveryPort()
        command = copy.deepcopy(self.fixtures["expectedCommand"])
        logical_id = "sha256:" + "1" * 64
        first = delivery.deliver(command, logical_message_id=logical_id)
        second = delivery.deliver(command, logical_message_id=logical_id)
        self.assertEqual(first.status, "accepted_by_transport")
        self.assertEqual(second.status, "redelivered")
        self.assertNotEqual(
            first.transport_delivery_attempt_id, second.transport_delivery_attempt_id
        )
        altered = copy.deepcopy(command)
        altered["payload"]["job_id"] = "other"
        self.assertEqual(
            delivery.deliver(altered, logical_message_id=logical_id).status,
            "rejected_known",
        )

    def test_replay_is_pure_and_does_not_deliver(self) -> None:
        prototype = self.make_prototype()
        initial = copy.deepcopy(prototype.cursor)
        event = copy.deepcopy(self.fixtures["matchingEvent"])
        outcomes = prototype.replay((event, event))
        self.assertEqual([outcome.kind for outcome in outcomes], ["Applied", "Duplicate"])
        self.assertEqual(prototype.cursor, initial)

    def test_source_binding_drift_is_reported_not_hidden(self) -> None:
        binding = load_default_registry().source_binding
        self.assertEqual(
            binding.valid,
            binding.expected_sha256 == binding.actual_sha256
            and binding.expected_size == binding.actual_size,
        )
        self.assertEqual(len(binding.actual_sha256), 64)
        self.assertGreater(binding.actual_size, 0)


if __name__ == "__main__":
    unittest.main()
