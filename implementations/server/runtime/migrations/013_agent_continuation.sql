CREATE TABLE runtime_agent_attempts(
  attempt_id TEXT PRIMARY KEY,
  dispatch_id TEXT NOT NULL REFERENCES confirmed_dispatches(dispatch_id),
  graph_id TEXT NOT NULL REFERENCES confirmed_turn_graphs(graph_id),
  aggregate_id TEXT NOT NULL UNIQUE,
  operation_id TEXT NOT NULL,
  seat_id TEXT NOT NULL,
  agent_instance_id TEXT NOT NULL,
  turn_ordinal INTEGER NOT NULL CHECK(turn_ordinal>=0),
  state TEXT NOT NULL CHECK(state IN ('requested','starting','running','completed')),
  version INTEGER NOT NULL CHECK(version BETWEEN 1 AND 4),
  requested_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
  last_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
  last_offset INTEGER NOT NULL UNIQUE REFERENCES events(journal_offset),
  CHECK(
    (state='requested' AND version=1) OR
    (state='starting' AND version=2) OR
    (state='running' AND version=3) OR
    (state='completed' AND version=4)
  )
);

CREATE INDEX runtime_agent_attempts_source_idx
ON runtime_agent_attempts(dispatch_id,graph_id,operation_id,seat_id,turn_ordinal,state);

CREATE TABLE runtime_attempt_snapshot_bindings(
  attempt_id TEXT PRIMARY KEY REFERENCES runtime_agent_attempts(attempt_id),
  artifact_id TEXT NOT NULL UNIQUE REFERENCES artifacts(artifact_id),
  content_hash TEXT NOT NULL,
  terminal_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
  terminal_offset INTEGER NOT NULL UNIQUE REFERENCES events(journal_offset),
  bound_at TEXT NOT NULL
);

CREATE TABLE agent_continuations(
  continuation_id TEXT PRIMARY KEY REFERENCES confirmed_turn_graphs(continuation_id),
  dispatch_id TEXT NOT NULL REFERENCES confirmed_dispatches(dispatch_id),
  graph_id TEXT NOT NULL REFERENCES confirmed_turn_graphs(graph_id),
  confirmed_authority_digest TEXT NOT NULL,
  source_attempt_id TEXT NOT NULL UNIQUE REFERENCES runtime_agent_attempts(attempt_id),
  source_turn_ordinal INTEGER NOT NULL CHECK(source_turn_ordinal>=0),
  target_turn_ordinal INTEGER NOT NULL CHECK(target_turn_ordinal=source_turn_ordinal+1),
  seat_id TEXT NOT NULL,
  agent_instance_id TEXT NOT NULL,
  context_snapshot_artifact_id TEXT NOT NULL REFERENCES artifacts(artifact_id),
  context_snapshot_content_hash TEXT NOT NULL,
  provider_continuation_ref_digest TEXT,
  resume_policy_ref_json TEXT NOT NULL,
  deadline_utc TEXT NOT NULL,
  state TEXT NOT NULL CHECK(state='suspended'),
  version INTEGER NOT NULL CHECK(version=1),
  suspended_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
  suspended_offset INTEGER NOT NULL UNIQUE REFERENCES events(journal_offset)
);

CREATE TABLE agent_continuation_mapping_members(
  continuation_id TEXT NOT NULL REFERENCES agent_continuations(continuation_id),
  mapping_id TEXT NOT NULL REFERENCES continuation_input_mappings(mapping_id),
  member_ordinal INTEGER NOT NULL CHECK(member_ordinal IN (0,1)),
  awaited INTEGER NOT NULL CHECK(awaited=1),
  confirmed_binding_digest TEXT NOT NULL,
  PRIMARY KEY(continuation_id,member_ordinal),
  UNIQUE(continuation_id,mapping_id)
);
