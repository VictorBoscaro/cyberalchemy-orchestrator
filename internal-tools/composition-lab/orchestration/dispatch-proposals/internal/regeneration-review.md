# Independent regeneration review — internal comparative study of composition

## Verdict

**BLOCK**

The regeneration does not establish a coherent exact-run package. The DomainSpec v2 annex itself
is correctly represented, but the execution and confirmation chain still mixes the new 35-source
freeze with artifacts derived from the former 22-source freeze.

## Evidence reviewed

- R1 reports **FAIL (17/18)** because one golden fixture retains old hashes for the
  `current-checkout` sources.
- R2 reports **PASS (27/27)**.
- `04-execution-sheet.md` records **35 sources / 280 obligations**, but its seat instructions still
  cover only **22 sources**.
- `10-human-confirmation-sheet.md` and `11-human-gate-check.md` still record **22 sources / 176
  obligations** and old hashes or digests.
- `launch-readiness.md`, the prior R1 review, and other dependent records are either still pending
  regeneration or certify the superseded freeze.
- The **13 DomainSpec v2 artifacts** have correct paths, hashes, sizes, revision, and scoped status.

## Blocking rationale

The package cannot honestly claim one frozen corpus while its seat instructions, human gate,
digests, and dependent certifications refer to different corpus versions. R2's passing mechanics
and the correct DomainSpec v2 annex do not cure that inconsistency.

## Boundary confirmation

No writes from this regeneration occurred in `.arcanum/inventory`, `.arcanum/observability`, or
`domainspec-core`. The pre-existing modification to
`implementations/server/runtime/local_pilot.py` was not touched. No dispatch was launched.

