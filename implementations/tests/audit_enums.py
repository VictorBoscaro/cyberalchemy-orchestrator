"""Auditoria: valores fora dos enums do schema v0.6.0 nos ledgers reais.

Não é um teste de código — é uma sonda sobre os DADOS. O leitor é deliberadamente
leniente, então valor fora do enum passa silencioso; isto o torna visível.
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from server import config as config_module  # noqa: E402
from server import ledger  # noqa: E402

EXIT_REASONS = {"resolved", "loop_ceiling_reached", "dissent_irreconcilable", "user_abort", "error"}
DISPATCH_TYPES = {"research", "code", "review", "plan", "suggestion", "experiment"}
AGENT_ROLES = {"explorer", "synthesizer", "skeptic", "writer", "auditor"}
CONNECTION_TYPES = {"sequential", "zig-zag", "feedback"}


def main() -> int:
    cfg = config_module.load()
    exits: Counter[str] = Counter()
    types: Counter[str] = Counter()
    roles: Counter[str] = Counter()
    conns: Counter[str] = Counter()
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
                if dt not in DISPATCH_TYPES:
                    offenders.append(f"{repo.name}/{row['dispatch_id']}: dispatch_type={dt!r}")

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
                        if r not in AGENT_ROLES:
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
            mark = "  " if value in allowed else "<-- FORA DO ENUM"
            print(f"  {str(value):<28} {n:>5}  {mark}")

    show("dispatch_type", types, DISPATCH_TYPES)
    show("exit_reason", exits, EXIT_REASONS)
    show("role (agentes)", roles, AGENT_ROLES)
    show("connections.type", conns, CONNECTION_TYPES)

    print(f"\n{len(offenders)} ocorrência(s) fora do enum")
    for o in offenders[:20]:
        print(f"  {o}")
    if len(offenders) > 20:
        print(f"  … e mais {len(offenders) - 20}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
