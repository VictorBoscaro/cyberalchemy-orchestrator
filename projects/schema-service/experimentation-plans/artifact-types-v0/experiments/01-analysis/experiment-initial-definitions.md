---
artifact_kind: experiment-initial-definitions
status: candidate
date: 2026-08-18
experiment_ref: exp-schema-analysis-001
---

# Analysis artifact type — initial definitions

## Context

Schema Service aims to keep repository artifacts identifiable, interpretable and governable while
allowing their semantic contracts to evolve. Before shared machinery is implemented, the proposed
roles need to be exercised against a small artifact family whose meaning is understandable to users
and whose representations can change without changing the underlying artifact.

Analyses are a useful first family because the system already produces documents that explain
observations, study relationships, evaluate experiments or preserve structured reasoning. Without a
clear but revisable distinction among these cases, people and agents cannot reliably find what a
document claims, which evidence it uses or whether a later reclassification changed its identity.

## Purpose

Establish the informational basis for later designing an experiment about the `analysis` family.
The result will inform whether the Schema Service's proposed lifecycle and the candidate subtype
distinctions are useful enough to justify further design.

## Experiment Question (Can be refined)

Can analyses with different epistemic roles be represented and evolved as governed artifacts while
preserving stable artifact identity, exact contract provenance and earlier classifications?

## Confirmed Product Constraints

- `analysis` is the root family considered by this experiment.
- Initial candidate refinements are `general`, `observed-phenomenon`, `observational-study` and
  `ab-test-result`.
- An A/B experiment and the analysis of its result are distinct artifacts; the analysis references
  the experiment.
- Observed-phenomenon analysis is commonly triggered by variation in relevant metrics, but metrics
  are not assumed to be its only possible evidence.
- Observed-phenomenon and observational-study may overlap; the system must preserve ambiguity or
  support reclassification rather than force a false distinction.
- Every analysis should be able to express its question or objective, scope, evidence, method,
  findings, conclusion and limitations.
- Type identity, exact schema revision, artifact identity, manifest revision and representation
  observation remain distinct roles.
- Path and content digest cannot be the enduring artifact identity.
- Candidate definitions are experiment-local and have no normative authority.
- Promotion, if later justified, must not reinterpret or mutate earlier experimental runs.

## Current Evidence Baseline

- The Schema Service README proposes a lifecycle from type and schema revision through manifest,
  representation snapshot and validation report, but states that the service is not implemented.
- The concrete-family research found partial document governance precedents but no complete
  operational witness, and recommended starting with one document package before the compound
  skill/tool/folder case.
- The staging-rule research concluded that candidate files may live with an experiment only when
  custody is separated from authority and normative consumers reject experimental references.
- Existing ontology conventions separate documentary role, maturity, format, confidence and
  relations, providing vocabulary precedents without proving this lifecycle.
- No accepted corpus currently establishes that the four proposed analysis refinements are
  mutually exclusive or collectively exhaustive.

## Known Gaps

- The durable serialization of `TypeId`, `SchemaId` and `ArtifactId` is not decided.
- No published fallback schema or operational Schema Service resolver is currently available for
  this package.
- The boundary between observed-phenomenon analysis and observational study is not settled.
- It is unknown whether `general` is a useful subtype or merely the fallback residue.
- The minimum required fields may differ among refinements and have not been validated against a
  corpus.
- The acquisition mode of each value — authored, inherited, observed, derived or generated — is
  not yet assigned.
- No criterion, sample, fixture, validator or enforcement profile has been selected.
- The evidence threshold and authority required to publish any surviving candidate remain open.