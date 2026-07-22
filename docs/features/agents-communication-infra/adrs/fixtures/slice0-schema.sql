-- SWU-ACI-001 / TASK-010 executable SQL contract fixture.
--
-- NON-PRODUCTION: this file freezes Slice-0 schema invariants for executable
-- contract tests. It is not a migration, runtime bootstrap script, or evidence
-- that the production SQLite writer exists. A later accepted ADR and TASK-010
-- implementation must version and apply production migrations explicitly.
--
-- Connection policy asserted by TASK-010 startup/tests:
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA synchronous = FULL;
PRAGMA busy_timeout = 5000;

BEGIN;

CREATE TABLE schema_migrations (
    schema_version INTEGER PRIMARY KEY CHECK (schema_version > 0),
    migration_id TEXT NOT NULL UNIQUE CHECK (length(migration_id) > 0),
    migration_checksum TEXT NOT NULL UNIQUE
        CHECK (length(migration_checksum) = 71
            AND substr(migration_checksum, 1, 7) = 'sha256:'
            AND substr(migration_checksum, 8) NOT GLOB '*[^0-9a-f]*'),
    applied_at TEXT NOT NULL CHECK (length(applied_at) > 0)
);

CREATE TABLE artifacts (
    artifact_id TEXT PRIMARY KEY CHECK (length(artifact_id) > 0),
    content_hash TEXT NOT NULL UNIQUE
        CHECK (length(content_hash) = 71
            AND substr(content_hash, 1, 7) = 'sha256:'
            AND substr(content_hash, 8) NOT GLOB '*[^0-9a-f]*'),
    media_type TEXT NOT NULL CHECK (length(media_type) > 0),
    schema_ref TEXT,
    classification TEXT NOT NULL CHECK (
        classification IN (
            'runtime-internal', 'sensitive-input', 'sensitive-output',
            'reveal-authorized', 'public'
        )
    ),
    size_bytes INTEGER NOT NULL CHECK (size_bytes >= 0),
    storage_ref TEXT NOT NULL CHECK (length(storage_ref) > 0),
    created_event_id TEXT,
    tombstoned_at TEXT,
    tombstone_reason TEXT,
    CHECK (
        (tombstoned_at IS NULL AND tombstone_reason IS NULL)
        OR (tombstoned_at IS NOT NULL AND tombstone_reason IS NOT NULL)
    ),
    FOREIGN KEY (created_event_id) REFERENCES events(event_id)
        DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE command_receipts (
    command_id TEXT PRIMARY KEY CHECK (length(command_id) > 0),
    scope_key TEXT NOT NULL CHECK (length(scope_key) > 0),
    idempotency_key TEXT NOT NULL CHECK (length(idempotency_key) > 0),
    command_digest TEXT NOT NULL
        CHECK (length(command_digest) = 71
            AND substr(command_digest, 1, 7) = 'sha256:'
            AND substr(command_digest, 8) NOT GLOB '*[^0-9a-f]*'),
    aggregate_id TEXT NOT NULL CHECK (length(aggregate_id) > 0),
    expected_version INTEGER NOT NULL CHECK (expected_version >= 0),
    status TEXT NOT NULL CHECK (
        status IN ('accepted', 'validation_rejected', 'idempotency_conflict', 'version_conflict')
    ),
    result_receipt_json TEXT NOT NULL CHECK (json_valid(result_receipt_json)),
    first_offset INTEGER,
    last_offset INTEGER,
    created_at TEXT NOT NULL CHECK (length(created_at) > 0),
    UNIQUE (scope_key, idempotency_key),
    CHECK (
        (status = 'accepted' AND first_offset IS NOT NULL AND last_offset IS NOT NULL
            AND first_offset > 0 AND last_offset >= first_offset)
        OR
        (status <> 'accepted' AND first_offset IS NULL AND last_offset IS NULL)
    ),
    FOREIGN KEY (first_offset) REFERENCES events(journal_offset)
        DEFERRABLE INITIALLY DEFERRED,
    FOREIGN KEY (last_offset) REFERENCES events(journal_offset)
        DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE events (
    journal_offset INTEGER PRIMARY KEY AUTOINCREMENT CHECK (journal_offset > 0),
    event_id TEXT NOT NULL UNIQUE CHECK (length(event_id) > 0),
    aggregate_type TEXT NOT NULL CHECK (length(aggregate_type) > 0),
    aggregate_id TEXT NOT NULL CHECK (length(aggregate_id) > 0),
    aggregate_version INTEGER NOT NULL CHECK (aggregate_version > 0),
    event_type TEXT NOT NULL CHECK (length(event_type) > 0),
    schema_ref TEXT NOT NULL CHECK (length(schema_ref) > 0),
    schema_digest TEXT NOT NULL
        CHECK (length(schema_digest) = 71
            AND substr(schema_digest, 1, 7) = 'sha256:'
            AND substr(schema_digest, 8) NOT GLOB '*[^0-9a-f]*'),
    command_id TEXT NOT NULL,
    causation_id TEXT NOT NULL CHECK (length(causation_id) > 0),
    correlation_id TEXT NOT NULL CHECK (length(correlation_id) > 0),
    recorded_at TEXT NOT NULL CHECK (length(recorded_at) > 0),
    observed_at TEXT,
    payload_ref TEXT NOT NULL,
    payload_hash TEXT NOT NULL
        CHECK (length(payload_hash) = 71
            AND substr(payload_hash, 1, 7) = 'sha256:'
            AND substr(payload_hash, 8) NOT GLOB '*[^0-9a-f]*'),
    authority_context_json TEXT NOT NULL CHECK (json_valid(authority_context_json)),
    UNIQUE (aggregate_id, aggregate_version),
    UNIQUE (event_id, journal_offset),
    FOREIGN KEY (command_id) REFERENCES command_receipts(command_id)
        DEFERRABLE INITIALLY DEFERRED,
    FOREIGN KEY (payload_ref) REFERENCES artifacts(artifact_id)
        DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE aggregate_heads (
    aggregate_id TEXT PRIMARY KEY CHECK (length(aggregate_id) > 0),
    aggregate_type TEXT NOT NULL CHECK (length(aggregate_type) > 0),
    current_version INTEGER NOT NULL CHECK (current_version >= 0),
    state_hash TEXT NOT NULL
        CHECK (length(state_hash) = 71
            AND substr(state_hash, 1, 7) = 'sha256:'
            AND substr(state_hash, 8) NOT GLOB '*[^0-9a-f]*'),
    last_event_id TEXT,
    last_offset INTEGER,
    reducer_version TEXT NOT NULL CHECK (length(reducer_version) > 0),
    CHECK (
        (current_version = 0 AND last_event_id IS NULL AND last_offset IS NULL)
        OR (current_version > 0 AND last_event_id IS NOT NULL AND last_offset IS NOT NULL)
    ),
    FOREIGN KEY (last_event_id, last_offset) REFERENCES events(event_id, journal_offset)
        DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE effect_intents (
    effect_id TEXT PRIMARY KEY CHECK (length(effect_id) > 0),
    command_id TEXT NOT NULL,
    requested_event_id TEXT NOT NULL,
    effect_type TEXT NOT NULL CHECK (length(effect_type) > 0),
    payload_ref TEXT NOT NULL,
    payload_digest TEXT NOT NULL
        CHECK (length(payload_digest) = 71
            AND substr(payload_digest, 1, 7) = 'sha256:'
            AND substr(payload_digest, 8) NOT GLOB '*[^0-9a-f]*'),
    retry_class TEXT NOT NULL CHECK (retry_class IN ('retryable', 'non_retryable')),
    status TEXT NOT NULL CHECK (status IN ('pending', 'claimed', 'succeeded', 'failed', 'unknown')),
    claim_epoch INTEGER NOT NULL DEFAULT 0 CHECK (claim_epoch >= 0),
    claimed_by TEXT,
    attempt_count INTEGER NOT NULL DEFAULT 0 CHECK (attempt_count >= 0),
    outcome_event_id TEXT UNIQUE,
    outcome_digest TEXT
        CHECK (outcome_digest IS NULL OR (
            length(outcome_digest) = 71
            AND substr(outcome_digest, 1, 7) = 'sha256:'
            AND substr(outcome_digest, 8) NOT GLOB '*[^0-9a-f]*'
        )),
    UNIQUE (command_id, requested_event_id, effect_type),
    CHECK (
        (status = 'pending' AND claimed_by IS NULL AND outcome_event_id IS NULL AND outcome_digest IS NULL)
        OR (status = 'claimed' AND claimed_by IS NOT NULL AND claim_epoch > 0
            AND outcome_event_id IS NULL AND outcome_digest IS NULL)
        OR (status IN ('succeeded', 'failed', 'unknown') AND claimed_by IS NOT NULL
            AND claim_epoch > 0 AND outcome_event_id IS NOT NULL AND outcome_digest IS NOT NULL)
    ),
    FOREIGN KEY (command_id) REFERENCES command_receipts(command_id)
        DEFERRABLE INITIALLY DEFERRED,
    FOREIGN KEY (requested_event_id) REFERENCES events(event_id)
        DEFERRABLE INITIALLY DEFERRED,
    FOREIGN KEY (payload_ref) REFERENCES artifacts(artifact_id)
        DEFERRABLE INITIALLY DEFERRED,
    FOREIGN KEY (outcome_event_id) REFERENCES events(event_id)
        DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE publication_candidates (
    candidate_id TEXT PRIMARY KEY CHECK (length(candidate_id) > 0),
    message_id TEXT NOT NULL UNIQUE CHECK (length(message_id) > 0),
    publication_event_id TEXT NOT NULL UNIQUE,
    group_aggregate_id TEXT NOT NULL CHECK (length(group_aggregate_id) > 0),
    seat_id TEXT NOT NULL CHECK (length(seat_id) > 0),
    round_id TEXT NOT NULL CHECK (length(round_id) > 0),
    message_type TEXT NOT NULL CHECK (length(message_type) > 0),
    attempt_id TEXT NOT NULL CHECK (length(attempt_id) > 0),
    operation_id TEXT NOT NULL CHECK (length(operation_id) > 0),
    payload_ref TEXT NOT NULL,
    payload_hash TEXT NOT NULL
        CHECK (length(payload_hash) = 71
            AND substr(payload_hash, 1, 7) = 'sha256:'
            AND substr(payload_hash, 8) NOT GLOB '*[^0-9a-f]*'),
    idempotency_key TEXT NOT NULL CHECK (length(idempotency_key) > 0),
    receipt_bytes BLOB NOT NULL CHECK (length(receipt_bytes) > 0),
    receipt_digest TEXT NOT NULL
        CHECK (length(receipt_digest) = 71
            AND substr(receipt_digest, 1, 7) = 'sha256:'
            AND substr(receipt_digest, 8) NOT GLOB '*[^0-9a-f]*'),
    journal_offset INTEGER NOT NULL CHECK (journal_offset > 0),
    status TEXT NOT NULL CHECK (status IN ('active', 'officially_accepted', 'abandoned')),
    candidate_version INTEGER NOT NULL DEFAULT 1 CHECK (candidate_version > 0),
    official_accepted_event_id TEXT UNIQUE,
    abandoned_event_id TEXT UNIQUE,
    UNIQUE (group_aggregate_id, seat_id, round_id, idempotency_key),
    UNIQUE (candidate_id, message_id, publication_event_id),
    UNIQUE (candidate_id, message_id, official_accepted_event_id),
    CHECK (
        (status = 'active' AND official_accepted_event_id IS NULL AND abandoned_event_id IS NULL)
        OR (status = 'officially_accepted' AND official_accepted_event_id IS NOT NULL
            AND abandoned_event_id IS NULL)
        OR (status = 'abandoned' AND official_accepted_event_id IS NULL
            AND abandoned_event_id IS NOT NULL)
    ),
    FOREIGN KEY (publication_event_id, journal_offset) REFERENCES events(event_id, journal_offset)
        DEFERRABLE INITIALLY DEFERRED,
    FOREIGN KEY (payload_ref) REFERENCES artifacts(artifact_id)
        DEFERRABLE INITIALLY DEFERRED,
    FOREIGN KEY (official_accepted_event_id) REFERENCES events(event_id)
        DEFERRABLE INITIALLY DEFERRED,
    FOREIGN KEY (abandoned_event_id) REFERENCES events(event_id)
        DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE publication_receipts (
    event_id TEXT PRIMARY KEY,
    candidate_id TEXT NOT NULL UNIQUE,
    message_id TEXT NOT NULL UNIQUE,
    group_aggregate_id TEXT NOT NULL,
    seat_id TEXT NOT NULL,
    round_id TEXT NOT NULL,
    idempotency_key TEXT NOT NULL,
    payload_hash TEXT NOT NULL
        CHECK (length(payload_hash) = 71
            AND substr(payload_hash, 1, 7) = 'sha256:'
            AND substr(payload_hash, 8) NOT GLOB '*[^0-9a-f]*'),
    receipt_bytes BLOB NOT NULL CHECK (length(receipt_bytes) > 0),
    receipt_digest TEXT NOT NULL
        CHECK (length(receipt_digest) = 71
            AND substr(receipt_digest, 1, 7) = 'sha256:'
            AND substr(receipt_digest, 8) NOT GLOB '*[^0-9a-f]*'),
    journal_offset INTEGER NOT NULL CHECK (journal_offset > 0),
    UNIQUE (group_aggregate_id, seat_id, round_id, idempotency_key),
    FOREIGN KEY (candidate_id, message_id, event_id)
        REFERENCES publication_candidates(candidate_id, message_id, publication_event_id)
        DEFERRABLE INITIALLY DEFERRED,
    FOREIGN KEY (event_id, journal_offset) REFERENCES events(event_id, journal_offset)
        DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE messages (
    message_id TEXT PRIMARY KEY,
    source_candidate_id TEXT NOT NULL UNIQUE,
    group_aggregate_id TEXT NOT NULL CHECK (length(group_aggregate_id) > 0),
    seat_id TEXT NOT NULL CHECK (length(seat_id) > 0),
    round_id TEXT NOT NULL CHECK (length(round_id) > 0),
    message_type TEXT NOT NULL CHECK (length(message_type) > 0),
    payload_ref TEXT NOT NULL,
    payload_hash TEXT NOT NULL
        CHECK (length(payload_hash) = 71
            AND substr(payload_hash, 1, 7) = 'sha256:'
            AND substr(payload_hash, 8) NOT GLOB '*[^0-9a-f]*'),
    official_accepted_event_id TEXT NOT NULL UNIQUE,
    UNIQUE (group_aggregate_id, seat_id, round_id, message_type),
    FOREIGN KEY (source_candidate_id, message_id, official_accepted_event_id)
        REFERENCES publication_candidates(candidate_id, message_id, official_accepted_event_id)
        DEFERRABLE INITIALLY DEFERRED,
    FOREIGN KEY (payload_ref) REFERENCES artifacts(artifact_id)
        DEFERRABLE INITIALLY DEFERRED,
    FOREIGN KEY (official_accepted_event_id) REFERENCES events(event_id)
        DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE attempts (
    attempt_id TEXT PRIMARY KEY CHECK (length(attempt_id) > 0),
    operation_id TEXT NOT NULL CHECK (length(operation_id) > 0),
    attempt_no INTEGER NOT NULL CHECK (attempt_no > 0),
    accepted_result INTEGER NOT NULL DEFAULT 0 CHECK (accepted_result IN (0, 1)),
    terminal_event_id TEXT UNIQUE,
    UNIQUE (operation_id, attempt_no),
    FOREIGN KEY (terminal_event_id) REFERENCES events(event_id)
        DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE reveal_manifests (
    reveal_manifest_id TEXT PRIMARY KEY CHECK (length(reveal_manifest_id) > 0),
    group_aggregate_id TEXT NOT NULL CHECK (length(group_aggregate_id) > 0),
    round_id TEXT NOT NULL CHECK (length(round_id) > 0),
    reveal_event_id TEXT NOT NULL UNIQUE,
    manifest_hash TEXT NOT NULL
        CHECK (length(manifest_hash) = 71
            AND substr(manifest_hash, 1, 7) = 'sha256:'
            AND substr(manifest_hash, 8) NOT GLOB '*[^0-9a-f]*'),
    UNIQUE (group_aggregate_id, round_id),
    FOREIGN KEY (reveal_event_id) REFERENCES events(event_id)
        DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE reveal_manifest_entries (
    reveal_manifest_id TEXT NOT NULL,
    ordinal INTEGER NOT NULL CHECK (ordinal >= 0),
    message_id TEXT NOT NULL,
    message_hash TEXT NOT NULL
        CHECK (length(message_hash) = 71
            AND substr(message_hash, 1, 7) = 'sha256:'
            AND substr(message_hash, 8) NOT GLOB '*[^0-9a-f]*'),
    payload_hash TEXT NOT NULL
        CHECK (length(payload_hash) = 71
            AND substr(payload_hash, 1, 7) = 'sha256:'
            AND substr(payload_hash, 8) NOT GLOB '*[^0-9a-f]*'),
    PRIMARY KEY (reveal_manifest_id, ordinal),
    UNIQUE (reveal_manifest_id, message_id),
    FOREIGN KEY (reveal_manifest_id) REFERENCES reveal_manifests(reveal_manifest_id),
    FOREIGN KEY (message_id) REFERENCES messages(message_id)
);

CREATE TABLE usage_observations (
    usage_event_id TEXT PRIMARY KEY,
    provider_ref TEXT,
    model_ref TEXT,
    attempt_id TEXT,
    input_tokens INTEGER CHECK (input_tokens IS NULL OR input_tokens >= 0),
    output_tokens INTEGER CHECK (output_tokens IS NULL OR output_tokens >= 0),
    cached_input_tokens INTEGER CHECK (cached_input_tokens IS NULL OR cached_input_tokens >= 0),
    tool_calls INTEGER CHECK (tool_calls IS NULL OR tool_calls >= 0),
    raw_usage_json TEXT NOT NULL CHECK (json_valid(raw_usage_json)),
    FOREIGN KEY (usage_event_id) REFERENCES events(event_id)
        DEFERRABLE INITIALLY DEFERRED,
    FOREIGN KEY (attempt_id) REFERENCES attempts(attempt_id)
        DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE pricing_sources (
    pricing_source_id TEXT PRIMARY KEY CHECK (length(pricing_source_id) > 0),
    provider_ref TEXT NOT NULL CHECK (length(provider_ref) > 0),
    model_ref TEXT NOT NULL CHECK (length(model_ref) > 0),
    effective_from TEXT NOT NULL CHECK (length(effective_from) > 0),
    effective_to TEXT,
    currency TEXT NOT NULL CHECK (length(currency) = 3 AND currency = upper(currency)),
    unit_semantics TEXT NOT NULL CHECK (length(unit_semantics) > 0),
    source_ref TEXT NOT NULL CHECK (length(source_ref) > 0),
    source_artifact_id TEXT,
    pricing_digest TEXT NOT NULL UNIQUE
        CHECK (length(pricing_digest) = 71
            AND substr(pricing_digest, 1, 7) = 'sha256:'
            AND substr(pricing_digest, 8) NOT GLOB '*[^0-9a-f]*'),
    CHECK (effective_to IS NULL OR effective_to > effective_from),
    UNIQUE (provider_ref, model_ref, effective_from, pricing_digest),
    FOREIGN KEY (source_artifact_id) REFERENCES artifacts(artifact_id)
        DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE usage_rollups (
    rollup_kind TEXT NOT NULL CHECK (length(rollup_kind) > 0),
    rollup_key TEXT NOT NULL CHECK (length(rollup_key) > 0),
    semantics_version TEXT NOT NULL CHECK (length(semantics_version) > 0),
    source_through_offset INTEGER NOT NULL CHECK (source_through_offset > 0),
    provider_ref TEXT,
    model_ref TEXT,
    observation_count INTEGER NOT NULL CHECK (observation_count >= 0),
    counters_json TEXT NOT NULL CHECK (json_valid(counters_json)),
    missing_counts_json TEXT NOT NULL CHECK (json_valid(missing_counts_json)),
    currency TEXT CHECK (currency IS NULL OR (length(currency) = 3 AND currency = upper(currency))),
    cost_summary_json TEXT CHECK (cost_summary_json IS NULL OR json_valid(cost_summary_json)),
    PRIMARY KEY (rollup_kind, rollup_key, semantics_version, source_through_offset),
    FOREIGN KEY (source_through_offset) REFERENCES events(journal_offset)
        DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE cost_calculations (
    cost_calculation_id TEXT PRIMARY KEY CHECK (length(cost_calculation_id) > 0),
    pricing_source_id TEXT NOT NULL,
    usage_event_id TEXT,
    rollup_kind TEXT,
    rollup_key TEXT,
    semantics_version TEXT,
    source_through_offset INTEGER NOT NULL CHECK (source_through_offset > 0),
    quantity NUMERIC NOT NULL CHECK (quantity >= 0),
    unit_price NUMERIC NOT NULL CHECK (unit_price >= 0),
    currency TEXT NOT NULL CHECK (length(currency) = 3 AND currency = upper(currency)),
    pricing_digest TEXT NOT NULL
        CHECK (length(pricing_digest) = 71
            AND substr(pricing_digest, 1, 7) = 'sha256:'
            AND substr(pricing_digest, 8) NOT GLOB '*[^0-9a-f]*'),
    calculation_digest TEXT NOT NULL UNIQUE
        CHECK (length(calculation_digest) = 71
            AND substr(calculation_digest, 1, 7) = 'sha256:'
            AND substr(calculation_digest, 8) NOT GLOB '*[^0-9a-f]*'),
    CHECK (
        (usage_event_id IS NOT NULL AND rollup_kind IS NULL AND rollup_key IS NULL
            AND semantics_version IS NULL)
        OR
        (usage_event_id IS NULL AND rollup_kind IS NOT NULL AND rollup_key IS NOT NULL
            AND semantics_version IS NOT NULL)
    ),
    FOREIGN KEY (pricing_source_id) REFERENCES pricing_sources(pricing_source_id),
    FOREIGN KEY (usage_event_id) REFERENCES usage_observations(usage_event_id)
        DEFERRABLE INITIALLY DEFERRED,
    FOREIGN KEY (rollup_kind, rollup_key, semantics_version, source_through_offset)
        REFERENCES usage_rollups(rollup_kind, rollup_key, semantics_version, source_through_offset)
        DEFERRABLE INITIALLY DEFERRED,
    FOREIGN KEY (source_through_offset) REFERENCES events(journal_offset)
        DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE runtime_projections (
    projection_name TEXT NOT NULL CHECK (length(projection_name) > 0),
    projection_key TEXT NOT NULL CHECK (length(projection_key) > 0),
    projection_json TEXT NOT NULL CHECK (json_valid(projection_json)),
    last_offset INTEGER NOT NULL CHECK (last_offset > 0),
    PRIMARY KEY (projection_name, projection_key),
    FOREIGN KEY (last_offset) REFERENCES events(journal_offset)
        DEFERRABLE INITIALLY DEFERRED
);

CREATE UNIQUE INDEX one_active_candidate_per_logical_key
    ON publication_candidates(group_aggregate_id, seat_id, round_id, message_type)
    WHERE status = 'active';

CREATE INDEX events_by_command ON events(command_id, journal_offset);
CREATE INDEX events_by_aggregate ON events(aggregate_id, aggregate_version);
CREATE INDEX events_by_correlation ON events(correlation_id, journal_offset);
CREATE INDEX effect_intents_by_status_type ON effect_intents(status, effect_type);
CREATE INDEX messages_by_group_round ON messages(group_aggregate_id, round_id);
CREATE UNIQUE INDEX one_accepted_attempt_per_operation
    ON attempts(operation_id) WHERE accepted_result = 1;
CREATE INDEX attempts_by_operation_number ON attempts(operation_id, attempt_no);
CREATE INDEX reveal_manifest_entries_by_message ON reveal_manifest_entries(message_id);
CREATE INDEX usage_observations_by_provider_model
    ON usage_observations(provider_ref, model_ref, usage_event_id);
CREATE INDEX pricing_sources_by_applicability
    ON pricing_sources(provider_ref, model_ref, effective_from, effective_to);
CREATE INDEX cost_calculations_by_source_offset
    ON cost_calculations(source_through_offset);
CREATE INDEX runtime_projections_by_offset
    ON runtime_projections(last_offset, projection_name);

-- Accepted journal and migration evidence is append-only. Correction requires
-- a new event/migration; rewriting an accepted identity would invalidate replay.
CREATE TRIGGER schema_migration_is_immutable
BEFORE UPDATE ON schema_migrations
BEGIN
    SELECT RAISE(ABORT, 'schema migration is immutable');
END;

CREATE TRIGGER command_receipt_is_immutable
BEFORE UPDATE ON command_receipts
BEGIN
    SELECT RAISE(ABORT, 'command receipt is immutable');
END;

CREATE TRIGGER event_is_immutable
BEFORE UPDATE ON events
BEGIN
    SELECT RAISE(ABORT, 'event is immutable');
END;

-- Artifact identity/content metadata is immutable. A creating-event link may
-- be filled once and tombstoning may occur once; neither may be removed or
-- replaced after it is recorded.
CREATE TRIGGER artifact_update_is_finalize_or_tombstone
BEFORE UPDATE ON artifacts
WHEN NEW.artifact_id IS NOT OLD.artifact_id
  OR NEW.content_hash IS NOT OLD.content_hash
  OR NEW.media_type IS NOT OLD.media_type
  OR NEW.schema_ref IS NOT OLD.schema_ref
  OR NEW.classification IS NOT OLD.classification
  OR NEW.size_bytes IS NOT OLD.size_bytes
  OR NEW.storage_ref IS NOT OLD.storage_ref
  OR (OLD.created_event_id IS NOT NULL AND NEW.created_event_id IS NOT OLD.created_event_id)
  OR (OLD.created_event_id IS NULL AND NEW.created_event_id IS NULL
      AND NEW.tombstoned_at IS OLD.tombstoned_at AND NEW.tombstone_reason IS OLD.tombstone_reason)
  OR (OLD.tombstoned_at IS NOT NULL AND (
      NEW.tombstoned_at IS NOT OLD.tombstoned_at OR NEW.tombstone_reason IS NOT OLD.tombstone_reason
  ))
BEGIN
    SELECT RAISE(ABORT, 'artifact update is not one-time finalization or tombstoning');
END;

CREATE TRIGGER reveal_manifest_is_immutable
BEFORE UPDATE ON reveal_manifests
BEGIN
    SELECT RAISE(ABORT, 'reveal manifest is immutable');
END;

CREATE TRIGGER reveal_manifest_entry_is_immutable
BEFORE UPDATE ON reveal_manifest_entries
BEGIN
    SELECT RAISE(ABORT, 'reveal manifest entry is immutable');
END;

CREATE TRIGGER usage_observation_is_immutable
BEFORE UPDATE ON usage_observations
BEGIN
    SELECT RAISE(ABORT, 'usage observation is immutable');
END;

CREATE TRIGGER pricing_source_is_immutable
BEFORE UPDATE ON pricing_sources
BEGIN
    SELECT RAISE(ABORT, 'pricing source is immutable');
END;

CREATE TRIGGER cost_calculation_is_immutable
BEFORE UPDATE ON cost_calculations
BEGIN
    SELECT RAISE(ABORT, 'cost calculation is immutable');
END;

-- Rollups and runtime projections are rebuildable. Their identity/semantics
-- stay fixed and their source cursor may only move forward.
CREATE TRIGGER usage_rollup_update_is_monotonic
BEFORE UPDATE ON usage_rollups
WHEN NEW.rollup_kind IS NOT OLD.rollup_kind
  OR NEW.rollup_key IS NOT OLD.rollup_key
  OR NEW.semantics_version IS NOT OLD.semantics_version
  OR NEW.source_through_offset < OLD.source_through_offset
  OR NEW.provider_ref IS NOT OLD.provider_ref
  OR NEW.model_ref IS NOT OLD.model_ref
BEGIN
    SELECT RAISE(ABORT, 'usage rollup identity changed or source offset regressed');
END;

CREATE TRIGGER runtime_projection_update_is_monotonic
BEFORE UPDATE ON runtime_projections
WHEN NEW.projection_name IS NOT OLD.projection_name
  OR NEW.projection_key IS NOT OLD.projection_key
  OR NEW.last_offset < OLD.last_offset
BEGIN
    SELECT RAISE(ABORT, 'runtime projection identity changed or cursor regressed');
END;

-- Authoritative facts and retained evidence are never physically deleted.
-- Artifacts use the tombstone fields above; corrections to every other row are
-- represented by later events/versions. Rebuildable rollups and runtime
-- projections are deliberately excluded from these guards.
CREATE TRIGGER schema_migration_delete_is_forbidden
BEFORE DELETE ON schema_migrations BEGIN
    SELECT RAISE(ABORT, 'schema migration deletion is forbidden');
END;

CREATE TRIGGER artifact_delete_is_forbidden
BEFORE DELETE ON artifacts BEGIN
    SELECT RAISE(ABORT, 'artifact deletion is forbidden; tombstone it');
END;

CREATE TRIGGER command_receipt_delete_is_forbidden
BEFORE DELETE ON command_receipts BEGIN
    SELECT RAISE(ABORT, 'command receipt deletion is forbidden');
END;

CREATE TRIGGER event_delete_is_forbidden
BEFORE DELETE ON events BEGIN
    SELECT RAISE(ABORT, 'event deletion is forbidden');
END;

CREATE TRIGGER aggregate_head_delete_is_forbidden
BEFORE DELETE ON aggregate_heads BEGIN
    SELECT RAISE(ABORT, 'aggregate head deletion is forbidden');
END;

CREATE TRIGGER effect_intent_delete_is_forbidden
BEFORE DELETE ON effect_intents BEGIN
    SELECT RAISE(ABORT, 'effect intent deletion is forbidden');
END;

CREATE TRIGGER publication_candidate_delete_is_forbidden
BEFORE DELETE ON publication_candidates BEGIN
    SELECT RAISE(ABORT, 'publication candidate deletion is forbidden');
END;

CREATE TRIGGER publication_receipt_delete_is_forbidden
BEFORE DELETE ON publication_receipts BEGIN
    SELECT RAISE(ABORT, 'publication receipt deletion is forbidden');
END;

CREATE TRIGGER official_message_delete_is_forbidden
BEFORE DELETE ON messages BEGIN
    SELECT RAISE(ABORT, 'official message deletion is forbidden');
END;

CREATE TRIGGER attempt_delete_is_forbidden
BEFORE DELETE ON attempts BEGIN
    SELECT RAISE(ABORT, 'attempt history deletion is forbidden');
END;

CREATE TRIGGER reveal_manifest_delete_is_forbidden
BEFORE DELETE ON reveal_manifests BEGIN
    SELECT RAISE(ABORT, 'reveal manifest deletion is forbidden');
END;

CREATE TRIGGER reveal_manifest_entry_delete_is_forbidden
BEFORE DELETE ON reveal_manifest_entries BEGIN
    SELECT RAISE(ABORT, 'reveal manifest entry deletion is forbidden');
END;

CREATE TRIGGER usage_observation_delete_is_forbidden
BEFORE DELETE ON usage_observations BEGIN
    SELECT RAISE(ABORT, 'usage observation deletion is forbidden');
END;

CREATE TRIGGER pricing_source_delete_is_forbidden
BEFORE DELETE ON pricing_sources BEGIN
    SELECT RAISE(ABORT, 'pricing source deletion is forbidden');
END;

CREATE TRIGGER cost_calculation_delete_is_forbidden
BEFORE DELETE ON cost_calculations BEGIN
    SELECT RAISE(ABORT, 'cost calculation deletion is forbidden');
END;

-- SQL cannot express a cross-table uniqueness exclusion as an index. Once an
-- official message owns a logical key, no later candidate may reserve it.
CREATE TRIGGER publication_candidate_must_start_active
BEFORE INSERT ON publication_candidates
WHEN NEW.status <> 'active'
BEGIN
    SELECT RAISE(ABORT, 'publication candidate must start active');
END;

CREATE TRIGGER publication_candidate_rejects_official_logical_key
BEFORE INSERT ON publication_candidates
WHEN EXISTS (
    SELECT 1
      FROM messages AS m
     WHERE m.group_aggregate_id = NEW.group_aggregate_id
       AND m.seat_id = NEW.seat_id
       AND m.round_id = NEW.round_id
       AND m.message_type = NEW.message_type
)
BEGIN
    SELECT RAISE(ABORT, 'official message already owns logical publication key');
END;

-- Candidate content and logical identity are immutable. The only update is a
-- one-step CAS-style terminal transition with an incremented candidate version.
CREATE TRIGGER publication_candidate_update_is_terminal_cas
BEFORE UPDATE ON publication_candidates
WHEN OLD.status <> 'active'
  OR NEW.status NOT IN ('officially_accepted', 'abandoned')
  OR NEW.candidate_version <> OLD.candidate_version + 1
  OR NEW.candidate_id IS NOT OLD.candidate_id
  OR NEW.message_id IS NOT OLD.message_id
  OR NEW.publication_event_id IS NOT OLD.publication_event_id
  OR NEW.group_aggregate_id IS NOT OLD.group_aggregate_id
  OR NEW.seat_id IS NOT OLD.seat_id
  OR NEW.round_id IS NOT OLD.round_id
  OR NEW.message_type IS NOT OLD.message_type
  OR NEW.attempt_id IS NOT OLD.attempt_id
  OR NEW.operation_id IS NOT OLD.operation_id
  OR NEW.payload_ref IS NOT OLD.payload_ref
  OR NEW.payload_hash IS NOT OLD.payload_hash
  OR NEW.idempotency_key IS NOT OLD.idempotency_key
  OR NEW.receipt_bytes IS NOT OLD.receipt_bytes
  OR NEW.receipt_digest IS NOT OLD.receipt_digest
  OR NEW.journal_offset IS NOT OLD.journal_offset
BEGIN
    SELECT RAISE(ABORT, 'publication candidate update is not a terminal CAS');
END;

-- The rebuildable receipt lookup must be byte-for-byte and field-for-field a
-- view of its authoritative candidate, never a competing receipt authority.
CREATE TRIGGER publication_receipt_must_match_candidate
BEFORE INSERT ON publication_receipts
WHEN NOT EXISTS (
    SELECT 1
      FROM publication_candidates AS c
     WHERE c.candidate_id = NEW.candidate_id
       AND c.message_id = NEW.message_id
       AND c.publication_event_id = NEW.event_id
       AND c.group_aggregate_id = NEW.group_aggregate_id
       AND c.seat_id = NEW.seat_id
       AND c.round_id = NEW.round_id
       AND c.idempotency_key = NEW.idempotency_key
       AND c.payload_hash = NEW.payload_hash
       AND c.receipt_bytes = NEW.receipt_bytes
       AND c.receipt_digest = NEW.receipt_digest
       AND c.journal_offset = NEW.journal_offset
)
BEGIN
    SELECT RAISE(ABORT, 'publication receipt diverges from authoritative candidate');
END;

CREATE TRIGGER publication_receipt_is_immutable
BEFORE UPDATE ON publication_receipts
BEGIN
    SELECT RAISE(ABORT, 'publication receipt is immutable');
END;

-- Official rows are admitted only from a candidate already won by the
-- officially_accepted CAS, with exact logical key and payload equality.
CREATE TRIGGER official_message_must_match_candidate
BEFORE INSERT ON messages
WHEN NOT EXISTS (
    SELECT 1
      FROM publication_candidates AS c
     WHERE c.candidate_id = NEW.source_candidate_id
       AND c.message_id = NEW.message_id
       AND c.status = 'officially_accepted'
       AND c.official_accepted_event_id = NEW.official_accepted_event_id
       AND c.group_aggregate_id = NEW.group_aggregate_id
       AND c.seat_id = NEW.seat_id
       AND c.round_id = NEW.round_id
       AND c.message_type = NEW.message_type
       AND c.payload_ref = NEW.payload_ref
       AND c.payload_hash = NEW.payload_hash
)
BEGIN
    SELECT RAISE(ABORT, 'official message diverges from accepted candidate');
END;

CREATE TRIGGER official_message_is_immutable
BEFORE UPDATE ON messages
BEGIN
    SELECT RAISE(ABORT, 'official message is immutable');
END;

CREATE TRIGGER cost_calculation_must_match_pricing_source
BEFORE INSERT ON cost_calculations
WHEN NOT EXISTS (
    SELECT 1
      FROM pricing_sources AS p
     WHERE p.pricing_source_id = NEW.pricing_source_id
       AND p.pricing_digest = NEW.pricing_digest
       AND p.currency = NEW.currency
)
BEGIN
    SELECT RAISE(ABORT, 'cost calculation diverges from pricing source');
END;

COMMIT;
