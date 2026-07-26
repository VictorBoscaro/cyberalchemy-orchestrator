CREATE TABLE collection_closures(
  collection_closure_id TEXT PRIMARY KEY,
  group_aggregate_id TEXT NOT NULL,
  round_id TEXT NOT NULL,
  message_entries_json TEXT NOT NULL,
  frozen_set_hash TEXT NOT NULL,
  expected_seat_count INTEGER NOT NULL CHECK(expected_seat_count=2),
  received_seat_count INTEGER NOT NULL CHECK(received_seat_count>=0),
  quorum_status TEXT NOT NULL CHECK(quorum_status IN ('quorum','no_quorum')),
  closed_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
  closed_offset INTEGER NOT NULL UNIQUE REFERENCES events(journal_offset),
  UNIQUE(group_aggregate_id,round_id)
);

CREATE TABLE reveal_manifests(
  reveal_manifest_id TEXT PRIMARY KEY,
  group_aggregate_id TEXT NOT NULL,
  round_id TEXT NOT NULL,
  message_entries_json TEXT NOT NULL,
  manifest_hash TEXT NOT NULL,
  collection_closed_event_id TEXT NOT NULL REFERENCES events(event_id),
  reveal_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
  reveal_offset INTEGER NOT NULL UNIQUE REFERENCES events(journal_offset),
  UNIQUE(group_aggregate_id,round_id)
);

CREATE TABLE agent_invocation_plans(
  plan_ref TEXT PRIMARY KEY,
  plan_digest TEXT NOT NULL UNIQUE,
  binding_id TEXT NOT NULL UNIQUE REFERENCES host_workflow_turn_bindings(binding_id),
  attempt_id TEXT NOT NULL UNIQUE,
  operation_id TEXT NOT NULL UNIQUE,
  seat_id TEXT NOT NULL,
  group_aggregate_id TEXT NOT NULL,
  plan_json TEXT NOT NULL
);

CREATE TABLE materialized_agent_invocations(
  materialized_invocation_id TEXT PRIMARY KEY,
  attempt_id TEXT NOT NULL UNIQUE REFERENCES agent_attempts(attempt_id),
  plan_ref TEXT NOT NULL UNIQUE REFERENCES agent_invocation_plans(plan_ref),
  plan_digest TEXT NOT NULL,
  effective_input_artifact_id TEXT NOT NULL UNIQUE
    REFERENCES effective_input_artifacts(effective_input_artifact_id),
  provider_invocation_ref TEXT NOT NULL REFERENCES artifacts(artifact_id),
  adapter_wrapper_refs_json TEXT NOT NULL,
  materialization_json TEXT NOT NULL,
  materialization_digest TEXT NOT NULL UNIQUE
);

CREATE TABLE agent_request_bindings(
  request_binding_id TEXT PRIMARY KEY,
  request_id TEXT NOT NULL UNIQUE REFERENCES agent_execution_requests(request_id),
  materialized_invocation_id TEXT NOT NULL UNIQUE
    REFERENCES materialized_agent_invocations(materialized_invocation_id),
  effective_input_artifact_id TEXT NOT NULL UNIQUE
    REFERENCES effective_input_artifacts(effective_input_artifact_id)
);

CREATE TABLE peer_input_deliveries(
  peer_input_delivery_id TEXT PRIMARY KEY,
  reveal_manifest_id TEXT NOT NULL REFERENCES reveal_manifests(reveal_manifest_id),
  source_group_aggregate_id TEXT NOT NULL,
  source_round_id TEXT NOT NULL,
  target_attempt_id TEXT NOT NULL UNIQUE REFERENCES agent_attempts(attempt_id),
  target_seat_id TEXT NOT NULL,
  peer_message_entries_json TEXT NOT NULL,
  effective_input_artifact_id TEXT NOT NULL UNIQUE
    REFERENCES effective_input_artifacts(effective_input_artifact_id),
  effective_input_manifest_hash TEXT NOT NULL,
  visibility_policy_ref TEXT NOT NULL,
  idempotency_key TEXT NOT NULL,
  semantic_digest TEXT NOT NULL UNIQUE,
  accepted_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
  journal_offset INTEGER NOT NULL UNIQUE REFERENCES events(journal_offset),
  UNIQUE(reveal_manifest_id,target_attempt_id),
  UNIQUE(reveal_manifest_id,target_attempt_id,idempotency_key)
);

CREATE TABLE peer_input_delivery_receipts(
  peer_input_delivery_id TEXT PRIMARY KEY
    REFERENCES peer_input_deliveries(peer_input_delivery_id),
  receipt_bytes BLOB NOT NULL,
  receipt_digest TEXT NOT NULL UNIQUE
);
