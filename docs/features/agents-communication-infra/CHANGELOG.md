---
tags: [agents-communication-infra, spec, changelog]
node_type: changelog
is_session: false
layer: application
nature: [reference]
status: draft
version: 0.2.3
last_updated: 2026-07-23
---

# Agents Communication Infra — Changelog

All notable domain/specification changes to **agents-communication-infra** are recorded here.

## 2026-07-23

### CVR authority-guard coordination (0.2.3)

- Inserted `SWU-ACI-CVR-GUARD-001` into the strict `000 -> GUARD -> 001 -> 002` sequence.
- Replaced self-bootstrap and writer-owned receipts with an external trusted one-time bootstrap,
  exactly one external bootstrap finalizer, then a common guard/finalizer exclusively for
  CVR-001/002. Root never writes receipts.
- Defined a five-entry packet and exactly three content-addressed authority artifacts per
  execution; removed current pointers, revocation artifacts, persisted ClaimReceipt and duplicate
  receipts.
- Materialized the concrete GUARD descriptor as `proposal_non_authorizing`; it creates no
  authorization, changes no gate and introduces no implementation.
- Added T-CVR-AUTH1–6 and CVR-002 PASS-receipt/baseline/delta/prehash and full CVR-001 rerun
  requirements. The proposed per-SWU predicate remains non-operative and no code or authorization
  was created.

### Canonical vault-read ApprovalPacket preparation

The lifecycle details in this earlier preparation entry are historical and superseded by 0.2.3
above; they do not define the current proposal.

- Added the proposed `SWU-ACI-CVR-000/001/002` task contracts, explicit shorthand aliases and an
  ApprovalPacket-ready work-pack lane.
- Recorded `cvrImplementationGateStatus=approval_packet_prepared` as explicitly non-pass and
  prepared for named owner review while
  preserving `workPackGateStatus=block` and `runtimeGate=block`.
- Froze proposed future CVR-001/002 write scopes, prerequisites, verification obligations and
  single-use authorization semantics. No implementation or owner/root acceptance is claimed.
- Specified absent AuthoritySlots and the future serialized authorization-record schema, parser
  ceilings, staged privacy, operation-specific capture, typed canonical digests, raw declarations
  in CVR-001 and endpoint/logical projection in CVR-002. No record, venv or dependency was created.
- The earlier preparation counted four normative paths plus seven indexes; 0.2.3 supersedes that
  count with a five-entry packet plus seven derived indexes (12 governed artifacts, descriptor
  included). It also replaced mutable authorization lifecycle language with immutable
  authorization plus append-only revocation/receipt, and defined the narrow effect-free CVR-001
  carve-out without promoting either global gate.
- Froze the 32,768-byte scalar ceiling, complete nested canonical schemas, total per-method error
  precedence, isolated no-cache CPython 3.12 commands and exact pytest nodeids. These remain future
  requirements; no test or install was executed.
- Unified the four governing documents on one authorization predicate, added the future
  create-new same-session claim, confined all venv/cache/temp effects with checked native exits
  and cleanup evidence, and made `get_edge` apply complete-corpus edge-source caps. No
  authorization, claim, receipt, temp environment or gate pass was created.
- Removed claim bootstrap from the implementation writer: root/authority owner now creates the
  preexisting claim and delivers ClaimReceipt; writers verify it with read-only built-ins and
  create only terminal receipts. CVR-002 now mirrors the full fresh auth/claim/temp/test/finalize
  protocol and re-runs CVR-001 non-regression nodeids.

### Canonical vault reads and authority clarification (0.2.2)

- Added the W0 `canonical-vault-reads` aspect, four read-only queries, eleven registered concepts
  and T-CVR-1 through T-CVR-12 while retaining `runtimeGate=block`.
- Clarified that `legacy-managed` is a pre-confirmation routing choice outside ACI runtime
  confirmation; only `runtime-managed` creates one immutable `ConfirmedDispatch` and one `Run`.
- Added T-ACI-AUTH1 and four independent vault-read limits: per-file bytes, aggregate bytes, source
  count and result count.
- Recorded that the v0.1.1 agent-tools discovery refines the earlier generic wording of ACI-D3.

## 2026-07-21

### SWU-ACI-001 accepted W0 contract (0.2.1)

- Accepted ADR-001 after independent authority, SQLite and canonical-vector closure reviews returned
  `PASS/PASS/PASS` on one hashed baseline.
- Froze the 17-table SQL contract fixture, exact Pydantic pins, six positive/six rejection vectors
  and 45 named TASK-010 conformance tests.
- Kept TASK-000 and every runtime gate blocked; acceptance is decision evidence, not production
  SQLite, migration, recovery or dependency-lock proof.

### External-tool adoption amendment (0.2.0)

- Ratified ETD-1–ETD-7 from [External Tool Adoptions v0.1.0](discovery/external-tool-adoption/external-tool-adoptions.md):
  Python/FastAPI host, Pydantic core validation with runtime-owned canonicalization/digest, local
  subprocess first provider, and no Octopus/Eve kernel authority.
- Added `SoleWriterEvidenceBundle`, `ExternalToolAdoptionPolicy`, `CanonicalContractPolicy`,
  `BoundaryValidationPolicy` and `ProviderAdapterAdmissionGate`, with the exclusive
  T-ACI-ETA1–ETA5 family and full
  work-pack/reverse-matrix ownership.
- Disposed OQ-ETA4 and OQ-ETA6 for this slice, deferred OQ-ETA5, and retained OQ-ETA1/OQ-ETA2 as
  explicit W0/EG-1 blockers. `runtimeGate=block` remains; B-003 stays open specifically for
  materializer cutover after its W0 contract obligations are frozen.
- Corrected the external-adoption review findings: preserved the three policy meta-types, separated
  trusted materialization from mandatory launcher-mediated provider start, and split W0's
  sole-writer schema/guard specification from TASK-020's target-host cutover proof.

### Review remediation

- Rebuilt the Concept Registry and glossary to match all first-class aspect concepts, including the
  plan/materialization/terminal pipeline, sandbox boundary and usage/cost evidence; wire event values
  and internal transitions remain intentionally outside the registry.
- Added missing specification/architecture transport sections, explicit
  `specified/proposed, not W0-accepted` precedence and preserved ACI-D1 through ACI-D15 individually.
- Resynchronized manual primary task ownership and concept-to-test follow-up while leaving B-001,
  B-002 and the runtime gate open.

### Added

- **DomainSpec baseline 0.1.0** — created the capability-driven [SPEC](specs/SPEC.md), six-view [architecture](specs/architecture.md), complete registry [glossary](specs/glossary.md) and contract [test specification](TEST-SPEC.md).
- **Discovery authority trace** — locked ACI-D1–ACI-D15 and recorded the dispositions of OQ-ACI1–OQ-ACI10 from the operator-designated discovery v0.2.1; v0.2.0 remains the historical introduction point for those IDs.
- **Agent I/O boundary** — specified `agents-communication-infra.AgentExecutionRequest`, `agents-communication-infra.EffectiveInputArtifact`, `agents-communication-infra.RawProviderOutput`, `agents-communication-infra.BusPublication` and `agents-communication-infra.PublicationReceipt` as separate contracts.
- **Persistence and recovery boundary** — specified SQLite/WAL atomic acceptance, pure replay, crash reconciliation, sealed reveal and official audit close obligations.
- **Explicit gates** — recorded `specAuthoringGate=pass` while retaining `runtimeGate=block` until W0 and EG-1 evidence is accepted.
