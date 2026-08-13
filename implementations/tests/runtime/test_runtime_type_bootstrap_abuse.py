from __future__ import annotations

import copy
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from implementations.server.runtime.canonical import canonical_text, digest_bytes
from implementations.server.runtime.dispatch_types import load_dispatch_type_registry, resolve_dispatch_capability
from implementations.server.runtime.dispatch_workflow import compile_bound_launch_plan
from implementations.server.runtime.errors import GateBlockedError, ValidationError
from implementations.server.runtime.errors import IntegrityError
from implementations.server.runtime.legacy import StrictLegacySnapshotResolver
from implementations.server.runtime.service import RuntimeService, RuntimeSettings


REPO = Path(__file__).resolve().parents[3]


class RuntimeTypeBootstrapAbuseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        registry_rel = Path("implementations/contracts/dispatch-type-registry.v1.json")
        registry = json.loads((REPO / registry_rel).read_text())
        paths = [registry_rel, Path(".claude/skills/register-dispatch/append-dispatch.cjs")]
        paths.extend(Path(e["capability_path"]) for e in registry["types"] if e["capability_path"])
        paths.append(Path(".claude/skills/backlog/SKILL.md"))
        for rel in paths:
            target = self.root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / rel, target)

    def tearDown(self) -> None:
        self.temp.cleanup()

    @staticmethod
    def agent(role: str = "auditor") -> dict:
        return {"role": role, "model": "gpt-test", "token_budget": 1000, "initial_prompt": "Do the bounded work."}

    def review_record(self) -> dict:
        route = resolve_dispatch_capability(self.root, capability_ref="review", authority_mode="legacy-managed")
        return {
            "dispatch_id": "2026-08-13-bootstrap-abuse", "schema_version": "0.6.4",
            "dispatch_type": "review", "goal": "Test fail-closed behavior.",
            "context": "All mutations are isolated in a temporary repository.", "max_loops": 1,
            "final_approver": "parent", "anti_bias_mode": "disabled", "output_mode": "inline",
            "capability_route": route,
            "groups": [{"group_id": "one", "agents": [self.agent()]}], "connections": [],
        }

    def compile(self, record: dict, *, capability: str = "review", output: str = "workflow"):
        return compile_bound_launch_plan(repo_root=self.root, record=record, capability_ref=capability, output_dir=Path(output))

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

    def output_receipt(self, record: dict, source: Path, body: bytes) -> dict:
        receipt = {
            "schema": "aci-host-workflow-producer-output/v1",
            "dispatch_id": record["dispatch_id"],
            "producer_binding_id": "binding",
            "producer_agent_id": "agent",
            "artifact_id": "art_" + digest_bytes(body).removeprefix("sha256:")[:32],
            "path": source.relative_to(self.root).as_posix(),
            "data_schema_ref": "text/plain@1",
            "sha256": digest_bytes(body),
            "size_bytes": len(body),
            "route_digest": record["capability_route"]["route_digest"],
        }
        receipt["receipt_digest"] = digest_bytes(canonical_text(receipt).encode("utf-8"))
        return receipt

    def test_unknown_qualified_malformed_unavailable_and_mismatched_skill_fail(self) -> None:
        for capability in ("unknown-capability", "backlog/child", "Backlog", "backlog--child", "../backlog"):
            with self.subTest(capability=capability), self.assertRaises((ValidationError, GateBlockedError)):
                resolve_dispatch_capability(self.root, capability_ref=capability, authority_mode="legacy-managed")
        with self.assertRaises(GateBlockedError):
            resolve_dispatch_capability(self.root, capability_ref="backlog", authority_mode="runtime-managed")
        skill = self.root / ".claude/skills/backlog/SKILL.md"
        skill.write_text(skill.read_text().replace("name: backlog", "name: forged-name", 1))
        with self.assertRaisesRegex(ValidationError, "name does not match"):
            resolve_dispatch_capability(self.root, capability_ref="backlog", authority_mode="legacy-managed")

    def test_missing_forged_and_post_confirmation_swapped_routes_fail(self) -> None:
        record = self.review_record()
        missing = copy.deepcopy(record)
        missing.pop("capability_route")
        forged = copy.deepcopy(record)
        forged["capability_route"]["route_digest"] = "sha256:" + "0" * 64
        swapped = copy.deepcopy(record)
        swapped["capability_route"] = resolve_dispatch_capability(
            self.root, capability_ref="research", authority_mode="legacy-managed"
        )
        for label, candidate in (("missing", missing), ("forged", forged), ("swapped", swapped)):
            with self.subTest(label=label), self.assertRaises(ValidationError):
                self.compile(candidate)

    def test_missing_tampered_cross_capability_and_stale_handoffs_fail(self) -> None:
        record = self.review_record()
        record["groups"].append({"group_id": "two", "agents": [self.agent()]})
        connection = {"from": "one", "to": "two", "type": "sequential"}
        record["connections"] = [connection]
        out = self.root / "workflow"
        out.mkdir()
        with self.assertRaises(GateBlockedError):
            self.compile(record)
        source = self.root / "output.txt"
        source.write_bytes(b"trusted")
        output_receipt = self.output_receipt(record, source, b"trusted")
        receipt = {
            "schema": "aci-workflow-sequential-handoff/v1", "dispatch_id": record["dispatch_id"],
            "capability_ref": "research", "route_digest": record["capability_route"]["route_digest"],
            "connection": connection,
            "sources": [{"seat_index": 0, "producer_output_receipt": output_receipt}],
        }
        receipt_path = out / "handoff-0-1.json"
        receipt_path.write_text(json.dumps(receipt))
        with self.assertRaisesRegex(ValidationError, "identity or capability route"):
            self.compile(record)
        receipt["capability_ref"] = "review"
        receipt_path.write_text(json.dumps(receipt))
        source.write_bytes(b"tampered")
        with self.assertRaisesRegex(ValidationError, "producer-output bytes differ"):
            self.compile(record)
        source.write_bytes(b"trusted")
        receipt["route_digest"] = "sha256:" + "f" * 64
        receipt_path.write_text(json.dumps(receipt))
        with self.assertRaisesRegex(ValidationError, "identity or capability route"):
            self.compile(record)

    def test_orphan_duplicate_and_unverifiable_current_close_fail_closed(self) -> None:
        record = self.review_record()
        close = {
            "close_of": record["dispatch_id"],
            "exit_reason": "resolved",
            "agents_spawned": {"total": 1, "tree": {"auditor": 1}, "loops_used": 1},
            "capability_route_digest": record["capability_route"]["route_digest"],
        }
        ledger_path = self.root / "telemetry/agents/subagents-dispatch.yaml"

        for label, candidate, validate_only in (
            ("orphan", close, False),
            ("validate-only orphan", close, True),
            ("fake historical assertion", {**close, "schema_version": "0.6.3"}, False),
        ):
            if ledger_path.exists():
                ledger_path.unlink()
            with self.subTest(case=label):
                result = self.appender(candidate, validate_only=validate_only)
                self.assertNotEqual(result.returncode, 0, result.stderr)

        for label, digest in (
            ("missing current digest", None),
            ("malformed current digest", "sha256:not-a-digest"),
            ("mismatched current digest", "sha256:" + "0" * 64),
        ):
            if ledger_path.exists():
                ledger_path.unlink()
            opened = self.appender(record, validate_only=False)
            self.assertEqual(opened.returncode, 0, opened.stderr)
            candidate = dict(close)
            if digest is None:
                candidate.pop("capability_route_digest")
            else:
                candidate["capability_route_digest"] = digest
            with self.subTest(case=label):
                result = self.appender(candidate, validate_only=False)
                self.assertNotEqual(result.returncode, 0, result.stderr)

        ledger_path.unlink()
        opened = self.appender(record, validate_only=False)
        self.assertEqual(opened.returncode, 0, opened.stderr)
        opening_bytes = ledger_path.read_bytes()
        ledger_path.write_bytes(opening_bytes + opening_bytes.split(b"dispatches:\n", 1)[1])
        with self.subTest(case="duplicate opening"):
            result = self.appender(close, validate_only=False)
            self.assertNotEqual(result.returncode, 0, result.stderr)

        ledger_path.write_bytes(opening_bytes.replace(
            record["capability_route"]["route_digest"].encode(),
            b"sha256:not-a-digest",
            1,
        ))
        with self.subTest(case="malformed opening route"):
            result = self.appender(close, validate_only=False)
            self.assertNotEqual(result.returncode, 0, result.stderr)

    def test_feedback_zigzag_reverse_and_unknown_edge_semantics_fail_explicitly(self) -> None:
        for edge_type in ("feedback", "zig-zag", "fanout"):
            record = self.review_record()
            record["groups"].append({"group_id": "two", "agents": [self.agent()]})
            record["connections"] = [{"from": "one", "to": "two", "type": edge_type, "loop_cap": 1}]
            with self.subTest(edge_type=edge_type), self.assertRaises((GateBlockedError, ValidationError)):
                self.compile(record, output=f"workflow-{edge_type}")
        reverse = self.review_record()
        reverse["groups"].append({"group_id": "two", "agents": [self.agent()]})
        reverse["connections"] = [{"from": "two", "to": "one", "type": "sequential"}]
        with self.assertRaisesRegex(GateBlockedError, "canonical declared group order"):
            self.compile(reverse, output="workflow-reverse")

    def test_code_never_falls_back_and_requires_complete_readiness_and_topology(self) -> None:
        route = resolve_dispatch_capability(self.root, capability_ref="domainspec-implement", authority_mode="legacy-managed")
        self.assertEqual(route["ledger_dispatch_type"], "code")
        fallback = self.review_record()
        fallback["dispatch_type"] = "other"
        fallback["capability_route"] = route
        with self.assertRaises(ValidationError):
            self.compile(fallback, capability="domainspec-implement", output="code-fallback")
        incomplete = self.review_record()
        incomplete.update({"dispatch_type": "code", "capability_route": route})
        incomplete.pop("output_mode")
        with self.assertRaises((GateBlockedError, ValidationError)):
            self.compile(incomplete, capability="domainspec-implement", output="code-incomplete")
        inflated = copy.deepcopy(incomplete)
        inflated["groups"].append({"group_id": "extra", "agents": [self.agent()]})
        with self.assertRaises((GateBlockedError, ValidationError)):
            self.compile(inflated, capability="domainspec-implement", output="code-inflated")

    def test_registry_tamper_and_duplicate_installed_identity_fail_closed(self) -> None:
        registry_path = self.root / "implementations/contracts/dispatch-type-registry.v1.json"
        registry = json.loads(registry_path.read_text())
        registry["generic_fallback"]["ledger_value"] = "others"
        registry["generic_fallback"]["api_aliases"] = ["others"]
        registry_path.write_text(json.dumps(registry))
        with self.assertRaises(GateBlockedError):
            load_dispatch_type_registry(self.root)

    def test_legacy_opening_versions_accept_only_061_through_064(self) -> None:
        resolver = StrictLegacySnapshotResolver()
        ledger = self.root / "legacy.yaml"
        for version in ("0.6.1", "0.6.2", "0.6.3", "0.6.4"):
            dispatch_id = f"accepted-{version.replace('.', '-')}"
            ledger.write_text(
                "dispatches:\n"
                f"  - dispatch_id: {json.dumps(dispatch_id)}\n"
                f"    schema_version: {json.dumps(version)}\n",
                encoding="utf-8",
            )
            self.assertEqual(resolver.resolve(ledger, dispatch_id).contract_version, version)
        for index, value in enumerate((None, "", "0.6", "0.6.5", "1.0.0", "unknown", 604)):
            dispatch_id = f"rejected-{index}"
            row = "dispatches:\n" + f"  - dispatch_id: {json.dumps(dispatch_id)}\n"
            if value is not None:
                row += f"    schema_version: {json.dumps(value)}\n"
            ledger.write_text(row, encoding="utf-8")
            with self.subTest(value=value), self.assertRaisesRegex(
                IntegrityError, "supported 0.6.1, 0.6.2, 0.6.3, or 0.6.4 contract"
            ):
                resolver.resolve(ledger, dispatch_id)

    def test_service_rejects_missing_malformed_stale_and_cross_route_digest(self) -> None:
        route = resolve_dispatch_capability(self.root, capability_ref="review", authority_mode="legacy-managed")
        other_route = resolve_dispatch_capability(self.root, capability_ref="research", authority_mode="legacy-managed")
        runtime = RuntimeService(RuntimeSettings(
            database_path=self.root / "runtime.sqlite3", repo_root=self.root,
            ledger_path=self.root / "telemetry/agents/subagents-dispatch.yaml",
            local_pilot_serve_enabled=True,
        ))
        base = {
            "schema": "aci-workflow-input-manifest/v1", "dispatch_id": "dispatch-1",
            "route_digest": route["route_digest"],
            "target": {"group_id": "workers", "seat_index": 0, "turn_ordinal": 0, "attempt_id": "attempt-1"},
            "slots": [],
        }
        variants = {
            "missing": {key: value for key, value in base.items() if key != "route_digest"},
            "malformed": {**base, "route_digest": "sha256:not-a-digest"},
            "stale": {**base, "route_digest": "sha256:" + "0" * 64},
            "cross-route": {**base, "route_digest": other_route["route_digest"]},
        }
        for label, manifest in variants.items():
            raw = json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()
            with self.subTest(label=label), self.assertRaises(IntegrityError):
                runtime._validate_workflow_manifest(
                    raw=raw, expected_digest=digest_bytes(raw),
                    opened_dispatch_route_digest=route["route_digest"], dispatch_id="dispatch-1",
                    group_id="workers", seat_index=0, turn_ordinal=0, attempt_id="attempt-1",
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
