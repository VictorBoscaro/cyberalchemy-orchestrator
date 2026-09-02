# Work pack — IMPL-ACI-DRAFT-COMPILER-CONFORMANCE-001

Status: `COMPLETE_REVIEW_KEEP`; predecessor gate passed and the bounded implementation received its
own dedicated aggregate `KEEP`

## Work unit

- ID: `IMPL-ACI-DRAFT-COMPILER-CONFORMANCE-001`
- Kind: bounded compiler implementation plus conformance harness
- Goal: implement the reviewed `DraftGraph -> ExecutionGraph` transformation and prove exact positive
  and negative behavior without runtime ingestion, confirmation, scheduling or effects.
- Entry gate: an independent reviewer must return aggregate `KEEP` on
  `SPEC-ACI-DRAFT-GRAPH-001`; any surviving artifact `FIX` blocks entry and must be repaired and
  rechecked first. This is the complete review-to-gate mapping; `PASS/BLOCK/FLAG` are not used here.
- Code authority: the predecessor gate passed with review SHA-256
  `E70B8D68CC426BF9E5F64B6ADD37BE2867F9864AE76BCC4DED8B30D54B2F3D94`; the bounded implementation
  write scope recorded in the successor `TASK-SESSION.md` was assigned and completed.

## Inputs after the gate

- reviewed DraftGraph schema;
- reviewed frozen compilation-context contract and fixture;
- reviewed field-ownership matrix and compilation contract;
- exactly five positive compiler inputs: frozen compilation context, DraftGraph, policy, catalog and
  resources; plus the expected ExecutionGraph as output oracle;
- reviewed negative vectors and typed error taxonomy;
- current proposed ExecutionGraph schema only as a predecessor artifact, not as accepted canonical
  v2 authority.

## Required outputs

1. Closed JSON Schemas for compilation context, policy, catalog and resource inputs.
2. Trusted allocator-context entry gate plus pure compiler with duplicate-key rejection,
   exact-key resolution and no execution-runtime choices/lookups.
3. Semantic validator for uniqueness, references, contracts, predicates, topology, lifecycle,
   budgets and monotone authority.
4. RFC 8785 / proposed `aci-cjson-1` canonicalization adapter and digest reproduction.
5. Positive conformance test that structurally reproduces
   `review-correct-verify.expected.execution.json` from the five input fixtures.
6. Negative runner for every `DG-N01` through `DG-N24`, including exact error paths and no-output
   postconditions.
7. Determinism test across clean processes and shuffled object-key input encodings.
8. Independent implementation review receipt and a separate recommendation about whether the
   result is ready to feed the canonical v2 specification SWU.

## Acceptance criteria

- Identical logical inputs yield identical logical EG, canonical bytes and digest.
- Draft input cannot supply or override dispatch identity/revision; stale/reserved-pair conflicts
  produce the exact reviewed typed errors.
- Every EG field is traceable to one field-ownership row and one source class.
- No unknown/ambiguous key or duplicate identifier is repaired or defaulted.
- Numeric restriction is monotone and externally reported; permission is never injected or widened.
- Positive output exactly equals the expected fixture structurally and validates against the target
  EG schema and semantic validator.
- `DG-N09` returns `DG_GLOBAL_BUDGET_EXCEEDED` for effective 30k/24k and emits no graph.
- `DG-N11` is the only safe numeric-restriction vector: it succeeds with the exact external
  restriction-report object while effective node totals remain within the global limit.
- All other negative vectors return their exact typed failure and emit no graph
  bytes/digest/state mutation.
- Compiler code has no provider/tool call, confirmation write, runtime scheduling or external effect.
- DraftGraph v1 rejects command allowlists and every argv/cwd/environment tuple; command admission
  remains a future specification unit, not an implementation inference.

## Stop conditions

- Independent review of this predecessor returns any artifact `FIX` or aggregate `FIX`.
- RFC 8785 cannot satisfy the proposed `aci-cjson-1` requirements without a product/spec change.
- A field needs a runtime lookup or nondeterministic choice.
- A policy transformation can widen the draft request.
- The expected EG cannot be reproduced without changing an inherited product decision.
- Implementation location, public API or error contract cannot be bounded without a new decision.

## Non-goals

- Promotion of `aci.execution-graph@2` to canonical status.
- Topology/basic/full projector implementation.
- Confirmation `@2`, persistence migration or CONF v1 compatibility changes.
- Runtime parser, scheduler, worker, provider/tool/credential invocation or external effects.
- CRAFT/ledger updates before independently reviewed evidence exists.

## Required review pairing

The implementation worker must have one dedicated reviewer who did not author the implementation.
The work unit is not complete until that reviewer is joined and returns durable aggregate `KEEP`;
any `FIX` blocks. A reviewer
finding that changes product authority, view semantics or canonicalization returns to specification;
it must not be decided opportunistically in code.

Closeout: the dedicated implementation reviewer completed Recheck 3 with aggregate `KEEP`; see
`../IMPL-ACI-DRAFT-COMPILER-CONFORMANCE-001/review.md` and its bounded `CLOSEOUT.md`. This completes
only the fixture-backed compiler/conformance work unit and does not promote canonical v2 or admit
runtime ingestion.
