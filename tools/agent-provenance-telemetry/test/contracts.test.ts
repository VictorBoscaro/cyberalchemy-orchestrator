import { createHash } from "node:crypto";
import { describe, expect, it } from "vitest";
import {
  authorizeSessionRollover, candidateDigest, canonicalSet, capturePayloadCandidate, decodeArtifact,
  decodeCompletionTelemetry, decodeDigest, decodeResearchCapture, decodeResearchFact,
  decodeProbeRecommendation, decodeRfc3339OffsetTimestamp, decodeSession, decodeSessionDispatchLink,
  emptyCandidateState, projectResearchRecordCandidate, reduceFixtureEventCandidate,
  replayFixtureCandidates, resolveSingleJoin, validateFact, validateProbeRecommendation,
  type CanonicalizerCandidate, type ContentDigest, type ExtractionProvenance,
  type FixtureSuppliedEvent, type ProbeRecommendationRef, type ResearchCapture,
  type ResearchFact, type SelectorEvidenceVerifier, type Session, type SessionDispatchLink,
} from "../src/index.js";

const digest = (text: string): ContentDigest => ({
  algorithm: "sha256", value: createHash("sha256").update(text).digest("hex"),
});
const artifact = {
  artifact_id: "artifact-1", content_digest: digest("hello"), media_type: "text/plain",
  charset: "utf-8" as const, classification: "internal", redaction_policy_ref: "redact-1",
  retention_policy_ref: "retain-1", tombstone_policy_ref: "tomb-1",
  finalization_receipt_ref: "receipt-structural-ref",
};
const capture = (o: Partial<ResearchCapture> = {}): ResearchCapture => ({
  schema_ref: "apt.research-capture@1", research_capture_id: "capture-1",
  expected_contribution_id: "seat-1", capture_operation_id: "capture-op-1",
  dispatch_id: "dispatch-1", dispatch_snapshot_ref: {
    kind: "aci_managed", dispatch_id: "dispatch-1", artifact_ref: "snapshot-artifact",
    artifact_digest: digest("snapshot"), accepted_event_id: "snapshot-event", accepted_offset: 1,
  }, origin_refs: [], producer_ref: {
    kind: "seat", group_id: "group-1", seat_id: "seat-1", attempt_id: "attempt-1", activation_id: "activation-1",
  }, capture_status: "captured", raw_return: artifact, partial_reason: null, failure_reason: null,
  failure_evidence_ref: null, supersedes_capture_id: null, synthesizes: [],
  captured_at: "2026-07-23T00:00:02Z", capture_digest: digest("capture-1"), ...o,
});
const verifier: SelectorEvidenceVerifier = {
  rawBytes: (c) => c.raw_return ? new TextEncoder().encode("hello") : null,
  digest: (bytes) => digest(new TextDecoder().decode(bytes)),
  canonicalBytesCandidate: (value) => new TextEncoder().encode(JSON.stringify(value)),
  verifyDispatchScopePointer: (snapshot, field, path) =>
    snapshot.kind === "aci_managed" && snapshot.dispatch_id === "dispatch-1" &&
    field === "declared_question" && path === "/declared_question",
  isCurrentCapture: () => true,
};
const candidateCanonicalizer: CanonicalizerCandidate = {
  canonicalizeCandidate: (v) => verifier.canonicalBytesCandidate(v),
  digestCandidate: (b) => digest(String(b.byteLength)),
};
const candidateOrder = <T>(values: T[]): T[] => [...values].sort((a, b) => {
  const left = verifier.canonicalBytesCandidate(a); const right = verifier.canonicalBytesCandidate(b);
  const limit = Math.min(left.length, right.length);
  for (let i = 0; i < limit; i++) if (left[i] !== right[i]) return left[i]! - right[i]!;
  return left.length - right.length;
});
const deepFreeze = <T>(value: T): T => {
  if (value && typeof value === "object") {
    Object.freeze(value);
    for (const child of Object.values(value as Record<string, unknown>)) deepFreeze(child);
  }
  return value;
};
const extraction = (): ExtractionProvenance => ({
  mode: "verbatim", actor_ref: "actor-1", method_ref: "extractor-v1",
  extracted_at: "2026-07-23T00:00:03Z", source_capture_id: "capture-1",
  source_capture_digest: digest("capture-1"), selector: {
    schema_ref: "apt.raw-selector@1", unit: "utf8-byte", start_inclusive: 0,
    end_exclusive: 2, selected_text_digest: digest("he"),
  },
});
const envelope = (subject: string, predecessor: string | null = null) => ({
  fact_id: `fact-${subject}-${predecessor ?? "0"}`, subject_id: subject, operation_id: `op-${subject}-${predecessor ?? "0"}`,
  occurred_at: "2026-07-23T00:00:03Z", supersedes_fact_id: predecessor,
});
const question = (): ResearchFact => ({
  kind: "question", research_question_id: "q1", research_capture_id: "capture-1",
  fact: envelope("q1"), question_text: "What?", derives_from: [], extraction: extraction(),
});
const claim = (): ResearchFact => ({
  kind: "claim", research_claim_id: "c1", research_capture_id: "capture-1",
  fact: envelope("c1"), statement: "P", answer_ids: [], extraction: extraction(),
});
const use = (): ResearchFact => ({
  kind: "reference_use", reference_use_id: "u1", research_capture_id: "capture-1",
  fact: envelope("u1"), reference_id: "ref-1", reference_kind: "paper",
  locator_observed: "p.1", source_observation_id: null, probe_recommendation_ref: null,
  use_kind: "cited", anchor_quality: "locator", extraction: extraction(),
});
const session: Session = {
  session_id: "s1", ensure_key: "context-1", start_operation_id: "start-1",
  origin_kind: "workspace", origin_ref: "workspace-1", initial_name: "APT",
  started_at: "2026-07-23T00:00:00Z",
};
const link: SessionDispatchLink = {
  session_dispatch_link_id: "l1", session_id: "s1", dispatch_id: "dispatch-1",
  link_operation_id: "link-op-1", linked_at: "2026-07-23T00:00:01Z",
};
const event = <T extends FixtureSuppliedEvent["type"]>(
  offset: number, type: T, payload: Extract<FixtureSuppliedEvent, { type: T }>["payload"],
): Extract<FixtureSuppliedEvent, { type: T }> => ({
  provenance: "fixture-supplied-unverified", event_id: `event-${offset}`, offset, type, payload,
} as Extract<FixtureSuppliedEvent, { type: T }>);

describe("closed decoders and privacy smoke obligations", () => {
  it("APT-TEST-C05 smoke — Digest is exact and fresh", () => {
    const input = { ...digest("x") };
    const decoded = decodeDigest(input); input.value = digest("y").value;
    expect(decoded).toEqual(digest("x"));
    expect(() => decodeDigest({ ...digest("x"), extra: true })).toThrow(/UNKNOWN_OR_MISSING_FIELD/);
  });
  it("APT-TEST-R3 smoke — Artifact is structural, closed and contains no caller finalized flag", () => {
    expect(decodeArtifact(artifact)).not.toHaveProperty("finalized");
    expect(() => decodeArtifact({ ...artifact, finalized: true })).toThrow(/UNKNOWN_OR_MISSING_FIELD/);
  });
  it("APT-TEST-R3 smoke — Capture rejects top-level and recursively nested extras", () => {
    expect(() => decodeResearchCapture({ ...capture(), raw_body: "secret" }, verifier)).toThrow();
    expect(() => decodeResearchCapture({
      ...capture(), dispatch_snapshot_ref: { ...capture().dispatch_snapshot_ref, extra: "x" },
    }, verifier)).toThrow();
  });
  it("APT-TEST-R8 smoke — Telemetry rejects extra, nested, raw content and invalid enum", () => {
    const valid = {
      schema_ref: "apt.operation.completed@1", timestamp: "2026-07-23T00:00:00Z",
      operation: "EnsureSession", operation_outcome: "accepted_new", error_family: null,
      correlation_id: "corr-1", command_identity: "cmd-1",
    };
    expect(Object.isFrozen(decodeCompletionTelemetry(valid))).toBe(true);
    expect(() => decodeCompletionTelemetry({ ...valid, extra: "x" })).toThrow();
    expect(() => decodeCompletionTelemetry({ ...valid, correlation_id: { nested: "x" } })).toThrow();
    expect(() => decodeCompletionTelemetry({ ...valid, correlation_id: "raw body" })).toThrow();
    expect(() => decodeCompletionTelemetry({ ...valid, operation: "Unknown" })).toThrow();
  });
  it("APT-TEST-C10 smoke — Fact decoder rejects unknown variant fields and returns fresh value", () => {
    const input = question() as unknown as Record<string, unknown>;
    const decoded = decodeResearchFact(input, capture(), new Map(), verifier);
    (input.fact as Record<string, unknown>).subject_id = "mutated";
    expect("fact" in decoded && decoded.fact.subject_id).toBe("q1");
    expect(() => decodeResearchFact({ ...question(), extra: true }, capture(), new Map(), verifier)).toThrow();
  });
  it("APT-TEST-C09 smoke — QuestionDerivationRef is an exact local union pinned to snapshot/capture", () => {
    const dispatchDerived = { ...question(), derives_from: [{
      kind: "dispatch_scope", dispatch_snapshot_ref: capture().dispatch_snapshot_ref,
      field_name: "declared_question", field_path: "/declared_question",
    }] };
    expect(() => decodeResearchFact(dispatchDerived, capture(), new Map(), verifier)).not.toThrow();
    expect(() => decodeResearchFact({ ...dispatchDerived, derives_from: [{
      ...dispatchDerived.derives_from[0], raw_body: "secret",
    }] }, capture(), new Map(), verifier)).toThrow(/UNKNOWN_OR_MISSING_FIELD/);
    const q1 = question();
    const q1Revision = question();
    if (!("fact" in q1Revision)) throw new Error("fixture");
    q1Revision.fact = envelope("q1", "fact-q1-0");
    const known = new Map([["fact-q1-0", q1], [q1Revision.fact.fact_id, q1Revision]]);
    const localDerived = { ...question(), research_question_id: "q2", fact: envelope("q2"),
      derives_from: [{ kind: "research_question", research_question_id: "q1",
        question_fact_id: "fact-q1-0", research_capture_id: "capture-1",
        research_capture_digest: digest("capture-1") }] };
    expect(() => decodeResearchFact(localDerived, capture(), known, verifier)).not.toThrow();
    expect(() => decodeResearchFact({ ...localDerived, derives_from: [{
      ...localDerived.derives_from[0], research_capture_id: "other",
    }] }, capture(), known, verifier)).toThrow(/DERIVATION_QUESTION_INVALID/);
    const noPointerVerifier = { ...verifier, verifyDispatchScopePointer: () => false };
    expect(() => decodeResearchFact(dispatchDerived, capture(), new Map(), noPointerVerifier))
      .toThrow(/DERIVATION_POINTER_UNVERIFIED/);
  });
  it("APT-TEST-C12 smoke — Per-variant nested values are typed, canonical and raw-object rejecting", () => {
    const formal = { kind: "formalization", formalization_id: "f1", research_capture_id: "capture-1",
      fact: envelope("f1"), research_claim_id: "c1", notation: "P", latex: null,
      legend: { P: "proposition" }, reading: "P", logic_family: "propositional",
      assumptions: ["a"], scope: "local", extraction: extraction(), syntax_checker_ref: null,
      proof_check_ref: null, governance_ref: null };
    const known = new Map([["fc", claim()]]);
    expect(() => decodeResearchFact(formal, capture(), known, verifier)).not.toThrow();
    expect(() => decodeResearchFact({ ...formal, legend: { P: { raw: "x" } } }, capture(), known, verifier)).toThrow();
    expect(() => decodeResearchFact({ ...formal, assumptions: [{ raw: "x" }] }, capture(), known, verifier)).toThrow();
    const problem = { kind: "problem", problem_id: "p1", research_capture_id: "capture-1",
      fact: envelope("p1"), problem_kind: "gap", statement: "gap", blocks: [],
      evidence_refs: [{ kind: "fact", fact_id: "fact-q1-0", research_capture_id: "capture-1" }],
      extraction: extraction() };
    const evidenceKnown = new Map([["fact-q1-0", question()]]);
    expect(() => decodeResearchFact(problem, capture(), evidenceKnown, verifier)).not.toThrow();
    expect(() => decodeResearchFact({ ...problem, evidence_refs: [{ raw_body: "x" }] }, capture(), evidenceKnown, verifier)).toThrow();
    expect(() => decodeResearchFact({ ...problem, blocks: ["q1", "q1"] }, capture(), evidenceKnown, verifier)).toThrow(/DUPLICATE/);
    expect(() => decodeResearchFact({ ...problem, evidence_refs: [{
      kind: "fact", fact_id: "missing", research_capture_id: "capture-1",
    }] }, capture(), evidenceKnown, verifier)).toThrow(/FACT_EVIDENCE/);
    const revisedQuestion = question();
    if (!("fact" in revisedQuestion)) throw new Error("fixture");
    revisedQuestion.fact = envelope("q1", "fact-q1-0");
    const history = new Map([...evidenceKnown, [revisedQuestion.fact.fact_id, revisedQuestion]]);
    expect(() => decodeResearchFact(problem, capture(), history, verifier)).toThrow(/FACT_EVIDENCE/);
    const currentProblem = { ...problem, evidence_refs: [{
      kind: "fact", fact_id: revisedQuestion.fact.fact_id, research_capture_id: "capture-1",
    }] };
    expect(() => decodeResearchFact(currentProblem, capture(), history, verifier)).not.toThrow();
    expect(() => decodeResearchFact({ ...currentProblem, evidence_refs: [{
      kind: "fact", fact_id: revisedQuestion.fact.fact_id, research_capture_id: "other",
    }] }, capture(), history, verifier)).toThrow(/FACT_EVIDENCE/);
  });
  it("APT-TEST-C12 smoke — ResearchProblem blocks resolve one current local entity subject", () => {
    const q = question();
    const validProblem = { kind: "problem", problem_id: "p-block", research_capture_id: "capture-1",
      fact: envelope("p-block"), problem_kind: "blocker", statement: "blocked", blocks: ["q1"],
      evidence_refs: [], extraction: extraction() };
    expect(() => decodeResearchFact(validProblem, capture(), new Map([["fact-q1-0", q]]), verifier)).not.toThrow();
    expect(() => decodeResearchFact({ ...validProblem, blocks: ["missing"] }, capture(), new Map(), verifier))
      .toThrow(/PROBLEM_BLOCK_TARGET/);
    const cross = { ...q, research_capture_id: "capture-other" } as ResearchFact;
    expect(() => decodeResearchFact(validProblem, capture(), new Map([["fact-q1-0", cross]]), verifier))
      .toThrow(/PROBLEM_BLOCK_TARGET/);
    const fork = question();
    if (!("fact" in fork)) throw new Error("fixture");
    fork.fact = { ...envelope("q1"), fact_id: "fact-q1-fork" };
    expect(() => decodeResearchFact(validProblem, capture(),
      new Map([["fact-q1-0", q], ["fact-q1-fork", fork]]), verifier)).toThrow(/PROBLEM_BLOCK_TARGET/);
  });
  it("APT-TEST-C10 smoke — Fact decode is pure for deeply frozen success and rejected input", () => {
    const frozen = deepFreeze(question());
    const before = JSON.stringify(frozen);
    expect(() => decodeResearchFact(frozen, capture(), new Map(), verifier)).not.toThrow();
    expect(JSON.stringify(frozen)).toBe(before);
    const invalid = deepFreeze({ ...question(), extra: { raw_body: "secret" } });
    const invalidBefore = JSON.stringify(invalid);
    expect(() => decodeResearchFact(invalid, capture(), new Map(), verifier)).toThrow();
    expect(JSON.stringify(invalid)).toBe(invalidBefore);
  });
});

describe("authority-boundary and structural evidence smoke obligations", () => {
  it("APT-TEST-R7 smoke — Profile matching is structural and carries registry/acceptance refs", () => {
    const binding = { protocol_profile_id: "probe-profile", protocol_profile_version: "1",
      protocol_profile_digest: digest("profile") };
    const ref: ProbeRecommendationRef = {
      probe_id: "p1", recommendation_id: "r1", bundle_digest: digest("bundle"),
      profile_binding: binding,
      bundle_acceptance_ref: { kind: "accepted_event", accepted_event_id: "e1", contract_version: "1", evidence_digest: digest("accept") },
      profile_registration_ref: { kind: "registry_event", accepted_event_id: "e2",
        ...binding, contract_version: "1", evidence_digest: digest("register") },
      source_observation_ids: ["o1"],
    };
    expect(() => validateProbeRecommendation(ref, verifier)).not.toThrow();
    expect(() => validateProbeRecommendation({ ...ref, profile_binding: { ...binding, protocol_profile_version: "2" } }, verifier)).toThrow();
    expect(() => decodeProbeRecommendation({
      ...ref, profile_registration_ref: { ...ref.profile_registration_ref, extra: "x" },
    }, verifier)).toThrow(/UNKNOWN_OR_MISSING_FIELD/);
  });
  it("APT-TEST-C17 smoke — Probe observation references reject duplicates", () => {
    const binding = { protocol_profile_id: "p", protocol_profile_version: "1", protocol_profile_digest: digest("p") };
    expect(() => validateProbeRecommendation({
      probe_id: "p", recommendation_id: "r", bundle_digest: digest("b"), profile_binding: binding,
      bundle_acceptance_ref: { kind: "publication_receipt", receipt_id: "a", contract_version: "1", evidence_digest: digest("a") },
      profile_registration_ref: { kind: "registry_receipt", receipt_id: "r", ...binding, contract_version: "1", evidence_digest: digest("r") },
      source_observation_ids: ["o", "o"],
    }, verifier)).toThrow(/DUPLICATE/);
  });
  it("APT-TEST-C08/R7 smoke — OriginRef probe and probe_bundle are exact evidence-bearing unions", () => {
    const profile = { profile_id: "profile-1", profile_version: "1", profile_digest: digest("profile") };
    const probe = { kind: "probe", owner_namespace: "agent-provenance-telemetry",
      probe_schema_ref: "apt.reference-probe@1", probe_profile_ref: profile, probe_id: "probe-1",
      aci_acceptance_ref: { kind: "accepted_event", accepted_event_id: "accepted-1",
        owner_namespace: "agents-communication-infra", contract_version: "1", evidence_digest: digest("accepted") } };
    const bundle = { kind: "probe_bundle", owner_namespace: "agent-provenance-telemetry",
      bundle_schema_ref: "apt.reference-probe-bundle@1", probe_profile_ref: profile,
      probe_id: "probe-1", bundle_digest: digest("bundle"), committed_event_id: "event-bundle",
      committed_event_digest: digest("event-bundle") };
    const origins = candidateOrder([probe, bundle]);
    expect(() => decodeResearchCapture({ ...capture(), origin_refs: origins }, verifier)).not.toThrow();
    const { aci_acceptance_ref: _missing, ...missing } = probe;
    expect(() => decodeResearchCapture({ ...capture(), origin_refs: [missing] }, verifier)).toThrow();
    expect(() => decodeResearchCapture({ ...capture(), origin_refs: [{
      ...probe, receipt_id: "opposite-variant",
    }] }, verifier)).toThrow(/UNKNOWN_OR_MISSING_FIELD/);
    expect(() => decodeResearchCapture({ ...capture(), origin_refs: [{
      ...probe, aci_acceptance_ref: { ...probe.aci_acceptance_ref, owner_namespace: "host" },
    }] }, verifier)).toThrow(/OWNER_NAMESPACE_INVALID/);
    expect(() => decodeResearchCapture({ ...capture(), origin_refs: [{
      ...probe, probe_profile_ref: { ...profile, profile_digest: { ...profile.profile_digest, extra: true } },
    }] }, verifier)).toThrow(/UNKNOWN_OR_MISSING_FIELD/);
    expect(() => decodeResearchCapture({ ...capture(), origin_refs: [{
      ...bundle, committed_event_digest: { algorithm: "sha256", value: "BAD" },
    }] }, verifier)).toThrow(/DIGEST_INVALID/);
  });
  it("APT-TEST-R6 smoke — Events explicitly say fixture-supplied-unverified", () => {
    expect(event(1, "session_started", session).provenance).toBe("fixture-supplied-unverified");
  });
});

describe("locality, selector and CAS smoke obligations", () => {
  it("APT-TEST-C07 smoke — Selector checks byte bounds and selected slice digest", () => {
    expect(() => validateFact(question(), capture(), new Map(), verifier)).not.toThrow();
    const bad = question(); if ("extraction" in bad) bad.extraction.selector.end_exclusive = 99;
    expect(() => validateFact(bad, capture(), new Map(), verifier)).toThrow(/SELECTOR_RANGE/);
    const wrong = question(); if ("extraction" in wrong) wrong.extraction.selector.selected_text_digest = digest("wrong");
    expect(() => validateFact(wrong, capture(), new Map(), verifier)).toThrow(/SELECTOR_DIGEST/);
  });
  it("APT-TEST-C11/C12 smoke — Relation targets must exist in the same capture", () => {
    const known = new Map([["fq", question()], ["fc", claim()], ["fu", use()]]);
    const relation: ResearchFact = {
      kind: "reference_claim_relation", relation_id: "rel1", research_capture_id: "capture-1",
      fact: envelope("rel1"), reference_use_id: "u1", research_claim_id: "c1",
      relation: "supports", extraction: extraction(),
    };
    expect(() => validateFact(relation, capture(), known, verifier)).not.toThrow();
    expect(() => validateFact({ ...relation, research_claim_id: "missing" }, capture(), known, verifier)).toThrow();
  });
  it("APT-TEST-C13/C14 smoke — Check and formalization targets must exist and be local", () => {
    const relation: ResearchFact = {
      kind: "reference_claim_relation", relation_id: "rel1", research_capture_id: "capture-1",
      fact: envelope("rel1"), reference_use_id: "u1", research_claim_id: "c1",
      relation: "supports", extraction: extraction(),
    };
    const known = new Map([["fc", claim()], ["fu", use()], ["fr", relation]]);
    const check: ResearchFact = { kind: "reference_check", reference_check_id: "check1",
      research_capture_id: "capture-1", fact: envelope("check1"), check_kind: "claim_support",
      reference_use_id: "u1", relation_id: "rel1", checked_by: "actor", method_ref: "m1",
      result: "pass", evidence_ref: null };
    const formal: ResearchFact = { kind: "formalization", formalization_id: "form1",
      research_capture_id: "capture-1", fact: envelope("form1"), research_claim_id: "c1",
      notation: "P", latex: null, legend: { P: "claim" }, reading: "P", logic_family: "propositional",
      assumptions: [], scope: "local", extraction: extraction(), syntax_checker_ref: null,
      proof_check_ref: null, governance_ref: null };
    expect(() => validateFact(check, capture(), known, verifier)).not.toThrow();
    expect(() => validateFact(formal, capture(), known, verifier)).not.toThrow();
    expect(() => decodeResearchFact({ ...check, check_kind: "source_identity", relation_id: null,
      result: "indeterminate" }, capture(), known, verifier)).not.toThrow();
    expect(() => decodeResearchFact({ ...check, check_kind: "identity", relation_id: null },
      capture(), known, verifier)).toThrow(/REFERENCE_CHECK_ENUM_INVALID/);
    const otherUse = { ...use(), reference_use_id: "u2", fact: envelope("u2") } as ResearchFact;
    const mismatched = new Map([...known, ["fu2", otherUse]]);
    expect(() => validateFact({ ...check, reference_use_id: "u2" }, capture(), mismatched, verifier))
      .toThrow(/CHECK_RELATION_USE_MISMATCH/);
  });
  it("APT-TEST-R1 smoke — Join returns exact duplicate and rejects same-session or same-dispatch conflict", () => {
    expect(resolveSingleJoin([link], link)).toBe("existing_exact");
    expect(() => resolveSingleJoin([link], { ...link, session_dispatch_link_id: "l2" })).toThrow(/JOIN_CONFLICT/);
    expect(resolveSingleJoin([link], { ...link, dispatch_id: "dispatch-2", session_dispatch_link_id: "l2" })).toBe("new");
  });
  it("APT-TEST-C02 smoke — Rollover needs explicit host/human authorization", () => {
    expect(() => authorizeSessionRollover("host", true)).not.toThrow();
    expect(() => authorizeSessionRollover("worker", true)).toThrow();
  });
  it("APT-TEST-R5/C06 smoke — Capture correction and synthesis enforce current/snapshot/non-missing CAS", () => {
    let s = reduceFixtureEventCandidate(emptyCandidateState(), event(1, "research_capture_appended", capture()), verifier);
    const correction = capture({ research_capture_id: "capture-2", capture_operation_id: "op2",
      capture_digest: digest("capture-2"), supersedes_capture_id: "capture-1" });
    expect(() => reduceFixtureEventCandidate(s, event(2, "research_capture_appended", correction), verifier)).not.toThrow();
    const synth = capture({ research_capture_id: "capture-s", expected_contribution_id: "synth",
      capture_operation_id: "ops", capture_digest: digest("s"), synthesizes: [{
        research_capture_id: "capture-1", capture_digest: digest("capture-1"),
      }] });
    expect(() => reduceFixtureEventCandidate(s, event(2, "research_capture_appended", synth), verifier)).not.toThrow();
  });
  it("APT-TEST-C15 smoke — Entity fact CAS rejects stale predecessor", () => {
    let s = reduceFixtureEventCandidate(emptyCandidateState(), event(1, "research_capture_appended", capture()), verifier);
    s = reduceFixtureEventCandidate(s, event(2, "research_fact_appended", question()), verifier);
    const revision = question();
    if (!("fact" in revision)) throw new Error("fixture");
    revision.fact = envelope("q1", "wrong");
    expect(() => reduceFixtureEventCandidate(s, event(3, "research_fact_appended", revision), verifier)).toThrow(/FACT_CAS/);
  });
  it("APT-TEST-C16 smoke — Aggregate CAS is independent from entity fact heads", () => {
    let s = reduceFixtureEventCandidate(emptyCandidateState(), event(1, "research_capture_appended", capture()), verifier);
    s = reduceFixtureEventCandidate(s, event(2, "research_fact_appended", claim()), verifier);
    const disposition: ResearchFact = { kind: "disposition_recorded",
      target: { target_kind: "claim", target_id: "c1", research_capture_id: "capture-1" },
      disposition: "proposed", actor_ref: "actor", policy_ref: "policy",
      aggregate_type: "apt.disposition-chain", aggregate_id: digest("chain"),
      expected_head_accepted_event_id: null, expected_aggregate_version: 0 };
    s = reduceFixtureEventCandidate(s, event(3, "research_fact_appended", disposition), verifier);
    expect(() => reduceFixtureEventCandidate(s, event(4, "research_fact_appended", disposition), verifier)).toThrow(/AGGREGATE_CAS/);
  });
  it("APT-TEST-C16 smoke — Disposition/assessment enums are discriminated by target kind", () => {
    const known = new Map([["fc", claim()], ["fp", {
      kind: "problem", problem_id: "p1", research_capture_id: "capture-1", fact: envelope("p1"),
      problem_kind: "gap", statement: "gap", blocks: [], evidence_refs: [], extraction: extraction(),
    } as ResearchFact]]);
    const base = { kind: "disposition_recorded", actor_ref: "a", policy_ref: "p",
      aggregate_type: "apt.disposition-chain", aggregate_id: digest("agg"),
      expected_head_accepted_event_id: null, expected_aggregate_version: 0 };
    expect(() => decodeResearchFact({ ...base,
      target: { target_kind: "claim", target_id: "c1", research_capture_id: "capture-1" },
      disposition: "supported" }, capture(), known, verifier)).not.toThrow();
    expect(() => decodeResearchFact({ ...base,
      target: { target_kind: "claim", target_id: "c1", research_capture_id: "capture-1" },
      disposition: "observed" }, capture(), known, verifier)).toThrow(/TARGET_KIND_MISMATCH/);
    expect(() => decodeResearchFact({ ...base,
      target: { target_kind: "problem", target_id: "p1", research_capture_id: "capture-1" },
      disposition: "supported" }, capture(), known, verifier)).toThrow(/TARGET_KIND_MISMATCH/);
    const assessment = { kind: "assessment_recorded", actor_ref: "a", method_ref: "m",
      policy_ref: "p", aggregate_type: "apt.assessment-chain", aggregate_id: digest("assess"),
      expected_head_accepted_event_id: null, expected_aggregate_version: 0 };
    expect(() => decodeResearchFact({ ...assessment,
      target: { target_kind: "claim", target_id: "c1", research_capture_id: "capture-1" },
      assessment: "contested" }, capture(), known, verifier)).not.toThrow();
    expect(() => decodeResearchFact({ ...assessment,
      target: { target_kind: "problem", target_id: "p1", research_capture_id: "capture-1" },
      assessment: "validated" }, capture(), known, verifier)).not.toThrow();
    expect(() => decodeResearchFact({ ...assessment,
      target: { target_kind: "claim", target_id: "c1", research_capture_id: "capture-1" },
      assessment: "validated" }, capture(), known, verifier)).toThrow(/TARGET_KIND_MISMATCH/);
  });
  it("APT-TEST-C16 smoke — Aggregate target is exact current/local and capture must be current non-missing", () => {
    const base = { kind: "disposition_recorded",
      target: { target_kind: "claim", target_id: "c1", research_capture_id: "capture-1" },
      disposition: "supported", actor_ref: "a", policy_ref: "p",
      aggregate_type: "apt.disposition-chain", aggregate_id: digest("agg-target"),
      expected_head_accepted_event_id: null, expected_aggregate_version: 0 };
    expect(() => decodeResearchFact({ ...base, target: { ...base.target, target_id: "dangling" } },
      capture(), new Map([["fc", claim()]]), verifier)).toThrow(/TARGET_NOT_FOUND/);
    const cross = { ...claim(), research_capture_id: "other" } as ResearchFact;
    expect(() => decodeResearchFact(base, capture(), new Map([["fc", cross]]), verifier))
      .toThrow(/TARGET_NOT_FOUND/);
    const fork = claim();
    if (!("fact" in fork)) throw new Error("fixture");
    fork.fact = { ...envelope("c1"), fact_id: "fact-c1-fork" };
    expect(() => decodeResearchFact(base, capture(),
      new Map([["fact-c1-0", claim()], ["fact-c1-fork", fork]]), verifier)).toThrow(/TARGET_NOT_FOUND/);
    const staleCaptureVerifier = { ...verifier, isCurrentCapture: () => false };
    expect(() => decodeResearchFact(base, capture(), new Map([["fc", claim()]]), staleCaptureVerifier))
      .toThrow(/FACT_CAPTURE_NOT_CURRENT/);
    expect(() => decodeResearchFact(base, capture({
      capture_status: "missing", raw_return: null, failure_reason: "timeout",
      failure_evidence_ref: { kind: "host_observation", owner_namespace: "host",
        contract_version: "1", source_observation_id: "o", evidence_digest: digest("o") },
    }), new Map([["fc", claim()]]), verifier)).toThrow(/FACT_CAPTURE_NOT_CURRENT/);
  });
});

describe("candidate-only normalization and projection smoke obligations", () => {
  it("APT-TEST-C05 smoke — Candidate canonicalizer is injected and explicitly candidate-only", () => {
    expect(capturePayloadCandidate(capture())).not.toHaveProperty("capture_digest");
    expect(candidateDigest({ b: 1 }, candidateCanonicalizer).algorithm).toBe("sha256");
    expect(canonicalSet(["Á", "a", "A"], candidateCanonicalizer)).toEqual(["A", "a", "Á"]);
    const problem = { kind: "problem", problem_id: "p-byte", research_capture_id: "capture-1",
      fact: envelope("p-byte"), problem_kind: "gap", statement: "gap", blocks: ["a", "A"],
      evidence_refs: [], extraction: extraction() };
    expect(() => decodeResearchFact(problem, capture(), new Map(), verifier))
      .toThrow(/STRING_SET_NONCANONICAL_ORDER/);
  });
  it("APT-TEST-R6 smoke — Candidate replay is deterministic at explicit fixture offset", () => {
    const events = [event(1, "research_capture_appended", capture())];
    const a = projectResearchRecordCandidate(replayFixtureCandidates(events, 1, verifier), "capture-1", candidateCanonicalizer);
    const b = projectResearchRecordCandidate(replayFixtureCandidates(events, 1, verifier), "capture-1", candidateCanonicalizer);
    expect(a).toEqual(b);
    expect(a?.as_of_fixture_offset).toBe(1);
  });
  it("APT-TEST-R8 smoke — Completion telemetry enforces timestamp/outcome/error-family matrix", () => {
    const valid = { schema_ref: "apt.operation.completed@1", timestamp: "2026-07-23T00:00:00Z",
      operation: "AppendResearchFact", operation_outcome: "conflict", error_family: "cas",
      correlation_id: "corr", command_identity: "cmd" };
    expect(() => decodeCompletionTelemetry(valid)).not.toThrow();
    expect(() => decodeCompletionTelemetry({ ...valid, timestamp: "yesterday" })).toThrow(/TIMESTAMP/);
    expect(() => decodeCompletionTelemetry({ ...valid, operation_outcome: "maybe" })).toThrow(/ENUM/);
    expect(() => decodeCompletionTelemetry({ ...valid, error_family: null })).toThrow(/INCONSISTENT/);
    expect(() => decodeCompletionTelemetry({ ...valid, operation_outcome: "accepted_new", error_family: "cas" })).toThrow(/INCONSISTENT/);
    expect(() => decodeCompletionTelemetry({ ...valid, timestamp: "2024-02-29T23:59:59+14:00" })).not.toThrow();
    expect(() => decodeCompletionTelemetry({ ...valid, timestamp: "2023-02-29T00:00:00Z" })).toThrow(/TIMESTAMP/);
    expect(() => decodeCompletionTelemetry({ ...valid, timestamp: "2026-04-31T00:00:00Z" })).toThrow(/TIMESTAMP/);
    expect(() => decodeCompletionTelemetry({ ...valid, timestamp: "2026-01-01T00:00:60Z" })).toThrow(/TIMESTAMP/);
    expect(() => decodeCompletionTelemetry({ ...valid, timestamp: "2026-01-01T00:00:00+24:00" })).toThrow(/TIMESTAMP/);
  });
  it("APT-TEST-C01/C04/C07 smoke — One strict RFC3339 decoder governs all domain timestamps", () => {
    expect(decodeRfc3339OffsetTimestamp("2024-02-29T12:00:00-03:00")).toBe("2024-02-29T12:00:00-03:00");
    expect(() => decodeResearchCapture({ ...capture(), captured_at: "2023-02-29T00:00:00Z" }, verifier)).toThrow(/RFC3339/);
    expect(() => decodeSession({ ...session, started_at: "2026-04-31T00:00:00Z" })).toThrow(/RFC3339/);
    expect(() => decodeSessionDispatchLink({ ...link, linked_at: "2026-01-01T00:00:00+24:00" })).toThrow(/RFC3339/);
    const badOccurred = question();
    if (!("fact" in badOccurred)) throw new Error("fixture");
    badOccurred.fact.occurred_at = "2026-13-01T00:00:00Z";
    expect(() => decodeResearchFact(badOccurred, capture(), new Map(), verifier)).toThrow(/RFC3339/);
    const badExtracted = question();
    if (!("extraction" in badExtracted)) throw new Error("fixture");
    badExtracted.extraction.extracted_at = "2026-01-01T00:00:60Z";
    expect(() => decodeResearchFact(badExtracted, capture(), new Map(), verifier)).toThrow(/RFC3339/);
  });
});
