---
artifact_kind: bounded-inventory-bootstrap-human-confirmation-sheet
status: bounded-unregistered-blocked-awaiting-human-decisions
date: 2026-08-13
scope: milestone-1-D1-descriptive-lens-use-inventory
sheet_producer_attempt: 3
registration: forbidden
inventory_root: .arcanum/inventory
---

# Human confirmation sheet — D1 bounded Inventory bootstrap

## Terminal status

**BLOCK pending the human choices at the end of this sheet and the remaining exact-run/launch
antecedents.** This sheet presents the bounded proposal; signing a reuse or owner/design choice does
not by itself launch agents or authorize writes. The run remains capability-owned, unregistered,
connectionless (`connections: []`), and outside the dispatch ledger. R1 and R2 fixtures are `PASS`
preparation evidence only.

## Objective

Use the already installed `.arcanum/inventory/` as the sole Inventory system to backfill a
source-linked, candidate-level description of perspective-like configurations in a frozen 22-file
corpus, covering 8 controls (176 source × control cells), followed by an independent read-only
coverage audit. Preserve selectors, trace, ambiguity, contradictions, duplicate representations,
residue, and typed gaps. The result supports later lookup and Research; it does not define a lens or
composition and does not validate causal effect.

## Frozen authorities and corpus

- Semantic execution authority: `04-execution-sheet.md`, attempt 3, SHA-256
  `2be8ed0276ea55d830907aad0f423db8b4b44f181134092aa44071163c6d4f07`, size `26176` bytes.
- Authoring revision recorded by that sheet:
  `6f9d7d860a3e3dd3c6e702fbb1117a3741b22930`.
- Mechanical external row source:
  `internal-tools/composition-lab/orchestration/milestone-1-strategy/d1-readiness/record/d1-dispatch-sheet.md`,
  SHA-256 `51e442ee7ccdc15122ee607d2fd3ac2ba8eae9d116ab8db695672d29bae2151e`,
  size `13063` bytes, at that recorded revision. It must equal the semantic table row-for-row; it
  cannot update expected values.
- Host-owned pre-write manifest: exact run path
  `internal-tools/composition-lab/orchestration/milestone-1-strategy/d1-readiness/runtime-blocker/inventory-bootstrap/runs/<run-id>/confirmed-corpus-manifest.json`.
  Its path, canonical bytes, SHA-256, size, revision, ordered rows, and ordered controls must be
  frozen at the exact-run gate and bound to both seats.
- Corpus selectors are initially `entire-file`; emitted citations must narrow them. Corpus growth,
  substitution, copies, and source edits are forbidden.
- Controls: `C1` file/source partition only; `C2` nominally different instructions seeking
  equivalent judgment; `C3` isolated `lens` language in single-agent prose; `C4` merely concatenated
  returns; `C5` unexecuted proposal; `C6` close without output demonstrating relations; `C7`
  duplicate proposal/manifest/ledger/report representations; `C8` prescribed mechanism without a
  linked instance. These are obligations, not declarations of “non-composition”.

### Frozen 22-file corpus

| # | path | SHA-256 |
|---:|---|---|
| 1 | `internal-tools/composition-lab/README.md` | `1d2ef9cae7b41028e0a53bf9ec1efc3a3970385c75f2943f2a175a6a3266e806` |
| 2 | `internal-tools/composition-lab/research/milestone-1/01-repository-inventory/research-initial-definitions.md` | `2183ce096aa33224ef94cf00f56aa1c42e69ae2dc630cde4ecddae7eaf098932` |
| 3 | `telemetry/agents/subagents-dispatch.yaml` | `e28aad64545131ac684731213eefa38b865f4807f439578950514eb3f9b9062c` |
| 4 | `.claude/skills/domainspec-subagents-strategy/SKILL.md` | `335987a8684f4672d644054ad3def4ef107d616a689edd84fe30e9652e73eb91` |
| 5 | `.claude/skills/research/SKILL.md` | `56ce56d0b8ac779455ee6f76b999f9c84e7bce0a3af14791b575f17b5ee6f4a9` |
| 6 | `.claude/skills/review/SKILL.md` | `60dbcb97707949aa7fe102479dbcd712e491bb833362f54b285a536365abd4be` |
| 7 | `.claude/skills/robot-talks/SKILL.md` | `a9dfd079ad9351c4bdb4b50d06b8755f31dda7d216cdc9774780e35af6805a39` |
| 8 | `.codex/dispatch-proposals/2026-08-06-irreducible-research-team-design.json` | `53c630b51db9c7224eb317b93c6d553921f2b3cc6771dec3b2af8cb02b382426` |
| 9 | `.codex/dispatch-proposals/2026-08-06-irreducible-research-team-design-close.json` | `9d3792ab905525ffde03f9c5da587052b5a692f1536d5d692247535f930aaecb` |
| 10 | `.codex/workflow-inputs/2026-07-25-work-context-technical-detail-research/abramsky-manifest.json` | `0040566b149d49e135d96dd363d3a3959de8091def79c339569183725d1dbb82` |
| 11 | `.codex/workflow-inputs/2026-07-25-work-context-technical-detail-research/rittel-manifest.json` | `ea9ecf2414d45bdc3b79d1a6959025f273c1e8b0ef14de8dc396b89136a9c418` |
| 12 | `plans/governed-agent-work-infrastructure/essays/robot-talks/2026-08-12-work-overview-composition/dialogue.md` | `491482947fcf2064c8d8078125e51162f0b73ecf1af431225c205316eada0672` |
| 13 | `plans/governed-agent-work-infrastructure/essays/robot-talks/2026-08-12-work-overview-composition/findings.md` | `be10623815ecbd8b5ac48d8505cb8aef93b13188f1fa3e52e43b5258c6d83cf5` |
| 14 | `plans/governed-agent-work-infrastructure/essays/robot-talks/2026-08-12-work-overview-composition/reports/01-reader-journey.md` | `d7e7a35bd37293a0c2b55763575e1051b2721915ffa5e1ed0df2d70198528a54` |
| 15 | `plans/governed-agent-work-infrastructure/essays/robot-talks/2026-08-12-work-overview-composition/reports/02-system-composition.md` | `ab1b5e57f38b2c362f9eee65cf27cb7ba61be34130ecc0dd841a6272aa346d8d` |
| 16 | `plans/governed-agent-work-infrastructure/essays/robot-talks/2026-08-12-work-overview-composition/reports/03-product-fidelity.md` | `046df6f3509e7b209fd156c45c04f33bea1fc41615ca3c97b5aa90ffb4690250` |
| 17 | `docs/temps/operational-knowledge-language/robot-talks/2026-08-11-editorial-next-step/dialogue.md` | `b6ebe1092e2c58250796d52aed91168c431bd5cc014bb3126c0a1ca9752743ee` |
| 18 | `docs/temps/operational-knowledge-language/robot-talks/2026-08-11-editorial-next-step/findings.md` | `b8bffbf658a1414b35fdeb133e99c7b422c540863c430bd2ffeb146dddf76b8a` |
| 19 | `docs/features/agent-provenance-telemetry/reviews/2026-07-22-system-tags-and-lens-review.md` | `5cadf61c8b19096229fa8b022a54de77ce2514417df748d6a45487f89b6949a7` |
| 20 | `docs/features/agent-provenance-telemetry/probes/APT-P007-emergent-lens.md` | `d3d77c7a55d1a4bb38d689434e9c25f656cd10f5e4eb90a99a866e881f57e4ce` |
| 21 | `docs/features/agent-provenance-telemetry/probes/lenses/README.md` | `dd6a05eef436f97fbf412855de766350de99c380d41cb363b357314c7337763f` |
| 22 | `docs/features/agent-provenance-telemetry/probes/lenses/agent-pool-scientist-tags@1.json` | `3cd34692e30b06708e7f790c0bd83d009f969d02b651447105b44f4ba0116e0f` |

All source hashes and the repository revision must be recomputed immediately before exact
confirmation. Any difference requires a revised sheet and new confirmation.

## Fixture identities

R1 `ConfirmedCorpusManifest` recheck: **PASS**, 18 tests. R2 post-audit telemetry recheck:
**PASS**, 27 cases. Neither PASS authorizes execution. Disposable `__pycache__` files are excluded
from the fixture identity.

### R1 files

| path | SHA-256 |
|---|---|
| `inventory-bootstrap/fixtures/confirmed-corpus-manifest/.gitignore` | `6feaded4e28ea86e001a6751b4e3d960e8b7c31b9616ff9936b79297086e809b` |
| `inventory-bootstrap/fixtures/confirmed-corpus-manifest/confirmed-corpus-manifest.schema.json` | `497b1d172fe88908b5af1a32040eff9b31c417028704995c228a515404fcc974` |
| `inventory-bootstrap/fixtures/confirmed-corpus-manifest/confirmed_corpus_manifest.py` | `cab17ba4a7345c826c9462dd1af8ebfec21a9d6a810193298abcde29a01a1dc0` |
| `inventory-bootstrap/fixtures/confirmed-corpus-manifest/d1-lens-use-corpus-manifest.schema.json` | `c8a42251ff19b5cf2cee3b80d1611df9fc7f0e0e3d672138da99e71269cb2e6f` |
| `inventory-bootstrap/fixtures/confirmed-corpus-manifest/README.md` | `b2b3fa366bb5e03965774919e67e2f7c50e5aa68d001b957060d363f5a4fbfd5` |
| `inventory-bootstrap/fixtures/confirmed-corpus-manifest/REVIEW.md` | `b8e3b72c15592dbbc595a7dd07de5d569072cc033eac8791e9a630fd8a328c40` |
| `inventory-bootstrap/fixtures/confirmed-corpus-manifest/test_confirmed_corpus_manifest.py` | `d08fa6f345c86874630f89ded2d0c9bdd16b4abc388fd68347dd391ea6c7955d` |

### R2 files

| path | SHA-256 |
|---|---|
| `internal-tools/composition-lab/orchestration/milestone-1-strategy/d1-readiness/runtime-blocker/inventory-bootstrap/fixtures/telemetry-post-audit/README.md` | `d79feab9df8b3bf55528c1974bbbb62aee15393de213bdd1a45f226c259c72ef` |
| `.../telemetry-post-audit/REVIEW.md` | `52510a52a6ce4a5e80772264f22e7619d9c08566a5aacf92c893174d4487f336` |
| `.../telemetry-post-audit/test.ps1` | `a07dfdaf22b1112a68ecdde2fa92a94644b6167303995d9a446975272a6f9f86` |
| `.../telemetry-post-audit/validate-schemas.py` | `9920cced0166e2cfc57062cd5ba0c7db30d1356f3f3615f815544b5693986663` |
| `.../telemetry-post-audit/verify-post-audit-telemetry.ps1` | `e5a80fe2328521f86153786bc6b18e8ffc9a281e4ec63bdf48c691ad783710c2` |
| `.../telemetry-post-audit/cases/positive-attempt-1/audit-barrier.json` | `ce52a0e94665a00a62e9ac7aae35e6cadac5ae3e0f691864aa0903f86b8efb6e` |
| `.../telemetry-post-audit/cases/positive-attempt-1/sigil-invocations.jsonl` | `18726ae732ee0778140a1a6d9875e3777802a7b2fc7841ddd8a825bc9550a0e4` |
| `.../telemetry-post-audit/cases/positive-attempt-2/audit-barrier.json` | `d8e5bad153818d0dada037a43792ea56801d963e12151e99b54aef3f711eec1e` |
| `.../telemetry-post-audit/cases/positive-attempt-2/sigil-invocations.jsonl` | `f28b48accdcecc1a3f8bac235160c4623eb5f76e7fcfe6ef88a34b6eb4773187` |
| `.../telemetry-post-audit/schemas/audit-barrier.schema.json` | `ef049ea6fbbe9680d69f65dbabf3fbab7f50fcbc5b05202beef2cde48cbb5e9e` |
| `.../telemetry-post-audit/schemas/post-audit-check.schema.json` | `388fb41f2311a83613bc0425f33ed715aac0373678f5bfa611655861daf60fc5` |
| `.../telemetry-post-audit/schemas/telemetry-events.schema.json` | `d9d4f9af724dab490a1aa5cb825a17cb83d2d4620c4d5e174df9f631e546ba53` |

Here and below, `.../telemetry-post-audit/` expands to the full R2 directory shown in the first row.
The exact-run digest must use expanded literal paths, not the abbreviation.

## Agents, prompts, ordering, and writes

The host/main only orchestrates and writes host-owned integrity/completion artifacts. It performs no
semantic extraction, selection, repair, or approval.

1. `extractor-writer`, `writer_attempt=1`: sole semantic mutator. Its immutable prompt is exactly
   `04-execution-sheet.md` § “Extractor-writer”, with only declared placeholders materialized and
   `ACI-WORKFLOW-BINDING-V1:<base64>` as the first line.
2. `coverage-auditor`, `audit_attempt=1`, consuming writer attempt 1: independent and read-only
   except for its exact attempt-specific audit report. Its immutable prompt is exactly
   `04-execution-sheet.md` § “Coverage-auditor”, with the same binding rule.
3. Only after `BOUNDED_CORRECTIONS`: the same writer identity may run `writer_attempt=2`, correcting
   only defects in the bound audit; then the same auditor identity may run `audit_attempt=2`. There
   is no third writer attempt.
4. The host runs the read-only R2 verifier after terminal audit and may write only its exact
   attempt-specific check artifact.

The exact-run confirmation must still freeze: `<run-id>`; concrete seat identities; model for each
seat; allowed tools; token/time budgets; `writer_attempt`/`audit_attempt`; rendered prompt bytes and
SHA-256; resolved run/audit paths; correction cap `1`; and host binding/barrier/close behavior.
Until these are filled, status remains `BLOCK/CONFIRMATION_MISSING_OR_DRIFTED`.

### Inventory and projection writes

The writer may create exactly:

- `.arcanum/inventory/raw/d1-lens-use-corpus.manifest.json`;
- `.arcanum/inventory/entries/d1-lens-use/occurrence-cards.json`;
- `.arcanum/inventory/entries/d1-lens-use/control-cards.json`;
- `.arcanum/inventory/entries/d1-lens-use/residue.md`;
- `internal-tools/composition-lab/research/milestone-1/01-repository-inventory/research.md`;
- `internal-tools/composition-lab/research/milestone-1/01-repository-inventory/findings.md`.

The writer may alter exactly these existing Inventory surfaces:

- `.arcanum/inventory/index.md`;
- `.arcanum/inventory/index.json`;
- `.arcanum/inventory/tags.md`;
- `.arcanum/inventory/log.md` (append-only).

It may not create `.arcanum/inventory/lint/d1-lens-use-validation.md`; validation belongs to the
auditor. `research-initial-definitions.md` remains pre-existing, read-only, and byte-identical.

### Host/auditor run artifacts

- `runs/<run-id>/confirmed-corpus-manifest.json` (host, before writer);
- `runs/<run-id>/barrier-writer-attempt-<writer_attempt>.json` (host);
- `runs/<run-id>/audit-attempt-<audit_attempt>.md` (auditor);
- `runs/<run-id>/barrier-audit-attempt-<audit_attempt>.json` (host);
- `runs/<run-id>/post-audit-telemetry-check-<audit_attempt>.json` (host verifier, atomic
  create-new/no overwrite);
- `runs/<run-id>/completion.json` (host factual completion only).

No bridge stdout may be persisted in the run folder; the journal already owns it.

## Exact observability write

The sole permitted observability surface is append-only
`.arcanum/observability/signals/sigil-invocations.jsonl`. No observability index is rebuilt.

The runtime appends exactly one matching pre-audit event per writer attempt, schema version
`1.0.0`, kind `inventory-bootstrap-pre-audit`, with RFC3339 UTC `Z` time, `run_id`,
`sheet_producer_attempt=3`, typed `writer_attempt`, mode `backfill-validate-lint`, `source_count`,
created/updated entry counts, contradictions, lint gaps, validation, downstream lookup count, filed
synthesis count, corpus digest, and profile version.

After the auditor terminates, the runtime appends exactly one terminal event, kind
`inventory-bootstrap-terminal`, with RFC3339 UTC `Z` time, `run_id`,
`sheet_producer_attempt=3`, typed `audit_attempt`, `consumed_writer_attempt`, auditor verdict,
correction count, exit reason, and exact audit artifact `{path, sha256, size}`. The R2 verifier reads
one captured-byte snapshot of the barrier and exact JSONL, requires unique matching events in JSONL
line order, rejects divergent attempts, and writes the exact post-audit check. Missing or ambiguous
telemetry yields `BLOCK/OBSERVABILITY_GAP`; it never triggers content rewriting and is not Inventory
partial-state recovery.

Telemetry is local ignored read-model evidence. It is not ACI/ledger evidence, authority,
epistemic validity, lifecycle close, or proof of a compositional effect.

## Validations and fail-closed conditions

Before any mutation:

- reuse and owner/design choices below are affirmative and recorded;
- canonical Inventory ownership/generated-surface conformance and first-line host binding are
  independently established;
- HEAD, the semantic sheet, external row source, 22 sources, controls, selectors, exact paths,
  fixture files, seat identities, prompts, models/tools/budgets, observability, recovery, and close
  semantics match the confirmed digest;
- the host manifest passes R1 canonical-path/bytes/schema/reconstruction checks and its Inventory
  projection is deterministic and field-equivalent;
- every resolved write target equals the literal allowlist and unexpected pre-existing targets,
  reparse/path escapes, copied sources, dynamic paths, or extra observability writes fail closed;
- required lifecycle, artifact-fit, authority-negative, conflict-preservation, recovery, retirement,
  R1–R4, and final `/review` evidence has no unresolved material finding; and
- a human separately authorizes launch after those antecedents.

After each writer attempt, the independent auditor checks:

- all 22 source hashes and `research-initial-definitions.md` are unchanged;
- all 176 obligations resolve to a cited candidate observation,
  `not_observed_within_selector`, or typed unresolved gap;
- evidence-card schema/enums, selectors, IDs, trace, residue, duplicate and contradiction links;
- exact host-manifest → Inventory-projection equivalence;
- `index.md`/`index.json` agreement, tags, append-only log, and projection-to-card linkage;
- separate preservation of conflicting assignments without normalization or majority vote;
- no undeclared writes or authority escape; and
- pre-audit telemetry linkage. Terminal telemetry is checked afterward by the host R2 verifier.

Any drift, invalid barrier, early launch, partial write, index/log divergence, source mutation,
authority escape, observability gap, missing artifact, or correction beyond the cap blocks. A
mechanical PASS establishes only structure, coverage, provenance, immutability, and boundary
compliance—not truth, causality, novelty, ontology, or effectiveness.

## No atomic rollback; recovery is not retirement

There is no demonstrated multi-file transaction, filesystem atomicity, or automatic rollback.
Pre-write hashes/snapshots and ordering only support detection. A torn or partial writer attempt
terminates `BLOCK/PARTIAL_STATE_REQUIRES_HUMAN_RECOVERY` and is excluded from the normal correction
loop. No retry occurs until a separately authorized recovery owner restores or repairs the exact
write set from recorded pre-write state and an independent audit verifies it.

Later retirement is a separate, separately confirmed Inventory operation. It marks D1 cards and
index rows `superseded` with a non-`none` owner, appends a tombstone with reason, IDs, last hashes,
replacement, and consumers, and preserves resolvable history. It removes no source, governed
artifact, milestone projection, or unrelated entry. Active undeclared consumers or governed
references block retirement. Retirement maintains/reverses a read model; it does not recover a
torn attempt.

## Authority expressly excluded

This confirmation does not authorize:

- editing or synchronizing canonical/generated Inventory skills, stale runtime metadata, or
  `.codex` regeneration ownership;
- LIVE registration, registry/dispatch-schema changes, ledger rows, a new lifecycle, ACI
  connections, or accepted-output receipts;
- a second Inventory root/schema/index/log/raw store/ID namespace/synchronization loop;
- definition of lens/composition, ontology or definitions promotion, novelty/soundness judgment,
  causal-effect validation, or GO/KILL recommendation;
- dynamic corpus expansion, source edits/copies, connected extractor/assembler behavior;
- deletion-based rollback or deletion of sources, governed artifacts, milestone projections, or
  unrelated Inventory entries; or
- treating a fixture PASS, Inventory validation, telemetry event, capability completion, or this
  signature as evidence stronger than its stated boundary.

## Human choices required

Record one choice for every item. A blank or qualified choice is `BLOCK` until converted into an
exact revised proposal.

### A. Reuse existing Inventory

1. Must the corpus be backfilled or revalidated after source changes? **YES / NO**
   - Concrete event if YES: `________________________________`
2. Must later milestone work retrieve occurrences by source, control, state, or evidence level
   without reparsing the corpus? **YES / NO**
   - Concrete consumer if YES: `________________________________`
3. Must downstream work cite stable source-linked records while preserving trace and residue?
   **YES / NO**
   - Concrete consumer if YES: `________________________________`

Decision: **REUSE EXISTING INVENTORY / STOP — INVENTORY_LIFECYCLE_UNWARRANTED**

At least one `YES` with a named consumer/event is required to reuse Inventory. Three `NO` answers
plus confirmation that a one-shot cited snapshot satisfies D1 require stopping this route.

### B. Owner/design decision

Decision: **GO / NO-GO / REVISE** for the bounded, unregistered, owner-directed,
connectionless Inventory bootstrap described here.

By choosing GO, the human explicitly accepts the sole-root policy; descriptive/non-authority
boundary; first-ingest precedent; candidate extension profile; the meanings of `research.md` and
`findings.md`; exact ownership/write split; no registered dispatch or ledger close; local ignored
telemetry; correction cap; and the disclosed lack of atomic rollback. GO does not authorize launch.

Canonical Inventory owner/ratifier: `________________________________`

### C. Exact-run effects and launch

Decision: **CONFIRM EXACT RUN / REVISE / BLOCK**

Before `CONFIRM EXACT RUN`, attach/fill: current commit; fresh corpus/sheet/fixture hashes; exact
`<run-id>`; manifest and run-root paths; seat identities; models; tools; budgets; rendered prompt
digests; typed attempts; output allowlist; telemetry retention/failure policy; recovery owner and
snapshot procedure; declared downstream consumers; maintenance/retirement owner; completion/close
semantics; and one digest binding the whole run.

Exact-run digest: `________________________________`

Recovery owner: `________________________________`

Maintenance/retirement owner: `________________________________`

Separate launch decision after all validations and final `/review`: **AUTHORIZE D1 LAUNCH / DO NOT
LAUNCH**

Human name/identity: `________________________________`

Recorded at (RFC3339): `________________________________`

Notes or required revision: `________________________________`
