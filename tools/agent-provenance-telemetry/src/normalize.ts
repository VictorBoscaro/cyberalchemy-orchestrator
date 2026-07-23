import type { CanonicalizerCandidate, ContentDigest, ResearchCapture, ResearchFact } from "./types.js";

export function canonicalSet(values: readonly string[], canonicalizer: CanonicalizerCandidate): string[] {
  if (new Set(values).size !== values.length) throw new Error("DUPLICATE_RELATIONAL_MEMBER");
  const compare = (a: string, b: string): number => {
    const left = canonicalizer.canonicalizeCandidate(a);
    const right = canonicalizer.canonicalizeCandidate(b);
    const limit = Math.min(left.length, right.length);
    for (let i = 0; i < limit; i++) if (left[i] !== right[i]) return left[i]! - right[i]!;
    return left.length - right.length;
  };
  return [...values].sort(compare);
}
export function capturePayloadCandidate(c: ResearchCapture): Omit<ResearchCapture, "capture_digest"> {
  const { capture_digest: _, ...candidate } = structuredClone(c);
  return candidate;
}
export function factPayloadCandidate(f: ResearchFact): ResearchFact {
  return structuredClone(f);
}
export function candidateDigest(value: unknown, c: CanonicalizerCandidate): ContentDigest {
  return c.digestCandidate(c.canonicalizeCandidate(structuredClone(value)));
}
