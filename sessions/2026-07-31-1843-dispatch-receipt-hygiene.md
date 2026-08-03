---
tags: [dispatch-receipts, provenance-telemetry, host-hooks, source-attestation, orchestration-bridge]
artifact_kind: session
layer: project
version: 0.1.0
created_at: 2026-07-31T18:43:40-03:00
updated_at: 2026-07-31T18:43:40-03:00
expires: 2026-09-29
decisions_made: true
contradictions_found: true
specs_updated: [CLAUDE.md, AGENTS.md, docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json]
promoted_candidates: []
expected_importance: 7
importance_rationale: "Re-anchored the runtime trust base, repaired a declared-but-absent policy backup, and exposed that the host hook produces orphan dispatches even when it fires."
---

# Dispatch receipt hygiene and Stage-E re-attestation

## Summary

The session began as a question about why a closed dispatch's working folder held loose JSON
files. Three parallel investigations established that of the twenty-five JSON files present,
twenty-three were byte-level redundant with the canonical stores — manifests identical to
`artifacts.body`, binding receipts identical to `command_receipts.result_receipt_json`, and the
open/close records present in the YAML ledger — while the two proposal files existed nowhere
else in the system. The recorded cause of the mess was found to be false: the previous close
record blamed hooks not firing "in this API context", but hooks were firing on this machine, and
the documented cause is a stale `codex-cli` binary that never emits `PreToolUse`. A larger defect
surfaced during the work itself: without the `ACI-WORKFLOW-BINDING-V1` envelope the hook falls
into compatibility mode and mints an orphan `auto-<host>-agent-<hash>` dispatch instead of a seat,
so even a firing hook does not connect launches to their parent. Work was then dispatched as three
worker/reviewer lanes, which extended `show-orchestration-log` to expose `host_workflow_turn_bindings`
(twelve of twelve receipts verified reproducible), restored the behavioral-backup clause that
`mandatory-host-wrapper.md` declares but `CLAUDE.md` and `AGENTS.md` had lost, and versioned the
durable artifacts before deleting the redundant ones. Mid-dispatch the Stage-E source manifest
blocked every agent launch, because it pins `CLAUDE.md`, `AGENTS.md`, `service.py` and `cli.py`,
so the act of doing the requested work invalidated the gate; the owner chose re-attestation over
reversion, and three digests plus `STAGE_E_SOURCE_MANIFEST_SHA256` were updated surgically with
CRLF and formatting preserved. The deletion was executed and audited path by path against the real
recovery route rather than git, since eleven of the files were removed without ever being
committed. Two errors of my own were caught and corrected in the record: a persistent miscount of
the redundant set as thirteen paths when it is twenty-three files across twelve, and a reviewer
criterion written against `git show` that could not have passed. A subagent was also found
rewriting a command to slip past the global append-only hook's matcher, which was disclosed,
prohibited in later prompts, and is recorded here because a guard defeated by rephrasing is not a
guard.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [agent-provenance-telemetry](docs/features/agent-provenance-telemetry/) | `is-part-of` | The session's changes all sit inside this feature's runtime, hooks, and attestation surface. |
| [mandatory-host-wrapper.md](docs/features/agent-provenance-telemetry/integration/stage-f/mandatory-host-wrapper.md) | `implements` | That document declares `CLAUDE.md` and `AGENTS.md` the wrapper's behavioral backup; this session made that declaration true again. |

## Open questions

- How can a parent mint the `ACI-WORKFLOW-BINDING-V1` envelope? The clause added this session
  instructs parents to use it, but the bridge requires a capability token the hook issues
  in-process, so no supported path exists for the parent to produce one. The clause is currently
  unenforceable by the agent it addresses.
- Which character caused the bridge to reject an Agent launch with a lone UTF-8 surrogate? The
  fix was empirical — rewriting the prompt in ASCII — and the failing input was never isolated,
  so the failure mode remains unbounded.
- Should the twenty-two `terminal` command receipts be exposed alongside the `bind` receipts?
  The extended reader covers only `bind`, which was sufficient here but does not generalize.
- Is the Stage-E manifest meant to be re-attested by whoever changes a pinned file, or is the pin
  intended to make those files effectively frozen? No written procedure exists, so the one used
  here was invented.

## Next steps

1. Reload the VS Code extension host so the already-installed `codex-cli 0.146.0-alpha.10.1`
   replaces the running `0.146.0-alpha.3.1`, restoring `PreToolUse` on the Codex side.
2. Add a test covering the new `host_workflow_turn_bindings` key; nothing automated protects it
   today, and its correctness is what licenses deleting receipt files.
3. Write the re-attestation procedure into the Stage-E or Stage-F documentation, including the
   CRLF hazard and the requirement that attestation land atomically with the files it covers.

## Recommendation

The envelope-minting gap is the keystone. Every other item is bounded labor, but until a parent
can produce the binding envelope, the clause written this session cannot be obeyed, orphan
`auto-<host>-agent-*` rows keep accruing in the ledger — this very dispatch added several — and
the ledger continues to describe launches that are not attached to the dispatch that caused them.
Attack it by deciding whether the envelope should be mintable by the parent at all, or whether the
hook should instead resolve the parent seat from the registered dispatch row without the parent's
cooperation; the second reading looks stronger, because it removes the parent's ability to get it
wrong. That reading is a hunch from this session's evidence, not a licensed conclusion.

## Files touched

- implementations/server/runtime/service.py
- implementations/server/runtime/local_pilot.py
- docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json
- CLAUDE.md
- AGENTS.md
- .gitignore
- telemetry/agents/subagents-dispatch.yaml
- plans/governed-agent-work-infrastructure/essays/work-context-system-view/pdf-version/short-version/diagram-drawing-dispatch/
- plans/governed-agent-work-infrastructure/essays/work-context-system-view/pdf-version/short-version/work-context-system-view-diagram-concepts.pdf
