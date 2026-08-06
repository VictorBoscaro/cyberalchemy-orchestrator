# Work Pack — Executable Evidence For Transport-Neutral Adapter Contract

Status: candidate, not admitted or executed  
Source design: `TransportNeutralWorkProtocolAdapterContract@candidate-2`  
Objective: turn authored design into executable, offline validation evidence
without implementing a transport adapter.

## Boundaries

Allowed only after separate authorization: a new candidate validation work
folder beneath the RWO development area. Existing canonical `DESIGN.md`,
ontology, definitions, runtime code, ARE, ACI, Git, and external transports are
read-only or out of scope.

## SWU-01 — Closed Candidate Schemas

Deliverables:

- JSON Schemas for canonical message, delivery attempt, observations,
  capability manifest, requirements, conformance receipt, and admission;
- canonicalization/digest rules;
- field-owner and forbidden-inference tables.

Acceptance:

- schemas reject unknown fields and capability atoms;
- command/event kinds are disjoint;
- canonical and transport metadata cannot overlap;
- accepted-record fields are impossible in adapter output schemas.

Dependencies: none.  
Execution: not selected.

## SWU-02 — Scenario Fixtures

Deliverables:

- positive and negative JSON fixtures derived from all Stage 08 scenarios;
- explicit expected single decision per fixture;
- mutation fixtures for digest, scope, epoch, capability, and owner drift.

Acceptance:

- every fixture validates structurally;
- each negative fixture fails for the expected reason;
- all five transport arrangements have honest capability fixtures.

Dependencies: SWU-01.  
Execution: not selected.

## SWU-03 — Deterministic Offline Validator

Deliverables:

- schema/canonical-digest validator;
- duplicate classifier;
- manifest-versus-requirements checker;
- exact-tuple admission evaluator;
- machine-readable validation receipt.

Acceptance:

- repeated runs over immutable inputs are byte-stable;
- absent/unknown/ambiguous capability fails closed;
- stale or mismatched conformance evidence blocks;
- no external network, model, transport, or effect calls occur.

Dependencies: SWU-01, SWU-02.  
Execution: not selected.

## SWU-04 — Recovery Separation Harness

Deliverables:

- transition-table tests for reconnect, redelivery, new Work Attempt, replay,
  and effect reconciliation;
- zero-call replay spy;
- unknown-effect reconciliation fixtures;
- budget/fence/convergence prerequisite tests.

Acceptance:

- adapter can never mint a Work Attempt;
- replay produces no route, adapter, model, allocation, or effect call;
- unknown external effect never selects automatic retry;
- identical redelivery converges and divergent duplicate conflicts.

Dependencies: SWU-03.  
Execution: not selected.

## SWU-05 — Owner Decision Pack

Deliverables:

- G1 journal/domain truth decision request;
- G2 exact-effect permit/outcome/reconciliation decision request;
- G3 ARE/ACI evidence and route admission decision request;
- reconciled candidate changes with provenance.

Acceptance:

- every unresolved semantic has one named owner;
- no absence is converted into a default;
- owner decisions are evidence locators, not authority bearer tokens.

Dependencies: SWU-04.  
Execution: not selected.

## SWU-06 — Independent Design Validation

Deliverables:

- rerun of the adapter architect, transport adversary, and
  recovery/authority audit over materialized schemas and fixtures;
- deterministic reducer receipt;
- final `design-validator-pass` or exact block report.

Acceptance:

- all three role receipts complete;
- every critical finding passes or remains a named external block;
- claim ceiling remains design evidence only.

Dependencies: SWU-05.  
Execution: not selected.

## Deferred Work

Ontology proposal, reference in-memory adapter, real transport adapters, RWO
runtime wiring, ARE/ACI integration, deployment, and production admission are
separate work packs after SWU-06 and their respective owner approvals.

## Stop Conditions

Stop on ambiguous owner, schema weakening, external calls, authority or
promotion change, unsupported capability fallback, failed critical fixture, or
any request to infer exactly-once business effects from delivery evidence.

