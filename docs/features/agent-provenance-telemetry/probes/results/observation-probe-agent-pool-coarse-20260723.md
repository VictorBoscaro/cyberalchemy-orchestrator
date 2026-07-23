# Observation Probe — agent-pool coarse labels

## Run

- canonical run: `probe-run-agent-pool-coarse-20260723-v2`
- mode: `session_direct`
- target: `agent-pool:sha256:5c7b9745a336670ecb55df1276912166954a0d7960443f0df787405564099eba`
- lens: `agent-pool-scientist-tags@1`
- lens digest: `sha256:3cd34692e30b06708e7f790c0bd83d009f969d02b651447105b44f4ba0116e0f`
- observation schema: `apt.observation.agent-pool-scientist-tags@1`
- state: `delivered`
- observations: 6
- observations digest: `sha256:7b8d03fb7538a75eb57eccafebe2e952aa794656ca8ced62ab08f100d6cc4fbb`
- delivery receipt: `experimental_rcpt_54554459e4094cf2ab4684eb08237b7b` (`verified=true`)

The preceding run `probe-run-agent-pool-coarse-20260723` is retained as negative experimental
evidence: a failed digest calculation produced `sha256:`, which the first implementation accepted.
The command gate now requires `sha256:` plus exactly 64 lowercase hexadecimal characters. Historical
replay remains possible, while new malformed lens/observation digests are rejected.

## Observations

- The pinned pool contains 414 entries; every entry has tags; there are 721 distinct fine tags.
- `field` is the existing coarse profile dimension. Counts are led by `math=138`, `cs=90`,
  `physics=54`, `management=32` and `philosophy=31`.
- Reproducible scientist-like evidence bands are 60 natural, 74 including behavioral, 89 including
  social, and 348 including formal/computational fields. The roster total 414 is not itself a
  scientist classification.
- `tags` are fine expertise labels; `role_fit`, `era` and `cited` are separate profile dimensions.
  None records observed agent behavior or establishes a fact.
- Knowledge Taxonomy's open domain and closed facets classify information records; they must not be
  merged into scientist expertise tags.
- The agent-pool MCP search surface omits `field` and `era`; a Probe must read and pin the pool
  snapshot rather than infer those values from search results.

## Design interpretation

The observations license a narrow next sequence, not automatic schema mutation:

1. `coarse-topic-granularity@1`: externally label raw terms as `broad | granular | unclear`, using
   two annotators and an unresolved result below the preregistered agreement threshold.
2. `profile-affinity-exact@1`: compare observed terms with a pinned scientist profile by exact
   overlap only; never infer expertise, correctness or influence.
3. `kt-facet-classification@1`: classify information records through pinned Knowledge Taxonomy
   facets, keeping those facets separate from topic/expertise tags.

No observation from this run writes to `agent-pool.yaml`, extends its 721-tag vocabulary or promotes
a scientist label to canonical knowledge.
