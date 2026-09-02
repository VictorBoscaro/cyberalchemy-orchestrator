---
tags: [agent-dispatch, execution-graph, confirmation-authority, llm-compilation, runtime-orchestration]
artifact_kind: session
layer: feature
version: 0.1.0
created_at: 2026-09-01T15:24:00-03:00
updated_at: 2026-09-01T15:24:00-03:00
expires: 2026-10-31
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 9
importance_rationale: "The session fixed the ACI product-authority model, tested a concrete ExecutionGraph v2 boundary, and exposed the required separation between LLM-authored semantics and deterministic compilation."
---

# ACI ExecutionGraph authority refinement and compiler boundary

## Summary

The repository objective is to keep delegated agent work bound to explicit objectives, authority, decisions and evidence across compilation, confirmation and execution. This session began by reconstructing the [bounded ACI roadmap closure](2026-09-01-1326-aci-bounded-roadmap-closure.md) and explaining that its remaining product blocker concerned who creates and confirms complete execution authority. The owner decided that an agent compiles one canonical `ExecutionGraph` JSON from a short user intent and that topology, basic and full are views of the same full-digest authority. The [ACI Craft ledger](../docs/features/agents-communication-infra/CRAFT.md) was updated to supersede the manual product-field premise and retain only the technical v2 contract gap. An approved Invoke Refine run produced a definition, competing-boundary selection, proposed closed schema, review-correct-verify toy, deterministic projections, repair validation and specification-first work pack. Two read-only reviewers independently blocked incomplete iterations for hidden runtime inputs, free-text control semantics and impossible output schemas, after which revision `r2` passed both reviews and deterministic local checks. The [refinement result](../docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/RESULT.md) kept one JSON as the sole proposed logical authority while leaving confirmation evidence and runtime-derived state outside it. The proposed schema covered exact node instructions, agents/models, inputs, outputs, topology, grants, limits, isolation, validation and lifecycle, but remained explicitly unimplemented. A final producer-consumer audit contradicted the assumption that a LLM should populate the whole canonical shape directly because IDs, digests, resolved capabilities, credential handles, validators, policies and audit constants need deterministic system owners. The next move is therefore to specify a compact LLM-authored `DraftGraph` and a deterministic `DraftGraph → ExecutionGraph` compiler before promoting the canonical v2 spec or writing runtime code.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [ACI bounded roadmap closure through POLICY-002](2026-09-01-1326-aci-bounded-roadmap-closure.md) | `derives-from` | This session resolves the earlier product-authority question and refines its remaining canonical-graph contract gap. |
| [Agents Communication Infrastructure Craft ledger](../docs/features/agents-communication-infra/CRAFT.md) | `validates` | The owner decisions and refinement evidence support the ledger's single canonical graph direction while preserving its specification/code boundary. |
| [ExecutionGraph authority Refine result](../docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/RESULT.md) | `derives-from` | The session's technical conclusion and next work are grounded in the completed ten-stage refinement evidence. |

## Open questions

- What is the smallest closed `DraftGraph` the LLM can reliably author without emitting runtime
  identities, hashes, resolved capability artifacts or policy boilerplate?
- Which proposed `ExecutionGraph` fields survive a strict producer-consumer-authority audit, and
  which should be derived, fixed by the contract or moved into reusable resource tables?
- Should display-only names and other non-executable presentation metadata participate in the full
  authority digest and therefore force reconfirmation when changed?

## Next steps

1. Define the LLM-owned `DraftGraph`, including its controlled vocabulary and validation boundary.
2. Define the deterministic compiler/resolver that expands the draft into the single complete
   canonical `ExecutionGraph` without creating a second authority.
3. Reduce the proposed canonical shape through internal resource/profile tables and remove fields
   without one named producer, consumer and authority purpose.
4. Write and independently review the canonical v2 spec, projector contract, real golden fixtures
   and negative vectors.
5. Authorize compiler/projector code only after the specification and conformance package pass.

## Recommendation

Begin the v2 specification with a field-ownership matrix—LLM, policy engine, resolver, compiler,
canonicalizer or runtime—and reject every field without one unambiguous producer and consumer;
then derive both the compact `DraftGraph` and full canonical `ExecutionGraph` from that matrix.

## Files touched

- `docs/features/agents-communication-infra/.craft/ledger.yml`
- `docs/features/agents-communication-infra/CRAFT.md`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/REFINE-SEED-PROPOSAL.md`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/REFINE-DISPATCH.json`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/RUN-MANIFEST.md`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/RUNTIME-HANDOFF.md`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/RESULT.md`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/evidence-index.json`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/stages/01-context-builder/context-pack.md`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/stages/01-context-builder/context-pack.json`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/stages/01-context-builder/RECEIPT.md`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/stages/02-invoke-define/DEFINITION.md`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/stages/02-invoke-define/TECHNIQUE-TRACE.md`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/stages/02-invoke-define/RECEIPT.md`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/stages/03-interrogation-review/DIALECTIC-REVIEW.md`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/stages/03-interrogation-review/RECEIPT.md`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/stages/04-research-decision/DECISION.md`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/stages/04-research-decision/RECEIPT.md`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/stages/05-distill/SELECTION.md`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/stages/05-distill/RECEIPT.md`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/stages/06-invoke-design/ARCHITECTURE.md`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/stages/06-invoke-design/execution-graph-v2.proposed.schema.json`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/stages/06-invoke-design/TECHNIQUE-TRACE.md`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/stages/06-invoke-design/RECEIPT.md`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/stages/07-interrogation-design-review/review-correct-verify-toy-graph.json`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/stages/07-interrogation-design-review/topology-view.json`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/stages/07-interrogation-design-review/basic-view.json`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/stages/07-interrogation-design-review/PROJECTOR-CONTRACT.md`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/stages/07-interrogation-design-review/DESIGN-REVIEW.md`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/stages/07-interrogation-design-review/RECEIPT.md`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/stages/08-distill-repair/validation.md`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/stages/08-distill-repair/RECEIPT.md`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/stages/09-invoke-plan/implementation-layering.md`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/stages/09-invoke-plan/WORK-PACK.md`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/stages/09-invoke-plan/PLAN-VALIDATION.md`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/stages/09-invoke-plan/TECHNIQUE-TRACE.md`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/stages/09-invoke-plan/RECEIPT.md`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/stages/10-final-interrogation/FINAL-INTERROGATION.md`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/stages/10-final-interrogation/RECEIPT.md`
- `sessions/2026-09-01-1326-aci-bounded-roadmap-closure.md`
- `sessions/2026-09-01-1524-aci-execution-graph-refinement.md`
