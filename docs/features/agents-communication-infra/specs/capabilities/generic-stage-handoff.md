---
tags: [agents-communication-infra, stage-handoff, provenance, evidence]
node_type: spec
is_session: false
layer: [domain, application]
nature: [technical, reference]
status: draft
version: 0.2.0
last_updated: 2026-09-01
---

# Generic Stage Handoff

## Contract status and objective

This capability specifies the semantic contract discovered in
[Generic Stage Handoff](../../discovery/generic-stage-handoff.md), verified at
`sha256:328139a23aff2d391d51f85869c36b8a943aaf4833547fe9afdeaa9acfc8b6ec`.
It defines what evidence is required for one exact result from one governed producing stage to
become immutable input accepted by one identified consuming stage.

This is a normative semantic contract, not an implementation claim. The accepted
[ACI-GSH-001 architecture decision](../../../../decisions/aci-generic-stage-handoff-architecture.md)
selects a staged extension of the existing bounded host-workflow compiler, mappings and handoff
operations; it rejects a standalone generic-handoff aggregate for this version. This document
still creates no aggregate-registry entries, persistent schemas, operations, events, interfaces,
migrations or runtime enforcement. Those promotions remain controlled by the
[architecture gate](#architecture-and-promotion-gate).

Normative keywords `MUST`, `MUST NOT`, `REQUIRED`, `SHOULD` and `MAY` have their ordinary RFC 2119
meanings. In this document, “established” means warranted by authoritative evidence for exactly
the named fact. It never means inferred from a later outcome, silence or a generic success label.

## Outcome and scope

A conforming handoff preserves five independently evidenced facts in prerequisite order:

```text
ResultCommitment
  -> PublicationAuthorization
  -> ResultPublication
  -> ImmutableDelivery
  -> ConsumerAcceptance
```

An arrow means that the later fact MUST identify and verify the earlier fact. It is not an
implication that the later fact occurred. The handoff is complete only at
`ConsumerAcceptance`. Access, use, reliance and claim support remain outside the completion
boundary and require their own evidence.

The admitted cardinality is exactly one producing stage outcome, one committed result, one named
handoff, one intended consuming stage and one immutable consumer input. Fan-in, fan-out,
cross-dispatch work graphs, remote runtimes and arbitrary workflow topologies are excluded from
this version.

## Capability-local concept allocation

These concepts are assessed against the [DomainSpec taxonomy](../../../../../domainspec/TAXONOMY.md)
but remain capability-local until aggregate promotion. Named meta-types below are settled
classifications. No row selects a storage shape or asserts that the corresponding aggregate aspect
already contains the concept.

| Concept | Meta-type | Normative meaning |
|---|---|---|
| `ResultCommitment` | Entity | Identity-bearing commitment by one governed producing-stage outcome to exact immutable bytes. |
| `PublicationAuthorization` | Event | Durable authority decision permitting exactly one commitment to be published through one named handoff to one intended consumer. |
| `ResultPublication` | Event | Durable occurrence fact that the authorized commitment was made available for that named handoff. |
| `ImmutableDelivery` | Entity | Identity-bearing binding of the published bytes, order and limits into one exact immutable consumer input. |
| `ConsumerAcceptance` | Event | Durable consumer-bound acknowledgement that the exact delivery is admitted as input for the identified consuming stage. |
| `AccessObservation` | Event | Evidence or explicitly typed assertion about a named access boundary for the accepted delivery. |
| `UseAssertion` | Entity | Attributable statement that identified delivered content was used. |
| `RelianceAssertion` | Entity | Attributable statement that an identified outcome materially depended on identified delivered content. |
| `ClaimSupportRelation` | Entity | Separately assessed, provenance-bearing relation between identified evidence and an identified claim. |
| `HandoffReceipt` | Value Object | Canonical, transition-local acknowledgement whose meaning is limited to one named fact. |

`HandoffUncertainty` remains a required conceptual placeholder, but no DomainSpec meta-type is
allocated until a closed finite vocabulary is approved. The discovery's `Enum / Type` is a
candidate, not a settled allocation.

The future aggregate concept graph MUST use only type-valid edges from
[DomainSpec relationships](../../../../../domainspec/RELATIONSHIPS.md). This capability does not
pre-register those edges.

## Fact contract

### Required bindings and proof ceilings

| Fact | REQUIRED evidence and bindings | Maximum warranted statement | MUST NOT establish |
|---|---|---|---|
| `ResultCommitment` | Governed producer-stage outcome; producer seat/actor and turn or attempt; authority scope; completion condition; exact artifact identity, bytes, digest and size. | The identified producer outcome committed these exact bytes as its result. | Authorization, occurred publication, delivery, acceptance, access, quality or truth. |
| `PublicationAuthorization` | One verified commitment; named handoff; intended consumer stage/seat/turn or attempt; admitted authorizing principal or boundary; immutable authority decision. | The admitted authority permitted this exact commitment to be published for this handoff and consumer. | That publication occurred or any later fact. |
| `ResultPublication` | The same commitment; one matching authorization; publishing principal or boundary; durable occurrence identity and evidence location. | The exact authorized commitment was durably made available for the named handoff. | Delivery, acceptance or any downstream evidence. |
| `ImmutableDelivery` | One verified publication; exact consumer identity; ordered input entries and limits; exact content identities and digests; immutable input identity; admitted delivery authority. | The exact published content became the ordered, bounded immutable input prepared for this consumer boundary. | Consumer acceptance, provider start, access, use, reliance or support. |
| `ConsumerAcceptance` | One verified delivery; exact consuming-stage identity; admitted accepting principal or boundary; durable acceptance identity and evidence location. | The governed consumer boundary admitted this exact immutable delivery as its input. | Provider execution, access, comprehension, use, agreement, reliance, output quality or claim support. |

Every later fact MUST resolve all required predecessor identities from authoritative evidence and
MUST reject a missing, ambiguous or divergent binding. Equal content bytes MUST NOT merge distinct
producer outcomes, commitments, publications, deliveries or consumer acceptances.

### Formal completion and non-implication rules

For handoff `h`, let `C(h)`, `A(h)`, `P(h)`, `D(h)` and `X(h)` denote its commitment,
authorization, occurred publication, immutable delivery and consumer acceptance. `binds(y,x)`
means that authoritative evidence for `y` names and verifies the exact identity and applicable
canonical content of `x`.

```text
valid(A(h)) => valid(C(h)) and binds(A(h), C(h))
valid(P(h)) => valid(C(h)) and valid(A(h))
               and binds(P(h), C(h)) and binds(P(h), A(h))
valid(D(h)) => valid(P(h)) and binds(D(h), P(h))
valid(X(h)) => valid(D(h)) and binds(X(h), D(h))

complete(h) <=> valid(C(h)) and valid(A(h)) and valid(P(h))
                and valid(D(h)) and valid(X(h))
                and oneProducer(h) and oneConsumer(h)
                and exactBindings(h)
```

These formulas are acceptance prerequisites: validating a later bounded-handoff fact includes
verifying the exact earlier facts it names. They do not permit an earlier fact to establish that a
later transition occurred. Evidence outside the bounded chain also cannot retroactively establish
a missing chain fact:

```text
established(C) -/-> established(A)
established(A) -/-> established(P)
established(P) -/-> established(D)
established(D) -/-> established(X)
established(X) -/-> access or use or reliance or claimSupport
downstreamEvidence or laterConsumerOutcome -/-> anyMissingChainFact
```

A status, receipt or projection MUST name the narrowest established fact. A generic `success`
result that can be interpreted as more than one of these transitions is non-conforming.

## Identity and authority contract

### Non-aliasing identity axes

A concrete design MUST preserve these independently comparable identity axes:

| Axis | Identities that MUST remain distinguishable |
|---|---|
| Producer | Producing stage, seat/actor, turn or attempt, outcome and authority scope. |
| Result | Logical result, commitment, artifact and exact content digest. |
| Authorization | Authorization decision, authorizing principal/boundary, authority scope and named handoff. |
| Publication | Publication occurrence, publishing principal/boundary and transport retry. |
| Consumer | Intended stage, seat/actor, turn or attempt and provider session, if any. |
| Delivery | Delivery, immutable input, ordered entries, limits and input digest. |
| Acceptance | Acceptance fact, accepting principal/boundary and accepted delivery. |
| Downstream evidence | Observer/assertor/assessor, method, time, delivered entry, outcome, claim and standing. |

A logical identity MUST bind its immutable semantic content. Reuse of one logical identity with a
different producer, consumer, authority, predecessor, order, limit, artifact, digest or meaning is
a permanent conflict, not a new version of the same transition.

### Authority separation

The following constraints implement GSHD-3 under the role and boundary allocations selected by
[ACI-GSH-001](../../../../decisions/aci-generic-stage-handoff-architecture.md). They do not select
concrete deployment principal identifiers, adapters, schemas or command/event names:

1. A producer MAY commit only within authenticated producing-stage authority.
2. `PublicationAuthorization` MUST come from an admitted authority decision scoped to the exact
   commitment, handoff and intended consumer. Producer-authored payload prose MUST NOT supply or
   override that authority.
3. `ResultPublication` MUST be a separate durable occurrence fact and MUST verify its matching
   authorization. The authorization record MUST NOT stand in for occurrence.
4. `ImmutableDelivery` MUST be recorded by a boundary authorized to materialize the exact
   publication for the exact consumer. Mutable current-file contents MUST NOT substitute for the
   committed bytes.
5. `ConsumerAcceptance` MUST come from the governed consumer boundary and MUST identify the exact
   delivery. Delivery materialization alone MUST NOT self-assert consumer acceptance.
6. Access observations, use assertions, reliance assertions and support assessments MUST each
   identify their own observer, assertor or assessor and MUST NOT inherit authority from a
   handoff fact.

One physical component MAY eventually implement more than one role only if the architecture
decision preserves separate authenticated authority inputs, separate facts and separate proof
ceilings. Component co-location MUST NOT collapse the roles.

ACI-GSH-001 resolves the responsible runtime boundaries by role: the confirmed-dispatch authority
and ACI command writer, the connection-handoff workflow, the materializer, and the governed
consumer-admission boundary. Concrete deployment principals and identifiers, adapters, schemas and
command/event names remain unresolved. [Runtime Confirmation Authority v1](../confirmation-authority.md)
supplies the authority root and separation precedent, but the existing contract does not itself
issue these generic handoff facts until the relevant aspects are promoted.

## Receipt contract

Each established transition MUST have a canonical `HandoffReceipt` or an equivalently verifiable
canonical acknowledgement. A receipt is not self-authenticating: verification MUST resolve it
against the authoritative transition fact, exact predecessor identities and responsible authority.

The common envelope MUST contain only fields meaningful to every transition:

1. receipt contract/version and one named transition kind;
2. logical transition identity and idempotency identity;
3. responsible actor or authority identity;
4. durable transition-fact identity and authoritative evidence location; and
5. canonical equality plus identical/divergent retry semantics.

Transition-local payloads MUST remain separate:

| Receipt kind | REQUIRED transition-local projection |
|---|---|
| Commitment | Producer outcome, exact artifact/content digest, size, completion condition and authority scope. |
| Publication authorization | Commitment, named handoff, intended consumer, authorizing principal/boundary and decision. |
| Publication occurrence | Commitment, matching authorization and durable occurrence; no delivery fields. |
| Delivery | Publication, recipient, immutable input, ordered entries, limits and digest. |
| Consumer acceptance | Delivery, consumer and durable acceptance; delivery details MAY be referenced but MUST remain verifiable. |

Access, use, reliance and support records MUST use their own provenance-bearing contracts and MUST
NOT be projected into a handoff-transition receipt. No receipt MAY contain a field whose presence
suggests that a later transition has occurred when only the named transition is established.

## Retry, recovery and uncertainty

### Retry

For every transition, a future concrete contract MUST define a canonical command or fact
projection and apply idempotency-key and logical-identity checks at its authoritative acceptance
boundary:

```text
sameRetryIdentity + sameCanonicalMeaning => preserveAcceptedFact and idempotentResult
sameRetryIdentity + divergentMeaning => conflict and noReinterpretation
sameLogicalIdentity + sameCanonicalMeaning => preserveAcceptedFact and idempotentResult
sameLogicalIdentity + divergentMeaning => conflict and noReinterpretation
```

An identical retry MAY return the first accepted receipt, but this semantic contract does not
select receipt-winner, transaction or concurrency mechanics. A transport retry identity MUST NOT
replace the logical transition identity.

### Recovery boundary

Recovery MAY establish the last independently proven fact and MUST stop there:

| Last established fact | Required report |
|---|---|
| Commitment only | Committed; publication authorization not established. |
| Authorization only after commitment | Authorized; publication occurrence not established. |
| Publication occurrence | Published; delivery not established. |
| Immutable delivery | Delivered; consumer acceptance not established. |
| Consumer acceptance | Handoff complete; access, use, reliance and support remain independently unknown unless separately evidenced. |

A later consumer output, later successful stage, missing negative event, log message or provider
silence MUST NOT fill an evidence gap. Lost-response recovery MUST resolve authoritative state;
it MUST NOT repeat an external effect merely because the receipt was not observed.

### First-class uncertainty

When evidence cannot establish a fact or its negation, the conformance result MUST carry an
explicit typed unknown or unresolved standing. When evidence sources disagree, it MUST carry an
explicit contested or reason-coded failure standing. The exact per-relation vocabulary is deferred,
but every future vocabulary MUST distinguish unknown from established success.

Agent self-report MAY establish only the admitted assertion class. It MUST NOT be relabeled as a
host observation or verified transition. Silence, retries and downstream completion MUST NOT
convert uncertainty into success.

## Access, use, reliance and claim support

These relations reference accepted delivery where applicable but do not form another ordered
handoff chain:

| Relation | REQUIRED evidence | Independent boundary |
|---|---|---|
| `AccessObservation` | Exact accepted delivery; named access boundary; admitted observation source or explicitly typed self-assertion; time and method. | Does not require or prove use, reliance, agreement or support. |
| `UseAssertion` | Exact accepted delivery and delivered entries; attributable consumer statement; time and limitations. | Does not require an access observation and does not prove reliance, correctness or support. |
| `RelianceAssertion` | Exact accepted delivery and entries; identified consumer outcome; attributable statement; time and limitations. | Does not require access or use and does not prove source truth or claim support. |
| `ClaimSupportRelation` | Stable evidence and claim identities; assessor or method; provenance; explicit standing and basis. | Has no handoff-stage predecessor and proves neither access, use, reliance nor claim truth. |

The relations are independently combinable. A conforming model MUST represent, without
contradiction, a consumer that accesses and rejects content, uses it as a counterexample, relies
on evidence later assessed as insufficient, or supports a claim without relying on one particular
delivered item.

Claim support implements GSHD-5: it MUST be separately assessed and MUST NOT be conferred by
commitment, authorization, publication, delivery, acceptance, access, use, reliance, signature or
producer authority. Its final standing vocabulary and assessment-authority model remain unresolved.

## Existing ACI seams and non-substitution

Existing ACI contracts remain authoritative for their bounded facts. They do not automatically
satisfy a generic handoff transition merely because their names or payloads look similar.

| Existing seam | Fact it currently establishes | Generic elevation that is forbidden without an explicit verified mapping |
|---|---|---|
| [`HostTerminalResponseArtifact`](../domain.md#hostterminalresponseartifact) and receipt | Exact host-observed terminal bytes plus producer-turn attribution. | Publication authorization, occurred publication, delivery or acceptance. |
| `SourceToSlotMapping` | Preconfirmed topology edge, producer and consumer selectors, required slot contract and visibility intent. | `PublicationAuthorization` for any later commitment. After commitment, a separate durable authorization MUST bind the exact commitment, handoff and consumer. |
| [`GroupResult`](../domain.md#groupresult) | One protocol result committed for a group version. | Named generic handoff publication or consumer acceptance. |
| [`PublicationReceipt`](../domain.md#publicationreceipt) | `persisted_candidate` only. | Official acceptance, named result publication, delivery or consumption. |
| [`MaterializeAuthorizedPeerInput`](../operations.md#materializeauthorizedpeerinput) | Bounded immutable peer-input materialization under its own contract. | Generic consumer acceptance, access, use, reliance or support. |
| [`MaterializeHostWorkflowInput`](../operations.md#materializehostworkflowinput) | Canonical host workflow input materialization; no consumer launch. | Consumer acceptance, provider execution or access. |
| [`ReferenceScoutBundleToEffectiveInput`](../mappings.md#referencescoutbundletoeffectiveinput) | Accepted target-attempt inclusion under the reference-delivery contract. | Reading, declared use or claim support. |
| [Resumable Agent Continuation](resumable-agent-continuation.md) | Exact two-source continuation input and bounded resume/reconstruction semantics. | Generic host-workflow handoff or arbitrary producer-to-consumer acceptance. |

A later architecture MAY reuse these seams only through explicit mappings that preserve all
identities, authorities, receipt meanings and proof ceilings in this capability.

## Formal rules

### GSH-R1 — Independently evidenced ordered facts

Commitment, authorization, occurred publication, delivery and acceptance MUST be separately
established. Each later fact MUST bind and verify its exact predecessors. An earlier fact MUST NOT
be treated as establishing a later transition, and downstream or out-of-chain evidence MUST NOT
retroactively establish a missing bounded-handoff fact.

### GSH-R2 — Completion ends at exact consumer acceptance

`complete(h)` is true only for one consumer-bound acceptance of one exact immutable delivery whose
publication, matching authorization and producer commitment all verify. Access, use, reliance and
support do not extend or retroactively complete the handoff.

### GSH-R3 — Fact-local authority and receipt meaning

Every fact MUST bind the actor or authority responsible for that fact. Payload prose cannot create
authority. A receipt MUST warrant only its named transition and MUST be verified against
authoritative evidence.

### GSH-R4 — Recovery preserves uncertainty

Recovery and retry MUST preserve the last established fact, canonical identity and exact content.
Missing, ambiguous or divergent evidence MUST remain unknown, unresolved or conflicted; later
success and silence cannot manufacture a transition.

### GSH-R5 — Claim support is orthogonal

Claim support MUST be a separately assessed relation with stable claim/evidence identities,
provenance, assessor or method, basis and standing. No handoff or downstream assertion fact implies
support.

### GSH-R6 — Exact bytes and attribution survive every transition

Every transition MUST trace to the committed artifact bytes and producer outcome without mutable
substitution. Equal bytes from different outcomes MUST retain distinct attribution.

### GSH-R7 — Retry cannot change meaning

Identical retries MUST preserve the established fact and canonical meaning and MAY return the
first accepted receipt. Any change to producer, consumer, authority, predecessor, content,
ordering, limits or semantic meaning under the same retry or logical identity MUST conflict rather
than reinterpret that fact.

### GSH-R8 — Narrow status only

Every status and projection MUST identify the exact established transition. A generic status that
can be read as authorization, publication, delivery and acceptance at once is forbidden.

## Required conformance tests

These are semantic obligations for the later architecture and aggregate/aspect promotion. They do
not claim executable tests already exist.

| ID | Required proof | Validates |
|---|---|---|
| `T-ACI-GSH1` | A complete one-producer/one-consumer fixture independently verifies all five facts, exact predecessor bindings and exact committed bytes. | GSH-R1, GSH-R2, GSH-R6 |
| `T-ACI-GSH2` | Five partial fixtures stop after each respective fact and prove that every later fact remains unestablished. Reverse inference from a later output is also rejected. | GSH-R1, GSH-R4, GSH-R8 |
| `T-ACI-GSH3` | Producer payload authority, a preconfirmed mapping or policy without separate post-commitment authorization, mismatched authorization, unauthorized materializer and materializer-authored acceptance are rejected or remain unestablished. | GSH-R3 |
| `T-ACI-GSH4` | Equal bytes from two producer outcomes retain distinct commitments; changed bytes, artifact, producer or consumer under one identity conflict. | GSH-R6, GSH-R7 |
| `T-ACI-GSH5` | Replacing committed bytes with mutable current-file bytes, reordering entries, changing limits or changing the immutable input digest rejects. | GSH-R2, GSH-R6 |
| `T-ACI-GSH6` | Each receipt verifies only against its named fact; fields from a later transition, a generic `success` label and a self-authenticating unresolved receipt reject. | GSH-R3, GSH-R8 |
| `T-ACI-GSH7` | Same retry or logical identity with unchanged canonical meaning preserves the established fact and yields an idempotent result; divergent meaning conflicts rather than reinterpreting the fact. No concurrency behavior is asserted. | GSH-R7 |
| `T-ACI-GSH8` | Crash/lost-response fixtures recover only the last durable fact, never infer the next one and never repeat an external effect solely due to an absent receipt. | GSH-R4 |
| `T-ACI-GSH9` | Provider silence, missing negative evidence and later consumer success all preserve an explicit unknown standing for the missing transition. | GSH-R4, GSH-R8 |
| `T-ACI-GSH10` | Access, use and reliance fixtures independently admit every applicable true/false/unknown combination without one relation creating another. | GSH-R1, GSH-R4 |
| `T-ACI-GSH11` | Support, contradiction, qualification, irrelevance and unknown candidates are evaluated from claim/evidence provenance, never copied from delivery, use or reliance. Final labels remain architecture-gated. | GSH-R5 |
| `T-ACI-GSH12` | Every collapse test below has a negative fixture and produces rejection, explicit incompleteness, unknown or a reason-coded conflict—not success. | All rules |

## Collapse-test gate

A proposed architecture, aggregate amendment or implementation is non-conforming if any of these
conditions is possible:

- a declared required stage dependency reaches the consumer with an empty required input;
- bytes can be attributed to a producer outcome that never committed them;
- authorization can be reported as occurred publication;
- publication can occur without a verified commitment and matching named authorization;
- delivery can substitute mutable bytes for the committed bytes;
- one status or receipt can mean both delivery and consumer acceptance;
- acceptance automatically creates access, use, reliance or support;
- retry can change producer, consumer, authority, content or meaning under one logical identity; or
- missing evidence is projected as success instead of explicit uncertainty or failure.

All nine conditions MUST be evaluated against both architectural candidates before the mechanism
decision is accepted.

## Architecture and promotion gate

### Accepted architecture decision

[ACI-GSH-001](../../../../decisions/aci-generic-stage-handoff-architecture.md) selects a staged
extension of the existing bounded host-workflow pipeline for the one-producer, one-required-slot,
one-consumer slice. The extension MUST add separate durable facts for commitment, publication
authorization, publication occurrence, immutable delivery and consumer acceptance. Existing seams
are evidence or execution boundaries and MUST NOT be renamed into those facts without the explicit
verified mappings required by the decision.

The initial graph compile freezes topology, required slot contract, selectors and confirmed
mapping. It MUST NOT fabricate a result-bound source. After producer commitment, the runtime
records the remaining facts in prerequisite order and admits the final downstream manifest,
binding and launch authorization only after exact consumer acceptance. Failure of any
[collapse test](#collapse-test-gate) blocks promotion and reopens the standalone-aggregate option.

### Gate result

| Gate | Status | Reason |
|---|---|---|
| Semantic specification | `pass` | GSHD-1 through GSHD-5 are translated into normative rules and conformance obligations. |
| Architecture selection | `pass` | ACI-GSH-001 selects the bounded staged extension and assigns the responsible authority boundary for each fact. |
| Aggregate/aspect promotion | `block` | `SPEC.md`, architecture, domain, states, events, operations, mappings, workflows, interfaces, rules and test-spec changes still require a coherent reviewed amendment. |
| Implementation | `block` | No concrete schema, canonicalization, persistence, lifecycle, authority adapter, status vocabulary, migration or implementation work pack is authorized by this document. |

The final access observation source, per-relation standing vocabularies and claim-support assessment
authority also remain open. They MAY be settled with the architecture decision or by separately
linked decisions, but implementation MUST NOT invent them.

## Source trace

| Source decision or contract | Normative result here |
|---|---|
| [GSHD-1](../../discovery/generic-stage-handoff.md#31-independent-facts-ordered-prerequisites) | GSH-R1, fact table, non-implication rules and independent downstream relations. |
| [GSHD-2](../../discovery/generic-stage-handoff.md#32-handoff-completion-boundary) | GSH-R2 and the exact consumer-acceptance completion formula. |
| [GSHD-3 / §4.1](../../discovery/generic-stage-handoff.md#41-identity-axes) | Non-aliasing identity axes and exact attribution in GSH-R3 and GSH-R6. |
| [GSHD-3 / §4.2](../../discovery/generic-stage-handoff.md#42-authority-split) | Fact-local authority separation and payload-authority rejection in GSH-R3. |
| [GSHD-3 / §4.3](../../discovery/generic-stage-handoff.md#43-receipt-scope) | Transition-local receipt meaning, verification, retry semantics and narrow status in GSH-R3, GSH-R7 and GSH-R8. |
| [GSHD-4 / §5.1](../../discovery/generic-stage-handoff.md#51-retry-and-reconciliation-meaning) | Identity-preserving retry, divergent conflict and last-established-fact recovery in GSH-R4 and GSH-R7. |
| [GSHD-4 / §5.2](../../discovery/generic-stage-handoff.md#52-unknown-is-a-first-class-result) | Explicit uncertainty, evidence-class preservation and no success by silence in GSH-R4 and GSH-R8. |
| [GSHD-4 / §5.3](../../discovery/generic-stage-handoff.md#53-collapse-tests) | The collapse-test gate, exact-byte preservation and prohibition on collapsed success meanings in GSH-R6 and GSH-R8. |
| [GSHD-5](../../discovery/generic-stage-handoff.md#62-support-is-evaluated-not-transported) | GSH-R5 and the orthogonal claim-support contract. |
| GSH-R6 trace | [Identity axes](../../discovery/generic-stage-handoff.md#41-identity-axes) and [collapse tests](../../discovery/generic-stage-handoff.md#53-collapse-tests) require exact bytes, distinct attribution and rejection of mutable substitution. |
| GSH-R7 trace | [Receipt scope](../../discovery/generic-stage-handoff.md#43-receipt-scope) and [retry/reconciliation](../../discovery/generic-stage-handoff.md#51-retry-and-reconciliation-meaning) require canonical retry equality and divergent conflict without selecting concurrency mechanics. |
| GSH-R8 trace | [Receipt scope](../../discovery/generic-stage-handoff.md#43-receipt-scope), [first-class unknown](../../discovery/generic-stage-handoff.md#52-unknown-is-a-first-class-result) and [collapse tests](../../discovery/generic-stage-handoff.md#53-collapse-tests) require narrow status and forbid missing evidence from becoming success. |
| [Runtime Confirmation Authority v1](../confirmation-authority.md#ownership-and-trust-boundary) | Precedent for separating decision, trusted observation, projection and runtime acceptance; not generic handoff authority. |
| [Resumable Agent Continuation](resumable-agent-continuation.md) | Precedent for exact input bindings, immutable effective input and uncertainty; its bounded graph remains distinct. |
| [ACI aggregate and aspects](../SPEC.md#capabilities) | Existing fact owners and proof ceilings preserved by the non-substitution table. |
| [ACI-GSH-001](../../../../decisions/aci-generic-stage-handoff-architecture.md) | Selects the staged host-workflow extension, fact owners, compiler staging and collapse-test reopening condition. |

## Explicitly unresolved and excluded

- concrete schemas and command/event names that realize the ACI-GSH-001 authority allocations;
- persistent schemas, canonical byte projections, identity derivation and storage topology;
- final lifecycle and per-relation unknown/asserted/observed/verified/contradicted vocabularies;
- an access-observation source and claim-support assessment-authority model;
- aggregate/aspect edits, interfaces, migrations, runtime adapters, implementation and cutover;
- fan-in, fan-out, optional slots, cross-dispatch graphs, remote runtimes and arbitrary topologies;
- claims of provider execution, cognitive access, comprehension, use, reliance, truth or support
  derived only from handoff completion; and
- any claim that an existing bounded ACI path already implements this generic lifecycle.

## Changelog

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-09-01 | Translated GSHD-1 through GSHD-5 into a normative semantic contract; preserved the mechanism and concrete-authority decisions as blocking gates. |
| 0.2.0 | 2026-09-01 | Synchronized ACI-GSH-001: selected the bounded staged pipeline extension, recorded fact-local owners and kept aggregate/aspect promotion and implementation gated. |
