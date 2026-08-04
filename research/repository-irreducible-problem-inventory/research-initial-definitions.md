---
tags: [agents, architecture, objectives, problem-inventory, research-brief]
artifact_kind: research-initial-definitions
layer: project
status: proposed
version: 0.5.0
created_at: 2026-08-04T14:38:34-03:00
updated_at: 2026-08-04T17:34:05-03:00
related_plan: plans/governed-agent-work-infrastructure/PLAN.md
---

# Research Initial Definitions: Repository Irreducible Problem Inventory

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Governed Agent Work Infrastructure Plan](../../plans/governed-agent-work-infrastructure/PLAN.md) | `is-part-of` | The planned investigation's eventual result will inform the root infrastructure Plan's problem framing and architectural boundaries. |
| [Foundational Kernel and Formalization definitions](../foundational-kernel-and-formalization/research-initial-definitions.md) | `contextualizes` | The earlier kernel-focused boundary supplies a narrower related formulation for comparison in this cross-repository investigation. |
| [Exploration research](stages/exploration/research.md) | `grounds` | This brief supplied the confirmed questions, evidence boundaries, and non-collapse criteria used by the first exploration stage. |
| [Exploration findings](stages/exploration/findings.md) | `grounds` | The exploratory findings remain bounded by this brief and do not promote a final irreducible inventory. |

## Context

This project develops infrastructure that keeps agent work connected to the objectives, decisions,
assumptions, actions, and evidence that give it meaning. It governs decomposition,
handoffs, observation, evaluation, and reconnection to source objectives so that locally correct
work does not silently become globally wrong work.

This repository and the sibling `../domainspec-core` contain overlapping formulations of why such
infrastructure is needed, including purpose linkage, collective-judgment quality, authority
containment, semantic composition, provenance, execution fidelity, observability, revisability,
typed intent, evidence-grounded correspondence between intent and reality, and systems that build
other systems. Without a defensible account of the relationships among these formulations,
foundational scope and architectural boundaries remain unstable, risking both false unification
and unnecessary separation.

## Purpose

This document establishes the informational boundary for an investigation across
`cyberalchemy-orchestrator` and `../domainspec-core` of the smallest defensible problem set. The
result will inform later architecture framing, kernel scope, objective composition, and decisions
about which concerns require independent owners or contracts.

It is not a problem inventory, architectural verdict, research plan, dispatch configuration,
implementation authorization, or claim that one problem is already foundational.

## Research Question (Can be refined)

Which problem formulations expressed across `cyberalchemy-orchestrator` and
`../domainspec-core`, if any, remain distinct under a defensible and refinable irreducibility
criterion; how do they relate to the repositories' authoritative objective formulations; and what
standing does loss of linkage between decomposed agent work and its source objective have among
them?

## Confirmed Product Constraints

- The project must keep agent work connected to the objectives, decisions, assumptions, actions,
  and evidence that give it meaning.
- Local correctness is insufficient when work no longer serves its larger purpose.
- The infrastructure governs decomposition, handoff, observation, evaluation, and connection back
  to source objectives.
- The goal is improved collective judgment through structurally different perspectives,
  independent checks, and explicit preservation of what each result supports, not maximization of
  agent count.
- Models and conclusions remain revisable.
- A connection may be followed only where its composition has been licensed; proximity, lineage,
  or execution alone must not manufacture meaning or authority.
- Proposal-only artifacts and hypotheses must not be treated as accepted specifications,
  implementation evidence, or runtime authority.

## Current Evidence Baseline

- `AGENTS.md` states that the project keeps agent work connected to the objectives, decisions,
  assumptions, actions, and evidence that give it meaning, and that it seeks improved collective
  judgment through structurally different perspectives and independent checks.
- `README.md` states that the reason work may be relied on should be recorded, typed, and traversed
  only through licensed compositions; it also names correlated bias, noise, and framing as
  hypothesized failure modes.
- `plans/governed-agent-work-infrastructure/PLAN.md` is the single root Plan for the infrastructure
  and includes decision hygiene, agent-language research, runtime/ACI, observability, and control
  surfaces under that boundary.
- `plans/governed-agent-work-infrastructure/essays/target-architecture-hypothesis/essay.md` proposes
  a durable connected record while explicitly leaving several load-bearing decisions open. The
  kernel-of-kernels acceptance boundary is not in that essay; it appears in the derived x-ray below,
  which files it under new hypotheses rather than inherited claims.
- `research/foundational-kernel-and-formalization/research-initial-definitions.md` already records
  that kernel structure is a research subject rather than a preselected answer and that several
  kernel-like responsibilities may remain distinct.
- `experiments/tracking-spine-primitives/criterion.md` (status proposal, `authority: proposal-only`,
  `freeze_state: not-frozen`) proposes a mechanical reduction test over candidate constituents — a
  constituent is necessary when at least one sampled link cannot be expressed without it — and states
  it becomes pre-registered only on owner acceptance at a human gate. No probe has been run against
  it.
- `plans/governed-agent-work-infrastructure/plans/agent-work-language-research/CANDIDATE-INVARIANTS.md`
  records candidate invariants K1–K7 as research input directed at removal, splitting, derivation, or
  falsification, and records that a Lean mechanization probe was authored out-of-sequence, ahead of
  the subplan's staged review at step 8, and run against them. Two findings survived an adversarial
  pass, against K7 and against K1 and K2, and
  no candidate has been changed or ratified in response. The same entry states that the probe
  contains no transition system, so minimality test 2, independence, is not answered by it.
- `CANDIDATE-INVARIANTS.md` carries frontmatter dated 2026-07-25, and its Lean-probe record was
  committed 2026-07-26, both before the target-architecture essay's frontmatter date of 2026-07-27
  and its first commit on 2026-07-28. `criterion.md` carries the same frontmatter date as the essay
  and was committed the same day. Neither of the two cites the essay.
- No completeness-probe result is recorded in this repository: no artifact carries a probe outcome in
  the three-value result vocabulary the sibling card prescribes.
- Three parts of the sibling repository have been sampled: one of fifty-six `CAV2-D` definitions in
  `authority/definitions/DEFINITIONS.md`, two of four cards in `cyberAlchemy-v2/disciplines/cards/`,
  and none of the three files in `cyberAlchemy-v2/authority/constitutions/` have been read. Further
  authority material sits outside those three and is unread: `authority/imports/` holds 536 files,
  531 of them under `house_project/`; `authority/decisions/` holds eight; and `authority/definitions/`
  holds five further files beside `DEFINITIONS.md` plus three subdirectories, alongside
  `AUTHORITY-MODEL.md`, `boundaries.md`, and `promotion-policy.md`.
- `../domainspec-core/AGENTS.md` frames DomainSpec as typed intent, Arcanum as reusable operational
  capability, and Saturn as the evidence loop connecting intent and reality under an authority
  spine; it states the umbrella objective as building a system that builds other systems.
- `../domainspec-core/README.md` describes DomainSpec and a Meta-Meta Framework as intertwined
  research projects and separates research claims, implementation, validation, and evidence
  sources.
- `../domainspec-core/cyberAlchemy-v2/authority/definitions/DEFINITIONS.md` records `CAV2-D21`
  (status active) requiring every governed action to bind, create, or record typed residue for a
  classification, schema, human-continuation, and machine-checkable facet before it may govern
  downstream work, and states the rule is not a promotion gate by itself and not proof of authority,
  promotion gates being stricter downstream uses of the same method.
- `../domainspec-core/cyberAlchemy-v2/disciplines/cards/provisional-model-stewardship.md` (status
  candidate) treats a finite member set as a candidate frame carrying a status separate from its
  members', requires a recorded completeness probe before the set is presented as complete, and
  requires the bounded context the model was derived inside to be marked. Its Evidence section
  already records three sibling-repository sets presented without a completeness probe: the
  "three altitudes of one spine" framing, the `AUTHORITY-KINDS.md` candidate-kinds table, and the
  discipline status ladder.
- `../domainspec-core/cyberAlchemy-v2/disciplines/cards/stable-repository-stewardship.md` (status
  candidate) governs turning dispersed material into a stable surface without collapsing authority
  boundaries, and names the route owning each promotion rather than promoting.
- `plans/governed-agent-work-infrastructure/essays/target-architecture-hypothesis/x-ray/infrastructure-context-rich.html`
  records candidate global invariants, among them non-manufacture of authority by projections,
  non-transmission by lineage, witnessed derivations, reconstructable history, local validity not
  implying compatibility, and checker acceptance not implying enforcement. It also records a
  provisional per-guarantee scope classification for R1–R7, two named translation-fidelity operators
  diagnosing collapsed and unexplained distinctions, and open decisions OD-K1–K7 and OD-C1–C4
  recorded without owners, among them OD-K3 on translation fidelity. The same page files the
  kernel-of-kernels boundary and that fidelity vocabulary together under its own new hypotheses, so
  the two are co-originated. It is labeled proposal and not implementation evidence.
- `plans/governed-agent-work-infrastructure/essays/target-architecture-hypothesis/essay.md` states at
  line 233 that six of nine rows cite no repository gate and at line 320 that four rows cite no gate
  in repository; the x-ray records the same disagreement as a preserved source inconsistency rather
  than resolving it.

## Known Gaps

- It is not known whether loss of objective linkage is a foundational problem, a system-level
  symptom, or a compressed statement covering several independent problems.
- The repository's different problem formulations have not been reduced against one another using
  a consistent irreducibility criterion.
- It is unclear which formulations describe failures in judgment, meaning, authority, memory,
  coordination, execution, evaluation, or governance, and which cross those boundaries.
- It is not established whether provenance loss, authority drift, semantic incompatibility,
  correlated judgment, execution divergence, and failure to evaluate realization can be derived
  from one another.
- It is not established whether repository artifacts consistently distinguish a problem, an
  architectural response, a required property, and an implementation mechanism.
- The relationship and authority standing among differing project-level objective formulations
  have not been reconciled.
- It is unclear whether the sibling repository's “system that builds other systems” objective and
  intent-to-reality loop expose additional irreducible problems or restate governance,
  correspondence, and revisability concerns already present here.
- It is not known whether the kernel hypothesis addresses a foundational problem, only one class of
  cross-domain failure, or several concerns that should remain separately governed.
- It is not established whether the sibling repository's governed authority formulations name
  problems distinct from those formulated here, or restate them inside a different derivation
  context.
- Whether the sibling material read so far is representative of its authority set as a whole is not
  known.
- No irreducibility criterion has been established for this investigation, and the fitness of the
  candidates that exist — the x-ray's fidelity operators and the repository's unfrozen reduction
  criterion — is unknown.
- It is not known whether a criterion co-originated with the kernel hypothesis can be used to judge
  that hypothesis without the result being circular.
- It is not known whether premature closure is affecting the problem formulations themselves.
