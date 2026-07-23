"""Trusted CLI for the descriptor's non-serving operations."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Sequence

from .errors import GateBlockedError
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
    activate = commands.add_parser("activate-local-probe")
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
    return result


def run(argv: Sequence[str] | None = None) -> dict:
    args = parser().parse_args(argv)
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
    raise GateBlockedError(
        "local-pilot serving remains blocked pending a separate review receipt"
    )


def main() -> None:
    print(json.dumps(run(), ensure_ascii=False, indent=2))
