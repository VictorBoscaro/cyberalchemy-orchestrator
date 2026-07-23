CREATE TABLE command_receipts(
  command_id TEXT PRIMARY KEY,
  scope_key TEXT NOT NULL,
  idempotency_key TEXT NOT NULL,
  command_digest TEXT NOT NULL,
  aggregate_id TEXT NOT NULL,
  expected_version INTEGER NOT NULL CHECK(expected_version>=0),
  status TEXT NOT NULL CHECK(status='accepted'),
  result_receipt_json TEXT NOT NULL,
  first_offset INTEGER NOT NULL,
  last_offset INTEGER NOT NULL,
  event_count INTEGER NOT NULL CHECK(event_count>0),
  ordered_event_ids_json TEXT NOT NULL,
  ordered_payload_digest TEXT NOT NULL,
  artifact_ids_json TEXT NOT NULL,
  recorded_at TEXT NOT NULL,
  UNIQUE(scope_key,idempotency_key),
  CHECK(last_offset-first_offset+1=event_count)
);

CREATE TABLE events(
  journal_offset INTEGER PRIMARY KEY AUTOINCREMENT,
  event_id TEXT NOT NULL UNIQUE,
  aggregate_type TEXT NOT NULL,
  aggregate_id TEXT NOT NULL,
  aggregate_version INTEGER NOT NULL CHECK(aggregate_version>0),
  event_type TEXT NOT NULL,
  schema_ref TEXT NOT NULL,
  schema_digest TEXT NOT NULL,
  canonicalizer_profile_id TEXT NOT NULL,
  canonicalizer_profile_version TEXT NOT NULL,
  canonicalizer_profile_digest TEXT NOT NULL,
  command_id TEXT NOT NULL,
  event_ordinal INTEGER NOT NULL CHECK(event_ordinal>=0),
  event_count INTEGER NOT NULL CHECK(event_count>0),
  group_digest TEXT NOT NULL,
  causation_id TEXT NOT NULL,
  correlation_id TEXT NOT NULL,
  recorded_at TEXT NOT NULL,
  observed_at TEXT,
  payload_ref TEXT NOT NULL,
  payload_hash TEXT NOT NULL,
  authority_context_json TEXT NOT NULL,
  authority_context_digest TEXT NOT NULL,
  UNIQUE(aggregate_id,aggregate_version),
  UNIQUE(command_id,event_ordinal),
  CHECK(event_ordinal<event_count)
);
CREATE INDEX events_command_idx ON events(command_id);
CREATE INDEX events_aggregate_idx ON events(aggregate_id,aggregate_version);
CREATE INDEX events_correlation_idx ON events(correlation_id);

CREATE TABLE aggregate_heads(
  aggregate_id TEXT PRIMARY KEY,
  aggregate_type TEXT NOT NULL,
  current_version INTEGER NOT NULL CHECK(current_version>=0),
  state_hash TEXT NOT NULL,
  last_event_id TEXT,
  last_offset INTEGER,
  reducer_version TEXT NOT NULL
);

CREATE TABLE runtime_projections(
  projection_name TEXT NOT NULL,
  projection_key TEXT NOT NULL,
  value_json TEXT NOT NULL,
  state_hash TEXT NOT NULL,
  last_offset INTEGER NOT NULL CHECK(last_offset>=0),
  PRIMARY KEY(projection_name,projection_key)
);

CREATE TABLE publication_candidates(
  candidate_id TEXT PRIMARY KEY,
  message_id TEXT NOT NULL UNIQUE,
  publication_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
  group_aggregate_id TEXT NOT NULL,
  seat_id TEXT NOT NULL,
  round_id TEXT NOT NULL,
  message_type TEXT NOT NULL,
  attempt_id TEXT NOT NULL,
  operation_id TEXT NOT NULL,
  payload_ref TEXT NOT NULL,
  payload_hash TEXT NOT NULL,
  idempotency_key TEXT NOT NULL,
  receipt_bytes BLOB NOT NULL,
  receipt_digest TEXT NOT NULL,
  journal_offset INTEGER NOT NULL UNIQUE REFERENCES events(journal_offset),
  status TEXT NOT NULL CHECK(status IN ('active','officially_accepted','abandoned')),
  candidate_version INTEGER NOT NULL CHECK(candidate_version>=1),
  official_accepted_event_id TEXT REFERENCES events(event_id),
  abandoned_event_id TEXT REFERENCES events(event_id),
  CHECK(NOT(official_accepted_event_id IS NOT NULL AND abandoned_event_id IS NOT NULL)),
  CHECK(status!='officially_accepted' OR official_accepted_event_id IS NOT NULL),
  CHECK(status!='abandoned' OR abandoned_event_id IS NOT NULL)
);
CREATE UNIQUE INDEX one_active_candidate_per_logical_key
ON publication_candidates(group_aggregate_id,seat_id,round_id,message_type)
WHERE status='active';

CREATE TABLE publication_receipts(
  event_id TEXT PRIMARY KEY REFERENCES events(event_id),
  message_id TEXT NOT NULL UNIQUE,
  scope_key TEXT NOT NULL,
  idempotency_key TEXT NOT NULL,
  payload_hash TEXT NOT NULL,
  receipt_bytes BLOB NOT NULL,
  receipt_digest TEXT NOT NULL,
  journal_offset INTEGER NOT NULL UNIQUE REFERENCES events(journal_offset),
  UNIQUE(scope_key,idempotency_key)
);

CREATE TABLE messages(
  message_id TEXT PRIMARY KEY,
  group_aggregate_id TEXT NOT NULL,
  seat_id TEXT NOT NULL,
  round_id TEXT NOT NULL,
  message_type TEXT NOT NULL,
  payload_ref TEXT NOT NULL,
  payload_hash TEXT NOT NULL,
  source_candidate_id TEXT NOT NULL UNIQUE REFERENCES publication_candidates(candidate_id),
  official_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
  accepted_offset INTEGER NOT NULL REFERENCES events(journal_offset),
  UNIQUE(group_aggregate_id,seat_id,round_id,message_type)
);
