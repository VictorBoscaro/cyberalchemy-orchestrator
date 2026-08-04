---
status: accepted
date: 2026-08-03
scope: agents-communication-infra-protocol-compilation
decision_id: ACI-PG-001
---

# ACI Protocol Governance ownership

## Decision

ACI Protocol Governance owns the contracts and lifecycle of `SkillExecutionProfile`,
`SkillProtocolBinding`, the digest-pinned reusable recipe/DAG, and deterministic compilation through
a non-authoritative `DispatchCandidate`.

The skill author or domain owner retains the skill's intent, obligations, deliverables, sources and
quality criteria. ACI confirmation retains effective capability resolution, final canonical
`DispatchSpec` bytes and digest, human acceptance, `ConfirmedDispatch` and `Run`. The ACI runtime
retains scheduling, attempts, effects, recovery and replay. Work Bus, audit-ledger/appender and APT
retain their existing routing/message, YAML-materialization and provenance boundaries.

## Authority boundary

```text
skill revision + governed profile/binding + recipe/DAG + invocation
  -> ACI Protocol Governance
  -> non-authoritative DispatchCandidate
  -> ACI confirmation and capability resolution
  -> human acceptance of exact DispatchSpec digest
  -> ConfirmedDispatch / Run authority
```

Protocol compilation cannot grant a capability, confirm a dispatch, create a `Run`, select a
provider, schedule a node or emit an external effect. A recipe/DAG is reusable protocol input, not a
parallel execution authority.

## Rationale

This separation prevents a skill author from self-authorizing execution, prevents the runtime from
silently defining reusable protocol semantics, and preserves the confirmed `DispatchSpec` as the
single executable authority. It settles OQ-ACP1 and OQ-ATD3 without promoting unrelated candidate
decisions.

## Source and consequences

The repository owner explicitly selected this recommendation in the active 2026-08-03 session and
authorized its promotion through discovery, SPEC, review, work-pack and bounded implementation.
Schemas, operations and implementation status still require their own specification, tests and
gates; this ownership decision alone does not claim that protocol compilation is implemented.

