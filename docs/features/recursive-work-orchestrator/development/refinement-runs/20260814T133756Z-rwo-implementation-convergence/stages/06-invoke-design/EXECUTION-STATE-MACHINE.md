# Execution State Machine — RWO-CVG-001

Status: `design-only; planned and unexecuted`
Version: `rwo-convergence-execution/v1`

## Deterministic order

1. Parse and validate the closed lock, axis/claim catalog, expectation bindings,
   source-closure manifest, runner graph and output identity.
2. Materialize a byte-exact read-only snapshot from the validated lock. Rehash
   the complete snapshot before any runner.
3. Traverse required descriptors in catalog order. Resolve that descriptor's
   executable, trust, dependencies and offline posture only when its turn is
   reached.
4. The first required descriptor that is blocked, fails, times out, receives a
   signal, emits invalid structured evidence, or observes snapshot drift is the
   chronological terminal cause. Stop launching later descriptors immediately.
5. Mark every later required descriptor `not-run` with the terminal descriptor
   ID. Project all axes and claims, including required unsupported claims.
6. Rehash the snapshot before projection and again before publication. Any
   mismatch invalidates all observations from that snapshot and supports no
   positive claim.
7. Attempt one complete create-new package publication. A publication defect is
   the terminal cause only when no earlier terminal cause exists; otherwise it
   is recorded as secondary and cannot replace the earlier cause.

A globally malformed lock/catalog/descriptor graph blocks before the snapshot.
A later prerequisite is not discovered early merely to outrank an earlier
executed descriptor. This makes block-before-fail and fail-before-block outcomes
depend only on declared order.

## Exit registry

| Condition | Process exit | Canonical termination |
| --- | ---: | --- |
| complete with no failed or blocked required axis | 0 | `complete` |
| lock/catalog/schema/path/source-closure invalid | 64 | `preflight-blocked` |
| runner graph/order invalid | 65 | `plan-blocked` |
| current descriptor prerequisite absent, stale or untrusted | 66 | `prerequisite-blocked` |
| source/snapshot drift | 67 | `source-drift` |
| structured evidence or normalizer invalid | 68 | `evidence-invalid` |
| claim projection invalid | 69 | `projection-invalid` |
| final package cannot be validated or atomically created | 70 | `publication-invalid` |
| child exits 1–123 or 125–255 | preserve exact code | `child-exit` |
| child times out | 124 | `timeout` |
| child is terminated by signal N | `128 + N` when <=255, else 125 | `signal` with exact N |

The canonical report field is `execution_termination`, never `conformance`,
`overall_status`, `score`, or a synonym. It records the first terminal sequence
number, runner ID when applicable, kind, exact child exit/signal when
applicable, wrapper exit, and secondary publication/cleanup defects.

## Required negative fixtures

- `TERM-BLOCK-BEFORE-FAIL`: an earlier untrusted required tool stops the later
  fake failing runner; exit 66 and later `not-run` are exact.
- `TERM-FAIL-BEFORE-BLOCK`: an earlier fake child exit 7 stops before the later
  missing tool; exit 7 is preserved.
- `TERM-TIMEOUT`: a fake child timeout maps to 124 without a cleanup override.
- `TERM-SIGNAL`: a fake signal records the signal and deterministic wrapper exit.
- `TERM-PUBLICATION-AFTER-FAIL`: publication failure is secondary to the earlier
  child exit and cannot replace it.
- `TERM-NO-UNLISTED-CHILD`: a descriptor that tries to launch an undeclared child
  is blocked before that child runs.

No retry occurs inside a run. A later attempt requires a new lock and output
identity.
