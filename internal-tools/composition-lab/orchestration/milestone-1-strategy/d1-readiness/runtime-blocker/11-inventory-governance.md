---
artifact_kind: inventory-governance-assessment
status: go-bounded-bootstrap
date: 2026-08-13
scope: executable descriptive inventory for D1
---

# Inventory ownership and execution governance

## Verdict

**GO, conditionally, for an Inventory-owned bounded/unregistered bootstrap. NO-GO for registering
`inventory` as a LIVE dispatch capability now.**

`inventory` already owns the semantic process and durable outputs D1 needs: `ingest`, `backfill`,
`lookup`, `lint`, and `validate`; source-backed evidence-cards; candidate EvidenceSets; human and
machine indexes; contradiction, trace, residue, and non-authority rules
([Inventory](../../../../../../.agents/skills/inventory/SKILL.md)). What it does not yet own is an
executable delegated workflow: roles, topology, confirmation, source/mutation boundaries, terminal
conditions, and a single acceptance verdict. That is a lifecycle gap, not evidence of a new
dispatch identity.

The independent check reached the same recommendation: use a bounded Inventory-owned helper first,
and register only after repeated use demonstrates a stable lifecycle and stable consumers. This
also follows the local discovery precedent: a capability with no LIVE type may explicitly own a
bounded bootstrap, while the routing skill says such a workflow terminates inside its capability
([discovery-writing](../../../../../../.codex/skills/discovery-writing/SKILL.md),
[strategy](../../../../../../.agents/skills/domainspec-subagents-strategy/SKILL.md)).

## Why registration is premature

The canonical registry currently exposes routable identities only for `research`,
`domainspec-implement`, `review`, and `experiment`; `others` is deliberately non-routable
([registry](../../../../../../implementations/contracts/dispatch-type-registry.v1.json)). A new LIVE
type would assert that Inventory has a stable, generally reusable dispatch lifecycle. The evidence
supports only one blocked D1 use and a rich inline skill contract. It does not yet establish stable
agent cardinality, topology, approval semantics, artifact consumers, or recurrence.

Registration also creates unnecessary runtime surface now: resolver/compile/open/close behavior,
ledger projection, binding fixtures, and compatibility obligations. A bounded bootstrap can test
the missing operational contract without claiming durable dispatch-type maturity.

**Promotion trigger:** reconsider registration after at least two additional materially distinct
Inventory delegations reuse the same topology, acceptance contract, and output boundaries, and at
least one downstream consumer successfully consumes the machine index/evidence-card handoff. If
those uses require different lifecycles, keep Inventory inline/bounded rather than hiding the
variation behind one generic dispatch type.

## Ratification and authority

Three approvals are distinct:

1. **Capability ratification:** the owner/maintainer of the canonical Arcanum `inventory` source
   ratifies the bounded bootstrap and its semantic boundary. The installed `.agents`/`.codex`/
   `.claude` copies declare generated-source mutation policy and therefore must not be treated as
   independent authorities. The declared canonical path `arcana/inventory/SKILL.md` was not found
   in this checkout; locating or restoring that source is a hard precondition to mutation.
2. **Run authorization:** the human confirms the complete bounded proposal—sources, targets,
   roles, prompts, budgets, topology, outputs, and mutation boundary—before any seat launches.
3. **Artifact acceptance:** the parent orchestrator may verify mechanical completion, but cannot
   promote candidate Inventory records into definitions, ontology, or claims. Those remain with
   Definitions Governance, Ontology Vault, or Research as already declared by Inventory's
   authority rule.

If a LIVE route is later proposed, the dispatch-registry/runtime owner must separately ratify it;
capability ownership alone cannot mutate infrastructure authority.

## Minimum bounded-bootstrap contract

Add one narrow orchestration section to the canonical Inventory skill, then regenerate all native
surfaces. It should define:

- **Applicability:** delegated, repository-local descriptive extraction where independent source
  partitions or an independent completeness check materially help; ordinary lookup remains inline.
- **Bounded topology:** one or more isolated read-only extractors over disjoint frozen source sets;
  exactly one controlled assembler that writes only the confirmed Inventory root; one independent
  coverage auditor reading the frozen assembled result. No robot-talks and no dynamic seat creation.
- **Proposal/gate:** predeclare every seat, lens, immutable prompt, source paths/digests, budgets,
  outputs, mutation scope, retry/round ceiling, and confirmation mode. Material changes require
  reconfirmation. This is workflow evidence, not a ledger dispatch or ACI receipt.
- **Native outputs:** evidence-cards/entries plus `index.json`, `index.md`, tags/log, and validation
  report. Raw extractor returns remain preserved as session evidence; they are not `findings.md` and
  are not silently upgraded into authoritative entries.
- **Terminal verdict:** `PASS | BOUNDED_CORRECTIONS | BLOCK`. `PASS` means frozen-corpus coverage,
  source linkage, schema validity, index parseability, explicit absences, and preserved ambiguity
  all pass. It says nothing about novelty, truth beyond the cited source, lens definition, or causal
  compositional effect.
- **Stop behavior:** stop on missing source binding, unauthorized mutation, schema/index failure,
  conflicting writes, exhausted correction ceiling, or any request for adjudication outside
  Inventory authority. Return residue and a typed handoff; do not reroute silently to Research.

For D1 specifically, the local schema must enumerate every frozen source/control and record an
occurrence or explicit absence. Permitted descriptive states include `prescribed`, `instantiated`,
`executed`, `effect-observed`, and `unknown`, but `effect-observed` requires a direct trace; absence
of such a trace becomes `unknown`, never an inferred negative.

## Hard discriminator: Inventory versus Research

Inventory answers: **what source-backed occurrence, absence, ambiguity, contradiction, or trace is
present, and where?** Research answers: **which claim survives precedent, witness, soundness, and
novelty adjudication?**

The bounded workflow must forbid Inventory workers and its terminal verdict from:

- defining what a lens or composition is;
- treating descriptive categories as validated constructs;
- attributing causal effect from co-occurrence;
- producing novelty, `GO/KILL`, witnessed/sound, or theory-selection verdicts;
- resolving ambiguity by majority vote or assembler preference.

When such a question appears, Inventory records it as candidate/inference/open question with source
refs and names a separate Research handoff. This avoids both failure modes: misrouting descriptive
collection into Research's verdict matrix, and allowing Inventory to become “research without
verdicts.” The existing D1 routing assessment already establishes this boundary
([07](07-capability-routing.md)); the Research adjudication confirms that a verdict-free inventory
does not fit Research's current contract ([08](08-research-contract-adjudication.md)).

## Minimal change set

### For the recommended bounded route

1. Locate/restore `arcana/inventory/SKILL.md`; amend that canonical source only.
2. Add the bounded-bootstrap contract above and regenerate `.agents`, `.codex`, and `.claude`
   Inventory packages with the repository generator.
3. Add static conformance checks that generated copies equal the canonical source and that the
   bootstrap declares roles, topology, boundaries, confirmation, outputs, validation, terminal
   verdict, and non-registration language.
4. Add two skill-level fixtures: a passing frozen-corpus D1 inventory and a failure containing an
   unsupported lens/effect verdict. Verify explicit absence, ambiguity preservation, parseable
   `index.json`, immutable raw inputs, and `BLOCK` on authority escape.
5. Reassess D1 routing. Do **not** edit the dispatch registry, appender, lifecycle, or runtime for
   this option.

### Only if later promoted to a registered capability

Add a dedicated registry type/capability route (do not overload `others`), a capability-owned
opening/acceptance contract, resolver and compiler fixtures, ledger schema acceptance/rejection,
open/binding/close integration tests, and routing tests proving Inventory cannot silently fall back
to Research. The registry and lifecycle owners must ratify those changes separately.

## GO conditions for D1 launch

D1 may proceed through the bounded bootstrap only when:

- the canonical skill source exists and contains the ratified lifecycle;
- generated surfaces are synchronized;
- the exact frozen corpus, Inventory root, schema, seats, prompts, budgets, and mutation boundary
  receive human confirmation;
- the two conformance fixtures pass; and
- the final contract contains the Inventory/Research discriminator and `PASS | BOUNDED_CORRECTIONS |
  BLOCK` acceptance semantics.

Until all five hold, the operational verdict remains **NO-GO / BLOCK**. The recommended governance
decision is nevertheless **GO to implement the bounded bootstrap**, not GO to launch D1 immediately.
