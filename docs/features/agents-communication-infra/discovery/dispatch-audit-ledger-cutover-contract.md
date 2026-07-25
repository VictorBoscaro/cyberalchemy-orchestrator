---
feature: agents-communication-infra
artifact: dispatch-audit-ledger-cutover-contract
status: proposed
version: 0.1.0
created: 2026-07-24
last_updated: 2026-07-24
runtimeGate: contract-only
productionCutoverGate: block
---

# Dispatch audit-ledger cutover contract

## Decision

The current migration does **not** stop recording dispatches in
`telemetry/agents/subagents-dispatch.yaml`.

It stops clients, skills, watchers and runtime components from writing that file independently.
For a `runtime-managed` dispatch, SQLite owns accepted workflow facts and durable effect intent; the
audit materializer derives the official opening and close rows and invokes
`.claude/skills/register-dispatch/append-dispatch.cjs`, which remains the sole physical YAML writer.
This is dual recording across stores, not dual authority.

Stopping all YAML writes is a separate store-retirement decision. It is neither implied by runtime
cutover nor authorized by the current work pack.

## Evidence and current boundary

| Evidence | Consequence |
|---|---|
| `work-pack/shared/context.md` assigns the journal accepted workflow intent and assigns official opening/closing to the audit ledger. | SQLite and YAML have disjoint authority during migration. |
| `specs/workflows.md` `AuditLedgerMaterializer` requires exact-row reconciliation and permits only the validated appender to write YAML. | A runtime worker or reconciler must never open the ledger for write. |
| `specs/workflows.md` `ExecutionAuthorityCutoverWorkflow` makes `runtime-managed` versus `legacy-managed` immutable at confirmation and forbids dual execution. | The two paths may coexist for different dispatches, never for the same dispatch. |
| `specs/operations.md` requires `audit_opening.verified` before execution and `audit_close.verified` before `closed`. | YAML is still an execution/closure barrier in the present target architecture. |
| `implementations/agent-runtime/agent_runtime/ledger_shadow.py` is read/compare-only. | The current SQLite pilot is not a materializer and does not authorize cutover. |
| `ADR-002-compatibility-terminal-snapshot-and-local-probe.md` keeps historical rows immutable and requires target-host process, ACL, inventory and bypass evidence before cutover. | Passing local journal/projection tests alone cannot enable YAML mutation or retirement. |

## Authority matrix

| Concern | `legacy-managed` dispatch | `runtime-managed` dispatch |
|---|---|---|
| Pre-confirmation routing | legacy/session path | ACI command boundary |
| Workflow authority | legacy/session chain | accepted SQLite journal facts |
| YAML opening/close request | legacy/session path | durable SQLite effect intent |
| Physical YAML writer | validated appender only | the same validated appender, invoked by materializer |
| Execution release | existing legacy protocol | journaled exact opening verification |
| Official close | validated close row | journaled exact close verification |
| Projection/read UI | lenient historical reader | runtime projection plus compatible audit-ledger view |

No row, marker, projection or successful subprocess exit may substitute for the authority assigned in
this table.

## Cutover states

### C0 — current shadow/local-pilot state

- The legacy path may invoke the validated appender.
- SQLite may link to and compare a pinned ledger snapshot.
- SQLite does not write or acknowledge YAML effects.
- Production, provider execution, materialization and authority cutover remain blocked.

### C1 — materializer-enabled compatibility

C1 may begin only when TASK-020 passes with the complete target-host
`SoleWriterEvidenceBundle`.

- A `runtime-managed` confirmation atomically appends `run.created`,
  `audit_opening.requested`, its effect intent and a stable receipt in SQLite.
- The materializer claims that intent, derives the complete canonical v0.6.1 opening row from frozen
  authority, reads the ledger, and classifies it as `absent`, `identical` or `divergent`.
- `absent` invokes the validated appender and then requires an independent exact re-read.
- `identical` records verified acknowledgement without another append.
- `divergent`, malformed, duplicate-identity or unknown observations fail closed as
  `reconciliation_required`.
- The same rules apply to the close row after the unique run terminal fact.
- The legacy watcher is disabled and evidence-bound for each runtime cutover epoch. It may not act
  on runtime-managed identities.

This stage writes both SQLite and YAML, but only SQLite accepts workflow facts and only the appender
writes the YAML audit record.

### C2 — client authority cutover

C2 moves skills, UI and API defaults to `runtime-managed`.

- New confirmed dispatches enter ACI; they still receive YAML opening and close rows through C1.
- `legacy-managed` remains an explicit rollback route for not-yet-confirmed proposals only.
- A dispatch accepted as `runtime-managed` never falls back into legacy execution.
- A pre-cutover legacy dispatch remains legacy-owned through its close.

C2 stops direct legacy initiation for new default-path dispatches; it does **not** stop YAML writes.

### C3 — optional YAML retirement

YAML writes may stop only after a new ADR and work-pack unit explicitly promote C3. At minimum, that
promotion must prove:

1. no execution, authorization, close, UI, reporting, skill or external consumer depends on a new
   YAML row;
2. a durable high-level audit projection with an owned schema replaces every required opening/close
   field and preserves stable `dispatch_id` lookup;
3. all accepted runtime effect intents are drained or formally migrated, with no `pending`,
   `unknown` or `reconciliation_required` ledger effects;
4. every legacy-open dispatch is closed by its original owner or is explicitly tombstoned by an
   approved historical disposition;
5. historical YAML bytes are preserved read-only with a file digest, backup/restore proof and a
   documented retention policy;
6. deployment inventory, filesystem permissions and negative bypass tests prove that no process can
   append after the retirement epoch;
7. the lenient reader and every user-facing query pass compatibility tests against the replacement
   projection;
8. rollback restores query availability without inventing, rewriting or backfilling official facts.

C3 changes the current product/audit contract. It cannot be activated by a feature flag intended
only for C1 or C2.

## Sole-writer and no-dual-owner rules

1. `append-dispatch.cjs` is the only sanctioned process boundary that may mutate the YAML file.
2. Materializers pass a candidate record to the appender; they receive no direct file-write
   capability.
3. Reconcilers and readers are read-only. They never repair, append, truncate or normalize history.
4. One `dispatch_id` has one immutable execution-authority mode.
5. A compatibility marker is transport/projection only and cannot authorize a runtime-managed run.
6. The legacy watcher and runtime worker must not be active owners of the same identity or cutover
   epoch. Overlap blocks startup and cutover.
7. Cross-store success requires a journal acknowledgement containing the observed canonical row
   digest. Appender exit code or identity-only deduplication is insufficient.
8. Replay reads persisted facts only; it does not invoke the appender or materializer.

## Historical handling

- Existing YAML rows remain byte-preserved, append-only historical artifacts.
- Pre-v0.6.1 rows are displayed leniently but are not revalidated under the current schema.
- Historical rows are not imported as runtime commands, `ConfirmedDispatch` entities or `Run`
  authority.
- Optional search/index projections must retain source repository, source path, schema/version when
  known, raw-row artifact reference and digest. Normalized fields must be labeled derived.
- A legacy dispatch open at the C1/C2 epoch closes through the legacy path and validated appender.
  Runtime may observe it but must not adopt it.
- A runtime-managed dispatch writes both rows through materializer intents even if client cutover
  occurs between opening and closing.
- Orphan closes, duplicate identities, malformed rows and divergent exact content are surfaced for
  operator disposition; they are never silently repaired.

## Crash recovery and rollback

### Cross-store recovery

| Crash point | Required recovery |
|---|---|
| before effect claim | reclaim the durable pending intent |
| after claim, before appender call | read/compare, then append only if absent |
| after YAML append, before journal acknowledgement | exact re-read; identical becomes verified without duplicate append |
| after appender error or unreadable re-read | retain pending/unknown; do not release execution or `closed` |
| same identity with different content | enter `reconciliation_required`; require explicit operator repair |

Accepted journal facts are never rolled back to conceal a failed cross-store effect.

### Authority rollback

- Rollback changes the default for future, not-yet-confirmed proposals to `legacy-managed`.
- It first disables new runtime confirmation and proves no proposal is crossing the boundary.
- Already accepted runtime-managed runs remain runtime-owned and continue reconciliation to a
  truthful terminal state.
- Partial runtime state is never translated into a legacy success or appended again by a legacy
  watcher.
- Rollback evidence records epoch, configuration digest, watcher/runtime process identities,
  outstanding effect counts and the exact dispatch identities retained by each owner.

After C3 retirement, rollback means restoring read/query service from preserved history or deploying
a new explicitly versioned audit sink. It does not authorize appending retroactive YAML rows unless
a separate recovery decision reopens that store and assigns one validated writer.

## Required logs and receipts

The cutover implementation must emit durable structured evidence, with sensitive payloads referenced
by digest rather than logged inline:

| Record | Minimum fields |
|---|---|
| `cutover.preflight` | epoch, mode, config digest, journal head, ledger file digest, writer process identity, ACL digest, deployed writer inventory digest, watcher-disable evidence digest |
| `ledger.materialization` | effect ID, run ID, dispatch ID, row kind, expected canonical digest, observed classification, observed digest if any, appender invocation ID, attempt, result |
| `ledger.verified` | effect ID, dispatch ID, row kind, canonical digest, post-read ledger file digest, acknowledgement event ID/offset |
| `ledger.divergence` | effect ID, identity, row kind, expected digest, observed digest, classification, repair-ticket reference |
| `cutover.authority_conflict` | epoch, dispatch ID if known, legacy owner identity, runtime owner identity, blocked action |
| `cutover.rollback` | from/to mode, epoch, outstanding effects by state, retained runtime identities digest, legacy identities digest, operator decision reference |
| `ledger.retirement` | retirement epoch, final file digest, backup artifact/digest, last opening/close identities, consumer inventory digest, permission-denial evidence |

Logs are diagnostic evidence, not acknowledgement. Only accepted journal events and exact store reads
advance runtime state.

## Acceptance tests

### C1/C2 mandatory tests

The implementation must pass the existing named plan
`adrs/fixtures/SWU-ACI-002-SOLE-WRITER-TEST-PLAN.md` (`T-ACI-WRITER-001..005` and
`T-ACI-LEGACY-001..006`) plus:

| ID | Test | Required result |
|---|---|---|
| `T-ACI-CUTOVER-001` | runtime confirmation and legacy watcher race for one ID | one owner wins before confirmation; overlap fails closed; no provider start |
| `T-ACI-CUTOVER-002` | crash after opening append and before acknowledgement | one opening row; recovery records exact verification |
| `T-ACI-CUTOVER-003` | same opening identity with divergent content | `reconciliation_required`; adapter start count remains zero |
| `T-ACI-CUTOVER-004` | crash after close append and before acknowledgement | one close row; recovery reaches `closed` only after exact verification |
| `T-ACI-CUTOVER-005` | rollback with an accepted runtime run and an unconfirmed proposal | accepted run remains runtime-owned; proposal routes legacy; no identity crosses owners |
| `T-ACI-CUTOVER-006` | journal replay with pending materialization | no appender/provider/tool invocation during replay |
| `T-ACI-CUTOVER-007` | pre-cutover legacy dispatch closes after default switches to runtime | legacy owner writes one validated close; runtime records no run authority for it |
| `T-ACI-CUTOVER-008` | runtime-managed dispatch spans rollback | runtime materializer completes its audit rows; legacy watcher remains barred |
| `T-ACI-CUTOVER-009` | malformed or duplicate YAML identity | strict authorization fails; lenient display does not unlock execution |
| `T-ACI-CUTOVER-010` | direct runtime file-write attempt | denied or detected; ledger bytes unchanged |

### C3 retirement tests

| ID | Test | Required result |
|---|---|---|
| `T-ACI-RETIRE-001` | inventory all repository and deployed readers/writers | no active consumer requires a post-epoch YAML row |
| `T-ACI-RETIRE-002` | attempt append through appender and direct write after epoch | both denied; file digest unchanged |
| `T-ACI-RETIRE-003` | compare final YAML history with replacement audit projection | every historical identity remains queryable with source digest and derived-field labels |
| `T-ACI-RETIRE-004` | backup/restore preserved ledger and replacement projection | byte-identical history and equivalent high-level queries |
| `T-ACI-RETIRE-005` | retirement with pending/unknown/divergent effects | activation fails closed |
| `T-ACI-RETIRE-006` | rollback query deployment after retirement | history remains available; no retroactive writes or invented acknowledgements |

## Promotion checklist

C1/C2 remain blocked until all boxes are evidenced on the target host:

- [ ] opening and close materializers exist and use the validated appender port;
- [ ] complete `SoleWriterEvidenceBundle` passes;
- [ ] exact canonical row fixtures match appender output;
- [ ] crash matrix and no-provider-before-opening assertions pass;
- [ ] watcher-disable authority fence and monotonic epoch pass;
- [ ] rollback receipt proves future-only rerouting and no dual owner;
- [ ] logs/metrics above are emitted and correlated to accepted journal offsets;
- [ ] production gate is explicitly promoted by the owner.

C3 additionally requires its own ADR, work-pack authorization, consumer migration receipt, historical
preservation receipt and all `T-ACI-RETIRE-*` tests.

