"""Test-only POLICY-001 persistence seam; never production authority."""

from __future__ import annotations

import json
import sqlite3
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

from implementations.server.runtime.artifacts import ArtifactStore
from implementations.server.runtime.canonical import (
    canonical_bytes,
    digest_bytes,
    parse_strict_json,
)
from implementations.server.runtime.database import RuntimeDatabase
from implementations.server.runtime.errors import (
    ConflictError,
    IntegrityError,
    NotFoundError,
    ValidationError,
)
from implementations.server.runtime.execution_policy import (
    ExecutionPolicyContractError,
    parse_execution_authority_fence,
    parse_execution_authority_fence_harness_for_test,
    parse_execution_policy_oracle_fixture_for_test,
    parse_production_policy_document,
    parse_resource_budget,
    parse_sandbox_policy,
)


RECEIPT_SCHEMA = "aci.execution-policy-synthetic-lineage-receipt@1"
UNIT_SCHEMA = "aci.execution-policy-synthetic-lineage-unit@1"
AUTHORITY = "test-only-non-executable"
RECEIPT_TABLE = "test_execution_policy_lineage_receipts"
MEMBER_TABLE = "test_execution_policy_lineage_members"
MEMBER_ORDER = (
    "budget_policy",
    "sandbox_enforcement_policy",
    "resource_budget",
    "sandbox_policy",
    "combined_oracle",
    "harness_fence_preimage",
    "harness_fence_document",
)
RECEIPT_FIELDS = {
    "schema",
    "authority",
    "synthetic_key",
    "lineage_identity",
    "members",
    "unit_digest",
}
EXPECTED_MEMBER_DIGESTS = (
    "sha256:08f3494d9e869053ee097e854840ade80afcda65cce75ef774038be5c6c242d2",
    "sha256:88f400d1661b69ac6536b548216bb7f5a370042050df2ea7bae49e03952725ea",
    "sha256:e6e3a27b6fecf0ca8667ca722bb1e74a39e4d1f685da172f75a8077a67ba3836",
    "sha256:d865e9f97c6b73afc4748e5bd6d58095e471450d72cd45c3fb4a55a8185e3b1a",
    "sha256:9abfb7e61f995a90e8a08a72dfa96dda2df956f63e4e4360e78eca22493641f6",
    "sha256:124d06fa0b4c2e55eef48bc5b0c33ce19880d15ce82e0d3af9518a80536de70f",
    "sha256:4672e47ccc7fb906a14c0cd57de0bbd74271cfb7697d3a539dc97251bb864ba4",
)
Failpoint = Callable[[str], None]
MemberInput = tuple[str, bytes]


class SyntheticLineageValidationError(ValidationError):
    """The proposed test-only unit is not the exact reviewed POLICY-000 corpus."""


class SyntheticLineageConflict(ConflictError):
    """A synthetic key or immutable lineage identity was reused with drift."""


class SyntheticPolicyLineageHarness:
    """Persist one exact synthetic unit in two local test tables and artifacts."""

    def __init__(self, database_path: Path) -> None:
        self.database = RuntimeDatabase(Path(database_path))
        self.database.migrate()
        self.artifacts = ArtifactStore(self.database)
        self._create_test_tables()

    def _create_test_tables(self) -> None:
        with self.database.write() as conn:
            conn.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {RECEIPT_TABLE}(
                  lineage_identity TEXT PRIMARY KEY,
                  synthetic_key TEXT NOT NULL UNIQUE,
                  unit_digest TEXT NOT NULL,
                  receipt_bytes BLOB NOT NULL
                )
                """
            )
            conn.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {MEMBER_TABLE}(
                  lineage_identity TEXT NOT NULL,
                  ordinal INTEGER NOT NULL CHECK(ordinal BETWEEN 0 AND 6),
                  name TEXT NOT NULL,
                  artifact_id TEXT NOT NULL,
                  content_digest TEXT NOT NULL,
                  PRIMARY KEY(lineage_identity, ordinal),
                  UNIQUE(lineage_identity, name),
                  FOREIGN KEY(lineage_identity) REFERENCES {RECEIPT_TABLE}(lineage_identity),
                  FOREIGN KEY(artifact_id) REFERENCES artifacts(artifact_id)
                )
                """
            )

    @staticmethod
    def _require_identity(value: str, label: str) -> None:
        if not isinstance(value, str) or not value:
            raise SyntheticLineageValidationError(f"{label} must be a non-empty string")

    @staticmethod
    def _reject_production_authority(combined: bytes, harness_fence: bytes) -> None:
        try:
            parse_production_policy_document(combined)
        except ExecutionPolicyContractError:
            pass
        else:
            raise SyntheticLineageValidationError(
                "combined oracle crossed the production-policy authority firewall"
            )
        try:
            parse_execution_authority_fence(harness_fence)
        except ExecutionPolicyContractError:
            pass
        else:
            raise SyntheticLineageValidationError(
                "harness fence crossed the production-fence authority firewall"
            )

    @classmethod
    def _normalize_candidate_members(
        cls, members: Sequence[MemberInput]
    ) -> tuple[MemberInput, ...]:
        if isinstance(members, (str, bytes, bytearray)) or len(members) != 7:
            raise SyntheticLineageValidationError("lineage requires exactly seven members")
        normalized: list[MemberInput] = []
        for ordinal, member in enumerate(members):
            if not isinstance(member, tuple) or len(member) != 2:
                raise SyntheticLineageValidationError("each member must be a (name, bytes) tuple")
            name, body = member
            if name != MEMBER_ORDER[ordinal]:
                raise SyntheticLineageValidationError(
                    f"member {ordinal} must be named {MEMBER_ORDER[ordinal]!r}"
                )
            if not isinstance(body, bytes):
                raise SyntheticLineageValidationError(f"member {name} body must be bytes")
            try:
                value = parse_strict_json(body)
            except ValidationError as exc:
                raise SyntheticLineageValidationError(f"member {name} is not strict JSON") from exc
            if canonical_bytes(value) != body:
                raise SyntheticLineageValidationError(f"member {name} is not exact aci-cjson-1")
            normalized.append((name, body))
        return tuple(normalized)

    @classmethod
    def _validate_members(cls, members: Sequence[MemberInput]) -> tuple[MemberInput, ...]:
        normalized = cls._normalize_candidate_members(members)
        for ordinal, (name, body) in enumerate(normalized):
            if digest_bytes(body) != EXPECTED_MEMBER_DIGESTS[ordinal]:
                raise SyntheticLineageValidationError(f"member {name} digest drift")

        by_name = dict(normalized)
        budget = parse_resource_budget(
            by_name["resource_budget"], by_name["budget_policy"], "tool.none"
        )
        sandbox = parse_sandbox_policy(
            by_name["sandbox_policy"], by_name["sandbox_enforcement_policy"], {}
        )
        parse_execution_policy_oracle_fixture_for_test(
            by_name["combined_oracle"],
            budget.canonical_bytes,
            sandbox.canonical_bytes,
            by_name["budget_policy"],
            by_name["sandbox_enforcement_policy"],
            {},
            "tool.none",
        )
        harness = parse_execution_authority_fence_harness_for_test(
            by_name["harness_fence_document"]
        )
        if harness.preimage_bytes != by_name["harness_fence_preimage"]:
            raise SyntheticLineageValidationError("harness fence preimage drift")
        cls._reject_production_authority(
            by_name["combined_oracle"], by_name["harness_fence_document"]
        )
        return tuple(normalized)

    @staticmethod
    def _prepared_member(name: str, body: bytes, store: ArtifactStore):
        return store.prepare(
            body,
            media_type="application/json",
            schema_ref=f"aci.execution-policy-synthetic-member.{name}@1",
            classification="runtime-internal",
            authorization_policy_ref="aci.artifact.test-only-non-executable@1",
        )

    @staticmethod
    def _receipt_from_bytes(raw: bytes) -> dict[str, Any]:
        try:
            value = parse_strict_json(raw)
        except ValidationError as exc:
            raise IntegrityError("persisted synthetic receipt is not strict JSON") from exc
        if not isinstance(value, dict) or canonical_bytes(value) != raw:
            raise IntegrityError("persisted synthetic receipt is not canonical")
        return value

    @staticmethod
    def _bindings_from_rows(rows: Sequence[sqlite3.Row]) -> list[dict[str, Any]]:
        if len(rows) != 7:
            raise IntegrityError("synthetic lineage has partial membership")
        bindings: list[dict[str, Any]] = []
        for ordinal, row in enumerate(rows):
            if row["ordinal"] != ordinal or row["name"] != MEMBER_ORDER[ordinal]:
                raise IntegrityError("synthetic lineage member order drift")
            bindings.append(
                {
                    "ordinal": row["ordinal"],
                    "name": row["name"],
                    "artifact_id": row["artifact_id"],
                    "content_digest": row["content_digest"],
                }
            )
        return bindings

    @classmethod
    def _validate_stored_receipt(
        cls,
        receipt_row: sqlite3.Row,
        bindings: list[dict[str, Any]],
    ) -> dict[str, Any]:
        lineage_identity = receipt_row["lineage_identity"]
        synthetic_key = receipt_row["synthetic_key"]
        if not isinstance(lineage_identity, str) or not lineage_identity:
            raise IntegrityError("persisted lineage identity is invalid")
        if not isinstance(synthetic_key, str) or not synthetic_key:
            raise IntegrityError("persisted synthetic key is invalid")
        preimage = {
            "schema": UNIT_SCHEMA,
            "authority": AUTHORITY,
            "lineage_identity": lineage_identity,
            "members": bindings,
        }
        expected_digest = digest_bytes(canonical_bytes(preimage))
        expected_receipt = {
            "schema": RECEIPT_SCHEMA,
            "authority": AUTHORITY,
            "synthetic_key": synthetic_key,
            "lineage_identity": lineage_identity,
            "members": bindings,
            "unit_digest": expected_digest,
        }
        receipt = cls._receipt_from_bytes(bytes(receipt_row["receipt_bytes"]))
        if (
            set(receipt) != RECEIPT_FIELDS
            or receipt_row["unit_digest"] != expected_digest
            or receipt != expected_receipt
        ):
            raise IntegrityError("synthetic lineage receipt integrity drift")
        return receipt

    @staticmethod
    def _lookup_matches(
        conn: sqlite3.Connection, synthetic_key: str, lineage_identity: str
    ) -> list[sqlite3.Row]:
        return conn.execute(
            f"""
            SELECT lineage_identity,synthetic_key,unit_digest,receipt_bytes
            FROM {RECEIPT_TABLE}
            WHERE synthetic_key=? OR lineage_identity=?
            ORDER BY lineage_identity
            """,
            (synthetic_key, lineage_identity),
        ).fetchall()

    def persist_synthetic_lineage(
        self,
        *,
        synthetic_key: str,
        lineage_identity: str,
        members: Sequence[MemberInput],
        failpoint: Failpoint | None = None,
    ) -> dict[str, Any]:
        """Persist or replay the exact unit; ``after_commit`` is outside the transaction."""

        self._require_identity(synthetic_key, "synthetic_key")
        self._require_identity(lineage_identity, "lineage_identity")
        candidate = self._normalize_candidate_members(members)
        fp = failpoint or (lambda _name: None)
        try:
            validated = self._validate_members(candidate)
        except SyntheticLineageValidationError as validation_error:
            # An unbound malformed corpus remains a validation failure.  When a
            # canonical candidate drifts under an already-bound key/identity, the
            # serialized identity lookup owns the stronger permanent-conflict
            # classification required by T-ACI-POL1-3/4.
            candidate_bindings = [
                {
                    "ordinal": ordinal,
                    "name": name,
                    "artifact_id": "art_" + digest_bytes(body)[7:39],
                    "content_digest": digest_bytes(body),
                }
                for ordinal, (name, body) in enumerate(candidate)
            ]
            candidate_preimage = {
                "schema": UNIT_SCHEMA,
                "authority": AUTHORITY,
                "lineage_identity": lineage_identity,
                "members": candidate_bindings,
            }
            candidate_digest = digest_bytes(canonical_bytes(candidate_preimage))
            with self.database.write() as conn:
                fp("policy_lineage.after_begin")
                matches = self._lookup_matches(conn, synthetic_key, lineage_identity)
                if matches and (
                    len(matches) != 1 or matches[0]["unit_digest"] != candidate_digest
                ):
                    raise SyntheticLineageConflict(
                        "synthetic key or lineage identity reused with a different unit"
                    ) from validation_error
            raise validation_error
        prepared = tuple(
            self._prepared_member(name, body, self.artifacts) for name, body in validated
        )
        bindings = [
            {
                "ordinal": ordinal,
                "name": name,
                "artifact_id": artifact.artifact_id,
                "content_digest": artifact.content_hash,
            }
            for ordinal, ((name, _body), artifact) in enumerate(zip(validated, prepared))
        ]
        preimage = {
            "schema": UNIT_SCHEMA,
            "authority": AUTHORITY,
            "lineage_identity": lineage_identity,
            "members": bindings,
        }
        unit_digest = digest_bytes(canonical_bytes(preimage))
        receipt = {
            "schema": RECEIPT_SCHEMA,
            "authority": AUTHORITY,
            "synthetic_key": synthetic_key,
            "lineage_identity": lineage_identity,
            "members": bindings,
            "unit_digest": unit_digest,
        }
        receipt_bytes = canonical_bytes(receipt)
        committed: dict[str, Any] | None = None

        with self.database.write() as conn:
            fp("policy_lineage.after_begin")
            matches = self._lookup_matches(conn, synthetic_key, lineage_identity)
            if matches:
                if len(matches) != 1 or matches[0]["unit_digest"] != unit_digest:
                    raise SyntheticLineageConflict(
                        "synthetic key or lineage identity reused with a different unit"
                    )
            if matches:
                member_rows = conn.execute(
                    f"""
                    SELECT ordinal,name,artifact_id,content_digest
                    FROM {MEMBER_TABLE} WHERE lineage_identity=? ORDER BY ordinal
                    """,
                    (matches[0]["lineage_identity"],),
                ).fetchall()
                committed = self._validate_stored_receipt(
                    matches[0], self._bindings_from_rows(member_rows)
                )
            else:
                for ordinal, artifact in enumerate(prepared):
                    reference = self.artifacts.finalize(conn, artifact)
                    if reference["artifact_id"] != bindings[ordinal]["artifact_id"]:
                        raise IntegrityError("artifact identity changed during finalization")
                    fp(f"policy_lineage.after_artifact.{ordinal}")
                try:
                    conn.execute(
                        f"""
                        INSERT INTO {RECEIPT_TABLE}(
                          lineage_identity,synthetic_key,unit_digest,receipt_bytes
                        ) VALUES(?,?,?,?)
                        """,
                        (lineage_identity, synthetic_key, unit_digest, receipt_bytes),
                    )
                    fp("policy_lineage.after_receipt")
                    for member in bindings:
                        conn.execute(
                            f"""
                            INSERT INTO {MEMBER_TABLE}(
                              lineage_identity,ordinal,name,artifact_id,content_digest
                            ) VALUES(?,?,?,?,?)
                            """,
                            (
                                lineage_identity,
                                member["ordinal"],
                                member["name"],
                                member["artifact_id"],
                                member["content_digest"],
                            ),
                        )
                        fp(f"policy_lineage.after_member.{member['ordinal']}")
                except sqlite3.IntegrityError as exc:
                    raise SyntheticLineageConflict("synthetic lineage uniqueness conflict") from exc
                committed = receipt
            fp("policy_lineage.before_commit")
        fp("policy_lineage.after_commit")
        assert committed is not None
        return committed

    def reopen_synthetic_lineage(self, lineage_identity: str) -> dict[str, Any]:
        """Reopen one complete unit through fresh database and artifact handles."""

        self._require_identity(lineage_identity, "lineage_identity")
        database = RuntimeDatabase(self.database.path)
        database.migrate()
        artifacts = ArtifactStore(database)
        with database.connect() as conn:
            receipt_row = conn.execute(
                f"SELECT * FROM {RECEIPT_TABLE} WHERE lineage_identity=?",
                (lineage_identity,),
            ).fetchone()
            if receipt_row is None:
                raise IntegrityError("synthetic lineage receipt not found")
            member_rows = conn.execute(
                f"""
                SELECT ordinal,name,artifact_id,content_digest
                FROM {MEMBER_TABLE} WHERE lineage_identity=? ORDER BY ordinal
                """,
                (lineage_identity,),
            ).fetchall()
        stored_bindings = self._bindings_from_rows(member_rows)
        bodies: list[MemberInput] = []
        for row in member_rows:
            try:
                body, reference = artifacts.get_authorized_with_reference(
                    row["artifact_id"],
                    principal_id="policy-lineage-test-harness",
                    action="read-test-fixture",
                    authorizer=lambda _principal, _action, classification: (
                        classification == "runtime-internal"
                    ),
                )
            except (NotFoundError, ConflictError) as exc:
                raise IntegrityError("synthetic lineage artifact is unavailable or corrupt") from exc
            if (
                reference["artifact_id"] != row["artifact_id"]
                or reference["content_hash"] != row["content_digest"]
                or digest_bytes(body) != row["content_digest"]
            ):
                raise IntegrityError("synthetic lineage artifact binding drift")
            bodies.append((row["name"], body))
        validated = self._validate_members(tuple(bodies))
        receipt = self._validate_stored_receipt(receipt_row, stored_bindings)
        return {"receipt": receipt, "members": validated}


def load_policy000_members(path: Path) -> tuple[MemberInput, ...]:
    """Load the closed POLICY-000 transport; validation remains in the harness."""

    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if set(value) != {"schema", "authority", "vectors"}:
        raise SyntheticLineageValidationError("POLICY-000 transport fields are not closed")
    if (
        value["schema"] != "aci.execution-policy-oracle-vectors@1"
        or value["authority"] != AUTHORITY
        or not isinstance(value["vectors"], list)
    ):
        raise SyntheticLineageValidationError("POLICY-000 transport identity mismatch")
    members: list[MemberInput] = []
    for item in value["vectors"]:
        if set(item) != {"name", "canonical_json", "digest"}:
            raise SyntheticLineageValidationError("POLICY-000 vector fields are not closed")
        body = item["canonical_json"].encode("utf-8")
        if digest_bytes(body) != item["digest"]:
            raise SyntheticLineageValidationError("POLICY-000 transport digest mismatch")
        members.append((item["name"], body))
    return tuple(members)
