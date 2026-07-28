# implementations — local control plane and governed runtime

This subtree contains four related implementation zones:

1. A FastAPI dispatch reader and human-gate UI over pending sheets and
   append-only dispatch ledgers.
2. A descriptor-bounded ACI/APT runtime with durable SQLite command handling,
   host hooks, reference delivery, and operator recovery.
3. A read-oriented Skill Control Center that combines skill-graph, dispatch,
   path, and evidence views.
4. An isolated experimental shadow runtime under `agent-runtime/`.

These zones share one repository subtree, but they do not share the same
authority or maturity boundary. The dispatch reader is **read-only against the
append-only ledger**. Its `POST /api/confirm` endpoint writes only a
`<sheet>.confirmed` marker beside a pending sheet. The validated appender used
by `register-dispatch` remains the only ledger writer.

The Linear dispatch UI enables marker confirmation for a valid, unconfirmed
pending sheet. The other nine variants still render disabled Dispatch buttons.
The marker endpoint and Linear client are implemented and tested, but the
external orchestrator reaction remains separate work.

## Vocabulary

- **ACI** — the agents-communication-infrastructure runtime: command, event,
  capability, delivery, and recovery mechanics under the repository-root
  [`docs/features/agents-communication-infra/`](../docs/features/agents-communication-infra/).
- **APT** — Agent Provenance Telemetry: session, dispatch, research, lineage,
  and evidence projections under the repository-root
  [`docs/features/agent-provenance-telemetry/`](../docs/features/agent-provenance-telemetry/).
- **SWU / Stage identifiers** — bounded work-unit and rollout labels. They name
  the accepted implementation slice; they are not additional runtime services.
- **Projection** — a rebuildable query view derived from authoritative journal
  events.

## Prerequisites

Python 3.11 or newer is required. From the repository root, install the runtime
dependencies before invoking either the reader or governed runtime:

```sh
pip install -r implementations/requirements.txt
```

Browser tests additionally require:

```sh
pip install -r implementations/requirements-dev.txt
playwright install chromium
```

## Implementation map

| Zone | Main paths | Implemented boundary |
|---|---|---|
| Dispatch reader and gate | `server/main.py`, `server/config.py`, `server/ledger.py`, `static/ui/` | Repo discovery, lenient historical parsing, cached read models, snapshot/overview/drill-down APIs, SSE, pending confirmation markers, ten offline UI variants. |
| Governed ACI/APT runtime | `server/runtime/`, `server/runtime/migrations/` | Canonicalization, 11 migrations, immutable artifacts, hash-chained journal, projections, exact profiles, opaque capabilities, runtime APIs, host hooks, orchestration bridge, reference/reveal delivery, local-pilot gates, backup and retirement. |
| Skill Control Center | `server/control_center/`, `static/control-center/`, `fixtures/skill-control-center/` | Six fail-closed API routes, skill and dispatch sources, deterministic path queries, evidence overlays, preview-only local state, and browser UI. |
| Experimental shadow runtime | `agent-runtime/` | Independent SQLite journal/projections for sessions, Reference Scout, Observation Probe, replay, receipts, CLI, and read/compare-only YAML reconciliation. |

The process composition root is `server/main.py`. It serves the reader and
static interfaces, binds all six Control Center routes only when the complete
interface identity is configured, and mounts the governed runtime intent routes
behind a closed production gate.

## Governed runtime boundary

`server/runtime/` contains the descriptor-bounded `SWU-ACI-APT-VS-001` local
runtime. Accepted commands use SQLite command groups, immutable artifacts,
exact profile imports, opaque capabilities, strict legacy snapshots,
session/dispatch linking, Reference Scout ingestion and delivery, bus reveal
delivery, and candidate-to-official reference-probe lineage.

Here `reference-probe` names the frozen v1 lineage/profile compatibility
surface. The authoritative `ReferenceScoutTool`/`ScoutRun` lifecycle reuses
that registered profile and the existing bus without renaming the Stage-B
identifiers.

Production serving remains disabled. The production reader mounts runtime
intent routes with a closed gate. A loopback-only local pilot is available only
when explicit opt-in, a dedicated database, the exact ledger, pinned receipts
and source manifest, registered profiles, journal integrity, and projection
gates all pass.

From the repository root, trusted non-serving commands include:

```sh
python -m implementations.server.runtime migrate
python -m implementations.server.runtime register-profiles
python -m implementations.server.runtime verify-store
python -m implementations.server.runtime show-orchestration-log --dispatch-id ID --database DB --repo-root ROOT --ledger LEDGER
```

The module intentionally derives its default repository, database, and ledger
paths from the current working directory, so run these forms from the
repository root. Use explicit `--repo-root`, `--database`, and `--ledger`
arguments where the subcommand provides them.

### Loopback local pilot and recovery

The local pilot is an explicit operator path, not a production-server switch.
From the repository root in PowerShell:

```powershell
$repoRoot = (Resolve-Path -LiteralPath ".").Path
$pilotDb = Join-Path $repoRoot "telemetry/runtime/local-pilot.sqlite3"
$ledger = Join-Path $repoRoot "telemetry/agents/subagents-dispatch.yaml"
$env:ACI_REPO_ROOT = $repoRoot
$env:ACI_LOCAL_PILOT_ENABLED = "1"
python -m implementations.server.runtime serve --local-pilot --host 127.0.0.1 --port 8766 --database $pilotDb --ledger $ledger
# After the pilot stops:
Remove-Item Env:ACI_LOCAL_PILOT_ENABLED
Remove-Item Env:ACI_REPO_ROOT
```

Preflight refuses the shared default database, a non-loopback host, a missing
or wrong-path ledger, a UTF-8-BOM-prefixed ledger, missing or drifted
Stage-B/Stage-C receipts and source manifest, profile drift, journal failure,
or projection lag.

After stopping the pilot, verification, online backup, and recoverable
retirement are separate explicit operations:

```powershell
$backup = Join-Path $repoRoot "telemetry/runtime/backups/local-pilot.sqlite3"
$retired = Join-Path $repoRoot "telemetry/runtime/retired/local-pilot.sqlite3"
python -m implementations.server.runtime verify-local-pilot-database --database $pilotDb --repo-root $repoRoot
python -m implementations.server.runtime backup-local-pilot-database --source $pilotDb --destination $backup --repo-root $repoRoot
python -m implementations.server.runtime retire-local-pilot-database --source $pilotDb --destination $retired --verified-backup $backup --repo-root $repoRoot --confirmed-stopped
```

Backup and retirement destinations must not already exist. Retirement moves
the stopped database to a recovery location; it does not delete the bytes.

## Run the dispatch reader

```sh
cd implementations
pip install -r requirements.txt
python -m server.main
# http://127.0.0.1:8765
```

`cd` first: `requirements.txt` lives in `implementations/`, not at the repo root.
On startup the server prints `observing N repos:`. The root URL serves the
selection hub for the ten dispatch variants. The static Control Center selector
is always available at `/static/control-center/index.html`, with candidate
shells at `a/index.html`, `b/index.html`, and `c/index.html` below that path.
Its six `/v1/control-center/*` API routes are published only when the complete
three-part interface identity is configured.

For the Playwright suite (`tests/test_ui.py`), also install the dev extras:

```sh
pip install -r requirements-dev.txt
playwright install chromium
```

## Why the reader and pending gate exist

On the confirm-gated path the ledger is written **after** the human confirm (the
`register-dispatch` skill is explicit: *"Only after the human's explicit confirm
of the sheet"*). Host-managed launches use the shared dispatch lifecycle bridge:
Claude registers it through `.claude/settings.json`, while Codex registers
`spawn_agent` and `followup_task` through `.codex/hooks.json`. The pre-launch
path validates the YAML append and ACI lifecycle record and must return a
`launch-authorized` receipt before an agent starts. The bridge appends the
opening during the pre-launch hook immediately before it returns authorization.
A UI that only reads the ledger is outside that authorization path and therefore
cannot itself be the pre-launch gate.

The pre-confirm artifact is
`telemetry/agents/pending/<dispatch_id>.json`: the sheet the human reviews
before confirming. Confirmation creates a sibling marker; it does not append a
dispatch row or launch an agent. Those effects remain owned by the external
orchestrator and validated appender chain.

## Structure

| Path | What |
|---|---|
| `server/ledger.py` | Ledger reader. Structural parsing, lenient, never writes. |
| `server/config.py` | Which repos to watch (auto-discovery by default). |
| `server/main.py` | FastAPI: `/api/snapshot`, `/api/stream` (SSE), `/api/dispatch/{repo}/{id}`, `/api/overview` (aggregates across all repos + attention queues), `/api/repo/{name}` (drill-down: full history `slim` + `summary` + `series`, with `?state=`/`?type=` filters). Full shapes in `UI-CONTRACT.md`. |
| `server/runtime/` | Governed ACI/APT runtime, APIs, hooks, orchestration bridge, delivery, local-pilot preflight, and operator recovery. |
| `server/control_center/` | Presentation-neutral Control Center sources, service, path engine, evidence provider, preview store, and six-route API. |
| `static/index.html` | Variant selection hub. |
| `static/ui/<slug>/` | One UI variant, self-contained in a single file. |
| `static/control-center/` | Shared Control Center frontend plus three interface shells. |
| `agent-runtime/` | Experimental, separately packaged shadow runtime; not the production composition root. |
| `fixtures/skill-control-center/` | Frozen Control Center fixtures and manifest digests. |
| `UI-CONTRACT.md` | Shared reader/data/testid baseline for the dispatch UIs. Its disabled-button activation clause is stale for the Linear marker-confirmation exception. |
| `tests/test_ledger.py` | Parser tests + smoke test against the real ledgers. |
| `tests/test_ui.py` | Playwright: the shared contract across ten variants, plus the Linear confirmation exception. |
| `tests/runtime/` | Governed runtime, hooks, delivery, recovery, and local-pilot tests. |
| `tests/control_center/` | Control Center API, binding, evidence, path, fixture, and browser tests. |

## Configuration

Without `config.json`, the server **auto-discovers**: it scans the repo's parent
directory for any sibling folder that holds **either** a
`telemetry/agents/subagents-dispatch.yaml` file **or** a `telemetry/agents/pending/`
directory (`server/config.py`, `_scan_repos`). A folder with an empty
`telemetry/agents/` does not qualify.

To override, copy `config.example.json` to `config.json`. Copied as-is it keeps
auto-discovery and only overrides the tuning knobs; the `scan_roots` and `repos`
examples are inert (`_example_` prefixed) precisely because absolute paths from
another machine would resolve to **zero** repos with no error. Uncomment them by
renaming to `scan_roots` / `repos` and put in paths that exist on this machine.

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

## Tests and working directories

```sh
# From the repository root: governed runtime imports use implementations.*
python -m unittest discover -s implementations/tests/runtime -t . -v

# From implementations/: reader/API scripts
python tests/test_ledger.py
python tests/test_main.py

# From implementations/: Control Center API and browser suite
python -m unittest discover -s tests/control_center -v
```

Before running the dispatch Playwright suite, keep
`python -m server.main` running from `implementations/` in a separate terminal.
Then run:

```sh
python tests/test_ui.py
python tests/test_ui.py terminal
```

The dispatch and Control Center browser suites require the Playwright
prerequisites described above. Dispatch UI screenshots land in
`tests/screenshots/`; Control Center browser evidence lands in the
repository-root
`output/playwright/ux-validator/skill-control-center-phase1/`.

For the isolated shadow runtime, from `implementations/` in PowerShell:

```powershell
$env:PYTHONPATH = (Resolve-Path -LiteralPath "agent-runtime").Path
python -m unittest discover -s agent-runtime/tests -v
```

Or in a POSIX shell:

```sh
PYTHONPATH="$(pwd)/agent-runtime" python -m unittest discover -s agent-runtime/tests -v
```

## Fixture

The repository-root-relative
`telemetry/agents/pending/2026-07-19-example-ui-control-plane.json` is a
**demo** sheet (marked with `"_example": true`), not a real dispatch. It
exists so the UIs have something to render. Delete it once the real flow is up.

## Current gates and deferred work

- **Dispatch activation:** `POST /api/confirm` and its Linear client exist; the
  other nine UI buttons remain disabled, and the external watcher/dispatch chain
  is not owned here.
- **Pending-sheet editing:** the reader exposes sheets but does not provide the
  editing workflow.
- **Production runtime serving:** runtime intent routes remain closed in the
  production reader; only the explicitly gated loopback local pilot can serve
  them.
- **Control Center authority:** its local store is preview-only and cannot apply
  authoritative lifecycle changes.
- **Shadow-runtime convergence:** `agent-runtime/` does not replace
  `server/runtime/`; no cutover or retirement decision is encoded here.

## Validation snapshot

Observed on 2026-07-26 against the then-current dirty working tree:

- Governed runtime: 103 tests passed.
- Dispatch reader/API scripts: passed, including live ledger smoke coverage.
- Experimental shadow runtime: 31 tests passed.
- Control Center: two semantic expectation failures
  (`partial`/`truncated` observed where tests expected `complete`/`success`) and
  one Playwright timeout waiting for `invalid-endpoint`; the remaining 32 tests
  in that run passed.

This dated snapshot records observed evidence, not a standing guarantee. Re-run
the commands above after changing fixtures, implementation, or source graphs.
