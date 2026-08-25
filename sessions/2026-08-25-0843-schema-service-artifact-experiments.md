---
tags: [schema-service, artifact-model, experimentation, review, craft-ledger]
artifact_kind: session
layer: project
version: 0.1.0
created_at: 2026-08-25T08:43:35-03:00
updated_at: 2026-08-25T08:43:35-03:00
expires: 2026-10-24
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 8
importance_rationale: "This session established the first executable evidence path for the Schema Service artifact model and identified the defects that must be repaired before experimentation."
---

# Schema Service artifact experiments

## Summary

This session advanced the repository objective of keeping agent work connected to explicit identity, authority, lifecycle, and evidence by testing the proposed Schema Service artifact model against concrete artifact families. The immediate objective was to turn the broad model into a small experimentation plan beginning with `analysis`, followed conditionally by `skill` and `folder`. Research against local ontology conventions and DomainSpec precedents supported separating semantic type, immutable schema revision, durable artifact, manifest revision, representation, snapshot, and validation without claiming that the model was proven. The session created experiment-local candidate definitions for `analysis` and four refinements while reserving normative `schema` authority for later governed publication. It also kept `criterion.md`, fixtures, runs, promotion, and enforcement absent until their evidence and authority gates exist. Because the current runtime could not execute the intended sequential review handoffs, the user explicitly authorized a degraded independent-wave review. The dedicated approver accepted the resulting report package, while the substantive review verdict remained `FIX`, not approval of the target artifacts. Four MAJOR contradictions survived: lifecycle cannot be represented per candidate, the unresolved root base leaves runs fail-closed after criterion freeze, revision immutability begins too late, and the `skill`/`folder` placeholders weaken the main plan's successor gates. The root Craft ledger now records this work as a blocked review-audit context with those four active gaps and the accepted review as evidence. The next governed move is to repair all four findings and revalidate the package before pre-registering or freezing `criterion.md`.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Schema Service artifact-model session](2026-08-17-1400-schema-service-artifact-model.md) | `derives-from` | This session continued the artifact-role and schema-service questions established there. |
| [Schema Service README](../projects/schema-service/README.md) | `is-part-of` | The work directly advances the Schema Service project and remains bounded by its candidate status. |
| [Artifact-types experimentation plan](../projects/schema-service/experimentation-plans/artifact-types-v0/experimentation-plan.md) | `contextualizes` | This node records why the three-experiment sequence exists and what currently blocks it. |
| [Full artifact review](../projects/schema-service/reviews/2026-08-20-artifacts-full-review/review.md) | `derives-from` | The session's blocking gaps and next move are grounded in the accepted report whose substantive verdict is `FIX`. |

## Open questions

- Should the `analysis` root acquire a revision-exact published `document` base, or should the experiment define a validated root-without-base semantic?
- Will the experiment distinguish observed-phenomenon, observational-study, A/B-result, and general analyses without making `general` a vacuous fallback?
- Which common fields and acquisition modes survive corpus-based validation strongly enough to justify later publication?

## Next steps

1. Make candidate lifecycle state representable and enforceable per candidate revision.
2. Add an explicit base-resolution gate, make revision immutability begin at catalog admission, and restore the substantive `skill` and `folder` gates.
3. Recompute catalog digests, validate references and hashes, and rerun a bounded review of the repaired package.
4. Pre-register and freeze `criterion.md` only after the review gaps close; then create fixtures and execute the `analysis` experiment.
5. Use `experiment.md` and `findings.md` to decide whether `skill` should begin; keep `folder` dependent on the `skill` evidence.

## Recommendation

Repair lifecycle representation and base resolution first because they determine whether any candidate can be resolved for a valid run; then close immutability and successor-gate consistency before freezing evidence.

## Files touched

- `.craft/ledger.yml`
- `CRAFT.md`
- `projects/schema-service/README.md`
- `projects/schema-service/research/experimental-type-staging-rule/findings.md`
- `projects/schema-service/research/experimental-type-staging-rule/reports/01-staging-precedents.md`
- `projects/schema-service/research/experimental-type-staging-rule/reports/02-authority-leak-review.md`
- `projects/schema-service/research/experimental-type-staging-rule/research.md`
- `projects/schema-service/experimentation-plans/artifact-types-v0/experimentation-plan.md`
- `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/README.md`
- `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/experiment-initial-definitions.md`
- `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/experiment-manifest.yaml`
- `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/candidate-types/README.md`
- `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/candidate-types/catalog.yaml`
- `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/candidate-types/definitions/analysis@0.yaml`
- `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/candidate-types/definitions/analysis-general@0.yaml`
- `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/candidate-types/definitions/analysis-observed-phenomenon@0.yaml`
- `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/candidate-types/definitions/analysis-observational-study@0.yaml`
- `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/candidate-types/definitions/analysis-ab-test-result@0.yaml`
- `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/fixtures/README.md`
- `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/runs/README.md`
- `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/02-skill/README.md`
- `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/03-folder/README.md`
- `.codex/workflow-inputs/2026-08-17-schema-experimental-type-staging-rule/opening.json`
- `.codex/workflow-inputs/2026-08-17-schema-experimental-type-staging-rule/launch-plan.json`
- `.codex/workflow-inputs/2026-08-17-schema-experimental-type-staging-rule/rule_reviewers-0-turn-0.json`
- `.codex/workflow-inputs/2026-08-17-schema-experimental-type-staging-rule/rule_reviewers-1-turn-0.json`
- `.codex/workflow-inputs/2026-08-17-schema-experimental-type-staging-rule/close.json`
- `.codex/workflow-inputs/2026-08-20-schema-artifacts-full-review/targets.json`
- `.codex/workflow-inputs/2026-08-20-schema-artifacts-full-review/opening.json`
- `.codex/workflow-inputs/2026-08-20-schema-artifacts-full-review/opening-v2.json`
- `.codex/workflow-inputs/2026-08-20-schema-artifacts-full-review/launch-plan.json`
- `.codex/workflow-inputs/2026-08-20-schema-artifacts-full-review/attackers-0-turn-0.json`
- `.codex/workflow-inputs/2026-08-20-schema-artifacts-full-review/attackers-1-turn-0.json`
- `.codex/workflow-inputs/2026-08-20-schema-artifacts-full-review/attackers-2-turn-0.json`
- `.codex/workflow-inputs/2026-08-20-schema-artifacts-full-review/verifiers-0-turn-0.json`
- `.codex/workflow-inputs/2026-08-20-schema-artifacts-full-review/verifiers-1-turn-0.json`
- `.codex/workflow-inputs/2026-08-20-schema-artifacts-full-review/synthesizer-0-turn-0.json`
- `.codex/workflow-inputs/2026-08-20-schema-artifacts-full-review/final_approval-0-turn-0.json`
- `.codex/workflow-inputs/2026-08-20-schema-artifacts-full-review/close.json`
- `projects/schema-service/reviews/2026-08-20-artifacts-full-review/review.md`
- `telemetry/agents/subagents-dispatch.yaml`
- `sessions/2026-08-25-0843-schema-service-artifact-experiments.md`
