# TASK-CONF-001 - durable ConfirmedDispatch writer

## Promotion status

- **State:** `implemented-reviewed-pass`
- **Evidence:** [CONF-001](../../development/invoke-runs/20260831-resumable-feedback/evidence/CONF-001.md)
- **Entry descriptor:** `sha256:797e14af8e53832cab4d44385529dc75f477cf96cf7ccab02889b0642db0c0fc`
- **Historical entry readiness:** `sha256:15b2117b05e92d01cec4797b0ee7fd989c1f1fd8406753152eead13297f6d588`

The entry readiness receipt remains pinned to the descriptor bytes authorized before implementation.
It is not repinned after this status promotion. The final implementation passed independent review,
56/56 negative cases, 21/21 failpoints, 66/66 red-team assertions and the 160/160 runtime suite.

## Objective and boundary

Implemented `SWU-ACI-CONFIRMED-DISPATCH-001`: one authenticated, single-writer SQLite acceptance
transaction that consumes the reviewed CONF-000 authority package and ends at durable
`opening_pending`.

The minimum useful proof is one byte-identical accepted unit containing the immutable confirmation
observation, derived confirmed authority, run/graph/mappings, exactly nine newly authoritative
artifact-metadata members, two events, version-2 run head, stable receipt, and one pending unclaimed
generic audit-opening effect intent. The transaction performs zero external action.

The service receives the trusted canonical document bytes and the finalized capability-preview
artifact reference/digest represented by the fixture. That preview is verified and referenced, not
re-finalized and not counted among the exactly nine new artifact-metadata members.

## Entry decision

- CONF-000 is closed by reviewed golden evidence.
- The brownfield alignment audit's only BLOCK was the obsolete CONF-000 package and missing successor
  work pack; this revision resolves that contradiction.
- The independent layering audit is PASS subject to the boundaries encoded below.
- A fresh exact-descriptor `domainspec-code-readiness@1` PASS is required before runtime mutation.

The readiness receipt proves descriptor/test/scope self-consistency. It is not a substitute for the
independent CONF-000 review or either brownfield audit.

## Frozen inputs

| Artifact | SHA-256 |
|---|---|
| `specs/fixtures/confirmed-dispatch-v1/manifest.json` | `sha256:919385d226240fa66621d7b660ef49b70ad7e3d3a379bee3d7c29729243acd0a` |
| `TEST-SPEC.md` | `sha256:1dba61d54e61538f95a3a383f18e55deddb152a7b210638bc2d8bf7b3b5a44ea` |
| `specs/confirmation-authority.md` | `sha256:4e9f92545c9ab35a9ab555efee0488e7c3aec9b849dad17f07a82e166018252c` |
| `confirmation-implementation-layering.md` | `sha256:09c4550df27beefa796fba063aff8dea2d4ff25d0b96240809fa076e171ae875` |
| `evidence/CONF-000.md` | `sha256:e412d43a671cb4c2c362ff62011a637474aeb237873c5c64a334b0120c07893a` |

All specifications, fixtures, golden vectors and the manifest are read-only for this SWU. Drift in
any frozen input is a stop condition.

## Exact ordered write scope

No implementation may write outside these paths, in this order:

1. `implementations/server/runtime/migrations/012_runtime_confirmation.sql`
2. `implementations/server/runtime/database.py`
3. `implementations/server/runtime/errors.py`
4. `implementations/server/runtime/artifacts.py`
5. `implementations/server/runtime/confirmation.py`
6. `implementations/server/runtime/journal.py`
7. `implementations/server/runtime/service.py`
8. `implementations/tests/runtime/test_runtime_confirmation.py`
9. `implementations/tests/runtime/aci-test-traceability.json`
10. `implementations/tests/runtime/test_aci_traceability.py`
11. `docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json`
12. `implementations/server/runtime/local_pilot.py`
13. `docs/features/agent-provenance-telemetry/integration/stage-e/execution-receipt.md`
14. `docs/features/agent-provenance-telemetry/integration/stage-e/execution-receipt.sha256`

Existing baseline repairs in the Stage-E manifest and `local_pilot.py` must be preserved. Those
paths may change only to bind the final task-owned source/test bytes, refresh the manifest digest,
append revalidation evidence, and refresh the companion receipt digest.

## Layer ownership

- `confirmation.py` owns pure strict decoding, trusted-observation verification, projection,
  deterministic identities, graph/mapping construction, authority/event/effect payloads and no I/O.
- `artifacts.py` adds a metadata-aware authorized read that returns and validates the complete
  artifact reference while preserving existing `get_authorized` callers and behavior.
- `service.py` owns application authorization and preparation from trusted document bytes plus the
  finalized capability-preview reference. It requires the fixture/contract metadata fields
  `artifact_id`, `content_hash`, `media_type`, `schema_ref`, `classification`, policy references and
  finalization receipt; it verifies and references that preview without re-finalizing it and
  performs no direct SQL.
- `journal.py` owns the specialized `accept_confirmed_dispatch` transaction and is the sole writer.
- migration `012` and `database.py` own persistence/discovery only.
- `errors.py` may add only task-specific fail-closed error vocabulary.
- `test_runtime_confirmation.py` owns the complete CONF-001 behavioral proof.

The generic `RuntimeJournal.accept` and `RuntimeService._stable_id` are not reusable for this unit:
their replay ordering and identity preimages differ from the confirmed-authority contract.

## Atomic acceptance contract

Inside one `BEGIN IMMEDIATE` transaction, the writer must:

1. replay by client idempotency key;
2. replay same `(dispatch_id, confirmed_authority_digest)` identity even under a fresh key;
3. reject the same dispatch identity with a different authority digest permanently;
4. perform the expected-head CAS only after those replay/conflict decisions;
5. persist all domain rows, exactly nine new artifact metadata rows, both events, version-2 head,
   stable receipt and one pending generic effect intent; and
6. commit once or leave every task-owned row absent.

The effect intent's command relationship must work within the same atomic unit. It may use a
deferred foreign key or an equivalently proven ordering, but it must not require an earlier external
command transaction.

## Required evidence

- T-ACI-AUTH1 through T-ACI-AUTH8 are mapped to real selectors in the focused runtime test.
- The final fixture acceptance bytes and all derived IDs/digests equal the reviewed golden.
- All 56 negative cases and all 21 failpoints are exercised at their declared boundary.
- Preview bytes with wrong `schema_ref`, `media_type`, `classification` or policy metadata reject
  before persistence; metadata-aware reads do not regress existing `get_authorized` callers.
- Same-key and same-identity/fresh-key replay return the first receipt; semantic drift conflicts.
- Concurrency, lost response after commit, reopen and migration idempotence converge to one unit.
- Every pre-commit failpoint leaves zero partial authority/domain/artifact/event/head/effect/receipt
  state; post-commit retry returns the identical receipt.
- Database inspection proves one graph, one continuation, two ordered mappings, exactly one pending
  unclaimed audit-opening intent, and no provider/tool/start effect.
- Focused Stage-B, traceability, Stage-C, orchestration bridge and the complete runtime suite pass.

## Validation commands

```text
python -B -m unittest implementations.tests.runtime.test_runtime_confirmation -v
python -B -m unittest implementations.tests.runtime.test_apt_stage_b -v
python -B -m unittest implementations.tests.runtime.test_aci_traceability -v
python -B -m unittest implementations.tests.runtime.test_stage_c -v
python -B -m unittest implementations.tests.runtime.test_orchestration_bridge -v
python -B -m unittest discover -s implementations/tests/runtime -t .
python -B -m compileall implementations/server/runtime implementations/tests/runtime
git diff --check
```

## Explicit exclusions and stop conditions

Do not add an API/endpoint, package export, UI, CLI, chat hook or host hook. Do not claim or deliver
the opening effect, invoke the audit-ledger appender, accept opening verification, start an agent,
call a provider/tool, implement continuation/suspension, decouple legacy foreign keys, seed
authority, or change `legacy-managed` semantics.

Stop on frozen-input drift, a need to edit specs/fixtures, a write outside the descriptor, any
external effect, inability to preserve the Stage-E baseline repair, or a failure that requires
widening into a deferred layer.

## Completion topology

Exactly one coder owned the write scope, and a different independent reviewer accepted the final
diff and evidence. CONF-001 completion permits planning the legacy-FK/TASK-CONT-001 layer; it does
not authorize that layer automatically. TASK-CONT-001 still requires an exact L2 work pack, two
independent brownfield audits and fresh readiness before code entry.
