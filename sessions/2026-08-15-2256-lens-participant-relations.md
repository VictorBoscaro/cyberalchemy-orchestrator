---
tags: [lens-composition, participant-roles, schema-instances, categorical-translation]
artifact_kind: session
layer: capability
version: 0.1.0
created_at: 2026-08-15T22:56:38-03:00
updated_at: 2026-08-15T22:56:38-03:00
expires: 2026-10-14
decisions_made: true
contradictions_found: true
specs_updated: [implementations/contracts/register-dispatch-runtime-package.v1.json]
promoted_candidates: []
expected_importance: 8
importance_rationale: "The session replaced an identity-level metaphor with an observable protocol and identified the first empirical test needed for lens composition."
---

# Participant-mediated lens relations

## Summary

This session advanced the repository objective of keeping agent work connected to attributable objectives, transformations, and evidence by examining how human and agent contributions relate in lens composition. Its main objective was to test the intuition that Victor, Vlad, and the agent are different lenses and sometimes act as schemas, functors, or consumers of one another's instances. A governed local research dispatch used two independent explorers and an adversarial reviewer over recent conversations and the formalization repository. The strong identity claim was rejected because person, lens enactment, schema, instance, and functor have different types, while the weaker participant-mediated account survived. The accepted working model indexes roles by episode: a participant can enact a readout, propose or adopt a schema, emit an artifact under it, or transform another artifact, and functoriality remains a separate proof obligation. The evidence witnesses a bilateral Victor–agent chain but contains no independently attributable recent Vlad input and output, so the three-part relation remains an open empirical claim rather than a finding. To execute the dispatch, the session completed the local runtime migration to schema 0.6.4, including immutable route closure, compatibility-hook routing, source manifests, and focused tests. The next decision is not to build a category or tool yet, but to preregister one real three-part episode with a fixed task, attributable inputs, typed transformations, downstream effects, and independent review.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Composition research program](../internal-tools/composition-lab/research-program.md) | `is-part-of` | The session investigates the program's first case, lens composition, and supplies a bounded local result rather than a general theory. |
| [Participant–agent lens findings](../internal-tools/composition-lab/research/2026-08-13-person-agent-lens-relations/findings.md) | `derives-from` | The session conclusions and forward registers are grounded in the accepted synthesis and its independent returns. |

## Open questions

- Does a real Victor–Vlad–agent episode exhibit three independently attributable enacted lenses, or does its result reduce to coordination, aggregation, or synthesis by one participant?
- Under what declared domains, mappings, and preservation laws could one observed transformation be promoted from contract-governed translation to a functor?
- Does consuming another participant's typed artifact change an independently fixed task or readout, rather than merely add text to the context?

## Next steps

1. Integrate the bounded findings into the Composition Lab research program as provisional local evidence, preserving the missing Vlad vertex and the rejected identity claim.
2. Create `experiment-initial-definitions.md` for one naturally occurring Victor–Vlad–agent task with the task and success criterion fixed before interaction.
3. Preregister and execute the episode with attributable inputs, schemas, artifacts, transformations, preserved/lost properties, downstream effects, and an independent reviewer.
4. Compare the observed episode with D1 and accepted external precedents before making any architecture, vocabulary, or tooling decision.

## Recommendation

Run the smallest real three-part episode next; it directly attacks the only load-bearing evidence gap and can distinguish lens composition from ordinary collaborative communication without prematurely building a lens ontology or tool.

## Files touched

- `.codex/dispatch-proposals/2026-08-13-person-agent-lens-relations-opening.json`
- `.codex/dispatch-proposals/2026-08-13-person-agent-lens-relations-close.json`
- `.codex/workflow-inputs/2026-08-13-person-agent-lens-relations/explorers-0-turn-0.json`
- `.codex/workflow-inputs/2026-08-13-person-agent-lens-relations/explorers-1-turn-0.json`
- `.codex/workflow-inputs/2026-08-13-person-agent-lens-relations/reviewer-0-turn-0.json`
- `.codex/workflow-inputs/2026-08-13-person-agent-lens-relations/launch-plan.json`
- `docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json`
- `implementations/contracts/register-dispatch-runtime-package.v1.json`
- `implementations/server/runtime/host_dispatch_hook.py`
- `implementations/server/runtime/legacy.py`
- `implementations/server/runtime/local_pilot.py`
- `implementations/tests/runtime/test_anti_bias_mode_appender.py`
- `internal-tools/composition-lab/research/2026-08-13-person-agent-lens-relations/explorer-formal.md`
- `internal-tools/composition-lab/research/2026-08-13-person-agent-lens-relations/explorer-operational.md`
- `internal-tools/composition-lab/research/2026-08-13-person-agent-lens-relations/reviewer.md`
- `internal-tools/composition-lab/research/2026-08-13-person-agent-lens-relations/research.md`
- `internal-tools/composition-lab/research/2026-08-13-person-agent-lens-relations/findings.md`
- `telemetry/agents/subagents-dispatch.yaml`
- `sessions/2026-08-15-2256-lens-participant-relations.md`
