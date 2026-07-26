---
tags: [agents-communication-infra, spec, test]
node_type: spec
is_session: false
layer: application
nature: [procedural, technical]
status: draft
version: 0.5.0
last_updated: 2026-07-25
---

# Test Spec: Agents Communication Infra

This document specifies contract tests, not test code. Fixtures derive from [rules.md](specs/rules.md), lifecycle transitions, operation postconditions, [persistence crash boundaries](specs/persistence-and-replay.md#5-crash-boundaries-and-observable-outcomes) and the executable [bus probe](experiments/bus-publication-probe/README.md).

## Test Matrix

| ID | Test | Validates |
|---|---|---|
| [T-ACI-R1](#t-aci-r1--authority-and-writer-boundary) | Only journal writer and validated ledger appender can mutate their stores | [ACI-R1](specs/rules.md#aci-r1--disjoint-authority-and-one-physical-writer) |
| [T-ACI-R2](#t-aci-r2--runtime-derived-authority) | Agent authority-field injection is rejected | [ACI-R2](specs/rules.md#aci-r2--runtime-derived-authority) |
| [T-ACI-R3](#t-aci-r3--append-before-ack) | Receipt exists only after commit and parent verification | [ACI-R3](specs/rules.md#aci-r3--append-before-receipt-and-parent-verification) |
| [T-ACI-R4](#t-aci-r4--sealed-collection-and-reveal) | Collection stays sealed until persisted matching reveal | [ACI-R4](specs/rules.md#aci-r4--sealed-collection-and-manifest-only-reveal) |
| [T-ACI-R5](#t-aci-r5--idempotency-and-cas) | Retry, digest conflict and expected-version races differ | [ACI-R5](specs/rules.md#aci-r5--command-idempotency-is-not-conflict-tolerance) |
| [T-ACI-R6](#t-aci-r6--atomic-command-acceptance) | Receipt, events, head and new intents are all-or-none | [ACI-R6](specs/rules.md#aci-r6--atomic-local-acceptance) |
| [T-ACI-R7](#t-aci-r7--pure-replay) | Replay from zero/checkpoint yields same hash with zero effects | [ACI-R7](specs/rules.md#aci-r7--pure-replay) |
| [T-ACI-R8](#t-aci-r8--logical-uniqueness) | Retries/attempts cannot create a second logical contribution/result | [ACI-R8](specs/rules.md#aci-r8--logical-uniqueness-survives-retries) |
| [T-ACI-R9](#t-aci-r9--artifact-separation-and-input-manifest) | Effective input, raw output and contribution remain distinct and linked | [ACI-R9](specs/rules.md#aci-r9--input-output-and-accepted-message-are-distinct-evidence) |
| [T-ACI-R10](#t-aci-r10--mixed-provider-conformance) | Mixed providers use the same protocol/state/event shapes | [ACI-R10](specs/rules.md#aci-r10--provider-heterogeneity-cannot-fork-protocol) |
| [T-ACI-R11](#t-aci-r11--sensitive-artifact-governance) | Sensitive access, secret rejection and tombstone provenance fail closed | [ACI-R11](specs/rules.md#aci-r11--sensitive-immutable-artifact-governance) |
| [T-ACI-R12](#t-aci-r12--usage-nullability-and-provenance) | Missing usage stays null and cost needs priced provenance | [ACI-R12](specs/rules.md#aci-r12--usage-observations-preserve-provider-semantics) |
| [T-ACI-R13](#t-aci-r13--verified-opening-barrier) | No provider/tool effect starts before exact opening verification | [ACI-R13](specs/rules.md#aci-r13--audit-opening-gates-every-providertool-effect) |
| [T-ACI-R14](#t-aci-r14--sqlite-durability-policy) | Writer startup asserts WAL, FULL and migration checksum | [ACI-R14](specs/rules.md#aci-r14--durability-is-a-feature-level-contract) |
| [T-ACI-R15](#t-aci-r15--candidate-versus-official-publication) | Candidate persistence alone never counts toward close/quorum | [Receipt workflow](specs/workflows.md#receiptgatedpublicationworkflow) |
| [T-ACI-R16](#t-aci-r16--canonical-receipt-and-terminal-result) | Receipt/result versions and exact field parsing fail closed | [PublicationReceipt](specs/domain.md#publicationreceipt) |
| [T-ACI-R17](#t-aci-r17--invocation-materialization-boundary) | Plan, materialization, sealed request and start effect remain ordered/distinct | [StartAgentAttempt](specs/operations.md#startagentattempt) |
| [T-ACI-R18](#t-aci-r18--typed-reveal-input-provenance) | Reveal input preserves manifest/message/author/hash/policy | [EffectiveInputEntry](specs/domain.md#effectiveinputentry) |
| [T-ACI-R19](#t-aci-r19--sandbox-authority-and-budget-fence) | Sandbox, authority cutover and finite budgets fail closed | [SandboxLauncher](specs/interfaces.md#internal-sandboxlauncher) |
| [T-ACI-R20](#t-aci-r20--causal-start-prerequisites) | Start cannot race past close/cancel using stale dependency heads | [RuntimeCommand](specs/domain.md#runtimecommand) |
| [T-ACI-R21](#t-aci-r21--candidate-abandonment-and-replacement) | Unknown orphan candidates release their key only through authorized audited CAS | [PublicationCandidate](specs/domain.md#publicationcandidate) |
| [T-ACI-R22](#t-aci-r22--reference-bundle-target-delivery) | Scout bundle delivery to a target attempt is source-bound, unique, ordered and atomic | [ACI-R19](specs/rules.md#aci-r19--reference-bundle-delivery-is-source-bound-and-attempt-atomic) |
| [T-ACI-PEER1](#bounded-authorized-peer-input-delivery) | Close freezes only official messages and grants no peer visibility | [CloseCollection](specs/operations.md#closecollection) |
| [T-ACI-PEER2](#bounded-authorized-peer-input-delivery) | One reveal binds the frozen ordered message set and survives restart | [PublishRevealManifest](specs/operations.md#publishrevealmanifest) |
| [T-ACI-PEER3](#bounded-authorized-peer-input-delivery) | Target identity and group are derived from the authenticated invocation plan | [MaterializeAuthorizedPeerInput](specs/operations.md#materializeauthorizedpeerinput) |
| [T-ACI-PEER4](#bounded-authorized-peer-input-delivery) | Derived peer entries preserve order, policy and self-exclusion | [PeerInputDelivery](specs/domain.md#peerinputdelivery) |
| [T-ACI-PEER5](#bounded-authorized-peer-input-delivery) | Attempt, input, delivery, events and pending effect are atomic | [`peer_input.materialized`](specs/events.md#peer_inputmaterialized) |
| [T-ACI-PEER6](#bounded-authorized-peer-input-delivery) | Retry is byte-stable and semantic drift conflicts | [PeerInputDeliveryReceipt](specs/domain.md#peerinputdeliveryreceipt) |
| [T-ACI-PEER7](#bounded-authorized-peer-input-delivery) | The bounded proof exposes no peer-read and starts no provider effect | [Agent Tool Gateway](specs/interfaces.md#external-agent-tool-gateway-mcp-or-equivalent) |
| [T-ACI-ETA1](#t-aci-eta1--external-tool-authority-classification) | External tools cannot acquire kernel or authoritative-store ownership | [ExternalToolAdoptionPolicy](specs/rules.md#aci-r15--external-tool-adoption-policy) |
| [T-ACI-ETA2](#t-aci-eta2--canonical-python-contract-vectors) | Boundary validation and runtime-owned canonical sealing remain distinct | [CanonicalContractPolicy](specs/rules.md#aci-r16--canonical-contract-policy) |
| [T-ACI-ETA3](#t-aci-eta3--derived-node-boundary-parity) | Any derived Node validator stays non-normative and vector-compatible | [BoundaryValidationPolicy](specs/rules.md#aci-r17--derived-boundary-validation-policy) |
| [T-ACI-ETA4](#t-aci-eta4--subprocess-provider-admission-gate) | A real subprocess provider cannot bypass launcher or admission evidence | [ProviderAdapterAdmissionGate](specs/rules.md#aci-r18--provider-adapter-admission-gate) |
| [T-ACI-ETA5](#t-aci-eta5--sole-writer-evidence-completeness) | The sole-writer evidence schema and component checks fail closed | [SoleWriterEvidenceBundle](specs/domain.md#solewriterevidencebundle) |
| [T-ACI-S1](#t-aci-s1--run-lifecycle-and-terminal-precedence) | Run accepts only listed transitions and one terminal winner | [RunLifecycle](specs/states.md#runlifecycle) |
| [T-ACI-S2](#t-aci-s2--group-decision-and-sealing) | Consensus, dissent and no-quorum stay distinct | [GroupLifecycle](specs/states.md#grouplifecycle) |
| [T-ACI-S3](#t-aci-s3--attempt-cancel-races) | Completion/failure/unknown/cancel races have one allowed terminal | [AttemptLifecycle](specs/states.md#attemptlifecycle) |
| [T-ACI-C1](#t-aci-c1--transaction-crash-boundaries) | Every local acceptance crash yields all four members or none | [Crash boundaries](specs/persistence-and-replay.md#5-crash-boundaries-and-observable-outcomes) |
| [T-ACI-C2](#t-aci-c2--audit-append-crash-reconciliation) | Absent, identical and divergent audit rows converge correctly | [Cross-store reconciliation](specs/persistence-and-replay.md#8-cross-store-reconciliation) |
| [T-ACI-C3](#t-aci-c3--closed-before-reveal-restart) | Restart between close and reveal preserves sealed access | [Publication/reveal persistence](specs/persistence-and-replay.md#7-publication-reveal-and-artifact-persistence) |
| [T-ACI-C4](#t-aci-c4--publish-to-terminal-recovery) | Crash anywhere from publish through terminal verification converges once | [Receipt workflow](specs/workflows.md#receiptgatedpublicationworkflow) |
| [T-ACI-C5](#t-aci-c5--effect-outcome-idempotency-matrix) | Terminal outcome retries compare digest before claim/epoch guards | [Atomic effect-outcome acceptance](specs/persistence-and-replay.md#41-atomic-effect-outcome-acceptance) |
| [T-ACI-P1](#t-aci-p1--probe-regression-corpus) | Production contract retains all ten publication-probe behaviors | [Probe](experiments/bus-publication-probe/README.md#run-the-contract-tests) |
| [T-CVR-1](#t-cvr-1--selector-and-root-confinement) | Selectors cannot escape effective roots lexically or after resolution | [CVR-R2](specs/canonical-vault-reads.md#formal-rules) |
| [T-CVR-2](#t-cvr-2--link-and-hidden-denial) | Hidden components and links/reparse points fail closed | [CVR-R6](specs/canonical-vault-reads.md#formal-rules) |
| [T-CVR-3](#t-cvr-3--privacy-and-directlist-parity) | Private or denied paths are non-enumerable and list/get agree | [CVR-R3](specs/canonical-vault-reads.md#formal-rules) |
| [T-CVR-4](#t-cvr-4--snapshot-coherence-under-mutation) | Mutation yields one byte-coherent result or snapshot conflict | [CVR-R4/R5](specs/canonical-vault-reads.md#formal-rules) |
| [T-CVR-5](#t-cvr-5--encoding-frontmatter-and-residue) | BOM/UTF-8/frontmatter variants preserve exact typed outcomes | [CVR-R7](specs/canonical-vault-reads.md#formal-rules) |
| [T-CVR-6](#t-cvr-6--deterministic-order-and-digests) | Nodes, edges, supports and SHA-256 digests are deterministic | [CVR-R4](specs/canonical-vault-reads.md#formal-rules) |
| [T-CVR-7](#t-cvr-7--bounded-edge-normalization) | CVR-002 folds duplicates and only the documented inverse pair | [CVR-R8](specs/canonical-vault-reads.md#formal-rules) |
| [T-CVR-8](#t-cvr-8--unresolved-edge-evidence) | CVR-001 preserves raw declarations; CVR-002 resolves endpoints without dropping residue | [CVR-R7](specs/canonical-vault-reads.md#formal-rules) |
| [T-CVR-9](#t-cvr-9--stale-and-projection-conflicts) | Expected source/projection digest drift returns typed conflict | [Closed outcomes](specs/canonical-vault-reads.md#closed-outcomes) |
| [T-CVR-10](#t-cvr-10--hard-bounds-and-complete-results) | Every success is complete and every cap breach returns no partial result | [CVR-R10](specs/canonical-vault-reads.md#formal-rules) |
| [T-CVR-11](#t-cvr-11--inventory-semantic-independence) | Inventory presence cannot change results or admission | [CVR-R1](specs/canonical-vault-reads.md#formal-rules) |
| [T-CVR-12](#t-cvr-12--zero-effects-and-provenance) | Read calls write and emit nothing and mint no APT/host facts | [CVR-R9](specs/canonical-vault-reads.md#formal-rules) |
| [T-CVR-AUTH1](#t-cvr-auth1--nonrecursive-guard-bootstrap) | GUARD bootstrap cannot authorize itself | [TASK-CVR](work-pack/tasks/TASK-CVR.md#non-recursive-bootstrap-authority) |
| [T-CVR-AUTH2](#t-cvr-auth2--canonical-authority-identities) | Authorization, claim and receipt identities are canonical and content-addressed | [TASK-CVR](work-pack/tasks/TASK-CVR.md#future-append-only-authorization-protocol) |
| [T-CVR-AUTH3](#t-cvr-auth3--closed-descriptor-and-scope) | Caller cannot inject paths, commands, tests or scope | [TASK-CVR](work-pack/tasks/TASK-CVR.md#future-append-only-authorization-protocol) |
| [T-CVR-AUTH4](#t-cvr-auth4--sole-terminal-authority) | Exactly one applicable finalizer creates the receipt: external bootstrap finalizer for GUARD, common guard for CVR-001/002 | [TASK-CVR](work-pack/tasks/TASK-CVR.md#future-append-only-authorization-protocol) |
| [T-CVR-AUTH5](#t-cvr-auth5--crash-and-cancellation-matrix) | Recovery is fail-closed and session-bound | [TASK-CVR](work-pack/tasks/TASK-CVR.md#future-append-only-authorization-protocol) |
| [T-CVR-AUTH6](#t-cvr-auth6--cvr-002-predecessor-binding) | CVR-002 binds and revalidates CVR-001 evidence | [TASK-CVR](work-pack/tasks/TASK-CVR.md#swu-aci-cvr-002--edge-projection) |
| [T-ACI-AUTH1](#t-aci-auth1--runtime-only-confirmed-dispatch) | Legacy routing creates no ACI runtime entity; runtime confirmation creates exactly one dispatch/run pair | [ConfirmRuntimeDispatch](specs/operations.md#confirmruntimedispatch) |
| [T-ACI-ARD1](#t-aci-ard1--exact-reference-bundle-delivery) | One accepted Scout bundle becomes one exact typed target-attempt input entry and target-delivery fact | [AgentReferenceDelivery](specs/domain.md#agentreferencedelivery) |
| [T-ACI-ARD2](#t-aci-ard2--bundle-authority-and-integrity) | Commit plus immutable bytes, never lifecycle delivery, determine ordered recommendation membership | [ReferenceScoutBundleToEffectiveInput](specs/mappings.md#referencescoutbundletoeffectiveinput) |
| [T-ACI-ARD3](#t-aci-ard3--recipient-and-dispatch-authority) | Capability-derived recipient and same-dispatch guards reject identity injection or cross-dispatch delivery | [DeliverReferenceScoutBundleToAgent](specs/operations.md#internal-transition--deliverreferencescoutbundletoagent) |
| [T-ACI-ARD4](#t-aci-ard4--atomic-delivery-and-idempotency) | Preallocated identities, complete acceptance and retries yield one delivery or none | [IF-ACI-14](specs/interfaces.md#interface-invariants) |
| [T-ACI-ARD5](#t-aci-ard5--delivery-evidence-boundary) | Accepted inclusion is never promoted to access, declared use or claim support | [`reference_scout.bundle_delivered_to_agent@1`](specs/events.md#referencescoutbundledeliveredtoagent) |

## Test Details

### T-ACI-R1 — Authority and writer boundary

Attempt journal writes through agent, adapter, projection and effect-worker principals and ledger writes outside the validated appender. All fail; authorized commands produce one physical write path per store. The EG-1 static/behavioral sole-writer fixture is mandatory before cutover.

### T-ACI-R2 — Runtime-derived authority

For every forbidden field (`run_id`, `dispatch_id`, group/version, seat, instance, attempt, principal, phase), inject a matching and a conflicting value. Both are rejected rather than trusted or normalized; accepted facts use authenticated launch context.

### T-ACI-R3 — Append before ack

Crash immediately before commit returns no receipt. Crash after commit/before response followed by
identical retry returns the byte-identical stored receipt. A transport may separately report
`transport_replayed=true`, but changing or embedding that metadata in the receipt fails the canonical
schema. Missing, invented or altered event/message/hash/key/offset fails parent verification.

### T-ACI-R4 — Sealed collection and reveal

Test every controlled read/tool surface during collection and after `collection.closed`; peer payload remains denied. After `reveal.published`, only IDs/hashes in the persisted manifest are delivered, and delivery is recorded in the receiver's effective input.

### T-ACI-R5 — Idempotency and CAS

Same scoped key and digest returns stable receipt without new events; same key/different digest is permanent conflict; two commands at one expected version have one CAS winner.

### T-ACI-R6 — Atomic command acceptance

Inject failure after each receipt/event/head/intent write boundary. Reopen SQLite and assert all members committed or none, never a partial acceptance.

### T-ACI-R7 — Pure replay

Replay the same corpus from version zero and from each valid checkpoint. Aggregate version/state hash and projection agree; provider, tool, clock and appender spies record zero calls. Gap, hash mismatch or unknown migration fails closed.

### T-ACI-R8 — Logical uniqueness

Run concurrent identical retries and distinct attempts for the same `(group version, seat, round, type)` and logical operation. Exactly one contribution, accepted event, receipt and satisfying result wins; later evidence is retained as rejected/ignored facts.

### T-ACI-R9 — Artifact separation and input manifest

Fixture one request with ordered system/developer/user instructions, history, tools, response schema, context and adapter wrappers. Reordering changes the manifest hash. Raw output alone never creates a contribution; accepted contribution links independently to attempt/output evidence.

### T-ACI-R10 — Mixed-provider conformance

Run fake A/fake B, then Codex/Claude adapters when permitted, with equal capability profiles. Assert
`protocol_equivalent` plans, sealed request semantics, terminal-result schema/parsing, event schemas,
state transitions and decision result; native request bytes may differ and provider-specific metadata
remains namespaced and non-authoritative.

### T-ACI-R11 — Sensitive artifact governance

Assert minimum operator access, audited break-glass, rejection of durable credentials/secrets, encryption requirement outside local development, and tombstone provenance after erasure. Concrete TTL/key fixtures remain blocked pending ADRs.

### T-ACI-R12 — Usage nullability and provenance

Exercise single-turn, tool-heavy, multi-turn, resumed and retried attempts. Missing dimensions remain null through attempt/operation/seat/group/run/dispatch rollups; each rollup exposes observation/missing counts; monetary cost is absent without a versioned price source.

### T-ACI-R13 — Verified opening barrier

At every run state before `ready`, try provider and tool effects; all remain unreleased. Only `audit_opening.verified` for exact canonical content permits release; divergence never does.

### T-ACI-R14 — SQLite durability policy

Startup fixture rejects non-WAL mode, `synchronous` other than FULL, unknown migration/checksum, missing constraints or non-contiguous authoritative streams.

### T-ACI-R15 — Candidate versus official publication

Persist `publication.persisted` for one or both seats and close collection before receipt
verification. Candidate-only messages are absent from the eligible set and quorum. After exact
verification, assert candidate CAS, official `messages` insertion, `attempt.result_accepted` and
`position.accepted` commit atomically and only that official contribution can be counted. Assert the
candidate transaction creates no official `messages` row and that the partial unique active-key
constraint serializes concurrent publishers.

### T-ACI-R16 — Canonical receipt and terminal result

Round-trip the single receipt schema including version, status, event/message/offset/hash/key and
canonical bytes. Return those same bytes on identical retry and place optional
`transport_replayed` only in an outer transport envelope. Mutate each identity field, version,
status and scope independently; verification fails closed. Feed Codex/Claude fixtures through their
native parsers and require the same versioned `AgentTerminalResult`; reject prose-only, ambiguous
multiple-receipt and unknown-version outputs.

### T-ACI-R17 — Invocation materialization boundary

Assert `AgentInvocationPlan -> MaterializedAgentInvocation + EffectiveInputArtifact -> sealed
AgentExecutionRequest -> start effect`. Missing/reordered stages, digest mismatch, adapter direct
journal mutation or start before sealing fails. The adapter may only translate or submit observations.

### T-ACI-R18 — Typed reveal input provenance

Materialize each revealed message as a typed `EffectiveInputEntry`. Alter manifest ID, message ID,
author principal, content hash, visibility policy or ordering; each mutation changes/fails the
manifest as appropriate and no unmanifested peer bytes reach the provider.

### T-ACI-R19 — Sandbox, authority and budget fence

Exercise filesystem/network/process escape, credential leakage, stale cutover epoch, absent
watcher-disable evidence and every `ResourceBudget` ceiling. Launcher validation or launch fails
closed and records an observation without starting the provider. `OQ-SANDBOX` remains an
S-003/L2/W3 real-provider blocker until target-host negative fixtures pass.

### T-ACI-R20 — Causal start prerequisites

Race StartAgentAttempt with collection close, group cancellation and run terminal election. Change
one prerequisite aggregate head after command construction. Start loses with
`prerequisite_head_conflict`; no process/effect starts from stale causal eligibility.

### T-ACI-R21 — Candidate abandonment and replacement

Create an active candidate, then cover all guards independently: nonterminal attempt, known failure,
terminal `unknown` with recoverable terminal evidence, terminal `unknown` without a persisted
no-evidence determination, and retry policy denied. Every case keeps the reservation. Only terminal
`unknown` plus no-recoverable-terminal-evidence plus retry authorization may CAS `active ->
abandoned` and append `publication.candidate_abandoned`. Race that command against receipt
verification; exactly one wins. If abandonment wins, a later terminal is ignored and a new attempt
may create one new active candidate. If verification wins, the official `messages` key prevents any
replacement candidate. Historical candidate rows remain queryable.

### T-ACI-R22 — Reference bundle target delivery

Start with accepted `reference_scout.bundle_committed@1` and
`reference_scout.bundle_delivered@1` facts plus their immutable ordered bundle, then target an
authenticated Attempt in the same dispatch. Assert one preallocated delivery/event identity, one
matching `reference_bundle` entry at the declared ordinal, exact artifact/digest/membership/policy,
`source_bundle_delivered_event_id` equal to the distinct accepted lifecycle-delivery event,
`accepted_event_id` equal to the target-delivery event, strict
source-commit/lifecycle-delivery/target-delivery offset order and atomic acceptance with
`attempt.requested`. Derive target Attempt, seat and agent instance from the authenticated
capability, reject cross-dispatch sources, and obtain ordered membership only from the accepted
commit plus immutable bundle bytes. Crash at every member boundary and require all-or-none.

Mutate, independently, source run, dispatch, artifact, digest, recommendation order, target
attempt/seat/instance, entry ordinal, manifest hash, visibility policy, event identity and
idempotency key; each mutation fails closed. An identical retry returns the original receipt, while
same source/target or scoped key with canonical drift conflicts. A lifecycle event carrying no
membership remains valid source evidence; attempting to derive membership from it fails. Assert the
accepted delivery alone creates no observed-access, declared-reference-use or claim-support fact.

### Bounded authorized peer-input delivery

#### T-ACI-PEER1 — Close remains sealed

Publish two candidates but verify only one receipt. Close the collection and assert that the frozen
set contains only the official message, while every controlled peer-read surface remains denied.

#### T-ACI-PEER2 — Reveal is exact and restart-stable

Restart after `collection.closed`; assert the set remains sealed. Publish one manifest whose ordered
IDs and payload hashes equal the frozen set. Identical retry returns the original receipt; any
membership, order, hash, group or round drift conflicts.

#### T-ACI-PEER3 — Recipient authority is derived

Preallocate the target identity in an authenticated
[AgentInvocationPlan](specs/domain.md#agentinvocationplan). Reject caller-supplied attempt, seat or
cross-group substitutions before any attempt, artifact, delivery, event or effect intent commits.

#### T-ACI-PEER4 — Peer filter and artifact binding

For each fixed seat, derive entries in manifest order, exclude its own contribution, apply
`aci.fixed-two-seat-peer-reveal@1`, and verify every remaining entry against the official
contribution, immutable artifact and manifest-entry payload hash. Reject a finalized derived set
containing a self, denied, absent, unaccepted or out-of-order entry.

#### T-ACI-PEER5 — Atomic acceptance

Inject a failure after each write in the complete acceptance unit:
finalized `EffectiveInputArtifact` metadata, `MaterializedAgentInvocation`, request binding, sealed
`AgentExecutionRequest`, `Attempt`, `PeerInputDelivery`, `peer_input.materialized`,
`attempt.requested` and the unclaimed effect intent. A fresh connection observes all members or
none, never a partial binding.

#### T-ACI-PEER6 — Stable receipt and conflict

Retry the same `(reveal_manifest_id,target_attempt_id,idempotency_key)` and semantic digest; require
the byte-identical stored `PeerInputDeliveryReceipt` and no new artifact/event. Change any source,
recipient, entry, policy, artifact, hash or key-bound byte and require a permanent conflict.

#### T-ACI-PEER7 — No direct peer-read or provider execution

Inspect the agent capability surface before and after reveal: it contains publication and declared
non-peer tools only, never list/search/read/export/debug over peer content. Accepted materialization
leaves the effect pending and a provider-start spy at zero.

### Phase-A bounded runtime-integrity repairs

#### T-ACI-PHASEA-I1 — Follow-up identity is mandatory

Create a terminal prior host-workflow turn with `agent_id = null`, then attempt a follow-up naming
an arbitrary target. Require an authorization failure and zero new binding rows, events, artifacts
or receipts. Repeat with a persisted non-empty identity and prove that only exact target equality
is accepted; mismatch fails with the same zero-write guarantee.

#### T-ACI-PHASEA-I2 — Peer bytes are rehashed at materialization

After official publication and reveal, alter only the stored body bytes of one peer artifact while
leaving its stored content hash, contribution hash and reveal hash unchanged. Materialization must
recompute the digest from the body, raise `IntegrityError` and commit no effective-input artifact,
materialized invocation, request, Attempt, delivery, event, receipt or effect. The unchanged
fixture must still materialize successfully and retry byte-identically.

#### T-ACI-PHASEA-I3 — Active BUS sources are startup-bound

Require the Stage-E source manifest to bind
`implementations/server/runtime/reveal_delivery.py` and
`implementations/server/runtime/migrations/011_bus_reveal_delivery.sql` by exact SHA-256.
Independently mutate each loaded source in an isolated fixture and require startup/source-integrity
verification to fail closed before the orchestration bridge or BUS path becomes usable.

### T-ACI-S1 — Run lifecycle and terminal precedence

Generate every listed transition plus every invalid source/event pair. Confirm explicit human cancellation, technical failure and protocol ceiling map to their distinct audit reasons; later terminal observations cannot replace the first CAS winner; `execution_terminal` is not `closed`.

### T-ACI-S2 — Group decision and sealing

Two equal valid votes yield consensus; two conflicting valid votes yield dissent; one/malformed vote yields no quorum and no verdict. Slice 0 cannot enter deliberation; one group result wins and preserves dissent references.

### T-ACI-S3 — Attempt cancel races

Permute cancel request/acknowledgement with completion, failure, unknown and cancelled observations. Acknowledgement is nonterminal, one terminal wins by accepted ordering, and non-retryable unknown effects are never automatically repeated.

### T-ACI-C1 — Transaction crash boundaries

Cover before begin, after each insert before commit, and after commit before response. Recovery returns either no acceptance or the stable complete acceptance.

### T-ACI-C2 — Audit append crash reconciliation

Crash after physical append/before journal acknowledgement. Identical row becomes already-applied/verified; absent invokes appender then verifies; divergent enters reconciliation-required and releases nothing.

### T-ACI-C3 — Closed-before-reveal restart

Restart after `collection.closed` and before `reveal.published`. Replay restores the frozen eligible set and sealed ACL; exactly one canonical manifest can later publish.

### T-ACI-C4 — Publish-to-terminal recovery

Inject crashes before/after `publication.persisted`, before/after provider terminal artifact commit,
before/after receipt verification and before response. Recover by `(attempt_id, operation_id,
logical_message_key)`. The outcome is candidate-only or exactly one atomic official event pair;
there is never duplicate acceptance and candidate-only evidence never enters quorum. Add a provider
that becomes terminal `unknown` without terminal evidence: the active key remains reserved until the
audited abandonment CAS commits, after which one authorized retry may publish. Crash before/after
that CAS converges without losing or reviving candidate evidence.

### T-ACI-C5 — Effect-outcome idempotency matrix

For one effect, exercise the matrix below before and after a simulated lost response:

| Stored effect state | Submitted epoch | Submitted outcome digest | Expected result |
|---|---|---|---|
| `claimed` | current | new digest | atomically commit receipt/event/head/effect terminal fields |
| `claimed` | stale | new digest | reject stale epoch; write nothing |
| terminal | any/stale | same accepted digest | return byte-identical stored command receipt; write nothing |
| terminal | any/stale | different digest | permanent `OUTCOME_CONFLICT`; write nothing |
| nonterminal but not `claimed` | any | new digest | reject invalid effect status; write nothing |

Run every SQL failpoint around the winning terminal transaction. This proves terminal digest
comparison occurs before the `claimed`/epoch requirement while new outcomes remain claim-fenced.

### T-ACI-P1 — Probe regression corpus

Port the ten probe behaviors: success/durable receipt, missing receipt, forged receipt, invalid payload, identical retry, idempotency conflict, logical duplicate, concurrent serialization, late publication rejection and publish-only tool surface. JSONL/environment context are not production fixtures.

### T-ACI-ETA1 — External-tool authority classification

Evaluate Pydantic core, Octopus Runtime, Eve, PydanticAI, Zod and the local subprocess implementation
against the per-fact authority matrix. The fixture fails if Octopus/Eve owns kernel lifecycle/replay,
PydanticAI becomes a schema dependency, or a boundary helper receives journal/ledger write authority.

### T-ACI-ETA2 — Canonical Python contract vectors

Under an explicitly pinned Pydantic version, validate equivalent/mutated vectors for omitted versus
null fields, Unicode normalization, numeric representation, property ordering and schema version.
Assert exact canonical bytes and SHA-256 digests independent of ordinary Pydantic dump defaults.
Until the pin and vectors are accepted in W0, this test is a blocking specification, not a pass claim.

### T-ACI-ETA3 — Derived Node boundary parity

The current fixture asserts that no Node surface is registered as an ACI canonical-contract
consumer. If one is later inventoried, require generated/derived validation and shared golden-vector
parity; a hand-authored second normative schema must fail admission.

### T-ACI-ETA4 — Subprocess provider admission gate

Execute the common adapter suite and target-host negative fixtures for sandbox escape, credential
visibility, process-tree cancellation, crash/restart reconciliation, receipt verification and usage
attribution. Assert the provider process is never created except by `SandboxLauncher` and that a
failed criterion leaves the adapter unavailable.

### T-ACI-ETA5 — Sole-writer evidence completeness

Validate one [SoleWriterEvidenceBundle](specs/domain.md#solewriterevidencebundle) for the exact writer and
host profile. Remove each process-identity, ACL, writer-inventory or negative-bypass component in
turn and assert EG-1 remains open. A bundle containing only the single-import lint must fail.

## Canonical Vault Read Contracts

### T-CVR-1 — Selector and root confinement

Exercise relative, absolute, case-mismatched, empty, dot and parent segments against
lexical and resolved roots. Only normalized repository-relative `.md` files under one
effective root can enter a snapshot.

### T-CVR-2 — Link and hidden denial

Create hidden components and platform-supported symlink, junction or reparse fixtures.
Every list and direct get denies them without exposing the resolved target.

### T-CVR-3 — Privacy and direct/list parity

For `allow_private=false`, a private existing file, a denied file and a missing file all
return the same `not_found` shape. The same selector is absent from list output. Repeat
with the authorized scope and assert list/get parity. Exercise staged precedence with
private+malformed, private+oversized and hidden+oversized sources: an unprivileged call
does not enumerate them or charge them to public aggregate/result caps; a privileged
private source is parsed as residue when applicable and consumes its caps. Assert no
denied metadata or failure class distinguishes a private source from missing.

### T-CVR-4 — Snapshot coherence under mutation

Inject add, remove and byte-change failpoints during capture. A call returns projections
whose source digests all belong to one snapshot or returns `snapshot_conflict`; it never
mixes observations. Assert list captures all admitted visible sources while direct get
validates and captures only its selected source. Mutation during quarantine/admission
recheck must either enter the selected admitted snapshot coherently or conflict; direct
get must not scan or fail because an unrelated admitted source changes.

### T-CVR-5 — Encoding, frontmatter and residue

Cover UTF-8, BOM, invalid encoding, current and legacy frontmatter, invalid YAML,
unterminated fences, absent Connections, canonical tables, legacy headers and free-form
rows. For invalid UTF-8 assert exactly one ordered `invalid_utf8`
`VaultNodeProjection` with the source byte digest and safe byte-span locator,
`title=null`, `sections=[]`, `connections=[]`, typed frontmatter residue, no exposed
undecoded or decoded source bytes, and one consumed artifact-result slot. No fixture is
silently repaired or dropped and no malformed source invents an edge.
Assert exact-limit success and `+1` `parse_limit_exceeded` whole-source residue for:
65,536 frontmatter bytes, depth 32, 10,000 YAML nodes, 4,096 collection items and
32,768 scalar UTF-8 bytes. Aliases, merge keys and custom tags are forbidden residues,
not expansions or repairs.

### T-CVR-6 — Deterministic order and digests

Permute filesystem enumeration and declaration discovery. Artifact order, logical-edge
order, supporting-declaration order, canonical bytes and SHA-256 digests remain equal.
Golden vectors assert exact compact UTF-8 JSON bytes for `aci.cvr.snapshot/v1` and
`aci.cvr.node/v1`, fixed field order, NFC normalization, required nulls, integer-only
numbers, float/NaN rejection, deterministic escaping, exact `snapshot_digest` and exact
node `projection_digest`.

### T-CVR-7 — Bounded edge normalization

Collapse exact same-direction duplicates and a matching `derives-from`/`grounds` pair.
Assert all other relation directions/spellings remain distinct. This is a CVR-002
endpoint-resolution/logical-projection test; CVR-001 must not fold raw declarations.

### T-CVR-8 — Unresolved edge evidence

Use broken paths, duplicate wiki names, external targets and malformed rows. Assert typed
raw residue remains source-located and no logical endpoint identity is minted. In
CVR-001 every recognized but not resolved target is preserved with
`resolution=unresolved`; malformed rows remain `malformed`. In CVR-002 assert endpoint
resolution changes only the derived resolution/logical view and never rewrites the raw
declaration.

### T-CVR-9 — Stale and projection conflicts

Mutate a selected file after recording its digest and mutate logical support after
recording a projection digest. Assert `selector_stale` and `projection_conflict`
respectively, with no host path leakage.
Execute the total per-method precedence table with pairwise collisions for every
adjacent stage and the named nonadjacent security pairs: invalid-request+private,
private+oversized, hidden+oversized, capture-race+stale and
snapshot-conflict+projection-conflict. Assert exactly one stable outcome and no lower
stage observation.

### T-CVR-10 — Hard bounds and complete results

Cross each cap independently by one while all other caps remain permissive:

1. one candidate source has `max_file_bytes + 1` bytes;
2. aggregate candidate bytes are `max_total_bytes + 1`, with every source within
   `max_file_bytes`;
3. candidate source count is `max_files + 1`, with byte caps respected; and
4. complete top-level projected item count is `max_results + 1`, with source and byte caps respected.

For every case assert only `result_set_too_large`: no partial items, continuation or reusable
snapshot reference. Run the result-cap boundary independently for every method:
`list_artifacts` counts top-level nodes, `get_artifact` counts exactly its returned
node, `list_edges` counts top-level logical edges, and `get_edge` counts exactly its
returned logical edge. Nested sections, declarations and residue never count
separately; one whole-source invalid item counts as one node. For both direct gets,
verify that an effective `max_results` below one is `policy_unavailable`, not a partial
or empty success.
For `get_edge`, add an unrelated visible oversized/candidate-count source and assert
the complete edge-source candidate set closes with `result_set_too_large` before
capture/parsing/selection, identically to `list_edges`; selecting a small edge does not
bypass corpus caps.
For parser ceilings, independently exercise exact and `+1` cases from T-CVR-5 and
assert `parse_limit_exceeded` is one whole-source result item rather than
`result_set_too_large`; source, aggregate and result caps retain their existing
call-closing precedence after privacy exclusion.

### T-CVR-11 — Inventory semantic independence

Run the same corpus and scope with the optional inventory absent, correct and stale.
For identical admitted source bytes, effective scope and parser version, the canonical
result and admission decision remain byte-equivalent. Mutate only an inventory
projection and assert it cannot change admission, result bytes or digests; mutate the
admitted source bytes and assert the source change, rather than inventory state,
controls the next coherent result. This is the executable mapping for CVR-R1.

### T-CVR-12 — Zero effects and provenance

Install spies for filesystem writes, ledgers, caches, events, `SourceObservation`, APT
extraction/reference facts and runtime artifacts. All counters remain zero after each
success and closed error.

### T-CVR-AUTH1 — Nonrecursive guard bootstrap

Attempt to verify or finalize GUARD bootstrap through the guard it creates and assert rejection.
The only accepted fixture uses an exact root-owned one-time bootstrap authorization, external
expected digests/session, the external trusted executor and exactly one external authority-owned
bootstrap finalizer; its diff is confined to the descriptor-listed paths.

### T-CVR-AUTH2 — Canonical authority identities

Exercise authorization preimages with omitted versus injected `authorization_id` and derived
paths, field reorderings, duplicates, Unicode variants and byte drift. Only the specified domain
separator and compact canonical JSON derive the expected ID/path. Repeat for claim and
`ExecutionReceipt`; assert exactly three per-execution artifacts exist. Reject a missing,
duplicated or reordered owner slot, any non-`ACCEPT` decision, acceptance-set drift, principal or
credential mismatch, packet/policy/repository/SWU/audience transplant, nonce replay and
non-canonical UTC. Hash equality alone never satisfies the authenticated-principal check. Golden
vectors independently derive the launch-context ID and digest from its body/envelope prefixes and
reject field-order, owner-binding, timestamp-bound and envelope drift.

### T-CVR-AUTH3 — Closed descriptor and scope

Try caller-supplied paths, commands, test IDs, index, receipt locator and scope. Each fails before
effects. Only the enumerated SWU and its exact deterministic descriptor can reach direct worker
invocation. Reject a missing, workspace/argv/environment-supplied, adulterated or expired
`AuthorityLaunchContext`; reject root/executor/finalizer, repository binding, policy, audience,
session, authenticated three-owner binding or launch-context drift. The accepted context arrives
only through the injected external authority-provider boundary.

### T-CVR-AUTH4 — Sole terminal authority

Make a worker or root return forged/writer-created receipt material. Assert it remains
non-authoritative. For GUARD bootstrap only the external authority-owned bootstrap finalizer may
create the receipt; for CVR-001/002 only the common guard/finalizer may do so. Exactly one is
applicable, never both. Reject a receipt whose finalizer attestation, launch-context digest or
executor/finalizer principal differs. Identical receipt bytes read idempotently and divergent bytes
fail integrity. Round-trip every closed nested receipt schema and reject wrong type, unknown field,
invalid state/hash/null pairing, unsorted residue/effect/predecessor data and an outcome/reason code
outside the descriptor. Reject repository/host locator kind confusion, locators outside their
authorized scopes, non-object residual locators and every outcome/reason combination absent from
the closed matrix. Reject duplicate predecessor IDs, duplicate effect/residual `(kind, locator)`
keys and cleanup-status/cardinality mismatches.

### T-CVR-AUTH5 — Crash and cancellation matrix

Test hard crash with pristine scope and same-session retry; partial write, drift or unknown cleanup
with no reinvocation and root-requested `BLOCK` from the one applicable finalizer; controlled
interruption with terminal receipt; and post-receipt replay rejection. Assert root never writes a
receipt and verify exact residual-path and cleanup evidence. Race two claims and require exactly one
create-exclusive winner; reject a different-session retry, expired immutable lease, stale launch
context, nonce reuse, a claim before authorization issuance, `claimed_at >= lease_expires_at`,
launch observation before `claimed_at`, lease after authorization expiry and delete-and-replay
evidence. Assert no lease, renewal,
revocation or fourth authority artifact is persisted.

### T-CVR-AUTH6 — CVR-002 predecessor binding

Mutate independently the CVR-001 PASS receipt, byte baseline, allowed delta and each pre-write
hash. Every mismatch blocks before invocation. The accepted fixture reruns the complete CVR-001
suite before CVR-002 tests and records both groups and the exact final delta.

### T-ACI-AUTH1 — Runtime-only confirmed dispatch

Submit the same valid pending proposal with each pre-confirmation routing choice. For
`legacy-managed`, assert the runtime confirmation endpoint returns its typed rejection and creates
zero `ConfirmedDispatch`, `Run`, journal fact and audit effect while preserving the legacy/session
path. For `runtime-managed`, assert one accepted confirmation creates exactly one immutable
`ConfirmedDispatch` and exactly one `Run`; identical replay returns the stable receipt and cannot
create a second pair.

### T-ACI-ARD1 — Exact reference-bundle delivery

Given one accepted Scout commit, its immutable ordered bundle, its distinct lifecycle-delivery fact
and an authenticated target capability in the same dispatch, start one Attempt. Assert exactly one
`reference_bundle` entry at the recorded ordinal of the delivery's `EffectiveInputArtifact`; assert
that artifact's `attempt_id = target_attempt_id` and
`manifest_hash = hash(canonical(orderedManifest)) = effective_input_manifest_hash`. Compare the
entry, delivery and `reference_scout.bundle_delivered_to_agent@1` specifically for artifact,
digest, delivery ID and visibility policy. Compare the delivery and target event specifically for
ordered recommendations, capability-derived recipient, manifest identity/hash/ordinal,
idempotency key, event identity and journal offset.

### T-ACI-ARD2 — Bundle authority and integrity

Mutate independently committed recommendation order/membership, artifact bytes, artifact digest,
ScoutRun, artifact identity and lifecycle-delivery digest. Each mutation rejects the complete start.
Supplying or inferring `recommendation_ids` from `reference_scout.bundle_delivered@1` also fails:
only the accepted commit plus `ordered_recommendation_ids(bundle_bytes)` may establish membership.
Also test a missing or unaccepted commit, a missing or unaccepted lifecycle-delivery fact, and equal
or reversed journal order at either boundary. Unless
`commit.offset < lifecycle_delivery.offset < target_delivery.offset`, reject StartAgentAttempt and
accept none of its transaction members.

### T-ACI-ARD3 — Recipient and dispatch authority

Try a ScoutRun from another dispatch and inject matching or conflicting target Attempt, seat and
agent-instance fields outside the authenticated capability. Reject all variants and accept no
Attempt or delivery fact. The passing fixture derives all recipient identities from the capability
and proves equality with the accepted target Attempt.

### T-ACI-ARD4 — Atomic delivery and idempotency

Inject failure after each member of the StartAgentAttempt unit: finalized effective-input metadata,
sealed request binding, Attempt, AgentReferenceDelivery, target-delivery event, `attempt.requested`
and launch effect intent. Reopen and assert all members or none. Identical retry returns the
original receipt and IDs; any source, recipient, membership, policy, manifest, digest or scoped-key
drift conflicts without a second delivery.
Instrument preparation to assert `agent_reference_delivery_id` and target `accepted_event_id` exist
before manifest canonicalization and request sealing, and that the manifest embeds that exact
preallocated delivery ID. Assert acceptance performs no post-acceptance manifest rewrite; a failed
settlement leaves no accepted dangling manifest or delivery reference.

### T-ACI-ARD5 — Delivery evidence boundary

Project an accepted target-agent delivery without any host source observation or declared reference
use. Assert the ACI fact says only that exact bytes were included in observable effective input and
that no ACI projection reports access, reading, declared use or claim support. Those later evidence
axes remain independently owned downstream.

## Fixture Corpus

| Fixture | Contents |
|---|---|
| `fixed-two-seat-proof@1` | Two seats, one collection round, reveal, vote and commit with consensus/dissent/no-quorum variants |
| `command-acceptance-boundaries@1` | Failpoints around receipt/events/head/intents and response |
| `audit-reconcile@1` | Absent, byte-identical and same-identity divergent opening/close rows |
| `effective-input@1` | Ordered instructions/history/tools/schema/context/wrappers and controlled reorder mutations |
| `provider-conformance@1` | Equal fake-provider capability profiles plus nullable usage variants |
| `provider-terminal-parsing@1` | Codex/Claude native terminals, canonical result/receipt versions and malformed variants |
| `invocation-sealing@1` | Plan/materialization/effective input/sealed request plus digest and stage-order mutations |
| `sandbox-authority-budget@1` | Escape attempts, stale fences, cutover evidence and every typed budget ceiling |
| `publish-terminal-crash@1` | Failpoints from candidate commit through terminal and official verification acknowledgement |
| `candidate-abandonment@1` | Unknown/no-evidence/retry-policy guards, verifier race, late terminal and replacement publication |
| `effect-outcome-matrix@1` | Claimed/current, claimed/stale, terminal/same digest, terminal/different digest and lost-response retries |
| `bus-probe-regression@1` | Ten behaviors from the executable probe, expressed against production interfaces |
| `external-tool-authority@1` | Allowed seams and prohibited authority for every evaluated external tool |
| `canonical-python-contracts@1` | Omitted/null, Unicode, numbers, ordering, version and digest vectors |
| `provider-admission@1` | Common adapter, sandbox, credential, cleanup, recovery, receipt and usage evidence |
| `sole-writer-bundle@1` | Complete and component-missing host-scoped EG-1 evidence bundles |
| `reference-bundle-delivery@1` | Accepted commit/lifecycle facts, immutable ordered bundle, capability-derived recipient, manifest, retry drift and atomic failpoints |

## Known Gaps

- `implementations/tests/runtime/aci-test-traceability.json` records only bounded evidence for
  T-ACI-R3/R5/R6/R7/R15/R16, T-ACI-C1/C2/C4 and T-ACI-ETA2. Its validator proves that every
  recorded ID and Python test selector exists; it does not promote those mappings to complete
  family coverage. Unmapped requirements and the remaining steps inside mapped requirements stay
  planned until dedicated fixtures close them.
- Concrete retention, key-management and crypto-erasure timing tests await the OQ-ACI9 ADRs.
- Real Codex, second-provider and mixed-provider empirical completeness tests remain L2/L3 gates.
- Host-loss, multi-host and multi-tenant recovery are outside the initial contract.
- `OQ-SANDBOX` remains an explicit S-003/L2/W3 real-provider blocker until target-host launcher
  isolation tests pass; it does not block fake-adapter Slice 1 work.
- OQ-ETA1's canonical projection, golden vectors and declared Pydantic pins are accepted. Broader
  runtime promotion still requires a digest-bound receipt proving resolution and execution of those
  exact dependency versions, as recorded in `specs/SPEC.md`.
- OQ-ETA2/B-003 remains open for materializer cutover until a complete target-host
  `SoleWriterEvidenceBundle` passes T-ACI-ETA5. W0 freezes its schema and negative-test
  specification; TASK-020 supplies the physical target-host proof.
- T-ACI-ARD1 through T-ACI-ARD5 specify the next bounded slice only; no runtime test implementation
  or implementation-completeness claim is made by this document.

## Out of Scope

- Test code, runner choice and database-library implementation.
- Statistical claims about decision quality or model independence.
- Provider billing reconciliation without an explicit provider price/source contract.
