# Investigator 02 — Persistence and transaction

## Key Findings

- **Implemented — the current SQLite/journal seam can host one atomic confirmation writer without
  introducing a second writer.** `RuntimeDatabase` opens every connection with foreign keys, WAL,
  `synchronous=FULL` and bounded busy handling, and `write()` serializes `BEGIN IMMEDIATE` through
  commit/rollback ([`implementations/server/runtime/database.py:43-56`](../../../../../../../implementations/server/runtime/database.py),
  [`implementations/server/runtime/database.py:137-146`](../../../../../../../implementations/server/runtime/database.py)).
  Within that transaction, `RuntimeJournal.accept()` checks the scoped idempotency key, finalizes
  additional and event artifacts, appends the ordered event group, advances the aggregate head,
  invokes an operation-specific mutation, and stores the receipt
  ([`implementations/server/runtime/journal.py:163-188`](../../../../../../../implementations/server/runtime/journal.py),
  [`implementations/server/runtime/journal.py:198-253`](../../../../../../../implementations/server/runtime/journal.py),
  [`implementations/server/runtime/journal.py:255-350`](../../../../../../../implementations/server/runtime/journal.py)).
  Existing failpoint tests demonstrate rollback across artifacts, events, heads, constrained rows,
  a specialized effect row and the receipt
  ([`implementations/tests/runtime/test_bus_reveal_delivery.py:496-573`](../../../../../../../implementations/tests/runtime/test_bus_reveal_delivery.py)).

- **Specified, not implemented — the smallest conformant acceptance unit is larger than a
  `confirmed_dispatches` insert.** `ConfirmRuntimeDispatch` must atomically create exactly one
  `ConfirmedDispatch` and one `Run`, emit `run.created` followed by
  `audit_opening.requested`, and persist the opening effect intent with the run facts
  ([`docs/features/agents-communication-infra/specs/operations.md:73-94`](../../../specs/operations.md),
  [`docs/features/agents-communication-infra/specs/events.md:38-60`](../../../specs/events.md)).
  To unblock suspension, that same accepted authority must also preserve the expanded fixed graph,
  one preallocated `continuation_id`, two ordered `ContinuationInputMapping` records, and their
  preallocated source message identities
  ([`docs/features/agents-communication-infra/specs/domain.md:178-203`](../../../specs/domain.md),
  [`docs/features/agents-communication-infra/specs/workflows.md:152-171`](../../../specs/workflows.md)).
  The active ledger correctly records that no such writer or persisted graph exists
  ([`docs/features/agents-communication-infra/CRAFT.md:115-122`](../../../CRAFT.md)).

- **Implemented seam / missing kernel primitive — artifacts and synchronous rows can join the
  transaction, but a general durable effect outbox cannot.** `ArtifactStore.prepare()` is
  non-persisting and content-addressed; `finalize(conn, prepared)` performs exact metadata/policy
  deduplication within the caller's transaction
  ([`implementations/server/runtime/artifacts.py:68-113`](../../../../../../../implementations/server/runtime/artifacts.py),
  [`implementations/server/runtime/artifacts.py:115-168`](../../../../../../../implementations/server/runtime/artifacts.py)).
  However, migrations 001–011 contain no `effect_intents` table; the only implemented effect row is
  `sandbox_launch_effects(effect_id, attempt_id, request_id, state='pending', created_at)`
  ([`implementations/server/runtime/migrations/010_agent_reference_delivery.sql:39-45`](../../../../../../../implementations/server/runtime/migrations/010_agent_reference_delivery.sql)),
  whereas the ratified store contract requires effect type, causal event, payload ref/digest, retry
  class, claim fence, status and terminal outcome fields
  ([`docs/features/agents-communication-infra/specs/persistence-and-replay.md:96-111`](../../../specs/persistence-and-replay.md)).
  The confirmation SWU therefore needs either the general `effect_intents` table now or an explicit
  opening-specific outbox that is accepted as a temporary contract deviation; the existing sandbox
  table cannot represent audit opening.

- **Specified but underdetermined / not implemented — there is no current bytes-to-`DispatchSpec`
  and fixed-turn-graph compiler for the writer to call.** The command boundary is required to read
  and verify the pending bytes once, finalize a `DispatchSpec`, freeze all schema versions, and
  persist capability resolution before command acceptance
  ([`docs/features/agents-communication-infra/specs/interfaces.md:46-63`](../../../specs/interfaces.md)).
  Yet `DispatchSpec.group_graph` is only constrained as a finite object
  ([`docs/features/agents-communication-infra/specs/domain.md:622-637`](../../../specs/domain.md)),
  the protocol compiler explicitly forbids mapping its candidate to `DispatchSpec` or runtime
  authority ([`docs/features/agents-communication-infra/specs/protocol-compilation.md:427-453`](../../../specs/protocol-compilation.md)),
  and the existing bound launch-plan compiler writes only turn-0 manifests/launches
  ([`implementations/server/runtime/dispatch_workflow.py:360-425`](../../../../../../../implementations/server/runtime/dispatch_workflow.py)).
  Before coding, the SWU must fix the canonical bounded input shape and deterministic expansion
  algorithm for `author:0 -> reviewer:0 -> author:1`, including graph, continuation, mapping and
  message IDs.

- **Specified vs implemented conflict — confirmation identity replay is stronger than the
  journal's present idempotency behavior.** The operation requires an existing dispatch/run
  identity with the same digest to return the original stable receipt, and the same identity with a
  different digest to fail permanently
  ([`docs/features/agents-communication-infra/specs/operations.md:96-103`](../../../specs/operations.md)).
  `RuntimeJournal.accept()` only replays by `(scope_key, idempotency_key)`; if that key is new it
  immediately verifies the target aggregate version
  ([`implementations/server/runtime/journal.py:165-179`](../../../../../../../implementations/server/runtime/journal.py),
  [`implementations/server/runtime/journal.py:357-366`](../../../../../../../implementations/server/runtime/journal.py)).
  Because the command digest itself includes the idempotency key
  ([`implementations/server/runtime/journal.py:58-79`](../../../../../../../implementations/server/runtime/journal.py)),
  simply collapsing every confirmation onto one dedupe key would convert a same-authority replay
  under a new client key into `IdempotencyConflict`. A conformant writer needs an in-transaction
  dispatch-identity/digest lookup that can return the first receipt, not an unlocked preflight.

## Gaps or Inconsistencies

- Migration `012` must minimally add `confirmed_dispatches`, `runs`, a digest-bound
  `confirmed_turn_graphs` record, exactly two queryable `continuation_input_mappings`, and a durable
  opening outbox row. Separate node/edge tables are not necessary for the bounded slice if the
  canonical expanded graph is a finalized artifact and the graph row stores its ref/digest plus the
  unique `continuation_id`; the mapping columns still need relational uniqueness over mapping ID,
  source message ID and `(continuation_id, slot_ordinal)`.
- `RuntimeService` has no confirmation method, `ACI_SCHEMAS` has no `run.created` or
  `audit_opening.requested` binding/validator, and the runtime API exposes no confirm endpoint
  ([`implementations/server/runtime/service.py:61-92`](../../../../../../../implementations/server/runtime/service.py),
  [`implementations/server/runtime/api.py:73-132`](../../../../../../../implementations/server/runtime/api.py)).
  These are absent implementation surfaces, not evidence that the contract is optional.
- The transaction should prepare exact pending-sheet, `DispatchSpec`, capability-resolution,
  expanded-graph and canonical-opening-row artifacts before entering the writer; then one
  `journal.accept()` call should finalize them, append `run.created` and
  `audit_opening.requested` at run aggregate versions 1 and 2, set the head to
  `opening_pending`, insert all synchronous rows plus one pending opening effect, and store a
  receipt containing stable run/graph/effect identities. Any failpoint must leave every member
  absent.
- `legacy-managed` must be rejected before artifact commit. For `runtime-managed`, dispatch, run,
  graph, continuation, mapping, source-message, event and effect identities should derive from the
  frozen authority plus structural coordinates, or the spec must explicitly authorize stored
  nondeterministic IDs. The current documents require stable/preallocated identities but do not
  specify their canonical derivation.
- The already-planned continuation task claims migration filename
  `012_agent_continuation.sql` ([`docs/features/agents-communication-infra/development/invoke-runs/20260831-resumable-feedback/plan/work-pack/tasks/TASK-CONT-001.md:25-41`](../../../development/invoke-runs/20260831-resumable-feedback/plan/work-pack/tasks/TASK-CONT-001.md)).
  A prerequisite confirmation migration must take 012 and the continuation task must be renumbered
  before either implementation begins.
- The writer can coherently stop at `opening_pending`; executing the pending materializer effect and
  accepting `audit_opening.verified` are separate work. It must not claim readiness to start agents
  merely because confirmation committed—the interface explicitly says provider/tool work remains
  blocked until opening verification
  ([`docs/features/agents-communication-infra/specs/interfaces.md:65-76`](../../../specs/interfaces.md)).

## Local Tensions

- **Runtime authority vs legacy foreign keys:** new runtime-managed authority must not be inferred
  from `dispatch_links`, but current `host_workflow_turn_bindings.dispatch_id` and
  `agent_attempts.dispatch_id` both reference that legacy table
  ([`implementations/server/runtime/migrations/009_host_workflow_binding.sql:1-4`](../../../../../../../implementations/server/runtime/migrations/009_host_workflow_binding.sql),
  [`implementations/server/runtime/migrations/010_agent_reference_delivery.sql:1-6`](../../../../../../../implementations/server/runtime/migrations/010_agent_reference_delivery.sql)).
  Confirmation can be persisted independently, but the later source attempt needed by suspension
  cannot currently exist without a legacy link. Silently inserting a `dispatch_links` row during
  confirmation would violate the recorded decision that it is not runtime authority.
- **General atomic contract vs operation-specific implementation:** the spec defines
  `atomic(receipt + events + aggregate_head + new_effect_intents)`
  ([`docs/features/agents-communication-infra/specs/rules.md:106-124`](../../../specs/rules.md)); the
  journal has an adequate generic `mutate` callback but no first-class effect-intent input or
  validation. Using `mutate` is the smallest implementation route, but it leaves effect invariants
  operation-specific unless the SWU adds a shared outbox primitive.
- **Exact bounded workflow vs generic graph contract:** the workflow fixes three nodes, two
  execution edges and exactly two ordered continuation sources, while `DispatchSpec` does not define
  the concrete JSON member names or expansion rules that would prove those facts. Accepting a caller
  supplied expanded graph would resolve mechanics by weakening the server-derived authority
  boundary.
- **Stable identity receipt vs aggregate CAS:** a unique `dispatch_id` row plus run aggregate CAS
  safely prevents duplicate state, but without identity-aware replay the losing same-digest request
  receives a version/uniqueness conflict instead of the required original receipt. An external
  read-before-write check is insufficient under concurrent confirmation.

## Questions for Synthesis

1. Does the next SWU include the authenticated command-boundary resolver that turns exact pending
   bytes into a finalized `DispatchSpec`, or may it accept a server-internal verified confirmation
   plan while a separate adapter SWU owns chat/UI transport? The latter is smaller but does not yet
   prove the complete chat-to-authority path.
2. Should migration 012 introduce the ratified generic `effect_intents` outbox, or is an
   `audit_opening_effects` table an explicitly accepted temporary slice? The generic table is more
   coherent; it broadens the SWU into claim/outcome schema even if claim execution remains deferred.
3. Is one canonical expanded-graph artifact plus a graph identity row and two normalized mapping
   rows sufficient evidence, or must nodes and edges be separately normalized for later scheduler
   queries?
4. Must this prerequisite also decouple runtime attempts/host bindings from `dispatch_links`, or is
   that a separate scheduler migration that remains blocking after the writer lands?
5. What exact fields enter `ConfirmedDispatch.digest`, and what deterministic namespace derives
   `run_id`, graph/continuation/mapping/message IDs and the opening effect ID? This must be fixed
   before idempotency and byte-identical replay tests can be authoritative.
6. Is success for this SWU deliberately “durable `opening_pending` with one unclaimed opening
   intent,” or must the audit materializer/verified-opening path be included before
   `TASK-CONT-001` is reopened?
