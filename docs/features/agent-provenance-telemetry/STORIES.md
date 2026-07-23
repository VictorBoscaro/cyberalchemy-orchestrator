# User Stories: Agent Provenance Telemetry

> Navigate by capability: [Session Registry](#session-registry) ·
> [Dispatch Scope Projection](#dispatch-scope-projection) ·
> [Research Capture & Facts](#research-capture--facts) ·
> [Reference Probe Lineage](#reference-probe-lineage) ·
> [Deterministic Read Models](#deterministic-read-models)

These stories derive behavior from the reviewed DomainSpec corpus and focused discovery. They do
not claim implementation, executable tests, runtime profile registration or UI interaction.

> **Taxonomy/compatibility note:** New product language uses
> `ReferenceScoutTool -> ScoutRun -> recommendations[]`. The `Reference Probe Lineage` headings and
> identifiers below are frozen v1 compatibility surfaces, not a claim that Scout is a Probe subtype.
> The separate general family is `ProbeTool` (pt-BR: **Sonda**) ->
> `ProbeRun(lens_ref) -> observations[]`. Tool and Run are distinct, and neither family promotes an
> output to fact.

## Session Registry

### US-1: Ensure one coarse Session for a host context

As a **trusted orchestration host**, I want **to ensure the current Session from an authenticated
origin context**, so that **repeated work in the same context has one stable parent identity**.

**Given** a trusted invocation with an exact `(origin_kind, origin_ref)` and initial Session name  
**When** the host invokes [EnsureSession](specs/operations.md#ensuresession)  
**Then** the first valid command accepts one [Session](specs/domain.md#session), while an exact
retry or semantic ensure reuses the same Session without creating a duplicate

**Acceptance checks**

- [ ] The initial creation binds one owner-issued `session_id`, `started_at`, immutable initial
  name and exact origin tuple.
- [ ] A same-context repeat returns the accepted Session; it does not append a second
  [SessionStarted](specs/events.md#sessionstarted).
- [ ] Same submitted command identity with a changed canonical digest returns
  `IDEMPOTENCY_CONFLICT`.
- [ ] Planned coverage links:
  [APT-TEST-C01](TEST-SPEC.md#session-context-binding) and
  [APT-TEST-R2](TEST-SPEC.md#apt-r2--idempotent-append).

**Domain coverage**

- Concepts: [Session](specs/domain.md#session),
  [EnsureSession](specs/operations.md#ensuresession),
  [SessionStarted](specs/events.md#sessionstarted)
- States/Rules: [APT-C01](specs/rules.md#session-context-binding),
  [APT-R2](specs/rules.md#apt-r2--idempotent-append)
- Interfaces/Flows: [ProvenanceAppendPort](specs/interfaces.md#provenanceappendport),
  [StartOrReuseSession](specs/workflows.md#startorreusesession)
- Exact IDs: `agent-provenance-telemetry.Session`,
  `agent-provenance-telemetry.EnsureSession`,
  `agent-provenance-telemetry.SessionStarted`, `APT-C01`, `APT-R2`

**Capability links**

- [Session Registry](specs/SPEC.md#capabilities)

### US-2: Roll over a Session only with explicit authorization

As an **authorized host principal**, I want **to start a successor Session explicitly**, so that
**context rollover is intentional, attributable and atomic**.

**Given** a current Session plus single-use owner authorization bound to action, origin,
predecessor, principal, nonce and expiry  
**When** the principal invokes [StartNewSession](specs/operations.md#startnewsession)  
**Then** ACI atomically accepts the successor
[SessionStarted](specs/events.md#sessionstarted) and matching
[SessionContextRebound](specs/events.md#sessioncontextrebound), or accepts neither

**Acceptance checks**

- [ ] Ensure/link failure alone never selects rollover.
- [ ] Missing, stale, mismatched or reused authorization rejects before mutation.
- [ ] The two events have one verified atomic grouping; no intermediate successor becomes visible.
- [ ] A lost response retried with the same command identity/digest returns the stable prior receipt.
- [ ] Planned coverage links:
  [APT-TEST-C02](TEST-SPEC.md#rollover-authorization) and
  [APT-TEST-R2](TEST-SPEC.md#apt-r2--idempotent-append).

**Domain coverage**

- Concepts: [Session](specs/domain.md#session),
  [StartNewSession](specs/operations.md#startnewsession),
  [SessionContextRebound](specs/events.md#sessioncontextrebound)
- States/Rules: [APT-C02](specs/rules.md#rollover-authorization),
  [Atomic Command Receipt and Read Grouping](specs/states.md#atomic-command-receipt-and-read-grouping)
- Interfaces/Flows:
  [HostAuthorizationEvidencePort](specs/interfaces.md#hostauthorizationevidenceport),
  [StartOrReuseSession](specs/workflows.md#startorreusesession)
- Exact IDs: `agent-provenance-telemetry.StartNewSession`,
  `agent-provenance-telemetry.SessionStarted`,
  `agent-provenance-telemetry.SessionContextRebound`, `APT-C02`

**Capability links**

- [Session Registry](specs/SPEC.md#capabilities)

### US-3: Link the current Session to an authoritative Dispatch

As an **authorized orchestration host**, I want **to link the current Session to a pinned Dispatch
snapshot**, so that **Session-to-Dispatch membership has one immutable authority**.

**Given** the exact current Session, an authorized link intent and a verified
[DispatchAuthoritySnapshotRef](specs/domain.md#dispatchauthoritysnapshotref)  
**When** the host invokes [LinkSessionDispatch](specs/operations.md#linksessiondispatch)  
**Then** one [SessionDispatchLink](specs/domain.md#sessiondispatchlink) is accepted without mutating
the Dispatch ledger

**Acceptance checks**

- [ ] The link uses the current origin binding and exact requested `dispatch_id`.
- [ ] [DispatchAuthoritySnapshotRef](specs/domain.md#dispatchauthoritysnapshotref) verifies every
  required authority field for its selected closed variant, rejects mixed/omitted variant fields,
  and the link authorization evidence verifies before append.
- [ ] `aci_managed` requires exact `dispatch_id`, `artifact_ref`, `artifact_digest`,
  `accepted_event_id` and `accepted_offset`; no offset requirement is generalized to the other
  variant.
- [ ] `legacy_ledger` requires exact `ledger_row_identity={dispatch_id,row_kind,appender_identity,
  contract_version}` plus `row_digest`; optional `row_index` is only a non-authoritative locator
  excluded from authority equality and deterministic hash.
- [ ] A contradictory link or stale Session binding fails closed and appends nothing.
- [ ] Reverse Session/Dispatch views remain projections and never become a second join authority.
- [ ] Planned coverage links:
  [APT-TEST-R1](TEST-SPEC.md#apt-r1--single-join-authority),
  [APT-TEST-C03](TEST-SPEC.md#link-session-dispatch-authorization) and
  [APT-TEST-C04](TEST-SPEC.md#dispatch-snapshot-identity).

**Domain coverage**

- Concepts: [SessionDispatchLink](specs/domain.md#sessiondispatchlink),
  [LinkSessionDispatch](specs/operations.md#linksessiondispatch),
  [SessionDispatchLinked](specs/events.md#sessiondispatchlinked)
- States/Rules: [APT-R1](specs/rules.md#apt-r1--single-join-authority),
  [APT-C03](specs/rules.md#link-session-dispatch-authorization),
  [APT-C04](specs/rules.md#dispatch-snapshot-identity)
- Interfaces/Flows: [DispatchSnapshotReader](specs/interfaces.md#dispatchsnapshotreader),
  [StartOrReuseSession](specs/workflows.md#startorreusesession)
- Exact IDs: `agent-provenance-telemetry.SessionDispatchLink`,
  `agent-provenance-telemetry.LinkSessionDispatch`,
  `agent-provenance-telemetry.SessionDispatchLinked`, `APT-R1`, `APT-C03`, `APT-C04`

**Capability links**

- [Session Registry](specs/SPEC.md#capabilities)

## Dispatch Scope Projection

### US-4: Read Dispatch scope without changing Dispatch authority

As an **authorized provenance reader**, I want **to project one Dispatch from its pinned authority
snapshot and accepted APT facts**, so that **Session and Research context is visible without new
Dispatch ledger keys or copied joins**.

**Given** an immutable Dispatch snapshot pin and a verified ACI prefix  
**When** the reader requests
[DispatchScopeProjection](specs/queries.md#dispatchscopeprojection) at `requested_o`  
**Then** the result derives Session membership from
[SessionDispatchLinked](specs/events.md#sessiondispatchlinked) and Research membership from
[ResearchCaptureAppended](specs/events.md#researchcaptureappended)

**Acceptance checks**

- [ ] The projection hash includes the pinned snapshot ref/digest and excludes separately fetched
  current Dispatch data.
- [ ] Historical rows without an authoritative link remain unlinked; no identity is invented.
- [ ] The projection writes no Dispatch row, reverse join or lifecycle state.
- [ ] A snapshot identity mismatch or invalid replay prefix returns a typed error with no
  authoritative partial value.
- [ ] Planned coverage links:
  [APT-TEST-R1](TEST-SPEC.md#apt-r1--single-join-authority),
  [APT-TEST-C04](TEST-SPEC.md#dispatch-snapshot-identity) and
  [APT-TEST-R6](TEST-SPEC.md#apt-r6--replay-determinism).

**Domain coverage**

- Concepts: [DispatchAuthoritySnapshotRef](specs/domain.md#dispatchauthoritysnapshotref),
  [DispatchScopeProjection](specs/queries.md#dispatchscopeprojection)
- States/Rules: [APT-R1](specs/rules.md#apt-r1--single-join-authority),
  [APT-R6](specs/rules.md#apt-r6--replay-determinism),
  [APT-C04](specs/rules.md#dispatch-snapshot-identity)
- Interfaces/Flows: [ProvenanceQueryPort](specs/interfaces.md#provenancequeryport),
  [ProvenanceFactsToReadModels](specs/mappings.md#provenancefactstoreadmodels)
- Exact IDs: `agent-provenance-telemetry.DispatchAuthoritySnapshotRef`,
  `agent-provenance-telemetry.DispatchScopeProjection`,
  `agent-provenance-telemetry.ProvenanceFactsToReadModels`, `APT-R1`, `APT-R6`, `APT-C04`

**Capability links**

- [Dispatch Scope Projection](specs/SPEC.md#capabilities)

## Research Capture & Facts

### US-5: Capture an exact producer outcome

As an **authenticated research producer**, I want **to append one immutable outcome for an expected
Dispatch contribution**, so that **captured, partial and missing work remain distinguishable and
auditable**.

**Given** a current Session/Dispatch link, exact expected contribution, producer evidence and pinned
Dispatch snapshot  
**When** the producer invokes
[AppendResearchCapture](specs/operations.md#appendresearchcapture)  
**Then** one immutable [ResearchCapture](specs/domain.md#researchcapture) is accepted under the
closed status matrix

**Acceptance checks**

- [ ] `captured` has one already-finalized UTF-8 artifact and canonical-null partial/failure slots.
- [ ] `partial` has one already-finalized artifact, non-empty partial reason, canonical-null failure
  reason and optional selected evidence ref/canonical null.
- [ ] `missing` has canonical-null raw return/partial reason, non-empty failure reason and required
  committed selected failure evidence.
- [ ] Raw bytes never enter the event, receipt, projection or telemetry.
- [ ] The complete closed capture preimage produces the accepted `capture_digest`.
- [ ] Planned coverage links:
  [APT-TEST-R3](TEST-SPEC.md#apt-r3--artifact-only-raw-return),
  [APT-TEST-C05](TEST-SPEC.md#capture-digest) and
  [APT-TEST-C08](TEST-SPEC.md#evidence-reference-validity).

**Domain coverage**

- Concepts: [ResearchCapture](specs/domain.md#researchcapture),
  [ArtifactReference](specs/domain.md#artifactreference),
  [AppendResearchCapture](specs/operations.md#appendresearchcapture)
- States/Rules: [APT-R3](specs/rules.md#apt-r3--artifact-only-raw-return),
  [APT-C05](specs/rules.md#capture-digest),
  [APT-C08](specs/rules.md#evidence-reference-validity)
- Interfaces/Flows:
  [ArtifactFinalizationVerifier](specs/interfaces.md#artifactfinalizationverifier),
  [CaptureAndEnrichResearch](specs/workflows.md#captureandenrichresearch)
- Exact IDs: `agent-provenance-telemetry.ResearchCapture`,
  `agent-provenance-telemetry.ArtifactReference`,
  `agent-provenance-telemetry.AppendResearchCapture`,
  `agent-provenance-telemetry.ResearchCaptureAppended`, `APT-R3`, `APT-C05`, `APT-C08`

**Capability links**

- [Research Capture & Facts](specs/SPEC.md#capabilities)

### US-6: Correct or synthesize captures by forward append

As a **research producer or reviewer**, I want **to append a correction or synthesis with exact
predecessor/input pins**, so that **history is preserved while the current Research result can
advance deterministically**.

**Given** the current capture-chain head or a non-empty ordered list of same-Dispatch current
capture/digest pins  
**When** the caller appends a correction or synthesis through
[AppendResearchCapture](specs/operations.md#appendresearchcapture)  
**Then** the new immutable capture becomes current only when all predecessor and synthesis guards
verify

**Acceptance checks**

- [ ] A correction has a new `research_capture_id` and exact
  `supersedes_capture_id=current_head`.
- [ ] A stale, cross-chain, self or forked predecessor returns `CAPTURE_CAS_CONFLICT`.
- [ ] Every synthesis input pins the exact `research_capture_id + capture_digest`, is unique,
  current-at-append and belongs to the same Dispatch.
- [ ] Later supersession of an input never rewrites the historical synthesis composition.
- [ ] Planned coverage links:
  [APT-TEST-R5](TEST-SPEC.md#apt-r5--capture-supersession),
  [APT-TEST-C06](TEST-SPEC.md#research-synthesis-pins) and
  [APT-TEST-C18](TEST-SPEC.md#relational-collection-canonicalization).

**Domain coverage**

- Concepts: [ResearchCapture](specs/domain.md#researchcapture),
  [AppendResearchCapture](specs/operations.md#appendresearchcapture)
- States/Rules: [APT-R5](specs/rules.md#apt-r5--capture-supersession),
  [APT-C06](specs/rules.md#research-synthesis-pins),
  [APT-C18](specs/rules.md#relational-collection-canonicalization)
- Interfaces/Flows:
  [AcceptedProvenanceStateReader](specs/interfaces.md#acceptedprovenancestatereader),
  [CaptureAndEnrichResearch](specs/workflows.md#captureandenrichresearch)
- Exact IDs: `agent-provenance-telemetry.ResearchCapture`,
  `agent-provenance-telemetry.AppendResearchCapture`, `APT-R5`, `APT-C06`, `APT-C18`

**Capability links**

- [Research Capture & Facts](specs/SPEC.md#capabilities)

### US-7: Enrich a capture with attributed questions, answers, problems and claims

As an **authenticated extractor or reviewer**, I want **to append typed research facts that point
into the exact capture witness**, so that **structured research remains attributable without
copying or mutating the raw response**.

**Given** a current non-missing capture, exact artifact bytes and a valid UTF-8 byte selector  
**When** the caller invokes [AppendResearchFact](specs/operations.md#appendresearchfact) for a
question, answer, problem or claim  
**Then** one closed Entity payload with [FactEnvelope](specs/domain.md#factenvelope) and
[ExtractionProvenance](specs/domain.md#extractionprovenance) is appended or resolved as exact
existing

**Acceptance checks**

- [ ] Selector bounds, selected digest, source capture ID/digest, extractor and method all verify.
- [ ] Questions derived from Dispatch scope or another question use exact typed derivation refs;
  assignment prompt text is not automatically a ResearchQuestion.
- [ ] Answers point to one or more same-capture questions and do not copy the complete witness.
- [ ] Problems and claims remain research-local facts and do not mutate Dispatch lifecycle or
  become promoted knowledge.
- [ ] Same-subject correction uses a new fact ID and current `supersedes_fact_id`; stale/forked
  revisions fail.
- [ ] Planned coverage links:
  [APT-TEST-R4](TEST-SPEC.md#apt-r4--extraction-provenance),
  [APT-TEST-C07](TEST-SPEC.md#raw-selector-validity),
  [APT-TEST-C09](TEST-SPEC.md#question-derivation-validity),
  [APT-TEST-C10](TEST-SPEC.md#research-fact-appended-closed-union),
  [APT-TEST-C11](TEST-SPEC.md#research-fact-locality),
  [APT-TEST-C12](TEST-SPEC.md#research-fact-typing) and
  [APT-TEST-C15](TEST-SPEC.md#fact-append-identity).

**Domain coverage**

- Concepts: [ResearchQuestion](specs/domain.md#researchquestion),
  [ResearchAnswer](specs/domain.md#researchanswer),
  [ResearchProblem](specs/domain.md#researchproblem),
  [ResearchClaimExtraction](specs/domain.md#researchclaimextraction),
  [AppendResearchFact](specs/operations.md#appendresearchfact)
- States/Rules: [APT-R4](specs/rules.md#apt-r4--extraction-provenance),
  [APT-C07](specs/rules.md#raw-selector-validity),
  [APT-C09](specs/rules.md#question-derivation-validity),
  [APT-C10](specs/rules.md#research-fact-appended-closed-union),
  [APT-C11](specs/rules.md#research-fact-locality),
  [APT-C12](specs/rules.md#research-fact-typing),
  [APT-C15](specs/rules.md#fact-append-identity)
- Interfaces/Flows: [ArtifactEvidenceReader](specs/interfaces.md#artifactevidencereader),
  [CaptureAndEnrichResearch](specs/workflows.md#captureandenrichresearch)
- Exact IDs: `agent-provenance-telemetry.ResearchQuestion`,
  `agent-provenance-telemetry.ResearchAnswer`,
  `agent-provenance-telemetry.ResearchProblem`,
  `agent-provenance-telemetry.ResearchClaimExtraction`,
  `agent-provenance-telemetry.AppendResearchFact`, `APT-R4`, `APT-C07`, `APT-C09`,
  `APT-C10`, `APT-C11`, `APT-C12`, `APT-C15`

**Capability links**

- [Research Capture & Facts](specs/SPEC.md#capabilities)

### US-8: Record reference use, claim relation and independent checks

As a **research reviewer**, I want **to distinguish attributed reference use, its relation to a
claim and an independent typed check**, so that **mention, consultation, support and verification
are not conflated**.

**Given** a current capture plus exact use/relation/check identities and any owner-verified optional
evidence  
**When** the reviewer appends
[ResearchReferenceUse](specs/domain.md#researchreferenceuse),
[ResearchReferenceClaimRelation](specs/domain.md#researchreferenceclaimrelation) or
[ReferenceCheck](specs/domain.md#referencecheck) through
[AppendResearchFact](specs/operations.md#appendresearchfact)  
**Then** each fact retains its own typed semantics and predecessor chain

**Acceptance checks**

- [ ] A reference use records exactly observed locator/use/anchor attribution; host observation is
  optional and never inferred from locator similarity.
- [ ] A relation binds one same-capture use to one same-capture claim with a closed epistemic
  relation.
- [ ] `ReferenceCheck` is the only non-extraction Entity variant and binds checker, method, kind,
  result and optional finalized evidence without reading the capture artifact body.
- [ ] Independent checker/method subject keys coexist; disagreement is preserved rather than
  overwritten.
- [ ] A recommendation reference proves delivery lineage only; source access/support requires the
  corresponding explicit fact/evidence.
- [ ] Planned coverage links:
  [APT-TEST-C08](TEST-SPEC.md#evidence-reference-validity),
  [APT-TEST-C11](TEST-SPEC.md#research-fact-locality),
  [APT-TEST-C13](TEST-SPEC.md#reference-check-typing) and
  [APT-TEST-C15](TEST-SPEC.md#fact-append-identity).

**Domain coverage**

- Concepts: [ResearchReferenceUse](specs/domain.md#researchreferenceuse),
  [ResearchReferenceClaimRelation](specs/domain.md#researchreferenceclaimrelation),
  [ReferenceCheck](specs/domain.md#referencecheck),
  [AppendResearchFact](specs/operations.md#appendresearchfact)
- States/Rules: [APT-C08](specs/rules.md#evidence-reference-validity),
  [APT-C11](specs/rules.md#research-fact-locality),
  [APT-C13](specs/rules.md#reference-check-typing),
  [APT-C15](specs/rules.md#fact-append-identity)
- Interfaces/Flows:
  [HostSourceObservationEvidencePort](specs/interfaces.md#hostsourceobservationevidenceport),
  [CaptureAndEnrichResearch](specs/workflows.md#captureandenrichresearch)
- Exact IDs: `agent-provenance-telemetry.ResearchReferenceUse`,
  `agent-provenance-telemetry.ResearchReferenceClaimRelation`,
  `agent-provenance-telemetry.ReferenceCheck`,
  `agent-provenance-telemetry.AppendResearchFact`, `APT-C08`, `APT-C11`, `APT-C13`, `APT-C15`

**Capability links**

- [Research Capture & Facts](specs/SPEC.md#capabilities)

### US-9: Preserve candidate formalization and append-only review chains

As a **research formalizer or reviewer**, I want **to bind interpreted notation to one exact
research claim and record dispositions/assessments separately**, so that **mathematical or logical
ideas are useful without becoming automatically accepted ontology**.

**Given** a same-capture ResearchClaimExtraction, exact notation/legend/reading/logic family/scope
and any optional checker/governance refs  
**When** the formalizer appends a
[FormalizationCandidate](specs/domain.md#formalizationcandidate) or a reviewer appends a
disposition/assessment through [AppendResearchFact](specs/operations.md#appendresearchfact)  
**Then** the candidate remains research-local and reviews advance their explicit aggregate chains

**Acceptance checks**

- [ ] A formalization targets exactly one same-capture claim and includes non-empty legend,
  natural-language reading, logic family and scope.
- [ ] Optional syntax/proof/governance refs remain distinct; none makes the candidate canonical
  vocabulary.
- [ ] The formalization Entity uses FactEnvelope/current fact-head CAS and extraction evidence.
- [ ] Disposition/assessment uses exact TargetRef plus aggregate type/ID/head/version CAS, no
  FactEnvelope and no capture artifact-body read.
- [ ] Concurrent stale aggregate writers cannot both advance the same review chain.
- [ ] Planned coverage links:
  [APT-TEST-C12](TEST-SPEC.md#research-fact-typing),
  [APT-TEST-C14](TEST-SPEC.md#formalization-locality) and
  [APT-TEST-C16](TEST-SPEC.md#disposition-and-assessment-chains).

**Domain coverage**

- Concepts: [FormalizationCandidate](specs/domain.md#formalizationcandidate),
  [ResearchClaimExtraction](specs/domain.md#researchclaimextraction),
  [AppendResearchFact](specs/operations.md#appendresearchfact)
- States/Rules: [APT-C12](specs/rules.md#research-fact-typing),
  [APT-C14](specs/rules.md#formalization-locality),
  [APT-C16](specs/rules.md#disposition-and-assessment-chains)
- Interfaces/Flows:
  [AcceptedProvenanceStateReader](specs/interfaces.md#acceptedprovenancestatereader),
  [CaptureAndEnrichResearch](specs/workflows.md#captureandenrichresearch)
- Exact IDs: `agent-provenance-telemetry.FormalizationCandidate`,
  `agent-provenance-telemetry.ResearchClaimExtraction`,
  `agent-provenance-telemetry.AppendResearchFact`, `APT-C12`, `APT-C14`, `APT-C16`

**Capability links**

- [Research Capture & Facts](specs/SPEC.md#capabilities)

## Reference Probe Lineage

### US-10: Ingest an idempotent mixed probe-lineage result

As an **authenticated probe-lineage ingestion principal**, I want **to map an already committed,
profile-bound recommendation into delivery lineage and optional evidenced reference uses**, so that
**probe origin is preserved without creating a second bus or claiming source access**.

**Given** an accepted probe bundle/recommendation receipt, exact registered protocol bindings,
current delivery/fact heads and an unordered unique item set  
**When** the principal invokes
[AppendReferenceProbeLineage](specs/operations.md#appendreferenceprobelineage)  
**Then** ACI partitions the request into `existing_exact`, `submitted_new` or conflict and commits
only the canonical non-empty new portion atomically

**Acceptance checks**

- [ ] Missing/mismatched probe, atomic-grouping or transactional semantic-registry profile evidence
  blocks the append.
- [ ] Input order permutations produce the same canonical item order and command digest; duplicate
  stable subject keys are rejected.
- [ ] Mixed success returns
  `existing_exact ∪ accepted(submitted_new)`; the receipt is non-null and contains exactly accepted
  new members, never existing refs.
- [ ] Zero-new returns `semantic_existing`, submits no command and returns a null new receipt.
- [ ] Same submitted command identity/digest returns the stored result; changed digest conflicts.
- [ ] Global `fact_id` collision across direct fact/probe paths returns existing exact only for the
  same payload digest, subject and predecessor; otherwise the group conflicts.
- [ ] Delivery-only lineage never asserts access, consultation or support.
- [ ] Planned coverage links:
  [APT-TEST-R2](TEST-SPEC.md#apt-r2--idempotent-append),
  [APT-TEST-R7](TEST-SPEC.md#apt-r7--protocol-profile-binding),
  [APT-TEST-C15](TEST-SPEC.md#fact-append-identity),
  [APT-TEST-C17](TEST-SPEC.md#probe-lineage-append) and
  [APT-TEST-C18](TEST-SPEC.md#relational-collection-canonicalization).

**Domain coverage**

- Concepts: [ACIProtocolProfileBinding](specs/domain.md#aciprotocolprofilebinding),
  [ProbeRecommendationRef](specs/domain.md#proberecommendationref),
  [AppendReferenceProbeLineage](specs/operations.md#appendreferenceprobelineage),
  [ReferenceProbeLineageAppended](specs/events.md#referenceprobelineageappended)
- States/Rules: [APT-R2](specs/rules.md#apt-r2--idempotent-append),
  [APT-R7](specs/rules.md#apt-r7--protocol-profile-binding),
  [APT-C15](specs/rules.md#fact-append-identity),
  [APT-C17](specs/rules.md#probe-lineage-append),
  [APT-C18](specs/rules.md#relational-collection-canonicalization)
- Interfaces/Flows: [ProbeLineageIngress](specs/interfaces.md#probelineageingress),
  [IngestReferenceProbeLineage](specs/workflows.md#ingestreferenceprobelineage)
- Exact IDs: `agent-provenance-telemetry.ACIProtocolProfileBinding`,
  `agent-provenance-telemetry.ProbeRecommendationRef`,
  `agent-provenance-telemetry.AppendReferenceProbeLineage`,
  `agent-provenance-telemetry.ReferenceProbeLineageAppended`,
  `APT-R2`, `APT-R7`, `APT-C15`, `APT-C17`, `APT-C18`

**Capability links**

- [Reference Probe Lineage](specs/SPEC.md#capabilities)

## Deterministic Read Models

### US-11: Rebuild Session, Dispatch and Research records at an explicit offset

As an **authorized provenance reader**, I want **deterministic Session, Dispatch and Research
records at one requested ACI offset**, so that **historical answers are reproducible and never mix
partial atomic groups or future facts**.

**Given** `requested_o`, an authorized ACI prefix, exact pinned manifests and an optional eligible
verified checkpoint  
**When** the reader invokes [ProvenanceQueryPort](specs/interfaces.md#provenancequeryport)  
**Then** the query returns a [SessionRecord](specs/queries.md#sessionrecord),
[DispatchScopeProjection](specs/queries.md#dispatchscopeprojection) or
[ResearchRecord](specs/queries.md#researchrecord) at the greatest verified complete-group boundary
not after `requested_o`

**Acceptance checks**

- [ ] Every result exposes exact `requested_o` and `effective_as_of`; a request inside a group uses
  the preceding verified boundary.
- [ ] A checkpoint is eligible only when its exact prefix/group binding verifies and
  `journal_offset ≤ effective_as_of(requested_o)`.
- [ ] Replay from the closed empty state and an eligible checkpoint yields the same canonical value
  and projection hash.
- [ ] Dedupe, capture/fact supersession, reference/check identity and aggregate heads are resolved
  only from the verified accepted prefix.
- [ ] Missing, overlapping, forked, schema/digest-invalid input returns
  `READ_INTEGRITY_FAILURE`; the Query never repairs or rebuilds a projection.
- [ ] The pure reducer performs zero external calls, writes, publications or telemetry I/O.
- [ ] Planned coverage links:
  [APT-TEST-R6](TEST-SPEC.md#apt-r6--replay-determinism),
  [APT-TEST-R1](TEST-SPEC.md#apt-r1--single-join-authority),
  [APT-TEST-R5](TEST-SPEC.md#apt-r5--capture-supersession) and
  [APT-TEST-C15](TEST-SPEC.md#fact-append-identity).

**Domain coverage**

- Concepts: [SessionRecord](specs/queries.md#sessionrecord),
  [DispatchScopeProjection](specs/queries.md#dispatchscopeprojection),
  [ResearchRecord](specs/queries.md#researchrecord)
- States/Rules: [APT-R6](specs/rules.md#apt-r6--replay-determinism),
  [Atomic Command Receipt and Read Grouping](specs/states.md#atomic-command-receipt-and-read-grouping)
- Interfaces/Flows: [ProvenanceQueryPort](specs/interfaces.md#provenancequeryport),
  [Replay, Checkpoints and Projections](specs/persistence-and-replay.md#replay-checkpoints-and-projections)
- Exact IDs: `agent-provenance-telemetry.SessionRecord`,
  `agent-provenance-telemetry.DispatchScopeProjection`,
  `agent-provenance-telemetry.ResearchRecord`,
  `agent-provenance-telemetry.ProvenanceQueryPort`, `APT-R6`

**Capability links**

- [Deterministic Read Models](specs/SPEC.md#capabilities)

### US-12: Diagnose safely without making telemetry authoritative

As an **authorized operator**, I want **minimal correlated logs, traces and bounded metrics without
research content**, so that **append/replay/profile/CAS failures are diagnosable without changing
domain outcomes or leaking sensitive evidence**.

**Given** an Operation, adapter submission, Workflow or deterministic read reaches a typed
observation point  
**When** [APT observability](specs/observability.md) attempts to emit its closed signal  
**Then** only classified/redacted metadata and permitted restricted correlation are observed, while
ACI receipts/journal remain the sole authority

**Acceptance checks**

- [ ] Raw research/checkpoint bodies, selectors, questions, answers, claims, problems,
  notation/legend/reading, locators, credentials and free-form exceptions never enter telemetry.
- [ ] Metrics use only bounded enums; opaque IDs/digests remain restricted log/span correlation and
  never labels.
- [ ] Accepted-event counters increment only from a newly accepted verified group, never a retry or
  semantic-existing result.
- [ ] Pre-boundary replay rejection has canonical-null `effective_as_of/boundary_lag`; pre-source
  rejection has canonical-null `input_source` and no source-labeled duration.
- [ ] Signal/export failure and alerts cause no append, retry, rebuild, repair or result change.
- [ ] Telemetry expiry changes no ACI event, receipt, head, semantic key, artifact or projection.
- [ ] Planned coverage links:
  [APT-TEST-R3](TEST-SPEC.md#apt-r3--artifact-only-raw-return) and
  [APT-TEST-R8](TEST-SPEC.md#apt-r8--telemetry-non-authority).

**Domain coverage**

- Concepts: [ArtifactReference](specs/domain.md#artifactreference),
  [ProvenanceAppendPort](specs/interfaces.md#provenanceappendport),
  [ProvenanceQueryPort](specs/interfaces.md#provenancequeryport)
- States/Rules: [APT-R3](specs/rules.md#apt-r3--artifact-only-raw-return),
  [APT-R8](specs/rules.md#apt-r8--telemetry-non-authority)
- Interfaces/Flows: [Observability](specs/observability.md),
  [Persistence and Replay](specs/persistence-and-replay.md)
- Exact IDs: `agent-provenance-telemetry.ArtifactReference`,
  `agent-provenance-telemetry.ProvenanceAppendPort`,
  `agent-provenance-telemetry.ProvenanceQueryPort`, `APT-R3`, `APT-R8`

**Capability links**

- [Deterministic Read Models](specs/SPEC.md#capabilities)

## Story Coverage Matrix

| Capability | Story IDs | Covered Concepts | Notes |
|---|---|---|---|
| Session Registry | US-1, US-2, US-3 | `Session`, `EnsureSession`, `StartNewSession`, `SessionDispatchLink`, `LinkSessionDispatch` | New/reuse, explicit rollover, sole Dispatch link and negative authorization/CAS paths |
| Dispatch Scope Projection | US-4 | `DispatchAuthoritySnapshotRef`, `DispatchScopeProjection`, `ProvenanceFactsToReadModels` | Pinned authority, historical unlinked data and no Dispatch mutation |
| Research Capture & Facts | US-5, US-6, US-7, US-8, US-9 | `ResearchCapture`, eight Entity fact variants, disposition/assessment payloads, `AppendResearchCapture`, `AppendResearchFact` | Status matrix, correction/synthesis, extraction, reference/check and formalization/review paths |
| Reference Probe Lineage | US-10 | `ACIProtocolProfileBinding`, `ProbeRecommendationRef`, `AppendReferenceProbeLineage` | Zero/mixed/all-new, idempotency, global fact identity and delivery-only negative semantics |
| Deterministic Read Models | US-11, US-12 | `SessionRecord`, `DispatchScopeProjection`, `ResearchRecord`, append/query ports | Historical as-of, checkpoint/empty replay, privacy and telemetry non-authority |

## Cross-Cutting Coverage

| Obligation | Story IDs | Planned test anchors |
|---|---|---|
| Three-level authority spine: Session → Dispatch → Research | US-1, US-3, US-4, US-5, US-11 | [APT-TEST-R1](TEST-SPEC.md#apt-r1--single-join-authority), [APT-TEST-C01](TEST-SPEC.md#session-context-binding) |
| Append-before-ack and idempotency | US-1, US-2, US-5, US-10 | [APT-TEST-R2](TEST-SPEC.md#apt-r2--idempotent-append) |
| Artifact-only raw capture and exact extraction | US-5, US-7, US-8, US-12 | [APT-TEST-R3](TEST-SPEC.md#apt-r3--artifact-only-raw-return), [APT-TEST-R4](TEST-SPEC.md#apt-r4--extraction-provenance) |
| Forward-only capture/fact/review correction | US-6, US-7, US-9 | [APT-TEST-R5](TEST-SPEC.md#apt-r5--capture-supersession), [APT-TEST-C16](TEST-SPEC.md#disposition-and-assessment-chains) |
| Exact profile-bound probe lineage | US-8, US-10 | [APT-TEST-R7](TEST-SPEC.md#apt-r7--protocol-profile-binding), [APT-TEST-C17](TEST-SPEC.md#probe-lineage-append) |
| Deterministic replay and non-authoritative telemetry | US-4, US-11, US-12 | [APT-TEST-R6](TEST-SPEC.md#apt-r6--replay-determinism), [APT-TEST-R8](TEST-SPEC.md#apt-r8--telemetry-non-authority) |
