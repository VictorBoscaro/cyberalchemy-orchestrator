"""ACI-owned projection registration and deterministic group reduction."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Any, Callable

from .canonical import canonical_digest, canonical_text
from .database import RuntimeDatabase
from .errors import ConflictError, NotFoundError

ProjectionReducer = Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]]


@dataclass(frozen=True)
class ProjectionRegistration:
    name: str
    owner_namespace: str
    reducer_ref: str
    reducer_digest: str
    reducer: ProjectionReducer


class ProjectionManager:
    """The only facility allowed to mutate ``runtime_projections``."""

    def __init__(self, database: RuntimeDatabase) -> None:
        self.database = database
        self._registrations: dict[str, ProjectionRegistration] = {}

    def register(self, registration: ProjectionRegistration) -> None:
        if registration.name in self._registrations:
            raise ConflictError(f"projection already registered: {registration.name}")
        if not registration.reducer_digest.startswith("sha256:"):
            raise ConflictError("projection reducer digest must be qualified")
        self._registrations[registration.name] = registration
        with self.database.write() as conn:
            existing = conn.execute(
                "SELECT * FROM projection_registrations WHERE projection_name=?",
                (registration.name,),
            ).fetchone()
            if existing:
                if existing["reducer_ref"] == "unbound-port@1":
                    conn.execute(
                        """
                        UPDATE projection_registrations
                        SET owner_namespace=?,reducer_ref=?,reducer_digest=?,
                            registered_at=strftime('%Y-%m-%dT%H:%M:%fZ','now')
                        WHERE projection_name=?
                        """,
                        (
                            registration.owner_namespace,
                            registration.reducer_ref,
                            registration.reducer_digest,
                            registration.name,
                        ),
                    )
                elif (
                    existing["owner_namespace"],
                    existing["reducer_ref"],
                    existing["reducer_digest"],
                ) != (
                    registration.owner_namespace,
                    registration.reducer_ref,
                    registration.reducer_digest,
                ):
                    raise ConflictError("persisted projection registration differs")
            else:
                conn.execute(
                    """
                    INSERT INTO projection_registrations(
                      projection_name,owner_namespace,reducer_ref,reducer_digest,registered_at
                    ) VALUES(?,?,?,?,strftime('%Y-%m-%dT%H:%M:%fZ','now'))
                    """,
                    (
                        registration.name,
                        registration.owner_namespace,
                        registration.reducer_ref,
                        registration.reducer_digest,
                    ),
                )

    def apply_complete_group(
        self,
        conn: sqlite3.Connection,
        *,
        projection_name: str,
        projection_key: str,
        events: list[dict[str, Any]],
        last_offset: int,
    ) -> dict[str, Any]:
        registration = self._registrations.get(projection_name)
        if not registration:
            raise NotFoundError(f"projection reducer is not registered: {projection_name}")
        row = conn.execute(
            """
            SELECT value_json,last_offset FROM runtime_projections
            WHERE projection_name=? AND projection_key=?
            """,
            (projection_name, projection_key),
        ).fetchone()
        import json

        state = json.loads(row["value_json"]) if row else {}
        for event in events:
            state = registration.reducer(state, event)
        value_json = canonical_text(state)
        state_hash = canonical_digest(state)
        conn.execute(
            """
            INSERT INTO runtime_projections(
              projection_name,projection_key,value_json,state_hash,last_offset
            ) VALUES(?,?,?,?,?)
            ON CONFLICT(projection_name,projection_key) DO UPDATE SET
              value_json=excluded.value_json,state_hash=excluded.state_hash,
              last_offset=excluded.last_offset
            """,
            (projection_name, projection_key, value_json, state_hash, last_offset),
        )
        return {
            "projection_name": projection_name,
            "projection_key": projection_key,
            "state_hash": state_hash,
            "last_offset": last_offset,
        }

    def get(self, name: str, key: str) -> dict[str, Any]:
        if name not in self._registrations and name not in {
            "apt.session-record",
            "apt.dispatch-scope",
            "apt.research-record",
        }:
            raise NotFoundError("projection is not allowlisted")
        with self.database.connect() as conn:
            row = conn.execute(
                """
                SELECT value_json,state_hash,last_offset FROM runtime_projections
                WHERE projection_name=? AND projection_key=?
                """,
                (name, key),
            ).fetchone()
        if not row:
            raise NotFoundError("projection not found")
        import json

        return {
            "name": name,
            "key": key,
            "value": json.loads(row["value_json"]),
            "state_hash": row["state_hash"],
            "last_offset": row["last_offset"],
        }
