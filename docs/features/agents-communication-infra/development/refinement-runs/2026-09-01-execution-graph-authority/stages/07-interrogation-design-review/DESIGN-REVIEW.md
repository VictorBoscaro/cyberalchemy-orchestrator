# Design review and toy game

## Initial independent verdict

Both read-only roles returned `BLOCK` for treating the first draft as executable. They agreed the
authority/evidence boundary was correct and found concrete completeness defects:

- `correct` lacked the original target; `verify` lacked target and review inputs;
- validation, success and stop behavior depended on free-text interpretation;
- dataflow was duplicated between inputs and edge mappings;
- output schemas were refs without demonstrated content;
- topology/basic/full lacked executable projection vectors;
- credential version could be confused with rotating secret bytes; and
- the first repaired inline schemas required fields while forbidding them.

## Repair exchange

The design was repaired in place because it is still a proposal:

1. Node inputs now name every consumed value; `review → verify` is explicit.
2. Node input sources are the only data mappings; edges authorize/order communication.
3. Success/stop predicates are closed variants and validators are digest-pinned refs.
4. Command allowlists require exact command ref, argv, cwd and optional environment member; the toy
   denies commands.
5. Output/receipt schemas are inline content members with matching digests and witnessed valid
   instances.
6. `flag` and `block` transitions are both explicit.
7. Credential authority uses resolver ref + stable handle contract version + scope digest.
8. Exact topology/basic projections and a full identity-projection contract bind one graph digest.
9. The repaired toy advanced to `r2`, proving that repair itself is a material change.

## Toy-game results

| Check | Result |
|---|---|
| Proposal JSON Schema is a valid Draft 2020-12 schema | pass |
| Toy validates against proposal schema | pass |
| Unique IDs and cross-referenced node/output/member/root/terminal targets | pass |
| All inline content digests match exact UTF-8 content | pass |
| Minimal valid instances pass all four embedded output/receipt schemas | pass |
| Topology and basic match the prescribed deterministic selection | pass |
| Full projection is lossless identity over graph value | pass |
| All views bind full graph digest | pass: `sha256:4a38e63293f630930cb624830433dea147bdb018f3ceb7eef949dafe052cd275` |

The placeholder hashes used for provider/model/profile/validator/projector refs intentionally make
this a **contract toy**, not an executable golden fixture.

## Remaining non-blocking residue

- Formalize and implement the semantic validator used by the inline proof.
- Replace placeholder refs with real immutable artifacts in specification golden vectors.
- Specify exact `@2` confirmation observation/envelope shapes and persistence migration.
- Independently review the accepted specification, not only this refinement proposal.
