# Test Spec (engine-derived): agent-provenance-telemetry

<!-- ENGINE-PROVENANCE
format_version: 1
feature: agent-provenance-telemetry
engine_commit: 5cc5a4e
inputs:
  domain.md: sha256:0f7678c1aad3a8d55d3c5e0b713a2121a9027185d583acc61ddd6264aca5a862
  events.md: sha256:d08bb11bbd5cdd62a78b97352be0fb24720417ff050422c51836c988aa054721
  interfaces.md: sha256:b0017f17a304236703e0c923095cc94f315a4bca1da430a75741dd79c3b2c089
  mappings.md: sha256:38b67755fa546a371a96bfbd2fbb2f8af9de8648c91e5a62c54f38b5b9c18074
  operations.md: sha256:931582aceb6000a83dc63901c00ae71467d98ee7c5ab0accb6797973d3afb26f
  queries.md: sha256:b09c593a3c9bc46788e08816bad4bf6ed74f6bd778b684ca8b14ea9d5758c796
  rules.md: sha256:badaa0f9de92b06e795260e2304abb450ff9f9613fa4a1d1ec685d26fcc23c95
  states.md: sha256:89e4c8e93e8c4f273945f7384bd1315472c4c674c08ad9658d5a24c14d26059d
  workflows.md: sha256:f5841cbf16ee36ceb80e8d15ae7d643e30928f0a64d9bf01610e369a047a834f
note: the ENGINE-REGION below is deterministic δ output, replaced wholesale on
      re-derive. Do not hand-edit it. Run `check` to detect drift.
-->

<!-- ENGINE-REGION-START — deterministic δ output; overwritten on re-derive, do not hand-edit -->

## Source Completeness Gate

| Doc | Status |
| --- | --- |
| states.md | present |
| operations.md | present |
| interfaces.md | present |
| events.md | present |
| workflows.md | present |
| queries.md | present |
| mappings.md | present |
| domain.md | present |
| rules.md | present |

## Coverage Summary

Total obligations: 379
Spec-formalization metric (pure / (pure + needs_formal)): 10.2%

| Tier | Count |
| --- | --- |
| derivable-needs-harness | 291 |
| derivable-pure | 9 |
| needs-formal | 79 |

| Rule class | Count |
| --- | --- |
| calculation | 9 |
| domain-enum | 8 |
| domain-field | 144 |
| error-obligation | 56 |
| event-obligation | 29 |
| invalid-transition | 12 |
| mapping-row | 6 |
| needs-formal | 79 |
| query-behavior | 4 |
| valid-transition | 4 |
| workflow-step | 28 |

## Suite Partition

- Unit (derivable-pure): 9
- Integration (derivable-needs-harness): 291
- Unresolved (needs-formal): 79

## Obligations

| ID | Key | Rule | Tier | Source | Obligation |
| --- | --- | --- | --- | --- | --- |
| APT-EVT-001 | 0257f1a8 | event-obligation | derivable-needs-harness | events.md#ResearchCaptureAppended:consumer:1 | Event ResearchCaptureAppended consumed by Planned ResearchRecord projection |
| APT-EVT-002 | 02db870d | event-obligation | derivable-needs-harness | events.md#ResearchFactAppended | Event ResearchFactAppended is emitted with valid payload |
| APT-NF-001 | 038829fe | needs-formal | needs-formal | operations.md#AppendResearchCapture:rule:0 | Rule APT-OP-CAP-1: needs_formal (prose Formal) |
| APT-ERR-001 | 04b66ac2 | error-obligation | derivable-needs-harness | operations.md#AppendResearchCapture:errorstate:6 | Error mapping for AppendResearchCapture: "Stale, unknown, cross-chain, self or cyclic predecessor" -> `CAPTURE_CAS_CONFLICT`; append nothing. |
| APT-WF-001 | 04b73811 | workflow-step | derivable-needs-harness | workflows.md#StartOrReuseSession:step:5 | Workflow StartOrReuseSession step 6 (Evaluate link decision) succeeds |
| APT-DOM-001 | 062ec390 | domain-field | derivable-needs-harness | domain.md#ResearchProblem:field:2 | ResearchProblem.fact: [FactEnvelope](#factenvelope) |
| APT-NF-002 | 07191df1 | needs-formal | needs-formal | operations.md#LinkSessionDispatch:calculation:0 | Calculation APT-OP-LINK-C1: needs_formal |
| APT-NF-003 | 07a16460 | needs-formal | needs-formal | operations.md#EnsureSession:rule:4 | Rule APT-OP-ENS-5: needs_formal (prose Formal) |
| APT-NF-004 | 094d9b2a | needs-formal | needs-formal | operations.md#AppendResearchCapture:rule:4 | Rule APT-OP-CAP-5: needs_formal (prose Formal) |
| APT-MAP-001 | 09e98f24 | mapping-row | derivable-needs-harness | mappings.md#ProvenanceFactsToReadModels | Mapping ProvenanceFactsToReadModels (closed Query intents and owner manifests from -> the four [deterministic Query results](queries.md)) maps all fields correctly |
| APT-DOM-002 | 0a905f61 | domain-field | derivable-needs-harness | domain.md#ResearchQuestion:field:2 | ResearchQuestion.fact: [FactEnvelope](#factenvelope) |
| APT-ERR-002 | 0ae8689e | error-obligation | derivable-needs-harness | operations.md#LinkSessionDispatch:errorstate:2 | Error mapping for LinkSessionDispatch: "Actor/action authorization missing, stale or digest-mismatched" -> `LINK_UNAUTHORIZED`; append nothing. |
| APT-DOM-003 | 0b09327e | domain-field | derivable-needs-harness | domain.md#DispatchAuthoritySnapshotRef:field:5 | DispatchAuthoritySnapshotRef.accepted_offset: non-negative integer (Required only for `aci_managed`.) |
| APT-TR-001 | 0b26f9ed | valid-transition | derivable-needs-harness | states.md#Research Capture Currentness:transition:0 | Transition no head for chain --grouped initial `ResearchCaptureAppended`--> new capture is head succeeds when guarded |
| APT-DOM-004 | 0c3b482a | domain-field | derivable-needs-harness | domain.md#DispatchAuthoritySnapshotRef:field:2 | DispatchAuthoritySnapshotRef.artifact_ref: external ACI artifact ref (Required only for `aci_managed`.) |
| APT-ERR-003 | 0cdfd6da | error-obligation | derivable-needs-harness | operations.md#LinkSessionDispatch:errorstate:7 | Error mapping for LinkSessionDispatch: "Historical Session linking or legacy backfill attempt" -> `BACKFILL_UNSUPPORTED_L0`; append nothing. |
| APT-NF-005 | 0d2b4c63 | needs-formal | needs-formal | operations.md#AppendReferenceProbeLineage:rule:7 | Rule APT-OP-PROBE-8: needs_formal (prose Formal) |
| APT-EVT-003 | 0f1fbad0 | event-obligation | derivable-needs-harness | events.md#ResearchFactAppended:consumer:1 | Event ResearchFactAppended consumed by Disposition/assessment reducers |
| APT-TR-002 | 0f692562 | invalid-transition | derivable-needs-harness | states.md#Research Capture Currentness:invalid:replacement is head; predecessor is derived superseded:grouped initial `ResearchCaptureAppended` | Event grouped initial `ResearchCaptureAppended` in state replacement is head; predecessor is derived superseded is rejected (no valid transition) |
| APT-DOM-005 | 0fb0a59e | domain-field | derivable-needs-harness | domain.md#ResearchCapture:field:4 | ResearchCapture.dispatch_id: external Dispatch ID |
| APT-DOM-006 | 0febf9fe | domain-field | derivable-needs-harness | domain.md#ResearchReferenceUse:field:5 | ResearchReferenceUse.locator_observed: string |
| APT-DOM-007 | 119a6780 | domain-field | derivable-needs-harness | domain.md#ResearchClaimExtraction:field:4 | ResearchClaimExtraction.answer_ids: canonical sorted set of [ResearchAnswer](#researchanswer).`research_answer_id` |
| APT-DOM-008 | 11c2d0b7 | domain-field | derivable-needs-harness | domain.md#ResearchProblem:field:7 | ResearchProblem.extraction: [ExtractionProvenance](#extractionprovenance) |
| APT-DOM-009 | 1207fc67 | domain-field | derivable-needs-harness | domain.md#ResearchReferenceClaimRelation:field:1 | ResearchReferenceClaimRelation.research_capture_id: [ResearchCapture](#researchcapture).`research_capture_id` |
| APT-NF-006 | 14cdac4a | needs-formal | needs-formal | operations.md#StartNewSession:rule:4 | Rule APT-OP-ROL-5: needs_formal (prose Formal) |
| APT-EVT-004 | 14d2a0c7 | event-obligation | derivable-needs-harness | events.md#ResearchCaptureAppended | Event ResearchCaptureAppended is emitted with valid payload |
| APT-DOM-010 | 15dacbac | domain-field | derivable-needs-harness | domain.md#ResearchReferenceUse:field:2 | ResearchReferenceUse.fact: [FactEnvelope](#factenvelope) |
| APT-TR-003 | 1602249f | invalid-transition | derivable-needs-harness | states.md#Session Context Binding:invalid:bound to new Session:authorized `StartNewSession` atomic acceptance | Event authorized `StartNewSession` atomic acceptance in state bound to new Session is rejected (no valid transition) |
| APT-ERR-004 | 166ff06d | error-obligation | derivable-needs-harness | operations.md#LinkSessionDispatch:errorstate:4 | Error mapping for LinkSessionDispatch: "Dispatch already linked contradictorily" -> `JOIN_CONFLICT`; append nothing. |
| APT-ERR-005 | 171dceb4 | error-obligation | derivable-needs-harness | operations.md#AppendReferenceProbeLineage:errorstate:12 | Error mapping for AppendReferenceProbeLineage: "Atomic grouping profile absent/mismatched" -> `ATOMIC_PROFILE_UNAVAILABLE`; operation remains blocked. |
| APT-ERR-006 | 183a0d60 | error-obligation | derivable-needs-harness | operations.md#StartNewSession:errorstate:5 | Error mapping for StartNewSession: "Same `command_identity(op)` with changed group digest" -> `IDEMPOTENCY_CONFLICT`; append nothing. |
| APT-ERR-007 | 1b642b24 | error-obligation | derivable-needs-harness | operations.md#AppendResearchFact:errorstate:3 | Error mapping for AppendResearchFact: "Empty/out-of-bounds/multibyte-split selector or digest/media/charset mismatch" -> `SELECTOR_INVALID`; append nothing. |
| APT-TR-004 | 1c2442e7 | valid-transition | derivable-needs-harness | states.md#Research Capture Currentness:transition:1 | Transition current head --grouped replacement `ResearchCaptureAppended`--> replacement is head; predecessor is derived superseded succeeds when guarded |
| APT-ERR-008 | 1c2cfe18 | error-obligation | derivable-needs-harness | operations.md#LinkSessionDispatch:errorstate:1 | Error mapping for LinkSessionDispatch: "Session is not the current exact origin-tuple binding" -> `SESSION_BINDING_STALE`; append nothing. |
| APT-EVT-005 | 1cb5cffe | event-obligation | derivable-needs-harness | events.md#ReferenceProbeLineageAppended:consumer:0 | Event ReferenceProbeLineageAppended consumed by Probe-delivery head reducer |
| APT-DOM-011 | 1d0a2e4a | domain-field | derivable-needs-harness | domain.md#ProbeRecommendationRef:field:4 | ProbeRecommendationRef.bundle_acceptance_ref: closed ACI acceptance ref (Accepted event or publication receipt plus contract version and evidence digest.) |
| APT-DOM-012 | 1d176bc5 | domain-field | derivable-needs-harness | domain.md#SessionDispatchLink:field:2 | SessionDispatchLink.dispatch_id: external Dispatch ID |
| APT-WF-002 | 1d6b9e2b | workflow-step | derivable-needs-harness | workflows.md#StartOrReuseSession:step:2 | Workflow StartOrReuseSession step 3 (Evaluate rollover decision) succeeds |
| APT-NF-007 | 202430ca | needs-formal | needs-formal | operations.md#AppendReferenceProbeLineage:rule:10 | Rule APT-OP-PROBE-11: needs_formal (prose Formal) |
| APT-DOM-013 | 20437ecc | domain-field | derivable-needs-harness | domain.md#DispatchAuthoritySnapshotRef:field:7 | DispatchAuthoritySnapshotRef.row_digest: [ContentDigest](#contentdigest) (Required only for `legacy_ledger`.) |
| APT-WF-003 | 204c22ec | workflow-step | derivable-needs-harness | workflows.md#StartOrReuseSession:step:0 | Workflow StartOrReuseSession step 1 (Bind invocation/context evidence) succeeds |
| APT-DOM-014 | 206531f4 | domain-field | derivable-needs-harness | domain.md#ResearchQuestion:field:1 | ResearchQuestion.research_capture_id: [ResearchCapture](#researchcapture).`research_capture_id` |
| APT-QRY-001 | 209af3e2 | query-behavior | derivable-needs-harness | queries.md#ResearchRecord | Query ResearchRecord returns its projected read model without side effects |
| APT-ENUM-001 | 213d70d8 | domain-enum | derivable-needs-harness | domain.md#ReferenceCheckKind:enum | ReferenceCheckKind vocabulary is exactly {source_identity,access_evidence,claim_support} |
| APT-DOM-015 | 22b6c29b | domain-field | derivable-needs-harness | domain.md#ResearchQuestion:field:5 | ResearchQuestion.extraction: [ExtractionProvenance](#extractionprovenance) |
| APT-DOM-016 | 2318c84c | domain-field | derivable-needs-harness | domain.md#ResearchCapture:field:1 | ResearchCapture.research_capture_id: opaque string |
| APT-EVT-006 | 23979e40 | event-obligation | derivable-needs-harness | events.md#ReferenceProbeLineageAppended | Event ReferenceProbeLineageAppended is emitted with valid payload |
| APT-DOM-017 | 23da730a | domain-field | derivable-needs-harness | domain.md#ResearchCapture:field:2 | ResearchCapture.expected_contribution_id: opaque string |
| APT-MAP-002 | 245149dc | mapping-row | derivable-needs-harness | mappings.md#APTFactToACIEvent | Mapping APTFactToACIEvent (validated bound command/candidate from the six -> exact APT event payload plus ACI-owned) maps all fields correctly |
| APT-DOM-018 | 249bccb5 | domain-field | derivable-needs-harness | domain.md#ACIProtocolProfileBinding:field:2 | ACIProtocolProfileBinding.protocol_profile_digest: [ContentDigest](#contentdigest) (Digest resolved by the ACI owner, never caller-authored authority.) |
| APT-WF-004 | 2564e514 | workflow-step | derivable-needs-harness | workflows.md#IngestReferenceProbeLineage:step:5 | Workflow IngestReferenceProbeLineage step 6 (Reconcile outcome) succeeds |
| APT-DOM-019 | 257a1570 | domain-field | derivable-needs-harness | domain.md#ResearchClaimExtraction:field:5 | ResearchClaimExtraction.extraction: [ExtractionProvenance](#extractionprovenance) |
| APT-ERR-009 | 26a0e74a | error-obligation | derivable-needs-harness | operations.md#AppendReferenceProbeLineage:errorstate:1 | Error mapping for AppendReferenceProbeLineage: "Profile registration/binding missing or mismatched" -> `PROFILE_BINDING_INVALID`; append no lineage. |
| APT-DOM-020 | 26a122a3 | domain-field | derivable-needs-harness | domain.md#ReferenceCheck:field:5 | ReferenceCheck.relation_id: [ResearchReferenceClaimRelation](#researchreferenceclaimrelation).`relation_id` |
| APT-CALC-001 | 27238065 | calculation | derivable-pure | operations.md#AppendResearchCapture:calculation:1 | Calculation APT-OP-CAP-C2: (dispatch_id,expected_contribution_id) |
| APT-EVT-007 | 29377114 | event-obligation | derivable-needs-harness | events.md#SessionDispatchLinked:consumer:2 | Event SessionDispatchLinked consumed by Research-capture application binder |
| APT-DOM-021 | 29bc1d52 | domain-field | derivable-needs-harness | domain.md#Session:field:1 | Session.origin_kind: string |
| APT-ERR-010 | 2a25cdb0 | error-obligation | derivable-needs-harness | operations.md#AppendResearchCapture:errorstate:8 | Error mapping for AppendResearchCapture: "Same `command_identity(op)` with different digest" -> `IDEMPOTENCY_CONFLICT`; append nothing. |
| APT-NF-008 | 2a79744b | needs-formal | needs-formal | operations.md#LinkSessionDispatch:rule:0 | Rule APT-OP-LINK-1: needs_formal (prose Formal) |
| APT-TR-005 | 2bcacc4a | valid-transition | derivable-needs-harness | states.md#Session Context Binding:transition:1 | Transition bound to predecessor --authorized `StartNewSession` atomic acceptance--> bound to successor succeeds when guarded |
| APT-MAP-003 | 2c2db8e4 | mapping-row | derivable-needs-harness | mappings.md#Fact Intent to Exact Payload and FactEnvelope | Mapping Fact Intent to Exact Payload and FactEnvelope (`apt.append-research-fact-intent@1` closed union in -> [AppendResearchFact](operations.md#appendresearchfact) bound command and exact) maps all fields correctly |
| APT-DOM-022 | 2ce6d2b3 | domain-field | derivable-needs-harness | domain.md#FormalizationCandidate:field:11 | FormalizationCandidate.extraction: [ExtractionProvenance](#extractionprovenance) |
| APT-EVT-008 | 2d6b67a6 | event-obligation | derivable-needs-harness | events.md#SessionStarted | Event SessionStarted is emitted with valid payload |
| APT-NF-009 | 2dbca5fa | needs-formal | needs-formal | operations.md#AppendResearchFact:rule:8 | Rule APT-OP-FACT-9: needs_formal (prose Formal) |
| APT-EVT-009 | 2e46a233 | event-obligation | derivable-needs-harness | events.md#ResearchFactAppended:consumer:3 | Event ResearchFactAppended consumed by Non-authoritative observability adapter |
| APT-WF-005 | 2e7c0413 | workflow-step | derivable-needs-harness | workflows.md#CaptureAndEnrichResearch:step:2 | Workflow CaptureAndEnrichResearch step 3 (Bind predecessor/synthesis pins) succeeds |
| APT-DOM-023 | 2fb0dfbb | domain-field | derivable-needs-harness | domain.md#ArtifactReference:field:4 | ArtifactReference.classification: external ACI classification value (Owner-stamped data class.) |
| APT-DOM-024 | 3038337e | domain-field | derivable-needs-harness | domain.md#FormalizationCandidate:field:4 | FormalizationCandidate.notation: string |
| APT-DOM-025 | 304f2210 | domain-field | derivable-needs-harness | domain.md#FormalizationCandidate:field:1 | FormalizationCandidate.research_capture_id: [ResearchCapture](#researchcapture).`research_capture_id` |
| APT-ENUM-002 | 30d04849 | domain-enum | derivable-needs-harness | domain.md#CaptureStatus:enum | CaptureStatus vocabulary is exactly {captured,partial,missing} |
| APT-NF-010 | 311f9d06 | needs-formal | needs-formal | operations.md#AppendReferenceProbeLineage:rule:1 | Rule APT-OP-PROBE-2: needs_formal (prose Formal) |
| APT-DOM-026 | 313c1bca | domain-field | derivable-needs-harness | domain.md#ArtifactReference:field:7 | ArtifactReference.tombstone_policy_ref: opaque external ref (Exact missing/erased-content behavior.) |
| APT-TR-006 | 317f08f0 | invalid-transition | derivable-needs-harness | states.md#Session Context Binding:invalid:unbound:authorized `StartNewSession` atomic acceptance | Event authorized `StartNewSession` atomic acceptance in state unbound is rejected (no valid transition) |
| APT-DOM-027 | 31901f49 | domain-field | derivable-needs-harness | domain.md#RawSelector:field:3 | RawSelector.end_exclusive: positive integer (Strictly greater than `start_inclusive`; at most the finalized raw byte length.) |
| APT-WF-006 | 31c1c629 | workflow-step | derivable-needs-harness | workflows.md#IngestReferenceProbeLineage:step:3 | Workflow IngestReferenceProbeLineage step 4 (Derive keys/order/dependencies) succeeds |
| APT-ERR-011 | 32302862 | error-obligation | derivable-needs-harness | operations.md#LinkSessionDispatch:errorstate:3 | Error mapping for LinkSessionDispatch: "Dispatch ID differs from either snapshot identity" -> `SNAPSHOT_IDENTITY_MISMATCH`; append nothing. |
| APT-DOM-028 | 32709474 | domain-field | derivable-needs-harness | domain.md#FormalizationCandidate:field:8 | FormalizationCandidate.logic_family: string |
| APT-DOM-029 | 32cfbbe9 | domain-field | derivable-needs-harness | domain.md#FormalizationCandidate:field:0 | FormalizationCandidate.formalization_id: opaque string |
| APT-DOM-030 | 338b027d | domain-field | derivable-needs-harness | domain.md#FormalizationCandidate:field:10 | FormalizationCandidate.scope: string |
| APT-DOM-031 | 34d6b600 | domain-field | derivable-needs-harness | domain.md#ResearchCapture:field:16 | ResearchCapture.capture_digest: [ContentDigest](#contentdigest) |
| APT-NF-011 | 3551bca7 | needs-formal | needs-formal | operations.md#LinkSessionDispatch:rule:2 | Rule APT-OP-LINK-3: needs_formal (prose Formal) |
| APT-NF-012 | 35893eda | needs-formal | needs-formal | operations.md#AppendReferenceProbeLineage:rule:14 | Rule APT-OP-PROBE-15: needs_formal (prose Formal) |
| APT-NF-013 | 36132ab0 | needs-formal | needs-formal | operations.md#AppendResearchFact:rule:7 | Rule APT-OP-FACT-8: needs_formal (prose Formal) |
| APT-DOM-032 | 3737cb9d | domain-field | derivable-needs-harness | domain.md#FormalizationCandidate:field:9 | FormalizationCandidate.assumptions: string list |
| APT-ERR-012 | 3cbde373 | error-obligation | derivable-needs-harness | operations.md#AppendResearchFact:errorstate:4 | Error mapping for AppendResearchFact: "Typed relation/check/formalization constraint fails or relational duplicate supplied" -> `FACT_TYPE_INVALID`; append nothing. |
| APT-DOM-033 | 3db19efc | domain-field | derivable-needs-harness | domain.md#ResearchProblem:field:3 | ResearchProblem.kind: constrained string |
| APT-ERR-013 | 3e5eed5c | error-obligation | derivable-needs-harness | operations.md#AppendResearchFact:errorstate:6 | Error mapping for AppendResearchFact: "Existing global fact ID has different canonical payload digest, `subject_id` or `supersedes_fact_id`" -> `FACT_IDENTITY_CONFLICT`; append nothing. |
| APT-NF-014 | 3ed9d9fe | needs-formal | needs-formal | states.md#Session Context Binding:invariant:4 | Invariant APT-STATE-I5: needs_formal (prose Formal) |
| APT-ERR-014 | 3eea00e2 | error-obligation | derivable-needs-harness | operations.md#AppendReferenceProbeLineage:errorstate:14 | Error mapping for AppendReferenceProbeLineage: "Partial/range/count/canonical-event-order/payload-digest grouping mismatch" -> `ATOMIC_GROUP_INVALID`; apply no lineage; bundle remains visible. |
| APT-DOM-034 | 3eea63a4 | domain-field | derivable-needs-harness | domain.md#ResearchReferenceClaimRelation:field:4 | ResearchReferenceClaimRelation.research_claim_id: [ResearchClaimExtraction](#researchclaimextraction).`research_claim_id` |
| APT-NF-015 | 3f502432 | needs-formal | needs-formal | operations.md#StartNewSession:rule:0 | Rule APT-OP-ROL-1: needs_formal (prose Formal) |
| APT-CALC-002 | 3fd3d9b8 | calculation | derivable-pure | operations.md#AppendResearchFact:calculation:3 | Calculation APT-OP-FACT-C4: H(raw_return.bytes[start:end]) = selected_text_digest |
| APT-EVT-010 | 40328d01 | event-obligation | derivable-needs-harness | events.md#SessionStarted:consumer:0 | Event SessionStarted consumed by Pure session-binding reducer |
| APT-DOM-035 | 4085cc7d | domain-field | derivable-needs-harness | domain.md#DispatchAuthoritySnapshotRef:field:6 | DispatchAuthoritySnapshotRef.ledger_row_identity: {dispatch_id, row_kind, appender_identity, contract_version} (Required only for `legacy_ledger`; contains the authoritative Dispatch identity.) |
| APT-NF-016 | 4195d1f1 | needs-formal | needs-formal | operations.md#AppendResearchFact:rule:2 | Rule APT-OP-FACT-3: needs_formal (prose Formal) |
| APT-CALC-003 | 41b2cf75 | calculation | derivable-pure | operations.md#AppendReferenceProbeLineage:calculation:4 | Calculation APT-OP-PROBE-C5: unique_key=fact_id; exact_tuple=(H_ACI(full_research_reference_use_payload),subject_id,fact.supersedes_fact_id) |
| APT-ERR-015 | 42201a21 | error-obligation | derivable-needs-harness | operations.md#EnsureSession:errorstate:3 | Error mapping for EnsureSession: "Caller-chosen or mismatched origin/context digest" -> `HOST_EVIDENCE_INVALID`; append nothing. |
| APT-NF-017 | 4240c646 | needs-formal | needs-formal | operations.md#EnsureSession:calculation:1 | Calculation APT-OP-ENS-C2: needs_formal |
| APT-TR-007 | 42b70519 | invalid-transition | derivable-needs-harness | states.md#Session Context Binding:invalid:bound to new Session:`EnsureSession` acceptance represented by grouped `SessionStarted` | Event `EnsureSession` acceptance represented by grouped `SessionStarted` in state bound to new Session is rejected (no valid transition) |
| APT-DOM-036 | 4313ea6d | domain-field | derivable-needs-harness | domain.md#RawSelector:field:4 | RawSelector.selected_text_digest: [ContentDigest](#contentdigest) (Digest of the exact selected byte slice.) |
| APT-NF-018 | 4335732a | needs-formal | needs-formal | operations.md#LinkSessionDispatch:rule:3 | Rule APT-OP-LINK-4: needs_formal (prose Formal) |
| APT-DOM-037 | 43a4c26a | domain-field | derivable-needs-harness | domain.md#Session:field:2 | Session.origin_ref: string |
| APT-DOM-038 | 4406b6e2 | domain-field | derivable-needs-harness | domain.md#DispatchAuthoritySnapshotRef:field:8 | DispatchAuthoritySnapshotRef.non_authoritative_locator: {row_index} (Optional only for `legacy_ledger`; lookup hint excluded from authority/hash.) |
| APT-NF-019 | 45385c00 | needs-formal | needs-formal | states.md#Research Capture Currentness:invariant:5 | Invariant APT-STATE-I12: needs_formal (prose Formal) |
| APT-DOM-039 | 459f315d | domain-field | derivable-needs-harness | domain.md#ReferenceCheck:field:3 | ReferenceCheck.check_kind: [ReferenceCheckKind](#referencecheckkind) |
| APT-ERR-016 | 467639c5 | error-obligation | derivable-needs-harness | operations.md#LinkSessionDispatch:errorstate:5 | Error mapping for LinkSessionDispatch: "Same `command_identity(op)` with changed payload digest" -> `IDEMPOTENCY_CONFLICT`; append nothing. |
| APT-ERR-017 | 4701ea92 | error-obligation | derivable-needs-harness | operations.md#StartNewSession:errorstate:1 | Error mapping for StartNewSession: "Expected Session is stale or belongs to another tuple" -> `BINDING_CAS_CONFLICT`; append neither event. |
| APT-NF-020 | 470d246e | needs-formal | needs-formal | operations.md#AppendResearchFact:rule:5 | Rule APT-OP-FACT-6: needs_formal (prose Formal) |
| APT-NF-021 | 4894d548 | needs-formal | needs-formal | states.md#Research Capture Currentness:invariant:0 | Invariant APT-STATE-I7: needs_formal (prose Formal) |
| APT-DOM-040 | 491f7677 | domain-field | derivable-needs-harness | domain.md#Session:field:5 | Session.started_at: offset timestamp |
| APT-NF-022 | 4935f75c | needs-formal | needs-formal | operations.md#EnsureSession:rule:1 | Rule APT-OP-ENS-2: needs_formal (prose Formal) |
| APT-QRY-002 | 499139d5 | query-behavior | derivable-needs-harness | queries.md#AgentReferenceLineage | Query AgentReferenceLineage returns its projected read model without side effects |
| APT-DOM-041 | 4e103c73 | domain-field | derivable-needs-harness | domain.md#ExtractionProvenance:field:1 | ExtractionProvenance.actor_ref: opaque actor ref (Producer, host parser or reviewer identity.) |
| APT-WF-007 | 4ee2dee3 | workflow-step | derivable-needs-harness | workflows.md#StartOrReuseSession:step:7 | Workflow StartOrReuseSession step 8 (Link current Session/Dispatch) succeeds |
| APT-DOM-042 | 4f029756 | domain-field | derivable-needs-harness | domain.md#ResearchProblem:field:4 | ResearchProblem.statement: string |
| APT-ERR-018 | 4f969080 | error-obligation | derivable-needs-harness | operations.md#AppendReferenceProbeLineage:errorstate:8 | Error mapping for AppendReferenceProbeLineage: "Extraction actor/mode/method/capture evidence is invalid or is overwritten with ingestion actor" -> `EXTRACTION_ATTRIBUTION_INVALID`; append nothing. |
| APT-DOM-043 | 505792c7 | domain-field | derivable-needs-harness | domain.md#Session:field:3 | Session.ensure_key: opaque string |
| APT-ERR-019 | 5092e6b0 | error-obligation | derivable-needs-harness | operations.md#AppendResearchFact:errorstate:9 | Error mapping for AppendResearchFact: "Disposition/assessment actor differs from authenticated owner-bound principal" -> `AGGREGATE_ACTOR_MISMATCH`; append nothing. |
| APT-DOM-044 | 509381bb | domain-field | derivable-needs-harness | domain.md#ExtractionProvenance:field:3 | ExtractionProvenance.extracted_at: offset timestamp (Owner-stamped extraction time.) |
| APT-NF-023 | 5099a118 | needs-formal | needs-formal | operations.md#AppendResearchFact:rule:6 | Rule APT-OP-FACT-7: needs_formal (prose Formal) |
| APT-MAP-004 | 50a5955a | mapping-row | derivable-needs-harness | mappings.md#Accepted ACI Events to Projection Rows | Mapping Accepted ACI Events to Projection Rows (complete verified accepted ACI command groups carrying the six -> pure reducer state in [states.md](states.md) and the four) maps all fields correctly |
| APT-ERR-020 | 50d7e45e | error-obligation | derivable-needs-harness | operations.md#EnsureSession:errorstate:5 | Error mapping for EnsureSession: "ACI append fails before durable acceptance" -> `APPEND_FAILED`; no success receipt. |
| APT-DOM-045 | 52cbeb9d | domain-field | derivable-needs-harness | domain.md#ACIProtocolProfileBinding:field:0 | ACIProtocolProfileBinding.protocol_profile_id: opaque external ACI profile ID (Exact registered profile.) |
| APT-DOM-046 | 52cc19b9 | domain-field | derivable-needs-harness | domain.md#Session:field:4 | Session.start_operation_id: opaque string |
| APT-NF-024 | 54be30cd | needs-formal | needs-formal | states.md#Session Context Binding:invariant:1 | Invariant APT-STATE-I2: needs_formal (prose Formal) |
| APT-DOM-047 | 54e62d14 | domain-field | derivable-needs-harness | domain.md#ReferenceCheck:field:4 | ReferenceCheck.reference_use_id: [ResearchReferenceUse](#researchreferenceuse).`reference_use_id` |
| APT-WF-008 | 5593708e | workflow-step | derivable-needs-harness | workflows.md#CaptureAndEnrichResearch:step:5 | Workflow CaptureAndEnrichResearch step 6 (Select fact family) succeeds |
| APT-NF-025 | 55df1893 | needs-formal | needs-formal | operations.md#AppendResearchFact:rule:1 | Rule APT-OP-FACT-2: needs_formal (prose Formal) |
| APT-QRY-003 | 56779fac | query-behavior | derivable-needs-harness | queries.md#SessionRecord | Query SessionRecord returns its projected read model without side effects |
| APT-DOM-048 | 57093b33 | domain-field | derivable-needs-harness | domain.md#ProbeRecommendationRef:field:3 | ProbeRecommendationRef.profile_binding: [ACIProtocolProfileBinding](#aciprotocolprofilebinding) (Required whenever this value exists.) |
| APT-DOM-049 | 575c42bf | domain-field | derivable-needs-harness | domain.md#SessionDispatchLink:field:3 | SessionDispatchLink.link_operation_id: opaque string |
| APT-ERR-021 | 5904e764 | error-obligation | derivable-needs-harness | operations.md#StartNewSession:errorstate:4 | Error mapping for StartNewSession: "Partial group, range/count/order/digest mismatch" -> `ATOMIC_GROUP_INVALID`; apply neither event. |
| APT-WF-009 | 592497bd | workflow-step | derivable-needs-harness | workflows.md#CaptureAndEnrichResearch:step:6 | Workflow CaptureAndEnrichResearch step 7 (Validate extraction-bearing Entity evidence) succeeds |
| APT-TR-008 | 5927516b | invalid-transition | derivable-needs-harness | states.md#Research Capture Currentness:invalid:replacement is head; predecessor is derived superseded:grouped replacement `ResearchCaptureAppended` | Event grouped replacement `ResearchCaptureAppended` in state replacement is head; predecessor is derived superseded is rejected (no valid transition) |
| APT-DOM-050 | 5927e826 | domain-field | derivable-needs-harness | domain.md#ResearchReferenceUse:field:1 | ResearchReferenceUse.research_capture_id: [ResearchCapture](#researchcapture).`research_capture_id` |
| APT-DOM-051 | 599da2ac | domain-field | derivable-needs-harness | domain.md#ResearchAnswer:field:1 | ResearchAnswer.research_capture_id: [ResearchCapture](#researchcapture).`research_capture_id` |
| APT-NF-026 | 5a14ecf0 | needs-formal | needs-formal | states.md#Session Context Binding:invariant:3 | Invariant APT-STATE-I4: needs_formal (prose Formal) |
| APT-ERR-022 | 5a3c1a7a | error-obligation | derivable-needs-harness | operations.md#StartNewSession:errorstate:0 | Error mapping for StartNewSession: "Unauthorized actor or invalid/mismatched pinned evidence" -> `ROLLOVER_UNAUTHORIZED`; append neither event. |
| APT-EVT-011 | 5a56d456 | event-obligation | derivable-needs-harness | events.md#ReferenceProbeLineageAppended:consumer:1 | Event ReferenceProbeLineageAppended consumed by Probe use-fact validator/reducer |
| APT-EVT-012 | 5acc0219 | event-obligation | derivable-needs-harness | events.md#ResearchCaptureAppended:consumer:0 | Event ResearchCaptureAppended consumed by Capture-currentness reducer |
| APT-DOM-052 | 5caf043b | domain-field | derivable-needs-harness | domain.md#ResearchCapture:field:5 | ResearchCapture.dispatch_snapshot_ref: [DispatchAuthoritySnapshotRef](#dispatchauthoritysnapshotref) |
| APT-DOM-053 | 5cb37d61 | domain-field | derivable-needs-harness | domain.md#ResearchClaimExtraction:field:0 | ResearchClaimExtraction.research_claim_id: opaque string |
| APT-NF-027 | 5cb5581d | needs-formal | needs-formal | states.md#Session Context Binding:invariant:7 | Invariant APT-STATE-I14: needs_formal (prose Formal) |
| APT-NF-028 | 5e22e8aa | needs-formal | needs-formal | operations.md#AppendReferenceProbeLineage:rule:9 | Rule APT-OP-PROBE-10: needs_formal (prose Formal) |
| APT-EVT-013 | 5fcd78ca | event-obligation | derivable-needs-harness | events.md#SessionContextRebound:consumer:0 | Event SessionContextRebound consumed by Pure session-binding reducer |
| APT-DOM-054 | 60c0abcf | domain-field | derivable-needs-harness | domain.md#RawSelector:field:2 | RawSelector.start_inclusive: non-negative integer (First selected byte.) |
| APT-DOM-055 | 60c4f62a | domain-field | derivable-needs-harness | domain.md#ArtifactReference:field:8 | ArtifactReference.finalization_receipt_ref: opaque ACI receipt ref (Evidence that the ACI boundary finalized the artifact reference.) |
| APT-TR-009 | 62cd09f2 | invalid-transition | derivable-needs-harness | states.md#Session Context Binding:invalid:bound to successor:authorized `StartNewSession` atomic acceptance | Event authorized `StartNewSession` atomic acceptance in state bound to successor is rejected (no valid transition) |
| APT-NF-029 | 64fca2ee | needs-formal | needs-formal | operations.md#AppendResearchFact:rule:10 | Rule APT-OP-FACT-11: needs_formal (prose Formal) |
| APT-NF-030 | 65a4fabd | needs-formal | needs-formal | operations.md#AppendReferenceProbeLineage:rule:5 | Rule APT-OP-PROBE-6: needs_formal (prose Formal) |
| APT-ERR-023 | 662a9696 | error-obligation | derivable-needs-harness | operations.md#AppendReferenceProbeLineage:errorstate:9 | Error mapping for AppendReferenceProbeLineage: "Use item references neither a current delivery nor a preceding delivery item in the group" -> `DELIVERY_ORIGIN_REQUIRED`; append nothing. |
| APT-CALC-004 | 66694a4a | calculation | derivable-pure | operations.md#AppendReferenceProbeLineage:calculation:6 | Calculation APT-OP-PROBE-C7: `result_by_request_key[k]={status: existing_exact |
| APT-CALC-005 | 68958e15 | calculation | derivable-pure | operations.md#AppendReferenceProbeLineage:calculation:5 | Calculation APT-OP-PROBE-C6: `H_ACI(canonical(canonical_request))` including exact-semantic-no-op items |
| APT-NF-031 | 691aedd4 | needs-formal | needs-formal | operations.md#EnsureSession:calculation:0 | Calculation APT-OP-ENS-C1: needs_formal |
| APT-ERR-024 | 692d14f8 | error-obligation | derivable-needs-harness | operations.md#AppendResearchFact:errorstate:7 | Error mapping for AppendResearchFact: "Required ACI transactional semantic-unique profile absent/mismatched" -> `SEMANTIC_REGISTRY_PROFILE_UNAVAILABLE`; implementation remains blocked. |
| APT-ERR-025 | 69de554d | error-obligation | derivable-needs-harness | operations.md#AppendResearchCapture:errorstate:3 | Error mapping for AppendResearchCapture: "Snapshot identity/version/digest mismatch" -> `DISPATCH_SNAPSHOT_INVALID`; append nothing. |
| APT-TR-010 | 69fd7f63 | invalid-transition | derivable-needs-harness | states.md#Research Capture Currentness:invalid:new capture is head:grouped replacement `ResearchCaptureAppended` | Event grouped replacement `ResearchCaptureAppended` in state new capture is head is rejected (no valid transition) |
| APT-ERR-026 | 6a58a363 | error-obligation | derivable-needs-harness | operations.md#StartNewSession:errorstate:3 | Error mapping for StartNewSession: "Atomic ACI profile absent/mismatched" -> `ATOMIC_PROFILE_UNAVAILABLE`; operation remains blocked. |
| APT-DOM-056 | 6b4ba93a | domain-field | derivable-needs-harness | domain.md#FormalizationCandidate:field:14 | FormalizationCandidate.governance_ref: opaque external ref |
| APT-WF-010 | 6b570242 | workflow-step | derivable-needs-harness | workflows.md#CaptureAndEnrichResearch:step:1 | Workflow CaptureAndEnrichResearch step 2 (Validate exact status/evidence branch) succeeds |
| APT-DOM-057 | 6cbf8164 | domain-field | derivable-needs-harness | domain.md#ResearchCapture:field:13 | ResearchCapture.supersedes_capture_id: [ResearchCapture](#researchcapture).`research_capture_id` or null |
| APT-ERR-027 | 6e2b33b1 | error-obligation | derivable-needs-harness | operations.md#AppendReferenceProbeLineage:errorstate:13 | Error mapping for AppendReferenceProbeLineage: "ACI journal transactional semantic-unique/result-mapping profile absent or mismatched" -> `SEMANTIC_REGISTRY_PROFILE_UNAVAILABLE`; implementation remains blocked. |
| APT-NF-032 | 6ecf1673 | needs-formal | needs-formal | operations.md#AppendResearchCapture:rule:6 | Rule APT-OP-CAP-7: needs_formal (prose Formal) |
| APT-DOM-058 | 6f819766 | domain-field | derivable-needs-harness | domain.md#ResearchCapture:field:9 | ResearchCapture.raw_return: [ArtifactReference](#artifactreference) or null |
| APT-ENUM-003 | 70f2966a | domain-enum | derivable-needs-harness | domain.md#ReferenceUseKind:enum | ReferenceUseKind vocabulary is exactly {mentioned,cited,claimed_consulted} |
| APT-DOM-059 | 71419658 | domain-field | derivable-needs-harness | domain.md#ResearchCapture:field:10 | ResearchCapture.partial_reason: non-empty string or null |
| APT-NF-033 | 719f03ff | needs-formal | needs-formal | operations.md#AppendResearchFact:rule:3 | Rule APT-OP-FACT-4: needs_formal (prose Formal) |
| APT-DOM-060 | 71b95153 | domain-field | derivable-needs-harness | domain.md#FormalizationCandidate:field:6 | FormalizationCandidate.legend: string-to-string map |
| APT-MAP-005 | 71ff9d21 | mapping-row | derivable-needs-harness | mappings.md#ProbeBundleToReferenceLineage | Mapping ProbeBundleToReferenceLineage (closed probe lineage intent and owner-bound items from -> submitted ACI event group plus [ProbeAppendOutcome](interfaces.md#probeappendoutcome)) maps all fields correctly |
| APT-DOM-061 | 725c04c3 | domain-field | derivable-needs-harness | domain.md#ResearchClaimExtraction:field:3 | ResearchClaimExtraction.statement: string |
| APT-NF-034 | 73275b98 | needs-formal | needs-formal | operations.md#AppendReferenceProbeLineage:rule:8 | Rule APT-OP-PROBE-9: needs_formal (prose Formal) |
| APT-NF-035 | 74702927 | needs-formal | needs-formal | operations.md#AppendResearchFact:rule:4 | Rule APT-OP-FACT-5: needs_formal (prose Formal) |
| APT-NF-036 | 74e287ef | needs-formal | needs-formal | operations.md#AppendReferenceProbeLineage:rule:0 | Rule APT-OP-PROBE-1: needs_formal (prose Formal) |
| APT-ERR-028 | 75f5bd43 | error-obligation | derivable-needs-harness | operations.md#AppendReferenceProbeLineage:errorstate:7 | Error mapping for AppendReferenceProbeLineage: "Delivery/event actor differs from authenticated ingestion principal" -> `LINEAGE_ACTOR_MISMATCH`; append nothing. |
| APT-DOM-062 | 77b6d3f5 | domain-field | derivable-needs-harness | domain.md#ResearchReferenceUse:field:0 | ResearchReferenceUse.reference_use_id: opaque string |
| APT-TR-011 | 77eedcbe | invalid-transition | derivable-needs-harness | states.md#Research Capture Currentness:invalid:new capture is head:grouped initial `ResearchCaptureAppended` | Event grouped initial `ResearchCaptureAppended` in state new capture is head is rejected (no valid transition) |
| APT-ERR-029 | 78584433 | error-obligation | derivable-needs-harness | operations.md#AppendReferenceProbeLineage:errorstate:2 | Error mapping for AppendReferenceProbeLineage: "Host observation/evidence dangling, stale or digest-mismatched" -> `HOST_EVIDENCE_INVALID`; append no lineage. |
| APT-ERR-030 | 791d6a5f | error-obligation | derivable-needs-harness | operations.md#AppendResearchFact:errorstate:2 | Error mapping for AppendResearchFact: "Missing capture, `missing` capture, cross-capture edge or stale snapshot" -> `FACT_LOCALITY_INVALID`; append nothing. |
| APT-NF-037 | 791f7bce | needs-formal | needs-formal | operations.md#AppendReferenceProbeLineage:rule:2 | Rule APT-OP-PROBE-3: needs_formal (prose Formal) |
| APT-ERR-031 | 7955ab22 | error-obligation | derivable-needs-harness | operations.md#EnsureSession:errorstate:2 | Error mapping for EnsureSession: "Origin tuple already bound" -> Reuse current immutable Session and expose its existing name; no error/event/rename. |
| APT-DOM-063 | 796e483c | domain-field | derivable-needs-harness | domain.md#ArtifactReference:field:1 | ArtifactReference.content_digest: [ContentDigest](#contentdigest) (Digest verified at finalization.) |
| APT-NF-038 | 79a8ba1d | needs-formal | needs-formal | states.md#Research Capture Currentness:invariant:4 | Invariant APT-STATE-I11: needs_formal (prose Formal) |
| APT-DOM-064 | 7bfdc0dc | domain-field | derivable-needs-harness | domain.md#ResearchProblem:field:1 | ResearchProblem.research_capture_id: [ResearchCapture](#researchcapture).`research_capture_id` |
| APT-ENUM-004 | 7c3760fa | domain-enum | derivable-needs-harness | domain.md#ProblemDisposition:enum | ProblemDisposition vocabulary is exactly {observed,validated,resolved,accepted_risk,refuted} |
| APT-ERR-032 | 7c85a3f1 | error-obligation | derivable-needs-harness | operations.md#AppendResearchCapture:errorstate:5 | Error mapping for AppendResearchCapture: "Legacy unlinked capture/backfill attempt" -> `BACKFILL_UNSUPPORTED_L0`; append nothing; legacy data remains read-only. |
| APT-NF-039 | 7d6c53ac | needs-formal | needs-formal | operations.md#AppendReferenceProbeLineage:rule:11 | Rule APT-OP-PROBE-12: needs_formal (prose Formal) |
| APT-DOM-065 | 7e9fce0b | domain-field | derivable-needs-harness | domain.md#ResearchQuestion:field:3 | ResearchQuestion.question_text: string |
| APT-DOM-066 | 7ffa6c12 | domain-field | derivable-needs-harness | domain.md#ExtractionProvenance:field:2 | ExtractionProvenance.method_ref: string (Extractor name and version.) |
| APT-CALC-006 | 8029db3d | calculation | derivable-pure | operations.md#AppendReferenceProbeLineage:calculation:3 | Calculation APT-OP-PROBE-C4: `H_ACI([canonical_payload_preimage(new_event₀),...,canonical_payload_preimage(new_eventₙ)])` in canonical item order |
| APT-ENUM-005 | 8067b399 | domain-enum | derivable-needs-harness | domain.md#FormalizationDisposition:enum | FormalizationDisposition vocabulary is exactly {candidate,reviewed,rejected} |
| APT-MAP-006 | 8174fc23 | mapping-row | derivable-needs-harness | mappings.md#Caller Intents to Bound Commands | Mapping Caller Intents to Bound Commands (closed mutation caller intents in -> closed application bound commands in) maps all fields correctly |
| APT-ERR-033 | 81bcc1b7 | error-obligation | derivable-needs-harness | operations.md#AppendResearchFact:errorstate:1 | Error mapping for AppendResearchFact: "Entity variant carries aggregate CAS, or disposition/assessment carries FactEnvelope/fact CAS" -> `FACT_VARIANT_BINDING_INVALID`; append nothing. |
| APT-NF-040 | 825dce5c | needs-formal | needs-formal | operations.md#AppendResearchFact:rule:11 | Rule APT-OP-FACT-12: needs_formal (prose Formal) |
| APT-NF-041 | 82de877a | needs-formal | needs-formal | operations.md#AppendReferenceProbeLineage:rule:6 | Rule APT-OP-PROBE-7: needs_formal (prose Formal) |
| APT-DOM-067 | 82f0b499 | domain-field | derivable-needs-harness | domain.md#ResearchCapture:field:12 | ResearchCapture.failure_evidence_ref: [FailureEvidenceRef embedded union](#failureevidenceref-embedded-union) or null |
| APT-DOM-068 | 8300fe8e | domain-field | derivable-needs-harness | domain.md#ResearchReferenceClaimRelation:field:5 | ResearchReferenceClaimRelation.relation: constrained string |
| APT-ERR-034 | 83122c78 | error-obligation | derivable-needs-harness | operations.md#StartNewSession:errorstate:2 | Error mapping for StartNewSession: "Successor identity reused, self-successor or origin tuple differs" -> `SUCCESSOR_INVALID`; append neither event. |
| APT-WF-011 | 833580f3 | workflow-step | derivable-needs-harness | workflows.md#CaptureAndEnrichResearch:step:9 | Workflow CaptureAndEnrichResearch step 10 (Append one fact/assessment/disposition) succeeds |
| APT-DOM-069 | 839f7ab3 | domain-field | derivable-needs-harness | domain.md#FactEnvelope:field:0 | FactEnvelope.fact_id: opaque string (Immutable identity of one accepted fact version.) |
| APT-EVT-014 | 842c8ea1 | event-obligation | derivable-needs-harness | events.md#SessionDispatchLinked | Event SessionDispatchLinked is emitted with valid payload |
| APT-DOM-070 | 85ed2e38 | domain-field | derivable-needs-harness | domain.md#FormalizationCandidate:field:12 | FormalizationCandidate.syntax_checker_ref: opaque external ref |
| APT-NF-042 | 8616acb6 | needs-formal | needs-formal | operations.md#EnsureSession:rule:3 | Rule APT-OP-ENS-4: needs_formal (prose Formal) |
| APT-NF-043 | 86b75237 | needs-formal | needs-formal | operations.md#LinkSessionDispatch:rule:4 | Rule APT-OP-LINK-5: needs_formal (prose Formal) |
| APT-WF-012 | 87328aba | workflow-step | derivable-needs-harness | workflows.md#IngestReferenceProbeLineage:step:1 | Workflow IngestReferenceProbeLineage step 2 (Verify recommendation/profile) succeeds |
| APT-ENUM-006 | 888a2232 | domain-enum | derivable-needs-harness | domain.md#ClaimDisposition:enum | ClaimDisposition vocabulary is exactly {proposed,supported,contested,refuted} |
| APT-DOM-071 | 894379d4 | domain-field | derivable-needs-harness | domain.md#ACIProtocolProfileBinding:field:1 | ACIProtocolProfileBinding.protocol_profile_version: string (Exact registered version.) |
| APT-NF-044 | 8aa691b7 | needs-formal | needs-formal | operations.md#AppendResearchFact:calculation:0 | Calculation APT-OP-FACT-C1: needs_formal |
| APT-ERR-035 | 8c112f2c | error-obligation | derivable-needs-harness | operations.md#AppendResearchFact:errorstate:5 | Error mapping for AppendResearchFact: "Fact predecessor stale/unknown/cross-subject/cyclic" -> `FACT_CAS_CONFLICT`; append nothing. |
| APT-DOM-072 | 8dab5688 | domain-field | derivable-needs-harness | domain.md#ResearchCapture:field:6 | ResearchCapture.origin_refs: canonical sorted set of [OriginRef embedded union](#originref-embedded-union) |
| APT-DOM-073 | 8e8e73f8 | domain-field | derivable-needs-harness | domain.md#ArtifactReference:field:3 | ArtifactReference.charset: string or null (Fixed to `utf-8` for an L0 `raw_return`; null only for artifacts outside the L0 capture path.) |
| APT-DOM-074 | 8f67541c | domain-field | derivable-needs-harness | domain.md#FactEnvelope:field:4 | FactEnvelope.supersedes_fact_id: opaque string or null (When present, names the current predecessor for the same subject.) |
| APT-DOM-075 | 8f8ccaa9 | domain-field | derivable-needs-harness | domain.md#ProbeRecommendationRef:field:5 | ProbeRecommendationRef.profile_registration_ref: closed ACI registry ref (Registry event or receipt plus the exact profile ID, version and digest.) |
| APT-DOM-076 | 8fbdcd58 | domain-field | derivable-needs-harness | domain.md#ResearchCapture:field:15 | ResearchCapture.captured_at: offset timestamp |
| APT-DOM-077 | 904a8f94 | domain-field | derivable-needs-harness | domain.md#ResearchCapture:field:7 | ResearchCapture.producer_ref: [ProducerRef embedded shape](#producerref-embedded-shape) |
| APT-EVT-015 | 92850796 | event-obligation | derivable-needs-harness | events.md#SessionStarted:consumer:2 | Event SessionStarted consumed by Non-authoritative observability adapter |
| APT-WF-013 | 93a333e5 | workflow-step | derivable-needs-harness | workflows.md#CaptureAndEnrichResearch:step:10 | Workflow CaptureAndEnrichResearch step 11 (Repeat or finish) succeeds |
| APT-ERR-036 | 942c96e9 | error-obligation | derivable-needs-harness | operations.md#EnsureSession:errorstate:4 | Error mapping for EnsureSession: "Duplicate Session ID or malformed/anonymous actor" -> `IDENTITY_INVALID`; append nothing. |
| APT-NF-045 | 95896be2 | needs-formal | needs-formal | operations.md#AppendReferenceProbeLineage:rule:13 | Rule APT-OP-PROBE-14: needs_formal (prose Formal) |
| APT-DOM-078 | 95c4a41e | domain-field | derivable-needs-harness | domain.md#FactEnvelope:field:2 | FactEnvelope.operation_id: opaque string (Idempotency identity for the append.) |
| APT-NF-046 | 96f1cc14 | needs-formal | needs-formal | operations.md#StartNewSession:calculation:1 | Calculation APT-OP-ROL-C2: needs_formal |
| APT-DOM-079 | 96f72926 | domain-field | derivable-needs-harness | domain.md#ContentDigest:field:0 | ContentDigest.algorithm: string (`sha256` in L0.) |
| APT-NF-047 | 99b54fb1 | needs-formal | needs-formal | operations.md#AppendResearchFact:calculation:2 | Calculation APT-OP-FACT-C3: needs_formal |
| APT-NF-048 | 9a0e2c30 | needs-formal | needs-formal | operations.md#AppendReferenceProbeLineage:calculation:0 | Calculation APT-OP-PROBE-C1: needs_formal |
| APT-DOM-080 | 9a96bd2d | domain-field | derivable-needs-harness | domain.md#ProbeRecommendationRef:field:2 | ProbeRecommendationRef.bundle_digest: [ContentDigest](#contentdigest) (Exact committed bundle digest.) |
| APT-NF-049 | 9b742bc1 | needs-formal | needs-formal | operations.md#AppendResearchCapture:rule:7 | Rule APT-OP-CAP-8: needs_formal (prose Formal) |
| APT-NF-050 | 9c0e3e7b | needs-formal | needs-formal | operations.md#AppendReferenceProbeLineage:rule:16 | Rule APT-OP-PROBE-17: needs_formal (prose Formal) |
| APT-DOM-081 | 9c194903 | domain-field | derivable-needs-harness | domain.md#ReferenceCheck:field:8 | ReferenceCheck.result: [ReferenceCheckResult](#referencecheckresult) |
| APT-DOM-082 | 9ce40bd5 | domain-field | derivable-needs-harness | domain.md#ResearchCapture:field:3 | ResearchCapture.capture_operation_id: opaque string |
| APT-DOM-083 | 9ce8731d | domain-field | derivable-needs-harness | domain.md#ExtractionProvenance:field:6 | ExtractionProvenance.selector: [RawSelector](#rawselector) (Exact selection in finalized raw bytes.) |
| APT-WF-014 | 9ce8a821 | workflow-step | derivable-needs-harness | workflows.md#IngestReferenceProbeLineage:step:0 | Workflow IngestReferenceProbeLineage step 1 (Decode closed request) on failure: Reject unknown/duplicate/owner fields. |
| APT-DOM-084 | 9dc63e72 | domain-field | derivable-needs-harness | domain.md#ResearchAnswer:field:2 | ResearchAnswer.fact: [FactEnvelope](#factenvelope) |
| APT-DOM-085 | 9dd20e29 | domain-field | derivable-needs-harness | domain.md#ResearchClaimExtraction:field:1 | ResearchClaimExtraction.research_capture_id: [ResearchCapture](#researchcapture).`research_capture_id` |
| APT-ERR-037 | 9de30f3e | error-obligation | derivable-needs-harness | operations.md#AppendResearchCapture:errorstate:0 | Error mapping for AppendResearchCapture: "Missing/unknown schema or slot, extra field, invalid null/status combination" -> `CAPTURE_SCHEMA_INVALID`; append nothing. |
| APT-DOM-086 | 9ea19d5e | domain-field | derivable-needs-harness | domain.md#RawSelector:field:1 | RawSelector.unit: string (Exactly `utf8-byte`.) |
| APT-CALC-007 | 9ee635ad | calculation | derivable-pure | operations.md#AppendReferenceProbeLineage:calculation:2 | Calculation APT-OP-PROBE-C3: canonical_request=sort(items,(kind_rank,stable_subject_key)); submitted_items=filter(submitted_new,canonical_request) |
| APT-DOM-087 | 9f496a65 | domain-field | derivable-needs-harness | domain.md#ResearchCapture:field:0 | ResearchCapture.schema_ref: string |
| APT-ERR-038 | 9f74e0cc | error-obligation | derivable-needs-harness | operations.md#AppendResearchFact:errorstate:0 | Error mapping for AppendResearchFact: "Unknown payload variant, extra/missing field or wrong subject binding" -> `FACT_SCHEMA_INVALID`; append nothing. |
| APT-WF-015 | 9f9f36aa | workflow-step | derivable-needs-harness | workflows.md#StartOrReuseSession:step:8 | Workflow StartOrReuseSession step 9 (Return workflow result) succeeds |
| APT-WF-016 | 9fee2008 | workflow-step | derivable-needs-harness | workflows.md#IngestReferenceProbeLineage:step:2 | Workflow IngestReferenceProbeLineage step 3 (Resolve evidence/current heads) succeeds |
| APT-WF-017 | 9fef3984 | workflow-step | derivable-needs-harness | workflows.md#StartOrReuseSession:step:6 | Workflow StartOrReuseSession step 7 (Resolve snapshot/link evidence) succeeds |
| APT-ERR-039 | a22e7c1f | error-obligation | derivable-needs-harness | operations.md#AppendReferenceProbeLineage:errorstate:3 | Error mapping for AppendReferenceProbeLineage: "Empty/unknown item or stale delivery head" -> `LINEAGE_INVALID`; append no lineage. |
| APT-NF-051 | a298b53e | needs-formal | needs-formal | states.md#Research Capture Currentness:invariant:2 | Invariant APT-STATE-I9: needs_formal (prose Formal) |
| APT-ERR-040 | a326ae2c | error-obligation | derivable-needs-harness | operations.md#AppendReferenceProbeLineage:errorstate:10 | Error mapping for AppendReferenceProbeLineage: "Global `fact_id` exists through either operation with different canonical payload digest, `subject_id` or `supersedes_fact_id`" -> `FACT_IDENTITY_CONFLICT`; append no delivery or use facts. |
| APT-EVT-016 | a66374aa | event-obligation | derivable-needs-harness | events.md#ResearchFactAppended:consumer:0 | Event ResearchFactAppended consumed by Fact-head reducer |
| APT-WF-018 | a6b1a5a9 | workflow-step | derivable-needs-harness | workflows.md#IngestReferenceProbeLineage:step:4 | Workflow IngestReferenceProbeLineage step 5 (Submit lineage command) succeeds |
| APT-ERR-041 | a6eaeb93 | error-obligation | derivable-needs-harness | operations.md#EnsureSession:errorstate:1 | Error mapping for EnsureSession: "Ensure key already belongs to another origin tuple" -> `ENSURE_ORIGIN_CONFLICT`; append nothing. |
| APT-DOM-088 | a7a3c741 | domain-field | derivable-needs-harness | domain.md#ContentDigest:field:1 | ContentDigest.value: lowercase hexadecimal string (Exactly 64 hexadecimal characters for `sha256`.) |
| APT-DOM-089 | a7d84f87 | domain-field | derivable-needs-harness | domain.md#ExtractionProvenance:field:5 | ExtractionProvenance.source_capture_digest: [ContentDigest](#contentdigest) (Must match the pinned capture.) |
| APT-ENUM-007 | a9289a3c | domain-enum | derivable-needs-harness | domain.md#ReferenceCheckResult:enum | ReferenceCheckResult vocabulary is exactly {pass,fail,indeterminate} |
| APT-NF-052 | a9371089 | needs-formal | needs-formal | operations.md#StartNewSession:rule:2 | Rule APT-OP-ROL-3: needs_formal (prose Formal) |
| APT-DOM-090 | a9a211da | domain-field | derivable-needs-harness | domain.md#ResearchReferenceUse:field:8 | ResearchReferenceUse.use_kind: [ReferenceUseKind](#referenceusekind) |
| APT-NF-053 | aa36b89d | needs-formal | needs-formal | states.md#Research Capture Currentness:invariant:3 | Invariant APT-STATE-I10: needs_formal (prose Formal) |
| APT-ERR-042 | aa545f2f | error-obligation | derivable-needs-harness | operations.md#AppendReferenceProbeLineage:errorstate:15 | Error mapping for AppendReferenceProbeLineage: "Submitted same `command_identity(op)` with changed command digest" -> `IDEMPOTENCY_CONFLICT`; append no lineage. |
| APT-NF-054 | abc20b0c | needs-formal | needs-formal | operations.md#AppendReferenceProbeLineage:rule:4 | Rule APT-OP-PROBE-5: needs_formal (prose Formal) |
| APT-EVT-017 | ac579871 | event-obligation | derivable-needs-harness | events.md#SessionStarted:consumer:1 | Event SessionStarted consumed by Planned SessionRecord projection |
| APT-WF-019 | ace41473 | workflow-step | derivable-needs-harness | workflows.md#StartOrReuseSession:step:3 | Workflow StartOrReuseSession step 4 (Resolve rollover authorization) succeeds |
| APT-DOM-091 | ad2a0119 | domain-field | derivable-needs-harness | domain.md#ResearchReferenceClaimRelation:field:6 | ResearchReferenceClaimRelation.extraction: [ExtractionProvenance](#extractionprovenance) |
| APT-ERR-043 | af029ca2 | error-obligation | derivable-needs-harness | operations.md#AppendResearchCapture:errorstate:2 | Error mapping for AppendResearchCapture: "Binary/non-UTF-8/unfinalized raw return" -> `RAW_ARTIFACT_INVALID`; append nothing. |
| APT-DOM-092 | b05958f9 | domain-field | derivable-needs-harness | domain.md#ReferenceCheck:field:9 | ReferenceCheck.evidence_ref: [ArtifactReference](#artifactreference) |
| APT-ERR-044 | b172693d | error-obligation | derivable-needs-harness | operations.md#AppendResearchCapture:errorstate:7 | Error mapping for AppendResearchCapture: "Invalid/duplicate/cross-Dispatch synthesis pin" -> `SYNTHESIS_INVALID`; append nothing. |
| APT-DOM-093 | b1c4e43f | domain-field | derivable-needs-harness | domain.md#FormalizationCandidate:field:7 | FormalizationCandidate.reading: string |
| APT-NF-055 | b23e9c94 | needs-formal | needs-formal | operations.md#AppendResearchCapture:rule:2 | Rule APT-OP-CAP-3: needs_formal (prose Formal) |
| APT-DOM-094 | b2c34499 | domain-field | derivable-needs-harness | domain.md#ResearchReferenceUse:field:9 | ResearchReferenceUse.anchor_quality: constrained string |
| APT-NF-056 | b2f6fa96 | needs-formal | needs-formal | operations.md#StartNewSession:rule:3 | Rule APT-OP-ROL-4: needs_formal (prose Formal) |
| APT-DOM-095 | b36a1d99 | domain-field | derivable-needs-harness | domain.md#Session:field:6 | Session.initial_name: string |
| APT-DOM-096 | b3c9ca2e | domain-field | derivable-needs-harness | domain.md#ResearchReferenceUse:field:7 | ResearchReferenceUse.probe_recommendation_ref: [ProbeRecommendationRef](#proberecommendationref) |
| APT-NF-057 | b3eb9fa3 | needs-formal | needs-formal | operations.md#AppendReferenceProbeLineage:rule:3 | Rule APT-OP-PROBE-4: needs_formal (prose Formal) |
| APT-DOM-097 | b3fc57f4 | domain-field | derivable-needs-harness | domain.md#ResearchCapture:field:8 | ResearchCapture.capture_status: [CaptureStatus](#capturestatus) |
| APT-DOM-098 | b46a17f5 | domain-field | derivable-needs-harness | domain.md#SessionDispatchLink:field:0 | SessionDispatchLink.session_dispatch_link_id: opaque string |
| APT-EVT-018 | b49e9919 | event-obligation | derivable-needs-harness | events.md#ReferenceProbeLineageAppended:consumer:3 | Event ReferenceProbeLineageAppended consumed by Non-authoritative observability adapter |
| APT-WF-020 | b525903d | workflow-step | derivable-needs-harness | workflows.md#IngestReferenceProbeLineage:step:0 | Workflow IngestReferenceProbeLineage step 1 (Decode closed request) succeeds |
| APT-DOM-099 | b588b3a2 | domain-field | derivable-needs-harness | domain.md#ExtractionProvenance:field:0 | ExtractionProvenance.mode: [ExtractionMode](#extractionmode) (Exactly one attribution mode.) |
| APT-WF-021 | b5a4fb50 | workflow-step | derivable-needs-harness | workflows.md#StartOrReuseSession:step:0 | Workflow StartOrReuseSession step 1 (Bind invocation/context evidence) on failure: Return typed authentication/evidence error. |
| APT-DOM-100 | b61fd4d9 | domain-field | derivable-needs-harness | domain.md#ResearchAnswer:field:4 | ResearchAnswer.extraction: [ExtractionProvenance](#extractionprovenance) |
| APT-DOM-101 | b73fa85d | domain-field | derivable-needs-harness | domain.md#ResearchProblem:field:5 | ResearchProblem.blocks: canonical sorted set of opaque subject refs |
| APT-WF-022 | b74adac4 | workflow-step | derivable-needs-harness | workflows.md#CaptureAndEnrichResearch:step:8 | Workflow CaptureAndEnrichResearch step 9 (Bind exact fact variant) succeeds |
| APT-DOM-102 | b76e4532 | domain-field | derivable-needs-harness | domain.md#ReferenceCheck:field:1 | ReferenceCheck.research_capture_id: [ResearchCapture](#researchcapture).`research_capture_id` |
| APT-DOM-103 | b89c4ac1 | domain-field | derivable-needs-harness | domain.md#DispatchAuthoritySnapshotRef:field:3 | DispatchAuthoritySnapshotRef.artifact_digest: [ContentDigest](#contentdigest) (Required only for `aci_managed`.) |
| APT-NF-058 | ba05d7df | needs-formal | needs-formal | operations.md#LinkSessionDispatch:rule:1 | Rule APT-OP-LINK-2: needs_formal (prose Formal) |
| APT-CALC-008 | bcfbdf48 | calculation | derivable-pure | operations.md#AppendReferenceProbeLineage:calculation:1 | Calculation APT-OP-PROBE-C2: submitted_new |
| APT-DOM-104 | bd672d7f | domain-field | derivable-needs-harness | domain.md#ResearchQuestion:field:0 | ResearchQuestion.research_question_id: opaque string |
| APT-NF-059 | bd6822b7 | needs-formal | needs-formal | states.md#Research Capture Currentness:invariant:1 | Invariant APT-STATE-I8: needs_formal (prose Formal) |
| APT-DOM-105 | bddd56bb | domain-field | derivable-needs-harness | domain.md#FactEnvelope:field:1 | FactEnvelope.subject_id: opaque string (Stable Entity subject shared across its versions.) |
| APT-DOM-106 | be0d2d26 | domain-field | derivable-needs-harness | domain.md#DispatchAuthoritySnapshotRef:field:4 | DispatchAuthoritySnapshotRef.accepted_event_id: external ACI event ID (Required only for `aci_managed`.) |
| APT-TR-012 | be0e3c4b | invalid-transition | derivable-needs-harness | states.md#Research Capture Currentness:invalid:current head:grouped initial `ResearchCaptureAppended` | Event grouped initial `ResearchCaptureAppended` in state current head is rejected (no valid transition) |
| APT-WF-023 | be12b78b | workflow-step | derivable-needs-harness | workflows.md#CaptureAndEnrichResearch:step:3 | Workflow CaptureAndEnrichResearch step 4 (Append immutable capture) succeeds |
| APT-WF-024 | c0baf55b | workflow-step | derivable-needs-harness | workflows.md#CaptureAndEnrichResearch:step:0 | Workflow CaptureAndEnrichResearch step 1 (Bind current research context) succeeds |
| APT-DOM-107 | c0e08ba8 | domain-field | derivable-needs-harness | domain.md#ReferenceCheck:field:2 | ReferenceCheck.fact: [FactEnvelope](#factenvelope) |
| APT-DOM-108 | c1a9f60f | domain-field | derivable-needs-harness | domain.md#ResearchReferenceUse:field:6 | ResearchReferenceUse.source_observation_id: external [`host.SourceObservation`](../discovery/session-dispatch-research-records.md#43-reference-uses-and-checks) ID |
| APT-DOM-109 | c22406b9 | domain-field | derivable-needs-harness | domain.md#Session:field:0 | Session.session_id: opaque string |
| APT-TR-013 | c24e2711 | valid-transition | derivable-needs-harness | states.md#Session Context Binding:transition:0 | Transition unbound --`EnsureSession` acceptance represented by grouped `SessionStarted`--> bound to new Session succeeds when guarded |
| APT-NF-060 | c2c3dd76 | needs-formal | needs-formal | operations.md#AppendResearchCapture:rule:3 | Rule APT-OP-CAP-4: needs_formal (prose Formal) |
| APT-DOM-110 | c2dee301 | domain-field | derivable-needs-harness | domain.md#ResearchReferenceUse:field:4 | ResearchReferenceUse.reference_kind: constrained string |
| APT-ERR-045 | c4b4ccb2 | error-obligation | derivable-needs-harness | operations.md#AppendReferenceProbeLineage:errorstate:11 | Error mapping for AppendReferenceProbeLineage: "Delivery-only item attempts to assert access/consultation/support" -> `LINEAGE_SCOPE_VIOLATION`; append no lineage. |
| APT-NF-061 | c6ebac36 | needs-formal | needs-formal | states.md#Session Context Binding:invariant:8 | Invariant APT-STATE-I15: needs_formal (prose Formal) |
| APT-ERR-046 | c7a4f3ed | error-obligation | derivable-needs-harness | operations.md#LinkSessionDispatch:errorstate:6 | Error mapping for LinkSessionDispatch: "Snapshot version/digest/evidence invalid" -> `SNAPSHOT_INVALID`; append nothing. |
| APT-NF-062 | c7debd40 | needs-formal | needs-formal | operations.md#StartNewSession:rule:1 | Rule APT-OP-ROL-2: needs_formal (prose Formal) |
| APT-DOM-111 | c80a3cd2 | domain-field | derivable-needs-harness | domain.md#FactEnvelope:field:3 | FactEnvelope.occurred_at: offset timestamp (Owner-stamped occurrence time.) |
| APT-DOM-112 | c8996387 | domain-field | derivable-needs-harness | domain.md#ExtractionProvenance:field:4 | ExtractionProvenance.source_capture_id: [ResearchCapture](#researchcapture).`research_capture_id` (Exact source capture.) |
| APT-WF-025 | c8f7c577 | workflow-step | derivable-needs-harness | workflows.md#CaptureAndEnrichResearch:step:4 | Workflow CaptureAndEnrichResearch step 5 (Decide enrichment eligibility) succeeds |
| APT-ERR-047 | c8f8708e | error-obligation | derivable-needs-harness | operations.md#LinkSessionDispatch:errorstate:0 | Error mapping for LinkSessionDispatch: "Session or Dispatch snapshot missing" -> `AUTHORITY_NOT_FOUND`; append nothing. |
| APT-NF-063 | ca89d4a4 | needs-formal | needs-formal | operations.md#EnsureSession:rule:5 | Rule APT-OP-ENS-6: needs_formal (prose Formal) |
| APT-DOM-113 | cb2db928 | domain-field | derivable-needs-harness | domain.md#FormalizationCandidate:field:13 | FormalizationCandidate.proof_check_ref: opaque external ref |
| APT-ERR-048 | cb360dd9 | error-obligation | derivable-needs-harness | operations.md#AppendResearchFact:errorstate:8 | Error mapping for AppendResearchFact: "Aggregate type/ID/head/version/predecessor/locality mismatch, gap or fork" -> `AGGREGATE_CAS_CONFLICT`; append nothing. |
| APT-DOM-114 | cbafdc2c | domain-field | derivable-needs-harness | domain.md#ResearchReferenceClaimRelation:field:3 | ResearchReferenceClaimRelation.reference_use_id: [ResearchReferenceUse](#researchreferenceuse).`reference_use_id` |
| APT-NF-064 | cbd19e5e | needs-formal | needs-formal | states.md#Session Context Binding:invariant:0 | Invariant APT-STATE-I1: needs_formal (prose Formal) |
| APT-DOM-115 | cc1892d9 | domain-field | derivable-needs-harness | domain.md#SessionDispatchLink:field:4 | SessionDispatchLink.linked_at: offset timestamp |
| APT-DOM-116 | cd4fae52 | domain-field | derivable-needs-harness | domain.md#ResearchCapture:field:14 | ResearchCapture.synthesizes: semantic ordered list of unique `{research_capture_id, capture_digest}` pins |
| APT-DOM-117 | cd64bd3e | domain-field | derivable-needs-harness | domain.md#FormalizationCandidate:field:5 | FormalizationCandidate.latex: string |
| APT-TR-014 | cdca1666 | invalid-transition | derivable-needs-harness | states.md#Session Context Binding:invalid:bound to successor:`EnsureSession` acceptance represented by grouped `SessionStarted` | Event `EnsureSession` acceptance represented by grouped `SessionStarted` in state bound to successor is rejected (no valid transition) |
| APT-ERR-049 | cde23868 | error-obligation | derivable-needs-harness | operations.md#AppendReferenceProbeLineage:errorstate:4 | Error mapping for AppendReferenceProbeLineage: "More than one item for the same `(kind,stable_subject_key)`" -> `DUPLICATE_MEMBER_KEY`; append nothing. |
| APT-ERR-050 | ce82f4a0 | error-obligation | derivable-needs-harness | operations.md#AppendReferenceProbeLineage:errorstate:0 | Error mapping for AppendReferenceProbeLineage: "Bundle acceptance missing, uncommitted, wrong identity or digest" -> `BUNDLE_ACCEPTANCE_INVALID`; append no lineage. |
| APT-DOM-118 | cf230fbc | domain-field | derivable-needs-harness | domain.md#ResearchClaimExtraction:field:2 | ResearchClaimExtraction.fact: [FactEnvelope](#factenvelope) |
| APT-EVT-019 | cf29ebff | event-obligation | derivable-needs-harness | events.md#SessionContextRebound | Event SessionContextRebound is emitted with valid payload |
| APT-ERR-051 | cf69cbab | error-obligation | derivable-needs-harness | operations.md#EnsureSession:errorstate:0 | Error mapping for EnsureSession: "Same `command_identity(op)`, different command digest" -> `IDEMPOTENCY_CONFLICT`; append nothing. |
| APT-NF-065 | d139239b | needs-formal | needs-formal | states.md#Session Context Binding:invariant:6 | Invariant APT-STATE-I13: needs_formal (prose Formal) |
| APT-EVT-020 | d153adc0 | event-obligation | derivable-needs-harness | events.md#SessionDispatchLinked:consumer:1 | Event SessionDispatchLinked consumed by Planned SessionRecord and DispatchScopeProjection |
| APT-DOM-119 | d1ef89bc | domain-field | derivable-needs-harness | domain.md#DispatchAuthoritySnapshotRef:field:1 | DispatchAuthoritySnapshotRef.dispatch_id: external Dispatch ID (Required only for `aci_managed`.) |
| APT-ERR-052 | d1f65cc6 | error-obligation | derivable-needs-harness | operations.md#AppendResearchCapture:errorstate:4 | Error mapping for AppendResearchCapture: "No current context Session or no exact SessionDispatchLink to the Dispatch" -> `CURRENT_LINK_REQUIRED`; append nothing. |
| APT-WF-026 | d278dc40 | workflow-step | derivable-needs-harness | workflows.md#StartOrReuseSession:step:4 | Workflow StartOrReuseSession step 5 (Replace current Session) succeeds |
| APT-ENUM-008 | d2d7bc4e | domain-enum | derivable-needs-harness | domain.md#ExtractionMode:enum | ExtractionMode vocabulary is exactly {verbatim,declared,inferred} |
| APT-DOM-120 | d2f32f59 | domain-field | derivable-needs-harness | domain.md#ResearchReferenceClaimRelation:field:2 | ResearchReferenceClaimRelation.fact: [FactEnvelope](#factenvelope) |
| APT-DOM-121 | d36c12bf | domain-field | derivable-needs-harness | domain.md#ProbeRecommendationRef:field:6 | ProbeRecommendationRef.source_observation_ids: canonical sorted set of external [`host.SourceObservation`](../discovery/session-dispatch-research-records.md#43-reference-uses-and-checks) IDs (`0..N`, unique; each supplied ID remains host-owned.) |
| APT-DOM-122 | d47d9611 | domain-field | derivable-needs-harness | domain.md#ResearchProblem:field:6 | ResearchProblem.evidence_refs: canonical sorted set of [ArtifactReference](#artifactreference) or fact refs |
| APT-WF-027 | d5d8871c | workflow-step | derivable-needs-harness | workflows.md#CaptureAndEnrichResearch:step:7 | Workflow CaptureAndEnrichResearch step 8 (Resolve disposition/assessment guards) succeeds |
| APT-EVT-021 | d6ed299b | event-obligation | derivable-needs-harness | events.md#Event Coverage and Test Derivation | Event Event Coverage and Test Derivation is emitted with valid payload |
| APT-NF-066 | d6f847a5 | needs-formal | needs-formal | operations.md#AppendResearchFact:rule:9 | Rule APT-OP-FACT-10: needs_formal (prose Formal) |
| APT-ERR-053 | d75d7311 | error-obligation | derivable-needs-harness | operations.md#AppendReferenceProbeLineage:errorstate:6 | Error mapping for AppendReferenceProbeLineage: "Use item lacks current capture, full ResearchReferenceUse payload, selector/artifact evidence or fact CAS" -> `PROVEN_USE_INVALID`; append no delivery or use facts. |
| APT-NF-067 | d872803c | needs-formal | needs-formal | states.md#Session Context Binding:invariant:5 | Invariant APT-STATE-I6: needs_formal (prose Formal) |
| APT-DOM-123 | d9be3df8 | domain-field | derivable-needs-harness | domain.md#ArtifactReference:field:5 | ArtifactReference.redaction_policy_ref: opaque external ref (Exact policy applied or required.) |
| APT-DOM-124 | dbd44932 | domain-field | derivable-needs-harness | domain.md#ArtifactReference:field:0 | ArtifactReference.artifact_id: external ACI artifact identity (Finalized through the [ACI artifact boundary](../../agents-communication-infra/specs/interfaces.md#internal-artifact-boundary).) |
| APT-EVT-022 | dc2a823d | event-obligation | derivable-needs-harness | events.md#ResearchCaptureAppended:consumer:2 | Event ResearchCaptureAppended consumed by AppendResearchFact binder |
| APT-NF-068 | dcd4c6d9 | needs-formal | needs-formal | operations.md#AppendResearchCapture:rule:5 | Rule APT-OP-CAP-6: needs_formal (prose Formal) |
| APT-NF-069 | dd4312ef | needs-formal | needs-formal | operations.md#AppendResearchFact:calculation:1 | Calculation APT-OP-FACT-C2: needs_formal |
| APT-EVT-023 | de878226 | event-obligation | derivable-needs-harness | events.md#SessionContextRebound:consumer:1 | Event SessionContextRebound consumed by Planned SessionRecord projection |
| APT-ERR-054 | dfe9c077 | error-obligation | derivable-needs-harness | operations.md#AppendReferenceProbeLineage:errorstate:5 | Error mapping for AppendReferenceProbeLineage: "Item predecessor depends on another same-command item or attempts a same-key fork/revision" -> `VIRTUAL_SEQUENCE_FORBIDDEN`; append nothing. |
| APT-DOM-125 | e07b70df | domain-field | derivable-needs-harness | domain.md#ResearchProblem:field:0 | ResearchProblem.problem_id: opaque string |
| APT-NF-070 | e1c40d73 | needs-formal | needs-formal | operations.md#AppendResearchCapture:calculation:0 | Calculation APT-OP-CAP-C1: needs_formal |
| APT-DOM-126 | e23a5017 | domain-field | derivable-needs-harness | domain.md#ArtifactReference:field:2 | ArtifactReference.media_type: string (Explicit media type.) |
| APT-CALC-009 | e26b3097 | calculation | derivable-pure | operations.md#AppendResearchFact:calculation:4 | Calculation APT-OP-FACT-C5: new⇒H_canonical({command_identity(op),fact_id}); existing⇒existing.fact.operation_id |
| APT-EVT-024 | e3d1a7e0 | event-obligation | derivable-needs-harness | events.md#SessionContextRebound:consumer:2 | Event SessionContextRebound consumed by Non-authoritative observability adapter |
| APT-NF-071 | e498d8ee | needs-formal | needs-formal | operations.md#EnsureSession:rule:0 | Rule APT-OP-ENS-1: needs_formal (prose Formal) |
| APT-DOM-127 | e4abfa4a | domain-field | derivable-needs-harness | domain.md#ResearchReferenceClaimRelation:field:0 | ResearchReferenceClaimRelation.relation_id: opaque string |
| APT-NF-072 | e50e9e28 | needs-formal | needs-formal | operations.md#AppendReferenceProbeLineage:rule:12 | Rule APT-OP-PROBE-13: needs_formal (prose Formal) |
| APT-DOM-128 | e51637ed | domain-field | derivable-needs-harness | domain.md#ArtifactReference:field:6 | ArtifactReference.retention_policy_ref: opaque external ref (Exact retention policy.) |
| APT-NF-073 | e5a0c188 | needs-formal | needs-formal | operations.md#EnsureSession:rule:2 | Rule APT-OP-ENS-3: needs_formal (prose Formal) |
| APT-DOM-129 | e7658367 | domain-field | derivable-needs-harness | domain.md#ResearchQuestion:field:4 | ResearchQuestion.derives_from: canonical sorted set of [QuestionDerivationRef embedded union](#questionderivationref-embedded-union) |
| APT-EVT-025 | e7a6877a | event-obligation | derivable-needs-harness | events.md#ReferenceProbeLineageAppended:consumer:2 | Event ReferenceProbeLineageAppended consumed by Planned ResearchRecord/reference projections |
| APT-DOM-130 | e8acd083 | domain-field | derivable-needs-harness | domain.md#ReferenceCheck:field:6 | ReferenceCheck.checked_by: opaque actor ref |
| APT-DOM-131 | e8de768f | domain-field | derivable-needs-harness | domain.md#ReferenceCheck:field:7 | ReferenceCheck.method_ref: string |
| APT-DOM-132 | e91e59fe | domain-field | derivable-needs-harness | domain.md#SessionDispatchLink:field:1 | SessionDispatchLink.session_id: [Session](#session).`session_id` |
| APT-DOM-133 | ea10828d | domain-field | derivable-needs-harness | domain.md#ReferenceCheck:field:0 | ReferenceCheck.reference_check_id: opaque string |
| APT-EVT-026 | eadb7fec | event-obligation | derivable-needs-harness | events.md#SessionDispatchLinked:consumer:0 | Event SessionDispatchLinked consumed by Session/Dispatch membership reducer |
| APT-NF-074 | eaee41ab | needs-formal | needs-formal | operations.md#StartNewSession:calculation:0 | Calculation APT-OP-ROL-C1: needs_formal |
| APT-TR-015 | ec85688c | invalid-transition | derivable-needs-harness | states.md#Research Capture Currentness:invalid:no head for chain:grouped replacement `ResearchCaptureAppended` | Event grouped replacement `ResearchCaptureAppended` in state no head for chain is rejected (no valid transition) |
| APT-DOM-134 | ed72fd1d | domain-field | derivable-needs-harness | domain.md#ResearchCapture:field:11 | ResearchCapture.failure_reason: non-empty string or null |
| APT-DOM-135 | ede0884e | domain-field | derivable-needs-harness | domain.md#ProbeRecommendationRef:field:1 | ProbeRecommendationRef.recommendation_id: opaque external recommendation ID (Exact recommendation within the bundle.) |
| APT-ERR-055 | edfd7aca | error-obligation | derivable-needs-harness | operations.md#AppendResearchCapture:errorstate:1 | Error mapping for AppendResearchCapture: "Artifact/failure/origin evidence missing, uncommitted or digest-mismatched" -> `EVIDENCE_INVALID`; append nothing. |
| APT-EVT-027 | ee70586f | event-obligation | derivable-needs-harness | events.md#Connections | Event Connections is emitted with valid payload |
| APT-WF-028 | ef3b6f28 | workflow-step | derivable-needs-harness | workflows.md#StartOrReuseSession:step:1 | Workflow StartOrReuseSession step 2 (Ensure coarse Session) succeeds |
| APT-DOM-136 | efe7645b | domain-field | derivable-needs-harness | domain.md#ProbeRecommendationRef:field:0 | ProbeRecommendationRef.probe_id: opaque external probe ID (Exact committed probe.) |
| APT-QRY-004 | f00f06bc | query-behavior | derivable-needs-harness | queries.md#DispatchScopeProjection | Query DispatchScopeProjection returns its projected read model without side effects |
| APT-NF-075 | f025f8cb | needs-formal | needs-formal | operations.md#AppendResearchCapture:calculation:2 | Calculation APT-OP-CAP-C3: needs_formal |
| APT-NF-076 | f0810360 | needs-formal | needs-formal | operations.md#AppendResearchFact:rule:0 | Rule APT-OP-FACT-1: needs_formal (prose Formal) |
| APT-NF-077 | f0d08995 | needs-formal | needs-formal | operations.md#AppendResearchCapture:rule:1 | Rule APT-OP-CAP-2: needs_formal (prose Formal) |
| APT-DOM-137 | f1f6850d | domain-field | derivable-needs-harness | domain.md#FormalizationCandidate:field:3 | FormalizationCandidate.research_claim_id: [ResearchClaimExtraction](#researchclaimextraction).`research_claim_id` |
| APT-DOM-138 | f6834d2c | domain-field | derivable-needs-harness | domain.md#ResearchReferenceUse:field:10 | ResearchReferenceUse.extraction: [ExtractionProvenance](#extractionprovenance) |
| APT-DOM-139 | f6c9250b | domain-field | derivable-needs-harness | domain.md#ResearchReferenceUse:field:3 | ResearchReferenceUse.reference_id: opaque string |
| APT-TR-016 | f787b8a3 | invalid-transition | derivable-needs-harness | states.md#Session Context Binding:invalid:bound to predecessor:`EnsureSession` acceptance represented by grouped `SessionStarted` | Event `EnsureSession` acceptance represented by grouped `SessionStarted` in state bound to predecessor is rejected (no valid transition) |
| APT-DOM-140 | f830ae7c | domain-field | derivable-needs-harness | domain.md#RawSelector:field:0 | RawSelector.schema_ref: string (`apt.raw-selector@1` in L0.) |
| APT-NF-078 | f8daa72e | needs-formal | needs-formal | states.md#Session Context Binding:invariant:2 | Invariant APT-STATE-I3: needs_formal (prose Formal) |
| APT-DOM-141 | fa33c8b7 | domain-field | derivable-needs-harness | domain.md#FormalizationCandidate:field:2 | FormalizationCandidate.fact: [FactEnvelope](#factenvelope) |
| APT-ERR-056 | fb104520 | error-obligation | derivable-needs-harness | operations.md#AppendResearchFact:errorstate:10 | Error mapping for AppendResearchFact: "Same `command_identity(op)` with changed canonical digest" -> `IDEMPOTENCY_CONFLICT`; append nothing. |
| APT-DOM-142 | fc0053e3 | domain-field | derivable-needs-harness | domain.md#ResearchAnswer:field:0 | ResearchAnswer.research_answer_id: opaque string |
| APT-DOM-143 | fe04509c | domain-field | derivable-needs-harness | domain.md#ResearchAnswer:field:3 | ResearchAnswer.question_ids: canonical sorted set of [ResearchQuestion](#researchquestion).`research_question_id` |
| APT-NF-079 | fe0a7350 | needs-formal | needs-formal | operations.md#AppendReferenceProbeLineage:rule:15 | Rule APT-OP-PROBE-16: needs_formal (prose Formal) |
| APT-DOM-144 | fe5b4b6a | domain-field | derivable-needs-harness | domain.md#DispatchAuthoritySnapshotRef:field:0 | DispatchAuthoritySnapshotRef.kind: `aci_managed \ (legacy_ledger`) |
| APT-EVT-028 | fe7b9c90 | event-obligation | derivable-needs-harness | events.md#ResearchFactAppended:consumer:2 | Event ResearchFactAppended consumed by Planned ResearchRecord/granular projections |
| APT-EVT-029 | ffbe88f9 | event-obligation | derivable-needs-harness | events.md#Common Event Boundary | Event Common Event Boundary is emitted with valid payload |

## Unresolved Formal Gaps

needs_formal (un-formalized — no closed checkable expression): 79

- `APT-NF-001` operations.md#AppendResearchCapture:rule:0 — Rule APT-OP-CAP-1: needs_formal (prose Formal)
- `APT-NF-002` operations.md#LinkSessionDispatch:calculation:0 — Calculation APT-OP-LINK-C1: needs_formal
- `APT-NF-003` operations.md#EnsureSession:rule:4 — Rule APT-OP-ENS-5: needs_formal (prose Formal)
- `APT-NF-004` operations.md#AppendResearchCapture:rule:4 — Rule APT-OP-CAP-5: needs_formal (prose Formal)
- `APT-NF-005` operations.md#AppendReferenceProbeLineage:rule:7 — Rule APT-OP-PROBE-8: needs_formal (prose Formal)
- `APT-NF-006` operations.md#StartNewSession:rule:4 — Rule APT-OP-ROL-5: needs_formal (prose Formal)
- `APT-NF-007` operations.md#AppendReferenceProbeLineage:rule:10 — Rule APT-OP-PROBE-11: needs_formal (prose Formal)
- `APT-NF-008` operations.md#LinkSessionDispatch:rule:0 — Rule APT-OP-LINK-1: needs_formal (prose Formal)
- `APT-NF-009` operations.md#AppendResearchFact:rule:8 — Rule APT-OP-FACT-9: needs_formal (prose Formal)
- `APT-NF-010` operations.md#AppendReferenceProbeLineage:rule:1 — Rule APT-OP-PROBE-2: needs_formal (prose Formal)
- `APT-NF-011` operations.md#LinkSessionDispatch:rule:2 — Rule APT-OP-LINK-3: needs_formal (prose Formal)
- `APT-NF-012` operations.md#AppendReferenceProbeLineage:rule:14 — Rule APT-OP-PROBE-15: needs_formal (prose Formal)
- `APT-NF-013` operations.md#AppendResearchFact:rule:7 — Rule APT-OP-FACT-8: needs_formal (prose Formal)
- `APT-NF-014` states.md#Session Context Binding:invariant:4 — Invariant APT-STATE-I5: needs_formal (prose Formal)
- `APT-NF-015` operations.md#StartNewSession:rule:0 — Rule APT-OP-ROL-1: needs_formal (prose Formal)
- `APT-NF-016` operations.md#AppendResearchFact:rule:2 — Rule APT-OP-FACT-3: needs_formal (prose Formal)
- `APT-NF-017` operations.md#EnsureSession:calculation:1 — Calculation APT-OP-ENS-C2: needs_formal
- `APT-NF-018` operations.md#LinkSessionDispatch:rule:3 — Rule APT-OP-LINK-4: needs_formal (prose Formal)
- `APT-NF-019` states.md#Research Capture Currentness:invariant:5 — Invariant APT-STATE-I12: needs_formal (prose Formal)
- `APT-NF-020` operations.md#AppendResearchFact:rule:5 — Rule APT-OP-FACT-6: needs_formal (prose Formal)
- `APT-NF-021` states.md#Research Capture Currentness:invariant:0 — Invariant APT-STATE-I7: needs_formal (prose Formal)
- `APT-NF-022` operations.md#EnsureSession:rule:1 — Rule APT-OP-ENS-2: needs_formal (prose Formal)
- `APT-NF-023` operations.md#AppendResearchFact:rule:6 — Rule APT-OP-FACT-7: needs_formal (prose Formal)
- `APT-NF-024` states.md#Session Context Binding:invariant:1 — Invariant APT-STATE-I2: needs_formal (prose Formal)
- `APT-NF-025` operations.md#AppendResearchFact:rule:1 — Rule APT-OP-FACT-2: needs_formal (prose Formal)
- `APT-NF-026` states.md#Session Context Binding:invariant:3 — Invariant APT-STATE-I4: needs_formal (prose Formal)
- `APT-NF-027` states.md#Session Context Binding:invariant:7 — Invariant APT-STATE-I14: needs_formal (prose Formal)
- `APT-NF-028` operations.md#AppendReferenceProbeLineage:rule:9 — Rule APT-OP-PROBE-10: needs_formal (prose Formal)
- `APT-NF-029` operations.md#AppendResearchFact:rule:10 — Rule APT-OP-FACT-11: needs_formal (prose Formal)
- `APT-NF-030` operations.md#AppendReferenceProbeLineage:rule:5 — Rule APT-OP-PROBE-6: needs_formal (prose Formal)
- `APT-NF-031` operations.md#EnsureSession:calculation:0 — Calculation APT-OP-ENS-C1: needs_formal
- `APT-NF-032` operations.md#AppendResearchCapture:rule:6 — Rule APT-OP-CAP-7: needs_formal (prose Formal)
- `APT-NF-033` operations.md#AppendResearchFact:rule:3 — Rule APT-OP-FACT-4: needs_formal (prose Formal)
- `APT-NF-034` operations.md#AppendReferenceProbeLineage:rule:8 — Rule APT-OP-PROBE-9: needs_formal (prose Formal)
- `APT-NF-035` operations.md#AppendResearchFact:rule:4 — Rule APT-OP-FACT-5: needs_formal (prose Formal)
- `APT-NF-036` operations.md#AppendReferenceProbeLineage:rule:0 — Rule APT-OP-PROBE-1: needs_formal (prose Formal)
- `APT-NF-037` operations.md#AppendReferenceProbeLineage:rule:2 — Rule APT-OP-PROBE-3: needs_formal (prose Formal)
- `APT-NF-038` states.md#Research Capture Currentness:invariant:4 — Invariant APT-STATE-I11: needs_formal (prose Formal)
- `APT-NF-039` operations.md#AppendReferenceProbeLineage:rule:11 — Rule APT-OP-PROBE-12: needs_formal (prose Formal)
- `APT-NF-040` operations.md#AppendResearchFact:rule:11 — Rule APT-OP-FACT-12: needs_formal (prose Formal)
- `APT-NF-041` operations.md#AppendReferenceProbeLineage:rule:6 — Rule APT-OP-PROBE-7: needs_formal (prose Formal)
- `APT-NF-042` operations.md#EnsureSession:rule:3 — Rule APT-OP-ENS-4: needs_formal (prose Formal)
- `APT-NF-043` operations.md#LinkSessionDispatch:rule:4 — Rule APT-OP-LINK-5: needs_formal (prose Formal)
- `APT-NF-044` operations.md#AppendResearchFact:calculation:0 — Calculation APT-OP-FACT-C1: needs_formal
- `APT-NF-045` operations.md#AppendReferenceProbeLineage:rule:13 — Rule APT-OP-PROBE-14: needs_formal (prose Formal)
- `APT-NF-046` operations.md#StartNewSession:calculation:1 — Calculation APT-OP-ROL-C2: needs_formal
- `APT-NF-047` operations.md#AppendResearchFact:calculation:2 — Calculation APT-OP-FACT-C3: needs_formal
- `APT-NF-048` operations.md#AppendReferenceProbeLineage:calculation:0 — Calculation APT-OP-PROBE-C1: needs_formal
- `APT-NF-049` operations.md#AppendResearchCapture:rule:7 — Rule APT-OP-CAP-8: needs_formal (prose Formal)
- `APT-NF-050` operations.md#AppendReferenceProbeLineage:rule:16 — Rule APT-OP-PROBE-17: needs_formal (prose Formal)
- `APT-NF-051` states.md#Research Capture Currentness:invariant:2 — Invariant APT-STATE-I9: needs_formal (prose Formal)
- `APT-NF-052` operations.md#StartNewSession:rule:2 — Rule APT-OP-ROL-3: needs_formal (prose Formal)
- `APT-NF-053` states.md#Research Capture Currentness:invariant:3 — Invariant APT-STATE-I10: needs_formal (prose Formal)
- `APT-NF-054` operations.md#AppendReferenceProbeLineage:rule:4 — Rule APT-OP-PROBE-5: needs_formal (prose Formal)
- `APT-NF-055` operations.md#AppendResearchCapture:rule:2 — Rule APT-OP-CAP-3: needs_formal (prose Formal)
- `APT-NF-056` operations.md#StartNewSession:rule:3 — Rule APT-OP-ROL-4: needs_formal (prose Formal)
- `APT-NF-057` operations.md#AppendReferenceProbeLineage:rule:3 — Rule APT-OP-PROBE-4: needs_formal (prose Formal)
- `APT-NF-058` operations.md#LinkSessionDispatch:rule:1 — Rule APT-OP-LINK-2: needs_formal (prose Formal)
- `APT-NF-059` states.md#Research Capture Currentness:invariant:1 — Invariant APT-STATE-I8: needs_formal (prose Formal)
- `APT-NF-060` operations.md#AppendResearchCapture:rule:3 — Rule APT-OP-CAP-4: needs_formal (prose Formal)
- `APT-NF-061` states.md#Session Context Binding:invariant:8 — Invariant APT-STATE-I15: needs_formal (prose Formal)
- `APT-NF-062` operations.md#StartNewSession:rule:1 — Rule APT-OP-ROL-2: needs_formal (prose Formal)
- `APT-NF-063` operations.md#EnsureSession:rule:5 — Rule APT-OP-ENS-6: needs_formal (prose Formal)
- `APT-NF-064` states.md#Session Context Binding:invariant:0 — Invariant APT-STATE-I1: needs_formal (prose Formal)
- `APT-NF-065` states.md#Session Context Binding:invariant:6 — Invariant APT-STATE-I13: needs_formal (prose Formal)
- `APT-NF-066` operations.md#AppendResearchFact:rule:9 — Rule APT-OP-FACT-10: needs_formal (prose Formal)
- `APT-NF-067` states.md#Session Context Binding:invariant:5 — Invariant APT-STATE-I6: needs_formal (prose Formal)
- `APT-NF-068` operations.md#AppendResearchCapture:rule:5 — Rule APT-OP-CAP-6: needs_formal (prose Formal)
- `APT-NF-069` operations.md#AppendResearchFact:calculation:1 — Calculation APT-OP-FACT-C2: needs_formal
- `APT-NF-070` operations.md#AppendResearchCapture:calculation:0 — Calculation APT-OP-CAP-C1: needs_formal
- `APT-NF-071` operations.md#EnsureSession:rule:0 — Rule APT-OP-ENS-1: needs_formal (prose Formal)
- `APT-NF-072` operations.md#AppendReferenceProbeLineage:rule:12 — Rule APT-OP-PROBE-13: needs_formal (prose Formal)
- `APT-NF-073` operations.md#EnsureSession:rule:2 — Rule APT-OP-ENS-3: needs_formal (prose Formal)
- `APT-NF-074` operations.md#StartNewSession:calculation:0 — Calculation APT-OP-ROL-C1: needs_formal
- `APT-NF-075` operations.md#AppendResearchCapture:calculation:2 — Calculation APT-OP-CAP-C3: needs_formal
- `APT-NF-076` operations.md#AppendResearchFact:rule:0 — Rule APT-OP-FACT-1: needs_formal (prose Formal)
- `APT-NF-077` operations.md#AppendResearchCapture:rule:1 — Rule APT-OP-CAP-2: needs_formal (prose Formal)
- `APT-NF-078` states.md#Session Context Binding:invariant:2 — Invariant APT-STATE-I3: needs_formal (prose Formal)
- `APT-NF-079` operations.md#AppendReferenceProbeLineage:rule:15 — Rule APT-OP-PROBE-16: needs_formal (prose Formal)

needs-harness (derivable, requires a runtime/effect to test): 291

<!-- ENGINE-REGION-END -->
