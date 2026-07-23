import type { AptCandidateState, FixtureSuppliedEvent, ResearchFact, SelectorEvidenceVerifier } from "./types.js";
import { ContractError, decodeResearchCapture, decodeResearchFact, decodeSession,
  decodeSessionDispatchLink, resolveSingleJoin, validateCapture, validateFact } from "./validation.js";

export function emptyCandidateState(): AptCandidateState {
  return { sessions: new Map(), ensureKeys: new Map(), links: new Map(), captures: new Map(),
    currentCaptureByContribution: new Map(), facts: new Map(), currentFactBySubject: new Map(),
    aggregateHeads: new Map(), throughOffset: 0 };
}
const clone = (s: AptCandidateState): AptCandidateState => ({
  sessions: new Map(s.sessions), ensureKeys: new Map(s.ensureKeys), links: new Map(s.links),
  captures: new Map(s.captures), currentCaptureByContribution: new Map(s.currentCaptureByContribution),
  facts: new Map(s.facts), currentFactBySubject: new Map(s.currentFactBySubject),
  aggregateHeads: new Map(s.aggregateHeads), throughOffset: s.throughOffset,
});
const entitySubject = (f: ResearchFact): string | null => {
  switch (f.kind) {
    case "question": return f.research_question_id; case "answer": return f.research_answer_id;
    case "reference_use": return f.reference_use_id; case "reference_claim_relation": return f.relation_id;
    case "reference_check": return f.reference_check_id; case "problem": return f.problem_id;
    case "claim": return f.research_claim_id; case "formalization": return f.formalization_id;
    default: return null;
  }
};
function decodeFixtureEventCandidate(value: unknown, s: AptCandidateState, verifier: SelectorEvidenceVerifier): FixtureSuppliedEvent {
  if (!value || typeof value !== "object" || Array.isArray(value)) throw new ContractError("FIXTURE_EVENT_OBJECT_REQUIRED");
  const r = value as Record<string, unknown>;
  const expected = ["provenance", "event_id", "offset", "type", "payload"].sort();
  const actual = Object.keys(r).sort();
  if (actual.length !== expected.length || actual.some((k, i) => k !== expected[i]))
    throw new ContractError("FIXTURE_EVENT_UNKNOWN_OR_MISSING_FIELD");
  if (r.provenance !== "fixture-supplied-unverified" || typeof r.event_id !== "string" ||
      !Number.isSafeInteger(r.offset) || (r.offset as number) < 0) throw new ContractError("FIXTURE_EVENT_INVALID");
  const base = { provenance: "fixture-supplied-unverified" as const, event_id: r.event_id, offset: r.offset as number };
  if (r.type === "session_started") return { ...base, type: r.type, payload: decodeSession(r.payload) };
  if (r.type === "session_dispatch_linked") return { ...base, type: r.type, payload: decodeSessionDispatchLink(r.payload) };
  if (r.type === "research_capture_appended") return { ...base, type: r.type, payload: decodeResearchCapture(r.payload, verifier) };
  if (r.type === "research_fact_appended") {
    const raw = r.payload as Record<string, unknown>;
    const captureId = raw && typeof raw === "object" && raw.target && typeof raw.target === "object"
      ? (raw.target as Record<string, unknown>).research_capture_id : raw?.research_capture_id;
    const c = typeof captureId === "string" ? s.captures.get(captureId) : undefined;
    if (!c) throw new ContractError("CAPTURE_NOT_FOUND");
    return { ...base, type: r.type, payload: decodeResearchFact(r.payload, c, s.facts, verifier) };
  }
  throw new ContractError("FIXTURE_EVENT_TYPE_INVALID");
}
export function reduceFixtureEventCandidate(s: AptCandidateState, supplied: unknown, verifier: SelectorEvidenceVerifier): AptCandidateState {
  const e = decodeFixtureEventCandidate(supplied, s, verifier);
  if (e.provenance !== "fixture-supplied-unverified" || e.offset <= s.throughOffset)
    throw new ContractError("FIXTURE_EVENT_INVALID");
  const n = clone(s);
  if (e.type === "session_started") {
    const existing = n.ensureKeys.get(e.payload.ensure_key);
    if (existing && existing !== e.payload.session_id) throw new ContractError("ENSURE_KEY_CONFLICT");
    n.sessions.set(e.payload.session_id, structuredClone(e.payload)); n.ensureKeys.set(e.payload.ensure_key, e.payload.session_id);
  } else if (e.type === "session_dispatch_linked") {
    if (!n.sessions.has(e.payload.session_id)) throw new ContractError("SESSION_NOT_FOUND");
    const result = resolveSingleJoin(n.links.values(), e.payload);
    if (result === "new") n.links.set(e.payload.session_dispatch_link_id, structuredClone(e.payload));
  } else if (e.type === "research_capture_appended") {
    validateCapture(e.payload);
    const key = `${e.payload.dispatch_id}\0${e.payload.expected_contribution_id}`;
    const head = n.currentCaptureByContribution.get(key) ?? null;
    if (e.payload.supersedes_capture_id !== head) throw new ContractError("CAPTURE_CAS_CONFLICT");
    for (const pin of e.payload.synthesizes) {
      const input = n.captures.get(pin.research_capture_id);
      const inputKey = input ? `${input.dispatch_id}\0${input.expected_contribution_id}` : "";
      if (!input || input.capture_status === "missing" || input.dispatch_id !== e.payload.dispatch_id ||
          n.currentCaptureByContribution.get(inputKey) !== pin.research_capture_id ||
          JSON.stringify(input.dispatch_snapshot_ref) !== JSON.stringify(e.payload.dispatch_snapshot_ref) ||
          JSON.stringify(input.capture_digest) !== JSON.stringify(pin.capture_digest))
        throw new ContractError("SYNTHESIS_PIN_INVALID");
    }
    n.captures.set(e.payload.research_capture_id, structuredClone(e.payload));
    n.currentCaptureByContribution.set(key, e.payload.research_capture_id);
  } else {
    const f = e.payload;
    const captureId = "target" in f ? f.target.research_capture_id : f.research_capture_id;
    const c = n.captures.get(captureId); if (!c) throw new ContractError("CAPTURE_NOT_FOUND");
    validateFact(f, c, n.facts, verifier);
    if ("target" in f) {
      const key = `${f.aggregate_type}:${f.aggregate_id.algorithm}:${f.aggregate_id.value}`;
      const head = n.aggregateHeads.get(key);
      if ((head?.accepted_event_id ?? null) !== f.expected_head_accepted_event_id ||
          (head?.version ?? 0) !== f.expected_aggregate_version) throw new ContractError("AGGREGATE_CAS_CONFLICT");
      n.aggregateHeads.set(key, { accepted_event_id: e.event_id, version: f.expected_aggregate_version + 1 });
    } else {
      const existing = n.facts.get(f.fact.fact_id);
      if (existing && JSON.stringify(existing) !== JSON.stringify(f)) throw new ContractError("FACT_ID_COLLISION");
      const subject = entitySubject(f)!;
      const head = n.currentFactBySubject.get(subject) ?? null;
      if (f.fact.supersedes_fact_id !== head) throw new ContractError("FACT_CAS_CONFLICT");
      n.facts.set(f.fact.fact_id, structuredClone(f)); n.currentFactBySubject.set(subject, f.fact.fact_id);
    }
  }
  n.throughOffset = e.offset; return n;
}
export function replayFixtureCandidates(events: readonly FixtureSuppliedEvent[], asOf: number, verifier: SelectorEvidenceVerifier): AptCandidateState {
  return events.filter((e) => e.offset <= asOf).reduce((s, e) => reduceFixtureEventCandidate(s, e, verifier), emptyCandidateState());
}
