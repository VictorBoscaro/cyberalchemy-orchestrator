from __future__ import annotations

import shutil
import tempfile
import threading
import unittest
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
                        if table == "artifacts" and column == "body":
                            continue
                        value = row[1]
                        json_text.append(
                            bytes(value).decode("utf-8", errors="replace")
                            if column_type == "BLOB"
                            else str(value)
                        )
            protected_artifact_id = projection["capture"]["raw_return"]["artifact_id"]
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
                    "expected_head_event_id": official_id,
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
        with self.runtime.database.connect() as conn:
            before = conn.execute("SELECT count(*) FROM events").fetchone()[0]
        exact = self.runtime.append_apt_event(
            token=append_token,
            command_name="apt.append-reference-probe-lineage@1",
            aggregate_id="apt-lineage:test",
            expected_version=1,
            idempotency_key="lineage-zero",
            payload=request,
        )
        self.assertFalse(exact["submitted"])
        with self.runtime.database.connect() as conn:
            self.assertEqual(conn.execute("SELECT count(*) FROM events").fetchone()[0], before)
        forged = {
            **request,
            "lineage_items": [
                {
                    **request["lineage_items"][0],
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


if __name__ == "__main__":
    unittest.main()
