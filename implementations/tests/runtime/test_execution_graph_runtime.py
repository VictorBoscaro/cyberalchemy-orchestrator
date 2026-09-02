from __future__ import annotations

import base64
import copy
import json
import tempfile
import unittest
from pathlib import Path

from implementations.server.runtime.canonical import canonical_bytes, canonical_text, digest_bytes
from implementations.server.runtime.draft_graph_compiler import DraftGraphCompileError
from implementations.server.runtime.errors import ConflictError, GateBlockedError, IntegrityError, ValidationError
from implementations.server.runtime.execution_graph_runtime import (
    ExecutionGraphRuntime,
    LocalCompilationCandidate,
    LocalWorkerFailure,
    LocalWorkerResult,
    ScriptedLocalAdapter,
)


REPO = Path(__file__).resolve().parents[3]
FIXTURE_BUNDLE = REPO / (
    "docs/features/agents-communication-infra/development/refinement-runs/"
    "2026-09-01-execution-graph-authority/followups/"
    "IMPL-ACI-EXECUTION-RUNTIME-001/fixtures/local-execution"
)
MANIFEST_PATH = FIXTURE_BUNDLE / "manifest.json"
EXPECTED_INPUT_KEYS = {
    "compilation_context", "allocator_evidence", "allocator_trust", "draft_graph",
    "policy", "catalog", "resources", "role_registry", "agent_pool",
}


def load_fixture_bundle(manifest: dict | None = None) -> dict:
    value = json.loads(MANIFEST_PATH.read_bytes()) if manifest is None else manifest
    if value.get("schema") != "aci.local-execution-fixture-manifest@1":
        raise ValidationError("local execution fixture manifest schema is invalid")
    if set(value.get("inputs", {})) != EXPECTED_INPUT_KEYS:
        raise ValidationError("local execution fixture input set is invalid")
    raw: dict[str, bytes] = {}
    for name, record in value["inputs"].items():
        path = (FIXTURE_BUNDLE / record["path"]).resolve()
        if not path.is_relative_to(REPO.resolve()) or not path.is_file():
            raise IntegrityError(f"local execution fixture input is missing: {name}")
        body = path.read_bytes()
        if digest_bytes(body) != record["digest"]:
            raise IntegrityError(f"local execution fixture input digest mismatch: {name}")
        raw[name] = body

    def exact_artifact(key: str) -> tuple[dict, bytes]:
        record = value[key]
        path = (FIXTURE_BUNDLE / record["path"]).resolve()
        if not path.is_relative_to(FIXTURE_BUNDLE.resolve()) or not path.is_file():
            raise IntegrityError(f"local execution fixture artifact is missing: {key}")
        body = path.read_bytes()
        if digest_bytes(body) != record["digest"]:
            raise IntegrityError(f"local execution fixture artifact digest mismatch: {key}")
        return json.loads(body), body

    issuer_evidence, issuer_evidence_bytes = exact_artifact("issuer_evidence")
    trust, trust_bytes = exact_artifact("acceptance_trust")
    try:
        acceptance = base64.b64decode(value["acceptance"]["canonical_base64"], validate=True)
    except (KeyError, ValueError) as error:
        raise IntegrityError("local execution fixture acceptance encoding is invalid") from error
    if digest_bytes(acceptance) != value["acceptance"]["digest"]:
        raise IntegrityError("local execution fixture acceptance digest mismatch")
    acceptance_value = json.loads(acceptance)
    if canonical_bytes(acceptance_value) != acceptance:
        raise IntegrityError("local execution fixture acceptance is not canonical")
    if (
        trust.get("schema") != "aci.local-execution-acceptance-trust@1"
        or issuer_evidence.get("schema") != "aci.local-acceptance-issuer-evidence@1"
        or trust["issuer_ref"] != issuer_evidence["issuer_ref"]
        or trust["issuer_evidence_digest"] != digest_bytes(issuer_evidence_bytes)
        or trust["accepted_acceptance_digest"] != digest_bytes(acceptance)
        or acceptance_value["issuer_ref"] != trust["issuer_ref"]
        or acceptance_value["issuer_evidence_digest"] != trust["issuer_evidence_digest"]
    ):
        raise IntegrityError("local execution fixture trust chain is invalid")
    issuer_key = f"{trust['issuer_ref']['name']}@{trust['issuer_ref']['version']}"
    return {
        "raw": raw,
        "acceptance": acceptance,
        "acceptance_value": acceptance_value,
        "issuer_key": issuer_key,
        "issuer_evidence_digest": trust["issuer_evidence_digest"],
        "acceptance_digest": trust["accepted_acceptance_digest"],
        "expected_candidate": value["expected_candidate"],
        "manifest": value,
        "trust_bytes": trust_bytes,
    }


def result(output_id: str, value: object, rule_id: str, valid: bool = True) -> LocalWorkerResult:
    return LocalWorkerResult(outputs={output_id: value}, validations={rule_id: valid})


def successful_script() -> dict[str, list[LocalWorkerResult | LocalWorkerFailure]]:
    return {
        "node:review": [
            result(
                "output:review_report",
                {"findings": ["defect-a"]},
                "rule:review_has_evidence",
            )
        ],
        "node:correct": [
            result(
                "output:correction",
                {"patch": "fixed-a", "coverage": ["defect-a"]},
                "rule:correction_contract",
            )
        ],
        "node:verify": [
            result(
                "output:verification",
                {"verdict": "pass", "evidence": ["fixed-a"]},
                "rule:verification_evidence",
            )
        ],
    }


class ExecutionGraphRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp.name) / "runtime.sqlite3"
        self.bundle = load_fixture_bundle()
        self.raw = self.bundle["raw"]

    def tearDown(self) -> None:
        self.temp.cleanup()

    def runtime(
        self,
        adapter: ScriptedLocalAdapter,
        *,
        acceptance_digests: tuple[str, ...] | None = None,
    ) -> ExecutionGraphRuntime:
        digests = acceptance_digests or (self.bundle["acceptance_digest"],)
        return ExecutionGraphRuntime(
            self.database_path,
            adapter,
            trusted_acceptance_issuers={
                self.bundle["issuer_key"]: self.bundle["issuer_evidence_digest"]
            },
            trusted_acceptance_digests={self.bundle["issuer_key"]: digests},
        )

    def acceptance(self, candidate: LocalCompilationCandidate) -> bytes:
        expected = self.bundle["expected_candidate"]
        if (
            candidate.graph_digest == expected["graph_digest"]
            and candidate.compilation_authority_digest
            == expected["compilation_authority_digest"]
        ):
            return self.bundle["acceptance"]
        graph = json.loads(candidate.graph_bytes)
        authority = json.loads(candidate.compilation_authority_bytes)
        value = copy.deepcopy(self.bundle["acceptance_value"])
        value.update(
            dispatch_id=graph["dispatch_id"],
            revision=graph["revision"],
            allocation_id=authority["allocation_id"],
            graph_digest=candidate.graph_digest,
            compilation_authority_digest=candidate.compilation_authority_digest,
        )
        return canonical_bytes(value)

    def trust_for_test(self, runtime: ExecutionGraphRuntime, acceptance: bytes) -> None:
        """Explicitly configure one alternate negative/scheduler fixture; never the positive E2E."""
        current = runtime.trusted_acceptance_digests.get(self.bundle["issuer_key"], frozenset())
        runtime.trusted_acceptance_digests[self.bundle["issuer_key"]] = current | {
            digest_bytes(acceptance)
        }

    def candidate(
        self, runtime: ExecutionGraphRuntime, raw: dict[str, bytes] | None = None
    ) -> LocalCompilationCandidate:
        return runtime.compile_candidate(**(raw or self.raw))

    @staticmethod
    def rebind_candidate(
        candidate: LocalCompilationCandidate, graph: dict
    ) -> LocalCompilationCandidate:
        graph_bytes = canonical_bytes(graph)
        graph_digest = digest_bytes(graph_bytes)
        authority = json.loads(candidate.compilation_authority_bytes)
        authority["graph_digest"] = graph_digest
        authority_bytes = canonical_bytes(authority)
        return LocalCompilationCandidate(
            graph_bytes=graph_bytes,
            graph_digest=graph_digest,
            compilation_authority_bytes=authority_bytes,
            compilation_authority_digest=digest_bytes(authority_bytes),
        )

    def admit(self, runtime: ExecutionGraphRuntime, raw: dict[str, bytes] | None = None) -> dict:
        candidate = self.candidate(runtime, raw)
        acceptance = self.acceptance(candidate)
        if raw is not None:
            self.trust_for_test(runtime, acceptance)
        return runtime.admit_execution_graph(
            execution_graph=candidate.graph_bytes,
            compilation_authority=candidate.compilation_authority_bytes,
            acceptance=acceptance,
        )

    def test_real_json_compiles_executes_and_replays_byte_identically(self) -> None:
        adapter = ScriptedLocalAdapter(successful_script())
        runtime = self.runtime(adapter)
        candidate = self.candidate(runtime)
        self.assertEqual(candidate.graph_digest, self.bundle["expected_candidate"]["graph_digest"])
        self.assertEqual(
            candidate.compilation_authority_digest,
            self.bundle["expected_candidate"]["compilation_authority_digest"],
        )
        self.assertEqual(digest_bytes(self.acceptance(candidate)), self.bundle["acceptance_digest"])
        completed = runtime.execute_accepted_graph(
            execution_graph=candidate.graph_bytes,
            compilation_authority=candidate.compilation_authority_bytes,
            acceptance=self.acceptance(candidate),
        )
        admitted = completed
        self.assertEqual(completed["run"]["status"], "succeeded")
        self.assertEqual(
            [node["status"] for node in completed["nodes"]],
            ["succeeded", "succeeded", "succeeded"],
        )
        self.assertEqual(
            [(node["display_name"], node["role"]) for node in completed["nodes"]],
            [("Popper, Karl", "skeptic"), ("Dijkstra, Edsger W.", "coder"), ("Lamport, Leslie", "auditor")],
        )
        self.assertEqual(
            [assignment.node_id for assignment in adapter.calls],
            ["node:review", "node:correct", "node:verify"],
        )
        correction = adapter.calls[1]
        self.assertEqual(correction.inputs["input:review_findings"], {"findings": ["defect-a"]})
        verification = adapter.calls[2]
        self.assertEqual(
            set(verification.inputs),
            {"input:target", "input:review_findings", "input:candidate_correction"},
        )
        self.assertTrue(all(attempt["assignment_digest"] for attempt in completed["attempts"]))
        self.assertTrue(all(attempt["result_digest"] for attempt in completed["attempts"]))

        frozen = runtime.snapshot_bytes(admitted["run"]["run_id"])
        replay = self.admit(runtime)
        self.assertEqual(runtime.snapshot_bytes(replay["run"]["run_id"]), frozen)
        self.assertEqual(len(adapter.calls), 3)

        reopened = self.runtime(ScriptedLocalAdapter({}))
        self.assertEqual(reopened.snapshot_bytes(admitted["run"]["run_id"]), frozen)

    def test_execution_requires_separate_trusted_acceptance_before_any_write(self) -> None:
        runtime = self.runtime(ScriptedLocalAdapter({}))
        self.assertFalse(hasattr(runtime, "execute_draft_locally"))
        self.assertFalse(hasattr(runtime, "compile_and_admit"))
        candidate = self.candidate(runtime)
        with self.assertRaisesRegex(ValidationError, "acceptance shape"):
            runtime.admit_execution_graph(
                execution_graph=candidate.graph_bytes,
                compilation_authority=candidate.compilation_authority_bytes,
                acceptance=canonical_bytes({}),
            )
        self.assertFalse(self.database_path.exists())

        tampered = json.loads(self.acceptance(candidate))
        tampered["graph_digest"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(GateBlockedError, "acceptance bytes are not trusted"):
            runtime.admit_execution_graph(
                execution_graph=candidate.graph_bytes,
                compilation_authority=candidate.compilation_authority_bytes,
                acceptance=canonical_bytes(tampered),
            )
        self.assertFalse(self.database_path.exists())

        forged = json.loads(self.acceptance(candidate))
        forged["accepted_by"] = "principal:forged-by-caller"
        with self.assertRaisesRegex(GateBlockedError, "acceptance bytes are not trusted"):
            runtime.admit_execution_graph(
                execution_graph=candidate.graph_bytes,
                compilation_authority=candidate.compilation_authority_bytes,
                acceptance=canonical_bytes(forged),
            )
        self.assertFalse(self.database_path.exists())

        untrusted = ExecutionGraphRuntime(self.database_path, ScriptedLocalAdapter({}))
        with self.assertRaisesRegex(GateBlockedError, "issuer is not trusted"):
            untrusted.admit_execution_graph(
                execution_graph=candidate.graph_bytes,
                compilation_authority=candidate.compilation_authority_bytes,
                acceptance=self.acceptance(candidate),
            )
        self.assertFalse(self.database_path.exists())

    def test_fixture_manifest_rejects_missing_or_digest_drifted_artifacts(self) -> None:
        missing = copy.deepcopy(self.bundle["manifest"])
        missing["inputs"]["resources"]["path"] = "missing-resources.json"
        with self.assertRaisesRegex(IntegrityError, "input is missing: resources"):
            load_fixture_bundle(missing)

        drifted = copy.deepcopy(self.bundle["manifest"])
        drifted["inputs"]["resources"]["digest"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(IntegrityError, "input digest mismatch: resources"):
            load_fixture_bundle(drifted)

        acceptance_drift = copy.deepcopy(self.bundle["manifest"])
        acceptance_drift["acceptance"]["digest"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(IntegrityError, "acceptance digest mismatch"):
            load_fixture_bundle(acceptance_drift)

    def test_same_identity_with_different_graph_conflicts_without_mutation(self) -> None:
        runtime = self.runtime(ScriptedLocalAdapter(successful_script()))
        admitted = self.admit(runtime)
        before = runtime.snapshot_bytes(admitted["run"]["run_id"])
        changed = dict(self.raw)
        draft = json.loads(changed["draft_graph"])
        draft["objective"]["statement"] = "Different material objective."
        changed["draft_graph"] = canonical_text(draft).encode("utf-8")
        with self.assertRaisesRegex(ConflictError, "identity conflict"):
            self.admit(runtime, changed)
        self.assertEqual(runtime.snapshot_bytes(admitted["run"]["run_id"]), before)

    def test_ingestion_rejects_expected_digest_drift_before_writes(self) -> None:
        runtime = self.runtime(ScriptedLocalAdapter({}))
        candidate = self.candidate(runtime)
        acceptance = json.loads(self.acceptance(candidate))
        acceptance["graph_digest"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(GateBlockedError, "acceptance bytes are not trusted"):
            runtime.admit_execution_graph(
                execution_graph=candidate.graph_bytes,
                compilation_authority=candidate.compilation_authority_bytes,
                acceptance=canonical_bytes(acceptance),
            )
        self.assertFalse(self.database_path.exists())
        runtime.open()
        with runtime.database.connect() as conn:
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM local_execution_admissions").fetchone()[0], 0)

    def test_unsupported_cancellation_and_audit_choices_fail_closed_before_writes(self) -> None:
        runtime = self.runtime(ScriptedLocalAdapter({}))
        base = self.candidate(runtime)
        graph = json.loads(base.graph_bytes)
        graph["lifecycle"]["cancellation"] = "allow_running_nodes_to_stop"
        candidate = self.rebind_candidate(base, graph)
        with self.assertRaisesRegex(GateBlockedError, "cancel_running_nodes"):
            runtime.admit_execution_graph(
                execution_graph=candidate.graph_bytes,
                compilation_authority=candidate.compilation_authority_bytes,
                acceptance=self.acceptance(candidate),
            )
        self.assertFalse(self.database_path.exists())

        graph = json.loads(base.graph_bytes)
        graph["audit_requirements"]["record_results"] = False
        candidate = self.rebind_candidate(base, graph)
        with self.assertRaisesRegex(DraftGraphCompileError, "audit_requirements.record_results"):
            runtime.admit_execution_graph(
                execution_graph=candidate.graph_bytes,
                compilation_authority=candidate.compilation_authority_bytes,
                acceptance=self.acceptance(candidate),
            )
        self.assertFalse(self.database_path.exists())

    def test_missing_or_incompatible_pinned_receipt_schema_fails_before_writes(self) -> None:
        runtime = self.runtime(ScriptedLocalAdapter({}))
        base = self.candidate(runtime)
        graph = json.loads(base.graph_bytes)
        graph["audit_requirements"]["receipt_schema_member_id"] = "member:missing"
        candidate = self.rebind_candidate(base, graph)
        with self.assertRaisesRegex(DraftGraphCompileError, "receipt_schema_member_id"):
            runtime.admit_execution_graph(
                execution_graph=candidate.graph_bytes,
                compilation_authority=candidate.compilation_authority_bytes,
                acceptance=self.acceptance(candidate),
            )
        self.assertFalse(self.database_path.exists())

        graph = json.loads(base.graph_bytes)
        member = next(
            item for item in graph["content_members"] if item["member_id"] == "member:receipt_schema"
        )
        member["content"] = canonical_text(
            {
                "type": "object",
                "required": ["status"],
                "properties": {"status": {"enum": ["pass", "flag", "block"]}},
                "additionalProperties": False,
            }
        )
        member["digest"] = digest_bytes(member["content"].encode("utf-8"))
        candidate = self.rebind_candidate(base, graph)
        acceptance = self.acceptance(candidate)
        self.trust_for_test(runtime, acceptance)
        with self.assertRaisesRegex(IntegrityError, "pinned graph schema"):
            runtime.admit_execution_graph(
                execution_graph=candidate.graph_bytes,
                compilation_authority=candidate.compilation_authority_bytes,
                acceptance=acceptance,
            )
        self.assertFalse(self.database_path.exists())

    def test_durable_graph_authority_assignment_result_and_receipt_tamper_fail_closed(self) -> None:
        seed_runtime = self.runtime(ScriptedLocalAdapter({}))
        candidate = self.candidate(seed_runtime)
        acceptance = self.acceptance(candidate)

        for target in ("graph", "authority", "assignment", "result", "receipt"):
            with self.subTest(target=target), tempfile.TemporaryDirectory() as directory:
                adapter = ScriptedLocalAdapter(successful_script())
                runtime = ExecutionGraphRuntime(
                    Path(directory) / "runtime.sqlite3",
                    adapter,
                    trusted_acceptance_issuers={
                        self.bundle["issuer_key"]: self.bundle["issuer_evidence_digest"]
                    },
                    trusted_acceptance_digests={
                        self.bundle["issuer_key"]: self.bundle["acceptance_digest"]
                    },
                )
                admitted = runtime.admit_execution_graph(
                    execution_graph=candidate.graph_bytes,
                    compilation_authority=candidate.compilation_authority_bytes,
                    acceptance=acceptance,
                )
                run_id = admitted["run"]["run_id"]
                expected_calls = 0
                if target == "assignment":
                    assignment = runtime._prepare_next_assignment(run_id)
                    self.assertIsNotNone(assignment)
                elif target == "result":
                    runtime.execute(run_id, max_steps=1)
                    expected_calls = 1

                with runtime.database.write() as conn:
                    if target == "graph":
                        row = conn.execute(
                            """SELECT a.graph_bytes FROM local_execution_admissions a
                               JOIN local_execution_runs r ON r.admission_id=a.admission_id
                               WHERE r.run_id=?""",
                            (run_id,),
                        ).fetchone()
                        value = json.loads(bytes(row["graph_bytes"]))
                        value["nodes"][0]["instructions"] = "TAMPERED AFTER ADMISSION"
                        conn.execute(
                            """UPDATE local_execution_admissions SET graph_bytes=?
                               WHERE admission_id=(SELECT admission_id FROM local_execution_runs WHERE run_id=?)""",
                            (canonical_bytes(value), run_id),
                        )
                    elif target == "authority":
                        row = conn.execute(
                            """SELECT a.authority_json FROM local_execution_admissions a
                               JOIN local_execution_runs r ON r.admission_id=a.admission_id
                               WHERE r.run_id=?""",
                            (run_id,),
                        ).fetchone()
                        value = json.loads(row["authority_json"])
                        value["acceptance"]["accepted_by"] = "principal:tampered"
                        conn.execute(
                            """UPDATE local_execution_admissions SET authority_json=?
                               WHERE admission_id=(SELECT admission_id FROM local_execution_runs WHERE run_id=?)""",
                            (canonical_text(value), run_id),
                        )
                    elif target == "assignment":
                        row = conn.execute(
                            "SELECT attempt_id,assignment_json FROM local_execution_attempts WHERE run_id=?",
                            (run_id,),
                        ).fetchone()
                        value = json.loads(row["assignment_json"])
                        value["instructions"] = "TAMPERED ASSIGNMENT"
                        conn.execute(
                            "UPDATE local_execution_attempts SET assignment_json=? WHERE attempt_id=?",
                            (canonical_text(value), row["attempt_id"]),
                        )
                    elif target == "result":
                        row = conn.execute(
                            "SELECT attempt_id,result_json FROM local_execution_attempts WHERE run_id=?",
                            (run_id,),
                        ).fetchone()
                        value = json.loads(row["result_json"])
                        value["outputs"]["output:review_report"]["findings"] = ["tampered"]
                        conn.execute(
                            "UPDATE local_execution_attempts SET result_json=? WHERE attempt_id=?",
                            (canonical_text(value), row["attempt_id"]),
                        )
                    else:
                        row = conn.execute(
                            "SELECT receipt_id,receipt_json FROM local_execution_receipts WHERE run_id=? ORDER BY sequence LIMIT 1",
                            (run_id,),
                        ).fetchone()
                        value = json.loads(row["receipt_json"])
                        value["kind"] = "tampered"
                        conn.execute(
                            "UPDATE local_execution_receipts SET receipt_json=? WHERE receipt_id=?",
                            (canonical_text(value), row["receipt_id"]),
                        )

                with self.assertRaisesRegex(IntegrityError, "digest mismatch"):
                    runtime.execute(run_id, max_steps=1)
                self.assertEqual(len(adapter.calls), expected_calls)

    def test_correction_validation_failure_retries_with_new_attempt(self) -> None:
        script = successful_script()
        script["node:correct"] = [
            result(
                "output:correction",
                {"patch": "bad", "coverage": ["defect-a"]},
                "rule:correction_contract",
                valid=False,
            ),
            result(
                "output:correction",
                {"patch": "fixed-a", "coverage": ["defect-a"]},
                "rule:correction_contract",
            ),
        ]
        runtime = self.runtime(ScriptedLocalAdapter(script))
        admitted = self.admit(runtime)
        completed = runtime.execute(admitted["run"]["run_id"])
        self.assertEqual(completed["run"]["status"], "succeeded")
        correction_attempts = [
            attempt for attempt in completed["attempts"] if attempt["node_id"] == "node:correct"
        ]
        self.assertEqual(
            [(attempt["attempt_number"], attempt["status"]) for attempt in correction_attempts],
            [(1, "validation_failed"), (2, "succeeded")],
        )
        self.assertTrue(any(
            item["receipt"]["kind"] == "node_retry_scheduled"
            for item in completed["receipts"]
        ))

    def test_worker_failure_fails_fast_and_skips_downstream(self) -> None:
        script = successful_script()
        script["node:review"] = [LocalWorkerFailure("fixture_worker_failed")]
        runtime = self.runtime(ScriptedLocalAdapter(script))
        admitted = self.admit(runtime)
        completed = runtime.execute(admitted["run"]["run_id"])
        self.assertEqual(completed["run"]["status"], "failed")
        self.assertEqual(
            [node["status"] for node in completed["nodes"]],
            ["failed", "skipped", "skipped"],
        )
        self.assertEqual(completed["attempts"][0]["failure_code"], "fixture_worker_failed")

    def test_any_predecessor_activates_on_first_route_event_without_hidden_barrier(self) -> None:
        raw = dict(self.raw)
        draft = json.loads(raw["draft_graph"])
        review, correct, verify = draft["nodes"]
        verify["inputs"] = [
            item
            for item in verify["inputs"]
            if item["source"].get("node_key") != "correct"
        ]
        verify["start_when"] = "any_predecessor_succeeded"
        draft["nodes"] = [review, verify, correct]
        draft["edges"] = [
            {
                "key": "correct_then_verify",
                "from_node_key": "correct",
                "to_node_key": "verify",
                "kind": "control",
                "condition": "on_success",
            }
        ]
        raw["draft_graph"] = canonical_bytes(draft)
        adapter = ScriptedLocalAdapter(successful_script())
        runtime = self.runtime(adapter)
        admitted = self.admit(runtime, raw)
        completed = runtime.execute(admitted["run"]["run_id"])
        self.assertEqual([call.node_id for call in adapter.calls], ["node:review", "node:verify"])
        self.assertEqual(completed["run"]["status"], "succeeded")
        self.assertEqual(
            {node["node_id"]: node["status"] for node in completed["nodes"]},
            {"node:review": "succeeded", "node:verify": "succeeded", "node:correct": "skipped"},
        )

    def test_verification_flag_takes_explicit_stop_branch(self) -> None:
        script = successful_script()
        script["node:verify"] = [
            result(
                "output:verification",
                {"verdict": "flag", "evidence": ["needs-human"]},
                "rule:verification_evidence",
            )
        ]
        runtime = self.runtime(ScriptedLocalAdapter(script))
        admitted = self.admit(runtime)
        completed = runtime.execute(admitted["run"]["run_id"])
        self.assertEqual(completed["run"]["status"], "stopped")
        self.assertEqual(completed["run"]["terminal_reason"], "verification_flag")
        self.assertEqual(completed["nodes"][2]["status"], "stopped")

    def test_verification_block_takes_explicit_failure_branch(self) -> None:
        script = successful_script()
        script["node:verify"] = [
            result(
                "output:verification",
                {"verdict": "block", "evidence": ["unsafe"]},
                "rule:verification_evidence",
            )
        ]
        runtime = self.runtime(ScriptedLocalAdapter(script))
        admitted = self.admit(runtime)
        completed = runtime.execute(admitted["run"]["run_id"])
        self.assertEqual(completed["run"]["status"], "failed")
        self.assertEqual(completed["run"]["terminal_reason"], "verification_block")
        self.assertEqual(completed["nodes"][2]["status"], "failed")

    def test_cancellation_after_one_step_preserves_completed_node(self) -> None:
        runtime = self.runtime(ScriptedLocalAdapter(successful_script()))
        admitted = self.admit(runtime)
        paused = runtime.execute(admitted["run"]["run_id"], max_steps=1)
        self.assertEqual(paused["run"]["status"], "running")
        self.assertEqual(paused["nodes"][0]["status"], "succeeded")
        requested = runtime.cancel(admitted["run"]["run_id"], reason="fixture_cancel")
        self.assertTrue(requested["run"]["cancel_requested"])
        cancelled = runtime.execute(admitted["run"]["run_id"])
        self.assertEqual(cancelled["run"]["status"], "cancelled")
        self.assertEqual(
            [node["status"] for node in cancelled["nodes"]],
            ["succeeded", "cancelled", "cancelled"],
        )

    def test_migration_016_is_idempotent(self) -> None:
        runtime = self.runtime(ScriptedLocalAdapter({}))
        first = runtime.open()
        second = runtime.open()
        self.assertEqual(first[-1]["name"], "016_local_execution_graph_runtime.sql")
        self.assertEqual(second, [])
        with runtime.database.connect() as conn:
            self.assertEqual(conn.execute("PRAGMA user_version").fetchone()[0], 16)
            tables = {
                row[0]
                for row in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'local_execution_%'"
                )
            }
        self.assertEqual(
            tables,
            {
                "local_execution_admissions",
                "local_execution_runs",
                "local_execution_nodes",
                "local_execution_attempts",
                "local_execution_receipts",
            },
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
