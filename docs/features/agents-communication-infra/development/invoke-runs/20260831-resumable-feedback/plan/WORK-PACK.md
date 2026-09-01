# WORK-PACK: Resumable Dispatch Feedback

## Purpose and current gate

Implement the bounded `author:0 -> reviewer:0 -> author:1` continuation in layers. CONF-000 and
CONF-001, CONT-001, HEADS-001 and BUS-001 are closed as bounded reviewed components. The active
boundary is now the hard `PRODUCT-PASS` decision gate. CONT-002 remains an unpromoted umbrella;
no real opening, positive Run transition, resume or worker step is authorized.

| Field | Value |
|---|---|
| plannerGateStatus | `heads-001-and-bus-001-implemented-reviewed-pass; block-cont-002-product` |
| activePlanRef | [W2](work-pack/waves/W2.md) |
| activeTask | `PRODUCT-PASS` under [TASK-CONT-002](work-pack/tasks/TASK-CONT-002.md) |
| descriptor | BUS entry authority retained historically at `work-pack/descriptors/SWU-ACI-RUNTIME-ATTEMPT-RESULT-BUS-001.json` |
| readiness | HEADS and BUS reviewed PASS/KEEP; PRODUCT-PASS and CONT-002 blocked |
| complexity | high |
| readinessProfile | local SQLite component proof; no production/provider claim |

## Task status board

| Task | Goal | Gate | Status |
|---|---|---|---|
| CONF-000 | Reviewed executable confirmation contract | closed | PASS |
| CONF-001 | Durable confirmed-dispatch writer through `opening_pending` | closed | implemented-reviewed-pass |
| [TASK-CONT-001](work-pack/tasks/TASK-CONT-001.md) | Consume CONF-001 authority and persist effect-free suspension | closed | implemented-reviewed-pass |
| HEADS-001 | Run/Group heads, total reducers, CAS and fail-closed fence | reviewed closure | implemented-reviewed-pass |
| BUS-001 | Official publication component proof | reviewed closure | implemented-reviewed-pass |
| PRODUCT-PASS | Supply missing bytes/policies and new CONF v2 confirmation | product decision | blocked |
| [TASK-CONT-002](work-pack/tasks/TASK-CONT-002.md) | Resolve official inputs and drive one fake-adapter resume | HEADS -> BUS -> PRODUCT -> later SWUs | not-promoted |
| [TASK-CONT-003](work-pack/tasks/TASK-CONT-003.md) | Loss reconstruction, unknown, cancellation, expiry and crash recovery | CONT-002 reviewed PASS | blocked-by-002 |
| TASK-VERIFY/AUDITS | Feature verification, alignment and layering closure | CONT-003 complete | blocked-by-003 |

## L2 decision lock

The 2026-09-01 [Robot Talks findings](../../../../robot-talks/2026-09-01-continuation-l2-d0/findings.md)
and two brownfield audits resolved every L2 code-entry decision:

- component/consumer claim only;
- test-only prerequisite using the complete journal-backed attempt lifecycle and immutable terminal
  snapshot binding; its validators are test-wired directly to the journal, with no production
  attempt-writer symbol or `ACI_SCHEMAS` widening;
- generic `RuntimeJournal.accept` with service-derived
  `aci.agent-continuation:<continuation_id>` / `suspend@1`; no caller idempotency key;
- UTC deadline = confirmed `confirmed_at + wall_clock_seconds`;
- exact zero-of-two official source facts accepts both mappings as awaited; every partial, complete
  or ambiguous state fails closed to CONT-002; and
- persisted derived-key replay precedes current-fact evaluation; only create prechecks and
  transactionally revalidates exact zero-of-two, so later facts preserve the first receipt; and
- migration 013 creates four isolated runtime tables with direct CONF-001 parents, no backfill and
  no change to legacy schema, rows or behavior.
- service uses read-only SELECTs plus mutation SQL only on the journal-supplied connection; no
  `database.write()`, commit, second transaction/writer or repository relocation to `database.py`.

## Architecture-guided directives

| Concern | Directive | Proof |
|---|---|---|
| Authority consumption | Derive continuation/dispatch/source/mappings only from CONF-001 rows; legacy/caller substitutions reject. | Authority negative matrix and unchanged legacy bytes. |
| Attempt prerequisite | Tests traverse `requested -> starting -> running -> completed` through generic journal acceptance and bind the finalized snapshot to terminal evidence. | Harness inspection plus lifecycle/event/offset assertions. |
| Atomic suspend | Pure kernel + service orchestration + generic journal transaction; one aggregate/members/event/head/receipt, zero effects. | T-ACI-CONT1, failpoints, replay/reopen. |
| Official inputs | Query exact two source-message identities; only zero facts is L2-admissible. | zero/one/two/ambiguous matrix. |
| Lifecycle | Closed pure reducer for L2/base events; reject all unlisted pairs without mutation. | base T-ACI-CONT9 Cartesian matrix. |
| Compatibility | Isolated runtime tables parent CONF-001 directly; migration 009/010 path remains legacy-only. | schema introspection, no backfill, legacy non-regression. |

## Wave status

| Wave | Objective | Entry | Exit | Status |
|---|---|---|---|---|
| W0/CW0-CW1 | Confirmation contract and durable writer | user authority | CONF-001 reviewed PASS | completed |
| [W1/CW2](work-pack/waves/W1.md) | CONF-001-backed continuation suspension | exact D0 + audits + readiness | CONT-001 reviewed PASS | completed |
| [W2/CW3](work-pack/waves/W2.md) | Gated same-session foundation | W1 PASS | CONT-002 reviewed PASS | HEADS/BUS complete / product-blocked |
| [W3/CW4](work-pack/waves/W3.md) | Failure/recovery hardening and closure | W2 PASS | CONT-003 + closure audits PASS | blocked |

## Exact L2 write and validation authority

The canonical ordered write scope, pre-mutation source pins, semantic-intent discriminants, test
matrix, exclusions and commands live in
`work-pack/descriptors/SWU-ACI-AGENT-CONTINUATION-001.json`. Its byte-matching readiness receipt was
the historical code-entry authority and remains unmodified after promotion. The final bounded
result is [evidenced here](evidence/TASK-CONT-001.md).

One code writer owned the 13 CONT-001 paths and a different reviewer returned PASS. HEADS-001 and
BUS-001 are also reviewed PASS/KEEP. BUS entry descriptor/readiness digests remain historical;
[final BUS evidence](evidence/TASK-BUS-001.md) records the implemented bytes and validation. No
further mutation writer is authorized before PRODUCT-PASS, and CONT-002 remains unpromoted.

## Stop boundary

Stop rather than widen L2 if authority/digests disagree, the prerequisite is not a complete
journal-backed lifecycle with terminal snapshot linkage, a target attempt exists, official facts
are not exact zero-of-two, suspension needs an effect, legacy/CONF-001 mutation is required,
scope/key must become caller-controlled, a second create shares the identity, or CONF/AUTH/full
runtime evidence regresses.

## Change log

| Date | Change |
|---|---|
| 2026-08-31 | Initial L0/L1 work pack and confirmation prerequisite gate. |
| 2026-08-31 | CONF-000/CONF-001 closed with reviewed evidence. |
| 2026-09-01 | L2 D0 resolved; exact CONT-001 descriptor/readiness issued for migration 013 component proof. |
| 2026-09-01 | CONT-001 promoted to implemented-reviewed-pass; CONT-002 exact planning is the next gate. |
| 2026-09-01 | C2 split into HEADS, BUS and hard PRODUCT gate; HEADS-001 selected as bounded foundation. |
| 2026-09-01 | HEADS-001 initial PASS reopened: local Group identity lacked graph scope; BUS readiness withheld. |
| 2026-09-01 | HEADS repair-entry readiness reissued over the same 12 paths; a second MAJOR requires same-transaction graph→run binding and A/B plus B/A zero-mutation tests; no promotion. |
| 2026-09-01 | HEADS repair closed with 8/8 focused, 177/177 runtime and red-team PASS/KEEP; exact BUS-001 descriptor/readiness issued. |
| 2026-09-01 | BUS-001 closed with 23/23 focused, 200/200 runtime and red-team PASS/KEEP; the route stopped at hard PRODUCT-PASS. |
