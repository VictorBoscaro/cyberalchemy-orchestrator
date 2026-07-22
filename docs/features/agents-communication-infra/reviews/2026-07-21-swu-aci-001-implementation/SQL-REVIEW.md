---
feature: agents-communication-infra
review_date: 2026-07-21
scope: SWU-ACI-001
axis: sqlite-correctness-and-enforceability
verdict: FIX
review_set_sha256: 35e54db2591fc2aa88f19345f91209e7ed99a379bf06dd3dc534daf78dfbf946
runtime_gate: block
---

# SWU-ACI-001 SQLite review

## Verdict

**FIX.** The four files match the immutable baseline, and the fixture executes successfully on a
file-backed SQLite database with the required core pragmas. The executable schema nevertheless does
not yet enforce all of the persistence contract it claims to freeze. This review is read-only with
respect to the implementation artifacts and does not promote any gate.

## Baseline verification

The independently recomputed file hashes are:

| Artifact | SHA-256 | Result |
|---|---|---|
| `ADR-001-persistence-replay-and-canonical-contracts.md` | `98c4a0713b554317dcd79862415fcb12a9b3d69949f7a3b8033c377c470c97f0` | match |
| `canonical-contract-vectors.json` | `a7d414c4fb684d73de43d46afdb77ff1b9fd138c8e02daffeaa5278e5ca9d204` | match |
| `SWU-ACI-001-TEST-PLAN.md` | `e8aa44eca8b666c367183b845426e675c1837a7974d7d9c043fe5d1ac032734a` | match |
| `slice0-schema.sql` | `fc6dfd222f82b22c542719626bd2bef08a8a1bef96a079e0abd3c01f3c5eca47` | match |

Recomposing `SHA256(UTF8(join(path=lowercase_sha256, LF)))` produced
`35e54db2591fc2aa88f19345f91209e7ed99a379bf06dd3dc534daf78dfbf946`, matching
`BASELINE.md`.

## Executed evidence

The schema was applied to a newly created file-backed database using Python's SQLite 3 binding.
Observed values were `journal_mode=wal`, `synchronous=2`, `foreign_keys=1`, `quick_check=ok`, and
`PRAGMA foreign_key_check` returned no rows before or after seeding the deferred
receipt/event/artifact cycles. This confirms that the cyclic core graph is executable atomically;
the cycles themselves are not a finding.

Positive constraints also behaved as intended: inserting a new candidate directly onto a logical
key already owned by an official message was rejected by
`publication_candidate_rejects_official_logical_key`.

## Material findings

### SQL-1 — Required constrained records are absent

`slice0-schema.sql` creates only `schema_migrations`, `artifacts`, `command_receipts`, `events`,
`aggregate_heads`, `effect_intents`, `publication_candidates`, `publication_receipts` and
`messages`. It omits the required `attempts`, `reveal_manifests`, `reveal_manifest_entries`,
`usage_observations`, `runtime_projections`, `pricing_sources`, `usage_rollups` and
`cost_calculations` records from persistence section 3. In particular, there is no database
constraint for `UNIQUE(operation_id) WHERE accepted_result = 1`, no manifest ordinal/message
uniqueness or reveal FKs, and no persistent usage/source-offset/pricing relationship.

This contradicts ADR-001 lines 163–166, which require the executable schema to include the
constrained records and indexes from persistence section 3, explicitly including attempt-winner
uniqueness and foreign keys. The test plan also contains no executable candidate/message/receipt,
attempt-winner, reveal-manifest or usage/pricing constraint matrix corresponding to persistence
acceptance fixtures 13 and 16–20.

Required fix: add the declared tables, authoritative keys, partial unique indexes, FKs and minimum
lookup indexes, then add adversarial tests for duplicate attempt winners, duplicate/dangling reveal
entries, missing usage dimensions/source offsets and incompatible/missing pricing. If any record is
intentionally outside Slice 0, narrow ADR-001 and persistence-and-replay explicitly instead of
claiming the broader executable contract.

### SQL-2 — INSERT-only triggers allow authoritative rows to diverge through UPDATE

The official-logical-key and equality triggers run only `BEFORE INSERT`. In an executed adversarial
case, an active candidate first inserted under another `message_type` was subsequently updated onto
the logical key of an existing official `messages` row. SQLite accepted the update. After creating
a matching `publication_receipts` row and an official `messages` row, SQLite also accepted:

- changing the candidate's `receipt_bytes`, making it disagree with its persisted receipt; and
- changing the accepted candidate's `payload_hash`, making it disagree with its official message.

`PRAGMA foreign_key_check` remained empty after all three mutations because the composite FKs do
not cover every field compared by the INSERT triggers. Thus the schema does not enforce the stated
rules that an official key prevents every later candidate, that receipt lookup is a field-for-field
view of its candidate, and that an official message exactly matches its accepted candidate.

Required fix: make identity/logical/payload/receipt fields immutable after creation or add equivalent
`BEFORE UPDATE` guards. Candidate state transitions must also preserve a monotonic CAS version and
legal one-way `active -> officially_accepted|abandoned` winner semantics. Add update-based
adversarial cases alongside the existing insert cases.

### SQL-3 — Digest checks accept values outside canonical lowercase SHA-256

The executable checks generally enforce only length 71 and the `sha256:` prefix. An executed insert
of `sha256:` followed by 64 uppercase `Z` characters into `schema_migrations.migration_checksum`
was accepted. The same incomplete pattern is used for artifact, command, event, payload, outcome
and receipt digests/hashes.

This violates ADR-001's lowercase 64-hex migration and acceptance digest contract. Required fix:
apply a complete character-class check such as the ADR's `NOT GLOB '*[^0-9a-f]*'` suffix rule to
every canonical SHA-256 field, and add negative tests for uppercase and non-hex characters.

### SQL-4 — Startup policy coverage omits the effective busy timeout

ADR-001 requires startup to set and verify `busy_timeout=5000`. The SQL fixture sets WAL, FULL and
foreign keys but not `busy_timeout`; the startup test checks only WAL/FULL/FK mismatch. The separate
lock-contention test proves bounded behavior only after a runtime exists and does not prove the
required effective startup value.

Required fix: include the exact effective busy-timeout assertion in the startup contract test (the
schema fixture may document or set it consistently with its non-production role).

## Closure conditions

A SQLite closure review can return `PASS` when a new immutable baseline demonstrates all of the
following:

1. the section-3 constrained records and indexes are present or the normative scope is explicitly
   and consistently narrowed;
2. INSERT and UPDATE adversarial paths cannot violate candidate/message/receipt authority;
3. every canonical digest column rejects uppercase and non-hex suffixes;
4. the test plan covers attempt, reveal, usage/pricing and the exact startup pragma policy; and
5. the complete schema still applies on a file-backed database with WAL/FULL/FK enabled and a clean
   `quick_check`/`foreign_key_check`.

## Closure review — final baseline

### Verdict

**FIX.** Closure was performed against `FINAL-BASELINE.md`, whose independently recomputed
composition is
`d6093473703ce1cf21353dff785ad69f7aa38f253980adfbcc0e21ded1ec014f`. Every artifact hash and the
composed hash match that baseline:

| Artifact | SHA-256 | Result |
|---|---|---|
| `ADR-001-persistence-replay-and-canonical-contracts.md` | `f13c2d746fff988fc238abc0dd41527b80d5c84a52b47de64dadc1b37a3fe911` | match |
| `canonical-contract-vectors.json` | `b29eba75b6bf157526e2c2fd60cc535d843b4c32298ccd81b1032dcb9130f8f1` | match |
| `SWU-ACI-001-TEST-PLAN.md` | `90bffe4b1414aaf5784dd07312aa2fb823feaefe18b0b6b265b17495f155f5f1` | match |
| `slice0-schema.sql` | `0eb809ab53c6c03d94fc112c19e845a2e400f30ad90c851c017e779d747c9b05` | match |

### Re-executed evidence

The final schema was applied to a new file-backed database. It reported `journal_mode=wal`,
`synchronous=2`, `foreign_keys=1`, `busy_timeout=5000` and `quick_check=ok`. A complete seeded graph
covering receipt/events, candidate/receipt/message, attempt, reveal, usage, pricing, rollup and cost
committed with an empty `foreign_key_check`.

The following adversarial operations were correctly rejected:

- uppercase/non-hex migration digest;
- moving or mutating a candidate outside its one-step terminal CAS, including a version jump;
- updating a publication receipt or official message;
- a second accepted attempt for one operation;
- duplicate/dangling reveal membership;
- negative usage counters; and
- cost rows with a mismatched digest or missing pricing source.

This closes SQL-2, SQL-3 and SQL-4 for the contract fixture. SQL-1 is only partially closed.

### Residual SQL-1 — schema and test-plan coverage remain incomplete

The added tables and indexes now cover attempts, reveal, usage, pricing, rollups and costs, but the
required `runtime_projections` table from persistence section 3.2 is still absent. More importantly,
`SWU-ACI-001-TEST-PLAN.md` still names no executable candidate/message/receipt, attempt-winner,
reveal-manifest, usage/rollup/pricing/cost or exact `busy_timeout=5000` contract tests. The first
review's closure condition 4 and persistence acceptance fixtures 13 and 16–20 therefore remain
unrepresented in the TASK-010 test inventory.

Required fix: add `runtime_projections` with `(projection_name, projection_key)` and `last_offset`
contract, and add named adversarial tests for every newly introduced table/constraint plus the exact
busy-timeout startup assertion.

### Residual SQL-5 — records declared frozen or immutable remain updateable

The remediation added correct INSERT constraints but no UPDATE guards for several records whose
normative contract is immutable. Executed updates to all of the following were accepted:

- `reveal_manifests.manifest_hash` and `reveal_manifest_entries.payload_hash`, despite the frozen
  reveal membership/hash contract;
- `usage_observations.input_tokens`, despite its immutable event-projection contract;
- `pricing_sources.pricing_digest` after a cost row referenced the source; and
- `cost_calculations.pricing_digest` and `currency`, despite cost calculations being immutable
  derived evidence.

The last two updates can leave the pricing source and calculation mutually divergent while
`PRAGMA foreign_key_check` remains empty because `cost_calculation_must_match_pricing_source` runs
only on INSERT and the FK covers only `pricing_source_id`.

Required fix: reject UPDATE/DELETE for frozen reveal, immutable usage, immutable pricing and
immutable cost rows, or provide an equivalent append-only mechanism that preserves the same
contract. Re-run both mutation and divergence cases in the named TASK-010 tests.

The final baseline remains W0 documentation/contract evidence only. This `FIX` does not alter
`runtime_gate=block` or authorize runtime implementation.

## Final closure — remediated final baseline

### Verdict

**PASS.** The updated `FINAL-BASELINE.md` closes every original and residual SQLite finding. Its
four file hashes independently match, and recomposing them produced
`70c2312b9ecd75bfa814ba9548fa11c3508b75a662fec42db3d29b71429b310b`, exactly the declared final
review-set digest.

| Artifact | SHA-256 | Result |
|---|---|---|
| `ADR-001-persistence-replay-and-canonical-contracts.md` | `5c932f4a41d9269a5750278f18f4908b24462d8b67068f36fa0c848e63391885` | match |
| `canonical-contract-vectors.json` | `b29eba75b6bf157526e2c2fd60cc535d843b4c32298ccd81b1032dcb9130f8f1` | match |
| `SWU-ACI-001-TEST-PLAN.md` | `ce3c78c1e79e69c911ce0c5d00d3e6feca41bc0f418eee2825652cd11a906267` | match |
| `slice0-schema.sql` | `72e644e9cfea36e7e6ca94240d0138d8508023e2d2f25acb3ed64b0a061c9be0` | match |

### Final executed evidence

The schema applied cleanly to a new file-backed database and reported `journal_mode=wal`,
`synchronous=2`, `foreign_keys=1`, `busy_timeout=5000`, `quick_check=ok` and an empty
`foreign_key_check` after a complete authority graph was committed.

The final adversarial run established:

- lowercase-hex digest enforcement rejects an uppercase/non-hex checksum;
- the partial attempt-winner index rejects a second accepted result;
- UPDATE and DELETE of reveal manifests/entries, usage observations, pricing sources and cost
  calculations are rejected by explicit immutability guards;
- rejected pricing/cost mutations leave source and calculation digest/currency equal, with a clean
  FK check;
- `runtime_projections` exists with its composite primary key and event-offset FK: duplicate and
  dangling rows are rejected, cursor advance is accepted, cursor regression is rejected, and
  deletion for rebuild is accepted; and
- the effective busy timeout is exactly 5000 milliseconds.

The executable test plan now contains 45 unique test names with no duplicates. It includes explicit
tests for the exact busy timeout, attempts, candidate/receipt/message rules, reveal uniqueness and
freeze, usage observations and rollups, pricing/cost immutability and consistency, and disposable
runtime projections. This closes the prior test-inventory residual.

No material SQLite correctness or enforceability finding remains within SWU-ACI-001's W0 contract
scope. This `PASS` accepts only the reviewed documentation/schema fixtures; it is not production
SQLite or runtime evidence and does not change `runtime_gate=block`.
