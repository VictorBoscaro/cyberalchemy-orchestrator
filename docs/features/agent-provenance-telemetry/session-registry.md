---
feature: agent-provenance-telemetry
artifact: coarse-session-registry
status: proposed
version: 0.4.0
created: 2026-07-23
last_updated: 2026-07-23
---

# Coarse session registry

## Purpose

Create the coarsest durable parent for orchestration telemetry:

```text
session
  ├─ dispatch
  │    ├─ group
  │    │    └─ seat
  │    │         └─ attempt
  │    │              └─ activation / tool operation
  │    ├─ reference-scout (dispatch_bound)
  │    │    └─ recommendations[]
  │    └─ research
  │         └─ question / answer / reference use / problem / claim / formalization
  └─ reference-scout (session_direct)
       └─ recommendations[]
```

The first dataset does not reproduce transcripts, prompts or agent outputs. It gives later telemetry
a stable session identity and permits simple questions such as “how did this work start?”, “what is
it currently called?” and “how many dispatches descended from it?”.

A runtime Session is not the same thing as a curated Markdown document under `sessions/`, and it is
not a host Conversation. A Conversation, CLI command, scheduled job or API request can originate a
Session through an opaque `origin_kind`/`origin_ref`; that reference does not copy the Conversation,
make their identities equal or authorize transcript storage.

The first storage cut contains no prompt, message, response, chain of thought or raw conversation
body. Compression and masking are deferred rather than silently approximated.

## Ensure, do not duplicate

Any orchestration, Scout or Probe tool begins by calling an idempotent `ensure_session` boundary:

- if the current execution context already has `session_id`, reuse it;
- otherwise create one `session.started` fact using a host-minted opaque ID;
- require an `ensure_key` stable for the originating execution context, so concurrent/retried
  ensures return the same session and receipt;
- every later skill/tool call inherits that ID;
- using another skill does not create another session.

This is “always register the session when the skill is used” without producing one session per skill
invocation.

Starting unrelated work is intentional. An authorized human or host calls
`start_new_session(rollover_operation_id, expected_current_session_id, new_ensure_key)`. After the
validated append boundary atomically commits `session.started` and `session.context_rebound` in one
journal operation. A concurrent rollover from the same predecessor conflicts before either fact is
visible; an identical retry returns the same new session and receipt. A storage adapter that cannot
commit the pair atomically is not conformant. This rollover does not end, mutate or delete the
previous session, and the context-binding fact never becomes session identity.

```json
{
  "event_type": "session.context_rebound",
  "context_ref": "conversation:conversation-01",
  "expected_current_session_id": "session-01",
  "successor_session_id": "session-02",
  "rollover_operation_id": "operation:rollover-02",
  "rebound_at": "2026-07-23T04:30:00Z"
}
```

## Minimal facts

The authoritative first cut is append-only:

```json
{
  "event_type": "session.started",
  "session_id": "session-01",
  "origin_kind": "conversation",
  "origin_ref": "conversation:conversation-01/turn:turn-07",
  "ensure_key": "ensure:<opaque-context-key>",
  "start_operation_id": "operation:<opaque-id>",
  "started_at": "2026-07-23T03:15:43Z",
  "name": "Agent provenance and Reference Scouts"
}
```

A changing name is a later fact, not an edit of history:

```json
{
  "event_type": "session.name_changed",
  "session_id": "session-01",
  "changed_at": "2026-07-23T04:10:00Z",
  "name": "Reference Scout bus and hierarchical session telemetry"
}
```

Dispatch attachment is likewise append-only:

```json
{
  "event_type": "session.dispatch_linked",
  "session_id": "session-01",
  "dispatch_id": "2026-07-23-probe-bus-slice",
  "linked_at": "2026-07-23T04:12:00Z"
}
```

## Current projection

The rebuildable coarse dataset exposes:

| field | source |
|---|---|
| `session_id` | `session.started` |
| `origin_kind`, `origin_ref` | `session.started` |
| `started_at` | `session.started` |
| `current_name` | latest valid start/name-change fact |
| `dispatch_count` | distinct linked dispatch IDs |
| `last_activity_at` | latest session-linked fact |

Later projections may add group, seat, attempt, ScoutRun, ProbeRun and reference counts without changing the
original facts.

The structured research child is defined by
[`discovery/session-dispatch-research-records.md`](discovery/session-dispatch-research-records.md).
`session.dispatch_linked` is the sole authority for Session→Dispatch. Research carries
`ResearchCapture.dispatch_id`; therefore session and dispatch research counts are projections over
those two edges. Neither the dispatch ledger nor research facts duplicate `session_id`,
`research_refs`, answers or formalizations.

A Reference Scout has exactly one mandatory Session parent and one of two derived launch modes:

- `dispatch_bound`: `dispatch_id` is present and its sole `session.dispatch_linked` edge resolves to
  the same `session_id`;
- `session_direct`: `dispatch_id` is null and the authorized host/root launches bounded
  reconnaissance directly from the Session.

The second mode is conversationally an “orphan Scout” only with respect to Dispatch; it is never
orphaned from Session. `launch_mode` is derived from `dispatch_id`, not caller-authored.
Recommendations are the Scout run's ordered/identified output collection (`recommendations[]`);
their normalized projection rows do not create a new orchestration level.

If later research arises from a recommendation, the research dispatch/artifact records the
originating `scout_run_id` and recommendation identity. `ScoutRun` is the canonical operational
concept. Frozen v1 lineage may retain `probe_id` and `probe.*` event names as compatibility
identifiers, but they do not denote a second entity.

`ReferenceScoutTool` is the capability an agent invokes; `ScoutRun` is the Session-owned execution
record. In a separate family, `ProbeTool` (pt-BR UI: **Sonda**) creates a `ProbeRun` that requires a
`lens_ref` and owns `observations[]`. Scout recommendations identify paths to inspect, whereas Probe
observations state what a lens observed. Neither becomes a fact automatically, and the shared
Session/optional-Dispatch shape does not make Scout a subtype of Probe.

## Naming

The initial name is a short host-generated description of the opening objective. It is a display
label, not identity. The host may propose a more representative name as the conversation changes;
renaming appends `session.name_changed` and never changes `session_id`.

Names must not contain secrets or pretend to be user-authored. Repeated names are valid.

## Coarse invariants

- one `session.started` fact per `session_id`;
- one `session.started` fact per `ensure_key`; retry returns the original append receipt;
- an inherited session ID is reused across skill invocations;
- only authorized `start_new_session` may replace the current context session;
- rollover requires `expected_current_session_id`; a second successor from the same binding
  conflicts under compare-and-swap;
- a dispatch links to at most one session unless an explicit future cross-session relation is added;
- `session.dispatch_linked` is the only persisted Session→Dispatch join;
- duplicate `session.dispatch_linked` retries do not increment the count;
- projection replay yields the same current name and dispatch count;
- missing origin detail remains explicit rather than inferred from timestamps or similar names;
- Markdown session notes may reference `session_id` but do not define runtime identity.

## First storage cut

Use the same append-before-ack journal/bus authority selected for the Reference Scout slice and build
a small read projection for UI/telemetry. Do not create an independently editable YAML registry that
would become a second source of truth.

The isolated [experimental runtime E0](specs/experimental-runtime-l0.md) may use SQLite to prove
this rule. Its journal events and receipts are the experimental authority; `sessions` and
`session_dispatch_links` are rebuildable projections. It is shadow-only, writes no dispatch YAML
and does not lift the ACI mutation gate.

## Connections

| Document | Type | Description |
|---|---|---|
| [Session–Dispatch–Research records](discovery/session-dispatch-research-records.md) | `grounds` | Supplies start-time session identity to the three-level provenance spine. |
| [Feature discovery](discovery.md) | `refines` | Provides the detailed session contract summarized by the feature discovery. |

## Appendix — Changelog

| Version | Date | Change |
|---|---|---|
| 0.4.0 | 2026-07-23 | Separates Session from Conversation, forbids transcript storage in E0, adopts Reference Scout product naming and links the shadow-only SQLite proof. |
| 0.3.0 | 2026-07-23 | Adds ensure idempotency, authorized session rollover and a single authoritative Session→Dispatch edge. |
| 0.2.0 | 2026-07-23 | Added Research as a dispatch child projection while preserving session fact ownership. No decision in this document is locked by a SPEC. |
