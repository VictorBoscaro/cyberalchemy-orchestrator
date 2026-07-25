---
tags: [agents, architecture, mathematics, lean, findings]
node_type: research-findings
status: proposed
version: 0.2.0
last_updated: 2026-07-24
related_plan: plans/governed-agent-work-infrastructure/subplans/agent-work-language-research/PLAN.md
stream_id: R1
dispatch_id: 2026-07-24-agent-language-formalization-design
evidence: research/agent-language-mathematical-formalization/research.md
---

# Findings: Agent-Language Mathematical Formalization

## Outcome

The research supports a small correspondence-oriented formal core, not a universal mathematical
kernel and not a category of the whole product. The recommended base is a many-sorted,
proof-relevant typed multigraph. Category structure is earned only for relation families with
explicit identities, admissible composition, and coherence laws.

This is a design finding for the appendix, not a product architecture verdict. The complete
independent returns and countermodels are preserved in [research.md](research.md).

## Findings

### F-01 — Start below category level

Use typed carriers, direct edges, and explicit composition witnesses. This represents incomplete
knowledge and heterogeneous relation policies without inventing closure. A relation family may
later become a category, preorder, transition system, or another structure when its laws justify
that promotion.

### F-02 — Make correspondence proof-relevant

Every mathematical construct needs a record of source, responsibility, applicability, authority
boundary, correspondence status, and residue. Formal soundness, product correspondence, and
execution authority are separate judgments.

### F-03 — Separate five semantic responsibilities

The model must preserve:

```text
semantic structure
≠ accepted runtime fact
≠ derived projection
≠ executable authority
≠ external physical effect
```

Collapsing these responsibilities would contradict the current ACI separation between accepted
commands/events, reducers, projections, effect reconciliation, fences, and physical writers.

### F-04 — Derived relations require witnesses

A derived path records its direct facts and the rule/version permitting composition. It is not
silently promoted to a direct fact, and it cannot create authority merely by reachability.

### F-05 — Deep structure does not require deep runtime authority

A finite recursive work graph may compile into bounded leaf assignments. The compiler must prove
that no invoked orchestrator receives the ability to invoke another orchestrator. Context, tools,
budgets, evidence, approval, and terminal state are explicit materializations, not lineage
inheritance.

### F-06 — Event replay is pure; projections remain non-authoritative

For a fixed accepted history and reducer version, replay should be deterministic and effect-free.
Folder trees, dashboards, and current-state views are projections that may be rebuilt or stale and
cannot mint execution authority.

### F-07 — Existing Lean assets are narrow precedents

The inspected corpus contains relevant results about graph-level acyclicity, permission-policy
composition, and a counterexample to instance-level preservation. Their status is only
`proof-present-in-bound-source`; no build or dependency audit was performed.

### F-08 — Countermodels are the first acceptance tests

The first formal model must express path/identity separation, lineage/authority separation,
projection/fact separation, schema-validity/authority separation, local/global separation,
schema/instance separation, fail-open empty policy, and bounded recursive execution.

### F-09 — Bootstrap is relative, finite, and explicit

A viable kernel-of-kernels hypothesis requires finite dependencies, pinned versions, declared
owners, decidable local checks, and explicit admitted roots. Such a boundary can terminate checking
but cannot justify its own roots absolutely.

### F-10 — Keep this work inside one program

The Plan registry is the program-level projection. The existing formalization directory owns the
brief, raw synthesis, and findings; the system view owns the appendix. Mathematical subtopics and
review rounds do not receive new folders by default.

### F-11 — Separate meta-contract, global laws, domain kernels, and composition

The owner critique and bounded Lean-kernel follow-up show that `kernel-of-kernels` is not yet one
coherent object. A meta-contract can define declaration well-formedness, while a separate small
checker can evaluate that judgment relative to an admitted bootstrap; neither derives domain
rules, proves their preservation or joint satisfiability, or authorizes effects. Global invariants,
bounded domain kernels, composition witnesses, and runtime enforcement remain separate
responsibilities until research establishes a smaller correspondence.

The actual Lean kernel is an `analogy-only` precedent for rich elaboration followed by a small
trusted checker and possible independent rechecking. It does not supply the product's authority,
provenance, precedence, conflict, temporal, or effect semantics. The local `permguard` “Lean
kernel” is a different artifact: an application policy decision program verified in Lean.

## Proposed first formal subset

The appendix should define:

- stable identity and versioned mutable descriptions;
- provisional many-sorted carriers;
- typed relation signatures and direct facts;
- witnessed derived paths and relation-specific cycle policy;
- provenance chains;
- accepted event history and pure reduction;
- rebuildable projections;
- indexed authority records and explicit context manifests;
- finite recursive work graphs and bounded leaf compilation; and
- a finite bootstrap, meta-well-formedness judgments, global-law preservation, and scoped
  compatibility witnesses without collapsing them into one metakernel.

The first Lean dependency cone should be smaller: identity, direct/derived relation separation,
cycle validation shape, deterministic fold, projection non-authority, lineage non-authority, and
finite work compilation. Category-theoretic encodings should enter only after a concrete proof
obligation requires them.

## Proof-status gate

No claim may advance to `machine-checked-currently` until a later verification pass records:

1. the selected Lean project and toolchain;
2. the exact build target and dependency cone;
3. successful build output;
4. `sorry` and axiom audit;
5. theorem and source digests;
6. correspondence review; and
7. the relationship to any runtime validator or generated artifact.

Even then, proof evidence does not authorize runtime effects.

## Recommendation

Proceed with the mathematical appendix on this basis, then freeze its revision and run the
previously planned staged review:

1. two independent reviewers for mathematical/categorical soundness;
2. two fresh independent reviewers for Lean mechanizability and infrastructure correspondence;
3. if the two sequential layers disagree materially, a third layer with fresh reviewers.

Each layer remains a separately confirmed Review Dispatch because the current runtime cannot bind
dynamic downstream handoff durably.

## Open Questions

The canonical question history is in [research.md](research.md#open-questions). The findings leave
`ALF-OQ-001` through `ALF-OQ-011` and `ALF-OQ-013` through `ALF-OQ-015` open. `ALF-OQ-012` is
resolved by the Plan registry and reuse of this single research node; resolution does not erase
its history.
