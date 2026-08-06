# Refine Seed Proposal: Transport-Neutral RWO Adapters

Status: confirmed, consumed, and closed; retained as historical seed evidence  
Run ID: `20260806T032327Z-rwo-transport-neutral-adapters`  
Preset: `full`  
Research mode: `bounded-research`  
Target: `docs/features/recursive-work-orchestrator/`

The confirmation bound this exact seed and its material projection. The
resulting review dispatch is closed and this artifact grants no reusable
authorization for later implementation or promotion.

## Operator Intent

Refine the RWO command and event adapter boundaries so that implementations can
use gRPC, sockets, Redis-backed queues, managed event buses, or an in-memory
transport without making transport behavior part of RWO policy, authority, or
domain meaning.

The intended result is not a claim that every adapter is interchangeable. The
bounded claim to test is:

> An adapter is RWO-conformant only when it implements a small protocol core,
> declares a capability profile, exposes delivery observations without turning
> them into lifecycle decisions, and passes the profile's positive and negative
> conformance fixtures.

## Current Evidence Boundary

Local owner evidence:

- `../../../DESIGN.md`, especially sections 4.3, 6, 6.1, 6.2 and invariants
  RWO-I07, RWO-I10, and RWO-I12: current candidate RWO boundary.
- `../20260805T184601Z-rwo-domain-recovery-model/RESULT.md` and
  `../20260805T184601Z-rwo-domain-recovery-model/stages/08-distill-repair.md`:
  prior candidate recovery model separating `DeliveryCase`, `ExecutionCase`,
  and `EffectCase`.
- `.arcanum/inventory/queries/2026-08-05-cyberalchemy-orchestrator-rwo-are-current-state-research-result.md`:
  discovery-only pointer to the prior RWO/ARE owner-boundary research.

Bounded external primary evidence already selected by the parent:

- `https://grpc.io/docs/guides/retry/`
- `https://grpc.io/docs/guides/flow-control/`
- `https://grpc.io/docs/guides/status-codes/`
- `https://redis.io/docs/latest/develop/data-types/streams/`
- `https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md`
- `https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-rule-retry-policy.html`
- `https://docs.aws.amazon.com/pdfs/decision-guides/latest/sns-or-sqs-or-eventbridge/sns-or-sqs-or-eventbridge.pdf`

These sources establish heterogeneous delivery, acknowledgement, ordering,
flow-control, duplicate, retry, and unknown-outcome semantics. They do not
select the RWO contract, prove an implementation, or authorize effects.

## Problem To Refine

The current design correctly treats the work protocol bus as a logical boundary,
but it does not yet define the smallest adapter contract or the capability
evidence required to use a concrete transport safely.

The Refine loop must compare and either select or reject:

1. one universal adapter interface at a lowest-common-denominator;
2. one protocol core plus optional capability profiles;
3. separate command-delivery, event-ingress, and journal/outbox/inbox ports;
4. a hybrid in which split ports share one canonical envelope and capability
   declaration.

## Exact Questions

- Are command delivery and event ingress separate ports, even when one broker
  carries both?
- Which envelope fields are canonical RWO identity and which are transport
  metadata?
- Who owns inbox, outbox, acknowledgement, journal acceptance, replay cursor,
  dead-letter handling, and consumer offset state?
- Which features belong to the mandatory protocol core, and which require
  profiles for durability, ordering, acknowledgement, replay, fan-out,
  backpressure, transactions, or request/response correlation?
- How does an adapter report delivery observations without selecting redelivery,
  new Work Attempt, repeat, replay, reconciliation, or compensation?
- What distinguishes reconnect, transport redelivery, and RWO recovery?
- What proof must RWO require before admitting an adapter/profile pair?
- Which negative fixtures expose false exactly-once, unsafe retry, authority
  collapse, silent loss, duplicate divergence, ordering drift, or journal
  substitution?
- What does an in-memory adapter truthfully support when it has no crash
  durability or cross-process delivery?

## Required Deliverables

1. exact glossary and identity table;
2. mandatory protocol-core ports and operations;
3. canonical command/event envelope model and transport-metadata boundary;
4. capability-profile vocabulary with support, evidence, and prohibition rules;
5. delivery-observation algebra that feeds but never decides RWO recovery;
6. ownership matrix for domain, RWO kernel, adapter, journal, inbox/outbox,
   ARE, ACI, and exact-effect owner;
7. state/sequence models for send, accept, redeliver, reconnect, replay, and
   unknown outcome;
8. adapter admission and conformance contract;
9. mappings for gRPC, sockets, Redis Streams, managed event buses, and memory;
10. negative fixtures and failure matrix;
11. delta against current `DESIGN.md` and candidate ontology;
12. implementation-ready but non-executed work plan.

## Hard Invariants

- Transport success is not journal acceptance, Work completion, domain truth,
  semantic truth, or effect authorization.
- Redelivery preserves logical message identity; a transport delivery attempt
  may change; a new Work Attempt is an RWO decision.
- No profile may claim exactly-once business effects from delivery behavior.
- Unknown outcome, duplicate divergence, unknown schema, unknown capability,
  and unsupported profile requirements fail closed to a named owner.
- A broker, socket, gRPC runtime, or in-memory queue does not select domain
  policy, lifecycle routing, ARE verdicts, or exact-effect authorization.
- Capability absence is explicit. It cannot be simulated by a silent fallback.
- The journal remains RWO's accepted-history authority unless a later owner
  decision changes that contract; transport offsets and acknowledgements are
  not substitutes.

## Write Scope

Writes are limited to this run folder and the required append-only DomainSpec
dispatch ledger rows after exact confirmation. Delegated roles are read-only;
the parent may capture their returned receipts under `delegated-review/returns/`.

## Forbidden Scope

- current `DESIGN.md`, ontology sources/materialized graph, runtime code, tests,
  schemas, adapters, journals, and transport implementations;
- ARE, ACI, domain, or exact-effect owner artifacts;
- canonical definitions, promotion, publication, deployment, external effects,
  or Git operations;
- any claim of runtime conformance or production readiness.

## Done Criteria

- The selected model is smaller than a transport SDK and stronger than a
  lowest-common-denominator send/receive interface.
- Every profile feature has one owner, observable evidence, and a negative
  conformance case.
- Every transport family can be mapped without changing RWO domain semantics or
  disguising unsupported behavior.
- Reconnect, same-message redelivery, new Work Attempt, repeat, replay,
  reconciliation, and compensation remain distinguishable.
- The final plan is non-executed and names future files, fixtures, and validation
  commands without mutating product, ontology, or runtime sources.
