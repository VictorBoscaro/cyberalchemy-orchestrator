---
artifact_kind: bounded-inventory-bootstrap-adversarial-review
status: block-pending-design-proof
date: 2026-08-13
scope: D1 bounded Inventory-owned bootstrap proposal
reviewed:
  - ../10-final-route-decision.md
  - ../11-inventory-governance.md
  - ../../../../../../../.codex/skills/inventory/SKILL.md
---

# Adversarial review of the bounded Inventory bootstrap

## Verdict

**BLOCK as an executable route.** A proposal may be drafted, but neither D1 launch nor canonical
Inventory mutation is justified yet.

The semantic ownership argument is credible: Inventory is a better owner than Research for durable,
source-backed descriptive records. The operational conclusion does not follow from it. The proposed
extractor -> assembler -> auditor bootstrap is still a dependent multi-seat dispatch. Calling it
"bounded" and "unregistered" does not supply governed confirmation, seat binding, handoffs,
observation, terminal state, or close. The repository has already established that the active
runtime cannot materialize non-empty connections for D1. Unless a dry run proves an honest common
lifecycle representation, the bootstrap is a dispatch-shaped exception outside governance.

There are also two antecedent blockers. The generated Inventory skill declares
`arcana/inventory/SKILL.md` as canonical, but that source is absent. And the repository already has
an installed `.arcanum/inventory/` package whose schema fixes that root. A second D1-specific
Inventory root under `composition-lab`, or a parallel index there, would be the competing system the
Inventory quality bar forbids.

## Unsupported transitions in 10/11

1. **Semantic owner -> executable owner.** `ingest` and `backfill` define inline knowledge
   operations, not a delegated lifecycle. Tool permission for `Agent` is not a lifecycle contract.
2. **Unregistered -> harmless.** An unregistered multi-seat run has less representational support,
   not less need for binding and close. If no existing dispatch identity honestly describes it,
   absence of registration is a blocker rather than an exemption.
3. **Existing package -> adaptable local package.** `.arcanum/inventory/README.md` and `schema.md`
   already declare the repository Inventory root, index, log, ID conventions, and authority
   boundary. "Select a composition-lab-compatible root" conflicts with that installed convention
   unless it means ordinary source/output artifacts indexed by the one existing package.
4. **Durable usefulness -> passed reuse gate.** No separate acceptance note or human answer to the
   three closed reuse questions was found. The decision itself says that gate precedes bootstrap
   drafting.
5. **Descriptive fields -> non-interpretive extraction.** Occurrence identity, deduplication,
   `prescribed/instantiated/executed/effect-observed`, explicit absence, evidence level, and
   contradiction are classifications. Inventory may preserve them as candidates, but cannot treat
   them as neutral facts or resolve disagreement by assembler preference.
6. **Inventory-native outputs -> Milestone acceptance.** The confirmed program and prepared D1
   sheet name `research.md` and `findings.md` in Composition Lab. Replacing these with evidence-cards,
   indexes, tags, and a log is a material contract change still marked
   `decided-awaiting-human-ratification`; it cannot be inferred from route ownership.

## Hard blockers

### B1 - Canonical authority is unavailable

`arcana/inventory/SKILL.md` does not exist in this checkout. Generated `.codex`, `.agents`, or
`.claude` surfaces have `mutation_policy: regenerate-from-canonical-source`. No bootstrap contract
may be added or treated as capability-owned until the canonical source is restored or its declared
authority is formally corrected and regeneration provenance is demonstrated.

**Stop condition:** any design instructing edits to a generated copy, or inventing a local D1
contract that supersedes the absent canonical owner.

### B2 - No honest governed runtime path is demonstrated

The desired topology has dependent returns and a sole writer. The previously diagnosed compiler
cannot materialize connections. A connectionless launch loses the very provenance and dependency
semantics D1 must study. A parent manually copying child returns simulates a lifecycle but provides
no dispatch-level handoff, binding, observation, or close evidence.

**Stop condition:** the design uses informal parent orchestration, borrows `research`, fabricates an
`others` type, calls bridge receipts workflow evidence, or claims common-lifecycle compatibility
without an executable dry run.

### B3 - Human gates are unsatisfied

The reuse gate, changed output contract, complete seats/prompts/budgets/topology, mutation boundary,
and exact execution record all require explicit human ratification. The user's milestone-wide
authorization to dispatch agents is not evidence of acceptance of a newly invented capability
lifecycle or replacement outputs.

**Stop condition:** proposal, ratification, mutation, or launch occurs in one act; material changes
are covered by presumed earlier consent.

### B4 - Competing Inventory surface risk

The installed repository package is `.arcanum/inventory/`. Its schema says every generated bundle
has a row in its `index.json`, and its log says other repository surfaces remain independent sources.
A second root/index in `internal-tools/composition-lab/` duplicates IDs, freshness, validation, and
maintenance authority. Conversely, putting all Milestone artifacts inside `.arcanum/inventory/`
breaks the accepted Composition Lab artifact tree.

**Required resolution:** use exactly one repository Inventory package for Inventory-owned read
models, while keeping Composition Lab's research/session artifacts at their accepted paths and
indexing them by reference. If that split cannot satisfy the D1 acceptance contract, stop for a
human output-contract decision.

### B5 - Schema precedes warranted vocabulary

D1 exists to observe boundaries among lens, concern, angle, role, prompt, occurrence, and effect.
A custom occurrence/control schema can silently decide those boundaries before evidence. In
particular, `effect-observed` is unsafe unless it means only "the source literally asserts an
effect"; it must not certify effect, relation, or causality. "Explicit absence" must mean absence
within a named selector/search obligation, not absence in the world or repository.

**Stop condition:** controlled vocabulary is presented as canonical, mandatory fields force an
interpretation unsupported by a source, or index validation is treated as epistemic validation.

### B6 - Ingest/backfill scope is not yet legitimate

Inventory `ingest` presumes a resolved source set, confirms raw immutability, and updates the
repository-wide indexes and log. `backfill` creates maintained entries from existing artifacts.
Neither mode is a neutral synonym for one-shot extraction. Before using either, D1 must name the
maintenance event and downstream lookup consumer that make durable backfill necessary. Otherwise
the reuse collapse-test says Inventory is over-classification.

## Minimum tests a viable design must pass

| ID | Test | Passing evidence |
|---|---|---|
| T1 | Canonical-owner test | Restored canonical source, verified authority history, generator command, and byte-equivalent generated surfaces. |
| T2 | Reuse falsifier | Separate human-ratified note answers the three closed reuse questions; at least one yes names a concrete consumer or revalidation event. All no yields `inventory-lifecycle-unwarranted`. |
| T3 | Single-system test | Design names `.arcanum/inventory/` as the sole Inventory index/log/schema owner; no second `index.json`, ID namespace, or sync loop is created in Composition Lab. |
| T4 | Artifact-fit test | Explicit human-approved mapping preserves all eight Milestone-1 deliverables and identifies which Composition Lab artifacts are session evidence versus Inventory read models. No fake Research matrix remains. |
| T5 | Governed-lifecycle dry run | One extractor, one assembler, and one auditor execute with real first-line seat bindings, immutable prompts, captured returns, typed handoffs, observation, terminal verdict, and bridge/ledger close through an existing honest representation. |
| T6 | Connection integrity | Removing connections causes the fixture to fail. The passing fixture proves the assembler consumed the bound extractor return and the auditor consumed the exact assembled hash, not parent-supplied prose. |
| T7 | Confirmation test | Exact sources/digests, targets, seats, prompts, budgets, topology, outputs, retry ceiling, mutation root, and close semantics are presented together; any material delta fails closed pending reconfirmation. |
| T8 | Source immutability | Before/after hashes for every frozen source match; writes outside the single confirmed Inventory root and accepted Composition Lab output paths fail. In-repo sources are referenced, never copied into `raw/`. |
| T9 | Minimal-schema challenge | Fixtures cover occurrence, selector-bounded not-observed, ambiguity, contradiction, duplicate representations, and schema residue without requiring a lens definition. An independent reviewer can mark every interpretive field candidate/inference/open-question. |
| T10 | Authority-escape negatives | Definition, causal effect, novelty, soundness, ontology promotion, and GO/KILL inputs produce `BLOCK` or typed handoff; they never enter indexes as validated conclusions. |
| T11 | Denominator/completeness | A frozen source x control manifest exists outside derived counts. Every cell has cited observation, selector-bounded not-observed, or unresolved gap. Index completeness is checked against this denominator, not against itself. |
| T12 | Mechanical validation | `index.json` parses and matches `index.md`; IDs and source refs resolve; log/index update atomically; validation boundary says read-model-only. Mechanical PASS never implies the observed category is true. |
| T13 | Observability | Existing observability receives mode, source count, created/updated entries, contradictions, lint gaps, validation, and lookup consumers. Workflow receipts remain only in the journal and are not copied into the working folder. |
| T14 | Conflict preservation | Two extractors assigning different states remain two traced candidate assignments plus residue. Assembler cannot majority-vote, normalize, or silently choose. |
| T15 | Reversibility | Removal fixture deletes no source or governed artifact, leaves no consumer depending on a D1-only schema, and can retire generated entries/index rows with a logged tombstone or equivalent documented operation. |
| T16 | No-launch review | Independent contract, epistemic, and infrastructure reviews all clear their blockers, followed by final `/review` and explicit human launch ratification. |

## Design constraints that survive the attack

A defensible proposal is narrower than 10/11 currently imply:

- it may specify an Inventory-owned **candidate read-model profile** for D1;
- it must reuse the installed `.arcanum/inventory/` package rather than install another;
- it must keep original session/raw extraction evidence in Composition Lab and reference it;
- it must regard all D1 categories as provisional assignments with trace and residue;
- it may not become executable until canonical ownership and connected governed runtime are proven;
- if the runtime cannot represent the topology honestly, the result is `BLOCK`, not a local
  bootstrap workaround.

## Disposition

Proceed only with a design document tested against T1-T16. Current evidence supports
**Inventory semantic ownership**, but not **Inventory dispatch executability**. The earliest valid
next claim is "proposal ready for review," not "bounded bootstrap ready" and not "D1 ready to
launch."
