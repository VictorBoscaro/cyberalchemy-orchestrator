# Refine Seed Proposal: RWO Degrees of Freedom

Status: proposed; no stage execution authorized  
Run ID: `20260813T122459Z-rwo-degrees-of-freedom`  
Preset: `standard`  
Research mode: `research-if-gap-appears`  
Target: `docs/features/recursive-work-orchestrator/`

## Operator intent

Frame a research program that determines which degrees of freedom the system should expose now,
which should remain unavailable in V1, which may become available under explicit permission later,
and which authority-creating actions should remain non-delegable.

The motivating example is that V1 may compose recursive work but must not allow an orchestrator,
composite, or delegated seat to instantiate another independently authoritative orchestrator.

## Research objective

Produce a decision-ready capability envelope for V1 and an evidence-gated evolution path. The
research must separate:

1. **expressivity** — what the system can describe;
2. **authority** — who may approve an action;
3. **capability** — the exact action, resource, phase, duration, and limits granted;
4. **enforcement** — what a runtime, adapter, sandbox, or external system actually prevents;
5. **evidence** — what proves that an action stayed inside the envelope.

## Primary research question

> How should CyberAlchemy define and enforce degrees of freedom across the user, root
> orchestrator, composite work, delegated agents, tools, and effect adapters so that V1 remains
> useful without recursive authority or silent scope amplification, while preserving an explicit,
> evidence-gated path to broader future capabilities?

## Subquestions

- What exactly can “the orchestrator is orchestrable” mean: being a development target, being a
  composable `Work`, accepting configuration, or creating another scheduler and authority root?
- Which actors and system surfaces need distinct capability envelopes?
- Which dimensions of freedom must be explicit: graph/topology, agents, tools, model, context,
  filesystem, network, subprocesses, external effects, secrets, budget, depth, time, retries,
  persistence, policy changes, and capability issuance?
- Which V1 actions are allowed, approval-gated, unavailable, or categorically non-delegable?
- When does parentage or composition risk becoming authority inheritance?
- What must “correct permission” include: policy decision, scoped capability, physical enforcement,
  and durable receipt?
- Which current restrictions are executable fences, which are host assumptions, and which are
  advisory governance only?
- What counterexamples falsify the proposed V1 envelope?
- What evidence would justify relaxing each restriction after V1?

## Candidate thesis to test

> V1 should support broad bounded composition under one root scheduler, while every effectful or
> scope-expanding action is fail-closed behind an explicit capability and enforcement point.
> Composition, lineage, or parentage never grants authority. Creation of another authority root,
> self-issued capability, silent graph expansion, and bypass of the accepted journal are outside
> the V1 envelope.

This is a hypothesis, not a settled repository decision. Existing material contains both a
root-only direction and a documented unresolved nested-orchestrator alternative.

## Initial local evidence

- `../../../DESIGN.md:19-36,372-387,455-465` — recursive composition, shallow authority,
  fail-closed invariants, and the bounded “any pipeline” claim.
- `../../skill-control-center/meta-orchestration/findings.md` — dispatch lineage is not execution
  authority and current child lineage is incomplete.
- `../../../../agents-communication-infra/README.md` and `../../../../agents-communication-infra/specs/`
  — candidate capability, authority-mode, confirmation, and enforcement boundaries.
- `../../../../../implementations/as-built/pairs/pair-03-authority.md` — current authority-chain
  and enforceability gaps.
- `../../../../../plans/governed-agent-work-infrastructure/essays/robot-talks/2026-08-12-work-overview-composition/findings.md`
  — unresolved root-only versus nested-orchestrator contradiction.
- `../../../../../research/agent-invocation-and-collaboration-topology/research-initial-definitions.md`
  — explicit non-inheritance and remaining capability/enforcement questions.

## Required research outputs

1. a canonical glossary for expressivity, authority, capability, enforcement, evidence, parentage,
   composition, scheduler, orchestrator, and authority root;
2. an actor × action × phase capability matrix;
3. a current-state / V1 / later-target comparison that distinguishes implemented, enforced,
   conventional, proposed, and forbidden behavior;
4. the closed V1 envelope: allowed, approval-gated, unavailable, and non-delegable actions;
5. a permission chain showing authorizer, policy, capability, enforcement point, receipt, revocation,
   and denial behavior;
6. a recursive-authority threat and failure model, including authority amplification and scope
   smuggling through children, tools, adapters, retries, or dynamic graph changes;
7. scenario witnesses and negative counterexamples for ordinary composition, child dispatches,
   tool access, external effects, policy change, self-modification, and nested orchestration;
8. staged relaxation criteria: the evidence required before each V1 restriction may be widened;
9. a concise decision set and recommended V1 capability envelope;
10. a non-executed follow-up plan for the owning decision/spec artifacts.

## Non-goals

- Do not design a complete multi-tenant IAM platform.
- Do not promise that every future computation or effect will become expressible.
- Do not implement sandboxing, tokens, RBAC/ABAC, schedulers, adapters, or UI controls.
- Do not promote the RWO proposal, resolve ACI ownership, or mutate canonical specifications.
- Do not treat a declared policy or capability as proof of physical enforcement.
- Do not collapse user configurability of the root orchestrator into recursive orchestration
  authority.

## Done criteria

- Every freedom is expressed as actor, action, target/resource, phase, bound, authorization owner,
  enforcement point, evidence, and failure posture.
- “Orchestrable” has disjoint meanings and the V1 decision addresses each separately.
- Current implementation claims do not exceed code/tests/as-built evidence.
- The recommended V1 envelope is useful enough for at least three representative workflows and
  rejects at least three authority-amplification counterexamples.
- Every proposed future relaxation names prerequisite evidence rather than relying on “correct
  permission” as an unspecified phrase.
- Remaining disagreements are preserved as decisions or research residue.

## Write scope

Until a later route is separately approved, writes are limited to this refinement-run folder.
All product, runtime, design, ontology, decision, and canonical research artifacts remain read-only.

