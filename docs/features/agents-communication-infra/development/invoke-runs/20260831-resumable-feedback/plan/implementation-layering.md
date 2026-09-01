---
title: Resumable Dispatch Feedback Implementation Layering
status: draft
updatedAt: 2026-08-31
owner: agents-communication-infra
scope: capability
---

# Resumable Dispatch Feedback Implementation Layering

This model sequences the bounded `author:0 -> reviewer:0 -> author:1` continuation capability. L0
is the smallest runtime proof; later layers preserve its deterministic input and journal-authority
guarantees while adding failure handling, a real host adapter and broader reuse.

## Context

- Target: deterministic resumable feedback dispatch.
- Current state: brownfield runtime with SQLite journal, official bus contributions, atomic attempt
  materialization and fake-first testing; no continuation persistence or adapter worker exists.
- Primary operator: the person confirming a dispatch and expecting it to finish without chat-agent
  supervision.
- Primary constraint: correctness must not depend on implicit provider memory or an agent polling the
  bus.
- Sources: [ACI-CONT-001](../../../../../../decisions/aci-resumable-agent-continuation.md),
  [capability contract](../../../../specs/capabilities/resumable-agent-continuation.md),
  [TEST-SPEC](../../../../TEST-SPEC.md#bounded-resumable-feedback), and the
  [host probe](../probes/host-continuation-probe.json).

## Layer Boundary Heuristic

```text
Layer value = decision unlocked + operator-visible outcome + risk reduced
Layer cost = implementation time + verification time + coordination burden
```

A layer stops once additional work no longer answers its decision question more cheaply than the
next layer. Promotion requires exit evidence; later layers must retain every earlier guarantee.

## Layer Decision Table

| Layer | Decision question | Minimum working unit | Operator outcome | Principal risk reduced | Promotion |
|---|---|---|---|---|---|
| L0 | After this layer, we know whether the journal can deterministically drive one same-session author-reviewer-author loop without the chat orchestrator. | SQLite continuation/mapping state, official-output materialization, scheduler reaction and a fake resumable adapter for the happy path. | One confirmed fixture reaches author turn 1 from journal facts alone. | The core bus-to-next-agent handoff may be unimplementable or non-atomic. | Continue only if T-CONT1-4/8 happy-path cases and restart replay pass. |
| L1 | After this layer, we know whether the same slice fails safely and converges after crashes. | Definitive-loss reconstruction, unknown reconciliation, cancellation, expiry, exhaustive invalid transitions and failpoints. | The bounded run either resumes once or stops with an explicit durable reason. | Duplicate provider work, stranded state and false terminalization. | Promote only if T-CONT5-9 and crash/reopen witnesses pass. |
| L2 | After this layer, we know whether a real host can preserve or explicitly lose a provider session under the same contracts. | One admitted Codex-host adapter with resume/status/dispose/cancel observations and retention measurements. | Real same-agent continuation when supported; explicit reconstruction or block otherwise. | Fake-adapter assumptions do not hold at the host boundary. | Promote only with live same-session, definitive-loss, unknown and cancellation evidence. |
| L3 | After this layer, we know whether continuation is reusable across skills and adapters without new kernel branches. | Capability-based dispatch compilation, a second conforming adapter and packaged operator controls. | Any eligible skill may request the same bounded feedback topology. | Capability leakage, provider branching and one-off workflow coupling. | Pilot only after conformance, migration and operational evidence. |

## Capability Progression

| Area | L0 | L1 | L2 | L3 |
|---|---|---|---|---|
| Dispatch graph | One fixed finite turn graph | Same graph with all race outcomes | Same graph on one real host | Capability-derived bounded graphs |
| Input delivery | Two exact official contributions | Corruption, ambiguity and replay negatives | Same bytes through real adapter | Provider-equivalent conformance |
| Continuation | Same-session fake handle | Unknown, reconstruction, cancel, expiry | Real opaque host handle | Multiple admitted adapters |
| Operations | Local deterministic witness | Restart/failpoint recovery | Host retention and cancellation runbook | Reusable pilot packaging |

## Layer Definitions

| Layer | Included | Explicitly deferred | Exit evidence | Value/cost note |
|---|---|---|---|---|
| L0 | New migration, domain/reducer, suspend/resume commands, journal-derived scheduler, deterministic input mapper, fake adapter and T-CONT1-4 plus happy-path T-CONT8 | Reconstruction, unknown outcome, real provider, arbitrary cycles | Focused tests, SQLite reopen witness, independent code review | Smallest slice proving the chat orchestrator can leave the execution path. |
| L1 | Reconstruct/cancel commands, unknown and deadline behavior, all invalid transitions, all atomic failpoints | Real provider, scale, generic cycles | T-CONT5-9, full runtime regression, independent review | Failure correctness is worth adding only after the handoff works. |
| L2 | Codex-host adapter, reconciliation observations, retention/cancel probes, operator diagnostics | Second provider and general skill routing | Live evidence bundle and adapter conformance review | Host uncertainty dominates only after the kernel is proven. |
| L3 | Capability/profile integration, second adapter, migration/pilot controls | Open-ended conversations, generic inbox, unbounded loops | Cross-skill and cross-adapter conformance witness | Reuse and packaging are expensive before host semantics are known. |

## Layer Delivery Backbone

These `LW*` identifiers describe promotion between implementation layers. They are distinct from
the Work Pack's concrete execution waves `W0` through `W3`.

| Layer wave | Layer | Goal | Primary artifacts | Verification |
|---|---|---|---|---|
| LW0 | L0 | Persist and reduce continuation state | migration, continuation module, service command surface | state/transaction unit tests and reviewer |
| LW1 | L0 | Complete official-output-to-resume happy path | input mapper, scheduler, fake adapter | T-CONT1-4/8 happy path and integrated witness |
| LW2 | L1 | Harden degraded modes and replay | reconstruct/cancel/reconcile commands and failpoints | T-CONT5-9, SQLite reopen and regression suite |
| LW3 | L2 | Admit one real continuation adapter | host adapter and evidence package | live probes, negative cases and admission review |
| LW4 | L3 | Package skill/adapter reuse | compiler/capability integration and second adapter | cross-skill/provider conformance |

## Non-Regression Guardrails

- A suspended continuation owns no running attempt, listener or bus-read capability.
- Only official receipt-verified contributions satisfy frozen mappings.
- Effective input is exact and canonical even when same-session provider memory exists.
- Unknown physical outcome never authorizes replacement.
- Every external action originates in one durable pending effect; replay itself performs no effect.
- Provider-specific behavior remains behind `AgentAdapter`; the journal writer alone accepts state.

## Recommended Next Layer

Implement L0 in two sequential single-writer units: persistence/reducer first, then the exact
official-output materialization and fake-adapter same-session witness. Each unit receives two
read-only pre-code auditors, one coder and one independent post-code verifier. Do not begin the real
Codex adapter until L1 proves loss, unknown, cancellation and restart convergence.

## Open Decisions

- Real Codex continuation-handle retention duration and restart survival remain empirical L2 facts.
- L3 must decide which skill-profile obligation requests this capability; `dispatch_type` is not
  assumed to be that mechanism.
- Production cutover and multi-host effect claiming remain outside this layering model.
