from __future__ import annotations

import unittest
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from server import config
from server.control_center import (
    ControlCenterService,
    FixtureEvidenceProvider,
    create_router,
)
from server.control_center.evidence import normalize_evidence


class EvidenceProviderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        fixture = (
            Path(__file__).resolve().parents[2]
            / "fixtures"
            / "skill-control-center"
            / "evidence-mixed.json"
        )
        provider = FixtureEvidenceProvider(
            fixture,
            {
                "skill:task-session": "complete-positive-fresh",
                "skill:context-builder": "complete-zero-stale",
                "skill:research": "partial-lower-bound",
                "skill:x-ray": "unavailable-not-zero",
            },
        )
        cls.service = ControlCenterService(
            repo_root=config.REPO_ROOT,
            repos=[config.REPO_ROOT],
            evidence_provider=provider,
        )
        app = FastAPI()
        app.include_router(create_router(lambda: cls.service))
        cls.client = TestClient(app)

    def params(self, **values):
        return {
            "scope_id": "repo",
            "request_id": "evidence-test",
            "schema_version": "1",
            **values,
        }

    def evidence(self, skill: str):
        return self.client.get(
            f"/v1/control-center/evidence/skill/{skill}",
            params=self.params(
                claim_id="times-used",
                window_start_utc="2026-07-01T00:00:00Z",
                window_end_utc="2026-08-01T00:00:00Z",
            ),
        ).json()

    def test_route_exposes_positive_complete_and_complete_zero_stale(self):
        positive = self.evidence("task-session")
        self.assertEqual(positive["result_state"], "complete")
        self.assertEqual(positive["data"]["logical_invocation_count"], 3)
        self.assertEqual(positive["data"]["freshness"], "fresh")
        zero = self.evidence("context-builder")
        self.assertEqual(zero["result_state"], "complete")
        self.assertEqual(zero["data"]["logical_invocation_count"], 0)
        self.assertEqual(zero["data"]["freshness"], "stale")
        self.assertTrue(zero["data"]["complete_window_coverage"])

    def test_partial_is_lower_bound_and_unavailable_is_null_never_zero(self):
        partial = self.evidence("research")
        self.assertEqual(partial["result_state"], "partial")
        self.assertEqual(partial["data"]["logical_invocation_count"], 2)
        self.assertFalse(partial["data"]["exhaustive"])
        unavailable = self.evidence("x-ray")
        self.assertEqual(unavailable["result_state"], "unavailable")
        self.assertIsNone(unavailable["data"])

    def test_catalog_uses_same_provider_summaries(self):
        body = self.client.get(
            "/v1/control-center/catalog",
            params=self.params(object_kinds="skill", limit=200),
        ).json()
        rows = {row["object_id"]: row["evidence_summary"] for row in body["data"]["matches"]}
        self.assertEqual(rows["task-session"]["logical_invocation_count"], 3)
        self.assertEqual(rows["context-builder"]["logical_invocation_count"], 0)
        self.assertEqual(rows["research"]["completeness"], "partial")
        self.assertIsNone(rows["x-ray"]["logical_invocation_count"])

    def test_object_detail_overlay_uses_same_partial_answer(self):
        body = self.client.get(
            "/v1/control-center/objects/skill/research",
            params=self.params(
                window_start_utc="2026-07-01T00:00:00Z",
                window_end_utc="2026-08-01T00:00:00Z",
            ),
        ).json()
        evidence = body["data"]["evidence"]
        self.assertEqual(evidence["logical_invocation_count"], 2)
        self.assertEqual(evidence["completeness"], "partial")
        self.assertFalse(evidence["exhaustive"])

    def test_invalid_zero_fails_closed(self):
        value = normalize_evidence(
            {
                "evidence_classes": ["observed"],
                "completeness": "partial",
                "freshness": "fresh",
                "logical_invocation_count": 0,
                "exhaustive": True,
            }
        )
        self.assertEqual(value["completeness"], "unavailable")
        self.assertIsNone(value["logical_invocation_count"])


if __name__ == "__main__":
    unittest.main()
