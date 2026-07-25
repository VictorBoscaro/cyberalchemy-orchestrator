---
tags: [agents, architecture, category-theory, lean, formalization, research-brief]
node_type: research-initial-definitions
is_session: false
status: proposed
version: 0.2.0
last_updated: 2026-07-24
related_plan: plans/agent-language-research-program/PLAN.md
target_document: docs/architecture/agent-language-system-view.md
---

# Research Initial Definitions: Agent-Language Mathematical Formalization

## Context

The project is developing a compositional and governable language for describing, relating,
authorizing, executing, and observing human and agent work. Its current high-level system view
contains candidate concepts for identity, properties, tags, typed relations, recursive work,
authority, lifecycle facts, projections, Dispatches, and formal verification, while deliberately
leaving their final boundaries open.

The system view now needs a mathematical appendix that can expose ambiguity, composition laws,
incompatible assumptions, and proof obligations before implementation choices harden. This matters
because a formal model can improve precision only when its constructs correspond explicitly to
the responsibilities and authority boundaries of the original infrastructure.

## Purpose

This document establishes the starting context for research that will inform the mathematical and
Lean formalization appendix of the high-level system view. That appendix will support later
ontology, architecture, specification, validator, and implementation decisions.

It is not the mathematical model, a Lean implementation, a proof, a research plan, a Dispatch, or
runtime authority.

## Research Question (Can be refined)

How should the agent-language system be expressed first in human-readable mathematics and then in
Lean so that its identities, typed relations, composition, recursive work, authority, lifecycle,
projections, and formal claims remain traceable to their original infrastructure responsibilities
without confusing model soundness, product correspondence, and execution authority?

## Confirmed Product Constraints

- The final part of the high-level system document must include a mathematical formalization and a
  subsequent Lean formalization.
- Category theory must be considered and used where it contributes real semantic or compositional
  structure. Other mathematics may be used where needed.
- Human-readable mathematical notation precedes Lean encoding.
- Every formal concept must link to the original infrastructure concept or artifact and explain the
  responsibility it models.
- The formalization must distinguish definitions, assumptions, candidate axioms, invariants,
  propositions, counterexamples, proof obligations, and machine-checked results.
- A mathematical or Lean result does not independently establish product correspondence, runtime
  truth, promotion, or execution authority.
- The formalization must preserve the distinction between structural recursive work and recursive
  orchestration authority. An invoked orchestrator must not invoke another orchestrator.
- Confirmed constraints, candidate invariants, architectural hypotheses, analogies, and open
  questions must not be assigned the same formal status.
- Each proposed correspondence must state whether it is direct, adapted, analogy-only,
  conflicting, or insufficiently supported.
- The mathematical appendix and every governed research, planning, design, specification,
  formalization, review, or decision artifact must contain an explicit `Open Questions` section.
  Resolved, superseded, deferred, rejected, or out-of-scope questions remain historically
  traceable.

## Current Evidence Baseline

- The current
  [system view](../../docs/architecture/agent-language-system-view.md) supplies the explanatory
  target and a planned formalization appendix.
- The
  [agent-language research plan](../../plans/agent-language-research-program/PLAN.md) makes kernel
  topology, composition, finite bootstrap, authority, and Lean boundaries first-phase questions.
- The
  [foundational definitions](../foundational-kernel-and-formalization/research-initial-definitions.md)
  preserve the current confirmed constraints and gaps around objects, relations, tags, workflow
  profiles, semantic materialization, and Lean.
- The invocation and event-driven initial definitions record existing boundaries for context
  materialization, confirmed Dispatch authority, lifecycle facts, projections, and no nested
  orchestrator invocation.
- `../domainspec-lean-formalization` contains documentary material on ontology conventions,
  categorization, composition, functors, reflection, and proof-bounded claims.
- DomainSpec-v2 and CAV2 material in `../domainspec-core` contains definitions and evidence about
  meta-types, typed relationships, invariants, authority, provenance, promotion, and validators.

## Known Gaps

- It is not settled what the primitive mathematical carriers should be or whether one notion of
  object is sufficiently discriminating.
- It is unclear which relation kinds should be morphisms, indexed morphisms, spans, profunctors,
  predicates, proof-relevant records, or another structure.
- Composition is not defined, including compatibility, partiality, precedence, conflict,
  transitivity, inheritance, cycles, and local-to-global preservation.
- The appropriate mathematical treatment of version, provenance, validity, authority, evidence,
  and temporal lifecycle is not established.
- It is not known whether workflow profiles and recursive work are best represented by categories,
  graphs, transition systems, operads, type systems, indexed structures, or a combination.
- The boundary among authoritative direct facts, derived closures, projections, and executable
  effects is not formalized.
- A finite bootstrap boundary for kernel or contract conformance has not been expressed
  mathematically.
- It is unknown which claims are stable enough for Lean, which need executable validators, and
  which remain empirical, governance, or product judgments.
- The correspondence criteria between mathematical structures, Lean definitions, infrastructure
  artifacts, and runtime observations are not defined.
- The minimal theorem and counterexample set needed to falsify an inadequate formalization is not
  established.
- The identity, status vocabulary, ownership, evidence links, closure criteria, reopening
  semantics, and cross-artifact references for Open Questions are not yet defined.
