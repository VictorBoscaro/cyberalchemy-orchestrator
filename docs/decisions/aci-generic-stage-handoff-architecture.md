---
status: accepted
date: 2026-09-01
scope: agents-communication-infra-generic-stage-handoff
decision_id: ACI-GSH-001
---

# ACI Generic Stage Handoff architecture

## Decision

Extend the existing bounded host-workflow compilation and materialization pipeline for the L0
one-producer, one-required-slot, one-consumer case. Do not introduce a standalone
`GenericStageHandoff` aggregate in this version.

The extension MUST preserve five independently evidenced durable facts. Existing ACI seams supply
evidence or execution boundaries, but none is automatically renamed into a generic fact:

| Generic fact | Selected owner and mapping |
|---|---|
| `ResultCommitment` | The host workflow runtime maps one verified `HostTerminalResponseArtifact` and receipt into a producer-bound commitment. Equal bytes from different producer turns retain different commitment identities. |
| `PublicationAuthorization` | The confirmed-dispatch authority supplies the frozen `SourceToSlotMapping` and visibility policy. After an exact commitment exists, the ACI command writer records a separate authorization fact binding that commitment, named handoff and consumer. The producer cannot issue it. |
| `ResultPublication` | The connection-handoff workflow records a separate publication-occurrence fact only after verifying the exact commitment and matching authorization. |
| `ImmutableDelivery` | `MaterializeHostWorkflowInput` verifies the publication and exact artifact, then records a distinct generic delivery identity alongside the canonical manifest and binding candidate. Materialization is not consumer acceptance. |
| `ConsumerAcceptance` | A new consumer-admission operation records that the governed host consumer boundary admitted the exact delivery. It precedes launch authorization and is distinct from scheduler authorization, provider start, access, use, reliance and claim support. |

Compilation becomes staged. The initial graph compile freezes topology, required slot contract,
producer/consumer selectors and the confirmed mapping, but cannot fabricate a result-bound source.
After the producer commitment, the runtime records authorization and publication, materializes the
exact delivery, records consumer acceptance, and only then compiles or admits the final downstream
manifest/binding and launch authorization. A required downstream launch with `slots: []` is
non-conforming.

## Authority boundary

```text
host-observed producer bytes
  -> ResultCommitment                 [host workflow runtime]
  -> PublicationAuthorization         [confirmed authority + sole command writer]
  -> ResultPublication               [connection-handoff workflow]
  -> ImmutableDelivery               [host workflow materializer]
  -> ConsumerAcceptance              [governed host consumer-admission boundary]
  -> launch authorization            [host workflow scheduler]
```

The sole journal writer persists the accepted facts, but persistence authority does not collapse
the distinct principals or boundaries responsible for them. ACI does not infer access, use,
reliance or claim support from this chain.

## Options considered

### Selected — extend the existing staged pipeline

Benefits:

- reuses exact producer receipts, confirmed source-to-slot mappings, canonical manifests,
  materialization and launch guards already specified for the bounded host-workflow slice;
- the runtime already validates ordered slot contracts and exact repository or binding-output
  sources;
- limits the first promotion to the discovery's one-producer/one-consumer boundary.

Costs and risks:

- requires new durable authorization, publication, delivery and consumer-acceptance identities and
  explicit mappings rather than aliases;
- requires the compiler to stop prebuilding launchable downstream envelopes with empty slots;
- remains host-workflow-specific and does not solve fan-in, fan-out, cross-dispatch or remote work.

### Rejected for this version — standalone `GenericStageHandoff` aggregate

This option offers transport-independent lifecycle ownership, but duplicates existing bounded
producer evidence, mapping, materialization, recovery and launch machinery before reuse has been
shown inadequate. Reopen this option if the extension cannot satisfy every collapse test without
one status, receipt, operation or actor carrying more than one fact meaning.

## Collapse-test decision record

Both candidates were evaluated against every required collapse test. The staged extension is
acceptable only while it preserves the same semantic separations that a standalone aggregate would
have to enforce:

| Collapse risk | Selected staged extension | Standalone aggregate candidate |
|---|---|---|
| Required dependency launches empty | The staged compiler/scheduler refuses launch until one exact required source, delivery, acceptance and manifest binding verify. | An aggregate transition withholds delivery, acceptance and launch eligibility until source cardinality and exact input are recorded. |
| Bytes attributed without commitment | Only a verified producer-turn receipt can create the commitment mapping. | Commitment creation consumes a verified producer receipt; aggregate identity cannot self-assert the bytes. |
| Authorization reported as publication | Separate durable identities and events; publication verifies but never aliases authorization. | Authorization and publication have distinct lifecycle states, events and receipts; authorization cannot advance publication state. |
| Publication without commitment/authorization | The publication command requires both exact predecessor identities and their current evidence. | The publication transition is guarded by the exact commitment and authorization identities. |
| Mutable bytes substituted | Delivery resolves content-addressed artifact bytes and verifies digest and size. | The aggregate stores or references the committed content digest, and delivery rejects byte, digest or size drift. |
| Delivery treated as acceptance | Consumer acceptance is a separate operation and fact after delivery. | Delivery and acceptance are separate states and events, and acceptance requires the consumer boundary's authority. |
| Acceptance creates downstream epistemic claims | Access, use, reliance and claim support remain independently evidenced outside the handoff. | The aggregate ends at acceptance and exports no access, use, reliance or claim-support fact. |
| Retry changes meaning | Same logical identity and canonical bytes return the first fact; any producer, consumer, authority, predecessor, content or meaning drift conflicts. | Transition identity and canonical payload govern idempotency; any divergent meaning conflicts. |
| Missing evidence becomes success | Every missing or ambiguous transition remains explicitly unestablished, unknown or conflicted. | A missing transition remains unestablished or unknown and cannot advance aggregate state. |

Both candidates can satisfy the required semantics. The staged extension is selected because it
reuses the bounded host-workflow seams with less duplicate authority and persistence machinery. This
matrix is architecture analysis, not implementation proof; failure to preserve any row during
implementation reopens the standalone-aggregate option.

Failure of any row blocks aggregate promotion and reopens the standalone-aggregate option.

## Source and rationale

The repository owner selected the extension recommendation in the active 2026-09-01 session after
reviewing the alternative. The decision is grounded in:

- the reviewed [discovery](../features/agents-communication-infra/discovery/generic-stage-handoff.md)
  and its five decisions;
- the accepted [semantic capability](../features/agents-communication-infra/specs/capabilities/generic-stage-handoff.md);
- existing exact producer evidence and mapping contracts in
  [domain](../features/agents-communication-infra/specs/domain.md#hostterminalresponseartifact);
- the bounded host operations in
  [operations](../features/agents-communication-infra/specs/operations.md#commithostterminalresponse);
- the compiler's current empty-slot emission in
  [`dispatch_workflow.py`](../../implementations/server/runtime/dispatch_workflow.py); and
- the runtime's existing populated-manifest validation in
  [`service.py`](../../implementations/server/runtime/service.py).

The code evidence proves validation and the current empty-slot gap; it does not prove that the
selected architecture is implemented.

## Consequences and remaining gates

- Update the ACI aggregate, architecture, domain, states, events, operations, mappings, workflows,
  interfaces, rules and test specification through a separately reviewed DomainSpec amendment.
- Red-team this decision together with the semantic capability before aggregate promotion.
- Keep access-observation sources, access/use/reliance standing vocabularies and claim-support
  assessment authority deferred to separately linked decisions.
- Keep schemas, migrations, runtime adapters, implementation, cutover, fan-in, fan-out, optional
  slots, cross-dispatch graphs and remote runtimes blocked.

This decision selects architecture only. It does not claim implementation, runtime enforcement or
production readiness.
