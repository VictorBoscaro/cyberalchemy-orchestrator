---
tags: [agents-communication-infra, spec, confirmation-authority]
node_type: spec
is_session: false
layer: [domain, application, interface]
nature: [technical, reference]
status: specified-bounded-slice
version: 1.0.0
last_updated: 2026-08-31
---

# Runtime Confirmation Authority v1

## Contract status and objective

This contract is the candidate closure for CONF-000 and the first runtime-managed confirmation
slice. It defines the
immutable human-confirmation observation, the three authority digests, the bounded projection from
one pending dispatch shape to a canonical `DispatchSpec`, deterministic runtime identities, the
complete atomic acceptance unit and exact golden vectors. It creates no runtime code authority by
itself; CONF-001 remains a separate implementation task.

The approved source is the
[ConfirmedDispatch Robot-Talks finding](../robot-talks/2026-08-31-confirmed-dispatch-next-increment/findings.md).
The admitted workflow is exactly the finite
[`author:0 -> reviewer:0 -> author:1`](workflows.md#resumablefeedbackworkflow) graph. Chat and a
future UI are transport adapters to the same operation; neither transport owns confirmation
semantics.

## Ownership and trust boundary

| Concern | Owner | V1 boundary |
|---|---|---|
| Human decision | Authenticated repository user | Supplies the affirmative decision after seeing the exact pending-sheet and `DispatchSpec` digests. |
| Principal, channel and host observation | Trusted `ConfirmationObservationIssuer` adapter | Derives these fields from authenticated host context; user-authored payload fields are never trusted. |
| Pending bytes and deterministic projection | Runtime command boundary | Reads exact bytes once, validates the closed shape, resolves capabilities and reproduces canonical `DispatchSpec` bytes. |
| Confirmation acceptance | `ConfirmRuntimeDispatch` and the single SQLite journal writer | Verifies observation/digests and commits the complete local authority unit atomically. |
| Audit-row materialization | Existing validated audit appender/materializer | Deferred until after durable `opening_pending`; it is not part of CONF-001 acceptance. |
| Provider, tool, suspension and continuation effects | Later runtime operations | Forbidden in this slice. The only effect intent is the unclaimed audit-opening intent. |

The golden package treats its issuer reference/evidence and capability resolution as explicit
trusted test preconditions. It proves their exact binding and rejection on drift; it does not claim
that fixture literals prove production host authentication, cryptographic attestation or provider
availability. The deterministic projection guarantee is therefore exactly
`(canonical pending bytes, admitted capability resolution) -> canonical DispatchSpec`.

The local pilot trusts configured issuer adapters rather than a new signature system. An issuer is
admitted only by exact versioned reference and authenticated host integration. A chat phrase such as
“pode seguir” has no authority by itself; authority comes from the trusted observation binding that
decision to one principal, dispatch revision and displayed digests.

## Canonical byte contract

All documents use [`aci-cjson-1`](../adrs/ADR-001-persistence-replay-and-canonical-contracts.md#6-pydantic-and-canonical-acceptance-bytes).
Closed decoders reject unknown or duplicate keys, missing required fields, invalid UTF-8, floats,
out-of-range integers, non-NFC key collisions and the wrong primitive type. Canonical objects sort
keys, arrays preserve contract order, and canonical bytes are compact UTF-8 JSON. A digest is
`"sha256:" + lowercase_hex(SHA-256(bytes))`.

Every file in the v1 confirmation fixture package contains exactly its canonical document bytes
with no BOM, insignificant whitespace or trailing newline. `pending_sheet_digest` therefore hashes
the exact approved source bytes; it does not parse and then silently repair a different container.

## Digest taxonomy

| Digest | Exact bytes | Meaning | Explicit exclusions |
|---|---|---|---|
| `pending_sheet_digest` | Exact pending-sheet source bytes presented to the user and finalized by the artifact boundary | Identity of the editable source revision that was approved | Compiled spec, observation, command envelope and journal data |
| `dispatch_spec_digest` | Canonical bytes of `aci.dispatch-spec@1` after server-side capability resolution | Identity of the executable logical contract shown to the user | Human observation, runtime IDs and journal data |
| `confirmed_authority_digest` | Canonical bytes of `aci.confirmed-authority@1` | Complete immutable confirmation authority | Command ID, idempotency key, journal offset, writer clock and transport response metadata |

`confirmation_observation_digest`, `confirmed_turn_graph_digest`, `mapping_set_digest` and
`capability_resolution_digest` are subordinate evidence digests included by
`confirmed_authority_digest`. None may substitute for one of the three digests above.

## ConfirmationObservation

**Type:** Entity

Schema literal: `aci.confirmation-observation@1`.

| Field | Type | Constraint |
|---|---|---|
| `schema` | string | Exact schema literal. |
| `observation_id` | string | Stable ID assigned by the trusted issuer; retry reuses the same observation. |
| `issuer_ref` | `VersionedReference` | Exact configured chat/UI adapter identity and digest. |
| `issuer_evidence_ref` | artifact reference | Restricted immutable host evidence for the observed confirmation. |
| `issuer_evidence_digest` | `ContentDigest` | Digest of the exact issuer evidence. |
| `human_principal_id` | string | Authenticated principal derived by the issuer, not the message payload. |
| `channel` | enum | Exact `chat` or `ui`. |
| `observed_at` | RFC3339 timestamp | Millisecond UTC observation time supplied once by the trusted issuer. |
| `dispatch_id` | string | Equals the pending sheet and command path identity. |
| `dispatch_revision` | string | Equals the presented immutable source revision. |
| `presented_pending_sheet_digest` | `ContentDigest` | Exact source digest shown to the principal. |
| `presented_dispatch_spec_digest` | `ContentDigest` | Exact canonical spec digest shown to the principal. |
| `action` | string | Exact literal `approve_runtime_dispatch`. |

The runtime stores the exact observation artifact and digest. `ConfirmedDispatch.confirmed_by` is
the projection of `human_principal_id`; `confirmed_at` is the projection of `observed_at`, never a
fresh writer clock. A second observation with different bytes is different authority even if the
displayed dispatch and spec are unchanged.

**Identity:** `observation_id`, unique within the trusted issuer namespace. The entity is immutable;
the same identity with different canonical bytes is an issuer-integrity conflict.

## Bounded pending sheet and DispatchSpec projection

The accepted source schema is `aci.pending-runtime-dispatch@1`. Its closed top-level fields are:

| Field | Contract |
|---|---|
| `schema` | Exact source schema literal. |
| `dispatch_id`, `dispatch_revision` | Non-empty immutable identity and revision. |
| `execution_authority_mode` | Exact `runtime-managed`; `legacy-managed` is rejected before runtime authority exists. |
| `recipe_ref` | Exact `VersionedReference` for `aci.author-reviewer-author@1`. |
| `schema_refs` | Ordered author-output, reviewer-output and revision-instruction schema references. |
| `workflow` | Exact bounded logical graph defined below. |
| `decision_policy_refs` | Exact reconstruction and visibility policy references. |
| `prompt_snapshot_refs` | Exactly author then reviewer immutable prompt artifact IDs. |
| `capability_requirements` | Ordered logical adapter, model and tool requirements; no effective grant. |
| `budgets` | Positive finite `max_attempts_per_turn`, `max_total_turns` and `wall_clock_seconds`. |

The workflow is closed and admits exactly three ordered nodes:

| Ordinal | Operation | Group | Seat | Role | Round | Turn |
|---:|---|---|---|---|---|---:|
| 0 | `author_turn_0` | `group_authoring` | `seat_author` | `author` | `round_0` | 0 |
| 1 | `reviewer_turn_0` | `group_review` | `seat_reviewer` | `reviewer` | `round_0` | 0 |
| 2 | `author_turn_1` | `group_authoring` | `seat_author` | `author` | `round_1` | 1 |

Its only edges are `author_turn_0 -> reviewer_turn_0` and
`reviewer_turn_0 -> author_turn_1`; `workflow_kind=author-reviewer-author` and `loop_ceiling=1`.
Any extra, missing, reordered, cyclic or differently bounded node/edge is outside v1.

The command boundary constructs `aci.dispatch-spec@1` deterministically:

| Pending source | DispatchSpec target | Transform |
|---|---|---|
| `recipe_ref` | `recipe_ref` | Exact projection. |
| `schema_refs` | `schema_refs` | Exact ordered projection. |
| `workflow` | `group_graph` | Replace the source schema label with `aci.logical-turn-graph@1`; preserve all logical nodes, edges, kind and ceiling. |
| `decision_policy_refs` | `decision_policies` | Resolve the reconstruction mode and preserve exact policy refs; freeze the two allowed source message types. |
| `prompt_snapshot_refs` | `prompt_snapshot_refs` | Verify artifacts, then preserve exact order. |
| `capability_requirements` | `capability_resolution` | Resolve server-side to exact adapter/model/tool references; caller-supplied effective grants are forbidden. |
| `budgets` | `budgets` | Exact projection after positive finite validation. |

The projection has no clock, randomness, environment discovery, provider call, journal write or
legacy marker input. A `DispatchCandidate` may become a future source, but v1 neither requires one
nor accepts its digest as `dispatch_spec_digest`.

The operation must compile and display the spec before confirmation. Acceptance recompiles from
the finalized pending bytes and requires equality with
`ConfirmationObservation.presented_dispatch_spec_digest`; it never trusts expanded graph rows or
runtime IDs supplied by the client.

## Deterministic identity derivation

Runtime identities use the closed preimage:

```json
{"coordinates":["..."],"dispatch_id":"...","dispatch_spec_digest":"sha256:...","kind":"...","schema":"aci.confirmed-dispatch-id-preimage@1"}
```

`derive_id_v1(kind, coordinates) = prefix[kind] + first_32_lower_hex(SHA-256(aci-cjson-1(preimage)))`.
Integers in coordinates are shortest decimal strings. The caller cannot supply or override a
derived ID.

The complete derivation contract is the exact canonical
[`identity-derivation.json`](fixtures/confirmed-dispatch-v1/identity-derivation.json) document. Its
digest is recorded both in the fixture manifest and the confirmed-authority envelope; the preimage
schema name alone is not treated as proof of the derivation algorithm.

| Kind | Prefix | Coordinates in exact order |
|---|---|---|
| `run` | `run_` | `[]` |
| `turn_graph` | `graph_` | `[]` |
| `continuation` | `cont_` | `[source_seat_id, source_turn_ordinal, target_turn_ordinal]` |
| `source_message` | `msg_` | `[source_operation_id, source_round_id, source_message_type]` |
| `input_mapping` | `map_` | `[slot_ordinal, source_operation_id, source_turn_ordinal]` |
| `effect` | `effect_` | `["audit_opening"]` |
| `event` | `event_` | `[event_type, aggregate_version]` |
| `receipt` | `receipt_` | `["confirmation"]` |

Because every preimage includes `dispatch_id` and `dispatch_spec_digest`, a rerun requires a new
dispatch identity and cannot collide with the first run. The observation and authority digest do
not generate a second graph for the same dispatch/spec; an authority change instead conflicts.

## Confirmed turn graph and mappings

After deriving identities, the runtime expands the logical graph into one immutable
`aci.confirmed-turn-graph@1` artifact/row. It preserves the three logical nodes and two edges,
binds the derived `graph_id`, binds one derived continuation from author turn 0 to author turn 1,
and preallocates exactly two source messages:

| Source | Message type | Target input slot |
|---|---|---|
| `author_turn_0` | `author.output` | `prior_author_output`, ordinal 0 |
| `reviewer_turn_0` | `reviewer.output` | `review_feedback`, ordinal 1 |

Exactly two `ContinuationInputMapping` rows are created in slot order. For each row,
`confirmed_binding_digest` is the canonical digest of
`aci.continuation-input-binding@1` containing the dispatch/continuation, source selector, target
selector, slot and visibility policy but excluding `mapping_id` and `mapping_version`. This avoids
digest/identity circularity while proving the complete frozen binding.

The binding preimage is a closed object with exactly these fields:

| Field | Type / constraint |
|---|---|
| `schema` | Exact `aci.continuation-input-binding@1`. |
| `dispatch_id`, `continuation_id` | Non-empty exact strings. |
| `source_group_id`, `source_seat_id`, `source_operation_id` | Exact source selector strings. |
| `source_turn_ordinal` | Non-negative integer. |
| `source_round_id`, `source_message_id`, `source_message_type` | Exact frozen publication selector strings. |
| `target_seat_id` | Exact target seat string. |
| `target_turn_ordinal` | Non-negative integer; v1 requires 1. |
| `slot_name` | Exact `prior_author_output` or `review_feedback`. |
| `slot_ordinal` | Integer 0 or 1 matching the slot name. |
| `visibility_policy_ref` | Exact digest-pinned `VersionedReference`. |

Unknown, missing or additional fields are invalid. The two normative preimages and their digests
are reproduced by [`continuation-mappings.json`](fixtures/confirmed-dispatch-v1/continuation-mappings.json).

Confirmation preallocates the continuation identity and mappings but does not create a suspended
`AgentContinuation` aggregate. `SuspendAgentContinuation` must later consume this exact
`continuation_id` and both mappings.

## Confirmed authority envelope

Schema `aci.confirmed-authority@1` contains exactly:

- `dispatch_id`, `dispatch_revision` and `execution_authority_mode`;
- `pending_sheet_digest`, `dispatch_spec_digest` and `confirmation_observation_digest`;
- `capability_resolution_digest`, `confirmed_turn_graph_digest` and `mapping_set_digest`;
- `derivation_schema`;
- `identity_derivation_digest`, which hashes the complete versioned derivation-contract document;
- `payload_schema_bundle_digest`, which hashes the exact closed confirmation payload-schema bundle;
- the complete frozen command/event/payload/recipe/identity schema-version map; and
- its exact schema literal.

`confirmed_authority_digest` is the canonical digest of this envelope. `ConfirmedDispatch` stores
it explicitly; a generic field named only `digest` must not be used for pending-sheet identity.

The payload-schema bundle is recursively closed by its exact versioned
`aci.closed-payload-schema-dialect@1` member. That dialect closes the definition/field shapes,
every primitive pattern, the literal/integer/list constructors and the complete named structures
for `versioned-reference`, the five-key confirmation `schema_versions` map and
`confirmed-run-head`. A member `schema_digest` hashes its exact ordered definition; it is valid
only with the authority-bound `payload_schema_bundle_digest`, which additionally binds the dialect
and the ordered member set. Validators must reject an unknown dialect field/type/constructor or a
member that the pinned dialect cannot interpret without invention.

## Atomic acceptance and success boundary

A new accepted `ConfirmRuntimeDispatch` commits all or none of the following in one local SQLite
transaction:

1. finalized pending-sheet, `DispatchSpec`, confirmation-observation, confirmed-turn-graph,
   mapping-set, confirmed-authority, two event-payload and audit-opening-effect-payload artifact
   metadata; the static payload-schema bundle and identity-derivation contract are digest-bound;
2. one immutable `ConfirmationObservation` record;
3. one immutable `ConfirmedDispatch` and one `Run`;
4. the confirmed turn graph, its one continuation binding and exactly two normalized mappings;
5. `run.created` at aggregate version 1;
6. `audit_opening.requested` at aggregate version 2;
7. the run head/state at version 2 and `opening_pending`;
8. exactly one generic `audit_opening` effect intent whose immutable payload requests appender
   contract `0.6.4`, in `pending` status with zero attempts, `claimed_by=null`, `claim_epoch=null`,
   `outcome_event_id=null` and `outcome_digest=null`; these fields are present, with `null` meaning
   never claimed and no accepted outcome; and
9. the first stable confirmation receipt.

Every event, effect and receipt identity uses the frozen derivation above. Prepared artifact bytes
may remain as non-authoritative orphan candidates after a crash before commit; no artifact grants
authority without the complete transaction. Success performs no audit-row append, marker cleanup,
provider/tool call, attempt creation, suspension, resume or continuation effect.

## Replay, conflict and concurrency

The single writer evaluates both layers inside the same `BEGIN IMMEDIATE` transaction:

1. Existing `(scope_key, idempotency_key)` with identical command digest returns its receipt;
   another command digest is a permanent key conflict.
2. Otherwise, no existing `dispatch_id` permits a new acceptance.
3. Existing `dispatch_id` plus identical `confirmed_authority_digest` returns the first accepted
   receipt, even under a different idempotency key, with zero new rows/events/effects.
4. Existing `dispatch_id` plus a different `confirmed_authority_digest` is a permanent authority
   conflict with zero mutation.

An unlocked pre-read is forbidden. Two concurrent confirmations with equal authority converge to
one unit and the same receipt; divergent authorities elect one unit and one permanent conflict.

## Golden package

The normative package is
[`fixtures/confirmed-dispatch-v1`](fixtures/confirmed-dispatch-v1/manifest.json). It freezes:

- exact pending sheet, capability resolution and canonical `DispatchSpec`;
- a chat-issued confirmation observation;
- the expanded turn graph and two ordered mappings;
- the complete confirmed-authority envelope;
- exact fixture command, both event payloads/envelopes, complete generic effect row/payload,
  version-2 head and stable receipt under the frozen fixture clock/initial offsets; and
- every document digest, payload-schema member digest, complete payload-schema dialect/bundle
  digest and derivation constant in the manifest.

The fixture's chat channel is not preferred over UI. A UI adapter passes when it produces a valid
observation with its own trusted issuer/channel evidence while the pending sheet, projected
`DispatchSpec`, graph and mapping semantics remain identical.

[`negative-vectors.json`](fixtures/confirmed-dispatch-v1/negative-vectors.json) fixes every rejected
or replay case as exact RFC6902 document operations or a closed behavioral scenario, expected typed
result and postcondition. It also names every transaction failpoint from individual artifact
finalization through `before_commit`;
each failpoint requires zero authoritative SQL rows after reopen, while pre-SQL prepared bytes may
remain non-authoritative.

## Formal rules

### CONF-R1 — Trusted observation

Only an admitted issuer may bind an authenticated human principal, channel, host evidence,
dispatch/revision and the two displayed digests into an immutable observation. Payload-asserted
authority is rejected. Formally:
`accepted => trusted(issuer_ref) and authenticated(principal) and observed_scope = presented_scope`.

### CONF-R2 — Digest separation

Pending source, canonical executable spec and complete confirmation authority are different byte
domains and cannot substitute for one another:
`pending_sheet_digest != dispatch_spec_digest != confirmed_authority_digest` for the normative
fixture, and each digest verifies only its declared bytes.

### CONF-R3 — Bounded deterministic projection

The v1 projector admits only the closed three-node/two-edge/one-loop source shape, resolves
capabilities server-side and returns one canonical `DispatchSpec`:
`same(pending, resolution) => byte_equal(dispatch_spec)`; any graph or resolution drift rejects.

### CONF-R4 — Versioned derived identities

Every runtime identity equals `derive_id_v1(kind, coordinates)` under the manifest-pinned
derivation document. Supplied IDs and another derivation version are rejected.

### CONF-R5 — Complete graph binding

An accepted projection contains one confirmed graph, one preallocated continuation and exactly two
ordered mappings whose closed binding preimages reproduce their digests:
`count(mappings)=2 and ordinals(mappings)=[0,1]`.

### CONF-R6 — Atomic local acceptance

The acceptance members listed above commit together or not at all. Every named failpoint followed
by reopen yields zero authoritative confirmation rows; success yields versions 1 and 2 and one
pending audit-opening intent.

### CONF-R7 — Two-layer replay and conflict

Key-level replay is evaluated with identity-level replay inside the same write transaction:
`same key + same command => first receipt`; `new key + same dispatch/authority => first receipt`;
key drift or authority drift is a permanent conflict with zero new mutation.

### CONF-R8 — Success ceiling

Successful confirmation ends at `opening_pending` with one unclaimed audit-opening intent and zero
audit appends, providers, tools, attempts, suspensions or continuation actions.

## Required contract tests

| ID | Required proof | Validates |
|---|---|---|
| `T-ACI-AUTH1` | Legacy mode creates no runtime authority; the golden runtime confirmation creates exactly the complete atomic unit. | [CONF-R3](#conf-r3--bounded-deterministic-projection), [CONF-R6](#conf-r6--atomic-local-acceptance) |
| `T-ACI-AUTH2` | All package documents equal their manifest-pinned canonical bytes/digests; all IDs independently reproduce from the versioned preimages. | [CONF-R2](#conf-r2--digest-separation), [CONF-R4](#conf-r4--versioned-derived-identities) |
| `T-ACI-AUTH3` | Principal, issuer, channel, evidence, dispatch, revision, time and displayed-digest drift reject before mutation. | [CONF-R1](#conf-r1--trusted-observation) |
| `T-ACI-AUTH4` | Pending, spec and authority digests remain distinct and each independent mutation invalidates the correct lineage. | [CONF-R2](#conf-r2--digest-separation) |
| `T-ACI-AUTH5` | Node/edge/ceiling drift, extra or reordered mapping, selector drift and caller-supplied derived IDs reject. | [CONF-R3](#conf-r3--bounded-deterministic-projection), [CONF-R4](#conf-r4--versioned-derived-identities), [CONF-R5](#conf-r5--complete-graph-binding) |
| `T-ACI-AUTH6` | Same authority under a new key returns the first receipt; divergent authority or same-key command drift conflicts. | [CONF-R7](#conf-r7--two-layer-replay-and-conflict) |
| `T-ACI-AUTH7` | Every named transaction failpoint yields the complete unit or none; reopen/lost-response retry converges. | [CONF-R6](#conf-r6--atomic-local-acceptance) |
| `T-ACI-AUTH8` | Success ends at one pending audit-opening intent and proves zero audit materializer, provider, tool, attempt, suspension or continuation action. | [CONF-R8](#conf-r8--success-ceiling) |

## Explicitly deferred

- runtime migration 012 and the durable CONF-001 writer;
- HTTP/chat/UI production adapters beyond the trusted issuer interface contract;
- audit-row materialization, effect claim and marker cleanup;
- continuation migration 013 and TASK-CONT-001/002/003;
- legacy `dispatch_links` foreign-key decoupling;
- arbitrary workflow topologies and candidate-to-DispatchSpec projection; and
- multi-host, production, cryptographic-attestation or external-provider claims.

## Decisions

| ID | Decision | Authority |
|---|---|---|
| CONF-D1 | Human confirmation is an immutable issuer-bound observation; chat and UI are adapters. | [RT-T01 and human disposition](../robot-talks/2026-08-31-confirmed-dispatch-next-increment/findings.md#rt-t01--confirmation-channel-parity-versus-missing-durable-observation) |
| CONF-D2 | Pending source, canonical executable spec and complete confirmation authority have separate digests. | [RT-T01/RT-T02 and human gate](../robot-talks/2026-08-31-confirmed-dispatch-next-increment/findings.md#human-gate) |
| CONF-D3 | DispatchSpec remains logical; runtime IDs are derived afterward to avoid circular authority. | [RT-T02/RT-T03 and approved bounded projection](../robot-talks/2026-08-31-confirmed-dispatch-next-increment/findings.md#rt-t03--confirmation-atomic-unit-versus-implicit-continuation-preallocation) |
| CONF-D4 | V1 admits only the three-turn, two-edge, one-continuation, two-mapping workflow. | [CONF-000 approved sequence](../robot-talks/2026-08-31-confirmed-dispatch-next-increment/findings.md#conf-000--contract-and-golden-vector-closure-no-runtime-code) |
| CONF-D5 | Replay converges by dispatch identity plus authority digest in addition to key-level deduplication. | [RT-T05 and human disposition](../robot-talks/2026-08-31-confirmed-dispatch-next-increment/findings.md#rt-t05--identity-level-replay-versus-key-level-journal-idempotency) |
| CONF-D6 | Confirmation ends at durable `opening_pending` with one unclaimed generic effect intent. | [RT-T04 and human disposition](../robot-talks/2026-08-31-confirmed-dispatch-next-increment/findings.md#rt-t04--ratified-effect-intent-contract-versus-missing-outbox-primitive) |

## Connections

| Document | Type | Description |
|---|---|---|
| [Robot-Talks findings](../robot-talks/2026-08-31-confirmed-dispatch-next-increment/findings.md) | `derives-from` | Human-approved CONF-000/CONF-001 sequence and authority choices. |
| [Domain](domain.md) | `depends-on` | Owns `ConfirmedDispatch`, `Run`, `DispatchSpec`, continuation and mapping concepts. |
| [Operations](operations.md#confirmruntimedispatch) | `governs` | Supplies executable confirmation inputs, postconditions and conflicts. |
| [Interfaces](interfaces.md#post-dispatchesdispatch_idconfirm) | `governs` | Supplies presentation, trusted issuer and command-boundary semantics. |
| [Workflows](workflows.md#resumablefeedbackworkflow) | `depends-on` | Owns the admitted finite feedback topology. |
| [Test specification](../TEST-SPEC.md#t-aci-auth1--runtime-only-confirmed-dispatch) | `governs` | Expands confirmation acceptance and negative evidence. |
