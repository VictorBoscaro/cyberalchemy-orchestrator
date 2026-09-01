CREATE TABLE runtime_attempt_result_acceptances(
  acceptance_id TEXT PRIMARY KEY,
  mapping_id TEXT NOT NULL UNIQUE REFERENCES continuation_input_mappings(mapping_id),
  source_message_id TEXT NOT NULL UNIQUE REFERENCES continuation_input_mappings(source_message_id),
  dispatch_id TEXT NOT NULL REFERENCES confirmed_dispatches(dispatch_id),
  run_id TEXT NOT NULL REFERENCES runs(run_id),
  graph_id TEXT NOT NULL REFERENCES confirmed_turn_graphs(graph_id),
  group_id TEXT NOT NULL,
  group_version INTEGER NOT NULL CHECK(group_version=1),
  group_aggregate_id TEXT NOT NULL,
  attempt_id TEXT NOT NULL UNIQUE REFERENCES runtime_agent_attempts(attempt_id),
  candidate_id TEXT NOT NULL UNIQUE REFERENCES publication_candidates(candidate_id),
  publication_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
  publication_receipt_event_id TEXT NOT NULL UNIQUE REFERENCES publication_receipts(event_id),
  official_message_id TEXT NOT NULL UNIQUE REFERENCES messages(message_id),
  attempt_result_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
  official_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
  accepted_offset INTEGER NOT NULL UNIQUE REFERENCES events(journal_offset),
  parent_principal_id TEXT NOT NULL,
  semantic_digest TEXT NOT NULL UNIQUE,
  FOREIGN KEY(graph_id,group_id,group_version)
    REFERENCES runtime_group_heads(graph_id,group_id,group_version),
  CHECK(source_message_id=official_message_id)
);
