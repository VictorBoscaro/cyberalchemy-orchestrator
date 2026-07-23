---
tags: [agent-provenance-telemetry, spec, events]
node_type: spec
is_session: false
layer: application
nature: technical, reference
status: draft
version: 0.1.0
last_updated: 2026-07-23
feature: agent-provenance-telemetry
specAuthoringGate: in-review
runtimeGate: block
derivedFrom: SPEC.md@0.1.0
---

# Events: Agent Provenance Telemetry

This document defines the six and only six APT Event concepts registered by
[SPEC.md](SPEC.md#concept-registry) and produced by the current
[Operations](operations.md). It specifies canonical domain payloads carried through ACI; it does
not claim that schemas are registered or that a runtime exists.

## Common Event Boundary

### ACI Envelope Versus APT Domain Payload

ACI owns the canonical [RuntimeEventEnvelope](../../agents-communication-infra/specs/domain.md#runtimeeventenvelope),
journal offset, aggregate version, payload artifact/hash and durable acceptance receipt. APT owns
only the versioned domain payload schema and validation rules.

| ACI envelope/grouping metadata — not duplicated into APT payload | APT domain payload |
|---|---|
| `event_id`, `event_type`, envelope `schema_ref/schema_digest` | Exact event-specific semantic fields below |
| `aggregate_id`, `aggregate_version`, `journal_offset` | Entity/fact/edge identity needed by the domain |
| `recorded_at`, nullable `observed_at` | Owner-bound semantic occurrence time only where the domain contract requires it |
| `causation_id`, `correlation_id` | Pinned actor/authorization/evidence fields required by the accepted operation |
| `payload_ref`, `payload_hash` | Closed canonical payload whose bytes the hash identifies |
| Atomic `command_id`, offsets, ordered event IDs and grouping digest from the registered receipt/read profile | No receipt, batch, grouping or command-receipt fields |

The APT payload canonical preimage excludes every receipt/grouping field and the ACI envelope.
Object-key order is non-semantic; closed-union discriminators, list semantics and every declared
field are semantic. Unknown fields, omitted closed slots, unbound owner values or payload/envelope
schema mismatch fail before append.

```text
accepted_event ⇔
  valid(closed_APT_payload)
  ∧ payload_hash=H_ACI(canonical(closed_APT_payload))
  ∧ accepted(ACI_RuntimeEventEnvelope)
  ∧ durable_receipt
```

An operation proposal is not an event. Only ACI acceptance makes the envelope/payload authoritative.

### Producer, Idempotency and Atomic Group Rules

- [EnsureSession](operations.md#ensuresession), [LinkSessionDispatch](operations.md#linksessiondispatch),
  [AppendResearchCapture](operations.md#appendresearchcapture) and direct
  [AppendResearchFact](operations.md#appendresearchfact) produce a one-event verified command group
  on new acceptance.
- [StartNewSession](operations.md#startnewsession) produces exactly the ordered pair
  `SessionStarted`, `SessionContextRebound` in one verified atomic group.
- [AppendReferenceProbeLineage](operations.md#appendreferenceprobelineage) produces an ordered
  group containing only events for `submitted_new`: one `ReferenceProbeLineageAppended` per new
  delivery item and one `ResearchFactAppended` per new proven use fact.
- Exact submitted command retry produces no new event and returns the existing receipt.
- A never-submitted semantic no-op produces no event/receipt. For probe ingestion, operation result
  is `existing_exact ∪ accepted(submitted_new)`, while event grouping and receipt membership equal
  only `accepted(submitted_new)`.
- Incomplete or invalid command grouping applies no member to projections. There is no
  commit-barrier APT event.
- Multi-event enablement remains blocked until the exact ACI receipt/read-grouping profile is
  registered. Entity-fact/probe semantic append is separately blocked until the exact
  `aci.transactional-semantic-uniqueness-result-mapping@1` digest/registration receipt verifies.

### Privacy and Authority

No event payload contains raw-return bytes, selected text, artifact backend paths/credentials,
operational log bodies or mutable projections. A captured/partial witness appears only as a governed
[ArtifactReference](domain.md#artifactreference); extraction points to byte offsets/digests. Logs,
traces, metrics and consumers cannot mutate or repair the journal.

## SessionStarted

**Produced by:** [EnsureSession](operations.md#ensuresession) for initial creation; also
[StartNewSession](operations.md#startnewsession) as the first member of authorized rollover.  
**Projection effect:** establishes an immutable [Session](domain.md#session); initial creation binds
an unbound origin tuple, while rollover binding changes only after the matching rebound group
verifies. See [Session Context Binding](states.md#session-context-binding).

### Payload

Schema: `apt.session-started@1`.

| Field | Type | Description |
|---|---|---|
| `session` | closed [Session](domain.md#session) projection | Exact `session_id`, origin tuple, ensure key, start operation ID/time and immutable initial name. |
| `actor_ref` | authenticated principal ref | Owner-bound actor that caused creation. |
| `actor_authentication_ref` | external owner evidence ref or canonical null | Required for ensure; canonical null for rollover under the governing `StartNewSession` contract. |
| `actor_authentication_digest` | [ContentDigest](domain.md#contentdigest) or canonical null | Exact authentication evidence digest paired with the ref. |
| `rollover_authorization` | closed record or canonical null | Null for ensure; for rollover contains the exact policy/evidence refs and digests pinned identically by the rebound payload. |

`rollover_authorization` may contain only
`{authorization_policy_ref, authorization_policy_digest, authorization_evidence_ref,
authorization_evidence_digest}`. The producing branch is closed:

| Branch | Producer | `actor_authentication_ref/digest` | `rollover_authorization` | Actor/group requirement |
|---|---|---|---|---|
| ensure | [EnsureSession](operations.md#ensuresession) | both required and exact owner-bound authentication evidence | canonical null | `actor_ref` is the authenticated ensure principal; verified single-event group |
| rollover | [StartNewSession](operations.md#startnewsession) | both canonical null because that governing operation binds action authorization instead | required closed record with all four fields | `actor_ref` equals the rebound actor; first member of the exact two-event group |

Mixed, partially null or opposite-branch fields are invalid. This matrix does not create a third
Session-start path or allow caller-provided authority.

### Atomicity, Idempotency and Validation

- Ensure branch: a verified single-event group; exact command retry or semantic Session reuse emits
  nothing.
- Rollover branch: first of exactly two ordered events; it is not projection-visible alone.
- Session/ensure IDs, origin tuple, times, actor and evidence are owner-bound before canonicalization.
- Rollover start and rebound must have identical origin and authorization fields.

### Consumed By

| Consumer | Action |
|---|---|
| Pure session-binding reducer | Adds the immutable Session at the verified group boundary. |
| Planned SessionRecord projection | Exposes Session identity/name and derived membership counts at explicit as-of. |
| Non-authoritative observability adapter | Emits classified metadata/digests only after commit. |

## SessionContextRebound

**Produced by:** [StartNewSession](operations.md#startnewsession), exactly once as the second member
of the rollover group.  
**Projection effect:** changes the current Session selected for one exact host origin tuple; neither
Session Entity is mutated.

### Payload

Schema: `apt.session-context-rebound@1`.

| Field | Type | Description |
|---|---|---|
| `origin_kind`, `origin_ref` | exact host-owned tuple | Context whose derived binding changes. |
| `predecessor_session_id` | [Session](domain.md#session).`session_id` | Expected current binding CAS value. |
| `successor_session_id` | [Session](domain.md#session).`session_id` | Session created by the preceding group member. |
| `rebound_at` | owner timestamp | Semantic occurrence time. |
| `actor_ref` | authenticated principal ref | Authorized rollover actor. |
| `authorization_policy_ref`, `authorization_policy_digest` | external ref + [ContentDigest](domain.md#contentdigest) | Exact evaluated policy/version evidence. |
| `authorization_evidence_ref`, `authorization_evidence_digest` | external ref + [ContentDigest](domain.md#contentdigest) | Exact decision evidence. |

### Atomicity, Idempotency and Validation

The same group must contain exactly one preceding `SessionStarted` for the successor. Both payloads
pin identical origin/actor/authorization fields. Stale predecessor, missing partner, field mismatch,
replayed authorization nonce or invalid grouping applies neither member. Exact retry emits neither.

### Consumed By

| Consumer | Action |
|---|---|
| Pure session-binding reducer | Rebinds the tuple once at the group's verified `last_offset`. |
| Planned SessionRecord projection | Shows the successor as current without deleting predecessor history. |
| Non-authoritative observability adapter | Records accepted rollover correlation without rerunning policy. |

## SessionDispatchLinked

**Produced by:** [LinkSessionDispatch](operations.md#linksessiondispatch).  
**Projection effect:** creates the sole [SessionDispatchLink](domain.md#sessiondispatchlink) for an
existing Dispatch; the Dispatch itself is not mutated.

### Payload

Schema: `apt.session-dispatch-linked@1`.

| Field | Type | Description |
|---|---|---|
| `link` | closed [SessionDispatchLink](domain.md#sessiondispatchlink) projection | Link ID, Session/Dispatch IDs, operation ID and owner-bound link time. |
| `origin_kind`, `origin_ref` | exact host tuple | Context whose current Session authored the link. |
| `dispatch_snapshot_ref` | [DispatchAuthoritySnapshotRef](domain.md#dispatchauthoritysnapshotref) | Exact external authority evidence used to validate `dispatch_id`. |
| `actor_ref` | authenticated principal ref | Owner-bound link actor. |
| `authorization_policy_ref`, `authorization_policy_digest` | external ref + [ContentDigest](domain.md#contentdigest) | Exact action policy evidence. |
| `authorization_evidence_ref`, `authorization_evidence_digest` | external ref + [ContentDigest](domain.md#contentdigest) | Exact link authorization evidence. |

### Atomicity, Idempotency and Validation

New acceptance is one event. An exact existing link under a new operation is a semantic no-op; exact
submitted retry emits nothing; a contradictory link or changed command digest conflicts. Payload
validation proves current context binding and snapshot identity without writing the Dispatch ledger.

### Consumed By

| Consumer | Action |
|---|---|
| Session/Dispatch membership reducer | Adds the only authoritative Session-to-Dispatch edge. |
| Planned SessionRecord and DispatchScopeProjection | Derive reverse membership without persisting another join. |
| Research-capture application binder | Requires the exact current link before proposing a capture. |

## ResearchCaptureAppended

**Produced by:** [AppendResearchCapture](operations.md#appendresearchcapture).  
**Projection effect:** adds one immutable [ResearchCapture](domain.md#researchcapture) and advances
the derived same-chain head when predecessor CAS succeeds.

### Payload

Schema: `apt.research-capture-appended@1`.

| Field | Type | Description |
|---|---|---|
| `research_capture` | exact closed [ResearchCapture](domain.md#researchcapture) | All `apt.research-capture@1` slots plus verified `capture_digest`. |
| `session_dispatch_link_id` | [SessionDispatchLink](domain.md#sessiondispatchlink).`session_dispatch_link_id` | Exact preexisting current link used at acceptance. |
| `actor_ref` | authenticated producer/host principal ref | Owner-bound ingestion actor; does not replace `producer_ref`. |

The event payload never contains raw bytes. `research_capture.raw_return` is one
[ArtifactReference](domain.md#artifactreference) for `captured`/`partial` and canonical null for
`missing`.

### Atomicity, Idempotency and Validation

New acceptance is one event. `capture_digest` must equal the ACI canonical digest of the complete
capture preimage excluding that digest field. Status/cardinality, artifact/evidence, snapshot,
synthesis and current predecessor all validate before append. Retry emits nothing; stale/fork/cycle
rejects.

### Consumed By

| Consumer | Action |
|---|---|
| Capture-currentness reducer | Adds immutable capture and advances the derived chain head. |
| Planned ResearchRecord projection | Establishes capture status, witness ref and later child-fact scope. |
| AppendResearchFact binder | Resolves current non-missing capture/digest before extraction append. |

## ResearchFactAppended

**Produced by:** [AppendResearchFact](operations.md#appendresearchfact); also by
[AppendReferenceProbeLineage](operations.md#appendreferenceprobelineage) for each
`submitted_new` proven `research_reference_use`.  
**Projection effect:** advances one Entity fact head, one policy disposition head or one independent
assessment head, according to the exclusive payload variant.

### Payload

Schema: `apt.research-fact-appended@1`.

| Field | Type | Description |
|---|---|---|
| `payload_variant` | closed discriminated union | Exactly one variant listed below. |
| `actor_ref` | authenticated ingestion principal ref | Owner-bound event actor; extraction attribution remains inside Entity payloads. |
| `event_occurred_at` | owner timestamp | Semantic event time; for Entity variants it equals `FactEnvelope.occurred_at`. |

The union is exhaustive and exclusive:

| Family | Variants | Required content | Forbidden content |
|---|---|---|---|
| Entity fact | `research_question`, `research_answer`, `reference_use`, `reference_claim_relation`, `reference_check`, `research_problem`, `research_claim`, `formalization_candidate` | Exact closed Entity including [FactEnvelope](domain.md#factenvelope) and extraction where defined | Aggregate CAS fields |
| Disposition | `disposition_recorded` | Exact [TargetRef/disposition aggregate payload](domain.md#disposition-and-assessment-payload-variants) | `FactEnvelope`, fact-head CAS |
| Assessment | `assessment_recorded` | Exact [TargetRef/assessment aggregate payload](domain.md#disposition-and-assessment-payload-variants) | `FactEnvelope`, fact-head CAS |

Disposition and assessment are not separate Event concepts or mutable Entities. The accepted ACI
envelope supplies event identity; their payload supplies explicit aggregate type, ID, expected head
and expected version.

For `disposition_recorded` and `assessment_recorded`, actor binding is exact:

```text
payload_variant.actor_ref = top_level.actor_ref = authenticated_ingestion_principal
```

For extraction-bearing Entity variants (`research_question`, `research_answer`, `reference_use`,
`reference_claim_relation`, `research_problem`, `research_claim`, `formalization_candidate`),
`top_level.actor_ref` remains the ingestion principal while
`payload_variant.extraction.actor_ref` remains the attributed extractor. They may be equal only when
that principal actually performed the registered extraction.

`reference_check` has no `extraction` field. Its `checked_by` and `method_ref` remain the checker
attribution and are never overwritten by `top_level.actor_ref`; equality is valid only when that
authenticated ingestion principal actually executed the named check method. Extraction attribution
or checker attribution, as applicable, remains inside the exact Entity `payload_variant` and
therefore inside `fact_semantic_digest`. Top-level ingestion actor/time remains outside the
collision tuple.

### Global Fact Identity, Atomicity and Idempotency

For Entity variants, semantic uniqueness is global by `fact_id` across both producers:

```text
unique_key = fact_id

fact_semantic_digest =
  H_ACI(canonical(exact Entity payload_variant including FactEnvelope))

collision_tuple =
  (fact_semantic_digest,
   payload_variant.fact.subject_id,
   payload_variant.fact.supersedes_fact_id)

event_payload_hash =
  H_ACI(canonical({
    payload_variant,
    top_level.actor_ref,
    top_level.event_occurred_at
  }))

existing_exact ⇔ same(collision_tuple)
```

`fact_semantic_digest` is the transactional registry/collision digest.
`event_payload_hash` is the ACI envelope `payload_hash` for a genuinely new event. Top-level
ingestion actor/time are outside the collision tuple; for an Entity variant, the semantic
`FactEnvelope.occurred_at` remains inside `fact_semantic_digest` even though a new event requires
top-level `event_occurred_at` to equal it.

An exact collision returns the original accepted event/ref and creates no new event payload,
envelope or event payload hash. Any collision-tuple mismatch conflicts. Direct new append forms a
one-event group. Probe-origin new facts appear only inside the `submitted_new` atomic group;
`existing_exact` facts are absent from the group and its receipt. Disposition/assessment use their
explicit ACI aggregate head+version CAS rather than `FactEnvelope`.

### Privacy

Entity payloads include selector offsets/digests and artifact references, never selected/raw bytes.
The event actor cannot overwrite `ExtractionProvenance.actor_ref` on extraction-bearing variants or
`ReferenceCheck.checked_by/method_ref`; attribution equality is accepted only when the principal
actually performed the registered extraction or check respectively.

### Consumed By

| Consumer | Action |
|---|---|
| Fact-head reducer | Advances one same-subject Entity fact chain. |
| Disposition/assessment reducers | Advance only the named policy or assessor aggregate and preserve disagreement. |
| Planned ResearchRecord/granular projections | Join current facts to their owning capture at explicit as-of. |
| Non-authoritative observability adapter | Emits event/fact/capture IDs and digests, never raw content. |

## ReferenceProbeLineageAppended

**Produced by:** [AppendReferenceProbeLineage](operations.md#appendreferenceprobelineage), once per
`submitted_new` `delivery_origin` item.  
**Projection effect:** advances one stable recommendation-delivery head. It does not by itself
create reference use, research access, consultation or claim-support semantics.

### Payload

Schema: `apt.reference-probe-lineage-appended@1`.

| Field | Type | Description |
|---|---|---|
| `delivery_subject_key` | [ContentDigest](domain.md#contentdigest) | `H_ACI({probe_id,bundle_digest,recommendation_id})`. |
| `probe_recommendation_ref` | [ProbeRecommendationRef](domain.md#proberecommendationref) | Exact committed recommendation, bundle/profile registration and optional host-observation refs. |
| `expected_head_event_id` | ACI event ID or canonical null | Pre-command delivery-head CAS value. |
| `actor_ref` | authenticated ingestion principal ref | Owner-bound delivery/event actor. |
| `event_occurred_at` | owner timestamp | Semantic delivery-lineage occurrence time. |

### Result Partition, Atomicity and Idempotency

The producer validates a unique unordered request, canonically sorts it, then transactionally
partitions it:

```text
result = existing_exact ∪ accepted(submitted_new)
receipt.members = accepted(submitted_new)
existing_exact ∩ receipt.members = ∅
```

Only new delivery and proven-use events enter the ordered atomic group. Every use event references a
preexisting delivery head or a preceding new delivery member. Duplicate keys, forward/dangling
references, same-key virtual sequencing, stale heads, profile mismatch or any member failure commit
no new event/result mapping/receipt. Preexisting exact facts remain visible solely through their
original acceptance. Zero-new preflight submits no command.

### Privacy and Evidence Meaning

The payload pins external bundle/profile/observation evidence but never embeds source bytes. A host
observation proves only the registered probe-worker acquisition/processing evidence; it does not
prove that a research agent accessed or consulted the source.

### Consumed By

| Consumer | Action |
|---|---|
| Probe-delivery head reducer | Advances one recommendation composite delivery head at the verified group boundary. |
| Probe use-fact validator/reducer | Permits a later/same-group proven use only with an accepted delivery dependency. |
| Planned ResearchRecord/reference projections | Show typed probe origin separately from use/access/support. |
| Non-authoritative observability adapter | Reports accepted delivery IDs/profile digests without source bodies. |

## Event Coverage and Test Derivation

| Operation | New-acceptance event set | No-event branches |
|---|---|---|
| `EnsureSession` | `{SessionStarted}` | submitted exact retry; semantic Session reuse |
| `StartNewSession` | ordered atomic `{SessionStarted, SessionContextRebound}` | submitted exact retry; any authorization/CAS/group failure |
| `LinkSessionDispatch` | `{SessionDispatchLinked}` | submitted exact retry; semantic exact link |
| `AppendResearchCapture` | `{ResearchCaptureAppended}` | submitted exact retry |
| `AppendResearchFact` | `{ResearchFactAppended}` | submitted exact retry; global exact `fact_id` collision |
| `AppendReferenceProbeLineage` | ordered atomic events for `submitted_new`:<br>`{ReferenceProbeLineageAppended*, ResearchFactAppended*}` | zero-new; submitted exact retry; `existing_exact` members |

Coverage is exactly `6/6` current Operations and `6/6` Event concepts. No operation above produces
an unregistered seventh event, commit barrier, receipt event, disposition event or assessment event.

The later TEST-SPEC gate must derive at least one producer-contract case per operation/event edge,
one consumer/reducer case per consumer row, payload schema/canonical-digest negatives, privacy
no-body assertions, exact-retry/no-event cases, global `fact_id` collision cases, both disposition
aggregate families, incomplete-group rejection and mixed/zero-new probe partition fixtures. The
current [TEST-SPEC skeleton](../TEST-SPEC.md) remains planned/not-run and is not expanded here.

## Connections

| Document | Type | Description |
|---|---|---|
| [SPEC.md](SPEC.md) | `derives-from` | Registers exactly these six Event concepts and producer edges. |
| [operations.md](operations.md) | `produced-by` | Defines the only operation paths allowed to propose these payloads. |
| [domain.md](domain.md) | `contains` | Defines the closed Entity, Value Object and aggregate payload shapes. |
| [states.md](states.md) | `transitions` | Defines verified-group application and derived projection effects. |
| [rules.md](rules.md) | `enforced-by` | Defines authority, idempotency, privacy, identity and profile constraints. |
