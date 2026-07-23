import type {
  ACIProtocolProfileBinding, ArtifactReference, ContentDigest, ExtractionProvenance,
  ProbeRecommendationRef, ResearchCapture, ResearchFact, SelectorEvidenceVerifier,
  Session, SessionDispatchLink,
} from "./types.js";

export class ContractError extends Error {
  constructor(public readonly code: string, message = code) { super(`${code}: ${message}`); }
}
type Rec = Record<string, unknown>;
const rec = (v: unknown): Rec => {
  if (!v || typeof v !== "object" || Array.isArray(v)) throw new ContractError("OBJECT_REQUIRED");
  return v as Rec;
};
const exact = (r: Rec, keys: readonly string[]): void => {
  const actual = Object.keys(r).sort();
  const expected = [...keys].sort();
  if (actual.length !== expected.length || actual.some((k, i) => k !== expected[i]))
    throw new ContractError("UNKNOWN_OR_MISSING_FIELD", `${actual.join(",")} != ${expected.join(",")}`);
};
const str = (v: unknown, code = "STRING_REQUIRED"): string => {
  if (typeof v !== "string" || v.length === 0) throw new ContractError(code);
  return v;
};
const int = (v: unknown, code = "INTEGER_REQUIRED"): number => {
  if (!Number.isSafeInteger(v) || (v as number) < 0) throw new ContractError(code);
  return v as number;
};
const eq = (a: unknown, b: unknown): boolean => JSON.stringify(a) === JSON.stringify(b);
const compareBytes = (a: Uint8Array, b: Uint8Array): number => {
  const limit = Math.min(a.length, b.length);
  for (let i = 0; i < limit; i++) if (a[i] !== b[i]) return a[i]! - b[i]!;
  return a.length - b.length;
};
const assertCanonicalSet = (values: readonly unknown[], verifier: SelectorEvidenceVerifier, code: string): void => {
  const encoded = values.map((v) => verifier.canonicalBytesCandidate(v));
  const keys = encoded.map((v) => Buffer.from(v).toString("hex"));
  if (new Set(keys).size !== keys.length) throw new ContractError(`${code}_DUPLICATE`);
  const sorted = [...encoded].sort(compareBytes);
  if (encoded.some((v, i) => compareBytes(v, sorted[i]!) !== 0)) throw new ContractError(`${code}_ORDER`);
};

export function decodeDigest(v: unknown): ContentDigest {
  const r = rec(v); exact(r, ["algorithm", "value"]);
  if (r.algorithm !== "sha256" || typeof r.value !== "string" || !/^[0-9a-f]{64}$/.test(r.value))
    throw new ContractError("DIGEST_INVALID");
  return { algorithm: "sha256", value: r.value };
}
export function decodeArtifact(v: unknown): ArtifactReference {
  const r = rec(v); exact(r, ["artifact_id", "content_digest", "media_type", "charset", "classification",
    "redaction_policy_ref", "retention_policy_ref", "tombstone_policy_ref", "finalization_receipt_ref"]);
  if (r.charset !== "utf-8" || typeof r.media_type !== "string" || !/^text\//.test(r.media_type))
    throw new ContractError("ARTIFACT_TEXT_UTF8_REQUIRED");
  return {
    artifact_id: str(r.artifact_id), content_digest: decodeDigest(r.content_digest),
    media_type: r.media_type, charset: "utf-8", classification: str(r.classification),
    redaction_policy_ref: str(r.redaction_policy_ref), retention_policy_ref: str(r.retention_policy_ref),
    tombstone_policy_ref: str(r.tombstone_policy_ref), finalization_receipt_ref: str(r.finalization_receipt_ref),
  };
}
function decodeSnapshot(v: unknown) {
  const r = rec(v);
  if (r.kind === "aci_managed") {
    exact(r, ["kind", "dispatch_id", "artifact_ref", "artifact_digest", "accepted_event_id", "accepted_offset"]);
    return { kind: "aci_managed" as const, dispatch_id: str(r.dispatch_id), artifact_ref: str(r.artifact_ref),
      artifact_digest: decodeDigest(r.artifact_digest), accepted_event_id: str(r.accepted_event_id),
      accepted_offset: int(r.accepted_offset) };
  }
  if (r.kind === "legacy_ledger") {
    const keys = r.non_authoritative_locator === undefined
      ? ["kind", "ledger_row_identity", "row_digest"] : ["kind", "ledger_row_identity", "row_digest", "non_authoritative_locator"];
    exact(r, keys);
    const id = rec(r.ledger_row_identity); exact(id, ["dispatch_id", "row_kind", "appender_identity", "contract_version"]);
    const locator = r.non_authoritative_locator === undefined ? undefined : rec(r.non_authoritative_locator);
    if (locator) exact(locator, ["row_index"]);
    return { kind: "legacy_ledger" as const, ledger_row_identity: {
      dispatch_id: str(id.dispatch_id), row_kind: str(id.row_kind), appender_identity: str(id.appender_identity),
      contract_version: str(id.contract_version),
    }, row_digest: decodeDigest(r.row_digest),
    ...(locator ? { non_authoritative_locator: { row_index: int(locator.row_index) } } : {}) };
  }
  throw new ContractError("SNAPSHOT_VARIANT_INVALID");
}
function decodeProducer(v: unknown) {
  const r = rec(v);
  if (r.kind === "seat") {
    exact(r, ["kind", "group_id", "seat_id", "attempt_id", "activation_id"]);
    return { kind: "seat" as const, group_id: str(r.group_id), seat_id: str(r.seat_id),
      attempt_id: str(r.attempt_id), activation_id: str(r.activation_id) };
  }
  if (r.kind === "host_actor") {
    exact(r, ["kind", "host_actor_id", "activation_id"]);
    return { kind: "host_actor" as const, host_actor_id: str(r.host_actor_id), activation_id: str(r.activation_id) };
  }
  throw new ContractError("PRODUCER_VARIANT_INVALID");
}
function decodeOrigin(v: unknown): ResearchCapture["origin_refs"][number] {
  const r = rec(v);
  if (r.kind === "probe") {
    exact(r, ["kind", "owner_namespace", "probe_schema_ref", "probe_profile_ref", "probe_id", "aci_acceptance_ref"]);
    if (r.owner_namespace !== "agent-provenance-telemetry") throw new ContractError("OWNER_NAMESPACE_INVALID");
    return { kind: "probe", owner_namespace: r.owner_namespace, probe_schema_ref: str(r.probe_schema_ref),
      probe_profile_ref: decodeOriginProfile(r.probe_profile_ref), probe_id: str(r.probe_id),
      aci_acceptance_ref: decodeProbeAcceptance(r.aci_acceptance_ref) };
  }
  if (r.kind === "probe_bundle") {
    exact(r, ["kind", "owner_namespace", "bundle_schema_ref", "probe_profile_ref", "probe_id",
      "bundle_digest", "committed_event_id", "committed_event_digest"]);
    if (r.owner_namespace !== "agent-provenance-telemetry") throw new ContractError("OWNER_NAMESPACE_INVALID");
    return { kind: "probe_bundle", owner_namespace: r.owner_namespace, bundle_schema_ref: str(r.bundle_schema_ref),
      probe_profile_ref: decodeOriginProfile(r.probe_profile_ref), probe_id: str(r.probe_id),
      bundle_digest: decodeDigest(r.bundle_digest), committed_event_id: str(r.committed_event_id),
      committed_event_digest: decodeDigest(r.committed_event_digest) };
  }
  if (r.kind === "aci_event") {
    exact(r, ["kind", "owner_namespace", "contract_version", "accepted_event_id", "evidence_digest"]);
    if (r.owner_namespace !== "agents-communication-infra") throw new ContractError("OWNER_NAMESPACE_INVALID");
    return { kind: "aci_event", owner_namespace: r.owner_namespace, contract_version: str(r.contract_version),
      accepted_event_id: str(r.accepted_event_id), evidence_digest: decodeDigest(r.evidence_digest) };
  }
  if (r.kind === "aci_receipt") {
    exact(r, ["kind", "owner_namespace", "contract_version", "receipt_id", "evidence_digest"]);
    if (r.owner_namespace !== "agents-communication-infra") throw new ContractError("OWNER_NAMESPACE_INVALID");
    return { kind: "aci_receipt", owner_namespace: r.owner_namespace, contract_version: str(r.contract_version),
      receipt_id: str(r.receipt_id), evidence_digest: decodeDigest(r.evidence_digest) };
  }
  if (r.kind === "artifact") {
    exact(r, ["kind", "owner_namespace", "contract_version", "artifact_id", "evidence_digest"]);
    if (r.owner_namespace !== "agents-communication-infra") throw new ContractError("OWNER_NAMESPACE_INVALID");
    return { kind: "artifact", owner_namespace: r.owner_namespace, contract_version: str(r.contract_version),
      artifact_id: str(r.artifact_id), evidence_digest: decodeDigest(r.evidence_digest) };
  }
  if (r.kind === "host_observation") {
    exact(r, ["kind", "owner_namespace", "contract_version", "source_observation_id", "evidence_digest"]);
    if (r.owner_namespace !== "host") throw new ContractError("OWNER_NAMESPACE_INVALID");
    return { kind: "host_observation", owner_namespace: "host", contract_version: str(r.contract_version),
      source_observation_id: str(r.source_observation_id), evidence_digest: decodeDigest(r.evidence_digest) };
  }
  throw new ContractError("ORIGIN_VARIANT_INVALID");
}
function decodeOriginProfile(v: unknown) {
  const r = rec(v); exact(r, ["profile_id", "profile_version", "profile_digest"]);
  return { profile_id: str(r.profile_id), profile_version: str(r.profile_version),
    profile_digest: decodeDigest(r.profile_digest) };
}
function decodeProbeAcceptance(v: unknown) {
  const r = rec(v);
  if (r.kind === "accepted_event") {
    exact(r, ["kind", "accepted_event_id", "owner_namespace", "contract_version", "evidence_digest"]);
    if (r.owner_namespace !== "agents-communication-infra") throw new ContractError("OWNER_NAMESPACE_INVALID");
    return { kind: "accepted_event" as const, accepted_event_id: str(r.accepted_event_id),
      owner_namespace: "agents-communication-infra" as const, contract_version: str(r.contract_version),
      evidence_digest: decodeDigest(r.evidence_digest) };
  }
  if (r.kind === "publication_receipt") {
    exact(r, ["kind", "receipt_id", "owner_namespace", "contract_version", "evidence_digest"]);
    if (r.owner_namespace !== "agents-communication-infra") throw new ContractError("OWNER_NAMESPACE_INVALID");
    return { kind: "publication_receipt" as const, receipt_id: str(r.receipt_id),
      owner_namespace: "agents-communication-infra" as const, contract_version: str(r.contract_version),
      evidence_digest: decodeDigest(r.evidence_digest) };
  }
  throw new ContractError("PROBE_ACCEPTANCE_VARIANT_INVALID");
}
function decodeFailureEvidence(v: unknown): ResearchCapture["failure_evidence_ref"] {
  const decoded = decodeOrigin(v);
  if (decoded.kind === "probe" || decoded.kind === "probe_bundle")
    throw new ContractError("FAILURE_EVIDENCE_VARIANT_INVALID");
  return decoded;
}
export function decodeResearchCapture(v: unknown, verifier: SelectorEvidenceVerifier): ResearchCapture {
  const r = rec(v); exact(r, ["schema_ref", "research_capture_id", "expected_contribution_id",
    "capture_operation_id", "dispatch_id", "dispatch_snapshot_ref", "origin_refs", "producer_ref",
    "capture_status", "raw_return", "partial_reason", "failure_reason", "failure_evidence_ref",
    "supersedes_capture_id", "synthesizes", "captured_at", "capture_digest"]);
  if (r.schema_ref !== "apt.research-capture@1" || !["captured", "partial", "missing"].includes(String(r.capture_status)))
    throw new ContractError("CAPTURE_SCHEMA_INVALID");
  const snapshot = decodeSnapshot(r.dispatch_snapshot_ref);
  const dispatchId = str(r.dispatch_id);
  const snapshotDispatch = snapshot.kind === "aci_managed" ? snapshot.dispatch_id : snapshot.ledger_row_identity.dispatch_id;
  if (dispatchId !== snapshotDispatch) throw new ContractError("DISPATCH_SNAPSHOT_MISMATCH");
  if (!Array.isArray(r.origin_refs) || !Array.isArray(r.synthesizes)) throw new ContractError("ARRAY_REQUIRED");
  const pins = r.synthesizes.map((x) => {
    const p = rec(x); exact(p, ["research_capture_id", "capture_digest"]);
    return { research_capture_id: str(p.research_capture_id), capture_digest: decodeDigest(p.capture_digest) };
  });
  if (new Set(pins.map((p) => p.research_capture_id)).size !== pins.length) throw new ContractError("SYNTHESIS_DUPLICATE");
  const origins = r.origin_refs.map(decodeOrigin);
  assertCanonicalSet(origins, verifier, "ORIGIN_SET_NONCANONICAL");
  const result: ResearchCapture = {
    schema_ref: "apt.research-capture@1", research_capture_id: str(r.research_capture_id),
    expected_contribution_id: str(r.expected_contribution_id), capture_operation_id: str(r.capture_operation_id),
    dispatch_id: dispatchId, dispatch_snapshot_ref: snapshot, origin_refs: origins,
    producer_ref: decodeProducer(r.producer_ref), capture_status: r.capture_status as ResearchCapture["capture_status"],
    raw_return: r.raw_return === null ? null : decodeArtifact(r.raw_return),
    partial_reason: r.partial_reason === null ? null : str(r.partial_reason),
    failure_reason: r.failure_reason === null ? null : str(r.failure_reason),
    failure_evidence_ref: r.failure_evidence_ref === null ? null : decodeFailureEvidence(r.failure_evidence_ref),
    supersedes_capture_id: r.supersedes_capture_id === null ? null : str(r.supersedes_capture_id),
    synthesizes: pins, captured_at: decodeRfc3339OffsetTimestamp(r.captured_at), capture_digest: decodeDigest(r.capture_digest),
  };
  validateCapture(result);
  return structuredClone(result);
}
export function validateCapture(c: ResearchCapture): void {
  if (c.synthesizes.some((p) => p.research_capture_id === c.research_capture_id)) throw new ContractError("SYNTHESIS_SELF");
  if (c.capture_status === "captured" && (!c.raw_return || c.partial_reason !== null || c.failure_reason !== null || c.failure_evidence_ref !== null))
    throw new ContractError("CAPTURE_STATUS_MATRIX");
  if (c.capture_status === "partial" && (!c.raw_return || !c.partial_reason || c.failure_reason !== null))
    throw new ContractError("CAPTURE_STATUS_MATRIX");
  if (c.capture_status === "missing" && (c.raw_return !== null || c.partial_reason !== null || !c.failure_reason || !c.failure_evidence_ref))
    throw new ContractError("CAPTURE_STATUS_MATRIX");
}
const entityId = (f: ResearchFact): string | null => {
  switch (f.kind) {
    case "question": return f.research_question_id; case "answer": return f.research_answer_id;
    case "reference_use": return f.reference_use_id; case "reference_claim_relation": return f.relation_id;
    case "reference_check": return f.reference_check_id; case "problem": return f.problem_id;
    case "claim": return f.research_claim_id; case "formalization": return f.formalization_id;
    default: return null;
  }
};
type EntityResearchFact = Extract<ResearchFact, { fact: unknown }>;
export function validateExtraction(x: ExtractionProvenance, c: ResearchCapture, verifier: SelectorEvidenceVerifier): void {
  if (c.capture_status === "missing" || x.source_capture_id !== c.research_capture_id || !eq(x.source_capture_digest, c.capture_digest))
    throw new ContractError("EXTRACTION_CAPTURE_INVALID");
  const bytes = verifier.rawBytes(c);
  if (!bytes || x.selector.start_inclusive < 0 || x.selector.end_exclusive <= x.selector.start_inclusive ||
      x.selector.end_exclusive > bytes.byteLength) throw new ContractError("SELECTOR_RANGE_INVALID");
  if (!c.raw_return || !eq(verifier.digest(bytes), c.raw_return.content_digest))
    throw new ContractError("RAW_ARTIFACT_DIGEST_INVALID");
  const slice = bytes.slice(x.selector.start_inclusive, x.selector.end_exclusive);
  try { new TextDecoder("utf-8", { fatal: true }).decode(slice); } catch { throw new ContractError("SELECTOR_UTF8_INVALID"); }
  if (!eq(verifier.digest(slice), x.selector.selected_text_digest)) throw new ContractError("SELECTOR_DIGEST_INVALID");
}
const currentBySubject = (known: Map<string, ResearchFact>, subject: string): ResearchFact | undefined => {
  const versions = [...known.values()].filter((f): f is EntityResearchFact =>
    entityId(f) === subject && "fact" in f);
  const heads = versions.filter((candidate) => !versions.some((other) =>
    other !== candidate && "fact" in other && other.fact.supersedes_fact_id === candidate.fact.fact_id));
  return heads.length === 1 ? heads[0] : undefined;
};
export function validateFact(f: ResearchFact, c: ResearchCapture, known: Map<string, ResearchFact>, verifier: SelectorEvidenceVerifier): void {
  if (c.capture_status === "missing" || !verifier.isCurrentCapture(c))
    throw new ContractError("FACT_CAPTURE_NOT_CURRENT_OR_MISSING");
  if ("target" in f) {
    if (f.target.research_capture_id !== c.research_capture_id) throw new ContractError("TARGET_CAPTURE_INVALID");
    const target = currentBySubject(known, f.target.target_id);
    if (!target || target.kind !== f.target.target_kind || !("research_capture_id" in target) ||
        target.research_capture_id !== f.target.research_capture_id)
      throw new ContractError("TARGET_NOT_FOUND_CURRENT_LOCAL");
    return;
  }
  if (f.research_capture_id !== c.research_capture_id || f.fact.subject_id !== entityId(f))
    throw new ContractError("FACT_SUBJECT_OR_CAPTURE_INVALID");
  if ("extraction" in f) validateExtraction(f.extraction, c, verifier);
  const local = (id: string, kind: ResearchFact["kind"]) => {
    const target = currentBySubject(known, id);
    if (!target || target.kind !== kind || !("research_capture_id" in target) || target.research_capture_id !== c.research_capture_id)
      throw new ContractError("TARGET_NOT_FOUND_OR_NONLOCAL");
  };
  if (f.kind === "answer") {
    if (!f.question_ids.length) throw new ContractError("QUESTION_REQUIRED");
    f.question_ids.forEach((id) => local(id, "question"));
  } else if (f.kind === "claim") f.answer_ids.forEach((id) => local(id, "answer"));
  else if (f.kind === "reference_claim_relation") { local(f.reference_use_id, "reference_use"); local(f.research_claim_id, "claim"); }
  else if (f.kind === "reference_check") {
    local(f.reference_use_id, "reference_use");
    if ((f.check_kind === "claim_support") !== (f.relation_id !== null)) throw new ContractError("CHECK_RELATION_INVALID");
    if (f.relation_id) {
      local(f.relation_id, "reference_claim_relation");
      const relation = currentBySubject(known, f.relation_id);
      if (!relation || relation.kind !== "reference_claim_relation" ||
          relation.reference_use_id !== f.reference_use_id) throw new ContractError("CHECK_RELATION_USE_MISMATCH");
    }
  } else if (f.kind === "problem") {
    const allowed = new Set(["question", "answer", "reference_use", "reference_claim_relation",
      "reference_check", "problem", "claim", "formalization"]);
    for (const id of f.blocks) {
      const target = currentBySubject(known, id);
      if (!target || !allowed.has(target.kind) || !("research_capture_id" in target) ||
          target.research_capture_id !== c.research_capture_id)
        throw new ContractError("PROBLEM_BLOCK_TARGET_NOT_CURRENT_LOCAL");
    }
  } else if (f.kind === "formalization") local(f.research_claim_id, "claim");
}
function decodeEnvelope(v: unknown) {
  const r = rec(v); exact(r, ["fact_id", "subject_id", "operation_id", "occurred_at", "supersedes_fact_id"]);
  return { fact_id: str(r.fact_id), subject_id: str(r.subject_id), operation_id: str(r.operation_id),
    occurred_at: decodeRfc3339OffsetTimestamp(r.occurred_at),
    supersedes_fact_id: r.supersedes_fact_id === null ? null : str(r.supersedes_fact_id) };
}
function decodeExtraction(v: unknown): ExtractionProvenance {
  const r = rec(v); exact(r, ["mode", "actor_ref", "method_ref", "extracted_at", "source_capture_id", "source_capture_digest", "selector"]);
  if (!["verbatim", "declared", "inferred"].includes(String(r.mode))) throw new ContractError("EXTRACTION_MODE_INVALID");
  const s = rec(r.selector); exact(s, ["schema_ref", "unit", "start_inclusive", "end_exclusive", "selected_text_digest"]);
  if (s.schema_ref !== "apt.raw-selector@1" || s.unit !== "utf8-byte") throw new ContractError("SELECTOR_SCHEMA_INVALID");
  return { mode: r.mode as ExtractionProvenance["mode"], actor_ref: str(r.actor_ref), method_ref: str(r.method_ref),
    extracted_at: decodeRfc3339OffsetTimestamp(r.extracted_at), source_capture_id: str(r.source_capture_id),
    source_capture_digest: decodeDigest(r.source_capture_digest), selector: {
      schema_ref: "apt.raw-selector@1", unit: "utf8-byte", start_inclusive: int(s.start_inclusive),
      end_exclusive: int(s.end_exclusive), selected_text_digest: decodeDigest(s.selected_text_digest),
    } };
}
const factKeys: Record<string, readonly string[]> = {
  question: ["kind", "research_question_id", "research_capture_id", "fact", "question_text", "derives_from", "extraction"],
  answer: ["kind", "research_answer_id", "research_capture_id", "fact", "question_ids", "extraction"],
  reference_use: ["kind", "reference_use_id", "research_capture_id", "fact", "reference_id", "reference_kind", "locator_observed", "source_observation_id", "probe_recommendation_ref", "use_kind", "anchor_quality", "extraction"],
  reference_claim_relation: ["kind", "relation_id", "research_capture_id", "fact", "reference_use_id", "research_claim_id", "relation", "extraction"],
  reference_check: ["kind", "reference_check_id", "research_capture_id", "fact", "check_kind", "reference_use_id", "relation_id", "checked_by", "method_ref", "result", "evidence_ref"],
  problem: ["kind", "problem_id", "research_capture_id", "fact", "problem_kind", "statement", "blocks", "evidence_refs", "extraction"],
  claim: ["kind", "research_claim_id", "research_capture_id", "fact", "statement", "answer_ids", "extraction"],
  formalization: ["kind", "formalization_id", "research_capture_id", "fact", "research_claim_id", "notation", "latex", "legend", "reading", "logic_family", "assumptions", "scope", "extraction", "syntax_checker_ref", "proof_check_ref", "governance_ref"],
  disposition_recorded: ["kind", "target", "disposition", "actor_ref", "policy_ref", "aggregate_type", "aggregate_id", "expected_head_accepted_event_id", "expected_aggregate_version"],
  assessment_recorded: ["kind", "target", "assessment", "actor_ref", "method_ref", "policy_ref", "aggregate_type", "aggregate_id", "expected_head_accepted_event_id", "expected_aggregate_version"],
};
function decodeStringList(v: unknown, canonicalSet: boolean, verifier: SelectorEvidenceVerifier): string[] {
  if (!Array.isArray(v)) throw new ContractError("ARRAY_REQUIRED");
  const values = v.map((x) => str(x));
  if (canonicalSet) assertCanonicalSet(values, verifier, "STRING_SET_NONCANONICAL");
  return values;
}
function decodeDerivation(v: unknown, c: ResearchCapture, known: Map<string, ResearchFact>, verifier: SelectorEvidenceVerifier) {
  const r = rec(v);
  if (r.kind === "dispatch_scope") {
    exact(r, ["kind", "dispatch_snapshot_ref", "field_name", "field_path"]);
    const snapshot = decodeSnapshot(r.dispatch_snapshot_ref);
    if (!eq(snapshot, c.dispatch_snapshot_ref)) throw new ContractError("DERIVATION_SNAPSHOT_MISMATCH");
    const fieldPath = str(r.field_path); const fieldName = str(r.field_name);
    if (!verifier.verifyDispatchScopePointer(snapshot, fieldName, fieldPath))
      throw new ContractError("DERIVATION_POINTER_UNVERIFIED");
    return { kind: "dispatch_scope" as const, dispatch_snapshot_ref: snapshot,
      field_name: fieldName, field_path: fieldPath };
  }
  if (r.kind === "research_question") {
    exact(r, ["kind", "research_question_id", "question_fact_id", "research_capture_id", "research_capture_digest"]);
    const id = str(r.research_question_id);
    const source = [...known.values()].find((f): f is Extract<ResearchFact, { kind: "question" }> =>
      f.kind === "question" && f.fact.fact_id === r.question_fact_id);
    if (!source || source.research_question_id !== id ||
        source.research_capture_id !== c.research_capture_id || r.research_capture_id !== c.research_capture_id ||
        !eq(decodeDigest(r.research_capture_digest), c.capture_digest))
      throw new ContractError("DERIVATION_QUESTION_INVALID");
    return { kind: "research_question" as const, research_question_id: id,
      question_fact_id: str(r.question_fact_id), research_capture_id: str(r.research_capture_id),
      research_capture_digest: decodeDigest(r.research_capture_digest) };
  }
  throw new ContractError("DERIVATION_VARIANT_INVALID");
}
function decodeEvidenceRef(v: unknown, c: ResearchCapture, known: Map<string, ResearchFact>) {
  const r = rec(v);
  if (r.kind === "artifact") {
    exact(r, ["kind", "artifact_ref"]);
    return { kind: "artifact" as const, artifact_ref: decodeArtifact(r.artifact_ref) };
  }
  if (r.kind === "fact") {
    exact(r, ["kind", "fact_id", "research_capture_id"]);
    const factId = str(r.fact_id); const captureId = str(r.research_capture_id);
    const target = known.get(factId);
    if (!target || !("fact" in target) || !("research_capture_id" in target) ||
        target.research_capture_id !== c.research_capture_id || captureId !== c.research_capture_id ||
        !("fact" in (currentBySubject(known, target.fact.subject_id) ?? {})) ||
        (currentBySubject(known, target.fact.subject_id) as EntityResearchFact).fact.fact_id !== factId)
      throw new ContractError("FACT_EVIDENCE_NOT_CURRENT_OR_LOCAL");
    return { kind: "fact" as const, fact_id: factId, research_capture_id: captureId };
  }
  throw new ContractError("RESEARCH_EVIDENCE_VARIANT_INVALID");
}
function decodeLegend(v: unknown): Record<string, string> {
  const r = rec(v); const entries = Object.entries(r);
  if (!entries.length) throw new ContractError("LEGEND_NONEMPTY_REQUIRED");
  const out: Record<string, string> = {};
  for (const [key, value] of entries) out[str(key)] = str(value);
  return out;
}
export function decodeResearchFact(v: unknown, c: ResearchCapture, known: Map<string, ResearchFact>, verifier: SelectorEvidenceVerifier): ResearchFact {
  const r = rec(structuredClone(v)); const kind = str(r.kind);
  const keys = factKeys[kind]; if (!keys) throw new ContractError("FACT_VARIANT_INVALID");
  exact(r, keys);
  if ("fact" in r) r.fact = decodeEnvelope(r.fact);
  if ("extraction" in r) r.extraction = decodeExtraction(r.extraction);
  if (r.evidence_ref !== undefined && r.evidence_ref !== null) r.evidence_ref = decodeArtifact(r.evidence_ref);
  if (kind === "reference_use" && r.probe_recommendation_ref !== null)
    r.probe_recommendation_ref = decodeProbeRecommendation(r.probe_recommendation_ref, verifier);
  if (r.aggregate_id !== undefined) r.aggregate_id = decodeDigest(r.aggregate_id);
  if (kind === "disposition_recorded" || kind === "assessment_recorded") {
    const t = rec(r.target); exact(t, ["target_kind", "target_id", "research_capture_id"]);
    if (!["problem", "claim", "formalization"].includes(String(t.target_kind))) throw new ContractError("TARGET_KIND_INVALID");
    r.target = { target_kind: t.target_kind, target_id: str(t.target_id), research_capture_id: str(t.research_capture_id) };
    const requiredType = kind === "disposition_recorded" ? "apt.disposition-chain" : "apt.assessment-chain";
    if (r.aggregate_type !== requiredType || !Number.isSafeInteger(r.expected_aggregate_version) ||
        (r.expected_aggregate_version as number) < 0) throw new ContractError("AGGREGATE_SHAPE_INVALID");
    r.actor_ref = str(r.actor_ref); r.policy_ref = str(r.policy_ref);
    r.expected_head_accepted_event_id = r.expected_head_accepted_event_id === null
      ? null : str(r.expected_head_accepted_event_id);
    const allowed = t.target_kind === "problem"
      ? ["observed", "validated", "resolved", "accepted_risk", "refuted"]
      : t.target_kind === "claim" ? ["proposed", "supported", "contested", "refuted"]
      : ["candidate", "reviewed", "rejected"];
    if (kind === "disposition_recorded") {
      r.disposition = str(r.disposition);
      if (!allowed.includes(r.disposition as string)) throw new ContractError("DISPOSITION_TARGET_KIND_MISMATCH");
    } else {
      r.assessment = str(r.assessment); r.method_ref = str(r.method_ref);
      if (!allowed.includes(r.assessment as string)) throw new ContractError("ASSESSMENT_TARGET_KIND_MISMATCH");
    }
  }
  if ("research_capture_id" in r) r.research_capture_id = str(r.research_capture_id);
  if (kind === "question") {
    r.research_question_id = str(r.research_question_id); r.question_text = str(r.question_text);
    if (!Array.isArray(r.derives_from)) throw new ContractError("ARRAY_REQUIRED");
    const derivations = r.derives_from.map((x: unknown) => decodeDerivation(x, c, known, verifier));
    r.derives_from = derivations;
    assertCanonicalSet(derivations, verifier, "DERIVATION_SET_NONCANONICAL");
  } else if (kind === "answer") {
    r.research_answer_id = str(r.research_answer_id); r.question_ids = decodeStringList(r.question_ids, true, verifier);
  } else if (kind === "reference_use") {
    for (const key of ["reference_use_id", "reference_id", "locator_observed"]) r[key] = str(r[key]);
    r.source_observation_id = r.source_observation_id === null ? null : str(r.source_observation_id);
  } else if (kind === "reference_claim_relation") {
    for (const key of ["relation_id", "reference_use_id", "research_claim_id"]) r[key] = str(r[key]);
  } else if (kind === "reference_check") {
    for (const key of ["reference_check_id", "reference_use_id", "checked_by", "method_ref"]) r[key] = str(r[key]);
    r.relation_id = r.relation_id === null ? null : str(r.relation_id);
  } else if (kind === "problem") {
    r.problem_id = str(r.problem_id); r.statement = str(r.statement);
    r.blocks = decodeStringList(r.blocks, true, verifier);
    if (!Array.isArray(r.evidence_refs)) throw new ContractError("ARRAY_REQUIRED");
    const evidenceRefs = r.evidence_refs.map((x: unknown) => decodeEvidenceRef(x, c, known));
    r.evidence_refs = evidenceRefs;
    assertCanonicalSet(evidenceRefs, verifier, "EVIDENCE_SET_NONCANONICAL");
  } else if (kind === "claim") {
    r.research_claim_id = str(r.research_claim_id); r.statement = str(r.statement);
    r.answer_ids = decodeStringList(r.answer_ids, true, verifier);
  } else if (kind === "formalization") {
    for (const key of ["formalization_id", "research_claim_id", "notation", "reading", "logic_family", "scope"])
      r[key] = str(r[key]);
    r.latex = r.latex === null ? null : str(r.latex); r.legend = decodeLegend(r.legend);
    r.assumptions = decodeStringList(r.assumptions, false, verifier);
    for (const key of ["syntax_checker_ref", "proof_check_ref", "governance_ref"])
      r[key] = r[key] === null ? null : str(r[key]);
  }
  const out = structuredClone(r) as unknown as ResearchFact;
  if (out.kind === "reference_use") {
    if (!["file", "url", "paper", "commit", "dataset", "command-output"].includes(out.reference_kind) ||
        !["mentioned", "cited", "claimed_consulted"].includes(out.use_kind) ||
        !["none", "locator", "span", "digest"].includes(out.anchor_quality)) throw new ContractError("REFERENCE_USE_ENUM_INVALID");
  } else if (out.kind === "reference_claim_relation" &&
    !["supports", "partially_supports", "contradicts", "contextualizes", "irrelevant"].includes(out.relation))
    throw new ContractError("RELATION_ENUM_INVALID");
  else if (out.kind === "reference_check" &&
    (!["source_identity", "access_evidence", "claim_support"].includes(out.check_kind) ||
      !["pass", "fail", "indeterminate"].includes(out.result)))
    throw new ContractError("REFERENCE_CHECK_ENUM_INVALID");
  else if (out.kind === "problem" &&
    !["gap", "contradiction", "blocker", "uncertainty", "failed_check"].includes(out.problem_kind))
    throw new ContractError("PROBLEM_KIND_INVALID");
  validateFact(out, c, known, verifier);
  return out;
}
export function resolveSingleJoin(links: Iterable<SessionDispatchLink>, candidate: SessionDispatchLink): "new" | "existing_exact" {
  for (const link of links) {
    if (link.dispatch_id === candidate.dispatch_id) {
      if (eq(link, candidate)) return "existing_exact";
      throw new ContractError("JOIN_CONFLICT");
    }
  }
  return "new";
}
export function decodeSession(v: unknown): Session {
  const r = rec(v); exact(r, ["session_id", "ensure_key", "start_operation_id", "origin_kind",
    "origin_ref", "initial_name", "started_at"]);
  return { session_id: str(r.session_id), ensure_key: str(r.ensure_key),
    start_operation_id: str(r.start_operation_id), origin_kind: str(r.origin_kind),
    origin_ref: str(r.origin_ref), initial_name: str(r.initial_name),
    started_at: decodeRfc3339OffsetTimestamp(r.started_at) };
}
export function decodeSessionDispatchLink(v: unknown): SessionDispatchLink {
  const r = rec(v); exact(r, ["session_dispatch_link_id", "session_id", "dispatch_id",
    "link_operation_id", "linked_at"]);
  return { session_dispatch_link_id: str(r.session_dispatch_link_id), session_id: str(r.session_id),
    dispatch_id: str(r.dispatch_id), link_operation_id: str(r.link_operation_id),
    linked_at: decodeRfc3339OffsetTimestamp(r.linked_at) };
}
export function authorizeSessionRollover(actor: string, explicit: boolean): void {
  if (!explicit || !["host", "human"].includes(actor)) throw new ContractError("ROLLOVER_NOT_AUTHORIZED");
}
export function validateProfileBinding(candidate: ACIProtocolProfileBinding, registration: ProbeRecommendationRef["profile_registration_ref"]): void {
  if (candidate.protocol_profile_id !== registration.protocol_profile_id ||
      candidate.protocol_profile_version !== registration.protocol_profile_version ||
      !eq(candidate.protocol_profile_digest, registration.protocol_profile_digest))
    throw new ContractError("PROFILE_BINDING_STRUCTURAL_MISMATCH");
}
export function validateProbeRecommendation(ref: ProbeRecommendationRef, verifier: SelectorEvidenceVerifier): void {
  validateProfileBinding(ref.profile_binding, ref.profile_registration_ref);
  assertCanonicalSet(ref.source_observation_ids, verifier, "PROBE_SOURCE_OBSERVATION_NONCANONICAL");
}
function decodeAcceptance(v: unknown): ProbeRecommendationRef["bundle_acceptance_ref"] {
  const r = rec(v);
  if (r.kind === "accepted_event") {
    exact(r, ["kind", "accepted_event_id", "contract_version", "evidence_digest"]);
    return { kind: "accepted_event", accepted_event_id: str(r.accepted_event_id),
      contract_version: str(r.contract_version), evidence_digest: decodeDigest(r.evidence_digest) };
  }
  if (r.kind === "publication_receipt") {
    exact(r, ["kind", "receipt_id", "contract_version", "evidence_digest"]);
    return { kind: "publication_receipt", receipt_id: str(r.receipt_id),
      contract_version: str(r.contract_version), evidence_digest: decodeDigest(r.evidence_digest) };
  }
  throw new ContractError("ACCEPTANCE_VARIANT_INVALID");
}
function decodeRegistry(v: unknown): ProbeRecommendationRef["profile_registration_ref"] {
  const r = rec(v);
  const common = ["kind", "protocol_profile_id", "protocol_profile_version", "protocol_profile_digest", "contract_version", "evidence_digest"];
  if (r.kind === "registry_event") {
    exact(r, [...common, "accepted_event_id"]);
    return { kind: "registry_event", accepted_event_id: str(r.accepted_event_id),
      protocol_profile_id: str(r.protocol_profile_id), protocol_profile_version: str(r.protocol_profile_version),
      protocol_profile_digest: decodeDigest(r.protocol_profile_digest), contract_version: str(r.contract_version),
      evidence_digest: decodeDigest(r.evidence_digest) };
  }
  if (r.kind === "registry_receipt") {
    exact(r, [...common, "receipt_id"]);
    return { kind: "registry_receipt", receipt_id: str(r.receipt_id),
      protocol_profile_id: str(r.protocol_profile_id), protocol_profile_version: str(r.protocol_profile_version),
      protocol_profile_digest: decodeDigest(r.protocol_profile_digest), contract_version: str(r.contract_version),
      evidence_digest: decodeDigest(r.evidence_digest) };
  }
  throw new ContractError("REGISTRY_VARIANT_INVALID");
}
export function decodeProbeRecommendation(v: unknown, verifier: SelectorEvidenceVerifier): ProbeRecommendationRef {
  const r = rec(v); exact(r, ["probe_id", "recommendation_id", "bundle_digest", "profile_binding",
    "bundle_acceptance_ref", "profile_registration_ref", "source_observation_ids"]);
  const b = rec(r.profile_binding); exact(b, ["protocol_profile_id", "protocol_profile_version", "protocol_profile_digest"]);
  if (!Array.isArray(r.source_observation_ids)) throw new ContractError("ARRAY_REQUIRED");
  const out: ProbeRecommendationRef = {
    probe_id: str(r.probe_id), recommendation_id: str(r.recommendation_id),
    bundle_digest: decodeDigest(r.bundle_digest), profile_binding: {
      protocol_profile_id: str(b.protocol_profile_id), protocol_profile_version: str(b.protocol_profile_version),
      protocol_profile_digest: decodeDigest(b.protocol_profile_digest),
    }, bundle_acceptance_ref: decodeAcceptance(r.bundle_acceptance_ref),
    profile_registration_ref: decodeRegistry(r.profile_registration_ref),
    source_observation_ids: r.source_observation_ids.map((x) => str(x)),
  };
  validateProbeRecommendation(out, verifier); return structuredClone(out);
}
const prohibited = /(raw|body|selector|question|answer|claim|problem|notation|locator|credential|exception)/i;
export function decodeRfc3339OffsetTimestamp(input: unknown): string {
  const value = str(input, "RFC3339_TIMESTAMP_REQUIRED");
  const m = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.(\d+))?(Z|([+-])(\d{2}):(\d{2}))$/.exec(value);
  if (!m) throw new ContractError("RFC3339_TIMESTAMP_INVALID");
  const [year, month, day, hour, minute, second] = m.slice(1, 7).map(Number);
  if (!year || month! < 1 || month! > 12 || hour! > 23 || minute! > 59 || second! > 59)
    throw new ContractError("RFC3339_TIMESTAMP_INVALID");
  const leap = year! % 4 === 0 && (year! % 100 !== 0 || year! % 400 === 0);
  const days = [31, leap ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  if (day! < 1 || day! > days[month! - 1]!) throw new ContractError("RFC3339_TIMESTAMP_INVALID");
  if (m[8] !== "Z" && (Number(m[10]) > 23 || Number(m[11]) > 59))
    throw new ContractError("RFC3339_TIMESTAMP_INVALID");
  const parsed = Date.parse(value);
  if (Number.isNaN(parsed)) throw new ContractError("RFC3339_TIMESTAMP_INVALID");
  const offset = m[8] === "Z" ? 0 : (m[9] === "+" ? 1 : -1) * (Number(m[10]) * 60 + Number(m[11]));
  const local = new Date(parsed + offset * 60_000);
  if (!(local.getUTCFullYear() === year && local.getUTCMonth() + 1 === month &&
    local.getUTCDate() === day && local.getUTCHours() === hour &&
    local.getUTCMinutes() === minute && local.getUTCSeconds() === second))
    throw new ContractError("RFC3339_TIMESTAMP_INVALID");
  return value;
}
export function decodeCompletionTelemetry(v: unknown): Readonly<Record<string, string | null>> {
  const r = rec(v); const keys = ["schema_ref", "timestamp", "operation", "operation_outcome",
    "error_family", "correlation_id", "command_identity"];
  exact(r, keys);
  const out: Record<string, string | null> = {};
  for (const key of keys) {
    const value = r[key];
    if (value !== null && (typeof value !== "string" || value.length > 128)) throw new ContractError("TELEMETRY_SCALAR_INVALID");
    if (prohibited.test(key) || (typeof value === "string" && prohibited.test(value))) throw new ContractError("TELEMETRY_PROHIBITED_CONTENT");
    out[key] = value as string | null;
  }
  if (out.schema_ref !== "apt.operation.completed@1") throw new ContractError("TELEMETRY_SCHEMA_INVALID");
  const timestamp = out.timestamp;
  try { decodeRfc3339OffsetTimestamp(timestamp); }
  catch { throw new ContractError("TELEMETRY_TIMESTAMP_INVALID"); }
  if (!out.operation || !["EnsureSession", "StartNewSession", "LinkSessionDispatch", "AppendResearchCapture", "AppendResearchFact", "AppendReferenceProbeLineage"].includes(out.operation))
    throw new ContractError("TELEMETRY_ENUM_INVALID");
  if (!out.command_identity) throw new ContractError("TELEMETRY_COMMAND_IDENTITY_REQUIRED");
  const outcomes = ["accepted_new", "submitted_retry", "semantic_existing", "conflict", "error"];
  const errors = ["authentication", "authorization", "schema", "evidence", "artifact", "profile",
    "idempotency", "semantic_identity", "cas", "atomic_group", "replay_integrity", "not_found", "internal"];
  const outcome = out.operation_outcome;
  const errorFamily = out.error_family;
  if (!outcome || !outcomes.includes(outcome) ||
      (errorFamily !== null && (typeof errorFamily !== "string" || !errors.includes(errorFamily))))
    throw new ContractError("TELEMETRY_ENUM_INVALID");
  const needsError = outcome === "conflict" || outcome === "error";
  if (needsError !== (errorFamily !== null)) throw new ContractError("TELEMETRY_OUTCOME_ERROR_INCONSISTENT");
  return Object.freeze({ ...out });
}
