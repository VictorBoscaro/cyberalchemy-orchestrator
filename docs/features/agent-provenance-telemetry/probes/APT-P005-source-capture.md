# APT-P005 — Tool-mediated paper/source capture

## Claim under test

The system can produce an auditable per-seat list of papers actually accessed during research without
asking the agent to write ledger files or treating every search result as researched.

The claim is bounded: “all papers” means all paper-like sources observed through mediated tools in
the harness. It says nothing about private model context or uninstrumented channels.

## Compared capture modes

- `G — gateway`: the research tool wrapper records returned, opened and content-accessed sources from
  tool responses and writer-stamped context.
- `D — deposit`: the agent calls `record_research_source(locator)` when it considers a source used;
  the service resolves metadata and writes the observation.
- `H — hybrid`: gateway capture plus deposit, with deterministic deduplication.

The agent never supplies conversation, dispatch, seat, attempt, timestamp or recipient fields.

## Method

1. Build six immutable research tasks that require literature lookup and expose only the mediated
   research tools under test.
2. Preserve the complete tool-call/result trace as the measurement reference.
3. Represent source progression separately: `returned`, `opened`, `content_accessed`. Define
   “researched paper” for this pilot as a paper with `content_accessed`; a search-result appearance is
   not enough.
4. Canonicalize work identity using the strongest observed locator in order DOI, arXiv identifier,
   canonical URL, content hash. Keep work identity distinct from version/manifestation identity.
5. Compare each mode on:

   - recall against `content_accessed` paper events in the tool trace;
   - false-researched rate: records classified as researched without content access;
   - duplicate work count and lost-version count;
   - unresolved-locator count;
   - records with missing or conflicting writer-stamped lineage.

## Preregistered decision

- Gateway capture is the default only if recall is 100% for mediated `content_accessed` events and
  false-researched rate is 0%.
- Deposit-only is rejected as a completeness claim if recall is below 95%; it may remain an explicit
  semantic signal (“agent says it used this”) with attributed provenance.
- Prefer hybrid only if it increases recall or resolves identifiers without increasing duplicate-work
  or false-researched counts. Otherwise use gateway capture and retain deposits as a separate signal.
- Any uninstrumented source channel narrows the claim; it is never silently counted as covered.

## Falsifiers and invalid runs

- Search results are counted as researched without an open/content event.
- The agent writes directly to the observation store.
- Work and version identities are collapsed so that distinct editions disappear.
- Tool trace and source observation use different attempts without an explicit link.

## Output

Pinned tool traces, per-mode source observations, work/version dedup tables, metrics and a capture-mode
decision. Papers’ full text is not copied into telemetry by this probe.

