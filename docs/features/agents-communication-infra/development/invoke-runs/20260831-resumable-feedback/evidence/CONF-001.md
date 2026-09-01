# CONF-001 - durable ConfirmedDispatch writer

## Result

`PASS` for the bounded durable confirmation writer. `SWU-ACI-CONFIRMED-DISPATCH-001` is
`implemented-reviewed-pass`: the reviewed CONF-000 authority is accepted by one authenticated
single-writer SQLite transaction that ends at durable `opening_pending`, with one pending/unclaimed
audit-opening intent and zero external action.

This result closes the CONF-000 -> CONF-001 prerequisite chain. It does not authorize
TASK-CONT-001, legacy-FK decoupling, effect claiming/materialization, audit-opening verification,
agent start, provider/tool execution, UI/API work, production cutover, commit, push or deploy.

## Entry and final integrity pins

| Artifact | SHA-256 |
|---|---|
| [Entry descriptor](../../../../work-pack/descriptors/SWU-ACI-CONFIRMED-DISPATCH-001.json), bytes authorized before implementation | `sha256:797e14af8e53832cab4d44385529dc75f477cf96cf7ccab02889b0642db0c0fc` |
| [Historical entry readiness receipt](../../../../work-pack/execution/SWU-ACI-CONFIRMED-DISPATCH-001-code-readiness.json) | `sha256:15b2117b05e92d01cec4797b0ee7fd989c1f1fd8406753152eead13297f6d588` |
| [Final Stage-E source manifest](../../../../../agent-provenance-telemetry/integration/stage-e/source-manifest.json) | `sha256:d29d7959fde52f6f7a67b50382dd2e7c52bc8ae395713cbcca9d095d2f6bbb92` |
| [Final Stage-E execution receipt](../../../../../agent-provenance-telemetry/integration/stage-e/execution-receipt.md) | `sha256:c45c7362c9f243f9e33805913a9e60acf20b2f146abeb25b6af7967b7cd0cde8` |

The descriptor is promoted after implementation, so its current bytes intentionally differ from
the entry digest above. The readiness JSON remains the immutable entry receipt and is not repinned
to the post-implementation status document.

## Verification evidence

- Focused confirmation PASS: 56/56 negative cases and 21/21 declared failpoints exercised, with
  golden acceptance, migration/reopen, replay, conflict, concurrency, lost-response and zero-partial
  state evidence.
- Independent red-team PASS: 66/66 bounded contract and implementation assertions reproduced,
  including exact authority/identity/binding/event/effect/receipt relationships and metadata-aware
  rejection of invalid capability-preview authority.
- Complete runtime discovery PASS: 160/160 tests.
- The independent implementation reviewer returned `PASS` after the final red-team correction and
  complete validation rerun.
- Stage-B, traceability, Stage-C, orchestration bridge, compileall and `git diff --check` passed; the
  latter reported line-ending conversion warnings only.
- Queries and reopen comparison prove one immutable observation/confirmed dispatch/run, one graph,
  one continuation, two ordered mappings, exactly nine new authoritative artifact-metadata rows,
  two events, version-2 head, one stable receipt and one pending/unclaimed audit-opening intent.
- No provider/tool/start effect, external audit materialization, continuation mutation or network
  action was performed.

## Isolated freeze incident

A concurrent-writer incident changed task-owned bytes after an intermediate pin. Ownership was not
attributed. The affected scope was isolated, writes were frozen, every task-owned path was rehashed,
and the complete validation matrix was rerun before the final Stage-E pins above were accepted. The
final 14-path snapshot remained byte-identical through the required validations.

## Promotion boundary

TASK-CONT-001 is now dependency-unblocked from CONF-000/CONF-001 but remains blocked for code entry.
The next layer requires its own exact L2 work pack, two independent brownfield audits and a fresh
exact-scope readiness receipt before any mutation.

