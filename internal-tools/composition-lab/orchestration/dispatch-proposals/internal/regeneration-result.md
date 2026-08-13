# Regeneration result — internal comparative study of composition

## Verdict

**BLOCK**

The regenerated package is not launch-ready.

## Results

- **R1: FAIL (17/18).** The remaining golden fixture still contains the old hashes for the
  `current-checkout` sources.
- **R2: PASS (27/27).**
- `04-execution-sheet.md` was only partially regenerated: it now represents **35 sources** and
  **280 source × control obligations**, while the seat instructions still bind the earlier
  **22-source** corpus.
- `10-human-confirmation-sheet.md` and `11-human-gate-check.md` still represent **22 sources / 176
  obligations** and retain old hashes and digests.
- `launch-readiness.md`, the earlier R1 review, and other dependent records remain pending
  regeneration or continue to certify the superseded freeze.
- All **13 DomainSpec v2 artifacts** have correct paths, hashes, sizes, revision, and scoped-status
  metadata.

## Mutation boundary

This regeneration wrote nothing to:

- `.arcanum/inventory`;
- `.arcanum/observability`;
- `domainspec-core`.

The pre-existing change in `implementations/server/runtime/local_pilot.py` was not touched.

No dispatch was launched.

