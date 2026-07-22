---
tags: [agents-communication-infra, spec, changelog]
node_type: changelog
is_session: false
layer: application
nature: [reference]
status: draft
version: 0.2.1
last_updated: 2026-07-21
---

# Agents Communication Infra — Changelog

All notable domain/specification changes to **agents-communication-infra** are recorded here.

## 2026-07-21

### SWU-ACI-001 accepted W0 contract (0.2.1)

- Accepted ADR-001 after independent authority, SQLite and canonical-vector closure reviews returned
  `PASS/PASS/PASS` on one hashed baseline.
- Froze the 17-table SQL contract fixture, exact Pydantic pins, six positive/six rejection vectors
  and 45 named TASK-010 conformance tests.
- Kept TASK-000 and every runtime gate blocked; acceptance is decision evidence, not production
  SQLite, migration, recovery or dependency-lock proof.

### External-tool adoption amendment (0.2.0)

- Ratified ETD-1–ETD-7 from [External Tool Adoptions v0.1.0](discovery/external-tool-adoptions.md):
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

- **DomainSpec baseline 0.1.0** — created the capability-driven [SPEC](SPEC.md), six-view [architecture](architecture.md), complete registry [glossary](glossary.md) and contract [test specification](TEST-SPEC.md).
- **Discovery authority trace** — locked ACI-D1–ACI-D15 and recorded the dispositions of OQ-ACI1–OQ-ACI10 from the operator-designated discovery v0.2.1; v0.2.0 remains the historical introduction point for those IDs.
- **Agent I/O boundary** — specified `agents-communication-infra.AgentExecutionRequest`, `agents-communication-infra.EffectiveInputArtifact`, `agents-communication-infra.RawProviderOutput`, `agents-communication-infra.BusPublication` and `agents-communication-infra.PublicationReceipt` as separate contracts.
- **Persistence and recovery boundary** — specified SQLite/WAL atomic acceptance, pure replay, crash reconciliation, sealed reveal and official audit close obligations.
- **Explicit gates** — recorded `specAuthoringGate=pass` while retaining `runtimeGate=block` until W0 and EG-1 evidence is accepted.
