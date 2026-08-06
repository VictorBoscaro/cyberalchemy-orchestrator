---
module: rwo-recovery-decision-contract
version: candidate-2
status: draft
updatedAt: 2026-08-05
docType: implementation-layering
---

# Implementation Layering: RWO Recovery Decision Contract

## Target And Scope

- Target: `RecoveryDecisionContract@candidate-2`
- Scope: RWO recovery decision capability and bounded owner integrations
- Current state: design candidate; no recovery implementation exists
- Source: `../stages/08-distill-repair.md`

## Layer Decision Table

| Layer | Decision question | Minimum working unit | Included scope | Deferred scope | Exit evidence | Promotion decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 — pure contract | After this layer, we know whether the exact case, digest, classification, and identity model is deterministic without storage or owners. | canonical ID wrapper + closed case admission + pure classifier + identity transitions | candidate schemas, existing `aci.canonical-json@1` reuse, golden vectors, all 20 design games as executable fixtures | journal mutation, domain/ARE/effect owners, ontology | byte-identical vectors; invalid shapes reject; every fixture single-valued; zero journal/ARE/adapter calls | continue only if all pure invariants pass |
| L1 — accepted history | After this layer, we know whether one trigger can release at most one treatment under concurrency and restart. | RecoveryFrontier reducer plus atomic validation-vector acceptance | trigger consumption, inhibition, counters, fences, SQLite transaction, replay/restart | domain/effect/ARE owner conformance, ontology promotion | concurrent and crash-window tests; one debit/allocation; restart reconstructs same frontier | continue only with journal owner acceptance |
| L2 — owner seams | After this layer, we know whether domain meaning, optional ARE evidence, and effect uncertainty integrate without authority collapse. | admitted handle conformance at each seam | domain signal/policy, exact-effect permit/reconciliation, optional ARE semantic receipt | ontology promotion and pilot | positive and owner-substitution negative fixtures; zero effect call on unknown outcome | continue only after G1/G2/G3 owners accept exact contracts |
| L3 — governed adoption | After this layer, we know whether the model may become a governed ontology/runtime capability. | evidence-backed ontology delta and bounded pilot decision | definitions/ontology proposal, migration/version policy, operating evidence | release/production | owner approvals, ontology validation, complete regression/evidence package | promote, revise, or defer; never inferred from L0-L2 |

## Non-Regression Guardrails

- Later layers preserve the thirteen-disposition and eight-case identity boundaries.
- `authority_effect: none` remains invariant through every layer.
- Outcome-unknown effect has zero direct retry routes.
- L1 cannot invent domain meaning; L2 cannot rewrite journal history.
- ARE remains optional semantic evidence and cannot return a disposition.
- L3 is a new authority decision; implementation evidence is not promotion.

## Recommended Next Layer

- Next layer: L0
- Key decision unlocked: whether the repaired contract is mechanically
  deterministic and internally implementable using the current canonicalizer
- First unit: `SWU-RRD-001`
- Major deferred scope: persistence and every cross-owner conformance decision

