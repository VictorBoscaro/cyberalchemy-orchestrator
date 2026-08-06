---
status: accepted
date: 2026-08-06
scope: recursive-work-orchestrator-composition-forms
decision_id: DG-RWO-CFM-002
selected_option: QUORUM-RWO-STRUCTURAL
---

# RWO structural quorum ownership

## Decision

RWO owns `ReleasePolicy.quorum(n)` only as a structural count over distinct eligible source arrivals already accepted by the journal.

For a FanIn with `N` declared keyed sources:

```text
1 <= quorum <= N
```

An arrival counts at most once for its declared `SourceKey` and only when its accepted record matches the exact graph, Work Run, Work Attempt, selector, and current fence. Transport deliveries, redeliveries, duplicate accepted observations, stale attempts, unlisted sources, and mismatched identities do not increase the count.

When the `n`th eligible distinct source is accepted, RWO freezes the release manifest in the declared canonical source order and may issue exactly one idempotent join command. Late arrivals cannot rewrite that manifest or create a second join command; their evidence treatment is owned by the separate late-arrival decision.

## Semantic boundary

Structural quorum means only “the declared count of eligible accepted arrivals has been reached.” It does not mean quality, agreement, consensus, truth, success, approval, admission, authority, or effect permission.

Weighted, qualified, semantic, or policy-driven quorum belongs in an explicit Decision Work. That Work may emit an opaque result that ordinary Gate or event routing consumes; RWO does not evaluate its meaning.

## Rationale

This follows the existing FanIn design, avoids another Work Run for deterministic count-only release, and preserves replayable reducer behavior. It also prevents transport redelivery from manufacturing progress and prevents a generic quorum facility from becoming a domain policy engine.

## Authority boundary

This decision settles structural quorum ownership and numeric bounds only. It does not authorize schema, reducer, journal, design, ontology, implementation, projection, promotion, release, deployment, or production mutation. Journal acceptance/fencing and exact runtime conformance retain their own gates.

## Source and consequences

- Source design: `docs/features/recursive-work-orchestrator/DESIGN.md` §5.3 and §6.2.
- Refined candidate and planned fixtures: `docs/features/recursive-work-orchestrator/development/refinement-runs/20260806T173343Z-rwo-composition-form-metamodel/delegated-research/findings.md`.
- Admissibility receipt: `docs/features/recursive-work-orchestrator/development/decision-gates/20260806T203541Z-composition-form-owners/receipts/DG-RWO-CFM-002-option-admissibility.json`.
- Decision source: repository owner selected option `QUORUM-RWO-STRUCTURAL` in the active 2026-08-06 Decision Gate.

Future candidate schemas and fixtures may cite this record for `1 <= n <= source_count`, distinct-source counting, and the frozen-manifest/single-command boundary. The late-arrival disposition remains independently unresolved.
