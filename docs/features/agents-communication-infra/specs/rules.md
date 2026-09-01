---
tags: [agents-communication-infra, spec, rules]
node_type: spec
is_session: false
layer: application
nature: [technical, reference]
status: draft
version: 0.5.1
last_updated: 2026-09-01
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

For POLICY-000, [ResourceBudget](domain.md#resourcebudget),
[SandboxPolicy](domain.md#sandboxpolicy), production
[ExecutionAuthorityFence](domain.md#executionauthorityfence) and the separately typed
[ExecutionAuthorityFenceHarness](domain.md#executionauthorityfenceharness) are recursively closed.
Their exact schema literals and nested fields, plus exact target bytes and any target schema required
by the reference owner's contract, are part of acceptance.
Unknown, missing, duplicate or misspelled fields reject. Booleans are not integers; numeric strings,
floats, negative values, nulls, non-finite values, overflow/wraparound representations and implicit
coercion reject. No absence means unlimited, inherited, host-default or allowed.

Every `ResourceBudget` ceiling and `SandboxPolicy.max_child_processes` is a closed int64 in
`0..9223372036854775807`; zero is an explicit denial. Production and harness `cutover_epoch` are
closed positive int64 values in `1..9223372036854775807`. Values outside those intervals reject
without truncation, wraparound or coercion.

Canonical bytes are exact `aci-cjson-1` bytes and every digest is qualified lowercase
`sha256:<64-lowercase-hex>` over its declared byte domain. A
[VersionedReference](domain.md#versionedreference) is accepted only when the caller supplies exact
target bytes keyed to that reference and those bytes reproduce its digest. Budget-policy and
sandbox-enforcement targets must also satisfy their specified closed schemas. Credential targets
are verified under the reference owner's contract; POLICY-000 invents no universal credential-target
schema. Missing bytes or a digest/schema mismatch reject, and the pure parser performs no
filesystem, network, credential-store or other I/O. Production and harness fence preimages use
their distinct exact schema literals; the production parser rejects the harness literal before
evidence resolution. The embedded `fence_digest` binds only the corresponding preimage, while
whole-value equality remains canonical-byte equality.

POLICY-000 validates sandbox roots lexically only. A root must be a canonical relative `/` path and
must contain no empty component, `.`, `..`, drive, UNC or wildcard syntax; `link_policy` is exactly
`deny`. Physical symlink, junction/reparse-point and resolved-path containment checks require host
observation and belong to POLICY-003/L3, never the pure L0 parser. `credential_refs` may be non-empty
but must be duplicate-free opaque references; secret bytes remain forbidden in the policy value.

Dispatch scheduling ceilings and one-[Attempt](domain.md#attempt) [ResourceBudget](domain.md#resourcebudget)
are disjoint contracts. No parser or validator may derive, divide, copy or reset one from the
other; unknown provider usage never becomes zero or fresh authority. The synthetic
[ExecutionPolicyOracleFixture](domain.md#executionpolicyoraclefixture) and harness fence are accepted
only by pure test-oracle parsers and never authorize confirmation, a plan/request, an effect or a
process. POLICY-000 performs no persistence or operational enforcement; POLICY-001/L1 synthetic
lineage, POLICY-002/L2 fake denial and POLICY-003/L3 target-host enforcement remain separate.

POLICY-001 admits only the exact seven reviewed POLICY-000 members, in the ordinal/name order
defined by [ExecutionPolicySyntheticLineageReceipt](domain.md#executionpolicysyntheticlineagereceipt).
Before persistence, every member body and declared digest must pass the POLICY-000 parser/oracle
checks. Addition, omission, rename, reorder, artifact substitution, reference-target or enclosing
policy-body drift, swapped targets and harness preimage/fence/full-document digest-domain
substitution reject before commit or conflict with an existing lineage unit.

All seven artifacts are prepared before one file-backed `RuntimeDatabase.write()` transaction. The
same transaction finalizes their artifact metadata and inserts one closed receipt plus seven
contiguous ordered bindings; per-artifact `ArtifactStore.commit()` is forbidden. A failure after
begin, after any artifact, after the receipt, after any binding or before commit must reopen to the
complete unit or none. A committed response lost before delivery and an identical retry converge
on the first receipt. Closing and reopening through fresh database/artifact handles must reproduce
every exact member body/digest, binding and receipt field.

`synthetic_key` and `lineage_identity` are independent uniqueness axes. Either one reused with the
same `unit_digest` returns the first receipt; either one reused with a changed digest is a permanent
conflict with no second unit. Persistence does not change authority type: production policy-
document parsers still reject the combined oracle structurally, and the production fence parser
rejects the harness schema before evidence resolution.

POLICY-001 rows may exist only in finalized artifact metadata and its two test-only lineage tables.
It creates no confirmation, Run/Group/Attempt, plan/request, command receipt, event/head, effect,
publication or message row; invokes no runtime service, journal, audit appender, provider, launcher,
tool, credential/policy resolver or external action; and creates no production migration, service,
API, CLI or package export. Artifact persistence is the only admitted L1 mutation. POLICY-002/L2
denial receipts or attempted actions and POLICY-003/L3 host enforcement remain excluded.
The exact production tables asserted empty are `confirmed_dispatches`, `runs`,
`confirmed_turn_graphs`, `agent_invocation_plans`, `agent_execution_requests`, `agent_attempts`,
`command_receipts`, `events`, `aggregate_heads`, `effect_intents`, `sandbox_launch_effects`,
`publication_candidates`, `publication_receipts` and `messages`.

Product authority may select the exact `ResourceBudget`, `SandboxPolicy`, tool profile and opaque
credential grants for a later confirmed dispatch. It cannot select or synthesize `cutover_epoch`
or watcher-disable evidence: those are operational facts supplied by the cutover verifier from the
target host. Neither product preference nor a test harness can substitute for them.

**Formal:**
```text
accepted_artifact(x) => pydantic_valid(x)
  AND bytes(x) = canonical_json(project(schema_version, x))
  AND digest(x) = sha256(bytes(x))
pydantic_valid(x) != accepted_artifact(x)

policy000_valid(x) => recursively_closed(x)
  AND exact_schema_literal(x)
  AND strict_json_primitives(x)
  AND bytes(x) = aci_cjson_1(x)
  AND resource_and_child_limits_in_closed_int64(x)
  AND fence_epoch_in_positive_int64(x)
  AND lexical_roots_only(x)
  AND link_policy(x) = deny
  AND every_reference_has_caller_supplied_bytes_and_verifies(x)
policy000_parser_io = 0
policy000_parser_effects = 0
physical_link_resolution => policy003_l3
missing_or_ambiguous_policy_field(x) => reject_before_effect(x)
production_fence_parser(harness_fence) => reject_before_reference_resolution
execution_policy_oracle_fixture => test_data AND NOT execution_authority
dispatch_budget != attempt_resource_budget
product_selected_policy_values != operational_fence_epoch_and_evidence

policy001_valid(u) => policy000_valid(every_member(u))
  AND members(u) = exact_ordered_policy000_members[0..6]
  AND receipt_schema(u) = aci.execution-policy-synthetic-lineage-receipt@1
  AND receipt_authority(u) = test-only-non-executable
  AND unit_digest(u) = sha256(aci_cjson_1(lineage_unit_preimage(u)))
policy001_commit(u) => atomic(seven_finalized_artifacts(u), receipt(u), seven_bindings(u))
policy001_failure_before_commit(u) => policy001_rows(u) = empty
same_key_or_identity_and_same_unit_digest(u) => first_receipt(u)
same_key_or_identity_and_different_unit_digest(u) => permanent_conflict_without_write
reopen(u) => exact_member_bodies_and_digests(u) AND exact_bindings(u) AND first_receipt(u)
production_policy_parser(combined_oracle) => reject_structurally
production_fence_parser(harness_fence) => reject_before_reference_resolution
policy001_runtime_authority_rows = 0
rows(confirmed_dispatches, runs, confirmed_turn_graphs,
     agent_invocation_plans, agent_execution_requests, agent_attempts,
     command_receipts, events, aggregate_heads, effect_intents,
     sandbox_launch_effects, publication_candidates, publication_receipts, messages) = 0
policy001_external_effects = 0
policy001_l2_denial_behavior = 0
```

**Checked by:** [TEST-SPEC T-ACI-ETA2](../TEST-SPEC.md#t-aci-eta2--canonical-python-contract-vectors)
and [T-ACI-POL0-1 through T-ACI-POL0-8](TEST-SPEC.md#policy-000-l0-test-matrix), plus
[T-ACI-POL1-1 through T-ACI-POL1-8](TEST-SPEC.md#policy-001-l1-test-matrix).

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

## ACI-R20 — Host terminal output is producer-bound, visibility-authorized and launch-atomic

**Rule:** Content-addressed response bytes and producer-turn evidence have separate identities.
An L0 consumer becomes launchable only from exactly one active confirmed mapping, a completed
producer receipt, an authorized visibility policy, one canonical manifest entry and a binding whose
workflow, consumer, mapping, manifest, cancellation and supersession heads all match atomically.

```text
launch_authorized(target) =>
  exactly_one(active SourceToSlotMapping for target)
  AND verified(HostWorkflowBindingRef(source,target))
  AND verified(HostTerminalResponseReceipt(source))
  AND HostTerminalResponseArtifact.payload_artifact_id = Artifact.artifact_id
  AND authorized(mapping.visibility_policy_ref,target,Artifact)
  AND exactly_one(WorkflowInputManifest.entry)
  AND verified(HostWorkflowTurnBinding)
  AND all(prerequisite_heads_match)
  AND atomic(host_workflow.turn_launch_authorized, launch_effect_intent)
```

Failed, cancelled and unknown producer outcomes carry no L0 response receipt and cannot satisfy the
required slot. Fan-in, optional slots and non-success completion policies require a later version.

**Checked by:** [TEST-SPEC T-ACI-HOST1](../TEST-SPEC.md#t-aci-host1--producer-bound-host-output-and-atomic-launch).

## ACI-R21 — Continuation is resumable state, never hidden authority

**Rule:** A terminal agent turn may create one bounded continuation whose same-session handle is an
optional adapter optimization. Resume authority derives only from the confirmed finite turn graph,
complete continuation input mappings, current deadline and prerequisite heads. Every resume presents an
exact immutable effective input. Definitive provider-handle loss may choose a preconfirmed
reconstruction branch; an unknown resume effect may not.

```text
resume_authorized(c) =>
  state(c) = suspended
  AND terminal(sourceAttempt(c))
  AND finalized(contextSnapshot(c))
  AND completeAndOrdered(awaitedSlots(c))
  AND deadlineCurrent(c)
  AND all(prerequisiteHeadsMatch(c))
  AND atomic(continuation.resume_requested,
             EffectiveInputArtifact,
             Attempt,
             AgentExecutionRequest,
             EffectIntent)

same_session(c) => same(seat_id, agent_instance_id)
reconstruct(c) => definitiveProviderLoss(c) AND same(seat_id) AND new(agent_instance_id)
unknownResumeEffect(c) => noAutomaticReconstruction(c)
providerLost(c) AND exists(targetAttempt(c)) => terminalFailedNoStart(targetAttempt(c))
```

The parked continuation exposes no bus read, listener or subscription. The scheduler reacts to
journal facts, resolves only the two confirmation-frozen official contribution mappings, and
materializes the declared outputs into a new attempt. The first admitted topology is exactly
`author turn 0 -> reviewer turn 0 -> author turn 1`; confirmation expands it to an acyclic turn
graph and freezes a loop ceiling of one.

**Checked by:** [T-ACI-CONT1 through T-ACI-CONT9](../TEST-SPEC.md#bounded-resumable-feedback).

## ACI-R22 — Runtime confirmation is presentation-bound, derived and atomic

A `ConfirmedDispatch` exists only after an admitted issuer has observed an authenticated human
approval for one exact dispatch revision and its displayed pending/spec digests, and the server has
reproduced the same projection. The request cannot author its principal, issuer evidence,
capability grant, expanded graph, mappings or runtime IDs.

```text
accepted(d) =>
  observation.schema = aci.confirmation-observation@1 AND
  matches(admittedIssuerContext,
          observation.issuer_ref,
          observation.issuer_evidence_ref,
          observation.issuer_evidence_digest,
          observation.human_principal_id,
          observation.channel,
          observation.action = approve_runtime_dispatch,
          observation.observed_at,
          observation.dispatch_id,
          observation.dispatch_revision,
          observation.presented_pending_sheet_digest,
          observation.presented_dispatch_spec_digest) AND
  issuerScopedImmutable(observation.observation_id, observation.issuer_ref) AND
  request.mode = pending.mode = cutover.mode = runtime-managed AND
  pending_sheet_digest = H(exactCanonicalPendingBytes) AND
  dispatch_spec_digest = H(serverProject(pending, admittedCapabilityResolution)) AND
  confirmation_observation_digest = H(exactCanonicalObservationBytes) AND
  capability_resolution_digest = H(immutableAdmittedCapabilityResolution) AND
  confirmed_turn_graph_digest = H(closedServerDerivedTurnGraph) AND
  mapping_set_digest = H(closedOrderedMappingSet) AND
  schema_versions = exactCompleteServerResolvedVersionMap AND
  distinctByteDomains(pending_sheet_digest,
                      dispatch_spec_digest,
                      confirmed_authority_digest) AND
  identity_derivation_digest = H(completeDerivationContract) AND
  payload_schema_bundle_digest = H(closedConfirmationPayloadSchemaBundle) AND
  confirmed_authority_digest = H(completeConfirmedAuthorityEnvelope) AND
  graph = serverDerived(3 nodes, 2 edges, 1 continuation, 2 mappings) AND
  everyRuntimeId = derive_id_v1(kind, coordinates) AND
  derivationPreimage = {schema, kind, dispatch_id, dispatch_spec_digest, coordinates} AND
  mappings.ordinals = [0,1] AND
  everyMappingBindingDigest = H(closedBindingWithoutMappingIdOrVersion) AND
  reject(callerSuppliedDerivedIdOrVersion) AND
  atomic(pendingMetadata,
         dispatchSpecMetadata,
         confirmationObservationMetadata,
         confirmedTurnGraphMetadata,
         mappingSetMetadata,
         confirmedAuthorityMetadata,
         runCreatedPayloadMetadata,
         auditOpeningRequestedPayloadMetadata,
         auditOpeningEffectPayloadMetadata,
         ConfirmationObservation,
         ConfirmedDispatch,
         Run,
         graph,
         continuationBinding,
         twoOrderedMappings,
         runCreatedV1,
         auditOpeningRequestedV2,
         version2OpeningPendingHead,
         onePendingAuditOpeningIntent,
         firstReceipt)

same(commandScope, idempotencyKey, commandDigest) => firstReceipt
same(commandScope, idempotencyKey, differentCommandDigest) => permanentKeyConflict
same(dispatchId, confirmedAuthorityDigest) => firstReceipt
same(dispatchId, differentConfirmedAuthorityDigest) => permanentConflict
confirmationSuccess =>
  opening_pending AND
  exactlyOne(effect_type = audit_opening,
             effect_id = derivedAuditOpeningEffectId,
             command_id = acceptedCommand.command_id,
             requested_event_id = auditOpeningRequestedV2.event_id,
             payload_ref = auditOpeningEffectPayloadArtifactId,
             payload_digest = H(exactCanonicalAuditOpeningEffectPayload),
             payload.appender_contract_version = "0.6.4",
             retry_class = retryable,
             status = pending,
             attempt_count = 0,
             claimed_by = null,
             claim_epoch = null,
             outcome_event_id = null,
             outcome_digest = null) AND
  zero(auditAppend, provider, tool, attempt, suspension, resume, continuationAction)
```

All JSON objects in this boundary are closed and canonical. Raw pending bytes are admitted only
when they already equal their strict `aci-cjson-1` encoding; whitespace, BOM, newline, duplicate
keys or key-order drift reject before presentation rather than being silently normalized after the
human decision. `matches(admittedIssuerContext, ...)` means exact equality with the host-derived
tuple and exact presentation; it does not introduce an expiry policy. Key-level and identity-level
replay are evaluated under the same single-writer
transaction; an unlocked identity pre-read cannot establish convergence.
Any drift in issuer evidence, principal, channel, action, observation time, dispatch/revision or
either presented digest rejects before mutation. Each of the three digest domains verifies only
its own canonical bytes and cannot substitute for another.

**Checked by:** [T-ACI-AUTH1 through T-ACI-AUTH8](../TEST-SPEC.md#runtime-confirmation-authority-v1).

## ACI-R23 — Synthetic fake denial is durable without attempted effect

POLICY-002 accepts only the exact, reopened POLICY-001 lineage and the closed test selector corpus
in [T-ACI-POL2-3](TEST-SPEC.md#t-aci-pol2-3--decision-reasons-and-attempt-labels-are-closed).
Each selector routes through the same test-only admission decision and returns the first canonical
[ExecutionPolicyFakeDenialReceipt](domain.md#executionpolicyfakedenialreceipt). A selector names the
failure class exercised by a test; it is not an action, capability, request, effect or receipt field
and can never authorize the named operation.

Before the denial transaction, the harness must reopen the exact seven-member POLICY-001 unit,
reproduce its receipt and member bytes/digests, and rerun the POLICY-000 parser/oracle checks. Every
ResourceBudget ceiling remains zero; filesystem, network, process and credential grant lists remain
empty; `max_child_processes=0`; and the combined oracle and harness fence remain rejected by their
production boundaries. A positive ceiling, non-empty grant, missing/tampered member or digest-domain
substitution falls outside the fake lane and rejects with no POLICY-002 row.

The harness may create exactly one additional test-only denial-receipt table in the same temporary
file-backed SQLite database as the POLICY-001 lineage. It resolves `denial_key` and
`lineage_identity` replay/conflict inside one writer transaction, inserts the canonical receipt or
nothing, and fires `after_commit` only after transaction exit. Same key or lineage identity plus the
same `denial_digest` returns the byte-identical first receipt; changed evidence conflicts without a
second row. Fresh-handle reopen reproduces the exact denial bytes and source-lineage binding.

For each closed selector, every external boundary remains uncalled: workload filesystem, network,
child process, credential, tool, provider, audit appender, journal, runtime service, clock and
environment. Temporary SQLite persistence is the only admitted I/O. POLICY-001 artifact/receipt/
member cardinalities remain unchanged; all production authority/runtime/effect tables remain empty.
The fake port accepts no `AgentExecutionRequest`, `EffectIntent`, production fence or external
callable and produces no runtime event, provider identity, verified opening, Run transition, host
path observation or POLICY-003 evidence.

**Formal:**

```text
policy002_source(u) => reopened_exact_policy001_lineage(u)
  AND policy000_valid(every_member(u))
  AND every_resource_budget_ceiling(u) = 0
  AND sandbox_grants(u) = empty
  AND max_child_processes(u) = 0

fake_attempt_labels = {
  filesystem.read, filesystem.write, network.connect, process.child.start,
  credential.resolve, tool.call, resource.wall_time.consume_positive,
  resource.input_tokens.consume_positive, resource.output_tokens.consume_positive,
  resource.tool_calls.consume_positive, resource.payload_bytes.consume_positive,
  resource.artifact_bytes.consume_positive
}

label in fake_attempt_labels =>
  decision = denied
  AND receipt = first_durable_fake_denial_receipt(policy002_source)
  AND label NOT_IN denial_preimage
  AND label NOT_IN receipt
  AND external_calls = empty

positive_budget_or_nonempty_grant OR invalid_lineage => reject_before_denial_transaction
policy002_commit => atomic(one_test_only_denial_row)
policy002_failure_before_commit => policy002_rows = empty
same_key_or_lineage_and_same_denial_digest => first_receipt
same_key_or_lineage_and_different_denial_digest => permanent_conflict_without_write
reopen => exact_denial_receipt AND exact_source_lineage_binding
policy002_production_rows = empty
policy002_l3_evidence = empty
```

**Checked by:** [T-ACI-POL2-1 through T-ACI-POL2-8](TEST-SPEC.md#policy-002-l2-test-matrix).

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
| OQ-RESOURCE-LIMITS / OQ-SANDBOX | **POLICY-000 L0 grammar, POLICY-001 test-only lineage and POLICY-002 fake-denial behavior specified; product-selected values and POLICY-003/L3 remain deferred** | ACI-R16 and ACI-R23 plus [T-ACI-POL0-1 through T-ACI-POL2-8](TEST-SPEC.md#policy-000-l0-test-matrix). Product selects policy values; the cutover verifier supplies operational fence epoch/evidence. |

## Connections

| Document | Type | Description |
|---|---|---|
| [TECH-POLICY-D0](../development/invoke-runs/20260831-resumable-feedback/plan/TECH-POLICY-D0.md) | `refines` | Reviewed POLICY-000 closed-schema, digest-domain, non-authority and layering contract. |
| [Execution-policy capability](capabilities/execution-policy-authority.md) | `refines` | Bounded L0/L1/L2 contract surface, synthetic-lineage and fake-denial invariants, and authority firewall. |
| [POLICY-001 persistence pattern inventory](../development/invoke-runs/20260831-resumable-feedback/plan/evidence/POLICY-001-PERSISTENCE-PATTERN-INVENTORY.md) | `refines` | Digest-pinned one-transaction, replay/conflict, failpoint/reopen and zero-row pattern. |
| [Domain model](domain.md) | `enforces` | Entities and value objects constrained here. |
| [Persistence and replay](persistence-and-replay.md) | `implements-contract` | Candidate store constraints that make ACI-R5–R7 and ACI-R14 executable. |
| [Discovery v0.2.1](../discovery/feature-discovery/agents-communication-infra.md) | `derives-from` | Authority for decisions ACI-D1–ACI-D15 and OQ settlements. |
| [External Tool Adoptions v0.1.0](../discovery/external-tool-adoption/external-tool-adoptions.md) | `derives-from` | Authority for ETD-1–ETD-7 and OQ-ETA dispositions. |
