# Project decisions

## Implementation Baseline Interview

This section records already-accepted repository decisions for the
`agents-communication-infra` brownfield runtime. No new option was selected during the
2026-07-26 Phase-A repair preflight.

| Decision | Selected baseline | Authority |
|---|---|---|
| Architecture pack | Use the current DomainSpec feature architecture and existing runtime package boundaries. No new `lib/architecture/` package is introduced. | `docs/features/agents-communication-infra/specs/architecture.md`; `docs/features/agents-communication-infra/IMPLEMENTATION-LAYERING.md` |
| Persistent storage | Required for journal, artifacts, attempts, receipts, effects and restart evidence. | `docs/features/agents-communication-infra/specs/persistence-and-replay.md` |
| Database engine | SQLite in WAL mode with `synchronous=FULL` for the proof and local pilot. | `docs/features/agents-communication-infra/specs/persistence-and-replay.md` |
| Data access boundary | Existing native Python `sqlite3` boundary owned by `implementations/server/runtime/database.py`; no ORM or alternate database library is introduced by the Phase-A repair. | `implementations/server/runtime/database.py`; `docs/features/agents-communication-infra/specs/architecture.md` |

These decisions remain feature-scoped. A production/distributed database, alternate architecture
pack or ORM requires a separate decision gate and cannot be inferred from this baseline.

