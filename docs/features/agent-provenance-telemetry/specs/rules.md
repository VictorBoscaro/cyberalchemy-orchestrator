---
tags: [agent-provenance-telemetry, spec, rules]
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

# Rules: Agent Provenance Telemetry

These rules make the approved APT authority, integrity, replay and evidence boundaries directly
testable. They do not claim that an ACI profile, adapter, store or runtime exists.

Normative sources are [SPEC.md](SPEC.md), [architecture.md](architecture.md),
[domain.md](domain.md), [states.md](states.md), [operations.md](operations.md), and the
[focused discovery](../discovery/session-dispatch-research-records.md). External evidence is bound
by its owner before pure domain validation; no rule below transfers that authority to APT.

## APT-R1 — Single Join Authority

**Applies To:** [SessionDispatchLink](domain.md#sessiondispatchlink),
[ResearchCapture](domain.md#researchcapture), [LinkSessionDispatch](operations.md#linksessiondispatch),
[AppendResearchCapture](operations.md#appendresearchcapture)

`SessionDispatchLinked` is the sole persisted Session-to-Dispatch edge.
`ResearchCapture.dispatch_id` is the sole persisted Dispatch-to-Research edge. Reverse joins,
summary fields and lists are projections only; existing Dispatch authority remains external.

```text
authoritative_edge(Session,Dispatch) = SessionDispatchLinked
authoritative_edge(Dispatch,ResearchCapture) = ResearchCapture.dispatch_id
∀d: |session_link(d)| ≤ 1
capture.dispatch_id = snapshot_dispatch_identity(capture.dispatch_snapshot_ref)
```

An exact existing link is a semantic no-op; a contradictory Session link conflicts. An append
requiring a current context must resolve the current Session and its exact preexisting link at one
accepted offset.

**Checked by:** planned [APT-TEST-R1](../TEST-SPEC.md#apt-r1--single-join-authority).

## APT-R2 — Idempotent Append

**Applies To:** all six [Operations](operations.md)

Command identity and ACI canonical command digest jointly determine retry behavior. Durable ACI
acceptance precedes acknowledgment. A never-submitted semantic no-op creates no command receipt or
idempotency claim.

```text
submitted(id,digest) ∧ retry(id,digest)
  ⇒ Δjournal=0 ∧ same(receipt)

submitted(id,digest₁) ∧ retry(id,digest₂) ∧ digest₁≠digest₂
  ⇒ IDEMPOTENCY_CONFLICT ∧ Δjournal=0

¬submitted(id) ∧ submitted_new=∅
  ⇒ no_command ∧ no_receipt ∧ semantic_existing_refs
```

For a multi-event operation, all `submitted_new` events, their head changes and their receipt
commit in one ACI transaction or none commits. Existing exact members remain outside that receipt.
Uncertain post-commit delivery retries the same identity and returns the persisted receipt/result.

**Checked by:** planned [APT-TEST-R2](../TEST-SPEC.md#apt-r2--idempotent-append).

## APT-R3 — Artifact-Only Raw Return

**Applies To:** [ResearchCapture](domain.md#researchcapture),
[AppendResearchCapture](operations.md#appendresearchcapture)

Every `apt.research-capture@1` slot is present. Conditional non-values are canonical nulls; omission
is invalid. L0 never embeds raw bytes.

| `capture_status` | `raw_return` | `partial_reason` | `failure_reason` | `failure_evidence_ref` |
|---|---|---|---|---|
| `captured` | exactly one finalized textual UTF-8 ArtifactReference | null | null | null |
| `partial` | exactly one finalized textual UTF-8 ArtifactReference | non-empty | null | committed ref or null |
| `missing` | null | null | non-empty | exactly one committed ref |

```text
captured ⇒ |raw_return|=1 ∧ no_reason_or_failure_evidence
partial  ⇒ |raw_return|=1 ∧ nonempty(partial_reason) ∧ failure_reason=null
missing  ⇒ raw_return=null ∧ partial_reason=null
           ∧ nonempty(failure_reason) ∧ committed(failure_evidence_ref)
```

**Checked by:** planned [APT-TEST-R3](../TEST-SPEC.md#apt-r3--artifact-only-raw-return).

## APT-R4 — Extraction Provenance

**Applies To:** every extracted fact Entity in [domain.md](domain.md),
[AppendResearchFact](operations.md#appendresearchfact),
[AppendReferenceProbeLineage](operations.md#appendreferenceprobelineage)

Every extracted question, answer, reference use/relation, problem, claim and formalization carries
one complete `ExtractionProvenance`. The actor is the attributed extractor, not automatically the
command-ingestion actor.

```text
valid_extraction(x) ⇔
  x.mode∈{verbatim,declared,inferred}
  ∧ nonempty(x.actor_ref,x.method_ref)
  ∧ current_nonmissing(x.source_capture_id,x.source_capture_digest)
  ∧ valid_raw_selector(x.selector)
  ∧ performed_extraction(x.actor_ref,x.method_ref)
```

A missing capture owns no extracted facts. Equality between extraction and ingestion actor is valid
only when that authenticated principal performed the registered extraction method.

**Checked by:** planned [APT-TEST-R4](../TEST-SPEC.md#apt-r4--extraction-provenance).

## APT-R5 — Capture Supersession

**Applies To:** [ResearchCapture](domain.md#researchcapture),
[AppendResearchCapture](operations.md#appendresearchcapture),
[Research capture currentness](states.md#research-capture-currentness)

Capture bytes/status never mutate. A correction appends a new capture naming the current head of the
same `(dispatch_id, expected_contribution_id)` chain.

```text
initial(c)     ⇔ supersedes_capture_id=null ∧ head(chain(c))=null
replacement(c)⇒ supersedes_capture_id=head_before(chain(c))
current_o(c)  ⇔ head_o(chain(c))=c.research_capture_id
```

Stale, unknown, cross-chain, self and cyclic predecessors reject without an event. `superseded` is
a projection label, never a `CaptureStatus`.

**Checked by:** planned [APT-TEST-R5](../TEST-SPEC.md#apt-r5--capture-supersession).

## APT-R6 — Replay Determinism

**Applies To:** [State and Projection Semantics](states.md),
[architecture projection reducer](architecture.md#view-3-low-level-components-view)

Replay is a pure fold over complete verified ACI command groups and a pinned Dispatch authority
snapshot. It performs no external call, append, repair, wall-clock read or current-state lookup.

```text
effective_as_of(requested_o) =
  max({g.last_offset | verified(g) ∧ g.last_offset≤requested_o} ∪ {genesis})

projection(requested_o,pinned_inputs) =
  fold(accepted_groups≤effective_as_of(requested_o),pinned_inputs)

same(prefix,pinned_inputs) ⇒ same(projection,hash,cursor)
```

Every response exposes `requested_o` and `effective_as_of`. Current external Dispatch context and
reorderable legacy locators stay outside deterministic hashes.

**Checked by:** planned [APT-TEST-R6](../TEST-SPEC.md#apt-r6--replay-determinism).

## APT-R7 — Protocol Profile Binding

**Applies To:** [ProbeRecommendationRef](domain.md#proberecommendationref),
[AppendReferenceProbeLineage](operations.md#appendreferenceprobelineage)

Probe-origin lineage requires bundle acceptance and profile-registration evidence matching the
same probe, recommendation, bundle and exact profile ID/version/digest. Direct reference use has no
probe/profile requirement.

```text
probe_ref present ⇒
  committed(bundle_acceptance_ref)
  ∧ registration(profile_id,profile_version,profile_digest)
  ∧ bundle_profile=registration_profile=probe_ref.profile_binding

direct_use ⇒ probe_recommendation_ref absent
```

Atomic multi-event operations also require the exact registered ACI receipt/read-grouping profile.
Entity-fact/probe append separately requires
`aci.transactional-semantic-uniqueness-result-mapping@1` with its exact ACI-published digest and
registration receipt. Any absent or mismatched required profile blocks implementation and produces
no mutation.

**Checked by:** planned [APT-TEST-R7](../TEST-SPEC.md#apt-r7--protocol-profile-binding).

## APT-R8 — Telemetry Non-Authority

**Applies To:** all APT operations, projections and observability paths

Logs, traces, metrics and read projections describe accepted outcomes but never authorize, append,
advance, repair, adjudicate or replay state. Raw artifact bodies never enter them.

```text
authority(logs ∪ traces ∪ metrics ∪ projections) = ∅
raw_body ∉ events ∪ projections ∪ logs ∪ traces ∪ metrics
Δauthoritative_state(telemetry_signal)=0
```

A probe-worker observation does not establish research-agent access, consultation or claim support.

**Checked by:** planned [APT-TEST-R8](../TEST-SPEC.md#apt-r8--telemetry-non-authority).

## Subordinate Coverage Clauses

APT-C01 through APT-C18 are stable coverage-clause IDs subordinate to APT-R1..APT-R8. They are not
additional DomainSpec Rule concepts and do not extend the [SPEC Concept Registry](SPEC.md#concept-registry).
Explicit legacy anchors preserve all approved cross-document references.

The referenced-anchor inventory is exactly 26: eight heading-derived anchors for APT-R1..APT-R8
plus the 18 explicit legacy anchors attached to APT-C01..APT-C18 below.

<a id="session-context-binding"></a>

## APT-C01 — Session Context Binding

`ensure_key` deduplicates initial creation; context identity is the exact host-owned
`(origin_kind, origin_ref)` tuple. If materialized, its key equals the ACI canonical digest of that
tuple and cannot be caller-selected.

```text
context_key=H_ACI({origin_kind,origin_ref})
|binding_o(origin_kind,origin_ref)|≤1
EnsureSession(bound_context) ⇒ reuse(binding) ∧ no_rename ∧ Δjournal=0
```

**Checked by:** planned [APT-TEST-C01](../TEST-SPEC.md#session-context-binding).

<a id="rollover-authorization"></a>

## APT-C02 — Rollover Authorization

The external host authorization owner binds one authenticated principal, action, origin tuple,
expected current Session, policy version/digest, expiry, nonce and evidence digest. The application
consumes that evidence before pure validation.

```text
authorized_rollover ⇔
  action=start_new_session
  ∧ expected_current_session_id=binding(origin)
  ∧ verified(policy_digest,evidence_digest,principal,nonce)
  ∧ host_owner_validated_expiry
```

Successor `SessionStarted` and `SessionContextRebound` pin identical authorization/origin fields and
commit in one verified atomic command group. Replay verifies pins and never reexecutes policy.

**Checked by:** planned [APT-TEST-C02](../TEST-SPEC.md#rollover-authorization).

<a id="link-session-dispatch-authorization"></a>

## APT-C03 — Link Session Dispatch Authorization

The authenticated current context principal must be authorized for the exact Dispatch action and
pinned snapshot. Caller-supplied authority values are ignored/rejected.

```text
authorized_link ⇔
  session_id=binding(origin,offset)
  ∧ dispatch_id=snapshot_dispatch_identity(snapshot_ref)
  ∧ verified(action_policy_digest,authorization_evidence_digest)
```

**Checked by:** planned [APT-TEST-C03](../TEST-SPEC.md#link-session-dispatch-authorization).

<a id="dispatch-snapshot-identity"></a>

## APT-C04 — Dispatch Snapshot Identity

`DispatchAuthoritySnapshotRef` is the closed `aci_managed | legacy_ledger` union from
[domain.md](domain.md#dispatchauthoritysnapshotref).

```text
aci_hash = H_ACI(complete_aci_managed_variant)
legacy_hash = H_ACI({kind,ledger_row_identity,row_digest})
```

No authority field may be omitted. `legacy_ledger.non_authoritative_locator.row_index` is excluded
from authority equality/hash; current external state is display-only.

**Checked by:** planned [APT-TEST-C04](../TEST-SPEC.md#dispatch-snapshot-identity).

<a id="capture-digest"></a>

## APT-C05 — Capture Digest

`capture_digest` is the ACI canonical digest of every closed `apt.research-capture@1` slot listed in
[ResearchCapture](domain.md#researchcapture), excluding only `capture_digest` itself.

```text
capture_digest = H_ACI(canonical(closed_capture_preimage_without_digest))
keys(preimage)=closed_slots(apt.research-capture@1)
```

Unknown/missing slots fail before canonicalization. Relational sets canonicalize; semantic
`synthesizes` order remains digest-significant.

**Checked by:** planned [APT-TEST-C05](../TEST-SPEC.md#capture-digest).

<a id="research-synthesis-pins"></a>

## APT-C06 — Research Synthesis Pins

Each synthesis pin is unique, preexisting, current at append, same-Dispatch, non-self and
digest-exact. The list is semantically ordered.

```text
∀p∈synthesizes:
  accepted_before(p.capture_id)
  ∧ current_at_append(p.capture_id)
  ∧ dispatch(p.capture_id)=output.dispatch_id
  ∧ p.capture_id≠output.capture_id
  ∧ p.capture_digest=accepted_digest(p.capture_id)
```

Later input supersession changes display state only and never rewrites the pin.

**Checked by:** planned [APT-TEST-C06](../TEST-SPEC.md#research-synthesis-pins).

<a id="raw-selector-validity"></a>

## APT-C07 — Raw Selector Validity

The selector addresses the finalized raw artifact's exact stored UTF-8 bytes.

```text
0≤start_inclusive<end_exclusive≤raw_byte_length
∧ utf8(raw_bytes[start_inclusive:end_exclusive])
∧ H(raw_bytes[start_inclusive:end_exclusive])=selected_text_digest
```

Normalization, transcoding, decoded derivatives, binary/incompatible media, unfinalized artifacts
and multibyte boundary splits reject.

**Checked by:** planned [APT-TEST-C07](../TEST-SPEC.md#raw-selector-validity).

<a id="evidence-reference-validity"></a>

## APT-C08 — Evidence Reference Validity

Every `OriginRef` and `FailureEvidenceRef` matches its closed discriminator, owner namespace,
contract version, committed identity and evidence digest. Probe/bundle logical identity is not
acceptance evidence. Bare probe/bundle identities are invalid failure evidence.

**Checked by:** planned [APT-TEST-C08](../TEST-SPEC.md#evidence-reference-validity).

<a id="question-derivation-validity"></a>

## APT-C09 — Question Derivation Validity

A dispatch-scope derivation uses the exact owning capture snapshot and a valid RFC 6901 pointer
against that snapshot's canonical projection. A research-question derivation names an accepted fact
in the same capture with exact capture digest.

```text
dispatch_scope ⇒ snapshot_ref=owning_capture.snapshot_ref ∧ resolves_rfc6901(field_path)
research_question ⇒ same_capture(source,target) ∧ exact(source_fact_id,capture_digest)
```

Text similarity, filenames, dates, newer snapshots and normalized paths cannot create derivation.

**Checked by:** planned [APT-TEST-C09](../TEST-SPEC.md#question-derivation-validity).

<a id="research-fact-appended-closed-union"></a>

## APT-C10 — Research Fact Appended Closed Union

Exactly one payload variant is present. Entity variants carry `FactEnvelope` and fact-head CAS only;
disposition/assessment variants carry explicit aggregate CAS only and never `FactEnvelope`.

```text
entity_variant xor disposition_recorded xor assessment_recorded
entity_variant ⇒ fact_CAS ∧ ¬aggregate_CAS
aggregate_variant ⇒ aggregate_CAS ∧ ¬FactEnvelope ∧ ¬fact_CAS
```

**Checked by:** planned [APT-TEST-C10](../TEST-SPEC.md#research-fact-appended-closed-union).

<a id="research-fact-locality"></a>

## APT-C11 — Research Fact Locality

All L0 fact edges resolve inside one current non-missing `research_capture_id`. Cross-capture
provenance is represented only by explicit capture synthesis pins.

```text
∀edge∈local_fact_edges:
  capture(source(edge))=capture(target(edge))=owning_capture
```

**Checked by:** planned [APT-TEST-C11](../TEST-SPEC.md#research-fact-locality).

<a id="research-fact-typing"></a>

## APT-C12 — Research Fact Typing

Each payload matches its exact closed Entity schema, stable subject binding and relationship
cardinality. Unknown fields and duplicate relational members reject.

```text
FactEnvelope.subject_id=stable_entity_id(payload)
valid(payload) ⇒ exact_schema_variant(payload) ∧ valid_local_edges(payload)
```

Reference relation, check and formalization constraints are further fixed below.

**Checked by:** planned [APT-TEST-C12](../TEST-SPEC.md#research-fact-typing).

<a id="reference-check-typing"></a>

## APT-C13 — Reference Check Typing

`claim_support` requires exactly one same-capture `ResearchReferenceClaimRelation`.
`source_identity` and `access_evidence` forbid that relation. Every check independently names its
use, checker and method.

```text
check_kind=claim_support
  ⇔ |relation_id|=1 ∧ relation.reference_use_id=check.reference_use_id

check_kind∈{source_identity,access_evidence}
  ⇒ relation_id absent
```

No check produces a generic verified flag or promotes a claim.

**Checked by:** planned [APT-TEST-C13](../TEST-SPEC.md#reference-check-typing).

<a id="formalization-locality"></a>

## APT-C14 — Formalization Locality

A `FormalizationCandidate` targets exactly one same-capture `ResearchClaimExtraction` and carries
the exact fields declared by [domain.md](domain.md#formalizationcandidate).

```text
|research_claim_id|=1
∧ same_capture(candidate,claim)
∧ nonempty(notation,legend,reading,logic_family,scope)
∧ assumptions is present-list
∧ valid_extraction(extraction)
```

`proof_check_ref` and `governance_ref` remain optional external evidence. Their presence does not
promote the candidate, claim ontology acceptance or transfer governance authority to APT.

**Checked by:** planned [APT-TEST-C14](../TEST-SPEC.md#formalization-locality).

<a id="fact-append-identity"></a>

## APT-C15 — Fact Append Identity

Entity fact identity is globally unique by `fact_id` across direct fact append and probe-lineage
append. `subject_id` is comparison evidence, not part of the unique key.

```text
unique_key = fact_id

collision(fact_id) ⇒ transactional_reread
existing_exact ⇔ same(canonical_payload_digest,subject_id,supersedes_fact_id)
¬existing_exact ⇒ FACT_IDENTITY_CONFLICT ∧ Δjournal=0
```

A revision uses a new fact/operation identity and names the current same-subject predecessor.
Semantic uniqueness, fact-head CAS, event append and receipt commit share the required ACI journal
transaction.

**Checked by:** planned [APT-TEST-C15](../TEST-SPEC.md#fact-append-identity).

<a id="disposition-and-assessment-chains"></a>

## APT-C16 — Disposition and Assessment Chains

Disposition and assessment are closed event payloads, not mutable Entity fields.

```text
disposition.aggregate_id =
  H_ACI({TargetRef,policy_ref})

assessment.aggregate_id =
  H_ACI({TargetRef,actor_ref,method_ref,policy_ref})

append ⇒
  expected_head=current_head
  ∧ expected_version=current_version
  ∧ new_version=current_version+1
```

Different policy/assessor chains coexist. Append order cannot erase disagreement or synthesize a
singular current value without a separately registered authority policy.

**Checked by:** planned [APT-TEST-C16](../TEST-SPEC.md#disposition-and-assessment-chains).

<a id="probe-lineage-append"></a>

## APT-C17 — Probe Lineage Append

The application canonically sorts unique request items, validates delivery-before-use dependencies,
and transactionally partitions them into `existing_exact`, `submitted_new` and `conflict`.

```text
conflict ⇒ reject ∧ Δjournal=0

operation_result = existing_exact ∪ accepted(submitted_new)
receipt.members = accepted(submitted_new)
existing_exact ∩ receipt.members = ∅

|submitted_new|=0 ⇒ no_command ∧ no_receipt
|submitted_new|>0 ⇒ atomic_append(sort(submitted_new))
```

Only `submitted_new` participates in new-event atomicity, head changes, offsets, grouping digest
and receipt. The total request-key mapping preserves preexisting refs as `existing_exact` without
reacceptance. In a failed mixed request, existing facts remain visible through their original
acceptance while no new member/result mapping/receipt commits.

Every use item names a preexisting delivery head or a delivery item preceding it in the submitted
canonical group. Same-key virtual sequencing and staged revisions inside one command are forbidden.

**Checked by:** planned [APT-TEST-C17](../TEST-SPEC.md#probe-lineage-append).

<a id="relational-collection-canonicalization"></a>

## APT-C18 — Relational Collection Canonicalization

Every relational ID/reference list is a duplicate-rejecting ACI-canonically sorted set, except
`synthesizes`, which is a unique semantic ordered list. Caller order is non-semantic for sets.

```text
set_field ⇒ encoded=sort_ACI(unique(input)) ∧ duplicates(input)⇒reject
synthesizes ⇒ unique(input) ∧ preserve_order(input)
```

**Checked by:** planned [APT-TEST-C18](../TEST-SPEC.md#relational-collection-canonicalization).

## Test Derivation and Traceability

| Rule/anchor | Primary approved source | Minimum planned derivation |
|---|---|---|
| APT-R1 | `domain.md` APT-DOM-1; operations link/capture | Exact/no-op and contradictory-edge tests |
| APT-R2 | operations common boundary; states atomic grouping | retry, changed digest, pre/post-commit crash, atomic rollback |
| APT-R3 | ResearchCapture status matrix | full positive/negative status-cardinality cross-product |
| APT-R4 | ExtractionProvenance/RawSelector | actor/method/capture/digest/bounds/UTF-8 properties |
| APT-R5 | capture currentness | initial, successor, stale/fork/cycle and replay parity |
| APT-R6 | states APT-GROUP-I1..I6 | genesis, between-group, mid-group and checkpoint parity |
| APT-R7 | profile and probe contracts | absent/mismatched/valid profile ID-version-digest receipts |
| APT-R8 | architecture boundary | zero-authority signals and no-raw-body assertions |
| APT-C01..APT-C05 | session/authorization/snapshot/capture contracts | binding, authorization, union/hash and closed digest fixtures |
| APT-C06..APT-C09 | synthesis/selector/evidence/derivation contracts | one positive plus every stated evidence/selection rejection |
| APT-C10..APT-C14 | fact union/locality/typing/check/formalization contracts | exact variants, local edges, cardinalities and real-field presence |
| APT-C15 | operations APT-OP-FACT-11/APT-OP-PROBE-13 | global same-ID exact, cross-subject, payload/predecessor mismatch and race |
| APT-C16 | domain payload variants; states projections | initial/successor CAS, fork/gap, independent heads and disagreement |
| APT-C17 | operations APT-OP-PROBE-1..17 | mixed/zero-new, receipt membership, delivery dependency, crash/race |
| APT-C18 | domain relational collections | duplicate rejection, canonical set order and semantic synthesis order |

Every formal implication yields a positive witness and a falsifying negative fixture. Every
immutability/currentness invariant yields a property test over accepted prefixes. Every atomic
contract yields pre-commit, member, commit, post-commit-response and concurrent-race fixtures.
Tests remain planned. The [TEST-SPEC skeleton](../TEST-SPEC.md) reserves coverage IDs/anchors only;
fixtures, executable cases and evidence remain pending its dedicated review gate.

## Connections

| Document | Type | Description |
|---|---|---|
| [SPEC.md](SPEC.md) | `derives-from` | Registers APT-R1 through APT-R8 as DomainSpec Rule concepts. |
| [architecture.md](architecture.md) | `constrains` | Supplies authority, dependency and ACI profile boundaries. |
| [domain.md](domain.md) | `constrains` | Supplies closed shapes, identities and cross-entity invariants. |
| [states.md](states.md) | `constrains` | Supplies atomic grouping and deterministic reducer invariants. |
| [operations.md](operations.md) | `enforces` | Operations enforce these rules before ACI acceptance. |
| [Focused discovery](../discovery/session-dispatch-research-records.md) | `derives-from` | Supplies APT-D1 through APT-D15 and the three-level provenance boundary. |
