PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS schema_migrations (
    version INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL
) STRICT;

CREATE TABLE IF NOT EXISTS journal_events (
    seq INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id TEXT NOT NULL UNIQUE,
    operation_id TEXT NOT NULL UNIQUE,
    event_type TEXT NOT NULL,
    occurred_at TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    payload_digest TEXT NOT NULL,
    previous_event_hash TEXT,
    event_hash TEXT NOT NULL UNIQUE
) STRICT;

CREATE TABLE IF NOT EXISTS command_receipts (
    receipt_id TEXT PRIMARY KEY,
    operation_id TEXT NOT NULL UNIQUE,
    command_name TEXT NOT NULL,
    payload_digest TEXT NOT NULL,
    event_id TEXT NOT NULL UNIQUE REFERENCES journal_events(event_id),
    committed_seq INTEGER NOT NULL UNIQUE REFERENCES journal_events(seq),
    result_json TEXT NOT NULL,
    result_digest TEXT NOT NULL,
    receipt_digest TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL
) STRICT;

CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    ensure_key TEXT NOT NULL UNIQUE,
    origin_kind TEXT NOT NULL,
    origin_ref TEXT NOT NULL,
    initial_name TEXT,
    current_name TEXT,
    started_at TEXT NOT NULL,
    start_operation_id TEXT NOT NULL,
    source_event_id TEXT NOT NULL UNIQUE,
    last_activity_at TEXT NOT NULL,
    source_through_seq INTEGER NOT NULL,
    UNIQUE (origin_kind, origin_ref)
) STRICT;

CREATE TABLE IF NOT EXISTS session_dispatch_links (
    session_dispatch_link_id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES sessions(session_id),
    dispatch_id TEXT NOT NULL UNIQUE,
    link_operation_id TEXT NOT NULL UNIQUE,
    linked_at TEXT NOT NULL,
    source_event_id TEXT NOT NULL,
    source_through_seq INTEGER NOT NULL
) STRICT;

CREATE TABLE IF NOT EXISTS reference_scout_runs (
    scout_run_id TEXT PRIMARY KEY,
    probe_id TEXT NOT NULL UNIQUE,
    session_id TEXT NOT NULL REFERENCES sessions(session_id),
    dispatch_id TEXT,
    objective_ref TEXT NOT NULL,
    shape TEXT NOT NULL,
    source_mode TEXT NOT NULL,
    protocol_profile_id TEXT NOT NULL,
    protocol_profile_version TEXT NOT NULL,
    protocol_profile_digest TEXT NOT NULL,
    requested_at TEXT NOT NULL,
    state TEXT NOT NULL CHECK (state IN ('requested', 'collecting', 'committed', 'delivered')),
    bundle_digest TEXT,
    committed_event_id TEXT,
    delivered_at TEXT,
    source_through_seq INTEGER NOT NULL
) STRICT;

CREATE TABLE IF NOT EXISTS reference_recommendations (
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
    comparability_state TEXT CHECK (
        comparability_state IS NULL OR
        comparability_state IN ('comparable', 'incommensurable', 'count_capped')
    ),
    source_event_id TEXT NOT NULL,
    source_through_seq INTEGER NOT NULL,
    UNIQUE (scout_run_id, reference_id)
) STRICT;

CREATE INDEX IF NOT EXISTS idx_events_type_seq
    ON journal_events(event_type, seq);
CREATE INDEX IF NOT EXISTS idx_scout_session
    ON reference_scout_runs(session_id, requested_at);
CREATE INDEX IF NOT EXISTS idx_recommendations_run
    ON reference_recommendations(scout_run_id, recommendation_id);
