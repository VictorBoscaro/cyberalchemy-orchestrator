CREATE TABLE sessions_v2(
  session_id TEXT PRIMARY KEY,
  origin_digest TEXT NOT NULL,
  name TEXT NOT NULL,
  started_at TEXT NOT NULL,
  event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id)
);
INSERT INTO sessions_v2 SELECT * FROM sessions;

CREATE TABLE dispatch_links_v2(
  dispatch_id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL REFERENCES sessions_v2(session_id),
  ledger_path TEXT NOT NULL,
  ledger_digest TEXT NOT NULL,
  row_digest TEXT NOT NULL,
  row_json TEXT NOT NULL,
  event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
  linked_at TEXT NOT NULL
);
INSERT INTO dispatch_links_v2 SELECT * FROM dispatch_links;

CREATE TABLE local_probe_contexts_v2(
  probe_context_id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL REFERENCES sessions_v2(session_id),
  dispatch_id TEXT NOT NULL REFERENCES dispatch_links_v2(dispatch_id),
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
  FOREIGN KEY(profile_id,profile_version)
    REFERENCES protocol_profiles(profile_id,profile_version)
);
INSERT INTO local_probe_contexts_v2 SELECT * FROM local_probe_contexts;

DROP TABLE local_probe_contexts;
DROP TABLE dispatch_links;
DROP TABLE sessions;
ALTER TABLE sessions_v2 RENAME TO sessions;
ALTER TABLE dispatch_links_v2 RENAME TO dispatch_links;
ALTER TABLE local_probe_contexts_v2 RENAME TO local_probe_contexts;
CREATE INDEX sessions_origin_history_idx
ON sessions(origin_digest,started_at,session_id);

CREATE TABLE session_origin_heads(
  origin_digest TEXT PRIMARY KEY,
  current_session_id TEXT NOT NULL UNIQUE REFERENCES sessions(session_id),
  head_version INTEGER NOT NULL CHECK(head_version>0),
  rebound_event_id TEXT REFERENCES events(event_id)
);
INSERT INTO session_origin_heads(origin_digest,current_session_id,head_version)
SELECT origin_digest,session_id,1 FROM sessions;

CREATE TABLE session_context_rebounds(
  predecessor_session_id TEXT NOT NULL REFERENCES sessions(session_id),
  successor_session_id TEXT PRIMARY KEY REFERENCES sessions(session_id),
  origin_digest TEXT NOT NULL,
  rebound_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
  rebound_at TEXT NOT NULL
);
