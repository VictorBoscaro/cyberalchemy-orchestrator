---
id: agents-communication-infra
feature: Agents Communication Infra
type: queries
title: "Agents Communication Infra — Queries"
status: draft
version: 0.1.0
derived-from: ../discovery/feature-discovery/agents-communication-infra.md@0.2.1
---

# Queries: Agents Communication Infra

Queries reduce accepted facts or read authorized immutable artifacts. They do not contact a provider
to decide state and do not create, repair or advance workflow authority.

## GetRuntimeProjection

**Type:** Query  
**Concept ID:** `agents-communication-infra.GetRuntimeProjection`  
**Reads:** [RuntimeEventEnvelope](domain.md#runtimeeventenvelope), [RuntimeProjection](#getruntimeprojection),
[JournalOffset](domain.md#journaloffset)

### Inputs

| Field | Type | Required | Rule |
|---|---|---:|---|
| `run_id` | opaque ID | yes | caller must be authorized for the run |
| `after_journal_offset` | [JournalOffset](domain.md#journaloffset) or `null` | no | absent requests a consistent snapshot; present requests later deltas |
| `group_id` | opaque ID or `null` | no | narrows the projection without changing source ordering |
| `detail_level` | `summary`, `protocol`, `authorized-content` | no | defaults to least detail permitted for the caller |

### Output

One [RuntimeProjection](#getruntimeprojection) containing its source offset, current run/group/
attempt states, pending reconciliation flags and redacted counters/content. If the cursor is outside
retention or a gap cannot be proven absent, the query returns `snapshot_required`; it never guesses
missing deltas.

### Invariants

- Rebuilding from the same accepted stream produces the same projection and state hash.
- `recorded_at`/journal order governs projection; provider `observed_at` does not reorder authority.
- Content sealed from the caller is absent or redacted consistently with all other interfaces.

## GetRunStatus

**Type:** Query  
**Concept ID:** `agents-communication-infra.GetRunStatus`  
**Reads:** [Run](domain.md#run), [Group](domain.md#group), [Attempt](domain.md#attempt),
[ReconciliationState](domain.md#reconciliationstate)

Returns the latest rebuildable status for one run, including `execution_terminal`, `close_pending`
and `reconciliation_required` as distinct states. `closed` is returned only after the official close
row was exactly verified and that acknowledgement was accepted by the journal.

## GetVisibleGroupMessages

**Type:** Query  
**Concept ID:** `agents-communication-infra.GetVisibleGroupMessages`  
**Reads:** [Contribution](domain.md#contribution), [RevealManifest](domain.md#revealmanifest), accepted
`collection.closed` and `reveal.published` [RuntimeEventEnvelope](domain.md#runtimeeventenvelope) facts.

### Inputs

| Field | Type | Required | Rule |
|---|---|---:|---|
| `principal_context` | authenticated runtime context | yes | supplied by the trusted gateway, never by an agent payload |
| `run_id`, `group_id`, `group_version` | opaque IDs | yes | must match capability scope |
| `round_id` | opaque ID | yes | must match the persisted reveal manifest |
| `after_message_id` | opaque ID or `null` | no | pagination only; cannot broaden visibility |

### Visibility rule

| State | Same-seat content | Peer content |
|---|---|---|
| `collecting` | authorized own contribution | denied |
| `collection.closed` without `reveal.published` | authorized own contribution | denied |
| manifest-specific `reveal.published` | authorized own contribution | only IDs/hashes in that manifest and permitted by role |
| later phase or terminal | policy-defined | still restricted to persisted manifests/role policy |

This query exists for trusted reveal materialization, operator projections and controlled inspection.
It is not exposed as a generic agent tool in the initial proof. Authorized peer messages are
delivered into a later [EffectiveInputArtifact](domain.md#effectiveinputartifact), making exactly what
the agent received auditable.

## Query Performance and Authority

| Query | Consistency | Cursor/order | Maximum authority |
|---|---|---|---|
| [GetRuntimeProjection](#getruntimeprojection) | snapshot plus ordered incremental deltas | global [JournalOffset](domain.md#journaloffset) | reconstruct only |
| [GetRunStatus](#getrunstatus) | latest committed projection | projection source offset | reconstruct only |
| [GetVisibleGroupMessages](#getvisiblegroupmessages) | persisted event + manifest constrained | message IDs within manifest | disclose only what policy already authorized |

Projection storage is disposable. A projection mismatch is repaired by replay; no query result is
written back as a new authoritative fact.
