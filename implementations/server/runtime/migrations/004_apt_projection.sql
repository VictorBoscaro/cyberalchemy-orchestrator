CREATE TABLE projection_registrations(
  projection_name TEXT PRIMARY KEY,
  owner_namespace TEXT NOT NULL,
  reducer_ref TEXT NOT NULL,
  reducer_digest TEXT NOT NULL,
  registered_at TEXT NOT NULL
);

CREATE TABLE apt_semantic_facts(
  fact_id TEXT PRIMARY KEY,
  research_capture_id TEXT NOT NULL,
  subject_id TEXT NOT NULL,
  fact_kind TEXT NOT NULL,
  supersedes_fact_id TEXT REFERENCES apt_semantic_facts(fact_id),
  canonical_payload_digest TEXT NOT NULL,
  accepted_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
  is_current INTEGER NOT NULL CHECK(is_current IN (0,1)),
  UNIQUE(fact_id,canonical_payload_digest,subject_id,supersedes_fact_id)
);
CREATE UNIQUE INDEX one_current_apt_fact_per_subject
ON apt_semantic_facts(research_capture_id,subject_id) WHERE is_current=1;

CREATE TABLE apt_semantic_request_results(
  request_key TEXT NOT NULL,
  item_key TEXT NOT NULL,
  request_digest TEXT NOT NULL,
  result_status TEXT NOT NULL CHECK(result_status IN ('existing_exact','accepted_new')),
  result_json TEXT NOT NULL,
  accepted_event_id TEXT NOT NULL REFERENCES events(event_id),
  PRIMARY KEY(request_key,item_key)
);

CREATE TABLE apt_capture_keys(
  research_capture_id TEXT PRIMARY KEY,
  dispatch_id TEXT NOT NULL,
  expected_contribution_id TEXT NOT NULL,
  capture_operation_id TEXT NOT NULL UNIQUE,
  supersedes_capture_id TEXT REFERENCES apt_capture_keys(research_capture_id),
  capture_digest TEXT NOT NULL,
  accepted_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
  is_current INTEGER NOT NULL CHECK(is_current IN (0,1))
);
CREATE UNIQUE INDEX one_current_apt_capture_per_contribution
ON apt_capture_keys(dispatch_id,expected_contribution_id) WHERE is_current=1;

CREATE TABLE apt_delivery_keys(
  delivery_subject_key TEXT PRIMARY KEY,
  canonical_payload_digest TEXT NOT NULL,
  expected_head_event_id TEXT,
  accepted_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id)
);

-- This migration deliberately creates ports, not APT-owned research tables.
-- APT projection reducers register through ProjectionManager after its package
-- is independently authorized.
INSERT INTO projection_registrations(
  projection_name,owner_namespace,reducer_ref,reducer_digest,registered_at
) VALUES
  ('apt.session-record','agent-provenance-telemetry','unbound-port@1','sha256:0000000000000000000000000000000000000000000000000000000000000000',strftime('%Y-%m-%dT%H:%M:%fZ','now')),
  ('apt.dispatch-scope','agent-provenance-telemetry','unbound-port@1','sha256:0000000000000000000000000000000000000000000000000000000000000000',strftime('%Y-%m-%dT%H:%M:%fZ','now')),
  ('apt.research-record','agent-provenance-telemetry','unbound-port@1','sha256:0000000000000000000000000000000000000000000000000000000000000000',strftime('%Y-%m-%dT%H:%M:%fZ','now'));
