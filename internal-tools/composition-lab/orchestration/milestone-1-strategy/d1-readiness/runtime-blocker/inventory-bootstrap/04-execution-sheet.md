---
artifact_kind: bounded-inventory-bootstrap-execution-sheet
status: proposed-blocked-awaiting-gates
date: 2026-08-13
sheet_producer_attempt: 3
mode: inventory/backfill-validate-lint
registration: forbidden
runtime_shape: owner-directed-helper-workflow
connections: []
inventory_root: .arcanum/inventory
head_at_authoring: 6f9d7d860a3e3dd3c6e702fbb1117a3741b22930
---

# D1 bounded Inventory bootstrap — exact execution sheet

## Terminal now

**BLOCK.** This sheet is a hashable execution proposal, not launch authority. It does not mutate
Inventory, launch seats, register a dispatch, append a ledger row, or claim that T1–T16 passed.

## Objective, boundary, and mode

Use the installed `.arcanum/inventory/` as the sole Inventory to `backfill` candidate-level,
source-linked descriptions of composition candidates in a frozen 35-file corpus (22 sources in
this checkout plus 13 DomainSpec v2 sources in a revision-pinned sibling checkout), then
run independent read-only `validate` plus bounded `lint`. Preserve ambiguity, conflicts, duplicate
representations, and selector-bounded non-observations. Later Research may consume the result; this
workflow does not define a lens or composition and does not validate causal effect.

Inventory owns candidate cards, indexes, tags, and log. Composition Lab receives only two
milestone-facing projections. The workflow is an unregistered, capability-owned helper workflow,
not a new dispatch type, ACI connection scheduler, accepted-output receipt, or ledger lifecycle.

## Freeze protocol

The current-checkout partition derives from the prepared D1a corpus; its 22 hashes were refreshed
for this regenerated package. The sibling partition is the reviewed 13-row annex. At authoring,
all 35 hashes matched their declared roots. Those observations expire at the human freeze.
The table in this execution sheet is the semantic freeze authority. For mechanical extraction only,
the proposed row source is `d1-readiness/record/d1-dispatch-sheet.md`, currently SHA-256
`51e442ee7ccdc15122ee607d2fd3ac2ba8eae9d116ab8db695672d29bae2151e`, size `13063`, at repository
commit `6f9d7d860a3e3dd3c6e702fbb1117a3741b22930`. The exact-run digest must bind that path/hash/size/
revision and prove row-for-row equality with this table. A mismatch returns
`BLOCK/FREEZE_AUTHORITY_DIVERGENCE`; it never updates this sheet's expected values.

Immediately before confirmation, the host must run the following read-only check and present the
resulting commit, each actual hash, total count, external-sheet identity, and any drift to the human:

```powershell
$sheet = 'internal-tools/composition-lab/orchestration/milestone-1-strategy/d1-readiness/record/d1-dispatch-sheet.md'
$sheetExpectedHash = '51e442ee7ccdc15122ee607d2fd3ac2ba8eae9d116ab8db695672d29bae2151e'
$sheetExpectedSize = 13063
$sheetItem = Get-Item -LiteralPath $sheet
if ($sheetItem.Length -ne $sheetExpectedSize) { throw 'BLOCK/FREEZE_AUTHORITY_DIVERGENCE' }
if ((Get-FileHash -Algorithm SHA256 -LiteralPath $sheet).Hash.ToLower() -ne $sheetExpectedHash) {
  throw 'BLOCK/FREEZE_AUTHORITY_DIVERGENCE'
}
$commit = git rev-parse HEAD
$pairs = Select-String -Path $sheet -Pattern '^([0-9a-f]{64})  (.+)$'
foreach ($m in $pairs) {
  $expected = $m.Matches[0].Groups[1].Value
  $path = $m.Matches[0].Groups[2].Value
  if (-not (Test-Path -LiteralPath $path)) { throw "BLOCK/source-missing:$path" }
  $actual = (Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash.ToLower()
  if ($actual -ne $expected) { throw "BLOCK/source-drift:$path" }
  [pscustomobject]@{ path=$path; selector='entire-file'; commit=$commit; sha256=$actual }
}
if ($pairs.Count -ne 22) { throw 'BLOCK/corpus-cardinality' }
```

The exact-run fixture must additionally compare the extracted rows to this sheet's 22-row table;
the command above alone is insufficient. No command updates expected hashes. Drift requires a
revised sheet and new human confirmation.
Every selector is `entire-file`; extraction citations must narrow it to heading, line span, anchor,
query, or fragment. D1 outputs are excluded and corpus expansion is forbidden.

## Proposed frozen corpus manifest — current checkout (22 sources)

| # | path | selector | SHA-256 |
|---:|---|---|---|
| 1 | `internal-tools/composition-lab/README.md` | entire-file | `96c7cd1a9e110b16b54692ed6d26d640796b27c8ad2157d22c67c1d9bb3d3d55` |
| 2 | `internal-tools/composition-lab/research/milestone-1/01-repository-inventory/research-initial-definitions.md` | entire-file | `eae0be17cdf4a6a27bfd2b7eb4d8604a50de03b729560a1d417017360fd22918` |
| 3 | `telemetry/agents/subagents-dispatch.yaml` | entire-file | `648946f7f7424fb0d539da4902544fd94021debf1b51f1df8b64149cefb726b8` |
| 4 | `.claude/skills/domainspec-subagents-strategy/SKILL.md` | entire-file | `335987a8684f4672d644054ad3def4ef107d616a689edd84fe30e9652e73eb91` |
| 5 | `.claude/skills/research/SKILL.md` | entire-file | `56ce56d0b8ac779455ee6f76b999f9c84e7bce0a3af14791b575f17b5ee6f4a9` |
| 6 | `.claude/skills/review/SKILL.md` | entire-file | `60dbcb97707949aa7fe102479dbcd712e491bb833362f54b285a536365abd4be` |
| 7 | `.claude/skills/robot-talks/SKILL.md` | entire-file | `a9dfd079ad9351c4bdb4b50d06b8755f31dda7d216cdc9774780e35af6805a39` |
| 8 | `.codex/dispatch-proposals/2026-08-06-irreducible-research-team-design.json` | entire-file | `53c630b51db9c7224eb317b93c6d553921f2b3cc6771dec3b2af8cb02b382426` |
| 9 | `.codex/dispatch-proposals/2026-08-06-irreducible-research-team-design-close.json` | entire-file | `9d3792ab905525ffde03f9c5da587052b5a692f1536d5d692247535f930aaecb` |
| 10 | `.codex/workflow-inputs/2026-07-25-work-context-technical-detail-research/abramsky-manifest.json` | entire-file | `0040566b149d49e135d96dd363d3a3959de8091def79c339569183725d1dbb82` |
| 11 | `.codex/workflow-inputs/2026-07-25-work-context-technical-detail-research/rittel-manifest.json` | entire-file | `ea9ecf2414d45bdc3b79d1a6959025f273c1e8b0ef14de8dc396b89136a9c418` |
| 12 | `plans/governed-agent-work-infrastructure/essays/robot-talks/2026-08-12-work-overview-composition/dialogue.md` | entire-file | `491482947fcf2064c8d8078125e51162f0b73ecf1af431225c205316eada0672` |
| 13 | `plans/governed-agent-work-infrastructure/essays/robot-talks/2026-08-12-work-overview-composition/findings.md` | entire-file | `be10623815ecbd8b5ac48d8505cb8aef93b13188f1fa3e52e43b5258c6d83cf5` |
| 14 | `plans/governed-agent-work-infrastructure/essays/robot-talks/2026-08-12-work-overview-composition/reports/01-reader-journey.md` | entire-file | `d7e7a35bd37293a0c2b55763575e1051b2721915ffa5e1ed0df2d70198528a54` |
| 15 | `plans/governed-agent-work-infrastructure/essays/robot-talks/2026-08-12-work-overview-composition/reports/02-system-composition.md` | entire-file | `ab1b5e57f38b2c362f9eee65cf27cb7ba61be34130ecc0dd841a6272aa346d8d` |
| 16 | `plans/governed-agent-work-infrastructure/essays/robot-talks/2026-08-12-work-overview-composition/reports/03-product-fidelity.md` | entire-file | `046df6f3509e7b209fd156c45c04f33bea1fc41615ca3c97b5aa90ffb4690250` |
| 17 | `docs/temps/operational-knowledge-language/robot-talks/2026-08-11-editorial-next-step/dialogue.md` | entire-file | `b6ebe1092e2c58250796d52aed91168c431bd5cc014bb3126c0a1ca9752743ee` |
| 18 | `docs/temps/operational-knowledge-language/robot-talks/2026-08-11-editorial-next-step/findings.md` | entire-file | `b8bffbf658a1414b35fdeb133e99c7b422c540863c430bd2ffeb146dddf76b8a` |
| 19 | `docs/features/agent-provenance-telemetry/reviews/2026-07-22-system-tags-and-lens-review.md` | entire-file | `5cadf61c8b19096229fa8b022a54de77ce2514417df748d6a45487f89b6949a7` |
| 20 | `docs/features/agent-provenance-telemetry/probes/APT-P007-emergent-lens.md` | entire-file | `d3d77c7a55d1a4bb38d689434e9c25f656cd10f5e4eb90a99a866e881f57e4ce` |
| 21 | `docs/features/agent-provenance-telemetry/probes/lenses/README.md` | entire-file | `dd6a05eef436f97fbf412855de766350de99c380d41cb363b357314c7337763f` |
| 22 | `docs/features/agent-provenance-telemetry/probes/lenses/agent-pool-scientist-tags@1.json` | entire-file | `3cd34692e30b06708e7f790c0bd83d009f969d02b651447105b44f4ba0116e0f` |

### Revision-pinned sibling annex — `domainspec-core` (13 sources)

The exact rows, sizes, roles and authority states are frozen by
`internal-tools/composition-lab/orchestration/dispatch-proposals/internal/domainspec-v2/corpus-manifest.md`.
They resolve relative to `C:/Users/victo/domainspec-core` at revision
`9bfec22712e4675d39c4cf1c21b36dc66614136c`, never relative to this checkout. The host verifies
revision, scoped clean status, path, size and SHA-256 before materialization. Sibling bytes are not
copied into this repository.

| global # | sibling repository-relative path | selector | SHA-256 | bytes |
|---:|---|---|---|---:|
| 23 | `projects/domainspec-v2/README.md` | entire-file | `ca5cfbc0a467e3f14e459236d373db4c046f428930c0fae7571246bfe0aeefff` | 6246 |
| 24 | `projects/domainspec-v2/research/TWO-LANE-DISCIPLINE.md` | entire-file | `cb09d2412e53288ae891ad6d1f03ff5d56c10808824bf0d7e025fc233cd93557` | 2575 |
| 25 | `projects/domainspec-v2/research/domainspec-v2-research-towers.dispatch.json` | entire-file | `83206a57f4ed8d05a1c623ede6db17ae058e74fcfdc184150d20f2f7096147fd` | 15381 |
| 26 | `projects/domainspec-v2/research/target-state/2026-07-02-comprehension-narrative-model/lens-narrative.md` | entire-file | `8b58ef34e0ce95ee5dc76757a963bc3512f53fc97fadc6e460608d00bb23f11c` | 18694 |
| 27 | `projects/domainspec-v2/research/target-state/2026-07-02-comprehension-narrative-model/lens-example.md` | entire-file | `d0885fe8899d245dcee081974d4551e9797f332b33afcfb399b031e3852ac20b` | 14843 |
| 28 | `projects/domainspec-v2/research/target-state/2026-07-02-comprehension-narrative-model/lens-distillation.md` | entire-file | `c96a7366c8bf67d263def4ec1358feb08b55aa6acb5ded10535557f8a109eec5` | 20274 |
| 29 | `projects/domainspec-v2/research/target-state/2026-07-02-comprehension-narrative-model/findings.md` | entire-file | `774c37b64ae35c9536ebb0fdc2442b052a578187f663f2ff39bece335639e3f4` | 7778 |
| 30 | `projects/domainspec-v2/research/2026-07-01-composability-edges-taxonomy-synthesis.md` | entire-file | `bf2a5a45f7214e36eda2048251315571a6d8d27be7a1e59c1c8f0ce23963fc0d` | 10798 |
| 31 | `projects/domainspec-v2/research/typed-artifacts-precedent/findings.md` | entire-file | `597bdf17b876b2d4ab68b91e6c748cdb849214cd36cec011d3e83b75dc59606f` | 9923 |
| 32 | `projects/domainspec-v2/research/spec-ontology-unification/DESIGN.md` | entire-file | `e5410e893314d0c000d291e02a527b4535e5f689f9862ab0b1259e1d78138432` | 6410 |
| 33 | `projects/domainspec-v2/development/ds-d1-improvement-plan/WORK-PACK.md` | entire-file | `c70bca7310ac0e3e06046f88a978e85edb82b6ba8fbe4d40f29f3f8526029d81` | 18242 |
| 34 | `projects/domainspec-v2/impl/spec/meta-types/ui/component.schema.yml` | entire-file | `46540796103bac845fc78aee3deceb8fe905a85968b76f7edb7d987efc8deca0` | 1286 |
| 35 | `projects/domainspec-v2/definitions/relationships/relationships.yml` | entire-file | `7757884f599bb18707f105add8b9de92fb2ea58d78e216d3aa228b0ad25ea013` | 27039 |

Each manifest row also carries the human-confirmed commit and these control obligations:

`C1` file/source partition only; `C2` nominally different instructions seeking equivalent judgment;
`C3` isolated `lens` language in single-agent prose; `C4` merely concatenated returns; `C5`
unexecuted proposal; `C6` close without output demonstrating relations; `C7` duplicate
proposal/manifest/ledger/report representations; `C8` prescribed mechanism without linked instance.
Every source × control cell ends in cited observation, `not_observed_within_selector`, or open gap.
None of these labels means “non-composition.”

## Exact write set and ownership

Run identifier, `sheet_producer_attempt`, `writer_attempt`, and `audit_attempt` values are frozen at
the exact-run gate. These namespaces are never interchangeable. Paths below are literal; no globs
or dynamic directories are allowed.

| owner | exact path / surface | rule |
|---|---|---|
| host | `.../runs/<run-id>/confirmed-corpus-manifest.json` | Immutable pre-write `ConfirmedCorpusManifest`, bound by path/hash/size/revision to both seats; contains the confirmed rows/controls and no interpretation. |
| extractor-writer | `.arcanum/inventory/raw/d1-lens-use-corpus.manifest.json` | Deterministic Inventory projection of `ConfirmedCorpusManifest`; tracked sources remain in place. Auditor proves declared projection equivalence. |
| extractor-writer | `.arcanum/inventory/entries/d1-lens-use/occurrence-cards.json` | Candidate cards only. |
| extractor-writer | `.arcanum/inventory/entries/d1-lens-use/control-cards.json` | Candidate controls/gaps only. |
| extractor-writer | `.arcanum/inventory/entries/d1-lens-use/residue.md` | Ambiguity/conflict/residue only. |
| extractor-writer | `.arcanum/inventory/index.md`, `.arcanum/inventory/index.json`, `.arcanum/inventory/tags.md`, `.arcanum/inventory/log.md` | Sole mutator; coordinated update, append-only log. |
| extractor-writer | `internal-tools/composition-lab/research/milestone-1/01-repository-inventory/research.md` | Human-readable extraction trace; not Research transcript. |
| extractor-writer | `internal-tools/composition-lab/research/milestone-1/01-repository-inventory/findings.md` | Non-authority projection; no Research verdict matrix. |
| coverage-auditor | `internal-tools/composition-lab/orchestration/milestone-1-strategy/d1-readiness/runtime-blocker/inventory-bootstrap/runs/<run-id>/audit-attempt-<audit_attempt>.md` | Immutable attempt-specific audit and verdict; never indexed as Inventory knowledge. |
| host | `.../runs/<run-id>/barrier-writer-attempt-<writer_attempt>.json` and `barrier-audit-attempt-<audit_attempt>.json` | Integrity metadata only: typed attempt fields, path, SHA-256, size, terminal state. No semantic prose. |
| host | `.../runs/<run-id>/post-audit-telemetry-check-<audit_attempt>.json` | Read-only mechanical verification of the terminal signal after auditor termination; no semantic synthesis. |
| host | `.../runs/<run-id>/completion.json` | Factual capability completion: confirmations, typed seat attempts, artifact hashes, audit verdict, correction count, mutation list, signal result, gaps, exit reason. |
| observability runtime | `.arcanum/observability/signals/sigil-invocations.jsonl` | Sole permitted observability write; rebuilding any observability index is out of scope. |
| none (pre-existing human-accepted source) | `internal-tools/composition-lab/research/milestone-1/01-repository-inventory/research-initial-definitions.md` | Read-only frozen source; no bootstrap writer. It remains byte-identical across every writer/audit attempt. |

`d1-lens-use-validation.md` is deliberately **not** an Inventory target. The independent auditor,
not the writer, owns validation; pre-indexing its future report would require an undeclared
post-audit Inventory writer. The auditor report above replaces it as capability-local workflow
evidence. A later human-approved Inventory operation may index that report by reference.

Before launch, resolve every path to an absolute path and require it to equal an allowlisted target.
Unexpected pre-existing targets, copied sources, tag drift, undeclared files, or observability writes
outside the exact JSONL surface return BLOCK before mutation. If the host cannot materialize the
pre-write manifest without parent semantic interpretation, return `BLOCK/HOST_WORKFLOW_UNPROVEN`.

## Seats and connectionless artifact barriers

The main agent only orchestrates: it freezes/presents the proposal, launches bound seats, waits for
terminal states, invokes host barrier generation, and reports terminal state. It never extracts,
summarizes, selects, rewrites, repairs, or approves semantic content.

| order | seat | inputs | writes | terminal |
|---:|---|---|---|---|
| 1 | `extractor-writer` | confirmed sheet + host `ConfirmedCorpusManifest`, corpus, installed Inventory package | writer-owned paths only | `WRITER_COMPLETE` or a BLOCK terminal; `writer_attempt=1` |
| 2 | `coverage-auditor` | same confirmed sheet/manifest plus host writer-barrier rows and exact files opened directly | attempt-specific audit only | `PASS`, `BOUNDED_CORRECTIONS`, or `BLOCK`; `audit_attempt=1` |
| 3, conditional | same `extractor-writer`, `writer_attempt=2` | frozen auditor artifact via host audit barrier; same confirmed revision and scope | writer-owned paths only | `WRITER_COMPLETE` or BLOCK; no `writer_attempt=3` |
| 4, conditional | same `coverage-auditor`, `audit_attempt=2` | fresh writer barrier and exact files | new attempt-specific audit only | `PASS` or `BLOCK` |
| 5 | host post-audit check | terminal audit barrier plus exact signal JSONL | post-audit telemetry check only | `TELEMETRY_VERIFIED` or `BLOCK/OBSERVABILITY_GAP` |

`connections` remains exactly `[]`. A barrier is an integrity precondition for a later independent
seat launch, not a runtime connection, causal relation, accepted-output receipt, or proof that one
artifact influenced another. The host creates it only after the producer is terminal. It contains
no return prose. Every barrier declares exactly one of `writer_attempt` or `audit_attempt` and also
the bound `sheet_producer_attempt`; a value in the wrong namespace is invalid. Wrong bytes/path/
typed attempt, absent expected artifact, early launch, or parent-created
semantic summary returns `BLOCK/artifact-barrier-invalid`. A need for independent extractor returns
or assembly returns `BLOCK/inventory-connected-topology-required`.

## Complete immutable seat prompts

The host replaces only declared placeholders after human confirmation. The binding line is always
the first line; failure to materialize it blocks launch.

### Extractor-writer

```text
ACI-WORKFLOW-BINDING-V1:<host-supplied-base64>
You are the sole extractor-writer for confirmed D1 Inventory run <run-id>, sheet_producer_attempt=<sheet_producer_attempt>, writer_attempt=<1|2>. Read the complete confirmed execution sheet, host-owned immutable ConfirmedCorpusManifest, and installed `.arcanum/inventory/{README.md,schema.md,index.json,index.md,tags.md,log.md}`. Verify the bound sheet identity, manifest path/hash/size/revision, confirmed commit, and every source SHA-256 before relying on bytes. Read only the 22 frozen sources. Keep `research-initial-definitions.md` read-only and byte-identical. Write only the exact extractor-writer allowlist. Materialize the raw Inventory manifest as the declared deterministic projection of ConfirmedCorpusManifest. Produce candidate evidence cards and source×control coverage; cite selectors; preserve separate conflicting assignments, duplicate representations, trace, residue, and gaps. Treat `source-asserted-effect` only as a literal source assertion. Do not define lens/composition, infer causality, judge novelty/soundness, promote ontology/definitions, recommend GO/KILL, expand/copy/edit sources, write audit/completion/barrier/ledger files, or launch agents. Keep index.md/index.json/tags/log and both Composition Lab projections mutually consistent. Recompute source hashes after writing. Return only WRITER_COMPLETE with sheet_producer_attempt, writer_attempt, exact path/hash/size/count/source-before-after rows, or BLOCK/<reason>. On writer_attempt=2, correct only defects cited in the bound audit artifact; do not reinterpret or exceed the confirmed scope.
```

### Coverage-auditor

```text
ACI-WORKFLOW-BINDING-V1:<host-supplied-base64>
You are the independent read-only coverage auditor for confirmed D1 Inventory run <run-id>, sheet_producer_attempt=<sheet_producer_attempt>, audit_attempt=<1|2>, consuming writer_attempt=<1|2>. Read the complete confirmed execution sheet, host-owned immutable ConfirmedCorpusManifest, installed Inventory conventions, and host-owned writer barrier. Verify the bound sheet identity, manifest path/hash/size/revision, writer terminal state, and every barrier path/SHA-256/size/typed attempt, then open the exact files directly. Reject any attempt value in the wrong namespace. Recompute all 22 source hashes and the frozen source×control denominator; prove the writer-owned raw manifest is the declared projection of ConfirmedCorpusManifest and `research-initial-definitions.md` remains byte-identical. Check schema/enums, selectors, trace, residue, conflict/duplicate preservation, index agreement, tags, append-only log, projection-to-card mapping, write boundary, authority escape, and pre-audit telemetry linkage. Mechanical validity never proves a category true or an effect causal. Write only the exact audit_attempt path. Return PASS, BOUNDED_CORRECTIONS with exact bounded defects, or BLOCK/<reason>. Never edit Inventory/projections/sources, validate the not-yet-emitted terminal signal, summarize hidden writer prose, launch agents, approve launch, or claim ACI/ledger handoff evidence. Any partial write, unexplained target, source drift, invalid barrier, authority escape, or correction beyond cap is BLOCK.
```

Models, tools, token budgets, concrete seat identities, run ID, prompt digests, and both resolved audit
paths remain placeholders and therefore **BLOCK** until frozen together at the exact-run gate.

## Validation, partial state, and recovery

Validation is mechanical and read-model-only. It checks canonical evidence-card envelope/version,
additional-field acceptance, source refs/selectors, stable IDs, cross-references, denominator coverage,
index parse/agreement, tags, append-only log, projections, immutability, allowlist, and observability.
It does not validate the truth of an assignment.

No transactional rollback or filesystem atomicity is demonstrated. Pre-write hashes/snapshots,
write ordering, partial-state detection, and bounded repair still require a human-confirmed fixture.
A partial write terminates `BLOCK/PARTIAL_STATE_REQUIRES_HUMAN_RECOVERY`; it cannot enter the normal
correction loop. No retry occurs until a separately authorized recovery owner restores or repairs
the exact write set and an independent audit verifies it. Detection is not rollback.

Later retirement is different: after separate human approval, an Inventory owner marks D1 cards and
rows `superseded` with a non-`none` owner, appends a tombstone containing reason/IDs/last hashes/
replacement/consumers, preserves resolvable history, and removes no source, governed artifact,
milestone projection, or unrelated entry. Active undeclared consumers or governed references block
retirement. Retirement is reversal of a maintained read model, not recovery from a torn write.

## Observability

The sole observability target is
`.arcanum/observability/signals/sigil-invocations.jsonl`; observability index rebuilding is out of
scope. Pre-audit attempt signals contain Inventory-owned mode, source count, created/updated entries,
contradictions, lint gaps, validation, downstream lookup count, filed synthesis count, `run_id`,
corpus digest, profile version, `sheet_producer_attempt`, and `writer_attempt`. The auditor verifies
only these already-existing records.

After the auditor terminates, the runtime appends a terminal signal containing `audit_attempt`,
auditor verdict, correction count, and exit reason. The host then performs a separately bound,
read-only mechanical check and writes only
`runs/<run-id>/post-audit-telemetry-check-<audit_attempt>.json`. The main does no semantic synthesis.
Missing or unresolvable telemetry after otherwise mechanically valid Inventory writes yields the
distinct run-level `BLOCK/OBSERVABILITY_GAP`; it does not trigger content rewriting and is not called
Inventory partial-state recovery. A torn Inventory write remains
`BLOCK/PARTIAL_STATE_REQUIRES_HUMAN_RECOVERY`.

Signals are local read-model evidence only: never ACI, ledger, authority, semantic validity, or
causal-effect evidence. Bridge stdout remains only in the journal and is never persisted in the run
folder.

## T1–T16 execution matrix

| test | owner | required evidence and moment | fail-closed result |
|---|---|---|---|
| T1 canonical owner | human + canonical owner | ratification, `.codex` ownership, runtime metadata and generated-surface conformance before exact-run gate | `BLOCK/CANONICAL_OWNER_OR_SURFACE` |
| T2 reuse falsifier | human | separate answer naming consumer/revalidation before preparing mutation | `BLOCK/INVENTORY_LIFECYCLE_UNWARRANTED` |
| T3 single system | auditor | static scan before and after; sole root/index/log/schema | `BLOCK/COMPETING_INVENTORY` |
| T4 artifact fit | human + auditor | approve projection semantics before run; verify card linkage after write | `BLOCK/ARTIFACT_CONTRACT` |
| T5 lifecycle dry run | host + auditor | bound-seat/order/typed-attempt/completion and ConfirmedCorpusManifest fixture before launch | `BLOCK/HOST_WORKFLOW_UNPROVEN` |
| T6 barrier integrity | host + auditor | wrong path/hash/attempt-namespace/early/missing/prose negatives before launch | `BLOCK/ARTIFACT_BARRIER_INVALID` |
| T7 confirmation | human | one digest freezes sheet/external-row source/ConfirmedCorpusManifest, targets, typed attempts, seats, prompts, tools/models/budgets, cap, observability, recovery, close | `BLOCK/CONFIRMATION_MISSING_OR_DRIFTED` |
| T8 immutability | writer + auditor | row-authority equality, independent before/after hashes including initial-definitions, and target-escape negatives each writer_attempt | `BLOCK/SOURCE_DRIFT_OR_WRITE_ESCAPE` |
| T9 minimal schema | canonical owner + auditor | canonical v0.2 validator and occurrence/absence/ambiguity/contradiction/duplicate fixtures before launch | `BLOCK/SCHEMA_OR_SEMANTIC_ESCAPE` |
| T10 authority negatives | auditor | definition/causality/novelty/soundness/promotion/GO-KILL fixtures before launch and run check | `BLOCK/AUTHORITY_ESCAPE` |
| T11 denominator | host materializes; human freezes; auditor checks | host ConfirmedCorpusManifest binds 35×8 = 280 obligations before write; Inventory projection equivalent; every cell resolved after | `BLOCK/DENOMINATOR_GAP` |
| T12 mechanical validity | auditor | JSON/schema/index/log/link/projection consistency after each writer attempt | `BLOCK/MECHANICAL_INVALID`; partial → human recovery |
| T13 observability | runtime + auditor + host verifier | pre-audit signal fixture, terminal signal, then post-audit host check; exact JSONL only | `BLOCK/OBSERVABILITY_GAP` |
| T14 conflict preservation | auditor | disagreement fixture before launch and no overwrite/normalization after write | `BLOCK/CONFLICT_LOSS` |
| T15 reversal | human + Inventory owner | recovery fixture before launch; separate retirement fixture/consumer check before later retirement | `BLOCK/RECOVERY_OR_RETIREMENT_UNPROVEN` |
| T16 no-launch review | independent reviewers + human | R1–R4, final `/review`, no unresolved material finding, explicit launch authorization | `BLOCK/REVIEW_OR_LAUNCH_GATE` |

## Material human gates

Four decisions are separate and recorded by digest:

1. **Reuse:** name a durable consumer/revalidation event; all-no stops.
2. **Owner/design:** canonical Inventory owner ratifies the candidate profile, connectionless helper
   workflow, sole-root policy, and stale-surface recovery result.
3. **Exact run:** human confirms commit/hashes/selectors/controls, first-ingest precedent, targets and
   output ownership, two identities, immutable prompts, models/tools/budgets, typed attempt paths,
   freeze-source identity/equality, ConfirmedCorpusManifest, barrier schema, exact observability
   target and post-audit verifier, correction cap, close semantics, and the explicit absence of transactional
   rollback plus partial-state recovery risk.
4. **Launch:** after fixtures, T1–T16, R1–R4, and final `/review`, human explicitly authorizes D1.

Any material delta invalidates confirmation. Earlier permission to use agents is not mutation or
launch authorization.

## Effects expressly excluded

The bootstrap does not authorize or prove: skill/canonical/generated-surface mutation or sync;
LIVE registration, ledger rows, dispatch-schema/runtime changes, or connected handoffs; a second
Inventory; definitions of lens/composition; ontology/canonical promotion; novelty, soundness,
causality, epistemic validity, GO/KILL, or composition effects; dynamic corpus expansion, source
edits/copies; transactional rollback; deletion of sources, governed artifacts, milestone
projections, or history.

## Terminal enum

- `PROPOSAL_BLOCKED` — current state; antecedent evidence/gates missing.
- `READY_FOR_EXACT_CONFIRMATION` — complete fixture/review evidence exists; no mutation authority.
- `READY_TO_LAUNCH` — exact human launch authorization exists.
- `WRITER_COMPLETE` — writer artifacts frozen; not success.
- `PASS` — independent mechanical audit passed; still no epistemic/causal claim.
- `BOUNDED_CORRECTIONS` — one exact correction attempt permitted.
- `BLOCK/<reason>` — stop without further normal writes.
- `BLOCK/PARTIAL_STATE_REQUIRES_HUMAN_RECOVERY` — partial mutation detected; no automatic retry or
  rollback claim.
- `INVENTORY_CONNECTED_TOPOLOGY_REQUIRED` — required work exceeds the two-seat artifact-barrier
  design.
- `COMPLETED_WITH_GAPS` — host completion records an accepted bounded run and explicit gaps; only
  available after auditor PASS and human-owned parent workflow close where applicable.

Current terminal: **`PROPOSAL_BLOCKED`**.
