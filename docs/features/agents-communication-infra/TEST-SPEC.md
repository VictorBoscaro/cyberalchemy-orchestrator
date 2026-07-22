---
tags: [agents-communication-infra, spec, test]
node_type: spec
is_session: false
layer: application
nature: [procedural, technical]
status: draft
version: 0.2.0
last_updated: 2026-07-21
---

# Test Spec: Agents Communication Infra

This document specifies contract tests, not test code. Fixtures derive from [rules.md](rules.md), lifecycle transitions, operation postconditions, [persistence crash boundaries](persistence-and-replay.md#5-crash-boundaries-and-observable-outcomes) and the executable [bus probe](experiments/bus-publication-probe/README.md).

## Test Matrix

| ID | Test | Validates |
|---|---|---|
| [T-ACI-R1](#t-aci-r1--authority-and-writer-boundary) | Only journal writer and validated ledger appender can mutate their stores | [ACI-R1](rules.md#aci-r1--disjoint-authority-and-one-physical-writer) |
| [T-ACI-R2](#t-aci-r2--runtime-derived-authority) | Agent authority-field injection is rejected | [ACI-R2](rules.md#aci-r2--runtime-derived-authority) |
| [T-ACI-R3](#t-aci-r3--append-before-ack) | Receipt exists only after commit and parent verification | [ACI-R3](rules.md#aci-r3--append-before-receipt-and-parent-verification) |
| [T-ACI-R4](#t-aci-r4--sealed-collection-and-reveal) | Collection stays sealed until persisted matching reveal | [ACI-R4](rules.md#aci-r4--sealed-collection-and-manifest-only-reveal) |
| [T-ACI-R5](#t-aci-r5--idempotency-and-cas) | Retry, digest conflict and expected-version races differ | [ACI-R5](rules.md#aci-r5--command-idempotency-is-not-conflict-tolerance) |
| [T-ACI-R6](#t-aci-r6--atomic-command-acceptance) | Receipt, events, head and new intents are all-or-none | [ACI-R6](rules.md#aci-r6--atomic-local-acceptance) |
| [T-ACI-R7](#t-aci-r7--pure-replay) | Replay from zero/checkpoint yields same hash with zero effects | [ACI-R7](rules.md#aci-r7--pure-replay) |
| [T-ACI-R8](#t-aci-r8--logical-uniqueness) | Retries/attempts cannot create a second logical contribution/result | [ACI-R8](rules.md#aci-r8--logical-uniqueness-survives-retries) |
| [T-ACI-R9](#t-aci-r9--artifact-separation-and-input-manifest) | Effective input, raw output and contribution remain distinct and linked | [ACI-R9](rules.md#aci-r9--input-output-and-accepted-message-are-distinct-evidence) |
| [T-ACI-R10](#t-aci-r10--mixed-provider-conformance) | Mixed providers use the same protocol/state/event shapes | [ACI-R10](rules.md#aci-r10--provider-heterogeneity-cannot-fork-protocol) |
| [T-ACI-R11](#t-aci-r11--sensitive-artifact-governance) | Sensitive access, secret rejection and tombstone provenance fail closed | [ACI-R11](rules.md#aci-r11--sensitive-immutable-artifact-governance) |
| [T-ACI-R12](#t-aci-r12--usage-nullability-and-provenance) | Missing usage stays null and cost needs priced provenance | [ACI-R12](rules.md#aci-r12--usage-observations-preserve-provider-semantics) |
| [T-ACI-R13](#t-aci-r13--verified-opening-barrier) | No provider/tool effect starts before exact opening verification | [ACI-R13](rules.md#aci-r13--audit-opening-gates-every-providertool-effect) |
| [T-ACI-R14](#t-aci-r14--sqlite-durability-policy) | Writer startup asserts WAL, FULL and migration checksum | [ACI-R14](rules.md#aci-r14--durability-is-a-feature-level-contract) |
| [T-ACI-R15](#t-aci-r15--candidate-versus-official-publication) | Candidate persistence alone never counts toward close/quorum | [Receipt workflow](workflows.md#receiptgatedpublicationworkflow) |
| [T-ACI-R16](#t-aci-r16--canonical-receipt-and-terminal-result) | Receipt/result versions and exact field parsing fail closed | [PublicationReceipt](domain.md#publicationreceipt) |
| [T-ACI-R17](#t-aci-r17--invocation-materialization-boundary) | Plan, materialization, sealed request and start effect remain ordered/distinct | [StartAgentAttempt](operations.md#startagentattempt) |
| [T-ACI-R18](#t-aci-r18--typed-reveal-input-provenance) | Reveal input preserves manifest/message/author/hash/policy | [EffectiveInputEntry](domain.md#effectiveinputentry) |
| [T-ACI-R19](#t-aci-r19--sandbox-authority-and-budget-fence) | Sandbox, authority cutover and finite budgets fail closed | [SandboxLauncher](interfaces.md#internal-sandboxlauncher) |
| [T-ACI-R20](#t-aci-r20--causal-start-prerequisites) | Start cannot race past close/cancel using stale dependency heads | [RuntimeCommand](domain.md#runtimecommand) |
| [T-ACI-R21](#t-aci-r21--candidate-abandonment-and-replacement) | Unknown orphan candidates release their key only through authorized audited CAS | [PublicationCandidate](domain.md#publicationcandidate) |
| [T-ACI-ETA1](#t-aci-eta1--external-tool-authority-classification) | External tools cannot acquire kernel or authoritative-store ownership | [ExternalToolAdoptionPolicy](rules.md#aci-r15--external-tool-adoption-policy) |
| [T-ACI-ETA2](#t-aci-eta2--canonical-python-contract-vectors) | Boundary validation and runtime-owned canonical sealing remain distinct | [CanonicalContractPolicy](rules.md#aci-r16--canonical-contract-policy) |
| [T-ACI-ETA3](#t-aci-eta3--derived-node-boundary-parity) | Any derived Node validator stays non-normative and vector-compatible | [BoundaryValidationPolicy](rules.md#aci-r17--derived-boundary-validation-policy) |
| [T-ACI-ETA4](#t-aci-eta4--subprocess-provider-admission-gate) | A real subprocess provider cannot bypass launcher or admission evidence | [ProviderAdapterAdmissionGate](rules.md#aci-r18--provider-adapter-admission-gate) |
| [T-ACI-ETA5](#t-aci-eta5--sole-writer-evidence-completeness) | The sole-writer evidence schema and component checks fail closed | [SoleWriterEvidenceBundle](domain.md#solewriterevidencebundle) |
| [T-ACI-S1](#t-aci-s1--run-lifecycle-and-terminal-precedence) | Run accepts only listed transitions and one terminal winner | [RunLifecycle](states.md#runlifecycle) |
| [T-ACI-S2](#t-aci-s2--group-decision-and-sealing) | Consensus, dissent and no-quorum stay distinct | [GroupLifecycle](states.md#grouplifecycle) |
| [T-ACI-S3](#t-aci-s3--attempt-cancel-races) | Completion/failure/unknown/cancel races have one allowed terminal | [AttemptLifecycle](states.md#attemptlifecycle) |
| [T-ACI-C1](#t-aci-c1--transaction-crash-boundaries) | Every local acceptance crash yields all four members or none | [Crash boundaries](persistence-and-replay.md#5-crash-boundaries-and-observable-outcomes) |
| [T-ACI-C2](#t-aci-c2--audit-append-crash-reconciliation) | Absent, identical and divergent audit rows converge correctly | [Cross-store reconciliation](persistence-and-replay.md#8-cross-store-reconciliation) |
| [T-ACI-C3](#t-aci-c3--closed-before-reveal-restart) | Restart between close and reveal preserves sealed access | [Publication/reveal persistence](persistence-and-replay.md#7-publication-reveal-and-artifact-persistence) |
| [T-ACI-C4](#t-aci-c4--publish-to-terminal-recovery) | Crash anywhere from publish through terminal verification converges once | [Receipt workflow](workflows.md#receiptgatedpublicationworkflow) |
| [T-ACI-C5](#t-aci-c5--effect-outcome-idempotency-matrix) | Terminal outcome retries compare digest before claim/epoch guards | [Atomic effect-outcome acceptance](persistence-and-replay.md#41-atomic-effect-outcome-acceptance) |
| [T-ACI-P1](#t-aci-p1--probe-regression-corpus) | Production contract retains all ten publication-probe behaviors | [Probe](experiments/bus-publication-probe/README.md#run-the-contract-tests) |

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

Validate one [SoleWriterEvidenceBundle](domain.md#solewriterevidencebundle) for the exact writer and
host profile. Remove each process-identity, ACL, writer-inventory or negative-bypass component in
turn and assert EG-1 remains open. A bundle containing only the single-import lint must fail.

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

## Known Gaps

- Concrete retention, key-management and crypto-erasure timing tests await the OQ-ACI9 ADRs.
- Real Codex, second-provider and mixed-provider empirical completeness tests remain L2/L3 gates.
- Host-loss, multi-host and multi-tenant recovery are outside the initial contract.
- `OQ-SANDBOX` remains an explicit S-003/L2/W3 real-provider blocker until target-host launcher
  isolation tests pass; it does not block fake-adapter Slice 1 work.
- OQ-ETA1 remains a W0 blocker until the Pydantic pin and canonical serialization vectors are accepted.
- OQ-ETA2/B-003 remains open for materializer cutover until a complete target-host
  `SoleWriterEvidenceBundle` passes T-ACI-ETA5. W0 freezes its schema and negative-test
  specification; TASK-020 supplies the physical target-host proof.

## Out of Scope

- Test code, runner choice and database-library implementation.
- Statistical claims about decision quality or model independence.
- Provider billing reconciliation without an explicit provider price/source contract.
