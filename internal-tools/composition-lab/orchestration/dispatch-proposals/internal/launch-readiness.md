# Launch readiness — internal comparative study of composition

## Decision

**C — REAUDIT / REGENERATE FOR THE NEW CORPUS. Do not execute.**

The user-required DomainSpec v2 annex materially changes the denominator. The former exact-run
package binds 22 sources, 176 source × control obligations, and a 41-row corpus/fixture hash check.
The proposed annex adds 13 exact sources from the sibling `domainspec-core` checkout. It therefore
invalidates every derived corpus count, partition, prompt binding, corpus digest, coverage
obligation, and human confirmation that assumes the earlier single-checkout freeze.

This is not dynamic expansion of the old run. The existing execution contract explicitly forbids
dynamic corpus expansion and says any corpus difference requires a revised sheet and new human
confirmation.

## Evidence checked

- `domainspec-v2/corpus-manifest.md` contains 13 rows under `projects/domainspec-v2/`.
- All 13 paths exist in `C:/Users/victo/domainspec-core`; their current sizes and SHA-256 values
  match the annex.
- `domainspec-core` HEAD matches the annex revision
  `9bfec22712e4675d39c4cf1c21b36dc66614136c`; the 13 selected paths are clean even though the
  surrounding checkout is dirty.
- The annex correctly treats DomainSpec v2 as a private internal-ecosystem source, not external
  literature, and forbids copying its prose to public Arcanum surfaces.
- The amended internal proposal preserves the descriptive Inventory boundary: it does not define
  composition, promote DomainSpec claims, or perform substantive extraction.
- `04-execution-sheet.md`, `10-human-confirmation-sheet.md`, and
  `11-human-gate-check.md` remain evidence for the superseded 22-source freeze only. In particular,
  the prior 41-row check cannot certify the 13 new source rows.
- R1 and R2 fixture PASS results remain useful evidence for their generic mechanics, but they do
  not validate a regenerated corpus package or authorize execution.

An independent readiness reviewer reached the same result: **C — REAUDIT / REGENERATE**.

## Required next preparation

Before another human gate can be presented, a delegated preparer must:

1. adopt and review the 13-source annex as part of one complete frozen corpus;
2. regenerate the execution sheet, complete manifest, source/control denominator, partitions,
   prompts, corpus digest, counts, and all derived hashes;
3. regenerate the human confirmation sheet and its independent gate check;
4. rerun the applicable R1/R2 mechanical checks against the regenerated exact-run material and
   complete the remaining required reviews;
5. present fresh reuse, owner/design, exact-run, and later launch decisions without carrying
   forward any stale approval.

## Remaining blocker

The new corpus does not resolve the previously recorded Inventory lifecycle/bootstrap problem.
The bounded Inventory-owned workflow, canonical ownership/binding/close path, exact mutation
allowlists, recovery ownership, and human choices must still be ratified. Consequently there is no
exact human gate ready now and no launch authority.

No Inventory, observability, skill, registry, runtime, or `domainspec-core` content was mutated by
this readiness review.
