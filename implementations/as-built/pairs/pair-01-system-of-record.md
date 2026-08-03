# Pair 01 — System of record

Worker: Parnas, David
Reviewer: Brooks, Frederick P.
Finalizer: Parnas, David

## Executive answer

The repository contains a federation rather than one runtime or one physical store. The reader process serves YAML and pending-sheet views plus a read-only Control Center; its runtime HTTP routes are present but closed. A separate governed runtime CLI remains directly reachable for trusted mutations, while loopback HTTP serving requires local-pilot preflight. Existing receipts and a changing live SQLite journal establish local operation, not production promotion.

Authority is partitioned by fact class. The frozen corpus declares YAML authoritative for official dispatch opening and closing and declares the validated appender the intended sole physical writer. The governed SQLite journal owns accepted runtime facts and projections are derived. Because the writer source is outside the frozen manifest, writer implementation and deployed exclusivity are only partially proven. The independent `agent-runtime` package is implemented and tested but has no evidenced operational, authorized, or official cutover status.

## Entrypoint and ownership map

| Entrypoint | Component | Reads | Writes | Reachable state | Authority |
|---|---|---|---|---|---|
| `python -m server.main` from `implementations/` | Reader, static UI, Control Center | YAML ledgers, pending sheets, frozen/live skill graph sources | Pending-sheet `.confirmed` marker only; browser UI separately uses `localStorage` | Reader and six Control Center query routes are code-reachable when bindings are complete; runtime HTTP returns 503 | Reader/query authority only; Control Center is auxiliary |
| Reader-mounted `/api/runtime`, `/api/provenance`, `/api/health` | Governed runtime intent APIs | Would use runtime SQLite and strict YAML snapshots | None while closed | Present but always disabled in this composition | No production serving authority |
| `python -m implementations.server.runtime serve --local-pilot ...` | Loopback local pilot | Exact YAML ledger, pinned receipts/source manifest, dedicated SQLite | Dedicated SQLite journal, artifacts, projections, capabilities | Reachable only after explicit preflight | Accepted local-pilot authority; not production promotion |
| Other `python -m implementations.server.runtime` subcommands | Trusted runtime CLI | Environment/default or explicit runtime paths | Migrations, profiles, capabilities, probe activation; recovery commands as selected | Directly reachable without serve opt-in | Command-specific authority boundary is only partially explicit |
| Host hook launchers under `.claude/hooks/` and `.codex/hooks.json` | Governed host workflow bridge | Host event payload, YAML ledger, pilot SQLite | YAML through the declared validated writer boundary; runtime events/receipts | Configured in repository; universal host enforcement is outside this pair | Operational local evidence, not universal adoption proof |
| `agent-runtime` console script or `python -m agent_runtime` | Experimental shadow runtime | Explicit independent SQLite and read-only YAML snapshot | Independent SQLite only | Independently executable and tested; no production imports found | Experimental; no official cutover authority |

## Atomic claims

### P01-C01 — Reader and Control Center

`implementations.server.main` is the reader HTTP composition root. It reads ledgers and pending sheets, writes only confirmation markers, and conditionally publishes six Control Center query routes. The reachable backend Control Center is read-only. `LocalControlCenterStore` is constructed at `implementations/server/control_center/service.py:93-99` but bounded search found no service/API call to it; browser-local state is implemented in `implementations/static/control-center/app.js:24-25,170,273,290`.

Status: implementation yes; proof yes; operation unknown; authority partial; official adoption partial; reconstructibility partial.

### P01-C02 — Governed runtime

The governed runtime is a separate executable composition. Reader-mounted HTTP is closed (`implementations/server/main.py:41-76`; `implementations/server/runtime/api.py:41-57,384-402,616-632`), and pilot serving is preflight-gated (`implementations/server/runtime/local_pilot.py:139-220`). Trusted non-serving CLI mutations remain reachable because `implementations/server/runtime/cli.py:148-172` opens the runtime and dispatches mutating commands without the serve opt-in.

Operational status is local and time-qualified. `telemetry/runtime/local-pilot/last-wrapper-log.json:2-23,79-136` records durable linked YAML/runtime events. A read-only sample at `2026-07-31T18:21:45.6941655Z` observed 1,029 events and maximum offset 1,029, but totals moved during the investigation and are not snapshot-stable.

Status: implementation yes; proof yes; operation yes; authority partial; official adoption partial; reconstructibility partial.

### P01-C03 — Source of record

The authorized model is disjoint authority, not one store. `docs/features/agents-communication-infra/work-pack/shared/context.md:13-19,52-55` assigns official opening/closing to YAML and accepted workflow facts to the journal. `docs/features/agents-communication-infra/specs/SPEC.md:21,137` declares the validated appender the intended sole YAML writer. That is authority evidence, not complete implementation proof: `.claude/skills/register-dispatch/append-dispatch.cjs` is outside the frozen source manifest, and no deployed writer inventory or negative bypass proof was run.

Status: implementation partial; proof partial; operation partial; authority yes; official adoption yes; reconstructibility partial.

### P01-C04 — Experimental agent-runtime

`implementations/agent-runtime` is independently packaged and supplies its own CLI, SQLite journal, receipts, projections, replay, and read/compare-only YAML reconciler. Its isolated suite passed 31 tests. No production implementation import, operational receipt, authority decision, or cutover evidence was found.

Status: implementation yes; proof yes; operation unknown; authority no; official adoption no; reconstructibility yes.

## Gaps and smallest next actions

| Gap | Smallest next action | What it buys | Completion evidence |
|---|---|---|---|
| Sole-writer declaration exceeds frozen implementation proof | Add the exact appender source/digest to a refreshed manifest; run writer inventory and negative direct-write test | Executable and deployment-level exclusivity proof | Manifest digest, complete inventory, passing bypass test with unchanged ledger |
| Backend `LocalControlCenterStore` is unreachable | Explicitly retain and connect it with a route-level test, or remove it from composition | Eliminates dead state or makes its auxiliary role observable | Accepted decision plus reachability test or removal diff |
| CLI mutation authority is not explicit per command | Publish and test a CLI authority matrix covering store targets and denied defaults | Distinguishes reachable code from authorized mutation | Accepted matrix and positive/negative tests for each mutating command |
| Live operational counts move | Capture a verified backup or journal-head receipt with UTC time, digest, offset, and verification | Reproducible operational baseline | Digest-bound snapshot whose counts reproduce |
| `agent-runtime` has no lifecycle disposition | Decide test-oracle retention, mine-and-retire, or governed convergence | One named runtime boundary and owner | Accepted decision with permitted uses, prohibited claims, and terminal evidence |

## Document drift

- `implementations/README.md:62-65` calls `server/main.py` “the process composition root”; that is accurate only for the reader HTTP process.
- `implementations/README.md:59` does not expose that composed backend local state is unreachable while actual UI mutations use browser `localStorage`.
- “The governed runtime is gated” is overbroad: production HTTP and pilot serving are gated, but trusted CLI mutation is reachable.
- “The validated appender is the proven sole writer” exceeds the frozen corpus; the evidence establishes intended authority, not implementation or deployed exclusivity.

## Robot-talk history

Round 1 contested four boundaries: frozen-corpus writer proof, Control Center store reachability, HTTP gating versus CLI reachability, and unstable live counts. Parnas conceded or narrowed each claim; Brooks accepted the corrections. No material disagreement remains.

## Commands and evidence

- The first 18-test attempt passed but failed to establish the requested isolated directory; it is excluded as proof.
- After creating `C:\tmp\cyberalchemy-as-built\pair-01-system-of-record`, the targeted reader, Control Center, and Stage-C selection passed 18 tests in 3.504 seconds.
- From `implementations/agent-runtime`, `python -m unittest discover -s tests -v` passed 31 tests in 6.335 seconds.
- A SQLite URI `mode=ro` query observed 1,029 events and maximum offset 1,029 at `2026-07-31T18:21:45.6941655Z`; it made no writes.
- Manifest membership inspection confirmed the three cited authority documents are frozen and `append-dispatch.cjs` is not.

## Snapshot

- Commit: `63777abd838995c8512bcea806546c3f2ab6add6`
- Source manifest SHA-256: `af35da963497918340ca7c74fa1a9e7a27d1a7027420e6edb517e55fd903cd11`
- The worktree was dirty before this pair. This pair changed only its authorized JSON and Markdown outputs.

## Disposition question

Should `implementations/agent-runtime` be retained as a historical/test oracle, mined for missing capabilities and retired, or assigned a governed convergence plan into `server/runtime`? Until that decision exists, it remains outside the official system boundary.
