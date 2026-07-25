CREATE TABLE reference_scout_runs(
  scout_run_id TEXT PRIMARY KEY,
  probe_id TEXT NOT NULL UNIQUE,
  session_id TEXT NOT NULL REFERENCES sessions(session_id),
  dispatch_id TEXT NOT NULL REFERENCES dispatch_links(dispatch_id),
  launch_mode TEXT NOT NULL CHECK(launch_mode='dispatch_bound'),
  objective_ref TEXT NOT NULL,
  shape TEXT NOT NULL CHECK(shape IN ('small','tensioned')),
  source_mode TEXT NOT NULL CHECK(
    source_mode IN ('internal','external','internal-and-external')
  ),
  profile_id TEXT NOT NULL,
  profile_version TEXT NOT NULL,
  profile_digest TEXT NOT NULL,
  group_aggregate_id TEXT NOT NULL UNIQUE,
  seat_id TEXT NOT NULL,
  attempt_id TEXT NOT NULL,
  operation_id TEXT NOT NULL UNIQUE,
  state TEXT NOT NULL CHECK(
    state IN ('requested','collecting','committed','delivered','failed','cancelled')
  ),
  bundle_artifact_id TEXT REFERENCES artifacts(artifact_id),
  bundle_digest TEXT,
  requested_at TEXT NOT NULL,
  committed_at TEXT,
  delivered_at TEXT,
  start_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
  last_event_id TEXT NOT NULL REFERENCES events(event_id),
  source_through_offset INTEGER NOT NULL REFERENCES events(journal_offset),
  FOREIGN KEY(profile_id,profile_version)
    REFERENCES protocol_profiles(profile_id,profile_version),
  CHECK((bundle_artifact_id IS NULL)=(bundle_digest IS NULL)),
  CHECK(state NOT IN ('committed','delivered') OR bundle_digest IS NOT NULL),
  CHECK(state!='delivered' OR delivered_at IS NOT NULL)
);

CREATE INDEX reference_scout_runs_session_idx
ON reference_scout_runs(session_id,requested_at);

CREATE INDEX reference_scout_runs_dispatch_idx
ON reference_scout_runs(dispatch_id,requested_at);

CREATE TABLE reference_recommendations(
  recommendation_id TEXT PRIMARY KEY,
  scout_run_id TEXT NOT NULL REFERENCES reference_scout_runs(scout_run_id),
  reference_id TEXT NOT NULL,
  source_class TEXT NOT NULL,
  locator_observed TEXT NOT NULL,
  access_state TEXT NOT NULL,
  found_by_seat_id TEXT NOT NULL,
  evaluated_by_seat_id TEXT,
  evaluation TEXT,
  why_inspect TEXT NOT NULL,
  comparability_state TEXT CHECK(
    comparability_state IS NULL OR
    comparability_state IN ('comparable','incommensurable','count_capped')
  ),
  message_id TEXT NOT NULL UNIQUE REFERENCES messages(message_id),
  payload_ref TEXT NOT NULL REFERENCES artifacts(artifact_id),
  payload_hash TEXT NOT NULL,
  source_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
  source_through_offset INTEGER NOT NULL REFERENCES events(journal_offset),
  UNIQUE(scout_run_id,reference_id)
);

CREATE INDEX reference_recommendations_run_idx
ON reference_recommendations(scout_run_id,recommendation_id);

CREATE TABLE dispatch_ingestions(
  ingestion_id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL REFERENCES sessions(session_id),
  dispatch_id TEXT NOT NULL REFERENCES dispatch_links(dispatch_id),
  host TEXT NOT NULL CHECK(host IN ('claude','codex')),
  agent_id TEXT,
  tool_use_id TEXT NOT NULL,
  tool_name TEXT NOT NULL,
  source_kind TEXT NOT NULL CHECK(
    source_kind IN (
      'repository_file','repository_search','external_url',
      'mcp_resource','shell_opaque'
    )
  ),
  locator TEXT NOT NULL,
  repo_relative_path TEXT,
  content_digest TEXT,
  artifact_id TEXT REFERENCES artifacts(artifact_id),
  media_type TEXT,
  size_bytes INTEGER CHECK(size_bytes IS NULL OR size_bytes>=0),
  coverage TEXT NOT NULL CHECK(
    coverage IN ('exact','metadata_only','opaque')
  ),
  purpose TEXT NOT NULL,
  observed_at TEXT NOT NULL,
  event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
  accepted_offset INTEGER NOT NULL UNIQUE REFERENCES events(journal_offset),
  UNIQUE(host,tool_use_id,locator),
  CHECK(source_kind!='repository_file' OR repo_relative_path IS NOT NULL),
  CHECK(coverage!='exact' OR (
    content_digest IS NOT NULL AND artifact_id IS NOT NULL AND size_bytes IS NOT NULL
  )),
  CHECK((artifact_id IS NULL)=(content_digest IS NULL))
);

CREATE INDEX dispatch_ingestions_dispatch_idx
ON dispatch_ingestions(dispatch_id,accepted_offset);

CREATE INDEX dispatch_ingestions_session_idx
ON dispatch_ingestions(session_id,accepted_offset);
