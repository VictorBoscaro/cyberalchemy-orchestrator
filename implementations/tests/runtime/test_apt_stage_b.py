from __future__ import annotations

import shutil
import socket
import subprocess
import tempfile
import threading
import time
import unittest
import json
import os
import urllib.request
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from implementations.server.runtime.api import create_provenance_router
from implementations.server.runtime.errors import (
    AuthorizationError,
    ConflictError,
    IdempotencyConflict,
    ValidationError,
)
from implementations.server.runtime.canonical import canonical_digest
from implementations.server.runtime.provenance import ProvenanceService
from implementations.server.runtime.service import RuntimeService, RuntimeSettings


REPO = Path(__file__).resolve().parents[3]
GOLDEN_LEDGER = (
    REPO
    / "docs/features/agents-communication-infra/adrs/fixtures/"
    "golden-opening-v0.6.1.yaml"
)
DISPATCH_ID = "2026-07-23-local-probe-fixture"
SECRET_ANSWER = "ONLY-IN-PROTECTED-ARTIFACT-7dd587"


class AptResearchEndToEndTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.ledger = self.root / "ledger.yaml"
        shutil.copyfile(GOLDEN_LEDGER, self.ledger)
        self.settings = RuntimeSettings(self.root / "runtime.db", REPO, self.ledger)
        self.runtime = RuntimeService(self.settings)
        self.runtime.open()
        self.runtime.register_profiles()
        self.session_id = self.runtime.ensure_session(
            origin_digest="sha256:" + "7" * 64, name="APT E2E"
        )["session"]["session_id"]
        self.runtime.link_session_dispatch(
            session_id=self.session_id, dispatch_id=DISPATCH_ID
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def token(self, action: str, phase: str, context: dict[str, str]) -> str:
        return self.runtime.issue_capability(
            principal_id="apt-e2e",
            action=action,
            phase=phase,
            context=context,
        )["token"]

    def test_capture_query_protected_answer_and_restart(self) -> None:
        scope = {"session_id": self.session_id, "dispatch_id": DISPATCH_ID}
        provenance = ProvenanceService(self.runtime)
        intent = {
            "session_id": self.session_id,
            "expected_contribution_id": "research-main",
            "question": "Qual é a propriedade de segurança mínima?",
            "final_answer": SECRET_ANSWER,
            "references": [
                {
                    "reference_kind": "file",
                    "locator_observed": "docs/features/agent-provenance-telemetry/specs/SPEC.md",
                    "use_kind": "claimed_consulted",
                }
            ],
            "problems": [
                {"kind": "gap", "statement": "Probe lineage still needs enablement."}
            ],
            "formalizations": [
                {
                    "claim": "An answer is disclosed only under exact scope.",
                    "notation": "read(a,c) -> scope(a)=scope(c)",
                    "latex": r"\operatorname{read}(a,c)\Rightarrow S(a)=S(c)",
                    "legend": {"S": "authorization scope"},
                    "reading": "Every answer read is scoped to its capture.",
                    "logic_family": "first-order implication",
                    "assumptions": ["capabilities are unforgeable"],
                    "scope": "local APT runtime",
                }
            ],
        }
        receipt = provenance.append_research_submission(
            token=self.token("apt.append", "capture", scope),
            dispatch_id=DISPATCH_ID,
            idempotency_key="research-1",
            intent=intent,
        )
        capture_id = receipt["research_capture_id"]
        self.assertEqual(
            receipt,
            provenance.append_research_submission(
                token=self.token("apt.append", "capture", scope),
                dispatch_id=DISPATCH_ID,
                idempotency_key="research-1",
                intent=intent,
            ),
        )
        with self.runtime.database.connect() as conn:
            event_count = conn.execute("SELECT count(*) FROM events").fetchone()[0]
        zero_new = provenance.append_research_submission(
            token=self.token("apt.append", "capture", scope),
            dispatch_id=DISPATCH_ID,
            idempotency_key="research-semantic-retry",
            intent=intent,
        )
        self.assertFalse(zero_new["submitted"])
        self.assertTrue(
            all(row["status"] == "existing_exact" for row in zero_new["semantic_results"])
        )
        with self.runtime.database.connect() as conn:
            self.assertEqual(
                conn.execute("SELECT count(*) FROM events").fetchone()[0], event_count
            )
        changed = {**intent, "question": intent["question"] + " (changed)"}
        with self.assertRaises(IdempotencyConflict):
            provenance.append_research_submission(
                token=self.token("apt.append", "capture", scope),
                dispatch_id=DISPATCH_ID,
                idempotency_key="research-1",
                intent=changed,
            )
        malformed = {
            **intent,
            "expected_contribution_id": "malformed",
            "formalizations": [{**intent["formalizations"][0], "legend": {"S": 7}}],
        }
        with self.assertRaises(ValidationError):
            provenance.append_research_submission(
                token=self.token("apt.append", "capture", scope),
                dispatch_id=DISPATCH_ID,
                idempotency_key="malformed",
                intent=malformed,
            )
        original_envelope = provenance._bound_envelope

        def divergent_formalization_frame(records):
            mutated = [
                {
                    **record,
                    **(
                        {"claim": record["claim"] + " divergent"}
                        if record.get("type") == "formalization"
                        else {}
                    ),
                }
                for record in records
            ]
            return original_envelope(mutated)

        provenance._bound_envelope = divergent_formalization_frame
        try:
            with self.assertRaises(ValidationError):
                provenance.append_research_submission(
                    token=self.token("apt.append", "capture", scope),
                    dispatch_id=DISPATCH_ID,
                    idempotency_key="divergent-formalization-frame",
                    intent={
                        **intent,
                        "expected_contribution_id": "divergent-formalization-frame",
                    },
                )
        finally:
            provenance._bound_envelope = original_envelope

        projection = provenance.get_research(
            token=self.token("projection.read", "observe", scope),
            capture_id=capture_id,
        )
        self.assertEqual(projection["questions"][0]["question_text"], intent["question"])
        self.assertEqual(len(projection["reference_uses"]), 1)
        self.assertEqual(len(projection["problems"]), 1)
        self.assertEqual(len(projection["formalizations"]), 1)
        with self.assertRaises(AuthorizationError):
            provenance.get_research(
                token=self.token("projection.read", "observe", {}),
                capture_id=capture_id,
            )

        answer_scope = {**scope, "research_capture_id": capture_id}
        self.assertEqual(
            provenance.get_answer(
                token=self.token("artifact.read", "collect", answer_scope),
                capture_id=capture_id,
            ),
            SECRET_ANSWER,
        )
        with self.assertRaises(AuthorizationError):
            provenance.get_answer(
                token=self.token(
                    "artifact.read",
                    "collect",
                    {**scope, "research_capture_id": "cap_wrong"},
                ),
                capture_id=capture_id,
            )
        with self.runtime.database.connect() as conn:
            event_text = "\n".join(
                bytes(row[0]).decode("utf-8")
                for row in conn.execute(
                    """SELECT a.body FROM events e
                       JOIN artifacts a ON a.artifact_id=e.payload_ref
                       WHERE a.classification='runtime-internal'"""
                )
            )
            projection_text = "\n".join(
                row[0]
                for row in conn.execute(
                    "SELECT payload_json FROM apt_research_facts_projection"
                )
            )
            json_text: list[str] = []
            protected_artifact_id = projection["capture"]["raw_return"]["artifact_id"]
            protected_rowid = conn.execute(
                "SELECT rowid FROM artifacts WHERE artifact_id=?",
                (protected_artifact_id,),
            ).fetchone()[0]
            tables = [
                row[0]
                for row in conn.execute(
                    """SELECT name FROM sqlite_master
                       WHERE type='table' AND name NOT LIKE 'sqlite_%'
                    """
                )
            ]
            for table in tables:
                columns = [
                    (row[1], row[2].upper())
                    for row in conn.execute(f'PRAGMA table_info("{table}")')
                    if row[2].upper() in {"TEXT", "BLOB"}
                ]
                for column, column_type in columns:
                    for row in conn.execute(
                        f'SELECT rowid,"{column}" FROM "{table}" WHERE "{column}" IS NOT NULL'
                    ):
                        if (
                            table == "artifacts"
                            and column == "body"
                            and row[0] == protected_rowid
                        ):
                            continue
                        value = row[1]
                        json_text.append(
                            bytes(value).decode("utf-8", errors="replace")
                            if column_type == "BLOB"
                            else str(value)
                        )
            protected_body = bytes(
                conn.execute(
                    "SELECT body FROM artifacts WHERE artifact_id=?",
                    (protected_artifact_id,),
                ).fetchone()[0]
            ).decode("utf-8")
        self.assertNotIn(SECRET_ANSWER, event_text)
        self.assertNotIn(SECRET_ANSWER, projection_text)
        self.assertNotIn(SECRET_ANSWER, "\n".join(json_text))
        self.assertEqual(protected_body.count(SECRET_ANSWER), 1)

        blocked_app = FastAPI()
        blocked_app.include_router(
            create_provenance_router(lambda: self.runtime, enabled=lambda: False)
        )
        self.assertEqual(
            TestClient(blocked_app)
            .get(
                f"/api/provenance/research/{capture_id}",
                headers={"Authorization": "Bearer inert"},
            )
            .status_code,
            503,
        )
        enabled_app = FastAPI()
        enabled_app.include_router(
            create_provenance_router(lambda: self.runtime, enabled=lambda: True)
        )
        answer_response = TestClient(enabled_app).get(
            f"/api/provenance/research/{capture_id}/answer",
            headers={
                "Authorization": "Bearer "
                + self.token("artifact.read", "collect", answer_scope)
            },
        )
        self.assertEqual(answer_response.status_code, 200)
        self.assertEqual(answer_response.json(), {"final_answer": SECRET_ANSWER})

        restarted = RuntimeService(self.settings)
        restarted.open()
        restarted_provenance = ProvenanceService(restarted)
        restarted_projection = restarted_provenance.get_research(
            token=restarted.issue_capability(
                principal_id="apt-e2e",
                action="projection.read",
                phase="observe",
                context=scope,
            )["token"],
            capture_id=capture_id,
        )
        self.assertEqual(restarted_projection["effective_as_of"], projection["effective_as_of"])
        self.assertEqual(
            restarted_provenance.get_answer(
                token=restarted.issue_capability(
                    principal_id="apt-e2e",
                    action="artifact.read",
                    phase="collect",
                    context=answer_scope,
                )["token"],
                capture_id=capture_id,
            ),
            SECRET_ANSWER,
        )

    def test_official_probe_lineage_requires_exact_receipts_and_zero_new_is_pure(self) -> None:
        activation = self.runtime.activate_local_probe(
            session_id=self.session_id,
            dispatch_id=DISPATCH_ID,
            probe_id="probe-lineage",
            group_aggregate_id="group-lineage",
            seat_id="seat-lineage",
            attempt_id="attempt-lineage",
            operation_id="operation-lineage",
        )
        payload = {
            "probe_id": "probe-lineage",
            "recommendation_id": "recommendation-1",
            "bundle_digest": "sha256:" + "8" * 64,
        }
        publication = self.runtime.publish(
            activation["issued_capabilities_once"]["agent"]["token"],
            {
                "idempotency_key": "publication-lineage",
                "operation_id": "operation-lineage",
                "round_id": "probe",
                "message_type": "reference_probe",
                "reply_to_message_ids": [],
                "payload": payload,
            },
        )
        official = self.runtime.verify_publication(
            activation["issued_capabilities_once"]["parent"]["token"],
            publication["publication_receipt"],
        )
        official_id = official["official_message"]["accepted_event_id"]
        with self.runtime.database.connect() as conn:
            profile = conn.execute(
                """SELECT * FROM protocol_profiles
                   WHERE profile_id='apt.reference-probe-lineage'
                   AND profile_version='1'"""
            ).fetchone()
            official_event = conn.execute(
                "SELECT schema_ref,payload_hash FROM events WHERE event_id=?",
                (official_id,),
            ).fetchone()
            registration = conn.execute(
                "SELECT schema_ref,payload_hash FROM events WHERE event_id=?",
                (profile["registration_event_id"],),
            ).fetchone()
        recommendation_ref = {
            **payload,
            "profile_binding": {
                "protocol_profile_id": profile["profile_id"],
                "protocol_profile_version": profile["profile_version"],
                "protocol_profile_digest": profile["canonical_digest"],
            },
            "bundle_acceptance_ref": {
                "kind": "accepted_event",
                "accepted_event_id": official_id,
                "contract_version": official_event["schema_ref"],
                "evidence_digest": official_event["payload_hash"],
            },
            "profile_registration_ref": {
                "kind": "registry_event",
                "accepted_event_id": profile["registration_event_id"],
                "protocol_profile_id": profile["profile_id"],
                "protocol_profile_version": profile["profile_version"],
                "protocol_profile_digest": profile["canonical_digest"],
                "contract_version": registration["schema_ref"],
                "evidence_digest": registration["payload_hash"],
            },
            "source_observation_ids": [],
        }
        subject = canonical_digest(payload)
        append_token = self.token(
            "apt.append",
            "capture",
            {"session_id": self.session_id, "dispatch_id": DISPATCH_ID},
        )
        request = {
            "operation_id": "lineage-append",
            "actor_ref": "apt-e2e",
            "lineage_items": [
                {
                    "kind": "delivery_origin",
                    "delivery_subject_key": subject,
                    "probe_recommendation_ref": recommendation_ref,
                    "expected_head_event_id": None,
                }
            ],
        }
        accepted = self.runtime.append_apt_event(
            token=append_token,
            command_name="apt.append-reference-probe-lineage@1",
            aggregate_id="apt-lineage:test",
            expected_version=0,
            idempotency_key="lineage-1",
            payload=request,
        )
        self.assertEqual(accepted["semantic_results"][0]["status"], "accepted_new")
        delivery_head = accepted["semantic_results"][0]["accepted_event_id"]
        research_intent = {
            "session_id": self.session_id,
            "expected_contribution_id": "lineage-research",
            "question": "Which probe reference was used?",
            "final_answer": "The accepted official probe reference.",
            "references": [
                {
                    "reference_kind": "url",
                    "locator_observed": "https://example.invalid/reference",
                    "use_kind": "claimed_consulted",
                }
            ],
            "problems": [],
            "formalizations": [],
        }
        research_receipt = ProvenanceService(self.runtime).append_research_submission(
            token=append_token,
            dispatch_id=DISPATCH_ID,
            idempotency_key="lineage-research",
            intent=research_intent,
        )
        capture_id = research_receipt["research_capture_id"]
        research = self.runtime.projections.get_apt_research(capture_id)
        reference = dict(research["reference_uses"][0])
        reference["reference_use_id"] = "ref_mixed_probe"
        reference["fact"] = {
            **reference["fact"],
            "fact_id": "fact_mixed_probe",
            "subject_id": "ref_mixed_probe",
            "operation_id": "operation-mixed-probe",
        }
        reference["probe_recommendation_ref"] = recommendation_ref
        reference_request = {
            **request,
            "operation_id": "lineage-reference",
            "lineage_items": [
                {"kind": "research_reference_use", "payload": reference},
            ],
        }
        self.runtime.append_apt_event(
            token=append_token,
            command_name="apt.append-reference-probe-lineage@1",
            aggregate_id="apt-lineage:test",
            expected_version=1,
            idempotency_key="lineage-reference",
            payload=reference_request,
        )
        mixed_request = {
            **request,
            "operation_id": "lineage-mixed",
            "lineage_items": [
                {
                    **request["lineage_items"][0],
                    "expected_head_event_id": delivery_head,
                },
                {"kind": "research_reference_use", "payload": reference},
            ],
        }
        mixed = self.runtime.append_apt_event(
            token=append_token,
            command_name="apt.append-reference-probe-lineage@1",
            aggregate_id="apt-lineage:test",
            expected_version=2,
            idempotency_key="lineage-mixed",
            payload=mixed_request,
        )
        self.assertEqual(
            [row["status"] for row in mixed["semantic_results"]],
            ["accepted_new", "existing_exact"],
        )
        advanced_head = mixed["semantic_results"][0]["accepted_event_id"]
        with self.runtime.database.connect() as conn:
            before = conn.execute("SELECT count(*) FROM events").fetchone()[0]
        exact = self.runtime.append_apt_event(
            token=append_token,
            command_name="apt.append-reference-probe-lineage@1",
            aggregate_id="apt-lineage:test",
            expected_version=3,
            idempotency_key="lineage-zero",
            payload={
                **reference_request,
                "operation_id": "lineage-zero",
            },
        )
        self.assertFalse(exact["submitted"])
        with self.runtime.database.connect() as conn:
            self.assertEqual(conn.execute("SELECT count(*) FROM events").fetchone()[0], before)
        for invalid_head in (None, official_id):
            with self.assertRaises(ConflictError):
                self.runtime.append_apt_event(
                    token=append_token,
                    command_name="apt.append-reference-probe-lineage@1",
                    aggregate_id="apt-lineage:test",
                    expected_version=3,
                    idempotency_key="lineage-stale-" + str(invalid_head),
                    payload={
                        **request,
                        "operation_id": "lineage-stale-" + str(invalid_head),
                        "lineage_items": [
                            {
                                **request["lineage_items"][0],
                                "expected_head_event_id": invalid_head,
                            }
                        ],
                    },
                )
        forged = {
            **request,
            "lineage_items": [
                {
                    **request["lineage_items"][0],
                    "expected_head_event_id": advanced_head,
                    "probe_recommendation_ref": {
                        **recommendation_ref,
                        "bundle_acceptance_ref": {
                            **recommendation_ref["bundle_acceptance_ref"],
                            "evidence_digest": "sha256:" + "0" * 64,
                        },
                    },
                }
            ],
        }
        with self.assertRaises(ConflictError):
            self.runtime.append_apt_event(
                token=append_token,
                command_name="apt.append-reference-probe-lineage@1",
                aggregate_id="apt-lineage:test",
                expected_version=1,
                idempotency_key="lineage-forged",
                payload=forged,
            )

    def test_concurrent_exact_converges_and_divergent_currentness_conflicts(self) -> None:
        scope = {"session_id": self.session_id, "dispatch_id": DISPATCH_ID}
        token = self.token("apt.append", "capture", scope)
        intent = {
            "session_id": self.session_id,
            "expected_contribution_id": "concurrent-exact",
            "question": "Q?",
            "final_answer": "A.",
            "references": [],
            "problems": [],
            "formalizations": [],
        }
        barrier = threading.Barrier(2)
        results: list[dict] = []
        errors: list[Exception] = []

        def exact_worker() -> None:
            other = RuntimeService(self.settings)
            other.open()
            barrier.wait()
            try:
                results.append(
                    ProvenanceService(other).append_research_submission(
                        token=token,
                        dispatch_id=DISPATCH_ID,
                        idempotency_key="concurrent-exact",
                        intent=intent,
                    )
                )
            except Exception as exc:  # evidence captures an unexpected race outcome
                errors.append(exc)

        threads = [threading.Thread(target=exact_worker) for _ in range(2)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual(errors, [])
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["research_capture_id"], results[1]["research_capture_id"])

        divergent_results: list[str] = []
        barrier = threading.Barrier(2)

        def divergent_worker(suffix: str) -> None:
            other = RuntimeService(self.settings)
            other.open()
            changed = {
                **intent,
                "expected_contribution_id": "concurrent-divergent",
                "question": "Q " + suffix,
            }
            barrier.wait()
            try:
                ProvenanceService(other).append_research_submission(
                    token=token,
                    dispatch_id=DISPATCH_ID,
                    idempotency_key="divergent-" + suffix,
                    intent=changed,
                )
                divergent_results.append("accepted")
            except ConflictError:
                divergent_results.append("conflict")

        threads = [
            threading.Thread(target=divergent_worker, args=(suffix,))
            for suffix in ("a", "b")
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual(sorted(divergent_results), ["accepted", "conflict"])

    def test_ensure_reuses_origin_and_explicit_start_new_rebinds(self) -> None:
        origin = "sha256:" + "7" * 64
        ensured = self.runtime.ensure_session(origin_digest=origin, name="APT E2E")
        self.assertEqual(ensured["session"]["session_id"], self.session_id)
        start_token = self.token(
            "session.start-new",
            "bootstrap",
            {
                "origin_digest": origin,
                "authorization_policy_ref": "host.session-rollover@1",
                "authorization_policy_digest": "sha256:" + "a" * 64,
                "authorization_evidence_ref": "host-evidence:rollover-1",
                "authorization_evidence_digest": "sha256:" + "b" * 64,
                "expected_current_session_id": self.session_id,
                "nonce": "rollover-nonce-1",
            },
        )
        started = self.runtime.start_new_session(
            token=start_token,
            name="successor",
            expected_current_session_id=self.session_id,
            idempotency_key="rollover-1",
        )
        retry = self.runtime.start_new_session(
            token=start_token,
            name="successor",
            expected_current_session_id=self.session_id,
            idempotency_key="rollover-1",
        )
        self.assertEqual(started, retry)
        self.assertNotEqual(started["session"]["session_id"], self.session_id)
        with self.runtime.database.connect() as conn:
            rows = conn.execute(
                "SELECT session_id FROM sessions WHERE origin_digest=?",
                (origin,),
            ).fetchall()
            head = conn.execute(
                "SELECT * FROM session_origin_heads WHERE origin_digest=?",
                (origin,),
            ).fetchone()
        self.assertEqual(len(rows), 2)
        self.assertEqual(head["current_session_id"], started["session"]["session_id"])
        self.assertEqual(head["head_version"], 2)

    def test_http_subprocess_restart_round_trip_preserves_ledger(self) -> None:
        ledger_before = self.ledger.read_bytes()
        scope = {"session_id": self.session_id, "dispatch_id": DISPATCH_ID}
        ensure_token = self.token(
            "session.ensure",
            "bootstrap",
            {"origin_digest": "sha256:" + "7" * 64},
        )
        link_token = self.token(
            "dispatch.link",
            "bootstrap",
            {
                "session_id": self.session_id,
                "authorization_policy_ref": "host.dispatch-link@1",
                "authorization_policy_digest": "sha256:" + "c" * 64,
                "authorization_evidence_ref": "host-evidence:link",
                "authorization_evidence_digest": "sha256:" + "d" * 64,
            },
        )
        append_token = self.token("apt.append", "capture", scope)
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            port = sock.getsockname()[1]
        environment = {
            **os.environ,
            "APT_TEST_DB": str(self.root / "runtime.db"),
            "APT_TEST_REPO": str(REPO),
            "APT_TEST_LEDGER": str(self.ledger),
            "APT_TEST_REPO_ID": "cyberalchemy-orchestrator",
        }
        command = [
            os.environ.get("PYTHON", "python"),
            "-m",
            "uvicorn",
            "implementations.tests.runtime.apt_subprocess_app:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
            "--log-level",
            "error",
        ]

        def start():
            process = subprocess.Popen(
                command,
                cwd=REPO,
                env=environment,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            for _ in range(100):
                try:
                    urllib.request.urlopen(
                        f"http://127.0.0.1:{port}/openapi.json", timeout=0.2
                    ).read()
                    return process
                except Exception:
                    if process.poll() is not None:
                        break
                    time.sleep(0.05)
            process.terminate()
            stdout, stderr = process.communicate(timeout=5)
            self.fail(f"subprocess server failed: {stdout!r} {stderr!r}")

        def request(method, path, token, body=None, idem=None):
            headers = {"Authorization": "Bearer " + token}
            if body is not None:
                headers["Content-Type"] = "application/json"
            if idem:
                headers["Idempotency-Key"] = idem
            req = urllib.request.Request(
                f"http://127.0.0.1:{port}{path}",
                data=json.dumps(body).encode() if body is not None else None,
                headers=headers,
                method=method,
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                return response.status, json.loads(response.read())

        process = start()
        try:
            self.assertEqual(
                request(
                    "POST",
                    "/api/provenance/sessions/ensure",
                    ensure_token,
                    {"name": "APT E2E"},
                    "ensure",
                )[0],
                200,
            )
            self.assertEqual(
                request(
                    "POST",
                    f"/api/provenance/sessions/{self.session_id}/dispatches",
                    link_token,
                    {"dispatch_id": DISPATCH_ID},
                    "link",
                )[0],
                200,
            )
            _, receipt = request(
                "POST",
                f"/api/provenance/dispatches/cyberalchemy-orchestrator/{DISPATCH_ID}/research",
                append_token,
                {
                    "session_id": self.session_id,
                    "expected_contribution_id": "subprocess",
                    "question": "Does restart preserve provenance?",
                    "final_answer": "Yes, across a real process boundary.",
                    "references": [],
                    "problems": [],
                    "formalizations": [],
                },
                "subprocess-research",
            )
            capture_id = receipt["research_capture_id"]
        finally:
            process.terminate()
            process.communicate(timeout=10)

        projection_token = self.token("projection.read", "observe", scope)
        answer_token = self.token(
            "artifact.read",
            "collect",
            {**scope, "research_capture_id": capture_id},
        )
        process = start()
        try:
            self.assertEqual(
                request(
                    "GET",
                    f"/api/provenance/research/{capture_id}",
                    projection_token,
                )[0],
                200,
            )
            status, answer = request(
                "GET",
                f"/api/provenance/research/{capture_id}/answer",
                answer_token,
            )
            self.assertEqual(status, 200)
            self.assertEqual(
                answer["final_answer"], "Yes, across a real process boundary."
            )
        finally:
            process.terminate()
            process.communicate(timeout=10)
        self.assertEqual(self.ledger.read_bytes(), ledger_before)


if __name__ == "__main__":
    unittest.main()
