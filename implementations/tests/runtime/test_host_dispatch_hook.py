from __future__ import annotations

import base64
import json
import re
import shutil
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

from implementations.server.runtime.canonical import canonical_digest
from implementations.server.runtime.errors import GateBlockedError
from implementations.server.runtime.dispatch_workflow import compile_bound_launch_plan
from implementations.server.runtime.host_dispatch_hook import HostDispatchHook, run

REPO = Path(__file__).resolve().parents[3]


class HostDispatchHookTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self._stage_project()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _stage_project(self) -> None:
        manifest_path = (
            REPO
            / "docs/features/agent-provenance-telemetry/integration/stage-e/"
            "source-manifest.json"
        )
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        required = list(manifest["files"]) + [
            "docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json",
            "docs/features/agent-provenance-telemetry/integration/stage-b/execution-receipt.md",
            "docs/features/agent-provenance-telemetry/integration/stage-c/local-pilot-enablement.md",
            "docs/features/agent-provenance-telemetry/integration/stage-f/host-hook-policy.json",
            "docs/features/agents-communication-infra/reviews/2026-07-23-stage-a-freeze/profile-registry-manifest.json",
        ]
        registry = json.loads(
            (
                REPO
                / "docs/features/agents-communication-infra/reviews/"
                "2026-07-23-stage-a-freeze/profile-registry-manifest.json"
            ).read_text(encoding="utf-8")
        )
        required.extend(
            profile["authoritative_profile_path"]
            for profile in registry["profiles"]
        )
        required.extend(
            "docs/features/agents-communication-infra/"
            + profile["local_review_mirror"]["path"]
            for profile in registry["profiles"]
        )
        for relative in dict.fromkeys(required):
            source = REPO / relative
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
        ledger = self.root / "telemetry/agents/subagents-dispatch.yaml"
        ledger.parent.mkdir(parents=True, exist_ok=True)
        ledger.write_text("# hook test\ndispatches:\n", encoding="utf-8")

    @staticmethod
    def event(
        root: Path,
        *,
        host: str,
        name: str = "PreToolUse",
        tool_use_id: str = "tool-1",
        response=None,
    ) -> dict:
        event = {
            "session_id": f"{host}-session-1",
            "cwd": str(root),
            "hook_event_name": name,
            "model": f"{host}-test-model",
        }
        if name in {"PreToolUse", "PostToolUse", "PostToolUseFailure"}:
            event.update(
                {
                    "tool_name": "Agent",
                    "tool_use_id": tool_use_id,
                    "tool_input": {
                        "task_name": "security_review",
                        "description": "Review security",
                        "message": "Review the bridge for security failures.",
                    },
                }
            )
        if response is not None:
            event["tool_response"] = response
        return event

    def hook(self, host: str) -> HostDispatchHook:
        return HostDispatchHook(
            root=self.root,
            host=host,
            now=lambda: datetime(2026, 7, 24, 20, 0, tzinfo=timezone.utc),
        )

    @staticmethod
    def bound_message(*, prompt: str, turn_ordinal: int = 0) -> str:
        envelope = {
            "schema": "aci-host-workflow-binding/v1",
            "dispatch_id": "2026-07-25-parent-research",
            "group_id": "kernel",
            "seat_index": 0,
            "turn_ordinal": turn_ordinal,
            "attempt_id": f"attempt-{turn_ordinal}",
            "prompt_template_path": None,
            "prompt_template_digest": canonical_digest(prompt),
            "workflow_manifest_path": "workflow/manifest.json",
            "workflow_manifest_digest": canonical_digest({"slots": []}),
        }
        encoded = base64.urlsafe_b64encode(
            json.dumps(envelope).encode("utf-8")
        ).decode("ascii").rstrip("=")
        return f"ACI-WORKFLOW-BINDING-V1:{encoded}\n{prompt}"

    def test_bound_launch_uses_parent_binding_without_opening_yaml_dispatch(self) -> None:
        hook = self.hook("claude")
        prompt = "Investigate the kernel invariants."
        event = self.event(self.root, host="claude")
        event["tool_input"]["message"] = self.bound_message(prompt=prompt)
        runtime = MagicMock()
        runtime.bind_host_workflow_turn.return_value = {
            "status": "launch-authorized",
            "dispatch_id": "2026-07-25-parent-research",
            "session_id": "session-parent",
            "binding_id": "hwb-kernel",
            "group_id": "kernel",
            "seat_index": 0,
            "turn_ordinal": 0,
            "attempt_id": "attempt-0",
            "bound_event_id": "evt-bound",
            "workflow_manifest_artifact_id": "art-manifest",
        }
        runtime.complete_host_workflow_turn.return_value = {
            "state": "resolved",
            "terminal_event_id": "evt-terminal",
        }
        completed_event = dict(event)
        completed_event["hook_event_name"] = "PostToolUse"
        completed_event["tool_response"] = {"result": "complete"}
        with patch.object(hook, "_runtime_bridge", return_value=(runtime, object())):
            opened = hook.pre_tool_use(event)
            closed = hook.post_tool_use(completed_event)
        self.assertEqual(opened["binding_id"], "hwb-kernel")
        self.assertEqual(closed["binding_state"], "resolved")
        runtime.bind_host_workflow_turn.assert_called_once()
        runtime.complete_host_workflow_turn.assert_called_once()
        ledger = (
            self.root / "telemetry/agents/subagents-dispatch.yaml"
        ).read_text(encoding="utf-8")
        self.assertNotIn("2026-07-25-parent-research", ledger)

    def test_compiled_bound_launch_opens_and_closes_one_parent_dispatch(self) -> None:
        hook = self.hook("codex")
        dispatch_id = "2026-08-03-integrated-bound-review"
        prompt = "Review the integrated governed dispatch path."
        opening = {
            "dispatch_id": dispatch_id,
            "schema_version": "0.6.3",
            "dispatch_type": "review",
            "goal": "Prove one parent-bound host dispatch.",
            "context": "The compiled launch must bind one reviewer to one parent row.",
            "max_loops": 1,
            "final_approver": "parent",
            "anti_bias_mode": "disabled",
            "output_mode": "inline",
            "groups": [
                {
                    "group_id": "reviewers",
                    "agents": [
                        {
                            "role": "auditor",
                            "model": "gpt-test",
                            "token_budget": 1000,
                            "initial_prompt": prompt,
                        }
                    ],
                }
            ],
        }
        opened = hook.open_parent_dispatch(
            record=opening,
            session_name="integrated-bound-review",
            origin_ref="codex:test",
            nonce="integrated-open",
        )
        compiled = compile_bound_launch_plan(
            repo_root=self.root,
            record=opening,
            capability_ref="review",
            output_dir=Path(".codex/workflow-inputs/integrated-bound-review"),
        )
        event = self.event(self.root, host="codex")
        event["tool_name"] = "collaboration.spawn_agent"
        event["tool_input"] = compiled["launches"][0]["spawn_arguments"]
        bound = hook.handle(event)
        self.assertEqual(bound["dispatch_id"], dispatch_id)
        self.assertEqual(bound["role"], "bound-seat")
        hook.handle(
            self.event(
                self.root,
                host="codex",
                name="PostToolUse",
                response={"agent_id": "agent-integrated", "status": "running"},
            )
            | {
                "tool_name": "collaboration.spawn_agent",
                "tool_input": compiled["launches"][0]["spawn_arguments"],
            }
        )
        hook.subagent_stop(
            {
                "session_id": "codex-session-1",
                "cwd": str(self.root),
                "hook_event_name": "SubagentStop",
                "agent_id": "agent-integrated",
                "agent_type": "reviewer",
            }
        )
        closing = {
            "close_of": dispatch_id,
            "exit_reason": "resolved",
            "agents_spawned": {
                "total": 1,
                "tree": {"auditor": 1, "helpers": 0},
                "loops_used": 1,
            },
        }
        closed = hook.close_parent_dispatch(
            record=closing,
            session_id=opened["session_id"],
            nonce="integrated-close",
        )
        self.assertEqual(closed["status"], "closed")
        ledger = (
            self.root / "telemetry/agents/subagents-dispatch.yaml"
        ).read_text(encoding="utf-8")
        self.assertEqual(ledger.count(f'  - dispatch_id: "{dispatch_id}"'), 1)
        self.assertEqual(ledger.count(f'  - close_of: "{dispatch_id}"'), 1)

    def test_unbound_followup_is_denied(self) -> None:
        hook = self.hook("codex")
        event = self.event(self.root, host="codex")
        event["tool_name"] = "followup_task"
        event["tool_input"] = {
            "target": "agent-1",
            "message": "Continue without a binding.",
        }
        with self.assertRaisesRegex(
            GateBlockedError, "governed workflow binding envelope"
        ):
            hook.pre_tool_use(event)

    def test_codex_namespaced_spawn_tool_is_normalized(self) -> None:
        hook = self.hook("codex")
        event = self.event(self.root, host="codex")
        event["tool_name"] = "collaboration.spawn_agent"

        opened = hook.handle(event)

        self.assertEqual(opened["status"], "opened")
        self.assertTrue(opened["dispatch_id"].startswith("2026-07-24-auto-codex"))

    def test_codex_flattened_spawn_tool_is_normalized(self) -> None:
        hook = self.hook("codex")
        event = self.event(self.root, host="codex")
        event["tool_name"] = "collaborationspawn_agent"

        opened = hook.handle(event)

        self.assertEqual(opened["status"], "opened")
        self.assertTrue(opened["dispatch_id"].startswith("2026-07-24-auto-codex"))

    def test_codex_running_response_closes_on_subagent_stop(self) -> None:
        hook = self.hook("codex")
        opened = hook.pre_tool_use(self.event(self.root, host="codex"))
        self.assertEqual(opened["status"], "opened")
        self.assertTrue(opened["dispatch_id"].startswith("2026-07-24-auto-codex"))

        correlated = hook.post_tool_use(
            self.event(
                self.root,
                host="codex",
                name="PostToolUse",
                response={"agent_id": "agent-123", "status": "running"},
            )
        )
        self.assertEqual(correlated["agent_id"], "agent-123")
        stopped = hook.subagent_stop(
            {
                "session_id": "codex-session-1",
                "cwd": str(self.root),
                "hook_event_name": "SubagentStop",
                "agent_id": "agent-123",
                "agent_type": "security_review",
            }
        )
        self.assertEqual(stopped["status"], "closed")
        self.assertEqual(stopped["exit_reason"], "resolved")
        log = hook._runtime_bridge()[0].get_orchestration_dispatch_log(
            dispatch_id=opened["dispatch_id"]
        )
        self.assertEqual(log["status"], "closed")
        self.assertEqual(len(log["events"]), 2)

    def test_claude_synchronous_post_closes_exact_tool_call(self) -> None:
        hook = self.hook("claude")
        opened = hook.pre_tool_use(self.event(self.root, host="claude"))
        closed = hook.post_tool_use(
            self.event(
                self.root,
                host="claude",
                name="PostToolUse",
                response={"result": "review complete"},
            )
        )
        self.assertEqual(closed["dispatch_id"], opened["dispatch_id"])
        self.assertEqual(closed["status"], "closed")

    def test_failed_agent_and_session_end_reconcile(self) -> None:
        hook = self.hook("claude")
        failed = hook.pre_tool_use(self.event(self.root, host="claude"))
        error = hook.post_tool_failure(
            self.event(
                self.root,
                host="claude",
                name="PostToolUseFailure",
            )
        )
        self.assertEqual(error["exit_reason"], "error")
        self.assertEqual(error["dispatch_id"], failed["dispatch_id"])

        second_event = self.event(
            self.root,
            host="claude",
            tool_use_id="tool-2",
        )
        second = hook.pre_tool_use(second_event)
        ended = hook.session_end(
            {
                "session_id": "claude-session-1",
                "cwd": str(self.root),
                "hook_event_name": "SessionEnd",
            }
        )
        self.assertEqual(len(ended), 1)
        self.assertEqual(ended[0]["dispatch_id"], second["dispatch_id"])
        self.assertEqual(ended[0]["exit_reason"], "user_abort")

    def test_retry_is_idempotent_and_divergence_denied(self) -> None:
        hook = self.hook("codex")
        event = self.event(self.root, host="codex")
        first = hook.pre_tool_use(event)
        second = hook.pre_tool_use(event)
        self.assertEqual(first["dispatch_id"], second["dispatch_id"])
        ledger = (
            self.root / "telemetry/agents/subagents-dispatch.yaml"
        ).read_text(encoding="utf-8")
        self.assertEqual(ledger.count(f'  - dispatch_id: "{first["dispatch_id"]}"'), 1)

        divergent = self.event(self.root, host="codex")
        divergent["tool_input"]["message"] = "A different task under the same tool id."
        with patch.dict(
            "os.environ",
            {"ACI_HOST_HOOK_PROJECT_ROOT": str(self.root)},
            clear=False,
        ):
            code, output = run(
                ["--host", "codex"],
                stdin=json.dumps(divergent),
            )
        self.assertEqual(code, 0)
        self.assertEqual(
            output["hookSpecificOutput"]["permissionDecision"], "deny"
        )
        self.assertIn(
            "differs from recorded launch",
            output["hookSpecificOutput"]["permissionDecisionReason"],
        )

    def test_missing_bridge_policy_denies_pre_tool_use(self) -> None:
        policy = (
            self.root
            / "docs/features/agent-provenance-telemetry/integration/stage-f/"
            "host-hook-policy.json"
        )
        policy.unlink()
        with patch.dict(
            "os.environ",
            {"ACI_HOST_HOOK_PROJECT_ROOT": str(self.root)},
            clear=False,
        ):
            code, output = run(
                ["--host", "claude"],
                stdin=json.dumps(self.event(self.root, host="claude")),
            )
        self.assertEqual(code, 0)
        self.assertEqual(
            output["hookSpecificOutput"]["permissionDecision"], "deny"
        )

    def test_hook_configuration_covers_both_hosts(self) -> None:
        codex = json.loads((REPO / ".codex/hooks.json").read_text(encoding="utf-8"))
        claude = json.loads(
            (REPO / ".claude/settings.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            set(codex["hooks"]),
            {"PreToolUse", "PostToolUse", "SubagentStop", "SessionEnd"},
        )
        self.assertIn(
            "PostToolUseFailure",
            claude["hooks"],
        )
        self.assertNotIn("SubagentStop", claude["hooks"])
        self.assertIn("Stop", claude["hooks"])
        matcher = (
            "^(?:Agent|spawn_agent|followup_task|"
            "collaboration(?:[._])?spawn_agent|"
            "collaboration(?:[._])?followup_task)$"
        )
        self.assertEqual(codex["hooks"]["PreToolUse"][0]["matcher"], matcher)
        self.assertEqual(codex["hooks"]["PostToolUse"][0]["matcher"], matcher)
        for tool_name in (
            "Agent",
            "spawn_agent",
            "followup_task",
            "collaboration.spawn_agent",
            "collaborationspawn_agent",
            "collaboration.followup_task",
            "collaborationfollowup_task",
        ):
            self.assertIsNotNone(re.fullmatch(matcher, tool_name), tool_name)
        for tool_name in ("not_spawn_agent", "spawn_agent_extra", "other.Agent"):
            self.assertIsNone(re.fullmatch(matcher, tool_name), tool_name)
        self.assertEqual(
            claude["hooks"]["PreToolUse"][0]["matcher"],
            "Agent",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
