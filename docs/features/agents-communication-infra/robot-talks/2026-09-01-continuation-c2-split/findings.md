# Continuation C2 split — findings

## Disposition

The technical/product split is accepted. HEADS-001 may enter implementation readiness as a bounded
foundation/component proof. CONT-002 itself is not promoted. BUS-001 needs a later exact work pack;
all work after BUS remains blocked by PRODUCT-PASS and new confirmation authority.

## Tensions and resolutions

| ID | Tension | Evidence | Impact | Resolution |
|---|---|---|---|---|
| C2-T1 | Temporary ledger versus complete opening authority | CONF-001 ends at `opening_pending`; the current confirmed package does not contain every canonical 0.6.4 opening-row value. | A local ledger prevents external mutation but cannot invent missing authoritative bytes. | Move OPEN after PRODUCT-PASS and require a new dispatch identity/CONF v2 plus human confirmation for changed authority. |
| C2-T2 | Monolithic CONT-002 versus explicit gates | HEADS/BUS mechanics are technically decidable; prompts, revision instruction and policy values are product decisions. | A monolith would bury product defaults in technical implementation. | Sequence HEADS, then BUS, then a hard product gate before OPEN/resume/worker. |
| C2-T3 | HEADS foundation versus dead schema | Run/Group transition tables and RUN-I2/RUN-I6 define useful fail-closed behavior independently of materialization. | Schema without reducers/CAS/fence evidence adds maintenance cost without proof. | Admit HEADS-001 only with total reducers, exact CAS/races/reopen, isolated parents and zero-effect fence tests. |
| C2-T4 | Harness verified opening versus materialization evidence | A positive Run transition needs a verified fence fact, but no production opening materializer is authorized. | A fixture could be misreported as an executable opening path. | Tests may create verified evidence directly through generic journal/DB seams, explicitly harness-only. Add no positive production writer, service or API. |
| C2-T5 | Pending/reconciliation state versus effect eligibility | RunLifecycle keeps `opening_pending` and `reconciliation_required` execution-blocked. | Releasing or claiming any effect would violate RUN-I2/RUN-I6. | Both states are permanently ineligible in HEADS-001 tests; zero provider/tool/start effects exist. |

## TECH-D0 decisions

- Runtime-aware publication derives `source_message_id` from the confirmed mapping.
- Group identity has one exact normalized derivation from the confirmed graph.
- Official author/reviewer events remain typed and are paired with `attempt.result_accepted`.
- Effective input has exactly four ordered entries; wrapper data is separate metadata/reference when
  literal four-entry cardinality is required.
- Attempt, plan, request, effect and event identities are deterministic.
- `agent_resume` is non-retryable.
- Commands that advance Run and Group heads use one atomic multi-head CAS contract.
- Author-turn-1 response schema and adapter/model/tool references derive from confirmed authority.

## PRODUCT-PASS inputs

Product authority must supply exact bytes/references/digests for the revision instruction and real
prompts; role/task references; `provider_ref` when distinct from the adapter; resource, sandbox and
execution-fence policies; and the total canonical opening-row projection including dispatch
type/route, goal, context, approver and agents.

## Hard stop

After BUS-001, do not materialize or verify a real opening, move Run to `ready`, finalize effective
input, create `agent_resume`, claim/release an effect or call an adapter until PRODUCT-PASS and new
human-confirmed authority exist.

