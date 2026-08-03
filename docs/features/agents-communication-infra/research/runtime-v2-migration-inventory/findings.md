# Runtime v2 Migration Inventory — Exploration Findings

Source dispatch: `2026-08-03-runtime-v2-as-built-exploration-retry`

## Answer

The repository already contains a reusable transactional and audit substrate plus useful legacy
bindings, but it does not contain an executable skill-to-DAG pipeline, an autonomous DAG scheduler,
or real provider execution; those remain the principal construction boundary.

## Convergent findings

1. **Reuse the transactional substrate.** Canonicalization, SQLite migrations, journal acceptance,
   artifacts, capability scopes, receipts/idempotency and database recovery are implemented and
   have focused passing tests ([runtime return](research.md#runtime-and-persistence--lamport-leslie)).
2. **Adapt, do not overclaim, the collaboration primitives.** Publication, officialization,
   collection close, reveal, peer-input binding and `AgentInvocationPlan` authorization exist, but
   they depend on an external trusted scheduler and stop before provider start
   ([runtime return](research.md#runtime-and-persistence--lamport-leslie)).
3. **Treat the current host path as a compatibility adapter.** Registry resolution, strict
   opening/close, YAML append, bridge receipts and host bindings are operational primitives, while
   the parent still schedules and relays the work
   ([legacy return](research.md#legacy-and-operations--torvalds-linus)).
4. **Do not claim a reusable DAG exists.** The profile, binding, candidate and confirmation chain is
   discovery/spec material; the documentary experiment is explicitly non-confirmable and no
   reusable DAG registry or executable compiler was found
   ([compiler return](research.md#skillprofilerecipedagdispatch--wirth-niklaus)).
5. **Do not claim the current launch compiler executes a graph.** It iterates all agents, emits
   turn-zero bindings with empty slots and does not consume `connections`; its five focused tests
   passed and confirm that limited behavior
   ([compiler return](research.md#skillprofilerecipedagdispatch--wirth-niklaus)).
6. **Do not merge the shadow runtime by assumption.** `implementations/agent-runtime` has a passing
   local suite but owns a parallel store/journal/receipt model and has no observed consumer in the
   main runtime ([runtime return](research.md#runtime-and-persistence--lamport-leslie)).
7. **Freeze a coherent snapshot before migration.** During the research the registry/appender pins
   changed while fixtures and Stage-E manifests remained on earlier values, leaving integration
   preflight red. This is direct evidence that the current working tree is not a stable migration
   baseline ([runtime return](research.md#runtime-and-persistence--lamport-leslie),
   [legacy return](research.md#legacy-and-operations--torvalds-linus)).

## Migration evidence matrix

| Candidate | Owner (precedent) | Witnessed? | Sound? | Verdict | Use-mode |
|---|---|---:|---:|---|---|
| Reuse canonicalization, journal, artifacts, capabilities and receipt primitives | `implementations/server/runtime/**` | yes | yes | GO | already-deployed |
| Adapt publication/reveal and invocation materialization | `RuntimeService`, `reveal_delivery.py` | yes | yes, if described as partial | GO | already-deployed |
| Preserve YAML/appender/hooks behind a legacy compatibility boundary | registry, appender, bridge and host hooks | yes | yes | GO | already-deployed |
| Treat current profiles as a reusable skill/DAG registry | Stage-A profile mirrors | no | no: different concept | KILL | tautological/ownership mismatch |
| Treat `compile_bound_launch_plan` as a DAG scheduler | `dispatch_workflow.py` | no | no | KILL | no-witness |
| Treat `AgentInvocationPlan` materialization as provider execution | `RuntimeService` materialization slice | no | no | KILL | no-witness |
| Automatically merge the shadow `agent-runtime` into the main runtime | `implementations/agent-runtime` | no integration witness | unresolved | KILL | no-witness |
| Build the skill-to-DAG compiler from the owned protocol discovery and prototype | Agents Communication Protocols discovery and compilation experiment | documentary witness only | yes as future work, not current capability | GO | build-from-owned |

## Current capability boundary

```text
Implemented and reusable
  canonical bytes/digests
  transactional journal
  artifacts and scoped capabilities
  receipts/idempotency
  publication/reveal primitives
  host bindings and legacy audit adapters

Not implemented as an integrated runtime
  skill closure and profile registry
  reusable DAG artifact/registry
  DispatchCandidate → canonical DispatchSpec compiler
  ConfirmedDispatch/Run runtime-managed path
  Run reducer and readiness scheduler
  dynamic input manifests and edge traversal
  provider launch/effect reconciliation
  workflow-terminal replay
```

## Limitations and next gate

This was the exploration wave, not the skeptic wave. It establishes the as-built baseline and kills
several overclaims, but it does not yet ratify the migration matrix or choose repository/branch
topology. The next synthesis must preserve the test failures and concurrent schema drift as evidence;
the subsequent precedent, non-vacuity and definitional-soundness skeptics must independently attack
that synthesis before an architecture-target discovery begins.
