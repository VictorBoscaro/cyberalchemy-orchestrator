"""Test-only POLICY-002 durable fake-denial seam; never execution authority."""

from __future__ import annotations

import sqlite3
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from implementations.server.runtime.canonical import (
    canonical_bytes,
    digest_bytes,
    parse_strict_json,
)
from implementations.server.runtime.database import RuntimeDatabase
from implementations.server.runtime.errors import ConflictError, IntegrityError, ValidationError
from implementations.server.runtime.execution_policy import (
    ExecutionPolicyContractError,
    parse_execution_authority_fence,
    parse_production_policy_document,
    parse_resource_budget,
    parse_sandbox_policy,
)
from implementations.tests.runtime.policy_lineage_harness import (
    SyntheticPolicyLineageHarness,
)


PREIMAGE_SCHEMA = "aci.execution-policy-fake-denial@1"
RECEIPT_SCHEMA = "aci.execution-policy-fake-denial-receipt@1"
AUTHORITY = "test-only-non-executable"
SPEC_DECISION = "denied"
SPEC_REASON_CODES = (
    "resource.max_wall_time_ms.zero",
    "sandbox.process.no-executable-grant",
)
# Candidate aliases are deliberately separate from the stored-evidence oracle so tests can
# simulate controlled projection drift without making authentic stored rows look corrupt.
DECISION = SPEC_DECISION
REASON_CODES = SPEC_REASON_CODES
DENIAL_TABLE = "test_execution_policy_fake_denial_receipts"
SOURCE_RECEIPT_TABLE = "test_execution_policy_lineage_receipts"
EXPECTED_DENIAL_DIGEST = (
    "sha256:bc8655ac88276258d8e320b8a9757a8b625c9e9249dc7255a5578d2eb7e65399"
)
EXPECTED_RECEIPT_DIGEST = (
    "sha256:5ffde80fbfb897ceb4b90cb85bcdb019538777c91ae3525ac0f7e0ebc43a9b11"
)
ORACLE_DENIAL_KEY = "policy-denial-command-001"
ACTION_ATTEMPT_LABELS = (
    "filesystem.read",
    "filesystem.write",
    "network.connect",
    "process.child.start",
    "credential.resolve",
    "tool.call",
    "resource.wall_time.consume_positive",
    "resource.input_tokens.consume_positive",
    "resource.output_tokens.consume_positive",
    "resource.tool_calls.consume_positive",
    "resource.payload_bytes.consume_positive",
    "resource.artifact_bytes.consume_positive",
)
FAILPOINTS = (
    "policy_denial.after_begin",
    "policy_denial.after_receipt",
    "policy_denial.before_commit",
    "policy_denial.after_commit",
)
RECEIPT_FIELDS = {
    "schema",
    "authority",
    "denial_key",
    "lineage_identity",
    "lineage_unit_digest",
    "resource_budget_digest",
    "sandbox_policy_digest",
    "decision",
    "reason_codes",
    "denial_digest",
}


def _closed_action_attempt_labels() -> tuple[str, ...]:
    return (
        "filesystem.read",
        "filesystem.write",
        "network.connect",
        "process.child.start",
        "credential.resolve",
        "tool.call",
        "resource.wall_time.consume_positive",
        "resource.input_tokens.consume_positive",
        "resource.output_tokens.consume_positive",
        "resource.tool_calls.consume_positive",
        "resource.payload_bytes.consume_positive",
        "resource.artifact_bytes.consume_positive",
    )


def _closed_failpoints() -> tuple[str, ...]:
    return (
        "policy_denial.after_begin",
        "policy_denial.after_receipt",
        "policy_denial.before_commit",
        "policy_denial.after_commit",
    )


class SyntheticDenialValidationError(ValidationError):
    """The proposed test-only denial is outside the exact closed L2 fixture."""


class SyntheticDenialConflict(ConflictError):
    """A denial key or lineage identity was reused with immutable evidence drift."""


class ExecutionPolicyFakeDenialHarness:
    """Persist one package-level denial in one local test-only table."""

    def __init__(self, database_path: Path) -> None:
        path = Path(database_path)
        if str(path) == ":memory:":
            raise SyntheticDenialValidationError("in-memory SQLite is not admitted")
        self.database = RuntimeDatabase(path)
        self.database.migrate()
        # This creates/reuses only the already-reviewed L1 test tables. L2 consumes L1 through
        # reopen_synthetic_lineage and never imports its private SQL, table constants or validators.
        SyntheticPolicyLineageHarness(path)
        self._validate_label_corpus(ACTION_ATTEMPT_LABELS)
        self._create_test_table()

    def _create_test_table(self) -> None:
        with self.database.write() as conn:
            conn.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {DENIAL_TABLE}(
                  lineage_identity TEXT PRIMARY KEY
                    REFERENCES {SOURCE_RECEIPT_TABLE}(lineage_identity),
                  denial_key TEXT NOT NULL UNIQUE,
                  lineage_unit_digest TEXT NOT NULL,
                  resource_budget_digest TEXT NOT NULL,
                  sandbox_policy_digest TEXT NOT NULL,
                  denial_digest TEXT NOT NULL,
                  receipt_digest TEXT NOT NULL,
                  receipt_bytes BLOB NOT NULL
                )
                """
            )

    @staticmethod
    def _require_nonempty_string(value: Any, label: str) -> str:
        if not isinstance(value, str) or not value:
            raise SyntheticDenialValidationError(f"{label} must be a non-empty string")
        return value

    @classmethod
    def _validate_label_corpus(cls, labels: Sequence[str]) -> None:
        if isinstance(labels, (str, bytes, bytearray)) or len(labels) != 12:
            raise SyntheticDenialValidationError("label corpus must contain exactly twelve items")
        if any(not isinstance(label, str) or not label for label in labels):
            raise SyntheticDenialValidationError("every label must be a non-empty string")
        if len(set(labels)) != 12:
            raise SyntheticDenialValidationError("label corpus contains a duplicate")
        if tuple(labels) != _closed_action_attempt_labels():
            raise SyntheticDenialValidationError("label corpus is not the exact closed selector set")

    @classmethod
    def _require_action_label(cls, value: Any) -> str:
        if not isinstance(value, str) or not value:
            raise SyntheticDenialValidationError(
                "action_attempt_label must be one non-empty scalar string"
            )
        if value not in _closed_action_attempt_labels():
            raise SyntheticDenialValidationError("unknown action-attempt label")
        return value

    @staticmethod
    def _require_failpoint(value: Any) -> str | None:
        if value is None:
            return None
        if not isinstance(value, str) or value not in _closed_failpoints():
            raise SyntheticDenialValidationError("failpoint must be one closed nominal label")
        return value

    @staticmethod
    def _trip(configured: str | None, point: str) -> None:
        if configured == point:
            raise RuntimeError(point)

    @staticmethod
    def _reject_production_authority(combined: bytes, harness_fence: bytes) -> None:
        for raw, parser, label in (
            (combined, parse_production_policy_document, "combined oracle"),
            (harness_fence, parse_execution_authority_fence, "harness fence"),
        ):
            try:
                parser(raw)
            except ExecutionPolicyContractError:
                continue
            raise SyntheticDenialValidationError(
                f"{label} crossed the production-authority firewall"
            )

    def _reopen_source(
        self,
        lineage_identity: str,
        lineage_harness: SyntheticPolicyLineageHarness | None = None,
    ) -> dict[str, Any]:
        fresh = lineage_harness or SyntheticPolicyLineageHarness(self.database.path)
        source = fresh.reopen_synthetic_lineage(lineage_identity)
        members = dict(source["members"])
        budget = parse_resource_budget(
            members["resource_budget"], members["budget_policy"], "tool.none"
        )
        sandbox = parse_sandbox_policy(
            members["sandbox_policy"], members["sandbox_enforcement_policy"], {}
        )
        budget_fields = (
            "max_wall_time_ms",
            "max_input_tokens",
            "max_output_tokens",
            "max_tool_calls",
            "max_payload_bytes",
            "max_artifact_bytes",
        )
        if any(budget.value[name] != 0 for name in budget_fields):
            raise SyntheticDenialValidationError("source ResourceBudget is not all-zero")
        sandbox_value = sandbox.value
        if (
            sandbox_value["filesystem_scope"]["read_roots"]
            or sandbox_value["filesystem_scope"]["write_roots"]
            or sandbox_value["network_scope"]["allowed_endpoints"]
            or sandbox_value["process_scope"]["allowed_executables"]
            or sandbox_value["process_scope"]["max_child_processes"] != 0
            or sandbox_value["credential_refs"]
        ):
            raise SyntheticDenialValidationError("source SandboxPolicy is not exact deny-all")
        self._reject_production_authority(
            members["combined_oracle"], members["harness_fence_document"]
        )
        return {
            "lineage_identity": lineage_identity,
            "lineage_unit_digest": source["receipt"]["unit_digest"],
            "resource_budget_digest": budget.content_digest,
            "sandbox_policy_digest": sandbox.content_digest,
        }

    @staticmethod
    def _preimage(
        source: dict[str, Any],
        *,
        decision: str,
        reason_codes: Sequence[str],
    ) -> dict[str, Any]:
        return {
            "schema": PREIMAGE_SCHEMA,
            "authority": AUTHORITY,
            "lineage_identity": source["lineage_identity"],
            "lineage_unit_digest": source["lineage_unit_digest"],
            "resource_budget_digest": source["resource_budget_digest"],
            "sandbox_policy_digest": source["sandbox_policy_digest"],
            "decision": decision,
            "reason_codes": list(reason_codes),
        }

    @classmethod
    def _candidate_receipt(
        cls, denial_key: str, source: dict[str, Any]
    ) -> tuple[dict[str, Any], bytes, str, str]:
        preimage = cls._preimage(source, decision=DECISION, reason_codes=REASON_CODES)
        denial_digest = digest_bytes(canonical_bytes(preimage))
        receipt = {
            "schema": RECEIPT_SCHEMA,
            "authority": AUTHORITY,
            "denial_key": denial_key,
            **{key: source[key] for key in (
                "lineage_identity",
                "lineage_unit_digest",
                "resource_budget_digest",
                "sandbox_policy_digest",
            )},
            "decision": DECISION,
            "reason_codes": list(REASON_CODES),
            "denial_digest": denial_digest,
        }
        receipt_bytes = canonical_bytes(receipt)
        return receipt, receipt_bytes, denial_digest, digest_bytes(receipt_bytes)

    @staticmethod
    def _lookup_matches(
        conn: sqlite3.Connection, denial_key: str, lineage_identity: str
    ) -> list[sqlite3.Row]:
        return conn.execute(
            f"""
            SELECT * FROM {DENIAL_TABLE}
            WHERE denial_key=? OR lineage_identity=?
            ORDER BY lineage_identity
            """,
            (denial_key, lineage_identity),
        ).fetchall()

    @classmethod
    def _validate_stored_receipt(
        cls, row: sqlite3.Row, source: dict[str, Any]
    ) -> dict[str, Any]:
        try:
            raw = bytes(row["receipt_bytes"])
            value = parse_strict_json(raw)
        except (TypeError, ValueError, ValidationError) as exc:
            raise IntegrityError("persisted denial receipt is not strict JSON") from exc
        if not isinstance(value, dict) or canonical_bytes(value) != raw:
            raise IntegrityError("persisted denial receipt is not canonical")
        preimage = cls._preimage(
            source, decision=SPEC_DECISION, reason_codes=SPEC_REASON_CODES
        )
        denial_digest = digest_bytes(canonical_bytes(preimage))
        expected = {
            "schema": RECEIPT_SCHEMA,
            "authority": AUTHORITY,
            "denial_key": row["denial_key"],
            **{key: source[key] for key in (
                "lineage_identity",
                "lineage_unit_digest",
                "resource_budget_digest",
                "sandbox_policy_digest",
            )},
            "decision": SPEC_DECISION,
            "reason_codes": list(SPEC_REASON_CODES),
            "denial_digest": denial_digest,
        }
        if (
            set(value) != RECEIPT_FIELDS
            or value != expected
            or row["lineage_identity"] != source["lineage_identity"]
            or row["lineage_unit_digest"] != source["lineage_unit_digest"]
            or row["resource_budget_digest"] != source["resource_budget_digest"]
            or row["sandbox_policy_digest"] != source["sandbox_policy_digest"]
            or row["denial_digest"] != denial_digest
            or row["receipt_digest"] != digest_bytes(raw)
        ):
            raise IntegrityError("persisted denial receipt integrity drift")
        return value

    def deny_synthetic_attempt(
        self,
        *,
        denial_key: str,
        lineage_identity: str,
        action_attempt_label: str,
        failpoint: str | None = None,
    ) -> dict[str, Any]:
        """Persist or replay the exact denial; the selector never enters durable identity."""

        denial_key = self._require_nonempty_string(denial_key, "denial_key")
        lineage_identity = self._require_nonempty_string(
            lineage_identity, "lineage_identity"
        )
        self._require_action_label(action_attempt_label)
        configured_failpoint = self._require_failpoint(failpoint)
        guard = self.database.connect()
        try:
            version_before_source = int(
                guard.execute("PRAGMA data_version").fetchone()[0]
            )
            source = self._reopen_source(lineage_identity)
            source_data_version = int(guard.execute("PRAGMA data_version").fetchone()[0])
            if source_data_version != version_before_source:
                raise IntegrityError("database changed during source integrity read")
            receipt, receipt_bytes, denial_digest, receipt_digest = self._candidate_receipt(
                denial_key, source
            )
            preflight_matches = self._lookup_matches(
                guard, denial_key, lineage_identity
            )
            validated_matches: list[tuple[sqlite3.Row, dict[str, Any]]] = []
            for row in preflight_matches:
                row_source = self._reopen_source(row["lineage_identity"])
                validated_matches.append(
                    (row, self._validate_stored_receipt(row, row_source))
                )
            preflight_rows = [tuple(row) for row in preflight_matches]
            committed: dict[str, Any] | None = None

            with self.database.write() as conn:
                self._trip(configured_failpoint, "policy_denial.after_begin")
                if int(guard.execute("PRAGMA data_version").fetchone()[0]) != source_data_version:
                    raise IntegrityError("database changed after source integrity preflight")
                matches = self._lookup_matches(conn, denial_key, lineage_identity)
                if [tuple(row) for row in matches] != preflight_rows:
                    raise IntegrityError("denial rows changed after integrity preflight")
                if len(matches) > 1:
                    raise SyntheticDenialConflict(
                        "denial key and lineage identity resolve to different rows"
                    )
                if validated_matches:
                    row, validated_receipt = validated_matches[0]
                    if row["lineage_identity"] != lineage_identity:
                        raise SyntheticDenialConflict(
                            "denial key is bound to another lineage identity"
                        )
                    committed = validated_receipt
                    if row["denial_digest"] != denial_digest:
                        raise SyntheticDenialConflict(
                            "denial key or lineage identity reused with changed evidence"
                        )
                else:
                    if denial_digest != EXPECTED_DENIAL_DIGEST:
                        raise SyntheticDenialValidationError(
                            "candidate denial is not the exact reviewed projection"
                        )
                    if (
                        denial_key == ORACLE_DENIAL_KEY
                        and receipt_digest != EXPECTED_RECEIPT_DIGEST
                    ):
                        raise SyntheticDenialValidationError(
                            "candidate receipt is not the exact reviewed first receipt"
                        )
                    try:
                        conn.execute(
                            f"""
                            INSERT INTO {DENIAL_TABLE}(
                              lineage_identity,denial_key,lineage_unit_digest,
                              resource_budget_digest,sandbox_policy_digest,denial_digest,
                              receipt_digest,receipt_bytes
                            ) VALUES(?,?,?,?,?,?,?,?)
                            """,
                            (
                                lineage_identity,
                                denial_key,
                                source["lineage_unit_digest"],
                                source["resource_budget_digest"],
                                source["sandbox_policy_digest"],
                                denial_digest,
                                receipt_digest,
                                receipt_bytes,
                            ),
                        )
                    except sqlite3.IntegrityError as exc:
                        raise SyntheticDenialConflict("denial uniqueness conflict") from exc
                    self._trip(configured_failpoint, "policy_denial.after_receipt")
                    committed = receipt
                self._trip(configured_failpoint, "policy_denial.before_commit")
        finally:
            guard.close()
        self._trip(configured_failpoint, "policy_denial.after_commit")
        assert committed is not None
        return committed

    def reopen_fake_denial(self, lineage_identity: str) -> dict[str, Any]:
        """Reopen one denial through fresh L1, database and strict receipt validation."""

        lineage_identity = self._require_nonempty_string(
            lineage_identity, "lineage_identity"
        )
        source = self._reopen_source(lineage_identity)
        database = RuntimeDatabase(self.database.path)
        database.migrate()
        with database.connect() as conn:
            row = conn.execute(
                f"SELECT * FROM {DENIAL_TABLE} WHERE lineage_identity=?",
                (lineage_identity,),
            ).fetchone()
        if row is None:
            raise IntegrityError("fake-denial receipt not found")
        return self._validate_stored_receipt(row, source)
