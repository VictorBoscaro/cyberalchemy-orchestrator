from __future__ import annotations

import json
import hashlib
import tempfile
import unittest
from pathlib import Path

from implementations.server.runtime.agent_roles import (
    AgentRoleError,
    load_accepted_role_registry,
    load_host_role_routing,
)


REPO = Path(__file__).resolve().parents[3]


class AgentRoleRegistryTests(unittest.TestCase):
    def test_v1_is_exactly_pinned_eight_roles(self) -> None:
        registry = load_accepted_role_registry(REPO)
        self.assertEqual(
            registry.roles,
            frozenset({"explorer", "synthesizer", "skeptic", "writer", "auditor", "planner", "coder", "other"}),
        )
        self.assertEqual(registry.ref["digest"], "sha256:39b378fa3a10cb64c2488af9b7c96f89e409aa699b2e22885f83a755ac33f4aa")
        self.assertEqual(registry.require("other"), "other")
        with self.assertRaises(AgentRoleError) as caught:
            registry.require("others")
        self.assertEqual(caught.exception.code, "DG_ROLE_UNKNOWN")

    def test_same_version_substitution_and_duplicate_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            contracts = root / "implementations/contracts"
            contracts.mkdir(parents=True)
            for name in ("agent-role-registry.v1.json", "agent-role-registry-authority.v1.json"):
                (contracts / name).write_bytes((REPO / "implementations/contracts" / name).read_bytes())
            value = json.loads((contracts / "agent-role-registry.v1.json").read_text(encoding="utf-8"))
            value["roles"][0]["purpose"] += " substituted"
            (contracts / "agent-role-registry.v1.json").write_text(json.dumps(value), encoding="utf-8")
            with self.assertRaises(AgentRoleError) as caught:
                load_accepted_role_registry(root)
            self.assertEqual(caught.exception.code, "DG_ROLE_REGISTRY_SUBSTITUTED")

    def test_host_routing_is_registry_closed(self) -> None:
        routing = load_host_role_routing(REPO)
        roles = load_accepted_role_registry(REPO).roles
        self.assertIn(routing["fallback_role"], roles)
        self.assertTrue(all(route["role"] in roles for route in routing["routes"]))

    def test_future_role_revision_is_data_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            contracts = root / "implementations/contracts"
            contracts.mkdir(parents=True)
            value = json.loads(
                (REPO / "implementations/contracts/agent-role-registry.v1.json").read_text(encoding="utf-8")
            )
            value["version"] = "2"
            value["roles"].append({"role_id": "facilitator", "enabled": True, "purpose": "Facilitate a future configured workflow."})
            raw = json.dumps(value, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
            (contracts / "agent-role-registry.v1.json").write_bytes(raw)
            ref = {"name": value["name"], "version": "2", "digest": "sha256:" + hashlib.sha256(raw).hexdigest()}
            authority = {"schema": "aci.role-registry-authority@1", "accepted": [ref]}
            (contracts / "agent-role-registry-authority.v1.json").write_text(json.dumps(authority), encoding="utf-8")
            self.assertEqual(load_accepted_role_registry(root).require("facilitator"), "facilitator")


if __name__ == "__main__":
    unittest.main()
