# Schema Service Craft Ledger

Source of truth: [`.craft/ledger.yml`](.craft/ledger.yml).

## Quick links

- Root context: [CTX-SCHEMA-SERVICE-ARTIFACT-TYPES-V0](#context-ctx-schema-service-artifact-types-v0).
- Blocking decisions: none.
- Active blockers: none.
- Active gaps: [candidate lifecycle](#gap-gap-schema-analysis-lifecycle-001), [base resolution](#gap-gap-schema-analysis-base-resolution-001), [revision immutability](#gap-gap-schema-analysis-immutability-001), and [successor-gate alignment](#gap-gap-schema-experiment-gate-alignment-001).
- Next move: correct the four confirmed review findings, then verify references and hashes before freezing `criterion.md`.

## Context and pending work

### <a id="context-ctx-schema-service-artifact-types-v0"></a>CTX-SCHEMA-SERVICE-ARTIFACT-TYPES-V0 — Schema Service Artifact Types v0

- Stage / gate: `review-audit` / `block`.
- Scope: test the artifact model first with `analysis`, then conditionally with `skill` and `folder`, before implementing a universal registry or runtime.
- Pending: four active blocking gaps; no blocker or decision rows.
- Next move: correct the four confirmed findings, then verify references and hashes before freezing `criterion.md`.

## Artifacts

### <a id="artifact-art-schema-artifact-types-plan"></a>ART-SCHEMA-ARTIFACT-TYPES-PLAN

- Status: `active`.
- [Experimentation plan](experimentation-plans/artifact-types-v0/experimentation-plan.md).

### <a id="artifact-art-schema-analysis-package"></a>ART-SCHEMA-ANALYSIS-PACKAGE

- Status: `flag`; criterion, fixtures, run, and verdict do not yet exist.
- [Analysis package](experimentation-plans/artifact-types-v0/experiments/01-analysis/README.md).

### <a id="artifact-art-schema-artifact-types-review"></a>ART-SCHEMA-ARTIFACT-TYPES-REVIEW

- Status: `flag`; the substantive review verdict is `FIX` with four major findings.
- [Review report](reviews/2026-08-20-artifacts-full-review/review.md).

### <a id="artifact-art-schema-artifact-types-session"></a>ART-SCHEMA-ARTIFACT-TYPES-SESSION

- Status: `pass`.
- [Session evidence](../../sessions/2026-08-25-0843-schema-service-artifact-experiments.md).

## Active gaps

### <a id="gap-gap-schema-analysis-lifecycle-001"></a>GAP-SCHEMA-ANALYSIS-LIFECYCLE-001

Candidate lifecycle is promised per candidate but represented only by one global catalog state. Evidence: [review finding F1](reviews/2026-08-20-artifacts-full-review/review.md#f1--candidate-lifecycle-is-promised-but-cannot-be-represented-per-candidate).

### <a id="gap-gap-schema-analysis-base-resolution-001"></a>GAP-SCHEMA-ANALYSIS-BASE-RESOLUTION-001

The unresolved `analysis@0` base leaves candidate resolution fail-closed even after criterion freeze. Evidence: [review finding F2](reviews/2026-08-20-artifacts-full-review/review.md#f2--the-stated-execution-gate-still-leaves-every-candidate-resolution-fail-closed).

### <a id="gap-gap-schema-analysis-immutability-001"></a>GAP-SCHEMA-ANALYSIS-IMMUTABILITY-001

Candidate revision immutability begins too late to preserve revision identity from catalog admission. Evidence: [review finding F3](reviews/2026-08-20-artifacts-full-review/review.md#f3--candidate-revision-immutability-begins-too-late).

### <a id="gap-gap-schema-experiment-gate-alignment-001"></a>GAP-SCHEMA-EXPERIMENT-GATE-ALIGNMENT-001

The `skill` and `folder` placeholders weaken the substantive successor gates in the main plan. Evidence: [review finding F4](reviews/2026-08-20-artifacts-full-review/review.md#f4--local-placeholders-weaken-the-programs-substantive-successor-gates).

## Boundary check

- This is a project-local Craft operational ledger, not the candidate append-only knowledge ledger discussed in `README.md`.
- Candidate schemas remain experiment-local and non-normative; no runtime, registry, resolver, criterion, fixture, or run is claimed complete.
