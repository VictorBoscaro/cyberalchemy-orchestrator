---
review: confirmation-authority-spec-review
date: 2026-08-31
scope: CONF-000
review_mode: direct-independent
verdict: PASS
runtime_evidence: false
---

# CONF-000 independent normative review

## Decision

**PASS** for the bounded CONF-000 normative contract and offline golden oracle. No critical, high,
medium or low finding was identified in the reviewed snapshot.

This is a direct independent review authorized by the repository owner. It did not invoke or claim
the formal `review`, `register-dispatch` or governed ACI dispatch workflows.

## Snapshot gate

- Supplied opaque fingerprint: `4c276163650aa8f517f8125538f67941ba9cf2a4939c9b6a731a991ae4d5266d`.
  No calculation recipe was available in the reviewed scope, so this review records it as an
  external pin and **does not claim to have reproduced it**.
- Manifest SHA-256 independently reproduced:
  `sha256:919385d226240fa66621d7b660ef49b70ad7e3d3a379bee3d7c29729243acd0a`.
- All 17 documents declared by the manifest reproduced their declared SHA-256 pins.
- All 18 fixture JSON documents strict-decoded without duplicate keys or floats, were NFC/int64
  admissible, and were byte-equal to their compact, key-sorted `aci-cjson-1` encoding.
- The 30 source artifacts listed in the appendix had identical SHA-256 values before and after the
  review. No source byte drift or conflict was observed.

## Findings by severity

| Severity | Count | Findings |
|---|---:|---|
| Critical | 0 | None. |
| High | 0 | None. |
| Medium | 0 | None. |
| Low | 0 | None. |

The opaque-fingerprint limitation above is an evidence caveat, not a semantic finding: source
stability was independently guarded by the complete per-file SHA-256 set and the reproducible
manifest/document pins.

## Normative checks

| Check | Result | Evidence |
|---|---|---|
| Human approval is the authority | PASS | The contract rejects a chat phrase as standalone authority and requires an admitted issuer plus authenticated host integration ([confirmation-authority.md:42](../../specs/confirmation-authority.md#ownership-and-trust-boundary), [confirmation-authority.md:48](../../specs/confirmation-authority.md#ownership-and-trust-boundary)). The immutable observation binds issuer evidence, principal, action, dispatch/revision and both displayed digests ([domain.md:20](../../specs/domain.md#confirmationobservation), [domain.md:28](../../specs/domain.md#confirmationobservation)). |
| Chat and UI are transports, not distinct authority models | PASS | Both surfaces must produce the same closed canonical observation ([domain.md:22](../../specs/domain.md#confirmationobservation)); the interface says they differ only in admitted issuer/channel evidence ([interfaces.md:25](../../specs/interfaces.md#external-dependency-trusted-confirmation-observation-issuer), [interfaces.md:50](../../specs/interfaces.md#post-dispatchesdispatch_idconfirm)); the workflow applies identical semantic checks ([workflows.md:25](../../specs/workflows.md#runtimedispatchconfirmationworkflow), [workflows.md:47](../../specs/workflows.md#runtimedispatchconfirmationworkflow)). |
| Three digest domains remain non-substitutable | PASS | The normative taxonomy assigns exact, distinct byte domains to pending source, canonical executable spec and complete authority ([confirmation-authority.md:64](../../specs/confirmation-authority.md#digest-taxonomy)); ACI-R22 independently requires the three domains and the complete authority envelope ([rules.md:481](../../specs/rules.md#aci-r22--runtime-confirmation-is-presentation-bound-derived-and-atomic), [rules.md:488](../../specs/rules.md#aci-r22--runtime-confirmation-is-presentation-bound-derived-and-atomic)). The fixture independently reproduced distinct pending, spec and authority digests. |
| Runtime identities are server-derived | PASS | The versioned preimage, prefixes and closed coordinate order are normative ([confirmation-authority.md:156](../../specs/confirmation-authority.md#deterministic-identity-derivation)); callers cannot supply expanded graph or IDs ([operations.md:78](../../specs/operations.md#confirmruntimedispatch), [operations.md:94](../../specs/operations.md#confirmruntimedispatch)). Independent derivation reproduced the run, graph, continuation, two source-message, two mapping, effect, two event and receipt IDs (11 checks) plus both mapping binding digests. |
| Acceptance contains exactly nine new authoritative artifact metadata records | PASS | The operation names the nine members and explicitly excludes prefinalized capability resolution plus the static schema/derivation contracts ([operations.md:132](../../specs/operations.md#confirmruntimedispatch)); the journal batch repeats the same boundary ([interfaces.md:228](../../specs/interfaces.md#confirmation-acceptance-batch)); AUTH1 distinguishes the nine offline members from future database proof ([TEST-SPEC.md:717](../../TEST-SPEC.md#t-aci-auth1--runtime-only-confirmed-dispatch)). The receipt contains exactly the nine corresponding content-derived artifact IDs. |
| Replay checks key before dispatch/authority identity | PASS | The operation requires key replay/conflict followed by identity replay/conflict inside the same `BEGIN IMMEDIATE`, forbidding an unlocked identity pre-read ([operations.md:115](../../specs/operations.md#confirmruntimedispatch)); the sole-writer interface repeats that ordering and convergence behavior ([interfaces.md:218](../../specs/interfaces.md#internal-eventjournal), [interfaces.md:260](../../specs/interfaces.md#confirmation-acceptance-batch)); AUTH6 reserves concurrency proof for CONF-001 ([TEST-SPEC.md:781](../../TEST-SPEC.md#t-aci-auth6--two-layer-replay-and-conflict)). |
| Event `schema_ref` is a string paired with a separate digest | PASS | The common envelope declares separate `schema_ref` and `schema_digest` fields ([events.md:11](../../specs/events.md#common-runtime-event-envelope)); both confirmation event envelopes use the literal string refs with the pinned member digests ([events.md:64](../../specs/events.md#runcreated), [events.md:100](../../specs/events.md#audit_openingrequested)). Both golden envelopes have string `schema_ref` and independent `schema_digest`. |
| `EffectIntent` initial fence uses required nullable fields | PASS | `claimed_by`, `claim_epoch`, `outcome_event_id` and `outcome_digest` are required nullable fields whose null value means never claimed/no accepted outcome ([domain.md:348](../../specs/domain.md#effectintent), [domain.md:363](../../specs/domain.md#effectintent)); the confirmation event freezes the same complete initial row ([events.md:110](../../specs/events.md#audit_openingrequested)). The golden effect contains all four keys as null, `attempt_count=0`, `status=pending`, and `retry_class=retryable`. |
| Success ceiling is durable `opening_pending` with no external action | PASS | Confirmation success ends at version 2 `opening_pending`, one unclaimed audit-opening intent and zero external effects ([workflows.md:38](../../specs/workflows.md#runtimedispatchconfirmationworkflow), [rules.md:525](../../specs/rules.md#aci-r22--runtime-confirmation-is-presentation-bound-derived-and-atomic)); the event reducer is explicitly forbidden to advance to `ready` ([events.md:123](../../specs/events.md#audit_openingrequested)). The oracle contains exactly two events and one pending/unclaimed effect. |
| CONF-000 is offline oracle; writer/runtime proof belongs to CONF-001 | PASS | The authority contract creates no runtime code authority and reserves the writer for CONF-001 ([confirmation-authority.md:15](../../specs/confirmation-authority.md#contract-status-and-objective), [confirmation-authority.md:383](../../specs/confirmation-authority.md#explicitly-deferred)); TEST-SPEC forbids reporting fixture validation as endpoint, migration, SQLite, concurrency, rollback or zero-effect runtime proof ([TEST-SPEC.md:700](../../TEST-SPEC.md#runtime-confirmation-authority-v1), [TEST-SPEC.md:1058](../../TEST-SPEC.md#known-gaps)); layering assigns migration 012 and the durable writer exclusively to CONF-001 ([confirmation-implementation-layering.md:148](../../development/invoke-runs/20260831-resumable-feedback/plan/confirmation-implementation-layering.md#l1--conf-001-durable-confirmation-writer)). |
| DomainSpec meta-types and relationships are coherent | PASS | Identity-bearing observation/dispatch/graph records are Entities, the authority envelope and spec are Value Objects, confirmation is an Operation, command/journal surfaces are Interfaces, accepted facts are Events, and the multi-step route is a Workflow ([SPEC.md:465](../../specs/SPEC.md#domain-concepts), [operations.md:55](../../specs/operations.md#confirmruntimedispatch), [interfaces.md:44](../../specs/interfaces.md#post-dispatchesdispatch_idconfirm), [events.md:38](../../specs/events.md#runcreated), [workflows.md:13](../../specs/workflows.md#runtimedispatchconfirmationworkflow)). The declared `exposes`, `produces` and `orchestrates` relations match the DomainSpec taxonomy. |

## Independent fixture validation

The independent checker produced:

```text
PASS files=18 manifest_documents=17 canonical=18 manifest_pin=1 document_pins=17
ids=11 mappings=2 metadata=9 events=2 negative=56 failpoints=21
```

It also reproduced:

- pending sheet: `sha256:7b7ff10271cae9e657033e5d3dd61261cb651c6cb66500a4c63fd2d111e162fa`;
- `DispatchSpec`: `sha256:a9c60706bfba455db2dd98a303f97be2eb9442df7a56d08274067db8f0753eab`;
- confirmed authority: `sha256:08543fc7902a1e113228473978f343326931107723853dbe3508b24325475e43`;
- payload-schema bundle: `sha256:44fbe7dd415bdcafd91c8f766f44b936e3e640234576f51aab399e5b2c565f33`;
- negative-vector corpus: `sha256:f7dd8dc62b2c23f67afc1cdc057af7d6bd7db9061c651c0f9ff3ac3c6e351807`.

The 56 negative cases split into 48 exact document mutations and 8 runtime scenarios. The 21
failpoints cover each of the nine artifact finalizations and every remaining acceptance mutation
through `before_commit`. These are closed obligations/oracles; their database and effect
postconditions remain unproved until CONF-001 runs them.

## Claims this PASS permits

- CONF-000 has a coherent, closed and independently reproducible normative meaning for one bounded
  `author:0 -> reviewer:0 -> author:1` approval.
- The reviewed fixture is a valid offline golden oracle for canonical bytes, digest lineage,
  runtime-derived IDs, graph/mapping closure, event/effect/receipt shape and negative-test planning.
- This PASS may satisfy the normative-review prerequisite for issuing the exact CONF-001 work pack
  and fresh code-readiness receipt.

## Claims this PASS prohibits

- It does not prove migration 012, SQLite persistence, transaction rollback, reopening, concurrent
  replay, lost-response recovery, database counts, or absence of runtime external calls.
- It does not prove a production chat/UI issuer, cryptographic attestation, provider availability,
  audit-row materialization, effect claiming, continuation, scheduling, deployment or cutover.
- It does not authorize continuation code, provider/tool/attempt start, audit append, commit, push or
  deploy.
- It does not reproduce or validate the opaque fingerprint `4c2761...`.

## Skills and normative references read

- `task-session` 0.3.1, read completely and applied only for bounded scope/gates/evidence; no formal
  runtime handoff or subagent workflow was invoked.
- `domainspec-spec-feature`, read completely, with `TAXONOMY.md`, `RELATIONSHIPS.md` and the applicable
  `SPEC.md`, `architecture.md`, `domain.md`, `operations.md`, `interfaces.md`, `events.md`, `rules.md`,
  `workflows.md`, `TEST-SPEC.md` and `implementation-layering.md` templates read completely.
- `dispatch-spec` 0.2.0, read completely and used only as a boundary/handoff/evidence checklist; no
  reusable dispatch document or formal dispatch lifecycle was claimed.

## Source SHA-256 set (pre-review = post-review)

| Source | SHA-256 |
|---|---|
| `docs/features/agents-communication-infra/development/invoke-runs/20260831-resumable-feedback/plan/confirmation-implementation-layering.md` | `sha256:09c4550df27beefa796fba063aff8dea2d4ff25d0b96240809fa076e171ae875` |
| `docs/features/agents-communication-infra/robot-talks/2026-08-31-confirmed-dispatch-next-increment/findings.md` | `sha256:78836a8cf68236b499636e1ceb133a4adf134aabcc54bd3389aba3cbe7a69913` |
| `docs/features/agents-communication-infra/specs/architecture.md` | `sha256:ef4b9571e38d8a351f94ae5056efc163a851243fca3bd65786d8727e6f7a0d96` |
| `docs/features/agents-communication-infra/specs/confirmation-authority.md` | `sha256:4e9f92545c9ab35a9ab555efee0488e7c3aec9b849dad17f07a82e166018252c` |
| `docs/features/agents-communication-infra/specs/domain.md` | `sha256:7768f69c6ced3621e6832389b1baf9f26206e06eb653bab7d70bb85817179ec4` |
| `docs/features/agents-communication-infra/specs/events.md` | `sha256:bc92beb371a3f5b956645d421f24b41d32d8ff9f204e524965eabb1c37a3c5bb` |
| `docs/features/agents-communication-infra/specs/fixtures/confirmed-dispatch-v1/audit-opening-effect.json` | `sha256:d8d67fb38877f55ffd7a7fd3582b7b1d774454694ddfadb44c1d3daf8f88be30` |
| `docs/features/agents-communication-infra/specs/fixtures/confirmed-dispatch-v1/audit-opening-requested-payload.json` | `sha256:8c195c13b588f5bcfcda27ac6153eaefefe5f6f19138c6d98e9c17711fa0056f` |
| `docs/features/agents-communication-infra/specs/fixtures/confirmed-dispatch-v1/capability-resolution.json` | `sha256:465ff114ed5894af33f1528abf431d33ce9e4c410ec779a7c2b3b4d248330480` |
| `docs/features/agents-communication-infra/specs/fixtures/confirmed-dispatch-v1/confirmation-command.json` | `sha256:92e6554d087e9febfb66a6076aef8d88f897bf31c6f73a73dd1d51fc945dae00` |
| `docs/features/agents-communication-infra/specs/fixtures/confirmed-dispatch-v1/confirmation-observation.json` | `sha256:c3134baac33c256976d4945ec94cfef6ff71529586bbc218d39efe83919d180e` |
| `docs/features/agents-communication-infra/specs/fixtures/confirmed-dispatch-v1/confirmation-payload-schemas.json` | `sha256:44fbe7dd415bdcafd91c8f766f44b936e3e640234576f51aab399e5b2c565f33` |
| `docs/features/agents-communication-infra/specs/fixtures/confirmed-dispatch-v1/confirmation-receipt.json` | `sha256:bdc6f158999a78eb8bc99acfab2cc3aa708f7d617861022526ef8f38bc15cf24` |
| `docs/features/agents-communication-infra/specs/fixtures/confirmed-dispatch-v1/confirmed-authority.json` | `sha256:08543fc7902a1e113228473978f343326931107723853dbe3508b24325475e43` |
| `docs/features/agents-communication-infra/specs/fixtures/confirmed-dispatch-v1/confirmed-turn-graph.json` | `sha256:a56237e28c1d297a4f12bfbb6851d0a54c30aba7e05b10adf9275ca4af38f2ba` |
| `docs/features/agents-communication-infra/specs/fixtures/confirmed-dispatch-v1/continuation-mappings.json` | `sha256:537ac7f86886907f4dbac67cd1d75738deeb0173586393139874f462f2928a62` |
| `docs/features/agents-communication-infra/specs/fixtures/confirmed-dispatch-v1/dispatch-spec.json` | `sha256:a9c60706bfba455db2dd98a303f97be2eb9442df7a56d08274067db8f0753eab` |
| `docs/features/agents-communication-infra/specs/fixtures/confirmed-dispatch-v1/expected-acceptance.json` | `sha256:fddfeebc18522e2e84d9dfa1a35fdfa845a798be20f160a994522e876c3e5bd2` |
| `docs/features/agents-communication-infra/specs/fixtures/confirmed-dispatch-v1/identity-derivation.json` | `sha256:e1d77f8e2e7eed4a94140d17ef05f10b227cba22727ed67d970244c8b910a3b5` |
| `docs/features/agents-communication-infra/specs/fixtures/confirmed-dispatch-v1/manifest.json` | `sha256:919385d226240fa66621d7b660ef49b70ad7e3d3a379bee3d7c29729243acd0a` |
| `docs/features/agents-communication-infra/specs/fixtures/confirmed-dispatch-v1/negative-vectors.json` | `sha256:f7dd8dc62b2c23f67afc1cdc057af7d6bd7db9061c651c0f9ff3ac3c6e351807` |
| `docs/features/agents-communication-infra/specs/fixtures/confirmed-dispatch-v1/pending-sheet.json` | `sha256:7b7ff10271cae9e657033e5d3dd61261cb651c6cb66500a4c63fd2d111e162fa` |
| `docs/features/agents-communication-infra/specs/fixtures/confirmed-dispatch-v1/run-created-payload.json` | `sha256:1a2b6ffebf0d777981c92af261f6fc494f610cff1e7b66a92549ec51ef8094e7` |
| `docs/features/agents-communication-infra/specs/fixtures/confirmed-dispatch-v1/trusted-issuer-context.json` | `sha256:69ec8770efadb2cbb4698273cb52c7315793a841d62c7e8326c744a316065bdd` |
| `docs/features/agents-communication-infra/specs/interfaces.md` | `sha256:81abe88be82693293fba9b45c43b1e64f9176559469bd4f6b921727a5a1182da` |
| `docs/features/agents-communication-infra/specs/operations.md` | `sha256:9ae0bbb3fd18949891171d8af0f6c25e5d14227c473b7c41a7aa2fa45bbc8134` |
| `docs/features/agents-communication-infra/specs/rules.md` | `sha256:09e0046c015fda03146dcc5d542d99750416030107d269b8dcfc95db23053819` |
| `docs/features/agents-communication-infra/specs/SPEC.md` | `sha256:7ce803d5ea1071c999bb5b2a4c5eb24b04b6faad5900ffabe6fe295dc552ef63` |
| `docs/features/agents-communication-infra/specs/workflows.md` | `sha256:7782300efa0ef3537f9f48f1379916e608f83d3834e0061947953f90848af32e` |
| `docs/features/agents-communication-infra/TEST-SPEC.md` | `sha256:1dba61d54e61538f95a3a383f18e55deddb152a7b210638bc2d8bf7b3b5a44ea` |
