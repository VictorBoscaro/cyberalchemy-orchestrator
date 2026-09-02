"""Deterministic local-only executor for compiler-produced ExecutionGraph candidates.

This module deliberately does not implement ConfirmRuntimeDispatch@2, provider calls, tools, or
external effects.  It gives the reviewed compiler a persisted fake-adapter execution path whose
authority and evidence ceiling are explicit.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Protocol, Sequence

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, ValidationError as JsonSchemaValidationError

from .canonical import canonical_bytes, canonical_digest, canonical_text, digest_bytes, parse_strict_json
from .database import RuntimeDatabase
from .draft_graph_compiler import (
    CompilationResult,
    DraftGraphCompiler,
    TrustedAllocatorContextGate,
    VerifiedCompilationContext,
    validate_execution_graph,
)
from .errors import ConflictError, GateBlockedError, IntegrityError, NotFoundError, ValidationError


COMPILATION_AUTHORITY_SCHEMA = "aci.local-compilation-authority@1"
ACCEPTANCE_SCHEMA = "aci.local-execution-acceptance@1"
ADMISSION_SCHEMA = "aci.local-execution-admission@2"
SNAPSHOT_SCHEMA = "aci.local-execution-snapshot@1"
RECEIPT_SCHEMA = "aci.local-execution-receipt@1"
AUTHORITY_CEILING = "proposed-execution-graph-local-fake-only"
INPUT_DIGEST_KEYS = (
    "compilation_context",
    "allocator_evidence",
    "allocator_trust",
    "draft_graph",
    "policy",
    "catalog",
    "resources",
    "role_registry",
    "agent_pool",
)
RUN_TERMINAL = frozenset({"succeeded", "failed", "cancelled", "stopped"})
NODE_TERMINAL = frozenset({"succeeded", "failed", "cancelled", "skipped", "stopped"})


@dataclass(frozen=True, slots=True)
class WorkerAssignment:
    run_id: str
    graph_digest: str
    node_id: str
    attempt_id: str
    attempt_number: int
    display_name: str
    role: str
    objective: str
    instructions: str
    agent: dict[str, Any]
    tools: tuple[dict[str, Any], ...]
    inputs: dict[str, Any]

    def value(self) -> dict[str, Any]:
        return {
            "schema": "aci.local-worker-assignment@1",
            "run_id": self.run_id,
            "graph_digest": self.graph_digest,
            "node_id": self.node_id,
            "attempt_id": self.attempt_id,
            "attempt_number": self.attempt_number,
            "display_name": self.display_name,
            "role": self.role,
            "objective": self.objective,
            "instructions": self.instructions,
            "agent": self.agent,
            "tools": list(self.tools),
            "inputs": self.inputs,
        }


@dataclass(frozen=True, slots=True)
class LocalWorkerResult:
    outputs: dict[str, Any]
    validations: dict[str, bool]

    def value(self) -> dict[str, Any]:
        return {
            "schema": "aci.local-worker-result@1",
            "outputs": self.outputs,
            "validations": self.validations,
        }


@dataclass(frozen=True, slots=True)
class LocalCompilationCandidate:
    """Frozen compiler output.  This value is evidence, never execution acceptance."""

    graph_bytes: bytes
    graph_digest: str
    compilation_authority_bytes: bytes
    compilation_authority_digest: str

    def value(self) -> dict[str, Any]:
        return {
            "schema": "aci.local-compilation-candidate@1",
            "graph_digest": self.graph_digest,
            "compilation_authority_digest": self.compilation_authority_digest,
        }


class LocalWorkerFailure(Exception):
    def __init__(self, code: str) -> None:
        if not isinstance(code, str) or not code:
            raise ValueError("local worker failure code must be non-empty")
        self.code = code
        super().__init__(code)


class LocalWorkerAdapter(Protocol):
    def execute(self, assignment: WorkerAssignment) -> LocalWorkerResult:
        """Return one deterministic local result or raise LocalWorkerFailure."""


class ScriptedLocalAdapter:
    """In-memory adapter: select one predeclared outcome by node and attempt number."""

    def __init__(
        self,
        script: Mapping[str, Sequence[LocalWorkerResult | LocalWorkerFailure]],
    ) -> None:
        self._script = {node_id: tuple(outcomes) for node_id, outcomes in script.items()}
        self.calls: list[WorkerAssignment] = []

    def execute(self, assignment: WorkerAssignment) -> LocalWorkerResult:
        self.calls.append(assignment)
        outcomes = self._script.get(assignment.node_id, ())
        index = assignment.attempt_number - 1
        if index >= len(outcomes):
            raise LocalWorkerFailure("scripted_outcome_unavailable")
        outcome = outcomes[index]
        if isinstance(outcome, LocalWorkerFailure):
            raise outcome
        if not isinstance(outcome, LocalWorkerResult):
            raise LocalWorkerFailure("scripted_outcome_invalid")
        return outcome


def _bytes(value: bytes | str) -> bytes:
    return value if isinstance(value, bytes) else value.encode("utf-8")


def _derived_id(prefix: str, value: Any) -> str:
    return prefix + canonical_digest(value).removeprefix("sha256:")[:32]


def _digest_string(value: object, label: str) -> str:
    if (
        not isinstance(value, str)
        or not value.startswith("sha256:")
        or len(value) != 71
        or any(character not in "0123456789abcdef" for character in value[7:])
    ):
        raise ValidationError(f"{label} must be a lowercase SHA-256 digest")
    return value


class ExecutionGraphRuntime:
    """Persist and execute one compiler-produced graph through a local fake adapter."""

    def __init__(
        self,
        database_path: Path,
        adapter: LocalWorkerAdapter,
        *,
        trusted_acceptance_issuers: Mapping[str, str] | None = None,
        trusted_acceptance_digests: Mapping[str, str | Sequence[str]] | None = None,
    ) -> None:
        self.database = RuntimeDatabase(Path(database_path))
        self.adapter = adapter
        self.trusted_acceptance_issuers = dict(trusted_acceptance_issuers or {})
        self.trusted_acceptance_digests: dict[str, frozenset[str]] = {}
        for issuer, evidence_digest in self.trusted_acceptance_issuers.items():
            if not isinstance(issuer, str) or not issuer:
                raise ValueError("trusted local acceptance issuer must be non-empty")
            _digest_string(evidence_digest, "trusted local acceptance issuer evidence digest")
        for issuer, configured in (trusted_acceptance_digests or {}).items():
            if not isinstance(issuer, str) or not issuer:
                raise ValueError("trusted local acceptance digest issuer must be non-empty")
            digests = (configured,) if isinstance(configured, str) else tuple(configured)
            if not digests:
                raise ValueError("trusted local acceptance digest set must be non-empty")
            for acceptance_digest in digests:
                _digest_string(acceptance_digest, "trusted local acceptance digest")
            self.trusted_acceptance_digests[issuer] = frozenset(digests)

    def open(self) -> list[dict[str, str]]:
        return self.database.migrate()

    def compile_candidate(
        self,
        *,
        compilation_context: bytes | str,
        allocator_evidence: bytes | str,
        allocator_trust: bytes | str,
        draft_graph: bytes | str,
        policy: bytes | str,
        catalog: bytes | str,
        resources: bytes | str,
        role_registry: bytes | str,
        agent_pool: bytes | str,
    ) -> LocalCompilationCandidate:
        raw = {
            "compilation_context": _bytes(compilation_context),
            "allocator_evidence": _bytes(allocator_evidence),
            "allocator_trust": _bytes(allocator_trust),
            "draft_graph": _bytes(draft_graph),
            "policy": _bytes(policy),
            "catalog": _bytes(catalog),
            "resources": _bytes(resources),
            "role_registry": _bytes(role_registry),
            "agent_pool": _bytes(agent_pool),
        }
        context = TrustedAllocatorContextGate.verify(
            raw["compilation_context"], raw["allocator_evidence"], raw["allocator_trust"]
        )
        result = DraftGraphCompiler().compile(
            context,
            raw["draft_graph"],
            raw["policy"],
            raw["catalog"],
            raw["resources"],
            raw["role_registry"],
            raw["agent_pool"],
        )
        authority = self._compilation_authority(
            result=result,
            context=context,
            input_digests={name: digest_bytes(raw[name]) for name in INPUT_DIGEST_KEYS},
        )
        authority_bytes = canonical_bytes(authority)
        return LocalCompilationCandidate(
            graph_bytes=result.canonical_bytes,
            graph_digest=result.digest,
            compilation_authority_bytes=authority_bytes,
            compilation_authority_digest=digest_bytes(authority_bytes),
        )

    def admit_execution_graph(
        self,
        *,
        execution_graph: bytes | str,
        compilation_authority: bytes | str,
        acceptance: bytes | str,
    ) -> dict[str, Any]:
        """Admit frozen graph bytes only under separately trusted local acceptance."""
        graph_bytes = _bytes(execution_graph)
        compilation_authority_bytes = _bytes(compilation_authority)
        acceptance_bytes = _bytes(acceptance)
        graph = self._decode_canonical_object(graph_bytes, "ExecutionGraph")
        compilation_authority_value = self._decode_canonical_object(
            compilation_authority_bytes, "compilation authority"
        )
        acceptance_value = self._decode_canonical_object(acceptance_bytes, "local acceptance")
        graph_digest = digest_bytes(graph_bytes)
        validate_execution_graph(graph)
        self._validate_local_subset(graph)
        self._validate_compilation_authority(
            compilation_authority_value, graph, graph_digest
        )
        compilation_authority_digest = digest_bytes(compilation_authority_bytes)
        self._validate_acceptance(
            acceptance_value,
            graph,
            graph_digest,
            compilation_authority_digest,
            digest_bytes(acceptance_bytes),
        )
        if acceptance_value["allocation_id"] != compilation_authority_value["allocation_id"]:
            raise IntegrityError("local execution acceptance allocation does not bind compiler authority")
        bundle = {
            "schema": ADMISSION_SCHEMA,
            "authority_ceiling": AUTHORITY_CEILING,
            "graph_digest": graph_digest,
            "compilation_authority": compilation_authority_value,
            "compilation_authority_digest": compilation_authority_digest,
            "acceptance": acceptance_value,
            "acceptance_digest": digest_bytes(acceptance_bytes),
        }
        return self._admit_verified(graph_bytes, graph, graph_digest, bundle)

    def execute_accepted_graph(
        self,
        *,
        execution_graph: bytes | str,
        compilation_authority: bytes | str,
        acceptance: bytes | str,
        max_steps: int | None = None,
    ) -> dict[str, Any]:
        """Admit and execute an independently accepted local/test ExecutionGraph."""
        admitted = self.admit_execution_graph(
            execution_graph=execution_graph,
            compilation_authority=compilation_authority,
            acceptance=acceptance,
        )
        return self.execute(admitted["run"]["run_id"], max_steps=max_steps)

    @staticmethod
    def _compilation_authority(
        *,
        result: CompilationResult,
        context: VerifiedCompilationContext,
        input_digests: Mapping[str, str],
    ) -> dict[str, Any]:
        return {
            "schema": COMPILATION_AUTHORITY_SCHEMA,
            "authority_ceiling": AUTHORITY_CEILING,
            "execution_mode": "local-fake",
            "dispatch_id": context.dispatch_id,
            "revision": context.revision,
            "allocation_id": context.allocation_id,
            "prior_accepted_graph_digest": context.prior_accepted_graph_digest,
            "graph_digest": result.digest,
            "compiler_report_digest": canonical_digest(list(result.report)),
            "input_digests": {name: input_digests[name] for name in INPUT_DIGEST_KEYS},
        }

    @staticmethod
    def _decode_canonical_object(value: bytes, label: str) -> dict[str, Any]:
        parsed = parse_strict_json(value)
        if not isinstance(parsed, dict):
            raise ValidationError(f"{label} must be an object")
        if canonical_bytes(parsed) != value:
            raise IntegrityError(f"{label} bytes are not canonical")
        return parsed

    def _admit_verified(
        self,
        graph_bytes: bytes,
        graph: dict[str, Any],
        graph_digest: str,
        authority: dict[str, Any],
    ) -> dict[str, Any]:
        """Persist already-validated graph and independent acceptance atomically."""
        authority_bytes = canonical_bytes(authority)
        authority_digest = digest_bytes(authority_bytes)
        admission_preimage = {
            "schema": "aci.local-execution-admission-id-preimage@1",
            "dispatch_id": graph["dispatch_id"],
            "revision": graph["revision"],
            "graph_digest": graph_digest,
            "authority_digest": authority_digest,
        }
        admission_id = _derived_id("adm_", admission_preimage)
        run_id = _derived_id(
            "run_",
            {"schema": "aci.local-execution-run-id-preimage@1", "admission_id": admission_id},
        )
        preflight_payload = {
            "admission_id": admission_id,
            "authority_digest": authority_digest,
            "dispatch_id": graph["dispatch_id"],
            "revision": graph["revision"],
        }
        self._validate_receipt_body(
            graph,
            {
                "schema": RECEIPT_SCHEMA,
                "run_id": run_id,
                "sequence": 0,
                "kind": "graph_admitted",
                "graph_digest": graph_digest,
                "node_id": None,
                "attempt_id": None,
                "payload_json": canonical_text(preflight_payload),
                "audit": self._receipt_audit(graph, None, preflight_payload),
            },
        )
        self.open()
        existing_run_id: str | None = None
        with self.database.write() as conn:
            existing = conn.execute(
                """
                SELECT a.*,r.run_id FROM local_execution_admissions a
                JOIN local_execution_runs r ON r.admission_id=a.admission_id
                WHERE a.dispatch_id=? AND a.revision=?
                """,
                (graph["dispatch_id"], graph["revision"]),
            ).fetchone()
            if existing:
                if (
                    existing["graph_digest"] != graph_digest
                    or bytes(existing["graph_bytes"]) != graph_bytes
                    or existing["authority_digest"] != authority_digest
                    or existing["authority_json"] != authority_bytes.decode("utf-8")
                ):
                    raise ConflictError("local execution admission identity conflict")
                existing_run_id = existing["run_id"]
            else:
                latest = conn.execute(
                    """
                    SELECT graph_digest,dispatch_sequence FROM local_execution_admissions
                    WHERE dispatch_id=? ORDER BY dispatch_sequence DESC LIMIT 1
                    """,
                    (graph["dispatch_id"],),
                ).fetchone()
                prior = authority["compilation_authority"]["prior_accepted_graph_digest"]
                if (latest is None and prior is not None) or (
                    latest is not None and prior != latest["graph_digest"]
                ):
                    raise ConflictError("local execution admission lineage conflict")
                sequence = 1 if latest is None else latest["dispatch_sequence"] + 1
                conn.execute(
                    """
                    INSERT INTO local_execution_admissions(
                      admission_id,dispatch_id,revision,graph_digest,graph_bytes,
                      authority_json,authority_digest,dispatch_sequence
                    ) VALUES(?,?,?,?,?,?,?,?)
                    """,
                    (
                        admission_id,
                        graph["dispatch_id"],
                        graph["revision"],
                        graph_digest,
                        graph_bytes,
                        authority_bytes.decode("utf-8"),
                        authority_digest,
                        sequence,
                    ),
                )
                conn.execute(
                    "INSERT INTO local_execution_runs(run_id,admission_id,status) VALUES(?,?,?)",
                    (run_id, admission_id, "pending"),
                )
                for ordinal, node in enumerate(graph["nodes"]):
                    conn.execute(
                        """
                        INSERT INTO local_execution_nodes(
                          run_id,node_id,node_ordinal,status,max_attempts,display_name,role
                        ) VALUES(?,?,?,?,?,?,?)
                        """,
                        (
                            run_id,
                            node["node_id"],
                            ordinal,
                            "pending",
                            node["limits"]["max_attempts"],
                            node["agent"]["display_name"],
                            node["agent"]["role"],
                        ),
                    )
                self._append_receipt(
                    conn,
                    run_id,
                    "graph_admitted",
                    {
                        "admission_id": admission_id,
                        "authority_digest": authority_digest,
                        "dispatch_id": graph["dispatch_id"],
                        "revision": graph["revision"],
                    },
                )
        return self.snapshot(existing_run_id or run_id)

    @staticmethod
    def _validate_compilation_authority(
        authority: dict[str, Any], graph: dict[str, Any], graph_digest: str
    ) -> None:
        required = {
            "schema",
            "authority_ceiling",
            "execution_mode",
            "dispatch_id",
            "revision",
            "allocation_id",
            "prior_accepted_graph_digest",
            "graph_digest",
            "compiler_report_digest",
            "input_digests",
        }
        if not isinstance(authority, dict) or set(authority) != required:
            raise ValidationError("local execution authority shape is invalid")
        if (
            authority["schema"] != COMPILATION_AUTHORITY_SCHEMA
            or authority["authority_ceiling"] != AUTHORITY_CEILING
            or authority["execution_mode"] != "local-fake"
            or authority["dispatch_id"] != graph["dispatch_id"]
            or authority["revision"] != graph["revision"]
            or authority["graph_digest"] != graph_digest
            or not isinstance(authority["allocation_id"], str)
            or not authority["allocation_id"]
        ):
            raise IntegrityError("local execution authority does not bind the compilation")
        _digest_string(authority["compiler_report_digest"], "compiler report digest")
        prior = authority["prior_accepted_graph_digest"]
        if prior is not None:
            _digest_string(prior, "prior accepted graph digest")
        digests = authority["input_digests"]
        if not isinstance(digests, dict) or set(digests) != set(INPUT_DIGEST_KEYS):
            raise ValidationError("local execution authority input digest set is invalid")
        for name in INPUT_DIGEST_KEYS:
            _digest_string(digests[name], f"{name} digest")

    def _validate_acceptance(
        self,
        acceptance: dict[str, Any],
        graph: dict[str, Any],
        graph_digest: str,
        compilation_authority_digest: str,
        acceptance_digest: str,
    ) -> None:
        required = {
            "schema",
            "authority_ceiling",
            "decision",
            "issuer_ref",
            "issuer_evidence_digest",
            "accepted_by",
            "dispatch_id",
            "revision",
            "allocation_id",
            "graph_digest",
            "compilation_authority_digest",
        }
        if not isinstance(acceptance, dict) or set(acceptance) != required:
            raise ValidationError("local execution acceptance shape is invalid")
        issuer = acceptance["issuer_ref"]
        if not isinstance(issuer, dict) or set(issuer) != {"name", "version"}:
            raise ValidationError("local execution acceptance issuer shape is invalid")
        if not all(isinstance(issuer[key], str) and issuer[key] for key in ("name", "version")):
            raise ValidationError("local execution acceptance issuer is invalid")
        issuer_key = f"{issuer['name']}@{issuer['version']}"
        evidence_digest = _digest_string(
            acceptance["issuer_evidence_digest"], "local acceptance issuer evidence digest"
        )
        if self.trusted_acceptance_issuers.get(issuer_key) != evidence_digest:
            raise GateBlockedError("local execution acceptance issuer is not trusted")
        if acceptance_digest not in self.trusted_acceptance_digests.get(issuer_key, frozenset()):
            raise GateBlockedError("local execution acceptance bytes are not trusted")
        if (
            acceptance["schema"] != ACCEPTANCE_SCHEMA
            or acceptance["authority_ceiling"] != AUTHORITY_CEILING
            or acceptance["decision"] != "accepted"
            or not isinstance(acceptance["accepted_by"], str)
            or not acceptance["accepted_by"]
            or acceptance["dispatch_id"] != graph["dispatch_id"]
            or acceptance["revision"] != graph["revision"]
            or acceptance["graph_digest"] != graph_digest
            or acceptance["compilation_authority_digest"] != compilation_authority_digest
            or not isinstance(acceptance["allocation_id"], str)
            or not acceptance["allocation_id"]
        ):
            raise IntegrityError("local execution acceptance does not bind the frozen candidate")

    @staticmethod
    def _validate_local_subset(graph: dict[str, Any]) -> None:
        if graph["lifecycle"]["max_parallel_nodes"] != 1:
            raise GateBlockedError("local fake executor requires max_parallel_nodes=1")
        if graph["lifecycle"]["cancellation"] != "cancel_running_nodes":
            raise GateBlockedError("local fake executor supports only cancel_running_nodes")
        if any(edge["kind"] == "feedback" for edge in graph["edges"]):
            raise GateBlockedError("local fake executor does not implement feedback cycles")
        audit = graph["audit_requirements"]
        supported_audit = {
            "record_objective": True,
            "record_agents": True,
            "record_route": True,
            "record_results": True,
        }
        if any(audit[name] is not value for name, value in supported_audit.items()):
            raise GateBlockedError("local fake executor requires complete objective/agent/route/result audit")
        members = {member["member_id"]: member for member in graph["content_members"]}
        receipt_member = members.get(audit["receipt_schema_member_id"])
        if (
            receipt_member is None
            or receipt_member["kind"] != "schema"
            or receipt_member["media_type"] != "application/schema+json"
            or receipt_member.get("encoding") != "utf-8"
            or "content" not in receipt_member
        ):
            raise GateBlockedError("local fake executor requires one inline JSON receipt schema")
        try:
            receipt_schema = parse_strict_json(receipt_member["content"])
            Draft202012Validator.check_schema(receipt_schema)
        except (ValidationError, SchemaError, JsonSchemaValidationError):
            raise GateBlockedError("local fake executor receipt schema is invalid") from None
        for member in graph["content_members"]:
            if "content" not in member or member["encoding"] != "utf-8":
                raise GateBlockedError("local fake executor requires inline UTF-8 content")
        for node in graph["nodes"]:
            isolation = node["isolation"]
            if (
                isolation["network"] != {"mode": "deny", "allow": []}
                or isolation["commands"] != {"mode": "deny", "grants": []}
                or isolation["external_effects"] != {"mode": "deny", "allow": []}
                or isolation["version_control"] != {"commit": False, "push": False}
            ):
                raise GateBlockedError("local fake executor admits no external effect authority")
            for item in node["inputs"]:
                if item["source"]["kind"] == "content_member" and item["source"]["selector"] != "$":
                    raise GateBlockedError("local fake executor supports only the exact $ selector")

    def _append_receipt(
        self,
        conn: Any,
        run_id: str,
        kind: str,
        payload: dict[str, Any],
        *,
        node_id: str | None = None,
        attempt_id: str | None = None,
    ) -> dict[str, Any]:
        graph, graph_digest = self._graph(conn, run_id)
        row = conn.execute(
            """
            SELECT r.next_receipt_sequence
            FROM local_execution_runs r
            JOIN local_execution_admissions a ON a.admission_id=r.admission_id
            WHERE r.run_id=?
            """,
            (run_id,),
        ).fetchone()
        if not row:
            raise NotFoundError("local execution run not found")
        sequence = row["next_receipt_sequence"]
        receipt = {
            "schema": RECEIPT_SCHEMA,
            "run_id": run_id,
            "sequence": sequence,
            "kind": kind,
            "graph_digest": graph_digest,
            "node_id": node_id,
            "attempt_id": attempt_id,
            "payload_json": canonical_text(payload),
            "audit": self._receipt_audit(graph, node_id, payload),
        }
        self._validate_receipt_body(graph, receipt)
        body = canonical_bytes(receipt)
        receipt_digest = digest_bytes(body)
        receipt_id = _derived_id(
            "rcpt_",
            {"schema": "aci.local-receipt-id-preimage@1", "receipt_digest": receipt_digest},
        )
        conn.execute(
            """
            INSERT INTO local_execution_receipts(
              receipt_id,run_id,sequence,receipt_json,receipt_digest
            ) VALUES(?,?,?,?,?)
            """,
            (receipt_id, run_id, sequence, body.decode("utf-8"), receipt_digest),
        )
        conn.execute(
            "UPDATE local_execution_runs SET next_receipt_sequence=? WHERE run_id=?",
            (sequence + 1, run_id),
        )
        return receipt

    def snapshot(self, run_id: str) -> dict[str, Any]:
        with self.database.connect() as conn:
            run = conn.execute(
                """
                SELECT r.*,a.dispatch_id,a.revision,a.graph_digest,a.authority_json,
                       a.authority_digest,a.admission_id,a.graph_bytes
                FROM local_execution_runs r
                JOIN local_execution_admissions a ON a.admission_id=r.admission_id
                WHERE r.run_id=?
                """,
                (run_id,),
            ).fetchone()
            if not run:
                raise NotFoundError("local execution run not found")
            self._verify_persisted_evidence(conn, run_id)
            nodes = conn.execute(
                "SELECT * FROM local_execution_nodes WHERE run_id=? ORDER BY node_ordinal",
                (run_id,),
            ).fetchall()
            attempts = conn.execute(
                """
                SELECT a.* FROM local_execution_attempts a
                JOIN local_execution_nodes n ON n.run_id=a.run_id AND n.node_id=a.node_id
                WHERE a.run_id=? ORDER BY n.node_ordinal,a.attempt_number
                """,
                (run_id,),
            ).fetchall()
            receipts = conn.execute(
                """
                SELECT receipt_json,receipt_digest FROM local_execution_receipts
                WHERE run_id=? ORDER BY sequence
                """,
                (run_id,),
            ).fetchall()
        return {
            "schema": SNAPSHOT_SCHEMA,
            "admission": {
                "admission_id": run["admission_id"],
                "dispatch_id": run["dispatch_id"],
                "revision": run["revision"],
                "graph_digest": run["graph_digest"],
                "authority": json.loads(run["authority_json"]),
                "authority_digest": run["authority_digest"],
            },
            "run": {
                "run_id": run["run_id"],
                "status": run["status"],
                "cancel_requested": bool(run["cancel_requested"]),
                "terminal_reason": run["terminal_reason"],
            },
            "nodes": [
                {
                    "node_id": row["node_id"],
                    "ordinal": row["node_ordinal"],
                    "status": row["status"],
                    "attempts": row["attempts"],
                    "max_attempts": row["max_attempts"],
                    "display_name": row["display_name"],
                    "role": row["role"],
                    "outputs": None if row["output_json"] is None else json.loads(row["output_json"]),
                    "output_digest": row["output_digest"],
                    "terminal_reason": row["terminal_reason"],
                }
                for row in nodes
            ],
            "attempts": [
                {
                    "attempt_id": row["attempt_id"],
                    "node_id": row["node_id"],
                    "attempt_number": row["attempt_number"],
                    "status": row["status"],
                    "assignment": json.loads(row["assignment_json"]),
                    "assignment_digest": row["assignment_digest"],
                    "result": None if row["result_json"] is None else json.loads(row["result_json"]),
                    "result_digest": row["result_digest"],
                    "failure_code": row["failure_code"],
                }
                for row in attempts
            ],
            "receipts": [
                {"receipt": json.loads(row["receipt_json"]), "receipt_digest": row["receipt_digest"]}
                for row in receipts
            ],
        }

    def snapshot_bytes(self, run_id: str) -> bytes:
        return canonical_bytes(self.snapshot(run_id))

    def cancel(self, run_id: str, *, reason: str = "operator_cancelled") -> dict[str, Any]:
        if not isinstance(reason, str) or not reason:
            raise ValidationError("cancellation reason must be non-empty")
        with self.database.write() as conn:
            run = conn.execute(
                "SELECT status,cancel_requested FROM local_execution_runs WHERE run_id=?",
                (run_id,),
            ).fetchone()
            if not run:
                raise NotFoundError("local execution run not found")
            self._verify_persisted_evidence(conn, run_id)
            if run["status"] not in RUN_TERMINAL and not run["cancel_requested"]:
                conn.execute(
                    "UPDATE local_execution_runs SET cancel_requested=1,terminal_reason=? WHERE run_id=?",
                    (reason, run_id),
                )
                self._append_receipt(conn, run_id, "cancellation_requested", {"reason": reason})
        return self.snapshot(run_id)

    def execute(self, run_id: str, *, max_steps: int | None = None) -> dict[str, Any]:
        """Run stable graph-order steps; a bound permits deterministic pause/cancel tests."""
        if max_steps is not None and (isinstance(max_steps, bool) or max_steps < 1):
            raise ValidationError("max_steps must be a positive integer")
        self.open()
        with self.database.write() as conn:
            run = conn.execute(
                "SELECT status FROM local_execution_runs WHERE run_id=?", (run_id,)
            ).fetchone()
            if not run:
                raise NotFoundError("local execution run not found")
            self._verify_persisted_evidence(conn, run_id)
            if run["status"] == "pending":
                conn.execute(
                    "UPDATE local_execution_runs SET status='running' WHERE run_id=?", (run_id,)
                )
                self._append_receipt(conn, run_id, "run_started", {})
        steps = 0
        while max_steps is None or steps < max_steps:
            assignment = self._prepare_next_assignment(run_id)
            if assignment is None:
                break
            self._assert_assignment_durable(assignment)
            try:
                result = self.adapter.execute(assignment)
                if not isinstance(result, LocalWorkerResult):
                    raise LocalWorkerFailure("adapter_result_type_invalid")
            except LocalWorkerFailure as error:
                self._record_worker_failure(assignment, error.code)
            else:
                self._record_worker_result(assignment, result)
            steps += 1
        return self.snapshot(run_id)

    def _verified_graph_authority(
        self, conn: Any, run_id: str
    ) -> tuple[dict[str, Any], str, dict[str, Any]]:
        row = conn.execute(
            """
            SELECT r.run_id,a.admission_id,a.dispatch_id,a.revision,a.graph_bytes,a.graph_digest,
                   a.authority_json,a.authority_digest
            FROM local_execution_runs r
            JOIN local_execution_admissions a ON a.admission_id=r.admission_id
            WHERE r.run_id=?
            """,
            (run_id,),
        ).fetchone()
        if not row:
            raise NotFoundError("local execution run not found")
        graph_bytes = bytes(row["graph_bytes"])
        graph_digest = _digest_string(row["graph_digest"], "stored graph digest")
        if digest_bytes(graph_bytes) != graph_digest:
            raise IntegrityError("stored local ExecutionGraph digest mismatch")
        graph = self._decode_canonical_object(graph_bytes, "stored local ExecutionGraph")
        try:
            validate_execution_graph(graph)
            self._validate_local_subset(graph)
        except (ValidationError, GateBlockedError) as error:
            raise IntegrityError("stored local ExecutionGraph is no longer admissible") from error
        if graph["dispatch_id"] != row["dispatch_id"] or graph["revision"] != row["revision"]:
            raise IntegrityError("stored local ExecutionGraph identity mismatch")

        authority_bytes = row["authority_json"].encode("utf-8")
        if digest_bytes(authority_bytes) != row["authority_digest"]:
            raise IntegrityError("stored local execution authority digest mismatch")
        authority = self._decode_canonical_object(authority_bytes, "stored local execution authority")
        required = {
            "schema",
            "authority_ceiling",
            "graph_digest",
            "compilation_authority",
            "compilation_authority_digest",
            "acceptance",
            "acceptance_digest",
        }
        if set(authority) != required or authority["schema"] != ADMISSION_SCHEMA:
            raise IntegrityError("stored local execution authority shape is invalid")
        if authority["authority_ceiling"] != AUTHORITY_CEILING or authority["graph_digest"] != graph_digest:
            raise IntegrityError("stored local execution authority graph binding mismatch")
        compilation_authority = authority["compilation_authority"]
        compilation_authority_bytes = canonical_bytes(compilation_authority)
        compilation_authority_digest = digest_bytes(compilation_authority_bytes)
        if compilation_authority_digest != authority["compilation_authority_digest"]:
            raise IntegrityError("stored compilation authority digest mismatch")
        self._validate_compilation_authority(compilation_authority, graph, graph_digest)
        acceptance = authority["acceptance"]
        acceptance_bytes = canonical_bytes(acceptance)
        if digest_bytes(acceptance_bytes) != authority["acceptance_digest"]:
            raise IntegrityError("stored local acceptance digest mismatch")
        self._validate_acceptance(
            acceptance,
            graph,
            graph_digest,
            compilation_authority_digest,
            authority["acceptance_digest"],
        )
        if acceptance["allocation_id"] != compilation_authority["allocation_id"]:
            raise IntegrityError("stored local acceptance allocation mismatch")
        expected_admission_id = _derived_id(
            "adm_",
            {
                "schema": "aci.local-execution-admission-id-preimage@1",
                "dispatch_id": graph["dispatch_id"],
                "revision": graph["revision"],
                "graph_digest": graph_digest,
                "authority_digest": row["authority_digest"],
            },
        )
        expected_run_id = _derived_id(
            "run_",
            {"schema": "aci.local-execution-run-id-preimage@1", "admission_id": expected_admission_id},
        )
        if row["admission_id"] != expected_admission_id or row["run_id"] != expected_run_id:
            raise IntegrityError("stored local execution derived identity mismatch")
        return graph, graph_digest, authority

    def _graph(self, conn: Any, run_id: str) -> tuple[dict[str, Any], str]:
        graph, graph_digest, _ = self._verified_graph_authority(conn, run_id)
        return graph, graph_digest

    @staticmethod
    def _receipt_schema(graph: dict[str, Any]) -> dict[str, Any]:
        member_id = graph["audit_requirements"]["receipt_schema_member_id"]
        member = next(item for item in graph["content_members"] if item["member_id"] == member_id)
        schema = parse_strict_json(member["content"])
        if not isinstance(schema, dict):
            raise IntegrityError("pinned local receipt schema is not an object")
        return schema

    def _receipt_audit(
        self,
        graph: dict[str, Any],
        node_id: str | None,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        node = None if node_id is None else self._node(graph, node_id)
        return {
            "objective_json": canonical_text(graph["objective"]),
            "agent_json": canonical_text(None if node is None else node["agent"]),
            "route_json": canonical_text([] if node is None else self._incoming(graph, node_id)),
            "result_json": canonical_text(payload),
        }

    def _validate_receipt_body(self, graph: dict[str, Any], receipt: dict[str, Any]) -> None:
        try:
            Draft202012Validator(self._receipt_schema(graph)).validate(receipt)
        except JsonSchemaValidationError as error:
            raise IntegrityError("local execution receipt violates pinned graph schema") from error
        payload = parse_strict_json(receipt["payload_json"])
        if not isinstance(payload, dict) or canonical_text(payload) != receipt["payload_json"]:
            raise IntegrityError("local execution receipt payload is not canonical JSON")
        expected_audit = self._receipt_audit(graph, receipt["node_id"], payload)
        if receipt.get("audit") != expected_audit:
            raise IntegrityError("local execution receipt audit projection mismatch")

    def _verify_persisted_evidence(
        self, conn: Any, run_id: str
    ) -> tuple[dict[str, Any], str]:
        """Fail closed on any durable byte/digest/head drift before use or presentation."""
        graph, graph_digest, _ = self._verified_graph_authority(conn, run_id)
        run_head = conn.execute(
            "SELECT status,cancel_requested,terminal_reason,next_receipt_sequence FROM local_execution_runs WHERE run_id=?",
            (run_id,),
        ).fetchone()
        if (
            not run_head
            or run_head["status"] not in {"pending", "running", *RUN_TERMINAL}
            or run_head["cancel_requested"] not in (0, 1)
            or isinstance(run_head["terminal_reason"], bytes)
        ):
            raise IntegrityError("stored local execution run head is invalid")
        node_rows = conn.execute(
            "SELECT * FROM local_execution_nodes WHERE run_id=? ORDER BY node_ordinal", (run_id,)
        ).fetchall()
        if len(node_rows) != len(graph["nodes"]):
            raise IntegrityError("stored local execution node set mismatch")
        for ordinal, (row, node) in enumerate(zip(node_rows, graph["nodes"], strict=True)):
            if (
                row["node_id"] != node["node_id"]
                or row["node_ordinal"] != ordinal
                or row["max_attempts"] != node["limits"]["max_attempts"]
                or row["display_name"] != node["agent"]["display_name"]
                or row["role"] != node["agent"]["role"]
                or row["status"] not in {"pending", "running", *NODE_TERMINAL}
                or isinstance(row["attempts"], bool)
                or not isinstance(row["attempts"], int)
                or not 0 <= row["attempts"] <= row["max_attempts"]
            ):
                raise IntegrityError("stored local execution node authority mismatch")
            if row["output_json"] is None:
                if row["output_digest"] is not None:
                    raise IntegrityError("stored local execution output digest is orphaned")
            else:
                output_bytes = row["output_json"].encode("utf-8")
                outputs = self._decode_canonical_object(output_bytes, "stored local worker outputs")
                if digest_bytes(output_bytes) != row["output_digest"]:
                    raise IntegrityError("stored local execution output digest mismatch")
                declared = {item["output_id"] for item in node["outputs"]}
                if set(outputs) - declared:
                    raise IntegrityError("stored local execution output authority mismatch")

        attempt_rows = conn.execute(
            """
            SELECT a.* FROM local_execution_attempts a
            JOIN local_execution_nodes n ON n.run_id=a.run_id AND n.node_id=a.node_id
            WHERE a.run_id=? ORDER BY n.node_ordinal,a.attempt_number
            """,
            (run_id,),
        ).fetchall()
        attempt_ids: set[str] = set()
        attempt_numbers: dict[str, list[int]] = {node["node_id"]: [] for node in graph["nodes"]}
        for row in attempt_rows:
            node = self._node(graph, row["node_id"])
            if (
                row["status"] not in {"launched", "succeeded", "failed", "validation_failed", "cancelled"}
                or isinstance(row["attempt_number"], bool)
                or not isinstance(row["attempt_number"], int)
                or row["attempt_number"] < 1
            ):
                raise IntegrityError("stored local execution attempt head is invalid")
            attempt_numbers[node["node_id"]].append(row["attempt_number"])
            expected_attempt_id = _derived_id(
                "attempt_",
                {
                    "schema": "aci.local-attempt-id-preimage@1",
                    "run_id": run_id,
                    "node_id": node["node_id"],
                    "attempt_number": row["attempt_number"],
                },
            )
            if row["attempt_id"] != expected_attempt_id:
                raise IntegrityError("stored local execution attempt identity mismatch")
            attempt_ids.add(row["attempt_id"])
            assignment_bytes = row["assignment_json"].encode("utf-8")
            assignment = self._decode_canonical_object(
                assignment_bytes, "stored local worker assignment"
            )
            if digest_bytes(assignment_bytes) != row["assignment_digest"]:
                raise IntegrityError("stored local worker assignment digest mismatch")
            inputs, missing = self._resolve_inputs(conn, run_id, graph, node)
            if missing:
                raise IntegrityError("stored local worker assignment lost required inputs")
            expected_assignment = WorkerAssignment(
                run_id=run_id,
                graph_digest=graph_digest,
                node_id=node["node_id"],
                attempt_id=row["attempt_id"],
                attempt_number=row["attempt_number"],
                display_name=node["agent"]["display_name"],
                role=node["agent"]["role"],
                objective=node["objective"],
                instructions=node["instructions"],
                agent=node["agent"],
                tools=tuple(node["tools"]),
                inputs=inputs,
            ).value()
            if assignment != expected_assignment:
                raise IntegrityError("stored local worker assignment authority mismatch")
            if row["result_json"] is None:
                if row["result_digest"] is not None:
                    raise IntegrityError("stored local worker result digest is orphaned")
            else:
                result_bytes = row["result_json"].encode("utf-8")
                result = self._decode_canonical_object(result_bytes, "stored local worker result")
                if digest_bytes(result_bytes) != row["result_digest"]:
                    raise IntegrityError("stored local worker result digest mismatch")
                if (
                    set(result) != {"schema", "outputs", "validations"}
                    or result["schema"] != "aci.local-worker-result@1"
                    or not isinstance(result["outputs"], dict)
                    or not isinstance(result["validations"], dict)
                ):
                    raise IntegrityError("stored local worker result shape is invalid")

        for row in node_rows:
            expected_numbers = list(range(1, row["attempts"] + 1))
            if attempt_numbers[row["node_id"]] != expected_numbers:
                raise IntegrityError("stored local execution attempt head mismatch")

        receipt_rows = conn.execute(
            """
            SELECT receipt_json,receipt_digest,sequence FROM local_execution_receipts
            WHERE run_id=? ORDER BY sequence
            """,
            (run_id,),
        ).fetchall()
        for expected_sequence, row in enumerate(receipt_rows):
            receipt_bytes = row["receipt_json"].encode("utf-8")
            receipt = self._decode_canonical_object(receipt_bytes, "stored local execution receipt")
            if digest_bytes(receipt_bytes) != row["receipt_digest"]:
                raise IntegrityError("stored local execution receipt digest mismatch")
            if (
                row["sequence"] != expected_sequence
                or receipt.get("schema") != RECEIPT_SCHEMA
                or receipt.get("run_id") != run_id
                or receipt.get("sequence") != expected_sequence
                or receipt.get("graph_digest") != graph_digest
                or (receipt.get("node_id") is not None and receipt["node_id"] not in {n["node_id"] for n in graph["nodes"]})
                or (receipt.get("attempt_id") is not None and receipt["attempt_id"] not in attempt_ids)
            ):
                raise IntegrityError("stored local execution receipt authority mismatch")
            self._validate_receipt_body(graph, receipt)
        if run_head["next_receipt_sequence"] != len(receipt_rows):
            raise IntegrityError("stored local execution receipt sequence head mismatch")
        return graph, graph_digest

    def _prepare_next_assignment(self, run_id: str) -> WorkerAssignment | None:
        with self.database.write() as conn:
            run = conn.execute(
                "SELECT * FROM local_execution_runs WHERE run_id=?", (run_id,)
            ).fetchone()
            if not run:
                raise NotFoundError("local execution run not found")
            if run["status"] in RUN_TERMINAL:
                return None
            graph, graph_digest = self._verify_persisted_evidence(conn, run_id)
            if run["cancel_requested"]:
                self._cancel_run(conn, run_id, run["terminal_reason"] or "operator_cancelled")
                return None
            running = conn.execute(
                """
                SELECT n.node_id,n.attempts,a.attempt_id FROM local_execution_nodes n
                LEFT JOIN local_execution_attempts a
                  ON a.run_id=n.run_id AND a.node_id=n.node_id
                 AND a.attempt_number=n.attempts
                WHERE n.run_id=? AND n.status='running'
                """,
                (run_id,),
            ).fetchall()
            for row in running:
                if row["attempt_id"]:
                    conn.execute(
                        """
                        UPDATE local_execution_attempts
                        SET status='failed',failure_code='interrupted_local_attempt'
                        WHERE attempt_id=? AND status='launched'
                        """,
                        (row["attempt_id"],),
                    )
                node = self._node(graph, row["node_id"])
                self._retry_or_exhaust(
                    conn,
                    run_id,
                    node,
                    row["attempts"],
                    "interrupted_local_attempt",
                    attempt_id=row["attempt_id"],
                )

            while True:
                rows = conn.execute(
                    """
                    SELECT * FROM local_execution_nodes
                    WHERE run_id=? ORDER BY node_ordinal
                    """,
                    (run_id,),
                ).fetchall()
                states = {row["node_id"]: row["status"] for row in rows}
                if self._finalize_if_decided(conn, run_id, graph, states):
                    return None
                selected: dict[str, Any] | None = None
                for node in graph["nodes"]:
                    if states[node["node_id"]] == "pending" and self._is_ready(graph, node, states):
                        selected = node
                        break
                if selected is None:
                    skipped = False
                    for node in graph["nodes"]:
                        node_id = node["node_id"]
                        if states[node_id] != "pending":
                            continue
                        predecessors = self._incoming(graph, node_id)
                        if predecessors and all(
                            states[edge["from_node_id"]] in NODE_TERMINAL
                            for edge in predecessors
                        ):
                            conn.execute(
                                """
                                UPDATE local_execution_nodes
                                SET status='skipped',terminal_reason='route_not_activated'
                                WHERE run_id=? AND node_id=?
                                """,
                                (run_id, node_id),
                            )
                            self._append_receipt(
                                conn,
                                run_id,
                                "node_skipped",
                                {"reason": "route_not_activated"},
                                node_id=node_id,
                            )
                            skipped = True
                            break
                    if skipped:
                        continue
                    if any(status == "running" for status in states.values()):
                        raise ConflictError("local execution already has a running attempt")
                    raise IntegrityError("local execution graph has no deterministic next state")

                inputs, missing = self._resolve_inputs(conn, run_id, graph, selected)
                if missing:
                    condition = next(
                        (
                            item
                            for item in selected["stop_conditions"]
                            if item["when"]["kind"] == "input_unavailable"
                            and item["when"]["input_id"] in missing
                        ),
                        None,
                    )
                    if condition is None:
                        self._apply_action(
                            conn,
                            run_id,
                            selected,
                            "fail_graph",
                            "required_input_unavailable",
                            attempt_id=None,
                        )
                    else:
                        self._apply_action(
                            conn,
                            run_id,
                            selected,
                            condition["action"],
                            condition["reason_code"],
                            attempt_id=None,
                        )
                    continue

                current = next(row for row in rows if row["node_id"] == selected["node_id"])
                attempt_number = current["attempts"] + 1
                attempt_id = _derived_id(
                    "attempt_",
                    {
                        "schema": "aci.local-attempt-id-preimage@1",
                        "run_id": run_id,
                        "node_id": selected["node_id"],
                        "attempt_number": attempt_number,
                    },
                )
                assignment = WorkerAssignment(
                    run_id=run_id,
                    graph_digest=graph_digest,
                    node_id=selected["node_id"],
                    attempt_id=attempt_id,
                    attempt_number=attempt_number,
                    display_name=selected["agent"]["display_name"],
                    role=selected["agent"]["role"],
                    objective=selected["objective"],
                    instructions=selected["instructions"],
                    agent=selected["agent"],
                    tools=tuple(selected["tools"]),
                    inputs=inputs,
                )
                assignment_json = canonical_text(assignment.value())
                conn.execute(
                    """
                    UPDATE local_execution_nodes SET status='running',attempts=?
                    WHERE run_id=? AND node_id=? AND status='pending'
                    """,
                    (attempt_number, run_id, selected["node_id"]),
                )
                conn.execute(
                    """
                    INSERT INTO local_execution_attempts(
                      attempt_id,run_id,node_id,attempt_number,status,
                      assignment_json,assignment_digest
                    ) VALUES(?,?,?,?,?,?,?)
                    """,
                    (
                        attempt_id,
                        run_id,
                        selected["node_id"],
                        attempt_number,
                        "launched",
                        assignment_json,
                        digest_bytes(assignment_json.encode("utf-8")),
                    ),
                )
                self._append_receipt(
                    conn,
                    run_id,
                    "worker_launched",
                    {
                        "attempt_number": attempt_number,
                        "display_name": assignment.display_name,
                        "role": assignment.role,
                    },
                    node_id=selected["node_id"],
                    attempt_id=attempt_id,
                )
                return assignment

    @staticmethod
    def _node(graph: dict[str, Any], node_id: str) -> dict[str, Any]:
        return next(node for node in graph["nodes"] if node["node_id"] == node_id)

    @staticmethod
    def _incoming(graph: dict[str, Any], node_id: str) -> list[dict[str, Any]]:
        return [edge for edge in graph["edges"] if edge["to_node_id"] == node_id]

    def _is_ready(
        self, graph: dict[str, Any], node: dict[str, Any], states: Mapping[str, str]
    ) -> bool:
        incoming = self._incoming(graph, node["node_id"])
        if not incoming:
            return node["node_id"] in graph["lifecycle"]["entry_nodes"]

        def active(edge: dict[str, Any]) -> bool:
            source = states[edge["from_node_id"]]
            return (
                (edge["condition"] == "on_success" and source == "succeeded")
                or (edge["condition"] == "on_failure" and source == "failed")
                or (edge["condition"] == "always" and source in NODE_TERMINAL)
            )

        if node["start_when"] == "all_predecessors_succeeded":
            return all(active(edge) for edge in incoming)
        if node["start_when"] == "any_predecessor_succeeded":
            return any(active(edge) for edge in incoming)
        return False

    @staticmethod
    def _content_value(member: dict[str, Any]) -> Any:
        if member["media_type"] in {"application/json", "application/schema+json"}:
            return parse_strict_json(member["content"])
        return member["content"]

    def _resolve_inputs(
        self,
        conn: Any,
        run_id: str,
        graph: dict[str, Any],
        node: dict[str, Any],
    ) -> tuple[dict[str, Any], set[str]]:
        members = {item["member_id"]: item for item in graph["content_members"]}
        values: dict[str, Any] = {}
        missing: set[str] = set()
        for item in node["inputs"]:
            source = item["source"]
            value: Any = None
            available = False
            if source["kind"] == "content_member":
                member = members.get(source["member_id"])
                if member is not None:
                    value = self._content_value(member)
                    available = True
            else:
                row = conn.execute(
                    """
                    SELECT status,output_json FROM local_execution_nodes
                    WHERE run_id=? AND node_id=?
                    """,
                    (run_id, source["node_id"]),
                ).fetchone()
                if row and row["status"] == "succeeded" and row["output_json"] is not None:
                    outputs = json.loads(row["output_json"])
                    if source["output_id"] in outputs:
                        value = outputs[source["output_id"]]
                        available = True
            if available:
                values[item["input_id"]] = value
            elif item["required"]:
                missing.add(item["input_id"])
        return values, missing

    def _record_worker_failure(self, assignment: WorkerAssignment, code: str) -> None:
        with self.database.write() as conn:
            graph, _ = self._verify_persisted_evidence(conn, assignment.run_id)
            node = self._node(graph, assignment.node_id)
            self._require_launched(conn, assignment)
            conn.execute(
                """
                UPDATE local_execution_attempts SET status='failed',failure_code=?
                WHERE attempt_id=?
                """,
                (code, assignment.attempt_id),
            )
            self._append_receipt(
                conn,
                assignment.run_id,
                "worker_failed",
                {"failure_code": code, "attempt_number": assignment.attempt_number},
                node_id=assignment.node_id,
                attempt_id=assignment.attempt_id,
            )
            self._retry_or_exhaust(
                conn,
                assignment.run_id,
                node,
                assignment.attempt_number,
                code,
                attempt_id=assignment.attempt_id,
            )

    @staticmethod
    def _require_launched(conn: Any, assignment: WorkerAssignment) -> None:
        row = conn.execute(
            """
            SELECT status FROM local_execution_attempts
            WHERE attempt_id=? AND run_id=? AND node_id=? AND attempt_number=?
            """,
            (
                assignment.attempt_id,
                assignment.run_id,
                assignment.node_id,
                assignment.attempt_number,
            ),
        ).fetchone()
        if not row or row["status"] != "launched":
            raise ConflictError("local worker attempt is not launched")

    def _assert_assignment_durable(self, assignment: WorkerAssignment) -> None:
        with self.database.connect() as conn:
            self._verify_persisted_evidence(conn, assignment.run_id)
            row = conn.execute(
                "SELECT status,assignment_json,assignment_digest FROM local_execution_attempts WHERE attempt_id=?",
                (assignment.attempt_id,),
            ).fetchone()
            expected = canonical_bytes(assignment.value())
            if (
                not row
                or row["status"] != "launched"
                or row["assignment_json"].encode("utf-8") != expected
                or row["assignment_digest"] != digest_bytes(expected)
            ):
                raise IntegrityError("local worker assignment changed before adapter launch")

    def _record_worker_result(
        self, assignment: WorkerAssignment, result: LocalWorkerResult
    ) -> None:
        with self.database.write() as conn:
            graph, _ = self._verify_persisted_evidence(conn, assignment.run_id)
            node = self._node(graph, assignment.node_id)
            self._require_launched(conn, assignment)
            result_value = result.value()
            result_json = canonical_text(result_value)
            result_digest = digest_bytes(result_json.encode("utf-8"))
            failure_action, failure_code = self._validate_result(graph, node, result)
            if failure_code is not None:
                conn.execute(
                    """
                    UPDATE local_execution_attempts
                    SET status='validation_failed',result_json=?,result_digest=?,failure_code=?
                    WHERE attempt_id=?
                    """,
                    (result_json, result_digest, failure_code, assignment.attempt_id),
                )
                self._append_receipt(
                    conn,
                    assignment.run_id,
                    "worker_result_rejected",
                    {"failure_code": failure_code, "result_digest": result_digest},
                    node_id=assignment.node_id,
                    attempt_id=assignment.attempt_id,
                )
                if failure_action == "retry":
                    self._retry_or_exhaust(
                        conn,
                        assignment.run_id,
                        node,
                        assignment.attempt_number,
                        failure_code,
                        attempt_id=assignment.attempt_id,
                    )
                else:
                    self._apply_action(
                        conn,
                        assignment.run_id,
                        node,
                        failure_action or "fail_graph",
                        failure_code,
                        attempt_id=assignment.attempt_id,
                    )
                return

            for stop in node["stop_conditions"]:
                if self._predicate(stop["when"], result.outputs, set()):
                    conn.execute(
                        """
                        UPDATE local_execution_attempts
                        SET status='succeeded',result_json=?,result_digest=?
                        WHERE attempt_id=?
                        """,
                        (result_json, result_digest, assignment.attempt_id),
                    )
                    self._apply_action(
                        conn,
                        assignment.run_id,
                        node,
                        stop["action"],
                        stop["reason_code"],
                        attempt_id=assignment.attempt_id,
                    )
                    return
            if not self._predicate(node["success_condition"], result.outputs, set()):
                conn.execute(
                    """
                    UPDATE local_execution_attempts
                    SET status='validation_failed',result_json=?,result_digest=?,
                        failure_code='success_condition_not_met'
                    WHERE attempt_id=?
                    """,
                    (result_json, result_digest, assignment.attempt_id),
                )
                self._retry_or_exhaust(
                    conn,
                    assignment.run_id,
                    node,
                    assignment.attempt_number,
                    "success_condition_not_met",
                    attempt_id=assignment.attempt_id,
                )
                return
            outputs_json = canonical_text(result.outputs)
            conn.execute(
                """
                UPDATE local_execution_attempts
                SET status='succeeded',result_json=?,result_digest=? WHERE attempt_id=?
                """,
                (result_json, result_digest, assignment.attempt_id),
            )
            conn.execute(
                """
                UPDATE local_execution_nodes
                SET status='succeeded',output_json=?,output_digest=?,terminal_reason=NULL
                WHERE run_id=? AND node_id=?
                """,
                (
                    outputs_json,
                    digest_bytes(outputs_json.encode("utf-8")),
                    assignment.run_id,
                    assignment.node_id,
                ),
            )
            self._append_receipt(
                conn,
                assignment.run_id,
                "node_succeeded",
                {
                    "attempt_number": assignment.attempt_number,
                    "result_digest": result_digest,
                    "output_digest": digest_bytes(outputs_json.encode("utf-8")),
                },
                node_id=assignment.node_id,
                attempt_id=assignment.attempt_id,
            )

    @staticmethod
    def _schema_members(graph: dict[str, Any]) -> dict[str, dict[str, Any]]:
        return {member["member_id"]: member for member in graph["content_members"]}

    def _validate_result(
        self, graph: dict[str, Any], node: dict[str, Any], result: LocalWorkerResult
    ) -> tuple[str | None, str | None]:
        if not isinstance(result.outputs, dict) or not isinstance(result.validations, dict):
            return "fail_graph", "worker_result_shape_invalid"
        declared = {item["output_id"]: item for item in node["outputs"]}
        if set(result.outputs) - set(declared):
            return "fail_graph", "undeclared_worker_output"
        if any(item["required"] and output_id not in result.outputs for output_id, item in declared.items()):
            return "retry", "required_worker_output_missing"
        members = self._schema_members(graph)
        for output_id, value in result.outputs.items():
            member = members[declared[output_id]["schema_member_id"]]
            try:
                schema = parse_strict_json(member["content"])
                Draft202012Validator.check_schema(schema)
                Draft202012Validator(schema).validate(value)
            except (ValidationError, SchemaError, JsonSchemaValidationError):
                return "retry", "worker_output_schema_invalid"
        rules = {rule["rule_id"]: rule for rule in node["validation"]}
        if set(result.validations) != set(rules) or any(
            not isinstance(value, bool) for value in result.validations.values()
        ):
            return "fail_graph", "worker_validation_evidence_invalid"
        for rule in node["validation"]:
            if not result.validations[rule["rule_id"]]:
                return rule["on_fail"], f"validation_failed:{rule['rule_id']}"
        return None, None

    @staticmethod
    def _pointer(value: Any, pointer: str) -> tuple[bool, Any]:
        if pointer == "":
            return True, value
        if not isinstance(pointer, str) or not pointer.startswith("/"):
            return False, None
        current = value
        for raw in pointer[1:].split("/"):
            token = raw.replace("~1", "/").replace("~0", "~")
            if isinstance(current, dict) and token in current:
                current = current[token]
            elif isinstance(current, list) and token.isdigit() and int(token) < len(current):
                current = current[int(token)]
            else:
                return False, None
        return True, current

    def _predicate(
        self, predicate: dict[str, Any], outputs: dict[str, Any], missing_inputs: set[str]
    ) -> bool:
        kind = predicate["kind"]
        if kind == "output_present":
            return predicate["output_id"] in outputs
        if kind == "output_field_equals":
            if predicate["output_id"] not in outputs:
                return False
            present, value = self._pointer(
                outputs[predicate["output_id"]], predicate["json_pointer"]
            )
            return present and type(value) is type(predicate["value"]) and value == predicate["value"]
        if kind == "input_unavailable":
            return predicate["input_id"] in missing_inputs
        return False

    def _retry_or_exhaust(
        self,
        conn: Any,
        run_id: str,
        node: dict[str, Any],
        attempt_number: int,
        reason: str,
        *,
        attempt_id: str | None,
    ) -> None:
        if attempt_number < node["limits"]["max_attempts"]:
            conn.execute(
                """
                UPDATE local_execution_nodes SET status='pending',terminal_reason=?
                WHERE run_id=? AND node_id=?
                """,
                (reason, run_id, node["node_id"]),
            )
            self._append_receipt(
                conn,
                run_id,
                "node_retry_scheduled",
                {"failure_code": reason, "next_attempt_number": attempt_number + 1},
                node_id=node["node_id"],
                attempt_id=attempt_id,
            )
            return
        exhausted = next(
            (
                item
                for item in node["stop_conditions"]
                if item["when"]["kind"] == "attempts_exhausted"
            ),
            None,
        )
        if exhausted is None:
            conn.execute(
                """
                UPDATE local_execution_nodes SET status='failed',terminal_reason='attempts_exhausted'
                WHERE run_id=? AND node_id=?
                """,
                (run_id, node["node_id"]),
            )
            self._append_receipt(
                conn,
                run_id,
                "node_failed",
                {"reason": "attempts_exhausted"},
                node_id=node["node_id"],
                attempt_id=attempt_id,
            )
            return
        self._apply_action(
            conn,
            run_id,
            node,
            exhausted["action"],
            exhausted["reason_code"],
            attempt_id=attempt_id,
        )

    def _apply_action(
        self,
        conn: Any,
        run_id: str,
        node: dict[str, Any],
        action: str,
        reason: str,
        *,
        attempt_id: str | None,
    ) -> None:
        node_status = {"stop_node": "stopped", "stop_graph": "stopped", "fail_graph": "failed"}[action]
        conn.execute(
            """
            UPDATE local_execution_nodes SET status=?,terminal_reason=?
            WHERE run_id=? AND node_id=?
            """,
            (node_status, reason, run_id, node["node_id"]),
        )
        self._append_receipt(
            conn,
            run_id,
            "node_terminal_action",
            {"action": action, "reason": reason},
            node_id=node["node_id"],
            attempt_id=attempt_id,
        )
        if action in {"stop_graph", "fail_graph"}:
            run_status = "stopped" if action == "stop_graph" else "failed"
            conn.execute(
                """
                UPDATE local_execution_nodes
                SET status='skipped',terminal_reason=?
                WHERE run_id=? AND status='pending'
                """,
                (f"graph_{run_status}", run_id),
            )
            conn.execute(
                "UPDATE local_execution_runs SET status=?,terminal_reason=? WHERE run_id=?",
                (run_status, reason, run_id),
            )
            self._append_receipt(
                conn, run_id, f"run_{run_status}", {"reason": reason}
            )

    def _finalize_if_decided(
        self,
        conn: Any,
        run_id: str,
        graph: dict[str, Any],
        states: Mapping[str, str],
    ) -> bool:
        lifecycle = graph["lifecycle"]
        if lifecycle["failure"] == "fail_fast" and any(
            status == "failed" for status in states.values()
        ):
            self._finish_run(conn, run_id, "failed", "node_failed")
            return True
        terminal_states = [states[node_id] for node_id in lifecycle["terminal_nodes"]]
        success = (
            all(status == "succeeded" for status in terminal_states)
            if lifecycle["completion"] == "all_terminal_succeeded"
            else any(status == "succeeded" for status in terminal_states)
        )
        if success:
            self._finish_run(conn, run_id, "succeeded", "completion_policy_satisfied")
            return True
        if all(status in NODE_TERMINAL for status in states.values()):
            self._finish_run(conn, run_id, "failed", "completion_policy_unsatisfied")
            return True
        return False

    def _finish_run(self, conn: Any, run_id: str, status: str, reason: str) -> None:
        conn.execute(
            """
            UPDATE local_execution_nodes SET status='skipped',terminal_reason=?
            WHERE run_id=? AND status='pending'
            """,
            (f"run_{status}", run_id),
        )
        conn.execute(
            "UPDATE local_execution_runs SET status=?,terminal_reason=? WHERE run_id=?",
            (status, reason, run_id),
        )
        self._append_receipt(conn, run_id, f"run_{status}", {"reason": reason})

    def _cancel_run(self, conn: Any, run_id: str, reason: str) -> None:
        conn.execute(
            """
            UPDATE local_execution_attempts
            SET status='cancelled',failure_code=?
            WHERE run_id=? AND status='launched'
            """,
            (reason, run_id),
        )
        conn.execute(
            """
            UPDATE local_execution_nodes SET status='cancelled',terminal_reason=?
            WHERE run_id=? AND status NOT IN ('succeeded','failed','cancelled','skipped','stopped')
            """,
            (reason, run_id),
        )
        conn.execute(
            "UPDATE local_execution_runs SET status='cancelled',terminal_reason=? WHERE run_id=?",
            (reason, run_id),
        )
        self._append_receipt(conn, run_id, "run_cancelled", {"reason": reason})
