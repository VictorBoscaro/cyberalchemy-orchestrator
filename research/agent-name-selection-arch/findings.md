# agent_name selection — architecture decision

**Dispatch:** `2026-07-20-agent-name-selection-arch` (meta, research, 2 tensioned agents)
**Axis:** methodology — minimalist-deterministic (Torvalds) vs systems-retrieval (Yu, Zoe)
**Claim ≤ proof:** both poles verified the actual artifacts before opining; both flagged their central risk as *unmeasured*.

## Baseline (corrected by the explorer)

Today's bar is **not** "no selection." `check-tension/SKILL.md` already instructs an LLM to
draw `agent_name` from the pool by prose — but never tells it to read `tags`, and
`append-dispatch.cjs:201` validates `agent_name` only as string-or-null (no pool cross-ref).
So the bar to beat is: *an LLM eyeballs 419 names, tag-blind, unverified.*

## Where both poles agree

- **(a) RAG — reject.** Embeddings are for fuzzy/unstructured text; the pool is hand-curated,
  closed-vocabulary, discrete tags. Embedding a controlled vocabulary to recover what set
  intersection gives exactly is lossier + adds a vector index + re-embed on every pool churn
  (already v0.5.0 in one day).
- **(b) MCP cheap-agent — reject.** Spends a stochastic LLM call per dispatch to do a
  set-intersection a for-loop does in microseconds; no more auditable than a script.
- **(d) functor / learned-opposition — defer, right shape.** Matches the repo's CT ethos, but
  the label it would learn from **does not exist yet**: `check-tension`'s pass/fail/disagreement
  outcomes are explicitly *not registered* ("no row") — no machine-readable training data.
- **(c) deterministic tag-overlap ∩ role_fit script — rank #1**, both. ~60–80 lines, zero deps,
  first thing that actually reads `tags`, deterministic/testable. Surface top-K with tags as a
  **non-binding suggestion**; final pick stays with the LLM/human (that's where angle-fit judgment
  belongs, not where compute belongs).

## Where they diverge (the crux)

**Does the selection step need to encode opposition (agent-to-agent distance), or is that
`check-tension`'s separate job?**

- **Torvalds (minimalist):** No. Pure overlap is enough; opposition is check-tension's concern,
  not retrieval's. Build nothing beyond the script. Falsifier: if dispatch logs show top-5 is
  consistently *not* where the picked agent came from, richer matching earns its cost.
- **Yu, Zoe (skeptic):** Two structural failures of pure overlap: (1) **hierarchy/synonym
  near-misses** — a ∩-scorer scores `category-theory` vs `monoidal-categories` as zero unless
  the exact token repeats, ranking a conceptual match below a coincidental one; (2) **opposition** —
  a similarity scorer only knows agent↔query distance, never agent↔agent, so running top-5 twice
  for a tensioned pair can return two near-clones (max relevant, min opposed). Her adds: a small
  static tag-cluster table + instrument check-tension close-rows with structured agree/disagree
  (the prerequisite for (d)).

## Adjudication

- The user **already deferred** name-level opposition (idea 2) to backlog. That resolves the crux
  for the near term: retrieval only needs to surface *relevant* candidates — opposition stays where
  it is today (LLM/human final pick + check-tension on the angles).
- Yu's opposition kill-shot is real but argues for the deferred item; her synonym/cluster point is
  **unmeasured** (she said so) → don't build the distance table speculatively.
- Cheap concession that costs nothing and blunts the clone risk: **return top-8–10 with full tags
  visible**, not top-5, so a tensioned pair has room to pick opposed names.

## Decision

- **Now:** build **(c)** — deterministic `tag-overlap ∩ role_fit` selector, returns top-K (≈8–10)
  with each candidate's tags, as a **non-binding suggestion** surfaced at dispatch time. No RAG,
  no MCP, no learned metric, no CT wrapper.
- **Backlog (with already-deferred idea 2):** name-level pairwise opposition + its prerequisite —
  persist `check-tension` pair outcomes as structured rows (Yu's #2). The tag-cluster table is a
  *conditional* backlog item, gated on first **measuring** the false-negative rate of naive overlap
  against real past angles (both poles named this exact falsification test).
- **Not building:** (a) RAG, (b) MCP-agent, (d) learned-opposition (until the label accrues).

## Revision (2026-07-20, same day) — MCP reinstated for a different job

The owner surfaced a use the two poles' rejection did **not** cover. They rejected
**MCP-for-retrieval** ("spend an LLM call to do a set-intersection"). The owner instead wants
**MCP-for-boundary-adjudication**: *"the agent may register a new tag, but only after we
guarantee it doesn't already exist."* A pure set-intersection **cannot** answer "is the wanted
concept already in the vocabulary under a different name?" — that is semantic, not lexical. This
was demonstrated live: `check_vocab("sheaf-semantics")` returns only lexical `*-semantics`
suggestions and misses the conceptually-correct `sheaf-theory` / `topos-theory` (zero substring
overlap). So the boundary genuinely needs a cheap LLM.

Decision updated to the **cross-repo MCP** shape, canonical pool **here** (owner picks). Built as
`tools/agent-pool-mcp/`:
- **deterministic core** — `search_pool` (tag-overlap ∩ role_fit), `check_vocab` (membership +
  cheap did-you-mean). No LLM.
- **boundary path** — `recommend_agents`: deterministic prefilter → a cheap Haiku that returns up
  to N **unordered** names + a coverage verdict, with names validated against the pool and any
  "new" tag that already exists rejected deterministically (two-layer guarantee).
- Consumers (`domainspec-lean-formalization`, future repos) call the server; the pool stays a
  single source of truth here. `search_pool`/`check_vocab` need no API key; `recommend_agents`
  degrades to the deterministic prefilter without one.
- **Latent bug found by building it:** the pool's front-matter had unquoted scalars with
  `colon-space` (`description`, the "Two known issues to revisit:" note) → invalid YAML that no
  machine had parsed before. Fixed in the canonical pool.

Idea 2 (name-level pairwise opposition) and its telemetry-label prerequisite remain **backlog**.
