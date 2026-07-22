# Cross-Task Gap Ledger

| Gap | Blocks | State | Repair path |
|---|---|---|---|
| G-001: persistence/offset/transaction contract absent | W1 | repaired for SWU-ACI-001; TASK-000 still blocks W1 | ADR-001 accepted by independent W0 review; TASK-010 supplies executable conformance after the remaining W0 gate passes. |
| G-002: initial decision and dissent semantics absent | fixed group protocol in W1 | blocker for 0E, not 0B-0D | TASK-000 protocol ADR |
| G-003: terminal mapping across attempt/group/run absent | W1 | blocker | TASK-000 terminal ADR |
| G-004: external-input snapshot boundary absent | 0E and real adapters | blocker for 0E | TASK-000 snapshot ADR |
| G-005: ledger consistency/repair ADR classified too late in architecture README | opening barrier in W1 | blocker | Promote into TASK-000 and later reconcile README question grouping. |
| G-006: historical enum drift and sole-writer guard unresolved | materializer cutover | blocker | Trace drift; add writer-boundary guard. |
| G-007: Invoke `plan.md` missing locally | formal Invoke conformance | flag | Regenerate/repair Invoke package separately; retain template fallback provenance. |
| G-008: Slice-1 security/realtime decisions absent | W2 | deferred blocker | Resolve OQ-VISIBILITY through OQ-SANDBOX before W2. |
| G-009: provider capability/credential/resource decisions absent | W3 | deferred blocker | Resolve OQ-CAPABILITIES through OQ-PRODUCT-EVAL before W3/W4. |
| G-010: recipe supply-chain and override decisions absent | W6 | deferred blocker | Resolve applicable section-17 ADRs before W6. |
| G-011: Pydantic pin and canonical JSON/digest vectors unaccepted | W1 runtime entry | repaired for W0 decision scope | ADR-001 accepts exact pins and reviewed omitted/null, Unicode, numeric, ordering, version-byte and SHA-256 vectors; TASK-010 must apply the lock and prove them executably. |
| G-012: sole-writer evidence bundle not proven on target host | materializer cutover, not TASK-010 journal start | blocker | W0 freezes schema, drift disposition, guard spec and named tests; TASK-020 produces process/ACL/inventory/negative-test evidence before cutover; lint is auxiliary only. |
| G-013: external-adoption tests collided with the existing T-ACI-R21 ID | traceability | repaired | Dedicated T-ACI-ETA1–ETA5 IDs are indexed once and mapped to all five adoption concepts. |

No gap may be closed by implementation alone when its repair path requires an authority decision.
