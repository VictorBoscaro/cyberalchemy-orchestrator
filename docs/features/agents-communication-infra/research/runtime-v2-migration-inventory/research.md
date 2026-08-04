# Runtime v2 Migration Inventory — Collected Returns

Dispatch: `2026-08-03-runtime-v2-as-built-exploration-retry`

The following returns are preserved by seat. They are evidence contributions, not yet the accepted
cross-seat synthesis.

## Runtime and persistence — Lamport, Leslie

Há bastante infraestrutura reutilizável, mas ainda não há um runtime autônomo de DAG.

O repositório contém duas implementações distintas:

1. `implementations/server/runtime`: runtime governado principal, relativamente amplo, integrado à
   lane `legacy-managed`, SQLite, ledger YAML, hooks e piloto local.
2. `implementations/agent-runtime`: shadow runtime independente e explicitamente experimental, sem
   integração com launcher/host e sem autoridade operacional demonstrada.

### Component inventory

| Capability / component | Evidence | Maturity | Migration signal | Limitations |
|---|---|---|---|---|
| Canonicalization and identity | `server/runtime/canonical.py`: `canonical_bytes`, `canonical_digest`, `parse_strict_json` | implemented and tested | reuse | schema-aware support is partly Stage-A-specific |
| SQLite and migrations | `database.py`: `RuntimeDatabase`; migrations `001`–`011` | implemented and tested | reuse | monolithic DB mixes ACI, APT and legacy slices |
| Transactional journal | `journal.py`: `RuntimeCommand`, `RuntimeJournal.accept`, `read_complete_groups`, `verify_store` | implemented and tested for atomicity, retry and integrity | reuse | not a `Run` reducer or scheduler |
| Artifact store | `artifacts.py`: `ArtifactStore.prepare/finalize/get_authorized` | implemented and tested | reuse | no external backend, executable retention or redaction engine |
| Capability scopes | `capabilities.py`: `CapabilityManager.issue/resolve/revoke` | implemented and tested fail-closed | reuse/adapt | no general identity/provider authority |
| Profile import | `profiles.py`: `ProfileImporter`; `RuntimeService.register_profiles` | implemented for four frozen profiles | adapt | not a skill, recipe or reusable-DAG registry |
| Projections and APT provenance | `projections.py`; `provenance.py` | implemented and broadly tested | reuse selectively | domain-specific; no generic `Run` state |
| Basic publication/bus | `RuntimeService.publish`, `verify_publication`, `close_collection`, `publish_reveal_manifest` | implemented and tested for official publication/reveal | adapt | not a complete DAG-routed Work Bus |
| Invocation plan/materialization | `service.py:2970` `authorize_agent_invocation_plan`; `service.py:3038` `materialize_authorized_peer_input`; `reveal_delivery.py` | implemented through persisted request/effect | reuse/adapt | trusts an external scheduler; provider start remains pending and tests prove zero starts |
| Reference Scout lifecycle | `RuntimeService.start_reference_scout` through termination | implemented and tested | adapt | specialized and does not launch the Scout |
| Host workflow binding | `bind_host_workflow_turn`, `complete_host_workflow_turn`; migration `009` | implemented and tested in isolation | adapt | authorizes host calls but does not discover transitions |
| Legacy launch compiler | `dispatch_workflow.py:94` `compile_bound_launch_plan` | implemented; five focused tests pass | adapt/rewrite boundary | only turn zero, `slots: []`, no readiness or dynamic handoffs |
| YAML↔ACI bridge | `orchestration_bridge.py`: `LocalOrchestrationLoggingBridge` | implemented; isolated logic passes | legacy adapter | Node subprocess, YAML dependency, legacy-only authority mode |
| Host hooks | `host_dispatch_hook.py`, `host_ingestion_hook.py` | present and partly tested | legacy adapter | host/source-manifest coupling; current runtime-suite coverage passes, without proving live-host operability |
| API/local pilot | `api.py`; `local_pilot.py:139` | loopback pilot implemented | adapt | production serve disabled; the current runtime suite passes, but serving still requires its explicit operator preflight |
| Recovery utilities | `operator_recovery.py` | nine tests pass | reuse | database recovery, not interrupted-`Run` recovery |
| Shadow `agent-runtime` | `agent_runtime/runtime.py`; `ledger_shadow.py` | experimental; 31 tests pass | mine or archive | parallel store/journal/receipts with no launcher, authorization or cutover |

The observed main composition is:

```text
CLI / API / host hooks
        ↓
RuntimeService
        ├── RuntimeDatabase + migrations
        ├── RuntimeJournal
        ├── ArtifactStore
        ├── CapabilityManager
        ├── ProjectionManager
        ├── ProfileImporter
        └── StrictLegacySnapshotResolver
                 ↓
        ledger YAML + appender Node
```

`RuntimeService` instantiates these dependencies in `service.py:104-123` and registers schemas and
validators in `service.py:125-171`. The separate `agent-runtime` package was not found as an import
of `server/runtime` or another consumer.

### Test evidence

The seat executed 149 focused tests:

- `implementations/agent-runtime/tests`: 31/31 passed.
- Core server tests for canonicalization, DB, journal, artifacts, capabilities, dispatch compiler,
  bus/reveal, delivery, binding and recovery: 54/54 passed.
- APT, Reference Scout, bridge, hooks, local pilot, appender and traceability: 46 passed and 18
  failed.

### Historical test observation and current recheck

The exploration reported 46 passing and 18 failing tests and attributed the failures to drift among
the appender/schema, fixtures and the Stage-E source manifest. That run did not preserve the exact
command, tree identity, manifest digests or output, so it is a historical, non-reproducible
observation rather than evidence about the current workspace. It does not support a concurrency
claim or a present-tense preflight verdict.

A reproducible recheck at `2026-08-03T20:11:56-03:00` ran:

```powershell
python -m unittest discover -s implementations/tests/runtime -t .
```

against `HEAD b2ad44b5ed6fbd761e7a9a33fdcc67088185f7a6`, with Stage-E manifest SHA-256
`62d660097272dc072c3c25a6ebadb443b81d5a567069c8888b044dd7f686c633`. The exact pre-command
`git status --short`, combined command output and exit code are frozen in the
[recheck receipt](runtime-suite-recheck-2026-08-03.txt), SHA-256
`336af234af257e98cc74541e9950056e76000652ff7e4ef0197947e6f9ed4381`. The receipt shows two
unrelated untracked dispatch proposal/input paths, so this was not a clean-tree test, and records
`119` tests in `109.872s` with `OK` and exit code `0`. This supports the current runtime-suite result
only; it does not prove production serving or recover the missing evidence from the historical run.

### Limiting facts

1. There is no generic scheduler runtime.
2. `AgentInvocationPlan` is accepted from a trusted scheduler that is not implemented in the scoped
   corpus.
3. Materialization does not start a provider; the launch effect remains pending.
4. The Work Bus is partial: publication, officialization, close, reveal and input binding exist, but
   active routing and DAG scheduling do not.
5. Recovery covers database integrity and backup, not workflow continuation or unknown provider
   effects.
6. Replay does not reduce a generic DAG `Run` into next commands.
7. Concrete execution authority remains legacy-managed.
8. The exploration recorded a failing historical integration run without enough frozen evidence to
   reproduce it; the current runtime suite passes under the tree identity recorded above.
9. The shadow runtime must not be counted as an already-integrated second half of the main runtime.

Migration verdict: reuse canonicalization, journal, artifacts, capabilities, migration discipline,
receipts/idempotency and deterministic materialization; adapt profiles, publication/reveal,
invocation plans, bindings and Reference Scout; retain bridge/YAML/hooks as legacy adapters; decide
APT and shadow-runtime disposition explicitly; build skill-to-DAG compilation, DAG registry,
`Run` reducer, readiness scheduler, command/effect loop, provider adapters, effect reconciliation and
workflow-terminal replay.

## Skill/profile/recipe/DAG/dispatch — Wirth, Niklaus

Não existe hoje um DAG reutilizável persistido nem um compilador executável
skill→DAG→`DispatchSpec`. O único compilador operacional no escopo é legacy e transforma uma opening
row já concreta em launches iniciais; ele ignora `connections`, lança todos os seats em
`turn_ordinal: 0` e grava manifests com `slots: []`.

### Evidence distinctions

- `discovery/agents-communication-protocols/README.md:18-24,82-83,87-132,192-225` defines
  `SkillExecutionProfile`, `SkillProtocolBinding`, `DispatchCandidate`, `ConfirmationProjection`
  and the candidate flow, but explicitly does not ratify schemas or implement runtime.
- The same discovery records that the current compiler materializes only initial launches and does
  not traverse a graph (`README.md:52-53`), and classifies confirmed runtime authority as
  draft-specified rather than generic-runtime implemented (`README.md:256-268`).
- `specs/SPEC.md:61-83,462-463` says skill-to-protocol is not ratified or implemented; there is no
  `SkillExecutionProfile` registry, active binding, trust anchor or `ProtocolAuthoringCommand`.
- `experiments/skill-protocol-compilation/README.md:1-7,17-22` is an explicitly non-ratified
  prototype with no compiler, registry, DB, execution fixture or runtime integration. Its example
  YAML is `example_only: true` and `confirmable: false`.
- `protocol-design.md:29-37,299-306` describes future compiler inputs and output, not code.
- `profiles/README.md` contains four non-authoritative Stage-A ACI/APT profile mirrors, not a
  `SkillExecutionProfile` registry.
- `domain.md:20-54,452-467` and `workflows.md:13-45` specify draft targets but do not prove
  implementation.
- `dispatch_workflow.py:94-202` validates a legacy opening row, iterates `groups[*].agents`, creates
  turn-zero attempts and empty manifests, and writes a launch plan. It does not read `connections`,
  create `DispatchCandidate`/`DispatchSpec`/`ConfirmedDispatch`/`Run`, reduce readiness or schedule
  transitions.
- The executable dispatch registry exposes only `legacy-managed` for routable types.

Focused validation: `python -m unittest implementations.tests.runtime.test_dispatch_workflow -v`
passed 5/5, including evidence for `slots: []` and refusal of `runtime-managed`.

| Stage | Owner | Artifact | Implementation evidence | Missing boundary |
|---|---|---|---|---|
| Skill revision | skill author/domain owner | skill bytes plus hypothetical source manifest/digest | skill files only | transitive dependency closure and canonical digest |
| `SkillExecutionProfile` | proposed ACI protocol governance, unsettled | immutable profile and binding | none; current profiles are unrelated mirrors | schema, lifecycle, registry, CAS binding, compatibility |
| Reusable protocol/DAG/recipe | proposed protocol governance | provisional design blocks and example DAG YAML | documentary prototype only | canonical reusable identity, storage, parameter semantics, invalidation |
| `DispatchCandidate` | proposed compiler | closed non-authoritative invocation proposal | none | versioned schema, total obligation mapping, compiler |
| `DispatchSpec` / confirmation projection | ACI confirmation/runtime contracts | canonical spec bytes, digest and derived view | draft domain schema only | server compiler, capability integration, equality proof, persistence |
| `ConfirmedDispatch` | ACI runtime confirmation | immutable confirmed spec/digest | draft SPEC only | confirmation transaction/CAS and canonical storage |
| `Run` | ACI runtime/kernel | aggregate referencing the spec digest | draft domain/workflow only | creation, reducer, scheduler and terminal integration |
| Legacy bound launch | legacy workflow/session and host adapter | launch plan and per-seat manifests | implemented and tested | not DAG execution; no later turns or dynamic inputs |

Maximum supported claim: the repository has a detailed conceptual direction, a documentary
protocol-graph prototype and a tested legacy adapter for initial launches. It does not have the
executable persistent chain skill→profile→reusable DAG→`DispatchCandidate`→`DispatchSpec`→`Run`, nor
`connections`-governed scheduling.

## Legacy and operations — Torvalds, Linus

The legacy lane is a governed wrapper over Claude/Codex subagents, not a DAG runtime. It already
provides useful validation, binding, audit, idempotency and observability, but the parent agent is
still the effective scheduler and relay.

### Live flow observed

```text
type skill
  → registry resolves legacy-managed route
  → confirmed opening record
  → dispatch_workflow compiles bindings
  → appender writes YAML opening
  → bridge creates Session/Dispatch and SQLite events
  → parent calls spawn_agent/followup_task
  → hook validates binding and tracks host lifecycle
  → parent collects and forwards results
  → appender + bridge close YAML/SQLite
```

Concrete entrypoints include `dispatch_workflow resolve|compile|open|close`, Claude and Codex hooks,
the host dispatch hook launcher, `LocalOrchestrationLoggingBridge`, the loopback opt-in pilot and the
FastAPI read/control surfaces.

### Authority observed

- `implementations/contracts/dispatch-type-registry.v1.json`: type, ledger schema, routability,
  authority mode and tool profile.
- Selected type skill: work semantics, roles, topology and criteria.
- Confirmed opening record: concrete legacy dispatch declaration.
- `append-dispatch.cjs`: sole authorized YAML writer.
- YAML ledger: append-only compatibility opening/close record.
- SQLite journal: operational sessions, bindings, attempts, receipts and lineage.
- Claude/Codex host: real agent execution and effective tool/model surface.
- Hook JSON: local correlation, not domain authority.
- Control Center: non-authoritative read model and local drafts.

Unbound agent calls are automatically wrapped by the hook as compatibility `review` dispatches
without a separate confirmation. This preserves some auditability but weakens the claim that every
opening is a previously confirmed plan.

### Structural limit

`dispatch_workflow.py:94-196` generates every seat at `turn_ordinal: 0` with `slots: []`, does not
calculate readiness from `connections`, and does not execute handoffs, zig-zag or feedback. The hook
can validate later turns only after some external actor supplies a governed envelope and calls
`followup_task`; it is a useful execution primitive, not an autonomous scheduler.

The research skill's statement that host/runtime owns dependency scheduling is therefore stronger
than the observed implementation. The lifecycle says “for each ready seat,” but no inspected
component computes readiness.

### Migration disposition

Preserve registry resolution, canonicalization/digests, strict opening/close validation,
append-only discipline, scoped and revocable capabilities, receipts/idempotency, exact
parent-seat-turn binding, the open-seat close barrier, lineage capture, lenient historical reads and
strict live authority resolution. Claim capability consumption after acceptance only where the
governing exact-operation contract explicitly requires it.

Encapsulate YAML/appender, Claude/Codex hooks, `.claude` skills, pending sheets/markers, hook
correlation files, `host/inherited@1` and the current Control Center as compatibility adapters.

Replace or evolve the static launch compiler, manual parent coordination, externally assembled
handoffs, automatic `review` compatibility classification, apparent YAML/SQLite dual authority and
file-based hook state where the journal can own it.

### Cutover risks

1. Losing compatibility with historical rows accepted by the lenient reader.
2. Duplicating authority between YAML and SQLite.
3. Mistaking existing binding materialization for scheduling.
4. Depending on unenforced host model/tool declarations.
5. Incomplete host-specific termination reconciliation.
6. Contract and digest drift.
7. Letting Control Center projections appear authoritative.
8. Non-uniform confirmation through compatibility wrappers.
9. Partial lineage for shell/search/web inputs.
10. Unsafe big-bang cutover instead of compatible projection and shadow mode.

Focused historical evidence: `implementations/tests/test_ledger.py` passed, while the exploration's
runtime integration command and Control Center run were not preserved completely enough to support
a current-state conclusion. The reproducible current runtime-suite result is recorded above as
119/119 passing. The Control Center result remains unknown because its historical run exceeded 120
seconds and no current rerun was performed here.

Conclusion: do not port the legacy lane wholesale into the new core. Reuse identity, binding,
journal, capability and receipt primitives; keep YAML/appender/hooks at a compatibility boundary;
build the missing reducer, readiness scheduler, bound input manifests, output delivery and edge
execution in the new kernel.
