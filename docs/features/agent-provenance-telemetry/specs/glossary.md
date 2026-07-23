---
feature: agent-provenance-telemetry
version: 0.1.0
status: draft
updatedAt: 2026-07-23
docType: glossary
specAuthoringGate: in-review
runtimeGate: block
---

# Glossary: Agent Provenance Telemetry

Quick-reference glossary of feature language and concepts distilled from the
[feature specification](SPEC.md). This document explains terms; authoritative behavior, fields,
rules and lifecycle contracts remain in their linked source aspects.

## Feature Language

| Term | Meaning in this feature | Related Concepts |
|---|---|---|
| Session | The coarse durable context that groups related dispatches without equating a runtime context to a curated Markdown session note. | [Session](domain.md#session), [SessionRecord](queries.md#sessionrecord) |
| Context binding | The association between one originating host context and the Session it currently reuses. | [StartNewSession](operations.md#startnewsession), [SessionContextRebound](events.md#sessioncontextrebound) |
| Dispatch scope | The confirmed intent and inputs already owned by an existing Dispatch, viewed without transferring that ownership to APT. | [DispatchScopeProjection](queries.md#dispatchscopeprojection), [DispatchAuthoritySnapshotRef](domain.md#dispatchauthoritysnapshotref) |
| Research capture | One identity-bearing record of an expected contribution outcome, distinct from later interpretation of that outcome. | [ResearchCapture](domain.md#researchcapture), [CaptureStatus](domain.md#capturestatus) |
| Research fact | An identity-bearing extracted item appended beside a capture, such as a question, answer, reference use, problem or claim extraction. | [FactEnvelope](domain.md#factenvelope), [AppendResearchFact](operations.md#appendresearchfact) |
| Research record | The read-oriented aggregation of one capture and its current extracted facts at a stated event boundary. | [ResearchRecord](queries.md#researchrecord) |
| Raw witness | The exact finalized producer-return evidence referenced by a captured or partial ResearchCapture; a missing capture has no raw witness. | [ArtifactReference](domain.md#artifactreference), [ArtifactOnlyRawReturnRule](rules.md#apt-r3--artifact-only-raw-return) |
| Extraction provenance | The attribution and exact source selection that explain who or what derived a structured fact from captured evidence. | [ExtractionProvenance](domain.md#extractionprovenance), [RawSelector](domain.md#rawselector) |
| As-of | A declaration that a projection reflects only accepted facts through a named event boundary. | [ReplayDeterminismRule](rules.md#apt-r6--replay-determinism), [ResearchRecord](queries.md#researchrecord) |
| Supersession | The predecessor-linked relationship by which a newer immutable version replaces an older version in current projections without deleting history. | [CaptureSupersessionRule](rules.md#apt-r5--capture-supersession), [FactEnvelope](domain.md#factenvelope) |
| Source observation | Host-owned evidence about mediated acquisition or access, referenced by APT but not created or reclassified by it. | [ResearchReferenceUse](domain.md#researchreferenceuse), [`host.SourceObservation`](../discovery/session-dispatch-research-records.md#43-reference-uses-and-checks) |
| Reference use | An attributed mention, citation or claimed consultation inside one research result, distinct from host access and claim support. | [ResearchReferenceUse](domain.md#researchreferenceuse), [ReferenceCheck](domain.md#referencecheck) |
| Formalization | Candidate mathematical or logical notation tied to one extracted research claim and accompanied by its interpretation. | [FormalizationCandidate](domain.md#formalizationcandidate), [FormalizationDisposition](domain.md#formalizationdisposition) |

## Terms

The 58 rows below correspond one-for-one with the current
[SPEC Concept Registry](SPEC.md#concept-registry). Aspect anchors are canonical locations validated
through the individual file-review gates; corpus-wide review remains in progress.

| Term | Concept ID | Type | Definition | Source |
|---|---|---|---|---|
| Session | `agent-provenance-telemetry.Session` | Entity | The durable identity for one coarse orchestration context. | [domain.md](domain.md#session) |
| SessionDispatchLink | `agent-provenance-telemetry.SessionDispatchLink` | Entity | The identity-bearing association that records a Session membership for an existing Dispatch. | [domain.md](domain.md#sessiondispatchlink) |
| ResearchCapture | `agent-provenance-telemetry.ResearchCapture` | Entity | One immutable expected-contribution outcome and its producer/evidence lineage. | [domain.md](domain.md#researchcapture) |
| ResearchQuestion | `agent-provenance-telemetry.ResearchQuestion` | Entity | An addressable question extracted or declared within one captured research outcome. | [domain.md](domain.md#researchquestion) |
| ResearchAnswer | `agent-provenance-telemetry.ResearchAnswer` | Entity | An addressable answer extraction associated with one or more ResearchQuestions. | [domain.md](domain.md#researchanswer) |
| ResearchReferenceUse | `agent-provenance-telemetry.ResearchReferenceUse` | Entity | An attributed use of a reference within one research outcome. | [domain.md](domain.md#researchreferenceuse) |
| ResearchReferenceClaimRelation | `agent-provenance-telemetry.ResearchReferenceClaimRelation` | Entity | An addressable typed relation between one reference use and one research-local claim extraction. | [domain.md](domain.md#researchreferenceclaimrelation) |
| ReferenceCheck | `agent-provenance-telemetry.ReferenceCheck` | Entity | One identified evaluation of source identity, access evidence or claim support. | [domain.md](domain.md#referencecheck) |
| ResearchProblem | `agent-provenance-telemetry.ResearchProblem` | Entity | An addressable gap, contradiction, blocker, uncertainty or failed check surfaced by research. | [domain.md](domain.md#researchproblem) |
| ResearchClaimExtraction | `agent-provenance-telemetry.ResearchClaimExtraction` | Entity | A research-local proposition extracted from captured evidence without global knowledge status. | [domain.md](domain.md#researchclaimextraction) |
| FormalizationCandidate | `agent-provenance-telemetry.FormalizationCandidate` | Entity | An addressable candidate notation and interpretation for exactly one ResearchClaimExtraction. | [domain.md](domain.md#formalizationcandidate) |
| FactEnvelope | `agent-provenance-telemetry.FactEnvelope` | Value Object | The common immutable identity, subject, operation, time and predecessor fields of an extracted fact version. | [domain.md](domain.md#factenvelope) |
| ExtractionProvenance | `agent-provenance-telemetry.ExtractionProvenance` | Value Object | The actor, method, mode and capture-bound selection describing an extraction's origin. | [domain.md](domain.md#extractionprovenance) |
| RawSelector | `agent-provenance-telemetry.RawSelector` | Value Object | A digest-bound half-open UTF-8 byte range selecting exact captured evidence. | [domain.md](domain.md#rawselector) |
| ContentDigest | `agent-provenance-telemetry.ContentDigest` | Value Object | A content-integrity value that identifies canonical bytes under a named digest scheme. | [domain.md](domain.md#contentdigest) |
| ArtifactReference | `agent-provenance-telemetry.ArtifactReference` | Value Object | A reference to finalized content together with integrity and governance metadata. | [domain.md](domain.md#artifactreference) |
| DispatchAuthoritySnapshotRef | `agent-provenance-telemetry.DispatchAuthoritySnapshotRef` | Value Object | A pinned ACI-managed or legacy-ledger Dispatch authority snapshot used by deterministic reads. | [domain.md](domain.md#dispatchauthoritysnapshotref) |
| ProbeRecommendationRef | `agent-provenance-telemetry.ProbeRecommendationRef` | Value Object | A reference to one committed probe recommendation and its bundle/source lineage. | [domain.md](domain.md#proberecommendationref) |
| ACIProtocolProfileBinding | `agent-provenance-telemetry.ACIProtocolProfileBinding` | Value Object | The exact ACI protocol profile identity, version and digest attached to probe-origin evidence. | [domain.md](domain.md#aciprotocolprofilebinding) |
| CaptureStatus | `agent-provenance-telemetry.CaptureStatus` | Enum / Type | The finite classification `captured`, `partial` or `missing` for a ResearchCapture outcome. | [domain.md](domain.md#capturestatus) |
| ExtractionMode | `agent-provenance-telemetry.ExtractionMode` | Enum / Type | The finite attribution mode describing an extraction as verbatim, declared or inferred. | [domain.md](domain.md#extractionmode) |
| ReferenceUseKind | `agent-provenance-telemetry.ReferenceUseKind` | Enum / Type | The finite kind of attributed reference use: mentioned, cited or claimed consulted. | [domain.md](domain.md#referenceusekind) |
| ReferenceCheckKind | `agent-provenance-telemetry.ReferenceCheckKind` | Enum / Type | The finite category of reference evaluation: source identity, access evidence or claim support. | [domain.md](domain.md#referencecheckkind) |
| ReferenceCheckResult | `agent-provenance-telemetry.ReferenceCheckResult` | Enum / Type | The finite result of a ReferenceCheck: pass, fail or indeterminate. | [domain.md](domain.md#referencecheckresult) |
| ProblemDisposition | `agent-provenance-telemetry.ProblemDisposition` | Enum / Type | The finite research-local disposition vocabulary for a ResearchProblem. | [domain.md](domain.md#problemdisposition) |
| ClaimDisposition | `agent-provenance-telemetry.ClaimDisposition` | Enum / Type | The finite research-local disposition vocabulary for a ResearchClaimExtraction. | [domain.md](domain.md#claimdisposition) |
| FormalizationDisposition | `agent-provenance-telemetry.FormalizationDisposition` | Enum / Type | The finite research-local review disposition for a FormalizationCandidate. | [domain.md](domain.md#formalizationdisposition) |
| EnsureSession | `agent-provenance-telemetry.EnsureSession` | Operation | The request to reuse or establish the Session associated with an originating context. | [operations.md](operations.md#ensuresession) |
| StartNewSession | `agent-provenance-telemetry.StartNewSession` | Operation | The request to start a successor Session and rebind an authorized current context. | [operations.md](operations.md#startnewsession) |
| LinkSessionDispatch | `agent-provenance-telemetry.LinkSessionDispatch` | Operation | The request to record the authoritative membership of an existing Dispatch in a Session. | [operations.md](operations.md#linksessiondispatch) |
| AppendResearchCapture | `agent-provenance-telemetry.AppendResearchCapture` | Operation | The request to append one immutable ResearchCapture outcome. | [operations.md](operations.md#appendresearchcapture) |
| AppendResearchFact | `agent-provenance-telemetry.AppendResearchFact` | Operation | The request to append one extracted fact version associated with captured research. | [operations.md](operations.md#appendresearchfact) |
| AppendReferenceProbeLineage | `agent-provenance-telemetry.AppendReferenceProbeLineage` | Operation | The request to append a committed probe recommendation's typed research lineage. | [operations.md](operations.md#appendreferenceprobelineage) |
| SessionRecord | `agent-provenance-telemetry.SessionRecord` | Query | The as-of read model for one Session and its derived activity summaries. | [queries.md](queries.md#sessionrecord) |
| DispatchScopeProjection | `agent-provenance-telemetry.DispatchScopeProjection` | Query | The as-of read model combining a pinned Dispatch authority snapshot with derived APT relationships. | [queries.md](queries.md#dispatchscopeprojection) |
| ResearchRecord | `agent-provenance-telemetry.ResearchRecord` | Query | The as-of read model of one ResearchCapture and its current extracted facts. | [queries.md](queries.md#researchrecord) |
| ProvenanceAppendPort | `agent-provenance-telemetry.ProvenanceAppendPort` | Interface | The APT application boundary through which validated facts are submitted to subordinate durable acceptance. | [interfaces.md](interfaces.md#provenanceappendport) |
| ProvenanceQueryPort | `agent-provenance-telemetry.ProvenanceQueryPort` | Interface | The read-only APT application boundary for explicit-offset provenance projections. | [interfaces.md](interfaces.md#provenancequeryport) |
| APTFactToACIEvent | `agent-provenance-telemetry.APTFactToACIEvent` | Mapping | The shape transformation from one validated APT fact to one ACI event payload. | [mappings.md](mappings.md#aptfacttoacievent) |
| ProbeBundleToReferenceLineage | `agent-provenance-telemetry.ProbeBundleToReferenceLineage` | Mapping | The shape transformation from committed probe evidence to typed research reference lineage. | [mappings.md](mappings.md#probebundletoreferencelineage) |
| ProvenanceFactsToReadModels | `agent-provenance-telemetry.ProvenanceFactsToReadModels` | Mapping | The deterministic transformation from accepted provenance facts to Session, Dispatch and Research query shapes. | [mappings.md](mappings.md#provenancefactstoreadmodels) |
| StartOrReuseSession | `agent-provenance-telemetry.StartOrReuseSession` | Workflow | The bounded coordination that resolves whether a context reuses or establishes a Session. | [workflows.md](workflows.md#startorreusesession) |
| CaptureAndEnrichResearch | `agent-provenance-telemetry.CaptureAndEnrichResearch` | Workflow | The bounded coordination that preserves a capture outcome before appending its structured extractions. | [workflows.md](workflows.md#captureandenrichresearch) |
| IngestReferenceProbeLineage | `agent-provenance-telemetry.IngestReferenceProbeLineage` | Workflow | The bounded coordination that binds committed probe evidence to research reference facts. | [workflows.md](workflows.md#ingestreferenceprobelineage) |
| SingleJoinAuthorityRule | `agent-provenance-telemetry.SingleJoinAuthorityRule` | Rule | The constraint that each relationship type has one authoritative persisted direction. | [rules.md](rules.md#apt-r1--single-join-authority) |
| IdempotentAppendRule | `agent-provenance-telemetry.IdempotentAppendRule` | Rule | The constraint that one operation identity and content digest denote one accepted append result. | [rules.md](rules.md#apt-r2--idempotent-append) |
| ArtifactOnlyRawReturnRule | `agent-provenance-telemetry.ArtifactOnlyRawReturnRule` | Rule | The conditional raw-return cardinality and artifact-reference constraint for each CaptureStatus. | [rules.md](rules.md#apt-r3--artifact-only-raw-return) |
| ExtractionProvenanceRule | `agent-provenance-telemetry.ExtractionProvenanceRule` | Rule | The constraint that extracted structure retains actor, method and exact captured-evidence selection. | [rules.md](rules.md#apt-r4--extraction-provenance) |
| CaptureSupersessionRule | `agent-provenance-telemetry.CaptureSupersessionRule` | Rule | The constraint governing predecessor-linked replacement of a current ResearchCapture. | [rules.md](rules.md#apt-r5--capture-supersession) |
| ReplayDeterminismRule | `agent-provenance-telemetry.ReplayDeterminismRule` | Rule | The constraint that an as-of projection is reproducible from pinned accepted evidence without external effects. | [rules.md](rules.md#apt-r6--replay-determinism) |
| ProtocolProfileBindingRule | `agent-provenance-telemetry.ProtocolProfileBindingRule` | Rule | The constraint that probe-origin lineage names the exact registered ACI protocol profile. | [rules.md](rules.md#apt-r7--protocol-profile-binding) |
| TelemetryNonAuthorityRule | `agent-provenance-telemetry.TelemetryNonAuthorityRule` | Rule | The constraint that logs, traces, metrics and projections do not become mutation authority. | [rules.md](rules.md#apt-r8--telemetry-non-authority) |
| SessionStarted | `agent-provenance-telemetry.SessionStarted` | Event | The accepted fact announcing creation of one Session identity. | [events.md](events.md#sessionstarted) |
| SessionContextRebound | `agent-provenance-telemetry.SessionContextRebound` | Event | The accepted fact announcing that an originating context is bound to a successor Session. | [events.md](events.md#sessioncontextrebound) |
| SessionDispatchLinked | `agent-provenance-telemetry.SessionDispatchLinked` | Event | The accepted fact announcing the authoritative Session membership of a Dispatch. | [events.md](events.md#sessiondispatchlinked) |
| ResearchCaptureAppended | `agent-provenance-telemetry.ResearchCaptureAppended` | Event | The accepted fact announcing persistence of one immutable ResearchCapture. | [events.md](events.md#researchcaptureappended) |
| ResearchFactAppended | `agent-provenance-telemetry.ResearchFactAppended` | Event | The accepted fact announcing persistence of one extracted research-fact version. | [events.md](events.md#researchfactappended) |
| ReferenceProbeLineageAppended | `agent-provenance-telemetry.ReferenceProbeLineageAppended` | Event | The accepted fact announcing persistence of one committed probe-lineage batch member. | [events.md](events.md#referenceprobelineageappended) |

## Cross-Feature Terms

These terms remain external; listing them does not add them to the APT Concept Registry or transfer
their ownership.

| Term | Concept ID | Type | Definition | Source |
|---|---|---|---|---|
| SourceObservation | `host.SourceObservation` | Event | Host-owned evidence about mediated source acquisition or access that APT may reference optionally. | [Focused discovery](../discovery/session-dispatch-research-records.md#43-reference-uses-and-checks) |
| ConfirmedDispatch | `agents-communication-infra.ConfirmedDispatch` | Entity | The ACI-owned frozen dispatch authority whose identity/snapshot APT reads without redefining it. | [ACI domain](../../agents-communication-infra/specs/domain.md#confirmeddispatch) |
| Artifact | `agents-communication-infra.Artifact` | Entity | The ACI-owned finalized evidence identity referenced by APT ArtifactReference values. | [ACI domain](../../agents-communication-infra/specs/domain.md#artifact) |
| RuntimeEventEnvelope | `agents-communication-infra.RuntimeEventEnvelope` | Value Object | The ACI-owned canonical envelope carrying an accepted APT event payload. | [ACI domain](../../agents-communication-infra/specs/domain.md#runtimeeventenvelope) |
| PublicationReceipt | `agents-communication-infra.PublicationReceipt` | Value Object | The ACI-owned durable publication evidence used when probe-origin lineage is bound. | [ACI domain](../../agents-communication-infra/specs/domain.md#publicationreceipt) |
| EventJournal | `agents-communication-infra.EventJournal` | Interface | The ACI-owned journal interface behind APT's subordinate append adapter. | [ACI interfaces](../../agents-communication-infra/specs/interfaces.md#internal-eventjournal) |
| ArtifactBoundary | `agents-communication-infra.ArtifactBoundary` | Interface | The ACI-owned finalization boundary hiding any physical artifact backend from APT. | [ACI interfaces](../../agents-communication-infra/specs/interfaces.md#internal-artifact-boundary) |

## Validation Status

- Concept Registry coverage: `58/58`.
- Concept IDs and DomainSpec meta-types: matched to [SPEC.md](SPEC.md#concept-registry).
- Duplicate formal terms/IDs: none.
- Existing external source paths: validated.
- APT aspect anchors: validated at the individual file gates across `domain.md`, `operations.md`,
  `queries.md`, `interfaces.md`, `mappings.md`, `workflows.md`, `rules.md` and `events.md`;
  corpus-wide no-objection receipt remains outstanding.

## Maintenance Rules

- Use Feature Language for important embedded words that readers need before formal concepts.
- Derive every formal row from the SPEC Concept Registry and reviewed aspect registries.
- Keep definitions explanatory and non-normative.
- Update this glossary whenever a concept name, ID, type, source anchor or definition changes.
- Do not introduce canonical behavior here; change the authoritative aspect first.
