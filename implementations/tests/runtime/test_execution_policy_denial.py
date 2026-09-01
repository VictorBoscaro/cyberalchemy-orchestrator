from __future__ import annotations

import ast
import json
import os
import socket
import subprocess
import tempfile
import time
import unittest
import urllib.request
from pathlib import Path
from unittest.mock import patch

from implementations.server.runtime.canonical import canonical_bytes, digest_bytes
from implementations.server.runtime.confirmation import build_confirmation_batch
from implementations.server.runtime.database import MIGRATION_NAMES, RuntimeDatabase
from implementations.server.runtime.errors import IntegrityError, RuntimeContractError
from implementations.server.runtime.execution_policy import (
    ExecutionPolicyContractError,
    parse_production_policy_document,
)
from implementations.server.runtime.journal import RuntimeJournal
from implementations.server.runtime.orchestration_bridge import LocalOrchestrationLoggingBridge
from implementations.server.runtime.reveal_delivery import validate_invocation_plan
from implementations.server.runtime.service import RuntimeService
from implementations.tests.runtime.policy_denial_harness import (
    ACTION_ATTEMPT_LABELS,
    AUTHORITY,
    DECISION,
    DENIAL_TABLE,
    EXPECTED_DENIAL_DIGEST,
    EXPECTED_RECEIPT_DIGEST,
    FAILPOINTS,
    ORACLE_DENIAL_KEY,
    PREIMAGE_SCHEMA,
    REASON_CODES,
    RECEIPT_SCHEMA,
    ExecutionPolicyFakeDenialHarness,
    SyntheticDenialConflict,
    SyntheticDenialValidationError,
)
from implementations.tests.runtime.policy_lineage_harness import (
    MEMBER_TABLE,
    RECEIPT_TABLE as LINEAGE_RECEIPT_TABLE,
    SyntheticPolicyLineageHarness,
    load_policy000_members,
)


HERE = Path(__file__).parent
SOURCE_FIXTURE = HERE / "execution_policy_oracle_v1.json"
DENIAL_FIXTURE = HERE / "execution_policy_denial_oracle_v1.json"
HARNESS_SOURCE = HERE / "policy_denial_harness.py"
SYNTHETIC_KEY = "policy-lineage-command-001"
LINEAGE_IDENTITY = "policy-lineage-oracle-001"
PRODUCTION_TABLES = (
    "confirmed_dispatches",
    "runs",
    "confirmed_turn_graphs",
    "agent_invocation_plans",
    "agent_execution_requests",
    "agent_attempts",
    "command_receipts",
    "events",
    "aggregate_heads",
    "effect_intents",
    "sandbox_launch_effects",
    "publication_candidates",
    "publication_receipts",
    "messages",
)


class ExecutionPolicyDenialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.oracle = json.loads(DENIAL_FIXTURE.read_text(encoding="utf-8"))
        cls.members = load_policy000_members(SOURCE_FIXTURE)

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.database_path = Path(self.temporary.name) / "runtime.sqlite3"
        forbidden = AssertionError("external/runtime effect boundary invoked")
        patchers = (
            patch.object(RuntimeJournal, "accept", side_effect=forbidden),
            patch.object(RuntimeService, "confirm_runtime_dispatch", side_effect=forbidden),
            patch.object(LocalOrchestrationLoggingBridge, "_append", side_effect=forbidden),
            patch.object(subprocess, "Popen", side_effect=forbidden),
            patch.object(subprocess, "run", side_effect=forbidden),
            patch.object(socket, "create_connection", side_effect=forbidden),
            patch.object(urllib.request, "urlopen", side_effect=forbidden),
            patch.object(os, "system", side_effect=forbidden),
        )
        self.effect_spies = []
        for patcher in patchers:
            spy = patcher.start()
            self.effect_spies.append(spy)
            self.addCleanup(patcher.stop)
            self.addCleanup(spy.assert_not_called)

    def make_source(self, path: Path | None = None) -> SyntheticPolicyLineageHarness:
        target_path = path or self.database_path
        harness = SyntheticPolicyLineageHarness(target_path)
        harness.persist_synthetic_lineage(
            synthetic_key=SYNTHETIC_KEY,
            lineage_identity=LINEAGE_IDENTITY,
            members=self.members,
        )
        return harness

    def harness(self, path: Path | None = None) -> ExecutionPolicyFakeDenialHarness:
        return ExecutionPolicyFakeDenialHarness(path or self.database_path)

    def deny(self, harness=None, **overrides):
        values = {
            "denial_key": ORACLE_DENIAL_KEY,
            "lineage_identity": LINEAGE_IDENTITY,
            "action_attempt_label": ACTION_ATTEMPT_LABELS[0],
        }
        values.update(overrides)
        return (harness or self.harness()).deny_synthetic_attempt(**values)

    @staticmethod
    def count(path: Path, table: str) -> int:
        with RuntimeDatabase(path).connect() as conn:
            return int(conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])

    def assert_quiet(self) -> None:
        for spy in self.effect_spies:
            spy.assert_not_called()

    def test_pol2_1_exact_denial_preimage_receipt_and_two_digests(self) -> None:
        self.assertEqual(self.oracle["authority"], AUTHORITY)
        self.assertEqual(tuple(self.oracle["input"]["action_attempt_labels"]), ACTION_ATTEMPT_LABELS)
        self.assertEqual(tuple(self.oracle["failpoints"]), FAILPOINTS)
        self.make_source()
        receipt = self.deny()
        self.assertEqual(receipt, self.oracle["expected_receipt"]["value"])
        self.assertEqual(canonical_bytes(receipt).decode(), self.oracle["expected_receipt"]["canonical_json"])
        self.assertEqual(digest_bytes(canonical_bytes(receipt)), EXPECTED_RECEIPT_DIGEST)
        self.assertEqual(self.oracle["expected_receipt"]["content_digest"], EXPECTED_RECEIPT_DIGEST)
        preimage = {
            "schema": PREIMAGE_SCHEMA,
            "authority": AUTHORITY,
            "lineage_identity": receipt["lineage_identity"],
            "lineage_unit_digest": receipt["lineage_unit_digest"],
            "resource_budget_digest": receipt["resource_budget_digest"],
            "sandbox_policy_digest": receipt["sandbox_policy_digest"],
            "decision": DECISION,
            "reason_codes": list(REASON_CODES),
        }
        self.assertEqual(canonical_bytes(preimage).decode(), self.oracle["denial_preimage"]["canonical_json"])
        self.assertEqual(digest_bytes(canonical_bytes(preimage)), EXPECTED_DENIAL_DIGEST)
        self.assertEqual(receipt["denial_digest"], EXPECTED_DENIAL_DIGEST)

    def test_pol2_2_source_must_reopen_and_remain_exact_deny_all(self) -> None:
        empty = Path(self.temporary.name) / "missing.sqlite3"
        with self.assertRaises(IntegrityError):
            self.deny(self.harness(empty))
        self.assertEqual(self.count(empty, DENIAL_TABLE), 0)

        source_harness = self.make_source()
        source = source_harness.reopen_synthetic_lineage(LINEAGE_IDENTITY)
        members = dict(source["members"])
        budget_fields = (
            "max_wall_time_ms", "max_input_tokens", "max_output_tokens",
            "max_tool_calls", "max_payload_bytes", "max_artifact_bytes",
        )
        mutations = []
        for field in budget_fields:
            value = json.loads(members["resource_budget"])
            value[field] = 1
            mutations.append(("resource_budget", canonical_bytes(value)))
        sandbox_mutations = (
            ("filesystem_scope", "read_roots", ["/tmp"]),
            ("filesystem_scope", "write_roots", ["/tmp"]),
            ("network_scope", "allowed_endpoints", ["https://example.invalid"]),
            ("process_scope", "allowed_executables", ["echo"]),
            ("process_scope", "max_child_processes", 1),
        )
        for outer, inner, changed in sandbox_mutations:
            value = json.loads(members["sandbox_policy"])
            value[outer][inner] = changed
            mutations.append(("sandbox_policy", canonical_bytes(value)))
        credentialed = json.loads(members["sandbox_policy"])
        credentialed["credential_refs"] = ["credential:test"]
        mutations.append(("sandbox_policy", canonical_bytes(credentialed)))

        for index, (name, changed_body) in enumerate(mutations):
            with self.subTest(index=index, name=name):
                changed = tuple((member_name, changed_body if member_name == name else body) for member_name, body in source["members"])
                projected = {"receipt": source["receipt"], "members": changed}
                with patch.object(SyntheticPolicyLineageHarness, "reopen_synthetic_lineage", return_value=projected):
                    with self.assertRaises((SyntheticDenialValidationError, ExecutionPolicyContractError)):
                        self.deny()
                self.assertEqual(self.count(self.database_path, DENIAL_TABLE), 0)

        with RuntimeDatabase(self.database_path).connect() as conn:
            artifact_id = conn.execute(
                f"SELECT artifact_id FROM {MEMBER_TABLE} WHERE lineage_identity=? ORDER BY ordinal LIMIT 1",
                (LINEAGE_IDENTITY,),
            ).fetchone()[0]
            conn.execute("PRAGMA foreign_keys=OFF")
            conn.execute("DELETE FROM artifacts WHERE artifact_id=?", (artifact_id,))
        with self.assertRaises(IntegrityError):
            self.deny()
        self.assertEqual(self.count(self.database_path, DENIAL_TABLE), 0)

    def test_pol2_3_labels_are_closed_scalar_selectors_not_identity(self) -> None:
        self.make_source()
        first = None
        for label in ACTION_ATTEMPT_LABELS:
            current = self.deny(action_attempt_label=label)
            first = first or current
            self.assertEqual(current, first)
        self.assertEqual(self.count(self.database_path, DENIAL_TABLE), 1)
        raw = canonical_bytes(first)
        self.assertTrue(all(label.encode() not in raw for label in ACTION_ATTEMPT_LABELS))
        for invalid in (None, "", "unknown", list(ACTION_ATTEMPT_LABELS), tuple(ACTION_ATTEMPT_LABELS), {"tool.call"}):
            with self.subTest(invalid=repr(invalid)):
                with self.assertRaises(SyntheticDenialValidationError):
                    self.deny(action_attempt_label=invalid)
        duplicate = list(ACTION_ATTEMPT_LABELS)
        duplicate[-1] = duplicate[0]
        with self.assertRaises(SyntheticDenialValidationError):
            ExecutionPolicyFakeDenialHarness._validate_label_corpus(duplicate)
        import implementations.tests.runtime.policy_denial_harness as module
        expanded = ACTION_ATTEMPT_LABELS + ("filesystem.delete",)
        with patch.object(module, "ACTION_ATTEMPT_LABELS", expanded):
            with self.assertRaises(SyntheticDenialValidationError):
                self.deny(action_attempt_label="filesystem.delete")

    def test_pol2_2a_persisted_lineage_faults_stop_before_l2_transaction(self) -> None:
        cases = ("missing_member", "reordered_members", "receipt_bytes", "unit_digest", "noncanonical_artifact")
        for index, case in enumerate(cases):
            with self.subTest(case=case):
                path = Path(self.temporary.name) / f"source-corrupt-{index}.sqlite3"
                self.make_source(path)
                harness = self.harness(path)
                database = RuntimeDatabase(path)
                if case == "missing_member":
                    with database.connect() as conn:
                        conn.execute("PRAGMA foreign_keys=OFF")
                        conn.execute(
                            f"DELETE FROM {MEMBER_TABLE} WHERE lineage_identity=? AND ordinal=0",
                            (LINEAGE_IDENTITY,),
                        )
                elif case == "reordered_members":
                    with database.write() as conn:
                        first_name = conn.execute(
                            f"SELECT name FROM {MEMBER_TABLE} WHERE lineage_identity=? AND ordinal=0",
                            (LINEAGE_IDENTITY,),
                        ).fetchone()[0]
                        second_name = conn.execute(
                            f"SELECT name FROM {MEMBER_TABLE} WHERE lineage_identity=? AND ordinal=1",
                            (LINEAGE_IDENTITY,),
                        ).fetchone()[0]
                        conn.execute(
                            f"UPDATE {MEMBER_TABLE} SET name='__temporary__' WHERE lineage_identity=? AND ordinal=0",
                            (LINEAGE_IDENTITY,),
                        )
                        conn.execute(
                            f"UPDATE {MEMBER_TABLE} SET name=? WHERE lineage_identity=? AND ordinal=1",
                            (first_name, LINEAGE_IDENTITY),
                        )
                        conn.execute(
                            f"UPDATE {MEMBER_TABLE} SET name=? WHERE lineage_identity=? AND ordinal=0",
                            (second_name, LINEAGE_IDENTITY),
                        )
                elif case == "receipt_bytes":
                    with database.write() as conn:
                        conn.execute(
                            f"UPDATE {LINEAGE_RECEIPT_TABLE} SET receipt_bytes=? WHERE lineage_identity=?",
                            (b"{}", LINEAGE_IDENTITY),
                        )
                elif case == "unit_digest":
                    with database.write() as conn:
                        conn.execute(
                            f"UPDATE {LINEAGE_RECEIPT_TABLE} SET unit_digest=? WHERE lineage_identity=?",
                            ("sha256:" + "f" * 64, LINEAGE_IDENTITY),
                        )
                else:
                    with database.write() as conn:
                        artifact_id, body = conn.execute(
                            f"""
                            SELECT a.artifact_id,a.body FROM artifacts a
                            JOIN {MEMBER_TABLE} m ON m.artifact_id=a.artifact_id
                            WHERE m.lineage_identity=? ORDER BY m.ordinal LIMIT 1
                            """,
                            (LINEAGE_IDENTITY,),
                        ).fetchone()
                        conn.execute(
                            "UPDATE artifacts SET body=?,size_bytes=? WHERE artifact_id=?",
                            (bytes(body) + b" ", len(body) + 1, artifact_id),
                        )
                with self.assertRaises(RuntimeContractError):
                    self.deny(harness)
                self.assertEqual(self.count(path, DENIAL_TABLE), 0)

        self.make_source()
        source = SyntheticPolicyLineageHarness(self.database_path).reopen_synthetic_lineage(LINEAGE_IDENTITY)
        import implementations.tests.runtime.policy_denial_harness as module
        with patch.object(SyntheticPolicyLineageHarness, "reopen_synthetic_lineage", return_value=source), patch.object(
            module, "parse_production_policy_document", return_value=object()
        ):
            with self.assertRaises(SyntheticDenialValidationError):
                self.deny()
        self.assertEqual(self.count(self.database_path, DENIAL_TABLE), 0)

    def test_pol2_2b_source_to_writer_race_fails_closed(self) -> None:
        self.make_source()
        harness = self.harness()
        original_candidate = harness._candidate_receipt

        def corrupt_after_source(denial_key, source):
            candidate = original_candidate(denial_key, source)
            with RuntimeDatabase(self.database_path).write() as conn:
                conn.execute(
                    f"UPDATE {LINEAGE_RECEIPT_TABLE} SET unit_digest=? WHERE lineage_identity=?",
                    ("sha256:" + "8" * 64, LINEAGE_IDENTITY),
                )
            return candidate

        with patch.object(harness, "_candidate_receipt", side_effect=corrupt_after_source):
            with self.assertRaises(IntegrityError):
                self.deny(harness)
        self.assertEqual(self.count(self.database_path, DENIAL_TABLE), 0)

    def test_pol2_2c_source_read_return_race_fails_closed(self) -> None:
        self.make_source()
        harness = self.harness()
        original_reopen = harness._reopen_source

        def corrupt_before_return(*args, **kwargs):
            source = original_reopen(*args, **kwargs)
            with RuntimeDatabase(self.database_path).write() as conn:
                conn.execute(
                    f"UPDATE {LINEAGE_RECEIPT_TABLE} SET unit_digest=? WHERE lineage_identity=?",
                    ("sha256:" + "7" * 64, LINEAGE_IDENTITY),
                )
            return source

        with patch.object(harness, "_reopen_source", side_effect=corrupt_before_return):
            with self.assertRaises(IntegrityError):
                self.deny(harness)
        self.assertEqual(self.count(self.database_path, DENIAL_TABLE), 0)

    def test_pol2_4_failpoints_are_atomic_and_lost_response_converges(self) -> None:
        for index, point in enumerate(FAILPOINTS):
            with self.subTest(point=point):
                path = Path(self.temporary.name) / f"fail-{index}.sqlite3"
                self.make_source(path)
                harness = self.harness(path)

                with self.assertRaisesRegex(RuntimeError, point):
                    self.deny(harness, failpoint=point)
                expected = 1 if point == "policy_denial.after_commit" else 0
                self.assertEqual(self.count(path, DENIAL_TABLE), expected)
                with RuntimeDatabase(path).connect() as conn:
                    self.assertEqual(conn.execute("PRAGMA foreign_key_check").fetchall(), [])
                if expected:
                    self.assertEqual(self.deny(self.harness(path)), self.oracle["expected_receipt"]["value"])
        self.make_source(Path(self.temporary.name) / "invalid-failpoint.sqlite3")
        invalid = self.harness(Path(self.temporary.name) / "invalid-failpoint.sqlite3")
        for value in ("unknown", lambda _point: None, 1):
            with self.subTest(invalid_failpoint=repr(value)):
                with self.assertRaises(SyntheticDenialValidationError):
                    self.deny(invalid, failpoint=value)

    def test_pol2_5_dual_replay_conflict_and_projection_drift(self) -> None:
        self.make_source()
        first = self.deny()
        self.assertEqual(self.deny(), first)
        self.assertEqual(self.deny(denial_key="unused-denial-key"), first)
        SyntheticPolicyLineageHarness(self.database_path).persist_synthetic_lineage(
            synthetic_key="other-lineage-command",
            lineage_identity="other-lineage",
            members=self.members,
        )
        with self.assertRaises(SyntheticDenialConflict):
            self.deny(lineage_identity="other-lineage")
        import implementations.tests.runtime.policy_denial_harness as module
        with patch.object(module, "DECISION", "allowed"):
            with self.assertRaises(SyntheticDenialConflict):
                self.deny()
            with self.assertRaises(SyntheticDenialConflict):
                self.deny(denial_key="another-unused-key")
        with patch.object(module, "REASON_CODES", tuple(reversed(REASON_CODES))):
            with self.assertRaises(SyntheticDenialConflict):
                self.deny()
            with self.assertRaises(SyntheticDenialConflict):
                self.deny(denial_key="another-unused-key")

        for field in (
            "lineage_unit_digest", "resource_budget_digest", "sandbox_policy_digest"
        ):
            for candidate_key in (ORACLE_DENIAL_KEY, "digest-axis-unused-key"):
                with self.subTest(field=field, candidate_key=candidate_key):
                    candidate_harness = self.harness()
                    original_source = candidate_harness._reopen_source(LINEAGE_IDENTITY)
                    changed_source = dict(original_source)
                    changed_source[field] = "sha256:" + "9" * 64
                    with patch.object(
                        candidate_harness,
                        "_reopen_source",
                        side_effect=[changed_source, original_source],
                    ):
                        with self.assertRaises(SyntheticDenialConflict):
                            self.deny(candidate_harness, denial_key=candidate_key)

        harness = self.harness()
        other_source = harness._reopen_source("other-lineage")
        other_receipt, other_raw, other_digest, other_receipt_digest = harness._candidate_receipt(
            "other-denial-key", other_source
        )
        with RuntimeDatabase(self.database_path).write() as conn:
            conn.execute(
                f"""
                INSERT INTO {DENIAL_TABLE}(
                  lineage_identity,denial_key,lineage_unit_digest,
                  resource_budget_digest,sandbox_policy_digest,denial_digest,
                  receipt_digest,receipt_bytes
                ) VALUES(?,?,?,?,?,?,?,?)
                """,
                (
                    "other-lineage", "other-denial-key",
                    other_receipt["lineage_unit_digest"],
                    other_receipt["resource_budget_digest"],
                    other_receipt["sandbox_policy_digest"], other_digest,
                    other_receipt_digest, other_raw,
                ),
            )
        with self.assertRaises(SyntheticDenialConflict):
            self.deny(denial_key=ORACLE_DENIAL_KEY, lineage_identity="other-lineage")
        with RuntimeDatabase(self.database_path).write() as conn:
            conn.execute(
                f"UPDATE {DENIAL_TABLE} SET receipt_bytes=? WHERE denial_key=?",
                (b"{}", ORACLE_DENIAL_KEY),
            )
        with self.assertRaises(IntegrityError):
            self.deny(denial_key=ORACLE_DENIAL_KEY, lineage_identity="other-lineage")
        self.assertEqual(self.count(self.database_path, DENIAL_TABLE), 2)

    def test_pol2_6_fresh_reopen_and_corruption_fail_closed(self) -> None:
        self.make_source()
        first = self.deny()
        self.assertEqual(self.harness().reopen_fake_denial(LINEAGE_IDENTITY), first)
        cases = (
            "receipt_digest", "denial_digest", "lineage_unit_digest",
            "resource_budget_digest", "sandbox_policy_digest",
            "receipt_noncanonical", "receipt_extra", "receipt_missing",
            "receipt_key", "receipt_lineage", "receipt_bytes_only", "receipt_and_digest",
            "row_key", "row_lineage", "missing_source_fk",
        )
        for index, case in enumerate(cases):
            with self.subTest(case=case):
                path = Path(self.temporary.name) / f"corrupt-{index}.sqlite3"
                self.make_source(path)
                harness = self.harness(path)
                receipt = self.deny(harness)
                if case == "row_lineage":
                    SyntheticPolicyLineageHarness(path).persist_synthetic_lineage(
                        synthetic_key="corrupt-other-source",
                        lineage_identity="corrupt-other-lineage",
                        members=self.members,
                    )
                database = RuntimeDatabase(path)
                if case in {
                    "receipt_digest", "denial_digest", "lineage_unit_digest",
                    "resource_budget_digest", "sandbox_policy_digest",
                }:
                    changed = "sha256:" + str(index) * 64
                    with database.write() as conn:
                        conn.execute(f"UPDATE {DENIAL_TABLE} SET {case}=?", (changed,))
                elif case.startswith("receipt_"):
                    changed_receipt = dict(receipt)
                    if case == "receipt_extra":
                        changed_receipt["extra"] = True
                    elif case == "receipt_missing":
                        changed_receipt.pop("decision")
                    elif case == "receipt_key":
                        changed_receipt["denial_key"] = "receipt-other-key"
                    elif case == "receipt_lineage":
                        changed_receipt["lineage_identity"] = "receipt-other-lineage"
                    elif case in {"receipt_bytes_only", "receipt_and_digest"}:
                        changed_receipt["decision"] = "allowed"
                    raw = canonical_bytes(changed_receipt)
                    if case == "receipt_noncanonical":
                        raw += b" "
                    with database.write() as conn:
                        conn.execute(
                            f"UPDATE {DENIAL_TABLE} SET receipt_bytes=?,receipt_digest=?",
                            (
                                raw,
                                EXPECTED_RECEIPT_DIGEST
                                if case == "receipt_bytes_only"
                                else digest_bytes(raw),
                            ),
                        )
                elif case == "row_key":
                    with database.write() as conn:
                        conn.execute(
                            f"UPDATE {DENIAL_TABLE} SET denial_key=?",
                            ("row-other-key",),
                        )
                elif case == "row_lineage":
                    with database.write() as conn:
                        conn.execute(
                            f"UPDATE {DENIAL_TABLE} SET lineage_identity=?",
                            ("corrupt-other-lineage",),
                        )
                else:
                    with database.connect() as conn:
                        conn.execute("PRAGMA foreign_keys=OFF")
                        conn.execute(
                            f"DELETE FROM {LINEAGE_RECEIPT_TABLE} WHERE lineage_identity=?",
                            (LINEAGE_IDENTITY,),
                        )
                with self.assertRaises(IntegrityError):
                    self.harness(path).reopen_fake_denial(LINEAGE_IDENTITY)
                with self.assertRaises(IntegrityError):
                    self.deny(self.harness(path))
                self.assertEqual(self.count(path, DENIAL_TABLE), 1)

    def test_pol2_7_every_label_has_zero_external_or_runtime_action(self) -> None:
        source = HARNESS_SOURCE.read_text(encoding="utf-8")
        tree = ast.parse(source)
        imported = {
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        }
        imported.update(
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module
        )
        self.assertEqual(
            imported,
            {
                "__future__",
                "sqlite3",
                "collections.abc",
                "pathlib",
                "typing",
                "implementations.server.runtime.canonical",
                "implementations.server.runtime.database",
                "implementations.server.runtime.errors",
                "implementations.server.runtime.execution_policy",
                "implementations.tests.runtime.policy_lineage_harness",
            },
        )
        self.make_source()
        harness = self.harness()
        forbidden = AssertionError("workload boundary invoked")
        original_read_bytes = Path.read_bytes

        def migration_reads_only(path):
            if path.suffix == ".sql" and "runtime/migrations" in path.as_posix():
                return original_read_bytes(path)
            raise forbidden

        with (
            patch.object(Path, "read_bytes", autospec=True, side_effect=migration_reads_only) as path_read,
            patch.object(Path, "write_bytes", side_effect=forbidden) as path_write,
            patch.object(Path, "unlink", side_effect=forbidden) as path_unlink,
            patch.object(Path, "rename", side_effect=forbidden) as path_rename,
            patch.object(time, "time", side_effect=forbidden) as wall_clock,
            patch.object(time, "monotonic", side_effect=forbidden) as monotonic,
            patch.object(os, "getenv", side_effect=forbidden) as getenv,
            patch.object(os, "putenv", side_effect=forbidden) as putenv,
        ):
            for label in ACTION_ATTEMPT_LABELS:
                self.deny(harness, action_attempt_label=label)
        self.assertGreater(path_read.call_count, 0)
        for spy in (path_write, path_unlink, path_rename, wall_clock, monotonic, getenv, putenv):
            spy.assert_not_called()
        self.assert_quiet()

    def test_pol2_8_one_l2_table_one_row_and_zero_production_authority(self) -> None:
        self.assertTrue(all(DENIAL_TABLE not in name for name in MIGRATION_NAMES))
        self.make_source()
        def l1_snapshot():
            with RuntimeDatabase(self.database_path).connect() as conn:
                return (
                    tuple(tuple(row) for row in conn.execute("SELECT * FROM artifacts ORDER BY artifact_id")),
                    tuple(tuple(row) for row in conn.execute(f"SELECT * FROM {LINEAGE_RECEIPT_TABLE}")),
                    tuple(tuple(row) for row in conn.execute(f"SELECT * FROM {MEMBER_TABLE} ORDER BY ordinal")),
                )

        before_artifacts, before_lineage_receipt, before_members = l1_snapshot()
        before = len(before_lineage_receipt), len(before_members)
        receipt = self.deny()
        self.assertEqual(l1_snapshot(), (before_artifacts, before_lineage_receipt, before_members))
        self.assertEqual(self.deny(), receipt)
        self.assertEqual(l1_snapshot(), (before_artifacts, before_lineage_receipt, before_members))
        with self.assertRaisesRegex(RuntimeError, "before_commit"):
            self.deny(failpoint="policy_denial.before_commit")
        self.assertEqual(l1_snapshot(), (before_artifacts, before_lineage_receipt, before_members))
        import implementations.tests.runtime.policy_denial_harness as module
        with patch.object(module, "DECISION", "allowed"):
            with self.assertRaises(SyntheticDenialConflict):
                self.deny()
        self.assertEqual(l1_snapshot(), (before_artifacts, before_lineage_receipt, before_members))
        self.assertEqual(self.harness().reopen_fake_denial(LINEAGE_IDENTITY), receipt)
        self.assertEqual(l1_snapshot(), (before_artifacts, before_lineage_receipt, before_members))
        self.assertEqual(before, (1, 7))
        self.assertEqual(
            (self.count(self.database_path, LINEAGE_RECEIPT_TABLE), self.count(self.database_path, MEMBER_TABLE)),
            before,
        )
        self.assertEqual(self.count(self.database_path, DENIAL_TABLE), 1)
        with RuntimeDatabase(self.database_path).connect() as conn:
            self.assertEqual(tuple(tuple(row) for row in conn.execute("SELECT * FROM artifacts ORDER BY artifact_id")), before_artifacts)
            self.assertEqual(tuple(tuple(row) for row in conn.execute(f"SELECT * FROM {LINEAGE_RECEIPT_TABLE}")), before_lineage_receipt)
            self.assertEqual(tuple(tuple(row) for row in conn.execute(f"SELECT * FROM {MEMBER_TABLE} ORDER BY ordinal")), before_members)
            l2_tables = {
                row["name"] for row in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'test_execution_policy_fake_denial_%'"
                )
            }
            production = {table: int(conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]) for table in PRODUCTION_TABLES}
        self.assertEqual(l2_tables, {DENIAL_TABLE})
        self.assertEqual(production, {table: 0 for table in PRODUCTION_TABLES})
        raw = canonical_bytes(receipt)
        with self.assertRaises(ExecutionPolicyContractError):
            parse_production_policy_document(raw)
        with self.assertRaises(RuntimeContractError):
            validate_invocation_plan(receipt)
        with self.assertRaises(RuntimeContractError):
            build_confirmation_batch(
                pending_sheet_bytes=raw,
                capability_resolution_bytes=raw,
                capability_resolution_artifact_id="art_invalid",
                trusted_issuer_context_bytes=raw,
                confirmation_observation_bytes=raw,
                identity_derivation_bytes=raw,
                payload_schema_bundle_bytes=raw,
                command_bytes=raw,
            )
        self.assert_quiet()

    def test_in_memory_sqlite_and_public_projection_fields_reject(self) -> None:
        with self.assertRaises(SyntheticDenialValidationError):
            ExecutionPolicyFakeDenialHarness(Path(":memory:"))
        self.make_source()
        with self.assertRaises(TypeError):
            self.harness().deny_synthetic_attempt(
                denial_key=ORACLE_DENIAL_KEY,
                lineage_identity=LINEAGE_IDENTITY,
                action_attempt_label=ACTION_ATTEMPT_LABELS[0],
                decision="allowed",
            )


if __name__ == "__main__":
    unittest.main()
