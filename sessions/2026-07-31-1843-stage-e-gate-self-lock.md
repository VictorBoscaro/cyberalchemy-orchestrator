---
tags: [stage-e-manifest, launch-gate, agent-policy, digest-attestation, source-drift]
artifact_kind: session
layer: project
version: 0.1.0
created_at: 2026-07-31T18:43:09-03:00
updated_at: 2026-07-31T18:43:09-03:00
expires: 2026-09-29
decisions_made: false
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 6
importance_rationale: "Refuted a live blocker claimed by the prior session and named the design defect behind it — the launch gate treats an ordinary policy edit as tampering and offers only blanket re-attestation as the exit."
---

# Stage-E launch gate self-lock and the blanket re-attestation exit

## Summary

The session opened as a request to report what the 2026-07-31-1659 provenance audit did, decided,
and left open, then narrowed to the hard block that audit named as its first next step. Tracing the
deny path established the mechanism: the `PreToolUse` hook matched to `Agent` runs the local-pilot
preflight, which verifies 47 files pinned in the Stage-E source manifest and converts any byte
divergence into a launch denial, with the manifest's own digest pinned as a constant in
`local_pilot.py`. The cause was that `AGENTS.md` and `CLAUDE.md` are byte-identical twins among
those 47 attested files, so appending the eight-line "Host wrapper binding" section to both at
15:46 denied every subsequent agent launch — editing the agent policy revoked the authority to
launch agents. Direct verification against disk then contradicted the audit's premise: the manifest
self-digest matches its pin and all 47 files match, because the block was repaired at 17:03 by
re-attesting both twins and bumping the manifest pin, after the audit node was written and outside
its record. The same re-attestation also advanced the pinned digest of
`implementations/server/runtime/service.py`, which the as-built drift record independently
classifies as an `unattributed_source_change` of unknown authorship inserting 43 lines, so the
repair blessed a change the gate exists to catch. The owner rejected the technical account and
asked for the product consequence, which was given as three points: the gate treats the most
routine act in this repository as an attack and fails closed with no partial service; its only exit
is a blanket "bless whatever is on disk now" with no granular consent, so every legitimate policy
edit launders unrelated drift along with it; and the blessed content of both twins is uncommitted,
so a fresh clone or a `git checkout` restores the `HEAD` form and re-denies every launch. Nothing
was changed this session — no document, no code, no manifest — and the finding is diagnostic only.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [docs/features/agent-provenance-telemetry/README.md](../docs/features/agent-provenance-telemetry/README.md) | `is-part-of` | The Stage-E source manifest and the launch gate that reads it are integration components of this feature; the session's whole subject was that gate's behavior. |
| [sessions/2026-07-31-1659-provenance-properties-audit.md](2026-07-31-1659-provenance-properties-audit.md) | `contradicts` | That node states the `AGENTS.md` digest mismatch as live and denying every `Agent` launch, and ranks clearing it first; verification shows the manifest self-digest matches its pin and all 47 attested files match, the block having been repaired at 17:03. |
| [implementations/as-built/source-drift-record.json](../implementations/as-built/source-drift-record.json) | `derives-from` | The claim that the repair laundered an unattributed change rests on this record's classification of the `service.py` delta as `unattributed_source_change` with authorship unknown. |

## Open questions

- Whether the `service.py` re-attestation was deliberate or incidental to fixing the twins. The
  drift record leaves authorship unknown and no author was identified this session.
- Whether pinning `AGENTS.md` and `CLAUDE.md` in the manifest was a considered scope choice or an
  artifact of sweeping the repository root. Nothing was read this session that states the intent,
  and that one choice is what converts a doc edit into a total launch outage.
- Whether any granular consent mechanism was ever considered — attesting one file without
  re-blessing the rest. Not checked.

## Next steps

1. Commit `AGENTS.md` and `CLAUDE.md`; the attested content exists only in the working tree, so the
   gate is one `git checkout` or one clone away from denying every launch again.
2. Resolve the authorship of the `service.py` delta before it stays blessed in the manifest.
3. Resume the audit node's own next steps, which the repaired gate no longer blocks.

## Recommendation

The keystone is the scoping question, not the commit. Committing the twins closes today's exposure
but leaves the mechanism intact: the next policy edit reproduces the outage, and the next repair
reproduces the laundering. Attack it by deciding whether policy documents belong in the same
attestation set as runtime code, because that single boundary is cheaper to move than a per-file
consent mechanism is to build, and moving it also removes the pressure that made the blanket
blessing attractive. This ranks above the `service.py` authorship question, which is a
one-off to settle rather than a defect that recurs.

## Files touched

- sessions/2026-07-31-1843-stage-e-gate-self-lock.md
