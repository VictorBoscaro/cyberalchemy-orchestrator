# Mint — experiment harness (stub)

**Status:** stub. Full initialization is owned by the `experiment-harness` sigil (`--profile
sigil-development`) and is the next lifecycle step. This file records the harness plan + acceptance
checks so the build has a target before any template is written.

## Golden fixture
`resonantos-economy-research` (external sibling, `<repo-root>/../resonantos-economy-research/`) — the
hand-done precedent Mint reproduces. Emit-templates are reverse-engineered from it (WORK-PACK SWU-2),
domain content stripped; **no domain leakage** into the parameterized skeletons.

## Acceptance checks (from WORK-PACK SWUs)
| SWU | check | evidence |
|---|---|---|
| SWU-1 (L0) | minted tree resolves clone-safe | scaffolder Step-7 verify passes on a throwaway target |
| SWU-3 (L1) | emitted authority-model parses; every proposed kind has a default-deny row | run on the resonantos domain; reproduce its spine shape |
| **SWU-5 (#8)** | the seeded load-bearing-term rule resolves against an emitted `DRIFT-AUDIT` target | assert the rule's target file exists in the minted tree |
| **SWU-6 (#11)** | no minted kind left `PROPOSED` after ratify-CLOSE | run on fixture; grep for `PROPOSED` → none |
| **SWU-7 (#13)** | each proposed kind carries a methods stub | diff vs domainspec-v2's hand-authored methods catalogue |
| SWU-8 (seed-format) | each seeds the empty contract, **zero cav2 rows copied** | diff each skeleton vs its cav2 source; assert no populated rows |

## Reflection triggers (defaults)
Manual (owner asks); 5 meaningful mints; 10 emitted artifacts since last reflection; 3 related gaps;
1 severe gap (e.g., a mint leaves kinds `PROPOSED`, or copies cav2 rows). Report via a Mint-local
reflection report.

## Observability
On each mint, emit a post-run JSON signal (stages reached, kinds proposed/ratified, gates hit —
public/private, signer-capability, templates-pending — and any guardrail violation) via the repo-local
observability package (`observability-setup`). Not yet wired; part of the next build increment.

## Build order (Tier-1 first, per owner decision 2026-07-01)
SWU-2 (template set) → **SWU-5, SWU-6, SWU-7** (close live defects #8/#11/#13) → SWU-8/9 (seed-format +
meta batches, under the empty-format guardrail) → SWU-10 (cheap nav/schema). L2 (SWU-4/#11 signing)
waits on the attestation/signer capability.

## Build state (2026-07-01)
**BUILT (emit-logic):** all of SWU-2 + SWU-5..10 are authored as templates + `EMIT-PROCEDURE.md`
(Steps 1–12) at `cyberAlchemy-v2/development/mint/templates/`, statically validated against the acceptance
markers above (#8 void closed, #11 no-PROPOSED, seed-format zero-cav2-rows, in-place #1/#2/#5/#12/#7).
**NOT yet run:** the acceptance checks against a live emit — that is this harness's next job
(`experiment-harness`, golden fixture = resonantos / the worked example `examples/release-approval/`).
