# Validation — IMPL-ACI-DRAFT-COMPILER-CONFORMANCE-001

Date: 2026-09-01

Status: accepted bounded validation evidence; dedicated Recheck 3 returned aggregate `KEEP`.

## Directed conformance accepted after Recheck 3

```powershell
python -m unittest implementations.tests.runtime.test_draft_graph_compiler -v
```

Closeout rerun result: exit `0`; 22 tests passed in 8.595s.

The suite preserves the original positive oracle and N01–N24 coverage and adds permanent attacks
for every review finding:

- F1: invalid Ed25519 receipt, stale/non-latest/bound receipts, public/direct construction,
  `object.__new__`, copy, deep-copy and pickle attacks;
- F2: cross-node alias identity and post-return graph mutation while bytes/digest remain coherent;
- F3: embedded `NaN` and required-`false` impossible contracts on both draft and emitted-EG paths;
- F4: free-form, path-like, empty and URI-like selectors; only `$` succeeds;
- F5: content-addressed and ordinary HTTPS URI records both fail structurally;
- F6/R1: conditional outcome dataflow distinguishes `on_success`, `on_failure` and `always`; the
  exact always-after-failure counterexample rejects; success-only ancestry and a bounded repair path
  succeed; mixed impossible routes reject; diamond `all` succeeds while unsafe diamond `any`
  rejects; optional feedback succeeds without changing roots; and required feedback, optional
  producer outputs and multiple unready required producers reject;
- F7: malformed nested structures return typed paths, all boundary roots reject missing/extra/wrong
  shapes, and invalid-catalog diagnostics remain identical under hash seeds 1–8;
- F8: a non-toy single-node graph and inline base64 resource compile through the public boundary;
  extra/missing/duplicate attacks remain source-linked;
- R2: lone surrogates at context, allocator evidence, draft, policy, catalog, resources, inner
  output schemas and canonicalization boundaries return typed paths; six hostile boundaries remain
  identical under clean-process hash seeds 1–4;
- R3: the seven embedded schema byte strings match the SHA-256 of their review artifacts, and a
  clean subprocess imports, verifies context and compiles while `builtins.open`, `Path.open`,
  `Path.read_text` and `Path.read_bytes` are blocked; and
- positive canonical bytes remain identical under reversed object keys and hash seeds 1–6.

Observed oracle result remains 9,902 bytes and
`sha256:f0341899e4fb3e4115ef42ff9394981b125fceee11c2f15b5b147ff9a32df510`.

## Predecessor and adjacent checks

```powershell
python docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/followups/SPEC-ACI-DRAFT-GRAPH-001/validate_artifacts.py
```

Result: exit `0`; all predecessor checks passed, including F1–F6, R1–R2, S1 and 105/105 ownership
leaves. Its printed evidence ceiling remains accurate for that predecessor script.

```powershell
python -m unittest implementations.tests.runtime.test_draft_graph_compiler implementations.tests.runtime.test_protocol_compilation -q
```

Closeout rerun result: exit `0`; 34 tests passed in 8.990s.

```powershell
python -m py_compile implementations/server/runtime/draft_graph_compiler.py implementations/tests/runtime/test_draft_graph_compiler.py
```

Result: exit `0`.

## Broad and exclusion runs

These outcomes are retained from the first repair and were not rerun for the bounded residual-R1
third repair or this closeout. They remain evidence about that shared-tree run, not current-suite
counts after later directed tests were added.

```powershell
python -m unittest discover -s implementations/tests/runtime -p "test_*.py" -q
```

Result: exit `1`; 284 tests ran in 89.613s with 7 failures and 6 errors.

The same discovery suite was flattened and every test whose ID contains
`test_draft_graph_compiler` was excluded.

Result: exit `1`; `EXCLUSION_COUNT 267`; 267 tests ran in 86.152s with the same 7 failures and 6
errors. This proves those 13 failure/error outcomes reproduce outside the new module in the current
shared tree. It does **not** establish that they historically predate this SWU. The failures remain
in dispatch workflow, continuation/bootstrap and runtime-type bootstrap surfaces; this SWU did not
modify them.

```powershell
python -m pip check
```

Result: exit `1` for the current environment’s `python-bcb 0.2.0` versus `httpx 0.27.0` conflict and
an invalid local Django distribution. No conflict involving `jsonschema==4.21.1` or
`cryptography==49.0.0` was reported.

`ruff` remains unavailable in this environment.

## Evidence ceiling

- The fixed public key and signed receipts prove only the conformance allocator fixture boundary;
  no private signing key is stored in the repository and no live allocator/key lifecycle ran.
- `DraftGraph` remains non-authoritative and never becomes a confirmation/runtime payload.
- Returned authority is canonical bytes; graph/report properties are defensive decodes and digest is
  recomputed from bytes. No projector or confirmation boundary consumed the result.
- Output-contract satisfiability is mechanical only for the explicitly admitted subset in
  `IMPLEMENTATION-BOUNDARIES.md`, not general JSON Schema satisfiability.
- URI resources are prohibited. Only exact inline UTF-8/base64 bytes are digest-checked.
- Feedback representation is compiled and checked, but no feedback scheduler ran.
- Required-input readiness is proven only by the documented conditional initial-DAG state model.
  The proof rejects beyond 4,096 abstract outcome states; this can produce safe false negatives.
  Runtime feedback activation remains outside the compiler.
- The compiler imports and runs without filesystem access. Schema artifact correspondence is proven
  by exact SHA-256 byte equality in the directed test; this is not a general code-generation or
  package-integrity claim.
- Credential mapping lacks a positive fixture.
- The ExecutionGraph schema is still proposed. Dedicated review returned aggregate `KEEP` only for
  using this bounded corpus as input to the next canonical-v2 specification work unit.
