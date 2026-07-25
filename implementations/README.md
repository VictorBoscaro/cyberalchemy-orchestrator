# implementations — dispatch control plane

**Phase 1: the reader.** A FastAPI server that reads, live, the pending sheets
(pre-confirm) and the dispatch history from the append-only ledgers scattered
across the repos. Ten UI variants over the same API.

> **Read-only.** Nothing here writes to the ledger — that belongs to the
> appender of the `register-dispatch` skill. The "Dispatch" button exists in
> every UI, but it's `disabled`: turning it on is Phase 2.

## Stage-B runtime core

`server/runtime/` contains the descriptor-bounded
`SWU-ACI-APT-VS-001` local runtime: SQLite command groups, immutable
artifacts, exact profile imports, opaque capabilities, strict legacy snapshots,
session/dispatch linking and the candidate-to-official reference-probe path.

Here `reference-probe` names the frozen v1 lineage/profile compatibility surface. Stage G adds a
distinct authoritative `ReferenceScoutTool`/`ScoutRun` lifecycle that reuses that registered
profile and the existing bus without renaming the Stage-B identifiers. The general
`ProbeTool`/`ProbeRun` observational capability and generic provider launcher remain deferred.

Production serving remains disabled. A loopback-only Stage-C local pilot is
available when the explicit opt-in, dedicated database, exact ledger, pinned
receipts/source manifest, profiles, journal, and projection gates all pass.
The production reader still mounts the intent routes behind a closed gate.

Trusted, non-serving commands use:

```sh
python -m server.runtime migrate
python -m server.runtime register-profiles
python -m server.runtime verify-store
python -m server.runtime show-orchestration-log --dispatch-id ID --database DB --repo-root ROOT --ledger LEDGER
```

## Run

```sh
pip install -r requirements.txt
cd implementations
python -m server.main
# http://127.0.0.1:8765
```

The root serves the selection hub for the ten variants.

## Why it exists

The ledger is only written **after** the human confirm (the `register-dispatch`
skill is explicit: *"Only after the human's explicit confirm of the sheet"*). So a
UI that only reads the ledger **always arrives late** — it shows what has
already been dispatched and can never *be* the gate.

The missing piece is a **pre-confirm** artifact. Hence
`telemetry/agents/pending/<dispatch_id>.json`: the sheet the human reviews
before confirming. It is the only editable surface; the ledger remains
append-only and untouched.

## Structure

| Path | What |
|---|---|
| `server/ledger.py` | Ledger reader. Structural parsing, lenient, never writes. |
| `server/config.py` | Which repos to watch (auto-discovery by default). |
| `server/main.py` | FastAPI: `/api/snapshot`, `/api/stream` (SSE), `/api/dispatch/{repo}/{id}`, `/api/overview` (aggregates across all repos + attention queues), `/api/repo/{name}` (drill-down: full history `slim` + `summary` + `series`, with `?state=`/`?type=` filters). Full shapes in `UI-CONTRACT.md`. |
| `static/index.html` | Variant selection hub. |
| `static/ui/<slug>/` | One UI variant, self-contained in a single file. |
| `UI-CONTRACT.md` | Normative contract for the UIs: API, data shape, testids. |
| `tests/test_ledger.py` | Parser tests + smoke test against the real ledgers. |
| `tests/test_ui.py` | Playwright: the same contract against the ten variants. |

## Configuration

Without `config.json`, the server **auto-discovers**: it scans the repo's
parent directory for any folder with `telemetry/agents/`. To pin the list,
copy `config.example.json` to `config.json`.

## Two decisions the real data forced

**1. The reader is lenient; the appender is strict.** The appender refuses to
write to a corrupted ledger — it *protects* the file. The reader has the
opposite job: show what exists. The `domainspec` ledger contains old
prettified rows (multi-line JSON, trailing commas) that the appender would
reject; in strict mode the reader returned **0** dispatches for that repo.
Leniently, it returns 55 and accumulates warnings. Losing the entire history
over one old row would be worse than displaying it.

**2. Calculated fields carry a `_` prefix — on objects with ROW SHAPE.** It's
not cosmetic: `status` is a **real** key of pre-v0.5.2 rows, and on an object
that shares the namespace of a ledger row, a calculated field with that name
would overwrite the historical data — a bug the `historical key 'status'
preserved` test locks down. The rule is scoped to rows/sheets: aggregate
objects that aren't rows (`summary`, `series`, `totals`) have no ledger
namespace to protect and deliberately return unprefixed keys (`total`, `open`,
`by_type`, ...).

## Tests

```sh
python implementations/tests/test_ledger.py      # parser + smoke test against the real ledgers
python implementations/tests/test_ui.py          # Playwright across the ten variants
python implementations/tests/test_ui.py terminal # just one
```

Screenshots land in `tests/screenshots/`.

## Fixture

`telemetry/agents/pending/2026-07-19-example-ui-control-plane.json` is a
**demo** sheet (marked with `"_example": true`), not a real dispatch. It
exists so the UIs have something to render. Delete it once the real flow is up.

## Next phases

- **Phase 2 — the button.** `POST /confirm` records the confirm; Claude,
  waiting via `Monitor`, follows the normal chain (`check-tension` →
  `register-dispatch` → agents → close row). The one dispatching remains
  Claude in the session, which preserves context and the skill chain.
- **Phase 3 — editing** the pending sheet before confirm.
