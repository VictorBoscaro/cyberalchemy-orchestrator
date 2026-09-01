---
node_type: agent-dialogue
status: closed
date: 2026-08-31
topic: confirmed-dispatch-next-increment
---

# Robot-Talks: ConfirmedDispatch next increment

## Scope

Determine the smallest safe increment that turns explicit user approval observed through chat into
durable `ConfirmedDispatch`, `Run` and confirmed-turn-graph authority, so that TASK-CONT-001 may be
reconsidered without weakening the accepted authority boundary. This investigation audits and
recommends; it does not implement.

## Central question

What is the smallest safe increment that transforms chat approval into `ConfirmedDispatch`, `Run`
and a confirmed turn graph, and what evidence must exist before TASK-CONT-001 readiness can reopen?

## Assumptions challenged

1. A natural-language approval such as "pode seguir" can be bound unambiguously to the exact
   `DispatchSpec` being approved.
2. The host can supply sufficient user-principal and approval-observation evidence.
3. Chat now and a future UI can invoke the same confirmation operation without changing authority
   semantics.
4. The current `ConfirmRuntimeDispatch` contract covers preallocation of the continuation graph and
   its two mappings.
5. Existing SQLite, journal, artifact and effect seams can accept the confirmation boundary with the
   required atomicity.
6. Provider continuation and TASK-CONT-001 implementation can remain outside this prerequisite.

## Approved strategy

The repository owner approved the strategy in chat on 2026-08-31.

### Investigator 01 — Authority and product

- Concern: semantics and evidence of human approval, exact dispatch binding and chat/UI equivalence.
- Central question: what must the confirmation ingress prove before runtime authority may exist?
- Exclusions: table design, migration mechanics and continuation/provider implementation.

### Investigator 02 — Persistence and transaction

- Concern: minimum persisted model, atomic journal acceptance, artifacts, events and effects.
- Central question: what is the smallest technically coherent writer transaction supported by the
  current runtime seams?
- Exclusions: user-interface design, natural-language UX and provider continuation behavior.

### Investigator 03 — Slicing and verification

- Concern: smallest independently reviewable SWU, tests, failpoints and readiness exit criteria.
- Central question: what bounded implementation and evidence package should precede TASK-CONT-001?
- Exclusions: redefining human authority, detailed UI design and implementing later continuation
  tasks.

## Alternative decomposition rejected

A decomposition by files (`domain.md`, `operations.md`, migration, `service.py`, tests) was
considered. It was rejected because the authority, atomicity and readiness obligations cross those
files, causing investigators to duplicate questions instead of exposing tensions between product,
contract and runtime layers.

## Conversation protocol

Each investigator works independently and reports:

1. Key Findings — three to five evidence-backed findings with file/line references.
2. Gaps or Inconsistencies.
3. Local Tensions.
4. Questions for Synthesis.

Synthesis will identify cross-layer tensions rather than merge summaries. No implementation action
is authorized until the repository owner disposes each material tension at the human gate.

## Agent prompts

The prompts above are the authoritative concern boundaries. Each report must stay within its
assigned concern, distinguish specification from implementation evidence and avoid implementation.

## Timeline

- Strategy approved by repository owner: 2026-08-31.
- Exploration: complete; three independent reports preserved under `reports/`.
- Synthesis: complete; seven cross-layer tensions recorded in `findings.md`.
- Human gate: approved by repository owner on 2026-08-31.

## Exploration reports

- [01 — Authority and product](reports/01-authority-product.md)
- [02 — Persistence and transaction](reports/02-persistence-transaction.md)
- [03 — Slicing and verification](reports/03-slicing-verification.md)

## Synthesis

The investigation found that the next action should be a non-code contract/golden-vector closure,
followed by one bounded durable writer SWU ending at `opening_pending`. The material tensions are:
approval-observation evidence, missing bounded bytes-to-graph projection, implicit graph
preallocation, missing effect outbox, identity-level replay, stale work-pack state/migration
collision and legacy foreign-key dependence. See [findings.md](findings.md) for evidence and proposed
dispositions.

## Human gate notes

The repository owner approved the recommended package: CONF-000 before CONF-001; an immutable
confirmation-observation contract; a generic effect-intent outbox; `opening_pending` as the writer
exit boundary; staged legacy-FK decoupling; migration 012 for CONF-001 and 013 for TASK-CONT-001.

The Robot-Talks investigation is closed. Its disposition authorizes a separate CONF-000
planning/contract route, not runtime mutation or an implementation claim.
