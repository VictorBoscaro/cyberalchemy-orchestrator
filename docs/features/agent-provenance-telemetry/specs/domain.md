---
feature: agent-provenance-telemetry
version: 0.2.0
status: draft
updatedAt: 2026-07-25
docType: domain
specAuthoringGate: in-review
runtimeGate: block
derivedFrom: SPEC.md@0.2.0
---

# Domain: Agent Provenance Telemetry

Structural model for the 27 Entity, Value Object and Enum/Type concepts declared by the
[SPEC Concept Registry](SPEC.md#concept-registry). These are contracts, not evidence that a runtime
or store exists. External Dispatch, ACI and host concepts remain references and are never re-owned
by APT.

## Entities

### Session

The durable identity of one coarse orchestration context.

| Field | Type | Required / Cardinality | Ownership and meaning |
|---|---|---:|---|
| `session_id` | opaque string | exactly 1 | Host-minted stable APT identity. |
| `origin_kind` | string | exactly 1 | Host classification of the originating context. |
| `origin_ref` | string | exactly 1 | Opaque foreign context reference; not Session identity. |
| `ensure_key` | opaque string | exactly 1 | Stable host context key used to deduplicate initial creation. |
| `start_operation_id` | opaque string | exactly 1 | Idempotency identity for creation. |
| `started_at` | offset timestamp | exactly 1 | Owner-stamped creation instant. |
| `initial_name` | string | exactly 1 | Immutable L0 display label; not identity. |

**Identity:** `session_id`; `ensure_key` is independently unique.  
**Lifecycle:** Derived from immutable accepted rows; see planned
[Session context binding](states.md#session-context-binding).  
**Operations:** [EnsureSession](operations.md#ensuresession),
[StartNewSession](operations.md#startnewsession).  
**Invariants:** [SingleJoinAuthorityRule](rules.md#apt-r1--single-join-authority),
[IdempotentAppendRule](rules.md#apt-r2--idempotent-append).

---

### SessionDispatchLink

The identity-bearing authoritative association between one [Session](#session) and one existing
external Dispatch.

| Field | Type | Required / Cardinality | Ownership and meaning |
|---|---|---:|---|
| `session_dispatch_link_id` | opaque string | exactly 1 | Host-minted APT association identity. |
| `session_id` | [Session](#session).`session_id` | exactly 1 | Owning APT Session. |
| `dispatch_id` | external Dispatch ID | exactly 1 | Identity owned by the existing dispatch ledger/runtime. |
| `link_operation_id` | opaque string | exactly 1 | Idempotency identity for the link append. |
| `linked_at` | offset timestamp | exactly 1 | Owner-stamped occurrence time. |

**Identity:** `session_dispatch_link_id`; `dispatch_id` is unique within this relation type.  
**Lifecycle:** No mutable lifecycle; existence is derived from the immutable accepted link fact.  
**Operation:** [LinkSessionDispatch](operations.md#linksessiondispatch).  
**Invariant:** [SingleJoinAuthorityRule](rules.md#apt-r1--single-join-authority).

---

### ResearchCapture

One immutable outcome for an expected research contribution. A Dispatch owns `0..N` captures through
this entity's `dispatch_id`; the reverse relationship is never persisted elsewhere.

| Field | Type | Required / Cardinality | Ownership and meaning |
|---|---|---:|---|
| `schema_ref` | string | exactly 1 | Fixed to `apt.research-capture@1` in L0; any other or missing value fails closed. |
| `research_capture_id` | opaque string | exactly 1 | Stable APT capture identity. |
| `expected_contribution_id` | opaque string | exactly 1 | Logical seat/generation or host contribution expectation. |
| `capture_operation_id` | opaque string | exactly 1 | Idempotency identity for this append. |
| `dispatch_id` | external Dispatch ID | exactly 1 | Sole persisted Dispatch-to-Research edge. |
| `dispatch_snapshot_ref` | [DispatchAuthoritySnapshotRef](#dispatchauthoritysnapshotref) | exactly 1 | Pinned authority evidence used at acceptance. |
| `origin_refs` | canonical sorted set of [OriginRef embedded union](#originref-embedded-union) | exactly 1 slot | Present as a list encoding a set; empty when there are no causal inputs. |
| `producer_ref` | [ProducerRef embedded shape](#producerref-embedded-shape) | exactly 1 | Closed, host-stamped seat or host-actor lineage; anonymous producers are invalid. |
| `capture_status` | [CaptureStatus](#capturestatus) | exactly 1 | Immutable outcome classification. |
| `raw_return` | [ArtifactReference](#artifactreference) or null | exactly 1 slot | Artifact for `captured`/`partial`; canonical null for `missing`. |
| `partial_reason` | non-empty string or null | exactly 1 slot | Non-empty for `partial`; canonical null for `captured`/`missing`. |
| `failure_reason` | non-empty string or null | exactly 1 slot | Non-empty for `missing`; canonical null for `captured`/`partial`. |
| `failure_evidence_ref` | [FailureEvidenceRef embedded union](#failureevidenceref-embedded-union) or null | exactly 1 slot | Required for `missing`, optional for `partial`, canonical null for `captured`. |
| `supersedes_capture_id` | [ResearchCapture](#researchcapture).`research_capture_id` or null | exactly 1 slot | Current predecessor for a correction; canonical null otherwise. |
| `synthesizes` | semantic ordered list of unique `{research_capture_id, capture_digest}` pins | exactly 1 slot | Present as a list; empty for no inputs. Existing, current-at-append, same-Dispatch, non-self immutable inputs; order participates in equality/digest. |
| `captured_at` | offset timestamp | exactly 1 | Host-stamped occurrence time. |
| `capture_digest` | [ContentDigest](#contentdigest) | exactly 1 | Digest of the canonical immutable capture contract. |

**Identity:** `research_capture_id`; the idempotency uniqueness tuple is
`(dispatch_id, expected_contribution_id, capture_operation_id)`.  
**Lifecycle:** Bytes and status never change. Currentness/supersession is a derived projection; see
planned [Research capture currentness](states.md#research-capture-currentness).  
**Operation:** [AppendResearchCapture](operations.md#appendresearchcapture).  
**Invariants:** [ArtifactOnlyRawReturnRule](rules.md#apt-r3--artifact-only-raw-return),
[CaptureSupersessionRule](rules.md#apt-r5--capture-supersession).

`dispatch_id` must equal the Dispatch identity carried by `dispatch_snapshot_ref`: the direct
`dispatch_id` in `aci_managed`, or `ledger_row_identity.dispatch_id` in `legacy_ledger`. Cross-
Dispatch, missing, or mismatched identities fail before append.

Every synthesis input ID is unique, exists before the synthesis append, is current at that instant,
belongs to the same `dispatch_id`, is not the output capture, and matches its exact accepted digest.
The ordered pin list participates in the synthesizing capture's equality and digest. Two
permutations of the same unique pins intentionally denote different synthesis composition and
produce different digests. Later input supersession cannot rewrite composition;
`input_now_superseded` is derived display state only.

`capture_digest` is computed by the ACI canonicalizer over this exact versioned projection, excluding
the digest field itself. Every listed slot is present. A conditionally nonapplicable value is encoded
as canonical `null`; omission is not equivalent to null:

```text
{
  schema_ref,
  research_capture_id,
  expected_contribution_id,
  capture_operation_id,
  dispatch_id,
  dispatch_snapshot_ref,
  origin_refs,
  producer_ref,
  capture_status,
  raw_return,
  partial_reason,
  failure_reason,
  failure_evidence_ref,
  supersedes_capture_id,
  synthesizes,
  captured_at
}
```

An unknown field, missing schema, wrong schema, or omitted preimage slot fails schema validation
before canonicalization. Golden/tamper vectors must cover every preimage field, schema version,
canonical null slots, raw artifact digest, reference digest, predecessor and synthesis-list order;
changing any semantic field or permuting synthesis pins changes `capture_digest`, while JSON object
key order alone does not. Reordering a relational set such as `origin_refs` canonicalizes to the
same digest; supplying a duplicate member is rejected before canonicalization.

The status matrix is closed:

| Status | `raw_return` | `partial_reason` | `failure_reason` | `failure_evidence_ref` |
|---|---|---|---|---|
| `captured` | finalized UTF-8 textual artifact | null | null | null |
| `partial` | finalized UTF-8 textual artifact | non-empty | null | committed evidence ref or null |
| `missing` | null | null | non-empty | committed evidence ref |

Any other combination fails closed.
Status-matrix fixtures reject every swapped/omitted slot, captured failure metadata, partial without
artifact or non-empty `partial_reason`, partial with `failure_reason`, and missing with an artifact,
empty reason or absent/uncommitted failure evidence.

---

### ResearchQuestion

An addressable question extracted or declared within one [ResearchCapture](#researchcapture).

| Field | Type | Required / Cardinality | Ownership and meaning |
|---|---|---:|---|
| `research_question_id` | opaque string | exactly 1 | Stable subject identity. |
| `research_capture_id` | [ResearchCapture](#researchcapture).`research_capture_id` | exactly 1 | Owning capture. |
| `fact` | [FactEnvelope](#factenvelope) | exactly 1 | Immutable fact-version metadata. |
| `question_text` | string | exactly 1 | The attributed question text. |
| `derives_from` | canonical sorted set of [QuestionDerivationRef embedded union](#questionderivationref-embedded-union) | `0..N`, unique | Closed dispatch-scope or same-capture question origins; never inferred by text similarity. |
| `extraction` | [ExtractionProvenance](#extractionprovenance) | exactly 1 | Attribution to exact captured bytes. |

**Identity:** `research_question_id`; versions are identified by
[FactEnvelope](#factenvelope).`fact_id`.  
**Operation:** [AppendResearchFact](operations.md#appendresearchfact).  
**Invariant:** [ExtractionProvenanceRule](rules.md#apt-r4--extraction-provenance).

---

### ResearchAnswer

An addressable answer extraction that points into, but does not copy, a raw witness.

| Field | Type | Required / Cardinality | Ownership and meaning |
|---|---|---:|---|
| `research_answer_id` | opaque string | exactly 1 | Stable answer subject identity. |
| `research_capture_id` | [ResearchCapture](#researchcapture).`research_capture_id` | exactly 1 | Owning capture. |
| `fact` | [FactEnvelope](#factenvelope) | exactly 1 | Immutable fact-version metadata. |
| `question_ids` | canonical sorted set of [ResearchQuestion](#researchquestion).`research_question_id` | `1..N`, unique | Questions this extraction addresses. |
| `extraction` | [ExtractionProvenance](#extractionprovenance) | exactly 1 | Contains the exact [RawSelector](#rawselector). |

**Identity:** `research_answer_id`; full response bytes remain exclusively behind the capture's
[ArtifactReference](#artifactreference). Every `question_id` resolves to the same
`research_capture_id` in L0.  
**Operation:** [AppendResearchFact](operations.md#appendresearchfact).  
**Invariant:** [ExtractionProvenanceRule](rules.md#apt-r4--extraction-provenance).

---

### ResearchReferenceUse

An attributed mention, citation or claimed consultation within one capture.

| Field | Type | Required / Cardinality | Ownership and meaning |
|---|---|---:|---|
| `reference_use_id` | opaque string | exactly 1 | Stable use subject identity. |
| `research_capture_id` | [ResearchCapture](#researchcapture).`research_capture_id` | exactly 1 | Owning capture. |
| `fact` | [FactEnvelope](#factenvelope) | exactly 1 | Immutable fact-version metadata. |
| `reference_id` | opaque string | exactly 1 | APT-local opaque reference identity; not bibliographic equivalence. |
| `reference_kind` | constrained string | exactly 1 | `file`, `url`, `paper`, `commit`, `dataset` or `command-output`. |
| `locator_observed` | string | exactly 1 | Locator exactly observed by the extracting actor. |
| `source_observation_id` | external [`host.SourceObservation`](../discovery/session-dispatch-research-records.md#43-reference-uses-and-checks) ID | `0..1` | Nullable host-owned evidence reference; never inferred. |
| `probe_recommendation_ref` | [ProbeRecommendationRef](#proberecommendationref) | `0..1` | Optional probe-origin evidence. |
| `use_kind` | [ReferenceUseKind](#referenceusekind) | exactly 1 | Attributed use category. |
| `anchor_quality` | constrained string | exactly 1 | `none`, `locator`, `span` or `digest`. |
| `extraction` | [ExtractionProvenance](#extractionprovenance) | exactly 1 | Content-derived attribution. |

**Identity:** `reference_use_id`; direct uses omit `probe_recommendation_ref`.  
**Operation:** [AppendResearchFact](operations.md#appendresearchfact).  
**Invariants:** [ExtractionProvenanceRule](rules.md#apt-r4--extraction-provenance),
[ProtocolProfileBindingRule](rules.md#apt-r7--protocol-profile-binding).

---

### ResearchReferenceClaimRelation

One typed epistemic relation between an exact [ResearchReferenceUse](#researchreferenceuse) and an
exact [ResearchClaimExtraction](#researchclaimextraction).

| Field | Type | Required / Cardinality | Ownership and meaning |
|---|---|---:|---|
| `relation_id` | opaque string | exactly 1 | Stable relation subject identity. |
| `research_capture_id` | [ResearchCapture](#researchcapture).`research_capture_id` | exactly 1 | Owning capture. |
| `fact` | [FactEnvelope](#factenvelope) | exactly 1 | Immutable fact-version metadata. |
| `reference_use_id` | [ResearchReferenceUse](#researchreferenceuse).`reference_use_id` | exactly 1 | Exact attributed use. |
| `research_claim_id` | [ResearchClaimExtraction](#researchclaimextraction).`research_claim_id` | exactly 1 | Exact research-local claim. |
| `relation` | constrained string | exactly 1 | `supports`, `partially_supports`, `contradicts`, `contextualizes` or `irrelevant`. |
| `extraction` | [ExtractionProvenance](#extractionprovenance) | exactly 1 | Attribution for the epistemic relation. |

**Identity:** `relation_id`; reverse claim/reference lists are projections.  
Both the use and claim resolve to this relation's `research_capture_id` in L0.  
**Operation:** [AppendResearchFact](operations.md#appendresearchfact).

---

### ReferenceCheck

One addressable check of reference identity, access evidence or claim support.

| Field | Type | Required / Cardinality | Ownership and meaning |
|---|---|---:|---|
| `reference_check_id` | opaque string | exactly 1 | Stable check subject identity. |
| `research_capture_id` | [ResearchCapture](#researchcapture).`research_capture_id` | exactly 1 | Owning capture. |
| `fact` | [FactEnvelope](#factenvelope) | exactly 1 | Immutable fact-version metadata. |
| `check_kind` | [ReferenceCheckKind](#referencecheckkind) | exactly 1 | What the check evaluates. |
| `reference_use_id` | [ResearchReferenceUse](#researchreferenceuse).`reference_use_id` | exactly 1 | Checked use. |
| `relation_id` | [ResearchReferenceClaimRelation](#researchreferenceclaimrelation).`relation_id` | conditional `0..1` | Exactly one for `claim_support`; absent otherwise. |
| `checked_by` | opaque actor ref | exactly 1 | Checker identity. |
| `method_ref` | string | exactly 1 | Checker method and version. |
| `result` | [ReferenceCheckResult](#referencecheckresult) | exactly 1 | Typed outcome. |
| `evidence_ref` | [ArtifactReference](#artifactreference) | `0..1` | Optional finalized check evidence. |

**Identity:** `reference_check_id`. The stable check subject key is
`(check_kind, reference_use_id, relation_id|null, checked_by, method_ref)`. The use and optional
relation resolve to this check's `research_capture_id`. Independent checker/method subject keys
coexist so disagreement remains visible. A retry reuses [FactEnvelope](#factenvelope).`operation_id`;
a retry also preserves the canonical fact digest, while a revision supersedes only the current fact
in the same subject-key chain.  
**Operation:** [AppendResearchFact](operations.md#appendresearchfact).

---

### ResearchProblem

An addressable gap, contradiction, blocker, uncertainty or failed check surfaced by research.

| Field | Type | Required / Cardinality | Ownership and meaning |
|---|---|---:|---|
| `problem_id` | opaque string | exactly 1 | Stable problem subject identity. |
| `research_capture_id` | [ResearchCapture](#researchcapture).`research_capture_id` | exactly 1 | Owning capture. |
| `fact` | [FactEnvelope](#factenvelope) | exactly 1 | Immutable creation/extraction fact version. |
| `kind` | constrained string | exactly 1 | `gap`, `contradiction`, `blocker`, `uncertainty` or `failed_check`. |
| `statement` | string | exactly 1 | Attributed problem statement. |
| `blocks` | canonical sorted set of opaque subject refs | `0..N`, unique | Explicitly named blocked subjects. |
| `evidence_refs` | canonical sorted set of [ArtifactReference](#artifactreference) or fact refs | `0..N`, unique | Supporting evidence identities. |
| `extraction` | [ExtractionProvenance](#extractionprovenance) | exactly 1 | Origin of the problem statement. |

**Identity:** `problem_id`; disposition and assessment records associate only through explicit
[TargetRef](#disposition-and-assessment-payload-variants) and are never embedded mutable fields.  
**Lifecycle:** See planned [Problem disposition projection](states.md#problem-disposition-projection).  
**Operation:** [AppendResearchFact](operations.md#appendresearchfact).

---

### ResearchClaimExtraction

An addressable research-local proposition extracted from one capture.

| Field | Type | Required / Cardinality | Ownership and meaning |
|---|---|---:|---|
| `research_claim_id` | opaque string | exactly 1 | Stable research-local claim identity. |
| `research_capture_id` | [ResearchCapture](#researchcapture).`research_capture_id` | exactly 1 | Owning capture. |
| `fact` | [FactEnvelope](#factenvelope) | exactly 1 | Immutable creation/extraction fact version. |
| `statement` | string | exactly 1 | Attributed proposition. |
| `answer_ids` | canonical sorted set of [ResearchAnswer](#researchanswer).`research_answer_id` | `0..N`, unique | Explicit answer grounding. |
| `extraction` | [ExtractionProvenance](#extractionprovenance) | exactly 1 | Origin of the proposition. |

**Identity:** `research_claim_id`; it is not a global assertion or promoted-knowledge identity.
Every `answer_id` resolves to the same `research_capture_id` in L0.
Disposition/assessment association is derived from explicit
[TargetRef](#disposition-and-assessment-payload-variants), never an embedded list. Confidence is
not part of L0.  
**Lifecycle:** See planned [Claim disposition projection](states.md#claim-disposition-projection).  
**Operation:** [AppendResearchFact](operations.md#appendresearchfact).

---

### FormalizationCandidate

An addressable candidate notation and interpretation for exactly one
[ResearchClaimExtraction](#researchclaimextraction).

| Field | Type | Required / Cardinality | Ownership and meaning |
|---|---|---:|---|
| `formalization_id` | opaque string | exactly 1 | Stable candidate identity. |
| `research_capture_id` | [ResearchCapture](#researchcapture).`research_capture_id` | exactly 1 | Owning capture. |
| `fact` | [FactEnvelope](#factenvelope) | exactly 1 | Immutable creation/extraction fact version. |
| `research_claim_id` | [ResearchClaimExtraction](#researchclaimextraction).`research_claim_id` | exactly 1 | Sole natural-language claim target. |
| `notation` | string | exactly 1 | Candidate expression. |
| `latex` | string | `0..1` | Optional LaTeX rendering of the same expression. |
| `legend` | string-to-string map | exactly 1, non-empty | Human meanings for symbols. |
| `reading` | string | exactly 1 | Natural-language reading. |
| `logic_family` | string | exactly 1 | Named notation/logic family. |
| `assumptions` | string list | `0..N` | Explicit assumptions. |
| `scope` | string | exactly 1 | Domain in which the reading is intended. |
| `extraction` | [ExtractionProvenance](#extractionprovenance) | exactly 1 | Origin of the candidate. |
| `syntax_checker_ref` | opaque external ref | `0..1` | Optional syntax-check evidence. |
| `proof_check_ref` | opaque external ref | `0..1` | Optional proof/type-check evidence. |
| `governance_ref` | opaque external ref | `0..1` | Optional external acceptance reference; not owned by APT. |

**Identity:** `formalization_id`; `research_claim_id` resolves to the same
`research_capture_id` in L0. Even a reviewed candidate remains local unless an external
governance owner acts. Disposition/assessment association is derived from explicit
[TargetRef](#disposition-and-assessment-payload-variants), never an embedded list.  
**Lifecycle:** See planned
[Formalization disposition projection](states.md#formalization-disposition-projection).  
**Operation:** [AppendResearchFact](operations.md#appendresearchfact).

## Closed Embedded Shapes

These closed records are embedded fields or event payload variants referenced by registered
concepts. They are not additional DomainSpec concepts or registry IDs.

### ProducerRef Embedded Shape

`ProducerRef` is a discriminated union; anonymous and mixed variants are invalid.

| Variant | Required fields | Forbidden fields |
|---|---|---|
| `seat` | `kind=seat`, `group_id`, `seat_id`, `attempt_id`, `activation_id` | `host_actor_id` |
| `host_actor` | `kind=host_actor`, `host_actor_id`, `activation_id` | `group_id`, `seat_id`, `attempt_id` |

All required IDs are non-empty opaque owner-stamped values. For `seat`, `group_id`, `seat_id` and
`attempt_id` are copied from one ACI-owner-verified Attempt/capability binding; `activation_id` is
resolved by the host activation owner as a child of that exact Attempt. APT never derives any of
them from a persona, agent display name, file path, locator, recommendation text or temporal
proximity. The v1 shape deliberately does not duplicate `agent_instance_id`: a read model that
needs that identity must resolve it from an exact owner-bound ACI Attempt or
[AgentReferenceDelivery](../../agents-communication-infra/specs/domain.md#agentreferencedelivery)
record and must verify the containing capture's `dispatch_id` plus the stored `attempt_id` and
`seat_id` against that delivery's target tuple.

For `host_actor`, `host_actor_id` and `activation_id` come from the authenticated host context and
its owner evidence; `host_actor_id` cannot be a generic label such as `unknown`, `anonymous` or a
persona name. Equality compares the discriminator and every field of the selected variant.

```text
valid_seat_producer(capture, producer) <=>
  producer.kind = seat
  and host_activation_owner(producer.activation_id) =
      (producer.group_id, producer.seat_id, producer.attempt_id)
  and ACI_attempt_owner(producer.attempt_id) =
      (capture.dispatch_id, producer.group_id, producer.seat_id,
       owner_resolved_agent_instance_id)

locator_or_name_or_time_match => no_producer_authority
```

Both owner checks must agree on the complete owner-resolved
`(dispatch_id, group_id, seat_id, attempt_id, agent_instance_id, activation_id)` binding before
append or query binding succeeds. `agent_instance_id` is resolved from the exact ACI Attempt and
is not an additional caller-authored `ProducerRef` field.

### QuestionDerivationRef Embedded Union

| Variant | Required fields | L0 constraint |
|---|---|---|
| `dispatch_scope` | `kind`, [DispatchAuthoritySnapshotRef](#dispatchauthoritysnapshotref), `field_name`, `field_path` | `field_name` is one declared scope field; `field_path` is an RFC 6901 JSON Pointer into that versioned snapshot's canonical projection. |
| `research_question` | `kind`, `research_question_id`, `question_fact_id`, `research_capture_id`, `research_capture_digest` | The source question/fact/digest resolve to the same capture as the derived question. |

The union is closed; text similarity, dates and filenames cannot create a derivation. Equality
compares every selected-variant field. Dispatch-scope validation resolves the pointer only against
the exact `dispatch_snapshot_ref` owned by the derived question's `ResearchCapture` in L0; an
equivalent-looking or newer snapshot is not interchangeable. Planned negatives cover missing initial
`/`, invalid `~0`/`~1` escaping, nonexistent path, wrong field root, array-index error, unknown
snapshot version, cross-capture/cross-Dispatch snapshots, wrong snapshot identity, stale/superseded
snapshots and pointers that resolve only after non-canonical transformation.

### OriginRef Embedded Union

Every variant contains exactly its listed logical identity and evidence fields:

| Variant | Logical owner and identity | Required acceptance/evidence fields |
|---|---|---|
| `probe` | `owner_namespace=agent-provenance-telemetry`, `probe_schema_ref`, `probe_profile_ref {profile_id, profile_version, profile_digest}`, `probe_id` | `aci_acceptance_ref` |
| `probe_bundle` | `owner_namespace=agent-provenance-telemetry`, `bundle_schema_ref`, `probe_profile_ref {profile_id, profile_version, profile_digest}`, `probe_id`, `bundle_digest`, `committed_event_id` | `committed_event_digest` |
| `aci_event` | `owner_namespace=agents-communication-infra`, `contract_version`, `accepted_event_id` | `evidence_digest` |
| `aci_receipt` | `owner_namespace=agents-communication-infra`, `contract_version`, `receipt_id` | `evidence_digest` |
| `artifact` | `owner_namespace=agents-communication-infra`, `contract_version`, `artifact_id` | `evidence_digest` |
| `host_observation` | `owner_namespace=host`, `contract_version`, `source_observation_id` | `evidence_digest` |

For `probe`, logical APT schema/profile identity is not acceptance evidence.
Its `aci_acceptance_ref` is required and is the closed union
`{kind: accepted_event, accepted_event_id, owner_namespace=agents-communication-infra,
contract_version, evidence_digest}` or
`{kind: publication_receipt, receipt_id, owner_namespace=agents-communication-infra,
contract_version, evidence_digest}`. It must resolve to committed ACI acceptance/publication of the
exact logical probe identity. For `probe_bundle`, the identity is exactly
`(bundle_schema_ref, probe_profile_ref, probe_id, bundle_digest, committed_event_id)`; no synthetic
`bundle_id` exists. `committed_event_id + committed_event_digest` must resolve to the ACI event that
committed that exact bundle digest for the same probe/schema/profile identity.

The union is closed and equality compares the discriminator and every field of its selected
variant, including the complete ACI acceptance evidence for probe and bundle variants. Unknown
variant/namespace/version, missing digest or acceptance evidence, or opposite-variant fields fail
closed.

`probe_bundle` identifies only the committed source bundle. It does not identify a recipient
Attempt, prove inclusion in effective input or stand in for
[`reference_scout.bundle_delivered_to_agent@1`](../../agents-communication-infra/specs/events.md#referencescoutbundledeliveredtoagent).
A generic `aci_event` origin may identify that target delivery only after the ACI owner verifies
the exact event type, payload digest and referenced
[AgentReferenceDelivery](../../agents-communication-infra/specs/domain.md#agentreferencedelivery);
event timing, a shared locator or matching prose cannot create that meaning. For a containing
capture with `producer_ref.kind=seat`, the delivery is a valid delivery-to-producer origin only
when:

```text
delivery.dispatch_id = capture.dispatch_id
and delivery.target_attempt_id = capture.producer_ref.attempt_id
and delivery.target_seat_id = capture.producer_ref.seat_id
and ACI_attempt_group(delivery.target_attempt_id) = capture.producer_ref.group_id
and ACI_attempt_agent_instance(delivery.target_attempt_id) =
    delivery.target_agent_instance_id
```

A `host_actor` producer cannot treat an agent-target delivery as delivery to itself without a
separately typed owner-authoritative mapping.

### FailureEvidenceRef Embedded Union

`FailureEvidenceRef` is a separate closed union. It permits only committed evidence variants:
`aci_event {accepted_event_id}`, `aci_receipt {receipt_id}`, `artifact {artifact_id}`, or
`host_observation {source_observation_id}`. Each carries its required owner namespace
(`agents-communication-infra` for the first three, `host` for the last), `contract_version` and
`evidence_digest`. Bare `probe` and `probe_bundle` identities are invalid failure evidence.

Equality compares the entire selected variant. A supplied reference must resolve to an accepted
event, committed receipt, finalized artifact or committed host observation whose version and digest
match. An unknown kind, namespace/version mismatch, dangling/uncommitted identity or digest mismatch
fails closed.

### Disposition and Assessment Payload Variants

`TargetRef` is the closed record
`{target_kind: problem|claim|formalization, target_id, research_capture_id}`. The target must exist
in the named capture. Disposition values are selected by target kind:
[ProblemDisposition](#problemdisposition), [ClaimDisposition](#claimdisposition) or
[FormalizationDisposition](#formalizationdisposition).

These are only closed payload variants for the future
[ResearchFactAppended](events.md#researchfactappended) event contract. They have no
[FactEnvelope](#factenvelope), independent ID, Entity identity or lifecycle; the accepted ACI event
envelope supplies immutable event/fact identity.

| Payload variant | Required fields | Explicit ACI aggregate |
|---|---|---|
| `disposition_recorded` | `TargetRef`, matching disposition value, non-empty `actor_ref`, exact `policy_ref`, `aggregate_type`, `aggregate_id`, `expected_head_accepted_event_id`, `expected_aggregate_version` | `aggregate_type=apt.disposition-chain`; chain key is `(TargetRef, policy_ref)`. |
| `assessment_recorded` | `TargetRef`, matching assessment value, non-empty `actor_ref`, `method_ref`, exact `policy_ref`, `aggregate_type`, `aggregate_id`, `expected_head_accepted_event_id`, `expected_aggregate_version` | `aggregate_type=apt.assessment-chain`; chain key is `(TargetRef, actor_ref, method_ref, policy_ref)`. |

Both payload variants are append-only accepted events. Entities contain no
disposition/assessment arrays; association is a derived join from event payload `TargetRef`.
Independent assessor chains coexist, and projections retain disagreement instead of resolving it by
append order. `aggregate_id` is the ACI canonical [ContentDigest](#contentdigest) of the
variant-specific chain key. For an initial append, `expected_head_accepted_event_id` is canonical
null and `expected_aggregate_version=0`; a revision supplies the current aggregate head event and
version.

The ACI journal atomically compares the named aggregate's head event and aggregate version, appends
the accepted event, then advances both. An event envelope supplies event identity but does not
automatically establish or advance this chain. Wrong aggregate type/digest, stale head/version,
unknown or cross-aggregate event, and fact IDs fail the compare-and-swap.

## Value Objects

### FactEnvelope

| Field | Type | Constraint |
|---|---|---|
| `fact_id` | opaque string | Immutable identity of one accepted fact version. |
| `subject_id` | opaque string | Stable Entity subject shared across its versions. |
| `operation_id` | opaque string | Idempotency identity for the append. |
| `occurred_at` | offset timestamp | Owner-stamped occurrence time. |
| `supersedes_fact_id` | opaque string or null | When present, names the current predecessor for the same subject. |

**Equality:** All five fields are equal.  
**Invariant:** A predecessor belongs to the same subject, is current at append time, and cannot form
a cycle; absence means an initial or independent fact.

Every fact-bearing Entity binds `FactEnvelope.subject_id` to its stable Entity ID:

| Entity | Required subject binding |
|---|---|
| [ResearchQuestion](#researchquestion) | `subject_id = research_question_id` |
| [ResearchAnswer](#researchanswer) | `subject_id = research_answer_id` |
| [ResearchReferenceUse](#researchreferenceuse) | `subject_id = reference_use_id` |
| [ResearchReferenceClaimRelation](#researchreferenceclaimrelation) | `subject_id = relation_id` |
| [ReferenceCheck](#referencecheck) | `subject_id = reference_check_id` and the stable checker subject key remains invariant across revisions. |
| [ResearchProblem](#researchproblem) | `subject_id = problem_id` |
| [ResearchClaimExtraction](#researchclaimextraction) | `subject_id = research_claim_id` |
| [FormalizationCandidate](#formalizationcandidate) | `subject_id = formalization_id` |

A retry is identified by the same `operation_id` plus the same ACI-computed canonical payload digest
and returns the accepted receipt. Same operation with a different canonical payload digest is a
conflict. A revision uses a new operation/fact identity and names the current fact predecessor.

---

### ExtractionProvenance

| Field | Type | Constraint |
|---|---|---|
| `mode` | [ExtractionMode](#extractionmode) | Exactly one attribution mode. |
| `actor_ref` | opaque actor ref | Producer, host parser or reviewer identity. |
| `method_ref` | string | Extractor name and version. |
| `extracted_at` | offset timestamp | Owner-stamped extraction time. |
| `source_capture_id` | [ResearchCapture](#researchcapture).`research_capture_id` | Exact source capture. |
| `source_capture_digest` | [ContentDigest](#contentdigest) | Must match the pinned capture. |
| `selector` | [RawSelector](#rawselector) | Exact selection in finalized raw bytes. |

**Equality:** All fields are equal.  
**Invariant:** Attribution cannot be replaced by the captured producer identity unless that producer
actually performed the extraction.

---

### RawSelector

| Field | Type | Constraint |
|---|---|---|
| `schema_ref` | string | `apt.raw-selector@1` in L0. |
| `unit` | string | Exactly `utf8-byte`. |
| `start_inclusive` | non-negative integer | First selected byte. |
| `end_exclusive` | positive integer | Strictly greater than `start_inclusive`; at most the finalized raw byte length. |
| `selected_text_digest` | [ContentDigest](#contentdigest) | Digest of the exact selected byte slice. |

**Equality:** All fields are equal.  
**Invariant:** Selection is non-empty and uses exact stored UTF-8 bytes, half-open bounds
`0 <= start_inclusive < end_exclusive <= raw_byte_length`, and no Unicode/newline normalization.
The [ExtractionProvenance](#extractionprovenance) capture digest, owning
[ArtifactReference](#artifactreference) content digest and `selected_text_digest` all verify before
the fact is accepted. In L0, offsets address the exact finalized `raw_return` artifact bytes, and
that artifact must have a compatible textual media type with `charset=utf-8`. Decoded views,
transcoded derivatives and binary originals are not selector sources. The selected byte slice must
itself decode as valid UTF-8; boundaries cannot split a multibyte code point. Missing captures
cannot own any extracted fact or selector.

Planned negative fixtures reject: empty (`start=end`), negative, reversed or out-of-bounds ranges;
capture/artifact/selected digest mismatch; selectors that require normalization to match; and any
selector or extracted fact whose owning capture status is `missing`. They also reject binary or
incompatible media types, absent/non-UTF-8 charset, decoded/transcoded views, unfinalized artifacts,
invalid UTF-8 and start/end offsets inside a multibyte sequence.

---

### ContentDigest

| Field | Type | Constraint |
|---|---|---|
| `algorithm` | string | `sha256` in L0. |
| `value` | lowercase hexadecimal string | Exactly 64 hexadecimal characters for `sha256`. |

**Equality:** Normalized `algorithm` and exact `value` are equal.

---

### ArtifactReference

| Field | Type | Constraint |
|---|---|---|
| `artifact_id` | external ACI artifact identity | Finalized through the [ACI artifact boundary](../../agents-communication-infra/specs/interfaces.md#internal-artifact-boundary). |
| `content_digest` | [ContentDigest](#contentdigest) | Digest verified at finalization. |
| `media_type` | string | Explicit media type. |
| `charset` | string or null | Fixed to `utf-8` for an L0 `raw_return`; null only for artifacts outside the L0 capture path. |
| `classification` | external ACI classification value | Owner-stamped data class. |
| `redaction_policy_ref` | opaque external ref | Exact policy applied or required. |
| `retention_policy_ref` | opaque external ref | Exact retention policy. |
| `tombstone_policy_ref` | opaque external ref | Exact missing/erased-content behavior. |
| `finalization_receipt_ref` | opaque ACI receipt ref | Evidence that the ACI boundary finalized the artifact reference. |

**Equality:** All fields are equal.  
**Invariant:** APT never embeds raw bytes in this value and never addresses the physical artifact
backend. In L0, every present `raw_return` is this value object, finalized with a compatible textual
media type and `charset=utf-8`; binary, undecoded and non-UTF-8 returns fail closed.

---

### DispatchAuthoritySnapshotRef

A closed discriminated union for pinned external Dispatch authority.

| Field | Type | Constraint |
|---|---|---|
| `kind` | `aci_managed \| legacy_ledger` | Required discriminator. |
| `dispatch_id` | external Dispatch ID | Required only for `aci_managed`. |
| `artifact_ref` | external ACI artifact ref | Required only for `aci_managed`. |
| `artifact_digest` | [ContentDigest](#contentdigest) | Required only for `aci_managed`. |
| `accepted_event_id` | external ACI event ID | Required only for `aci_managed`. |
| `accepted_offset` | non-negative integer | Required only for `aci_managed`. |
| `ledger_row_identity` | `{dispatch_id, row_kind, appender_identity, contract_version}` | Required only for `legacy_ledger`; contains the authoritative Dispatch identity. |
| `row_digest` | [ContentDigest](#contentdigest) | Required only for `legacy_ledger`. |
| `non_authoritative_locator` | `{row_index}` | Optional only for `legacy_ledger`; lookup hint excluded from authority/hash. |

**Equality:** `aci_managed` compares every required authority field. `legacy_ledger` compares
`kind + ledger_row_identity + row_digest`; locator changes do not change authority equality.  
**Invariant:** Unknown variants, mixed variant fields or omitted authority fields are invalid.
Deterministic hash follows the same variant-specific equality surface. When embedded by a
[ResearchCapture](#researchcapture), the owning capture's `dispatch_id` equals this union's
`dispatch_id` for `aci_managed` or `ledger_row_identity.dispatch_id` for `legacy_ledger`.

---

### ProbeRecommendationRef

| Field | Type | Constraint |
|---|---|---|
| `probe_id` | opaque external probe ID | Exact committed probe. |
| `recommendation_id` | opaque external recommendation ID | Exact recommendation within the bundle. |
| `bundle_digest` | [ContentDigest](#contentdigest) | Exact committed bundle digest. |
| `profile_binding` | [ACIProtocolProfileBinding](#aciprotocolprofilebinding) | Required whenever this value exists. |
| `bundle_acceptance_ref` | closed ACI acceptance ref | Accepted event or publication receipt plus contract version and evidence digest. |
| `profile_registration_ref` | closed ACI registry ref | Registry event or receipt plus the exact profile ID, version and digest. |
| `source_observation_ids` | canonical sorted set of external [`host.SourceObservation`](../discovery/session-dispatch-research-records.md#43-reference-uses-and-checks) IDs | `0..N`, unique; each supplied ID remains host-owned. |

`bundle_acceptance_ref` is exactly one of
`{kind: accepted_event, accepted_event_id, contract_version, evidence_digest}` or
`{kind: publication_receipt, receipt_id, contract_version, evidence_digest}`.
`profile_registration_ref` is exactly one of
`{kind: registry_event, accepted_event_id, protocol_profile_id, protocol_profile_version,
protocol_profile_digest, contract_version, evidence_digest}` or
`{kind: registry_receipt, receipt_id, protocol_profile_id, protocol_profile_version,
protocol_profile_digest, contract_version, evidence_digest}`. Both unions are closed and owned by
`agents-communication-infra`.

**Equality:** All fields, including canonically sorted observation IDs, are equal.  
**Invariant:** This value is optional on [ResearchReferenceUse](#researchreferenceuse); direct use has
no implied probe or profile. Append verifies that bundle acceptance resolves to the same
`(probe_id, bundle_digest, recommendation_id)` identity and that profile registration resolves to
the same profile ID/version/digest as `profile_binding`; cross-bundle, cross-profile, stale,
uncommitted, unknown-variant or digest-mismatched evidence fails closed.

Under the frozen v1 `reference-probe` compatibility profile, the stored field remains `probe_id`;
no profile-shape or profile-digest change is implied. Resolution to the product `scout_run_id`
comes only from an explicit owner-verified alias record bound to the exact accepted
[`reference_scout.bundle_committed@1`](../integration/stage-g/reference-scout-and-ingestion.md#reference-scout-lifecycle)
event, bundle artifact/digest and ScoutRun. Neither that commit event nor ScoutRun owner evidence
is treated as carrying `probe_id`. Recommendation membership comes from the accepted commit plus
the digest-matching immutable bundle bytes. Neither the later Scout lifecycle
[`reference_scout.bundle_delivered@1`](../integration/stage-g/reference-scout-and-ingestion.md#reference-scout-lifecycle)
fact nor locator equality supplies recommendation membership. `source_observation_ids`, when
present, are only host-owned reference identities; their presence alone proves nothing. Only
successful resolution through the exact versioned host-owned contract proves the recorded
observation/coverage level, and that evidence never proves declared use or claim support.

---

### ACIProtocolProfileBinding

| Field | Type | Constraint |
|---|---|---|
| `protocol_profile_id` | opaque external ACI profile ID | Exact registered profile. |
| `protocol_profile_version` | string | Exact registered version. |
| `protocol_profile_digest` | [ContentDigest](#contentdigest) | Digest resolved by the ACI owner, never caller-authored authority. |

**Equality:** All three fields are equal.  
**Invariant:** A probe-origin value is invalid if any field is absent or mismatches committed bundle
evidence.

## Enums

### CaptureStatus

| Value | Description |
|---|---|
| `captured` | A complete returned witness exists as exactly one [ArtifactReference](#artifactreference). |
| `partial` | An incomplete returned witness exists as exactly one [ArtifactReference](#artifactreference). |
| `missing` | No raw witness exists; expected contribution and failure evidence remain recorded. |

`superseded` is a derived currentness label, not a [CaptureStatus](#capturestatus) value.

---

### ExtractionMode

| Value | Description |
|---|---|
| `verbatim` | The selected bytes directly express the recorded structure. |
| `declared` | The actor explicitly declared the structure represented by the fact. |
| `inferred` | The extractor interpreted the structure from the captured evidence. |

---

### ReferenceUseKind

| Value | Description |
|---|---|
| `mentioned` | The reference is mentioned without a citation or consultation assertion. |
| `cited` | The reference is presented as a citation. |
| `claimed_consulted` | The producer claims consultation; this is not host access evidence. |

---

### ReferenceCheckKind

| Value | Description |
|---|---|
| `source_identity` | Evaluates whether the referenced source identity/locator matches evidence. |
| `access_evidence` | Evaluates available host-mediated access evidence. |
| `claim_support` | Evaluates one [ResearchReferenceClaimRelation](#researchreferenceclaimrelation). |

---

### ReferenceCheckResult

| Value | Description |
|---|---|
| `pass` | The named check condition was satisfied by its evidence. |
| `fail` | The named check condition was not satisfied. |
| `indeterminate` | Available evidence did not decide the named check. |

---

### ProblemDisposition

| Value | Description |
|---|---|
| `observed` | Recorded but not yet independently validated. |
| `validated` | Confirmed as a current research problem. |
| `resolved` | Addressed within the research-local review. |
| `accepted_risk` | Retained knowingly without claiming resolution. |
| `refuted` | Later evidence rejects the problem statement. |

---

### ClaimDisposition

| Value | Description |
|---|---|
| `proposed` | Recorded as a research-local proposition. |
| `supported` | Current research-local assessment finds support. |
| `contested` | Current assessments preserve substantive disagreement. |
| `refuted` | Current research-local assessment rejects the proposition. |

---

### FormalizationDisposition

| Value | Description |
|---|---|
| `candidate` | Proposed notation awaiting or retaining review. |
| `reviewed` | Reviewed within research without becoming canonical vocabulary. |
| `rejected` | Rejected as a useful representation; the natural-language claim may remain. |

## Cross-Entity Invariants

Every relational collection (`origin_refs`, `derives_from`, `question_ids`, `blocks`,
`evidence_refs`, `answer_ids`, and `source_observation_ids`) is encoded as a unique canonical sorted
set. Sorting uses ascending bytewise comparison of each element's ACI canonical encoding; caller
order is non-semantic, and duplicate input is rejected rather than silently deduplicated.
`synthesizes` is the sole relational exception: it is unique but semantically ordered, so
permutations differ. `assumptions` is authored content, not a relational ID/ref collection.

| ID | Invariant | Planned Rule Source |
|---|---|---|
| APT-DOM-1 | `session.dispatch_linked` solely owns Session-to-Dispatch; `ResearchCapture.dispatch_id` solely owns Dispatch-to-Research, with `0..N` captures per Dispatch, and equals the Dispatch identity in either snapshot variant. | [APT-R1](rules.md#apt-r1--single-join-authority) |
| APT-DOM-2 | Every Entity creation/version is immutable; correction appends a current-predecessor fact or capture. Disposition/assessment payloads are immutable accepted ACI events, not Entities. | [APT-R2/R5](rules.md#apt-r2--idempotent-append) |
| APT-DOM-3 | All capture status slots are present. `captured` has a finalized UTF-8 textual artifact and all reason/evidence slots null; `partial` has that artifact, non-empty `partial_reason`, null `failure_reason` and optional committed evidence; `missing` has null artifact/partial reason, non-empty `failure_reason` and required committed evidence. | [APT-R3](rules.md#apt-r3--artifact-only-raw-return) |
| APT-DOM-4 | Every extracted question, answer, use, relation, problem, claim and formalization carries non-empty byte-exact capture/artifact/selection-digest-bound [ExtractionProvenance](#extractionprovenance); a `missing` capture owns no extracted facts. | [APT-R4](rules.md#apt-r4--extraction-provenance) |
| APT-DOM-5 | `claim_support` requires exactly one relation; source-identity/access checks forbid it. | Planned [Reference check rules](rules.md#reference-check-typing) |
| APT-DOM-6 | A [FormalizationCandidate](#formalizationcandidate) targets exactly one research-local claim and never represents ontology acceptance by itself. | Planned [Formalization rule](rules.md#formalization-locality) |
| APT-DOM-7 | `ProbeRecommendationRef present ⇒ exact ACIProtocolProfileBinding + same-identity bundle acceptance + same-profile registry evidence`; direct reference uses require none of them. | [APT-R7](rules.md#apt-r7--protocol-profile-binding) |
| APT-DOM-8 | APT stores only external IDs/evidence values for Dispatch, ACI artifacts/profiles/events and `host.SourceObservation`; ownership never transfers. | [Architecture boundary](architecture.md#scope-boundary) |
| APT-DOM-9 | In L0, question derivation, answer-to-question, relation-to-use/claim, check-to-use/relation, claim-to-answer and formalization-to-claim edges stay within one `research_capture_id`; cross-capture provenance is represented only by explicit `synthesizes` pins, not a local fact edge. | Planned [Locality rule](rules.md#research-fact-locality) |
| APT-DOM-10 | Synthesis pins are a semantic ordered list: unique, preexisting, current-at-append, same-Dispatch, non-self and exact-digest; order participates in equality/output digest, so permutations intentionally differ, while later input supersession changes display state only. | Planned [Synthesis rule](rules.md#research-synthesis-pins) |
| APT-DOM-11 | A ReferenceCheck subject key includes kind, use, optional relation, checker and method; retry shares operation identity, revision stays within that chain, and independent checker chains coexist. | Planned [Reference check rules](rules.md#reference-check-typing) |
| APT-DOM-12 | Disposition/assessment are only closed event payloads mapped to explicit ACI aggregates `apt.disposition-chain`/`apt.assessment-chain`; aggregate ID is the canonical chain-key digest, and the journal atomically CASes expected head event+aggregate version before append. The envelope alone creates no chain. | Planned [Disposition rule](rules.md#disposition-and-assessment-chains) |
| APT-DOM-13 | Every fact-bearing Entity binds `FactEnvelope.subject_id` to its stable Entity ID. Retry means the same `operation_id` plus identical ACI canonical payload digest; a differing digest conflicts, while revision uses a new operation/fact ID and current predecessor. | Planned [Fact append rules](rules.md#fact-append-identity) |
| APT-DOM-14 | `capture_digest` is computed only by the ACI canonicalizer from every closed slot in the exact `apt.research-capture@1` projection listed above, excluding the digest field; nonapplicable values are canonical null, and missing schema/slot fails before digesting. | Planned [Capture digest rule](rules.md#capture-digest) |
| APT-DOM-15 | A `RawSelector` addresses a non-empty, valid UTF-8 byte slice directly in the finalized compatible textual `raw_return` artifact; binary/non-UTF-8 returns, decoded/transcoded views, unfinalized artifacts and multibyte splits fail closed. | Planned [Selector rule](rules.md#raw-selector-validity) |
| APT-DOM-16 | `OriginRef` separates logical APT probe/bundle schema/profile identity from required committed ACI event/publication evidence. `FailureEvidenceRef` permits only committed event, receipt, artifact or host-observation evidence; bare probe/bundle refs and unknown, dangling or mismatched refs fail closed. | Planned [Evidence reference rule](rules.md#evidence-reference-validity) |
| APT-DOM-17 | A dispatch-scope derivation uses the exact owning capture snapshot and an RFC 6901 JSON Pointer resolved only against that pinned versioned canonical projection; malformed paths plus cross/wrong/stale snapshots fail closed. | Planned [Question derivation rule](rules.md#question-derivation-validity) |
| APT-DOM-18 | Every relational ID/ref list is a duplicate-rejecting canonical sorted set with non-semantic input order, except the unique semantic ordered `synthesizes` list. | Planned [Collection canonicalization rule](rules.md#relational-collection-canonicalization) |
| APT-DOM-19 | A declared reference use is attributable to one target Attempt only when its owning `ResearchCapture.producer_ref` is the `seat` variant and `capture.dispatch_id` plus `producer_ref.{group_id,seat_id,attempt_id}` equal the complete ACI owner-resolved target. `agent_instance_id` is resolved by the owner from that exact Attempt/delivery and is never inferred or stored implicitly in `ProducerRef`. `ExtractionProvenance.actor_ref` identifies the extractor and cannot replace that target identity. | [AgentReferenceLineage](queries.md#agentreferencelineage) |
| APT-DOM-20 | A recommendation joins an ACI target delivery only when owner evidence verifies an explicit alias from legacy `ProbeRecommendationRef.probe_id` to the delivery's `scout_run_id`, the accepted `reference_scout.bundle_committed@1`, digest-matching immutable bundle bytes, and exact `recommendation_id` membership. The later `reference_scout.bundle_delivered@1` carries no membership, and string or locator equality alone is insufficient. | [AgentReferenceLineage](queries.md#agentreferencelineage) |
| APT-DOM-21 | `access_observed` requires host-owner evidence that one `SourceObservation` is bound exactly to the target `AgentReferenceDelivery`, recommendation and owner-resolved dispatch/group/seat/Attempt/agent-instance tuple, with an observation kind that the versioned host contract defines as access. A use's `ProbeRecommendationRef.source_observation_ids` may name the same observation but is neither required nor sufficient to activate this independent axis. Search-result visibility, locator/digest/text equality, Scout-worker observation or another Attempt cannot join or activate it. | [AgentReferenceLineage](queries.md#agentreferencelineage) |
| APT-DOM-22 | `recommended`, `delivered`, `access_observed`, `declared_used`, `claim_relation` and `claim_support_check` are independent derived evidence axes. Presence or absence on one axis never synthesizes another. | [AgentReferenceLineage](queries.md#agentreferencelineage) |

## Deferred Structural Extensions

`confidence` is absent from [ResearchClaimExtraction](#researchclaimextraction) in L0. Any future
confidence concept requires a separately registered typed Value Object with at least value,
scale/range and version, actor, method/version, source selector/evidence, calibration semantics and
explicit missingness. A scalar or unowned confidence field is not a compatible extension.

## External References, Not APT Concepts

| External reference | Owner | APT representation |
|---|---|---|
| Dispatch / confirmed dispatch row | Existing dispatch ledger or ACI authority variant | `dispatch_id` plus [DispatchAuthoritySnapshotRef](#dispatchauthoritysnapshotref). |
| `host.SourceObservation` | Host-mediated acquisition boundary | Nullable foreign ID in [ResearchReferenceUse](#researchreferenceuse) or [ProbeRecommendationRef](#proberecommendationref). |
| `agents-communication-infra.AgentReferenceDelivery` | ACI target-input settlement authority | Read-only accepted delivery ID/event, source Scout/bundle membership and owner-derived target Attempt/seat/agent-instance. |
| `agents-communication-infra.EffectiveInputArtifact` | ACI canonical effective-input authority | Read-only proof that the exact `reference_bundle` entry was included for the target Attempt. |
| ACI artifact and physical bytes | ACI artifact finalization boundary; physical backend remains external | [ArtifactReference](#artifactreference) only. |
| ACI event/journal/receipt/profile | ACI | IDs, digests and [ACIProtocolProfileBinding](#aciprotocolprofilebinding). |
| Knowledge/assertion/ontology acceptance | Future external governance | Optional foreign mapping/governance refs; never inferred from APT status. |

## Planned Aspect Links

- Mutations and formal pre/postconditions: `operations.md`.
- Derived currentness/disposition projections: `states.md`.
- Cross-entity rules and formal expressions: `rules.md`.
- Accepted immutable fact payloads: `events.md`.
- Read aggregation and as-of formulas: `queries.md`.

These planned anchors require final cross-link validation when their files pass review. This domain
document does not authorize implementation while the [work-pack mutation gate](../WORK-PACK.md#mutation-gate-authority-and-evidence)
is blocked.
