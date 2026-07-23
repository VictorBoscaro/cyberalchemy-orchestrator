"""ACI-owned projection registration and deterministic group reduction."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Any, Callable

from .canonical import canonical_digest, canonical_text, digest_bytes, parse_strict_json
from .database import RuntimeDatabase
from .errors import ConflictError, IntegrityError, NotFoundError

ProjectionReducer = Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]]
APT_PROJECTOR_NAME = "apt.granular"
APT_PROJECTOR_VERSION = "apt.granular-projector@1"


class ProjectionLagError(NotFoundError):
    """The authoritative fact exists beyond the materialized APT boundary."""

    code = "PROJECTION_LAG"


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

    def apply_apt_group(
        self, conn: sqlite3.Connection, events: list[dict[str, Any]]
    ) -> None:
        """Materialize accepted APT events through the ACI-owned projection facility.

        These tables are disposable read models.  Callers cannot invoke this
        method without an already-open journal transaction owned by RuntimeJournal.
        """
        import json

        for event in events:
            event_type = event["event_type"]
            payload = event["payload"]
            event_id = event["event_id"]
            offset = event["journal_offset"]
            if event_type == "apt.research_capture_appended":
                capture = payload["research_capture"]
                predecessor = capture["supersedes_capture_id"]
                if predecessor:
                    updated = conn.execute(
                        """
                        UPDATE apt_research_captures_projection SET is_current=0
                        WHERE research_capture_id=? AND is_current=1
                        """,
                        (predecessor,),
                    )
                    if updated.rowcount != 1:
                        raise ConflictError("capture projection predecessor is not current")
                raw = capture["raw_return"]
                conn.execute(
                    """
                    INSERT INTO apt_research_captures_projection(
                      research_capture_id,dispatch_id,expected_contribution_id,
                      capture_status,raw_artifact_id,capture_digest,payload_json,
                      accepted_event_id,accepted_offset,is_current
                    ) VALUES(?,?,?,?,?,?,?,?,?,1)
                    """,
                    (
                        capture["research_capture_id"],
                        capture["dispatch_id"],
                        capture["expected_contribution_id"],
                        capture["capture_status"],
                        raw["artifact_id"] if raw else None,
                        _digest_text(capture["capture_digest"]),
                        canonical_text(capture),
                        event_id,
                        offset,
                    ),
                )
                continue
            if event_type == "apt.reference_probe_lineage_appended":
                conn.execute(
                    """
                    INSERT INTO apt_reference_lineage_projection(
                      delivery_subject_key,accepted_event_id,accepted_offset,payload_json
                    ) VALUES(?,?,?,?)
                    """,
                    (
                        payload["delivery_subject_key"],
                        event_id,
                        offset,
                        canonical_text(payload),
                    ),
                )
                continue
            if event_type != "apt.research_fact_appended":
                continue
            kind = payload["payload_variant"]
            entity = payload["payload"]
            fact = entity["fact"]
            predecessor = fact["supersedes_fact_id"]
            if predecessor:
                updated = conn.execute(
                    """
                    UPDATE apt_research_facts_projection SET is_current=0
                    WHERE fact_id=? AND subject_id=? AND is_current=1
                    """,
                    (predecessor, fact["subject_id"]),
                )
                if updated.rowcount != 1:
                    raise ConflictError("fact projection predecessor is not current")
            conn.execute(
                """
                INSERT INTO apt_research_facts_projection(
                  fact_id,research_capture_id,subject_id,fact_kind,supersedes_fact_id,
                  payload_json,accepted_event_id,accepted_offset,is_current
                ) VALUES(?,?,?,?,?,?,?,?,1)
                """,
                (
                    fact["fact_id"],
                    entity["research_capture_id"],
                    fact["subject_id"],
                    kind,
                    predecessor,
                    canonical_text(entity),
                    event_id,
                    offset,
                ),
            )
            common = (
                fact["fact_id"],
                entity["research_capture_id"],
                canonical_text(entity),
            )
            if kind == "research_question":
                conn.execute(
                    """INSERT INTO apt_research_questions_projection
                       (research_question_id,fact_id,research_capture_id,question_text,payload_json)
                       VALUES(?,?,?,?,?)""",
                    (
                        entity["research_question_id"],
                        fact["fact_id"],
                        entity["research_capture_id"],
                        entity["question_text"],
                        canonical_text(entity),
                    ),
                )
            elif kind == "research_answer":
                capture = conn.execute(
                    """SELECT raw_artifact_id FROM apt_research_captures_projection
                       WHERE research_capture_id=?""",
                    (entity["research_capture_id"],),
                ).fetchone()
                if not capture or not capture["raw_artifact_id"]:
                    raise ConflictError("answer projection has no raw artifact")
                conn.execute(
                    """INSERT INTO apt_research_answers_projection
                       (research_answer_id,fact_id,research_capture_id,question_ids_json,
                        artifact_id,selector_json,payload_json)
                       VALUES(?,?,?,?,?,?,?)""",
                    (
                        entity["research_answer_id"],
                        fact["fact_id"],
                        entity["research_capture_id"],
                        canonical_text(entity["question_ids"]),
                        capture["raw_artifact_id"],
                        canonical_text(entity["extraction"]["selector"]),
                        canonical_text(entity),
                    ),
                )
            elif kind == "reference_use":
                conn.execute(
                    """INSERT INTO apt_reference_uses_projection
                       (reference_use_id,fact_id,research_capture_id,reference_id,
                        reference_kind,locator_observed,use_kind,
                        probe_recommendation_ref_json,payload_json)
                       VALUES(?,?,?,?,?,?,?,?,?)""",
                    (
                        entity["reference_use_id"],
                        fact["fact_id"],
                        entity["research_capture_id"],
                        entity["reference_id"],
                        entity["reference_kind"],
                        entity["locator_observed"],
                        entity["use_kind"],
                        canonical_text(entity["probe_recommendation_ref"])
                        if entity["probe_recommendation_ref"]
                        else None,
                        canonical_text(entity),
                    ),
                )
            elif kind == "research_problem":
                conn.execute(
                    """INSERT INTO apt_research_problems_projection
                       (problem_id,fact_id,research_capture_id,problem_kind,statement,payload_json)
                       VALUES(?,?,?,?,?,?)""",
                    (
                        entity["problem_id"],
                        fact["fact_id"],
                        entity["research_capture_id"],
                        entity["kind"],
                        entity["statement"],
                        canonical_text(entity),
                    ),
                )
            elif kind == "research_claim":
                conn.execute(
                    """INSERT INTO apt_research_claims_projection
                       (research_claim_id,fact_id,research_capture_id,statement,
                        answer_ids_json,payload_json) VALUES(?,?,?,?,?,?)""",
                    (
                        entity["research_claim_id"],
                        fact["fact_id"],
                        entity["research_capture_id"],
                        entity["statement"],
                        canonical_text(entity["answer_ids"]),
                        canonical_text(entity),
                    ),
                )
            elif kind == "formalization_candidate":
                conn.execute(
                    """INSERT INTO apt_formalizations_projection
                       (formalization_id,fact_id,research_capture_id,research_claim_id,
                        notation,latex,legend_json,reading,logic_family,assumptions_json,
                        scope,payload_json) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (
                        entity["formalization_id"],
                        fact["fact_id"],
                        entity["research_capture_id"],
                        entity["research_claim_id"],
                        entity["notation"],
                        entity["latex"],
                        canonical_text(entity["legend"]),
                        entity["reading"],
                        entity["logic_family"],
                        canonical_text(entity["assumptions"]),
                        entity["scope"],
                        canonical_text(entity),
                    ),
                )

    def apt_state(self) -> dict[str, Any]:
        with self.database.connect() as conn:
            row = conn.execute(
                "SELECT * FROM apt_projection_state WHERE projection_name=?",
                (APT_PROJECTOR_NAME,),
            ).fetchone()
        if not row:
            raise IntegrityError("APT projector state is missing")
        return {
            "projection_name": row["projection_name"],
            "projector_version": row["projector_version"],
            "apt_source_through_offset": int(row["apt_source_through_offset"]),
            "source_through_offset": int(row["source_through_offset"]),
            "current": int(row["apt_source_through_offset"])
            >= int(row["source_through_offset"]),
        }

    def catch_up_apt(self, journal, *, failpoint=None) -> dict[str, Any]:
        """Scan only verified complete groups and atomically project one group at a time."""
        prefix = journal.read_complete_groups()
        source_through = int(prefix["effective_as_of"])
        with self.database.write() as conn:
            conn.execute(
                """
                UPDATE apt_projection_state
                SET source_through_offset=?,updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now')
                WHERE projection_name=?
                """,
                (source_through, APT_PROJECTOR_NAME),
            )
        state = self.apt_state()
        watermark = int(state["apt_source_through_offset"])
        if watermark > source_through:
            raise IntegrityError("APT projection watermark is beyond verified source")
        groups = journal.read_complete_groups(after=watermark, through=source_through)["groups"]
        for group in groups:
            with self.database.write() as conn:
                current = conn.execute(
                    """
                    SELECT apt_source_through_offset,projector_version
                    FROM apt_projection_state WHERE projection_name=?
                    """,
                    (APT_PROJECTOR_NAME,),
                ).fetchone()
                if (
                    not current
                    or current["projector_version"] != APT_PROJECTOR_VERSION
                    or int(current["apt_source_through_offset"]) != watermark
                ):
                    raise ConflictError("APT projector checkpoint changed")
                projected: list[dict[str, Any]] = []
                for metadata in group["events"]:
                    row = conn.execute(
                        """
                        SELECT e.event_type,e.event_id,e.journal_offset,e.payload_hash,a.body
                        FROM events e JOIN artifacts a ON a.artifact_id=e.payload_ref
                        WHERE e.event_id=?
                        """,
                        (metadata["event_id"],),
                    ).fetchone()
                    if (
                        not row
                        or int(row["journal_offset"]) != int(metadata["journal_offset"])
                        or row["payload_hash"] != metadata["payload_hash"]
                        or digest_bytes(bytes(row["body"])) != row["payload_hash"]
                    ):
                        raise IntegrityError("APT projector source event changed after verification")
                    projected.append(
                        {
                            "event_type": row["event_type"],
                            "payload": parse_strict_json(bytes(row["body"])),
                            "event_id": row["event_id"],
                            "journal_offset": int(row["journal_offset"]),
                        }
                    )
                if failpoint:
                    failpoint("before_group_apply", group)
                apt_events = [
                    event
                    for event in projected
                    if event["event_type"].startswith("apt.")
                ]
                self.apply_apt_group(conn, apt_events)
                by_capture: dict[str, list[dict[str, Any]]] = {}
                for event in apt_events:
                    if event["event_type"] == "apt.research_capture_appended":
                        capture_id = event["payload"]["research_capture"][
                            "research_capture_id"
                        ]
                    elif event["event_type"] == "apt.research_fact_appended":
                        capture_id = event["payload"]["payload"]["research_capture_id"]
                    else:
                        continue
                    by_capture.setdefault(capture_id, []).append(event)
                for capture_id, events in by_capture.items():
                    self.apply_complete_group(
                        conn,
                        projection_name="apt.research-record",
                        projection_key=capture_id,
                        events=events,
                        last_offset=int(group["last_offset"]),
                    )
                if failpoint:
                    failpoint("before_checkpoint", group)
                conn.execute(
                    """
                    UPDATE apt_projection_state
                    SET apt_source_through_offset=?,
                        updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now')
                    WHERE projection_name=? AND apt_source_through_offset=?
                    """,
                    (int(group["last_offset"]), APT_PROJECTOR_NAME, watermark),
                )
            watermark = int(group["last_offset"])
        return self.apt_state()

    def rebuild_apt(self, journal, *, failpoint=None) -> dict[str, Any]:
        """Discard all APT read models and deterministically replay from offset zero."""
        with self.database.write() as conn:
            for table in (
                "apt_formalizations_projection",
                "apt_research_claims_projection",
                "apt_research_problems_projection",
                "apt_reference_uses_projection",
                "apt_research_answers_projection",
                "apt_research_questions_projection",
                "apt_research_facts_projection",
                "apt_reference_lineage_projection",
                "apt_research_captures_projection",
            ):
                conn.execute(f"DELETE FROM {table}")
            conn.execute(
                "DELETE FROM runtime_projections WHERE projection_name='apt.research-record'"
            )
            conn.execute(
                """
                UPDATE apt_projection_state
                SET projector_version=?,apt_source_through_offset=0,
                    source_through_offset=0,
                    updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now')
                WHERE projection_name=?
                """,
                (APT_PROJECTOR_VERSION, APT_PROJECTOR_NAME),
            )
        return self.catch_up_apt(journal, failpoint=failpoint)

    def _require_apt_offset(self, required_offset: int) -> None:
        state = self.apt_state()
        if int(state["apt_source_through_offset"]) < required_offset:
            raise ProjectionLagError(
                "APT projection has not reached authoritative offset "
                f"{required_offset} (watermark={state['apt_source_through_offset']})"
            )

    def get_apt_research(self, capture_id: str) -> dict[str, Any]:
        import json

        with self.database.connect() as conn:
            authority = conn.execute(
                """
                SELECT cr.last_offset
                FROM apt_capture_keys k
                JOIN events e ON e.event_id=k.accepted_event_id
                JOIN command_receipts cr ON cr.command_id=e.command_id
                WHERE k.research_capture_id=?
                """,
                (capture_id,),
            ).fetchone()
            if not authority:
                raise NotFoundError("research capture not found")
            required_offset = int(authority["last_offset"])
        self._require_apt_offset(required_offset)
        with self.database.connect() as conn:
            capture = conn.execute(
                """SELECT * FROM apt_research_captures_projection
                   WHERE research_capture_id=?""",
                (capture_id,),
            ).fetchone()
            if not capture:
                raise NotFoundError("research capture projection not found")
            result: dict[str, Any] = {
                "capture": json.loads(capture["payload_json"]),
                "accepted_event_id": capture["accepted_event_id"],
                "accepted_offset": capture["accepted_offset"],
                "current": bool(capture["is_current"]),
            }
            table_buckets = (
                ("questions", "apt_research_questions_projection"),
                ("answers", "apt_research_answers_projection"),
                ("reference_uses", "apt_reference_uses_projection"),
                ("problems", "apt_research_problems_projection"),
                ("claims", "apt_research_claims_projection"),
                ("formalizations", "apt_formalizations_projection"),
            )
            max_offset = int(capture["accepted_offset"])
            for bucket, table in table_buckets:
                rows = conn.execute(
                    f"""
                    SELECT t.payload_json,f.accepted_offset
                    FROM {table} t
                    JOIN apt_research_facts_projection f ON f.fact_id=t.fact_id
                    WHERE t.research_capture_id=? AND f.is_current=1
                    ORDER BY f.subject_id
                    """,
                    (capture_id,),
                ).fetchall()
                result[bucket] = [json.loads(row["payload_json"]) for row in rows]
                if rows:
                    max_offset = max(max_offset, *(int(row["accepted_offset"]) for row in rows))
            result["effective_as_of"] = max_offset
        return result

    def get_apt_dispatch(self, dispatch_id: str) -> dict[str, Any]:
        import json

        with self.database.connect() as conn:
            link = conn.execute(
                "SELECT * FROM dispatch_links WHERE dispatch_id=?", (dispatch_id,)
            ).fetchone()
            if not link:
                raise NotFoundError("dispatch link not found")
            authority = conn.execute(
                """
                SELECT max(cr.last_offset) AS required_offset
                FROM apt_capture_keys k
                JOIN events e ON e.event_id=k.accepted_event_id
                JOIN command_receipts cr ON cr.command_id=e.command_id
                WHERE k.dispatch_id=?
                """,
                (dispatch_id,),
            ).fetchone()
            required_offset = int(authority["required_offset"] or 0)
        self._require_apt_offset(required_offset)
        with self.database.connect() as conn:
            link = conn.execute(
                "SELECT * FROM dispatch_links WHERE dispatch_id=?", (dispatch_id,)
            ).fetchone()
            captures = conn.execute(
                """
                SELECT payload_json,accepted_offset FROM apt_research_captures_projection
                WHERE dispatch_id=? AND is_current=1
                ORDER BY expected_contribution_id
                """,
                (dispatch_id,),
            ).fetchall()
        return {
            "dispatch_id": dispatch_id,
            "session_id": link["session_id"],
            "snapshot": json.loads(link["row_json"]),
            "research": [json.loads(row["payload_json"]) for row in captures],
            "effective_as_of": max(
                [int(row["accepted_offset"]) for row in captures] + [0]
            ),
        }


def _digest_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if (
        isinstance(value, dict)
        and value.get("algorithm") == "sha256"
        and isinstance(value.get("value"), str)
    ):
        return "sha256:" + value["value"]
    raise ConflictError("projection digest shape is invalid")
