from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from implementations.server.runtime.host_dispatch_hook import HostDispatchHook
from implementations.server.runtime.host_ingestion_hook import HostIngestionHook
from implementations.server.runtime.service import RuntimeService, RuntimeSettings

REPO = Path(__file__).resolve().parents[3]
GOLDEN_LEDGER = (
    REPO
    / "docs/features/agents-communication-infra/adrs/fixtures/"
    "golden-opening-v0.6.1.yaml"
)
POLICY = (
    REPO
    / "docs/features/agent-provenance-telemetry/integration/stage-f/"
    "host-hook-policy.json"
)
DISPATCH_ID = "2026-07-23-local-probe-fixture"


class HostIngestionHookTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        destination = (
            self.root
            / "docs/features/agent-provenance-telemetry/integration/stage-f/"
            "host-hook-policy.json"
        )
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(POLICY, destination)
        dispatch_registry_relative = (
            "implementations/contracts/dispatch-type-registry.v2.json"
        )
        dispatch_registry = json.loads(
            (REPO / dispatch_registry_relative).read_text(encoding="utf-8")
        )
        dispatch_paths = [
            dispatch_registry_relative,
            "implementations/contracts/dispatch-ledger-row.v0.7.0.schema.json",
            "implementations/contracts/agent-role-registry.v1.json",
            "implementations/contracts/agent-role-registry-authority.v1.json",
            "implementations/contracts/agent-role-host-routing.v1.json",
        ]
        dispatch_paths.extend(
            entry["capability_path"]
            for entry in dispatch_registry["types"]
            if entry["capability_path"] is not None
        )
        for relative in dispatch_paths:
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / relative, target)
        policy = json.loads(destination.read_text(encoding="utf-8"))
        self.database = self.root / policy["database"]
        self.ledger = self.root / policy["ledger"]
        self.ledger.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(GOLDEN_LEDGER, self.ledger)
        self.service = RuntimeService(
            RuntimeSettings(self.database, REPO, self.ledger)
        )
        self.service.open()
        self.service.register_profiles()
        self.session_id = self.service.ensure_session(
            origin_digest="sha256:" + "8" * 64,
            name="host input lineage",
            actor_ref="host:test",
            actor_authentication_ref="auth:test",
            actor_authentication_digest="sha256:" + "a" * 64,
        )["session"]["session_id"]
        self.service.link_session_dispatch(
            session_id=self.session_id,
            dispatch_id=DISPATCH_ID,
            actor_ref="host:test",
            authorization_policy_ref="policy:test@1",
            authorization_policy_digest="sha256:" + "b" * 64,
            authorization_evidence_ref="evidence:test",
            authorization_evidence_digest="sha256:" + "c" * 64,
        )
        self.service.record_orchestration_dispatch_opened(
            session_id=self.session_id,
            dispatch_id=DISPATCH_ID,
            actor_ref="host:test",
            authorization_evidence_ref="evidence:test",
            authorization_evidence_digest="sha256:" + "c" * 64,
        )
        self.now = lambda: datetime(
            2026, 7, 24, 17, 0, tzinfo=timezone.utc
        )
        self.dispatch_hook = HostDispatchHook(
            root=self.root, host="codex", now=self.now
        )
        agent_event = {
            "session_id": "host-session",
            "tool_use_id": "agent-tool",
        }
        state_path = self.dispatch_hook._state_path(agent_event)
        self.dispatch_hook._write_state(
            state_path,
            {
                "schema": "aci-host-dispatch-state/v1",
                "host": "codex",
                "host_session_id": "host-session",
                "tool_use_id": "agent-tool",
                "tool_input_digest": "sha256:" + "d" * 64,
                "dispatch_id": DISPATCH_ID,
                "session_id": self.session_id,
                "role": "explorer",
                "agent_type": "explorer",
                "agent_id": "agent-1",
                "status": "opened",
                "record": {},
            },
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def hook(self) -> HostIngestionHook:
        hook = HostIngestionHook(root=self.root, host="codex", now=self.now)
        hook.dispatch_hook._runtime_bridge = lambda: (self.service, None)
        return hook

    def event(self, *, tool_name: str, tool_input: dict, tool_use_id: str):
        return {
            "session_id": "host-session",
            "agent_id": "agent-1",
            "tool_use_id": tool_use_id,
            "tool_name": tool_name,
            "tool_input": tool_input,
            "tool_response": {"status": "ok"},
            "cwd": str(self.root),
            "hook_event_name": "PostToolUse",
        }

    def test_exact_read_and_opaque_shell_are_persisted(self) -> None:
        source = self.root / "input.txt"
        source.write_text("source bytes", encoding="utf-8")
        exact = self.hook().post_tool_use(
            self.event(
                tool_name="Read",
                tool_input={"file_path": str(source)},
                tool_use_id="read-1",
            )
        )
        self.assertEqual(exact["ingestion"]["coverage"], "exact")
        opaque = self.hook().post_tool_use(
            self.event(
                tool_name="shell_command",
                tool_input={"command": "Get-Content input.txt"},
                tool_use_id="shell-1",
            )
        )
        self.assertEqual(opaque["ingestion"]["coverage"], "opaque")
        lineage = self.service.get_dispatch_operational_lineage(DISPATCH_ID)
        self.assertEqual(
            [row["source_kind"] for row in lineage["ingestions"]],
            ["repository_file", "shell_opaque"],
        )
        self.assertEqual(
            lineage["ingestions"][0]["repo_relative_path"], "input.txt"
        )

    def test_search_records_metadata_without_claiming_file_reads(self) -> None:
        receipt = self.hook().post_tool_use(
            self.event(
                tool_name="Grep",
                tool_input={"pattern": "Scout", "path": "docs"},
                tool_use_id="grep-1",
            )
        )
        self.assertEqual(receipt["ingestion"]["coverage"], "metadata_only")
        lineage = self.service.get_dispatch_operational_lineage(DISPATCH_ID)
        self.assertIsNone(lineage["ingestions"][0]["artifact_id"])


if __name__ == "__main__":
    unittest.main()
