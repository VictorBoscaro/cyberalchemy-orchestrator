CREATE TABLE host_workflow_turn_bindings(
  binding_id TEXT PRIMARY KEY,
  dispatch_id TEXT NOT NULL REFERENCES dispatch_links(dispatch_id),
  session_id TEXT NOT NULL REFERENCES sessions(session_id),
  parent_row_digest TEXT NOT NULL,
  group_id TEXT NOT NULL,
  seat_index INTEGER NOT NULL CHECK(seat_index>=0),
  turn_ordinal INTEGER NOT NULL CHECK(turn_ordinal>=0),
  attempt_id TEXT NOT NULL UNIQUE,
  host TEXT NOT NULL CHECK(host IN ('claude','codex')),
  operation_kind TEXT NOT NULL CHECK(operation_kind IN ('spawn','followup')),
  prompt_template_digest TEXT NOT NULL,
  workflow_manifest_artifact_id TEXT NOT NULL REFERENCES artifacts(artifact_id),
  workflow_manifest_hash TEXT NOT NULL,
  source_artifact_ids_json TEXT NOT NULL,
  tool_input_digest TEXT NOT NULL,
  host_session_id TEXT NOT NULL,
  tool_use_id TEXT NOT NULL,
  agent_id TEXT,
  state TEXT NOT NULL CHECK(
    state IN ('running','resolved','error','cancelled')
  ),
  bound_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
  terminal_event_id TEXT UNIQUE REFERENCES events(event_id),
  bound_at TEXT NOT NULL,
  terminal_at TEXT,
  UNIQUE(dispatch_id,group_id,seat_index,turn_ordinal),
  UNIQUE(host,host_session_id,tool_use_id),
  CHECK((terminal_event_id IS NULL)=(terminal_at IS NULL)),
  CHECK(state='running' OR terminal_event_id IS NOT NULL)
);

CREATE INDEX host_workflow_turn_bindings_dispatch_idx
ON host_workflow_turn_bindings(dispatch_id,group_id,seat_index,turn_ordinal);

CREATE INDEX host_workflow_turn_bindings_agent_idx
ON host_workflow_turn_bindings(host,host_session_id,agent_id);
