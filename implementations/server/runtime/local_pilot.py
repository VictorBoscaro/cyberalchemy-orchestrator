"""Fail-closed Stage-C composition for the explicitly authorized local pilot."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

from fastapi import FastAPI

from .api import create_health_router, create_provenance_router, create_router
from .errors import GateBlockedError
from .service import RuntimeService, RuntimeSettings

STAGE_C_RECEIPT = Path(
    "docs/features/agent-provenance-telemetry/integration/stage-c/"
    "local-pilot-enablement.md"
)
STAGE_C_RECEIPT_SHA256 = (
    "9ce50d2b96f49cdd077235fd5a9cfd72f1598e1ca03b5f7fc8eaddead8cb82e2"
)
STAGE_B_RECEIPT = Path(
    "docs/features/agent-provenance-telemetry/integration/stage-b/"
    "execution-receipt.md"
)
STAGE_B_RECEIPT_SHA256 = (
    "73f9d568153cffa2d8cdb45f92256802047ab1aa28f32654d09a91e9f4a00ebc"
)
STRICT_LEDGER = Path("telemetry/agents/subagents-dispatch.yaml")
DEFAULT_RUNTIME_DB = Path("telemetry/runtime/aci-slice0.sqlite3")
STAGE_E_SOURCE_MANIFEST = Path(
    "docs/features/agent-provenance-telemetry/integration/stage-e/"
    "source-manifest.json"
)
STAGE_E_SOURCE_MANIFEST_SHA256 = (
    "81df64e6a58896b5fc2dbee54fa7f13deacc33e2c92b4fec1e1da02943ee56f6"
)


def _verify_file(path: Path, expected_sha256: str, label: str) -> None:
    try:
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as exc:
        raise GateBlockedError(f"{label} is unavailable") from exc
    if actual != expected_sha256:
        raise GateBlockedError(f"{label} digest mismatch")


def _verify_source_manifest(root: Path) -> None:
    manifest_path = root / STAGE_E_SOURCE_MANIFEST
    _verify_file(
        manifest_path,
        STAGE_E_SOURCE_MANIFEST_SHA256,
        "Stage-E source manifest",
    )
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        files = manifest["files"]
    except (OSError, KeyError, json.JSONDecodeError) as exc:
        raise GateBlockedError("Stage-E source manifest is malformed") from exc
    if (
        set(manifest) != {"manifest_version", "scope", "files"}
        or manifest["manifest_version"] != "1"
        or not isinstance(files, dict)
        or not files
    ):
        raise GateBlockedError("Stage-E source manifest shape is invalid")
    for relative, qualified_digest in files.items():
        if (
            not isinstance(relative, str)
            or not isinstance(qualified_digest, str)
            or not qualified_digest.startswith("sha256:")
            or len(qualified_digest) != 71
        ):
            raise GateBlockedError("Stage-E source manifest entry is invalid")
        candidate = (root / relative).resolve()
        try:
            candidate.relative_to(root)
        except ValueError as exc:
            raise GateBlockedError("Stage-E source path escapes repository") from exc
        _verify_file(candidate, qualified_digest[7:], f"Stage-E source {relative}")


def _verify_exact_registered_profiles(
    runtime: RuntimeService, registration_event_id: str
) -> None:
    expected = sorted(
        (
            profile.profile_id,
            profile.profile_version,
            profile.authoritative_path,
            profile.authoritative_file_digest,
            profile.canonical_digest,
            profile.canonical_size_bytes,
        )
        for profile in runtime._profiles
    )
    with runtime.database.connect() as conn:
        rows = conn.execute(
            """
            SELECT profile_id,profile_version,authoritative_path,
                   authoritative_file_digest,canonical_digest,canonical_size_bytes,
                   registration_event_id
            FROM protocol_profiles ORDER BY profile_id,profile_version
            """
        ).fetchall()
        actual = [
            (
                row["profile_id"],
                row["profile_version"],
                row["authoritative_path"],
                row["authoritative_file_digest"],
                row["canonical_digest"],
                row["canonical_size_bytes"],
            )
            for row in rows
        ]
        registration_ids = {row["registration_event_id"] for row in rows}
        registration = (
            conn.execute(
                "SELECT event_type FROM events WHERE event_id=?",
                (next(iter(registration_ids)),),
            ).fetchone()
            if len(registration_ids) == 1 and registration_ids
            else None
        )
    if (
        len(expected) != 4
        or actual != expected
        or registration_ids != {registration_event_id}
        or not registration
        or registration["event_type"] != "aci.protocol_profile_registered@1"
    ):
        raise GateBlockedError("registered profile set differs from verified manifest")


def preflight_local_pilot(
    *,
    repo_root: Path,
    database_path: Path | None,
    ledger_path: Path | None,
    host: str,
    opted_in: bool,
    repo_id: str = "cyberalchemy-orchestrator",
    now: Callable[[], datetime] | None = None,
) -> tuple[RuntimeService, dict[str, Any]]:
    """Complete every authorized check before a caller may open a socket."""
    root = repo_root.resolve()
    if not opted_in:
        raise GateBlockedError("ACI_LOCAL_PILOT_ENABLED must be exactly 1")
    if host != "127.0.0.1":
        raise GateBlockedError("local pilot must bind exactly 127.0.0.1")
    if database_path is None:
        raise GateBlockedError("an explicit dedicated SQLite database path is required")
    if ledger_path is None:
        raise GateBlockedError("an explicit strict dispatch ledger path is required")
    database = database_path.resolve()
    ledger = ledger_path.resolve()
    if database == (root / DEFAULT_RUNTIME_DB).resolve():
        raise GateBlockedError("the shared/default runtime database is forbidden")
    if database == ledger or not database.is_absolute():
        raise GateBlockedError("a dedicated absolute SQLite database path is required")
    if ledger != (root / STRICT_LEDGER).resolve() or not ledger.is_file():
        raise GateBlockedError("the exact strict dispatch ledger path is required")

    _verify_file(root / STAGE_C_RECEIPT, STAGE_C_RECEIPT_SHA256, "Stage-C receipt")
    _verify_file(root / STAGE_B_RECEIPT, STAGE_B_RECEIPT_SHA256, "Stage-B receipt")
    _verify_source_manifest(root)
    ledger_before = ledger.read_bytes()
    if ledger_before.startswith(b"\xef\xbb\xbf"):
        raise GateBlockedError("strict dispatch ledger must be UTF-8 without BOM")

    runtime = RuntimeService(
        RuntimeSettings(
            database_path=database,
            repo_root=root,
            ledger_path=ledger,
            local_pilot_serve_enabled=True,
            repo_id=repo_id,
        ),
        now=now,
    )
    opened = runtime.open()
    profiles = runtime.register_profiles()
    ordered_event_ids = profiles.get("ordered_event_ids", [])
    if len(ordered_event_ids) != 1:
        raise GateBlockedError("profile registration receipt is not one atomic event")
    _verify_exact_registered_profiles(runtime, ordered_event_ids[0])
    journal = runtime.journal.verify_store()
    projection = runtime.projections.catch_up_apt(runtime.journal)
    health = runtime.health()
    if not health["ready"] or not projection["current"]:
        raise GateBlockedError("runtime preflight is not ready")
    if ledger.read_bytes() != ledger_before:
        raise GateBlockedError("strict dispatch ledger changed during preflight")
    return runtime, {
        "opened": opened,
        "profiles": profiles,
        "journal": journal,
        "projection": projection,
        "health": health,
    }


def create_local_pilot_app(runtime: RuntimeService) -> FastAPI:
    """Mount only the Stage-B reviewed runtime, provenance and health routes."""
    app = FastAPI(
        title="ACI/APT local pilot",
        version="stage-c",
        openapi_url=None,
        docs_url=None,
        redoc_url=None,
    )
    provider = lambda: runtime
    enabled = lambda: True
    app.include_router(create_router(provider, enabled=enabled))
    app.include_router(create_provenance_router(provider, enabled=enabled))
    app.include_router(create_health_router(provider, enabled=enabled))
    return app
