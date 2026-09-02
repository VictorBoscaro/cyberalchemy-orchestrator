---
tags: [generic-stage-handoff, agent-communication, publication-authority, immutable-delivery]
artifact_kind: session
layer: capability
version: 0.1.0
created_at: 2026-09-01T22:35:12-03:00
updated_at: 2026-09-01T22:35:12-03:00
expires: 2026-10-31
decisions_made: true
contradictions_found: true
specs_updated: [docs/features/agents-communication-infra/specs/capabilities/generic-stage-handoff.md]
promoted_candidates: [docs/features/agents-communication-infra/specs/capabilities/generic-stage-handoff.md]
expected_importance: 8
importance_rationale: "This session closes the architectural and capability-level contract for exact producer-to-consumer handoff while preserving the remaining aggregate and implementation gates."
---

# Generic Stage Handoff Capability Specification

## Summary

The repository objective is to keep agent work connected to the authority, exact results and evidence that make later staged work trustworthy. This session set out to turn the approved generic-stage-handoff discovery into a normative ACI capability and a recorded architecture decision. The local DomainSpec subagent strategy was updated so feature-specification work routes through `other` to the exact `domainspec-spec-feature` capability, and that skill was brought into the repository instead of remaining only an external junction. A governed writer/reviewer dispatch produced the capability spec; an initial launch failed because hyphenated group identifiers were invalid, and the corrected second dispatch completed the author/reviewer loop. Review and repair preserved five separate facts—result commitment, publication authorization, publication occurrence, immutable delivery and consumer acceptance—and kept access, use, reliance and claim support independently evidenced. The owner selected ACI-GSH-001: extend the bounded host-workflow pipeline rather than introduce a standalone aggregate in this version, while reopening that alternative if any of nine collapse tests fails. The same reviewer passed the corrected capability and decision at digests `sha256:cb150f5dfd3518b610fd5d6d40baee2613dbbb4bdab0dda665b9bde6a22d6064` and `sha256:e0303e89bd279b949df27de9f768877bf0db252f11db617ebec6afc9d0ad8a91`. The ACI Craft ledger now records this closed architecture choice and an active promotion gap; no aggregate contract or runtime implementation is claimed.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Agents Communication Infrastructure](../docs/features/agents-communication-infra/README.md) | `is-part-of` | The session closes one bounded ACI capability and leaves its aggregate promotion inside the feature's governed work. |
| [Generic stage handoff discovery](../docs/features/agents-communication-infra/discovery/generic-stage-handoff.md) | `contextualizes` | The session records how the reviewed discovery was approved, specified and converted into an architectural choice. |
| [Generic stage handoff capability](../docs/features/agents-communication-infra/specs/capabilities/generic-stage-handoff.md) | `contextualizes` | The session preserves the author/reviewer lifecycle, corrections, final digest and remaining proof ceiling of the capability spec. |
| [ACI-GSH-001](../docs/decisions/aci-generic-stage-handoff-architecture.md) | `contextualizes` | The session records the owner selection, two-candidate collapse analysis and final independent recheck of the decision. |

## Open questions

- Which exact aggregate aspects, durable commands/events, mappings and workflow guards should realize the five accepted facts without collapsing their authorities?

## Next steps

1. Promote the accepted capability into the ACI domain, operation, mapping and workflow specifications with explicit aggregate placement and conformance fixtures.
2. Independently red-team the promoted contract against all nine collapse tests.
3. Authorize implementation only after aggregate and implementation-readiness gates pass.

## Recommendation

Promote the five facts as separate durable contracts in the selected staged pipeline, treating `SourceToSlotMapping` only as preconfirmed topology and visibility intent rather than post-commitment publication authorization.

## Files touched

- `.agents/skills/domainspec-subagents-strategy/SKILL.md`
- `.claude/skills/domainspec-spec-feature/SKILL.md`
- `.claude/skills/domainspec-subagents-strategy/SKILL.md`
- `.codex/skills/domainspec-subagents-strategy/SKILL.md`
- `.gitignore`
- `.codex/dispatch-proposals/2026-09-01-generic-stage-handoff-capability-spec.json`
- `.codex/dispatch-proposals/2026-09-01-generic-stage-handoff-capability-spec-close.json`
- `.codex/dispatch-proposals/2026-09-01-generic-stage-handoff-capability-spec-r2.json`
- `.codex/dispatch-proposals/2026-09-01-generic-stage-handoff-capability-spec-r2-close.json`
- `.codex/workflow-inputs/generic-stage-handoff-bootstrap/proposal.json`
- `.codex/workflow-inputs/2026-09-01-generic-stage-handoff-capability-spec/launch-plan.json`
- `.codex/workflow-inputs/2026-09-01-generic-stage-handoff-capability-spec/spec-writer-0-turn-0.json`
- `.codex/workflow-inputs/2026-09-01-generic-stage-handoff-capability-spec/document-reviewer-0-turn-0.json`
- `.codex/workflow-inputs/2026-09-01-generic-stage-handoff-capability-spec-r2/launch-plan.json`
- `.codex/workflow-inputs/2026-09-01-generic-stage-handoff-capability-spec-r2/spec_writer-0-turn-0.json`
- `.codex/workflow-inputs/2026-09-01-generic-stage-handoff-capability-spec-r2/document_reviewer-0-turn-0.json`
- `docs/features/agents-communication-infra/discovery/generic-stage-handoff-intention.md`
- `docs/features/agents-communication-infra/discovery/generic-stage-handoff.md`
- `docs/features/agents-communication-infra/specs/capabilities/generic-stage-handoff.md`
- `docs/decisions/aci-generic-stage-handoff-architecture.md`
- `docs/features/agents-communication-infra/.craft/ledger.yml`
- `docs/features/agents-communication-infra/CRAFT.md`
- `sessions/2026-09-01-2049-generic-stage-handoff-discovery.md`
- `sessions/2026-09-01-2235-generic-stage-handoff-spec.md`
