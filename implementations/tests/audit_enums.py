"""Audit: values outside the current v0.6.1 schema enums in real ledgers.

Not a code test — it's a probe over the DATA. The reader is deliberately lenient,
so a value outside the enum passes silently; this makes it visible.
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from server import config as config_module  # noqa: E402
from server import ledger  # noqa: E402
from server.runtime.agent_roles import load_accepted_role_registry  # noqa: E402
from server.runtime.dispatch_types import live_dispatch_type_values  # noqa: E402

EXIT_REASONS = {"resolved", "loop_ceiling_reached", "dissent_irreconcilable", "user_abort", "error"}
CONNECTION_TYPES = {"sequential", "zig-zag", "feedback"}
OUTPUT_MODES = {"inline", "persisted"}


def main() -> int:
    cfg = config_module.load()
    repo_root = Path(__file__).resolve().parents[2]
    agent_roles = set(load_accepted_role_registry(repo_root).roles)
    dispatch_types = live_dispatch_type_values(repo_root)
    exits: Counter[str] = Counter()
    types: Counter[str] = Counter()
    roles: Counter[str] = Counter()
    conns: Counter[str] = Counter()
    output_modes: Counter[str] = Counter()
    offenders: list[str] = []

    for repo in cfg.resolved_repos():
        path = repo / ledger.LEDGER_RELPATH
        if not path.is_file():
            continue
        parsed = ledger.parse_ledger(path.read_text(encoding="utf-8-sig"))
        for row in ledger.join_rows(parsed.rows):
            dt = row.get("dispatch_type")
            if dt is not None:
                types[dt] += 1
                if dt not in dispatch_types:
                    offenders.append(f"{repo.name}/{row['dispatch_id']}: dispatch_type={dt!r}")

            output_mode = row.get("output_mode")
            if output_mode is not None:
                output_modes[output_mode] += 1
                if output_mode not in OUTPUT_MODES:
                    offenders.append(f"{repo.name}/{row['dispatch_id']}: output_mode={output_mode!r}")

            close = row.get("_close")
            if close:
                er = close.get("exit_reason")
                exits[er] += 1
                if er not in EXIT_REASONS:
                    offenders.append(f"{repo.name}/{row['dispatch_id']}: exit_reason={er!r}")

            for group in row.get("groups") or []:
                if not isinstance(group, dict):
                    continue
                for agent in group.get("agents") or []:
                    if isinstance(agent, dict):
                        r = agent.get("role")
                        roles[r] += 1
                        if r not in agent_roles:
                            offenders.append(f"{repo.name}/{row['dispatch_id']}: role={r!r}")

            for conn in row.get("connections") or []:
                if isinstance(conn, dict):
                    t = conn.get("type")
                    conns[t] += 1
                    if t not in CONNECTION_TYPES:
                        offenders.append(f"{repo.name}/{row['dispatch_id']}: connection type={t!r}")

    def show(title: str, counter: Counter, allowed: set[str]) -> None:
        print(f"\n{title}")
        for value, n in counter.most_common():
            mark = "  " if value in allowed else "<-- OUTSIDE THE ENUM"
            print(f"  {str(value):<28} {n:>5}  {mark}")

    show("dispatch_type", types, dispatch_types)
    show("exit_reason", exits, EXIT_REASONS)
    show("role (agents)", roles, agent_roles)
    show("connections.type", conns, CONNECTION_TYPES)
    show("output_mode", output_modes, OUTPUT_MODES)

    print(f"\n{len(offenders)} occurrence(s) outside the enum")
    for o in offenders[:20]:
        print(f"  {o}")
    if len(offenders) > 20:
        print(f"  … and {len(offenders) - 20} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
