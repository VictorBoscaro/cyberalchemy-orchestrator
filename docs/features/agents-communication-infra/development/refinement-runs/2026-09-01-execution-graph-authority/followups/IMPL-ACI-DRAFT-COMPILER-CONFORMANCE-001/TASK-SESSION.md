# Task session — IMPL-ACI-DRAFT-COMPILER-CONFORMANCE-001

## Task Session Result

- Task: `IMPL-ACI-DRAFT-COMPILER-CONFORMANCE-001`
- Route: bounded implementation/conformance closeout after dedicated Recheck 3
- Result: `PASS`; dedicated Recheck 3 returned aggregate `KEEP`
- Runtime: local Python implementation; no runtime integration
- Adapter: none
- Handoff pack: none
- Strict coverage: pass for conditional R1 and preserved R2/R3/F1-F9 bounded scope
- Fallback search: only governing predecessor and existing runtime compiler/test conventions
- Gate verdict: predecessor aggregate `KEEP` passed; initial review, Recheck 1 and Recheck 2 returned
  `FIX`; the repaired residual R1 passed dedicated Recheck 3 with aggregate `KEEP`
- Subagent closeout: `pass`; the worker spawned no agents, and the parent-owned dedicated reviewer
  completed Recheck 3 with aggregate `KEEP`
- Synchronized records: this file, `VALIDATION.md`, implementation boundary, schemas/fixtures and
  code/tests only. Canonical spec, CRAFT, ledger and predecessor `review.md` remain untouched.

## Repaired obligation matrix

| ID | Obligation | Repair evidence | Worker status |
|---|---|---|---|
| F1 | Non-forgeable context boundary | signed allocator evidence; opaque registered context; direct/copy/pickle attacks | review_keep |
| F2 | Coherent immutable result | bytes-only stored authority; computed digest; defensive graph/report views | review_keep |
| F3 | Strict and satisfiable contracts | strict embedded parser, metaschema, admitted witness subset, symmetric attacks | review_keep |
| F4 | Closed selectors | literal `$` contract and negative matrix | review_keep |
| F5 | Verified resource bytes | URI branch removed; inline UTF-8/base64 digest checks | review_keep |
| F6 | Condition-aware topology | conditional outcome states, satisfiable joins, feedback and any/all tests | review_keep |
| F7 | Schema-equivalent deterministic gates | bundled delivered validators, stable paths/table order, hash-seed attacks | review_keep |
| F8 | Non-overfit harness | F1–F7 attacks, non-toy positive and alternative inline encoding | review_keep |
| F9 | Claim discipline | current-tree exclusion evidence; no historical-preexistence claim; exact counts | review_keep |
| R1 | Required-input readiness | conditional must-availability, exact `always` counterexample, mixed/diamond/repair matrix | review_keep |
| R2 | Typed Unicode domain | recursive scalar guard across all inputs/evidence/inner schemas; clean hash-seed attacks | review_keep |
| R3 | Filesystem-free pure boundary | seven exact embedded schema blobs, explicit digests, blocked-I/O clean import/compile | review_keep |
| Recheck 3 | Dedicated implementation review | parent-owned reviewer | keep |

## Technical decisions

- `TrustedAllocatorContextGate.verify(context_json, allocator_evidence_json)` replaces the public
  `AllocatorReservation` convention. The receipt binds context digest/latest/unbound assertions
  under the fixture public key. The compiler re-verifies it on every use.
- `CompilationResult` stores only immutable canonical bytes plus canonicalized external report
  bytes. Its digest is derived, never independently mutable.
- Exact bytes of all seven delivered schemas are compressed into the module and bound to explicit
  SHA-256 values. Their validators gate values before semantic validation; no import/compile
  filesystem access occurs. The proposed EG validator still runs before canonicalization.
- Required node-output inputs must reference required producer outputs. Conditional dataflow tracks
  compatible succeeded/failed outcome states through `on_success`, `on_failure` and `always` routes.
  Every required producer must be succeeded in all states that can activate its consumer. The
  4,096-state cap rejects complex proofs fail-closed rather than assuming readiness.
- All parsed strings, including inner output-schema strings, are checked for lone surrogates before
  validation, hashing or serialization and fail through typed source paths.
- The implementation-specific admitted subsets and topology state machine are explicit in
  `IMPLEMENTATION-BOUNDARIES.md`.
- Policy still restricts/rejects and never widens. Commands remain deny-only. No default executable
  authority was introduced.
- `cryptography==49.0.0` is the only new repair dependency; `jsonschema==4.21.1` remains justified.
- Formal DomainSpec implementation readiness is still not claimed because the local
  `implementation-axioms` dependency is absent.

## Write scope realized

- `implementations/server/runtime/draft_graph_compiler.py`
- `implementations/tests/runtime/test_draft_graph_compiler.py`
- `implementations/requirements.txt`
- `followups/IMPL-ACI-DRAFT-COMPILER-CONFORMANCE-001/`: implementation schemas, allocator evidence
  fixtures, `IMPLEMENTATION-BOUNDARIES.md`, `VALIDATION.md`, `TASK-SESSION.md`

`review.md` was read but not modified.

## Validation and residue

Directed 22/22, adjacent 34/34, predecessor and `py_compile` pass. The earlier broad and exclusion
outcomes remain recorded exactly in `VALIDATION.md` and support only current-tree independence;
they were not rerun for this residual-R1-only repair.

Residue:

- dedicated Recheck 3 completed with aggregate `KEEP` for the bounded corpus;
- the signed allocator surface is fixture-only, not a production allocator/key lifecycle;
- general JSON Schema satisfiability, positive credentials, feedback scheduling, canonical-v2
  promotion, projectors, confirmation, persistence and runtime execution remain outside this SWU;
- 13 broad-suite failure/error outcomes reproduce outside this module in the current shared tree;
  their historical origin is not established.

## Readiness recommendation

The aggregate reviewer `KEEP` recommends this bounded implementation corpus as input to the next
canonical-v2 specification SWU. It remains unsuitable for runtime ingestion or production
execution.

## Decision Gate Result

- Target scope: repaired implementation SWU
- Result: `n/a`
- Blockers remaining: 0 for this bounded implementation SWU; canonical-v2 promotion and runtime
  integration remain separate work
- Next step: canonical-v2 specification work using this corpus as bounded input
