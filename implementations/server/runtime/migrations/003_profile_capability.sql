CREATE TABLE protocol_profiles(
  profile_id TEXT NOT NULL,
  profile_version TEXT NOT NULL,
  authoritative_path TEXT NOT NULL,
  authoritative_file_digest TEXT NOT NULL,
  canonical_digest TEXT NOT NULL,
  canonical_size_bytes INTEGER NOT NULL,
  registration_event_id TEXT NOT NULL REFERENCES events(event_id),
  registered_at TEXT NOT NULL,
  PRIMARY KEY(profile_id,profile_version)
);

CREATE TABLE capabilities(
  capability_id TEXT PRIMARY KEY,
  token_digest TEXT NOT NULL UNIQUE,
  principal_id TEXT NOT NULL,
  action TEXT NOT NULL,
  phase TEXT NOT NULL,
  context_json TEXT NOT NULL,
  issued_at TEXT NOT NULL,
  expires_at TEXT,
  revoked_at TEXT
);
CREATE INDEX capabilities_resolution_idx ON capabilities(token_digest,action,phase);

CREATE TABLE sessions(
  session_id TEXT PRIMARY KEY,
  origin_digest TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  started_at TEXT NOT NULL,
  event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id)
);

CREATE TABLE dispatch_links(
  dispatch_id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL REFERENCES sessions(session_id),
  ledger_path TEXT NOT NULL,
  ledger_digest TEXT NOT NULL,
  row_digest TEXT NOT NULL,
  row_json TEXT NOT NULL,
  event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
  linked_at TEXT NOT NULL
);

CREATE TABLE local_probe_contexts(
  probe_context_id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL REFERENCES sessions(session_id),
  dispatch_id TEXT NOT NULL REFERENCES dispatch_links(dispatch_id),
  probe_id TEXT NOT NULL,
  profile_id TEXT NOT NULL,
  profile_version TEXT NOT NULL,
  profile_digest TEXT NOT NULL,
  group_aggregate_id TEXT NOT NULL,
  seat_id TEXT NOT NULL,
  attempt_id TEXT NOT NULL,
  operation_id TEXT NOT NULL,
  phase TEXT NOT NULL CHECK(phase='collect'),
  event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
  UNIQUE(session_id,dispatch_id,probe_id,profile_digest),
  FOREIGN KEY(profile_id,profile_version) REFERENCES protocol_profiles(profile_id,profile_version)
);
