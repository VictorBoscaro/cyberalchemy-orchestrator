"""Immutable artifact boundary with policy-preserving byte deduplication."""

from __future__ import annotations

import secrets
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable

from .canonical import canonical_digest, digest_bytes
from .database import RuntimeDatabase
from .errors import AuthorizationError, ConflictError, NotFoundError, ValidationError


@dataclass(frozen=True)
class PreparedArtifact:
    artifact_id: str
    body: bytes
    content_hash: str
    media_type: str
    schema_ref: str
    classification: str
    redaction_policy_ref: str
    retention_policy_ref: str
    tombstone_policy_ref: str
    authorization_policy_ref: str
    policy_bundle_digest: str
    finalization_receipt_ref: str
    finalized_at: str
    created_event_id: str | None = None

    def reference(self) -> dict[str, object]:
        return {
            "artifact_id": self.artifact_id,
            "content_hash": self.content_hash,
            "media_type": self.media_type,
            "schema_ref": self.schema_ref,
            "classification": self.classification,
            "size_bytes": len(self.body),
            "redaction_policy_ref": self.redaction_policy_ref,
            "retention_policy_ref": self.retention_policy_ref,
            "tombstone_policy_ref": self.tombstone_policy_ref,
            "finalization_receipt_ref": self.finalization_receipt_ref,
        }


class ArtifactStore:
    CLASSIFICATIONS = {
        "runtime-internal",
        "sensitive-input",
        "sensitive-output",
        "reveal-authorized",
        "public",
    }

    def __init__(
        self,
        database: RuntimeDatabase,
        *,
        now: Callable[[], datetime] | None = None,
        id_factory: Callable[[], str] | None = None,
    ) -> None:
        self.database = database
        self._now = now or (lambda: datetime.now(timezone.utc))
        self._id = id_factory or (lambda: secrets.token_hex(16))

    def prepare(
        self,
        body: bytes,
        *,
        media_type: str,
        schema_ref: str,
        classification: str,
        redaction_policy_ref: str = "aci.redaction.none@1",
        retention_policy_ref: str = "aci.retention.local-proof@1",
        tombstone_policy_ref: str = "aci.tombstone.retain-digest@1",
        authorization_policy_ref: str = "aci.artifact.runtime-operator@1",
        policy_bundle_digest: str | None = None,
        created_event_id: str | None = None,
    ) -> PreparedArtifact:
        if not isinstance(body, bytes):
            raise ValidationError("artifact body must be bytes")
        if classification not in self.CLASSIFICATIONS:
            raise ValidationError("unknown artifact classification")
        if not media_type or not schema_ref:
            raise ValidationError("media_type and schema_ref are required")
        content_hash = digest_bytes(body)
        policy = {
            "classification": classification,
            "redaction_policy_ref": redaction_policy_ref,
            "retention_policy_ref": retention_policy_ref,
            "tombstone_policy_ref": tombstone_policy_ref,
            "authorization_policy_ref": authorization_policy_ref,
        }
        artifact_id = "art_" + content_hash.removeprefix("sha256:")[:32]
        finalized_at = self._now().isoformat()
        return PreparedArtifact(
            artifact_id=artifact_id,
            body=body,
            content_hash=content_hash,
            media_type=media_type,
            schema_ref=schema_ref,
            classification=classification,
            redaction_policy_ref=redaction_policy_ref,
            retention_policy_ref=retention_policy_ref,
            tombstone_policy_ref=tombstone_policy_ref,
            authorization_policy_ref=authorization_policy_ref,
            policy_bundle_digest=policy_bundle_digest or canonical_digest(policy),
            finalization_receipt_ref="afr_" + self._id(),
            finalized_at=finalized_at,
            created_event_id=created_event_id,
        )

    def finalize(
        self, conn: sqlite3.Connection, prepared: PreparedArtifact
    ) -> dict[str, object]:
        existing = conn.execute(
            "SELECT * FROM artifacts WHERE content_hash=?", (prepared.content_hash,)
        ).fetchone()
        if existing:
            exact = (
                bytes(existing["body"]) == prepared.body
                and existing["media_type"] == prepared.media_type
                and existing["schema_ref"] == prepared.schema_ref
                and existing["classification"] == prepared.classification
                and existing["redaction_policy_ref"] == prepared.redaction_policy_ref
                and existing["retention_policy_ref"] == prepared.retention_policy_ref
                and existing["tombstone_policy_ref"] == prepared.tombstone_policy_ref
                and existing["authorization_policy_ref"]
                == prepared.authorization_policy_ref
                and existing["policy_bundle_digest"] == prepared.policy_bundle_digest
            )
            if not exact:
                raise ConflictError(
                    "identical bytes already exist under different artifact metadata/policy"
                )
            return self._row_reference(existing)
        conn.execute(
            """
            INSERT INTO artifacts(
              artifact_id,content_hash,body,media_type,schema_ref,classification,
              size_bytes,storage_ref,redaction_policy_ref,retention_policy_ref,
              tombstone_policy_ref,authorization_policy_ref,policy_bundle_digest,
              finalization_receipt_ref,finalized_at,created_event_id,created_at
            ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                prepared.artifact_id,
                prepared.content_hash,
                prepared.body,
                prepared.media_type,
                prepared.schema_ref,
                prepared.classification,
                len(prepared.body),
                "sqlite-blob:" + prepared.artifact_id,
                prepared.redaction_policy_ref,
                prepared.retention_policy_ref,
                prepared.tombstone_policy_ref,
                prepared.authorization_policy_ref,
                prepared.policy_bundle_digest,
                prepared.finalization_receipt_ref,
                prepared.finalized_at,
                prepared.created_event_id,
                prepared.finalized_at,
            ),
        )
        return prepared.reference()

    def commit(self, prepared: PreparedArtifact) -> dict[str, object]:
        with self.database.write() as conn:
            return self.finalize(conn, prepared)

    def get_authorized(
        self,
        artifact_id: str,
        *,
        principal_id: str,
        action: str,
        authorizer: Callable[[str, str, str], bool],
    ) -> bytes:
        with self.database.connect() as conn:
            row = conn.execute(
                "SELECT * FROM artifacts WHERE artifact_id=?", (artifact_id,)
            ).fetchone()
        if not row:
            raise NotFoundError("artifact not found")
        if row["tombstoned_at"] is not None:
            raise NotFoundError("artifact payload is tombstoned")
        if not authorizer(principal_id, action, row["classification"]):
            raise AuthorizationError("artifact read denied")
        body = bytes(row["body"])
        if len(body) != row["size_bytes"] or digest_bytes(body) != row["content_hash"]:
            raise ConflictError("artifact integrity mismatch")
        return body

    @staticmethod
    def _row_reference(row: sqlite3.Row) -> dict[str, object]:
        return {
            "artifact_id": row["artifact_id"],
            "content_hash": row["content_hash"],
            "media_type": row["media_type"],
            "schema_ref": row["schema_ref"],
            "classification": row["classification"],
            "size_bytes": row["size_bytes"],
            "redaction_policy_ref": row["redaction_policy_ref"],
            "retention_policy_ref": row["retention_policy_ref"],
            "tombstone_policy_ref": row["tombstone_policy_ref"],
            "finalization_receipt_ref": row["finalization_receipt_ref"],
        }
