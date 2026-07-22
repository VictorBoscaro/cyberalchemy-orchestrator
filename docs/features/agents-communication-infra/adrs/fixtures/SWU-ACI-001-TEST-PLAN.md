---
feature: agents-communication-infra
task: TASK-000
swu: SWU-ACI-001
status: contract-fixture-not-runtime-proof
version: 0.1.2
last_updated: 2026-07-21
---

# SWU-ACI-001 executable test plan

This plan names the executable tests that TASK-010 must implement. It is W0 contract evidence only:
no test listed here has passed against a production journal, migration set or recovery runtime. The
normative golden data is [`canonical-contract-vectors.json`](canonical-contract-vectors.json).
It contains six positive canonical vectors and six executable rejection vectors.

## Dependency and canonical contract

TASK-010 must declare and resolve the exact production pins `pydantic==2.13.4` and
`pydantic-core==2.46.4`. A change to either pin must rerun this entire vector corpus and receive
review before its output can be accepted. Pydantic validates the decoded model; the runtime-owned
projection, canonical serializer and SHA-256 calculation define acceptance identity. Every digest
is rendered as `sha256:<lowercase 64-hex>`.

| Executable test name | Contract assertion | Source fixture/rule |
|---|---|---|
| `test_canonical_vectors_match_exact_utf8_bytes_and_prefixed_sha256` | Every canonical string encodes to the declared byte length and `sha256:<64-hex>` digest without BOM/newline. | `V-ACI-CANON-001`–`006`; ACI-R16 |
| `test_equivalent_inputs_project_to_same_canonical_digest` | Input ordering, UTC-equivalent timestamps, decimal spelling, NFC/NFD spelling and integer `0`/`-0` converge within one vector. | `V-ACI-CANON-001`, `003`, `004`, `006` |
| `test_omitted_and_explicit_null_have_distinct_digests` | Omitted optional value and explicit nullable value are distinct accepted values. | `V-ACI-CANON-001` vs `002` |
| `test_arrays_preserve_order_while_object_keys_sort_recursively` | Object order is canonical at every depth and array order is untouched. | `V-ACI-CANON-003` |
| `test_schema_version_change_changes_canonical_digest` | Otherwise equal @1/@2 projections differ because `schema_version` participates in canonical bytes. | `V-ACI-CANON-001` vs `005` |
| `test_integer_zero_and_negative_zero_inputs_emit_zero` | Raw JSON integer `0` and `-0` both project to the shortest integer spelling `0`. | `V-ACI-CANON-006` |
| `test_decimal_float_nonfinite_and_integer_overflow_fail_closed` | Execute raw inputs against their target schemas and match the declared stage/code before sealing. | `R-ACI-CANON-001-json-float-for-decimal`, `R-ACI-CANON-002-int64-overflow`, `R-ACI-CANON-006-nonfinite-decimal` |
| `test_timestamp_timezone_and_millisecond_precision_fail_closed` | Execute raw inputs and match timezone/precision stage and code; accepted values emit UTC milliseconds and `Z`. | `R-ACI-CANON-003-naive-timestamp`, `R-ACI-CANON-004-submillisecond-timestamp`; `V-ACI-CANON-004` |
| `test_unicode_normalization_collision_is_rejected` | A duplicate-pair-preserving raw loader exposes keys that collide after NFC; projection returns the declared code. | `R-ACI-CANON-005-nfc-key-collision` |
| `test_same_scoped_key_and_digest_returns_stored_receipt_without_write` | An identical retry returns the original receipt bytes and does not append events/effects. | First idempotency expectation; ACI-R5 |
| `test_same_scoped_key_with_different_digest_is_permanent_conflict` | Null/omitted mutation under the same key returns `IDEMPOTENCY_CONFLICT` and writes nothing. | Second idempotency expectation; ACI-R5 |
| `test_same_digest_under_different_idempotency_key_is_independent` | Digest equality does not merge two different command identities. | Third idempotency expectation; ACI-R5 |

## SQLite acceptance, CAS and crash matrix

Each test below runs with `journal_mode=WAL`, `synchronous=FULL`, `foreign_keys=ON` and bounded busy
handling. Failpoints are injected at every named boundary; assertions inspect a newly opened
connection after simulated process death, not the failed writer's connection.

| Executable test name | Required setup and assertion |
|---|---|
| `test_command_acceptance_crash_before_begin_leaves_no_members` | Crash before `BEGIN IMMEDIATE`; receipt, events, head delta and effect intents are all absent. Same key/digest retry succeeds once. |
| `test_command_acceptance_crash_after_each_member_before_commit_rolls_back_all` | Crash after each receipt/event/head/intent SQL mutation but before commit; a fresh connection observes none of the four acceptance members. |
| `test_command_acceptance_crash_after_commit_returns_stored_receipt_on_retry` | Crash after commit and before response; all four members exist and the retry returns byte-identical stored receipt with no new offset/effect. |
| `test_two_commands_at_same_expected_version_have_exactly_one_cas_winner` | Race two distinct commands at one aggregate version; one commits, one returns `VERSION_CONFLICT`, and versions remain contiguous. |
| `test_prerequisite_head_change_rejects_start_without_partial_writes` | Advance a prerequisite after command construction; target event, receipt and effect are absent. |
| `test_effect_outcome_crash_before_commit_is_all_or_none` | Fail after each terminal receipt/event/head/intent update; before commit none survive, after commit all survive. |
| `test_effect_outcome_retry_compares_terminal_digest_before_epoch_guard` | Lost-response same-digest retry returns stored receipt after status became terminal; different digest returns `OUTCOME_CONFLICT`. |
| `test_sqlite_busy_never_returns_false_receipt` | Hold the writer lock beyond the bounded policy; command returns the declared retryable busy result and no receipt/event/head/effect is visible. |

## Startup, migration, corruption and replay

| Executable test name | Required setup and assertion |
|---|---|
| `test_writer_startup_rejects_non_wal_non_full_or_foreign_keys_off` | Mutate each required pragma independently; startup fails closed before admitting a command. |
| `test_writer_startup_requires_busy_timeout_exactly_5000` | Assert the effective `PRAGMA busy_timeout` is exactly `5000`; zero, shorter, longer or silently defaulted values fail startup before admitting a command. |
| `test_writer_startup_rejects_unknown_or_checksum_mismatched_migration` | Present a newer unknown version and a known version with changed checksum; both block writes and replay. |
| `test_every_digest_column_rejects_bad_prefix_uppercase_nonhex_and_length` | Parameterize every canonical digest/hash column; reject missing/wrong prefix, uppercase hex, non-hex suffix, 63/65 hex and otherwise well-sized malformed values. |
| `test_writer_startup_rejects_missing_required_constraint_or_index` | Remove each authoritative PK/UNIQUE/FK/CHECK/partial index named by the accepted ADR; startup fails closed. |
| `test_corrupt_database_fails_closed_without_projection_repair` | Use a deterministic corrupt-database fixture; no event is skipped and no projection/log is promoted to authority. |
| `test_replay_from_zero_reproduces_head_hash_without_external_calls` | Fold the full event prefix and match aggregate version/state hash while provider, tool, clock, appender, upload and randomness spies remain at zero calls. |
| `test_replay_from_each_verified_checkpoint_matches_zero_replay` | Every valid compatible checkpoint plus suffix produces the same result as replay from zero. |
| `test_replay_rejects_gap_hash_schema_or_reducer_mismatch` | Independently mutate aggregate-version contiguity, payload/schema digest, checkpoint hash and reducer version; replay quarantines/fails closed. |
| `test_replay_global_offsets_are_monotonic_not_required_dense` | Rolled-back allocation cannot create an accepted event; consumers order committed offsets monotonically and do not require arithmetic density. |

## Constrained SQL records and immutability

These are TASK-010 test obligations for the complete accepted schema surface. Executing the
non-production SQL fixture during W0 can review constraint feasibility, but only implementation
tests attached to TASK-010 may claim runtime proof.

| Executable test name | Required setup and assertion |
|---|---|
| `test_attempt_partial_winner_allows_retries_and_only_one_accepted_result` | Insert multiple `(operation_id, attempt_no)` retry rows with `accepted_result=0`; permit exactly one row with `accepted_result=1`, reject a second winner and reject duplicate attempt number/ID. |
| `test_candidate_active_and_official_logical_keys_are_mutually_exclusive` | The partial index admits at most one active candidate per group/seat/round/type; an official message permanently blocks every later candidate for that key. |
| `test_candidate_update_requires_one_step_terminal_cas_and_immutable_identity` | Reject identity/content/key mutation, version jumps, terminal-to-terminal/reopen transitions and nonterminal updates; admit exactly one `active -> officially_accepted|abandoned` transition with `candidate_version + 1`. |
| `test_candidate_official_acceptance_and_abandonment_race_has_one_winner` | Race the two legal terminal updates from one active version; exactly one wins and the losing update cannot later revive or replace the candidate. |
| `test_publication_receipt_requires_exact_candidate_match_and_is_immutable` | Mutate each candidate equality field on insert and reject; after valid insert, reject UPDATE and DELETE so stored canonical bytes cannot diverge. |
| `test_official_message_requires_accepted_candidate_match_and_is_immutable` | Reject a message from active/abandoned candidate or mismatched logical/payload/event fields; after a valid accepted insert, reject UPDATE and DELETE. |
| `test_reveal_manifest_group_round_and_reveal_event_are_unique` | Reject duplicate manifest ID, duplicate `(group_aggregate_id, round_id)`, duplicate reveal event and dangling event reference. |
| `test_reveal_entries_reject_duplicate_ordinal_message_and_dangling_references` | Enforce manifest-scoped ordinal and message uniqueness plus manifest/message FKs; hashes must satisfy the canonical digest contract. |
| `test_reveal_manifest_and_entries_are_frozen_after_insert` | Reject UPDATE and DELETE of a manifest or entry, including membership, ordinal, message hash, payload hash and manifest hash mutations. |
| `test_usage_observation_preserves_missing_null_semantics_and_is_immutable` | Nullable provider/model/attempt and counters stay missing/null rather than becoming zero; reject negative counters, dangling event/attempt, invalid raw JSON, UPDATE and DELETE. |
| `test_usage_rollup_keys_source_offset_and_missing_counts_are_persistent` | Enforce the complete rollup PK and source offset FK; reject negative observations, invalid counter/missing-count JSON and duplicate semantic snapshots while preserving missing-count dimensions. |
| `test_pricing_source_validates_applicability_currency_digest_and_is_immutable` | Enforce provider/model/effective interval, uppercase three-letter currency, unique canonical digest and optional artifact FK; reject UPDATE/DELETE after insertion. |
| `test_cost_calculation_requires_matching_pricing_digest_currency_and_scope` | Require an existing applicable pricing source with exact digest/currency and exactly one usage-event or rollup scope; reject dangling scope/source/offset and mismatches. |
| `test_cost_calculation_is_immutable_and_cannot_diverge_from_pricing_source` | After valid calculation insertion, reject UPDATE/DELETE of quantity, price, currency, pricing/calculation digest or source; source immutability prevents later divergence. |
| `test_runtime_projection_primary_key_cursor_and_disposable_rebuild_are_non_authoritative` | Enforce `(projection_name, projection_key)` and valid `last_offset`; deleting/rebuilding projections changes no receipt/event/head/intent and invokes no effect. |

## Exit evidence for SWU-ACI-001

Reviewers may accept this W0 fixture when its JSON and every raw input parse with a duplicate-key-
preserving loader, every declared byte length and prefixed SHA-256 is recomputed independently,
every rejection identifies a target schema/stage/code, all test names are unique, and the accepted
persistence ADR references the same policies. This does not pass TASK-010, prove production SQLite,
change the runtime gate or authorize an adapter/provider. TASK-010 must attach executable results
for every name above.
