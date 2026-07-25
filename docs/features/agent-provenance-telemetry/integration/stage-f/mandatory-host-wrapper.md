# Stage F - Mandatory Claude and Codex host wrapper

Status: implemented for trusted project-local Claude Code and Codex sessions.

## Contract

Every host Agent-tool call is independently recoverable. Two launch modes are supported:

1. Compatibility mode derives a deterministic Dispatch identity from host, Session, and tool-use
   identity.
2. Bound-workflow mode receives a digest-bound envelope for one group/seat/turn under an already
   confirmed parent Dispatch. It persists the internal binding without appending another YAML
   Dispatch row.

Both modes then follow the common fail-closed lifecycle:

1. `PreToolUse(Agent|spawn_agent|followup_task)` validates the launch mode and exact tool input.
2. The hook writes a preparing state under the ignored local runtime directory.
3. Stage-C preflight verifies the dedicated database, exact ledger, pinned source set, profiles,
   journal, and projection.
4. The hook issues an expiring operation-specific capability bound to the exact generated record.
5. Compatibility mode opens the validated YAML/ACI Dispatch. Bound mode verifies that its parent
   is still open, validates the declared seat, prompt/template, input manifest and source hashes,
   then accepts `host_workflow.turn_bound@1`.
6. Only `status=launch-authorized` allows the host tool call. Any exception returns a structured
   `deny`.
7. Compatibility completion appends the exact YAML close and accepts
   `orchestration.dispatch_closed@1`. Bound completion accepts
   `host_workflow.turn_terminal@1`; the parent closes only after no bound turn remains running.
   Codex correlates asynchronous launches using the agent ID returned by `PostToolUse` and closes
   on `SubagentStop`.
8. `SessionEnd` reconciles remaining open states as `user_abort`.

The state file is written before the bridge opening so a process failure after a YAML or ACI side
effect retains enough information for an exact retry. A reused tool-use identity with different
input is denied. A tool-use identity that already closed cannot launch another agent.

## Host wiring

- Claude Code: `.claude/settings.json`
- Codex: `.codex/hooks.json`
- Shared launcher: `.claude/hooks/host-dispatch-hook.py`
- Shared implementation: `implementations/server/runtime/host_dispatch_hook.py`
- Standing owner policy: `host-hook-policy.json`
- Behavioral backup: `CLAUDE.md` and `AGENTS.md`

Claude uses `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `Stop`, and `SessionEnd`.
Synchronous Agent calls close at `PostToolUse`; `Stop` reconciles any remaining lifecycle and
blocks the parent from stopping when reconciliation fails. Background calls close as `user_abort`
when their parent stops if the host does not provide exact completion correlation.

Codex uses `PreToolUse`, `PostToolUse`, `SubagentStop`, and `SessionEnd`. A running result must
contain an `agent_id`; otherwise the lifecycle fails visibly.

Both hosts also run the Stage-G ingestion adapter after supported read, search, web, MCP, and shell
tools. Exact repository reads become immutable input artifacts. Search/web/MCP operations record
metadata-only lineage, while shell execution is explicitly recorded as opaque rather than
misrepresented as complete file provenance.

## Bound workflow envelope

The first prompt line is `ACI-WORKFLOW-BINDING-V1:` followed by URL-safe base64 JSON. The envelope
strictly declares the parent `dispatch_id`, `group_id`, zero-based `seat_index`, `turn_ordinal`,
`attempt_id`, prompt-template path/digest, and workflow-manifest path/digest. The remaining prompt
body must equal the confirmed initial prompt for turn zero or the frozen UTF-8 template for a
follow-up.

The `aci-workflow-input-manifest/v1` file targets the same seat/turn and contains ordered,
cardinality-bounded, size-bounded data slots. Every source is repository-relative and carries its
exact SHA-256 and byte size. A `binding-output` source additionally names a terminal producer
binding from the same parent Dispatch. Unbound `followup_task` calls are denied.

This is a host-observable compatibility binding. It does not claim to capture hidden provider or
system inputs and is not a complete `EffectiveInputArtifact`.

## Compatibility classification

Schema v0.6.1 has no generic host-agent dispatch type and keeps `code`, `plan`, and `suggestion`
reserved. Automatic host calls therefore use a disclosed `review`/`inline` compatibility envelope.
The concrete role and full initial prompt remain in `groups[].agents[]`. This avoids silently
activating reserved ontology while keeping every call in the existing validated ledger.

## Enforcement boundary

Within an active project hook layer, launch is fail-closed even when the host permission mode would
otherwise allow the Agent tool. The bridge database and ledger are mandatory dependencies.

Repository code cannot force a client to load repository hooks:

- Codex loads project hooks only for a trusted project and requires the exact hook definition to be
  reviewed/trusted. Users can otherwise disable non-managed hooks. Organization-wide
  non-disableable enforcement requires an administrator-managed `requirements.toml` with hooks
  pinned on and the script deployed through the managed directory.
- Claude Code must load the checked-in project settings. A user who removes or ignores project
  settings is outside this repository enforcement boundary.
- Hosted agent surfaces that do not execute local lifecycle hooks are not covered.

The checked-in wrapper is therefore mandatory for supported trusted local Claude/Codex execution,
not an assertion of control over clients that refuse project configuration.

## Recovery

- A denied opening means no Agent call was authorized. Repair the reported integrity, database,
  ledger, policy, or source problem and retry the exact tool call.
- An `opened` state without a close is reconciled by the exact completion hook or Session end.
- A `preparing` state is safe to retry; YAML and journal idempotency converge partial openings.
- Never delete hook state to bypass the bridge. Inspect it together with the corresponding
  `show-orchestration-log` result.

The verified implementation hashes, test matrix, fail-closed smoke result, and exact offsets
generated by the controlled Codex hook-wire lifecycle are recorded in `execution-receipt.md`.
