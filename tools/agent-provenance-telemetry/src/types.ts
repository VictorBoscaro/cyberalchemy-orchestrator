export type OpaqueId = string;
export interface ContentDigest { algorithm: "sha256"; value: string }
export type CaptureStatus = "captured" | "partial" | "missing";
export type ExtractionMode = "verbatim" | "declared" | "inferred";

export type AcceptanceRef =
  | { kind: "accepted_event"; accepted_event_id: OpaqueId; contract_version: string; evidence_digest: ContentDigest }
  | { kind: "publication_receipt"; receipt_id: OpaqueId; contract_version: string; evidence_digest: ContentDigest };
export type RegistryRef =
  | { kind: "registry_event"; accepted_event_id: OpaqueId; protocol_profile_id: OpaqueId; protocol_profile_version: string; protocol_profile_digest: ContentDigest; contract_version: string; evidence_digest: ContentDigest }
  | { kind: "registry_receipt"; receipt_id: OpaqueId; protocol_profile_id: OpaqueId; protocol_profile_version: string; protocol_profile_digest: ContentDigest; contract_version: string; evidence_digest: ContentDigest };

export interface ArtifactReference {
  artifact_id: OpaqueId;
  content_digest: ContentDigest;
  media_type: string;
  charset: "utf-8";
  classification: string;
  redaction_policy_ref: OpaqueId;
  retention_policy_ref: OpaqueId;
  tombstone_policy_ref: OpaqueId;
  finalization_receipt_ref: OpaqueId;
}
export type DispatchAuthoritySnapshotRef =
  | { kind: "aci_managed"; dispatch_id: OpaqueId; artifact_ref: OpaqueId; artifact_digest: ContentDigest; accepted_event_id: OpaqueId; accepted_offset: number }
  | { kind: "legacy_ledger"; ledger_row_identity: { dispatch_id: OpaqueId; row_kind: string; appender_identity: OpaqueId; contract_version: string }; row_digest: ContentDigest; non_authoritative_locator?: { row_index: number } };
export type ProducerRef =
  | { kind: "seat"; group_id: OpaqueId; seat_id: OpaqueId; attempt_id: OpaqueId; activation_id: OpaqueId }
  | { kind: "host_actor"; host_actor_id: OpaqueId; activation_id: OpaqueId };
export interface OriginProfileRef {
  profile_id: OpaqueId; profile_version: string; profile_digest: ContentDigest;
}
export type ProbeAcceptanceRef =
  | { kind: "accepted_event"; accepted_event_id: OpaqueId; owner_namespace: "agents-communication-infra"; contract_version: string; evidence_digest: ContentDigest }
  | { kind: "publication_receipt"; receipt_id: OpaqueId; owner_namespace: "agents-communication-infra"; contract_version: string; evidence_digest: ContentDigest };
export type EvidenceOwnerRef =
  | { kind: "aci_event"; owner_namespace: "agents-communication-infra"; contract_version: string; accepted_event_id: OpaqueId; evidence_digest: ContentDigest }
  | { kind: "aci_receipt"; owner_namespace: "agents-communication-infra"; contract_version: string; receipt_id: OpaqueId; evidence_digest: ContentDigest }
  | { kind: "artifact"; owner_namespace: "agents-communication-infra"; contract_version: string; artifact_id: OpaqueId; evidence_digest: ContentDigest }
  | { kind: "host_observation"; owner_namespace: "host"; contract_version: string; source_observation_id: OpaqueId; evidence_digest: ContentDigest };
export type OriginRef = EvidenceOwnerRef
  | { kind: "probe"; owner_namespace: "agent-provenance-telemetry"; probe_schema_ref: string;
      probe_profile_ref: OriginProfileRef; probe_id: OpaqueId; aci_acceptance_ref: ProbeAcceptanceRef }
  | { kind: "probe_bundle"; owner_namespace: "agent-provenance-telemetry"; bundle_schema_ref: string;
      probe_profile_ref: OriginProfileRef; probe_id: OpaqueId; bundle_digest: ContentDigest;
      committed_event_id: OpaqueId; committed_event_digest: ContentDigest };
export interface CapturePin { research_capture_id: OpaqueId; capture_digest: ContentDigest }
export interface ResearchCapture {
  schema_ref: "apt.research-capture@1";
  research_capture_id: OpaqueId;
  expected_contribution_id: OpaqueId;
  capture_operation_id: OpaqueId;
  dispatch_id: OpaqueId;
  dispatch_snapshot_ref: DispatchAuthoritySnapshotRef;
  origin_refs: OriginRef[];
  producer_ref: ProducerRef;
  capture_status: CaptureStatus;
  raw_return: ArtifactReference | null;
  partial_reason: string | null;
  failure_reason: string | null;
  failure_evidence_ref: EvidenceOwnerRef | null;
  supersedes_capture_id: OpaqueId | null;
  synthesizes: CapturePin[];
  captured_at: string;
  capture_digest: ContentDigest;
}
export interface RawSelector {
  schema_ref: "apt.raw-selector@1"; unit: "utf8-byte";
  start_inclusive: number; end_exclusive: number; selected_text_digest: ContentDigest;
}
export interface ExtractionProvenance {
  mode: ExtractionMode; actor_ref: OpaqueId; method_ref: string; extracted_at: string;
  source_capture_id: OpaqueId; source_capture_digest: ContentDigest; selector: RawSelector;
}
export interface FactEnvelope {
  fact_id: OpaqueId; subject_id: OpaqueId; operation_id: OpaqueId;
  occurred_at: string; supersedes_fact_id: OpaqueId | null;
}
export type QuestionDerivationRef =
  | { kind: "dispatch_scope"; dispatch_snapshot_ref: DispatchAuthoritySnapshotRef; field_name: string; field_path: string }
  | { kind: "research_question"; research_question_id: OpaqueId; question_fact_id: OpaqueId;
      research_capture_id: OpaqueId; research_capture_digest: ContentDigest };
export type ResearchEvidenceRef =
  | { kind: "artifact"; artifact_ref: ArtifactReference }
  | { kind: "fact"; fact_id: OpaqueId; research_capture_id: OpaqueId };
interface EntityFactBase {
  research_capture_id: OpaqueId; fact: FactEnvelope; extraction: ExtractionProvenance;
}
export interface ResearchQuestion extends EntityFactBase { kind: "question"; research_question_id: OpaqueId; question_text: string; derives_from: QuestionDerivationRef[] }
export interface ResearchAnswer extends EntityFactBase { kind: "answer"; research_answer_id: OpaqueId; question_ids: OpaqueId[] }
export interface ResearchReferenceUse extends EntityFactBase {
  kind: "reference_use"; reference_use_id: OpaqueId; reference_id: OpaqueId;
  reference_kind: "file" | "url" | "paper" | "commit" | "dataset" | "command-output";
  locator_observed: string; source_observation_id: OpaqueId | null;
  probe_recommendation_ref: ProbeRecommendationRef | null;
  use_kind: "mentioned" | "cited" | "claimed_consulted";
  anchor_quality: "none" | "locator" | "span" | "digest";
}
export interface ResearchReferenceClaimRelation extends EntityFactBase {
  kind: "reference_claim_relation"; relation_id: OpaqueId; reference_use_id: OpaqueId;
  research_claim_id: OpaqueId; relation: "supports" | "partially_supports" | "contradicts" | "contextualizes" | "irrelevant";
}
export interface ReferenceCheck {
  kind: "reference_check"; reference_check_id: OpaqueId; research_capture_id: OpaqueId;
  fact: FactEnvelope; check_kind: "source_identity" | "access_evidence" | "claim_support";
  reference_use_id: OpaqueId; relation_id: OpaqueId | null; checked_by: OpaqueId;
  method_ref: string; result: "pass" | "fail" | "indeterminate"; evidence_ref: ArtifactReference | null;
}
export interface ResearchProblem extends EntityFactBase {
  kind: "problem"; problem_id: OpaqueId; problem_kind: "gap" | "contradiction" | "blocker" | "uncertainty" | "failed_check";
  statement: string; blocks: OpaqueId[]; evidence_refs: ResearchEvidenceRef[];
}
export interface ResearchClaimExtraction extends EntityFactBase {
  kind: "claim"; research_claim_id: OpaqueId; statement: string; answer_ids: OpaqueId[];
}
export interface FormalizationCandidate extends EntityFactBase {
  kind: "formalization"; formalization_id: OpaqueId; research_claim_id: OpaqueId;
  notation: string; latex: string | null; legend: Record<string, string>; reading: string;
  logic_family: string; assumptions: string[]; scope: string;
  syntax_checker_ref: OpaqueId | null; proof_check_ref: OpaqueId | null; governance_ref: OpaqueId | null;
}
export interface TargetRef { target_kind: "problem" | "claim" | "formalization"; target_id: OpaqueId; research_capture_id: OpaqueId }
type ProblemTarget = { target_kind: "problem"; target_id: OpaqueId; research_capture_id: OpaqueId };
type ClaimTarget = { target_kind: "claim"; target_id: OpaqueId; research_capture_id: OpaqueId };
type FormalizationTarget = { target_kind: "formalization"; target_id: OpaqueId; research_capture_id: OpaqueId };
type ProblemDisposition = "observed" | "validated" | "resolved" | "accepted_risk" | "refuted";
type ClaimDisposition = "proposed" | "supported" | "contested" | "refuted";
type FormalizationDisposition = "candidate" | "reviewed" | "rejected";
interface DispositionBase {
  kind: "disposition_recorded"; actor_ref: OpaqueId;
  policy_ref: OpaqueId; aggregate_type: "apt.disposition-chain"; aggregate_id: ContentDigest;
  expected_head_accepted_event_id: OpaqueId | null; expected_aggregate_version: number;
}
export type DispositionRecorded =
  | (DispositionBase & { target: ProblemTarget; disposition: ProblemDisposition })
  | (DispositionBase & { target: ClaimTarget; disposition: ClaimDisposition })
  | (DispositionBase & { target: FormalizationTarget; disposition: FormalizationDisposition });
interface AssessmentBase {
  kind: "assessment_recorded"; actor_ref: OpaqueId;
  method_ref: string; policy_ref: OpaqueId; aggregate_type: "apt.assessment-chain";
  aggregate_id: ContentDigest; expected_head_accepted_event_id: OpaqueId | null;
  expected_aggregate_version: number;
}
export type AssessmentRecorded =
  | (AssessmentBase & { target: ProblemTarget; assessment: ProblemDisposition })
  | (AssessmentBase & { target: ClaimTarget; assessment: ClaimDisposition })
  | (AssessmentBase & { target: FormalizationTarget; assessment: FormalizationDisposition });
export type ResearchFact = ResearchQuestion | ResearchAnswer | ResearchReferenceUse |
  ResearchReferenceClaimRelation | ReferenceCheck | ResearchProblem | ResearchClaimExtraction |
  FormalizationCandidate | DispositionRecorded | AssessmentRecorded;

export interface ACIProtocolProfileBinding {
  protocol_profile_id: OpaqueId; protocol_profile_version: string; protocol_profile_digest: ContentDigest;
}
export interface ProbeRecommendationRef {
  probe_id: OpaqueId; recommendation_id: OpaqueId; bundle_digest: ContentDigest;
  profile_binding: ACIProtocolProfileBinding; bundle_acceptance_ref: AcceptanceRef;
  profile_registration_ref: RegistryRef; source_observation_ids: OpaqueId[];
}
export interface Session {
  session_id: OpaqueId; ensure_key: OpaqueId; start_operation_id: OpaqueId;
  origin_kind: string; origin_ref: string; initial_name: string; started_at: string;
}
export interface SessionDispatchLink {
  session_dispatch_link_id: OpaqueId; session_id: OpaqueId; dispatch_id: OpaqueId;
  link_operation_id: OpaqueId; linked_at: string;
}
export type FixtureSuppliedEvent =
  | { provenance: "fixture-supplied-unverified"; event_id: OpaqueId; offset: number; type: "session_started"; payload: Session }
  | { provenance: "fixture-supplied-unverified"; event_id: OpaqueId; offset: number; type: "session_dispatch_linked"; payload: SessionDispatchLink }
  | { provenance: "fixture-supplied-unverified"; event_id: OpaqueId; offset: number; type: "research_capture_appended"; payload: ResearchCapture }
  | { provenance: "fixture-supplied-unverified"; event_id: OpaqueId; offset: number; type: "research_fact_appended"; payload: ResearchFact };
export interface CanonicalizerCandidate {
  canonicalizeCandidate(candidate: unknown): Uint8Array;
  digestCandidate(bytes: Uint8Array): ContentDigest;
}
export interface SelectorEvidenceVerifier {
  rawBytes(capture: ResearchCapture): Uint8Array | null;
  digest(bytes: Uint8Array): ContentDigest;
  canonicalBytesCandidate(value: unknown): Uint8Array;
  verifyDispatchScopePointer(snapshot: DispatchAuthoritySnapshotRef, fieldName: string, fieldPath: string): boolean;
  isCurrentCapture(capture: ResearchCapture): boolean;
}
export interface AptCandidateState {
  sessions: Map<string, Session>; ensureKeys: Map<string, string>; links: Map<string, SessionDispatchLink>;
  captures: Map<string, ResearchCapture>; currentCaptureByContribution: Map<string, string>;
  facts: Map<string, ResearchFact>; currentFactBySubject: Map<string, string>;
  aggregateHeads: Map<string, { accepted_event_id: string; version: number }>; throughOffset: number;
}
