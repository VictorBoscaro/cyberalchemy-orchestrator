# Refine result — canonical ExecutionGraph authority

Status: `pass_for_specification`; `code_entry_blocked`

## Conclusion

The selected decision is the best current boundary, with one necessary precision:

> A single canonical JSON contains every value that determines what execution is authorized to
> do. The confirmation observation and facts created during execution remain separate evidence or
> state and bind back to that JSON's digest.

This keeps the owner's product model intact: the agent compiles the dispatch, the user confirms it,
and topology/basic/full are views of the same complete authority. It avoids the impossible claim
that a pre-execution proposal already contains who confirmed it, when it was confirmed, future
attempts, receipts or results.

## Proposed contract

The proposed `aci.execution-graph@2` contains logical dispatch identity/revision, objective,
digest-pinned semantics/content, exact per-node instructions and agent/provider/model/profile,
tools, inputs/outputs, limits, isolation/effects, structured validation/stop predicates, typed
edges, lifecycle and audit requirements.

It deliberately excludes its own digest, trusted principal/channel/time, accepted command/envelope
IDs, journal positions, runtime graph/run/attempt/message/effect IDs, status, receipts and results.

## What was tested

- Two independent roles attacked completeness and the runtime boundary.
- The first design was blocked for hidden inputs and free-text control semantics.
- The repaired design was blocked again for impossible embedded output schemas.
- Revision `r2` repaired those schemas and both reviewers returned `PASS`.
- JSON Schema/meta-schema, semantic references, content hashes, valid output witnesses and
  topology/basic/full binding all pass for the toy.

These checks validate internal proposal coherence only. They do not prove production execution.

## Recommended next step

Run `SPEC-ACI-EXECUTION-GRAPH-V2-001`:

1. write the canonical v2 spec and all closed graph/view/observation/command/envelope contracts;
2. build real golden and negative vectors with deterministic semantic/projector validation;
3. obtain independent PASS;
4. update the ledger at that exact specification ceiling; and
5. only then authorize a separate compiler/projector code unit.

Do not modify runtime code yet. The proposed layering is spec → conformance package →
compiler/preview → confirmation `@2` → execution integration.

## Primary artifacts

- Definition: `stages/02-invoke-define/DEFINITION.md`
- Boundary selection: `stages/05-distill/SELECTION.md`
- Architecture/schema: `stages/06-invoke-design/`
- Toy/review/projections: `stages/07-interrogation-design-review/`
- Repair validation: `stages/08-distill-repair/validation.md`
- Implementation plan/work pack: `stages/09-invoke-plan/`
- Final interrogation: `stages/10-final-interrogation/FINAL-INTERROGATION.md`

## Residue

- The installed Invoke package lacked `define.md`, `design.md` and `plan.md`; available local
  DomainSpec, architecture, layering and work-pack templates were used and the gap is recorded.
- Provider/model/validator/projector refs in the toy are placeholders, so it is not a production
  golden fixture.
- No feature spec, fixture, ledger entry or runtime code was changed by this run.
