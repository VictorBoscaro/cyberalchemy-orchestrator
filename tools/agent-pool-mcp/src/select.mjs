// Deterministic core. No LLM, no network. Pure functions over the loaded pool.
import { loadPool } from "./pool.mjs";

// Vocabulary membership + cheap "did you mean" (substring/token overlap, NOT semantic).
// This is the deterministic half of the "does what I want already exist?" guarantee;
// the semantic half lives in the LLM adjudicator (adjudicate.mjs).
export function checkVocab(tags) {
  const { vocab } = loadPool();
  const known = [];
  const unknown = [];
  for (const t of tags) (vocab.has(t) ? known : unknown).push(t);

  const suggestions = {};
  if (unknown.length) {
    const all = [...vocab];
    for (const u of unknown) {
      const ul = String(u).toLowerCase();
      const toks = ul.split(/[-\s]+/).filter(Boolean);
      suggestions[u] = all
        .map((v) => {
          const vl = v.toLowerCase();
          let score = 0;
          if (vl.includes(ul) || ul.includes(vl)) score += 3;
          for (const tk of toks) if (vl.includes(tk)) score += 1;
          return { v, score };
        })
        .filter((x) => x.score > 0)
        .sort((a, b) => b.score - a.score || a.v.localeCompare(b.v))
        .slice(0, 5)
        .map((x) => x.v);
    }
  }
  return { known, unknown, suggestions };
}

// Fast path: rank pool entries by |entry.tags ∩ query.tags| ∩ role_fit. Fully
// deterministic ordering (no random tie-break) so the same query always yields the
// same list — testable and diffable in dispatch logs.
export function searchPool({ tags = [], role = null, exclude = [], k = 10 }) {
  const { tagged } = loadPool();
  const q = new Set(tags);
  const ex = new Set(exclude);
  return tagged
    .filter((e) => (!role || (e.role_fit || []).includes(role)) && !ex.has(e.name))
    .map((e) => ({
      name: e.name,
      overlap: e.tags.filter((t) => q.has(t)).length,
      tags: e.tags,
      role_fit: e.role_fit || [],
      cited: !!e.cited,
      role_rank: role ? (e.role_fit || []).indexOf(role) : 0,
    }))
    .filter((c) => c.overlap > 0)
    .sort(
      (a, b) =>
        b.overlap - a.overlap || // more shared tags
        a.role_rank - b.role_rank || // role as a primary fit wins
        (b.cited === a.cited ? 0 : b.cited ? 1 : -1) || // cited before proposed
        a.name.localeCompare(b.name), // stable final tiebreak
    )
    .slice(0, k);
}

// Broad recall for the LLM adjudicator: every entry sharing >=1 query tag, plus the
// neighborhood of tags that co-occur with the query (so the LLM can judge whether a
// wanted concept is already represented under a different-but-related tag).
export function prefilter({ tags = [], role = null, exclude = [], cap = 40 }) {
  const { tagged } = loadPool();
  const q = new Set(tags);
  const ex = new Set(exclude);

  const candidates = tagged
    .filter((e) => !ex.has(e.name) && e.tags.some((t) => q.has(t)))
    .map((e) => ({
      name: e.name,
      overlap: e.tags.filter((t) => q.has(t)).length,
      tags: e.tags,
      role_fit: e.role_fit || [],
      cited: !!e.cited,
      role_hint: role ? (e.role_fit || []).includes(role) : true,
    }))
    .sort(
      (a, b) =>
        Number(b.role_hint) - Number(a.role_hint) ||
        b.overlap - a.overlap ||
        a.name.localeCompare(b.name),
    )
    .slice(0, cap);

  const neighborhood = new Set();
  for (const e of tagged) {
    if (e.tags.some((t) => q.has(t))) {
      for (const t of e.tags) if (!q.has(t)) neighborhood.add(t);
    }
  }
  return { candidates, neighborhood: [...neighborhood].sort() };
}
