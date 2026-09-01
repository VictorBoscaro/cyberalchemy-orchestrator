from __future__ import annotations

import ast
import json
import os
import socket
import subprocess
import tempfile
import unittest
import urllib.request
from pathlib import Path
from unittest.mock import patch

from implementations.server.runtime.artifacts import ArtifactStore
from implementations.server.runtime.canonical import canonical_bytes, digest_bytes
from implementations.server.runtime.database import MIGRATION_NAMES, RuntimeDatabase
from implementations.server.runtime.errors import IntegrityError
from implementations.server.runtime.execution_policy import (
    ExecutionPolicyContractError,
    parse_execution_authority_fence,
    parse_production_policy_document,
)
from implementations.server.runtime.journal import RuntimeJournal
from implementations.server.runtime.orchestration_bridge import LocalOrchestrationLoggingBridge
from implementations.server.runtime.service import RuntimeService
from implementations.tests.runtime.policy_lineage_harness import (
    AUTHORITY,
    EXPECTED_MEMBER_DIGESTS,
    MEMBER_ORDER,
    MEMBER_TABLE,
    RECEIPT_SCHEMA,
    RECEIPT_TABLE,
    UNIT_SCHEMA,
    SyntheticLineageConflict,
    SyntheticLineageValidationError,
    SyntheticPolicyLineageHarness,
    load_policy000_members,
)


HERE = Path(__file__).parent
SOURCE_FIXTURE = HERE / "execution_policy_oracle_v1.json"
LINEAGE_FIXTURE = HERE / "execution_policy_lineage_oracle_v1.json"
HARNESS_SOURCE = HERE / "policy_lineage_harness.py"
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
INDEPENDENT_DIGEST_AUTHORITY = dict(zip(MEMBER_ORDER, EXPECTED_MEMBER_DIGESTS))


class ExecutionPolicyLineageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.oracle = json.loads(LINEAGE_FIXTURE.read_text(encoding="utf-8"))
        cls.members = load_policy000_members(SOURCE_FIXTURE)
        cls.synthetic_key = cls.oracle["input"]["synthetic_key"]
        cls.lineage_identity = cls.oracle["input"]["lineage_identity"]

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

    def harness(self) -> SyntheticPolicyLineageHarness:
        return SyntheticPolicyLineageHarness(self.database_path)

    def persist(self, harness=None, **overrides):
        target = harness or self.harness()
        values = {
            "synthetic_key": self.synthetic_key,
            "lineage_identity": self.lineage_identity,
            "members": self.members,
        }
        values.update(overrides)
        return target.persist_synthetic_lineage(**values)

    def counts(self, database_path=None, tables=()) -> dict[str, int]:
        database = RuntimeDatabase(database_path or self.database_path)
        with database.connect() as conn:
            return {
                table: int(conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])
                for table in tables
            }

    def assert_effect_spies_quiet(self) -> None:
        for spy in self.effect_spies:
            spy.assert_not_called()

    def assert_inventory(
        self,
        database_path=None,
        *,
        artifacts: int,
        receipts: int,
        members: int,
    ) -> None:
        tables = ("artifacts", RECEIPT_TABLE, MEMBER_TABLE) + PRODUCTION_TABLES
        expected = {table: 0 for table in tables}
        expected.update(
            {"artifacts": artifacts, RECEIPT_TABLE: receipts, MEMBER_TABLE: members}
        )
        self.assertEqual(self.counts(database_path, tables), expected)
        self.assert_effect_spies_quiet()

    def test_pol1_1_exact_closed_seven_member_unit_and_mutations(self) -> None:
        self.assertEqual(
            set(self.oracle),
            {"schema", "authority", "source_fixture", "input", "expected_receipt", "failpoints"},
        )
        self.assertEqual(self.oracle["schema"], "aci.execution-policy-synthetic-lineage-oracle@1")
        self.assertEqual(self.oracle["authority"], AUTHORITY)
        self.assertEqual(self.oracle["source_fixture"], SOURCE_FIXTURE.name)
        self.assertEqual(
            set(self.oracle["input"]),
            {"synthetic_key", "lineage_identity", "ordered_member_names"},
        )
        self.assertEqual(tuple(self.oracle["input"]["ordered_member_names"]), MEMBER_ORDER)
        self.assertEqual(tuple(name for name, _body in self.members), MEMBER_ORDER)
        for name, body in self.members:
            self.assertEqual(digest_bytes(body), INDEPENDENT_DIGEST_AUTHORITY[name])

        harness = self.harness()
        original_prepare = ArtifactStore.prepare
        prepare_calls: list[str] = []

        def observing_prepare(store, body, **kwargs):
            prepare_calls.append(kwargs["schema_ref"])
            return original_prepare(store, body, **kwargs)

        def at_begin(name):
            if name == "policy_lineage.after_begin":
                self.assertEqual(len(prepare_calls), 7)

        with patch.object(ArtifactStore, "prepare", autospec=True, side_effect=observing_prepare), patch.object(
            ArtifactStore, "commit", side_effect=AssertionError("per-artifact commit forbidden")
        ) as forbidden_commit:
            receipt = self.persist(harness, failpoint=at_begin)
        forbidden_commit.assert_not_called()
        self.assertEqual(receipt, self.oracle["expected_receipt"])
        self.assertEqual(set(receipt), {
            "schema", "authority", "synthetic_key", "lineage_identity", "members", "unit_digest"
        })
        self.assertEqual(receipt["schema"], RECEIPT_SCHEMA)
        self.assertEqual(receipt["authority"], AUTHORITY)
        preimage = {
            "schema": UNIT_SCHEMA,
            "authority": AUTHORITY,
            "lineage_identity": self.lineage_identity,
            "members": receipt["members"],
        }
        self.assertEqual(receipt["unit_digest"], digest_bytes(canonical_bytes(preimage)))
        self.assert_inventory(artifacts=7, receipts=1, members=7)

        mutations = []
        mutations.append(self.members[:-1])
        mutations.append(self.members + (("extra", b"{}"),))
        renamed = list(self.members)
        renamed[0] = ("renamed", renamed[0][1])
        mutations.append(tuple(renamed))
        reordered = list(self.members)
        reordered[0], reordered[1] = reordered[1], reordered[0]
        mutations.append(tuple(reordered))
        for index in range(7):
            drifted = list(self.members)
            drifted[index] = (drifted[index][0], drifted[index][1] + b" ")
            mutations.append(tuple(drifted))
        canonical_drift = list(self.members)
        budget = json.loads(canonical_drift[2][1])
        budget["max_wall_time_ms"] = 1
        canonical_drift[2] = (canonical_drift[2][0], canonical_bytes(budget))
        mutations.append(tuple(canonical_drift))
        swapped_targets = list(self.members)
        swapped_targets[0] = (swapped_targets[0][0], self.members[1][1])
        swapped_targets[1] = (swapped_targets[1][0], self.members[0][1])
        mutations.append(tuple(swapped_targets))
        noncanonical_oracle = list(self.members)
        noncanonical_oracle[4] = (
            noncanonical_oracle[4][0],
            b'{"schema":"aci.execution-policy-oracle-fixture@1",'
            + noncanonical_oracle[4][1][1:-1]
            + b"}",
        )
        mutations.append(tuple(noncanonical_oracle))
        for mutation in mutations:
            with self.subTest(mutation=tuple(name for name, _ in mutation)):
                other_path = Path(self.temporary.name) / f"mutation-{len(str(mutation))}-{id(mutation)}.sqlite3"
                other = SyntheticPolicyLineageHarness(other_path)
                with self.assertRaises(SyntheticLineageValidationError):
                    other.persist_synthetic_lineage(
                        synthetic_key="mutation-key",
                        lineage_identity="mutation-identity",
                        members=mutation,
                    )
                self.assert_inventory(
                    other_path, artifacts=0, receipts=0, members=0
                )

    def test_pol1_2_every_transaction_failpoint_is_all_or_none(self) -> None:
        failpoints = self.oracle["failpoints"]
        self.assertEqual(len(failpoints), 18)
        self.assertEqual(failpoints[-1], "policy_lineage.after_commit")
        for index, point in enumerate(failpoints):
            with self.subTest(point=point):
                path = Path(self.temporary.name) / f"fail-{index}.sqlite3"
                harness = SyntheticPolicyLineageHarness(path)

                def fail(name, target=point):
                    if name == target:
                        raise RuntimeError(target)

                with self.assertRaisesRegex(RuntimeError, point):
                    harness.persist_synthetic_lineage(
                        synthetic_key=self.synthetic_key,
                        lineage_identity=self.lineage_identity,
                        members=self.members,
                        failpoint=fail,
                    )
                reopened = SyntheticPolicyLineageHarness(path)
                expected = (
                    {"artifacts": 7, RECEIPT_TABLE: 1, MEMBER_TABLE: 7}
                    if point == "policy_lineage.after_commit"
                    else {"artifacts": 0, RECEIPT_TABLE: 0, MEMBER_TABLE: 0}
                )
                self.assert_inventory(
                    path,
                    artifacts=expected["artifacts"],
                    receipts=expected[RECEIPT_TABLE],
                    members=expected[MEMBER_TABLE],
                )
                if point == "policy_lineage.after_commit":
                    self.assertEqual(
                        reopened.reopen_synthetic_lineage(self.lineage_identity)["receipt"],
                        self.oracle["expected_receipt"],
                    )
                    self.assert_inventory(
                        path, artifacts=7, receipts=1, members=7
                    )

    def test_pol1_3_synthetic_key_replay_and_conflict(self) -> None:
        harness = self.harness()
        first = self.persist(harness)
        self.assert_inventory(artifacts=7, receipts=1, members=7)
        replay = self.persist(harness)
        self.assertEqual(canonical_bytes(replay), canonical_bytes(first))
        self.assert_inventory(artifacts=7, receipts=1, members=7)
        with self.assertRaises(SyntheticLineageConflict):
            self.persist(harness, lineage_identity="policy-lineage-other-identity")
        self.assert_inventory(artifacts=7, receipts=1, members=7)

    def test_pol1_4_lineage_identity_replay_and_conflict(self) -> None:
        harness = self.harness()
        first = self.persist(harness)
        self.assert_inventory(artifacts=7, receipts=1, members=7)
        replay = self.persist(harness, synthetic_key="unused-transport-key")
        self.assertEqual(replay, first)
        self.assertEqual(replay["synthetic_key"], self.synthetic_key)
        self.assert_inventory(artifacts=7, receipts=1, members=7)
        drifted = list(self.members)
        budget = json.loads(drifted[2][1])
        budget["max_wall_time_ms"] = 1
        drifted[2] = (drifted[2][0], canonical_bytes(budget))
        with self.assertRaises(SyntheticLineageConflict):
            self.persist(
                harness,
                synthetic_key="another-unused-key",
                members=tuple(drifted),
            )
        self.assert_inventory(artifacts=7, receipts=1, members=7)

    def test_pol1_5_lost_response_fresh_retry_returns_first_receipt(self) -> None:
        harness = self.harness()

        def lost_response(name):
            if name == "policy_lineage.after_commit":
                raise RuntimeError(name)

        with self.assertRaisesRegex(RuntimeError, "after_commit"):
            self.persist(harness, failpoint=lost_response)
        self.assert_inventory(artifacts=7, receipts=1, members=7)
        fresh = SyntheticPolicyLineageHarness(self.database_path)
        recovered = self.persist(fresh)
        self.assertEqual(recovered, self.oracle["expected_receipt"])
        self.assert_inventory(artifacts=7, receipts=1, members=7)

    def test_pol1_6_close_reopen_reproduces_exact_bytes_and_receipt(self) -> None:
        first = self.persist()
        self.assert_inventory(artifacts=7, receipts=1, members=7)
        reopened = SyntheticPolicyLineageHarness(self.database_path)
        unit = reopened.reopen_synthetic_lineage(self.lineage_identity)
        self.assertEqual(unit["receipt"], first)
        self.assertEqual(unit["members"], self.members)
        for (name, body), binding in zip(unit["members"], first["members"]):
            self.assertEqual(binding["name"], name)
            self.assertEqual(binding["content_digest"], digest_bytes(body))
            self.assertEqual(binding["artifact_id"], "art_" + digest_bytes(body)[7:39])
        self.assert_inventory(artifacts=7, receipts=1, members=7)

        with RuntimeDatabase(self.database_path).connect() as conn:
            artifact_id = first["members"][0]["artifact_id"]
            conn.execute("PRAGMA foreign_keys=OFF")
            conn.execute("DELETE FROM artifacts WHERE artifact_id=?", (artifact_id,))
        with self.assertRaises(IntegrityError):
            reopened.reopen_synthetic_lineage(self.lineage_identity)
        self.assert_inventory(artifacts=6, receipts=1, members=7)

    def test_pol1_6a_receipt_byte_tamper_blocks_retry_and_reopen(self) -> None:
        first = self.persist()
        tampered = dict(first)
        tampered["synthetic_key"] = "tampered-key"
        with RuntimeDatabase(self.database_path).write() as conn:
            conn.execute(
                f"UPDATE {RECEIPT_TABLE} SET receipt_bytes=? WHERE lineage_identity=?",
                (canonical_bytes(tampered), self.lineage_identity),
            )

        with self.assertRaises(IntegrityError):
            self.persist(self.harness())
        with self.assertRaises(IntegrityError):
            self.harness().reopen_synthetic_lineage(self.lineage_identity)
        self.assert_inventory(artifacts=7, receipts=1, members=7)

    def test_pol1_6b_row_and_receipt_key_mismatch_blocks_retry_and_reopen(self) -> None:
        self.persist()
        with RuntimeDatabase(self.database_path).write() as conn:
            conn.execute(
                f"UPDATE {RECEIPT_TABLE} SET synthetic_key=? WHERE lineage_identity=?",
                ("tampered-row-key", self.lineage_identity),
            )

        with self.assertRaises(IntegrityError):
            self.persist(self.harness())
        with self.assertRaises(IntegrityError):
            self.harness().reopen_synthetic_lineage(self.lineage_identity)
        self.assert_inventory(artifacts=7, receipts=1, members=7)

    def test_pol1_7_production_parser_rejection_survives_persistence(self) -> None:
        by_name = dict(self.members)
        for raw, parser in (
            (by_name["combined_oracle"], parse_production_policy_document),
            (by_name["harness_fence_document"], parse_execution_authority_fence),
        ):
            with self.assertRaises(ExecutionPolicyContractError):
                parser(raw)
        self.assert_effect_spies_quiet()
        self.persist()
        self.assert_inventory(artifacts=7, receipts=1, members=7)
        reopened = self.harness().reopen_synthetic_lineage(self.lineage_identity)
        reopened_by_name = dict(reopened["members"])
        for raw, parser in (
            (reopened_by_name["combined_oracle"], parse_production_policy_document),
            (reopened_by_name["harness_fence_document"], parse_execution_authority_fence),
        ):
            with self.assertRaises(ExecutionPolicyContractError):
                parser(raw)
        self.assert_inventory(artifacts=7, receipts=1, members=7)

    def test_pol1_8_two_local_tables_zero_authority_rows_and_external_effects(self) -> None:
        source = HARNESS_SOURCE.read_text(encoding="utf-8")
        tree = ast.parse(source)
        imported = {
            alias.name.split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        }
        imported.update(
            node.module.split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module
        )
        self.assertTrue(imported.isdisjoint({"subprocess", "socket", "urllib", "requests"}))
        self.assertTrue(all(RECEIPT_TABLE not in name and MEMBER_TABLE not in name for name in MIGRATION_NAMES))

        self.persist()

        with RuntimeDatabase(self.database_path).connect() as conn:
            local_tables = {
                row["name"]
                for row in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'test_execution_policy_lineage_%'"
                )
            }
        self.assertEqual(local_tables, {RECEIPT_TABLE, MEMBER_TABLE})
        self.assert_inventory(artifacts=7, receipts=1, members=7)


if __name__ == "__main__":
    unittest.main()
