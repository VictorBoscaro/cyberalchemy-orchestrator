# Review — DomainSpec v2 corpus amendment

Targets:

- `corpus-manifest.md`
- `../../../../../research/internal-composition-uses/dispatch-proposal.md`
- the prior 22-source execution and human-confirmation freeze

## Coverage

| attacker | lens | target coverage | findings raised | zero-findings defence |
|---|---|---|---:|---|
| independent reviewer | corpus integrity / launch readiness | Entire amendment, all 13 source rows, affected proposal, and prior exact-freeze surfaces | 1 MAJOR | Not applicable |

The reviewer recomputed every listed SHA-256 and byte count against
`C:/Users/victo/domainspec-core`, checked repository revision and branch, and checked scoped worktree
status for all 13 paths. The review also tested whether the amendment introduced substantive
research or prematurely adjudicated composition, and whether the earlier execution and human
confirmation freeze remained valid.

## `corpus-manifest.md`

All 13 paths exist. Every listed SHA-256 and byte count matches the inspected file. The source
repository revision is `9bfec22712e4675d39c4cf1c21b36dc66614136c`, the branch is `master`, and
the scoped status for the 13 paths is clean.

No substantive composition finding was introduced. The manifest states: “This annex locates
candidate evidence. It does not claim that any listed artifact realizes composition, that the list
is a taxonomy, or that DomainSpec v2 supplies a general theory.”

**Verdict:** KEEP

## Affected freeze and confirmation surfaces

| # | file | evidence | severity | proposed fix |
|---|---|---|---|---|
| 1 | `corpus-manifest.md`; prior execution and human-confirmation sheets | The amendment states: “Adding it changes the future corpus denominator and therefore requires regeneration and review of any exact row count, obligation count, partition, prompt, corpus digest or human confirmation sheet derived from the earlier single-checkout corpus.” The affected sheets still bind the earlier 22-source corpus, 41 hash rows, and 176 obligations. | MAJOR | Regenerate the corpus manifest, partitions, control denominator, obligation count, execution sheet, human-confirmation sheet, hashes and digests; rerun affected fixture checks and independently reaudIT before any launch decision. |

The finding is accepted. The amendment is **adopted-for-redesign**, not launch-ready. Prior
mechanical PASS results and documentary KEEP results remain historical evidence only for the
superseded freeze.

**Verdict:** FIX

## Change requests

1. MAJOR — Regenerate and independently review every exact-run surface derived from the earlier
   22-source denominator before seeking exact-run confirmation or launch authorization.

## Close

- `state`: adopted-for-redesign
- `launch_readiness`: BLOCK
- `inventory_bootstrap`: BLOCK — Inventory ownership and the bounded-bootstrap lifecycle gap remain
  unresolved; the corpus amendment does not remove either blocker.
- `exit_reason`: resolved review — the amendment is accepted as redesign input while its impact on
  the stale execution freeze remains an explicit required change.
- `agents_spawned`: 1 — one independent reviewer; no subagents spawned by this reviewer.
