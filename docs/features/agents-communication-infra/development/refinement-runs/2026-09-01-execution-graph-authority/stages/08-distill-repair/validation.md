# Distill repair validation

## Verdict

`PASS` for the refinement design; `BLOCK` for implementation until specification promotion. The
selected single-authority unit survives recomposition after the independent objections and toy
repairs.

## Repaired invariants

- One graph revision supplies every logical executable value.
- Observation, calculated digest and runtime state remain outside and bind the graph.
- Runtime interpretation of control/validation does not depend on arbitrary phrases.
- Every consumed node input has an explicit authority-bound source.
- Dataflow ownership is not duplicated.
- Every output/receipt schema used by the toy is exact content in the same graph JSON.
- Every presentation is a deterministic projection of the same graph digest.
- Repair changed revision/digest; it did not pretend the old confirmation remained valid.

## Deterministic evidence

The local validation performed:

1. Draft 2020-12 meta-schema check of `execution-graph-v2.proposed.schema.json`.
2. Toy validation against that schema.
3. Inline SHA-256 checks for all five content members.
4. Minimal valid-instance checks for review, correction, verification and receipt schemas.
5. Uniqueness/reference checks for nodes, edges, members, inputs, outputs, roots and terminals.
6. Exact projector comparison for topology/basic and identity proof for full.

Results:

- `PROPOSAL_SCHEMA=pass`
- `TOY_STRUCTURAL_AND_SEMANTIC=pass`
- `INLINE_CONTENT_DIGESTS=pass`
- `OUTPUT_SCHEMA_WITNESSES=pass`
- `THREE_PROJECTIONS_ONE_DIGEST=pass`
- graph digest: `sha256:4a38e63293f630930cb624830433dea147bdb018f3ceb7eef949dafe052cd275`
- topology view digest: `sha256:f0cb9120c5bd53bd53897d213085687cc16289c13d38baebf12f72494096df62`
- basic view digest: `sha256:c7b0bbed9808eaa7d93de46cc1cf70ea03fc838cacfca22484e201fee8725a6b`

## Recomposition proof

Agent compilation produces one graph; canonicalization produces its external digest; projection
produces a chosen view; trusted observation activates that digest; acceptance derives and persists
runtime state. Removing any one component either removes authority, proof of approval or
operational materialization, but none becomes a competing logical plan.

## Boundary result

The original owner decision is **kept with a precise boundary**:

> one JSON contains all information that can determine what the runtime is authorized to do; the
> confirmation observation and facts produced by execution are separate evidence/state that cite
> the JSON digest.

The claim “one JSON contains every lifecycle fact” is rejected as temporally impossible.

## Promotion residue

- Accepted v2 prose/spec and closed semantic validator contract.
- Real golden refs and negative vectors.
- `aci.execution-graph-view@2`, confirmation observation/envelope and command schemas.
- CONF v1 coexistence/cutover and database/service migration.
- Independent spec review before code entry.
