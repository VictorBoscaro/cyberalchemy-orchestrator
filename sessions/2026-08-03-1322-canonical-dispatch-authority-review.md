---
tags: [agent-orchestration, canonical-authority, dispatch-graphs, independent-review]
artifact_kind: session
layer: feature
version: 0.1.0
created_at: 2026-08-03T13:22:19-03:00
updated_at: 2026-08-03T13:22:19-03:00
expires: 2026-10-02
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 9
importance_rationale: "The session established the intended single-authority dispatch model, corrected its discovery boundary, and exposed the missing governed follow-up compiler needed to execute its own review topology."
---

# Canonical Dispatch Authority Discovery and Review

## Summary

The repository aims to keep agent work connected to confirmed objectives, decisions, authority and evidence through execution. This session set out to identify and rewrite the discovery that should own the model in which one user-confirmed structure is persisted and carried forward into agent provisioning, routing, scheduling and runtime effects. Independent research identified Agents Communication Protocols as the primary discovery, with capability resolution, bus semantics and audit-ledger cutover retained by companion owners. The central decision was that the persisted `ConfirmedDispatch`, containing the canonical `DispatchSpec`, is the authority for a future `runtime-managed` run, while the graph is its structural nucleus and all other surfaces are derived. The discovery was restructured around that invariant without treating `subagents-dispatch.yaml`, a diagram, a recipe or the chat parent as a parallel execution authority. Three independent reviewers then found that v0.4.0 overstated ratification, blurred the `legacy-managed` boundary and left confirmation identity, transactionality, revocation races and audit barriers incomplete. Those objections produced v0.4.1, which scopes the proposal to `runtime-managed`, makes confirmation digest-bound over server-resolved bytes, separates YAML ownership and defines idempotency, revocation-state and opening/closing rules. The planned zig-zag review could not reach a terminal round because the governed compiler emits only turn-zero bindings while the mandatory hook rejects unbound follow-ups, so the dispatch closed honestly with `exit_reason: error`. A consolidated `FIX` review records the verified findings, applied remediations and the requirement for a later all-reviewer `NO_OBJECTION` round. Structural validation otherwise passed, with the pre-existing nested discovery path remaining incompatible with the current `discovery/<slug>.md` validator contract.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Agents Communication Protocols](../docs/features/agents-communication-infra/discovery/agents-communication-protocols/README.md) | `refines` | This session produced and reviewed the v0.4.x canonical-authority framing for the discovery. |
| [Canonical Authority v0.4.0 Review](../docs/features/agents-communication-infra/discovery/agents-communication-protocols/review/canonical-authority-v0.4.0/review.md) | `derives-from` | The session close inherits the independent findings, remediation record and execution residue consolidated in the review. |

## Open questions

- What governed compiler contract should produce frozen `turn_ordinal > 0` manifests and binding envelopes for an existing seat without allowing the chat parent to synthesize authority?

## Next steps

1. Extend the governed dispatch compiler to emit authorized follow-up turns with exact prompt-template and input-manifest digests.
2. Re-run the same three independent reviewer lenses over discovery SHA-256 `D7230A422CA08665A05D674430F806FA476D9AA9770B82681BB6B59EA3EED9E7` until one round returns three `NO_OBJECTION` verdicts or the confirmed ceiling is reached.
3. Coordinate the discovery-path migration from nested `discovery/<slug>/README.md` to `discovery/<slug>.md`, updating inbound and outbound links atomically.

## Recommendation

Implement the governed follow-up compiler before claiming that the proposed canonical graph can execute autonomous zig-zag workflows; use this exact blocked review as the first acceptance fixture.

## Files touched

- `.codex/workflow-inputs/2026-08-03-canonical-authority-discovery-review/`
- `.codex/workflow-inputs/2026-08-03-agents-communication-protocols-v040-review/`
- `docs/features/agents-communication-infra/discovery/agents-communication-protocols/README.md`
- `docs/features/agents-communication-infra/discovery/agents-communication-protocols/review/canonical-authority-v0.4.0/review.md`
- `telemetry/agents/subagents-dispatch.yaml`
- `sessions/2026-08-03-1322-canonical-dispatch-authority-review.md`
