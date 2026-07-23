from __future__ import annotations

import hashlib
import json
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterator, Mapping


class RuntimeErrorBase(Exception):
    """Base class for expected runtime errors."""


class InvalidCommand(RuntimeErrorBase):
    pass


class CommandConflict(RuntimeErrorBase):
    """An operation_id was reused with a different command or payload."""


class DomainConflict(RuntimeErrorBase):
    pass


class ReceiptNotFound(RuntimeErrorBase):
    pass


_COMMAND_TO_EVENT = {
    "ensure_session": "session.started",
    "link_session_dispatch": "session.dispatch_linked",
    # Product operations use Reference Scout terminology. Frozen v1 wire/event
    # identifiers retain probe.* compatibility names.
    "start_reference_scout": "probe.requested",
    "publish_scout_contribution": "probe.contribution.published",
    "commit_reference_bundle": "probe.bundle.committed",
    "deliver_reference_bundle": "probe.bundle.delivered",
}

_COMMAND_FIELDS = {
    "ensure_session": {
        "session_id", "ensure_key", "origin_kind", "origin_ref", "initial_name", "started_at"
    },
    "link_session_dispatch": {
        "session_dispatch_link_id", "session_id", "dispatch_id", "linked_at"
    },
    "start_reference_scout": {
        "scout_run_id", "probe_id", "session_id", "dispatch_id", "objective_ref",
        "shape", "source_mode", "protocol_profile_id", "protocol_profile_version",
        "protocol_profile_digest", "requested_at"
    },
    "publish_scout_contribution": {
        "recommendation_id", "scout_run_id", "probe_id", "reference_id", "source_class",
        "locator_observed", "access_state", "found_by_seat_id",
        "evaluated_by_seat_id", "evaluation", "why_inspect", "comparability_state"
    },
    "commit_reference_bundle": {"scout_run_id", "probe_id", "bundle_digest"},
    "deliver_reference_bundle": {"scout_run_id", "probe_id", "delivered_at"},
}

_FORBIDDEN_KEYS = {
    "transcript",
    "transcript_raw",
    "raw_transcript",
    "conversation_text",
    "raw_conversation",
    "prompt",
    "messages",
    "residue_score",
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _canonical_json(value: Any) -> str:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    )


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _required_text(payload: Mapping[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise InvalidCommand(f"{key} must be a non-empty string")
    return value


def _optional_text(payload: Mapping[str, Any], key: str) -> str | None:
    value = payload.get(key)
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise InvalidCommand(f"{key} must be null or a non-empty string")
    return value


def _reject_sensitive(value: Any, path: str = "$") -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            normalized = str(key).strip().lower()
            if normalized in _FORBIDDEN_KEYS:
                raise InvalidCommand(f"sensitive or derived field is forbidden: {path}.{key}")
            _reject_sensitive(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _reject_sensitive(child, f"{path}[{index}]")


class Runtime:
    """SQLite-backed experimental shadow runtime.

    Each command is one transaction: validate domain state, append an event,
    apply its projection, and persist a receipt before returning it.
    """

    def __init__(
        self,
        database: str | Path,
        *,
        log_sink: Callable[[dict[str, Any]], None] | None = None,
    ):
        self.database = str(database)
        self.log_sink = log_sink
        if self.database != ":memory:":
            Path(self.database).parent.mkdir(parents=True, exist_ok=True)
        self._memory_connection: sqlite3.Connection | None = None
        if self.database == ":memory:":
            self._memory_connection = self._new_connection()
        self.migrate()

    def close(self) -> None:
        if self._memory_connection is not None:
            self._memory_connection.close()
            self._memory_connection = None

    def _new_connection(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database, isolation_level=None, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        if self.database != ":memory:":
            connection.execute("PRAGMA journal_mode = WAL")
            connection.execute("PRAGMA synchronous = FULL")
        return connection

    @contextmanager
    def _connection(self) -> Iterator[sqlite3.Connection]:
        if self._memory_connection is not None:
            yield self._memory_connection
            return
        connection = self._new_connection()
        try:
            yield connection
        finally:
            connection.close()

    @contextmanager
    def _transaction(self) -> Iterator[sqlite3.Connection]:
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                yield connection
            except Exception:
                connection.rollback()
                raise
            else:
                connection.commit()

    def migrate(self) -> None:
        schema = Path(__file__).with_name("schema.sql").read_text(encoding="utf-8")
        with self._connection() as connection:
            connection.executescript(schema)
            connection.execute(
                "INSERT OR IGNORE INTO schema_migrations(version, applied_at) VALUES (1, ?)",
                (_now(),),
            )

    def execute(
        self, command_name: str, operation_id: str, payload: Mapping[str, Any]
    ) -> dict[str, Any]:
        if command_name not in _COMMAND_TO_EVENT:
            raise InvalidCommand(f"unsupported command: {command_name}")
        if not isinstance(operation_id, str) or not operation_id.strip():
            raise InvalidCommand("operation_id must be a non-empty string")
        if not isinstance(payload, Mapping):
            raise InvalidCommand("payload must be an object")
        _reject_sensitive(payload)
        normalized_payload = dict(payload)
        unknown = set(normalized_payload) - _COMMAND_FIELDS[command_name]
        if unknown:
            raise InvalidCommand(
                f"unsupported fields for {command_name}: {', '.join(sorted(unknown))}"
            )
        payload_digest = _digest(normalized_payload)

        with self._transaction() as connection:
            existing = connection.execute(
                "SELECT * FROM command_receipts WHERE operation_id = ?", (operation_id,)
            ).fetchone()
            if existing is not None:
                if (
                    existing["command_name"] != command_name
                    or existing["payload_digest"] != payload_digest
                ):
                    raise CommandConflict(
                        f"operation_id {operation_id!r} already has a different command or payload"
                    )
                receipt = self._receipt_dict(existing, replayed=True)
                replayed = True
            else:
                receipt = self._execute_new(
                    connection, command_name, operation_id, normalized_payload, payload_digest
                )
                replayed = False
        self._emit_log(receipt, replayed=replayed)
        return receipt

    def _execute_new(
        self,
        connection: sqlite3.Connection,
        command_name: str,
        operation_id: str,
        normalized_payload: Mapping[str, Any],
        payload_digest: str,
    ) -> dict[str, Any]:
            event_type = self._event_type_for(
                connection, command_name, normalized_payload
            )
            event_id = f"evt_{uuid.uuid4().hex}"
            occurred_at = _now()
            previous = connection.execute(
                "SELECT event_hash FROM journal_events ORDER BY seq DESC LIMIT 1"
            ).fetchone()
            previous_hash = previous["event_hash"] if previous else None
            event_hash = _digest(
                {
                    "event_id": event_id,
                    "operation_id": operation_id,
                    "event_type": event_type,
                    "occurred_at": occurred_at,
                    "payload_digest": payload_digest,
                    "previous_event_hash": previous_hash,
                }
            )
            cursor = connection.execute(
                """
                INSERT INTO journal_events(
                    event_id, operation_id, event_type, occurred_at, payload_json,
                    payload_digest, previous_event_hash, event_hash
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event_id,
                    operation_id,
                    event_type,
                    occurred_at,
                    _canonical_json(normalized_payload),
                    payload_digest,
                    previous_hash,
                    event_hash,
                ),
            )
            seq = int(cursor.lastrowid)
            result = self._apply(
                connection,
                event_type,
                normalized_payload,
                event_id,
                operation_id,
                occurred_at,
                seq,
            )
            receipt_id = f"experimental_rcpt_{uuid.uuid4().hex}"
            receipt_created_at = _now()
            result_json = _canonical_json(result)
            result_digest = _digest(result)
            receipt_digest = _digest(
                {
                    "namespace": "agent-runtime-e0",
                    "receipt_id": receipt_id,
                    "operation_id": operation_id,
                    "command_name": command_name,
                    "payload_digest": payload_digest,
                    "event_id": event_id,
                    "committed_seq": seq,
                    "result_digest": result_digest,
                    "created_at": receipt_created_at,
                }
            )
            connection.execute(
                """
                INSERT INTO command_receipts(
                    receipt_id, operation_id, command_name, payload_digest, event_id,
                    committed_seq, result_json, result_digest, receipt_digest, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    receipt_id,
                    operation_id,
                    command_name,
                    payload_digest,
                    event_id,
                    seq,
                    result_json,
                    result_digest,
                    receipt_digest,
                    receipt_created_at,
                ),
            )
            row = connection.execute(
                "SELECT * FROM command_receipts WHERE receipt_id = ?", (receipt_id,)
            ).fetchone()
            return self._receipt_dict(row, replayed=False)

    @staticmethod
    def _event_type_for(
        connection: sqlite3.Connection,
        command_name: str,
        payload: Mapping[str, Any],
    ) -> str:
        if command_name != "ensure_session":
            return _COMMAND_TO_EVENT[command_name]
        session_id = payload.get("session_id")
        ensure_key = payload.get("ensure_key")
        origin_kind = payload.get("origin_kind")
        origin_ref = payload.get("origin_ref")
        existing = connection.execute(
            """
            SELECT session_id, ensure_key, origin_kind, origin_ref
            FROM sessions
            WHERE session_id = ? OR ensure_key = ?
               OR (origin_kind = ? AND origin_ref = ?)
            LIMIT 1
            """,
            (session_id, ensure_key, origin_kind, origin_ref),
        ).fetchone()
        if existing and (
            existing["session_id"],
            existing["ensure_key"],
            existing["origin_kind"],
            existing["origin_ref"],
        ) == (session_id, ensure_key, origin_kind, origin_ref):
            return "session.ensure_reused"
        return "session.started"

    def ensure_session(self, operation_id: str, **payload: Any) -> dict[str, Any]:
        return self.execute("ensure_session", operation_id, payload)

    def link_session_dispatch(self, operation_id: str, **payload: Any) -> dict[str, Any]:
        return self.execute("link_session_dispatch", operation_id, payload)

    def start_reference_scout(self, operation_id: str, **payload: Any) -> dict[str, Any]:
        return self.execute("start_reference_scout", operation_id, payload)

    def publish_scout_contribution(
        self, operation_id: str, **payload: Any
    ) -> dict[str, Any]:
        return self.execute("publish_scout_contribution", operation_id, payload)

    def commit_reference_bundle(self, operation_id: str, **payload: Any) -> dict[str, Any]:
        return self.execute("commit_reference_bundle", operation_id, payload)

    def deliver_reference_bundle(self, operation_id: str, **payload: Any) -> dict[str, Any]:
        return self.execute("deliver_reference_bundle", operation_id, payload)

    def _apply(
        self,
        connection: sqlite3.Connection,
        event_type: str,
        payload: Mapping[str, Any],
        event_id: str,
        operation_id: str,
        occurred_at: str,
        seq: int,
    ) -> dict[str, Any]:
        handlers: dict[str, Callable[..., dict[str, Any]]] = {
            "session.started": self._apply_session_ensured,
            "session.ensure_reused": self._apply_session_ensured,
            "session.dispatch_linked": self._apply_dispatch_linked,
            "probe.requested": self._apply_scout_started,
            "probe.contribution.published": self._apply_contribution_published,
            "probe.bundle.committed": self._apply_bundle_committed,
            "probe.bundle.delivered": self._apply_bundle_delivered,
        }
        return handlers[event_type](
            connection, payload, event_id, operation_id, occurred_at, seq
        )

    def _apply_session_ensured(
        self, c: sqlite3.Connection, p: Mapping[str, Any], event_id: str,
        operation_id: str, at: str, seq: int
    ) -> dict[str, Any]:
        session_id = _required_text(p, "session_id")
        ensure_key = _required_text(p, "ensure_key")
        origin_kind = _required_text(p, "origin_kind")
        origin_ref = _required_text(p, "origin_ref")
        initial_name = _optional_text(p, "initial_name")
        started_at = _optional_text(p, "started_at") or at
        by_key = c.execute(
            "SELECT * FROM sessions WHERE ensure_key = ?", (ensure_key,)
        ).fetchone()
        by_id = c.execute(
            "SELECT * FROM sessions WHERE session_id = ?", (session_id,)
        ).fetchone()
        by_origin = c.execute(
            "SELECT * FROM sessions WHERE origin_kind = ? AND origin_ref = ?",
            (origin_kind, origin_ref),
        ).fetchone()
        existing = by_key or by_id or by_origin
        if existing:
            identity = (
                existing["session_id"],
                existing["ensure_key"],
                existing["origin_kind"],
                existing["origin_ref"],
            )
            proposed = (session_id, ensure_key, origin_kind, origin_ref)
            if identity != proposed:
                raise DomainConflict("session_id or ensure_key identifies another session")
            c.execute(
                "UPDATE sessions SET last_activity_at = ?, source_through_seq = ? WHERE session_id = ?",
                (at, seq, session_id),
            )
        else:
            c.execute(
                """
                INSERT INTO sessions(
                    session_id, ensure_key, origin_kind, origin_ref, initial_name,
                    current_name, started_at, start_operation_id, source_event_id,
                    last_activity_at, source_through_seq
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    session_id,
                    ensure_key,
                    origin_kind,
                    origin_ref,
                    initial_name,
                    initial_name,
                    started_at,
                    operation_id,
                    event_id,
                    at,
                    seq,
                ),
            )
        return {"session_id": session_id, "ensure_key": ensure_key}

    def _apply_dispatch_linked(
        self, c: sqlite3.Connection, p: Mapping[str, Any], event_id: str,
        operation_id: str, at: str, seq: int
    ) -> dict[str, Any]:
        link_id = _required_text(p, "session_dispatch_link_id")
        session_id = _required_text(p, "session_id")
        dispatch_id = _required_text(p, "dispatch_id")
        linked_at = _optional_text(p, "linked_at") or at
        if not c.execute(
            "SELECT 1 FROM sessions WHERE session_id = ?", (session_id,)
        ).fetchone():
            raise DomainConflict(f"unknown session_id: {session_id}")
        existing = c.execute(
            "SELECT * FROM session_dispatch_links WHERE dispatch_id = ? OR session_dispatch_link_id = ?",
            (dispatch_id, link_id),
        ).fetchone()
        if existing:
            if (
                existing["session_dispatch_link_id"],
                existing["session_id"],
                existing["dispatch_id"],
            ) != (link_id, session_id, dispatch_id):
                raise DomainConflict("dispatch_id or link_id is already linked differently")
        else:
            c.execute(
                """
                INSERT INTO session_dispatch_links(
                    session_dispatch_link_id, session_id, dispatch_id, link_operation_id,
                    linked_at, source_event_id,
                    source_through_seq
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (link_id, session_id, dispatch_id, operation_id, linked_at, event_id, seq),
            )
        c.execute(
            "UPDATE sessions SET last_activity_at = ?, source_through_seq = ? WHERE session_id = ?",
            (at, seq, session_id),
        )
        return {
            "session_dispatch_link_id": link_id,
            "session_id": session_id,
            "dispatch_id": dispatch_id,
        }

    def _apply_scout_started(
        self, c: sqlite3.Connection, p: Mapping[str, Any], event_id: str,
        operation_id: str, at: str, seq: int
    ) -> dict[str, Any]:
        scout_run_id = _required_text(p, "scout_run_id")
        probe_id = _required_text(p, "probe_id")
        session_id = _required_text(p, "session_id")
        dispatch_id = _optional_text(p, "dispatch_id")
        objective_ref = _required_text(p, "objective_ref")
        shape = _required_text(p, "shape")
        source_mode = _required_text(p, "source_mode")
        profile_id = _optional_text(p, "protocol_profile_id")
        profile_version = _optional_text(p, "protocol_profile_version")
        profile_digest = _optional_text(p, "protocol_profile_digest")
        requested_at = _optional_text(p, "requested_at") or at
        if shape not in ("small", "tensioned"):
            raise InvalidCommand("shape must be small or tensioned")
        if source_mode not in ("internal", "external", "internal-and-external"):
            raise InvalidCommand(
                "source_mode must be internal, external, or internal-and-external"
            )
        if not profile_id or not profile_version or not profile_digest:
            raise InvalidCommand(
                "protocol_profile_id, protocol_profile_version, and "
                "protocol_profile_digest are required"
            )
        if not c.execute(
            "SELECT 1 FROM sessions WHERE session_id = ?", (session_id,)
        ).fetchone():
            raise DomainConflict(f"unknown session_id: {session_id}")
        if dispatch_id:
            link = c.execute(
                "SELECT session_id FROM session_dispatch_links WHERE dispatch_id = ?",
                (dispatch_id,),
            ).fetchone()
            if not link:
                raise DomainConflict("dispatch must have an existing session link")
            if link["session_id"] != session_id:
                raise DomainConflict("dispatch belongs to another session")
        if c.execute(
            "SELECT 1 FROM reference_scout_runs WHERE scout_run_id = ? OR probe_id = ?",
            (scout_run_id, probe_id),
        ).fetchone():
            raise DomainConflict("scout_run_id or frozen probe_id already exists")
        c.execute(
            """
            INSERT INTO reference_scout_runs(
                scout_run_id, session_id, dispatch_id, objective_ref, shape,
                probe_id, source_mode, protocol_profile_id, protocol_profile_version,
                protocol_profile_digest,
                requested_at, state, source_through_seq
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'requested', ?)
            """,
            (
                scout_run_id,
                session_id,
                dispatch_id,
                objective_ref,
                shape,
                probe_id,
                source_mode,
                profile_id,
                profile_version,
                profile_digest,
                requested_at,
                seq,
            ),
        )
        return {
            "scout_run_id": scout_run_id,
            "probe_id": probe_id,
            "session_id": session_id,
            "dispatch_id": dispatch_id,
            "state": "requested",
        }

    def _apply_contribution_published(
        self, c: sqlite3.Connection, p: Mapping[str, Any], event_id: str,
        operation_id: str, at: str, seq: int
    ) -> dict[str, Any]:
        recommendation_id = _required_text(p, "recommendation_id")
        scout_run_id = _required_text(p, "scout_run_id")
        probe_id = _required_text(p, "probe_id")
        run = c.execute(
            "SELECT state, probe_id FROM reference_scout_runs WHERE scout_run_id = ?",
            (scout_run_id,),
        ).fetchone()
        if not run:
            raise DomainConflict(f"unknown scout_run_id: {scout_run_id}")
        if run["state"] not in ("requested", "collecting"):
            raise DomainConflict("contributions are accepted only before scout commit")
        if run["probe_id"] != probe_id:
            raise DomainConflict("probe_id does not match Reference Scout run")
        comparability_state = _optional_text(p, "comparability_state")
        if comparability_state not in (None, "comparable", "incommensurable", "count_capped"):
            raise InvalidCommand(
                "comparability_state must be comparable, incommensurable, or count_capped"
            )
        duplicate = c.execute(
            """
            SELECT 1 FROM reference_recommendations
            WHERE recommendation_id = ? OR (scout_run_id = ? AND reference_id = ?)
            """,
            (recommendation_id, scout_run_id, _required_text(p, "reference_id")),
        ).fetchone()
        if duplicate:
            raise DomainConflict("recommendation_id or run/reference identity already exists")
        c.execute(
            """
            INSERT INTO reference_recommendations(
                recommendation_id, scout_run_id, reference_id, source_class,
                locator_observed, access_state, found_by_seat_id,
                evaluated_by_seat_id, evaluation, why_inspect,
                comparability_state, source_event_id, source_through_seq
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                recommendation_id,
                scout_run_id,
                _required_text(p, "reference_id"),
                _required_text(p, "source_class"),
                _required_text(p, "locator_observed"),
                _required_text(p, "access_state"),
                _required_text(p, "found_by_seat_id"),
                _optional_text(p, "evaluated_by_seat_id"),
                _optional_text(p, "evaluation"),
                _required_text(p, "why_inspect"),
                comparability_state,
                event_id,
                seq,
            ),
        )
        c.execute(
            "UPDATE reference_scout_runs SET state = 'collecting', source_through_seq = ? WHERE scout_run_id = ?",
            (seq, scout_run_id),
        )
        return {
            "scout_run_id": scout_run_id,
            "probe_id": probe_id,
            "recommendation_id": recommendation_id,
            "source_event_id": event_id,
        }

    def _apply_bundle_committed(
        self, c: sqlite3.Connection, p: Mapping[str, Any], event_id: str,
        operation_id: str, at: str, seq: int
    ) -> dict[str, Any]:
        scout_run_id = _required_text(p, "scout_run_id")
        probe_id = _required_text(p, "probe_id")
        bundle_digest = _required_text(p, "bundle_digest")
        run = c.execute(
            "SELECT state, probe_id FROM reference_scout_runs WHERE scout_run_id = ?",
            (scout_run_id,),
        ).fetchone()
        if not run:
            raise DomainConflict(f"unknown scout_run_id: {scout_run_id}")
        if run["state"] not in ("requested", "collecting"):
            raise DomainConflict("only an uncommitted scout can be committed")
        if run["probe_id"] != probe_id:
            raise DomainConflict("probe_id does not match Reference Scout run")
        count = c.execute(
            "SELECT COUNT(*) AS n FROM reference_recommendations WHERE scout_run_id = ?",
            (scout_run_id,),
        ).fetchone()["n"]
        c.execute(
            """
            UPDATE reference_scout_runs
            SET state = 'committed', bundle_digest = ?, committed_event_id = ?,
                source_through_seq = ?
            WHERE scout_run_id = ?
            """,
            (bundle_digest, event_id, seq, scout_run_id),
        )
        return {
            "scout_run_id": scout_run_id,
            "probe_id": probe_id,
            "state": "committed",
            "bundle_digest": bundle_digest,
            "recommendation_count": count,
        }

    def _apply_bundle_delivered(
        self, c: sqlite3.Connection, p: Mapping[str, Any], event_id: str,
        operation_id: str, at: str, seq: int
    ) -> dict[str, Any]:
        scout_run_id = _required_text(p, "scout_run_id")
        probe_id = _required_text(p, "probe_id")
        delivered_at = _optional_text(p, "delivered_at") or at
        run = c.execute(
            "SELECT state, bundle_digest, probe_id FROM reference_scout_runs WHERE scout_run_id = ?",
            (scout_run_id,),
        ).fetchone()
        if not run:
            raise DomainConflict(f"unknown scout_run_id: {scout_run_id}")
        if run["state"] != "committed":
            raise DomainConflict("only a committed scout can be delivered")
        if run["probe_id"] != probe_id:
            raise DomainConflict("probe_id does not match Reference Scout run")
        c.execute(
            """
            UPDATE reference_scout_runs
            SET state = 'delivered', delivered_at = ?, source_through_seq = ?
            WHERE scout_run_id = ?
            """,
            (delivered_at, seq, scout_run_id),
        )
        return {
            "scout_run_id": scout_run_id,
            "probe_id": probe_id,
            "state": "delivered",
            "bundle_digest": run["bundle_digest"],
        }

    @staticmethod
    def _receipt_dict(row: sqlite3.Row, replayed: bool) -> dict[str, Any]:
        return {
            "receipt_id": row["receipt_id"],
            "operation_id": row["operation_id"],
            "command_name": row["command_name"],
            "payload_digest": row["payload_digest"],
            "event_id": row["event_id"],
            "committed_seq": row["committed_seq"],
            "result": json.loads(row["result_json"]),
            "result_digest": row["result_digest"],
            "receipt_digest": row["receipt_digest"],
            "created_at": row["created_at"],
            "replayed": replayed,
        }

    def verify_receipt(self, receipt_id: str) -> dict[str, Any]:
        with self._connection() as connection:
            row = connection.execute(
                """
                SELECT r.*, e.payload_digest AS event_payload_digest,
                       e.payload_json AS event_payload_json
                FROM command_receipts r
                JOIN journal_events e
                  ON e.event_id = r.event_id AND e.seq = r.committed_seq
                WHERE r.receipt_id = ?
                """,
                (receipt_id,),
            ).fetchone()
            if not row:
                raise ReceiptNotFound(receipt_id)
            if row["payload_digest"] != row["event_payload_digest"]:
                raise DomainConflict("receipt payload digest does not match journal event")
            if _digest(json.loads(row["event_payload_json"])) != row["event_payload_digest"]:
                raise DomainConflict("journal payload bytes do not match event digest")
            if _digest(json.loads(row["result_json"])) != row["result_digest"]:
                raise DomainConflict("receipt result digest does not match result")
            expected_receipt_digest = _digest(
                {
                    "namespace": "agent-runtime-e0",
                    "receipt_id": row["receipt_id"],
                    "operation_id": row["operation_id"],
                    "command_name": row["command_name"],
                    "payload_digest": row["payload_digest"],
                    "event_id": row["event_id"],
                    "committed_seq": row["committed_seq"],
                    "result_digest": row["result_digest"],
                    "created_at": row["created_at"],
                }
            )
            if expected_receipt_digest != row["receipt_digest"]:
                raise DomainConflict("receipt digest mismatch")
            receipt = self._receipt_dict(row, replayed=False)
            receipt["verified"] = True
            return receipt

    def replay(self) -> dict[str, int]:
        """Rebuild every projection in one transaction from the ordered journal."""
        projection_tables = (
            "reference_recommendations",
            "reference_scout_runs",
            "session_dispatch_links",
            "sessions",
        )
        counts: dict[str, int] = {}
        with self._transaction() as connection:
            for table in projection_tables:
                connection.execute(f"DELETE FROM {table}")
            events = connection.execute(
                "SELECT * FROM journal_events ORDER BY seq"
            ).fetchall()
            previous_hash = None
            for event in events:
                payload = json.loads(event["payload_json"])
                if _digest(payload) != event["payload_digest"]:
                    raise DomainConflict(f"payload digest mismatch at seq {event['seq']}")
                if event["previous_event_hash"] != previous_hash:
                    raise DomainConflict(f"event chain mismatch at seq {event['seq']}")
                expected_hash = _digest(
                    {
                        "event_id": event["event_id"],
                        "operation_id": event["operation_id"],
                        "event_type": event["event_type"],
                        "occurred_at": event["occurred_at"],
                        "payload_digest": event["payload_digest"],
                        "previous_event_hash": previous_hash,
                    }
                )
                if expected_hash != event["event_hash"]:
                    raise DomainConflict(f"event hash mismatch at seq {event['seq']}")
                self._apply(
                    connection,
                    event["event_type"],
                    payload,
                    event["event_id"],
                    event["operation_id"],
                    event["occurred_at"],
                    event["seq"],
                )
                previous_hash = event["event_hash"]
            for table in projection_tables:
                counts[table] = connection.execute(
                    f"SELECT COUNT(*) AS n FROM {table}"
                ).fetchone()["n"]
        return counts

    def _emit_log(self, receipt: Mapping[str, Any], *, replayed: bool) -> None:
        if self.log_sink is None:
            return
        result = receipt["result"]
        with self._connection() as connection:
            event = connection.execute(
                "SELECT event_type FROM journal_events WHERE event_id = ?",
                (receipt["event_id"],),
            ).fetchone()
        record = {
            "operation_id": receipt["operation_id"],
            "event_id": receipt["event_id"],
            "receipt_id": receipt["receipt_id"],
            "event_type": event["event_type"],
            "journal_offset": receipt["committed_seq"],
            "session_id": result.get("session_id"),
            "dispatch_id": result.get("dispatch_id"),
            "scout_run_id": result.get("scout_run_id"),
            "state": result.get("state"),
            "outcome": "idempotent_replay" if replayed else "committed",
            "error_code": None,
        }
        self.log_sink(record)

    def shadow_runtime_refs(self, dispatch_id: str) -> dict[str, Any] | None:
        """Derive the candidate v0.7 runtime_refs fragment without side effects."""
        with self._connection() as connection:
            link = connection.execute(
                """
                SELECT session_dispatch_link_id, session_id, dispatch_id,
                       link_operation_id, source_event_id
                FROM session_dispatch_links
                WHERE dispatch_id = ?
                """,
                (dispatch_id,),
            ).fetchone()
            if not link:
                return None
            scout_ids = [
                row["scout_run_id"]
                for row in connection.execute(
                    """
                    SELECT scout_run_id FROM reference_scout_runs
                    WHERE dispatch_id = ? ORDER BY scout_run_id
                    """,
                    (dispatch_id,),
                ).fetchall()
            ]
            return {
                "schema_version": "subagents-dispatch.runtime_refs@0.7",
                "session_id": link["session_id"],
                "session_dispatch_link_id": link["session_dispatch_link_id"],
                "link_operation_id": link["link_operation_id"],
                "source_event_id": link["source_event_id"],
                "scout_run_ids": scout_ids,
            }

    def projection(self, table: str) -> list[dict[str, Any]]:
        allowed = {
            "sessions",
            "session_dispatch_links",
            "reference_scout_runs",
            "reference_recommendations",
            "journal_events",
            "command_receipts",
        }
        if table not in allowed:
            raise InvalidCommand(f"unsupported table: {table}")
        with self._connection() as connection:
            rows = connection.execute(f"SELECT * FROM {table} ORDER BY 1").fetchall()
            return [dict(row) for row in rows]
