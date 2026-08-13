---
artifact_kind: governed-dispatch-readiness-sheet
status: prepared-not-opened
date: 2026-08-13
dispatch_id: 2026-08-13-repository-lens-inventory-extraction
---

# D1a — raw repository inventory extraction

## Decision

Split D1 into D1a raw extraction and a later D1b classification/gates dispatch. This record covers
only D1a. D1b cannot be concretely prepared until D1a has frozen its raw inventory and hashes.
Do not register, compile, open, or launch D1a until the human confirms the exact record and the
compiler/topology incompatibility below is resolved.

Delegation is warranted because configuration identity, preserved enactment traces, normative
status, and negative controls have different proof regimes. The four explorers are honestly a
partitioned collection team, not four lenses. A single writer merges their non-overlapping fields,
an auditor checks coverage/provenance, and a separate auditor only approves.

## Route

- capability: `research`
- dispatch type: `research`
- authority: `legacy-managed`
- tool profile: `host/inherited@1`
- ledger schema: `0.6.3`
- route receipt: `route-receipt.json`
- exact proposed opening: `opening-record.json`
- working folder: `internal-tools/composition-lab/research/milestone-1/01-repository-inventory`
- required outputs: `research.md` and `findings.md`
- files already present in working folder: `research-initial-definitions.md` only

## Frozen corpus

Only these 22 internal files are in scope: 1,969,246 bytes at Git commit
`6f9d7d860a3e3dd3c6e702fbb1117a3741b22930`. Hash algorithm is SHA-256. Digest or commit drift is a
fail-closed condition; absence is recorded as evidence rather than silently substituted.

```text
1d2ef9cae7b41028e0a53bf9ec1efc3a3970385c75f2943f2a175a6a3266e806  internal-tools/composition-lab/README.md
2183ce096aa33224ef94cf00f56aa1c42e69ae2dc630cde4ecddae7eaf098932  internal-tools/composition-lab/research/milestone-1/01-repository-inventory/research-initial-definitions.md
e28aad64545131ac684731213eefa38b865f4807f439578950514eb3f9b9062c  telemetry/agents/subagents-dispatch.yaml
335987a8684f4672d644054ad3def4ef107d616a689edd84fe30e9652e73eb91  .claude/skills/domainspec-subagents-strategy/SKILL.md
56ce56d0b8ac779455ee6f76b999f9c84e7bce0a3af14791b575f17b5ee6f4a9  .claude/skills/research/SKILL.md
60dbcb97707949aa7fe102479dbcd712e491bb833362f54b285a536365abd4be  .claude/skills/review/SKILL.md
a9dfd079ad9351c4bdb4b50d06b8755f31dda7d216cdc9774780e35af6805a39  .claude/skills/robot-talks/SKILL.md
53c630b51db9c7224eb317b93c6d553921f2b3cc6771dec3b2af8cb02b382426  .codex/dispatch-proposals/2026-08-06-irreducible-research-team-design.json
9d3792ab905525ffde03f9c5da587052b5a692f1536d5d692247535f930aaecb  .codex/dispatch-proposals/2026-08-06-irreducible-research-team-design-close.json
0040566b149d49e135d96dd363d3a3959de8091def79c339569183725d1dbb82  .codex/workflow-inputs/2026-07-25-work-context-technical-detail-research/abramsky-manifest.json
ea9ecf2414d45bdc3b79d1a6959025f273c1e8b0ef14de8dc396b89136a9c418  .codex/workflow-inputs/2026-07-25-work-context-technical-detail-research/rittel-manifest.json
491482947fcf2064c8d8078125e51162f0b73ecf1af431225c205316eada0672  plans/governed-agent-work-infrastructure/essays/robot-talks/2026-08-12-work-overview-composition/dialogue.md
be10623815ecbd8b5ac48d8505cb8aef93b13188f1fa3e52e43b5258c6d83cf5  plans/governed-agent-work-infrastructure/essays/robot-talks/2026-08-12-work-overview-composition/findings.md
d7e7a35bd37293a0c2b55763575e1051b2721915ffa5e1ed0df2d70198528a54  plans/governed-agent-work-infrastructure/essays/robot-talks/2026-08-12-work-overview-composition/reports/01-reader-journey.md
ab1b5e57f38b2c362f9eee65cf27cb7ba61be34130ecc0dd841a6272aa346d8d  plans/governed-agent-work-infrastructure/essays/robot-talks/2026-08-12-work-overview-composition/reports/02-system-composition.md
046df6f3509e7b209fd156c45c04f33bea1fc41615ca3c97b5aa90ffb4690250  plans/governed-agent-work-infrastructure/essays/robot-talks/2026-08-12-work-overview-composition/reports/03-product-fidelity.md
b6ebe1092e2c58250796d52aed91168c431bd5cc014bb3126c0a1ca9752743ee  docs/temps/operational-knowledge-language/robot-talks/2026-08-11-editorial-next-step/dialogue.md
b8bffbf658a1414b35fdeb133e99c7b422c540863c430bd2ffeb146dddf76b8a  docs/temps/operational-knowledge-language/robot-talks/2026-08-11-editorial-next-step/findings.md
5cadf61c8b19096229fa8b022a54de77ce2514417df748d6a45487f89b6949a7  docs/features/agent-provenance-telemetry/reviews/2026-07-22-system-tags-and-lens-review.md
d3d77c7a55d1a4bb38d689434e9c25f656cd10f5e4eb90a99a866e881f57e4ce  docs/features/agent-provenance-telemetry/probes/APT-P007-emergent-lens.md
dd6a05eef436f97fbf412855de766350de99c380d41cb363b357314c7337763f  docs/features/agent-provenance-telemetry/probes/lenses/README.md
3cd34692e30b06708e7f790c0bd83d009f969d02b651447105b44f4ba0116e0f  docs/features/agent-provenance-telemetry/probes/lenses/agent-pool-scientist-tags@1.json
```

The corpus intentionally contains prescriptions, dispatch/proposal traces, two Robot-Talks
instances, a persisted review, provenance probes, and controls. It is a bounded inventory sample,
not a repository-wide census and not evidence of general causal effect.

| corpus family | source type | period/schema | inclusion and identity rule |
|---|---|---|---|
| Composition Lab README + initial definitions | normative/context only | 2026-08-13 | bounds claims; never counts automatically as an occurrence |
| dispatch ledger | occurrence index and open/close trace | historical through commit; mixed schemas | census all rows in this frozen file; opening/close with one dispatch ID is one occurrence |
| active `.claude` skills | normative | versions at commit | records prescriptions only; duplicates in other skill trees are excluded |
| two proposal/manifests sets | configuration/controls | 2026-07-25 and 2026-08-06 | proposal, manifest, ledger, and output with the same dispatch/session key are representations of one occurrence |
| two Robot-Talks sessions | preserved execution sample | 2026-08-11 and 2026-08-12 | dialogue, reports, and findings under one session directory are one occurrence |
| persisted review | preserved review sample | 2026-07-22 | one occurrence; not evidence that every recommendation executed |
| APT probe/lens files | proposal/result/provenance context | frozen versions at commit | preserve each file's declared status; a prescribed probe is not an executed occurrence |

There is no dynamic corpus expansion. D1a outputs are excluded from the corpus. D1a may record a
referenced-but-missing output, but may not open it or substitute another path. The bounded ledger is
censused; deep artifacts are the exact maximum-variation sample above, selected before reading by
family, date, registered topology, and preserved state. No saturation or repository-exhaustiveness
claim is authorized.

## Seat × question × corpus × evidence

| owner | bounded question | corpus segment | expected evidence / merge rule |
|---|---|---|---|
| Liskov | What literal configuration and identity fields are present? | ledger, two proposals, two manifests | occurrence-keyed transcription and equivalence links; owns configuration fields |
| Nonaka | What literal enacted traces survive? | two Robot-Talks sessions | occurrence-keyed path:line traces; owns preserved-event fields |
| Lamport | What is prescribed or proposed, with what status? | active skills, APT files, persisted review | clause/status/version table; owns normative-status fields |
| Peirce | Which preregistered controls and outliers occur? | same fixed occurrence keys across all families | challenge annotations only; never overwrites another owner's raw field |
| Knuth | How are raw returns preserved and merged without classification? | all four bound returns | verbatim `research.md`; raw `findings.md`; conflict remains unresolved |
| Hamming | Is the raw bundle reproducible and within its evidence boundary? | frozen manifest + D1a outputs | PASS or bounded correction; no classification or approval |
| Parnas | Did D1a satisfy its exact acceptance contract? | final bundle + audit return | ACCEPT or RETURN only |

The only deliberate overlap is Peirce's replication against shared occurrence IDs. Its adjudication
rule is additive: attach the control challenge and evidence to the owning row; never replace the
literal field or force agreement.

## Seats and effects

| group | agents | function | budget |
|---|---|---|---:|
| extractors | Liskov, Nonaka, Lamport, Peirce | four partitioned raw-evidence surfaces | 26,000 |
| raw inventory writer | Knuth | sole owner of `research.md` and `findings.md` | 10,500 |
| coverage audit | Hamming | hashes, provenance, deduplication, controls, boundaries | 5,000 |
| approver | Parnas | dedicated approval only | 4,000 |

Total declared output budget: 45,500 tokens across 7 seats. The host tool surface is inherited;
the record requests models but the lifecycle must verify the effective host model and tools before
launch.

`anti_bias_mode` is `disabled`. The user's general authorization of multiple agents and final
review is not the dispatch-specific opt-in required by the strategy skill. Therefore the record has
no `angle`, `anti_bias`, `anti_bias_pairs`, or `anti_bias_global` fields. The different collection
responsibilities remain explicit only in prompts.

## Topology and ownership

```text
extractors --sequential--> raw inventory writer --feedback, cap 2--> coverage auditor --sequential--> approver
```

Only Knuth may edit `research.md` and `findings.md`. Extractors and the coverage auditor return
material through governed handoffs. Parnas performs no working task and returns only `ACCEPT` or
`RETURN`.

No agent may modify the frozen corpus, the ledger, or any file outside the two declared outputs.

## Preregistered controls and zero-result rule

D1a must record one concrete witness or `not-observed` for each control, without calling the control
"non-composition":

1. agents divided only by files or sources;
2. nominally different instructions requesting equivalent judgment;
3. isolated use of `lens` in single-agent prose;
4. multiple returns merely concatenated;
5. proposal never executed;
6. close without output capable of showing a relation among contributions;
7. one event represented in proposal, manifest, ledger, and report, testing deduplication;
8. mechanism prescribed in a skill without a demonstrably linked instance.

It is preregistered that the corpus may demonstrate zero compositions and zero compositional
effects. Such a result is valid and limits downstream claims; it does not authorize searching beyond
the manifest or manufacturing a witness.

## Deferred D1b

D1b will consume only the frozen raw inventory and manifest from D1a. Its minimum epistemic shape
is two blind classifiers, one writer, separate internal-ownership/provenance, non-vacuity, and
definitional-soundness gates, a coverage auditor, and a dedicated approver. Classification categories
and collapse tests are intentionally absent from D1a extractor prompts. No D1b opening record is
prepared now because its concrete inputs and hashes do not yet exist.

## Validation and blocking incompatibility

The exact opening record passed the canonical appender's non-mutating `validate_opening_record`
path on 2026-08-13. Its SHA-256 is
`ce18e35a7ececf057ce2fe7e20488784171a1f17912f8b484c6e548302863875`. The route was resolved again
immediately before freeze and remained byte-for-byte equivalent to `route-receipt.json`; the seven
agent names all exist in `telemetry/agents/agent-pool.yaml`; the proposed dispatch ID is absent from
the ledger. No append was used for validation.

The record is not currently compilable even if it passes opening validation. The active
`legacy-managed` compiler in `implementations/server/runtime/dispatch_workflow.py` rejects every
non-empty `connections` array because it cannot materialize downstream handoffs. Removing
`connections` would erase the research capability's required upstream → writer → downstream-audit
semantics and would leave the writer without governed extractor inputs. Therefore this
sheet does not improvise a connectionless dispatch.

Required resolution before confirmation/open: add a governed compiler/runtime path that
materializes these handoffs, or obtain a capability/lifecycle-owned revised record that preserves
equivalent typed sequencing and return it through the strategy skill for mode re-evaluation.
Any such revision requires revalidation and a new exact human confirmation.

Consequently, there is currently no smaller *executable* governed D1a record that preserves the
research contract, one-writer ownership, upstream returns, downstream audit, and dedicated
approval. This is a runtime capability gap, not permission to flatten the graph.

## Explicitly not performed

- no ledger append or direct `register-dispatch` call;
- no workflow compile or generated binding envelope;
- no bridge `open`;
- no seat launch;
- no research output creation;
- no close row.
