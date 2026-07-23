---
tags: [agent-provenance-telemetry, spec, queries]
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

# Queries: Agent Provenance Telemetry

This aspect specifies exactly the three read-only Query concepts registered in the
[concept registry](SPEC.md#concept-registry) and exposed by
[ProvenanceQueryPort](interfaces.md#provenancequeryport). It introduces no write operation,
external API, persisted read-model authority or additional Query concept.

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

## Query Coverage and Required Checks

| Registry Query | Interface method | Aspect anchor | Coverage |
|---|---|---|---:|
| `agent-provenance-telemetry.SessionRecord` | `get_session_record(intent)` | [SessionRecord](#sessionrecord) | `1/1` |
| `agent-provenance-telemetry.DispatchScopeProjection` | `get_dispatch_scope_projection(intent)` | [DispatchScopeProjection](#dispatchscopeprojection) | `1/1` |
| `agent-provenance-telemetry.ResearchRecord` | `get_research_record(intent)` | [ResearchRecord](#researchrecord) | `1/1` |

- Registry coverage is exactly `3/3`; interface coverage is exactly `3/3`.
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
| [SPEC.md](SPEC.md) | `implements-contract-for` | Registers exactly these three Query concepts and their relationships. |
| [interfaces.md](interfaces.md) | `exposed-by` | Defines Query intents, bound manifests, results, authorization and errors. |
| [states.md](states.md) | `reduces` | Defines verified grouping, current capture and independent adjudication heads. |
| [rules.md](rules.md) | `constrained-by` | Defines replay determinism, no authority and canonical collection rules. |
| [domain.md](domain.md) | `queries` | Supplies immutable entities, value objects and closed enums. |
| [events.md](events.md) | `folds` | Supplies accepted payloads applied only through verified command groups. |
