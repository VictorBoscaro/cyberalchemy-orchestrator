CREATE TABLE confirmation_observations(
  issuer_ref_json TEXT NOT NULL,
  observation_id TEXT NOT NULL,
  observation_artifact_id TEXT NOT NULL UNIQUE REFERENCES artifacts(artifact_id),
  observation_digest TEXT NOT NULL,
  issuer_evidence_ref TEXT NOT NULL,
  issuer_evidence_digest TEXT NOT NULL,
  human_principal_id TEXT NOT NULL,
  channel TEXT NOT NULL CHECK(channel IN ('chat','ui')),
  observed_at TEXT NOT NULL,
  dispatch_id TEXT NOT NULL,
  dispatch_revision TEXT NOT NULL,
  presented_pending_sheet_digest TEXT NOT NULL,
  presented_dispatch_spec_digest TEXT NOT NULL,
  action TEXT NOT NULL CHECK(action='approve_runtime_dispatch'),
  PRIMARY KEY(issuer_ref_json,observation_id)
);

CREATE TABLE confirmed_dispatches(
  dispatch_id TEXT PRIMARY KEY,
  dispatch_revision TEXT NOT NULL,
  pending_sheet_artifact_id TEXT NOT NULL REFERENCES artifacts(artifact_id),
  pending_sheet_digest TEXT NOT NULL,
  dispatch_spec_artifact_id TEXT NOT NULL REFERENCES artifacts(artifact_id),
  dispatch_spec_digest TEXT NOT NULL,
  confirmation_observation_artifact_id TEXT NOT NULL
    REFERENCES artifacts(artifact_id),
  confirmation_observation_digest TEXT NOT NULL,
  capability_resolution_artifact_id TEXT NOT NULL REFERENCES artifacts(artifact_id),
  capability_resolution_digest TEXT NOT NULL,
  confirmed_turn_graph_artifact_id TEXT NOT NULL REFERENCES artifacts(artifact_id),
  confirmed_turn_graph_digest TEXT NOT NULL,
  continuation_mapping_set_artifact_id TEXT NOT NULL REFERENCES artifacts(artifact_id),
  continuation_mapping_set_digest TEXT NOT NULL,
  confirmed_authority_artifact_id TEXT NOT NULL REFERENCES artifacts(artifact_id),
  confirmed_authority_digest TEXT NOT NULL,
  execution_authority_mode TEXT NOT NULL CHECK(execution_authority_mode='runtime-managed'),
  confirmed_by TEXT NOT NULL,
  confirmed_at TEXT NOT NULL,
  accepted_command_id TEXT NOT NULL UNIQUE
    REFERENCES command_receipts(command_id) DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE runs(
  run_id TEXT PRIMARY KEY,
  dispatch_id TEXT NOT NULL UNIQUE REFERENCES confirmed_dispatches(dispatch_id),
  dispatch_spec_digest TEXT NOT NULL,
  aggregate_version INTEGER NOT NULL CHECK(aggregate_version=2),
  state TEXT NOT NULL CHECK(state='opening_pending'),
  state_hash TEXT NOT NULL,
  opening_state TEXT NOT NULL CHECK(opening_state='pending'),
  terminal_event_id TEXT REFERENCES events(event_id)
);

CREATE TABLE confirmed_turn_graphs(
  graph_id TEXT PRIMARY KEY,
  dispatch_id TEXT NOT NULL UNIQUE REFERENCES confirmed_dispatches(dispatch_id),
  run_id TEXT NOT NULL UNIQUE REFERENCES runs(run_id),
  dispatch_spec_digest TEXT NOT NULL,
  graph_artifact_id TEXT NOT NULL UNIQUE REFERENCES artifacts(artifact_id),
  graph_digest TEXT NOT NULL,
  continuation_id TEXT NOT NULL UNIQUE,
  mapping_set_artifact_id TEXT NOT NULL UNIQUE REFERENCES artifacts(artifact_id),
  mapping_set_digest TEXT NOT NULL,
  node_count INTEGER NOT NULL CHECK(node_count=3),
  edge_count INTEGER NOT NULL CHECK(edge_count=2),
  mapping_count INTEGER NOT NULL CHECK(mapping_count=2),
  nodes_json TEXT NOT NULL,
  edges_json TEXT NOT NULL,
  source_messages_json TEXT NOT NULL,
  source_operation_id TEXT NOT NULL,
  source_seat_id TEXT NOT NULL,
  source_turn_ordinal INTEGER NOT NULL CHECK(source_turn_ordinal=0),
  target_operation_id TEXT NOT NULL,
  target_seat_id TEXT NOT NULL,
  target_turn_ordinal INTEGER NOT NULL CHECK(target_turn_ordinal=1),
  identity_derivation_ref_json TEXT NOT NULL
);

CREATE TABLE continuation_input_mappings(
  mapping_id TEXT PRIMARY KEY,
  mapping_version INTEGER NOT NULL CHECK(mapping_version=1),
  dispatch_id TEXT NOT NULL REFERENCES confirmed_dispatches(dispatch_id),
  continuation_id TEXT NOT NULL REFERENCES confirmed_turn_graphs(continuation_id),
  source_group_id TEXT NOT NULL,
  source_seat_id TEXT NOT NULL,
  source_operation_id TEXT NOT NULL,
  source_turn_ordinal INTEGER NOT NULL CHECK(source_turn_ordinal>=0),
  source_round_id TEXT NOT NULL,
  source_message_id TEXT NOT NULL UNIQUE,
  source_message_type TEXT NOT NULL CHECK(source_message_type IN ('author.output','reviewer.output')),
  target_seat_id TEXT NOT NULL,
  target_turn_ordinal INTEGER NOT NULL CHECK(target_turn_ordinal=1),
  slot_name TEXT NOT NULL CHECK(slot_name IN ('prior_author_output','review_feedback')),
  slot_ordinal INTEGER NOT NULL CHECK(slot_ordinal IN (0,1)),
  visibility_policy_ref_json TEXT NOT NULL,
  confirmed_binding_digest TEXT NOT NULL,
  UNIQUE(dispatch_id,slot_ordinal),
  UNIQUE(dispatch_id,slot_name)
);

CREATE TABLE effect_intents(
  effect_id TEXT PRIMARY KEY,
  command_id TEXT NOT NULL
    REFERENCES command_receipts(command_id) DEFERRABLE INITIALLY DEFERRED,
  requested_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
  effect_type TEXT NOT NULL CHECK(effect_type='audit_opening'),
  payload_ref TEXT NOT NULL REFERENCES artifacts(artifact_id),
  payload_digest TEXT NOT NULL,
  retry_class TEXT NOT NULL CHECK(retry_class IN ('retryable','non_retryable')),
  status TEXT NOT NULL CHECK(status IN ('pending','claimed','succeeded','failed','unknown')),
  claim_epoch INTEGER,
  claimed_by TEXT,
  attempt_count INTEGER NOT NULL CHECK(attempt_count>=0),
  outcome_event_id TEXT REFERENCES events(event_id),
  outcome_digest TEXT,
  CHECK((claim_epoch IS NULL)=(claimed_by IS NULL)),
  CHECK((outcome_event_id IS NULL)=(outcome_digest IS NULL)),
  CHECK(status!='pending' OR (claim_epoch IS NULL AND claimed_by IS NULL AND attempt_count=0 AND outcome_event_id IS NULL AND outcome_digest IS NULL))
);

CREATE INDEX effect_intents_pending_idx ON effect_intents(status,effect_type);
