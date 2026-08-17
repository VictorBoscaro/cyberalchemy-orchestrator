---
tags: [agents-communication-infra, typed-graph, research, phase-1]
node_type: research-findings
is_session: false
layer: [architecture, domain, application]
nature: [informational, evidence]
status: draft
veracity: medium
version: 0.1.0
last_updated: 2026-08-17
---

# Typed Interaction Graph Basis — Exploration Findings

## Phase result

The explored evidence supports a typed graph whose edge relations state semantic obligations, while
topology, workflow recipes, policy, and runtime mechanics remain separate layers. It does **not** yet
establish a universally minimal basis.

For the local corpus, the strongest provisional basis is:

| Candidate relation | Meaning | Phase-1 disposition |
|---|---|---|
| `requires` | The target cannot become eligible until a source condition is satisfied. | Retain. Local execution dependencies cannot be reduced to payload delivery or authority. |
| `supplies` | A versioned source artifact or result becomes admissible input/evidence for the target. | Retain. The current sequential compiler already distinguishes delivery from launch authority. |
| `assessed_by` | A subject is examined and an assessment is returned without itself deciding progression. | Provisional. Synthesis must test whether this is an irreducible relation or a composition of `supplies` plus typed node roles and artifacts. |
| `gates` | A decision with scoped authority controls progression or acceptance. | Retain. Review evidence and authority are observably distinct. |

Two additional candidates are required by the external counterexamples, but are not yet admitted to
the basis:

| External candidate | Counterexample it preserves | Required synthesis test |
|---|---|---|
| `delegates` | A manager retains responsibility while a specialist performs bounded work and returns a result. | Determine whether this is only `requires` + `supplies` with role metadata, or whether retained responsibility changes the relation's observable semantics. |
| `transfers_control` | The active agent or task owner changes, carrying a defined context and future decision responsibility. | Determine whether ownership transfer can be represented without loss by a gate plus state mutation, or requires its own relation. |

This is deliberately a candidate set, not the research verdict. The local derivation is in
[`generative-basis.md`](generative-basis.md); authority and information-flow counterexamples are in
[`authority-evidence.md`](authority-evidence.md); the external witnesses are in
[`current-solutions.md`](current-solutions.md).

## What the current labels actually hide

The current labels `sequential`, `zig-zag`, and `feedback` mix several independent concerns:

- dependency and activation;
- delivery of artifacts, messages, or evidence;
- assessment and decision authority;
- topology such as fan-out, fan-in, branch, and back-edge;
- policies such as quorum, convergence, loop bounds, timeout, and partial failure;
- runtime mechanics such as checkpoint, retry, cancellation, and resumption.

That makes equal-looking edges ambiguous and makes different-looking workflows duplicate the same
primitive semantics. The local inventory also shows that schema acceptance is not execution:
`sequential` has a tested handoff compiler but cannot currently progress from upstream execution to
downstream compilation without an externally materialized handoff; `zig-zag` and `feedback` are not
compiled by the runtime. See [`local-as-built.md`](local-as-built.md).

## Reconstruction of the named patterns

The evidence favors treating the named communication modes as recipes over relations, graph
combinators, and policy:

| Pattern | Provisional reconstruction |
|---|---|
| sequential | dependency plus evidence delivery; authority does not transfer merely because output is delivered |
| review | subject supplied to one or more assessors, assessments returned, and an explicit gate deciding acceptance or rework |
| zig-zag | repeated review recipe with the same or identified assessors, revision evidence, convergence policy, and loop cap |
| feedback | an assessment or observation supplied back to a producer, with a separate policy deciding whether response or revision is required |
| robot-talks | fan-out of independent perspectives, cross-supply or cross-assessment, consolidation, and an optional human gate |

No explored evidence requires any of those five names to be a primitive edge type. Their important
differences reside in composition, role constraints, authority, visibility, and termination.

## Current-solution evidence

The external sweep examined current official material for OpenAI Agents SDK, LangGraph, Google ADK,
Microsoft Agent Framework, and CrewAI; AutoGen was retained only as an adjacent maintenance-mode
precedent. The sample converges on graph/state execution, conditional routing, joins, loops,
interruption, and durability, but none presents a proven minimal algebra of semantically typed
agent-interaction relations.

The most useful market signal is negative and architectural: topology is usually first-class, while
the semantics of advice, evidence, review authority, quorum, and convergence remain in application
code or higher-level orchestration. The strongest positive semantic distinction is independently
witnessed by OpenAI Agents SDK and Microsoft Agent Framework: delegation with return is not the same
as handoff or transfer of active ownership. The detailed, date-qualified comparison and official
links are in [`current-solutions.md`](current-solutions.md).

## Constraints carried into synthesis

The synthesis phase must:

1. test every candidate for necessity using a counterexample that loses observable behavior when the
   candidate is removed;
2. test collapse pairs, especially `assessed_by`, `delegates`, and `transfers_control`;
3. reconstruct all five local patterns without making them primitive edge labels;
4. keep relation semantics separate from topology, node roles, payload schemas, policy, and runtime
   effects;
5. distinguish “minimal for the examined corpus” from “universal”; the latter is not supported by
   this evidence;
6. state what remains in application code or recipe definitions and what the runtime must enforce.

## Evidence boundary

This phase establishes a grounded candidate vocabulary and counterexample set. It does not yet
validate necessity, sufficiency, implementability, or universality. Those claims require the
separate synthesis and adversarial gates defined by the staged execution decision.

