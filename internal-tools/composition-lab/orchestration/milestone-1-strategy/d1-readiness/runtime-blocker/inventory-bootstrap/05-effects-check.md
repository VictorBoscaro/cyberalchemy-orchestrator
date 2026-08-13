---
artifact_kind: bounded-inventory-bootstrap-effects-check
status: inspected-blocked-for-execution
date: 2026-08-13
scope: material-effects-before-D1-inventory-bootstrap
inspection_only: true
reviewed:
  - 02-bootstrap-design.md
  - 03-bootstrap-adversary.md
  - .arcanum/inventory/
---

# Effects check for the bounded D1 Inventory bootstrap

## Disposition

**The design can adapt the installed Inventory without creating a second system, but execution
remains BLOCK.** The installed package is structurally ready and empty; all proposed D1 target paths
and IDs are presently free. That absence of collisions does not make the run inert. It would be the
first ingest/backfill, establish repository precedent for D1 IDs and profile fields, update the
repository-wide catalogs and append-only operation record, create two milestone projections, and
emit local runtime evidence.

The human must confirm those effects, the reuse purpose, artifact mapping, exact mutation set,
observability behavior, and later retirement semantics. T1-T16, owner/stale-surface recovery,
fixtures, independent reviews, and the final launch gate remain antecedent blockers.

## Exact current state

| Surface | Inspected state | Consequence |
|---|---|---|
| `.arcanum/inventory/` | Installed, tracked, and the sole declared Inventory root. | Adapt this package; do not install another. |
| Package directories | `entries/`, `indexes/`, `lint/`, `queries/`, `raw/`, and `wiki/` contain only `.gitkeep`. | Proposed D1 paths do not collide with existing Inventory artifacts. |
| `index.json` | Parses as `inventory.index.v0.1`; `inventory_root` is `.arcanum/inventory`; `entries` and all lookup maps are empty; `validation_boundary` is `inventory-read-model-only`; source coverage is `unknown`. | D1 would create the first indexed records. Existing root, schema version, index families, and validation boundary must not change. |
| `index.md` | No pages; explicitly requires synchronization with `index.json`; documents card and EvidenceSet lookup families. | Human and machine catalogs must represent the same D1 artifacts. |
| `log.md` | One install entry; explicitly append-only. No ingest has occurred and no first target was chosen. | Bootstrap must append a conforming operation entry and cannot rewrite install history. |
| `schema.md` | Fixes root, in-place source references, frontmatter for generated pages, ID conventions, machine-index fields, authority boundary, and log heading pattern. | D1 extensions may remain additional candidate fields, but may not create a competing schema authority. |
| `tags.md` | Does not yet register `composition-lab` or `d1-lens-use`. | Both proposed reusable tags collide with the tag-governance rule unless added in the same confirmed update. |
| Proposed Inventory targets | `raw/d1-lens-use-corpus.manifest.json`, `entries/d1-lens-use/`, and `lint/d1-lens-use-validation.md` do not exist. | No path overwrite is currently required. Recheck immediately before a confirmed run. |
| Composition Lab target | `research-initial-definitions.md` exists; `research.md` and `findings.md` do not. The directory is currently untracked. | Preserve the existing file. New files are milestone projections, not a second Inventory package or Research verdict surface. |
| Observability | `.arcanum/observability/` exists. Its source is `signals/sigil-invocations.jsonl`, which is local/ignored; indexes are rebuildable. | Signal emission is required by the selected Inventory convention but produces local read-model evidence, not tracked dispatch or authority evidence. |
| Worktree | No diff was observed under `.arcanum/inventory/`; the bootstrap design directory and milestone inventory directory are untracked. | Existing tracked Inventory files are clean at inspection time. This is not a future-run precondition; hashes/status must be rechecked at launch. |

## Adaptation map: one system only

The following existing files can be adapted without creating a competing system:

| Existing owner | Permitted D1 adaptation | Forbidden parallel surface |
|---|---|---|
| `.arcanum/inventory/schema.md` | Reference its current conventions and canonical evidence-card envelope. Do not amend it merely to encode D1 vocabulary. | A Composition Lab D1 schema presented as Inventory authority. |
| `.arcanum/inventory/index.json` | Add stable rows and maintain `by_*` maps for the manifest, bundles, lint report, and two projections. | Another machine index under Composition Lab or a D1-only ID registry. |
| `.arcanum/inventory/index.md` | Add the corresponding human-readable entries and remove/update the empty-state gap truthfully. | A second Inventory catalog masquerading as `findings.md`. |
| `.arcanum/inventory/log.md` | Append one conforming operation record per meaningful operation. | A parallel Inventory operation log or rewritten history. |
| `.arcanum/inventory/tags.md` | Register the two D1 tags before repeated use. | Undeclared local tag vocabulary embedded only in cards. |
| `.arcanum/inventory/raw/` | Store only the frozen manifest; reference tracked sources in place. | Copies of tracked corpus files. |
| `.arcanum/inventory/entries/` | Store the candidate card bundles under the proposed D1 directory. | Canonical definitions, ontology claims, or duplicate source evidence stores. |
| `.arcanum/inventory/lint/` | Store the mechanical validation report. | An epistemic validation or Research verdict. |
| Composition Lab milestone tree | Preserve `research-initial-definitions.md`; create only the accepted `research.md` trace and `findings.md` non-authority projection, each traced to Inventory card IDs. | `index.json`, Inventory schema/log/raw store, duplicate cards, or autonomous synchronization loop. |

## Source immutability and write isolation

The design is consistent with the installed source policy only if the exact source set is frozen as
repo-relative paths with commit, SHA-256, selectors, and source x control obligations. Tracked
sources remain in place and are never copied into `raw/`. Each writer attempt and the independent
auditor must recompute source hashes; a mismatch is `BLOCK/source-drift`, not an invitation to
refresh the corpus dynamically.

The exact allowlist is material. It comprises the named D1 manifest, bundles, lint report, existing
Inventory indexes/tags/log, the two approved Composition Lab projections, the capability-local
completion record, and configured local observability output. Resolved absolute targets must be
checked before mutation. Any copied source, undeclared file, target escape, or post-confirmation path
change must fail closed and invalidate confirmation.

## Index, log, and schema constraints

- `index.json` remains the primary machine catalog and must parse against
  `inventory.index.v0.1`. D1 rows need stable IDs, paths, kinds, types, summaries, tags, source
  selectors, dates, candidate status, confidence, card IDs, and residue.
- `index.md` and `index.json` must agree. The manifest, occurrence/control bundles, lint report,
  `research.md`, and `findings.md` require deliberate row/page treatment; neither index may infer
  completeness from its own derived counts.
- The source x control manifest is the external denominator. Every cell ends in a cited candidate
  observation, selector-bounded non-observation, or unresolved gap.
- `log.md` is append-only and its heading must match
  `## [YYYY-MM-DD] <mode> | <short title>`. A correction and a later retirement are meaningful
  operations and need their own truthful append entries.
- The evidence-card schema permits additional properties, so `d1_observation` can be represented
  without changing the canonical schema. Schema permissiveness is not semantic ratification.
  Assignments remain candidate/inference/open; `source-asserted-effect` records only a literal
  source assertion and supplies no causal evidence.
- Terminal `superseded` status requires a non-`none` promotion owner. Retirement fixtures must
  prove their exact owner/status representation before launch.
- `composition-lab` and `d1-lens-use` must be added to `tags.md` if used repeatedly. An undeclared
  tag is a validation failure under the installed convention.
- A partial bundle/index/tag/log/projection update is a validation failure. The design specifies
  coordinated consistency but does not demonstrate filesystem transactionality. The execution
  sheet must name pre-write snapshots/hashes, write ordering, detection of partial state, and the
  bounded recovery procedure; it must not claim atomic rollback without a fixture.

## Artifact barrier and workflow effects

The connectionless writer-then-auditor topology is viable only as a bounded owner-directed helper
workflow, not as evidence of a new registered dispatch type or connected runtime. The main agent
only orchestrates. The single writer is the sole mutator; the auditor is read-only and starts only
after the writer is terminal and every predeclared artifact is supplied as
`{path, sha256, size, producer_attempt}`.

Changed bytes, wrong path, wrong attempt, absent output, early audit, parent-summarized prose, an
unbound seat, or inability to preserve attempt identity must BLOCK. If independent extractor
returns or an assembler become necessary, the correct result is
`inventory-connected-topology-required`, not informal parent mediation.

The workflow completion report is capability-local evidence. It is not an ACI accepted-output
receipt, ledger projection, registered lifecycle, or proof of durable handoff. Bridge stdout remains
in the journal and must not be copied into the working folder.

## Observability effects

Because observability is installed and enabled by the Inventory install decision, a run emits mode,
source count, entries created/updated, contradictions, lint gaps, validation result, downstream
lookups, and filed synthesis count, plus bounded D1 dimensions for corpus digest, profile version,
writer attempt, auditor verdict, correction count, and exit reason.

These signals are material local writes. The current source-of-truth JSONL is ignored by git, so
the execution sheet must state retention, failure behavior, and how the auditor resolves the emitted
signal back to the run. Signal success cannot prove lens effect, epistemic correctness, lifecycle
close, or authority promotion; signal failure cannot be hidden behind a successful content check.

## Rollback versus retirement

Two different mechanisms must not be conflated:

1. **Failed-attempt recovery:** the design has no demonstrated transactional rollback. A partial
   update is BLOCK and requires an explicit, bounded recovery from recorded pre-write hashes or
   snapshots before retry. The one-correction cap does not itself make files atomic.
2. **Later retirement:** a separately approved Inventory operation marks D1 cards and index rows
   `superseded`, appends a tombstone with reason, IDs, hashes, replacement, and unresolved
   consumers, and preserves resolvable history. It removes no source, governed artifact, milestone
   projection, or unrelated Inventory entry and blocks when undeclared active consumers or governed
   references exist.

Retirement is therefore reversible maintenance of a read model, not erasure and not recovery from
a torn write.

## Material effects requiring explicit human confirmation

The human must separately confirm:

1. **Reuse:** at least one concrete downstream lookup consumer or revalidation event; otherwise
   stop with `inventory-lifecycle-unwarranted`.
2. **Artifact contract:** `research.md` becomes an extraction/session trace and `findings.md` a
   non-authority projection rather than Research-agent outputs.
3. **First-ingest precedent:** D1 becomes the first maintained Inventory corpus, fixes stable IDs,
   adopts the candidate extension profile, and changes the repository-wide empty-state indexes.
4. **Exact corpus and controls:** paths, commits, hashes, selectors, obligations, and denominator.
5. **Exact mutation boundary:** every Inventory, Composition Lab, completion, and observability
   target, including tag registration and correction behavior.
6. **Workflow identity:** two bound seats, immutable prompts, models/tools/budgets, ordering,
   artifact barrier, correction cap, terminal states, and close limitations.
7. **Local telemetry:** fields, local ignored storage, retention, audit linkage, and failure policy.
8. **Recovery and retirement:** pre-write recovery for partial failure and the later
   supersede/tombstone protocol, including declared consumers and maintenance owner.
9. **Launch:** explicit D1 authorization only after T1-T16, R1-R4, fixtures, stale-surface recovery,
   and final `/review` clear their blockers.

Earlier milestone-wide authorization to use agents does not confirm any of these material effects.

## Effects expressly excluded

This bootstrap does not authorize or achieve:

- mutation or synchronization of canonical/generated Inventory skills;
- correction of stale runtime metadata or `.codex` regeneration ownership;
- LIVE registration, dispatch-schema changes, ledger rows, or a new lifecycle type;
- a second Inventory root, schema, index, log, raw store, ID namespace, or sync loop;
- definition of lens/composition, ontology promotion, canonical definition, novelty or soundness
  judgment, causal-effect validation, or GO/KILL recommendation;
- dynamic corpus growth, source edits, or tracked-source copies;
- connected extractor/assembler behavior; or
- deletion-based rollback or removal of milestone/governed artifacts.

## Fail-closed recommendation

Use the execution sheet only to present an exact, hashable proposal and fixtures for confirmation.
Do not treat it as launch authority. Any unresolved T1-T16 item, stale surface, missing human gate,
unproven first-line binding, failed artifact barrier, source drift, index/log divergence, partial
write, telemetry gap, active retirement consumer, or authority escape keeps the bootstrap and D1
launch **BLOCK**.
