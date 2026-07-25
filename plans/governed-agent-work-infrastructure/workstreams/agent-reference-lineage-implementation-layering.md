---
tags: [plans, agent-reference-lineage, implementation-layering, aci, apt]
node_type: plan-workstream
title: Agent Reference Lineage Implementation Layering
status: draft
version: 0.1.0
last_updated: 2026-07-25
owner: governed-agent-work-infrastructure
scope: capability
owning_plan: plans/governed-agent-work-infrastructure/PLAN.md
authority:
  decision: docs/decisions/host-agent-dispatch-input-binding.md
  selected_option: A
---

# Agent Reference Lineage Implementation Layering

This workstream sequences the specified, not implemented Agent Reference Lineage capability. Layer
0 is the smallest authority-bearing proof. Each later layer adds one decision-relevant capability
and preserves all earlier evidence boundaries.

## Context

- Target: `Agent Reference Lineage implementation`.
- Current state: the ACI and APT contracts are specified; the bounded Option-A host workflow bridge
  exists; target delivery, the ACI evidence reader and the APT lineage Query are not implemented.
- Primary operator: an authorized internal reviewer querying which references were delivered to,
  observed by and declared by one owner-resolved agent target.
- Primary constraint: preserve ACI, host and APT ownership while proving the smallest useful local
  slice before adding access observations or broader hardening.
- Governing decision: accepted
  [Option A](../../../docs/decisions/host-agent-dispatch-input-binding.md#decision), the bounded
  host-workflow binding bridge. This plan does not reopen Option A versus the general invocation
  pipeline.

## Layering Method

- Minimum proof: first establish an ACI-owned, source-bound target-delivery/effective-input fact
  that can be read back through a complete evidence wrapper.
- Decision-first: each layer answers one question that unlocks or blocks the next layer.
- Progressive hardening: APT projection, host access evidence and end-to-end hardening remain
  distinct.
- Non-regression: a later layer cannot collapse delivery, access, declared use, relation or check.
- Evidence-gated promotion: contract tests ship with the layer whose claim they verify.

## Layer Boundary Heuristic

```text
Layer value = decision unlocked + operator-visible outcome + risk reduced
Layer cost = implementation time + verification time + coordination burden

Stop the layer when the next unit adds less value-per-cost to the current
decision than starting the next decision layer.
```

## Layer Decision Table

| Layer | Decision question | Minimum working unit | Operator-visible outcome | Risk reduced | Main cost drivers | Promotion decision |
|---|---|---|---|---|---|---|
| L0 — ACI settlement proof | After this layer, we know whether the bounded Option-A attempt binding can accept and replay one exact Scout bundle as an ACI-owned target delivery and effective-input entry. | `AgentReferenceDelivery` + `EffectiveInputEntry.reference_bundle` + target-delivery event + complete evidence reader, with `T-ACI-R22`/ARD contract tests. | An owner-authenticated Attempt has durable, read-only proof of exact bundle membership and input inclusion. | Removes ambiguity between Scout lifecycle delivery and target-attempt delivery. | Atomic journal/artifact settlement, canonical manifest, capability-derived identity, retries and crash tests. | Promote when exact retry, drift, crash and evidence-boundary tests pass. |
| L1 — APT deterministic projection | After this layer, we know whether APT can produce deterministic per-agent lineage from complete ACI and host activation-binding evidence while the host source-access contract remains unavailable. | Host-owned `AgentActivationBinding/producer_resolution`, Query binder, pure reducer, mapper and port for `AgentReferenceLineage`, with the closed SourceObservation `unavailable` branch. | Authorized reviewers see recommendation, delivery/effective input, declared use, relation and check axes; access is honestly empty. | Removes inferred producer joins and reducer-time owner calls. | Complete wrappers, seven digests, host activation-binding coordination, replay/as-of behavior and synchronized R9 contract tests. | Promote when producer-resolution plus R9 unavailable-path tests and deterministic replay/mapping pass. |
| L2 — Host access authority | After this layer, we know whether the host can author an exact observation-to-delivery/recommendation/Attempt manifest without transferring access authority to APT. | Versioned `available` host observation manifest and binder integration, with malformed/cross-target/coverage tests. | Verified access observations appear on the correct delivered recommendation line with original coverage. | Removes false access claims from raw Stage-G or locator similarity. | Host schema/versioning, target/origin evidence, H_HOST manifest and compatibility behavior. | Promote when host owner tests and APT available-path tests pass without changing L0/L1 results. |
| L3 — E2E hardening and observability | After this layer, we know whether the complete local capability survives replay, crash, tamper and diagnostic failures without leaking raw content or gaining a second authority. | Cross-layer scenario suite, recovery/checkpoint proof, safe signals and operational runbook evidence. | A local operator can diagnose and replay the complete lineage path predictably. | Reduces integration, recovery, privacy and observability-authority risk. | Failure injection, checkpoint parity, performance bounds, redaction and support artifacts. | Admit the bounded local capability when all owner and E2E receipts pass; broader rollout remains separate. |

## Capability Progression

| Capability / scope | L0 | L1 | L2 | L3 |
|---|---|---|---|---|
| Target identity | ACI capability-derived Dispatch/Attempt/seat/agent instance | APT consumes the ACI target wrapper and the host-owned activation/producer wrapper | Host observation manifest binds the same tuple | Cross-layer tamper/replay proof |
| Reference evidence | Commit + immutable bytes + lifecycle delivery + target delivery + effective input | Canonical per-target delivered lines | Exact host observation origin joins access axis | E2E replay, recovery and privacy |
| Evidence axes | Delivery only; explicitly not access/use/support | Delivery, declared use, relation and check remain distinct; access empty | Access becomes available but remains independent | Non-implication and non-authority regression suite |
| Verification | `T-ACI-R22`, `T-ACI-ARD1..5` and atomic fault matrix | Synchronized `APT-R9`/`R9-01..11` producer-resolution, unavailable-SourceObservation and mapping tests | R9 host-available/malformed/cross-binding tests | Full owner-contract, fault, checkpoint and observability suite |

## Layer Definitions

| Layer | Objective | Builds on | Included scope | Explicitly deferred | Exit evidence | Value/cost note |
|---|---|---|---|---|---|---|
| L0 | Prove exact ACI target-input settlement and complete read evidence. | Accepted Option-A host binding and existing Scout lifecycle facts. | ACI domain persistence, atomic acceptance, target-delivery event, reference-bundle input entry, evidence reader, contract tests. | APT Query, host access manifest, general invocation pipeline, provider adapter, production rollout. | Passing T-ACI-R22/ARD1..5, retry/drift/crash matrix, independent ACI reviewer and contract-test reviewer. | Smallest slice that creates the authority APT must later consume. |
| L1 | Project ACI delivery plus host-bound producer identity and APT facts deterministically. | L0. | Host `AgentActivationBinding/producer_resolution`, binder, pure reducer, seven pinned digests, SourceObservation unavailable union, query interface/mapper and tests. | Host available source observations, scale and operational dashboards. | Current Query/Rule/Interface/TEST-SPEC synchronization receives a fresh cross-document PASS; then producer-wrapper and R9-01..11 applicable cases, replay parity and zero reducer I/O pass. | Proves usefulness without waiting for access instrumentation while retaining independent producer authority. |
| L2 | Add owner-authoritative access observations. | L0 and L1. | Host schema, versioned manifest, target/origin bindings, binder validation and tests. | Provider-hidden inputs, automatic truth/adjudication and broad ingestion redesign. | Host contract receipt plus R9-07/R9-08 and cross-owner negative cases. | Pays coordination cost only after the delivery/read path is proven. |
| L3 | Harden the integrated local capability. | L0–L2. | Crash/restart/replay, checkpoints, safe observability, performance bounds and runbook evidence. | Production SLOs, multi-host durability and general provider pipeline. | Cross-layer evidence receipt and independent final review. | Operational cost is justified only after all three ownership boundaries work. |

## L0 Minimum Working Unit

### Goal

Accept one already committed and lifecycle-delivered Scout bundle into one authenticated,
same-Dispatch target Attempt, finalize its exact `reference_bundle` input entry, commit the delivery
and attempt facts atomically, then read the complete owner-authored evidence back without inferring
access or use.

### Included Scope

- Consume the accepted Option-A host envelope only for its confirmed Dispatch/group/seat/attempt and
  host-observable manifest binding; do not reinterpret it as complete provider input.
- Preallocate delivery and target-event identities before manifest canonicalization.
- Verify source commit, immutable bundle bytes/order/digest and distinct lifecycle-delivery event.
- Atomically accept `AgentReferenceDelivery`, effective-input metadata, target-delivery event,
  `attempt.requested` and the existing sealed-request/effect members required by ACI.
- Expose complete, versioned target-resolution and delivery evidence through the ACI-owned reader.
- Implement contract tests concurrently with each contract branch.

### Explicitly Deferred Beyond L0

- `AgentReferenceLineage` binder/reducer/port and all APT query behavior.
- Host `AgentActivationBinding/producer_resolution` and its APT binder/tests.
- The host `available` observation manifest and any claim of access.
- The general `AgentInvocationPlan → MaterializedAgentInvocation → AgentExecutionRequest` program.
- Provider admission, automatic launch, UI, production deployment and new telemetry.

### Exit Evidence

- `T-ACI-R22` and `T-ACI-ARD1..5` executable cases pass.
- Atomic failpoints show all settlement members or none; exact retry is stable and canonical drift
  conflicts.
- Evidence-reader fixtures reject omission, extra/future members, wrong scope/version/digest and
  incomplete groups.
- ACI implementation reviewer and independent contract-test reviewer both return PASS.

### Promotion Decision

- Continue to L1 when all L0 evidence exists and no delivery fact implies access/use/support.
- Pivot to a narrower fixture-only proof if the bounded host Attempt binding cannot satisfy ACI
  identity or atomicity without entering the deferred general pipeline.
- Stop if exact bundle membership or same-Dispatch recipient authority cannot be proven.

## Layer-by-Layer Improvement Model

### L1 over L0

- Added scope: host-owned activation/producer evidence plus deterministic APT Query with source
  access unavailable.
- Hardening delta: complete seven-digest binder manifests, pure replay and forbidden heuristic
  joins.
- Verification delta: obtain a fresh cross-document review of the current synchronized
  `producer_resolution`/seven-digest contract, then exercise exact cardinality,
  omission/extra/duplicate/future/scope/version/digest failures, activation/Attempt binding, R9
  cases, mapping round-trip and zero-external-call assertions.
- Preserved: only ACI proves delivery/effective input; L0 evidence remains immutable.

### L2 over L1

- Added scope: host-owner access observations.
- Hardening delta: exact target/origin binding and versioned coverage semantics.
- Verification delta: malformed wrapper, cross-target, invalid coverage and unavailable/available
  compatibility cases.
- Preserved: APT cannot mint host observations and access does not imply declared use.

### L3 over L2

- Added scope: E2E fault, replay, privacy and operational evidence.
- Hardening delta: recovery, checkpoints, diagnostic non-authority and bounded performance.
- Verification delta: integrated fault matrix and safe observability checks.
- Preserved: all owner boundaries, pure reducer, evidence-axis asymmetry and no locator joins.

## Implementation Wave Backbone

| Wave | Target layer | Goal | Key artifacts | Verification |
|---|---|---|---|---|
| W0 | L0 | ACI delivery/effective-input proof | ACI runtime/storage/reader changes and colocated contract tests | T-ACI-R22/ARD, atomic fault tests, two independent reviews |
| W1 | L1 | APT deterministic lineage | Host activation-binding contract, fresh cross-doc review receipt, binder/reducer/query/mapper and R9 tests | Producer-resolution integrity, R9 unavailable path, replay and mapping |
| W2 | L2 | Host access authority | Host manifest/version/binder changes and tests | R9 available/malformed/cross-binding |
| W3 | L3 | Local E2E hardening | Integrated fixtures, recovery evidence and safe diagnostics | Full cross-layer suite and final review |

## Non-Regression Guardrails

- Option A remains a bounded host-observable bridge and never becomes a claim of complete provider
  input or the general invocation pipeline.
- ACI exclusively owns target delivery, Attempt identity and effective-input inclusion.
- The host exclusively owns activation-to-producer binding; APT consumes its complete
  `producer_resolution` wrapper and never derives it from append-time acceptance alone.
- The host exclusively owns source-access observation; APT only binds and projects it.
- APT reducers perform zero owner, registry, artifact or host calls.
- Recommendation, delivery, access, declared use, claim relation and claim-support check never
  collapse into one boolean.
- Locator, title, digest, text, timestamp, persona and model labels never establish identity.
- Contract tests accompany every layer and cannot be deferred to L3.

## Decision Inventory

- Accepted and not reopened: Option A bounded host-workflow binding bridge.
- Assumption for readiness planning: the existing Option-A confirmed Attempt binding can be exposed
  to L0 through an ACI-owned adapter without claiming general invocation completeness.
- Pending L1 evidence gate, not an L0 blocker: the current APT
  Query/Rule/Interface/TEST-SPEC synchronization for `producer_resolution` and seven digests must
  receive a fresh cross-document PASS before L1 implementation begins.
- Deferrable: exact migration number, module split and internal class names; the L0 owner chooses
  them inside the declared write scope and contract constraints.
- No blocker-level multi-option decision is currently visible.

## Recommendation

Start L0 only. Its proof creates the owner evidence required by every later layer. The most
important deferred scope is the general invocation/provider pipeline; pulling it into L0 would
invalidate the accepted bounded-bridge decision and destroy the layer's value/cost boundary.
