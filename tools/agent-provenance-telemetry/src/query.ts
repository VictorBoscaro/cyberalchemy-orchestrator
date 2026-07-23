import type { AptCandidateState, CanonicalizerCandidate, ResearchFact } from "./types.js";
const compare = (canonicalizer: CanonicalizerCandidate) => (a: unknown, b: unknown): number => {
  const left = canonicalizer.canonicalizeCandidate(a); const right = canonicalizer.canonicalizeCandidate(b);
  const limit = Math.min(left.length, right.length);
  for (let i = 0; i < limit; i++) if (left[i] !== right[i]) return left[i]! - right[i]!;
  return left.length - right.length;
};
const facts = (s: AptCandidateState, captureId: string, canonicalizer: CanonicalizerCandidate): ResearchFact[] =>
  [...s.currentFactBySubject.values()].map((id) => s.facts.get(id)!)
    .filter((f) => "research_capture_id" in f && f.research_capture_id === captureId)
    .sort(compare(canonicalizer));
export function projectSessionRecordCandidate(s: AptCandidateState, id: string, canonicalizer: CanonicalizerCandidate) {
  const session = s.sessions.get(id); if (!session) return null;
  const dispatch_ids = [...s.links.values()].filter((l) => l.session_id === id)
    .map((l) => l.dispatch_id).sort(compare(canonicalizer));
  return { session_id: id, name: session.initial_name, dispatch_ids, as_of_fixture_offset: s.throughOffset };
}
export function projectDispatchScopeCandidate(s: AptCandidateState, dispatchId: string) {
  const captures = [...s.currentCaptureByContribution.values()].map((id) => s.captures.get(id)!)
    .filter((c) => c.dispatch_id === dispatchId);
  return { dispatch_id: dispatchId, research_expected_count: captures.length,
    research_returned_count: captures.filter((c) => c.capture_status !== "missing").length,
    research_missing_count: captures.filter((c) => c.capture_status === "missing").length,
    as_of_fixture_offset: s.throughOffset };
}
export function projectResearchRecordCandidate(s: AptCandidateState, id: string, canonicalizer: CanonicalizerCandidate) {
  const capture = s.captures.get(id); if (!capture) return null;
  return { research_capture_id: id, dispatch_id: capture.dispatch_id, capture_status: capture.capture_status,
    fact_candidates: facts(s, id, canonicalizer), as_of_fixture_offset: s.throughOffset };
}
