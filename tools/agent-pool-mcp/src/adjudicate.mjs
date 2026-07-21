// Boundary path: a cheap LLM (Haiku by default) judges (a) which candidates best fit
// the objective and (b) whether the objective needs a concept NOT already in the
// vocabulary. The LLM's picks are validated against the pool (trust-but-verify) and a
// proposed "new" tag that already exists is rejected deterministically — the two-layer
// guarantee the owner asked for: semantic judgment + a hard vocab guard.
import Anthropic from "@anthropic-ai/sdk";
import { loadPool } from "./pool.mjs";
import { checkVocab, prefilter } from "./select.mjs";

const MODEL = process.env.AGENT_POOL_MODEL || "claude-haiku-4-5-20251001";

export async function recommendAgents({ objective, tags = [], role = null, exclude = [], n = 5 }) {
  const { names, vocab } = loadPool();
  const vocabCheck = checkVocab(tags);
  const { candidates, neighborhood } = prefilter({ tags, role, exclude });

  // Degrade gracefully to the deterministic prefilter if there is no API key.
  if (!process.env.ANTHROPIC_API_KEY) {
    return {
      mode: "deterministic-fallback",
      reason: "ANTHROPIC_API_KEY not set — returning top deterministic candidates without LLM adjudication.",
      vocab: vocabCheck,
      names: candidates.slice(0, n).map((c) => c.name),
    };
  }

  const client = new Anthropic();
  const system = [
    "You select agent personas from a FIXED pool for a subagent dispatch.",
    "Inputs: an objective, desired topical tags, an optional role, a CANDIDATE list (name + tags + role_fit), and the vocabulary neighborhood.",
    `Return UP TO ${n} names, UNORDERED, that best fit the objective — chosen ONLY from the candidate list. Never invent a name.`,
    "Coverage judgment: decide whether the objective needs a concept NOT represented by any tag in the neighborhood. If it is genuinely new, propose ONE kebab-case tag; if an existing tag already covers it, propose none.",
    'Respond with STRICT JSON only, no prose outside it: {"names": string[], "proposed_new_tag": string|null, "rationale": string}.',
  ].join("\n");

  const user = JSON.stringify({
    objective,
    desired_tags: tags,
    role: role || "any",
    vocab_check: vocabCheck,
    vocabulary_neighborhood: neighborhood,
    candidates: candidates.map((c) => ({ name: c.name, tags: c.tags, role_fit: c.role_fit })),
    n,
  });

  const msg = await client.messages.create({
    model: MODEL,
    max_tokens: 700,
    system,
    messages: [{ role: "user", content: user }],
  });

  const text = msg.content
    .filter((b) => b.type === "text")
    .map((b) => b.text)
    .join("");

  let parsed;
  try {
    parsed = JSON.parse(extractJson(text));
  } catch {
    return {
      mode: "llm-parse-error",
      raw: text,
      names: candidates.slice(0, n).map((c) => c.name),
      vocab: vocabCheck,
    };
  }

  const requested = Array.isArray(parsed.names) ? parsed.names : [];
  const valid = requested.filter((nm) => names.has(nm)); // trust-but-verify
  const dropped_invalid = requested.filter((nm) => !names.has(nm));

  // Deterministic guard: a "new" tag that already exists is not new.
  let proposed = parsed.proposed_new_tag || null;
  const proposed_already_exists = !!(proposed && vocab.has(proposed));

  return {
    mode: "llm",
    names: valid,
    dropped_invalid,
    proposed_new_tag: proposed_already_exists ? null : proposed,
    proposed_already_exists,
    rationale: typeof parsed.rationale === "string" ? parsed.rationale : "",
    vocab: vocabCheck,
    model: MODEL,
  };
}

function extractJson(s) {
  const a = s.indexOf("{");
  const b = s.lastIndexOf("}");
  return a >= 0 && b > a ? s.slice(a, b + 1) : s;
}
