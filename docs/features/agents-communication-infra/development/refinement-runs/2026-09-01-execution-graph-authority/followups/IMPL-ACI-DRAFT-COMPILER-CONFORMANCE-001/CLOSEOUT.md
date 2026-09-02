# Closeout — SPEC-ACI-DRAFT-GRAPH-001 + IMPL-ACI-DRAFT-COMPILER-CONFORMANCE-001

Date: 2026-09-01

Status: `READY_FOR_REVIEW`. This is an evidence synchronization closeout, not a new implementation
or a canonical-v2 promotion.

## Outcome

- The specification corpus received final dedicated Recheck 3 `KEEP` in
  [`../SPEC-ACI-DRAFT-GRAPH-001/review.md`](../SPEC-ACI-DRAFT-GRAPH-001/review.md).
- The pure fixture-backed compiler/conformance corpus received final dedicated Recheck 3 `KEEP` in
  [`review.md`](review.md).
- The four accepted closeout checks pass in the current shared worktree.
- The accepted result is bounded to a non-authoritative DraftGraph and pure compilation into the
  still-proposed ExecutionGraph shape. No runtime integration was performed.

## Context pack and controlling evidence

Lean strict context coverage was complete for this closeout: the two task sessions and validation
records, the implementation work pack, both final review sections, the original session, and the
feature CRAFT/ledger authority ceiling. There was no unresolved product decision and no runtime
handoff.

The final review files were not edited during closeout. Their complete-file SHA-256 values are:

| Review | Final verdict | SHA-256 |
|---|---|---|
| `../SPEC-ACI-DRAFT-GRAPH-001/review.md` | Recheck 3 `KEEP` | `E70B8D68CC426BF9E5F64B6ADD37BE2867F9864AE76BCC4DED8B30D54B2F3D94` |
| `review.md` | Recheck 3 `KEEP` | `7083B3E20EC391826D36B3509D2E3F8F5958E6CD44AD18F8219EB8C428A13984` |

The review pair requirement is satisfied: each worker had a dedicated reviewer; both final review
sections report that the reviewer spawned zero further agents. This closeout worker spawned none.

## Delivered files

Specification/conformance proposal:

- `../SPEC-ACI-DRAFT-GRAPH-001/COMPILATION-CONTRACT.md`
- `../SPEC-ACI-DRAFT-GRAPH-001/FIELD-OWNERSHIP.md`
- `../SPEC-ACI-DRAFT-GRAPH-001/draft-graph-v1.proposed.schema.json`
- `../SPEC-ACI-DRAFT-GRAPH-001/review-correct-verify.draft.json`
- `../SPEC-ACI-DRAFT-GRAPH-001/review-correct-verify.expected.execution.json`
- `../SPEC-ACI-DRAFT-GRAPH-001/NEGATIVE-VECTORS.md`
- `../SPEC-ACI-DRAFT-GRAPH-001/fixtures/`
- `../SPEC-ACI-DRAFT-GRAPH-001/validate_artifacts.py`
- its `WORK-PACK.md`, `TASK-SESSION.md`, `VALIDATION.md`, and immutable `review.md`

Bounded implementation/conformance:

- `implementations/server/runtime/draft_graph_compiler.py`
- `implementations/tests/runtime/test_draft_graph_compiler.py`
- additions `jsonschema==4.21.1` and `cryptography==49.0.0` in
  `implementations/requirements.txt`
- `IMPLEMENTATION-BOUNDARIES.md`
- `schemas/` and `fixtures/` in this implementation follow-up
- this package's `TASK-SESSION.md`, `VALIDATION.md`, immutable `review.md`, and this closeout

## Current validation

Executed from the repository root on 2026-09-01:

```powershell
python -m unittest implementations.tests.runtime.test_draft_graph_compiler -v
```

Exit `0`; `Ran 22 tests in 8.595s`; `OK`.

```powershell
python -m unittest implementations.tests.runtime.test_draft_graph_compiler implementations.tests.runtime.test_protocol_compilation -q
```

Exit `0`; `Ran 34 tests in 8.990s`; `OK`.

```powershell
python docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/followups/SPEC-ACI-DRAFT-GRAPH-001/validate_artifacts.py
```

Exit `0`; all declared checks passed: seven JSON inputs, five resource and ten catalog digests,
exact mapping, F1-F6, R1-R2, S1, remaining negative preconditions, and 105/105 ownership leaves.
The script printed its own limit: no compiler, live allocator, or RFC 8785 canonicalizer was
executed by that predecessor validator.

```powershell
python -m py_compile implementations/server/runtime/draft_graph_compiler.py implementations/tests/runtime/test_draft_graph_compiler.py
```

Exit `0`; no output.

The broad runtime discovery, flattened exclusion run, `pip check`, and `ruff` availability were not
rerun. `VALIDATION.md` retains their earlier exact results: broad 284 tests with 7 failures and 6
errors; exclusion 267 tests with the same 7 failures and 6 errors; environment-level `pip check`
failure; and unavailable `ruff`. Those are historical current-tree observations only, not current
closeout rerun evidence and not proof of historical pre-existence.

## Write-scope audit

The scoped status command currently reports:

```text
 M implementations/requirements.txt
?? docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/followups/IMPL-ACI-DRAFT-COMPILER-CONFORMANCE-001/
?? docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/followups/SPEC-ACI-DRAFT-GRAPH-001/
?? implementations/server/runtime/draft_graph_compiler.py
?? implementations/tests/runtime/test_draft_graph_compiler.py
```

The tracked requirements diff adds only the two pinned dependencies named above. All other
SPEC+IMPL artifacts are currently untracked, so Git proves their present location but cannot prove
historical authorship or distinguish individual edits within those directories.

The shared worktree also contains out-of-scope tracked modifications to the generated
`research-initial-definitions` skill copies, feature `CRAFT.md` and `.craft/ledger.yml`, and the
earlier roadmap session, plus unrelated untracked `.codex/`, research, telemetry, discovery, image,
and session/refinement-stage artifacts. They are treated as pre-existing/shared changes for this
closeout and were not edited, removed, staged, or attributed to these work units.

Closeout mutations are confined to:

- `../SPEC-ACI-DRAFT-GRAPH-001/WORK-PACK.md`
- `../SPEC-ACI-DRAFT-GRAPH-001/TASK-SESSION.md`
- `../SPEC-ACI-DRAFT-GRAPH-001/VALIDATION.md`
- `TASK-SESSION.md`
- `VALIDATION.md`
- `CLOSEOUT.md`

Neither review file was changed. Feature `CRAFT.md`, `.craft/ledger.yml`, the original session,
canonical specs, and implementation code/tests were not changed by closeout.

## Claim ceiling and residue

This closeout supports only these claims:

- the frozen DraftGraph proposal corpus passed dedicated review;
- the bounded pure fixture-backed compiler/conformance corpus is implemented and passed dedicated
  review;
- the current directed 22, adjacent 34, predecessor validator, and `py_compile` checks pass; and
- the reviewed corpus may be used as input to a future canonical-v2 specification work unit.

It does **not** support claims of:

- canonical `aci.execution-graph@2` promotion or general RFC 8785 compliance;
- topology/basic/full projector or preview implementation;
- confirmation `@2` or CONF v1 cutover;
- persistence, runtime ingestion, scheduling, worker/provider/tool/credential execution, or live
  allocator/key lifecycle;
- feedback runtime semantics beyond the compiler's documented conditional initial-DAG model;
- general JSON Schema satisfiability beyond the admitted witness subset; or
- production/runtime readiness.

Feature `CRAFT.md` and `.craft/ledger.yml` remain intentionally intact: their canonical-graph gap
still includes schema promotion, projections, confirmation, compatibility, persistence and runtime
ingestion. The accepted work pack did not authorize collapsing that broader gap based on this
bounded compiler evidence.

## Next work

The next independently reviewed unit should consume this corpus to specify and promote the complete
canonical ExecutionGraph v2 boundary, including canonicalization authority, projectors/previews,
confirmation binding, CONF v1 compatibility, persistence, and runtime-ingestion contracts. Runtime
integration remains gated behind that work; it is not part of this closeout.
