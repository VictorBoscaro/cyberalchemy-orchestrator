---
tags: [agents-communication-infra, spec, test]
node_type: spec
is_session: false
layer: application
nature: [procedural, technical]
status: draft
version: 0.7.2
last_updated: 2026-09-01
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
| [T-ACI-HOST1](#t-aci-host1--producer-bound-host-output-and-atomic-launch) | One completed producer receipt and active authorized mapping materialize one exact consumer manifest and atomic launch authorization | [ACI-R20](specs/rules.md#aci-r20--host-terminal-output-is-producer-bound-visibility-authorized-and-launch-atomic) |
| [T-ACI-CONT1](#bounded-resumable-feedback) | Suspending a terminal author turn persists reconstruction evidence and starts no effect | [SuspendAgentContinuation](specs/operations.md#suspendagentcontinuation) |
| [T-ACI-CONT2](#bounded-resumable-feedback) | Accepted reviewer output alone, not a bus poll, satisfies the declared feedback slot | [ACI-R21](specs/rules.md#aci-r21--continuation-is-resumable-state-never-hidden-authority) |
| [T-ACI-CONT3](#bounded-resumable-feedback) | Author turn 1 input contains base, two exact official bus outputs and revision instruction in canonical order | [Runtime continuation input materialization](specs/operations.md#runtime-continuation-input-materialization-contract) |
| [T-ACI-CONT4](#bounded-resumable-feedback) | Same-session resume preserves seat and agent instance while creating a new attempt/turn | [AgentContinuationLifecycle](specs/states.md#agentcontinuationlifecycle) |
| [T-ACI-CONT5](#bounded-resumable-feedback) | Definitive handle loss permits only one explicit reconstruction after the abandoned target is terminal | [ReconstructAgentContinuation](specs/operations.md#reconstructagentcontinuation) |
| [T-ACI-CONT6](#bounded-resumable-feedback) | Unknown resume outcome never starts reconstruction automatically | [AgentAdapter](specs/interfaces.md#internal-agentadapter) |
| [T-ACI-CONT7](#bounded-resumable-feedback) | Resume, cancellation and expiry races elect one terminal continuation outcome | [AgentContinuationLifecycle](specs/states.md#agentcontinuationlifecycle) |
| [T-ACI-CONT8](#bounded-resumable-feedback) | Crash/retry across suspend, materialize, request and effect boundaries converges to one target attempt/effect | [ResumeAgentContinuation](specs/operations.md#resumeagentcontinuation) |
| [T-ACI-CONT9](#bounded-resumable-feedback) | Every lifecycle state/event pair not listed by the transition table rejects without mutation | [AgentContinuationLifecycle](specs/states.md#agentcontinuationlifecycle) |
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
| [T-ACI-AUTH1](#t-aci-auth1--runtime-only-confirmed-dispatch) | Legacy routing creates no ACI runtime entity; golden runtime confirmation creates the complete bounded atomic unit | [ACI-R22](specs/rules.md#aci-r22--runtime-confirmation-is-presentation-bound-derived-and-atomic) |
| [T-ACI-AUTH2](#t-aci-auth2--canonical-authority-and-derived-identities) | Every golden document/digest and every derived ID independently reproduces, including the derivation-contract digest bound into authority | [CONF-R2](specs/confirmation-authority.md#conf-r2--digest-separation), [CONF-R4](specs/confirmation-authority.md#conf-r4--versioned-derived-identities) |
| [T-ACI-AUTH3](#t-aci-auth3--trusted-observation-boundary) | Issuer, evidence, principal, channel, action, time, dispatch/revision and displayed-digest drift reject before mutation | [CONF-R1](specs/confirmation-authority.md#conf-r1--trusted-observation) |
| [T-ACI-AUTH4](#t-aci-auth4--digest-domain-lineage) | Pending, spec and authority digests verify only their declared byte domains and invalidate the correct lineage | [CONF-R2](specs/confirmation-authority.md#conf-r2--digest-separation) |
| [T-ACI-AUTH5](#t-aci-auth5--bounded-projection-and-mapping-closure) | Graph/ceiling/mapping/selector/identity drift rejects the entire confirmation | [CONF-R3](specs/confirmation-authority.md#conf-r3--bounded-deterministic-projection), [CONF-R4](specs/confirmation-authority.md#conf-r4--versioned-derived-identities), [CONF-R5](specs/confirmation-authority.md#conf-r5--complete-graph-binding) |
| [T-ACI-AUTH6](#t-aci-auth6--two-layer-replay-and-conflict) | Key replay and dispatch-authority replay converge independently under one writer transaction | [CONF-R7](specs/confirmation-authority.md#conf-r7--two-layer-replay-and-conflict) |
| [T-ACI-AUTH7](#t-aci-auth7--atomic-failure-and-reopen) | Every transaction failpoint is all-or-none; lost response and reopen return the first receipt | [CONF-R6](specs/confirmation-authority.md#conf-r6--atomic-local-acceptance) |
| [T-ACI-AUTH8](#t-aci-auth8--confirmation-effect-ceiling) | Success stops at one unclaimed pending audit-opening intent with zero external or continuation action | [CONF-R8](specs/confirmation-authority.md#conf-r8--success-ceiling) |
| [T-ACI-ARD1](#t-aci-ard1--exact-reference-bundle-delivery) | One accepted Scout bundle becomes one exact typed target-attempt input entry and target-delivery fact | [AgentReferenceDelivery](specs/domain.md#agentreferencedelivery) |
| [T-ACI-ARD2](#t-aci-ard2--bundle-authority-and-integrity) | Commit plus immutable bytes, never lifecycle delivery, determine ordered recommendation membership | [ReferenceScoutBundleToEffectiveInput](specs/mappings.md#referencescoutbundletoeffectiveinput) |
| [T-ACI-ARD3](#t-aci-ard3--recipient-and-dispatch-authority) | Capability-derived recipient and same-dispatch guards reject identity injection or cross-dispatch delivery | [DeliverReferenceScoutBundleToAgent](specs/operations.md#internal-transition--deliverreferencescoutbundletoagent) |
| [T-ACI-ARD4](#t-aci-ard4--atomic-delivery-and-idempotency) | Preallocated identities, complete acceptance and retries yield one delivery or none | [IF-ACI-14](specs/interfaces.md#interface-invariants) |
| [T-ACI-ARD5](#t-aci-ard5--delivery-evidence-boundary) | Accepted inclusion is never promoted to access, declared use or claim support | [`reference_scout.bundle_delivered_to_agent@1`](specs/events.md#reference_scoutbundle_delivered_to_agent1) |
| [T-ACI-PC1](#t-aci-pc1--closed-schema-validation) | Every protocol document and result is recursively closed and strict | [Protocol compilation](specs/protocol-compilation.md#canonical-contract-common-to-every-schema) |
| [T-ACI-PC2](#t-aci-pc2--canonical-golden-vectors) | Exact canonical bytes and qualified digests are stable | [PC-R1](specs/protocol-compilation.md#rules-and-invariants) |
| [T-ACI-PC3](#t-aci-pc3--digest-lineage-and-invalidation) | Every supplied digest verifies exact bytes and invalidates stale lineage | [PC-R2/R3/R11](specs/protocol-compilation.md#rules-and-invariants) |
| [T-ACI-PC4](#t-aci-pc4--explicit-parameters-only) | Parameters admit no default, coercion, inference or undeclared placeholder | [SkillProtocolInvocation](specs/protocol-compilation.md#skillprotocolinvocation) |
| [T-ACI-PC5](#t-aci-pc5--total-obligation-disposition) | Obligation mapping is total, unique and fail-closed | [ObligationDisposition](specs/protocol-compilation.md#obligationdisposition) |
| [T-ACI-PC6](#t-aci-pc6--closed-dag) | The built-in recipe DAG is bounded, closed, acyclic and terminal-reachable | [DAG validity](specs/protocol-compilation.md#dag-validity) |
| [T-ACI-PC7](#t-aci-pc7--logical-capability-ceiling) | Candidate carries logical needs and no effective grant | [PC-R8](specs/protocol-compilation.md#rules-and-invariants) |
| [T-ACI-PC8](#t-aci-pc8--restart-determinism) | Equal requests produce byte-identical candidates/results across restarts | [PC-R9](specs/protocol-compilation.md#rules-and-invariants) |
| [T-ACI-PC9](#t-aci-pc9--pure-compilation) | Compilation has zero clock, registry, runtime or external effects | [PC-R10](specs/protocol-compilation.md#rules-and-invariants) |
| [T-ACI-PC10](#t-aci-pc10--artifact-only-persistence) | Optional storage is idempotent and creates no runtime authority | [Artifact seam](specs/protocol-compilation.md#artifact-persistence-seam) |
| [T-ACI-PC11](#t-aci-pc11--built-in-fixture-traceability) | Every golden candidate field traces to explicit fixture input | [Mapping](specs/protocol-compilation.md#protocolinputstodispatchcandidate) |
| [T-ACI-PC12](#t-aci-pc12--candidate-authority-isolation) | Candidate cannot substitute for DispatchSpec or create runtime entities | [Ownership boundary](specs/protocol-compilation.md#ownership-and-authority-boundary) |

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

### T-ACI-HOST1 — Producer-bound host output and atomic launch

Persist exact completed producer bytes as one content-addressed
[Artifact](specs/domain.md#artifact), then persist the separately identified
[HostTerminalResponseArtifact](specs/domain.md#hostterminalresponseartifact) and completed
[HostTerminalResponseReceipt](specs/domain.md#hostterminalresponsereceipt). Prove equal content bytes
from another producer turn reuse content identity without reusing producer attribution or receipt
identity. Failed, cancelled and unknown producer outcomes carry no completed receipt and cannot
satisfy the slot.

For one L0 consumer, admit exactly one active confirmed
[SourceToSlotMapping](specs/domain.md#sourcetoslotmapping), its authorized visibility policy and
matching [HostWorkflowBindingRef](specs/domain.md#hostworkflowbindingref). Materialize exactly one
canonical [WorkflowInputManifest](specs/domain.md#workflowinputmanifest) entry whose artifact ID,
content hash, producer receipt and mapping identity match the source. Require the
[HostWorkflowTurnBinding](specs/domain.md#hostworkflowturnbinding) to reproduce the same workflow,
consumer, mapping, manifest, cancellation and supersession heads immediately before acceptance.

Independently inject no mapping, two active mappings, wrong/unfinished receipt, unauthorized
visibility, artifact/hash drift, missing/duplicate entry or noncanonical entry encoding/order, source or consumer
identity drift and stale prerequisite heads. Every case rejects with no launch authorization or
effect intent. Inject a crash around `host_workflow.turn_launch_authorized` and the one pending
launch effect intent; a fresh connection observes both or neither, and no provider effect is
claimed or started. Fan-in, optional slots and non-success completion policies remain outside this
L0 obligation.

### Bounded resumable feedback

Use one frozen dispatch fixture expanded to `author:turn0 -> reviewer:turn0 -> author:turn1`, with
one author continuation, two exact `ContinuationInputMapping` records, their official contribution
receipts and a loop ceiling of one.

#### T-ACI-CONT1 — Suspension is effect-free

Complete author turn 0, finalize its reconstruction snapshot and suspend it while the review slot
is absent. Assert one continuation/event/receipt unit, zero provider/tool/bus-read effects and no
nonterminal author attempt. Retry byte-identically; mutate snapshot, mapping, target turn or handle
digest and require conflict. Substitute a continuation identity not preallocated by the confirmed
turn graph and require rejection with no write.

#### T-ACI-CONT2 — Feedback eligibility is journal-derived

Publish candidate review bytes without accepting the required producer receipt and assert no
resume. Accept the exact reviewer terminal/output receipt and mapping, then assert eligibility.
Agent polling, a caller-supplied artifact path and a cross-dispatch receipt remain ineffective.

#### T-ACI-CONT3 — Canonical revision input

Accept author and reviewer publication receipts through the bus and assert author turn 1 contains,
in frozen order, base snapshot, author turn-0 official output, reviewer official output and revision
instruction with exact artifact IDs/hashes/policies. Substitute a raw output, candidate, host
terminal receipt, caller path or cross-dispatch contribution; each must reject before request
acceptance. Omit or reorder an entry and require rejection or a different digest. Inject zero and
multiple candidate/contribution chains for one preallocated message selector and require a closed
ambiguity rejection with no authoritative write.

#### T-ACI-CONT4 — Same-session identity

With an available fake-adapter handle, accept one resume unit and observe provider running. Assert
same seat and agent instance, new attempt and turn ordinal, exact effective input and one effect.

#### T-ACI-CONT5 — Definitive-loss reconstruction

Return `definitively_unavailable` before provider start. Assert the same-session target/effect is
terminal `failed(continuation_unavailable)` and the continuation is `reconstruction_eligible`.
When and only when reconstruction was confirmed, accept one separate replacement attempt with the
same seat, new agent instance and same effective-input semantics. Retry returns the same unit;
unknown/active prior work, a second replacement or absent permission rejects.
Also cover a provider preconfirmed with `resume=unsupported`: matching immutable adapter capability,
source attempt and terminal no-handle evidence may enter `reconstruction_eligible` without calling
resume. Mutate the adapter/capability digest, source attempt or terminal observation, or omit prior
confirmation, and require rejection/unknown with no reconstruction authority. Inject a crash
between every reconstruction acceptance member and require all-or-none SQL authority for the
stable command receipt, `continuation.reconstruction_requested`, `attempt.requested`, replacement
instance, finalized input metadata, attempt, materialized invocation, request binding, sealed
request and effect; prepared orphan bytes remain non-authoritative.

#### T-ACI-CONT6 — Unknown is not unavailable

Inject loss after resume invocation where provider outcome cannot be reconciled. Record
`continuation.resume_unknown` and assert no replacement/start effect, even after restart or
duplicate scheduler evaluation. Reconciliation may move the same target only to `resumed`,
`reconstruction_eligible` with definitive no-start evidence, or the cancellation path.
An absent handle without the exact preconfirmed unsupported capability and matching terminal
no-handle evidence must remain unknown and create no replacement.

#### T-ACI-CONT7 — Cancel/expire/resume race

Race resume eligibility, authorized cancellation and journal-backed deadline commands at the same
continuation version. Exactly one CAS path wins; late facts remain observable and cannot launch.
After an effect claim, deadline handling must enter cancellation/reconciliation rather than mark
the continuation expired while provider work may exist.
When cancellation wins before claim, assert the pending resume/start effect atomically becomes
`failed(cancelled_before_claim)`, `claimEffect` rejects it forever, and the target attempt follows
the local no-start cancellation path without invoking the adapter.
For suspended-handle disposal, assert `acknowledged` and `unknown` observations remain
`cancel_requested`; only a correlated `disposed` observation produces `continuation.cancelled`.
Mismatched command ID, handle digest, adapter cursor or worker epoch rejects without transition.

#### T-ACI-CONT8 — Atomicity and replay

Inject a crash around every member of suspension and resume acceptance. Finalized snapshot/input
payload bytes prepared before SQL may remain as non-authoritative orphan artifacts and must be
collectable; they grant no continuation or launch authority. Within each SQL acceptance boundary,
require all or none of continuation/event, finalized artifact metadata, attempt, materialized
invocation, request binding, sealed request and pending effect. For suspension require the stable
command receipt plus `continuation.suspended`; for resume require the stable command receipt plus
both `continuation.resume_requested` and `attempt.requested`. Reopen SQLite, replay and repeat
scheduler evaluation; require zero new effects.

#### T-ACI-CONT9 — Exhaustive invalid-transition rejection

Parameterize the Cartesian product of every `AgentContinuationLifecycle` state, including no state
and all three terminals, with every `continuation.*` lifecycle event. For every pair absent from the
normative transition table, submit the event/command with otherwise valid syntax and assert typed
invalid-transition rejection, unchanged aggregate version/state, no event append and no effect.
This includes every terminal exit, `provider_lost` from unclaimed `resume_requested`, reconstruction
outside `reconstruction_eligible`, direct expiry after a claim and resume from any terminal.

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

## Runtime confirmation authority v1

The normative positive oracle is
[`specs/fixtures/confirmed-dispatch-v1`](specs/fixtures/confirmed-dispatch-v1/manifest.json). Each
test first strict-parses the package, requires every file byte sequence to already equal its
`aci-cjson-1` encoding and verifies every manifest digest. Fixture issuer/evidence values and the
capability resolution are explicit trusted test preconditions, not proof of production host
authentication or provider availability; tests inject exact admitted configuration and prove that
the runtime accepts no caller assertion as a substitute.

**Evidence partition:** CONF-000 executes only the offline contract oracle: strict bytes, closed
schemas, all manifest/member/authority digests, derivation preimages and IDs, graph/mapping closure,
and the declared shape/classification of every negative scenario and failpoint. Endpoint, SQLite,
migration, transactional failpoint, concurrent replay and effect-boundary spy results below are
mandatory CONF-001 evidence and remain planned until the writer exists. A CONF-000 pass must never
be reported as runtime proof for any AUTH test. It can satisfy AUTH2's offline oracle and the
offline shape/coverage portions of AUTH1, AUTH4 and AUTH5; every endpoint rejection, zero-mutation
claim, database count, replay/concurrency result, failpoint rollback and effect spy requires
CONF-001 runtime evidence.

### T-ACI-AUTH1 — Runtime-only confirmed dispatch

Submit the same valid pending proposal with each pre-confirmation routing choice. For
`legacy-managed`, assert the runtime confirmation endpoint returns its typed rejection and creates
zero `ConfirmationObservation`, `ConfirmedDispatch`, `Run`, graph, mapping, journal fact or effect
while preserving the legacy/session path. For `runtime-managed`, compare the acceptance to the
closed golden oracle: exact finalized artifacts, one immutable observation/dispatch/run, one graph,
one preallocated continuation binding, two ordered mappings, `run.created@1`,
`audit_opening.requested@2`, version-2 `opening_pending` head, one pending/unclaimed audit-opening
intent and the first stable receipt. Assert no additional confirmation row exists.

The complete positive unit contains exactly nine new artifact-metadata records: pending sheet,
`DispatchSpec`, confirmation observation, confirmed graph, ordered mapping set, confirmed authority,
two event payloads and one audit-opening effect payload. Capability resolution is prefinalized
preview evidence; the payload-schema bundle and identity-derivation contract are digest-bound
inputs, not new acceptance metadata. CONF-000 validates this shape offline; CONF-001 must prove the
endpoint/database counts and all-or-none acceptance.

### T-ACI-AUTH2 — Canonical authority and derived identities

For every member named by `manifest.documents`, independently compare raw bytes, strict decoded
value, re-encoded canonical bytes and the member digest declared by the manifest. Require
`manifest.json` itself to equal its canonical encoding and report its computed digest; compare that
digest with an external readiness/review pin when one exists, never with an impossible self-entry.
Recompute the pending/spec/observation/capability/graph/mapping/derivation
digests and require each embedded reference to match. Require
`confirmed_authority.identity_derivation_digest` to equal the complete
`identity-derivation.json` document digest, then recompute `confirmed_authority_digest`. Reimplement
the closed derivation preimage independently and reproduce run, graph, continuation, both source
messages, both mappings, effect, both events and receipt IDs. No production helper under test may
serve as the expected-value oracle.
Independently recompute every member definition digest in the closed payload-schema bundle, then
the bundle digest and its `payload_schema_bundle_digest` binding into confirmed authority. Execute
the exact `payload_schema_bundle_drift` vector and require
`confirmation_payload_schema_mismatch` with zero mutation once CONF-001 exists.

### T-ACI-AUTH3 — Trusted observation boundary

Configure exactly the fixture issuer reference, issuer evidence reference/digest, observation
action/time/presentation, human principal and allowed `chat` channel as one admitted host-context
tuple. Apply each exact observation mutation from `negative-vectors.json`: missing/wrong
`aci.confirmation-observation@1` schema, issuer reference, issuer evidence reference/digest,
principal, channel, action, observed time, dispatch, revision, pending digest and spec digest.
Replay the same `(issuer_ref, observation_id)` with byte-identical content and require the original
observation; submit different canonical bytes under that same issuer-scoped identity and require a
permanent integrity conflict with zero new state. Also inject each same
value as a request-body authority assertion without matching trusted context. Every case must return
the named typed rejection before any authoritative row, event, head, effect or receipt; the positive
fixture must project `confirmed_by`/`confirmed_at` exactly from the verified observation.

### T-ACI-AUTH4 — Digest-domain lineage

Prove the normative pending, spec and authority byte sequences are pairwise distinct and each digest
verifies only its declared bytes. Mutate one canonical pending byte, one admitted capability
resolution field, one observation leaf, one graph leaf, one mapping binding and the complete
identity-derivation contract. Assert the first applicable typed failure and zero mutation. Pending
bytes containing BOM, terminal newline, whitespace, alternate key order, duplicate key or any
strict-schema error reject before presentation; the runtime never parses and silently repairs them
under the old human-approved digest.
Mutate one payload-schema member and the bundle digest independently; neither may be accepted under
the original authority digest. Remove, add and drift each key/value family in the exact closed
five-key `schema_versions` map; every case rejects with zero mutation rather than inventing or
defaulting a version.

### T-ACI-AUTH5 — Bounded projection and mapping closure

Execute every exact graph, mapping and identity mutation present in `negative-vectors.json`.
Additionally generate deterministic parameterized mutations for add/remove/reorder of nodes and
edges; source/target/slot selector drift; reverse/duplicate/add mapping; and supplied
run/graph/continuation/message/mapping/effect/event/receipt IDs not already materialized as package cases. Package
coverage and generated coverage must be reported separately. Every mutation rejects the complete
confirmation. The positive oracle must contain
exactly three logical operation identities, two edges, one continuation, two ordered source
messages and two mappings whose closed binding preimages reproduce their digests.

### T-ACI-AUTH6 — Two-layer replay and conflict

Within the same single-writer transaction, exercise: same key/same command digest; same key/another
command digest; new key/same `dispatch_id` and `confirmed_authority_digest`; new key/same dispatch
and another authority digest; two equal concurrent confirmations for the same dispatch under
distinct idempotency keys; and two divergent concurrent confirmations for that same dispatch under
distinct keys. Equal cases return the byte-identical first receipt with no new rows/events/effects.
Drift cases return their permanent typed conflict and preserve only the elected first unit. Add a
barrier around the former unlocked-pre-read window to prove identity convergence is not performed
outside `BEGIN IMMEDIATE`.

### T-ACI-AUTH7 — Atomic failure and reopen

Trigger every failpoint listed by `negative-vectors.json`, from artifact finalization through
`before_commit`, then reopen the database. Before commit, every authoritative confirmation table,
event/head, generic effect and receipt count is zero; prepared non-authoritative candidate bytes may
remain outside authority. Trigger `after_commit` as a lost response, reopen, retry, and require the
first receipt plus exactly two contiguous events, head version `2`, one graph/continuation, two
ordered mappings and one pending effect. The post-reopen oracle must byte-compare the complete AUTH1
unit: nine metadata records, Observation, ConfirmedDispatch, Run, graph/binding/two mappings, both
events, head, effect and first receipt. Reopen must not reapply a migration or change its checksum.

### T-ACI-AUTH8 — Confirmation effect ceiling

Spy on audit appender/materializer, effect claimer, marker cleanup, provider, tool, scheduler/start,
Attempt, suspension, resume, reconstruction and continuation-lifecycle boundaries. Successful confirmation invokes none of
them. It finalizes only the declared local artifacts and leaves exactly one generic `audit_opening`
intent with the derived `effect_id`, accepted `command_id`,
`requested_event_id=audit_opening.requested.event_id`, exact immutable effect-payload ref/digest,
`retry_class=retryable`, `status=pending`, `claim_epoch=null`, `claimed_by=null`, zero attempts and
null outcome event/digest. The returned receipt proves local journal acceptance only; it must not claim opening
verification, readiness, start, continuation creation or external delivery.
Also attempt to widen the acceptance with an immediate materialization or any second effect; require
the corpus result `forbidden_effect_boundary` and zero mutation, independently of the successful
one-intent spy case.

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

### T-ACI-PC1 — Closed schema validation

For the outer request, every embedded document, every nested item, candidate and result, mutate one
case per missing field, unknown field, duplicate JSON key, forbidden null, wrong primitive, bool as
integer, float, BOM, invalid UTF-8 and normative safety-bound overflow. Strict parsing and closed
schema validation of all embedded documents precede canonical-byte comparison and digest
acceptance. Each mutation returns the specified closed failure before any digest trust or
persistence.
Whitespace, alternate key order and trailing-newline variants of an otherwise valid outer request
must return `invalid_request_schema`; analogous embedded-document variants return
`noncanonical_bytes` in the specified document order.

### T-ACI-PC2 — Canonical golden vectors

Freeze exact UTF-8 document, candidate and result bytes plus qualified SHA-256 digests.
Cover NFC-equivalent strings, normalization collisions, object-key order, required sorted arrays,
integer boundaries, whitespace normalization and rejected noncanonical embedded documents.

The compile request is assembled deterministically in the test from the four canonical document
strings and their literal digests listed below plus the literal `compiler_contract_digest`. Tests
assert that repeated assembly produces byte-identical canonical request bytes and digest; this
version does not claim a separate checked-in request-byte oracle.

The checked-in fixture files are newline-terminated transport containers. Tests MUST distinguish
their raw file hashes from the canonical-document digests produced after strict JSON parsing and
`aci-cjson-1` serialization. The following canonical digests are literal test oracles; a mutable
manifest is not trusted as their sole source:

| Document | Canonical digest |
|---|---|
| `skill-source.json` | `sha256:13ea3dea6640fd553a56662c7efd4bc63480f82b07c49f6e3614b72f4201bc36` |
| `profile.json` | `sha256:43229944b101d12c6d14008d1db17f40c41277b7b441417c7ca5cd38006d7d17` |
| `recipe.json` | `sha256:92fbf20eebbe5ba490bcd1969eed86e3ae91e4e643d7f448a1a089d3be2b50e3` |
| `binding.json` | `sha256:26d7a8a3fb4955a9442d5807b7c27c1c1f204b394e3862437c49a4aae5b14c7b` |
| `invocation.json` | `sha256:469dff24fc67a048a0f5f7040704c3601861beb386b9713dc3eb4e3b233de77b` |
| `compiler-contract.json` | `sha256:9fd10473647a5ea5a7f03df6370773fab2af911cca9d37ffc1e2b7912a009543` |
| `candidate.json` | `sha256:9b829ca70a4717a133a8e42b18e7d95210d1bbfcd5c1e785b56b38778f6df795` |
| `result.json` | `sha256:1a38bb57cddfc8940c1ff19011f543b18e8844a2e2d68b12a340ded527aecb84` |
| `unsupported-profile.json` | `sha256:43ec4c29eca01a6786ec9fff2723c2623828af286e80c67f2b320672d002fa1e` |
| `unsupported-recipe.json` | `sha256:16ce0d514a5b1b42d1c2170d0c4eb8b04a72d150adb4f7bb7b0ef91796c8aaa1` |
| `unsupported-binding.json` | `sha256:10bc707b787041d8b3327a1f3096b5635fae56d75975b0ffbf81f82fa2b00f8a` |
| `unsupported-invocation.json` | `sha256:0fdbd75e214f91a0ad53cec35849d43208af1d51dfa1f1c0300cfa0be3a11c17` |
| `unsupported-result.json` | `sha256:9544a32ccf39309dc778d78623948675c9f80e73ecae52a0108458db35ae0578` |
| `manifest.json` | `sha256:e5cc329254ab8f748888f198ee004cba45f186b5ca21702612932f2c66ef0420` |

### T-ACI-PC3 — Digest lineage and invalidation

Independently mismatch the supplied profile, binding, recipe and invocation document digests.
A request whose supplied `compiler_contract_digest` differs from the implementation's fixed admitted
digest returns `compiler_identity_mismatch`. Separately, fixture-integrity validation canonicalizes
`compiler-contract.json` and requires its digest to equal the literal oracle above; that file is
test evidence for compiler identity, not a document supplied to `CompileDispatchCandidate`.
Changing any supplied canonical input document changes its digest and prevents reuse of the old
candidate lineage. This test does not claim to discover unreported skill-source changes.

Every closed failure is exercised with its exact code and with assertions that no partial result,
artifact descriptor or mutation exists. Composite vectors prove the total first-failure order from
the normative calculation, including the named document order within categories:

1. `invalid_request_schema`;
2. `invalid_document_schema` in profile, binding, recipe, invocation order;
3. `noncanonical_bytes` in profile, binding, recipe, invocation order;
4. `digest_mismatch` in profile, binding, recipe, invocation order;
5. `compiler_identity_mismatch`;
6. `inactive_binding`;
7. `binding_mismatch`;
8. `invocation_mismatch`;
9. `invalid_parameter_value`;
10. `invalid_obligation_mapping`;
11. `invalid_graph`;
12. `fixture_not_admitted`.

At minimum, one composite vector covers every adjacent category pair, and pairwise vectors cover
profile before binding, binding before recipe and recipe before invocation inside each of the three
document categories. The `artifact_content_conflict` outcome is tested separately after a compiled
result because it belongs only to the optional persistence seam, not this calculation precedence.

### T-ACI-PC4 — Explicit parameters only

Exercise required/optional parameters, declared enum/string/integer/boolean values and explicit
scalar substitution. Reject missing required, duplicate, unsorted, undeclared, coerced, defaulted,
or out-of-bounds values. Invocation strings containing `{{` or `}}` are rejected as
`invalid_parameter_value` before admission, making recursive or second-pass template evaluation
impossible in V1.

### T-ACI-PC5 — Total obligation disposition

Require the recipe obligation IDs to equal the profile obligation IDs exactly once. Validate every
closed disposition shape and target reference. The admitted `required-unsupported` case returns
the exact sorted `unsupported-result.json`, contains no candidate bytes or artifact descriptor and
never reaches ArtifactStore. A recipe-obligation mutation to `superseded` supplies the required
authority reference and recomputes the recipe, binding and invocation digests; after all semantic
checks it is rejected as a schema-valid third tuple with `fixture_not_admitted`. No failure creates
a partial result.

### T-ACI-PC6 — Closed DAG

Mutate the fixture with unknown endpoints, duplicate node/edge IDs, self-edge, unsorted input,
cycle, unresolved profile reference, nonterminal without terminal path, terminal with outgoing edge
and each array limit overflow. The valid graph has deterministic topological order.

### T-ACI-PC7 — Logical capability ceiling

Assert byte-for-byte equality between profile logical requirements and candidate requirements.
Reject or prove absent every provider, credential, permission, availability, capability token,
resolution or effective-grant field.

### T-ACI-PC8 — Restart determinism

Compile identical request bytes in independent compiler instances and after database/service
restart. Candidate document, candidate digest and compiled result bytes remain identical; optional
artifact storage resolves the same content-derived artifact identity.

### T-ACI-PC9 — Pure compilation

Use dependency spies and before/after store snapshots to prove the pure compiler reads no clock,
randomness, environment, filesystem discovery, registry, network, provider, tool, scheduler, bus,
journal, confirmation, YAML or legacy dispatch surface and performs no mutation.

### T-ACI-PC10 — Artifact-only persistence

The application wrapper writes only an `application/json`, `aci.dispatch-candidate@1`,
`runtime-internal` artifact through the existing ArtifactStore. Equal content/policy is idempotent;
unequal bytes presented at the same content identity return `artifact_content_conflict` with no
artifact descriptor and no mutation. The operational `finalization_receipt_ref` is outside both
candidate and compiled-result bytes. Metadata/policy conflict also fails closed. Existing runtime
events, pending sheets, YAML, `ConfirmedDispatch`, `Run`, attempts and effects remain unchanged.
ArtifactStore-owned finalization metadata is allowed and remains operational metadata rather than
candidate authority. No runtime command, publication receipt or dispatch receipt is created.

### T-ACI-PC11 — Built-in fixture traceability

Compile the package's admitted read-only `compiled` case and enumerate the exact input JSON pointer
for every candidate field. Assert every `source_binding` digest equals its literal input oracle,
every graph/capability/output field retains its source link and order, and prompt text differs from
its recipe source only through the documented single scalar substitution. The admitted
`required-unsupported` case links its obligation disposition to the exact profile obligation and
recipe rule but produces no candidate.

### T-ACI-PC12 — Candidate authority isolation

Attempt to pass candidate bytes/digest to existing confirmation, dispatch-spec, legacy compiler and
runtime entrypoints. Schema/type boundaries reject them; no public route is added and no runtime
entity or external action is created.

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
| `resumable-feedback@1` | Author/reviewer/author finite turn graph, continuation handle modes, exact revision input, cancel/expiry races and crash failpoints |
| [`confirmed-dispatch-v1@1`](specs/fixtures/confirmed-dispatch-v1/manifest.json) | Seventeen manifest-pinned authority/payload/receipt documents plus the manifest, 56 classified negative/replay scenarios and 21 named transaction failpoints; manifest cardinalities govern if this package is revised |
| [`protocol-compilation-v1@1`](specs/fixtures/protocol-compilation-v1/manifest.json) | Golden closed package with exact admitted `compiled` and `required-unsupported` read-only cases, compiler/schema identity and exact outputs; PC1-PC12 mutations are generated deterministically in tests from these golden documents and are not additional admitted fixtures |

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
- T-ACI-PC1 through T-ACI-PC12 specify the governed candidate compiler slice. They authorize no
  profile registry, confirmation, runtime-managed route, scheduler or provider implementation.
- T-ACI-AUTH1 through T-ACI-AUTH8 have a CONF-000 offline contract oracle only. Runtime endpoint,
  migration, SQLite atomicity, concurrent replay, reopen/failpoint and zero-effect spy evidence remain
  unimplemented until CONF-001 and cannot be marked PASS from fixture validation alone.
- T-ACI-CONT1 through T-ACI-CONT9 are specified by ACI-CONT-001 but have no implementation or live
  restart-retention evidence yet. The host probe proves only same-agent follow-up and active
  interruption on the observed Codex collaboration surface.

## Out of Scope

- Test code, runner choice and database-library implementation.
- Statistical claims about decision quality or model independence.
- Provider billing reconciliation without an explicit provider price/source contract.
