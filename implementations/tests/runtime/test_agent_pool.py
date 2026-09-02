from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

from implementations.server.runtime.agent_pool import (
    AgentPoolError,
    load_agent_pool,
    migrate_legacy_pool,
    normalize_pool_documents,
    parse_pool_stream,
)
from implementations.server.runtime.agent_roles import load_accepted_role_registry


REPO = Path(__file__).resolve().parents[3]
SPEC = REPO / "docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/followups/SPEC-ACI-AGENT-IDENTITY-ROLE-001"


class AgentPoolTests(unittest.TestCase):
    def test_real_pool_is_canonical_v07_and_unique(self) -> None:
        pool = load_agent_pool(REPO)
        self.assertEqual(pool.value["version"], "0.7.0")
        self.assertEqual(len(pool.value["agents"]), 414)
        self.assertEqual(len(pool.by_name), 414)
        raw = (REPO / "telemetry/agents/agent-pool.yaml").read_text(encoding="utf-8")
        self.assertEqual(raw.count("\n  - agent_name:"), 414)
        self.assertNotIn("\n  - name:", raw)
        self.assertNotIn("\n  - agent-name:", raw)

    def test_tracked_v06_migrates_exactly_to_current_value(self) -> None:
        raw = subprocess.check_output(["git", "show", "HEAD:telemetry/agents/agent-pool.yaml"], cwd=REPO)
        authority = json.loads((SPEC / "fixtures/pool-migration-authority.json").read_text(encoding="utf-8"))
        registry = load_accepted_role_registry(REPO)
        expected = migrate_legacy_pool(raw, authority, registry)
        actual = parse_pool_stream((REPO / "telemetry/agents/agent-pool.yaml").read_bytes())
        self.assertEqual(actual, expected)

    def test_name_spellings_duplicate_keys_and_unknown_roles_fail_typed(self) -> None:
        registry = load_accepted_role_registry(REPO)
        base = parse_pool_stream((REPO / "telemetry/agents/agent-pool.yaml").read_bytes())
        for key, code in (("name", "DG_POOL_LEGACY_NAME_FORBIDDEN"), ("agent-name", "DG_POOL_NAME_KEY_INVALID")):
            hostile = json.loads(json.dumps(base))
            row = hostile[1]["scientists"][0]
            row[key] = row.pop("agent_name")
            with self.subTest(key=key), self.assertRaises(AgentPoolError) as caught:
                normalize_pool_documents(hostile, registry)
            self.assertEqual(caught.exception.code, code)
        with self.assertRaises(AgentPoolError) as caught:
            parse_pool_stream("profile: one\nprofile: two\n---\nscientists: []\n")
        self.assertEqual(caught.exception.code, "DG_DUPLICATE_YAML_KEY")
        hostile = json.loads(json.dumps(base)); hostile[1]["scientists"][0]["role_fit"] = ["others"]
        with self.assertRaises(Exception) as caught:
            normalize_pool_documents(hostile, registry)
        self.assertEqual(caught.exception.code, "DG_ROLE_UNKNOWN")


if __name__ == "__main__":
    unittest.main()
