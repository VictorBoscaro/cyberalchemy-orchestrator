---
title: Confirmed Dispatch and Resumable Feedback Implementation Layering
status: draft
updatedAt: 2026-08-31
owner: agents-communication-infra
scope: capability
---

# Confirmed Dispatch and Resumable Feedback Implementation Layering

This document sequences the approved confirmation-authority prerequisite and the bounded
`author:0 -> reviewer:0 -> author:1` continuation capability. It is a planning artifact produced by
direct delegation, not evidence of an ACI governed dispatch, receipt, binding, or implementation.

Layer 0 is deliberately a reviewed executable-contract proof rather than runtime code. The
Robot-Talks human gate determined that code cannot be authoritative until the approval observation,
digest taxonomy, bounded graph projection, identity derivation, and golden vectors are unambiguous.
Every later layer must preserve all accepted guarantees from earlier layers.

## Context

- Target: explicit user approval observed through chat becomes durable runtime authority, then drives
  one finite resumable feedback graph without chat supervision.
- Current state: brownfield SQLite runtime with an atomic journal/artifact seam and official bus
  contributions, but no `ConfirmedDispatch` writer, confirmed turn graph, continuation aggregate,
  generic effect-intent outbox, or runtime-managed attempt path independent of legacy foreign keys.
- Primary operator: the person who approves an exact dispatch and expects the runtime to carry it
  forward without hidden authority or agent bus polling.
- Primary constraint: claim strength must follow evidence. A conversational “pode seguir” is valid
  human intent only after a trusted host binds it to the exact dispatch revision and canonical
  confirmation observation.
- Governing decisions: the approved Robot-Talks [findings](../../../../robot-talks/2026-08-31-confirmed-dispatch-next-increment/findings.md)
  and [dialogue](../../../../robot-talks/2026-08-31-confirmed-dispatch-next-increment/dialogue.md).
- Existing continuation plan: [WORK-PACK.md](WORK-PACK.md), [READINESS.md](READINESS.md), and the
  current [continuation layering](implementation-layering.md). Those records require later refresh;
  this document does not mutate or silently supersede them.
- Repaired baseline: the full runtime suite passes 152/152 after the separately authorized global
  baseline repair aligned Stage-E integrity pins and old agent-reference fixtures. Every later SWU
  must preserve that green baseline.

## Layering Method

- Minimum proof: first make authority derivation executable and reviewable, then implement it once.
- Decision-first: each layer answers one question that changes what may responsibly start next.
- Progressive hardening: authority creation, authority consumption, happy-path execution, and
  degraded-mode safety remain separate decisions.
- Non-regression: later layers retain exact bytes, authority provenance, identity replay, atomicity,
  effect fencing, and no-legacy-authority guarantees established earlier.
- Evidence-gated promotion: no layer starts because a prior document says “planned”; it starts only
  after the previous layer's named evidence and independent review pass.

## Layer Boundary Heuristic

```text
Layer value = decision unlocked + operator-visible outcome + risk reduced
Layer cost = implementation time + verification time + coordination burden

Stop a layer when the next unit of work has lower value-per-cost for its current decision than
starting the next decision layer.
```

The model uses five layers because each unlocks a distinct decision. Combining confirmation with
continuation would obscure whether failures arise in authority creation or authority consumption;
combining the happy path with recovery would make duplicate-work safety impossible to evaluate
independently.

## Layer Decision Table

| Layer | Decision question | Minimum working unit | Operator-visible outcome | Principal risk reduced | Main cost drivers | Promotion decision |
|---|---|---|---|---|---|---|
| L0 — CONF-000 | After this layer, we know whether one chat-observed approval can be represented as unambiguous, deterministic runtime authority before code exists. | Reviewed closed contract, admitted fixture, golden vector, and negative mutations. | A reviewer can reproduce the exact authority bytes, digests, graph, IDs, mappings, and opening intent authorized by one approval. | Competing implementations deriving different authority from the same approval. | Cross-spec alignment, canonicalization design, golden vectors, independent review. | Promote only if every output is reproducible and no authority field remains caller-selected or semantically ambiguous. |
| L1 — CONF-001 | After this layer, we know whether the existing single SQLite/journal writer can persist that exact authority atomically and converge under replay and failure. | Migration 012 plus one authenticated `ConfirmRuntimeDispatch` writer ending at durable `opening_pending`. | The same approved authority yields one stable receipt, one dispatch/run/graph, two mappings, and one unclaimed opening intent. | Partial authority, duplicate runs, lost-response divergence, and effects released before verified opening. | Schema migration, artifact/event integration, identity-level replay, failpoints, reopen tests, independent review. | Promote if the writer passes all focused evidence; otherwise remediate L0/L1 without starting continuation. |
| L2 — authority consumption | After this layer, we know whether continuation suspension can consume writer-created authority while the runtime-managed attempt path no longer structurally depends on legacy `dispatch_links`. | Explicit legacy-FK decoupling followed by TASK-CONT-001 on migration 013. | A terminal author turn can be parked effect-free using only confirmed graph/mapping identities derived by the runtime. | Legacy compatibility state becoming hidden authority; caller-injected continuation identity; partial suspension. | Compatibility migration, authority queries, continuation reducer/state tables, invalid-transition matrix, review coordination. | Promote if runtime-managed rows need no authoritative legacy link and suspension proves O-CONT-S5 from persisted confirmation data. |
| L3 — deterministic happy path | After this layer, we know whether journal facts alone can drive one exact same-session fake-adapter author-reviewer-author loop. | TASK-CONT-002 with two official contributions, canonical target input, scheduler reaction, one target attempt/effect, and fake adapter. | After approval, the bounded feedback loop reaches author turn 1 without chat supervision or agent bus polling. | Bus-to-next-turn handoff being non-deterministic, non-atomic, or dependent on provider memory. | Official-source joins, input materialization, scheduler, fake adapter, restart/idempotency evidence. | Promote if T-ACI-CONT2..4 and the happy-path/restart portion of CONT8 pass without weakening L0-L2 authority. |
| L4 — failure and recovery | After this layer, we know whether the bounded workflow fails safely and converges across definitive loss, unknown outcome, cancellation, expiry, crashes, and races. | TASK-CONT-003 with reconstruction, reconciliation, cancellation/expiry, exhaustive reducer checks, and failpoint/reopen evidence. | The run resumes or reconstructs at most once, or stops with an explicit durable reason; unknown never creates replacement work. | Duplicate physical work, stranded claimable effects, false terminalization, and unsafe fallback. | Race matrices, adapter status/dispose/cancel semantics, exhaustive failpoints, replay/reopen verification, closure audits. | Promote to any real-provider pilot only if T-ACI-CONT5..9 pass and all earlier invariants remain true; otherwise stop at the local fake-adapter capability. |

## Capability and Scope Progression

| Area | L0 — CONF-000 | L1 — CONF-001 | L2 — authority consumption | L3 — happy path | L4 — failure/recovery |
|---|---|---|---|---|---|
| Human approval | Versioned observation binds trusted principal, channel/host observation, dispatch revision, presented spec digest, and time | Authenticated boundary consumes that exact observation; chat is the initial surface, UI remains deferred | Read-only provenance | Read-only provenance | Read-only provenance |
| Digest taxonomy | Distinct `pending_sheet_digest`, `dispatch_spec_digest`, and `confirmed_authority_digest` | Exact artifacts and digests persisted and returned by stable receipt | Suspension queries the frozen authority digest | Input lineage retains it | Recovery/replay retain it |
| Graph and identities | Golden three-node/two-edge expansion; versioned derivation for run, graph, continuation, mappings, source messages, and effect | One graph record/artifact, one continuation ID, exactly two normalized mappings, deterministic effect ID | Same IDs are consumed, never accepted as caller authority | Official contributions resolve through those IDs | Reconstruction preserves those IDs and source lineage |
| Persistence | Normative relational/transaction projection only | Migration 012; `ConfirmedDispatch`, `Run`, graph/mappings, two events, run head, receipt, generic `effect_intents` row | Legacy-FK decoupling plus migration 013 continuation aggregate | Target input/attempt/request/effect acceptance | Cancellation, reconstruction, terminal and reconciliation state |
| External effects | Defines one unclaimed audit-opening intent and verified-opening fence | Creates the intent but neither claims nor materializes it; no agent/provider effect | Suspension creates zero effects | One fake resumable effect after prerequisites | Claim/cancel/reconcile semantics; still no real provider claim |
| Execution | Deferred | Deferred in `opening_pending` | Effect-free suspension only | Same-session fake-adapter loop | Fake degraded modes and convergence |
| Legacy compatibility | Declared non-authoritative | May coexist but cannot supply confirmation or mapping authority | FKs are decoupled before accepting the runtime-managed consumer slice | No runtime attempt depends on a legacy authority row | Compatibility cannot change recovery outcomes |
| Verification | Golden and negative vectors; exact-digest review | Atomicity, replay, conflict, failpoint, lost-response, reopen | Authority-source negatives, migration compatibility, exhaustive base transitions | Exact-source/input order, scheduler retry, restart | Full races, failpoints, reopen, exhaustive invalid pairs |

## Layer Definitions

### L0 — CONF-000: contract and golden-vector closure

**Decision question:** After this layer, we know whether one observed user approval has one
reproducible runtime-authority meaning.

**Minimum working unit:** a closed, versioned confirmation contract with one admitted bounded input,
one canonical successful fixture, golden expected outputs, and deterministic negative mutations.

**Included scope**

- Immutable confirmation-observation record and trusted issuer boundary.
- Exact meanings and canonical domains of the three approved digests.
- One admitted bounded pending-sheet-to-`DispatchSpec` projection for
  `author:0 -> reviewer:0 -> author:1`; no generic protocol compiler claim.
- Versioned derivation of `run_id`, graph identity, turn identities, `continuation_id`, both
  `mapping_id`s, both `source_message_id`s, `confirmed_binding_digest`, and opening `effect_id`.
- Explicit O-CONF atomic outputs: exact authority artifacts, one `ConfirmedDispatch`, one `Run`,
  expanded graph, exactly two ordered normalized mappings, `run.created`,
  `audit_opening.requested`, one unclaimed effect intent, `opening_pending`, and stable receipt.
- Identity-level replay by `(dispatch_id, confirmed_authority_digest)` and permanent conflict on a
  changed authority digest, independent of a new client idempotency key.
- Expanded T-ACI-AUTH1 fixture and negative vectors for mode, principal/observation, digest,
  capability resolution, graph shape, identity, ordering, replay, and conflict.

**Explicitly deferred**

- Runtime migration or writer code, REST/UI design, effect claiming/materialization, provider work,
  continuation state, legacy-FK migration, multi-host operation, and production cutover.

**Operator-visible result:** an independent reviewer can calculate and compare every canonical byte,
digest, ID, graph edge, mapping slot, event payload, effect payload, and receipt field for the
approved fixture.

**Risk reduced:** semantic ambiguity at the authority boundary and accidental acceptance of
caller-supplied expanded authority.

**Main cost drivers:** reconciling interface/architecture contracts, choosing one narrow projection,
canonicalization/golden data, mutation corpus, and independent exact-digest review.

**Exit evidence**

- Approved contract delta with no unresolved blocker-level field or derivation question.
- Machine-readable admitted fixture and golden vector whose hashes reproduce independently.
- Negative vector manifest proving closed rejection and no-authority outcomes.
- Traceability through O-CONF-1..11, CONF-R1..8 and T-ACI-AUTH1..8.
- Independent review report accepting semantics, derivations, and declared deferrals.

**Promotion decision:** continue to CONF-001 only when two independent implementations could consume
the same fixture and derive byte-identical authority. Pivot to a narrower admitted fixture if the
projection remains ambiguous. Stop if trusted host evidence cannot bind approval to one exact
dispatch revision.

**Non-regression carried forward:** approval is human authority; chat and a future UI are transport
surfaces, not different authority models; source bytes and all authority derivations are immutable;
legacy rows and caller fields are never confirmation authority.

### L1 — CONF-001: durable confirmation writer

**Decision question:** After this layer, we know whether the existing runtime can accept the L0
authority exactly once and preserve it atomically through crashes and retries.

**Minimum working unit:** migration `012` and one authenticated writer using the existing
SQLite/journal/artifact transaction to end at durable `opening_pending`.

**Included scope**

- Current chat/host ingress supplies the L0 canonical observation to the authenticated command
  boundary; no dedicated confirmation UI is required.
- Verify the already finalized capability-resolution preview evidence, then finalize exactly nine
  new artifact-metadata members: pending sheet, `DispatchSpec`, confirmation observation,
  confirmed graph, ordered mapping set, confirmed authority envelope, two event payloads and one
  audit-opening effect payload. The static payload-schema bundle and identity-derivation contract
  are digest-bound inputs; there is no opening-row artifact in confirmation.
- Persist one immutable `ConfirmationObservation`, one `ConfirmedDispatch`, one `Run`, the confirmed
  graph and sole continuation binding, exactly two queryable ordered mappings, both events, version-2
  run head, stable receipt and one generic `effect_intents` row in the same acceptance transaction.
- Return the first accepted receipt for same-identity/same-authority replay even with a fresh client
  idempotency key; reject same identity/different authority permanently.
- Failpoints around validation, every artifact/event/head/domain/outbox/receipt mutation,
  `before_commit`, and lost response after commit; reopen and concurrent confirmation evidence.
- Enforce `legacy-managed` rejection before artifact persistence and block every start/provider/tool
  effect until `audit_opening.verified` exists.

**Explicitly deferred**

- Claiming the opening intent, invoking the audit-ledger appender, accepting opening verification,
  starting agents, continuation operations, legacy-FK decoupling, a UI, and real-provider work.

**Operator-visible result:** retrying the same confirmed dispatch yields one stable receipt and one
durable `opening_pending` authority; inspection shows no external work has started.

**Risk reduced:** partial confirmation, duplicate runs, incorrect identity replay, and premature
external effects.

**Main cost drivers:** migration 012, operation-specific validation, generic outbox shape, journal
transaction integration, identity-aware replay under concurrency, failure injection, and review.

**Exit evidence**

- Migration applies once, reopens idempotently, and preserves database policy.
- Focused confirmation suite passes the full golden, negative, replay, conflict, concurrency,
  rollback, after-commit, and reopen matrix.
- Every failpoint leaves all transaction members absent, or—after commit—an identical retry returns
  the first receipt with exactly one accepted unit.
- Queries prove one graph, one continuation ID, exactly two ordered mappings, and one unclaimed
  opening intent; zero provider/tool/start effects exist.
- Focused Stage-B remains 19/19, the full suite adds no new signature, `git diff --check` passes,
  and an independent reviewer accepts the implementation/evidence package.

**Promotion decision:** continue only if CONF-001 is accepted as a focused capability and readiness
can state precisely that the writer passes while feature-wide verification remains FLAG/BLOCK for
unrelated drift. Remediate L0/L1 if identity, graph, atomicity, or effect fencing fails.

**Non-regression carried forward:** every L0 byte/digest/identity matches the golden contract;
confirmation stays single-writer, immutable, runtime-managed, and independent of legacy authority.

### L2 — authority consumption: legacy-FK decoupling plus TASK-CONT-001

**Decision question:** After this layer, we know whether an effect-free continuation aggregate can
consume CONF-001 authority without a legacy structural dependency or caller-selected identities.

**Minimum working unit:** a reviewed legacy-FK compatibility migration followed by
`TASK-CONT-001` on migration `013`, exposing suspend/query behavior against writer-created graph and
mapping rows.

**Included scope**

- Replace runtime-managed attempt/binding dependence on authoritative `dispatch_links` with an
  explicit parent relation to runtime confirmation authority; preserve legacy rows only as
  non-authoritative compatibility projections where still needed.
- Add continuation aggregate/mapping-consumer persistence, pure lifecycle reducer, atomic
  `SuspendAgentContinuation`, and query behavior.
- Derive/validate `continuation_id`, both mapping IDs, source messages, dispatch, source/target turn,
  and slot order from CONF-001 rows; caller and legacy-link substitutions reject with no write.
- Require a completed author source attempt and finalized reconstruction snapshot; commit one
  continuation/event/receipt unit with zero new effects.
- Byte-identical replay, semantic drift conflict, migration reopen, base invalid-transition matrix,
  and compatibility tests proving legacy-managed behavior remains isolated.

**Explicitly deferred**

- Official contribution resolution, target input materialization, scheduler, adapter, resume,
  reconstruction, cancellation, expiry, real audit materialization, and real provider.

**Operator-visible result:** a writer-confirmed terminal author turn can be parked durably and
queried, while neither the caller nor a legacy link can invent its continuation authority.

**Risk reduced:** O-CONT-S5 violation, hidden legacy authority, partial suspension, and effects
created merely to wait.

**Main cost drivers:** compatibility/FK migration and backfill policy, authority joins, reducer and
transition tests, migration renumbering, and two-stage review of decoupling plus suspension.

**Exit evidence**

- Schema inspection and tests show runtime-managed attempts/bindings can reference CONF-001
  authority without requiring a `dispatch_links` authority row.
- Legacy-managed fixtures still use their own path and cannot satisfy a runtime mapping query.
- T-ACI-CONT1 and the base T-ACI-CONT9 matrix pass, including caller/legacy substitution negatives,
  atomic failpoints, idempotency/drift, and database reopen.
- The task plan records migration 013 and contains no seeded-authority shortcut.
- Focused and baseline non-regression checks pass; independent reviewer accepts both authority
  decoupling and suspension evidence.

**Promotion decision:** continue only if the continuation is a consumer of persisted confirmation
authority and creates no effect. Pivot the FK migration if it changes legacy semantics. Stop the
runtime-managed execution claim if attempts still structurally require legacy authority.

**Non-regression carried forward:** all L0/L1 authority, replay, atomicity, opening fence, and
no-premature-effect guarantees remain intact; compatibility cannot grant runtime authority.

### L3 — TASK-CONT-002: deterministic same-session feedback path

**Decision question:** After this layer, we know whether two exact official bus contributions can
drive one same-session fake-adapter author turn without chat supervision.

**Minimum working unit:** scheduler plus canonical input materialization and one fake resumable
adapter path for the fixed confirmed graph.

**Included scope**

- Resolve each preallocated source message through official contribution, verified receipt,
  publication candidate, and completed attempt, with exact dispatch/operation/seat/round/turn/type
  matching.
- Materialize target input in the fixed order: reconstruction base, official author output,
  official reviewer output, frozen revision instruction.
- Atomically accept finalized input metadata, target attempt, materialized invocation, request
  binding, event, and one unclaimed fake-adapter effect.
- Deterministic scheduler evaluation, same-seat/same-instance resume, retry and crash/reopen
  convergence, and candidate/raw/host/cross-dispatch/ambiguous-source negatives.

**Explicitly deferred**

- Definitive-loss reconstruction, unknown reconciliation, cancel/expiry, real provider retention,
  multi-host claiming, production deployment, and reusable multi-profile packaging.

**Operator-visible result:** after confirmation and official author/reviewer publication, the local
runtime reaches author turn 1 without chat supervision or agent bus polling.

**Risk reduced:** nondeterministic source selection, provider-memory-only correctness, duplicate
target effects, and a chat-owned scheduler.

**Main cost drivers:** authoritative joins, exact input artifact construction, scheduler/event
coordination, fake adapter/worker harness, effect idempotency, and restart tests.

**Exit evidence**

- T-ACI-CONT2..4 and the happy-path/restart portion of T-ACI-CONT8 pass.
- Golden input bytes prove the exact four-entry order and exact official source hashes.
- Repeated scheduler evaluation and crash/reopen produce one target attempt and one claimable effect.
- End-to-end local witness starts from CONF-001-created authority and never reads legacy authority or
  asks the chat/agents to poll.
- Focused and baseline non-regression checks pass; independent reviewer accepts.

**Promotion decision:** continue to recovery hardening only after the deterministic local loop is
repeatable. Pivot the scheduler or input seam if retry evidence diverges. Do not infer real-provider
support from the fake adapter.

**Non-regression carried forward:** exact confirmation provenance, no legacy authority, frozen
mapping identity, official-only inputs, verified-opening fence, and at-most-one claimable effect.

### L4 — TASK-CONT-003: failure and recovery hardening

**Decision question:** After this layer, we know whether every admitted loss, uncertainty,
cancellation, expiry, crash, and race converges without duplicate physical work.

**Minimum working unit:** explicit reconstruction, unknown reconciliation, cancellation/expiry,
exhaustive transition validation, and full failpoint/reopen matrices on the L3 slice.

**Included scope**

- Reconstruction only for `capability_absent_no_handle` or
  `handle_definitively_unavailable_no_start`, with one replacement instance/attempt and unchanged
  canonical input semantics.
- Unknown outcome blocks automatic replacement; only reconciliation or cancellation may advance it.
- Cancellation before claim atomically revokes claimability; claimed cancellation reconciles the
  target; expiry after claim routes through cancellation.
- Exhaustive state/event rejection for every unlisted pair, resume/reconstruct/cancel race matrices,
  all internal failpoints, SQLite reopen, replay, and unique terminal outcome evidence.

**Explicitly deferred**

- Real Codex adapter admission, measured handle retention, durable provider cancellation proof,
  multi-host execution, generalized skill/profile graphs, UI productization, deployment, and scale.

**Operator-visible result:** the bounded local workflow resumes/reconstructs once or stops with a
durable explicit reason; it never silently duplicates work after uncertainty.

**Risk reduced:** duplicate provider work, unsafe automatic fallback, stranded claimable effects,
invalid lifecycle mutation, and false success/terminalization.

**Main cost drivers:** complete event/state/race cross-product, failure injection, fake adapter
observation semantics, reconciliation logic, closure verification, and independent audits.

**Exit evidence**

- T-ACI-CONT5..9 pass, including exhaustive invalid transitions and every crash boundary.
- Unknown, cancellation, expiry, resume, and reconstruction races elect one allowed outcome and at
  most one physical-work lineage.
- Reopen/replay preserves exact authority/input lineage and creates no duplicate attempt/effect.
- Feature verification, alignment, and layering audits publish bounded verdicts; they do not convert
  the known unrelated full-suite drift into PASS.
- Independent reviewer accepts the L4 diff and evidence; all L0-L3 regression suites remain green.

**Promotion decision:** a separate L2 real-provider plan may begin only after this local safety claim
passes. Remediate or stop if unknown outcome or cancellation can create a second work lineage.

**Non-regression carried forward:** all earlier authority, atomicity, replay, decoupling,
official-input, no-polling, and single-effect guarantees remain true in every terminal path.

## Implementation Wave Backbone

| Wave | Target layer | Goal | Key artifacts | Required verification |
|---|---|---|---|---|
| CW0 | L0 | Close executable confirmation semantics | CONF-000 contract delta, admitted fixture, golden/negative vectors, traceability, review | Exact-byte/digest reproduction, closed mutation corpus, independent contract review |
| CW1 | L1 | Persist one confirmation authority atomically | Migration 012, writer/service boundary, generic effect intent, focused tests, evidence report | Golden equality, identity replay/conflict, every failpoint, after-commit retry, concurrency, reopen, reviewer PASS |
| CW2 | L2 | Remove legacy authority dependency and persist effect-free suspension | Legacy-FK migration/compatibility evidence, migration 013, continuation reducer/service/tests | Runtime/legacy isolation, T-ACI-CONT1, base CONT9, failpoints, reopen, reviewer PASS |
| CW3 | L3 | Prove the deterministic same-session loop | Continuation runtime/scheduler, input materializer, fake adapter, happy-path evidence | T-ACI-CONT2..4 and CONT8 happy path/restart, exact input bytes, one attempt/effect, reviewer PASS |
| CW4 | L4 | Prove safe degraded modes and convergence | Reconstruction/reconciliation/cancel/expiry implementation, race/failpoint evidence, closure audits | T-ACI-CONT5..9, full reopen/race matrix, prior-layer regression, independent review/audits |

No wave may share a mutation writer with a later wave. Each code SWU retains the work pack's
single-writer topology: read-only auditors before mutation, one coder, and a different independent
verifier after tests.

## Non-Regression Guardrails

- Human approval is the authority; a chat message, UI action, policy evaluation, legacy marker, or
  caller-supplied graph becomes authoritative only through the same trusted, exact-digest
  confirmation boundary.
- The three digests remain distinct and are never substituted for one another.
- The confirmed graph is exactly three nodes and two declared execution edges with loop ceiling one;
  continuation input has exactly two official source mappings in fixed order.
- Same dispatch and same confirmed-authority digest return the first receipt; changed authority is a
  permanent conflict, including concurrent and lost-response retries.
- Confirmation is one SQLite/journal transaction; replay never repeats effects.
- CONF-001 ends at `opening_pending` with one unclaimed audit-opening intent. No agent/provider/tool
  effect is eligible before verified audit opening.
- `dispatch_links` may remain compatibility data but cannot confirm a dispatch, authorize a mapping,
  or satisfy O-CONT-S5; complete runtime-managed execution requires legacy-FK decoupling.
- Suspension is parked state, not a running process, listener, inbox, or bus-poll loop.
- Same-session continuation is an optimization; exact reconstruction evidence remains the
  correctness boundary.
- Unknown physical outcome never starts reconstruction automatically; at most one replacement is
  allowed after definitive no-start evidence.
- Every layer runs its focused suite and all prior-layer suites. The full-suite signature may not
  regress, and the unrelated existing drift cannot be repaired opportunistically or described as a
  feature PASS.

## Promotion and Readiness Rules

1. CONF-000 review PASS authorizes CONF-001 code entry; it does not authorize continuation code.
2. CONF-001 focused PASS plus independent implementation review permits reissuing readiness, but
   TASK-CONT-001 remains blocked until the plan allocates migration 013 and removes seeded authority.
3. Legacy-FK decoupling must be accepted before any complete runtime-managed attempt-path claim and
   before L3 begins.
4. Each continuation task begins only after its predecessor's evidence and reviewer verdict exist.
5. L4 completion supports only a bounded local SQLite/fake-adapter capability claim. Real provider,
   production, multi-host, and generalized-graph claims require separate layering and evidence.

## Open Decisions

- Which exact host adapter or wrapper emits the canonical confirmation observation in the first chat
  path; this may change transport mechanics but not L0 authority semantics.
- The precise compatibility migration for existing `dispatch_links` foreign keys and whether legacy
  bindings use a neutral dispatch-identity parent or split legacy/runtime parent columns. It must be
  decided and reviewed within CW2 before mutation.
- Whether audit-opening materialization is scheduled between L1 and L2 for an executable source
  attempt fixture. It is not part of CONF-001, and no later agent start may bypass the verified
  opening fence.
- Repair ownership and schedule for the unrelated full-suite Stage-E/fixture drift.

## Recommended Next Layer

Start **L0 / CONF-000**. Its narrow outcome is a reviewed canonical fixture and golden vector that
makes the approved authority decisions executable. The most important deferral is all runtime code,
including migration 012 and the writer, until that evidence passes. The most important later
boundary is that CONF-001 stops at durable `opening_pending`; external audit materialization,
continuation, and provider work do not belong in the writer proof.
