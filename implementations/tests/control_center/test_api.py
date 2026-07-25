from __future__ import annotations

import unittest
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock

from fastapi import FastAPI
from fastapi.testclient import TestClient

from server import config
from server.control_center import ControlCenterService, create_router
from server.control_center.sources import SourceSnapshot


class ControlCenterAPITest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.service = ControlCenterService(
            repo_root=config.REPO_ROOT, repos=[config.REPO_ROOT]
        )
        app = FastAPI()
        app.include_router(create_router(lambda: cls.service))
        cls.client = TestClient(app)

    def params(self, **extra):
        return {"scope_id": "repo", "request_id": "request-1", "schema_version": "1", **extra}

    def test_closed_six_route_inventory(self):
        paths = {
            path
            for path in self.client.get("/openapi.json").json()["paths"]
            if path.startswith("/v1/control-center")
        }
        self.assertEqual(
            paths,
            {
                "/v1/control-center/attention",
                "/v1/control-center/catalog",
                "/v1/control-center/objects/{object_kind}/{object_id}",
                "/v1/control-center/topology/{model}",
                "/v1/control-center/path-query",
                "/v1/control-center/evidence/{object_kind}/{object_id}",
            },
        )
        self.assertFalse(
            any(
                token in path
                for path in paths
                for token in ("apply", "retry", "reconcile", "receipt", "promote")
            )
        )

    def test_catalog_exposes_frozen_skills_and_unknown_usage(self):
        response = self.client.get(
            "/v1/control-center/catalog",
            params=self.params(object_kinds="skill", limit=200),
        )
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["result_state"], "complete")
        live_skill_count = len(list((config.REPO_ROOT / ".agents" / "skills").glob("*/SKILL.md")))
        self.assertEqual(len(body["data"]["matches"]), live_skill_count)
        self.assertTrue(
            all(
                row["evidence_summary"]["logical_invocation_count"] is None
                for row in body["data"]["matches"]
            )
        )
        self.assertTrue(
            all(row["owner"] == "@VictorBoscaro" for row in body["data"]["matches"])
        )

    def test_object_detail_is_typed_and_authority_route_unavailable(self):
        response = self.client.get(
            "/v1/control-center/objects/skill/task-session", params=self.params()
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()["data"]
        self.assertEqual(data["query_state"], "found")
        self.assertEqual(data["authority_route"], "unavailable")

    def test_skill_topology_has_semantic_parity(self):
        response = self.client.get(
            "/v1/control-center/topology/skill-relations",
            params=self.params(
                focus_id="anti-bias-vector-composition",
                direction="outbound",
                depth=1,
                edge_kinds="explicit_path",
            ),
        )
        data = response.json()["data"]
        self.assertEqual(data["query_state"], "success")
        edge_ids = {
            (edge["source_id"], edge["edge_kind"], edge["evidence_id"], edge["target_id"])
            for edge in data["edges"]
        }
        row_ids = {
            tuple(row["identity"])
            for row in data["semantic_rows"]
            if row["row_kind"] == "edge"
        }
        self.assertEqual(edge_ids, row_ids)

    def test_path_query_is_read_only_and_deterministic(self):
        payload = self.params(
            model="skill-relations",
            source_id="anti-bias-vector-composition",
            target_id="check-tension",
            direction="outbound",
            allowed_edge_kinds=["explicit_path"],
            max_depth=2,
            max_paths=10,
        )
        first = self.client.post("/v1/control-center/path-query", json=payload)
        second = self.client.post("/v1/control-center/path-query", json=payload)
        self.assertEqual(first.status_code, 200)
        self.assertEqual(first.json(), second.json())
        self.assertEqual(first.json()["data"]["query_state"], "success")
        self.assertEqual(first.json()["data"]["returned_depth"], 1)

    def test_unconfigured_usage_is_unavailable_never_zero(self):
        response = self.client.get(
            "/v1/control-center/evidence/skill/task-session",
            params=self.params(
                claim_id="times-used",
                window_start_utc="2026-07-01T00:00:00Z",
                window_end_utc="2026-08-01T00:00:00Z",
            ),
        )
        body = response.json()
        self.assertEqual(body["result_state"], "unavailable")
        self.assertEqual(body["completeness"], "unavailable")
        self.assertIsNone(body["data"])
        self.assertIn("unknown", body["warnings"][0].lower())

    def test_partial_or_bad_requests_do_not_claim_absence(self):
        response = self.client.get(
            "/v1/control-center/catalog",
            params=self.params(object_kinds="unknown"),
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["data"]["query_state"], "invalid-request")

    def test_topology_model_responses_keep_the_selected_model(self):
        for model, focus, edge_kind in (
            ("skill-relations", "task-session", "explicit_path"),
            (
                "dispatch-lineage",
                "cyberalchemy-orchestrator:missing",
                "parent_dispatch_id",
            ),
        ):
            body = self.client.get(
                f"/v1/control-center/topology/{model}",
                params=self.params(focus_id=focus, edge_kinds=edge_kind),
            ).json()
            self.assertEqual(body["data"]["model"], model)

    def test_catalog_cursor_is_bound_and_does_not_restart(self):
        first = self.client.get(
            "/v1/control-center/catalog",
            params=self.params(object_kinds="skill", limit=5),
        )
        self.assertEqual(first.status_code, 200)
        first_data = first.json()["data"]
        self.assertIsNotNone(first_data["next_cursor"])
        second = self.client.get(
            "/v1/control-center/catalog",
            params=self.params(
                object_kinds="skill",
                limit=5,
                cursor=first_data["next_cursor"],
            ),
        )
        self.assertEqual(second.status_code, 200)
        first_ids = {row["object_id"] for row in first_data["matches"]}
        second_ids = {row["object_id"] for row in second.json()["data"]["matches"]}
        self.assertFalse(first_ids & second_ids)
        invalid = self.client.get(
            "/v1/control-center/catalog",
            params=self.params(object_kinds="skill", cursor="not-a-cursor"),
        )
        self.assertEqual(invalid.status_code, 409)
        self.assertEqual(invalid.json()["data"]["query_state"], "invalid-cursor")

    def test_primitive_parse_error_uses_response_envelope(self):
        response = self.client.get(
            "/v1/control-center/catalog",
            params=self.params(object_kinds="skill", limit="abc"),
        )
        self.assertEqual(response.status_code, 400)
        body = response.json()
        self.assertEqual(body["result_state"], "complete")
        self.assertEqual(body["data"]["query_state"], "invalid-request")
        self.assertEqual(body["data"]["field_errors"], ["limit"])
        malformed = self.client.post(
            "/v1/control-center/path-query",
            content="{",
            headers={"content-type": "application/json"},
        )
        self.assertEqual(malformed.status_code, 400)
        self.assertEqual(malformed.json()["data"]["query_state"], "invalid-request")

    def test_node_limit_always_retains_focus(self):
        body = self.client.get(
            "/v1/control-center/topology/skill-relations",
            params=self.params(
                focus_id="anti-bias-vector-composition",
                direction="both",
                depth=1,
                node_limit=1,
                edge_kinds="explicit_path",
            ),
        ).json()
        self.assertEqual(
            [node["id"] for node in body["data"]["nodes"]],
            ["anti-bias-vector-composition"],
        )
        self.assertEqual(body["data"]["query_state"], "truncated")

    def test_intra_dispatch_uses_composite_node_and_edge_identities(self):
        with tempfile.TemporaryDirectory() as folder:
            repo = Path(folder)
            ledger = repo / "telemetry" / "agents" / "subagents-dispatch.yaml"
            ledger.parent.mkdir(parents=True)
            row = {
                "dispatch_id": "d1",
                "schema_version": "0.6.1",
                "dispatch_type": "research",
                "goal": "fixture",
                "groups": [
                    {"group_id": "probe", "role": "investigate", "agents": []},
                    {"group_id": "join", "role": "synthesize", "agents": []},
                ],
                "connections": [{"from": "probe", "to": "join", "type": "sequential"}],
            }
            text = "dispatches:\n" + "\n".join(
                (
                    ("  - " if index == 0 else "    ")
                    + key
                    + ": "
                    + json.dumps(value)
                )
                for index, (key, value) in enumerate(row.items())
            )
            ledger.write_text(text + "\n", encoding="utf-8")
            service = ControlCenterService(repo_root=config.REPO_ROOT, repos=[repo])
            app = FastAPI()
            app.include_router(create_router(lambda: service))
            client = TestClient(app)
            body = client.get(
                "/v1/control-center/topology/intra-dispatch",
                params=self.params(
                    dispatch_id="d1",
                    focus_id="probe",
                    edge_kinds="sequential",
                    direction="outbound",
                ),
            ).json()["data"]
            prefix = f"{repo.name}:d1:"
            self.assertTrue(all(node["id"].startswith(prefix) for node in body["nodes"]))
            self.assertTrue(all(edge["source_id"].startswith(prefix) for edge in body["edges"]))
            path = client.post(
                "/v1/control-center/path-query",
                json=self.params(
                    model="intra-dispatch",
                    dispatch_id="d1",
                    source_id="probe",
                    target_id="join",
                    direction="outbound",
                    allowed_edge_kinds=["sequential"],
                    max_depth=2,
                    max_paths=3,
                ),
            ).json()["data"]
            self.assertEqual(path["query_state"], "success")
            self.assertTrue(all(node.startswith(prefix) for node in path["paths"][0]["node_ids"]))

    def test_catalog_reduces_partiality_across_selected_skill_source(self):
        partial = SourceSnapshot(
            snapshot_id="partial-skills",
            nodes=[],
            edges=[],
            source_facts=[{"source_id": "skills", "ingestion_state": "accepted"}],
            completeness="partial",
        )
        service = ControlCenterService(
            repo_root=config.REPO_ROOT, repos=[config.REPO_ROOT]
        )
        service.skills = Mock()
        service.skills.read.return_value = partial
        body = service.catalog(
            self.params(object_kinds=["skill"], query="absent", limit=20)
        )
        self.assertEqual(body["result_state"], "partial")
        self.assertEqual(body["completeness"], "partial")
        self.assertEqual(body["data"]["query_state"], "success")
        self.assertFalse(body["data"]["no_match"])

    def test_catalog_unavailable_has_no_data_or_query_state(self):
        unavailable = SourceSnapshot(
            snapshot_id="unavailable-skills",
            nodes=[],
            edges=[],
            source_facts=[{"source_id": "skills", "ingestion_state": "failed"}],
            completeness="unavailable",
        )
        service = ControlCenterService(
            repo_root=config.REPO_ROOT, repos=[config.REPO_ROOT]
        )
        service.skills = Mock()
        service.skills.read.return_value = unavailable
        body = service.catalog(
            self.params(object_kinds=["skill"], query="absent", limit=20)
        )
        self.assertEqual(body["result_state"], "unavailable")
        self.assertEqual(body["completeness"], "unavailable")
        self.assertIsNone(body["data"])


if __name__ == "__main__":
    unittest.main()
