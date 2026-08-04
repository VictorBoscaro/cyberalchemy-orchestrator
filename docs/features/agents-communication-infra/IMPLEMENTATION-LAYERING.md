---
module: agents-communication-infra
version: current
status: draft
updatedAt: 2026-07-23
docType: implementation-layering
owners: [architecture_owner, product_protocol_owner, host_operator_owner, root_final_approver]
---

# Implementation Layering: Agents Communication Infra

## Purpose

Turn the current skill-led dispatch flow into a recoverable runtime without weakening the
existing human-confirmation and audit-ledger guarantees. Each layer answers one decision before
the next layer adds provider, portability, or recipe complexity.

## Target and scope

- **Target:** `agents-communication-infra`.
- **Scope:** single-host, single-tenant orchestration runtime and its migration path.
- **Current state:** partially implemented. Pending sheets, human confirmation markers, the
  validated audit-ledger appender, read APIs and disk-watching SSE already exist. Journal, kernel,
  outbox, runtime adapters and protocol buses do not.
- **Source architecture:** [README.md](README.md), especially sections 3, 4, 9, 11, 12 and 14.
- **Source discovery:** [discovery/feature-discovery/agents-communication-infra.md](discovery/feature-discovery/agents-communication-infra.md), which owns the migration problem, candidate decisions and OQ trace.
- **Executable plan:** [WORK-PACK.md](WORK-PACK.md).

## Layer boundary rule

Every boundary uses: `After this layer, we know whether ...`. Promotion requires the named exit
evidence; completing tasks without that evidence does not promote the layer.

## Layer decision table

| Layer | Decision question | Minimum working unit | Included scope | Explicitly deferred | Operator-visible outcome | Risk reduced | Main cost drivers | Exit evidence | Promotion decision |
|---|---|---|---|---|---|---|---|---|---|
| **L0 — protocol proof** | After this layer, we know whether one confirmed dispatch can be journaled, opened in the audit ledger, executed deterministically, closed and replayed without duplicate logical effects. | One run, one group, two fixed seats, deterministic fake adapters, fixed `collect -> reveal -> vote -> commit`, opening/close materializers and query endpoint. | SQLite/WAL journal; conditional append; command dedupe; pure reducer; **minimal durable effect outbox and reconciliation for opening, fake execution and close**; current appender as sole audit-ledger writer; restart replay. L0 is gated internally as 0A contracts, 0B journal, 0C opening barrier, 0D lifecycle bridge, 0E fixed group protocol. | Real providers; arbitrary recipes; UI operation; rich deliberation; cancellation; checkpoints; distributed workers; large artifact service. | A fixture run reaches one official terminal result and can be reconstructed after restart with the same state hash. | Invalid authority split, non-replayable state, ledger-before-execution breach, cross-store crash gap and duplicate terminal facts. | Persistence schema, event contracts, reducer/kernel, materializer reconciliation, crash-boundary tests and golden legacy rows. | Continue only if replay, duplication, clock and ledger-barrier tests pass. Otherwise simplify or pivot the runtime model. |
| **L1 — recoverability, sealing and observation** | After this layer, we know whether the protocol remains private, recoverable and observable under failure and concurrency. | L0 slice plus one bounded deliberation round, phase ACL, durable outbox/reconciler, deadline/cancel races and cursor-based SSE. | Read-policy enforcement; reveal barrier; crash recovery; reconciliation states; minimal read-only sandbox and credential boundary; incremental runtime projection. | Real provider semantics; provider portability; recipe registry; mutating tools; multi-host leases. | An operator can reconnect, see authoritative progress and repair/retry pending projections without exposing sealed peer content. | Early reveal, hidden partial failure, stale UI authority, unsafe retries and race-created double terminals. | Fault injection after every append/effect boundary; sealing matrix; SSE gap recovery; race traces; reconciliation fixtures. | Continue only if every allowed race has one terminal winner and all alternate channels enforce sealing. |
| **L2 — one real provider** | After this layer, we know whether the runtime contract can control one nondeterministic provider without losing replay, safety or resource bounds. | One CLI adapter satisfying the canonical adapter contract against one fixed read-only protocol fixture. | Idempotent start/reconciliation/cancel; structured-output validation; immutable provider observations; read-only tool profile; budgets for time, tokens, payload, disk and queue. | Second provider; mixed groups; generic recipes; mutating code tasks; provider-independent semantic equality. | A real run is observable through the same states/events as the fake adapter and fails explicitly when output or limits are invalid. | Unknown external effects, malformed/late results, host credential leakage and unbounded consumption. | Adapter conformance suite, credential/sandbox inspection, failure injection and resource-limit receipts. | Proceed to portability only after the product-value experiment is preregistered and L2 safety gates pass. |
| **L3 — portability and product value** | After this layer, we know whether a second provider can participate through the same protocol and whether the multi-agent protocol earns its added cost. | Second CLI adapter, one mixed-provider group and a preregistered comparison against a single-agent baseline. | Capability matrix; mixed-provider conformance; quality/dissent/false-consensus/cost/latency/recovery evaluation. | Provider-specific kernel branches; semantic identity of model outputs; production scale; open recipe registry. | The same runtime runs fake, provider A, provider B and a mixed group, with an explicit continue/simplify/stop decision. | Vendor coupling and an expensive architecture with no demonstrated product value. | Common contract suite plus signed/preregistered evaluation report and decision threshold. | Continue only if operational equivalence holds and the value gate meets its preregistered threshold. |
| **L4 — composition and recipes** | After this layer, we know whether the proven runtime can compose reusable workflows without specializing the kernel. | Two sequential groups and two immutable built-in read-only recipes (`research` and `review`). | Sequential handoff dedupe; recipe digests; compiler from built-in recipe to canonical `DispatchSpec`; compatibility cutover for skills/UI. | Namespaced user recipes; `feedback`/`zig-zag`; mutating `code`; knowledge promotion; multi-tenancy; distributed execution. | Skills and UI submit the same canonical spec and the kernel executes two workflow types without `if research/review` branches. | Parallel runtimes hidden in skills, schema drift and business semantics leaking into the kernel. | Recipe/compiler contract tests, sequential recovery test, skill/UI migration receipt and kernel branch audit. | Pilot the runtime; do not open the registry until supply-chain and override ADRs are accepted. |

## Non-regression guardrails

1. Human confirmation remains explicit; silence, marker discovery or UI connection is not consent.
2. No provider or tool effect starts before an identical audit-ledger opening row is verified.
3. The current validated appender remains the only physical writer of the audit ledger.
4. The audit ledger remains append-only and backward-compatible; runtime events never leak into it.
5. Journal replay reduces persisted facts only; it never calls providers, tools or materializers.
6. Every logical command, contribution, handoff and terminal result has one acceptance key.
7. Realtime and query projections are reconstructible and never become workflow authority.
8. Later layers retain state hashes and fault fixtures from all earlier layers.
9. A layer may add one bounded improvement theme but may not silently pull later-layer scope forward.
10. The CVR adjunct never imports or adds routes to `implementations/server/`, mutates canonical
    sources, emits runtime/APT/bus facts, or treats an inventory/cache as authority.

## CVR adjunct boundary

**Decision sentence:** after this adjunct, we know whether admitted Markdown bytes can produce a
deterministic, bounded, effect-free artifact projection before edge identity or transport is added.

| Unit | Value gained | Main cost | Promotion evidence | Current state |
|---|---|---|---|---|
| `SWU-ACI-CVR-000` | Parser, scope, limits, module and delivery contracts become reviewable. | Owner/reviewer time and unresolved authorization. | Exact-document review plus named owner/root acceptance. | Documentation prepared; not accepted as implementation authority. |
| `SWU-ACI-CVR-GUARD-001` | Pure verification, closed descriptors and direct worker invocation become executable. | External trusted bootstrap with exactly one external authority-owned bootstrap finalizer, canonical schemas and crash tests. | Exact one-time root bootstrap, authenticated external AuthorityLaunchContext, target-filesystem CAS proof plus T-CVR-AUTH1–5. | Blocked pending packet acceptance and external trust prerequisites. |
| `SWU-ACI-CVR-001` | Capture/snapshot, artifact list/get and raw Connections declaration preservation become executable. | Restricted loader, dependency lock, canonical digest vectors, confinement/privacy and zero-effect tests. | Applicable artifact/raw-declaration T-CVR receipts and terminal scoped receipt. | Blocked by global and nominal gates. |
| `SWU-ACI-CVR-002` | Endpoint resolution and logical edges extend the same core. | Resolution and predecessor-baseline fixtures. | CVR-001 PASS/baseline, delta/prehash proof, full CVR-001 rerun and T-CVR-AUTH6. | Deferred and blocked. |

The order is strict: `000 -> GUARD-001 -> 001 -> 002`. CVR is an adjunct to L0, not evidence that L0, TASK-000
or W0 passed. Promotion must retain the preceding unit's golden vectors, source authority,
admission parity, complete-call bounds, import isolation and zero-effect proofs.
The descriptor-bound per-SWU branch is non-operative until the coordinated packet is accepted.
GUARD-001 then uses a non-recursive external trusted bootstrap; later workers run only through the
guard. Each execution has exactly three content-addressed authority artifacts and one
authority-created terminal receipt. Descriptors are governance entries, not execution artifacts.
The immutable claim is the only lease; the launch context is external/ephemeral and only its digest
enters the receipt. Workspace hashes prove integrity, not authenticated identity. The unrestricted
host boundary is advisory, not a sandbox.

## Protocol Governance adjunct boundary

**Decision sentence:** after this adjunct, we know whether one frozen, digest-bound
skill/profile/binding/recipe/invocation package can compile deterministically to a
non-authoritative candidate/result without acquiring confirmation or runtime authority.

| Unit | Value gained | Main cost | Promotion evidence | Current state |
|---|---|---|---|---|
| `SWU-ACI-PROTOCOL-COMPILATION-001` | Pure closed compilation, exact two-case admission and a separate idempotent ArtifactStore seam become executable. | Strict canonical/schema/digest/graph validation, PC1–PC12 harness and independent audit/verification. | Refreshed exact-SWU readiness receipt; resolved brownfield findings; exact nine-path diff including mandatory Stage-E integrity closure; T-ACI-PC1–PC12 and full runtime suite PASS; verifier PASS. | Complete for the bounded SWU; no L3/L4, confirmation or execution promotion. |

This is an independent **L0 Protocol Governance adjunct**. It neither proves the L0 runtime slice
nor enters/promotes W6, L3 or L4. It does not reuse the historical `ACI-030` recipe-compiler
placeholder. Its authority ceiling is canonical `DispatchCandidate`/compile-result bytes plus
optional artifact metadata; capability resolution, final `DispatchSpec`, confirmation,
`ConfirmedDispatch`, `Run`, scheduler, provider/tool effects, routes, production and cutover remain
outside the unit.

## Recommended next layer

- **Next layer:** L0.
- **First gate:** complete Wave W0 decisions and promote the work-pack from `block` to `pass` for
  L0 mutation.
- **Key decision unlocked:** whether the current dispatch discipline can be represented as a
  deterministic, replayable runtime while preserving the audit-ledger authorization barrier.
- **Major deferred scope:** real providers, agent-to-agent deliberation depth, generic recipes,
  mutating tools and distributed infrastructure.
