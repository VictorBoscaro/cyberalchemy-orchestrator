from __future__ import annotations

import unittest

from server.control_center.local_store import LocalControlCenterStore


class LocalStoreTest(unittest.TestCase):
    def setUp(self) -> None:
        self.store = LocalControlCenterStore()

    def draft(self, **updates):
        value = {
            "proposal_id": "proposal-1",
            "expected_draft_revision": 0,
            "target_kind": "skill",
            "target_id": "task-session",
            "base_revision_or_hash": "sha256:base",
            "proposed_patch": [{"op": "replace", "path": "/description", "value": "Clearer"}],
            "effective_values": {"description": {"value": "Clearer", "origin": "proposal"}},
            "schema_version": "1",
        }
        value.update(updates)
        return value

    def test_preference_cas_increments_once_and_retains_conflict(self):
        input_ = {
            "user_scope_id": "user",
            "expected_revision": 0,
            "preference_kind": "layout",
            "value": "compact",
            "schema_version": "1",
        }
        saved = self.store.save_preference(input_, "user")
        self.assertEqual((saved["code"], saved["revision"]), ("saved-local", 1))
        conflict = self.store.save_preference(input_, "user")
        self.assertEqual(conflict["code"], "local-conflict")
        self.assertTrue(conflict["input_retained"])
        self.assertEqual(self.store.load_preferences("user", "1")["revision"], 1)

    def test_draft_save_and_validation_are_preview_only(self):
        saved = self.store.save_proposal(self.draft())
        self.assertEqual((saved["code"], saved["draft_revision"]), ("draft-saved", 1))
        result = self.store.validate_proposal(
            {
                "proposal_id": "proposal-1",
                "draft_revision": 1,
                "validator_id": "phase1-preview",
                "validator_version": "1",
            }
        )
        self.assertEqual(result["code"], "validation-valid")
        self.assertFalse(result["preview"]["authoritative"])
        self.assertEqual(result["authoritative_effects"], [])

    def test_draft_cas_conflict_retains_input(self):
        self.store.save_proposal(self.draft())
        conflict = self.store.save_proposal(self.draft())
        self.assertEqual(conflict["code"], "draft-conflict")
        self.assertTrue(conflict["input_retained"])

    def test_authoritative_paths_are_invalid_preview_not_applied(self):
        saved = self.store.save_proposal(
            self.draft(proposed_patch=[{"op": "add", "path": "/apply", "value": True}])
        )
        result = self.store.validate_proposal(
            {
                "proposal_id": "proposal-1",
                "draft_revision": saved["draft_revision"],
                "validator_id": "phase1-preview",
                "validator_version": "1",
            }
        )
        self.assertEqual(result["code"], "validation-invalid")
        self.assertTrue(result["preview"]["findings"])
        self.assertEqual(result["authoritative_effects"], [])

    def test_invalid_origin_and_forbidden_lifecycle_are_closed(self):
        invalid = self.store.save_proposal(
            self.draft(effective_values={"description": {"value": "x"}})
        )
        self.assertEqual(invalid["code"], "invalid-draft")
        forbidden = self.store.save_proposal(self.draft(lifecycle_state="applying"))
        self.assertEqual(forbidden["code"], "forbidden-draft-state")

    def test_validator_rejects_requested_authoritative_effect(self):
        saved = self.store.save_proposal(self.draft())
        result = self.store.validate_proposal(
            {
                "proposal_id": "proposal-1",
                "draft_revision": saved["draft_revision"],
                "validator_id": "phase1-preview",
                "validator_version": "1",
                "requested_effects": ["reconcile"],
            }
        )
        self.assertEqual(result["code"], "forbidden-validation-effect")
        self.assertEqual(result["authoritative_effects"], [])

    def test_preference_revision_is_scope_wide_across_kinds(self):
        layout = self.store.save_preference(
            {
                "user_scope_id": "user",
                "expected_revision": 0,
                "preference_kind": "layout",
                "value": "compact",
                "schema_version": "1",
            },
            "user",
        )
        filtered = self.store.save_preference(
            {
                "user_scope_id": "user",
                "expected_revision": layout["revision"],
                "preference_kind": "filter",
                "value": {"status": ["open"]},
                "schema_version": "1",
            },
            "user",
        )
        self.assertEqual((filtered["code"], filtered["revision"]), ("saved-local", 2))
        snapshot = self.store.load_preferences("user", "1")
        self.assertEqual(snapshot["revision"], 2)
        self.assertEqual(set(snapshot["values"]), {"layout", "filter"})


if __name__ == "__main__":
    unittest.main()
