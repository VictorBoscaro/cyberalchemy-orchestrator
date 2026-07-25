---
tags: [agents-communication-infra, spec, rules]
node_type: spec
is_session: false
layer: application
nature: [technical, reference]
status: draft
version: 0.3.0
last_updated: 2026-07-25
---

# Rules: Agents Communication Infra

These rules make store authority, authenticated publication, sealing, idempotency, replay and
sensitive-artifact governance independently testable.

## ACI-R1 — Disjoint authority and one physical writer

The journal owns accepted runtime facts; the audit ledger owns official opening/close rows; the
artifact boundary owns immutable bodies; projections own no fact. Every authoritative store has one
validated physical write boundary. Logical publishers call an interface and never open a store.

**Formal:**
```text
owner(fact) = exactly_one(authoritative_store)
physical_write(store, fact) => caller = validated_writer(store)
projection(x) => reconstructible(x) AND NOT authoritative(x)
```

The current audit ledger remains writable only through its validated appender. Historical rows are
not rewritten or revalidated.

**Checked by:** [TEST-SPEC T-ACI-R1](../TEST-SPEC.md#t-aci-r1--authority-and-writer-boundary).

## ACI-R2 — Runtime-derived authority

A [BusPublication](domain.md#buspublication) cannot self-assert `run_id`, `dispatch_id`, `group_id`,
`group_version`, `seat_id`, `agent_instance_id`, `attempt_id`, `actor_principal_id` or `phase`.
Those fields derive from a live authenticated capability scoped to run, group version, seat,
attempt, action and phase. Any conflicting field rejects the whole publication.

**Formal:**
```text
accepted(publication) => authority_fields(publication) = authenticated_context(capability)
payload_contains_conflicting_authority_field => rejected
```

**Checked by:** [TEST-SPEC T-ACI-R2](../TEST-SPEC.md#t-aci-r2--runtime-derived-authority).

## ACI-R3 — Append before receipt and parent verification

A [PublicationReceipt](domain.md#publicationreceipt) is returned only after its acceptance event
commits. The value transported through the model/tool boundary remains a receipt candidate. An
adapter/parent may promote it to an official [Contribution](domain.md#contribution) only after
independently matching `event_id`, `message_id`, logical publication key, `payload_hash` and scoped
`idempotency_key` to persisted journal evidence.

**Formal:**
```text
receipt_returned(r) => committed(event(r.event_id))
official_result(r) => persisted_match(r.event_id, r.message_id, r.payload_hash, r.idempotency_key)
provider_terminal AND NOT persisted_match(candidate_receipt) => NOT official_contribution
```

Missing, fabricated or mismatched receipts reject the candidate without inventing a contribution.

**Checked by:** [TEST-SPEC T-ACI-R3](../TEST-SPEC.md#t-aci-r3--append-before-ack).

## ACI-R4 — Sealed collection and manifest-only reveal

During collection, an agent principal cannot read, list, search, subscribe to, fetch or debug a
peer contribution through any runtime-controlled surface. `collection.closed` atomically freezes
eligibility and the message/hash set but grants no read capability. Only a committed
`reveal.published` grants access to exactly its [RevealManifest](domain.md#revealmanifest).

**Formal:**
```text
phase = collect AND requester.seat_id != message.seat_id => deny(message.payload)
collection.closed => frozen(manifest_entries) AND NOT peer_read_enabled
peer_read_enabled(entry) <=> committed(reveal.published(manifest)) AND entry IN manifest
```

Reveal content is delivered as a content-addressed input to a later attempt/turn and appears in that
attempt's effective-input artifact; the initial proof exposes no generic peer-read tool.

**Checked by:** [TEST-SPEC T-ACI-R4](../TEST-SPEC.md#t-aci-r4--sealed-collection-and-reveal).

## ACI-R5 — Command idempotency is not conflict tolerance

Within one command scope, the same idempotency key and same canonical command digest returns the
original stable receipt without new events or effects. Reusing the key with a different digest is a
permanent conflict. A stale expected aggregate version or any changed `prerequisite_heads[]` entry
is a CAS conflict and must be retried only after re-reading state. Preconditions for starting work
include the relevant group/run heads so start cannot win after close, cancellation or run terminality.

**Formal:**
```text
existing(key, digest) AND incoming(key, digest) => stable_receipt(existing)
existing(key, d1) AND incoming(key, d2) AND d1 != d2 => IDEMPOTENCY_CONFLICT
incoming.expected_version != head.version => VERSION_CONFLICT
exists(p IN prerequisite_heads, current(p.aggregate_id) != p.expected) => VERSION_CONFLICT
```

**Checked by:** [TEST-SPEC T-ACI-R5](../TEST-SPEC.md#t-aci-r5--idempotency-and-cas).

## ACI-R6 — Atomic local acceptance

For a newly accepted command, its command receipt, all derived events, new aggregate head and all
new effect intents commit in one SQLite transaction. Accepting a delivered effect outcome likewise
commits its stable command receipt, terminal event/head, constrained records and the intent's fenced
`status`, `claim_epoch`, `outcome_event_id` and immutable `outcome_digest` together. The caller
observes neither a partial accept nor a receipt before commit.

**Formal:**
```text
commit(command) = atomic(receipt + events + aggregate_head + new_effect_intents)
commit(outcome) = atomic(receipt + terminal_event + aggregate_head + intent_status_epoch_event_digest)
rollback(any_member) => absent(all_members)
same(effect_id, claim_epoch, outcome_digest) => stored_receipt
same(effect_id, claim_epoch) AND different(outcome_digest) => OUTCOME_CONFLICT
```

Audit-ledger append is outside this transaction and is reconciled by identity plus exact canonical
row content; divergent content enters `reconciliation_required` and releases no effect/closure.
No independent decision append is conformant: persistence must satisfy the atomic interfaces and
their failpoint tests. Authoritative artifact metadata is written only through the artifact-store
writer interface.

**Checked by:** [TEST-SPEC T-ACI-R6](../TEST-SPEC.md#t-aci-r6--atomic-command-acceptance).

## ACI-R7 — Pure replay

State is a pure reduction of a verified checkpoint plus accepted events ordered by global journal
offset. Replay does not invoke commands, providers, tools, materializers, wall clock or random
sources and emits no new event implicitly.

**Formal:**
```text
state_n = fold(reducer_version, checkpoint_state, ordered(events_after_checkpoint))
same(checkpoint, events, reducer_version) => same(state_hash)
effects_during_replay = 0
```

Provider output, tool results, deadlines, cancellation and human choices affect state only after
they become accepted events.

**Checked by:** [TEST-SPEC T-ACI-R7](../TEST-SPEC.md#t-aci-r7--pure-replay).

## ACI-R8 — Logical uniqueness survives retries

Retry preserves `operation_id` and creates a new `attempt_id`; any number of non-winning attempt rows
may exist, while a partial unique constraint permits at most one `accepted_result=1` winner per
operation. Replacement creates a new
`agent_instance_id`; it does not increase quorum unless policy explicitly changes the eligible set.
At most one message per logical contribution key, one result per group version, one handoff per
source/connection and one run terminal may be accepted.

**Formal:**
```text
unique(group_aggregate_id, seat_id, round_id, message_type)
unique(group_aggregate_id, committed_result)
unique(source_aggregate_id, connection_id)
unique(run_id, terminal_event)
unique(operation_id) WHERE accepted_result = 1
```

Late and superseded observations remain auditable but cannot overwrite the winner.

**Checked by:** [TEST-SPEC T-ACI-R8](../TEST-SPEC.md#t-aci-r8--logical-uniqueness).

## ACI-R9 — Input, output and accepted message are distinct evidence

The canonical effective input, raw provider-native output and accepted bus contribution are three
separate immutable artifacts/records linked through attempt, exchange, message and event identities.
No raw output becomes a contribution merely because an adapter completed.

**Formal:**
```text
effective_input_id != raw_output_id != contribution.payload_artifact_id
accepted(contribution) => schema_valid AND authorized AND committed(acceptance_event)
```

The effective-input manifest orders and hashes exact system/developer/user instructions, history,
tool names/descriptions/input schemas, response schema, context artifacts and adapter wrappers.
Unobservable provider-side transformations are limitations, never reconstructed facts.

**Checked by:** [TEST-SPEC T-ACI-R9](../TEST-SPEC.md#t-aci-r9--artifact-separation-and-input-manifest).

## ACI-R10 — Provider heterogeneity cannot fork protocol

Provider, adapter and model are selected per agent instance. Every adapter consumes the same
[AgentExecutionRequest](domain.md#agentexecutionrequest) and produces canonical attempt, result and
usage observations. Provider differences remain namespaced metadata or recorded input. A missing
semantics-changing capability rejects the combination or requires a newly confirmed spec.

**Formal:**
```text
capability_profile_satisfied(adapter) => same(kernel_protocol, event_schema, bus_schema)
missing(semantics_changing_capability) => reject OR reconfirm(new_spec_digest)
```

**Checked by:** [TEST-SPEC T-ACI-R10](../TEST-SPEC.md#t-aci-r10--mixed-provider-conformance).

## ACI-R11 — Sensitive immutable artifact governance

Effective inputs and raw provider outputs are sensitive immutable artifacts. Runtime-operator
access is the default minimum role; break-glass is explicit and audited. Secrets are prohibited in
durable payloads. Encryption at rest is mandatory outside local development. Deletion or
crypto-erasure preserves an auditable tombstone, digest and allowed provenance so replay never
pretends content is available.

Concrete retention periods, key custody and legal-hold precedence are deliberately deferred to the
Slice-1 retention and credential ADRs; until accepted, deployment beyond local development is
blocked rather than governed by an implicit default.

**Checked by:** [TEST-SPEC T-ACI-R11](../TEST-SPEC.md#t-aci-r11--sensitive-artifact-governance).

## ACI-R12 — Usage observations preserve provider semantics

Every provider-reported usage record is immutable, provider/model attributed and nullable per
dimension. Missing counters are `null`, never zero. Rollups preserve provenance, missing counts,
currency and the exact `source_through_offset`. Cost is absent unless an immutable applicable
pricing source, matching pricing digest and compatible unit semantics are recorded. A cost record is
created only for a completed calculation and remains estimated evidence, never invoice/billing truth.

**Formal:**
```text
not_reported(counter) => counter = null
cost != null => pricing_ref != null AND pricing_units_compatible
rollup.value derives_only_from compatible_observations_through(source_through_offset)
cost_calculation => immutable(pricing_digest, currency, quantity, unit_price, source_through_offset)
missing_or_incompatible_pricing => no_cost_calculation
```

**Checked by:** [TEST-SPEC T-ACI-R12](../TEST-SPEC.md#t-aci-r12--usage-nullability-and-provenance).

## ACI-R13 — Audit opening gates every provider/tool effect

No provider or tool effect starts until the canonical audit opening row is present, content-identical
to the frozen authority and acknowledged by a committed journal event. Same identity plus divergent
row content blocks the run in `reconciliation_required`.

**Checked by:** [TEST-SPEC T-ACI-R13](../TEST-SPEC.md#t-aci-r13--verified-opening-barrier).

## ACI-R14 — Durability is a feature-level contract

The proof and pilot journal use SQLite WAL with `synchronous=FULL` for every write transaction. A
relaxation to `NORMAL` or another policy changes the durability claim for the entire atomic command
acceptance and requires measured fault evidence plus an explicit superseding decision.

**Checked by:** [TEST-SPEC T-ACI-R14](../TEST-SPEC.md#t-aci-r14--sqlite-durability-policy).

## ACI-R15 — External tool adoption policy

An external tool is admitted only as a kernel dependency, boundary-local dependency, experimental
adapter or reference-only artifact through an explicit classification. A tool that claims facts
already owned by the journal, audit ledger, artifact boundary or reducers is rejected from the
kernel. Octopus Runtime and Eve are reference-only under the current evidence.

**Formal:**
```text
admit(tool, seam) => classified(tool) AND authority(tool, seam) subset_of permitted_authority(seam)
overlaps_authoritative_fact(tool) => reject_kernel_dependency(tool)
```

**Checked by:** [TEST-SPEC T-ACI-ETA1](../TEST-SPEC.md#t-aci-eta1--external-tool-authority-classification).

## ACI-R16 — Canonical contract policy

Pydantic core validates decoded Python boundary models, but acceptance identity derives only from a
versioned runtime-owned canonical projection serialized to canonical JSON bytes and sealed with
SHA-256. Library serialization defaults never silently define omitted/null, Unicode, numeric or
ordering semantics. W0 must pin the dependency and accept golden vectors before runtime work.

**Formal:**
```text
accepted_artifact(x) => pydantic_valid(x)
  AND bytes(x) = canonical_json(project(schema_version, x))
  AND digest(x) = sha256(bytes(x))
pydantic_valid(x) != accepted_artifact(x)
```

**Checked by:** [TEST-SPEC T-ACI-ETA2](../TEST-SPEC.md#t-aci-eta2--canonical-python-contract-vectors).

## ACI-R17 — Derived boundary validation policy

Python is the normative contract authority. Zod or another language-native validator may exist only
for an inventoried, non-authoritative transport consumer and must be generated or verified against
shared golden vectors from that authority. Current Node surfaces are not identified ACI contract
consumers, so this feature adds no Zod dependency in the present slice.

**Formal:**
```text
node_validator_allowed => inventoried_aci_consumer AND derived_from_python_contract
                         AND cross_boundary_vectors_pass
hand_authored_second_normative_schema => reject
```

**Checked by:** [TEST-SPEC T-ACI-ETA3](../TEST-SPEC.md#t-aci-eta3--derived-node-boundary-parity).

## ACI-R18 — Provider adapter admission gate

A real provider implementation is admitted only after fake-adapter conformance, the common
`materialize/start/events/result/cancel/status/capabilities` suite, fail-closed sandbox and
credential tests, process-tree cleanup, recovery, receipt acceptance and usage-attribution evidence
pass on its target host. The first implementation is a repository-local subprocess adapter behind
`SandboxLauncher`. PydanticAI may be evaluated later only as a direct-API adapter implementing the
same contract; it cannot become a kernel dependency or bypass the gate.

**Formal:**
```text
real_provider_admitted(a, host) => fake_suite_passed
  AND adapter_conformance_passed(a)
  AND sandbox_negative_fixtures_passed(host)
  AND recovery_receipt_usage_evidence_passed(a, host)
provider_process_created => launched_by(SandboxLauncher)
```

**Checked by:** [TEST-SPEC T-ACI-ETA4](../TEST-SPEC.md#t-aci-eta4--subprocess-provider-admission-gate).

## ACI-R19 — Reference bundle delivery is source-bound and attempt-atomic

**Status:** Specified; not implemented.

An accepted target-agent reference delivery is distinct from the accepted
`reference_scout.bundle_delivered@1` Scout lifecycle fact. The lifecycle event proves that the
Scout's committed bundle reached its lifecycle delivery boundary; it does not identify a target
Attempt and does not carry ordered recommendation membership. Target-attempt inclusion is accepted
only when the accepted `reference_scout.bundle_committed@1` fact and exact immutable bundle bytes
agree on artifact identity, digest and ordered recommendation membership, and the accepted
lifecycle-delivery fact agrees on Scout run, artifact and digest.

The target Attempt, seat and agent-instance identities derive from one authenticated capability.
The source ScoutRun, [AgentReferenceDelivery](domain.md#agentreferencedelivery) and target Attempt
must share the same `dispatch_id`. Stable delivery and target-event identities are allocated before
the effective-input manifest is canonicalized. The matching `reference_bundle` entry, finalized
manifest metadata, sealed request binding, Attempt, AgentReferenceDelivery,
`reference_scout.bundle_delivered_to_agent@1`, `attempt.requested` and launch effect intent are then
accepted in one transaction or not at all.

**Formal:**
```text
accepted(target_delivery) =>
  accepted(bundle_committed)
  AND accepted(bundle_delivered)
  AND bundle_committed.scout_run_id = bundle_delivered.scout_run_id
  AND bundle_committed.bundle_artifact_id = bundle_delivered.bundle_artifact_id
  AND bundle_committed.bundle_digest = bundle_delivered.bundle_digest
  AND bundle_committed.bundle_digest = hash(immutable_bundle_bytes)
  AND bundle_committed.recommendation_ids = ordered_recommendation_ids(immutable_bundle_bytes)
  AND target_delivery.source_bundle_delivered_event_id = bundle_delivered.event_id
  AND target_delivery.accepted_event_id = target_event.event_id
  AND bundle_delivered.event_id != target_event.event_id
  AND bundle_committed.journal_offset
      < bundle_delivered.journal_offset
      < target_event.journal_offset
  AND ScoutRun.dispatch_id = AgentReferenceDelivery.dispatch_id = Attempt.dispatch_id
  AND (Attempt.id, Attempt.seat_id, Attempt.agent_instance_id)
      = authenticated_target(capability)
  AND preallocated(agent_reference_delivery_id, target_event_id)
  AND exactly_one(
        entry = EffectiveInputEntry where
          entry.ordinal = target_delivery.effective_input_entry_ordinal
          AND entry.entry_type = reference_bundle
          AND entry.artifact_ref = target_delivery.bundle_artifact_id
          AND entry.content_hash = target_delivery.bundle_digest
          AND entry.visibility_policy_ref = target_delivery.visibility_policy_ref
          AND entry.agent_reference_delivery_id = target_delivery.agent_reference_delivery_id
          AND entry IN EffectiveInputArtifact(target_delivery.effective_input_artifact_id)
      )
  AND EffectiveInputArtifact(target_delivery.effective_input_artifact_id).attempt_id
      = target_delivery.target_attempt_id
  AND EffectiveInputArtifact(target_delivery.effective_input_artifact_id).manifest_hash
      = target_delivery.effective_input_manifest_hash
  AND atomic(
        finalized_effective_input_metadata,
        sealed_request_binding,
        Attempt,
        AgentReferenceDelivery,
        reference_scout.bundle_delivered_to_agent@1,
        attempt.requested,
        launch_effect_intent
      )
```

This acceptance proves exact inclusion in observable effective input only. It does not prove that
the target accessed the source, declared it used, or relied on it for a claim. Those remain separate
host- and APT-owned evidence.

This bounded amendment formalizes
[OQ-ACI8](../discovery/feature-discovery/agents-communication-infra.md#oq-aci8--canonical-effective-input)
against the accepted
[Stage G lifecycle contract](../../agent-provenance-telemetry/integration/stage-g/reference-scout-and-ingestion.md#reference-scout-lifecycle);
it does not introduce or claim a new discovery decision.

**Checked by:** [TEST-SPEC T-ACI-R22](../TEST-SPEC.md#t-aci-r22--reference-bundle-target-delivery).

## OQ dispositions

| Question | Disposition | Rule coverage |
|---|---|---|
| OQ-ACI1 | **Ratified** | ACI-R5–R7 and [persistence contract](persistence-and-replay.md). |
| OQ-ACI4 | **Ratified** | ACI-R7 and [DispatchSpec](domain.md#dispatchspec). |
| OQ-ACI7 | **Ratified** | ACI-R14. |
| OQ-ACI8 | **Ratified** | ACI-R9 and the bounded specified/not-implemented ACI-R19 amendment. |
| OQ-ACI9 | **Boundary ratified; concrete retention/key parameters deferred** | ACI-R11; Slice-1 ADR remains blocking. |
| OQ-ETA1 | **Deferred blocker to W0** | ACI-R16; pin and canonical vectors remain unaccepted. |
| OQ-ETA2 | **Evidence shape ratified; cutover proof open** | ACI-R1 and [SoleWriterEvidenceBundle](domain.md#solewriterevidencebundle); W0 freezes schema/guard/tests, while TASK-020 supplies physical evidence before cutover without blocking TASK-010. |
| OQ-ETA4 | **Disposed: no identified ACI Node consumer** | ACI-R17; do not add Zod now. |
| OQ-ETA5 | **Deferred post-first-provider** | ACI-R18; no PydanticAI dependency now. |
| OQ-ETA6 | **Disposed as non-blocking provenance maintenance** | [External-tool discovery](../discovery/external-tool-adoption/external-tool-adoptions.md). |

## Connections

| Document | Type | Description |
|---|---|---|
| [Domain model](domain.md) | `enforces` | Entities and value objects constrained here. |
| [Persistence and replay](persistence-and-replay.md) | `implements-contract` | Candidate store constraints that make ACI-R5–R7 and ACI-R14 executable. |
| [Discovery v0.2.1](../discovery/feature-discovery/agents-communication-infra.md) | `derives-from` | Authority for decisions ACI-D1–ACI-D15 and OQ settlements. |
| [External Tool Adoptions v0.1.0](../discovery/external-tool-adoption/external-tool-adoptions.md) | `derives-from` | Authority for ETD-1–ETD-7 and OQ-ETA dispositions. |
