---
artifact_kind: experiment-package-readme
status: preparing
experiment_ref: exp-schema-analysis-001
---

# Experiment 01 — analysis

This package prepares the first experiment in the
[`artifact-types-v0` experimentation plan](../../experimentation-plan.md).

## Current boundary

The package contains context, a local experiment manifest and candidate type definitions. It does
not yet contain a pre-registered criterion, fixtures, a run or a verdict. None of its candidate
definitions are registry entries or valid normative `schema` references.

## Contents

- [`experiment-initial-definitions.md`](experiment-initial-definitions.md): product meaning,
  confirmed constraints, evidence baseline and gaps.
- [`experiment-manifest.yaml`](experiment-manifest.yaml): custody, lifecycle and resolution mode.
- [`candidate-types/README.md`](candidate-types/README.md): local reference, resolution and
  lifecycle contract.
- [`candidate-types/catalog.yaml`](candidate-types/catalog.yaml): experiment-local catalog.
- `candidate-types/definitions/`: immutable candidate revision files.
- [`fixtures/README.md`](fixtures/README.md): freeze policy for later fixtures.
- [`runs/README.md`](runs/README.md): evidence required from later executions.

## Next governed action

Propose and validity-check `criterion.md` through an `experiment` dispatch. Only after the owner
freezes that criterion may concrete fixtures be executed.
