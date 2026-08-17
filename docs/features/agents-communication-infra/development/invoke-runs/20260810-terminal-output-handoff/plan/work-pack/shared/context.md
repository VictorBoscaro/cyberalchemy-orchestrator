# Shared execution context

## Objective

Make a confirmed sequential research dispatch executable without fabricating future handoffs or weakening producer attribution.

## Source contracts

- `../../../ARCHITECTURE.md` — accepted exact-response architecture and TOH witnesses.
- `../../../CONTEXT.md` — D1/D2 and evidence boundary.
- `../../../DESIGN-TRANSPORT.md` — L0/L1 scope and connected-topology fence.
- `../../../../../../specs/operations.md#commithostterminalresponse` — normative byte-commit operation.
- `../../../../../../specs/rules.md` — exact-response launch invariant.
- `../../../../../../../agent-provenance-telemetry/integration/stage-f/mandatory-host-wrapper.md` — bounded host binding.
- `../../../../../../../../../implementations/server/runtime/service.py` — current SQLite/artifact owner.
- `../../../../../../../../../implementations/server/runtime/host_dispatch_hook.py` — host lifecycle adapter.
- `../../../../../../../../../implementations/server/runtime/dispatch_workflow.py` — compiler fence.

## New host evidence

Codex CLI 0.146 returns completed agent final answers through the host-owned `collaboration.list_agents` tool result. This observation does not yet prove that `PostToolUse.tool_response` is canonical, complete or untruncated. HTR-000 must first capture the real hook payload and freeze/test the UTF-8 byte rule for Unicode, newlines, limits, ambiguity and unknown schemas. The adapter may consume only that proven host field.

## Constraints

- No repository path may substitute for terminal-response bytes.
- No migration or parallel architecture package without a newly proven need.
- Source-manifest and local-pilot digest closure are part of every source-changing unit.
- Existing unrelated worktree changes remain untouched.
