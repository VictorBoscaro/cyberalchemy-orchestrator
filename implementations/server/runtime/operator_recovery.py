"""Conservative backup, verification and retirement for local-pilot databases."""

from __future__ import annotations

import hashlib
import os
import sqlite3
import uuid
from contextlib import closing
from pathlib import Path
from typing import Any

from .artifacts import ArtifactStore
from .database import MIGRATION_NAMES, RuntimeDatabase
from .errors import GateBlockedError, IntegrityError
from .journal import RuntimeJournal
from .profiles import ProfileImporter
from .projections import ProjectionManager
from .service import ACI_SCHEMAS, PROFILE_MANIFEST


def _qualified(path: Path) -> Path:
    return Path(path).expanduser().resolve()


def _require_existing_database(path: Path) -> Path:
    resolved = _qualified(path)
    if not resolved.is_file():
        raise GateBlockedError(f"runtime database is unavailable: {resolved}")
    return resolved


def _database_identity(conn: sqlite3.Connection) -> dict[str, Any]:
    event = conn.execute(
        """
        SELECT journal_offset,event_id
        FROM events ORDER BY journal_offset DESC LIMIT 1
        """
    ).fetchone()
    return {
        "user_version": int(conn.execute("PRAGMA user_version").fetchone()[0]),
        "event_count": int(conn.execute("SELECT count(*) FROM events").fetchone()[0]),
        "last_offset": int(event[0]) if event else 0,
        "last_event_id": str(event[1]) if event else None,
        "command_receipt_count": int(
            conn.execute("SELECT count(*) FROM command_receipts").fetchone()[0]
        ),
    }


def verify_local_pilot_database(path: Path, *, repo_root: Path) -> dict[str, Any]:
    """Verify migrations, SQLite integrity, journal grouping and APT watermark."""
    database_path = _require_existing_database(path)
    database = RuntimeDatabase(database_path)

    # migrate() is a no-op for a valid database and is the canonical checksum
    # verifier for the immutable migration manifest.
    if database.migrate():
        raise IntegrityError("verification unexpectedly applied missing migrations")

    root = _qualified(repo_root)
    profiles_manifest = ProfileImporter(root)
    verified_profiles = profiles_manifest.load_manifest(root / PROFILE_MANIFEST)
    bindings = ProfileImporter.event_bindings(verified_profiles)
    bindings.update(ACI_SCHEMAS)
    journal = RuntimeJournal(database, ArtifactStore(database))
    journal.bind_event_schemas(bindings)
    journal_receipt = journal.verify_store()
    projection = ProjectionManager(database).apt_state()
    expected_profiles = sorted(
        (
            profile.profile_id,
            profile.profile_version,
            profile.authoritative_path,
            profile.authoritative_file_digest,
            profile.canonical_digest,
            profile.canonical_size_bytes,
        )
        for profile in verified_profiles
    )
    with database.connect() as conn:
        migration_count = int(
            conn.execute("SELECT count(*) FROM schema_migrations").fetchone()[0]
        )
        profile_rows = conn.execute(
            """
            SELECT profile_id,profile_version,authoritative_path,
                   authoritative_file_digest,canonical_digest,canonical_size_bytes,
                   registration_event_id
            FROM protocol_profiles ORDER BY profile_id,profile_version
            """
        ).fetchall()
        actual_profiles = [
            (
                row["profile_id"],
                row["profile_version"],
                row["authoritative_path"],
                row["authoritative_file_digest"],
                row["canonical_digest"],
                row["canonical_size_bytes"],
            )
            for row in profile_rows
        ]
        registration_ids = {row["registration_event_id"] for row in profile_rows}
        registration = (
            conn.execute(
                "SELECT event_type FROM events WHERE event_id=?",
                (next(iter(registration_ids)),),
            ).fetchone()
            if len(registration_ids) == 1 and registration_ids
            else None
        )
        foreign_key_violations = conn.execute("PRAGMA foreign_key_check").fetchall()
        identity = _database_identity(conn)
    if migration_count != len(MIGRATION_NAMES):
        raise IntegrityError("migration count differs from the runtime manifest")
    if foreign_key_violations:
        raise IntegrityError("SQLite foreign-key integrity check failed")
    if (
        len(expected_profiles) != 4
        or actual_profiles != expected_profiles
        or not registration
        or registration["event_type"] != "aci.protocol_profile_registered@1"
    ):
        raise IntegrityError("local-pilot profile set differs from verified manifest")
    if not projection["current"]:
        raise IntegrityError("APT projection is behind the verified journal")

    return {
        "path": str(database_path),
        "size_bytes": database_path.stat().st_size,
        "sha256": hashlib.sha256(database_path.read_bytes()).hexdigest(),
        "migrations": migration_count,
        "profiles": len(actual_profiles),
        "journal": journal_receipt,
        "projection": projection,
        "identity": identity,
    }


def create_local_pilot_backup(
    source: Path, destination: Path, *, repo_root: Path
) -> dict[str, Any]:
    """Create and verify an atomic SQLite online backup at a new path."""
    source_path = _require_existing_database(source)
    destination_path = _qualified(destination)
    if source_path == destination_path:
        raise GateBlockedError("backup destination must differ from its source")
    if destination_path.exists():
        raise GateBlockedError("backup destination already exists")
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination_path.with_name(
        f".{destination_path.name}.incomplete-{uuid.uuid4().hex}"
    )

    try:
        source_uri = source_path.as_uri() + "?mode=ro"
        with closing(
            sqlite3.connect(source_uri, uri=True, timeout=3)
        ) as source_conn, closing(
            sqlite3.connect(temporary, timeout=3)
        ) as destination_conn:
            source_conn.execute("PRAGMA busy_timeout=3000")
            if source_conn.execute("PRAGMA quick_check").fetchone()[0] != "ok":
                raise IntegrityError("source database quick_check failed")
            source_conn.backup(destination_conn)
        receipt = verify_local_pilot_database(temporary, repo_root=repo_root)
        os.replace(temporary, destination_path)
    except Exception:
        if temporary.exists():
            temporary.unlink()
        raise
    receipt["path"] = str(destination_path)
    receipt["sha256"] = hashlib.sha256(destination_path.read_bytes()).hexdigest()
    receipt["size_bytes"] = destination_path.stat().st_size
    receipt["source"] = str(source_path)
    return receipt


def retire_local_pilot_database(
    source: Path,
    destination: Path,
    *,
    verified_backup: Path,
    repo_root: Path,
    confirmed_stopped: bool = False,
) -> dict[str, Any]:
    """Move a stopped database to an explicit recovery location.

    Retirement never deletes bytes. It requires a verified backup with the same
    journal identity and refuses a database with WAL/SHM sidecars, which is the
    conservative signal that the local pilot may still be open.
    """
    source_path = _require_existing_database(source)
    destination_path = _qualified(destination)
    backup_path = _require_existing_database(verified_backup)
    if len({source_path, destination_path, backup_path}) != 3:
        raise GateBlockedError("source, retirement destination and backup must differ")
    if destination_path.exists():
        raise GateBlockedError("retirement destination already exists")

    if not confirmed_stopped:
        raise GateBlockedError(
            "operator must explicitly confirm the local pilot is stopped"
        )

    checkpoint = sqlite3.connect(source_path, timeout=3)
    try:
        checkpoint.execute("PRAGMA busy_timeout=3000")
        result = checkpoint.execute("PRAGMA wal_checkpoint(TRUNCATE)").fetchone()
        if result is None or int(result[0]) != 0:
            raise GateBlockedError(
                "runtime database is busy; stop the pilot before retirement"
            )
    finally:
        checkpoint.close()
    if any(
        Path(str(source_path) + suffix).exists() for suffix in ("-wal", "-shm")
    ):
        raise GateBlockedError(
            "runtime WAL/SHM sidecars remain; stop the pilot before retirement"
        )

    source_receipt = verify_local_pilot_database(source_path, repo_root=repo_root)
    backup_receipt = verify_local_pilot_database(backup_path, repo_root=repo_root)
    if source_receipt["identity"] != backup_receipt["identity"]:
        raise GateBlockedError("verified backup does not match runtime journal identity")

    # Verification can create transient WAL sidecars. Their persistence means
    # another connection is still holding the database open.
    if any(
        Path(str(source_path) + suffix).exists() for suffix in ("-wal", "-shm")
    ):
        raise GateBlockedError("runtime database remained open after verification")

    destination_path.parent.mkdir(parents=True, exist_ok=True)
    os.replace(source_path, destination_path)
    return {
        "status": "retired",
        "recoverable": True,
        "source": str(source_path),
        "destination": str(destination_path),
        "verified_backup": str(backup_path),
        "identity": source_receipt["identity"],
        "sha256": hashlib.sha256(destination_path.read_bytes()).hexdigest(),
    }
