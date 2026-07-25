CREATE TABLE agent_attempts(
  attempt_id TEXT PRIMARY KEY,
  host_workflow_binding_id TEXT NOT NULL UNIQUE
    REFERENCES host_workflow_turn_bindings(binding_id),
  dispatch_id TEXT NOT NULL REFERENCES dispatch_links(dispatch_id),
  operation_id TEXT NOT NULL UNIQUE,
  seat_id TEXT NOT NULL,
  agent_instance_id TEXT NOT NULL,
  provider_ref TEXT NOT NULL,
  adapter_ref TEXT NOT NULL,
  model_ref TEXT NOT NULL,
  effective_input_artifact_id TEXT NOT NULL UNIQUE REFERENCES artifacts(artifact_id),
  request_digest TEXT NOT NULL,
  state TEXT NOT NULL CHECK(state='requested'),
  requested_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
  requested_offset INTEGER NOT NULL UNIQUE REFERENCES events(journal_offset)
);

CREATE INDEX agent_attempts_dispatch_idx
ON agent_attempts(dispatch_id,seat_id,agent_instance_id);

CREATE TABLE effective_input_artifacts(
  effective_input_artifact_id TEXT PRIMARY KEY REFERENCES artifacts(artifact_id),
  attempt_id TEXT NOT NULL UNIQUE REFERENCES agent_attempts(attempt_id),
  manifest_hash TEXT NOT NULL,
  entries_json TEXT NOT NULL,
  entry_count INTEGER NOT NULL CHECK(entry_count>=0)
);

CREATE TABLE agent_execution_requests(
  request_id TEXT PRIMARY KEY,
  attempt_id TEXT NOT NULL UNIQUE REFERENCES agent_attempts(attempt_id),
  effective_input_artifact_id TEXT NOT NULL UNIQUE
    REFERENCES effective_input_artifacts(effective_input_artifact_id),
  request_digest TEXT NOT NULL UNIQUE,
  sealed_at TEXT NOT NULL
);

CREATE TABLE sandbox_launch_effects(
  effect_id TEXT PRIMARY KEY,
  attempt_id TEXT NOT NULL UNIQUE REFERENCES agent_attempts(attempt_id),
  request_id TEXT NOT NULL UNIQUE REFERENCES agent_execution_requests(request_id),
  state TEXT NOT NULL CHECK(state='pending'),
  created_at TEXT NOT NULL
);

CREATE TABLE agent_reference_deliveries(
  agent_reference_delivery_id TEXT PRIMARY KEY,
  dispatch_id TEXT NOT NULL REFERENCES dispatch_links(dispatch_id),
  scout_run_id TEXT NOT NULL REFERENCES reference_scout_runs(scout_run_id),
  source_bundle_delivered_event_id TEXT NOT NULL REFERENCES events(event_id),
  bundle_artifact_id TEXT NOT NULL REFERENCES artifacts(artifact_id),
  bundle_digest TEXT NOT NULL,
  recommendation_ids_json TEXT NOT NULL,
  target_attempt_id TEXT NOT NULL REFERENCES agent_attempts(attempt_id),
  target_seat_id TEXT NOT NULL,
  target_agent_instance_id TEXT NOT NULL,
  effective_input_artifact_id TEXT NOT NULL
    REFERENCES effective_input_artifacts(effective_input_artifact_id),
  effective_input_entry_ordinal INTEGER NOT NULL
    CHECK(effective_input_entry_ordinal>=0),
  effective_input_manifest_hash TEXT NOT NULL,
  visibility_policy_ref TEXT NOT NULL,
  idempotency_key TEXT NOT NULL,
  accepted_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
  journal_offset INTEGER NOT NULL UNIQUE REFERENCES events(journal_offset),
  UNIQUE(scout_run_id,target_attempt_id),
  UNIQUE(scout_run_id,target_attempt_id,idempotency_key)
);

CREATE INDEX agent_reference_deliveries_target_idx
ON agent_reference_deliveries(target_attempt_id,journal_offset);
