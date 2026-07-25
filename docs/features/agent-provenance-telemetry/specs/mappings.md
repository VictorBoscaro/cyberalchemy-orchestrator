---
tags: [agent-provenance-telemetry, spec, mappings]
node_type: spec
is_session: false
layer: application
nature: technical, reference
status: draft
version: 0.2.0
last_updated: 2026-07-25
feature: agent-provenance-telemetry
specAuthoringGate: in-review
runtimeGate: block
derivedFrom: SPEC.md@0.2.0
---

# Mappings: Agent Provenance Telemetry

This aspect defines only connective transformations among the registered APT contracts. It creates
no Entity, Event, Operation, Query, Interface, authority store or alternate schema. Source and
target shapes remain owned by [interfaces.md](interfaces.md), [operations.md](operations.md),
[events.md](events.md), [queries.md](queries.md) and ACI.

## Mapping Principles

- Caller values express intent; host/application/ACI-owned identity, evidence, time, heads,
  canonicalization and receipts are resolved and verified before domain validation.
- Every mapping is closed. Unknown source fields, missing required slots and caller-authored owner
  fields fail; they are never ignored, copied to an extension bag or logged.
- `direct` means byte/semantic equality after closed-schema decoding. `resolved` means owner lookup
  plus identity/version/digest verification. `derived` means the stated deterministic formula.
- A nonapplicable slot is canonical `null` only when its target schema declares that nullable slot
  present. A `0..1` optional field or a field forbidden by the selected variant is absent; null is
  not an alternative encoding.
- Mapping never copies raw artifact bytes into a domain Entity, event payload, envelope, result,
  projection row, log, trace or metric.
- APT proposes exact payload values. ACI alone canonicalizes accepted bytes, owns the runtime event
  envelope/journal transaction and assigns acceptance metadata.

---

## Caller Intents to Bound Commands

**From:** closed mutation caller intents in
[ProvenanceAppendPort](interfaces.md#provenanceappendport)  
**To:** closed application bound commands in
[operations.md](operations.md#caller-versus-owner-bound-values)  
**Direction:** Inbound

### Session and Dispatch Command Field Mapping

| Source field | Target field | Transform | Ownership / notes |
|---|---|---|---|
| [EnsureSession](operations.md#ensuresession).`operation_id` | [EnsureSession](operations.md#ensuresession).`EnsureSessionBoundCommand.operation_id` | direct | Caller idempotency identity. |
| [EnsureSession](operations.md#ensuresession).`requested_initial_name` | [EnsureSession](operations.md#ensuresession).`EnsureSessionBoundCommand.requested_initial_name` | direct | Used only on new creation; semantic reuse preserves the existing immutable name. |
| [TrustedInvocationContext](interfaces.md#trustedinvocationcontext).actor/authentication evidence | [EnsureSession](operations.md#ensuresession).`owner.actor_ref/actor_authentication_ref/actor_authentication_digest` | resolved | Host-owned authenticated evidence; request-body copies are forbidden. |
| [EnsureSession](operations.md#ensuresession) host context evidence | [EnsureSession](operations.md#ensuresession).`owner.origin_kind/origin_ref/ensure_key` | resolved/derived | Exact tuple; optional materialized context key is canonical digest, while `ensure_key` remains the owner creation-dedupe key. |
| [EnsureSession](operations.md#ensuresession) identity owner | [EnsureSession](operations.md#ensuresession).`owner.session_id/started_at/session_started_event_id` | resolved/minted | Present together only for the new-session branch; absent together on semantic reuse. |
| [StartNewSession](operations.md#startnewsession).`operation_id` | [StartNewSession](operations.md#startnewsession).`StartNewSessionBoundCommand.operation_id` | direct | Atomic two-event command identity. |
| [StartNewSession caller intent](interfaces.md#caller-intent-shapes).`requested_initial_name` | [StartNewSession](operations.md#startnewsession).`requested_initial_name` | direct | Immutable successor name. |
| [StartNewSession caller intent](interfaces.md#caller-intent-shapes).`expected_current_session_id` | [StartNewSession](operations.md#startnewsession).`expected_current_session_id` | direct then CAS-verified | Must equal the current exact origin-tuple binding. |
| [Session context binding](states.md#session-context-binding) | [StartNewSession](operations.md#startnewsession).`owner.origin_kind/origin_ref/predecessor_session_id` | resolved | `predecessor_session_id=expected_current_session_id`. |
| [StartNewSession](operations.md#startnewsession) owner derivation | [StartNewSession](operations.md#startnewsession).`owner.successor_session_id/successor_ensure_key/started_at/rebound_at` | minted/derived | Successor key follows the operation formula. |
| [StartNewSession](operations.md#startnewsession) event identity owner | [StartNewSession](operations.md#startnewsession).`owner.session_started_event_id/session_context_rebound_event_id` | minted | Distinct IDs, exact ordered group. |
| [HostAuthorizationEvidencePort](interfaces.md#hostauthorizationevidenceport) | [StartNewSession](operations.md#startnewsession).`owner.actor_ref/authorization_policy_ref/authorization_policy_digest/authorization_evidence_ref/authorization_evidence_digest` | resolved | Principal/action/origin/predecessor/nonce/expiry binding must verify. |
| [LinkSessionDispatch](operations.md#linksessiondispatch).`operation_id` | [LinkSessionDispatch](operations.md#linksessiondispatch).`LinkSessionDispatchBoundCommand.operation_id` | direct | Command identity. |
| [LinkSessionDispatch caller intent](interfaces.md#caller-intent-shapes).`requested_dispatch_id` | [LinkSessionDispatch](operations.md#linksessiondispatch).`requested_dispatch_id` | direct | Exact external identity, never locator-derived. |
| [LinkSessionDispatch caller intent](interfaces.md#caller-intent-shapes).`requested_dispatch_id` | [DispatchSnapshotReader](interfaces.md#dispatchsnapshotreader).`resolve_for_link(requested_dispatch_id)` → [LinkSessionDispatch](operations.md#linksessiondispatch).`owner.dispatch_snapshot_ref` | owner resolve/verify | Caller supplies only the Dispatch ID; the owner chooses `aci_managed` or `legacy_ledger` and returns the complete verified variant whose embedded Dispatch identity matches it. |
| [Session context binding](states.md#session-context-binding) | [LinkSessionDispatch](operations.md#linksessiondispatch).`owner.origin_kind/origin_ref/session_id` | resolved | Must be the current Session for the tuple. |
| [LinkSessionDispatch](operations.md#linksessiondispatch) identity/time owner | [LinkSessionDispatch](operations.md#linksessiondispatch).`owner.session_dispatch_link_id/linked_at/session_dispatch_linked_event_id` | minted | Owner-bound. |
| [HostAuthorizationEvidencePort](interfaces.md#hostauthorizationevidenceport) | [LinkSessionDispatch](operations.md#linksessiondispatch).`owner.actor_ref/authorization_policy_ref/authorization_policy_digest/authorization_evidence_ref/authorization_evidence_digest` | resolved | Exact action evidence, never caller authority. |
| [ACIProtocolProfileBinding](domain.md#aciprotocolprofilebinding) | each linked [Operation](SPEC.md#concept-registry).`owner.canonicalizer_profile_id/version/digest` | resolved | Exact ACI registration ID/version/digest; missing/mismatch blocks mapping. |

### Research Capture Command Field Mapping

| Source field | Target field | Transform | Ownership / notes |
|---|---|---|---|
| [Capture caller intent](interfaces.md#caller-intent-shapes).`capture_operation_id` | [AppendResearchCapture](operations.md#appendresearchcapture).`capture_operation_id` | direct | Sole capture command identity; no additional `operation_id`. |
| [Capture caller intent](interfaces.md#caller-intent-shapes).`expected_contribution_id` | [ResearchCapture](domain.md#researchcapture).`expected_contribution_id` | direct | Stable capture-chain component. |
| [Capture caller intent](interfaces.md#caller-intent-shapes).`capture_status` | [ResearchCapture](domain.md#researchcapture).`capture_status` | direct/closed enum | Exactly `captured | partial | missing`. |
| [Capture caller intent](interfaces.md#caller-intent-shapes).`raw_return_intent.artifact_id` | [ResearchCapture](domain.md#researchcapture).`raw_return` | resolved | ACI artifact boundary returns the complete finalized [ArtifactReference](domain.md#artifactreference); raw bytes are verifier-only transient input. |
| canonical-null [Capture caller intent](interfaces.md#caller-intent-shapes).`raw_return_intent` | [ResearchCapture](domain.md#researchcapture).`raw_return` | canonical null | Allowed only for `missing`. |
| [Capture caller intent](interfaces.md#caller-intent-shapes).`partial_reason/failure_reason` | [ResearchCapture](domain.md#researchcapture).`partial_reason/failure_reason` | direct or canonical null | All slots remain present and obey the status matrix. |
| [Capture caller intent](interfaces.md#caller-intent-shapes).`failure_evidence_ref_intent.aci_event` | [ACIProfileReceiptVerifier](interfaces.md#aciprofilereceiptverifier).`verify_acceptance({kind="aci_event",accepted_event_id}, expected_contract_version, expected_evidence_digest)` → [FailureEvidenceRef](domain.md#failureevidenceref-embedded-union).`aci_event` | Verify committed event, then inject owner namespace and verified version/digest. | No receipt/artifact/host fields permitted. |
| [Capture caller intent](interfaces.md#caller-intent-shapes).`failure_evidence_ref_intent.aci_receipt` | [ACIProfileReceiptVerifier](interfaces.md#aciprofilereceiptverifier).`verify_acceptance({kind="aci_receipt",receipt_id}, expected_contract_version, expected_evidence_digest)` → [FailureEvidenceRef](domain.md#failureevidenceref-embedded-union).`aci_receipt` | Verify committed receipt, then inject owner namespace and verified version/digest. | No event/artifact/host fields permitted. |
| [Capture caller intent](interfaces.md#caller-intent-shapes).`failure_evidence_ref_intent.artifact` | [ArtifactFinalizationVerifier](interfaces.md#artifactfinalizationverifier).`verify_finalized(artifact_id)` → [FailureEvidenceRef](domain.md#failureevidenceref-embedded-union).`artifact` | Verify finalization, compare returned contract version/evidence digest to both expected fields, then inject owner namespace. | No event/receipt/host fields permitted. |
| [Capture caller intent](interfaces.md#caller-intent-shapes).`failure_evidence_ref_intent.host_observation` | [HostSourceObservationEvidencePort](interfaces.md#hostsourceobservationevidenceport).`resolve(source_observation_id)` → [FailureEvidenceRef](domain.md#failureevidenceref-embedded-union).`host_observation` | Resolve committed host observation, compare returned contract version/evidence digest to both expected fields, then inject host namespace. | No ACI event/receipt/artifact fields permitted. |
| canonical-null [Capture caller intent](interfaces.md#caller-intent-shapes).`failure_evidence_ref_intent` | [ResearchCapture](domain.md#researchcapture).`failure_evidence_ref` | canonical null | Allowed for `captured` and `partial`; forbidden for `missing`. |
| [Capture caller intent](interfaces.md#caller-intent-shapes).`supersedes_capture_id` | [ResearchCapture](domain.md#researchcapture).`supersedes_capture_id` plus [AppendResearchCapture](operations.md#appendresearchcapture).`owner.current_capture_head` | direct then resolved/CAS-verified | Null for initial; otherwise must equal current `(dispatch_id,expected_contribution_id)` head. |
| [Capture caller intent](interfaces.md#caller-intent-shapes).`synthesis_pin_intent[].research_capture_id` | [ResearchCapture](domain.md#researchcapture).`synthesizes[]` | resolved | Each becomes exact `{research_capture_id,capture_digest}`; order is semantic and preserved. |
| host/current [SessionDispatchLink](domain.md#sessiondispatchlink) | [AppendResearchCapture](operations.md#appendresearchcapture).`owner.origin_kind/origin_ref/session_id/session_dispatch_link_id/dispatch_id` | resolved | Exact current context and sole authoritative link. |
| accepted [SessionDispatchLink](domain.md#sessiondispatchlink).`dispatch_snapshot_ref` | [DispatchSnapshotReader](interfaces.md#dispatchsnapshotreader).`verify_pinned(existing_owner_bound_ref, accepted_prefix_boundary)` → [ResearchCapture](domain.md#researchcapture).`dispatch_snapshot_ref` | owner re-verification | Reuses the exact accepted owner-bound pin; caller cannot inject or reselect a variant, and current mutable Dispatch state is not read. |
| [AppendResearchCapture](operations.md#appendresearchcapture) producer/evidence owners | [ResearchCapture](domain.md#researchcapture).`origin_refs/producer_ref` | resolved | Closed refs with verified evidence digests. |
| [AppendResearchCapture](operations.md#appendresearchcapture) identity/time owner | [AppendResearchCapture](operations.md#appendresearchcapture).`owner.schema_ref/research_capture_id/research_capture_appended_event_id/captured_at` | constant/minted | `schema_ref=apt.research-capture@1`. |
| complete closed [ResearchCapture](domain.md#researchcapture) preimage | [ResearchCapture](domain.md#researchcapture).`capture_digest` | derived by ACI | Digest excludes only `capture_digest` itself; every other capture slot participates. |

For every non-null route:

```text
ResearchCapture.failure_evidence_ref =
  complete verified FailureEvidenceRef variant

FailureEvidenceRef.contract_version = intent.expected_contract_version
FailureEvidenceRef.evidence_digest = intent.expected_evidence_digest
```

The binder never copies an intent selector as though it were the owner-bound result.

### Defaults

| Target field | Default value | Condition |
|---|---|---|
| [ResearchCapture](domain.md#researchcapture).`raw_return` | canonical null | `capture_status=missing`. |
| [ResearchCapture](domain.md#researchcapture).`partial_reason` | canonical null | `capture_status∈{captured,missing}`. |
| [ResearchCapture](domain.md#researchcapture).`failure_reason` | canonical null | `capture_status∈{captured,partial}`. |
| [ResearchCapture](domain.md#researchcapture).`failure_evidence_ref` | canonical null | `captured`, or `partial` with canonical-null `failure_evidence_ref_intent`; `missing` never defaults. |
| [ResearchCapture](domain.md#researchcapture).`supersedes_capture_id` | canonical null | Initial chain append. |
| [ResearchCapture](domain.md#researchcapture).`synthesizes` | present empty list | No synthesis inputs; omission is invalid. |
| [ResearchCapture](domain.md#researchcapture).`origin_refs` | present empty canonical set | No causal origin refs. |

### Validation

| Field/surface | Validation | On failure |
|---|---|---|
| caller shape | Exact allowlist from [Caller Intent Shapes](interfaces.md#caller-intent-shapes). | Typed schema/owner-injection error; no bound command. |
| capture status slots | Exact matrix in [ResearchCapture](domain.md#researchcapture). | `CAPTURE_SCHEMA_INVALID` or evidence error; append nothing. |
| failure evidence selector | Exact intent matrix plus the discriminator-specific [owner verification route](interfaces.md#caller-intent-shapes); verified ID/version/digest must equal the selector and opposite fields are forbidden. | `EVIDENCE_INVALID`; no bound command/event. |
| artifact | Finalized, textual, UTF-8, exact digest/media/charset. | `RAW_ARTIFACT_INVALID`; raw bytes never propagate. |
| predecessor | Same chain, current, non-self, acyclic. | `CAPTURE_CAS_CONFLICT`. |
| synthesis | Existing, current-at-append, same Dispatch, non-self, unique IDs, exact digest. | `SYNTHESIS_INVALID`. |

---

## Fact Intent to Exact Payload and FactEnvelope

**From:** `apt.append-research-fact-intent@1` closed union in
[interfaces.md](interfaces.md#caller-intent-shapes)  
**To:** [AppendResearchFact](operations.md#appendresearchfact) bound command and exact
[ResearchFactAppended](events.md#researchfactappended) payload variant  
**Direction:** Inbound

### Common Entity Fact Mapping

| Source field | Target field | Transform | Ownership / notes |
|---|---|---|---|
| [Fact caller intent](interfaces.md#caller-intent-shapes).`operation_id` | [AppendResearchFact](operations.md#appendresearchfact).`operation_id` / ACI command identity | direct | Command/receipt identity; distinct from member fact operation identity. |
| [Fact caller intent](interfaces.md#caller-intent-shapes).`payload_intent_variant.variant` | [ResearchFactAppended](events.md#researchfactappended).`payload_variant` discriminator | exact rename | One of the eight Entity variants only in this branch. |
| stable Entity ID from selected [Entity](SPEC.md#concept-registry) intent | Entity stable ID and [FactEnvelope](domain.md#factenvelope).`subject_id` | direct + derived equality | Question/answer/use/relation/check/problem/claim/formalization ID is the stable subject. |
| [AppendResearchFact](operations.md#appendresearchfact).`expected_subject_head_fact_id` | [FactEnvelope](domain.md#factenvelope).`supersedes_fact_id` and fact CAS guard | direct | Canonical null for initial; otherwise exact current same-subject head. |
| [AppendResearchFact](operations.md#appendresearchfact) fact identity owner | [FactEnvelope](domain.md#factenvelope).`fact_id` | minted | Globally unique semantic fact ID. |
| [AppendResearchFact](operations.md#appendresearchfact) member identity owner | [FactEnvelope](domain.md#factenvelope).`operation_id` | minted/derived | Member identity, not command identity. |
| [AppendResearchFact](operations.md#appendresearchfact) semantic time owner | [FactEnvelope](domain.md#factenvelope).`occurred_at` | stamped | Equals top-level event `event_occurred_at` for Entity variants. |
| current [ResearchCapture](domain.md#researchcapture) | selected [Entity fact payload](events.md#researchfactappended).`research_capture_id` | resolved/injected | Exact non-missing current capture and digest. |
| [Caller fact intent](interfaces.md#caller-intent-shapes).`extraction_intent.mode/actor_ref/method_ref` | [ExtractionProvenance](domain.md#extractionprovenance).`mode/actor_ref/method_ref` | direct then evidence-validated | Attributed extractor; never overwritten with ingestion actor. |
| [Caller fact intent](interfaces.md#caller-intent-shapes).`selector_intent.start_inclusive/end_exclusive` | [RawSelector](domain.md#rawselector).`start_inclusive/end_exclusive` | direct | Half-open UTF-8 byte offsets. |
| [ArtifactEvidenceReader](interfaces.md#artifactevidencereader) verification | [ExtractionProvenance](domain.md#extractionprovenance).`extracted_at/source_capture_id/source_capture_digest/selector` | owner-stamped/derived | Selector `schema_ref=apt.raw-selector@1`, `unit=utf8-byte`; selected digest comes from exact bytes. |
| [TrustedInvocationContext](interfaces.md#trustedinvocationcontext) | [ResearchFactAppended](events.md#researchfactappended).`actor_ref` | resolved | Authenticated ingestion principal. |
| [AppendResearchFact](operations.md#appendresearchfact) event identity/time owner | [ResearchFactAppended](events.md#researchfactappended).`event_id/event_occurred_at` | minted/stamped | ACI envelope event ID proposal plus semantic payload time. |

### Variant Field Mapping

Every listed semantic field maps directly and losslessly; fields not listed for the selected variant
are forbidden.

| Intent variant | Direct semantic fields in exact Entity payload | Additional resolved/derived fields |
|---|---|---|
| [ResearchQuestion](domain.md#researchquestion) intent | [ResearchQuestion](domain.md#researchquestion).`research_question_id/question_text/derives_from` | capture, [FactEnvelope](domain.md#factenvelope), complete extraction |
| [ResearchAnswer](domain.md#researchanswer) intent | [ResearchAnswer](domain.md#researchanswer).`research_answer_id/question_ids` | each question same capture; [FactEnvelope](domain.md#factenvelope)/extraction |
| [ResearchReferenceUse](domain.md#researchreferenceuse) intent | [ResearchReferenceUse](domain.md#researchreferenceuse).`reference_use_id/reference_id/reference_kind/locator_observed/source_observation_id/probe_recommendation_ref/use_kind/anchor_quality` | verified optional refs are absent when not supplied; [FactEnvelope](domain.md#factenvelope)/extraction |
| [ResearchReferenceClaimRelation](domain.md#researchreferenceclaimrelation) intent | [ResearchReferenceClaimRelation](domain.md#researchreferenceclaimrelation).`relation_id/reference_use_id/research_claim_id/relation` | same-capture endpoints, [FactEnvelope](domain.md#factenvelope)/extraction |
| [ReferenceCheck](domain.md#referencecheck) intent | [ReferenceCheck](domain.md#referencecheck).`reference_check_id/check_kind/reference_use_id/relation_id/checked_by/method_ref/result/evidence_ref` | `relation_id` is present only for `claim_support`; optional evidence is absent when not supplied; [FactEnvelope](domain.md#factenvelope); no extraction field |
| [ResearchProblem](domain.md#researchproblem) intent | [ResearchProblem](domain.md#researchproblem).`problem_id/kind/statement/blocks/evidence_refs` | verified evidence refs, [FactEnvelope](domain.md#factenvelope)/extraction |
| [ResearchClaimExtraction](domain.md#researchclaimextraction) intent | [ResearchClaimExtraction](domain.md#researchclaimextraction).`research_claim_id/statement/answer_ids` | same-capture answers, [FactEnvelope](domain.md#factenvelope)/extraction |
| [FormalizationCandidate](domain.md#formalizationcandidate) intent | [FormalizationCandidate](domain.md#formalizationcandidate).`formalization_id/research_claim_id/notation/latex/legend/reading/logic_family/assumptions/scope/syntax_checker_ref/proof_check_ref/governance_ref` | every unsupplied `0..1` field is absent; same-capture claim, [FactEnvelope](domain.md#factenvelope)/extraction |

### Disposition and Assessment Mapping

| Source field | Target field | Transform | Ownership / notes |
|---|---|---|---|
| aggregate [Fact caller intent](interfaces.md#caller-intent-shapes).`target_kind/target_id` | exact [TargetRef](domain.md#disposition-and-assessment-payload-variants) | direct plus inject `research_capture_id` | Target must exist in current named capture. |
| disposition [Fact caller intent](interfaces.md#caller-intent-shapes).`disposition/policy_ref` | [ResearchFactAppended](events.md#researchfactappended).`disposition_recorded` payload values | direct | Value must match target kind. |
| assessment [Fact caller intent](interfaces.md#caller-intent-shapes).`assessment/method_ref/policy_ref` | [ResearchFactAppended](events.md#researchfactappended).`assessment_recorded` payload values | direct | Independent assessor/method/policy chain. |
| [TrustedInvocationContext](interfaces.md#trustedinvocationcontext) principal | aggregate payload and [ResearchFactAppended](events.md#researchfactappended).`actor_ref` | resolved/injected | Exact equality required. |
| aggregate [Fact caller intent](interfaces.md#caller-intent-shapes).`expected_head_accepted_event_id/expected_aggregate_version` | [ResearchFactAppended](events.md#researchfactappended) aggregate CAS fields | direct then CAS-verified | Null/0 initial or exact current head/version. |
| [TargetRef](domain.md#disposition-and-assessment-payload-variants) + `policy_ref` | [ResearchFactAppended](events.md#researchfactappended).`aggregate_type/aggregate_id` | constant/derived | `apt.disposition-chain`; `aggregate_id=H_ACI` over TargetRef plus `policy_ref`. |
| [TargetRef](domain.md#disposition-and-assessment-payload-variants) + actor/method/policy | [ResearchFactAppended](events.md#researchfactappended).`aggregate_type/aggregate_id` | constant/derived | `apt.assessment-chain`; `aggregate_id=H_ACI` over TargetRef plus actor/method/policy. |

Disposition/assessment never receive a [FactEnvelope](domain.md#factenvelope) or fact-head guard. Entity variants never
receive aggregate fields.

### Defaults

| Target field | Default value | Condition |
|---|---|---|
| [FactEnvelope](domain.md#factenvelope).`supersedes_fact_id` | canonical null | Initial Entity fact subject. |
| [ResearchReferenceUse](domain.md#researchreferenceuse).`source_observation_id/probe_recommendation_ref`; [ReferenceCheck](domain.md#referencecheck).`relation_id/evidence_ref`; [FormalizationCandidate](domain.md#formalizationcandidate).`latex/syntax_checker_ref/proof_check_ref/governance_ref` | absent | Corresponding `0..1` value is not supplied or, for check `relation_id`, `check_kind≠claim_support`. Null is invalid. |
| [ResearchFactAppended](events.md#researchfactappended).`expected_head_accepted_event_id` | canonical null | Initial aggregate version `0`. |

### Validation

| Field/surface | Validation | On failure |
|---|---|---|
| variant union | Exactly one of eight Entity, disposition or assessment; no cross-family slots. | `FACT_SCHEMA_INVALID` / `FACT_VARIANT_BINDING_INVALID`. |
| [FactEnvelope](domain.md#factenvelope) | All five fields; subject binding; current predecessor; time equality. | Fact locality/CAS/identity error. |
| extraction | Exact capture/artifact bytes, UTF-8 boundaries and selected digest. | `SELECTOR_INVALID`; bytes are discarded after validation. |
| relational sets | Duplicate-rejecting canonical sorted sets; `synthesizes` exception does not apply here. | `FACT_TYPE_INVALID`. |
| global fact collision | Same fact semantic digest, subject ID and predecessor or conflict. | Existing exact ref or `FACT_IDENTITY_CONFLICT`; never synthesize a new envelope. |

---

## APTFactToACIEvent

**Mapping scope:** validated bound commands to exact APT payloads and ACI runtime envelopes.

**From:** validated bound command/candidate from the six
[Operations](SPEC.md#concept-registry)  
**To:** exact APT event payload plus ACI-owned
[RuntimeEventEnvelope](../../agents-communication-infra/specs/domain.md#runtimeeventenvelope)  
**Direction:** Outbound to ACI command boundary

### Event Payload Mapping

| Bound command | Event payload(s) | Field mapping |
|---|---|---|
| [EnsureSession](operations.md#ensuresession) bound command, new branch | [SessionStarted](events.md#sessionstarted) | Closed [Session](domain.md#session) from owner IDs/origin/key/operation/time/name; actor and authentication ref/digest; rollover authorization canonical null. |
| [StartNewSession](operations.md#startnewsession) bound command | ordered [SessionStarted](events.md#sessionstarted), [SessionContextRebound](events.md#sessioncontextrebound) | Successor [Session](domain.md#session) first; authentication pair canonical null; identical rollover authorization/origin/actor in both; predecessor/successor and rebound time in second. |
| [LinkSessionDispatch](operations.md#linksessiondispatch) bound command | [SessionDispatchLinked](events.md#sessiondispatchlinked) | Closed [SessionDispatchLink](domain.md#sessiondispatchlink), origin tuple, snapshot, actor and exact authorization fields. |
| [AppendResearchCapture](operations.md#appendresearchcapture) bound command | [ResearchCaptureAppended](events.md#researchcaptureappended) | Complete [ResearchCapture](domain.md#researchcapture) including digest, current link ID and ingestion actor; raw bytes omitted. |
| [AppendResearchFact](operations.md#appendresearchfact) bound command | [ResearchFactAppended](events.md#researchfactappended) | Exact exclusive payload variant, ingestion actor and event semantic time. |
| [AppendReferenceProbeLineage](operations.md#appendreferenceprobelineage) delivery bound item | [ReferenceProbeLineageAppended](events.md#referenceprobelineageappended) | Derived delivery key, complete committed recommendation ref, expected head, actor/time. |
| [AppendReferenceProbeLineage](operations.md#appendreferenceprobelineage) use bound item | [ResearchFactAppended](events.md#researchfactappended) `reference_use` | Complete [ResearchReferenceUse](domain.md#researchreferenceuse) including [FactEnvelope](domain.md#factenvelope)/extraction/probe ref, ingestion actor/time. |

### ACI Envelope Field Mapping

| Source | [RuntimeEventEnvelope](../../agents-communication-infra/specs/domain.md#runtimeeventenvelope) field | Transform / authority |
|---|---|---|
| owner-bound [APT Event](events.md) candidate | [RuntimeEventEnvelope](../../agents-communication-infra/specs/domain.md#runtimeeventenvelope).`event_id/event_type` | Exact proposed ID and registered past-tense ACI event type; ACI validates uniqueness. |
| registered [APT Event](events.md) payload contract | [RuntimeEventEnvelope](../../agents-communication-infra/specs/domain.md#runtimeeventenvelope).`schema_ref/schema_digest` | ACI registry-resolved exact version/digest. |
| [SessionStarted](events.md#sessionstarted) | [RuntimeEventEnvelope](../../agents-communication-infra/specs/domain.md#runtimeeventenvelope).`aggregate_id/aggregate_version` | Session stream selected by `session_id`; ACI compares the current stream version and assigns the next contiguous version. |
| [SessionContextRebound](events.md#sessioncontextrebound) | [RuntimeEventEnvelope](../../agents-communication-infra/specs/domain.md#runtimeeventenvelope).`aggregate_id/aggregate_version` | Binding stream selected by exact `(origin_kind,origin_ref)`; predecessor binding guard must pass before ACI assigns the next contiguous version. |
| [SessionDispatchLinked](events.md#sessiondispatchlinked) | [RuntimeEventEnvelope](../../agents-communication-infra/specs/domain.md#runtimeeventenvelope).`aggregate_id/aggregate_version` | Link stream selected by `session_dispatch_link_id`; contradictory Dispatch link is rejected before next version. |
| [ResearchCaptureAppended](events.md#researchcaptureappended) | [RuntimeEventEnvelope](../../agents-communication-infra/specs/domain.md#runtimeeventenvelope).`aggregate_id/aggregate_version` | Capture-head stream selected by `(dispatch_id,expected_contribution_id)`; predecessor CAS from [states.md](states.md#research-capture-currentness) precedes next version. |
| Entity [ResearchFactAppended](events.md#researchfactappended) | [RuntimeEventEnvelope](../../agents-communication-infra/specs/domain.md#runtimeeventenvelope).`aggregate_id/aggregate_version` | Fact-head stream selected by [FactEnvelope](domain.md#factenvelope).`subject_id`; predecessor and global fact-ID guards precede next version. |
| [ReferenceProbeLineageAppended](events.md#referenceprobelineageappended) | [RuntimeEventEnvelope](../../agents-communication-infra/specs/domain.md#runtimeeventenvelope).`aggregate_id/aggregate_version` | Delivery stream selected by owner-derived `delivery_subject_key`; expected head guard precedes next version. |
| disposition [ResearchFactAppended](events.md#researchfactappended) | [RuntimeEventEnvelope](../../agents-communication-infra/specs/domain.md#runtimeeventenvelope).`aggregate_id/aggregate_version` | `aggregate_type=apt.disposition-chain`; `aggregate_id=H_ACI` over [TargetRef](domain.md#disposition-and-assessment-payload-variants) plus `policy_ref`; ACI requires expected head/current version and assigns `aggregate_version=expected_aggregate_version+1`. |
| assessment [ResearchFactAppended](events.md#researchfactappended) | [RuntimeEventEnvelope](../../agents-communication-infra/specs/domain.md#runtimeeventenvelope).`aggregate_id/aggregate_version` | `aggregate_type=apt.assessment-chain`; `aggregate_id=H_ACI` over [TargetRef](domain.md#disposition-and-assessment-payload-variants) plus actor/method/policy; ACI requires expected head/current version and assigns `aggregate_version=expected_aggregate_version+1`. |
| [RuntimeEventEnvelope](../../agents-communication-infra/specs/domain.md#runtimeeventenvelope) ACI journal commit | [RuntimeEventEnvelope](../../agents-communication-infra/specs/domain.md#runtimeeventenvelope).`journal_offset/recorded_at` | Assigned only by ACI on durable commit; absent from APT payload preimage. |
| APT L0 [envelope mapping rule](events.md#aci-envelope-versus-apt-domain-payload) | [RuntimeEventEnvelope](../../agents-communication-infra/specs/domain.md#runtimeeventenvelope).`observed_at` | canonical null; APT L0 has no contracted owner observation timestamp and never derives one from invocation context. |
| [TrustedInvocationContext](interfaces.md#trustedinvocationcontext).`correlation_ref` | [RuntimeEventEnvelope](../../agents-communication-infra/specs/domain.md#runtimeeventenvelope).`correlation_id` | Direct preservation: `correlation_id=correlation_ref`. |
| accepted bound [Operation command identity](operations.md#common-execution-boundary), formed from `operation_id` or capture `capture_operation_id` | [RuntimeEventEnvelope](../../agents-communication-infra/specs/domain.md#runtimeeventenvelope).`causation_id` | ACI's exact encoding/reference of `command_identity(op)`; no separate caller `causation_id` field exists. |
| exact [APT Event](events.md) payload bytes | [RuntimeEventEnvelope](../../agents-communication-infra/specs/domain.md#runtimeeventenvelope).`payload_ref` | ACI-owned immutable payload storage reference; not an APT artifact/raw-return copy. |
| exact [APT Event](events.md) payload canonical preimage | [RuntimeEventEnvelope](../../agents-communication-infra/specs/domain.md#runtimeeventenvelope).`payload_hash` | `H_ACI(canonical(exact APT payload))`. |

ACI envelope fields, command receipt, grouping fields, offsets and recorded time are excluded from
the APT payload canonical preimage. The APT payload is not reconstructed from an envelope, log row
or projection.

### Defaults

| Target field | Default value | Condition |
|---|---|---|
| SessionStarted authentication pair | canonical null pair | Rollover branch only. |
| SessionStarted `rollover_authorization` | canonical null | Ensure branch only. |
| [RuntimeEventEnvelope](../../agents-communication-infra/specs/domain.md#runtimeeventenvelope).`observed_at` | canonical null | APT L0 has no contracted owner observation timestamp. |

### Validation

| Field/surface | Validation | On failure |
|---|---|---|
| branch null matrix | Authentication pair and rollover authorization are exclusive/exact. | Reject candidate; no event. |
| atomic rollover | Exactly two events in specified order with identical shared evidence. | ACI transaction commits neither. |
| payload schema/digest | Registered exact schema and canonicalizer profile. | Profile/schema error; no append. |
| durable acceptance | Envelope refs/hash, grouping and receipt reconcile exactly. | No success acknowledgement. |

---

## ProbeBundleToReferenceLineage

**Mapping scope:** committed probe recommendation intents through transactional partition and total
APT lineage result.

**From:** closed probe lineage intent and owner-bound items from
[AppendReferenceProbeLineage](operations.md#appendreferenceprobelineage)  
**To:** submitted ACI event group plus [ProbeAppendOutcome](interfaces.md#probeappendoutcome)  
**Direction:** Inbound mapping, transactional submit and result mapping

### Request Item Mapping

| Caller item field | Bound item/event field | Transform |
|---|---|---|
| [Probe caller intent](interfaces.md#caller-intent-shapes).`probe_recommendation_ref_intent` | [ProbeRecommendationRef](domain.md#proberecommendationref) | Resolve committed bundle/recommendation/profile receipts and exact digests. |
| accepted [ProbeRecommendationRef](domain.md#proberecommendationref) composite | [ReferenceProbeLineageAppended](events.md#referenceprobelineageappended).`delivery_subject_key` and dependent use mapping | `H_ACI(canonical({probe_id,bundle_digest,recommendation_id}))`; caller key forbidden. |
| delivery [Probe caller intent](interfaces.md#caller-intent-shapes).`expected_head_event_id` | [ReferenceProbeLineageAppended](events.md#referenceprobelineageappended).`expected_head_event_id` and CAS guard | Direct then compare with current delivery head. |
| use [Probe caller intent](interfaces.md#caller-intent-shapes) semantic fields | full [ResearchReferenceUse](domain.md#researchreferenceuse) payload | Lossless direct mapping plus capture/ref/evidence resolution. |
| use [Probe caller intent](interfaces.md#caller-intent-shapes).`expected_subject_head_fact_id` | [FactEnvelope](domain.md#factenvelope).`supersedes_fact_id` / fact CAS | Direct then compare current fact head. |
| [Probe caller intent](interfaces.md#caller-intent-shapes).`kind` plus owner-resolved stable subject | [ProbeAppendOutcome](interfaces.md#probeappendoutcome).`result_by_request_key` key | Exact tuple `(kind,stable_subject_key)`; retained only in the total result map and never an event authority field. |

For delivery, `stable_subject_key` is the owner-derived delivery key. For use,
`stable_subject_key=reference_use_id`, the stable reference-use subject. Caller-supplied delivery
keys remain forbidden.

After duplicate rejection, bound items form `canonical_request`, ordered exactly by
`(kind_rank,stable_subject_key)`. A use must depend on a preexisting accepted delivery head or a
preceding delivery in that canonical submitted group.

### Transaction Partition and Event Mapping

```text
partition(items) = existing_exact ⊎ submitted_new
conflict ≠ partition member; any conflict rejects the whole new portion

canonical_request =
  sort(unique_bound_items, key=(kind_rank,stable_subject_key))

submitted_items =
  [item for item in canonical_request if partition(item)=submitted_new]

events(submitted_new) =
  [
    ReferenceProbeLineageAppended(item) if item.kind=delivery_origin
    else ResearchFactAppended(reference_use(item))
    for item in submitted_items
  ]

result = existing_exact ∪ accepted(submitted_new)
receipt.members = accepted(submitted_new)
existing_exact ∩ receipt.members = ∅
```

| Partition/result field | Mapping rule |
|---|---|
| `result_by_request_key` | Total canonical map over every original request key to original existing ref or newly accepted ref. |
| `existing_exact` | Canonical set of original accepted refs; no new payload, envelope, offset or receipt membership. |
| `accepted_submitted_new` | Event refs in verified ACI accepted order for only newly submitted members. |
| `receipt` | New or byte-stable prior ACI receipt whose members equal `accepted_submitted_new`; canonical null for zero-new semantic existing. |
| `submission_status=accepted_new` | Nonempty new list and newly durable receipt. |
| `submission_status=submitted_retry` | Same command identity/digest and exact prior total mapping/receipt. |
| `submission_status=semantic_existing` | New list empty, every entry existing, no command, canonical-null receipt. |

No mapping changes `existing_exact` to newly accepted or inserts it into a new atomic group.

### Validation

| Field/surface | Validation | On failure |
|---|---|---|
| request keys/items | Nonempty, unique, closed, order-independent. | Reject before ACI. |
| delivery dependency | Same accepted recommendation composite and valid predecessor direction. | `DELIVERY_ORIGIN_REQUIRED` / lineage error. |
| partition | Total, disjoint and stable on retry. | Reconciliation/integrity error; no acknowledgement. |
| receipt | Exact new-member set, range/order/count/digest. | `ATOMIC_GROUP_INVALID`. |

---

## ProvenanceFactsToReadModels

**Mapping scope:** Query intents, owner manifests and accepted ACI prefix to the four deterministic
APT read models.

**From:** closed Query intents and owner manifests from
[ProvenanceQueryPort](interfaces.md#provenancequeryport), plus accepted ACI prefix  
**To:** the four [deterministic Query results](queries.md)
**Direction:** Read mapping

### Query Intent to Bound Request

| Caller intent field | [BoundQueryRequest](interfaces.md#query-request-and-result) field | Transform / validation |
|---|---|---|
| [QueryIntent](interfaces.md#query-request-and-result).`schema_ref` | [BoundQueryRequest](interfaces.md#query-request-and-result).`schema_ref` | Direct exact constant; unknown schema fails. |
| [QueryIntent](interfaces.md#query-request-and-result).`session_id/dispatch_id/research_capture_id` | [BoundQueryRequest](interfaces.md#query-request-and-result).`identity` | Direct schema-specific identity mapping. |
| [AgentReferenceQueryIntent](interfaces.md#query-request-and-result).`dispatch_id/target` | [BoundQueryRequest](interfaces.md#query-request-and-result).`identity` | Exact `{dispatch_id,target}`; target relationships come only from ACI owner evidence, never locator/display fields. |
| [QueryIntent](interfaces.md#query-request-and-result).`requested_o` | [BoundQueryRequest](interfaces.md#query-request-and-result).`requested_o` | Direct inclusive requested boundary. |
| [SessionPinnedInputManifest](interfaces.md#query-request-and-result) accepted prefix grouping | [BoundQueryRequest](interfaces.md#query-request-and-result).`pinned_input_manifest/pinned_input_digests` | Owner binds requested/effective offsets, exact grouping profile and verified manifest digest. |
| existing accepted owner-bound [DispatchAuthoritySnapshotRef](domain.md#dispatchauthoritysnapshotref) | [DispatchSnapshotReader](interfaces.md#dispatchsnapshotreader).`verify_pinned(existing_owner_bound_ref, accepted_prefix_boundary)` → [DispatchPinnedInputManifest](interfaces.md#query-request-and-result) and digest | Owner re-verifies the stored pin at the complete verified APT boundary, then binds exactly that ref and `H_ACI(canonical(ref))`; no caller snapshot or variant selector. |
| accepted [ResearchCapture](domain.md#researchcapture) + its existing owner-bound snapshot | [DispatchSnapshotReader](interfaces.md#dispatchsnapshotreader).`verify_pinned(existing_owner_bound_ref, accepted_prefix_boundary)` → [ResearchPinnedInputManifest](interfaces.md#query-request-and-result) and two-key digest map | Owner binds capture ID/event/digest and re-verifies its exact stored Dispatch snapshot; no current mutable Dispatch read. |

| Agent-reference owner source | Bound request field | Transform / validation |
|---|---|---|
| [ACIAgentReferenceEvidenceReader](interfaces.md#aciagentreferenceevidencereader), [HostAgentActivationBindingEvidencePort](interfaces.md#hostagentactivationbindingevidenceport), accepted-state probe binding reader and host observation owner | [AgentReferencePinnedInputManifest](interfaces.md#query-request-and-result) plus seven-key digest map | Bind complete query-scoped target/producer/delivery/probe wrappers, derived APT fact heads and closed host `unavailable \| available` manifest; verify every owner, digest, scope and selector-complete producer cardinality before pure reduction. |
| `HostAgentActivationBindingEvidencePort.bind_capture_producers(scope,capture_producer_selector,effective_as_of)` verified result | `AgentReferencePinnedInputManifest.producer_resolution` and `AgentReferencePinnedInputDigests.producer_resolution` | Copy the complete wrapper byte-for-byte and set its digest to `H_ACI(canonical(producer_resolution))`; preserve exact scope `{dispatch_id,target_resolution_digest,aci_delivery_snapshot_digest,probe_scout_bindings_digest,capture_producer_selector_digest}`. Owner resolution occurs only while constructing/verifying the bound manifest. |

Caller-supplied manifests, digests, effective offset, hashes, snapshots or snapshot variant
selectors are rejected. A caller supplies only `requested_dispatch_id` to the link intent or the
identity plus `requested_o` in a closed QueryIntent.

### Accepted Prefix to Output Field Mapping

| Accepted source | [SessionRecord](queries.md#sessionrecord) fields | Transform |
|---|---|---|
| [SessionStarted](events.md#sessionstarted) | [SessionRecord](queries.md#sessionrecord).`session_id/started_at/initial_name/origin_kind/origin_ref` | Direct from immutable [Session](domain.md#session). |
| [Session binding fold](states.md#session-context-binding) | [SessionRecord](queries.md#sessionrecord).`is_current_for_origin` | Compare requested [Session](domain.md#session) with tuple head at `effective_as_of`. |
| [SessionDispatchLinked](events.md#sessiondispatchlinked) | [SessionRecord](queries.md#sessionrecord).`dispatches/dispatch_count` | Authoritative link set, canonical order, distinct Dispatch IDs. |
| [Research capture/fact heads](queries.md#canonical-collections-currentness-and-dedupe) under linked Dispatches | [SessionRecord](queries.md#sessionrecord) research status/answer counts | Count stable current subjects, never event rows. |
| [Disposition heads](states.md#disposition-read-projections) | [SessionRecord](queries.md#sessionrecord) problem/formalization maps | Existing policy keys only, canonical order and exact allowed dispositions. |

| Accepted source | [DispatchScopeProjection](queries.md#dispatchscopeprojection) fields | Transform |
|---|---|---|
| pinned [DispatchAuthoritySnapshotRef](domain.md#dispatchauthoritysnapshotref) canonical projection | [DispatchScopeProjection](queries.md#dispatchscopeprojection).`dispatch_id/dispatch_snapshot_ref/declared_scope` | Exact verified scope subset; omit full prompt/body/current mutable snapshot. |
| accepted [SessionDispatchLink](domain.md#sessiondispatchlink) rows | [DispatchScopeProjection](queries.md#dispatchscopeprojection).`session_links` | Canonical authoritative reverse projection, never persisted as another join. |
| current [ResearchCapture](domain.md#researchcapture) heads | [DispatchScopeProjection](queries.md#dispatchscopeprojection) capture summaries/status counts | One head per contribution chain. |
| current [FactEnvelope](domain.md#factenvelope) heads on those captures | [DispatchScopeProjection](queries.md#dispatchscopeprojection) answer/use/check summaries | Stable-subject dedupe; independent check targets preserve disagreement. |
| current [Disposition heads](states.md#disposition-read-projections) | [DispatchScopeProjection](queries.md#dispatchscopeprojection) problem/formalization maps | Existing policy keys only; no singular adjudication. |

| Accepted source | [ResearchRecord](queries.md#researchrecord) fields | Transform |
|---|---|---|
| exact pinned [ResearchCaptureAppended](events.md#researchcaptureappended) event/digest | [ResearchRecord](queries.md#researchrecord) immutable capture fields/currentness | Direct immutable [ResearchCapture](domain.md#researchcapture) values; compare capture with current chain head. |
| [ResearchCapture](domain.md#researchcapture).`raw_return` | [ResearchRecord](queries.md#researchrecord).`raw_return_ref` | Artifact reference only; raw bytes omitted. |
| [ResearchCapture](domain.md#researchcapture).`synthesizes` pins | [ResearchRecord](queries.md#researchrecord).`synthesis_inputs` | Preserve semantic order/digest pins; resolve each ID/digest and derive later supersession label. |
| current [Entity fact heads](queries.md#canonical-collections-currentness-and-dedupe) local to capture | [ResearchRecord](queries.md#researchrecord) eight canonical Entity collections | Compare fact ID to unique current subject head; exclude prior revisions/cross-capture facts. |
| current [Disposition heads](states.md#disposition-read-projections) | [ResearchRecord](queries.md#researchrecord) problem/claim/formalization maps | Preserve policy/assessor keys and disagreement. |
| current [ReferenceCheck](domain.md#referencecheck) heads | [ResearchRecord](queries.md#researchrecord).`reference_checks/reference_check_summary` | Latest only within exact subject chain; independent checker targets coexist. |
| current [ReferenceProbeLineageAppended](events.md#referenceprobelineageappended) heads referenced by uses | [ResearchRecord](queries.md#researchrecord).`probe_delivery_origins` | Resolve derived recommendation composite key, current lineage head and canonical order. |

| Accepted/bound source | [AgentReferenceLineage](queries.md#agentreferencelineage) field | Transform |
|---|---|---|
| [AgentReferenceQueryIntent](interfaces.md#query-request-and-result).`dispatch_id` | `dispatch_id` | Echo exact bound identity; it selects scope but grants no authority. |
| [AgentReferenceQueryIntent](interfaces.md#query-request-and-result).`target` | `requested_target` | Echo the exact closed selector for transparency; it is non-authoritative and owner-resolved `resolved_targets` remain separate. |
| verified `target_resolution.members.{dispatch_id,group_id,seat_id,attempt_id,agent_instance_id,owner_evidence_digest}` | `resolved_targets[]` same fields | Direct equality; duplicate-reject and canonical-sort complete owner target tuples. |
| ACI [AgentReferenceDelivery](../../agents-communication-infra/specs/domain.md#agentreferencedelivery).`scout_run_id` | `reference_lines[].source.scout_run_id` | Direct after delivery-member verification. |
| verified `probe_scout_bindings.members.probe_id` | optional `reference_lines[].source.probe_id` | Unique exact legacy alias for the same Scout/commit; when no alias exists the optional field is canonically absent, never null or text-derived. |
| ACI [AgentReferenceDelivery](../../agents-communication-infra/specs/domain.md#agentreferencedelivery).`bundle_artifact_id/bundle_digest` | `reference_lines[].source.bundle_artifact_id/bundle_digest` | Direct exact immutable bundle identity/digest. |
| verified committed membership `recommendation_id` | `reference_lines[].source.recommendation_id` and `recommended.recommendation_id` | Expand exactly one row per accepted delivery/recommendation pair. |
| `aci_delivery_snapshot.members.source_bundle_committed_event_ref.{event_id,offset,payload_digest}` | `source.bundle_committed_event_ref` same closed shape | Direct equality; every field required. |
| same commit event ref + `bundle_artifact_id/bundle_digest` | `recommended.committed_membership_evidence_ref.{commit_event_ref,bundle_artifact_id,bundle_digest}` | Nest the same closed event ref without renaming/dropping fields; attach verified artifact/digest. |
| ACI [AgentReferenceDelivery](../../agents-communication-infra/specs/domain.md#agentreferencedelivery).`agent_reference_delivery_id` | `delivered_to_attempt.agent_reference_delivery_id` | Direct stable identity. |
| `aci_delivery_snapshot.members.accepted_delivery_event_ref.{event_id,offset,payload_digest}` | `delivered_to_attempt.target_delivery_event_ref` same closed shape | Direct equality; lifecycle `bundle_delivered@1` cannot substitute. |
| ACI [AgentReferenceDelivery](../../agents-communication-infra/specs/domain.md#agentreferencedelivery).`dispatch_id/target_attempt_id/target_seat_id/target_agent_instance_id` | `delivered_to_attempt` same target fields | Direct owner-derived identities; all must equal the resolved target. |
| ACI delivery `effective_input_artifact_id/effective_input_entry_ordinal/effective_input_manifest_hash` | `in_effective_input.effective_input_artifact_id/entry_ordinal/manifest_hash` | Direct after exact finalized-manifest verification. |
| ACI `EffectiveInputEntry.reference_bundle.artifact_ref/content_hash` | `in_effective_input.artifact_ref/content_hash` | Direct; equal delivery bundle artifact/digest. |
| host `unavailable` variant | every `access_observed` | Canonical empty set; current Stage-G rows cannot be upgraded or locator-joined. |
| host `available.observations.source_observation_id/coverage/tool_name/source_kind/purpose/evidence_digest` | `access_observed[]` same member fields | Direct after query scope, target tuple and delivery/recommendation owner-ref verification; preserve `exact \| metadata_only \| opaque`. |
| host `host_observation_projection.owner_contract_version` | every included `access_observed[].owner_contract_version` | Copy the verified wrapper-level version into each projected observation row; member values cannot override it. |
| current [ResearchReferenceUse](domain.md#researchreferenceuse).`research_capture_id/reference_use_id/use_kind` plus owning [ResearchCapture](domain.md#researchcapture).`producer_ref` and verified `producer_resolution.members` | `declared_used[]` same fields | Direct current-head values only after exact probe/Scout/bundle/recommendation join and one complete owner-resolved producer member matches the stored producer digest, activation and delivery target tuple. |
| current [ResearchReferenceClaimRelation](domain.md#researchreferenceclaimrelation).`relation_id/reference_use_id/research_claim_id/relation` | `claim_relation[]` same fields | Direct only when `reference_use_id` is included in the row. |
| current [ReferenceCheck](domain.md#referencecheck).`reference_check_id/relation_id/checked_by/method_ref/result/evidence_ref` | `claim_support_check[]` same fields | Direct only for `check_kind=claim_support` and an exact included relation; no generic verdict. |

The mapping never emits a combined `used`, `read`, `verified` or `supports_claim` field. Empty and
non-empty axes map independently.

### Defaults

There are no implicit defaults. Optional `source.probe_id` is canonically absent when no exact
verified alias exists. `access_observed=[]` is emitted only from the verified closed host
`unavailable` variant; missing, malformed or unverified host evidence is an integrity error, not a
fallback to empty.

### Validation

- Every intent, bound request, wrapper, member and result must satisfy its exact closed shape.
- The `AgentReferencePinnedInputDigests` map must contain exactly
  `apt_accepted_prefix`, `target_resolution`, `producer_resolution`, `aci_delivery_snapshot`,
  `probe_scout_bindings`, `apt_fact_heads` and `host_observation_projection`; every echoed
  wrapper/value must hash to its corresponding digest.
- Every owner wrapper must be complete for its exact scope, have `accepted_through<=effective_as_of`
  and reject omitted, extra, duplicate, future, cross-scope, wrong-owner/version or
  digest-mismatched members.
- `producer_resolution` must contain exactly one host-owner-resolved member per canonical
  target-and-lineage candidate selector, preserve its stored producer digest and activation, and
  match the accepted complete Attempt/delivery target tuple; missing, extra or ambiguous members
  fail closed before projection.
- Mapping and reduction of `declared_used` consume only that already verified member and perform
  zero lazy or per-use calls to the host owner.
- Target, delivery, effective-input, immutable-bundle and recommendation membership must agree
  exactly; lifecycle delivery cannot substitute for target delivery or recommendation membership.
- An incomplete accepted group, a future fact, a swapped scope/digest or any locator-derived
  identity fails closed before projection.

### Result Wrapper Mapping

| Bound/reduced value | [QueryResult](interfaces.md#query-request-and-result) field | Transform |
|---|---|---|
| [BoundQueryRequest](interfaces.md#query-request-and-result).`schema_ref` | [QueryResult](interfaces.md#query-request-and-result).`schema_ref` | Exact equality. |
| [QueryIntent](interfaces.md#query-request-and-result).`requested_o` | [QueryResult](interfaces.md#query-request-and-result).`requested_o` | Exact equality through binding/result. |
| [Accepted prefix](queries.md#intent-binding-and-replay-boundary) verified grouping boundary | [QueryResult](interfaces.md#query-request-and-result).`effective_as_of` | Greatest verified group `last_offset≤requested_o`, or genesis. |
| [BoundQueryRequest](interfaces.md#query-request-and-result).`pinned_input_manifest/pinned_input_digests` | [QueryResult](interfaces.md#query-request-and-result).`pinned_input_manifest/pinned_input_digests` | Echo exact verified closed values. |
| [BoundQueryRequest](interfaces.md#query-request-and-result) manifest + digests | [QueryResult](interfaces.md#query-request-and-result).`snapshot_digest` | `H_ACI(canonical({pinned_input_manifest,pinned_input_digests}))` using these exact canonical field names. |
| [BoundQueryRequest](interfaces.md#query-request-and-result) plus reduced value | [QueryResult](interfaces.md#query-request-and-result).`projection_hash` | Exact formula in [queries.md](queries.md#external-snapshot-and-hash-rules). |
| pure [Query reducer](queries.md#common-deterministic-query-contract) output | [QueryResult](interfaces.md#query-request-and-result).`value` | Closed Query-specific output, canonical collections. |

No projection result is mapped back into a command, event or authority table.

---

## Accepted ACI Events to Projection Rows

**From:** complete verified accepted ACI command groups carrying the six
[APT Events](SPEC.md#concept-registry)  
**To:** pure reducer state in [states.md](states.md) and the four
[Query rows](queries.md)  
**Direction:** Read projection

| Accepted APT payload | Reducer key/head | Projection effect | Query consumers |
|---|---|---|---|
| [SessionStarted](events.md#sessionstarted) | [Session](domain.md#session).`session_id` and exact origin tuple | Add immutable [Session](domain.md#session); bind tuple only on valid ensure or complete rollover group. | [SessionRecord](queries.md#sessionrecord) |
| [SessionContextRebound](events.md#sessioncontextrebound) | [Session context binding](states.md#session-context-binding) origin tuple | Replace derived tuple head with exact successor after predecessor CAS. | [SessionRecord](queries.md#sessionrecord) |
| [SessionDispatchLinked](events.md#sessiondispatchlinked) | [SessionDispatchLink](domain.md#sessiondispatchlink).`session_dispatch_link_id` (row identity), with `session_id/dispatch_id` membership | Add sole exact link; derive reverse membership without persisting it. | [SessionRecord](queries.md#sessionrecord), [DispatchScopeProjection](queries.md#dispatchscopeprojection) |
| [ResearchCaptureAppended](events.md#researchcaptureappended) | [ResearchCapture](domain.md#researchcapture).`dispatch_id/expected_contribution_id` | Add immutable capture and move current head only on valid predecessor. | [SessionRecord](queries.md#sessionrecord), [DispatchScopeProjection](queries.md#dispatchscopeprojection), [ResearchRecord](queries.md#researchrecord) |
| [ResearchFactAppended](events.md#researchfactappended) Entity variant | [FactEnvelope](domain.md#factenvelope).`fact_id/subject_id` | Add immutable fact; move unique subject head. | [SessionRecord](queries.md#sessionrecord)/[DispatchScopeProjection](queries.md#dispatchscopeprojection) counts, [ResearchRecord](queries.md#researchrecord) collections |
| disposition [ResearchFactAppended](events.md#researchfactappended) variant | [TargetRef](domain.md#disposition-and-assessment-payload-variants) + `policy_ref` aggregate | Move only that policy disposition head. | Policy-keyed maps/counts |
| assessment [ResearchFactAppended](events.md#researchfactappended) variant | [TargetRef](domain.md#disposition-and-assessment-payload-variants) + actor/method/policy aggregate | Move only that assessor head; retain independent disagreement. | [ResearchRecord](queries.md#researchrecord) maps |
| [ReferenceProbeLineageAppended](events.md#referenceprobelineageappended) | [ProbeRecommendationRef](domain.md#proberecommendationref) derived composite key | Move one delivery head; asserts no use/access/support alone. | [ResearchRecord](queries.md#researchrecord) delivery-origin projection |

AgentReferenceLineage additionally consumes query-bound external evidence without adding an APT
event or reducer head:

| Bound external source | Projection effect | Authority retained by |
|---|---|---|
| ACI `reference_scout.bundle_delivered_to_agent@1` + `AgentReferenceDelivery` + `EffectiveInputArtifact` | Recommended/delivered/effective-input row spine. | ACI |
| host `SourceObservation` manifest | Access-observed axis only when the future `available` contract proves exact scope/target/origin; current `unavailable` maps empty. | Host |
| APT accepted current fact heads | Declared-use, relation and claim-support-check axes. | APT accepted prefix |

Only a verified complete group applies, exactly once at its `last_offset`. Envelope `journal_offset`
orders groups; `recorded_at`, `observed_at`, caller order and wall clock never choose semantic
precedence.

---

## Digest Inclusion, Exclusion and Losslessness

| Digest/hash | Included | Excluded |
|---|---|---|
| capture digest | Every closed `apt.research-capture@1` slot in domain order, including canonical nulls, snapshot/artifact refs, predecessor and ordered synthesis pins | `capture_digest` itself; event envelope, receipt/grouping |
| fact semantic digest | Exact Entity payload variant including complete [FactEnvelope](domain.md#factenvelope) and extraction/check attribution | top-level ingestion actor/time, ACI envelope, receipt/grouping |
| fact event payload hash | exact payload variant + top-level actor + event semantic time | ACI envelope acceptance fields and receipt/grouping |
| delivery key | accepted `{probe_id,bundle_digest,recommendation_id}` | caller precomputed key, mutable locator |
| command digest | exact canonical command identity/input, expected heads and owner evidence required by the Operation | receipt, offsets and post-commit fields |
| query snapshot digest | exact pinned input manifest + exact digest map | current mutable external snapshot/display context |
| query projection hash | schema, identity, `effective_as_of`, manifest, digests and closed value | `requested_o` except through effective/bound manifest as specified; raw bytes, current external state |
| `apt_accepted_prefix` digest | requested/effective boundary, grouping profile/digest and complete verified groups | incomplete/future group, mutable journal tail |
| `target_resolution` digest | complete closed wrapper: ACI owner constants, query scope, accepted boundary, non-self-referential verified owner digest and canonical target members | bare member set, caller subset, owner state after boundary |
| `producer_resolution` digest | `H_ACI(canonical(producer_resolution))` over the complete closed host wrapper: exact owner constants, five-field scope, accepted boundary, non-self-referential verified owner digest and canonical producer members | caller subset, post-boundary state, bare members or self-referential digest material |
| `aci_delivery_snapshot` digest | complete closed wrapper: ACI delivery owner constants, target-wrapper digest scope, accepted boundary, verified owner digest and canonical delivery members | raw bundle bytes, omitted/future delivery, another target-wrapper scope |
| `probe_scout_bindings` digest | complete closed wrapper: canonical APT owner constants, delivery-wrapper digest scope, accepted boundary, verified owner digest and canonical binding members | ambiguous alias, forked commit/membership, another delivery scope |
| `apt_fact_heads` digest | complete canonical current fact-head set derived from `apt_accepted_prefix.complete_groups` | caller-supplied subset, superseded/non-head fact, any `owner_manifest_digest` |
| `host_observation_projection` digest | entire closed union; `unavailable` includes owner constants, `scope={dispatch_id,target_resolution_digest,aci_delivery_snapshot_digest}` and required contract digest; `available` includes that same scope plus accepted boundary, non-self-referential owner digest and canonical observations | fields of the opposite variant, locator join, mutable/current host state |

Mappings are lossless over every semantic source field: a direct field remains equal, an owner field
retains its owner evidence, a derived field is reproducible from its stated preimage, and an omitted
field is omitted only because the target contract explicitly forbids it. Raw bytes are the sole
intentional non-propagating verifier input; their immutable artifact reference and digests preserve
evidence without duplicating content.

## Mapping Coverage and Required Checks

| Required surface | Mapping section | Coverage |
|---|---|---:|
| three registered Mapping concepts | [APTFactToACIEvent](#aptfacttoacievent), [ProbeBundleToReferenceLineage](#probebundletoreferencelineage), [ProvenanceFactsToReadModels](#provenancefactstoreadmodels) | `3/3` |
| six caller mutation intents → six bound commands | [Caller Intents to Bound Commands](#caller-intents-to-bound-commands), [Fact Intent](#fact-intent-to-exact-payload-and-factenvelope), [Probe](#probebundletoreferencelineage) | `6/6` |
| six Operations → accepted event sets | [APTFactToACIEvent](#aptfacttoacievent) | `6/6` |
| eight Entity fact variants + disposition + assessment | [Variant Field Mapping](#variant-field-mapping) | `10/10` |
| probe partition/result branches | [Probe mapping](#probebundletoreferencelineage) | `3/3` |
| four Query intents/manifests/results | [Query mapping](#provenancefactstoreadmodels) | `4/4` |
| six registered APT Events / eight reducer-family rows | [Projection rows](#accepted-aci-events-to-projection-rows) | `6/6 events; 8/8 rows` |

- Schema fixtures reject every unknown, missing and caller-authored owner field.
- Canonical-null fixtures distinguish null, omission, empty string/list and zero.
- Round-trip fixtures prove direct-field equality and deterministic recomputation of every derived
  digest/key/hash; no test reconstructs authority from a projection.
- Privacy fixtures prove raw/selected bytes occur only inside the transient verifier and never in
  mapped payloads/envelopes/results/telemetry.
- Retry/existing-exact fixtures prove no duplicate event/envelope/receipt membership.
- Query fixtures prove the same accepted prefix and manifests map to the same rows/hash with zero
  external calls or side effects during replay.
- Agent-reference fixtures permute canonical members, swap query scopes/wrappers, omit facts or
  deliveries and exercise every asymmetric evidence-axis combination; invalid or incomplete
  evidence fails rather than mapping to a false empty.
- Producer-resolution negative fixtures omit/add a selector member, swap the producer digest, use
  the wrong activation, omit an Attempt tuple field, mismatch the delivery target, alter any of the
  five scope fields, and instrument an implicit owner lookup during reduction. Each case fails
  closed before any `declared_used` member is emitted; reducer owner-call count remains zero.

## Connections

| Document | Type | Description |
|---|---|---|
| [SPEC.md](SPEC.md) | `derives-from` | Registry and relationship authority; this aspect adds no concept. |
| [interfaces.md](interfaces.md) | `maps-from` | Closed caller intents, outcomes, manifests and errors. |
| [operations.md](operations.md) | `maps-to` | Owner-bound command contracts and guards. |
| [events.md](events.md) | `maps-to` | Exact APT payloads carried by ACI envelopes. |
| [queries.md](queries.md) | `maps-to` | Four deterministic result shapes and formulas. |
| [states.md](states.md) | `reduces-through` | Current binding/capture/fact/aggregate heads. |
| [rules.md](rules.md) | `constrained-by` | Authority, idempotency, replay, privacy and canonicalization invariants. |
| [TEST-SPEC](../TEST-SPEC.md) | `verification-planned` | Planned fixtures only; unchanged by this aspect. |
