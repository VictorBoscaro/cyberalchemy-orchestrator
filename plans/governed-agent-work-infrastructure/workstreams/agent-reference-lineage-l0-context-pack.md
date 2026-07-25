---
tags: [plans, agent-reference-lineage, context-pack, lean, l0]
node_type: context-pack
status: draft
version: 0.1.0
last_updated: 2026-07-25
task_ref: SWU-ARL-L0-001
mode: lean
strict: true
handoff_pack: none
runtime_handoff: false
---

# Agent Reference Lineage L0 Lean Context Pack

This is a planning context pack for `SWU-ARL-L0-001`. It is not a runtime handoff pack, carries no
execution authority and intentionally emits no JSON/index.

## Context Pack Summary

| Field | Result |
|---|---|
| Task | `SWU-ARL-L0-001` |
| Mode | `lean` |
| Files selected | `8/8` |
| Selector groups | `17` |
| Visible excerpt budget | `16/140` lines |
| Obligation coverage | `8/8` (`100%`) |
| Noise ratio | `0/8` selected files without an obligation (`0.00`) |
| Strict coverage | `pass` for planning/dry-run |
| Runtime handoff | none |
| Output index | none |
| Blockers | `0` |

## Obligation Matrix

| ID | L0 obligation | Required evidence | Coverage |
|---|---|---|---|
| `CTX-L0-01` | Keep Option A closed and preserve its bounded/non-correspondence claim. | Accepted decision plus task non-goals. | covered |
| `CTX-L0-02` | Accept one source-bound, same-Dispatch target delivery with exact bundle membership. | ACI entity and mapping contracts. | covered |
| `CTX-L0-03` | Bind one exact `reference_bundle` entry and finalized effective-input metadata atomically. | ACI domain/mapping plus T-ACI tests. | covered |
| `CTX-L0-04` | Expose complete target/delivery evidence for the APT consumer without reducer owner calls. | APT evidence-reader and Query binder contracts. | covered |
| `CTX-L0-05` | Preserve delivery ≠ access/use/support. | ACI and APT test obligations. | covered |
| `CTX-L0-06` | Put ACI contract tests in L0, including retries, drift, crash and wrapper integrity. | T-ACI-R22 and T-ACI-ARD1..5. | covered |
| `CTX-L0-07` | Keep future changes inside an explicit write/validation scope with independent reviews. | L0 work-pack contract. | covered |
| `CTX-L0-08` | Stop before L1/L2/L3, implementation or external runtime handoff in this session. | Work-pack and accepted decision boundaries. | covered |

## Selected Evidence

### 1. L0 task contract

- Path: `plans/governed-agent-work-infrastructure/workstreams/agent-reference-lineage-l0-work-pack.md`
- Selectors: `SWU Manifest`, `Dependencies`, `Declared Write Scope for Future Execution`,
  `Deliverables`, `Done Criteria`, `Validation Surface`, `Explicit Non-Goals`.
- Obligations: `CTX-L0-01`, `CTX-L0-06..08`.
- Evidence excerpt:

  > Exactly one SWU, L0 only; future execution must block rather than broaden when the Option-A
  > Attempt binding is insufficient.

### 2. Accepted host-input boundary

- Path: `docs/decisions/host-agent-dispatch-input-binding.md`
- Selectors: `Decision`, `Implemented boundary`, `Explicit non-goals`.
- Obligations: `CTX-L0-01`, `CTX-L0-08`.
- Evidence excerpt:

  > Option A is accepted. The bridge binds host-observable repository inputs/outputs and does not
  > claim hidden provider inputs or replace the general ACI pipeline.

### 3. ACI delivery and effective-input entities

- Path: `docs/features/agents-communication-infra/specs/domain.md`
- Selectors: `AgentReferenceDelivery`, `EffectiveInputArtifact`, `EffectiveInputEntry`.
- Obligations: `CTX-L0-02`, `CTX-L0-03`, `CTX-L0-05`.
- Evidence excerpt:

  > `AgentReferenceDelivery` is distinct from Scout lifecycle delivery; it binds immutable bundle
  > membership and one exact target Attempt input entry, but proves no access or use.

### 4. ACI source-to-target mapping

- Path: `docs/features/agents-communication-infra/specs/mappings.md`
- Selector: `ReferenceScoutBundleToEffectiveInput`, including `Validation`.
- Obligations: `CTX-L0-02`, `CTX-L0-03`, `CTX-L0-05`.
- Evidence excerpt:

  > Commit plus immutable bytes own membership. Target capability owns recipient identity. Delivery,
  > effective-input metadata, Attempt and target event accept atomically or not at all.

### 5. ACI test authority

- Path: `docs/features/agents-communication-infra/TEST-SPEC.md`
- Selectors: `T-ACI-R22 — Reference bundle target delivery`,
  `T-ACI-ARD1 — Exact reference bundle delivery` through
  `T-ACI-ARD5 — Delivery evidence boundary`.
- Obligations: `CTX-L0-02`, `CTX-L0-03`, `CTX-L0-05`, `CTX-L0-06`.
- Evidence excerpt:

  > Independently mutate source, recipient, membership, policy, manifest, event and idempotency
  > fields; crash every member boundary; require stable exact retry and all-or-none acceptance.

### 6. APT consumer boundary

- Path: `docs/features/agent-provenance-telemetry/specs/interfaces.md`
- Selectors: `ACIAgentReferenceEvidenceReader`, `ProvenanceQueryPort`.
- Obligations: `CTX-L0-04`, `CTX-L0-08`.
- Evidence excerpt:

  > ACI resolves complete target/delivery wrappers and verifies the exact bundle entry. The reader
  > cannot synthesize delivery, amend the manifest or return raw bytes.

### 7. APT binder/reducer expectation

- Path: `docs/features/agent-provenance-telemetry/specs/queries.md`
- Selectors: `AgentReferenceLineage / Binder Manifest`,
  `AgentReferenceLineage / Formulas and Non-Implication Invariants`,
  `AgentReferenceLineage / Reads From`.
- Obligations: `CTX-L0-04`, `CTX-L0-05`.
- Evidence excerpt:

  > Complete owner-authored wrappers are verified before reduction; the pure reducer receives no
  > owner resolver, artifact reader, bundle bytes or host contract lookup.

### 8. Downstream regression obligations

- Path: `docs/features/agent-provenance-telemetry/TEST-SPEC.md`
- Selectors: `APT-TEST-R9 — Agent Reference Lineage`,
  `R9-03-prefix-and-event-ref`, `R9-04-delivery-membership-input`,
  `R9-07-host-unavailable`, `R9-11-determinism-and-mapping`.
- Obligations: `CTX-L0-04`, `CTX-L0-05`.
- Evidence excerpt:

  > Exact target delivery/effective input is required; lifecycle delivery alone creates no target
  > line; current host access stays unavailable and reducer external-call count is zero.

## Controlling Constraints

1. Authority precedence is repository-owner Option A, then ACI owner contracts for target
   delivery/effective input, then APT consumer contracts. Planning prose cannot override them.
2. L0 may use the Option-A binding only as bounded host-observable input to an ACI-owned adapter.
3. Any need for the general invocation pipeline is `BLOCK`, not implicit expansion.
4. ACI owns target identity, delivery and effective-input inclusion.
5. L0 produces no host SourceObservation access fact and no APT declared-use projection.
6. Complete wrappers fail closed on omissions, extras, future members, wrong
   scope/version/digest, duplicates or incomplete groups.
7. Contract tests and both independent reviews are L0 exit evidence.
8. This session performs no implementation, telemetry mutation or external runtime handoff.

## Compatibility Note

The APT Query/Rule authority and current APT TEST-SPEC are synchronized on the separate host
`AgentActivationBinding/producer_resolution` wrapper and all seven pinned-input digests. This
producer/declared-use path remains outside `SWU-ARL-L0-001` because it belongs to L1, not because of
an unresolved specification gap. Its synchronization still requires a fresh cross-document review
receipt before L1 implementation; that evidence gate does not block this ACI-only L0 dry-run.

## Excluded Candidates

| Candidate | Why excluded from lean pack |
|---|---|
| ACI `operations.md` and `events.md` | The selected ACI domain/mapping/test sections restate the exact L0 atomic unit and event identities; follow their links only if execution finds a contract ambiguity. |
| ACI `interfaces.md` | L0's required owner inputs are closed by the domain/mapping and consumer reader selectors within the eight-file budget. |
| APT `rules.md` | The Query and TEST-SPEC selectors cover the L0-facing owner-wrapper and evidence-boundary obligations; producer-specific behavior is a synchronized L1 concern. |
| Runtime implementation files | This is a contract-first dry-run; the future implementer must inspect only the declared write scope before selecting internal placement. |
| Host ingestion/runtime docs | Host source-access authority is L2 and unavailable in L0/L1. |

## Fallback Exploration Rule

During future execution, expand context only for a named uncovered L0 obligation. The implementer
may follow direct links from the selected ACI mapping to the exact operation/event/interface
section, but must record the new selector and why it closes the gap. Broad repository search,
provider work or L1/L2 context expansion is not authorized.

## Context Result

- Strict coverage: `pass` for planning and local task-session dry-run.
- Contradictions: `0`.
- Missing write scope: none.
- Missing validation surface: none.
- Runtime handoff readiness: `n/a`; no handoff was requested or produced.
- Next action: evaluate the L0 task gates and append the dry-run report to its work-pack.
