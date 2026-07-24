"""Trusted CLI for the descriptor's non-serving operations."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Sequence

from .errors import GateBlockedError
from .local_pilot import create_local_pilot_app, preflight_local_pilot
from .operator_recovery import (
    create_local_pilot_backup,
    retire_local_pilot_database,
    verify_local_pilot_database,
)
from .service import RuntimeService, RuntimeSettings


def settings_from_environment() -> RuntimeSettings:
    repo = Path(os.environ.get("ACI_REPO_ROOT", Path.cwd())).resolve()
    return RuntimeSettings(
        database_path=Path(
            os.environ.get(
                "ACI_RUNTIME_DB", repo / "telemetry/runtime/aci-slice0.sqlite3"
            )
        ),
        repo_root=repo,
        ledger_path=Path(
            os.environ.get(
                "ACI_LEDGER_PATH", repo / "telemetry/agents/subagents-dispatch.yaml"
            )
        ),
        local_pilot_serve_enabled=False,
        repo_id=os.environ.get("ACI_REPO_ID", "cyberalchemy-orchestrator"),
    )


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(prog="runtime")
    commands = result.add_subparsers(dest="command", required=True)
    for name in ("migrate", "register-profiles", "verify-store"):
        commands.add_parser(name)
    issue = commands.add_parser("issue-capability")
    issue.add_argument("--principal", required=True)
    issue.add_argument("--action", required=True)
    issue.add_argument("--phase", required=True)
    issue.add_argument("--context-json", required=True)
    issue.add_argument("--expires-at")
    activate = commands.add_parser(
        "activate-local-probe",
        help=(
            "activate the frozen v1 reference-probe lineage context; "
            "this is not a general ProbeTool or a Reference Scout launch"
        ),
    )
    for name in (
        "session-id",
        "dispatch-id",
        "probe-id",
        "group-aggregate-id",
        "seat-id",
        "attempt-id",
        "operation-id",
    ):
        activate.add_argument("--" + name, required=True)
    serve = commands.add_parser("serve")
    serve.add_argument("--local-pilot", action="store_true", required=True)
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8766)
    serve.add_argument("--database", type=Path)
    serve.add_argument("--ledger", type=Path)
    verify_pilot = commands.add_parser("verify-local-pilot-database")
    verify_pilot.add_argument("--database", type=Path, required=True)
    verify_pilot.add_argument("--repo-root", type=Path, default=Path.cwd())
    backup = commands.add_parser("backup-local-pilot-database")
    backup.add_argument("--source", type=Path, required=True)
    backup.add_argument("--destination", type=Path, required=True)
    backup.add_argument("--repo-root", type=Path, default=Path.cwd())
    retire = commands.add_parser("retire-local-pilot-database")
    retire.add_argument("--source", type=Path, required=True)
    retire.add_argument("--destination", type=Path, required=True)
    retire.add_argument("--verified-backup", type=Path, required=True)
    retire.add_argument("--repo-root", type=Path, default=Path.cwd())
    retire.add_argument("--confirmed-stopped", action="store_true", required=True)
    show_log = commands.add_parser("show-orchestration-log")
    show_log.add_argument("--dispatch-id", required=True)
    show_log.add_argument("--database", type=Path, required=True)
    show_log.add_argument("--repo-root", type=Path, default=Path.cwd())
    show_log.add_argument("--ledger", type=Path, required=True)
    return result


def run(argv: Sequence[str] | None = None) -> dict:
    args = parser().parse_args(argv)
    if args.command == "serve":
        if not 1 <= args.port <= 65535:
            raise GateBlockedError("local-pilot port must be between 1 and 65535")
        repo = Path(os.environ.get("ACI_REPO_ROOT", Path.cwd())).resolve()
        runtime, preflight = preflight_local_pilot(
            repo_root=repo,
            database_path=args.database,
            ledger_path=args.ledger,
            host=args.host,
            opted_in=os.environ.get("ACI_LOCAL_PILOT_ENABLED") == "1",
            repo_id=os.environ.get("ACI_REPO_ID", "cyberalchemy-orchestrator"),
        )
        import uvicorn

        uvicorn.run(
            create_local_pilot_app(runtime),
            host="127.0.0.1",
            port=args.port,
            log_level="warning",
        )
        return {"status": "stopped", "preflight": preflight}
    if args.command == "verify-local-pilot-database":
        return verify_local_pilot_database(
            args.database, repo_root=args.repo_root
        )
    if args.command == "backup-local-pilot-database":
        return create_local_pilot_backup(
            args.source,
            args.destination,
            repo_root=args.repo_root,
        )
    if args.command == "retire-local-pilot-database":
        return retire_local_pilot_database(
            args.source,
            args.destination,
            verified_backup=args.verified_backup,
            repo_root=args.repo_root,
            confirmed_stopped=args.confirmed_stopped,
        )
    if args.command == "show-orchestration-log":
        runtime = RuntimeService(
            RuntimeSettings(
                database_path=args.database.resolve(),
                repo_root=args.repo_root.resolve(),
                ledger_path=args.ledger.resolve(),
            )
        )
        runtime.open()
        return runtime.get_orchestration_dispatch_log(
            dispatch_id=args.dispatch_id
        )
    runtime = RuntimeService(settings_from_environment())
    opened = runtime.open()
    if args.command == "migrate":
        return opened
    if args.command == "register-profiles":
        return runtime.register_profiles()
    if args.command == "verify-store":
        return runtime.journal.verify_store()
    if args.command == "issue-capability":
        return runtime.issue_capability(
            principal_id=args.principal,
            action=args.action,
            phase=args.phase,
            context=json.loads(args.context_json),
            expires_at=args.expires_at,
        )
    if args.command == "activate-local-probe":
        return runtime.activate_local_probe(
            session_id=args.session_id,
            dispatch_id=args.dispatch_id,
            probe_id=args.probe_id,
            group_aggregate_id=args.group_aggregate_id,
            seat_id=args.seat_id,
            attempt_id=args.attempt_id,
            operation_id=args.operation_id,
        )
    raise AssertionError("unreachable")


def main() -> None:
    print(json.dumps(run(), ensure_ascii=False, indent=2))
