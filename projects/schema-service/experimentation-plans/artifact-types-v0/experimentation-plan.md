---
artifact_kind: document
classification_label: experimentation-plan
classification_authority: descriptive-only
schema_service_status: unregistered-bootstrap
status: active
version: 0.1.0
created_at: 2026-08-18
---

# Experimentation plan — artifact types v0

## Authority notice

`experimentation-plan` is used here as a descriptive classification. It is not a published Schema
Service type, it confers no validation or behavioral authority, and this file is not a registry
entry. This follows the bootstrap distinction between a descriptive label, a candidate definition,
an authorized publication and active enforcement.

## Objective

Determine whether the Schema Service's proposed kernel is useful across progressively harder
artifact families without first building a universal runtime or registry. The program will preserve
the distinction among semantic type, immutable schema revision, durable artifact, manifest revision,
representation, representation snapshot and validation report.

## Why three sequential experiments

| order | experiment | pressure introduced | start gate |
| --- | --- | --- | --- |
| 1 | `analysis` | A document-like artifact with meaningful subtypes, reclassification and content change. | Experimental staging rule recorded; initial definitions complete. |
| 2 | skill | A compound artifact graph: definition, source package, release, installation, tool, invocation and receipt. | Experiment 1 identifies a useful kernel and does not require collapsing those roles. |
| 3 | folder | A conditional boundary: distinguish artifact from representation or container. | Experiment 2 demonstrates that compound containment and independent identity can be kept separate. |

The sequence is a learning dependency, not a commitment to execute all three. A falsified or invalid
experiment can redirect the next step.

## Rule for unregistered types

There are two distinct cases:

1. **A label is merely being used.** Record it as a descriptive classification, as this plan does.
   It remains non-normative and does not require a candidate schema.
2. **A reusable contract is deliberately under test.** Store its candidate definitions inside the
   owning experiment under `candidate-types/`, use experiment-only references and forbid normative
   resolution.

For the second case, the provisional rule is:

- path provides custody only, never identity or authority;
- `schema` remains reserved for an authorized published `SchemaId`;
- fixtures use `experimental_schema_ref` containing `experiment_ref`, exact candidate revision and
  definition digest;
- normative and experimental resolution are separate capabilities with no fallback between them;
- candidate revision, proposed type identity and eventual published schema identity remain distinct;
- changes create new candidate revisions; prior runs keep their exact references and digests;
- only `active` candidates serve new runs; `superseded`, `abandoned` and `promoted` remain available
  only for exact replay and provenance;
- promotion is an authorized operation producing an explicit candidate-to-publication mapping; it
  never rewrites earlier runs;
- normative schemas cannot depend on candidates, and derived experimental outputs retain their
  experimental provenance.

Evidence and the collapse-test are recorded in
[`experimental-type-staging-rule/findings.md`](../../research/experimental-type-staging-rule/findings.md).

## Shared evidence contract

Each experiment must eventually preserve enough evidence to reconstruct this chain:

```text
candidate type + exact candidate revision
    -> artifact identity + manifest revision
        -> representation + observed snapshot
            -> validation report + validator identity
                -> change or reclassification
                    -> preserved earlier state
```

The artifacts required before a run are:

- `experiment-initial-definitions.md`, containing product context and known gaps but no frozen
  hypothesis or method;
- `experiment-manifest.yaml`, declaring owner, lifecycle and the experiment-local resolution root;
- `candidate-types/catalog.yaml` and immutable candidate definition files;
- a later `criterion.md`, pre-registered and frozen before fixtures are executed;
- fixtures and run artifacts added only under the frozen criterion;
- `experiment.md` and `findings.md` produced by the later run and adjudication.

## Experiment 1 — analysis

Working folder: [`experiments/01-analysis`](experiments/01-analysis/README.md).

The family begins with one root and four candidate refinements:

- `analysis/general`: structured reasoning or documentation not covered by a more specific subtype;
- `analysis/observed-phenomenon`: investigation starting from an observed change or anomaly, usually
  in one or more metrics;
- `analysis/observational-study`: study of patterns or relationships without controlled assignment;
- `analysis/ab-test-result`: analysis of an A/B experiment's outcome. The experiment itself remains
  a separate artifact referenced by the analysis.

The experiment must make the overlap between observed phenomenon and observational study visible,
not hide it in definitions. Reclassification must preserve the artifact identity and earlier
manifest revision.

The exact hypothesis, sample and verdict rule are intentionally absent until a governed
pre-registration produces `criterion.md`.

## Experiment 2 — skill

Working folder: [`experiments/02-skill`](experiments/02-skill/README.md).

This experiment is deferred. Its pressure case is the compound chain:

```text
SkillDefinitionRevision
    -> representedBy SkillSourcePackage
    -> releasedAs SkillPackageRevision
        -> installedAs InstalledSkill
            -> contains/uses ToolRevision
                -> invokedAs ToolInvocation
                    -> produces OperationReceipt
```

It must not begin until the document experiment shows which kernel roles are useful and which are
ceremony.

## Experiment 3 — folder

Working folder: [`experiments/03-folder`](experiments/03-folder/README.md).

This experiment is deferred. Its central boundary is conditional: a normal directory remains a
representation or container; it becomes an artifact only when evidence demonstrates an independent
owner, lifecycle and interface. Path alone cannot provide durable identity.

## Program decisions and stop conditions

- Do not implement a universal registry, resolver or ledger before Experiment 1 supplies evidence.
- Do not promote any candidate merely because a fixture validates against it.
- If a normative-only consumer accepts an experimental reference, stop: the staging rule failed.
- If the `analysis` criterion cannot discriminate its proposed subtypes, redesign or reduce the
  family before running.
- If the lifecycle roles cannot be traversed without invented identities or authority, record the
  typed negative rather than filling gaps with names.
- Start the next experiment only through an explicit plan revision after the preceding findings are
  accepted.

## Current state

| item | state |
| --- | --- |
| Experimental staging rule | Candidate rule researched and accepted for use in this plan. |
| Experiment 1 initial definitions | Created. |
| Experiment 1 candidate definitions | Created as experiment-local, non-normative revisions. |
| Experiment 1 criterion | Not authored; requires governed pre-registration. |
| Experiment 1 fixtures and run | Not started. |
| Experiments 2 and 3 | Deferred behind explicit gates. |

