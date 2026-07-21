# Smallest Working Unit Manifest

This is the shared index. Task files remain authoritative for implementation details. Only one SWU
may be selected for mutation unless the wave explicitly proves disjoint write scopes.

| SWU | Parent | Dependencies | Write scope | Done / acceptance evidence | Validation | Owner |
|---|---|---|---|---|---|---|
| ACI-001 | TASK-000 | none | ADRs/decision ledger | accepted persistence ADR, schema and crash table | architecture review | manual |
| ACI-002 | TASK-000 | none | ADRs/feature questions | accepted compatibility/ledger/protocol ADRs and EG-1 guard spec | constitution review | manual |
| ACI-003 | TASK-010 | 001 | runtime persistence/tests | atomic journal/head/outbox and dedupe/CAS receipts | persistence tests | local-fallback |
| ACI-004 | TASK-010 | 001 | runtime domain/tests | pure replay with stable state hash | reducer tests | local-fallback |
| ACI-005 | TASK-020 | 002-004 | opening materializer/tests | verified opening or explicit reconciliation | crash/fault tests | local-fallback |
| ACI-006 | TASK-020 | 003-005 | close materializer/tests | one verified close and terminal | crash/fault tests | local-fallback |
| ACI-007 | TASK-020 | 002,005-006 | writer guard/fixtures | sole-writer and golden-row evidence | static/compatibility tests | local-fallback |
| ACI-008 | TASK-030 | 003-005 | fake adapter/worker | durable claim and one logical fake result | adapter tests | local-fallback |
| ACI-009 | TASK-030 | 004,008 | fixed group kernel | fixed collect/reveal/vote/commit trace | protocol tests | local-fallback |
| ACI-010 | TASK-030 | 003-009 | confirm/query/API | frozen sheet, one runtime owner and lifecycle query | API compatibility tests | local-fallback |
| ACI-011 | TASK-030 | 005-010 | E2E/fault fixtures | L0 crash matrix and rollback receipt | full L0 suite | local-fallback |
| ACI-012 | TASK-040 | L0 pass | outbox/reconciler | pending/unknown recovery traces | fault suite | local-fallback |
| ACI-013 | TASK-040 | 012 + visibility ADR | policy/capabilities | sealed cross-surface deny matrix | security tests | local-fallback |
| ACI-014 | TASK-040 | 012 + race ADRs | domain policy/reactors | one allowed terminal per ordering | race suite | local-fallback |
| ACI-015 | TASK-040 | 012 + realtime ADR | projections/API/SSE | cursor reconnect and consistent fallback | API/SSE tests | local-fallback |
| ACI-016 | TASK-040 | sandbox ADR | launcher/credentials | fail-closed/no-secret evidence | adversarial tests | local-fallback |
| ACI-017 | TASK-050 | L1 + capability ADR | adapter contracts | reusable fake conformance receipt | contract suite | local-fallback |
| ACI-018 | TASK-050 | 017 + credential ADR | provider adapter | canonical provider lifecycle trace | provider tests | local-fallback |
| ACI-019 | TASK-050 | 018 + unknown ADR | adapter policy | malformed/late/unknown mappings | failure suite | local-fallback |
| ACI-020 | TASK-050 | 018 + resource ADR | launcher/budgets | limit and secret inspection receipts | security/resource tests | local-fallback |
| ACI-021 | TASK-060 | L2 + product ADR | experiment protocol | immutable preregistration | independent review | manual |
| ACI-022 | TASK-060 | 021 | evaluation data | blinded run receipts and complete dataset | reproducibility check | local-fallback |
| ACI-023 | TASK-060 | 022 | evaluation report | threshold-applied decision | blinded review | manual |
| ACI-024 | TASK-070 | W4 continue | capability spec | reviewed matrix/rejection fixtures | contract review | manual |
| ACI-025 | TASK-070 | 024 | second adapter | common conformance receipt | adapter suite | local-fallback |
| ACI-026 | TASK-070 | 025 | mixed fixtures | single-protocol mixed trace | integration tests | local-fallback |
| ACI-027 | TASK-070 | 026 | audit report | no-kernel-fork finding | trace/path review | manual |
| ACI-028 | TASK-080 | L3 pass | handoff modules | one restart-safe logical handoff | duplication/fault tests | local-fallback |
| ACI-029 | TASK-080 | recipe ADRs | built-in packages | two immutable recipe digests | package validation | local-fallback |
| ACI-030 | TASK-080 | 029 | recipe compiler | canonical specs and rejection fixtures | compiler tests | local-fallback |
| ACI-031 | TASK-080 | 028-030 | skill/UI/API clients | cutover/rollback and no dual owner | compatibility E2E | local-fallback |
| ACI-032 | TASK-080 | 031 | audit/check | zero business/provider kernel branches | static scan/review | manual |

## Execution receipt

Every selected SWU returns:

```yaml
swu_id: SWU-ACI-NNN
result: pass | flag | block | interrupted
files_touched: []
validation: []
state_or_event_hashes: []
blockers: []
handoff_note: ""
```

