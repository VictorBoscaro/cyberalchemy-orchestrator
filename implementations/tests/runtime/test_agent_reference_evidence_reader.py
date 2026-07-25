from __future__ import annotations

import unittest

from implementations.server.runtime.errors import IntegrityError, ValidationError
from implementations.server.runtime.reference_delivery import (
    DELIVERY_EVIDENCE_SCHEMA,
    TARGET_RESOLUTION_SCHEMA,
    verify_reference_bundle_entry,
)
from implementations.server.runtime.service import RuntimeService, RuntimeSettings
from implementations.tests.runtime.test_agent_reference_delivery import (
    ReferenceDeliveryFixture,
)


class AgentReferenceEvidenceReaderTests(ReferenceDeliveryFixture, unittest.TestCase):
    def setUp(self) -> None:
        self.build_fixture()
        self.receipt = self.settle()

    def tearDown(self) -> None:
        self.cleanup_fixture()

    def test_target_and_delivery_wrappers_are_complete_and_restart_stable(self) -> None:
        attempt_id = self.receipt["target"]["target_attempt_id"]
        target = self.runtime.get_agent_reference_target(attempt_id=attempt_id)
        evidence = self.runtime.get_agent_reference_delivery_evidence(
            attempt_id=attempt_id
        )
        self.runtime.verify_agent_reference_wrapper(
            target, schema=TARGET_RESOLUTION_SCHEMA
        )
        self.runtime.verify_agent_reference_wrapper(
            evidence, schema=DELIVERY_EVIDENCE_SCHEMA
        )
        self.assertEqual(target["target"], self.receipt["target"])
        self.assertEqual(
            evidence["delivery"]["recommendation_ids"], ["rec-1"]
        )
        self.assertEqual(
            evidence["accepted_group"]["ordered_event_ids"],
            self.receipt["ordered_event_ids"],
        )
        self.assertEqual(
            evidence["evidence_boundary"],
            {
                "included_in_effective_input": True,
                "access_observed": False,
                "declared_used": False,
                "claim_support": False,
            },
        )

        restarted = RuntimeService(
            RuntimeSettings(
                self.project / "runtime.sqlite3",
                self.project,
                self.ledger,
                local_pilot_serve_enabled=True,
            )
        )
        restarted.open()
        self.assertEqual(
            restarted.get_agent_reference_delivery_evidence(
                attempt_id=attempt_id
            ),
            evidence,
        )

    def test_wrapper_digest_schema_owner_and_extra_fields_fail_closed(self) -> None:
        attempt_id = self.receipt["target"]["target_attempt_id"]
        evidence = self.runtime.get_agent_reference_delivery_evidence(
            attempt_id=attempt_id
        )
        for changed in (
            {**evidence, "wrapper_digest": "sha256:" + "0" * 64},
            {**evidence, "schema": "aci.agent-reference-delivery-evidence/v2"},
            {**evidence, "owner": "other-owner"},
            {**evidence, "unexpected": True},
        ):
            with self.subTest(changed=set(changed) - set(evidence)):
                with self.assertRaises(IntegrityError):
                    self.runtime.verify_agent_reference_wrapper(
                        changed, schema=DELIVERY_EVIDENCE_SCHEMA
                    )
        with self.assertRaises(ValidationError):
            self.runtime.verify_agent_reference_wrapper(
                evidence, schema="unknown@1"
            )

    def test_reference_entry_omission_duplicate_and_digest_drift_fail_closed(self) -> None:
        attempt_id = self.receipt["target"]["target_attempt_id"]
        evidence = self.runtime.get_agent_reference_delivery_evidence(
            attempt_id=attempt_id
        )
        delivery = evidence["delivery"]
        manifest = evidence["effective_input"]
        omitted = {**manifest, "entries": manifest["entries"][:-1]}
        duplicate = {
            **manifest,
            "entries": manifest["entries"] + [manifest["entries"][-1]],
        }
        drifted = {
            **manifest,
            "entries": [
                *manifest["entries"][:-1],
                {**manifest["entries"][-1], "content_hash": "sha256:" + "f" * 64},
            ],
        }
        for candidate in (omitted, duplicate, drifted):
            with self.assertRaises(IntegrityError):
                verify_reference_bundle_entry(delivery, candidate)

    def test_reader_rejects_incomplete_accepted_group(self) -> None:
        attempt_id = self.receipt["target"]["target_attempt_id"]
        with self.runtime.database.write() as conn:
            conn.execute(
                """
                UPDATE command_receipts SET ordered_event_ids_json='[]'
                WHERE command_id=?
                """,
                (self.receipt["command_id"],),
            )
        with self.assertRaises(IntegrityError):
            self.runtime.get_agent_reference_delivery_evidence(
                attempt_id=attempt_id
            )


if __name__ == "__main__":
    unittest.main()
