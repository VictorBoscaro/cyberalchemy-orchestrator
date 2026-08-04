# Runtime v2 Migration Inventory — Exploration Findings

Source dispatch: `2026-08-03-runtime-v2-as-built-exploration-retry`

## Answer

The repository already contains a reusable transactional and audit substrate plus useful legacy
bindings, but it does not contain an executable skill-to-DAG pipeline, an autonomous DAG scheduler,
or integrated `runtime-managed` provider start and effect reconciliation; those remain the principal
construction boundary. The live Claude/Codex host does execute real agents in the legacy lane.

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
7. **Freeze a coherent evidence snapshot before migration.** The exploration recorded 46 passing
   and 18 failing tests, but did not preserve the command, tree identity, manifest digests or output
   needed to reproduce its drift attribution. A recheck at `2026-08-03T20:11:56-03:00`, using
   `python -m unittest discover -s implementations/tests/runtime -t .` against
   `HEAD b2ad44b5ed6fbd761e7a9a33fdcc67088185f7a6` and Stage-E manifest SHA-256
   `62d660097272dc072c3c25a6ebadb443b81d5a567069c8888b044dd7f686c633`, passed 119/119 tests with
   exit code 0. The exact pre-command status and combined output are frozen in the
   [recheck receipt](runtime-suite-recheck-2026-08-03.txt), SHA-256
   `336af234af257e98cc74541e9950056e76000652ff7e4ef0197947e6f9ed4381`; the receipt also shows the
   two unrelated untracked dispatch proposal/input paths. This current result does not prove the
   historical cause or concurrency; it demonstrates why future migration evidence must freeze
   command, tree state, digests and output
   ([runtime return](research.md#historical-test-observation-and-current-recheck)).

## Migration evidence matrix

| Candidate | Authority owner | Implementation precedent | Witnessed? | Sound? | Verdict | Use-mode |
|---|---|---|---:|---:|---|---|
| Reuse canonical bytes, digests and SQLite persistence | [ADR-001 persistence and canonical contracts](../../adrs/ADR-001-persistence-replay-and-canonical-contracts.md) | `canonical.py`, `database.py`, migrations | yes | yes | GO | already-deployed |
| Reuse journal acceptance, heads and replay primitives | [EventJournal](../../specs/interfaces.md#internal-eventjournal) | `journal.py`, `projections.py` | yes | yes | GO | already-deployed |
| Reuse immutable artifact primitives | [ArtifactBoundary](../../specs/interfaces.md#internal-artifact-boundary) | `artifacts.py` | yes | yes | GO | already-deployed |
| Reuse scoped and revocable capability primitives | [ACI SPEC capability/registry/gate source](../../specs/SPEC.md#what-this-module-owns) | `capabilities.py` | yes | yes within operation-specific contracts | GO | already-deployed |
| Reuse publication receipt and idempotency primitives | [ACI-R3 append-before-receipt rule](../../specs/rules.md#aci-r3--append-before-receipt-and-parent-verification) | `RuntimeService.publish`, journal receipts | yes | yes | GO | already-deployed |
| Adapt reveal publication | [PublishRevealManifest](../../specs/operations.md#publishrevealmanifest) | `RuntimeService.publish_reveal_manifest`, `reveal_delivery.py` | yes | yes, if described as partial | GO | already-deployed |
| Adapt invocation-plan authorization and peer-input materialization | [AuthorizeAgentInvocationPlan](../../specs/operations.md#authorizeagentinvocationplan) and [MaterializeAuthorizedPeerInput](../../specs/operations.md#materializeauthorizedpeerinput), each retaining its own operation boundary | `RuntimeService` authorization/materialization slice | yes | yes, if described as partial | GO | already-deployed |
| Preserve legacy route/type resolution behind the compatibility boundary | `implementations/contracts/dispatch-type-registry.v1.json` | `dispatch_workflow.py`, host hooks | yes | yes | GO | already-deployed |
| Preserve legacy opening/close append mechanics behind the compatibility boundary | `telemetry/agents/subagents-dispatch.yaml` through the sole authorized appender contract | `append-dispatch.cjs`, orchestration bridge | yes | yes | GO | already-deployed |
| Treat current profiles as a reusable skill/DAG registry | APT owns the digest-bound imported profiles; the Stage-A files are non-authoritative review mirrors | `profiles.py` import and canonical-equality checks | no | no: different concept | KILL | ownership mismatch |
| Treat `compile_bound_launch_plan` as a DAG scheduler | Legacy workflow/session authority only | `dispatch_workflow.py` | no | no | KILL | no-witness |
| Treat `AgentInvocationPlan` materialization as provider execution | Existing ACI invocation/materialization contracts; provider execution is not owned by this slice | `RuntimeService` materialization slice | no | no | KILL | no-witness |
| Automatically merge the shadow `agent-runtime` into the main runtime | Unsettled; no cutover authority has been ratified | `implementations/agent-runtime` | no integration witness | unresolved | KILL | no-witness |
| Build the skill-to-DAG compiler from the protocol discovery and prototype | Unsettled pending owner decision, ratification and promotion into `SPEC` | Agents Communication Protocols discovery and compilation experiment, as proposal precedent only | documentary witness only | sound only as a proposal for future work | BLOCK | proposal-only |

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

This exploration establishes an evidence-bounded as-built baseline and kills several overclaims, but
it does not ratify the migration matrix, settle skill-to-DAG ownership or choose repository/branch
topology. Before an architecture-target discovery begins, route these existing artifacts through the
canonical `review` gate: independent explorer attackers differentiated by lens, one writer, skeptic
verifiers, and a single persisted `review.md`. Any future test-state claim must preserve its exact
command, timestamp, tree identity, relevant manifest digests and output.
