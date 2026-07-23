---
feature: agent-provenance-telemetry
version: 0.1.0
status: draft
updatedAt: 2026-07-23
docType: operations
owners:
  - victor
specAuthoringGate: in-review
runtimeGate: block
derivedFrom: SPEC.md@0.1.0
---

# Operations: Agent Provenance Telemetry

This document specifies exactly the six Operations in the
[Concept Registry](SPEC.md#concept-registry). It defines contracts, not an implemented runtime.

### Common Execution Boundary

Domain functions are pure: they form the exact closed payload preimage, validate it, and invoke an
injected pure canonicalizer implementation that has passed the registered ACI golden/tamper
vectors. They return canonical bytes, a proposed digest, an event proposal or typed errors. They
perform no I/O, clock read, ID generation, authorization lookup, artifact read, journal query or
policy execution. The application submits those exact bytes/digest to ACI; only ACI acceptance and
its receipt make them authoritative.

Application-layer binders resolve and pin authenticated actor, owner timestamp/ID, host evidence,
current aggregate heads, Dispatch snapshots, finalized artifacts, ACI profile registrations and
receipts before invoking the domain function. These binders are implementation roles, not new
DomainSpec concepts. The application then maps proposals through
[APTFactToACIEvent](mappings.md#aptfacttoacievent) and appends through the planned
[ProvenanceAppendPort](interfaces.md#provenanceappendport). Durable append precedes acknowledgment.

For all six Operations:

```text
command_identity(EnsureSession)                 := operation_id
command_identity(StartNewSession)               := operation_id
command_identity(LinkSessionDispatch)           := operation_id
command_identity(AppendResearchCapture)         := capture_operation_id
command_identity(AppendResearchFact)            := operation_id
command_identity(AppendReferenceProbeLineage)   := operation_id

submitted(op) ∧ same(command_identity(op), canonical_command_digest)
  => prior_receipt and journal_delta = 0
submitted(op) ∧ same(command_identity(op), different_canonical_command_digest)
  => IDEMPOTENCY_CONFLICT
¬submitted(op) ∧ zero_new_events_after_semantic_preflight
  => semantic_existing_refs and no ACI command/receipt/idempotency claim
```

`AppendResearchCapture.operation_id` is an exact alias of `capture_operation_id`, not a second
field; its closed command contains only `capture_operation_id`. Every idempotency rule below uses
`command_identity(op)`.

Atomic multi-event operations additionally require the proposed ACI receipt/read grouping in
[states.md](states.md#atomic-command-receipt-and-read-grouping). Its absence or profile mismatch is
an implementation blocker, not permission to emulate partial atomicity.

Command lookup precedes semantic preflight. If `command_identity(op)` already has a submitted
receipt, normal command idempotency applies. For a never-submitted identity, preflight may return
semantic existing refs without registering that identity. Therefore repeated zero-new preflight
calls have no command-receipt guarantee; they are repeatable semantic lookups, not retries of a
submitted command.

The global semantic registry required below is an **ACI-journal-synchronous transactional unique
constraint/profile**, not an application projection, cache or separate store. Its exact required
binding is `{profile_id=aci.transactional-semantic-uniqueness-result-mapping, profile_version=1,
profile_digest=<ACI-registered digest>}`. The same ACI transaction owns global `fact_id`
uniqueness, semantic collision comparison, event append, aggregate/fact head CAS, total
request-result mapping and receipt creation. Its absence or profile/digest/receipt mismatch blocks
L0 implementation.

On a `fact_id` collision, exactness requires the stored canonical payload digest, `subject_id` and
`supersedes_fact_id` all to match; `subject_id` is comparison evidence, not part of the unique key.
For a probe request:

```text
operation_result = existing_exact ∪ accepted(submitted_new)
receipt.members   = accepted(submitted_new)
```

Only `submitted_new` participates in the new command's atomic append, head changes, offsets,
grouping digest and receipt. The total mapping preserves existing refs as `existing_exact`; it
never represents them as reaccepted.

`H_ACI(x)` below means the result of that injected, vector-qualified pure canonicalizer, later
verified and accepted by ACI, never a caller-authored hash. Every `APT-OP-*` rule is normative for
its linked planned
[Rules](rules.md) and [Test Specification](../TEST-SPEC.md); missing target files remain an
authoring dependency and do not weaken the contract.

### Caller Versus Owner-Bound Values

Caller-supplied values express intent. Owner-bound values are ignored if supplied by a caller and
are resolved/stamped by the host/application/ACI authority before pure domain validation.
`BoundCommand` below names a closed application input shape, not an additional registered
DomainSpec concept.

| Operation | Caller-supplied intent | Owner/application/ACI-bound authority |
|---|---|---|
| `EnsureSession` | `operation_id`, requested `initial_name` | `ensure_key`, `(origin_kind,origin_ref)`, actor/authentication, `session_id`, `started_at`, event ID, canonical bytes/digest, receipt |
| `StartNewSession` | `operation_id`, requested `initial_name`, `expected_current_session_id` | exact origin tuple/current binding, successor ensure/session IDs, timestamp, both event IDs, actor/action-authorization refs+digests, canonical bytes/digest, atomic receipt grouping |
| `LinkSessionDispatch` | `operation_id`, requested `dispatch_id` | exact origin tuple/current Session, link ID/time/event ID, Dispatch snapshot authority/digest, actor/action-authorization refs+digests, canonical bytes/digest, receipt |
| `AppendResearchCapture` | `capture_operation_id`, expected contribution, outcome intent, predecessor/synthesis intent | fixed `schema_ref=apt.research-capture@1`, capture/event IDs, `captured_at`, current context/link/head, producer/host evidence, snapshot/artifact/evidence authority+digests, canonical bytes/`capture_digest`, receipt |
| `AppendResearchFact` | `operation_id`, closed semantic payload, expected fact or aggregate head/version | fact/member/event IDs, `occurred_at`, actor, current capture/fact/aggregate heads, artifact bytes and authority/digests, canonical bytes/payload digest, receipt |
| `AppendReferenceProbeLineage` | `operation_id`, unordered closed delivery/use item collection | delivery metadata, lineage/fact event IDs/times, full owner-bound use payloads, committed bundle/profile receipts+digests, probe-worker evidence, current delivery/fact/capture heads, raw artifact evidence, canonical bytes/digests, atomic receipt grouping |

## EnsureSession

**Type:** Operation (mutation)  
**Actor:** Authenticated host/orchestrator principal.  
**Trigger:** A host execution context needs its coarse [Session](domain.md#session).

### Input

| Field | Type | Required | Description |
|---|---|---:|---|
| `operation_id` | opaque string | yes | Idempotency identity for this command. |
| `ensure_key` | opaque host key | yes | Creation-deduplication key; distinct from context identity. |
| `origin_kind` | string | yes | Host-stamped context kind. |
| `origin_ref` | opaque host ref | yes | Host-stamped context identity. |
| `initial_name` | non-empty string | yes | Caller-requested name; used only when a new Session is created. |
| `actor_ref` | authenticated principal ref | yes | Bound by the application. |

The host, not the caller, supplies `origin_kind`, `origin_ref`, `ensure_key`, `session_id`,
`started_at`, event ID and authority evidence.

```text
EnsureSessionBoundCommand = closed {
  operation_id, requested_initial_name,
  owner: {ensure_key, origin_kind, origin_ref, actor_ref,
          actor_authentication_ref, actor_authentication_digest,
          session_id?, started_at?, session_started_event_id?,
          canonicalizer_profile_id, canonicalizer_profile_version, canonicalizer_profile_digest}
}
```

The nullable owner-minted Session/event/time fields are all present only on the new-session branch;
they are absent together on semantic reuse. Unknown or caller-authored owner fields fail closed.

### Rules

| ID | Rule | Formal | Planned rule | Planned test |
|---|---|---|---|---|
| APT-OP-ENS-1 | A submitted command retry is command identity plus command digest: exact retry returns its receipt; changed digest conflicts. | `submitted(op)∧same(command_identity(op),digest)⇒same(receipt); submitted(op)∧same(command_identity(op))∧different(digest)⇒conflict` | [APT-R2](rules.md#apt-r2--idempotent-append) | [APT-OP-ENS-1](../TEST-SPEC.md#apt-op-ens-1) |
| APT-OP-ENS-2 | Context identity is exactly the host tuple; an optional materialized key is its canonical digest and is not caller-selectable. | `context=(origin_kind,origin_ref) ∧ key=H_canonical(context)` | [Session binding](rules.md#session-context-binding) | [APT-OP-ENS-2](../TEST-SPEC.md#apt-op-ens-2) |
| APT-OP-ENS-3 | `ensure_key` is an independent semantic lookup: same key and origin, under any new operation, reuses the immutable Session with no event. | `lookup(ensure_key)=(session,origin)⇒return(session)∧Δjournal=0` | [APT-R1](rules.md#apt-r1--single-join-authority) | [APT-OP-ENS-3](../TEST-SPEC.md#apt-op-ens-3) |
| APT-OP-ENS-4 | Session ID, time and host evidence are owner-stamped before pure validation. | `authority(session_id,started_at,origin)=host` | [APT-R8](rules.md#apt-r8--telemetry-non-authority) | [APT-OP-ENS-4](../TEST-SPEC.md#apt-op-ens-4) |
| APT-OP-ENS-5 | Same origin tuple reuses its currently bound immutable Session even with a new ensure key or different requested name; Ensure never renames. | `binding(origin)=s⇒return(s,initial_name(s))∧Δjournal=0` | [Session binding](rules.md#session-context-binding) | [APT-OP-ENS-5](../TEST-SPEC.md#apt-op-ens-5) |
| APT-OP-ENS-6 | An ensure key already associated with another origin tuple is a conflict. | `lookup(ensure_key).origin≠input.origin⇒conflict` | [Session binding](rules.md#session-context-binding) | [APT-OP-ENS-6](../TEST-SPEC.md#apt-op-ens-6) |

### Calculations

| ID | Calculation | Formula |
|---|---|---|
| APT-OP-ENS-C1 | Optional context binding key. | `H_canonical({origin_kind,origin_ref})` |
| APT-OP-ENS-C2 | Command digest, independent of owner-minted Session/event IDs and timestamps. | `H_ACI(canonical({ensure_key,origin_kind,origin_ref,initial_name}))` |

Lookup order is normative: first resolve `operation_id`; an existing operation requires the same
command digest. Only a new operation proceeds to semantic lookup by `ensure_key` and origin tuple,
where a different requested name does not rename or conflict with the existing Session.

### Preconditions

- The actor and host origin evidence are pinned.
- The current binding and any prior operation/ensure receipt are loaded at one accepted offset.
- Semantic lookup by `ensure_key` and origin tuple occurs independently of operation retry lookup.
- A new append is allowed only when the ensure key is unused and the origin tuple is unbound.

### Projection Transition

`unbound origin tuple -> bound to immutable Session` at the verified single-event grouping
`last_offset`; exact retry has no reducer transition.

### Events

- New context: exactly one [SessionStarted](events.md#sessionstarted).
- Exact operation retry: no event; return the prior receipt.
- Semantic ensure lookup/reuse under a new operation: no event; return the existing Session and its
  observable stored `initial_name`, even when the requested name differs.

### Postconditions

- One immutable [Session](domain.md#session) exists with the exact host origin tuple and initial
  name.
- [Session context binding](states.md#session-context-binding) selects that Session.
- A reuse response exposes the existing stored `initial_name`; a different requested name is not
  persisted and does not imply rename.

### Error States

| Condition | Result |
|---|---|
| Same `command_identity(op)`, different command digest | `IDEMPOTENCY_CONFLICT`; append nothing. |
| Ensure key already belongs to another origin tuple | `ENSURE_ORIGIN_CONFLICT`; append nothing. |
| Origin tuple already bound | Reuse current immutable Session and expose its existing name; no error/event/rename. |
| Caller-chosen or mismatched origin/context digest | `HOST_EVIDENCE_INVALID`; append nothing. |
| Duplicate Session ID or malformed/anonymous actor | `IDENTITY_INVALID`; append nothing. |
| ACI append fails before durable acceptance | `APPEND_FAILED`; no success receipt. |

## StartNewSession

**Type:** Operation (mutation)  
**Actor:** Authenticated principal authorized by the pinned rollover policy.  
**Trigger:** Explicit replacement of the Session currently bound to one host origin tuple.

### Input

| Field | Type | Required | Description |
|---|---|---:|---|
| `operation_id` | opaque string | yes | Atomic command/idempotency identity. |
| `origin_kind`, `origin_ref` | exact host tuple | yes | Context retained across rollover. |
| `expected_current_session_id` | [Session](domain.md#session).`session_id` | yes | Binding CAS value. |
| `successor_ensure_key` | opaque host key | yes | Owner-derived new creation-deduplication key; caller supply forbidden. |
| `initial_name` | non-empty string | yes | Immutable name of the successor. |
| `actor_ref` | authenticated principal ref | yes | Actor pinned into both events. |
| `authorization_policy_ref`, `authorization_policy_digest` | pinned policy evidence | yes | Exact evaluated policy/version. |
| `authorization_evidence_ref`, `authorization_evidence_digest` | pinned decision evidence | yes | Exact authorization result. |

```text
StartNewSessionBoundCommand = closed {
  operation_id, requested_initial_name, expected_current_session_id,
  owner: {origin_kind, origin_ref, predecessor_session_id,
          successor_session_id, successor_ensure_key, started_at, rebound_at,
          session_started_event_id, session_context_rebound_event_id,
          actor_ref, authorization_policy_ref, authorization_policy_digest,
          authorization_evidence_ref, authorization_evidence_digest,
          canonicalizer_profile_id, canonicalizer_profile_version, canonicalizer_profile_digest}
}

successor_ensure_key :=
  H_canonical({origin_kind,origin_ref,predecessor_session_id,command_identity(op)})
```

Unknown fields or caller-supplied owner fields fail closed.

### Rules

| ID | Rule | Formal | Planned rule | Planned test |
|---|---|---|---|---|
| APT-OP-ROL-1 | Rollover consumes exactly the current tuple binding. | `expected_current_session_id=binding(origin_kind,origin_ref)` | [Session binding](rules.md#session-context-binding) | [APT-OP-ROL-1](../TEST-SPEC.md#apt-op-rol-1) |
| APT-OP-ROL-2 | Successor has a new Session ID/ensure key and the same exact origin tuple. | `new(ids) ∧ origin(successor)=origin(predecessor)=input_origin` | [APT-R1](rules.md#apt-r1--single-join-authority) | [APT-OP-ROL-2](../TEST-SPEC.md#apt-op-rol-2) |
| APT-OP-ROL-3 | Both events pin identical actor, authorization refs/digests and origin tuple; replay never reruns policy. | `auth(start)=auth(rebound) ∧ origin(start)=origin(rebound)` | [Rollover authorization](rules.md#rollover-authorization) | [APT-OP-ROL-3](../TEST-SPEC.md#apt-op-rol-3) |
| APT-OP-ROL-4 | Successor start and rebound append as one ordered atomic command or neither appends. | `accepted(start) ⇔ accepted(rebound)` | [APT-R2](rules.md#apt-r2--idempotent-append) | [APT-OP-ROL-4](../TEST-SPEC.md#apt-op-rol-4) |
| APT-OP-ROL-5 | Exact submitted retry reuses the atomic receipt; changed event set/digest conflicts. | `submitted(op)∧same(command_identity(op),digest)⇒same(receipt); submitted(op)∧same(command_identity(op))∧different(digest)⇒conflict` | [APT-R2](rules.md#apt-r2--idempotent-append) | [APT-OP-ROL-5](../TEST-SPEC.md#apt-op-rol-5) |

### Calculations

| ID | Calculation | Formula |
|---|---|---|
| APT-OP-ROL-C1 | Context key check. | `H_canonical({origin_kind,origin_ref})` |
| APT-OP-ROL-C2 | Atomic grouping digest. | `H_ACI([start_payload_preimage,rebound_payload_preimage])` |

### Preconditions

- The application binds the current Session and authorization evidence at one offset.
- The required atomic-command ACI profile is registered by exact ID/version/digest.
- The successor IDs/timestamp and two event IDs are owner-stamped before domain evaluation.

### Projection Transition

`bound to predecessor -> bound to successor` once, at the atomic grouping `last_offset`.

### Events

In this exact ordered grouping:

1. [SessionStarted](events.md#sessionstarted) for the successor.
2. [SessionContextRebound](events.md#sessioncontextrebound) from expected predecessor to successor.

### Postconditions

- Both events are durably visible under one verified receipt/read grouping or neither is visible.
- The predecessor remains immutable; only replay-derived binding selects the successor.

### Error States

| Condition | Result |
|---|---|
| Unauthorized actor or invalid/mismatched pinned evidence | `ROLLOVER_UNAUTHORIZED`; append neither event. |
| Expected Session is stale or belongs to another tuple | `BINDING_CAS_CONFLICT`; append neither event. |
| Successor identity reused, self-successor or origin tuple differs | `SUCCESSOR_INVALID`; append neither event. |
| Atomic ACI profile absent/mismatched | `ATOMIC_PROFILE_UNAVAILABLE`; operation remains blocked. |
| Partial group, range/count/order/digest mismatch | `ATOMIC_GROUP_INVALID`; apply neither event. |
| Same `command_identity(op)` with changed group digest | `IDEMPOTENCY_CONFLICT`; append nothing. |

## LinkSessionDispatch

**Type:** Operation (mutation)  
**Actor:** Authenticated host/orchestrator principal.  
**Trigger:** An existing [Session](domain.md#session) must acquire the sole authoritative relation to
an existing external Dispatch.

### Input

| Field | Type | Required | Description |
|---|---|---:|---|
| `operation_id` | opaque string | yes | Link idempotency identity. |
| `origin_kind`, `origin_ref` | exact host tuple | yes | Owner-bound context whose current Session performs the action. |
| `session_id` | [Session](domain.md#session).`session_id` | yes | Owner-bound current tuple binding. |
| `dispatch_id` | external Dispatch ID | yes | Existing Dispatch identity. |
| `dispatch_snapshot_ref` | [DispatchAuthoritySnapshotRef](domain.md#dispatchauthoritysnapshotref) | yes | Exact authority evidence pinned for validation. |
| `actor_ref` | authenticated principal ref | yes | Host actor authoring the link. |
| `authorization_policy_ref`, `authorization_policy_digest` | pinned policy evidence | yes | Exact action-authorization policy/version. |
| `authorization_evidence_ref`, `authorization_evidence_digest` | pinned decision evidence | yes | Exact authorization result for this link action. |

```text
LinkSessionDispatchBoundCommand = closed {
  operation_id, requested_dispatch_id,
  owner: {origin_kind, origin_ref, session_id,
          session_dispatch_link_id, linked_at, session_dispatch_linked_event_id,
          dispatch_snapshot_ref,
          actor_ref, authorization_policy_ref, authorization_policy_digest,
          authorization_evidence_ref, authorization_evidence_digest,
          canonicalizer_profile_id, canonicalizer_profile_version, canonicalizer_profile_digest}
}
```

Unknown fields or caller-supplied owner fields fail closed.

### Rules

| ID | Rule | Formal | Planned rule | Planned test |
|---|---|---|---|---|
| APT-OP-LINK-1 | Session is exactly the current binding of the supplied host origin tuple at the action offset. Historical/unbound Session writes are forbidden. | `session_id=binding(origin_kind,origin_ref,offset)` | [APT-R1](rules.md#apt-r1--single-join-authority) | [APT-OP-LINK-1](../TEST-SPEC.md#apt-op-link-1) |
| APT-OP-LINK-2 | Input Dispatch equals the identity in either snapshot variant. | `dispatch_id=snapshot_dispatch_identity(snapshot_ref)` | [Dispatch snapshot](rules.md#dispatch-snapshot-identity) | [APT-OP-LINK-2](../TEST-SPEC.md#apt-op-link-2) |
| APT-OP-LINK-3 | No contradictory Session-to-Dispatch relation exists; exact submitted command identity/digest retry is idempotent. | `existing(dispatch_id)∈{null,same_link} ∧ submitted(op)∧same(command_identity(op),digest)⇒retry` | [APT-R1](rules.md#apt-r1--single-join-authority) | [APT-OP-LINK-3](../TEST-SPEC.md#apt-op-link-3) |
| APT-OP-LINK-4 | APT records only the foreign ID and pinned evidence; it does not mutate Dispatch. | `writes(APT) ∧ writes(Dispatch)=0` | [APT-R8](rules.md#apt-r8--telemetry-non-authority) | [APT-OP-LINK-4](../TEST-SPEC.md#apt-op-link-4) |
| APT-OP-LINK-5 | Actor and action-specific policy/evidence refs and digests are pinned and verified without replay-time policy execution. | `authorized(actor,link_action,pinned_policy,pinned_evidence)` | [Link authorization](rules.md#link-session-dispatch-authorization) | [APT-OP-LINK-5](../TEST-SPEC.md#apt-op-link-5) |

### Calculations

| ID | Calculation | Formula |
|---|---|---|
| APT-OP-LINK-C1 | Link payload digest. | `H_ACI(canonical(SessionDispatchLinked payload preimage))` |

### Preconditions

- Exact current context binding, current link index and immutable Dispatch snapshot are bound at one
  accepted offset.
- Snapshot owner namespace/version/digest and accepted evidence validate without domain I/O.
- Action authorization is evaluated once and its exact evidence is pinned.

### Projection Transition

`unlinked pair -> immutable SessionDispatchLink`; retry does not add another relation.

### Events

- Exactly one [SessionDispatchLinked](events.md#sessiondispatchlinked) for a new link.
- No event for exact retry.

### Postconditions

- One [SessionDispatchLink](domain.md#sessiondispatchlink) is the sole persisted edge.
- No reverse join or Dispatch mutation is persisted by APT.
- The accepted event pins the exact actor and action-authorization policy/evidence refs and digests
  used for the decision.

### Error States

| Condition | Result |
|---|---|
| Session or Dispatch snapshot missing | `AUTHORITY_NOT_FOUND`; append nothing. |
| Session is not the current exact origin-tuple binding | `SESSION_BINDING_STALE`; append nothing. |
| Actor/action authorization missing, stale or digest-mismatched | `LINK_UNAUTHORIZED`; append nothing. |
| Dispatch ID differs from either snapshot identity | `SNAPSHOT_IDENTITY_MISMATCH`; append nothing. |
| Dispatch already linked contradictorily | `JOIN_CONFLICT`; append nothing. |
| Same `command_identity(op)` with changed payload digest | `IDEMPOTENCY_CONFLICT`; append nothing. |
| Snapshot version/digest/evidence invalid | `SNAPSHOT_INVALID`; append nothing. |
| Historical Session linking or legacy backfill attempt | `BACKFILL_UNSUPPORTED_L0`; append nothing. |

## AppendResearchCapture

**Type:** Operation (mutation)  
**Actor:** Authenticated host on behalf of a bound seat/attempt or host actor.  
**Trigger:** One expected contribution returns complete/partial evidence, fails, or is corrected.

### Input

| Field | Type | Required | Description |
|---|---|---:|---|
| `capture_operation_id` | opaque string | yes | Idempotency component of the capture append. |
| `schema_ref` | string | yes | Owner-bound constant `apt.research-capture@1`; caller override forbidden. |
| `research_capture_id` | opaque APT ID | yes | Owner-minted new immutable capture identity. |
| `expected_contribution_id` | opaque string | yes | Stable contribution chain component. |
| `origin_kind`, `origin_ref` | exact host tuple | yes | Owner-bound current context identity. |
| `session_id`, `session_dispatch_link_id` | current APT IDs | yes | Owner-bound current context Session and its existing exact Dispatch link. |
| `dispatch_id` | external Dispatch ID | yes | Owning Dispatch. |
| `dispatch_snapshot_ref` | [DispatchAuthoritySnapshotRef](domain.md#dispatchauthoritysnapshotref) | yes | Exact pinned Dispatch authority. |
| `origin_refs`, `producer_ref` | closed domain refs | yes | Canonical causal set and authenticated producer lineage. |
| `capture_status` | [CaptureStatus](domain.md#capturestatus) | yes | `captured`, `partial` or `missing`. |
| `raw_return`, `partial_reason`, `failure_reason`, `failure_evidence_ref` | closed status slots | yes | Every slot present; nonapplicable values canonical null. |
| `supersedes_capture_id` | capture ID or null | yes | Expected current predecessor for correction. |
| `synthesizes` | semantic ordered unique pin list | yes | Same-Dispatch current-at-append exact capture/digest inputs. |
| `captured_at` | owner timestamp | yes | Host-stamped occurrence time. |

```text
AppendResearchCaptureBoundCommand = closed {
  capture_operation_id, expected_contribution_id, capture_status,
  raw_return_intent, partial_reason, failure_reason,
  supersedes_capture_id, synthesis_pin_intent,
  owner: {schema_ref="apt.research-capture@1",
          research_capture_id, research_capture_appended_event_id, captured_at,
          origin_kind, origin_ref, session_id, session_dispatch_link_id,
          dispatch_id, dispatch_snapshot_ref, origin_refs, producer_ref,
          raw_return, failure_evidence_ref, synthesizes,
          current_capture_head, canonicalizer_profile_id,
          canonicalizer_profile_version, canonicalizer_profile_digest}
}
```

There is no additional `operation_id` slot: `capture_operation_id` is the sole command identity.
Unknown fields or caller-supplied owner fields fail closed.

### Rules

| ID | Rule | Formal | Planned rule | Planned test |
|---|---|---|---|---|
| APT-OP-CAP-1 | All `apt.research-capture@1` preimage slots are present and closed; nonapplicable slots are null. | `keys(payload)=closed_slots_v1` | [APT-R3](rules.md#apt-r3--artifact-only-raw-return) | [APT-OP-CAP-1](../TEST-SPEC.md#apt-op-cap-1) |
| APT-OP-CAP-2 | Status matrix is exact. | `captured⇒artifact∧no_reason; partial⇒artifact∧partial_reason; missing⇒¬artifact∧failure_reason∧failure_evidence` | [APT-R3](rules.md#apt-r3--artifact-only-raw-return) | [APT-OP-CAP-2](../TEST-SPEC.md#apt-op-cap-2) |
| APT-OP-CAP-3 | Present raw artifact is finalized compatible textual UTF-8; evidence refs resolve by owner/version/digest. | `raw≠null⇒finalized∧textual∧charset=utf-8` | [APT-R3](rules.md#apt-r3--artifact-only-raw-return) | [APT-OP-CAP-3](../TEST-SPEC.md#apt-op-cap-3) |
| APT-OP-CAP-4 | Dispatch equals the identity pinned in either snapshot variant. | `dispatch_id=snapshot_dispatch_identity(snapshot_ref)` | [Dispatch snapshot](rules.md#dispatch-snapshot-identity) | [APT-OP-CAP-4](../TEST-SPEC.md#apt-op-cap-4) |
| APT-OP-CAP-5 | Initial append has no head/predecessor; correction CASes the same-chain current head and cannot fork/cycle. | `supersedes=null⇔head=null; supersedes≠null⇒supersedes=head(chain)` | [APT-R5](rules.md#apt-r5--capture-supersession) | [APT-OP-CAP-5](../TEST-SPEC.md#apt-op-cap-5) |
| APT-OP-CAP-6 | Synthesis pins are unique, semantic-order-preserving, preexisting, current, same-Dispatch and exact-digest. | `valid_synthesis_ordered_pins(synthesizes,dispatch_id)` | [Synthesis pins](rules.md#research-synthesis-pins) | [APT-OP-CAP-6](../TEST-SPEC.md#apt-op-cap-6) |
| APT-OP-CAP-7 | Same submitted command identity and digest retries; changed digest conflicts; capture identity uses the sole `capture_operation_id` field and retains the domain uniqueness tuple. | `command_identity(op)=capture_operation_id ∧ unique(dispatch,expected,command_identity(op)) ∧ submitted(op)∧same(command_identity(op),digest)⇒retry` | [APT-R2](rules.md#apt-r2--idempotent-append) | [APT-OP-CAP-7](../TEST-SPEC.md#apt-op-cap-7) |
| APT-OP-CAP-8 | Every new capture append requires the Session currently bound to its origin context and that Session's exact existing link to this Dispatch. | `session=binding(origin) ∧ link(session,dispatch_id)=current_exact_link` | [APT-R1](rules.md#apt-r1--single-join-authority) | [APT-OP-CAP-8](../TEST-SPEC.md#apt-op-cap-8) |

### Calculations

| ID | Calculation | Formula |
|---|---|---|
| APT-OP-CAP-C1 | Canonical capture digest. | `H_ACI(canonical({schema_ref,research_capture_id,expected_contribution_id,capture_operation_id,dispatch_id,dispatch_snapshot_ref,origin_refs,producer_ref,capture_status,raw_return,partial_reason,failure_reason,failure_evidence_ref,supersedes_capture_id,synthesizes,captured_at}))` |
| APT-OP-CAP-C2 | Chain key. | `(dispatch_id,expected_contribution_id)` |
| APT-OP-CAP-C3 | Idempotency digest. | `H_ACI(canonical(ResearchCaptureAppended payload preimage))` |

`origin_refs` canonicalize as a sorted unique set; `synthesizes` retains semantic order. Duplicate
members in either are rejected before digesting.

### Preconditions

- The application binds current context Session, exact SessionDispatchLink, producer authentication,
  snapshot, artifact/failure evidence, current chain head, synthesis inputs and prior operation
  receipt at one accepted offset.
- ACI canonicalizer/profile and artifact finalization receipts verify exactly.

### Projection Transition

`no head -> initial head` or `current head -> replacement head`; prior captures remain immutable and
only [Research capture currentness](states.md#research-capture-currentness) changes.

### Events

- Exactly one [ResearchCaptureAppended](events.md#researchcaptureappended) on new acceptance.
- No event on exact retry.

### Postconditions

- The accepted capture digest equals the domain-calculated exact preimage digest.
- Currentness selects the new capture; `CaptureStatus` remains immutable and never becomes
  `superseded`.
- The owning SessionDispatchLink preexisted the capture and remains the only Session-to-Dispatch
  authority.

### Error States

| Condition | Result |
|---|---|
| Missing/unknown schema or slot, extra field, invalid null/status combination | `CAPTURE_SCHEMA_INVALID`; append nothing. |
| Artifact/failure/origin evidence missing, uncommitted or digest-mismatched | `EVIDENCE_INVALID`; append nothing. |
| Binary/non-UTF-8/unfinalized raw return | `RAW_ARTIFACT_INVALID`; append nothing. |
| Snapshot identity/version/digest mismatch | `DISPATCH_SNAPSHOT_INVALID`; append nothing. |
| No current context Session or no exact SessionDispatchLink to the Dispatch | `CURRENT_LINK_REQUIRED`; append nothing. |
| Legacy unlinked capture/backfill attempt | `BACKFILL_UNSUPPORTED_L0`; append nothing; legacy data remains read-only. |
| Stale, unknown, cross-chain, self or cyclic predecessor | `CAPTURE_CAS_CONFLICT`; append nothing. |
| Invalid/duplicate/cross-Dispatch synthesis pin | `SYNTHESIS_INVALID`; append nothing. |
| Same `command_identity(op)` with different digest | `IDEMPOTENCY_CONFLICT`; append nothing. |

## AppendResearchFact

**Type:** Operation (mutation)  
**Actor:** Authenticated extractor, reviewer or host actor.  
**Trigger:** Structured research is extracted/revised, or a disposition/assessment event is
recorded.

### Input

| Field | Type | Required | Description |
|---|---|---:|---|
| `operation_id` | opaque string | yes | Fact/event idempotency identity. |
| `payload_variant` | closed union | yes | Exactly one of `research_question`, `research_answer`, `reference_use`, `reference_claim_relation`, `reference_check`, `research_problem`, `research_claim`, `formalization_candidate`, `disposition_recorded`, `assessment_recorded`. |
| `expected_subject_head_fact_id` | fact ID or null | entity variants only | Fact CAS head; forbidden for disposition/assessment. |
| `expected_head_accepted_event_id` | ACI event ID or null | disposition/assessment only | Aggregate CAS head; forbidden for Entity variants. |
| `expected_aggregate_version` | non-negative integer | disposition/assessment only | Aggregate CAS version; forbidden for Entity variants. |
| `fact_id`, `fact.operation_id`, `fact.occurred_at` | owner semantic ID/operation ID/timestamp | entity variants only | Owner-bound [FactEnvelope](domain.md#factenvelope) values; `fact.operation_id` is member identity, not ACI command identity. |
| `event_id` | owner ACI event ID | yes | Owner-bound identity of the proposed accepted event. |
| `event_occurred_at` | owner timestamp | yes | Owner-bound event occurrence time; equals fact time for Entity variants. |
| `actor_ref` | authenticated principal ref | yes | Owner-bound command/event ingestion principal; extraction attribution remains inside Entity payloads. |

```text
AppendResearchFactBoundCommand = closed {
  operation_id, payload_variant,
  expected_subject_head_fact_id?, expected_head_accepted_event_id?,
  expected_aggregate_version?,
  owner: {fact_id?, member_fact_operation_id?, event_id,
          fact_occurred_at?, event_occurred_at,
          actor_ref, authenticated_principal_ref,
          research_capture, current_fact_head?, current_aggregate_head?,
          raw_artifact_bytes?, artifact_authority_ref?, artifact_digest?,
          dispatch_snapshot_ref?, canonicalizer_profile_id,
          canonicalizer_profile_version, canonicalizer_profile_digest}
}
```

Question marks are variant-conditional closed slots, not caller-selectable omissions. Unknown fields
or caller-supplied owner fields fail closed.

### Rules

| ID | Rule | Formal | Planned rule | Planned test |
|---|---|---|---|---|
| APT-OP-FACT-1 | Entity FactEnvelope equality covers all five fields; member operation/subject/time/predecessor bind to owner semantic identity, stable Entity ID, event time and expected current same-subject head. Member operation identity is not the ACI command/receipt identity. | `fact=(fact_id,entity_id,member_fact_operation_id,event_occurred_at,expected_subject_head_fact_id) ∧ expected_subject_head_fact_id=head(entity_id)` | [Fact identity](rules.md#fact-append-identity) | [APT-OP-FACT-1](../TEST-SPEC.md#apt-op-fact-1) |
| APT-OP-FACT-2 | Every entity fact, reference and selector remains in one owning current non-missing capture in L0. | `∀edge: capture(source)=capture(target)=owning_capture` | [Research locality](rules.md#research-fact-locality) | [APT-OP-FACT-2](../TEST-SPEC.md#apt-op-fact-2) |
| APT-OP-FACT-3 | Extraction verifies capture/artifact/selected digests, exact non-empty UTF-8 raw-artifact byte bounds and actor/method. | `0≤start<end≤raw_len ∧ verify(all_digests) ∧ utf8(slice)` | [APT-R4](rules.md#apt-r4--extraction-provenance) | [APT-OP-FACT-3](../TEST-SPEC.md#apt-op-fact-3) |
| APT-OP-FACT-4 | Typed relation/check/formalization cardinalities and canonical relational sets validate closed. | `valid_variant_constraints(payload)` | [Fact typing](rules.md#research-fact-typing) | [APT-OP-FACT-4](../TEST-SPEC.md#apt-op-fact-4) |
| APT-OP-FACT-5 | Disposition/assessment aggregate type and ID equal the canonical chain-key mapping. | `aggregate_id=H_ACI(chain_key) ∧ aggregate_type=variant_type` | [Disposition chains](rules.md#disposition-and-assessment-chains) | [APT-OP-FACT-5](../TEST-SPEC.md#apt-op-fact-5) |
| APT-OP-FACT-6 | Aggregate append atomically CASes expected head and version on the same local target chain. | `(expected_head,expected_version)=current_aggregate_head` | [Disposition chains](rules.md#disposition-and-assessment-chains) | [APT-OP-FACT-6](../TEST-SPEC.md#apt-op-fact-6) |
| APT-OP-FACT-7 | Same submitted command identity plus canonical payload digest retries; changed digest conflicts. | `submitted(op)∧same(command_identity(op),digest)⇒retry; submitted(op)∧same(command_identity(op))∧different(digest)⇒conflict` | [APT-R2](rules.md#apt-r2--idempotent-append) | [APT-OP-FACT-7](../TEST-SPEC.md#apt-op-fact-7) |
| APT-OP-FACT-8 | The union is exclusive: Entity variants carry FactEnvelope and fact CAS only; disposition/assessment carry aggregate CAS only and never FactEnvelope. | `entity_variant xor disposition xor assessment ∧ entity⇒fact_CAS∧¬aggregate_CAS ∧ aggregate_variant⇒aggregate_CAS∧¬FactEnvelope∧¬fact_CAS` | [Fact union](rules.md#research-fact-appended-closed-union) | [APT-OP-FACT-8](../TEST-SPEC.md#apt-op-fact-8) |
| APT-OP-FACT-9 | Fact/member/event IDs and occurrence times are owner-bound; the domain forms canonical bytes with the injected vector-qualified canonicalizer and ACI acceptance makes the digest authoritative. | `authority(fact_id,member_fact_operation_id,event_id,fact.occurred_at,event_occurred_at)=owner ∧ fact.occurred_at=event_occurred_at(entity_variant) ∧ accepted_digest=ACI(canonical_bytes)` | [APT-R2](rules.md#apt-r2--idempotent-append) | [APT-OP-FACT-9](../TEST-SPEC.md#apt-op-fact-9) |
| APT-OP-FACT-10 | Disposition/assessment payload actor equals the authenticated owner-bound principal; the assessment aggregate chain key uses that identical actor. | `payload.actor_ref=actor_ref=authenticated_principal_ref ∧ assessment_chain.actor_ref=authenticated_principal_ref` | [Disposition chains](rules.md#disposition-and-assessment-chains) | [APT-OP-FACT-10](../TEST-SPEC.md#apt-op-fact-10) |
| APT-OP-FACT-11 | Entity facts share one ACI-journal transactional unique registry across both operations. The globally unique key is `fact_id`; collision rereads in the same transaction and compares canonical payload digest, `subject_id` and `supersedes_fact_id`. Exact equality returns the existing accepted event/ref; any mismatch conflicts. | `unique_key=fact_id; collision⇒tx_reread; same(payload_digest,subject_id,supersedes_fact_id)⇒existing_exact; otherwise⇒conflict` | [Fact identity](rules.md#fact-append-identity) | [APT-OP-FACT-11](../TEST-SPEC.md#apt-op-fact-11) |
| APT-OP-FACT-12 | Extraction actor remains the attributed extractor/producer and is validated against extraction mode, method, capture and evidence. It is not replaced by the authenticated command/event ingestion actor; equality is allowed only when that principal actually performed the registered host-parser/self extraction. | `valid_attribution(extraction.actor_ref,mode,method,capture,evidence) ∧ (extraction.actor_ref=ingestion_actor⇒performed_extraction(ingestion_actor,method))` | [APT-R4](rules.md#apt-r4--extraction-provenance) | [APT-OP-FACT-12](../TEST-SPEC.md#apt-op-fact-12) |

### Calculations

| ID | Calculation | Formula |
|---|---|---|
| APT-OP-FACT-C1 | Entity fact payload digest. | `H_ACI(canonical(closed fact payload preimage))` |
| APT-OP-FACT-C2 | Disposition aggregate ID. | `H_ACI(canonical(TargetRef,policy_ref))` |
| APT-OP-FACT-C3 | Assessment aggregate ID. | `H_ACI(canonical(TargetRef,actor_ref,method_ref,policy_ref))` |
| APT-OP-FACT-C4 | Selected-text digest check. | `H(raw_return.bytes[start:end]) = selected_text_digest` |
| APT-OP-FACT-C5 | New direct fact member identity; semantic duplicates reuse the stored member identity. | `new⇒H_canonical({command_identity(op),fact_id}); existing⇒existing.fact.operation_id` |

### Preconditions

- The application binds owner fact/event IDs and time, current capture/fact/aggregate heads,
  finalized raw artifact bytes, accepted event offset and actor evidence without passing I/O
  capabilities into domain code.
- For Entity variants, semantic lookup by `fact_id` occurs before minting member/event metadata.
  An existing fact rebinds its stored owner fields, canonical payload and subject CAS for exact
  comparison; only a truly new fact receives new owner fields.
- Semantic uniqueness, head CAS, event append and receipt commit execute in one ACI journal
  transaction under the exact registered
  `aci.transactional-semantic-uniqueness-result-mapping@1` profile/digest.
- For dispatch-scope question derivation, the pinned snapshot is exactly the owning capture
  snapshot.

### Projection Transition

Entity payload: `no subject head -> initial fact` or `current fact -> revised fact`.  
Disposition payload: update only one `adjudication_heads_by_policy` aggregate.  
Assessment payload: update only one independent `assessment_heads_by(actor,method,policy)`
aggregate.

### Events

- Exactly one [ResearchFactAppended](events.md#researchfactappended) on new acceptance.
- Submitted exact command retry: no new event; return the prior command receipt.
- For a never-submitted command identity, preflight exact semantic fact dedup submits no ACI command
  and returns the existing accepted event/ref, with no command-idempotency or receipt claim.

### Postconditions

- Entity and predecessor remain immutable; replay selects only the new same-chain head.
- Disposition/assessment remains event payload, not a new Entity or `FactEnvelope`.
- Independent assessor chains and disagreement remain visible.
- Result distinguishes command retry (`prior_receipt`) from cross-command semantic fact dedup
  (`existing_accepted_event_ref`).

### Error States

| Condition | Result |
|---|---|
| Unknown payload variant, extra/missing field or wrong subject binding | `FACT_SCHEMA_INVALID`; append nothing. |
| Entity variant carries aggregate CAS, or disposition/assessment carries FactEnvelope/fact CAS | `FACT_VARIANT_BINDING_INVALID`; append nothing. |
| Missing capture, `missing` capture, cross-capture edge or stale snapshot | `FACT_LOCALITY_INVALID`; append nothing. |
| Empty/out-of-bounds/multibyte-split selector or digest/media/charset mismatch | `SELECTOR_INVALID`; append nothing. |
| Typed relation/check/formalization constraint fails or relational duplicate supplied | `FACT_TYPE_INVALID`; append nothing. |
| Fact predecessor stale/unknown/cross-subject/cyclic | `FACT_CAS_CONFLICT`; append nothing. |
| Existing global fact ID has different canonical payload digest, `subject_id` or `supersedes_fact_id` | `FACT_IDENTITY_CONFLICT`; append nothing. |
| Required ACI transactional semantic-unique profile absent/mismatched | `SEMANTIC_REGISTRY_PROFILE_UNAVAILABLE`; implementation remains blocked. |
| Aggregate type/ID/head/version/predecessor/locality mismatch, gap or fork | `AGGREGATE_CAS_CONFLICT`; append nothing. |
| Disposition/assessment actor differs from authenticated owner-bound principal | `AGGREGATE_ACTOR_MISMATCH`; append nothing. |
| Same `command_identity(op)` with changed canonical digest | `IDEMPOTENCY_CONFLICT`; append nothing. |

## AppendReferenceProbeLineage

**Type:** Operation (mutation)  
**Actor:** Authenticated host ingestion principal.  
**Trigger:** Delivery/origin lineage from a preexisting committed probe bundle/recommendation is
recorded, optionally together with fully evidenced ResearchReferenceUse facts.

### Input

| Field | Type | Required | Description |
|---|---|---:|---|
| `operation_id` | opaque string | yes | Atomic lineage command identity. |
| `lineage_items` | unordered collection of closed union items | yes, non-empty | `delivery_origin` and zero-or-more fully evidenced `research_reference_use` items; caller order is ignored. |
| `actor_ref` | authenticated host principal | yes | Owner-bound command/event ingestion actor; not the use fact's attributed extractor by default. |

The probe bundle/publication receipt already exists and remains independently visible. It is not
created, recommitted or hidden by this Operation.

The item union is exact:

```text
delivery_origin = closed {
  kind="delivery_origin",
  delivery_subject_key,
  probe_recommendation_ref,
  expected_head_event_id,
  owner: {actor_ref, event_id, event_occurred_at}
}

research_reference_use = closed {
  kind="research_reference_use",
  full_research_reference_use_payload
}
```

`full_research_reference_use_payload` is the complete
[ResearchReferenceUse](domain.md#researchreferenceuse) fact, including its FactEnvelope fields,
reference identity/kind/locator, optional preexisting `probe_recommendation_ref`, use kind, anchor
quality and byte-exact [ExtractionProvenance](domain.md#extractionprovenance). It is the sole
canonical source for capture ID/digest, selector/extraction, subject/predecessor, actor,
`member_fact_operation_id`, owner fact ID and fact time. The binder constructs those owner-bound
fields inside this payload before validation; the item has no duplicate copies.

```text
stable_subject_key(delivery_origin) :=
  H_ACI({probe_id,bundle_digest,recommendation_id})
predecessor(delivery_origin) := expected_head_event_id

stable_subject_key(research_reference_use) :=
  full_research_reference_use_payload.reference_use_id
predecessor(research_reference_use) :=
  full_research_reference_use_payload.fact.supersedes_fact_id
member_fact_operation_id(research_reference_use) :=
  full_research_reference_use_payload.fact.operation_id :=
  H_canonical({command_identity(AppendReferenceProbeLineage),
               full_research_reference_use_payload.reference_use_id})
```

```text
AppendReferenceProbeLineageBoundCommand = closed {
  operation_id, lineage_items,
  owner: {actor_ref, authenticated_principal_ref,
          bundle_acceptance_receipts, profile_registration_receipts,
          probe_worker_observation_evidence,
          current_delivery_heads, current_fact_heads, current_captures,
          finalized_raw_artifact_bytes, lineage_event_ids, research_fact_event_ids,
          lineage_event_times, research_fact_event_times,
          canonicalizer_profile_id, canonicalizer_profile_version,
          canonicalizer_profile_digest}
}
```

Event-envelope metadata is positionally bound after canonical item sorting. Fact-envelope,
ExtractionProvenance and fact actor metadata exist only inside
`full_research_reference_use_payload`. Unknown fields or caller-supplied owner fields fail closed.

### Rules

| ID | Rule | Formal | Planned rule | Planned test |
|---|---|---|---|---|
| APT-OP-PROBE-1 | Bundle acceptance is an existing committed ACI event/publication receipt with exact probe/bundle/recommendation identity and digest. | `resolves(bundle_acceptance_ref,probe_id,bundle_digest,recommendation_id)` | [APT-R7](rules.md#apt-r7--protocol-profile-binding) | [APT-OP-PROBE-1](../TEST-SPEC.md#apt-op-probe-1) |
| APT-OP-PROBE-2 | Profile registration evidence exactly matches profile ID/version/digest and the bundle binding. | `registration_profile=profile_binding=bundle_profile` | [APT-R7](rules.md#apt-r7--protocol-profile-binding) | [APT-OP-PROBE-2](../TEST-SPEC.md#apt-op-probe-2) |
| APT-OP-PROBE-3 | A host observation is only committed evidence of probe-worker acquisition/processing; it never by itself proves research-agent access, consultation or claim support. | `host_observation⇒probe_worker_evidence ∧ host_observation_alone⇒¬(research_access∨consulted∨claim_support)` | [APT-R8](rules.md#apt-r8--telemetry-non-authority) | [APT-OP-PROBE-3](../TEST-SPEC.md#apt-op-probe-3) |
| APT-OP-PROBE-4 | Delivery subject key is stable from the recommendation composite, and predecessor CAS stays on that key. | `delivery_subject_key=H_ACI(probe_id,bundle_digest,recommendation_id) ∧ expected_head=current_delivery_head(delivery_subject_key)` | [Probe lineage](rules.md#probe-lineage-append) | [APT-OP-PROBE-4](../TEST-SPEC.md#apt-op-probe-4) |
| APT-OP-PROBE-5 | A `research_reference_use` item invokes the same pure validator/fact-head CAS and ACI-journal transactional semantic registry as AppendResearchFact—not an application projection/store. `member_fact_operation_id` is semantic member identity; every submitted group event carries outer `command_identity(op)`. | `validate_use=AppendResearchFact.validate(reference_use) ∧ semantic_registry_owner=ACI_journal_tx ∧ role(member_fact_operation_id)=semantic_member ∧ submitted(event)⇒event.command_id=command_identity(op)` | [APT-R4](rules.md#apt-r4--extraction-provenance) | [APT-OP-PROBE-5](../TEST-SPEC.md#apt-op-probe-5) |
| APT-OP-PROBE-6 | Only a submitted outer command has receipt idempotency. Exact submitted command/digest returns its receipt; an unseen command whose preflight has zero new events returns semantic refs without submitting or claiming command idempotency. | `submitted(op)∧same(command_identity(op),digest)⇒receipt; ¬submitted(op)∧|new|=0⇒existing_refs∧¬receipt_claim` | [APT-R2](rules.md#apt-r2--idempotent-append) | [APT-OP-PROBE-6](../TEST-SPEC.md#apt-op-probe-6) |
| APT-OP-PROBE-7 | The specialized operation may create zero-or-more proven ResearchReferenceUse facts, but every one requires a current non-missing capture, finalized raw bytes, byte-exact ExtractionProvenance and all fact evidence. | `0≤|use_items| ∧ ∀u: current_nonmissing_capture(u) ∧ byte_exact_extraction(u) ∧ all_fact_evidence(u)` | [APT-R4](rules.md#apt-r4--extraction-provenance) | [APT-OP-PROBE-7](../TEST-SPEC.md#apt-op-probe-7) |
| APT-OP-PROBE-8 | A recommendation composite without a fully evidenced use item creates only delivery/origin lineage and never access, consulted or support semantics. | `delivery_origin ∧ |valid_use_items|=0 ⇒ delivery_only ∧ ¬(access∨consulted∨support)` | [APT-R8](rules.md#apt-r8--telemetry-non-authority) | [APT-OP-PROBE-8](../TEST-SPEC.md#apt-op-probe-8) |
| APT-OP-PROBE-9 | Input is unordered. After duplicate rejection, the binder canonically sorts by `(kind_rank, stable_subject_key)`; permutations produce identical event order and digest. | `canonical_items=sort(items,key=(kind_rank,stable_subject_key)) ∧ digest(permute(items))=digest(items)` | [Probe lineage](rules.md#probe-lineage-append) | [APT-OP-PROBE-9](../TEST-SPEC.md#apt-op-probe-9) |
| APT-OP-PROBE-10 | Only `submitted_new` delivery/use-fact events form the separate atomic command grouping and receipt: all new members append or none does. `existing_exact` remains outside grouping/receipt and keeps its original acceptance. | `accepted(group)⇒accepted(all(submitted_new)); partial⇒apply(submitted_new)=0; existing_exact∩receipt.members=∅` | [APT-R2](rules.md#apt-r2--idempotent-append) | [APT-OP-PROBE-10](../TEST-SPEC.md#apt-op-probe-10) |
| APT-OP-PROBE-11 | Every use item's recommendation composite already has a current delivery head or has its delivery item earlier in the same canonical group. | `∀u: current_delivery(probe_ref(u)) ∨ precedes(delivery(probe_ref(u)),u)` | [Probe lineage](rules.md#probe-lineage-append) | [APT-OP-PROBE-11](../TEST-SPEC.md#apt-op-probe-11) |
| APT-OP-PROBE-12 | At most one item per `(kind,stable_subject_key)` may occur in a command group. Every predecessor compares with the pre-command head; member-to-member virtual sequencing, same-key forks and staged revisions are forbidden. | `unique(kind,stable_subject_key) ∧ ∀i: predecessor(i)=head_before_command(i)` | [Probe lineage](rules.md#probe-lineage-append) | [APT-OP-PROBE-12](../TEST-SPEC.md#apt-op-probe-12) |
| APT-OP-PROBE-13 | ACI enforces global transactional uniqueness on `fact_id`. A concurrent loser rereads inside the same journal transaction: equality of canonical payload digest, `subject_id` and `supersedes_fact_id` reclassifies the item as `existing_exact`; any mismatch conflicts the whole group. | `unique_key=fact_id; collision⇒tx_reread; same(payload_digest,subject_id,supersedes_fact_id)⇒existing_exact; otherwise⇒group_conflict` | [Fact identity](rules.md#fact-append-identity) | [APT-OP-PROBE-13](../TEST-SPEC.md#apt-op-probe-13) |
| APT-OP-PROBE-14 | Delivery and event actors equal the authenticated ingestion principal. A use payload's ExtractionProvenance actor remains the attributed extractor/producer and is validated by mode/method/capture/evidence; it equals ingestion actor only when that principal actually performed the registered host-parser/self extraction. | `delivery.actor_ref=event.actor_ref=authenticated_principal_ref ∧ valid_attribution(use.extraction) ∧ (use.extraction.actor_ref=authenticated_principal_ref⇒performed_extraction(authenticated_principal_ref,use.extraction.method_ref))` | [APT-R4](rules.md#apt-r4--extraction-provenance) | [APT-OP-PROBE-14](../TEST-SPEC.md#apt-op-probe-14) |
| APT-OP-PROBE-15 | Preflight partitions the request into `existing_exact`, `submitted_new` and `conflict`. Conflict rejects; zero new returns only existing refs; mixed requests submit only canonically ordered `submitted_new`. Exact result is `existing_exact ∪ accepted(submitted_new)`. | `partition(items)=(existing_exact,submitted_new,conflict); conflict⇒reject; |submitted_new|=0⇒no_submit; result=existing_exact∪accepted(submitted_new)` | [Probe lineage](rules.md#probe-lineage-append) | [APT-OP-PROBE-15](../TEST-SPEC.md#apt-op-probe-15) |
| APT-OP-PROBE-16 | ACI atomically commits uniqueness/head changes/events and receipt only for `submitted_new`, while persisting total request mapping that also points to `existing_exact`. Existing refs are not receipt members and are not reaccepted. | `commit(receipt)⇔commit(events(submitted_new),keys(submitted_new),heads(submitted_new)); result_mapping=existing_exact∪accepted(submitted_new); receipt.members=accepted(submitted_new)` | [APT-R2](rules.md#apt-r2--idempotent-append) | [APT-OP-PROBE-16](../TEST-SPEC.md#apt-op-probe-16) |
| APT-OP-PROBE-17 | Delivery preflight is also journal-synchronous: exact accepted `(delivery_subject_key, composite payload, expected predecessor)` returns its event/ref; same semantic delivery identity with mismatched payload/predecessor conflicts. | `exact_delivery⇒existing_event_ref; same(delivery_subject_key)∧different(composite∨predecessor)⇒conflict` | [Probe lineage](rules.md#probe-lineage-append) | [APT-OP-PROBE-17](../TEST-SPEC.md#apt-op-probe-17) |

### Calculations

| ID | Calculation | Formula |
|---|---|---|
| APT-OP-PROBE-C1 | Delivery stable subject key. | `H_ACI(canonical({probe_id,bundle_digest,recommendation_id}))` |
| APT-OP-PROBE-C2 | Atomic grouping verification when `|submitted_new|>0`. | `submitted⇒count=last-first+1=|ordered_event_ids|=|accepted(submitted_new)| ∧ verify(ordered_payload_digest)` |
| APT-OP-PROBE-C3 | Canonical request order after duplicate rejection; submitted event order filters that order to new items only. | `canonical_request=sort(items,(kind_rank,stable_subject_key)); submitted_items=filter(submitted_new,canonical_request)` |
| APT-OP-PROBE-C4 | Ordered ACI event payload digest after semantic no-op facts are resolved. | `H_ACI([canonical_payload_preimage(new_event₀),...,canonical_payload_preimage(new_eventₙ)])` in canonical item order |
| APT-OP-PROBE-C5 | Global fact identity and exact-collision tuple. | `unique_key=fact_id; exact_tuple=(H_ACI(full_research_reference_use_payload),subject_id,fact.supersedes_fact_id)` |
| APT-OP-PROBE-C6 | Outer command semantic digest. | `H_ACI(canonical(canonical_request))` including exact-semantic-no-op items |
| APT-OP-PROBE-C7 | Total request/result mapping. | `result_by_request_key[k]={status: existing_exact|accepted_new, accepted_event_ref}` for every requested `(kind,stable_subject_key)`, with `accepted_new ⇔ k∈submitted_new` |

Any input permutation with the same unique items produces the same `canonical_request`, event order
and digest. Duplicate `(kind,stable_subject_key)` input is rejected; it is never silently
deduplicated.

Receipt/grouping fields and receipt/group digest are excluded from each event payload preimage, as
required by [Atomic Command Receipt and Read Grouping](states.md#atomic-command-receipt-and-read-grouping).

### Preconditions

- The application binds the preexisting bundle acceptance receipt, profile registration, host
  observations, current delivery heads and exact registered ACI atomic profile.
- For every `research_reference_use` intent, shared semantic lookup by
  `reference_use_id/fact_id` runs before new fact/event metadata is minted. Exact existing facts
  reuse their stored full payload and accepted event/ref; mismatches abort the whole group.
- For a new use, the binder resolves the current non-missing capture, complete finalized UTF-8 raw
  artifact bytes/digests and current fact head, then constructs the complete ResearchReferenceUse
  payload—including FactEnvelope and ExtractionProvenance owner fields—as the sole canonical fact
  input to the shared AppendResearchFact validator.
- The required proposed ACI receipt/read-grouping profile is registered; otherwise implementation
  remains blocked.
- The exact `aci.transactional-semantic-uniqueness-result-mapping@1` profile digest and
  registration receipt are verified; otherwise semantic preflight/submission remains blocked.

### Projection Transition

`bundle visible, lineage absent/current -> same bundle visibility plus all delivery heads and
zero-or-more proven ResearchReferenceUse fact heads` once at the separate grouping `last_offset`.

### Events

- One [ReferenceProbeLineageAppended](events.md#referenceprobelineageappended) per new
  `delivery_origin` item.
- One [ResearchFactAppended](events.md#researchfactappended) per valid
  new `research_reference_use` fact, assembled by the same fact validator/CAS as
  [AppendResearchFact](#appendresearchfact).
- Mixed request: exclude all `existing_exact` members and submit only the non-empty canonical
  `submitted_new` subsequence under one atomic command grouping; receipt membership is exactly that
  subsequence.
- Zero-new preflight: submit no ACI command/event, create no command-idempotency/receipt claim, and
  return only the semantic existing refs.
- Submitted exact command retry: emit no new event and return the persisted receipt/result mapping.

### Postconditions

- On success, the total result is exactly
  `existing_exact ∪ accepted(submitted_new)`. All `submitted_new` delivery/use members become
  visible together or none becomes visible, and the receipt covers exactly those accepted new
  members.
- In a failed mixed request, no `submitted_new` member or new receipt/result mapping commits;
  `existing_exact` remains visible through its original acceptance and is neither rolled back nor
  reaccepted. A bundle without APT lineage remains valid.
- APT stores only pinned external identity/evidence and never mutates or re-owns the probe bundle,
  profile registry or host observation.
- Zero-or-more ResearchReferenceUse facts may be created only with complete current-capture,
  byte-exact extraction evidence. Delivery alone creates no use/access/consultation/support fact.
- Exact semantic use duplicates resolve to the same accepted fact/event identity across both
  operations.
- Every requested item has one result mapping entry. Exact result is
  `existing_exact ∪ accepted(submitted_new)`; preexisting refs retain original acceptance identity
  and never appear in the new receipt.

### Error States

| Condition | Result |
|---|---|
| Bundle acceptance missing, uncommitted, wrong identity or digest | `BUNDLE_ACCEPTANCE_INVALID`; append no lineage. |
| Profile registration/binding missing or mismatched | `PROFILE_BINDING_INVALID`; append no lineage. |
| Host observation/evidence dangling, stale or digest-mismatched | `HOST_EVIDENCE_INVALID`; append no lineage. |
| Empty/unknown item or stale delivery head | `LINEAGE_INVALID`; append no lineage. |
| More than one item for the same `(kind,stable_subject_key)` | `DUPLICATE_MEMBER_KEY`; append nothing. |
| Item predecessor depends on another same-command item or attempts a same-key fork/revision | `VIRTUAL_SEQUENCE_FORBIDDEN`; append nothing. |
| Use item lacks current capture, full ResearchReferenceUse payload, selector/artifact evidence or fact CAS | `PROVEN_USE_INVALID`; append no delivery or use facts. |
| Delivery/event actor differs from authenticated ingestion principal | `LINEAGE_ACTOR_MISMATCH`; append nothing. |
| Extraction actor/mode/method/capture evidence is invalid or is overwritten with ingestion actor | `EXTRACTION_ATTRIBUTION_INVALID`; append nothing. |
| Use item references neither a current delivery nor a preceding delivery item in the group | `DELIVERY_ORIGIN_REQUIRED`; append nothing. |
| Global `fact_id` exists through either operation with different canonical payload digest, `subject_id` or `supersedes_fact_id` | `FACT_IDENTITY_CONFLICT`; append no delivery or use facts. |
| Delivery-only item attempts to assert access/consultation/support | `LINEAGE_SCOPE_VIOLATION`; append no lineage. |
| Atomic grouping profile absent/mismatched | `ATOMIC_PROFILE_UNAVAILABLE`; operation remains blocked. |
| ACI journal transactional semantic-unique/result-mapping profile absent or mismatched | `SEMANTIC_REGISTRY_PROFILE_UNAVAILABLE`; implementation remains blocked. |
| Partial/range/count/canonical-event-order/payload-digest grouping mismatch | `ATOMIC_GROUP_INVALID`; apply no lineage; bundle remains visible. |
| Submitted same `command_identity(op)` with changed command digest | `IDEMPOTENCY_CONFLICT`; append no lineage. |

### Required Crash and Race Tests

- Crash after semantic preflight but before submission: no command, receipt, event, unique key or
  head change exists; retry reruns preflight.
- Zero-new preflight repeated with the same unseen command identity: both calls return semantic
  existing refs; neither may claim command idempotency or a receipt.
- Crash after ACI commit but before response: submitted command lookup returns the persisted receipt
  and total request/result mapping without another event.
- Concurrent exact fact insert: one transaction wins; the loser rereads the ACI unique key in its
  transaction and returns the same accepted event/ref. If other new items remain, only those items
  commit under the loser's command; if none remain, it becomes a zero-new no-submit result.
- Concurrent same global `fact_id` with different canonical payload digest, `subject_id` or
  `supersedes_fact_id`: loser
  conflicts and commits no receipt, event, semantic key or head.
- Crash or CAS race during a mixed atomic group: receipt, new events, semantic keys and heads for
  `submitted_new`, plus total result mapping, are visible together or none of the new portion is;
  `existing_exact` remains visible only through original acceptance and never joins the new receipt.
