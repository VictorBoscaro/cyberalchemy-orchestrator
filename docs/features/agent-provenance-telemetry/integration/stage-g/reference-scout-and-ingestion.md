# Stage G - Operational Reference Scout and dispatch ingestion

Status: implemented for the local pilot.

## Reference Scout lifecycle

The authoritative ACI runtime now owns the small, single-seat Reference Scout lifecycle:

1. `scout.start/bootstrap` verifies the current Session, Dispatch link, open orchestration
   lifecycle, registered compatibility profile, and exact capability-bound intent.
2. The start event and `reference_scout_runs` row commit atomically with the publish, verify,
   commit, deliver, and terminate capabilities. An exact start retry reissues lost plaintext
   capabilities without creating another ScoutRun.
3. The agent publishes each recommendation through the existing append-before-ack bus.
   `message_type=reference_scout:<recommendation_id>` prevents the bus logical key from collapsing
   distinct recommendations.
4. The parent verifies the publication receipt. Only the official message becomes a
   `reference_recommendations` row.
5. Commit derives the bundle from the ordered accepted recommendations and stores it as an
   immutable artifact. The caller cannot assert the bundle digest.
6. Delivery makes the bundle terminal. Failure or cancellation uses the explicit termination
   path.
7. A Dispatch cannot close while one of its ScoutRuns is requested, collecting, or committed.

The implemented HTTP surface under `/api/runtime` is:

- `POST /scouts`
- `POST /bus/publications`
- `POST /bus/publications/verify`
- `POST /scouts/{scout_run_id}/commit`
- `POST /scouts/{scout_run_id}/deliver`
- `POST /scouts/{scout_run_id}/terminate`
- `GET /scouts/{scout_run_id}`

The active operational shape is `small`. The `tensioned` value remains a target-schema value but
is rejected by the service until a multi-seat provider adapter and reveal policy are implemented.

## Dispatch input ingestion

Claude and Codex `PostToolUse` hooks now attribute supported input operations to exactly one open
wrapped Dispatch:

| Tool class | Recorded evidence | Coverage |
|---|---|---|
| Exact repository file read or image view | repository-relative path, immutable input artifact, SHA-256, media type, size, event and offset | `exact` |
| Repository search | query digest and tool identity | `metadata_only` |
| Web or MCP acquisition | observed locator and tool identity | `metadata_only` |
| Shell execution | command-input digest and explicit uncertainty | `opaque` |

The hook never infers individual file reads from an arbitrary shell process. Exact provenance
requires the instrumented read path. Outside-repository file capture is denied.

Each input has its own `aci.dispatch-ingestion:<ingestion_id>` aggregate, so ingestion events cannot
advance the fixed two-event orchestration aggregate and break Dispatch closing. The event and
artifact commit atomically; exact retries converge, while changed bytes under the same identity
fail closed.

The Dispatch lineage query is:

`GET /api/runtime/dispatches/{dispatch_id}/lineage`

It returns the Session link, ScoutRuns, accepted recommendations, ingestions, and research captures.
The read verifies the journal, event artifacts, exact input artifacts, and Scout bundle before
returning.

## Host wiring

- Claude configuration: `.claude/settings.json`
- Codex configuration: `.codex/hooks.json`
- Launcher: `.claude/hooks/host-ingestion-hook.py`
- Shared adapter: `implementations/server/runtime/host_ingestion_hook.py`
- Authoritative service: `implementations/server/runtime/service.py`
- Ordered migration: `008_reference_scout_ingestion.sql`

## Boundary

This makes the Scout state machine, bus, recovery, API, persistence, and provenance queries
operational in the local pilot. A generic provider launcher or native MCP tool that automatically
hands the publish capability to an external Scout model is still a separate adapter/cutover task.
No external-network or production authority is granted.
