from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .ledger_shadow import ShadowLedgerReconciler
from .runtime import Runtime, RuntimeErrorBase


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Experimental shadow agent runtime")
    parser.add_argument("--database", required=True, type=Path)
    subparsers = parser.add_subparsers(dest="action", required=True)

    subparsers.add_parser("init")
    command = subparsers.add_parser("command")
    command.add_argument("command_name")
    command.add_argument("operation_id")
    command.add_argument("payload_json", help="JSON object; transcripts/prompts are rejected")

    receipt = subparsers.add_parser("verify-receipt")
    receipt.add_argument("receipt_id")

    subparsers.add_parser("replay")
    show = subparsers.add_parser("show")
    show.add_argument(
        "table",
        choices=[
            "sessions",
            "session_dispatch_links",
            "reference_scout_runs",
            "reference_recommendations",
            "journal_events",
            "command_receipts",
        ],
    )
    reconcile = subparsers.add_parser("reconcile-ledger")
    reconcile.add_argument("ledger_path", type=Path)
    reconcile.add_argument("dispatch_id")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    runtime = Runtime(args.database)
    try:
        if args.action == "init":
            output = {"database": str(args.database), "initialized": True}
        elif args.action == "command":
            payload = json.loads(args.payload_json)
            output = runtime.execute(args.command_name, args.operation_id, payload)
        elif args.action == "verify-receipt":
            output = runtime.verify_receipt(args.receipt_id)
        elif args.action == "replay":
            output = runtime.replay()
        elif args.action == "reconcile-ledger":
            output = ShadowLedgerReconciler(runtime).reconcile(
                args.ledger_path, args.dispatch_id
            )
        else:
            output = runtime.projection(args.table)
        print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except (RuntimeErrorBase, json.JSONDecodeError) as error:
        print(json.dumps({"error": type(error).__name__, "message": str(error)}))
        return 2
    finally:
        runtime.close()


if __name__ == "__main__":
    raise SystemExit(main())
