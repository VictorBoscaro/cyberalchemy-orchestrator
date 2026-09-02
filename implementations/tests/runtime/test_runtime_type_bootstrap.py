from __future__ import annotations

import base64
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from implementations.server import ledger
from implementations.server.runtime.canonical import canonical_text, digest_bytes
from implementations.server.runtime.dispatch_types import (
    live_dispatch_type_values,
    load_dispatch_type_registry,
    normalize_dispatch_type,
    resolve_dispatch_capability,
)
from implementations.server.runtime.dispatch_workflow import (
    BINDING_MARKER,
    compile_bound_launch_plan,
)
from implementations.server.runtime.host_dispatch_hook import HostDispatchHook
from implementations.server.runtime.service import RuntimeService, RuntimeSettings


REPO = Path(__file__).resolve().parents[3]


class RuntimeTypeBootstrapTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        registry_rel = Path("implementations/contracts/dispatch-type-registry.v2.json")
        registry = json.loads((REPO / registry_rel).read_text(encoding="utf-8"))
        paths = [
            registry_rel,
            Path("implementations/contracts/dispatch-ledger-row.v0.7.0.schema.json"),
            Path("implementations/contracts/agent-role-registry.v1.json"),
            Path("implementations/contracts/agent-role-registry-authority.v1.json"),
            Path("implementations/contracts/agent-role-registry-selection.json"),
            Path("implementations/contracts/agent-role-host-routing.v1.json"),
            Path(".claude/skills/register-dispatch/append-dispatch.cjs"),
        ]
        paths.append(Path("docs/features/agent-provenance-telemetry/integration/stage-f/host-hook-policy.json"))
        paths.extend(
            Path(entry["capability_path"])
            for entry in registry["types"]
            if entry["capability_path"]
        )
        for capability in ("backlog", "craft", "whisper"):
            paths.append(Path(".claude/skills") / capability / "SKILL.md")
        for relative in paths:
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / relative, target)

    def tearDown(self) -> None:
        self.temp.cleanup()

    @staticmethod
    def agent(role: str = "auditor", prompt: str = "Perform the bounded task.") -> dict:
        return {"role": role, "model": "gpt-test", "token_budget": 1000, "initial_prompt": prompt}

    def record(self, capability: str = "review", *, groups: list[dict] | None = None) -> dict:
        route = resolve_dispatch_capability(
            self.root, capability_ref=capability, authority_mode="legacy-managed"
        )
        registry = load_dispatch_type_registry(self.root)
        value = {
            "dispatch_id": f"2026-08-13-{capability}-bootstrap-test",
            "schema_version": registry["ledger_schema_version"],
            "agent_role_registry_ref": registry["agent_role_registry_ref"],
            "dispatch_type": route["ledger_dispatch_type"],
            "goal": "Exercise the frozen Stage-A runtime contract.",
            "context": "A deterministic isolated fixture verifies routing and binding.",
            "max_loops": 1,
            "final_approver": "parent",
            "anti_bias_mode": "disabled",
            "capability_route": route,
            "groups": groups or [{"group_id": "workers", "agents": [self.agent()]}],
            "connections": [],
        }
        if value["dispatch_type"] == "review":
            value["output_mode"] = "inline"
        return value

    def appender(self, record: dict, *, validate_only: bool = True) -> subprocess.CompletedProcess[str]:
        record_path = self.root / "record.json"
        record_path.write_text(json.dumps(record), encoding="utf-8")
        env = dict(os.environ)
        env["CLAUDE_PROJECT_DIR"] = str(self.root)
        if validate_only:
            env["REGISTER_DISPATCH_VALIDATE_ONLY"] = "1"
        return subprocess.run(
            ["node", str(self.root / ".claude/skills/register-dispatch/append-dispatch.cjs"), str(record_path)],
            cwd=self.root,
            env=env,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )

    def test_registry_bump_alias_and_canonical_new_row(self) -> None:
        registry = load_dispatch_type_registry(self.root)
        self.assertEqual(registry["ledger_schema_version"], "0.7.0")
        self.assertEqual(registry["generic_fallback"]["ledger_value"], "other")
        self.assertNotIn("others", live_dispatch_type_values(self.root))
        self.assertIn("other", live_dispatch_type_values(self.root))
        self.assertEqual(normalize_dispatch_type(self.root, "others"), "other")
        self.assertEqual(normalize_dispatch_type(self.root, "other"), "other")
        result = self.appender(self.record("backlog"))
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_multiple_installed_unmapped_capabilities_retain_exact_identity(self) -> None:
        routes = [
            resolve_dispatch_capability(
                self.root, capability_ref=name, authority_mode="legacy-managed"
            )
            for name in ("backlog", "craft", "whisper")
        ]
        self.assertEqual({route["ledger_dispatch_type"] for route in routes}, {"other"})
        self.assertEqual({route["capability_ref"] for route in routes}, {"backlog", "craft", "whisper"})
        self.assertEqual(len({route["route_digest"] for route in routes}), 3)
        for route in routes:
            self.assertEqual(route["execution_authority_mode"], "legacy-managed")
            self.assertEqual(route["tool_profile_ref"], "host/inherited@1")
            self.assertEqual(route["capability_digest"], digest_bytes((self.root / route["capability_path"]).read_bytes()))

    def test_specialized_mappings_win_including_code(self) -> None:
        for capability in ("research", "review", "experiment", "domainspec-implement"):
            with self.subTest(capability=capability):
                route = resolve_dispatch_capability(
                    self.root, capability_ref=capability, authority_mode="legacy-managed"
                )
                expected = "code" if capability == "domainspec-implement" else capability
                self.assertEqual(route["dispatch_type_ref"], expected)
                self.assertEqual(route["ledger_dispatch_type"], expected)

    def test_historical_plural_rows_remain_readable_closable_and_aggregated(self) -> None:
        ledger_path = self.root / "telemetry/agents/subagents-dispatch.yaml"
        ledger_path.parent.mkdir(parents=True)
        original = (
            "dispatches:\n"
            "  - dispatch_id: \"2026-08-01-historical-others\"\n"
            "    schema_version: \"0.6.3\"\n"
            "    dispatch_type: \"others\"\n"
            "    goal: \"Historical row\"\n"
            "    created: \"2026-08-01T00:00:00Z\"\n"
        ).encode()
        ledger_path.write_bytes(original)
        parsed = ledger.parse_ledger(original.decode())
        self.assertEqual(parsed.rows[0]["dispatch_type"], "others")
        close = {
            "close_of": "2026-08-01-historical-others",
            "exit_reason": "resolved",
            "agents_spawned": {"total": 1, "tree": {"worker": 1}, "loops_used": 1},
        }
        result = self.appender(close, validate_only=False)
        self.assertNotEqual(result.returncode, 0, result.stderr)
        self.assertEqual(ledger_path.read_bytes(), original)
        summary = ledger.summarize_repo(self.root, today="2026-08-13", pending=[])
        self.assertEqual(summary["by_type"]["others"], 1)
        self.assertEqual(summary["closed"], 0)
        series = ledger.daily_series(ledger.load_repo_rows(self.root).rows)
        self.assertIn("others", series["series"])

    def test_valid_code_requires_complete_readiness_and_canonical_topology(self) -> None:
        for relative in (
            "docs/features/agents-communication-infra/WORK-PACK.md",
            "docs/features/agents-communication-infra/TEST-SPEC.md",
        ):
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / relative, target)
        route = resolve_dispatch_capability(
            self.root, capability_ref="domainspec-implement", authority_mode="legacy-managed"
        )
        digest = lambda relative: "sha256:" + hashlib.sha256((self.root / relative).read_bytes()).hexdigest()
        work_pack = "docs/features/agents-communication-infra/WORK-PACK.md"
        test_spec = "docs/features/agents-communication-infra/TEST-SPEC.md"
        readiness_ref = "plans/code-readiness.json"
        write_scope = ["implementations/server/runtime/example.py"]
        commands = ["python -m unittest example"]
        readiness = {
            "schema": "domainspec-code-readiness@1", "status": "PASS", "task_id": "STAGE-A-CODE",
            "work_pack_ref": work_pack, "work_pack_digest": digest(work_pack),
            "test_spec_ref": test_spec, "test_spec_digest": digest(test_spec),
            "brownfield": False, "write_scope": write_scope, "validation_commands": commands,
            "capability_profile": {"filesystem": "task-scoped-write", "network": "none",
                                   "credentials": False, "production": False, "destructive": False},
        }
        readiness_path = self.root / readiness_ref
        readiness_path.parent.mkdir(parents=True)
        readiness_path.write_text(json.dumps(readiness), encoding="utf-8")
        record = self.record("review")
        record.update({"dispatch_type": "code", "capability_route": route})
        record.pop("output_mode")
        record["code_contract"] = {
            "type_skill_ref": ".claude/skills/domainspec-implement/SKILL.md",
            "type_skill_digest": digest(".claude/skills/domainspec-implement/SKILL.md"),
            "work_pack_ref": work_pack, "work_pack_digest": digest(work_pack),
            "test_spec_ref": test_spec, "test_spec_digest": digest(test_spec),
            "readiness_ref": readiness_ref, "readiness_digest": digest(readiness_ref),
            "brownfield": False, "write_scope": write_scope, "validation_commands": commands,
            "implementation_group_id": "implementation", "verification_group_id": "verification",
        }
        record["groups"] = [
            {"group_id": "implementation", "agents": [self.agent("coder")]},
            {"group_id": "verification", "agents": [self.agent("skeptic")]},
        ]
        record["connections"] = [{"from": "implementation", "to": "verification", "type": "sequential"}]
        result = self.appender(record)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_open_and_close_preserve_exact_route_digest(self) -> None:
        record = self.record("review")
        opened = self.appender(record, validate_only=False)
        self.assertEqual(opened.returncode, 0, opened.stderr)
        close = {
            "close_of": record["dispatch_id"], "exit_reason": "resolved",
            "schema_version": record["schema_version"],
            "agent_role_registry_ref": record["agent_role_registry_ref"],
            "agents_spawned": {"total": 1, "tree": {"auditor": 1}, "loops_used": 1},
            "capability_route_digest": record["capability_route"]["route_digest"],
        }
        closed = self.appender(close, validate_only=False)
        self.assertEqual(closed.returncode, 0, closed.stderr)
        text = (self.root / "telemetry/agents/subagents-dispatch.yaml").read_text()
        self.assertIn(record["capability_route"]["route_digest"], text)

    def test_automatic_host_opening_derives_route_without_changing_task_fields(self) -> None:
        hook = HostDispatchHook(
            root=self.root,
            host="codex",
            now=lambda: datetime(2026, 8, 13, 12, 0, tzinfo=timezone.utc),
        )
        event = {
            "session_id": "host-session",
            "tool_use_id": "tool-1",
            "tool_input": {
                "task_name": "security review",
                "message": "Review the boundary without changing files.",
                "model": "gpt-test-model",
            },
        }
        record, role, session_id, tool_use_id = hook._opening_record(event)
        registry = load_dispatch_type_registry(self.root)
        self.assertEqual(record["schema_version"], registry["ledger_schema_version"])
        self.assertEqual(record["dispatch_type"], record["capability_route"]["ledger_dispatch_type"])
        self.assertEqual(record["capability_route"], resolve_dispatch_capability(
            self.root, capability_ref="review", authority_mode="legacy-managed"
        ))
        agent = record["groups"][0]["agents"][0]
        self.assertEqual((role, session_id, tool_use_id), ("auditor", "host-session", "tool-1"))
        self.assertEqual(agent["model"], "gpt-test-model")
        self.assertEqual(agent["initial_prompt"], event["tool_input"]["message"])
        self.assertEqual(record["anti_bias_mode"], "disabled")
        self.assertEqual(record["output_mode"], "inline")

    def test_route_digest_is_shared_by_appender_compiler_and_binding(self) -> None:
        record = self.record("review")
        self.assertEqual(self.appender(record).returncode, 0)
        compiled = compile_bound_launch_plan(
            repo_root=self.root,
            record=record,
            capability_ref="review",
            output_dir=Path(".codex/workflow-inputs/shared-route"),
        )
        self.assertEqual(compiled["route"]["route_digest"], record["capability_route"]["route_digest"])
        marker, _ = compiled["launches"][0]["spawn_arguments"]["message"].split("\n", 1)
        envelope = json.loads(base64.urlsafe_b64decode(marker[len(BINDING_MARKER):] + "=="))
        manifest = json.loads((self.root / envelope["workflow_manifest_path"]).read_text())
        self.assertIn("route_digest", manifest, "dynamic input manifest must be route-digest-bound")
        self.assertEqual(manifest["route_digest"], record["capability_route"]["route_digest"])

    def test_service_accepts_manifest_only_at_exact_opened_route_digest(self) -> None:
        route = resolve_dispatch_capability(
            self.root, capability_ref="review", authority_mode="legacy-managed"
        )
        manifest = {
            "schema": "aci-workflow-input-manifest/v1",
            "dispatch_id": "dispatch-1",
            "route_digest": route["route_digest"],
            "target": {"group_id": "workers", "seat_index": 0, "turn_ordinal": 0, "attempt_id": "attempt-1"},
            "slots": [],
        }
        raw = json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()
        runtime = RuntimeService(RuntimeSettings(
            database_path=self.root / "runtime.sqlite3", repo_root=self.root,
            ledger_path=self.root / "telemetry/agents/subagents-dispatch.yaml",
            local_pilot_serve_enabled=True,
        ))
        accepted, artifacts = runtime._validate_workflow_manifest(
            raw=raw, expected_digest=digest_bytes(raw),
            opened_dispatch_route_digest=route["route_digest"], dispatch_id="dispatch-1",
            group_id="workers", seat_index=0, turn_ordinal=0, attempt_id="attempt-1",
        )
        self.assertEqual(accepted, manifest)
        self.assertEqual(artifacts, [])

    def test_sequential_output_materializes_ordered_digest_bound_manifest(self) -> None:
        groups = [
            {"group_id": "produce", "agents": [self.agent(prompt="Produce A"), self.agent(prompt="Produce B")]},
            {"group_id": "consume", "agents": [self.agent(prompt="Consume exact outputs")]},
        ]
        record = self.record("review", groups=groups)
        record["connections"] = [{"from": "produce", "to": "consume", "type": "sequential"}]
        output = self.root / ".codex/workflow-inputs/sequential"
        output.mkdir(parents=True)
        sources = []
        for seat, text in enumerate((b"first", b"second")):
            relative = f"outputs/produce-{seat}.txt"
            path = self.root / relative
            path.parent.mkdir(exist_ok=True)
            path.write_bytes(text)
            output_receipt = {
                "schema": "aci-host-workflow-producer-output/v1",
                "dispatch_id": record["dispatch_id"],
                "producer_binding_id": f"binding-{seat}",
                "producer_agent_id": f"agent-{seat}",
                "artifact_id": "art_" + digest_bytes(text).removeprefix("sha256:")[:32],
                "path": relative,
                "data_schema_ref": "text/plain@1",
                "sha256": digest_bytes(text),
                "size_bytes": len(text),
                "route_digest": record["capability_route"]["route_digest"],
            }
            output_receipt["receipt_digest"] = digest_bytes(
                canonical_text(output_receipt).encode("utf-8")
            )
            sources.append({
                "seat_index": seat,
                "producer_output_receipt": output_receipt,
            })
        receipt = {
            "schema": "aci-workflow-sequential-handoff/v1",
            "dispatch_id": record["dispatch_id"],
            "capability_ref": "review",
            "route_digest": record["capability_route"]["route_digest"],
            "connection": record["connections"][0],
            "sources": sources,
        }
        (output / "handoff-0-1.json").write_text(json.dumps(receipt), encoding="utf-8")
        compiled = compile_bound_launch_plan(
            repo_root=self.root, record=record, capability_ref="review",
            output_dir=Path(".codex/workflow-inputs/sequential"),
        )
        consumer = next(item for item in compiled["launches"] if item["group_id"] == "consume")
        manifest = json.loads((self.root / consumer["workflow_manifest_path"]).read_text())
        self.assertEqual(
            [
                source["producer_output_receipt"]["producer_binding_id"]
                for source in manifest["slots"][0]["sources"]
            ],
            ["binding-0", "binding-1"],
        )
        self.assertTrue(all(
            source["source_kind"] == "binding-output"
            and set(source) == {"source_kind", "producer_output_receipt"}
            for source in manifest["slots"][0]["sources"]
        ))
        self.assertEqual(compiled["handoffs"][0]["route_digest"], record["capability_route"]["route_digest"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
