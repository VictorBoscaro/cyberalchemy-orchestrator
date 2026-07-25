---
tags: [agent-provenance-telemetry, spec, queries]
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

# Queries: Agent Provenance Telemetry

This aspect defines exactly four read-only Query concepts, all exposed by
[ProvenanceQueryPort](interfaces.md#provenancequeryport) as specified, not implemented contracts.
Registration in the [concept registry](SPEC.md#concept-registry) is `4/4`. This aspect introduces
no write operation, external API, persisted read-model authority or additional Query concept.

## Common Deterministic Query Contract

### Intent, Binding and Replay Boundary

Each method accepts only its closed caller-owned `*QueryIntent` from
[interfaces.md](interfaces.md#query-request-and-result). Before replay, the application binder:

1. authenticates and authorizes the caller;
2. resolves the accepted ACI prefix and exact owner-owned pinned inputs;
3. verifies receipt/read-grouping, canonicalizer profile and manifest digests;
4. creates the method-specific `BoundQueryRequest`; and
5. passes immutable verified values to the pure reducer.

The binder may call owner evidence/snapshot readers. The reducer performs zero external calls,
network/tool invocations, current-state lookups, appends, repairs, locks or writes. Query execution
has no side effect, including cache warming that could alter a later answer.

```text
effective_as_of(requested_o) =
  max({g.last_offset | verified(g) ∧ g.last_offset≤requested_o} ∪ {genesis})

accepted_prefix(requested_o) =
  canonically ordered complete verified groups with g.last_offset≤effective_as_of(requested_o)

projection(intent,bound) =
  fold(
    accepted_prefix(bound.requested_o),
    verified_pinned_values(
      bound.pinned_input_manifest,
      bound.pinned_input_digests
    )
  )

result.requested_o = intent.requested_o = bound.requested_o
result.effective_as_of ≤ result.requested_o
```

A request inside an atomic group returns the preceding verified boundary. An invalid group,
overlapping range, duplicate/reused identity with different content, digest mismatch or replay
disagreement fails closed with `READ_INTEGRITY_FAILURE`; the reducer never chooses a branch or
repairs the journal.

### Canonical Collections, Currentness and Dedupe

All result collections are canonical ACI-byte-order sorted sets or maps. Caller/event arrival order
is non-semantic except for the accepted global group order and the semantic ordered
[ResearchCapture](domain.md#researchcapture).`synthesizes` list.

```text
capture_chain(c) = (c.dispatch_id,c.expected_contribution_id)
current_capture_o(k) = head_o(k)

fact_subject(f) = f.fact.subject_id
current_fact_id_o(s) =
  null, if no fact with subject_id=s is accepted in accepted_prefix≤o;
  otherwise, the unique head fact_id of subject chain s in that prefix

head fact_id h of subject chain s ⇔
  accepted(h)≤o
  ∧ subject_id(h)=s
  ∧ every non-null supersedes_fact_id in the chain names the immediately
    preceding accepted fact_id with subject_id=s
  ∧ the chain has no unknown predecessor, cycle, gap or fork
  ∧ ¬∃ accepted successor x≤o:
       subject_id(x)=s ∧ supersedes_fact_id(x)=h

visible_current_captures_o(d) =
  {c | c.dispatch_id=d ∧ c.research_capture_id=current_capture_o(capture_chain(c))}

visible_current_facts_o(c) =
  {f | f.research_capture_id=c.research_capture_id
     ∧ f.fact.fact_id=current_fact_id_o(f.fact.subject_id)}
```

Retries and `existing_exact` results reuse the original accepted identity and are counted once.
Duplicate set members are invalid rather than silently deduplicated. Superseded captures remain
historically addressable, but Session/Dispatch summary counts include only current capture heads.
A `ResearchRecord` for a named capture exposes that immutable capture, its derived currentness and
the current fact head of each subject local to that exact capture.

The following never enter any result or count:

- incomplete/unverified command groups or rejected proposals;
- raw artifact bytes, decoded/transcoded bodies or operational log content;
- inferred Session–Dispatch membership, text-similarity joins or unlinked legacy captures;
- current mutable external Dispatch state or a reorderable legacy row locator;
- facts from another capture/Dispatch, dangling edges and non-head fact revisions; and
- delivery-only probe lineage as evidence of access, consultation or claim support.

### Check and Adjudication Precedence

For a [ReferenceCheck](domain.md#referencecheck), latest applies only inside its explicit
same-subject predecessor chain:

```text
check_subject =
  (check_kind,reference_use_id,relation_id|null,checked_by,method_ref)

current_checks_o =
  {c | type(c)=ReferenceCheck
     ∧ c.fact.fact_id=current_fact_id_o(c.fact.subject_id)}

check_target = (check_kind,reference_use_id,relation_id|null)
check_disagreement_o(check_target) =
  |{result(c) | c∈current_checks_o ∧ target(c)=check_target}| > 1
```

Independent checker/method subjects coexist. The projection groups their current `pass | fail |
indeterminate` results and derives disagreement when distinct current values exist; append order
never breaks a tie. No generic `verified` boolean or verification badge is emitted in L0 because
the three Query intents pin no named aggregation policy.

Disposition and assessment precedence follows the explicit aggregate maps in
[states.md](states.md#disposition-read-projections):

```text
disposition_head_o(TargetRef,policy_ref) = explicit disposition-chain head
assessment_head_o(TargetRef,actor_ref,method_ref,policy_ref) =
  explicit assessment-chain head
```

The output preserves every current policy/assessor head and disagreement. It never synthesizes one
`current_disposition` or `current_assessment`. Counts such as open problems or eligible
formalizations are maps keyed by `policy_ref`, never unqualified scalar verdicts.

### External Snapshot and Hash Rules

The Session binder pins the verified accepted-prefix/grouping manifest. The Dispatch binder pins
exactly one [DispatchAuthoritySnapshotRef](domain.md#dispatchauthoritysnapshotref). The Research
binder pins the named [ResearchCapture](domain.md#researchcapture) identity/event/digest plus that
capture's exact Dispatch snapshot. Snapshot content is resolved and digest-verified before the
pure fold; replay never fetches it.

For `aci_managed`, every required snapshot authority field participates in equality. For
`legacy_ledger`, equality/hash includes `kind + ledger_row_identity + row_digest` and excludes only
`non_authoritative_locator.row_index`. Current mutable Dispatch content is neither returned nor
used as display context.

```text
snapshot_digest =
  H_ACI(canonical({pinned_input_manifest,pinned_input_digests}))

projection_hash =
  H_ACI(canonical({
    schema_ref,
    identity,
    effective_as_of,
    pinned_input_manifest,
    pinned_input_digests,
    value
  }))

same(accepted_prefix,pinned_input_manifest,pinned_input_digests)
  ⇒ same(value,projection_hash,effective_as_of)
```

### Authorization, Errors and Pagination

The host read boundary authorizes the exact Session, Dispatch or Research identity before invoking
the reducer. Errors are exactly the closed `QueryError` union in
[interfaces.md](interfaces.md#query-authorization-and-errors):
`SCHEMA_UNSUPPORTED`, `UNKNOWN_FIELD`, `AUTHENTICATION_REQUIRED`, `AUTHORIZATION_DENIED`,
`NOT_FOUND`, `PINNED_INPUT_INVALID`, or `READ_INTEGRITY_FAILURE`, with its specified retryability.
Owner-specific error codes cannot cross the boundary.

There is no pagination/filter surface in L0. Each closed Query intent returns one aggregate with
complete canonical nested sets at one boundary. A future page/cursor contract requires a registered
spec revision that binds cursor, projection hash and collection order; implementations cannot add
offset/page parameters to these schemas.

---

## SessionRecord

**Type:** Query (read-only)  
**Actor:** Authenticated internal principal authorized for the named Session.

### Input

| Field | Type | Required | Description |
|---|---|---:|---|
| `schema_ref` | constant `apt.session-record-query@1` | yes | Closed [SessionQueryIntent](interfaces.md#query-request-and-result) discriminator. |
| `session_id` | [Session](domain.md#session).`session_id` | yes | Exact Session identity; names cannot resolve identity. |
| `requested_o` | inclusive ACI journal offset | yes | Requested replay boundary. |

### Binder Manifest

`SessionPinnedInputManifest` is exactly the accepted-prefix manifest defined by
[ProvenanceQueryPort](interfaces.md#query-request-and-result):

| Bound field | Required equality |
|---|---|
| `kind` | `session_accepted_prefix` |
| `accepted_prefix.requested_o` | `intent.requested_o` |
| `accepted_prefix.effective_as_of` | common `effective_as_of(intent.requested_o)` |
| `accepted_prefix.grouping_profile_ref` | exact verified ACI receipt/read-grouping profile |
| `accepted_prefix.verified_grouping_manifest_digest` | `H_ACI`-verified digest of the accepted grouping manifest |
| `pinned_input_digests.accepted_prefix_grouping` | `H_ACI(canonical(accepted_prefix))` |

### Filters

None. Superseded Sessions are addressable by ID; `is_current_for_origin` is derived at the requested
boundary. Dispatch/capture children are filtered only by authoritative links and current-head
formulas below.

### Output

The value inside `QueryResult<SessionRecord,...>` has this closed shape:

| Field | Type | Source | Description |
|---|---|---|---|
| `session_id` | opaque ID | [Session](domain.md#session).`session_id` | Exact requested identity. |
| `started_at` | timestamp | [Session](domain.md#session).`started_at` | Immutable owner-stamped start time. |
| `initial_name` | string | [Session](domain.md#session).`initial_name` | Immutable L0 name; there is no rename projection. |
| `origin_kind`, `origin_ref` | host tuple | [Session](domain.md#session).`origin_kind`, `origin_ref` | Exact coarse execution context. |
| `is_current_for_origin` | boolean | [Session context binding](states.md#session-context-binding) | Whether this Session is the tuple head at `effective_as_of`. |
| `dispatches` | canonical set of link summaries | [SessionDispatchLink](domain.md#sessiondispatchlink) | Exact linked Dispatch IDs/link IDs/times/snapshot refs; no inferred reverse link. |
| `dispatch_count` | integer | derived from `dispatches` | `|distinct(dispatches.dispatch_id)|`. |
| `research_expected_count` | integer | [ResearchCapture](domain.md#researchcapture) current heads | One per current `(dispatch_id,expected_contribution_id)` chain under linked Dispatches. |
| `research_returned_count` | integer | [CaptureStatus](domain.md#capturestatus) | Current captures with status `captured | partial`. |
| `research_missing_count` | integer | [CaptureStatus](domain.md#capturestatus) | Current captures with status `missing`. |
| `answer_count` | integer | [ResearchAnswer](domain.md#researchanswer) current fact heads | Current answers attached to current captures only. |
| `open_problem_count_by_policy` | canonical map | [ResearchProblem](domain.md#researchproblem) disposition heads | Per policy, current problems whose disposition is `observed | validated`; absent policy head is not counted or guessed. |
| `eligible_formalization_count_by_policy` | canonical map | [FormalizationCandidate](domain.md#formalizationcandidate) disposition heads | Per policy, current `candidate | reviewed`, excluding `rejected`. |

The wrapper also returns `schema_ref`, `requested_o`, `effective_as_of`, exact
`pinned_input_manifest`, exact `pinned_input_digests`, `snapshot_digest`, and `projection_hash`.

### Formulas

```text
D = distinct {
  link.dispatch_id |
  accepted(link)≤effective_as_of
  ∧ link.session_id=session_id
}

C = ⋃{visible_current_captures_effective(d) | d∈D}
F = ⋃{visible_current_facts_effective(c) | c∈C}

research_expected_count = |C|
research_returned_count = |{c∈C | c.capture_status∈{captured,partial}}|
research_missing_count = |{c∈C | c.capture_status=missing}|
answer_count =
  |{a∈F | type(a)=ResearchAnswer}|

Problems = {f∈F | type(f)=ResearchProblem}
ProblemPolicies =
  canonical_sort({
    p | ∃t∈Problems: disposition_head_effective(t,p) exists
  })
open_problem_count_by_policy =
  canonical_map([
    p -> |{t∈Problems |
            disposition_head_effective(t,p).disposition∈{observed,validated}}|
    for p in ProblemPolicies
  ])

Formalizations = {f∈F | type(f)=FormalizationCandidate}
FormalizationPolicies =
  canonical_sort({
    p | ∃t∈Formalizations: disposition_head_effective(t,p) exists
  })
eligible_formalization_count_by_policy =
  canonical_map([
    p -> |{t∈Formalizations |
            disposition_head_effective(t,p).disposition∈{candidate,reviewed}}|
    for p in FormalizationPolicies
  ])
```

A policy absent from the current policy-head universe creates no map key and contributes no count.

### Reads From

| Entity/projection | Relationship | Fields Used |
|---|---|---|
| [Session](domain.md#session) | queries | Identity, immutable name/time and origin tuple. |
| [SessionDispatchLink](domain.md#sessiondispatchlink) | queries | Authoritative Session–Dispatch membership. |
| [ResearchCapture](domain.md#researchcapture) | queries | Current chain heads and statuses. |
| [ResearchAnswer](domain.md#researchanswer) | queries | Current answer fact subjects for counts. |
| [ResearchProblem](domain.md#researchproblem) | queries | Policy-keyed open-problem counts. |
| [FormalizationCandidate](domain.md#formalizationcandidate) | queries | Policy-keyed eligible counts. |

---

## DispatchScopeProjection

**Type:** Query (read-only)  
**Actor:** Authenticated internal principal authorized for the named Dispatch and pinned scope.

### Input

| Field | Type | Required | Description |
|---|---|---:|---|
| `schema_ref` | constant `apt.dispatch-scope-query@1` | yes | Closed [DispatchQueryIntent](interfaces.md#query-request-and-result) discriminator. |
| `dispatch_id` | external Dispatch ID | yes | Exact external identity. |
| `requested_o` | inclusive ACI journal offset | yes | Requested replay boundary. |

The caller cannot provide a snapshot. The binder resolves the sole exact snapshot already pinned by
the authoritative link/capture evidence.

### Binder Manifest

| Bound field | Required equality |
|---|---|
| `kind` | `dispatch_snapshot` |
| `dispatch_snapshot_ref` | exact verified [DispatchAuthoritySnapshotRef](domain.md#dispatchauthoritysnapshotref) for `intent.dispatch_id` |
| `pinned_input_digests.dispatch_snapshot` | `H_ACI(canonical(dispatch_snapshot_ref))` |
| `effective_as_of` | common verified group boundary `≤ intent.requested_o` |

A mismatched kind/Dispatch identity/digest is `PINNED_INPUT_INVALID`. Two contradictory exact links
are `READ_INTEGRITY_FAILURE`; the query does not pick the latest.

### Filters

None. Membership requires an accepted [SessionDispatchLink](domain.md#sessiondispatchlink) with the
same Dispatch and snapshot authority. Current captures are selected independently per
`expected_contribution_id`.

### Output

The value inside `QueryResult<DispatchScopeProjection,...>` has this closed shape:

| Field | Type | Source | Description |
|---|---|---|---|
| `dispatch_id` | external ID | pinned [DispatchAuthoritySnapshotRef](domain.md#dispatchauthoritysnapshotref) | Exact requested identity. |
| `dispatch_snapshot_ref` | closed authority union | bound manifest | Exact authority used by the projection. |
| `session_links` | canonical set | [SessionDispatchLink](domain.md#sessiondispatchlink) | Exact linked Session/link summaries; normally one, never inferred. |
| `declared_scope` | closed scope summary | pinned Dispatch canonical projection | Requested reference identifiers and declared question/problem scope only; excludes full prompt/body. |
| `current_capture_summaries` | canonical set | [ResearchCapture](domain.md#researchcapture) | Capture ID, contribution ID, producer, status, digest and currentness for each chain head. |
| `research_expected_count` | integer | current capture summaries | Number of current contribution chains. |
| `research_returned_count` | integer | [CaptureStatus](domain.md#capturestatus) | Current `captured | partial` captures. |
| `research_missing_count` | integer | [CaptureStatus](domain.md#capturestatus) | Current `missing` captures. |
| `answer_count` | integer | [ResearchAnswer](domain.md#researchanswer) | Current answer subjects on current captures. |
| `reference_use_count_by_kind` | canonical map | [ResearchReferenceUse](domain.md#researchreferenceuse) | Current uses grouped by `mentioned | cited | claimed_consulted`; does not assert access. |
| `reference_check_summary` | canonical map | [ReferenceCheck](domain.md#referencecheck) | Current independent checks counted by kind/result and disagreement grouped by exact `(kind,use,relation?)` target; no generic verified count. |
| `open_problem_count_by_policy` | canonical map | [ResearchProblem](domain.md#researchproblem) | Per-policy `observed | validated` current problems. |
| `eligible_formalization_count_by_policy` | canonical map | [FormalizationCandidate](domain.md#formalizationcandidate) | Per-policy `candidate | reviewed`, excluding `rejected`. |

### Formulas

```text
C = visible_current_captures_effective(dispatch_id)
F = ⋃{visible_current_facts_effective(c) | c∈C}

research_expected_count = |C|
research_returned_count = |{c∈C | status(c)∈{captured,partial}}|
research_missing_count = |{c∈C | status(c)=missing}|
answer_count = |{f∈F | type(f)=ResearchAnswer}|

reference_use_count_by_kind[k] =
  |{f∈F | type(f)=ResearchReferenceUse ∧ f.use_kind=k}|

reference_check_summary[k][r] =
  |{f∈F | type(f)=ReferenceCheck ∧ f.check_kind=k ∧ f.result=r}|

reference_check_summary.disagreement_targets =
  canonical_sort({
    (f.check_kind,f.reference_use_id,f.relation_id|null) |
    f∈F ∧ type(f)=ReferenceCheck
    ∧ |current_results(f.check_kind,f.reference_use_id,f.relation_id|null)|>1
  })

Problems = {f∈F | type(f)=ResearchProblem}
ProblemPolicies =
  canonical_sort({
    p | ∃t∈Problems: disposition_head_effective(t,p) exists
  })
open_problem_count_by_policy =
  canonical_map([
    p -> |{t∈Problems |
            disposition_head_effective(t,p).disposition∈{observed,validated}}|
    for p in ProblemPolicies
  ])

Formalizations = {f∈F | type(f)=FormalizationCandidate}
FormalizationPolicies =
  canonical_sort({
    p | ∃t∈Formalizations: disposition_head_effective(t,p) exists
  })
eligible_formalization_count_by_policy =
  canonical_map([
    p -> |{t∈Formalizations |
            disposition_head_effective(t,p).disposition∈{candidate,reviewed}}|
    for p in FormalizationPolicies
  ])
```

A policy absent from the current policy-head universe creates no map key and contributes no count.

### Reads From

| Entity/projection | Relationship | Fields Used |
|---|---|---|
| [DispatchAuthoritySnapshotRef](domain.md#dispatchauthoritysnapshotref) | queries | Exact pinned authority and canonical declared scope. |
| [SessionDispatchLink](domain.md#sessiondispatchlink) | queries | Authoritative reverse membership projection. |
| [ResearchCapture](domain.md#researchcapture) | queries | Current contribution heads/status summaries. |
| [ResearchAnswer](domain.md#researchanswer) | queries | Current answer count. |
| [ResearchReferenceUse](domain.md#researchreferenceuse) | queries | Typed use counts without access inference. |
| [ReferenceCheck](domain.md#referencecheck) | queries | Independent current check sets/disagreement. |
| [ResearchProblem](domain.md#researchproblem) | queries | Per-policy open-problem counts. |
| [FormalizationCandidate](domain.md#formalizationcandidate) | queries | Per-policy eligible counts. |

---

## ResearchRecord

**Type:** Query (read-only)  
**Actor:** Authenticated internal research author/reviewer authorized for the named capture.

### Input

| Field | Type | Required | Description |
|---|---|---:|---|
| `schema_ref` | constant `apt.research-record-query@1` | yes | Closed [ResearchQueryIntent](interfaces.md#query-request-and-result) discriminator. |
| `research_capture_id` | [ResearchCapture](domain.md#researchcapture).`research_capture_id` | yes | Stable immutable capture identity. |
| `requested_o` | inclusive ACI journal offset | yes | Requested replay boundary. |

### Binder Manifest

| Bound field | Required equality |
|---|---|
| `kind` | `research_capture_and_dispatch_snapshot` |
| `research_capture.research_capture_id` | `intent.research_capture_id` |
| `research_capture.capture_event_ref` | exact accepted [ResearchCaptureAppended](events.md#researchcaptureappended) event |
| `research_capture.capture_digest` | ACI-verified [ResearchCapture](domain.md#researchcapture).`capture_digest` |
| `dispatch_snapshot_ref` | exact snapshot embedded by the named capture |
| `pinned_input_digests.research_capture` | `H_ACI(canonical(research_capture))` |
| `pinned_input_digests.dispatch_snapshot` | `H_ACI(canonical(dispatch_snapshot_ref))` |

The capture event must be accepted no later than `effective_as_of`. A missing capture is
`NOT_FOUND`; event/capture/snapshot identity or digest disagreement is `PINNED_INPUT_INVALID`.

### Filters

None. The query returns the exact named capture even when it is now superseded. Child Entity
collections include only current fact heads local to that capture. Disposition/assessment events
are reduced into their explicit independent aggregate-head maps.

### Output

The value inside `QueryResult<ResearchRecord,...>` has this closed shape:

| Field | Type | Source | Description |
|---|---|---|---|
| `research_capture_id` | opaque ID | [ResearchCapture](domain.md#researchcapture).`research_capture_id` | Exact requested capture. |
| `dispatch_id`, `expected_contribution_id` | opaque IDs | [ResearchCapture](domain.md#researchcapture) | Stable owning chain. |
| `capture_status` | [CaptureStatus](domain.md#capturestatus) | [ResearchCapture](domain.md#researchcapture).`capture_status` | Immutable `captured | partial | missing`. |
| `currentness` | `current | superseded` | [capture currentness](states.md#research-capture-currentness) | Derived at `effective_as_of`; never persisted as status. |
| `supersedes_capture_id` | capture ID or null | [ResearchCapture](domain.md#researchcapture).`supersedes_capture_id` | Immutable predecessor. |
| `captured_at`, `producer_ref`, `origin_refs` | immutable lineage | [ResearchCapture](domain.md#researchcapture) | Owner-stamped capture provenance. |
| `raw_return_ref` | artifact ref or null | [ResearchCapture](domain.md#researchcapture).`raw_return` | Governed artifact reference only; never body/excerpt bytes. |
| `partial_reason`, `failure_reason`, `failure_evidence_ref` | closed status evidence | [ResearchCapture](domain.md#researchcapture) | Exact canonical-null/status slots. |
| `capture_digest`, `dispatch_snapshot_ref` | verified evidence | [ResearchCapture](domain.md#researchcapture) | Pinned immutable capture/scope evidence. |
| `synthesis_inputs` | semantic ordered list | [ResearchCapture](domain.md#researchcapture).`synthesizes` | Original pins plus derived `input_now_superseded`; composition never rewrites. |
| `questions` | canonical set | [ResearchQuestion](domain.md#researchquestion) | Current question fact head per subject. |
| `answers` | canonical set | [ResearchAnswer](domain.md#researchanswer) | IDs, question IDs and extraction selectors; answer bytes stay in artifact. |
| `reference_uses` | canonical set | [ResearchReferenceUse](domain.md#researchreferenceuse) | Current typed attributed uses and optional probe origin. |
| `reference_claim_relations` | canonical set | [ResearchReferenceClaimRelation](domain.md#researchreferenceclaimrelation) | Current explicit typed use-to-claim edges. |
| `reference_checks` | canonical set | [ReferenceCheck](domain.md#referencecheck) | Every independent current check subject; no generic verified field. |
| `reference_check_summary` | canonical map | derived from `reference_checks` | Check kind/result counts and disagreement grouped by exact `(kind,use,relation?)` target. |
| `problems` | canonical set | [ResearchProblem](domain.md#researchproblem) | Current problem facts with policy disposition and assessor maps. |
| `claims` | canonical set | [ResearchClaimExtraction](domain.md#researchclaimextraction) | Current local propositions with policy disposition and assessor maps. |
| `formalizations` | canonical set | [FormalizationCandidate](domain.md#formalizationcandidate) | Current notation/legend/reading/scope and evidence refs with policy/assessor maps. |
| `probe_delivery_origins` | canonical set | [ReferenceProbeLineageAppended](events.md#referenceprobelineageappended) | Current delivery heads referenced by this capture's current reference-use facts; kept distinct from proven use/access/support. |

### Formulas

```text
C = exact accepted capture(research_capture_id)
F = visible_current_facts_effective(C)

currentness =
  current     if current_capture_effective(chain(C))=C.research_capture_id
  superseded  otherwise

collection[T] =
  canonical_sort({f∈F | type(f)=T}, stable_subject_id)

resolved_input(pin) =
  exact_accepted_capture(pin.research_capture_id)

valid_pin(pin) =
  resolved_input(pin).capture_digest = pin.capture_digest

require ∀pin∈C.synthesizes: valid_pin(pin)

synthesis_inputs =
  [
    pin + {
      input_now_superseded =
        current_capture_effective(chain(resolved_input(pin)))
          ≠ pin.research_capture_id
    }
    for pin in C.synthesizes in original semantic order
  ]

reference_check_summary[k][r] =
  |{f∈collection[ReferenceCheck] | f.check_kind=k ∧ f.result=r}|

reference_check_summary.disagreement_targets =
  canonical_sort({
    (f.check_kind,f.reference_use_id,f.relation_id|null) |
    f∈collection[ReferenceCheck]
    ∧ |current_results(f.check_kind,f.reference_use_id,f.relation_id|null)|>1
  })

ProbeKeys =
  canonical_sort({
    H_ACI(canonical({
      u.probe_recommendation_ref.probe_id,
      u.probe_recommendation_ref.bundle_digest,
      u.probe_recommendation_ref.recommendation_id
    })) |
    u∈collection[ResearchReferenceUse]
    ∧ u.probe_recommendation_ref≠null
  })

delivery_head_effective(k) =
  unique head produced by accepted ReferenceProbeLineageAppended events
  with delivery_subject_key=k and accepted group last_offset≤effective_as_of

probe_delivery_origins =
  canonical_sort(
    {delivery_head_effective(k) | k∈ProbeKeys},
    delivery_subject_key
  )
```

Every synthesis pin must resolve and satisfy `valid_pin(pin)=true`; a missing input or digest
mismatch is `READ_INTEGRITY_FAILURE`. Every `ProbeKeys` member must resolve to one current delivery
head at the boundary; missing, forked or invalid predecessor lineage is
`READ_INTEGRITY_FAILURE`. Thus delivery origins are restricted to the exact capture through its
current reference-use facts, deduplicated/current by the owner-derived composite key and canonically
ordered.

For each problem, claim or formalization target `t`, the query attaches:

```text
adjudication_heads_by_policy[t] =
  canonical current disposition-chain heads keyed by policy_ref

assessment_heads_by[t] =
  canonical current assessment-chain heads keyed by
  (actor_ref,method_ref,policy_ref)

assessment_disagreement[t] =
  |distinct(assessment_heads_by[t].assessment)| > 1
```

No event arrival time supplies precedence across independent keys.

### Reads From

| Entity/projection | Relationship | Fields Used |
|---|---|---|
| [ResearchCapture](domain.md#researchcapture) | queries | Exact immutable capture, status, lineage, artifact ref and snapshot. |
| [ResearchCapture](domain.md#researchcapture).`synthesizes` | queries | Immutable ordered pins and query-time supersession label. |
| [ResearchQuestion](domain.md#researchquestion) | queries | Current question fact subjects. |
| [ResearchAnswer](domain.md#researchanswer) | queries | Current answer/extraction fact subjects. |
| [ResearchReferenceUse](domain.md#researchreferenceuse) | queries | Current typed uses. |
| [ResearchReferenceClaimRelation](domain.md#researchreferenceclaimrelation) | queries | Current explicit epistemic edges. |
| [ReferenceCheck](domain.md#referencecheck) | queries | Current independent check chains and disagreement. |
| [ResearchProblem](domain.md#researchproblem) | queries | Current problems plus policy/assessor heads. |
| [ResearchClaimExtraction](domain.md#researchclaimextraction) | queries | Current claims plus policy/assessor heads. |
| [FormalizationCandidate](domain.md#formalizationcandidate) | queries | Current formalizations plus policy/assessor heads. |
| [ReferenceProbeLineageAppended](events.md#referenceprobelineageappended) | queries | Accepted delivery origins without access inference. |

## AgentReferenceLineage

**Type:** Query (read-only)
**Contract status:** specified; not implemented.
**Actor:** Authenticated internal operator/reviewer authorized for the requested Dispatch and target
agent identity.

This Query projects the evidence path for references delivered to one owner-resolved agent target.
It reads ACI target-delivery/effective-input authority, host observation evidence and APT attributed
research facts without copying or re-owning any of them.

### Input

| Field | Type | Required | Description |
|---|---|---:|---|
| `schema_ref` | constant `apt.agent-reference-lineage-query@1` | yes | Closed Query discriminator. |
| `dispatch_id` | opaque owner ID | yes | Exact Dispatch scope; never inferred from the selector. |
| `target` | closed `attempt \| seat \| agent_instance` selector | yes | Exactly one of `{kind=attempt,attempt_id}`, `{kind=seat,seat_id}`, or `{kind=agent_instance,agent_instance_id}`. |
| `requested_o` | inclusive ACI journal offset | yes | Requested replay boundary. |

The caller supplies an opaque selector, not its relationships. The ACI owner resolves it to a
canonical target set of `(dispatch_id, group_id, seat_id, attempt_id, agent_instance_id)` tuples.
Unknown, foreign or conflicting/unverifiable resolution fails closed. A seat or agent-instance
selector may legitimately resolve to multiple historical/current Attempt tuples; canonical
cardinality greater than one is not ambiguity. Persona/display name, locator, path, recommendation
text, timestamps and model labels are forbidden selectors and join keys.

### Binder Manifest

The owner-created `AgentReferencePinnedInputManifest` is closed:

```text
closed {
  kind="agent_reference_lineage",
  apt_accepted_prefix: {
    requested_o,
    effective_as_of,
    grouping_profile_ref,
    verified_grouping_manifest_digest,
    complete_groups
  },
  target_resolution: closed {
    owner_namespace="agents-communication-infra",
    owner_contract_id="agents-communication-infra.Attempt",
    owner_contract_version=expected_aci_attempt_contract_version,
    scope: {dispatch_id,target_selector_digest},
    accepted_through,
    owner_manifest_digest,
    members: canonical set<{
      dispatch_id,group_id,seat_id,attempt_id,agent_instance_id,
      accepted_attempt_read_group_id,
      accepted_attempt_event_ref: {event_id,offset,payload_digest},
      owner_evidence_digest
    }>
  },
  producer_resolution: closed {
    owner_namespace="host",
    owner_contract_id="host.AgentActivationBinding",
    owner_contract_version=expected_host_agent_activation_binding_contract_version,
    scope: {
      dispatch_id,
      target_resolution_digest,
      aci_delivery_snapshot_digest,
      probe_scout_bindings_digest,
      capture_producer_selector_digest
    },
    accepted_through,
    owner_manifest_digest,
    members: canonical set<{
      research_capture_id,
      producer_ref_digest,
      dispatch_id,group_id,seat_id,attempt_id,agent_instance_id,activation_id,
      accepted_attempt_read_group_id,
      accepted_attempt_event_ref: {event_id,offset,payload_digest},
      owner_evidence_digest
    }>
  },
  aci_delivery_snapshot: closed {
    owner_namespace="agents-communication-infra",
    owner_contract_id="agents-communication-infra.AgentReferenceDelivery",
    owner_contract_version=expected_aci_agent_reference_delivery_contract_version,
    scope: {dispatch_id,target_resolution_digest},
    accepted_through,
    owner_manifest_digest,
    members: canonical set<{
      agent_reference_delivery_id,
      accepted_read_group_id,
      accepted_delivery_event_ref: {event_id,offset,payload_digest},
      dispatch_id,
      scout_run_id,
      source_bundle_committed_event_ref: {
        event_id,offset,payload_digest
      },
      source_bundle_delivered_event_ref: {event_id,offset,payload_digest},
      bundle_artifact_id,
      bundle_digest,
      recommendation_ids,
      target_group_id,
      target_seat_id,
      target_attempt_id,
      target_agent_instance_id,
      idempotency_key,
      effective_input_artifact_id,
      effective_input_manifest_hash,
      effective_input_entry_ordinal,
      effective_input_entry: {
        entry_type="reference_bundle",
        artifact_ref,
        content_hash,
        agent_reference_delivery_id,
        visibility_policy_ref
      }
    }>
  },
  probe_scout_bindings: closed {
    owner_namespace="agent-provenance-telemetry",
    owner_contract_id="agent-provenance-telemetry.ProbeRecommendationRef",
    owner_contract_version=expected_apt_probe_recommendation_ref_contract_version,
    scope: {dispatch_id,aci_delivery_snapshot_digest},
    accepted_through,
    owner_manifest_digest,
    members: canonical set<{
      probe_id,scout_run_id,bundle_artifact_id,bundle_digest,
      recommendation_ids,accepted_commit_read_group_id,
      commit_event_ref: {event_id,offset,payload_digest}
    }>
  },
  apt_fact_heads: canonical set<
    {
      fact_type,fact_id,subject_id,research_capture_id,
      accepted_read_group_id,
      accepted_event_ref: {event_id,offset,payload_digest},
      closed_value
    }
  >,
  host_observation_projection:
    closed {
      status="unavailable",
      owner_namespace="host",
      owner_contract_id="host.SourceObservation",
      owner_contract_version=expected_host_source_observation_contract_version,
      scope: {
        dispatch_id,target_resolution_digest,aci_delivery_snapshot_digest
      },
      required_contract_digest
    }
    |
    closed {
      status="available",
      owner_namespace="host",
      owner_contract_id="host.SourceObservation",
      owner_contract_version=expected_host_source_observation_contract_version,
      scope: {
        dispatch_id,target_resolution_digest,aci_delivery_snapshot_digest
      },
      accepted_through,
      owner_manifest_digest,
      observations: canonical set<{
        source_observation_id,
        dispatch_id,
        target_binding: {
          group_id,seat_id,attempt_id,agent_instance_id,owner_evidence_digest
        },
        reference_origin_ref: {
          agent_reference_delivery_id,recommendation_id,owner_evidence_digest
        },
        tool_name,source_kind,coverage,purpose,accepted_offset,evidence_digest
      }>
    }
}
```

`target_resolution.members` comes from ACI Attempt/capability ownership. Every
`aci_delivery_snapshot.members` member
must resolve to an accepted
[`AgentReferenceDelivery`](../../agents-communication-infra/specs/domain.md#agentreferencedelivery)
whose target tuple is in `target_resolution.members`, and to the exact
[`EffectiveInputEntry.reference_bundle`](../../agents-communication-infra/specs/domain.md#effectiveinputentry)
accepted in its finalized manifest. Each target-resolution member carries the exact accepted
Attempt event and its verified atomic group:

```text
accepted_attempt_event =
  exact_event(apt_accepted_prefix.complete_groups,
              target.accepted_attempt_read_group_id,
              target.accepted_attempt_event_ref.event_id)

accepted_attempt_event.event_type = "attempt.requested"
accepted_attempt_event.journal_offset = target.accepted_attempt_event_ref.offset
H_ACI(canonical(accepted_attempt_event.payload)) =
  target.accepted_attempt_event_ref.payload_digest
read_group(accepted_attempt_event) = target.accepted_attempt_read_group_id
accepted_attempt_event.attempt_id = target.attempt_id
accepted_attempt_event.dispatch_id = target.dispatch_id
accepted_attempt_event.group_id = target.group_id
accepted_attempt_event.seat_id = target.seat_id
accepted_attempt_event.agent_instance_id = target.agent_instance_id
target.accepted_attempt_event_ref.offset <=
  target_resolution.accepted_through <= effective_as_of
```

`producer_resolution` is the separately pinned host-owner resolution of the stored seat producer
references that may participate in this Query. Its selector is derived before the owner call from
the verified current APT fact heads, never supplied by the caller:

```text
capture_producer_selector =
  canonical set<{
    research_capture_id,
    producer_ref_digest=H_ACI(canonical(capture.producer_ref))
  }> for each accepted current capture that:
    capture.dispatch_id = intent.dispatch_id
    and capture.producer_ref.kind = seat
    and capture.producer_ref.(group_id,seat_id,attempt_id) equals
        one target_resolution member's (group_id,seat_id,attempt_id)
    and owns a current ResearchReferenceUse head u in apt_fact_heads
    and u's exact verified probe/Scout/bundle/recommendation identity is present in
        probe_scout_bindings and one aci_delivery_snapshot member for that same target

producer_resolution.scope = {
  dispatch_id=intent.dispatch_id,
  target_resolution_digest=pinned_input_digests.target_resolution,
  aci_delivery_snapshot_digest=pinned_input_digests.aci_delivery_snapshot,
  probe_scout_bindings_digest=pinned_input_digests.probe_scout_bindings,
  capture_producer_selector_digest=
    H_ACI(canonical(capture_producer_selector))
}

for every p in producer_resolution.members:
  exactly_one selector in capture_producer_selector:
    selector.research_capture_id = p.research_capture_id
    and selector.producer_ref_digest = p.producer_ref_digest
  capture = accepted_current_capture(
    apt_accepted_prefix.complete_groups,
    p.research_capture_id)
  p.producer_ref_digest = H_ACI(canonical(capture.producer_ref))
  capture.dispatch_id = p.dispatch_id = intent.dispatch_id
  capture.producer_ref =
    {kind=seat,group_id=p.group_id,seat_id=p.seat_id,
     attempt_id=p.attempt_id,activation_id=p.activation_id}
  p.(dispatch_id,group_id,seat_id,attempt_id,agent_instance_id) in
    target_resolution.members
  producer_attempt_event =
    exact_event(apt_accepted_prefix.complete_groups,
                p.accepted_attempt_read_group_id,
                p.accepted_attempt_event_ref.event_id)
  producer_attempt_event.event_type = "attempt.requested"
  producer_attempt_event.journal_offset = p.accepted_attempt_event_ref.offset
  H_ACI(canonical(producer_attempt_event.payload)) =
    p.accepted_attempt_event_ref.payload_digest
  read_group(producer_attempt_event) = p.accepted_attempt_read_group_id
  producer_attempt_event.(dispatch_id,group_id,seat_id,attempt_id,agent_instance_id) =
    p.(dispatch_id,group_id,seat_id,attempt_id,agent_instance_id)
  p.accepted_attempt_event_ref.offset <=
    producer_resolution.accepted_through <= effective_as_of
```

The `host.AgentActivationBinding` owner contract attests that `activation_id` is a child of the
same accepted Attempt tuple. The wrapper's complete member set must equal the
`capture_producer_selector` cardinality exactly: one member per selector and no member outside it.
Missing, extra, duplicate, future, cross-Dispatch, cross-target, ambiguous or digest-mismatched
resolution fails closed. This owner wrapper is specified here as a required Query source contract;
it is not implemented by the current pilot.

Any absent or unequal event/group evidence fails closed; an ID-only or latest-state lookup is not
authority. Every commit, delivery, binding, fact and observation used in the result has
`accepted_offset<=effective_as_of`; `complete_groups` carries the exact accepted event values needed
by the fold, not only event IDs.

The current Stage-G host ingestion pilot records `dispatch_id`, optional `agent_id`, `tool_name`,
`source_kind`, `coverage`, `purpose` and accepted offset, but does not provide an
owner-authoritative observation-to-recommendation/delivery plus Attempt/seat binding. Therefore its
`host_observation_projection.status=unavailable`, and this Query returns empty `access_observed`
sets under that runtime. The `available` variant is a required future host-owner contract
extension, specified but not implemented. APT does not mint it. Existing
`exact | metadata_only | opaque` coverage is preserved, and no `action` field is invented.

The binder pins the complete typed union, including the unavailable variant rather than only its
digest field:

```text
host_observation_snapshot_digest =
  H_ACI(canonical(
    HostObservationProjection =
      Unavailable {
        status="unavailable",
        owner_namespace="host",
        owner_contract_id,
        owner_contract_version,
        scope,
        required_contract_digest
      }
      | Available {
          status="available",
          owner_namespace="host",
          owner_contract_id,
          owner_contract_version,
          scope,
          accepted_through,
          owner_manifest_digest,
          observations
        }
  ))

host_observation_projection.status = available
  => host_observation_projection.accepted_through <= effective_as_of

host_observation_projection.scope = {
  dispatch_id=intent.dispatch_id,
  target_resolution_digest=pinned_input_digests.target_resolution,
  aci_delivery_snapshot_digest=pinned_input_digests.aci_delivery_snapshot
}

pinned_input_digests = {
  apt_accepted_prefix: H_ACI(canonical(apt_accepted_prefix)),
  target_resolution: H_ACI(canonical(target_resolution)),
  producer_resolution: H_ACI(canonical(producer_resolution)),
  aci_delivery_snapshot: H_ACI(canonical(aci_delivery_snapshot)),
  probe_scout_bindings: H_ACI(canonical(probe_scout_bindings)),
  apt_fact_heads: H_ACI(canonical(apt_fact_heads)),
  host_observation_projection: host_observation_snapshot_digest
}

owner_manifest_preimage(w) = canonical({
  owner_namespace=w.owner_namespace,
  owner_contract_id=w.owner_contract_id,
  owner_contract_version=w.owner_contract_version,
  scope=w.scope,
  accepted_through=w.accepted_through,
  members=w.members
})

binder_verify_owner_manifest(w) =
  owner_registry.verify(
    w.owner_namespace,
    w.owner_contract_id,
    w.owner_contract_version,
    w.owner_manifest_digest,
    owner_manifest_preimage(w))

bound_verified(w) =
  binder_verify_owner_manifest(w)
  and pinned_input_digests[field_name(w)] = H_ACI(canonical(w))

apt_fact_heads =
  current_fact_heads(
    fold_verified_complete_groups(
      apt_accepted_prefix.complete_groups,
      effective_as_of))

for every f in apt_fact_heads:
  fact_event =
    exact_event(apt_accepted_prefix.complete_groups,
                f.accepted_read_group_id,
                f.accepted_event_ref.event_id)
  fact_event.journal_offset = f.accepted_event_ref.offset
  H_ACI(canonical(fact_event.payload)) = f.accepted_event_ref.payload_digest
  f.accepted_event_ref.offset <= effective_as_of

host_observation_projection.status = available =>
  host_observation_projection.owner_manifest_digest =
    H_HOST(canonical({
      owner_namespace="host",
      owner_contract_id="host.SourceObservation",
      owner_contract_version=
        expected_host_source_observation_contract_version,
      scope=host_observation_projection.scope,
      accepted_through=host_observation_projection.accepted_through,
      observations=host_observation_projection.observations
    }))
```

Before reduction, `ACIAgentReferenceEvidenceReader.verify_reference_bundle_entry` verifies each
delivery member's accepted events/groups, immutable bundle artifact/digest/ordered membership and
exact finalized effective-input entry/manifest. It returns the same member or a typed failure; the
reducer receives no bundle bytes, artifact reader or effective-input resolver.

`target_resolution`, `producer_resolution`, `aci_delivery_snapshot` and
`probe_scout_bindings` are the complete closed
owner-authored/versioned wrappers shown above, not caller collections. The binder verifies each
wrapper's serialized `owner_namespace`, `owner_contract_id`, `owner_contract_version`, `scope`,
`accepted_through` and `owner_manifest_digest`, requires each exact canonical owner namespace and
contract identity shown in the closed shapes, requires `accepted_through<=effective_as_of`, and
requires `members` to equal the owner's complete enumeration for the selector/scope. The binder and
reducer hash the complete wrapper exactly as shown in `pinned_input_digests`, never a bare member
set.
`owner_manifest_digest` hashes `owner_manifest_preimage`, which explicitly excludes the digest
field itself; `pinned_input_digests` then hashes the complete wrapper including the verified owner
digest. The exact owner namespace/contract/version allowlists are the constants in the closed shape;
an unexpected value fails before reduction. Only wrappers marked `bound_verified` by the binder and
echoed byte-for-byte in the bound request reach the pure reducer; the reducer performs no owner
resolution or registry call.
`apt_fact_heads` is derived only by folding
`apt_accepted_prefix.complete_groups`; it is not an independently supplied subset. Any omitted,
extra, future, duplicate or digest-mismatched member fails closed.

For the available host variant, the binder separately verifies the complete H_HOST manifest,
contract version, exact upstream-digest scope and pinned complete-union digest through
`HostSourceObservationEvidencePort.bind_agent_reference_observations`. Its immutable
`observations` set contains only members the selected versioned owner contract certifies as access
observations. The reducer receives that already verified wrapper and performs no host-contract
lookup. The unavailable variant is likewise pinned as its complete closed union value.

For every `(scout_run_id,bundle_artifact_id,bundle_digest,commit_event_ref.event_id)`, the legacy v1
`probe_id` binding resolves to exactly one owner-verified alias or to canonical absence. The binding
must match commit identity, offset, digest and complete recommendation membership. Multiple aliases,
one alias bound to conflicting ScoutRuns/commits, or a forked membership set is
`READ_INTEGRITY_FAILURE`.

Any missing/extra/ambiguous owner evidence, digest disagreement, future delivery/observation,
cross-scope producer member, incomplete ACI atomic group or target mismatch is
`PINNED_INPUT_INVALID` or `READ_INTEGRITY_FAILURE`; the reducer does not repair or infer.

### Filters

The exact `dispatch_id` and owner-resolved `target` are the complete filter. There is no locator,
title, DOI, persona, free-text, page or cursor filter in this version.

### Output

The value inside `QueryResult<AgentReferenceLineage,...>` has this closed shape:

| Field | Type | Source | Description |
|---|---|---|---|
| `dispatch_id` | opaque ID | Query intent + ACI target resolution | Exact authorized scope. |
| `requested_target` | closed selector | Query intent | Echoed selector, not authority. |
| `resolved_targets` | canonical set | ACI Attempt/capability owner | Exact target tuples and owner evidence refs. |
| `reference_lines` | canonical set by `(agent_reference_delivery_id,recommendation_id)` | ACI delivery membership + APT facts + host observations | One evidence-separated row per accepted delivered recommendation. |

Each `reference_line` is:

```text
closed {
  source: {
    scout_run_id,
    probe_id?,
    bundle_artifact_id,
    bundle_digest,
    recommendation_id,
    bundle_committed_event_ref: {
      event_id,offset,payload_digest
    }
  },
  recommended: {
    recommendation_id,
    committed_membership_evidence_ref: {
      commit_event_ref: {event_id,offset,payload_digest},
      bundle_artifact_id,bundle_digest
    }
  },
  delivered_to_attempt: {
    agent_reference_delivery_id,
    target_delivery_event_ref: {event_id,offset,payload_digest},
    dispatch_id,
    target_attempt_id,
    target_seat_id,
    target_agent_instance_id
  },
  in_effective_input: {
    effective_input_artifact_id,
    entry_ordinal,
    manifest_hash,
    artifact_ref,
    content_hash
  },
  access_observed: canonical set<
    {
      source_observation_id,
      coverage: exact|metadata_only|opaque,
      tool_name,
      source_kind,
      purpose,
      owner_contract_version,
      evidence_digest
    }
  >,
  declared_used: canonical set<
    {
      research_capture_id,
      reference_use_id,
      use_kind: mentioned|cited|claimed_consulted,
      producer_ref
    }
  >,
  claim_relation: canonical set<
    {relation_id,reference_use_id,research_claim_id,relation}
  >,
  claim_support_check: canonical set<
    {reference_check_id,relation_id,checked_by,method_ref,result,evidence_ref?}
  >
}
```

Every nested set is duplicate-rejecting and ACI-byte-order sorted by its complete semantic
identity: observations by `source_observation_id`, uses by
`(research_capture_id,reference_use_id)`, relations by `relation_id`, and checks by
`reference_check_id`.
`reference_lines` is likewise duplicate-rejecting and ACI-byte-order sorted by the complete
`(agent_reference_delivery_id,recommendation_id)` pair. The source/commit references come from the
owner-verified accepted `reference_scout.bundle_committed@1` evidence; the target-delivery
reference comes from the distinct accepted `reference_scout.bundle_delivered_to_agent@1` evidence
in `aci_delivery_snapshot`. A caller cannot author or omit their identity, offset or digest fields.

`access_observed` contains only exact host observation IDs explicitly bound by owner evidence to the
resolved target and to this recommendation/delivery lineage. `metadata_only` and `opaque` describe
what the host exposed; they are retained as such and never upgraded to `exact`. An observation
without an owner-authored exact recommendation/delivery relation remains outside that
recommendation line rather than being joined by locator. A `source_observation_id` named by a
ResearchReferenceUse does not, by itself, prove that relation. Each output member's
`owner_contract_version` is copied from the enclosing
`host_observation_projection.owner_contract_version`; observations cannot override it.

`declared_used` contains only current [ResearchReferenceUse](domain.md#researchreferenceuse) heads
whose exact [ProbeRecommendationRef](domain.md#proberecommendationref) resolves to the line's
`(probe_id,bundle_digest,recommendation_id)` and whose containing capture has a valid seat
`producer_ref` accepted with that capture and matching the delivery's Dispatch, Attempt, seat and
owner-resolved group. The reducer establishes the complete owner identity by matching the delivery
to an already binder-verified `target_resolution.members` tuple; it performs no owner lookup.
`ExtractionProvenance.actor_ref` records extraction authorship and cannot replace the capture
producer or owner-resolved target identity. Its
`source_observation_id`, when present, may contribute to `access_observed` only after independent
host verification. Direct reference uses without a probe recommendation do not join by locator.

`claim_relation` contains only current explicit
[ResearchReferenceClaimRelation](domain.md#researchreferenceclaimrelation) heads for a listed use.
`claim_support_check` contains only current [ReferenceCheck](domain.md#referencecheck) heads with
`check_kind=claim_support` and the exact listed `relation_id`. Identity/access checks stay outside
that axis.

### Formulas and Non-Implication Invariants

```text
Targets =
  target_resolution.members
  where bound_verified(target_resolution)
    and target_resolution.scope.dispatch_id = intent.dispatch_id
    and target_resolution.scope.target_selector_digest =
        H_ACI(canonical(intent.target))
    and target_resolution.accepted_through <= effective_as_of

Deliveries =
  {d |
    bound_verified(aci_delivery_snapshot)
    and aci_delivery_snapshot.scope.dispatch_id = intent.dispatch_id
    and aci_delivery_snapshot.scope.target_resolution_digest =
        pinned_input_digests.target_resolution
    and aci_delivery_snapshot.accepted_through <= effective_as_of
    and d in aci_delivery_snapshot.members
    and exists t in Targets:
      target_tuple(d) = target_tuple(t)
      and delivery_event =
        exact_event(apt_accepted_prefix.complete_groups,
                    d.accepted_read_group_id,
                    d.accepted_delivery_event_ref.event_id)
      and delivery_event.event_type =
        "reference_scout.bundle_delivered_to_agent@1"
      and delivery_event.journal_offset =
        d.accepted_delivery_event_ref.offset
      and H_ACI(canonical(delivery_event.payload)) =
        d.accepted_delivery_event_ref.payload_digest
      and delivery_event.payload = exact_delivery_payload(d)
      and delivery_event.dispatch_id = d.dispatch_id
      and delivery_event.group_id = d.target_group_id
      and delivery_event.attempt_id = d.target_attempt_id
      and delivery_event.seat_id = d.target_seat_id
      and delivery_event.agent_instance_id = d.target_agent_instance_id
      and attempt_event =
        exact_event(apt_accepted_prefix.complete_groups,
                    t.accepted_attempt_read_group_id,
                    t.accepted_attempt_event_ref.event_id)
      and attempt_event.event_type = "attempt.requested"
      and attempt_event.journal_offset =
        t.accepted_attempt_event_ref.offset
      and H_ACI(canonical(attempt_event.payload)) =
        t.accepted_attempt_event_ref.payload_digest
      and d.accepted_read_group_id = t.accepted_attempt_read_group_id
      and same_atomic_group(delivery_event,attempt_event)
      and d.accepted_delivery_event_ref.offset <=
          aci_delivery_snapshot.accepted_through
      and t.accepted_attempt_event_ref.offset <=
          target_resolution.accepted_through}

Lines =
  canonical_sort({
    line(d,r) |
      d in aci_delivery_snapshot.members
      and d in Deliveries
      and r in d.recommendation_ids
      and commit_event =
        exact_event(apt_accepted_prefix.complete_groups,
                    d.source_bundle_committed_event_ref)
      and commit_event.event_type = "reference_scout.bundle_committed@1"
      and commit_event.journal_offset =
        d.source_bundle_committed_event_ref.offset
      and H_ACI(canonical(commit_event.payload)) =
        d.source_bundle_committed_event_ref.payload_digest
      and commit_event.payload.scout_run_id = d.scout_run_id
      and commit_event.payload.bundle_artifact_id = d.bundle_artifact_id
      and commit_event.payload.bundle_digest = d.bundle_digest
      and commit_event.payload.recommendation_ids = d.recommendation_ids
      and lifecycle_delivered_event =
        exact_event(apt_accepted_prefix.complete_groups,
                    d.source_bundle_delivered_event_ref)
      and lifecycle_delivered_event.event_type =
        "reference_scout.bundle_delivered@1"
      and lifecycle_delivered_event.journal_offset =
        d.source_bundle_delivered_event_ref.offset
      and H_ACI(canonical(lifecycle_delivered_event.payload)) =
        d.source_bundle_delivered_event_ref.payload_digest
      and lifecycle_delivered_event.payload.scout_run_id = d.scout_run_id
      and lifecycle_delivered_event.payload.bundle_artifact_id =
        d.bundle_artifact_id
      and lifecycle_delivered_event.payload.bundle_digest = d.bundle_digest
      and d.source_bundle_committed_event_ref.offset <
          d.source_bundle_delivered_event_ref.offset <
          d.accepted_delivery_event_ref.offset
      and d.effective_input_entry.entry_type = "reference_bundle"
      and d.effective_input_entry.artifact_ref = d.bundle_artifact_id
      and d.effective_input_entry.content_hash = d.bundle_digest
      and d.effective_input_entry.agent_reference_delivery_id =
        d.agent_reference_delivery_id
      and line.source.bundle_committed_event_ref =
          d.source_bundle_committed_event_ref
      and line.delivered_to_attempt.target_delivery_event_ref =
          d.accepted_delivery_event_ref
      and line.recommended.committed_membership_evidence_ref =
          {commit_event_ref=d.source_bundle_committed_event_ref,
           bundle_artifact_id=d.bundle_artifact_id,
             bundle_digest=d.bundle_digest}
  }, (agent_reference_delivery_id,recommendation_id))

VerifiedProbeScoutBindings =
  {b |
    bound_verified(probe_scout_bindings)
    and probe_scout_bindings.scope.dispatch_id = intent.dispatch_id
    and probe_scout_bindings.scope.aci_delivery_snapshot_digest =
        pinned_input_digests.aci_delivery_snapshot
    and probe_scout_bindings.accepted_through <= effective_as_of
    and b in probe_scout_bindings.members
    and binding_commit =
      exact_event(apt_accepted_prefix.complete_groups,
                  b.accepted_commit_read_group_id,
                  b.commit_event_ref.event_id)
    and binding_commit.journal_offset = b.commit_event_ref.offset
    and H_ACI(canonical(binding_commit.payload)) =
        b.commit_event_ref.payload_digest
    and b.commit_event_ref.offset <= probe_scout_bindings.accepted_through
    and binding_commit.event_type = "reference_scout.bundle_committed@1"
    and binding_commit.payload.scout_run_id = b.scout_run_id
    and binding_commit.payload.bundle_artifact_id = b.bundle_artifact_id
    and binding_commit.payload.bundle_digest = b.bundle_digest
    and binding_commit.payload.recommendation_ids = b.recommendation_ids
    and exists d in Deliveries:
        d.scout_run_id = b.scout_run_id
        and d.bundle_artifact_id = b.bundle_artifact_id
        and d.bundle_digest = b.bundle_digest
        and d.recommendation_ids = b.recommendation_ids}

require unique b in VerifiedProbeScoutBindings per
  (scout_run_id,bundle_artifact_id,bundle_digest,commit_event_ref)
require unique probe_id alias per that same commit identity

declared_use_in_line(u,d,r,b) =>
  exists use_head in apt_fact_heads:
    use_head.fact_type = "ResearchReferenceUse"
    and u = use_head.closed_value
  and capture(u) =
      resolve_capture_from_verified_complete_groups(
        apt_accepted_prefix.complete_groups,
        u.research_capture_id)
  and b in probe_scout_bindings.members
  and b in VerifiedProbeScoutBindings
  and b.probe_id = u.probe_recommendation_ref.probe_id
  and b.scout_run_id = d.scout_run_id
  and b.bundle_digest = d.bundle_digest = u.probe_recommendation_ref.bundle_digest
  and r = u.probe_recommendation_ref.recommendation_id
  and r in b.recommendation_ids
  and capture(u).dispatch_id = d.dispatch_id
  and capture(u).producer_ref.kind = seat
  and bound_verified(producer_resolution)
  and exists p in producer_resolution.members:
      p.research_capture_id = capture(u).research_capture_id
      and p.producer_ref_digest =
        H_ACI(canonical(capture(u).producer_ref))
      and p.activation_id = capture(u).producer_ref.activation_id
      and p.(dispatch_id,group_id,seat_id,attempt_id,agent_instance_id) =
        (d.dispatch_id,d.target_group_id,d.target_seat_id,
         d.target_attempt_id,d.target_agent_instance_id)

access_in_line(o,d,r) =>
  host_observation_projection.status = available
  and host_observation_projection in binder_verified_inputs
  and host_observation_projection.owner_namespace = "host"
  and host_observation_projection.owner_contract_id =
      expected_host_source_observation_contract_id
  and host_observation_projection.accepted_through <= effective_as_of
  and o in host_observation_projection.observations
  and o.accepted_offset <= host_observation_projection.accepted_through
  and o.reference_origin_ref.agent_reference_delivery_id =
      d.agent_reference_delivery_id
  and o.reference_origin_ref.recommendation_id = r
  and o.target_binding.(group_id,seat_id,attempt_id,agent_instance_id) =
      target_tuple(d)

access_observed != empty does_not_imply declared_used != empty
declared_used != empty does_not_imply access_observed != empty
recommended does_not_imply delivered_to_attempt
delivered_to_attempt does_not_imply access_observed != empty
access_observed.coverage in {metadata_only,opaque} does_not_imply content_bytes_exposed_or_read
declared_used != empty does_not_imply claim_relation != empty
claim_relation != empty does_not_imply claim_support_check contains pass
claim_support_check contains pass does_not_adjudicate_or_promote claim
```

The ACI source contract necessarily requires a committed recommendation before target delivery, so
this target-scoped Query contains only recommendation rows with an accepted delivery. The general
rule remains `recommended does_not_imply delivered`: undelivered recommendations do not belong to
any target's result. That causal prerequisite does not collapse the two evidence objects into one
status. There is no
aggregate `used`, `read`, `trusted`, `supported` or `verified` boolean.

### Reads From

| Entity/event/projection | Owner | Fields Used |
|---|---|---|
| [AgentReferenceDelivery](../../agents-communication-infra/specs/domain.md#agentreferencedelivery) and [`reference_scout.bundle_delivered_to_agent@1`](../../agents-communication-infra/specs/events.md#referencescoutbundledeliveredtoagent) | ACI | Source membership, target identities, accepted event/offset and effective-input binding. |
| [EffectiveInputArtifact](../../agents-communication-infra/specs/domain.md#effectiveinputartifact) | ACI | Exact manifest/entry inclusion evidence. |
| future host `SourceObservation` target/origin extension | Host | Exact observation identity, target/origin binding, coverage/tool/source/purpose and evidence digest; specified but not implemented. |
| [ResearchCapture](domain.md#researchcapture) | APT | Dispatch and owner-verified producer tuple. |
| [ResearchReferenceUse](domain.md#researchreferenceuse) | APT | Declared-use kind and exact probe recommendation reference. |
| [ResearchReferenceClaimRelation](domain.md#researchreferenceclaimrelation) | APT | Explicit use-to-claim relation. |
| [ReferenceCheck](domain.md#referencecheck) | APT | Explicit claim-support checks only. |

## Query Coverage and Required Checks

| Registry Query | Interface method | Aspect anchor | Coverage |
|---|---|---|---:|
| `agent-provenance-telemetry.SessionRecord` | `get_session_record(intent)` | [SessionRecord](#sessionrecord) | `1/1` |
| `agent-provenance-telemetry.DispatchScopeProjection` | `get_dispatch_scope_projection(intent)` | [DispatchScopeProjection](#dispatchscopeprojection) | `1/1` |
| `agent-provenance-telemetry.ResearchRecord` | `get_research_record(intent)` | [ResearchRecord](#researchrecord) | `1/1` |
| `agent-provenance-telemetry.AgentReferenceLineage` | `get_agent_reference_lineage(intent)` | [AgentReferenceLineage](#agentreferencelineage) | `1/1` |

- Query definition and Interface coverage are exactly `4/4`.
- Every result binds `requested_o`, `effective_as_of`, the exact owner manifest/digests and the
  deterministic projection hash.
- Replay external-call and side-effect counters are zero.
- Incomplete groups, wrong snapshots, raw bodies, unlinked rows and cross-capture facts are absent.
- Counts use current capture/fact subjects, never event-row counts.
- Check precedence is latest only within an explicit subject chain; independent disagreement
  remains visible and no unpinned policy creates a singular verdict.
- Both Dispatch snapshot variants, legacy locator reorder, multiple offsets, capture/fact
  supersession, retries/exact duplicates and independent check/assessment order are fixture-covered
  by the planned [TEST-SPEC](../TEST-SPEC.md).

## Connections

| Document | Type | Description |
|---|---|---|
| [SPEC.md](SPEC.md) | `implements-contract-for` | Registers these four Query concepts and their relationships after its separate document gate. |
| [interfaces.md](interfaces.md) | `exposed-by` | Defines all four Query methods and their owner-evidence dependencies as specified, not implemented contracts. |
| [states.md](states.md) | `reduces` | Defines verified grouping, current capture and independent adjudication heads. |
| [rules.md](rules.md) | `constrained-by` | Defines replay determinism, no authority and canonical collection rules. |
| [domain.md](domain.md) | `queries` | Supplies immutable entities, value objects and closed enums. |
| [events.md](events.md) | `folds` | Supplies accepted payloads applied only through verified command groups. |
