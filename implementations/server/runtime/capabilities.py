"""Opaque, audience/action-bound capability issuance and authentication."""

from __future__ import annotations

import hashlib
import hmac
import json
import secrets
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable

from .canonical import canonical_text
from .database import RuntimeDatabase
from .errors import AuthorizationError, ValidationError

FORBIDDEN_AUTHORITY_FIELDS = {
    "run_id",
    "dispatch_id",
    "group_id",
    "group_version",
    "group_aggregate_id",
    "seat_id",
    "agent_instance_id",
    "attempt_id",
    "actor_principal_id",
    "principal_id",
    "phase",
    "session_id",
    "probe_id",
}


@dataclass(frozen=True)
class CapabilityContext:
    capability_id: str
    principal_id: str
    action: str
    phase: str
    context: dict[str, Any]


class CapabilityManager:
    def __init__(
        self,
        database: RuntimeDatabase,
        *,
        now: Callable[[], datetime] | None = None,
        token_factory: Callable[[], str] | None = None,
    ) -> None:
        self.database = database
        self._now = now or (lambda: datetime.now(timezone.utc))
        self._tokens = token_factory or (lambda: secrets.token_urlsafe(32))

    @staticmethod
    def _digest(token: str) -> str:
        return "sha256:" + hashlib.sha256(token.encode("utf-8")).hexdigest()

    def issue(
        self,
        *,
        principal_id: str,
        action: str,
        phase: str,
        context: dict[str, Any],
        expires_at: str | None = None,
        conn=None,
    ) -> dict[str, str]:
        if not principal_id or not action or not phase:
            raise ValidationError("capability principal/action/phase are required")
        token = self._tokens()
        token_digest = self._digest(token)
        capability_id = "cap_" + secrets.token_hex(12)
        issued_at = self._now().isoformat()
        sql = """
            INSERT INTO capabilities(
              capability_id,token_digest,principal_id,action,phase,context_json,
              issued_at,expires_at
            ) VALUES(?,?,?,?,?,?,?,?)
        """
        args = (
            capability_id,
            token_digest,
            principal_id,
            action,
            phase,
            canonical_text(context),
            issued_at,
            expires_at,
        )
        if conn is None:
            with self.database.write() as owned:
                owned.execute(sql, args)
        else:
            conn.execute(sql, args)
        return {"capability_id": capability_id, "token": token}

    def resolve(self, token: str, *, action: str, phase: str) -> CapabilityContext:
        submitted = self._digest(token)
        with self.database.connect() as conn:
            rows = conn.execute(
                """
                SELECT * FROM capabilities
                WHERE action=? AND phase=? AND revoked_at IS NULL
                """,
                (action, phase),
            ).fetchall()
        row = next(
            (
                candidate
                for candidate in rows
                if hmac.compare_digest(candidate["token_digest"], submitted)
            ),
            None,
        )
        if not row:
            raise AuthorizationError("capability is invalid for action/phase")
        if row["expires_at"] and datetime.fromisoformat(row["expires_at"]) <= self._now():
            raise AuthorizationError("capability expired")
        return CapabilityContext(
            capability_id=row["capability_id"],
            principal_id=row["principal_id"],
            action=row["action"],
            phase=row["phase"],
            context=json.loads(row["context_json"]),
        )

    @staticmethod
    def reject_authority_fields(intent: dict[str, Any]) -> None:
        forbidden = sorted(FORBIDDEN_AUTHORITY_FIELDS.intersection(intent))
        if forbidden:
            raise AuthorizationError(
                "intent supplied runtime authority fields: " + ",".join(forbidden)
            )

    def revoke(self, capability_id: str) -> None:
        with self.database.write() as conn:
            updated = conn.execute(
                """
                UPDATE capabilities SET revoked_at=?
                WHERE capability_id=? AND revoked_at IS NULL
                """,
                (self._now().isoformat(), capability_id),
            )
            if updated.rowcount != 1:
                raise AuthorizationError("capability not active")
