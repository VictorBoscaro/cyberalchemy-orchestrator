# Validation — SPEC-ACI-DRAFT-GRAPH-001

Date: 2026-09-01

Status: artifact checks pass; dedicated Recheck 3 returned aggregate `KEEP` for the frozen proposal
corpus. The review does not expand the evidence ceiling below.

## Reproducible artifact check

Executed from the repository root:

```powershell
python docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/followups/SPEC-ACI-DRAFT-GRAPH-001/validate_artifacts.py
```

Result: exit code `0`.

```text
PASS schemas, context and duplicate-key parsing: 7 JSON files
PASS fixture digests: 5 resources and 10 catalog records
PASS exact full-collection draft+context+fixtures to expected-EG mapping
PASS F1 regressions: author identity/revision rejected; stale system context rejected
PASS F2 regressions: 30k/24k rejected; safe restriction report exact
PASS F3 regressions: 17 extra/missing/duplicate authority mutations rejected
PASS F4 regressions: failure-as-success and optional-output success rejected
PASS F5 regression: command allowlist/argv/cwd/environment tuple rejected structurally
PASS R1 regression: work-pack inputs, N01-N24 outcomes and KEEP/FIX gate synchronized
PASS R2 regressions: missing pointer and enum-invalid value rejected in draft and emitted EG
PASS S1 regressions: typeless/nullable object/array ancestors rejected symmetrically
PASS remaining negative preconditions and F6 non-controlling done_when ownership
PASS field-ownership inventory: 105 of 105 schema leaves
EVIDENCE LIMIT: no compiler, live allocator or RFC 8785 canonicalizer executed
```

The script performs only artifact/conformance assertions. It does not emit an ExecutionGraph,
canonical bytes or a digest and is not compiler/runtime code.

## Checks performed

- Draft schema passes `Draft202012Validator.check_schema`.
- Positive draft validates against the closed draft schema.
- Current proposed ExecutionGraph schema passes its meta-schema check.
- Expected ExecutionGraph validates against that proposed schema.
- All seven local JSON files parse with duplicate-key rejection.
- Five inline resource digests match exact encoded content.
- Ten catalog reference digests match their explicit fixture `digest_source` bytes.
- Draft aliases, node-local keys, resource bindings and producer/output references resolve uniquely.
- Agent tuples, capabilities, validators, paths, network/effects/VCS and budgets are admitted by the
  explicit policy without authority expansion.
- The frozen system compilation context, not the DraftGraph, supplies dispatch identity/revision;
  obsolete author identity fields and stale contexts are rejected.
- The full expected graph is compared as one exact structure, including cardinality, ordered nested
  collections, lifecycle and audit requirements. No non-strict truncating comparison remains.
- Seventeen persistent mutations prove extra, missing and duplicate node/tool/input/output/rule/
  stop/command-grant authority plus lifecycle/audit drift is rejected.
- Post-policy budget checks prove the reviewed 30k reservation fails against the 24k global limit,
  while the safe restriction produces one exact external report record.
- Failure-as-success, optional-output success and all command allowlist tuples are rejected.
- Positive `/verdict=pass|flag|block` predicates resolve through the exact bound verification schema;
  N19 missing-pointer and N20 enum-invalid-value attacks are rejected on both draft and emitted-EG
  semantic paths.
- N21-N24 validate scalar/null counterexamples against typeless and nullable object/array ancestor
  schemas, then prove both draft and emitted-EG traversal reject them as unprovable.
- The `done_when` ownership row is checked as non-controlling and does not name validators.
- Work-pack inspection requires exactly five compiler inputs, vectors N01-N24, DG-N09 failure,
  DG-N11 safe restriction and aggregate `KEEP`/artifact `FIX` gate vocabulary.
- The ownership document contains the complete extracted inventory of all 105 leaf paths in the
  current proposed ExecutionGraph schema.

## Write-scope check

Executed:

```powershell
$target = 'docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/followups/SPEC-ACI-DRAFT-GRAPH-001'
Get-ChildItem -LiteralPath $target -Recurse -File | Sort-Object FullName
git status --short -- $target
```

Result: all produced files were under `$target`; Git reported only that target directory as
untracked. Preexisting modifications to feature `CRAFT.md`, `.craft/ledger.yml` and unrelated files
were not changed by this worker.

## Evidence ceiling

These checks prove internal structural coherence of the proposal and fixtures. They do **not** prove:

- that a compiler can reproduce the expected EG;
- that a live allocator issued or verified the fixture compilation context;
- byte-for-byte equivalence with the earlier toy graph;
- RFC 8785 / `aci-cjson-1` canonical bytes or digest;
- production catalog, policy, resource or credential resolution; command resolution is deliberately
  unsupported in DraftGraph v1;
- canonical v2 acceptance, projection, confirmation, persistence or runtime execution; or
- the exact typed compiler error/postcondition behavior in `NEGATIVE-VECTORS.md`.

Those claims were outside this specification validation. Independent review later returned
aggregate `KEEP`, and the bounded successor compiler/conformance SWU was implemented and reviewed
separately; canonical-v2 and runtime claims remain open.
