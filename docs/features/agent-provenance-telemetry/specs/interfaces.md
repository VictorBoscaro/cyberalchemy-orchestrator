---
tags: [agent-provenance-telemetry, spec, interfaces]
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

# Interfaces: Agent Provenance Telemetry

This document specifies internal L0 module contracts only. It registers no REST, GraphQL, CLI or
public network API and adds no Interface concept beyond
[ProvenanceAppendPort](SPEC.md#concept-registry) and
[ProvenanceQueryPort](SPEC.md#concept-registry). Supporting owner/evidence ports below are
architecture dependency roles, not new APT-owned domain concepts or registry entries.

## Boundary Principles

- Callers provide intent. Authenticated host/application and ACI owners bind identity, evidence,
  IDs, times, current heads, canonical bytes and receipts.
- Every input is a closed versioned shape. Unknown fields, caller-authored owner fields and missing
  canonical slots fail closed.
- Domain validation is pure. Owner resolution, artifact reads, profile checks and journal I/O occur
  outside the domain and before/after it in the order specified below.
- ACI remains the sole bus, journal, canonicalizer, artifact-finalization and receipt authority.
  No interface returns a journal/store handle or permits a direct write.
- Durable append precedes acknowledgment. Operational logs/projections never substitute for a
  receipt.
- There is no physical artifact-backend interface in APT. The ACI artifact boundary hides it.

## Common Closed Shapes

### TrustedInvocationContext

This is host-supplied transport context, not an untrusted request-body field and not a registered
DomainSpec concept.

```text
closed {
  authenticated_principal_ref,
  actor_authentication_ref,
  actor_authentication_digest,
  origin_kind,
  origin_ref,
  correlation_ref
}
```

The application ignores/rejects duplicate caller claims for any of these fields. Action-specific
authorization is separately resolved by the host authorization owner.

### Caller Intent Shapes

Every schema and nested variant below is an exhaustive allowlist. An omitted slot is forbidden
unless marked `?`; unknown fields and every field in the exhaustive forbidden sets fail closed.

```text
apt.ensure-session-intent@1 =
  closed {operation_id, requested_initial_name}

apt.start-new-session-intent@1 =
  closed {operation_id, requested_initial_name, expected_current_session_id}

apt.link-session-dispatch-intent@1 =
  closed {operation_id, requested_dispatch_id}

raw_return_intent = canonical null | closed {artifact_id}
failure_evidence_ref_intent =
  canonical null |
  closed {
    kind="aci_event",
    accepted_event_id,
    expected_contract_version,
    expected_evidence_digest
  } |
  closed {
    kind="aci_receipt",
    receipt_id,
    expected_contract_version,
    expected_evidence_digest
  } |
  closed {
    kind="artifact",
    artifact_id,
    expected_contract_version,
    expected_evidence_digest
  } |
  closed {
    kind="host_observation",
    source_observation_id,
    expected_contract_version,
    expected_evidence_digest
  }
synthesis_pin_intent =
  canonical ordered unique list<closed {research_capture_id}>
probe_recommendation_ref_intent =
  closed {probe_id, recommendation_id, bundle_digest}
evidence_ref_intent = closed {artifact_id}
evidence_ref_intents =
  canonical sorted unique set<
    closed {kind="artifact", artifact_id} |
    closed {kind="fact", fact_id}
  >

apt.append-research-capture-intent@1 = closed {
  capture_operation_id,
  expected_contribution_id,
  capture_status,
  raw_return_intent,
  partial_reason,
  failure_reason,
  failure_evidence_ref_intent,
  supersedes_capture_id,
  synthesis_pin_intent
}

extraction_intent = closed {
  mode,
  actor_ref,
  method_ref,
  selector_intent: closed {start_inclusive, end_exclusive}
}

research_question_intent = closed {
  variant="research_question",
  research_question_id, question_text, derives_from, extraction_intent
}
research_answer_intent = closed {
  variant="research_answer",
  research_answer_id, question_ids, extraction_intent
}
reference_use_intent = closed {
  variant="reference_use",
  reference_use_id, reference_id, reference_kind, locator_observed,
  source_observation_id?, probe_recommendation_ref_intent?,
  use_kind, anchor_quality, extraction_intent
}
reference_claim_relation_intent = closed {
  variant="reference_claim_relation",
  relation_id, reference_use_id, research_claim_id, relation, extraction_intent
}
reference_check_intent = closed {
  variant="reference_check",
  reference_check_id, check_kind, reference_use_id, relation_id?,
  checked_by, method_ref, result, evidence_ref_intent?
}
research_problem_intent = closed {
  variant="research_problem",
  problem_id, kind, statement, blocks, evidence_ref_intents, extraction_intent
}
research_claim_intent = closed {
  variant="research_claim",
  research_claim_id, statement, answer_ids, extraction_intent
}
formalization_candidate_intent = closed {
  variant="formalization_candidate",
  formalization_id, research_claim_id, notation, latex?, legend, reading,
  logic_family, assumptions, scope, extraction_intent,
  syntax_checker_ref?, proof_check_ref?, governance_ref?
}
disposition_recorded_intent = closed {
  variant="disposition_recorded",
  target_kind, target_id, disposition, policy_ref
}
assessment_recorded_intent = closed {
  variant="assessment_recorded",
  target_kind, target_id, assessment, method_ref, policy_ref
}

entity_fact_intent =
  research_question_intent|research_answer_intent|reference_use_intent|
  reference_claim_relation_intent|reference_check_intent|research_problem_intent|
  research_claim_intent|formalization_candidate_intent

apt.append-research-fact-intent@1 =
  closed {
    operation_id,
    payload_intent_variant: entity_fact_intent,
    expected_subject_head_fact_id
  }
  |
  closed {
    operation_id,
    payload_intent_variant: disposition_recorded_intent|assessment_recorded_intent,
    expected_head_accepted_event_id,
    expected_aggregate_version
  }

probe_delivery_origin_intent = closed {
  kind="delivery_origin",
  probe_recommendation_ref_intent,
  expected_head_event_id
}
probe_use_intent = closed {
  kind="use_intent",
  reference_use_id,
  probe_recommendation_ref_intent,
  reference_id,
  reference_kind,
  locator_observed,
  source_observation_id?,
  use_kind,
  anchor_quality,
  extraction_intent,
  expected_subject_head_fact_id
}
apt.append-reference-probe-lineage-intent@1 = closed {
  operation_id,
  lineage_items: non-empty unordered unique set<
    probe_delivery_origin_intent|probe_use_intent
  >
}
```

These nested `*_intent` shapes are caller selectors/claims, not verified owner evidence. Their
binders either produce the exact operation-defined value or fail.

The capture failure-evidence intent matrix is closed:

| `capture_status` | `failure_evidence_ref_intent` |
|---|---|
| `captured` | canonical null |
| `partial` | canonical null or the non-null closed selector |
| `missing` | non-null closed selector required |

The four non-null routes are exact:

| Intent variant | Verification route | Owner-bound result |
|---|---|---|
| `aci_event` | [ACIProfileReceiptVerifier](#aciprofilereceiptverifier).`verify_acceptance({kind="aci_event",accepted_event_id}, expected_contract_version, expected_evidence_digest)` | `aci_event {owner_namespace="agents-communication-infra", contract_version, accepted_event_id, evidence_digest}` |
| `aci_receipt` | [ACIProfileReceiptVerifier](#aciprofilereceiptverifier).`verify_acceptance({kind="aci_receipt",receipt_id}, expected_contract_version, expected_evidence_digest)` | `aci_receipt {owner_namespace="agents-communication-infra", contract_version, receipt_id, evidence_digest}` |
| `artifact` | [ArtifactFinalizationVerifier](#artifactfinalizationverifier).`verify_finalized(artifact_id)` plus exact expected-version/digest comparison | `artifact {owner_namespace="agents-communication-infra", contract_version, artifact_id, evidence_digest}` |
| `host_observation` | [HostSourceObservationEvidencePort](#hostsourceobservationevidenceport).`resolve(source_observation_id)` plus exact expected-version/digest comparison | `host_observation {owner_namespace="host", contract_version, source_observation_id, evidence_digest}` |

Each result's `contract_version=expected_contract_version` and
`evidence_digest=expected_evidence_digest`. Success produces the complete owner-bound
[FailureEvidenceRef](domain.md#failureevidenceref-embedded-union) in
[ResearchCapture](domain.md#researchcapture).`failure_evidence_ref`. Unknown discriminators,
missing fields, opposite-variant fields, not-found/uncommitted evidence, owner/version/digest
mismatch or wrong evidence meaning fails mapping. Caller-authored `failure_evidence_ref` remains
forbidden.

The exhaustive forbidden owner fields are:

- ensure intent: `ensure_key`, `origin_kind`, `origin_ref`, `actor_ref`,
  `actor_authentication_ref`, `actor_authentication_digest`, `session_id`, `started_at`,
  `session_started_event_id`, `canonicalizer_profile_id`, `canonicalizer_profile_version`,
  `canonicalizer_profile_digest`;
- rollover intent: `origin_kind`, `origin_ref`, `predecessor_session_id`, `successor_session_id`,
  `successor_ensure_key`, `started_at`, `rebound_at`, `session_started_event_id`,
  `session_context_rebound_event_id`, `actor_ref`, `authorization_policy_ref`,
  `authorization_policy_digest`, `authorization_evidence_ref`, `authorization_evidence_digest`,
  `canonicalizer_profile_id`, `canonicalizer_profile_version`, `canonicalizer_profile_digest`;
- link intent: `origin_kind`, `origin_ref`, `session_id`, `session_dispatch_link_id`, `linked_at`,
  `session_dispatch_linked_event_id`, `dispatch_snapshot_ref`, `actor_ref`,
  `authorization_policy_ref`, `authorization_policy_digest`, `authorization_evidence_ref`,
  `authorization_evidence_digest`, `canonicalizer_profile_id`, `canonicalizer_profile_version`,
  `canonicalizer_profile_digest`;
- capture intent: `schema_ref`, `research_capture_id`,
  `research_capture_appended_event_id`, `captured_at`, `origin_kind`, `origin_ref`, `session_id`,
  `session_dispatch_link_id`, `dispatch_id`, `dispatch_snapshot_ref`, `origin_refs`, `producer_ref`,
  verified `raw_return`, `failure_evidence_ref`, verified `synthesizes`, `current_capture_head`,
  `capture_digest`, `canonicalizer_profile_id`, `canonicalizer_profile_version`,
  `canonicalizer_profile_digest`;
- fact intent: `payload_variant`, `research_capture_id`, `fact`, `FactEnvelope`, `fact_id`,
  `subject_id`, `member_fact_operation_id`, `fact_occurred_at`, `occurred_at`,
  `supersedes_fact_id`, `event_id`, `event_occurred_at`, `actor_ref`,
  `authenticated_principal_ref`, `research_capture`, `extracted_at`, `source_capture_id`,
  `source_capture_digest`, selector `schema_ref`, selector `unit`, `selected_text_digest`,
  `current_fact_head`, `current_aggregate_head`, `aggregate_type`, `aggregate_id`,
  `raw_artifact_bytes`, `artifact_authority_ref`, `artifact_digest`, `dispatch_snapshot_ref`,
  `canonical_payload_digest`, `canonicalizer_profile_id`, `canonicalizer_profile_version`,
  `canonicalizer_profile_digest`;
- probe intent: `full_research_reference_use_payload`, `delivery_origin_payload`,
  `delivery_subject_key`, `stable_subject_key`, `payload_variant`, `FactEnvelope`, `fact_id`,
  `member_fact_operation_id`, `event_id`,
  `fact_occurred_at`, `event_occurred_at`, `actor_ref`, `authenticated_principal_ref`,
  `probe_recommendation_ref` inside a use item, `bundle_acceptance_receipts`,
  `profile_registration_receipts`, `probe_worker_observation_evidence`,
  `current_delivery_heads`, `current_fact_heads`, `current_captures`,
  `finalized_raw_artifact_bytes`, `lineage_event_ids`, `research_fact_event_ids`,
  `lineage_event_times`, `research_fact_event_times`, `canonical_payload_digest`,
  `command_digest`,
  `canonicalizer_profile_id`, `canonicalizer_profile_version`,
  `canonicalizer_profile_digest`.

The APT binders resolve those fields and create exact operation-defined payload variants and, for
Entity fact/probe-use variants, the `FactEnvelope`. No linked schema loosens these allowlists.

For probe intents, delivery and use name the same caller-owned recommendation composite
`{probe_id,bundle_digest,recommendation_id}` through `probe_recommendation_ref_intent`. The binder
must resolve it to one accepted committed recommendation, validate that the use points to the
accepted delivery, and derive:

```text
delivery_composite =
  {accepted.probe_id, accepted.bundle_digest, accepted.recommendation_id}
derived_delivery_subject_key = H_ACI(canonical(delivery_composite))

bound_delivery.delivery_subject_key = derived_delivery_subject_key
bound_use.delivery_subject_key = derived_delivery_subject_key
```

Both exact payloads receive that owner-derived key. A caller-authored `delivery_subject_key`,
`stable_subject_key` or other precomputed key is rejected even when it equals the derived value.

### AppendOutcome

The return union is closed:

```text
accepted_new = closed {
  kind="accepted_new",
  domain_result,
  accepted_event_refs,
  receipt
}

submitted_retry = closed {
  kind="submitted_retry",
  domain_result,
  accepted_event_refs,
  prior_receipt
}

semantic_existing = closed {
  kind="semantic_existing",
  domain_result,
  existing_accepted_event_refs,
  receipt=null
}
```

`accepted_new` is returned only after durable commit. `submitted_retry` reuses the byte-stable
receipt for the same command identity/digest. `semantic_existing` is for a never-submitted command
whose preflight finds no new semantic member; it makes no receipt/idempotency claim.

`EnsureSession`/`LinkSessionDispatch` may specialize `domain_result` as reused Session/exact link.
`AppendResearchFact` uses the original event ref for global exact fact collision.
`AppendReferenceProbeLineage` uses the result shape below.

### ProbeAppendOutcome

```text
closed {
  kind="probe_result",
  submission_status: accepted_new|submitted_retry|semantic_existing,
  result_by_request_key: canonical map<
    request_key,
    {status: existing_exact|accepted_new, accepted_event_ref}
  >,
  existing_exact: canonical set<accepted_event_ref>,
  accepted_submitted_new: ordered list<accepted_event_ref>,
  receipt: ACI receipt|null
}

result = existing_exact ∪ accepted(submitted_new)
receipt.members = accepted(submitted_new)
existing_exact ∩ receipt.members = ∅
```

The three branches are exact:

| `submission_status` | Required invariants |
|---|---|
| `accepted_new` | `accepted_submitted_new≠∅`; `receipt≠null`; the receipt is the newly durable command receipt; `receipt.members=accepted_submitted_new`. |
| `submitted_retry` | the same command identity and digest was already submitted; `accepted_submitted_new≠∅`; `receipt` is the byte-stable prior receipt; the total mapping equals the prior result. |
| `semantic_existing` | `accepted_submitted_new=∅`; `receipt=null`; every result entry is `existing_exact`; no ACI command is submitted. |

For every branch, `result_by_request_key` is total over the submitted request keys, its
`existing_exact` entries equal the `existing_exact` set, and its `accepted_new` entries equal the
`accepted_submitted_new` list as a set. For a mixed newly accepted result, only new
events/heads/semantic keys and the total mapping commit in the ACI transaction; preexisting refs
retain their original acceptance. Failure commits none of the new portion and does not hide or
reaccept `existing_exact`.

### InterfaceError

```text
boundary_error = closed {
  kind="boundary_error",
  code:
    SCHEMA_UNSUPPORTED|UNKNOWN_FIELD|AUTHENTICATION_REQUIRED|AUTHORIZATION_DENIED|
    OWNER_EVIDENCE_INVALID|PROFILE_UNAVAILABLE|APPEND_FAILED|READ_INTEGRITY_FAILURE|NOT_FOUND,
  operation_ref,
  retryability: never|same-command|refresh-owner-evidence,
  safe_detail,
  correlation_ref
}

operation_error = closed {
  kind="operation_error",
  code:
    IDEMPOTENCY_CONFLICT|ENSURE_ORIGIN_CONFLICT|HOST_EVIDENCE_INVALID|IDENTITY_INVALID|
    ROLLOVER_UNAUTHORIZED|BINDING_CAS_CONFLICT|SUCCESSOR_INVALID|ATOMIC_PROFILE_UNAVAILABLE|
    ATOMIC_GROUP_INVALID|AUTHORITY_NOT_FOUND|SESSION_BINDING_STALE|LINK_UNAUTHORIZED|
    SNAPSHOT_IDENTITY_MISMATCH|JOIN_CONFLICT|SNAPSHOT_INVALID|BACKFILL_UNSUPPORTED_L0|
    CAPTURE_SCHEMA_INVALID|EVIDENCE_INVALID|RAW_ARTIFACT_INVALID|DISPATCH_SNAPSHOT_INVALID|
    CURRENT_LINK_REQUIRED|CAPTURE_CAS_CONFLICT|SYNTHESIS_INVALID|FACT_SCHEMA_INVALID|
    FACT_VARIANT_BINDING_INVALID|FACT_LOCALITY_INVALID|SELECTOR_INVALID|FACT_TYPE_INVALID|
    FACT_CAS_CONFLICT|FACT_IDENTITY_CONFLICT|SEMANTIC_REGISTRY_PROFILE_UNAVAILABLE|
    AGGREGATE_CAS_CONFLICT|AGGREGATE_ACTOR_MISMATCH|BUNDLE_ACCEPTANCE_INVALID|
    PROFILE_BINDING_INVALID|LINEAGE_INVALID|DUPLICATE_MEMBER_KEY|VIRTUAL_SEQUENCE_FORBIDDEN|
    PROVEN_USE_INVALID|LINEAGE_ACTOR_MISMATCH|EXTRACTION_ATTRIBUTION_INVALID|
    DELIVERY_ORIGIN_REQUIRED|LINEAGE_SCOPE_VIOLATION,
  operation_ref,
  retryability: never|same-command|refresh-owner-evidence,
  safe_detail,
  correlation_ref
}
```

`InterfaceError = boundary_error | operation_error`. `retryability` is derived, never selected by
an adapter:

- `same-command`: `APPEND_FAILED` only.
- `refresh-owner-evidence`: `AUTHENTICATION_REQUIRED`, `AUTHORIZATION_DENIED`,
  `OWNER_EVIDENCE_INVALID`, `PROFILE_UNAVAILABLE`, `ROLLOVER_UNAUTHORIZED`,
  `BINDING_CAS_CONFLICT`, `ATOMIC_PROFILE_UNAVAILABLE`, `AUTHORITY_NOT_FOUND`,
  `SESSION_BINDING_STALE`, `LINK_UNAUTHORIZED`, `CURRENT_LINK_REQUIRED`,
  `CAPTURE_CAS_CONFLICT`, `FACT_CAS_CONFLICT`, `SEMANTIC_REGISTRY_PROFILE_UNAVAILABLE`,
  `AGGREGATE_CAS_CONFLICT`, `BUNDLE_ACCEPTANCE_INVALID`, and `PROFILE_BINDING_INVALID`.
- `never`: every other listed code.

An owner/adapter failure must map to one listed code; owner-defined or arbitrary codes cannot cross
this interface. Errors contain no raw bytes, credentials or unredacted evidence.

## ProvenanceAppendPort

**Type:** registered internal Interface concept.  
**Consumers:** trusted orchestration host/application callers.  
**Implementation:** APT application service coordinating pure validation, owner-evidence ports and
the ACI append adapter.

The six methods below are the complete L0 mutation surface. There is no generic
`append_event`, `put`, `update`, transaction callback or store handle.

| Method | Input | Success | Maps To |
|---|---|---|---|
| `ensure_session(intent, invocation)` | `apt.ensure-session-intent@1`, `TrustedInvocationContext` | `AppendOutcome<Session>` | [EnsureSession](operations.md#ensuresession) |
| `start_new_session(intent, invocation)` | `apt.start-new-session-intent@1`, `TrustedInvocationContext` | `AppendOutcome<Session>` with one atomic two-event receipt | [StartNewSession](operations.md#startnewsession) |
| `link_session_dispatch(intent, invocation)` | `apt.link-session-dispatch-intent@1`, `TrustedInvocationContext` | `AppendOutcome<SessionDispatchLink>` | [LinkSessionDispatch](operations.md#linksessiondispatch) |
| `append_research_capture(intent, invocation)` | `apt.append-research-capture-intent@1`, `TrustedInvocationContext` | `AppendOutcome<ResearchCapture>` | [AppendResearchCapture](operations.md#appendresearchcapture) |
| `append_research_fact(intent, invocation)` | `apt.append-research-fact-intent@1`, `TrustedInvocationContext` | `AppendOutcome<ResearchFactAppended ref>` | [AppendResearchFact](operations.md#appendresearchfact) |
| `append_reference_probe_lineage(intent, invocation)` | `apt.append-reference-probe-lineage-intent@1`, `TrustedInvocationContext` | `ProbeAppendOutcome` | [AppendReferenceProbeLineage](operations.md#appendreferenceprobelineage) |

### Authentication and Authorization

| Method | Authentication | Additional authorization/evidence |
|---|---|---|
| `ensure_session` | authenticated host/orchestrator principal | host-owned origin/ensure binding |
| `start_new_session` | authenticated principal | single-use host authorization evidence for action/origin/expected Session/policy/nonce/expiry |
| `link_session_dispatch` | authenticated principal | action authorization plus pinned Dispatch snapshot |
| `append_research_capture` | authenticated producer/host principal | current context Session/link, producer evidence, snapshot and artifact/failure evidence |
| `append_research_fact` | authenticated extractor/reviewer/host principal | current capture/head, artifact bytes/evidence and exact attribution |
| `append_reference_probe_lineage` | authenticated ingestion principal | committed bundle/profile receipts, delivery/fact heads, optional host observation and use evidence |

The domain receives already bound evidence values; it never calls an authorization, clock, artifact
or network interface.

### Processing Order

```text
1. reject unknown schema/fields and caller-authored owner fields
2. authenticate trusted invocation
3. resolve current accepted state and required owner evidence at one offset
4. verify artifact/snapshot/profile/receipt evidence
5. run pure closed-shape/domain validation and canonical projection
6. call the APT-owned `ACICommandAdapter`, which sends one command request to the ACI-owned command
   boundary
7. inside ACI, atomically perform command lookup, semantic preflight, CAS, journal append and
   receipt/result creation, appending only genuinely new payload(s)
8. verify and reconcile the returned transactional partition/result mapping
9. acknowledge only after verified durable receipt; otherwise return typed error
```

For `fact_id`, step 6 uses the global ACI transactional unique key and compares
`fact_semantic_digest`, `subject_id`, and `supersedes_fact_id`. An exact match returns the original
event and does not create new event payload/envelope metadata. Any mismatch conflicts.

## ACICommandAdapter

**Classification:** supporting outbound adapter role; not an APT DomainSpec Interface concept.  
**Owner:** APT owns the adapter role and implementation. ACI owns the invoked command boundary,
canonicalizer, registered profiles, journal transaction and receipts/results.

| Method | Input | Output | Boundary rule |
|---|---|---|---|
| `submit_single(validated_candidate)` | exact canonical payload proposal, command identity/digest, expected heads and optional fact semantic guard | `accepted_new | submitted_retry | semantic_existing | conflict` with receipt where applicable | one request to the ACI command boundary; inside one journal transaction ACI performs command lookup, semantic guard, CAS, append and receipt/result creation |
| `submit_atomic(validated_candidate_batch)` | non-empty canonical candidate items, command identity/digest, expected heads and semantic guards | transactional partition plus verified grouping receipt when `submitted_new` is non-empty, or typed conflict/error | one request to the ACI command boundary; inside one journal transaction ACI performs command lookup, determines `existing_exact/submitted_new`, applies all guards and commits all new members/heads/keys/total mapping or none |

Semantic fact preflight is an internal ACI command-boundary step of `submit_single/submit_atomic`
and is not exposed as a standalone method or two-phase application check. The exact required profile is
`aci.transactional-semantic-uniqueness-result-mapping@1` with the ACI-registered digest. Multi-event
methods also require the exact ACI receipt/read-grouping profile. Missing/mismatched profiles block
the method; the adapter cannot emulate them.

The adapter exposes no Work Bus publishing primitive, journal connection, receipt table, physical
artifact backend or transaction handle. No ACI transaction handle crosses the command boundary.
It exposes no command lookup method: lookup is part of every ACI submit transaction and no
read/poll/diagnostic result may authorize a success branch.

## Owner Evidence Ports

These are outbound dependency roles consumed by application binders. Their values are trusted only
after owner namespace/version/digest verification. They are not public APT APIs or new registry
concepts.

### HostAuthorizationEvidencePort

| Method | Input | Output | Used By |
|---|---|---|---|
| `authorize(action, principal, origin, expected_subject, correlation_ref)` | exact action context | owner-bound policy/evidence refs+digests, expiry, nonce, principal/action/origin/expected-subject binding | `start_new_session`, `link_session_dispatch` |

The host owner validates expiry using its clock. APT replay pins and verifies the resulting values;
it never reruns current policy.

### HostSourceObservationEvidencePort

| Method | Input | Output | Used By |
|---|---|---|---|
| `resolve(source_observation_id)` | opaque host-owned ID | committed owner/version/digest evidence or `not_found` | reference use, probe ingress and failure evidence |
| `bind_agent_reference_observations(dispatch_id, target_resolution, delivery_snapshot, effective_as_of)` | exact owner-verified target/delivery wrappers | closed `unavailable` or complete owner-authored `available` observation manifest from [AgentReferenceLineage](queries.md#agentreferencelineage) | agent-reference query binder |

Absence stays null. Locator similarity cannot synthesize a source observation. The result proves
only the meaning defined by the host observation contract. The current Stage-G contract returns the
closed `unavailable` variant because it lacks authoritative observation-to-delivery plus Attempt
binding; APT cannot upgrade current ingestion rows into `available`.
Both variants serialize the same closed
`scope {dispatch_id,target_resolution_digest,aci_delivery_snapshot_digest}`. The binder requires
that scope to equal the Query intent and pinned complete-wrapper digests before reduction; the
`available.owner_manifest_digest` includes the scope in its non-self-referential preimage.

### HostAgentActivationBindingEvidencePort

**Contract status:** specified for the next bounded slice; not implemented by the current pilot.

| Method | Input | Output | Used By |
|---|---|---|---|
| `bind_capture_producers(scope, capture_producer_selector, effective_as_of)` | closed exact `scope {dispatch_id,target_resolution_digest,aci_delivery_snapshot_digest,probe_scout_bindings_digest,capture_producer_selector_digest}`, canonical binder-derived selector and verified effective boundary | complete owner-authored `producer_resolution` wrapper from [AgentReferenceLineage](queries.md#agentreferencelineage), or typed integrity failure | agent-reference query binder before pure reduction |

The binder derives `capture_producer_selector` from verified current APT facts and the already
verified target/delivery/probe wrappers. A caller cannot supply relationships, members or owner
evidence. The port requires exactly
`owner_namespace="host"`, `owner_contract_id="host.AgentActivationBinding"` and the expected
contract version; verifies exact scope, `accepted_through<=effective_as_of`, non-self-referential
owner manifest digest, complete one-member-per-selector cardinality, accepted Attempt event/group
evidence and the `activation_id` child binding to that same complete Attempt tuple. Missing, extra,
duplicate, future, cross-scope, ambiguous or digest-mismatched members fail closed. Locator,
persona, model label, timestamp and text equality are forbidden joins. Only the verified wrapper
enters the bound request; the reducer performs zero owner or external calls.

### ArtifactFinalizationVerifier

| Method | Input | Output | Used By |
|---|---|---|---|
| `verify_finalized(reference_or_artifact_id)` | [ArtifactReference](domain.md#artifactreference) or opaque artifact ID selector | verified immutable ref/classification/policy/finalization evidence including owner contract version/evidence digest, or typed failure | capture, fact, probe-use and failure-evidence binding |

It verifies through the ACI artifact boundary. It neither uploads bytes nor exposes the physical
backend.

### ArtifactEvidenceReader

| Method | Input | Output | Used By |
|---|---|---|---|
| `read_verified_utf8(reference)` | already finalized [ArtifactReference](domain.md#artifactreference) | exact bytes plus verified digest/media/charset metadata | byte-exact selector/extraction validation only |

The reader is unavailable to pure domain and projection code. Bytes may exist transiently in the
application validator but never enter events, results, logs, traces or metrics.

### DispatchSnapshotReader

| Method | Input | Owner source | Output | Used By |
|---|---|---|---|---|
| `resolve_for_link(requested_dispatch_id)` | caller's external Dispatch ID only | ACI-managed Dispatch snapshot/event authority or legacy Dispatch ledger authority, selected by the owner | owner-selected and verified closed [DispatchAuthoritySnapshotRef](domain.md#dispatchauthoritysnapshotref), or typed failure | initial Session–Dispatch link binding |
| `verify_pinned(existing_owner_bound_ref, accepted_prefix_boundary)` | immutable snapshot ref already stored in accepted owner-bound link/capture evidence plus the binder's complete verified APT prefix boundary | same snapshot owner selected by the stored discriminator, plus ACI accepted-prefix/grouping verification for the boundary | the same ref after owner verification, or typed failure | capture, query and replay binding |

It supports only the closed `aci_managed | legacy_ledger` variants. It cannot append Dispatch rows
or add L0 ledger keys. For `resolve_for_link`, the owner—not the caller—selects the authority
variant. An `aci_managed` result contains and verifies exact `dispatch_id`, `artifact_ref`,
`artifact_digest`, `accepted_event_id` and `accepted_offset`; a `legacy_ledger` result contains and
verifies exact `{dispatch_id,row_kind,appender_identity,contract_version}` row identity plus
`row_digest`, with optional `row_index` only as a non-authoritative lookup hint and no invented
`accepted_offset`.

`verify_pinned` cannot select another snapshot or accept a caller-created ref. For `aci_managed` it
re-verifies every required field and its accepted event/offset semantics. For `legacy_ledger` it
re-verifies canonical row identity/digest and ignores locator reorder for equality/hash. Its
`accepted_prefix_boundary` is the owner-bound complete verified APT boundary carrying the stored
pin; it does not add an offset field to the legacy variant. The caller supplies only
`requested_dispatch_id` when linking or a closed QueryIntent when reading.
`requested_o/effective_as_of` remains the separate APT query-prefix boundary. Current mutable
Dispatch reads never enter deterministic query results or hashes.

### ACIAgentReferenceEvidenceReader

**Contract status:** specified for the next bounded slice; not implemented.

| Method | Input | Output | Boundary rule |
|---|---|---|---|
| `resolve_targets(dispatch_id, target_selector, effective_as_of)` | exact Dispatch plus closed `attempt \| seat \| agent_instance` selector | complete closed `target_resolution` wrapper from [AgentReferenceLineage](queries.md#agentreferencelineage) | ACI owner resolves Attempt/seat/agent-instance; caller names no relationships. |
| `read_target_deliveries(dispatch_id, target_resolution_digest, effective_as_of)` | exact query scope plus verified complete target-wrapper digest | complete closed `aci_delivery_snapshot` wrapper | Accepted `AgentReferenceDelivery` and effective-input facts only; locators are forbidden. |
| `verify_reference_bundle_entry(delivery_member)` | one delivery member and its event/effective-input refs | same member after event/group/digest/artifact/entry verification or typed failure | Cannot synthesize delivery, amend the manifest or return raw bundle bytes. |

Both wrapper methods return owner namespace/contract/version, serialized query scope,
`accepted_through`, non-self-referential owner manifest digest and the complete duplicate-rejecting
canonical member set. Unexpected owner identity/version, omitted member, future member, scope/digest
swap or incomplete atomic group fails closed. This reader exposes no lookup by locator, title, DOI,
persona or model label.

### ACIProfileReceiptVerifier

| Method | Input | Output | Used By |
|---|---|---|---|
| `verify_profile(profile_binding, registration_ref)` | exact ID/version/digest and owner receipt/event ref | verified owner-bound profile evidence or typed mismatch | atomic operations, probe ingress, semantic registry |
| `verify_acceptance(acceptance_ref, expected_contract_version, expected_evidence_digest)` | closed `aci_event {accepted_event_id} | aci_receipt {receipt_id}` plus exact expected owner contract version/evidence digest | committed acceptance evidence or typed mismatch | artifacts, probe bundle/recommendation, origin/failure evidence |
| `verify_atomic_grouping(receipt)` | receipt/read-grouping shape | verified command ID, offsets, ordered event IDs and payload digest | rollover and probe batch |

Verification does not register a profile, repair a receipt or accept an event.

### AcceptedProvenanceStateReader

| Method | Input | Output | Boundary rule |
|---|---|---|---|
| `read_binding(origin, as_of)` | host origin tuple and verified offset | current Session or null | accepted-prefix read only |
| `read_session_dispatch_link(dispatch_id, as_of)` | Dispatch ID and verified offset | exact link or null | reverse projection cannot become a second authority |
| `read_capture_head(chain_key, as_of)` | `(dispatch_id, expected_contribution_id)` | current capture/digest or null | current predecessor CAS evidence |
| `read_fact_head(subject_id, as_of)` | stable fact subject | current fact/event ref or null | fact CAS evidence |
| `read_aggregate_head(aggregate_id, as_of)` | explicit disposition/assessment aggregate | head event/version or null | aggregate CAS evidence |
| `read_delivery_head(delivery_subject_key, as_of)` | stable probe recommendation composite | delivery event ref or null | probe dependency/CAS evidence |
| `read_probe_scout_binding_manifest(dispatch_id, aci_delivery_snapshot_digest, as_of)` | exact Dispatch and verified delivery-wrapper digest | complete closed `probe_scout_bindings` wrapper | Legacy v1 alias is unique per exact commit/bundle or canonically absent; forks fail closed. |

This reader exposes accepted state; it cannot append, reserve IDs, lock future heads or provide
mutable store access.

## ProbeLineageIngress

**Classification:** inbound transport/application adapter role; not a new Interface concept or bus.  
**Source:** already committed ACI probe bundle/publication delivery.

| Method | Input | Delegates To | Output |
|---|---|---|---|
| `ingest_committed_probe_lineage(delivery, invocation)` | exact bundle/profile/receipt refs plus unordered delivery/use intents | `ProvenanceAppendPort.append_reference_probe_lineage` | `ProbeAppendOutcome` |

Ingress never accepts an uncommitted bundle, publishes a Work Bus message, or treats recommendation
delivery as source access/use/support. It uses ACI profile/receipt verification and submits only
`submitted_new`.

## ProvenanceQueryPort

**Type:** registered internal Interface concept.  
**Consumers:** existing orchestration read surfaces and authorized internal reviewers.  
**Mutation:** none.

The four methods below are the complete specified query surface from the
[SPEC Concept Registry](SPEC.md#concept-registry). They define contracts without claiming query
implementation.

### Query Request and Result

```text
SessionQueryIntent = closed {
  schema_ref="apt.session-record-query@1",
  session_id,
  requested_o
}

DispatchQueryIntent = closed {
  schema_ref="apt.dispatch-scope-query@1",
  dispatch_id,
  requested_o
}

ResearchQueryIntent = closed {
  schema_ref="apt.research-record-query@1",
  research_capture_id,
  requested_o
}

AgentReferenceQueryIntent = closed {
  schema_ref="apt.agent-reference-lineage-query@1",
  dispatch_id,
  target: closed
    {kind="attempt",attempt_id}
    | {kind="seat",seat_id}
    | {kind="agent_instance",agent_instance_id},
  requested_o
}

BoundQueryRequest<TManifest, TDigests> = closed {
  schema_ref,
  requested_o,
  identity,
  pinned_input_manifest: TManifest,
  pinned_input_digests: TDigests
}

QueryResult<T, TManifest, TDigests> = closed {
  schema_ref,
  requested_o,
  effective_as_of,
  pinned_input_manifest: TManifest,
  pinned_input_digests: TDigests,
  projection_hash,
  snapshot_digest,
  value: T
}

effective_as_of =
  max({g.last_offset | verified(g) ∧ g.last_offset≤requested_o} ∪ {genesis})

SessionPinnedInputManifest = closed {
  kind="session_accepted_prefix",
  accepted_prefix: closed {
    requested_o,
    effective_as_of,
    grouping_profile_ref,
    verified_grouping_manifest_digest
  }
}

DispatchPinnedInputManifest = closed {
  kind="dispatch_snapshot",
  dispatch_snapshot_ref
}

ResearchPinnedInputManifest = closed {
  kind="research_capture_and_dispatch_snapshot",
  research_capture: closed {research_capture_id, capture_event_ref, capture_digest},
  dispatch_snapshot_ref
}

AgentReferencePinnedInputManifest =
  exact closed owner-bound shape in
  queries.md#agentreferencelineage
```

The four `*QueryIntent` shapes are caller-owned exhaustive allowlists. A caller-authored
`pinned_input_manifest`, `pinned_input_digests`, `effective_as_of`, `projection_hash`,
`snapshot_digest` or display snapshot is forbidden. The query binder maps the one schema-specific
identity field to `identity` and creates `BoundQueryRequest`; its manifest variant is fixed by the
method and owner-bound after verification. Callers cannot add, remove or replace manifest slots.
`pinned_input_digests` is a canonical ordered map whose exact keys are:

| Method | Exact digest keys |
|---|---|
| `get_session_record` | `accepted_prefix_grouping = H_ACI(canonical(accepted_prefix))` |
| `get_dispatch_scope_projection` | `dispatch_snapshot = H_ACI(canonical(dispatch_snapshot_ref))` |
| `get_research_record` | `research_capture = H_ACI(canonical(research_capture))`; `dispatch_snapshot = H_ACI(canonical(dispatch_snapshot_ref))` |
| `get_agent_reference_lineage` | `apt_accepted_prefix`, `target_resolution`, `producer_resolution`, `aci_delivery_snapshot`, `probe_scout_bindings`, `apt_fact_heads`, `host_observation_projection`: each equals the exact complete-wrapper/derived-set digest defined by [AgentReferenceLineage](queries.md#agentreferencelineage) |

The following equalities are mandatory:

```text
bound.schema_ref = intent.schema_ref
bound.identity = intent.<schema-specific identity>
bound.requested_o = intent.requested_o
result.schema_ref = bound.schema_ref
result.requested_o = bound.requested_o
result.effective_as_of =
  max({g.last_offset | verified(g) ∧ g.last_offset≤bound.requested_o} ∪ {genesis})
result.effective_as_of ≤ result.requested_o

for SessionPinnedInputManifest:
  manifest.accepted_prefix.requested_o = bound.requested_o
  manifest.accepted_prefix.effective_as_of = result.effective_as_of

for AgentReferencePinnedInputManifest:
  bound.identity = {intent.dispatch_id,intent.target}
  manifest.kind = "agent_reference_lineage"
  manifest.apt_accepted_prefix.requested_o = bound.requested_o
  manifest.apt_accepted_prefix.effective_as_of = result.effective_as_of
  every owner wrapper = binder-verified complete query-bound wrapper
  reducer_input =
    bound_verified(target_resolution,producer_resolution,aci_delivery_snapshot,
                   probe_scout_bindings,host_observation_projection)
    + derived apt_fact_heads
```

The result echoes the exact verified bound-request manifest and digest map.
`snapshot_digest = H_ACI(canonical({pinned_input_manifest,pinned_input_digests}))` and
`projection_hash = H_ACI(canonical({schema_ref,identity,effective_as_of,
pinned_input_manifest,pinned_input_digests,value}))`; therefore neither the manifest nor the
effective boundary can change without changing the projection hash.

Every query result exposes requested/effective boundaries. Reducers fold only verified complete
groups, make zero external calls and perform no repair.

| Method | Caller intent | Owner-bound request | Closed result | Maps To |
|---|---|---|---|---|
| `get_session_record(intent)` | `SessionQueryIntent` | `BoundQueryRequest<SessionPinnedInputManifest, SessionPinnedInputDigests>` | `QueryResult<SessionRecord, SessionPinnedInputManifest, SessionPinnedInputDigests>` | planned `SessionRecord` Query in [SPEC](SPEC.md#concept-registry) |
| `get_dispatch_scope_projection(intent)` | `DispatchQueryIntent` | `BoundQueryRequest<DispatchPinnedInputManifest, DispatchPinnedInputDigests>` | `QueryResult<DispatchScopeProjection, DispatchPinnedInputManifest, DispatchPinnedInputDigests>` | planned `DispatchScopeProjection` Query in [SPEC](SPEC.md#concept-registry) |
| `get_research_record(intent)` | `ResearchQueryIntent` | `BoundQueryRequest<ResearchPinnedInputManifest, ResearchPinnedInputDigests>` | `QueryResult<ResearchRecord, ResearchPinnedInputManifest, ResearchPinnedInputDigests>` | planned `ResearchRecord` Query in [SPEC](SPEC.md#concept-registry) |
| `get_agent_reference_lineage(intent)` | `AgentReferenceQueryIntent` | `BoundQueryRequest<AgentReferencePinnedInputManifest, AgentReferencePinnedInputDigests>` | `QueryResult<AgentReferenceLineage, AgentReferencePinnedInputManifest, AgentReferencePinnedInputDigests>` | specified [AgentReferenceLineage](queries.md#agentreferencelineage); not implemented |

### Query Authorization and Errors

Authentication/authorization is enforced by the host read boundary before invoking the pure
projection. A caller cannot supply any authority snapshot for an existing capture or omit required
intent fields.

```text
QueryError = closed {
  code:
    SCHEMA_UNSUPPORTED|UNKNOWN_FIELD|AUTHENTICATION_REQUIRED|AUTHORIZATION_DENIED|
    NOT_FOUND|PINNED_INPUT_INVALID|READ_INTEGRITY_FAILURE,
  retryability: never|refresh-owner-evidence,
  safe_detail,
  correlation_ref
}
```

`AUTHENTICATION_REQUIRED`, `AUTHORIZATION_DENIED`, and `PINNED_INPUT_INVALID` have
`retryability=refresh-owner-evidence`; every other QueryError code has `retryability=never`.
Owner/adaptor failures must map to this finite union; arbitrary owner codes cannot cross the query
interface.

| Condition | Result |
|---|---|
| unauthenticated/unauthorized read | `AUTHENTICATION_REQUIRED` or `AUTHORIZATION_DENIED` |
| unknown schema/field/identity | `SCHEMA_UNSUPPORTED`, `UNKNOWN_FIELD`, or `NOT_FOUND` |
| invalid/incomplete atomic group | buffer to preceding verified boundary or `READ_INTEGRITY_FAILURE` |
| manifest/snapshot kind, identity or digest mismatch | `PINNED_INPUT_INVALID` |
| checkpoint/replay disagreement | fail closed with `READ_INTEGRITY_FAILURE`; never repair in query |

## Interface Coverage

### Business Surface

| Registered interface | Methods | Contract coverage |
|---|---:|---|
| `ProvenanceAppendPort` | 6 | exactly [EnsureSession](operations.md#ensuresession), [StartNewSession](operations.md#startnewsession), [LinkSessionDispatch](operations.md#linksessiondispatch), [AppendResearchCapture](operations.md#appendresearchcapture), [AppendResearchFact](operations.md#appendresearchfact), [AppendReferenceProbeLineage](operations.md#appendreferenceprobelineage) |
| `ProvenanceQueryPort` | 4 | exactly the four Query concepts in [SPEC.md](SPEC.md#concept-registry) |

Supporting adapters/owner ports expose evidence and infrastructure functions only; they do not add
business Operations or Queries. `ProbeLineageIngress` delegates to the existing sixth append method.

### Required Contract Checks

- Method-to-operation coverage is `6/6` with no generic mutation escape hatch.
- Method-to-query coverage is `4/4` with no write side effect.
- Every mutation caller intent matches one exhaustive allowlist and rejects every forbidden
  owner-bound field/unknown slot; fact/probe-use binders alone create exact payload variants and
  `FactEnvelope`.
- Every accepted-new result reconciles event refs with a durable receipt.
- Probe `submission_status` keeps retry, semantic-existing and accepted-new result branches
  distinct and satisfies the branch/partition invariants above.
- Probe callers supply no delivery key; delivery/use resolve the same accepted recommendation
  composite and the binder injects its canonical `H_ACI` key into both exact payloads.
- APT owns only the ACI command adapter; ACI owns command execution, canonicalization, profiles,
  journal transaction and receipts, with no transaction handle exposed.
- The execution adapter exposes no standalone lookup; every submit performs command lookup,
  semantic guards and CAS inside the same ACI transaction.
- Every query accepts only its exhaustive caller `QueryIntent`; its binder creates the owner-bound
  method-specific manifest/digest map, and projection hashes bind that manifest plus
  `effective_as_of`.
- Agent-reference queries obtain target and delivery wrappers only through
  `ACIAgentReferenceEvidenceReader`, producer bindings only through
  `HostAgentActivationBindingEvidencePort`, legacy bindings through the accepted-state reader and
  host observations through the host owner. Producer binding verifies the exact derived selector,
  target/delivery/probe digest scope, complete cardinality, Attempt evidence and activation child
  relationship before reduction. The current observation contract binds `unavailable`; the current
  pilot does not implement producer binding; locators and caller collections cannot replace any
  wrapper, and the reducer performs zero owner calls.
- Append/query errors belong to their finite unions with derived retryability; owner-arbitrary codes
  are rejected.
- Global fact collision uses `fact_id` and the exact semantic tuple; no application cache/store owns
  uniqueness.
- Probe mixed/zero-new results prove total mapping and receipt membership only for
  `submitted_new`.
- Dependency tests forbid domain imports of owner/evidence ports and forbid direct journal,
  physical artifact backend or dispatch-ledger writes.
- Privacy checks prove raw bytes cannot cross event/result/telemetry boundaries.

## Connections

| Document | Type | Description |
|---|---|---|
| [SPEC.md](SPEC.md) | `derives-from` | Registers the two APT Interface concepts and their operation/query edges. |
| [architecture.md](architecture.md) | `constrains` | Defines layer direction, owner boundaries and no-parallel-authority rules. |
| [operations.md](operations.md) | `exposes` | Supplies the six exact mutation contracts, auth, receipts and errors. |
| [events.md](events.md) | `carries` | Defines accepted event payload versus ACI envelope semantics. |
| [rules.md](rules.md) | `enforces` | Defines authority, idempotency, profile, fact identity and replay constraints. |
| [TEST-SPEC](../TEST-SPEC.md) | `verification-planned` | Exists and completed its file-review gate; executable cases remain planned/not-run and do not lift readiness or runtime gates. |
