# Cross-Task Gap Ledger

| Gap | Blocks | State | Repair path |
|---|---|---|---|
| G-001: persistence/offset/transaction contract absent | W1 | blocker | TASK-000 persistence ADR |
| G-002: initial decision and dissent semantics absent | fixed group protocol in W1 | blocker for 0E, not 0B-0D | TASK-000 protocol ADR |
| G-003: terminal mapping across attempt/group/run absent | W1 | blocker | TASK-000 terminal ADR |
| G-004: external-input snapshot boundary absent | 0E and real adapters | blocker for 0E | TASK-000 snapshot ADR |
| G-005: ledger consistency/repair ADR classified too late in architecture README | opening barrier in W1 | blocker | Promote into TASK-000 and later reconcile README question grouping. |
| G-006: historical enum drift and sole-writer guard unresolved | materializer cutover | blocker | Trace drift; add writer-boundary guard. |
| G-007: Invoke `plan.md` missing locally | formal Invoke conformance | flag | Regenerate/repair Invoke package separately; retain template fallback provenance. |
| G-008: Slice-1 security/realtime decisions absent | W2 | deferred blocker | Resolve OQ-VISIBILITY through OQ-SANDBOX before W2. |
| G-009: provider capability/credential/resource decisions absent | W3 | deferred blocker | Resolve OQ-CAPABILITIES through OQ-PRODUCT-EVAL before W3/W4. |
| G-010: recipe supply-chain and override decisions absent | W6 | deferred blocker | Resolve applicable section-17 ADRs before W6. |

No gap may be closed by implementation alone when its repair path requires an authority decision.

