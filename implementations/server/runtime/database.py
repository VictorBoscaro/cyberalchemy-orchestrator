"""SQLite policy, immutable migrations and serialized write boundary."""

from __future__ import annotations

import hashlib
import sqlite3
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from .errors import IntegrityError

MIGRATION_NAMES = (
    "001_aci_slice0.sql",
    "002_artifact_store.sql",
    "003_profile_capability.sql",
    "004_apt_projection.sql",
    "005_apt_granular_projection.sql",
    "006_apt_projector_state.sql",
    "007_session_origin_heads.sql",
    "008_reference_scout_ingestion.sql",
    "009_host_workflow_binding.sql",
    "010_agent_reference_delivery.sql",
    "011_bus_reveal_delivery.sql",
)


class _ClosingConnection(sqlite3.Connection):
    def __exit__(self, exc_type, exc_value, traceback):
        try:
            return super().__exit__(exc_type, exc_value, traceback)
        finally:
            self.close()


class RuntimeDatabase:
    def __init__(self, path: Path, *, busy_timeout_ms: int = 3000) -> None:
        self.path = Path(path)
        self.busy_timeout_ms = busy_timeout_ms
        self._write_lock = threading.RLock()

    def connect(self) -> sqlite3.Connection:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(
            self.path,
            timeout=self.busy_timeout_ms / 1000,
            isolation_level=None,
            check_same_thread=False,
            factory=_ClosingConnection,
        )
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys=ON")
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=FULL")
        conn.execute(f"PRAGMA busy_timeout={self.busy_timeout_ms}")
        return conn

    def migrate(self) -> list[dict[str, str]]:
        migration_dir = Path(__file__).with_name("migrations")
        applied: list[dict[str, str]] = []
        with self._write_lock, self.connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            try:
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS schema_migrations(
                      version INTEGER PRIMARY KEY,
                      name TEXT NOT NULL UNIQUE,
                      checksum TEXT NOT NULL,
                      applied_at TEXT NOT NULL
                    )
                    """
                )
                rows = {
                    row["version"]: row
                    for row in conn.execute(
                        "SELECT version,name,checksum FROM schema_migrations"
                    )
                }
                for version, name in enumerate(MIGRATION_NAMES, start=1):
                    body = (migration_dir / name).read_bytes()
                    checksum = "sha256:" + hashlib.sha256(body).hexdigest()
                    existing = rows.get(version)
                    if existing:
                        if existing["name"] != name or existing["checksum"] != checksum:
                            raise IntegrityError(
                                f"migration {version} checksum/name mismatch"
                            )
                        continue
                    for statement in body.decode("utf-8").split(";"):
                        if statement.strip():
                            conn.execute(statement)
                    conn.execute(
                        """
                        INSERT INTO schema_migrations(version,name,checksum,applied_at)
                        VALUES(?,?,?,strftime('%Y-%m-%dT%H:%M:%fZ','now'))
                        """,
                        (version, name, checksum),
                    )
                    conn.execute(f"PRAGMA user_version={version}")
                    applied.append({"name": name, "checksum": checksum})
                unknown = conn.execute(
                    "SELECT version,name FROM schema_migrations WHERE version>?",
                    (len(MIGRATION_NAMES),),
                ).fetchall()
                if unknown:
                    raise IntegrityError("database contains unknown future migrations")
                user_version = int(conn.execute("PRAGMA user_version").fetchone()[0])
                if user_version != len(MIGRATION_NAMES):
                    raise IntegrityError(
                        f"user_version {user_version} does not match migration manifest"
                    )
                conn.commit()
            except Exception:
                conn.rollback()
                raise
        return applied

    def verify_policy(self) -> dict[str, str | int]:
        with self.connect() as conn:
            policy = {
                "journal_mode": str(conn.execute("PRAGMA journal_mode").fetchone()[0]).lower(),
                "synchronous": int(conn.execute("PRAGMA synchronous").fetchone()[0]),
                "foreign_keys": int(conn.execute("PRAGMA foreign_keys").fetchone()[0]),
                "quick_check": str(conn.execute("PRAGMA quick_check").fetchone()[0]),
            }
        if policy != {
            "journal_mode": "wal",
            "synchronous": 2,
            "foreign_keys": 1,
            "quick_check": "ok",
        }:
            raise IntegrityError(f"SQLite policy mismatch: {policy}")
        return policy

    @contextmanager
    def write(self) -> Iterator[sqlite3.Connection]:
        with self._write_lock, self.connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            try:
                yield conn
                conn.commit()
            except Exception:
                conn.rollback()
                raise
