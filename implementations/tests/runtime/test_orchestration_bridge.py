from __future__ import annotations

import json
import hashlib
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from implementations.server.runtime.canonical import canonical_digest
from implementations.server.runtime.cli import run as runtime_run
from implementations.server.runtime.errors import AuthorizationError, GateBlockedError
from implementations.server.runtime.orchestration_bridge import (
    LocalOrchestrationLoggingBridge,
    run as bridge_run,
)
from implementations.server.runtime.service import RuntimeService, RuntimeSettings

REPO = Path(__file__).resolve().parents[3]
APPENDER = REPO / ".claude/skills/register-dispatch/append-dispatch.cjs"
EVIDENCE_REF = "codex-thread:test-confirmation"
EVIDENCE_DIGEST = canonical_digest({"confirmation": "test-authorized"})


class OrchestrationLoggingBridgeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.project = Path(self.temp.name)
        self.ledger = self.project / "telemetry/agents/subagents-dispatch.yaml"
        self.database = self.project / "telemetry/runtime/bridge.sqlite3"
        self.runtime = RuntimeService(
            RuntimeSettings(
                database_path=self.database,
                repo_root=REPO,
                ledger_path=self.ledger,
                local_pilot_serve_enabled=True,
            )
        )
        self.bridge = LocalOrchestrationLoggingBridge(
            runtime=self.runtime,
            project_dir=self.project,
            appender_path=APPENDER,
        )
        self.opening = {
            "dispatch_id": "2026-07-24-bridge-review",
            "schema_version": "0.6.1",
            "dispatch_type": "review",
            "goal": "Review the local orchestration logging bridge.",
            "context": (
                "The bridge must append through the validated appender and accept "
                "ACI receipts before launch. The reviewer checks fail-closed and "
                "idempotency behavior."
            ),
            "max_loops": 1,
            "final_approver": "parent",
            "output_mode": "inline",
            "groups": [
                {
                    "group_id": "reviewer",
                    "agents": [
                        {
                            "agent_name": None,
                            "role": "auditor",
                            "model": "gpt-5.6",
                            "token_budget": 1200,
                            "initial_prompt": "Review the logging bridge and return findings.",
                        }
                    ],
                }
            ],
        }
        self.closing = {
            "close_of": self.opening["dispatch_id"],
            "exit_reason": "resolved",
            "agents_spawned": {
                "total": 1,
                "tree": {"auditor": 1, "helpers": 0},
                "loops_used": 1,
            },
        }

    def tearDown(self) -> None:
        self.temp.cleanup()

    def common(self) -> dict[str, str]:
        return {
            "actor_ref": "operator:test",
            "authorization_evidence_ref": EVIDENCE_REF,
            "authorization_evidence_digest": EVIDENCE_DIGEST,
        }

    def authority(
        self,
        operation: str,
        record: dict,
        *,
        session_name: str | None = None,
        origin_ref: str | None = None,
        session_id: str | None = None,
        nonce: str = "test-nonce",
    ):
        self.bridge.prepare()
        context = {
            "operation": operation,
            "dispatch_id": record.get(
                "dispatch_id" if operation == "open" else "close_of"
            ),
            "record_digest": canonical_digest(record),
            "authorization_evidence_ref": EVIDENCE_REF,
            "authorization_evidence_digest": EVIDENCE_DIGEST,
            "nonce": nonce,
        }
        action = f"orchestration.bridge.{operation}"
        phase = "bootstrap" if operation == "open" else "finalize"
        if operation == "open":
            context.update(
                {"session_name": session_name, "origin_ref": origin_ref}
            )
        else:
            context["session_id"] = session_id
        issued = self.runtime.issue_capability(
            principal_id="operator:test",
            action=action,
            phase=phase,
            context=context,
            expires_at="2099-01-01T00:00:00+00:00",
        )
        return self.runtime.capabilities.resolve(
            issued["token"], action=action, phase=phase
        )

    def staged_cli_project(self) -> tuple[Path, Path, Path]:
        root = self.project / "staged-project"
        source_manifest_path = (
            REPO
            / "docs/features/agent-provenance-telemetry/integration/stage-e/"
            "source-manifest.json"
        )
        source_manifest = json.loads(
            source_manifest_path.read_text(encoding="utf-8")
        )
        required = list(source_manifest["files"]) + [
            "docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json",
            "docs/features/agent-provenance-telemetry/integration/stage-b/execution-receipt.md",
            "docs/features/agent-provenance-telemetry/integration/stage-c/local-pilot-enablement.md",
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
        for relative in required:
            source = REPO / relative
            destination = root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
        ledger = root / "telemetry/agents/subagents-dispatch.yaml"
        ledger.parent.mkdir(parents=True, exist_ok=True)
        ledger.write_text(
            "# test ledger\n"
            "dispatches:\n",
            encoding="utf-8",
        )
        database = root / "telemetry/runtime/cli-bridge.sqlite3"
        return root, database, ledger

    def open(self):
        session_name = "bridge-test"
        origin_ref = "codex:test-thread"
        return self.bridge.open_dispatch(
            authority=self.authority(
                "open",
                self.opening,
                session_name=session_name,
                origin_ref=origin_ref,
            ),
            record=self.opening,
            session_name=session_name,
            origin_ref=origin_ref,
        )

    def close(self, session_id: str, record: dict | None = None, *, nonce="close"):
        submitted = record or self.closing
        return self.bridge.close_dispatch(
            authority=self.authority(
                "close",
                submitted,
                session_id=session_id,
                nonce=nonce,
            ),
            record=submitted,
            session_id=session_id,
        )

    def test_open_and_close_write_yaml_and_aci_receipts(self) -> None:
        opened = self.open()
        self.assertEqual(opened["status"], "launch-authorized")
        self.assertEqual(
            opened["orchestration_receipt"]["orchestration_dispatch"]["status"],
            "opened",
        )
        self.assertTrue(opened["yaml"]["changed"])

        closed = self.close(opened["session_id"])
        self.assertEqual(closed["status"], "closed")
        self.assertEqual(
            closed["orchestration_receipt"]["orchestration_dispatch"]["status"],
            "closed",
        )
        text = self.ledger.read_text(encoding="utf-8")
        self.assertIn(
            f'  - dispatch_id: "{self.opening["dispatch_id"]}"',
            text,
        )
        self.assertIn(
            f'  - close_of: "{self.opening["dispatch_id"]}"',
            text,
        )
        with self.runtime.database.connect() as conn:
            event_types = [
                row["event_type"]
                for row in conn.execute(
                    """
                    SELECT event_type FROM events
                    WHERE aggregate_id=? ORDER BY aggregate_version
                    """,
                    (f"aci.orchestration-dispatch:{self.opening['dispatch_id']}",),
                )
            ]
            link = conn.execute(
                "SELECT session_id FROM dispatch_links WHERE dispatch_id=?",
                (self.opening["dispatch_id"],),
            ).fetchone()
        self.assertEqual(
            event_types,
            [
                "orchestration.dispatch_opened@1",
                "orchestration.dispatch_closed@1",
            ],
        )
        self.assertEqual(link["session_id"], opened["session_id"])
        self.assertFalse(
            Path(str(self.ledger) + ".append.lock").exists(),
            "successful appends must release the exclusive lock",
        )

        log = self.runtime.get_orchestration_dispatch_log(
            dispatch_id=self.opening["dispatch_id"]
        )
        self.assertEqual(log["status"], "closed")
        self.assertEqual(
            [event["journal_offset"] for event in log["events"]],
            sorted(event["journal_offset"] for event in log["events"]),
        )
        self.assertEqual(
            log["yaml"]["closing"]["record"]["exit_reason"],
            "resolved",
        )

    def test_open_and_close_retries_are_idempotent(self) -> None:
        first = self.open()
        second = self.open()
        self.assertFalse(second["yaml"]["changed"])
        self.assertEqual(
            first["orchestration_receipt"]["command_id"],
            second["orchestration_receipt"]["command_id"],
        )

        first_close = self.close(first["session_id"], nonce="close-1")
        second_close = self.close(first["session_id"], nonce="close-2")
        self.assertFalse(second_close["yaml"]["changed"])
        self.assertEqual(
            first_close["orchestration_receipt"]["command_id"],
            second_close["orchestration_receipt"]["command_id"],
        )
        with self.runtime.database.connect() as conn:
            count = conn.execute(
                "SELECT count(*) FROM events WHERE aggregate_id=?",
                (f"aci.orchestration-dispatch:{self.opening['dispatch_id']}",),
            ).fetchone()[0]
        self.assertEqual(count, 2)

    def test_divergent_idempotent_retry_is_rejected(self) -> None:
        opened = self.open()
        divergent = {**self.opening, "goal": "A different semantic request."}
        with self.assertRaisesRegex(GateBlockedError, "differs at field goal"):
            self.bridge.open_dispatch(
                authority=self.authority(
                    "open",
                    divergent,
                    session_name="bridge-test",
                    origin_ref="codex:test-thread",
                ),
                record=divergent,
                session_name="bridge-test",
                origin_ref="codex:test-thread",
            )
        closed = self.close(opened["session_id"])
        divergent_close = {
            **self.closing,
            "exit_reason": "error",
        }
        with self.assertRaisesRegex(
            GateBlockedError, "differs at field exit_reason"
        ):
            self.close(opened["session_id"], divergent_close)
        self.assertEqual(closed["status"], "closed")

    def code_record(self, *, readiness_status: str = "PASS") -> dict:
        record = {**self.opening, "dispatch_type": "code"}
        record.pop("output_mode")
        pinned = [
            ".claude/skills/domainspec-implement/SKILL.md",
            "docs/features/agents-communication-infra/WORK-PACK.md",
            "docs/features/agents-communication-infra/TEST-SPEC.md",
        ]
        for relative in pinned:
            target = self.project / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / relative, target)
        digest = lambda relative: "sha256:" + hashlib.sha256(
            (REPO / relative).read_bytes()
        ).hexdigest()
        readiness_ref = "plans/test-code-readiness.json"
        write_scope = ["implementations/server/runtime/example.py"]
        validation_commands = ["python -m unittest example"]
        readiness = {
            "schema": "domainspec-code-readiness@1",
            "status": readiness_status,
            "task_id": "TEST-CODE-001",
            "work_pack_ref": "docs/features/agents-communication-infra/WORK-PACK.md",
            "work_pack_digest": digest(
                "docs/features/agents-communication-infra/WORK-PACK.md"
            ),
            "test_spec_ref": "docs/features/agents-communication-infra/TEST-SPEC.md",
            "test_spec_digest": digest(
                "docs/features/agents-communication-infra/TEST-SPEC.md"
            ),
            "brownfield": False,
            "write_scope": write_scope,
            "validation_commands": validation_commands,
            "capability_profile": {
                "filesystem": "task-scoped-write",
                "network": "none",
                "credentials": False,
                "production": False,
                "destructive": False,
            },
        }
        readiness_path = self.project / readiness_ref
        readiness_path.parent.mkdir(parents=True, exist_ok=True)
        readiness_path.write_text(
            json.dumps(readiness, sort_keys=True), encoding="utf-8"
        )
        record["code_contract"] = {
            "type_skill_ref": ".claude/skills/domainspec-implement/SKILL.md",
            "type_skill_digest": digest(
                ".claude/skills/domainspec-implement/SKILL.md"
            ),
            "work_pack_ref": "docs/features/agents-communication-infra/WORK-PACK.md",
            "work_pack_digest": digest(
                "docs/features/agents-communication-infra/WORK-PACK.md"
            ),
            "test_spec_ref": "docs/features/agents-communication-infra/TEST-SPEC.md",
            "test_spec_digest": digest(
                "docs/features/agents-communication-infra/TEST-SPEC.md"
            ),
            "readiness_ref": readiness_ref,
            "readiness_digest": "sha256:" + hashlib.sha256(
                readiness_path.read_bytes()
            ).hexdigest(),
            "brownfield": False,
            "write_scope": write_scope,
            "validation_commands": validation_commands,
            "implementation_group_id": "implementation",
            "verification_group_id": "verification",
        }
        record["groups"] = [
            {
                "group_id": "implementation",
                "agents": [
                    {
                        "agent_name": None,
                        "role": "coder",
                        "model": "gpt-5.6",
                        "token_budget": 1200,
                        "initial_prompt": "Implement the pinned DomainSpec task.",
                    }
                ],
            },
            {
                "group_id": "verification",
                "agents": [
                    {
                        "agent_name": None,
                        "role": "skeptic",
                        "model": "gpt-5.6",
                        "token_budget": 1200,
                        "initial_prompt": "Verify the bounded implementation and evidence.",
                    }
                ],
            },
        ]
        record["connections"] = [
            {"from": "implementation", "to": "verification", "type": "sequential"}
        ]
        return record

    def test_code_dispatch_type_is_live(self) -> None:
        record = self.code_record()
        opened = self.bridge.open_dispatch(
            authority=self.authority(
                "open",
                record,
                session_name="bridge-test",
                origin_ref="codex:test-thread",
            ),
            record=record,
            session_name="bridge-test",
            origin_ref="codex:test-thread",
        )
        self.assertEqual(opened["status"], "launch-authorized")
        self.assertEqual(opened["dispatch_id"], record["dispatch_id"])
        self.assertTrue(self.ledger.exists())

    def test_others_dispatch_type_is_live(self) -> None:
        record = {
            **self.opening,
            "dispatch_id": "2026-07-25-bridge-document-authoring",
            "dispatch_type": "others",
        }
        record.pop("output_mode")
        opened = self.bridge.open_dispatch(
            authority=self.authority(
                "open",
                record,
                session_name="bridge-test",
                origin_ref="codex:test-thread",
            ),
            record=record,
            session_name="bridge-test",
            origin_ref="codex:test-thread",
        )
        self.assertEqual(opened["status"], "launch-authorized")
        self.assertEqual(opened["dispatch_id"], record["dispatch_id"])
        self.assertTrue(self.ledger.exists())

    def test_reserved_dispatch_type_fails_before_yaml_or_dispatch_acceptance(self) -> None:
        record = {**self.opening, "dispatch_type": "plan"}
        with self.assertRaisesRegex(GateBlockedError, "live research"):
            self.bridge.open_dispatch(
                authority=self.authority(
                    "open",
                    record,
                    session_name="bridge-test",
                    origin_ref="codex:test-thread",
                ),
                record=record,
                session_name="bridge-test",
                origin_ref="codex:test-thread",
            )
        self.assertFalse(self.ledger.exists())
        with self.runtime.database.connect() as conn:
            self.assertEqual(
                conn.execute("SELECT count(*) FROM dispatch_links").fetchone()[0],
                0,
            )

    def test_code_without_pinned_domainspec_contract_is_rejected(self) -> None:
        record = {**self.opening, "dispatch_type": "code"}
        record.pop("output_mode")
        with self.assertRaisesRegex(GateBlockedError, "code_contract is required"):
            self.bridge.open_dispatch(
                authority=self.authority(
                    "open",
                    record,
                    session_name="bridge-test",
                    origin_ref="codex:test-thread",
                ),
                record=record,
                session_name="bridge-test",
                origin_ref="codex:test-thread",
            )
        self.assertFalse(self.ledger.exists())

    def test_code_readiness_fail_is_rejected(self) -> None:
        record = self.code_record(readiness_status="FAIL")
        with self.assertRaisesRegex(GateBlockedError, 'readiness status must be "PASS"'):
            self.bridge.open_dispatch(
                authority=self.authority(
                    "open",
                    record,
                    session_name="bridge-test",
                    origin_ref="codex:test-thread",
                ),
                record=record,
                session_name="bridge-test",
                origin_ref="codex:test-thread",
            )

    def test_code_write_scope_escape_is_rejected(self) -> None:
        record = self.code_record()
        record["code_contract"]["write_scope"] = ["../outside.py"]
        with self.assertRaisesRegex(GateBlockedError, "must stay below project_dir"):
            self.bridge.open_dispatch(
                authority=self.authority(
                    "open",
                    record,
                    session_name="bridge-test",
                    origin_ref="codex:test-thread",
                ),
                record=record,
                session_name="bridge-test",
                origin_ref="codex:test-thread",
            )

    def test_code_topology_inflation_is_rejected(self) -> None:
        record = self.code_record()
        record["groups"].append(
            {
                "group_id": "extra-coder",
                "agents": [
                    {
                        "role": "coder",
                        "model": "gpt-5.6",
                        "token_budget": 100,
                        "initial_prompt": "Undeclared extra implementation lane.",
                    }
                ],
            }
        )
        record["connections"].append(
            {"from": "extra-coder", "to": "verification", "type": "sequential"}
        )
        with self.assertRaisesRegex(
            GateBlockedError, "groups must be exactly|exactly 1 canonical"
        ):
            self.bridge.open_dispatch(
                authority=self.authority(
                    "open",
                    record,
                    session_name="bridge-test",
                    origin_ref="codex:test-thread",
                ),
                record=record,
                session_name="bridge-test",
                origin_ref="codex:test-thread",
            )

    def test_code_brownfield_mismatch_is_rejected(self) -> None:
        record = self.code_record()
        record["code_contract"]["brownfield"] = True
        record["code_contract"]["alignment_group_id"] = "alignment-audits"
        with self.assertRaisesRegex(
            GateBlockedError, "readiness brownfield must equal"
        ):
            self.bridge.open_dispatch(
                authority=self.authority(
                    "open",
                    record,
                    session_name="bridge-test",
                    origin_ref="codex:test-thread",
                ),
                record=record,
                session_name="bridge-test",
                origin_ref="codex:test-thread",
            )

    def test_code_unknown_capability_permission_is_rejected(self) -> None:
        record = self.code_record()
        readiness_path = self.project / record["code_contract"]["readiness_ref"]
        readiness = json.loads(readiness_path.read_text(encoding="utf-8"))
        readiness["capability_profile"]["external_write"] = True
        readiness_path.write_text(
            json.dumps(readiness, sort_keys=True), encoding="utf-8"
        )
        record["code_contract"]["readiness_digest"] = (
            "sha256:" + hashlib.sha256(readiness_path.read_bytes()).hexdigest()
        )
        with self.assertRaisesRegex(
            GateBlockedError, "capability_profile must deny"
        ):
            self.bridge.open_dispatch(
                authority=self.authority(
                    "open",
                    record,
                    session_name="bridge-test",
                    origin_ref="codex:test-thread",
                ),
                record=record,
                session_name="bridge-test",
                origin_ref="codex:test-thread",
            )

    def test_close_preflight_prevents_yaml_side_effect_without_opening(self) -> None:
        self.bridge.prepare()
        self.bridge._append(self.opening)
        session = self.runtime.ensure_session(
            origin_digest=canonical_digest({"origin_ref": "codex:test-thread"}),
            name="bridge-test",
            actor_ref="operator:test",
            actor_authentication_ref=EVIDENCE_REF,
            actor_authentication_digest=EVIDENCE_DIGEST,
            idempotency_key="bridge-session",
        )
        self.runtime.link_session_dispatch(
            session_id=session["session"]["session_id"],
            dispatch_id=self.opening["dispatch_id"],
            actor_ref="operator:test",
            authorization_policy_ref="policy:test",
            authorization_policy_digest=canonical_digest({"policy": "test"}),
            authorization_evidence_ref=EVIDENCE_REF,
            authorization_evidence_digest=EVIDENCE_DIGEST,
            idempotency_key="test-link",
        )
        with self.assertRaisesRegex(Exception, "opening.*required"):
            self.close(session["session"]["session_id"])
        self.assertNotIn(
            f'  - close_of: "{self.opening["dispatch_id"]}"',
            self.ledger.read_text(encoding="utf-8"),
        )

    def test_yaml_only_open_and_close_crashes_converge_on_retry(self) -> None:
        fired: set[str] = set()

        def fail_once(name: str) -> None:
            if name in {"after_yaml_open", "after_yaml_close"} and name not in fired:
                fired.add(name)
                raise RuntimeError(name)

        self.bridge.failpoint = fail_once
        with self.assertRaisesRegex(RuntimeError, "after_yaml_open"):
            self.open()
        self.bridge.failpoint = lambda _: None
        opened = self.open()
        self.assertFalse(opened["yaml"]["changed"])

        self.bridge.failpoint = fail_once
        with self.assertRaisesRegex(RuntimeError, "after_yaml_close"):
            self.close(opened["session_id"])
        self.bridge.failpoint = lambda _: None
        closed = self.close(opened["session_id"], nonce="close-retry")
        self.assertFalse(closed["yaml"]["changed"])
        text = self.ledger.read_text(encoding="utf-8")
        self.assertEqual(
            text.count(f'  - dispatch_id: "{self.opening["dispatch_id"]}"'), 1
        )
        self.assertEqual(
            text.count(f'  - close_of: "{self.opening["dispatch_id"]}"'), 1
        )

    def test_exclusive_appender_lock_fails_closed(self) -> None:
        self.ledger.parent.mkdir(parents=True)
        lock = Path(str(self.ledger) + ".append.lock")
        lock.write_text("other-writer", encoding="utf-8")
        with self.assertRaisesRegex(GateBlockedError, "exclusive ledger lock"):
            self.open()
        self.assertFalse(self.ledger.exists())

    def test_supported_cli_preflight_capability_open_and_close(self) -> None:
        root, database, ledger = self.staged_cli_project()
        runtime = RuntimeService(RuntimeSettings(database, root, ledger))
        runtime.open()
        runtime.register_profiles()
        opening_path = root / "opening.json"
        opening_path.write_text(json.dumps(self.opening), encoding="utf-8")
        open_context = {
            "operation": "open",
            "dispatch_id": self.opening["dispatch_id"],
            "record_digest": canonical_digest(self.opening),
            "authorization_evidence_ref": EVIDENCE_REF,
            "authorization_evidence_digest": EVIDENCE_DIGEST,
            "nonce": "cli-open",
            "session_name": "cli-bridge-test",
            "origin_ref": "codex:cli-test",
        }
        open_capability = runtime.issue_capability(
            principal_id="operator:cli-test",
            action="orchestration.bridge.open",
            phase="bootstrap",
            context=open_context,
            expires_at="2099-01-01T00:00:00+00:00",
        )
        base = [
            "--project-dir",
            str(root),
            "--database",
            str(database),
            "--ledger",
            str(ledger),
        ]
        with patch.dict(
            "os.environ",
            {
                "ACI_LOCAL_PILOT_ENABLED": "1",
                "ACI_ORCHESTRATION_BRIDGE_TOKEN": open_capability["token"],
            },
            clear=False,
        ):
            opened = bridge_run(
                [
                    *base,
                    "open",
                    "--record",
                    str(opening_path),
                    "--session-name",
                    "cli-bridge-test",
                    "--origin-ref",
                    "codex:cli-test",
                ]
            )
        with self.assertRaises(AuthorizationError):
            runtime.capabilities.resolve(
                open_capability["token"],
                action="orchestration.bridge.open",
                phase="bootstrap",
            )

        closing_path = root / "closing.json"
        closing_path.write_text(json.dumps(self.closing), encoding="utf-8")
        close_context = {
            "operation": "close",
            "dispatch_id": self.opening["dispatch_id"],
            "record_digest": canonical_digest(self.closing),
            "authorization_evidence_ref": EVIDENCE_REF,
            "authorization_evidence_digest": EVIDENCE_DIGEST,
            "nonce": "cli-close",
            "session_id": opened["session_id"],
        }
        close_capability = runtime.issue_capability(
            principal_id="operator:cli-test",
            action="orchestration.bridge.close",
            phase="finalize",
            context=close_context,
            expires_at="2099-01-01T00:00:00+00:00",
        )
        with patch.dict(
            "os.environ",
            {
                "ACI_LOCAL_PILOT_ENABLED": "1",
                "ACI_ORCHESTRATION_BRIDGE_TOKEN": close_capability["token"],
            },
            clear=False,
        ):
            closed = bridge_run(
                [
                    *base,
                    "close",
                    "--record",
                    str(closing_path),
                    "--session-id",
                    opened["session_id"],
                ]
            )
        self.assertEqual(opened["status"], "launch-authorized")
        self.assertEqual(closed["status"], "closed")
        shown = runtime_run(
            [
                "show-orchestration-log",
                "--dispatch-id",
                self.opening["dispatch_id"],
                "--database",
                str(database),
                "--repo-root",
                str(root),
                "--ledger",
                str(ledger),
            ]
        )
        self.assertEqual(shown["status"], "closed")
        self.assertEqual(len(shown["events"]), 2)

    def test_supported_cli_rejects_missing_or_mismatched_capability(self) -> None:
        root, database, ledger = self.staged_cli_project()
        runtime = RuntimeService(RuntimeSettings(database, root, ledger))
        runtime.open()
        runtime.register_profiles()
        opening_path = root / "opening.json"
        opening_path.write_text(json.dumps(self.opening), encoding="utf-8")
        argv = [
            "--project-dir",
            str(root),
            "--database",
            str(database),
            "--ledger",
            str(ledger),
            "open",
            "--record",
            str(opening_path),
            "--session-name",
            "cli-bridge-test",
            "--origin-ref",
            "codex:cli-test",
        ]
        with patch.dict(
            "os.environ",
            {"ACI_LOCAL_PILOT_ENABLED": "1"},
            clear=False,
        ):
            os.environ.pop("ACI_ORCHESTRATION_BRIDGE_TOKEN", None)
            with self.assertRaisesRegex(GateBlockedError, "TOKEN is required"):
                bridge_run(argv)
        wrong = runtime.issue_capability(
            principal_id="operator:cli-test",
            action="orchestration.bridge.open",
            phase="bootstrap",
            context={
                "operation": "open",
                "dispatch_id": "different-dispatch",
                "record_digest": canonical_digest(self.opening),
                "authorization_evidence_ref": EVIDENCE_REF,
                "authorization_evidence_digest": EVIDENCE_DIGEST,
                "nonce": "wrong",
                "session_name": "cli-bridge-test",
                "origin_ref": "codex:cli-test",
            },
            expires_at="2099-01-01T00:00:00+00:00",
        )
        with patch.dict(
            "os.environ",
            {
                "ACI_LOCAL_PILOT_ENABLED": "1",
                "ACI_ORCHESTRATION_BRIDGE_TOKEN": wrong["token"],
            },
            clear=False,
        ):
            with self.assertRaisesRegex(GateBlockedError, "scope"):
                bridge_run(argv)
        self.assertNotIn(
            self.opening["dispatch_id"],
            ledger.read_text(encoding="utf-8"),
        )

        wrong_action = runtime.issue_capability(
            principal_id="operator:cli-test",
            action="orchestration.bridge.close",
            phase="finalize",
            context={
                "operation": "open",
                "dispatch_id": self.opening["dispatch_id"],
                "record_digest": canonical_digest(self.opening),
                "authorization_evidence_ref": EVIDENCE_REF,
                "authorization_evidence_digest": EVIDENCE_DIGEST,
                "nonce": "wrong-action",
                "session_name": "cli-bridge-test",
                "origin_ref": "codex:cli-test",
            },
            expires_at="2099-01-01T00:00:00+00:00",
        )
        with patch.dict(
            "os.environ",
            {
                "ACI_LOCAL_PILOT_ENABLED": "1",
                "ACI_ORCHESTRATION_BRIDGE_TOKEN": wrong_action["token"],
            },
            clear=False,
        ):
            with self.assertRaisesRegex(
                AuthorizationError, "invalid for action/phase"
            ):
                bridge_run(argv)

    def test_supported_cli_rejects_failed_source_manifest(self) -> None:
        root, database, ledger = self.staged_cli_project()
        manifest = (
            root
            / "docs/features/agent-provenance-telemetry/integration/stage-e/"
            "source-manifest.json"
        )
        manifest.write_text(
            manifest.read_text(encoding="utf-8") + "\n",
            encoding="utf-8",
        )
        opening_path = root / "opening.json"
        opening_path.write_text(json.dumps(self.opening), encoding="utf-8")
        with patch.dict(
            "os.environ",
            {
                "ACI_LOCAL_PILOT_ENABLED": "1",
                "ACI_ORCHESTRATION_BRIDGE_TOKEN": "not-reached",
            },
            clear=False,
        ):
            with self.assertRaisesRegex(
                GateBlockedError, "source manifest digest mismatch"
            ):
                bridge_run(
                    [
                        "--project-dir",
                        str(root),
                        "--database",
                        str(database),
                        "--ledger",
                        str(ledger),
                        "open",
                        "--record",
                        str(opening_path),
                        "--session-name",
                        "cli-bridge-test",
                        "--origin-ref",
                        "codex:cli-test",
                    ]
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
