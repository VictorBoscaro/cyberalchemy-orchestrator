# Cross-Task Gap Ledger

| Gap | Blocks | State | Repair path |
|---|---|---|---|
| G-001: persistence/offset/transaction contract absent | named mutation SWU | repaired for SWU-ACI-001; remaining W0 corpus review pending | ADR-001 accepted; ADR-002/fixtures/profiles/storage/descriptor await one digest-bound corpus PASS. |
| G-002: compatibility/terminal/snapshot W0 acceptance | named mutation SWU | authored; review-pending blocker | Review the W0 closure artifact manifest and close B-001/B-002 without enabling serving/cutover. |
| G-003: target-host sole-writer proof | TASK-020/cutover | deferred blocker | W0 freezes schema/guard/tests; TASK-020 supplies process, ACL, inventory and negative bypass evidence. |
| G-004: local pilot enablement | post implementation | blocker | Separate reviewer/root PASS after mutation tests; never inferred from test authorization. |
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
| G-CVR-001: coordinated CVR packet acceptance absent | SWU-ACI-CVR-GUARD-001/001/002 | blocker; proposed predicate non-operative | Amend and accept ADR, spec, tests, task and selected deterministic descriptor as one packet. |
| G-CVR-002: reproducible PyYAML pin and restricted-loader goldens absent | SWU-ACI-CVR-001 semantic acceptance | blocker | Resolve exactly `PyYAML==6.0.1` from `implementations/vault_read/requirements.lock` and pass duplicate/tag/merge/alias/coercion goldens before accepting semantic code. |
| G-CVR-003: `max_results` projection calibration absent | SWU-ACI-CVR-001 completion | blocker | Record golden artifact projection cardinality and owner-ratified effective limit; CVR-002 later records edge cardinality. |
| G-CVR-004: edge implementation evidence absent | SWU-ACI-CVR-002 | deferred blocker | Bind CVR-001 PASS receipt/byte baseline, allowed delta/prehashes; rerun all CVR-001 tests before edge tests. |
| G-CVR-005: stable AuthoritySlot principals and acceptances absent | SWU-ACI-CVR-001 authorization | blocker; no role may be inferred from writer/reviewer | Record architecture, product/protocol and host/operator principal IDs plus decision/digest evidence; record session root orchestrator only as final approver. |
| G-CVR-006: GUARD bootstrap absent | first guard write | blocker | Root creates one exact bootstrap authorization/claim; external trusted executor invokes guard/tests and its one external authority-owned bootstrap finalizer terminalizes. |
| G-CVR-007: authority artifacts absent | any CVR execution | blocker | Materialize exactly three canonical content-addressed artifacts; no current/revocation/ClaimReceipt/second receipt. |
| G-CVR-008: unrestricted host is not a sandbox | every CVR SWU | accepted limitation requiring operator visibility | Treat the guard as advisory workflow integrity; keep expected digests/session external and never claim structural isolation. |
| G-CVR-009: concrete GUARD descriptor absent | five-entry packet assembly | repaired as non-authorizing proposal | `work-pack/descriptors/SWU-ACI-CVR-GUARD-001.json` now closes the descriptor-absence gap; guard code, owner acceptance and authorization remain absent. |

No gap may be closed by implementation alone when its repair path requires an authority decision.
