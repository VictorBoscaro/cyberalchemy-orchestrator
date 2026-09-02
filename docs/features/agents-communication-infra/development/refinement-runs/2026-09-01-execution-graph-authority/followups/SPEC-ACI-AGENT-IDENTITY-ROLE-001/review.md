# Review — SPEC-ACI-AGENT-IDENTITY-ROLE-001

Status: independent review complete.  
Verdict: **FIX**.  
`recheck_required: true`

## Coverage

| reviewer | lens | corpus and attacks | result |
|---|---|---|---|
| independent reviewer | provenance / authority | DraftGraph authorship, signed node assignment, pool/registry digests, final digest participation, stale/tamper/replay | one MAJOR finding; DraftGraph rejection and assignment-to-projection path otherwise survived |
| independent reviewer | mechanics / operability | real two-document pool, normalization errors, role registry, registrar/appender compatibility, fixtures and executable validator | three MAJOR findings |
| independent reviewer | ownership / governance | consumer-status ceiling, CRAFT/ledger state, implementation gate and historical-review preservation | no additional finding |

Every file in the new follow-up was read. The comparison corpus included the real agent pool,
`register-dispatch` skill/appender, current compiler/gate/tests, the predecessor DraftGraph and
ExecutionGraph proposals, the feature CRAFT/ledger, and the two historical reviews.

## Findings

### AIR-R1 — The proposed source-pool boundary cannot consume the real governed pool, and the work pack cannot perform its own atomic migration

- **Severity:** MAJOR
- **Files / evidence:**
  - `schemas/source-agent-pool.schema.json:5-11` requires exactly `schema`, `name`, `version`,
    `agents`: `"additionalProperties": false` and
    `"required": ["schema", "name", "version", "agents"]`.
  - `schemas/source-agent-pool.schema.json:18-31` also closes each entry to only one name spelling
    plus `role_fit`.
  - The real `telemetry/agents/agent-pool.yaml:2-23` is a two-document YAML: its metadata document
    starts with `profile: subagents-strategy`, while the roster document starts with `scientists:`;
    real entries such as `:26-31` also retain `field`, `era`, `cited` and `tags` around legacy
    `name` and `role_fit`.
  - `WORK-PACK.md:26-30` says to “atomically migrate that real YAML from legacy `name` to canonical
    `agent_name` and update all known consumers/tests”, but its declared write scope at `:12-19`
    excludes `telemetry/agents/agent-pool.yaml`, the registrar/appender, skill consumers and their
    generated copies.
- **Verification:** Loading the two real YAML documents with the proposed duplicate-key loader and
  passing either document to `normalize_pool` returned `DG_POOL_SCHEMA_INVALID`. The mismatch is
  broader than the intended incremental `name` rename: document topology and preserved roster
  metadata are also incompatible.
- **Required fix:** Specify the actual two-document pool adapter or a lossless versioned migration,
  including which metadata is preserved/projected; enumerate every affected consumer/generated
  copy/test; and put the real YAML plus those exact files in the implementation write scope so the
  migration can be atomic.

### AIR-R2 — Registry version/digest pinning does not enforce the declared initial set or immutable-version rule

- **Severity:** MAJOR
- **Files / evidence:**
  - `COMPILATION-DELTA.md:70-73` says: “Adding a role ... requires a new immutable role registry
    version and digest” and “Changing a registry in place is drift and must fail.”
  - `schemas/role-registry.schema.json:6-20` accepts any non-empty version and any array of
    syntactically valid role rows; it neither fixes the contents of version `1` nor requires unique
    `role_id` values.
  - `validate_artifacts.py:125-127` checks uniqueness only among enabled roles and requires only
    that `other` exists and `others` does not.
- **Verification:** Replacing unused `planner` with arbitrary enabled `hacker` while keeping registry
  name/version `aci.agent-roles/1`, then recomputing the registry and signed-context fixture digests,
  passed `validate_contract`. Appending a disabled duplicate `skeptic` row also passed. Thus the
  evidence proves only self-consistency with the supplied digest, not that version `1` denotes the
  owner-selected eight-role set or that a version cannot change in place.
- **Required fix:** Give the compiler/gate a trusted `(registry name, version) -> digest` authority
  or an equivalent immutable registry-resolution contract; freeze the exact v1 role set, reject
  duplicate IDs across enabled and disabled rows, and add negative vectors for in-place version
  mutation, duplicate IDs and disabled requested roles.

### AIR-R3 — The role registry is not the configuration source for the existing dispatch consumers, so `other` already fails and future roles still require code edits

- **Severity:** MAJOR
- **Files / evidence:**
  - `DECISION.md:19-22` declares the initial registry including singular `other`, and
    `COMPILATION-DELTA.md:69-76` presents registry replacement as the configurability boundary.
  - `.agents/skills/register-dispatch/append-dispatch.cjs:140` still defines
    `const AGENT_ROLES = ['explorer', 'synthesizer', 'skeptic', 'writer', 'auditor', 'planner',
    'coder'];`; `:389` rejects anything outside that constant.
  - `.agents/skills/register-dispatch/SKILL.md:78` and `:143` repeat the same seven-role enum for
    opening and close rows. Equivalent `.codex` and `.claude` copies remain hard-coded, as do
    `implementations/UI-CONTRACT.md:99` and enum-audit code.
  - `WORK-PACK.md:14-19` authorizes only the compiler, its tests, a pool loader, follow-up fixtures
    and later CRAFT/ledger; it contains no task to reconcile or deliberately separate these role
    consumers.
- **Verification:** Static appender validation makes `other` invalid today. Adding a registry role
  cannot make it acceptable without editing code and governed skill copies, contrary to the stated
  easy configuration boundary.
- **Required fix:** Either make the governed role registry the validated source for every role
  consumer that shares this vocabulary (including open/close rows and generated skill copies), or
  explicitly define a separate registrar-role vocabulary and a total mapping/boundary. Add `other`
  and future-version compatibility tests and extend the implementation write scope accordingly.

### AIR-R4 — The conformance suite does not exercise the load-bearing identity/evidence failures, and its stale/replay flags produce the wrong error class

- **Severity:** MAJOR
- **Files / evidence:**
  - `WORK-PACK.md:34-35` requires preserving “signature/digest verification across all new fields”,
    and `VALIDATION.md:33` claims “context evidence covers registry ref, pool ref and all node
    assignments”.
  - `schemas/allocator-evidence.schema.json:11-12` defines both `is_latest` and `pair_is_unbound` as
    `{"const": true}`. This prevents the semantic gate from classifying a stale allocation as
    `DG_IDENTITY_CONTEXT_STALE` or a replay/bound pair as `DG_AUTHORITY_CONFLICT`; they fail earlier
    as generic evidence-schema errors.
  - `validate_artifacts.py:254-257` says every semantic mutation models a freshly signed context,
    but merely rewrites `context_digest`; the fixture validator performs no signature check.
  - The complete manifest in `NEGATIVE-VECTORS.md:8-19` / `fixtures/negative-vectors.json:4-15`
    contains only AIR-N01..N12. It omits same-value dual spelling, empty/non-string names, duplicate
    YAML keys, unknown keys, legacy `name`, forged signature, assignment tamper with stale evidence,
    false `is_latest`, false `pair_is_unbound`, registry replay/version reuse, unknown pool member,
    invalid override reason and duplicate assignment keys.
- **Verification:** The declared 12/12 vectors pass. Independently setting `is_latest=false` or
  `pair_is_unbound=false` yielded `DG_ALLOCATOR_EVIDENCE_INVALID`, confirming that the intended
  stale/conflict branches are structurally unreachable in this proposal. Loader probes showed the
  omitted normalization cases currently reject, but they have no manifest regression protection;
  cryptographic tamper/replay is explicitly outside this validator.
- **Required fix:** Keep these flags boolean and test the semantic stale/conflict codes; add exact
  negative vectors for the omitted normalization, assignment, signature, drift and replay cases;
  and require the successor implementation tests to verify that changing any assignment or pinned
  ref without a valid new allocator signature fails before compilation emits graph bytes/digest.

## Artifact verdicts

| artifact group | verdict | rationale |
|---|---|---|
| decision, compilation delta, schemas, fixtures, validator and implementation work pack | **FIX** | AIR-R1 through AIR-R4 are load-bearing contract or integration gaps |
| `FIELD-OWNERSHIP.md` | **KEEP** | it correctly separates `compiler-only` from `projected`, states runtime ingestion is absent, and does not repeat the 105/105 runtime-consumer claim |
| feature `CRAFT.md` and `.craft/ledger.yml` | **KEEP** | owner decision is closed, current compiler is marked stale, the delta remains candidate/unreviewed, and runtime/OPEN stay blocked; no promotion claim was found |

## Checks

| check | result |
|---|---|
| `python validate_artifacts.py` | PASS: positive projection and declared 12/12 vectors; scope limit printed |
| `python -m py_compile validate_artifacts.py` | PASS |
| Draft 2020-12 schema meta-validation exercised by validator | PASS for all loaded schemas |
| real pool through proposed normalization boundary | FAIL as expected for review: both YAML documents return `DG_POOL_SCHEMA_INVALID` |
| same-version registry mutation `planner -> hacker` with recomputed refs | unexpectedly PASS; supports AIR-R2 |
| disabled duplicate `role_id=skeptic` | unexpectedly PASS; supports AIR-R2 |
| evidence `is_latest=false` / `pair_is_unbound=false` | `DG_ALLOCATOR_EVIDENCE_INVALID` / `DG_ALLOCATOR_EVIDENCE_INVALID`; supports AIR-R4 |
| feature ledger parse and `indexes.by_id` resolution | PASS: 114/114 index targets resolve |
| `git diff --check` over CRAFT, ledger and follow-up | PASS; LF/CRLF warnings only |
| historical review hashes | PASS: SPEC `E70B8D68...B2F3D94`; IMPL `7083B3E2...28A13984` |
| toy names/role-fit against real pool | PASS: Popper/skeptic, Dijkstra override to coder, Lamport/auditor are grounded |

## Change requests

1. **MAJOR** — Make the real two-document agent pool and its atomic consumer migration executable
   within the declared work scope.
2. **MAJOR** — Add an immutable registry trust anchor and freeze/validate the exact v1 role set.
3. **MAJOR** — Reconcile the registry with registrar/appender and all shared role consumers, including
   `other` and future version changes.
4. **MAJOR** — Complete negative coverage and preserve typed stale/tamper/replay semantics through
   the signed-context gate.

`exit_reason: resolved`; `agents_spawned: 0`; this reviewer was independent of the worker and did
not modify any reviewed target.

---

## Recheck 1 — repaired candidate

Frozen predecessor review SHA-256 before this append:
`FDE04552C23478714A9922A7986FB7EC113EB2BA92D4CE124224C41ECC797BD4` — **MATCH**.

Verdict: **FIX**.  
`recheck_required: true`

### Original finding disposition

| finding | status | recheck evidence |
|---|---|---|
| AIR-R1 — real pool boundary and atomic migration | **PARTIALLY RESOLVED** | The repaired adapter verifies the actual two-document, 414-row v0.6 bytes and preserves row order/non-identity data, but the exact implementation scope still omits live telemetry components required by the new row contract; see AIR-R5. |
| AIR-R2 — immutable v1 registry | **RESOLVED** | Trusted `(name,version)->digest`, exact ordered eight-role schema and typed missing/extra/duplicate/disabled/substitution checks now reject the original attacks. |
| AIR-R3 — shared configurable role consumers | **PARTIALLY RESOLVED** | Registrar/MCP/UI migrations are planned, but a structural pool enum still blocks a future accepted role and live row producers/readers remain outside the exact scope; see AIR-R5 and AIR-R6. |
| AIR-R4 — evidence and negative conformance | **RESOLVED** | Ed25519 verification and reachable typed tamper/signature/replay/stale/conflict branches pass; the 37 declared vectors return exact codes/paths. Remaining unmanifested attacks are MINOR coverage residue in AIR-R7. |

### Recheck findings

#### AIR-R5 — The telemetry schema migration omits live row producers/readers from its exact atomic scope

- **Severity:** MAJOR
- **Files / evidence:**
  - `DECISION.md:32-35` requires preserving legacy versioned validation while “new open/close rows”
    pin the accepted role-registry ref.
  - `WORK-PACK.md:24-39` labels its list “Registry, compiler, registrar and shared consumers” but
    names `dispatch_workflow.py` and selected tests without
    `implementations/server/runtime/host_dispatch_hook.py`,
    `implementations/server/runtime/legacy.py`,
    `implementations/contracts/dispatch-type-registry.v1.json`, or
    `implementations/tests/runtime/test_host_dispatch_hook.py`.
  - `host_dispatch_hook.py:358-443` is a live opening-row producer: it creates a record carrying
    `schema_version` at `:410`; its close-row producer at `:632-645` likewise emits no registry ref.
  - `legacy.py:14` permits only opening contracts `0.6.1` through `0.6.4`; `:112-116` rejects every
    other opening schema. The canonical dispatch-type registry still declares
    `"ledger_schema_version": "0.6.4"` at
    `implementations/contracts/dispatch-type-registry.v1.json:3`.
- **Verification:** A new versioned row shape cannot both require a pinned registry ref and traverse
  the current host-hook → appender → strict legacy-snapshot path unless these components migrate
  together. Keeping `0.6.4` while changing its required fields would silently redefine a historical
  schema; bumping it without `legacy.py` support blocks runtime acceptance. The catch-all at
  `WORK-PACK.md:42-43` mentions newly discovered pool/role readers, but does not make these concrete
  telemetry schema producers/readers part of the otherwise exact write scope.
- **Required fix:** Add the host hook, strict legacy resolver, canonical dispatch-type registry (or
  its explicitly selected successor), `test_host_dispatch_hook.py`, and any directly affected
  resolver tests to the atomic write scope; specify the new opening/close schema version and prove
  old rows still resolve while every new host/workflow opening and close pins the same registry ref.

#### AIR-R6 — The canonical pool schema hard-codes v1 roles and defeats registry-driven future configuration

- **Severity:** MAJOR
- **Files / evidence:**
  - `DECISION.md:26-29` requires future roles to come through a new accepted registry and says shared
    consumers must resolve it “rather than embed seven-role constants”.
  - `COMPILATION-DELTA.md:45-48` says an accepted future role does not require editing each
    consumer's source enum; `WORK-PACK.md:75` strengthens this to “not source enum edits”.
  - `schemas/source-agent-pool.schema.json:38-40` nevertheless embeds exactly
    `explorer|synthesizer|skeptic|writer|auditor|planner|coder|other` in `$defs.role`.
  - `validate_artifacts.py:157-164` first admits `role_fit` against the dynamically supplied
    `allowed_roles`, then revalidates against that fixed schema enum.
- **Verification:** Adding synthetic accepted role `hacker` to `allowed_roles` and using it in a
  canonical pool entry passed the semantic registry check but failed afterward with
  `DG_POOL_SCHEMA_INVALID` at `$.documents[1].scientists[0].role_fit[0]`. A future role therefore
  still requires editing this source enum.
- **Required fix:** Make the pool schema structural for role IDs and keep closure in the accepted
  registry semantic check; add a positive future-registry/role-fit vector proving consumer source
  enums do not change, while an unaccepted string still returns `DG_ROLE_UNKNOWN`.

#### AIR-R7 — Three explicitly requested authority attacks are executable but absent from the manifest

- **Severity:** MINOR
- **Files / evidence:**
  - `NEGATIVE-VECTORS.md:3-14` claims the executable 37-vector manifest pins error code/path across
    pool authority and registry immutability.
  - `fixtures/negative-vectors.json` has metadata drift and registry mutation/version attacks, but
    no vector for raw-only source substitution, role-row reorder, or registry-name substitution.
- **Verification:** Independent attacks reached the correct failures:
  `DG_POOL_SOURCE_SUBSTITUTION @ $.yaml`,
  `DG_ROLE_REGISTRY_SCHEMA_INVALID @ $.roles[0]`, and
  `DG_ROLE_REGISTRY_UNTRUSTED @ $.name`.
- **Required fix:** Add these attacks to the executable manifest so the already-correct mechanics
  receive exact regression coverage.

#### AIR-R8 — CRAFT and ledger preserve the authority ceiling but report the superseded vector count

- **Severity:** MINOR
- **Files / evidence:**
  - `CRAFT.md:38-42` still says the candidate contains “12 negative vectors”.
  - `.craft/ledger.yml:322` repeats “12 negative vectors”, while repaired `VALIDATION.md:11` records
    `37/37`.
- **Verification:** Ledger parses and all 114 indexed IDs resolve; the compiler remains explicitly
  stale, the artifact remains `candidate`, and runtime/OPEN remain blocked. This is factual drift,
  not an authority promotion.
- **Required fix:** Update only the candidate evidence count/status wording after the next recheck;
  retain the stale-compiler and blocked-runtime ceiling.

### Recheck checks

| check | result |
|---|---|
| frozen prior review hash | PASS: exact `FDE04552...797BD4` before append |
| `python validate_artifacts.py` | PASS: schemas, Ed25519, singular `other`, real 414-row migration, 37/37 exact vectors |
| `python -m py_compile validate_artifacts.py` | PASS |
| real source raw/metadata authorities | PASS: `5c7b9745...99eba` / `85ed11d7...095bc` |
| v0.6 → v0.7 row order and all non-identity fields | PASS across 414/414 rows |
| raw-only source substitution | PASS: rejected `DG_POOL_SOURCE_SUBSTITUTION @ $.yaml` |
| registry reorder / name substitution | PASS: rejected with exact paths; missing manifest coverage noted in AIR-R7 |
| synthetic accepted future role in pool `role_fit` | FAIL: fixed schema enum returns `DG_POOL_SCHEMA_INVALID`; supports AIR-R6 |
| direct-consumer search | FAIL for exact scope: live `host_dispatch_hook.py`/`legacy.py` path omitted; supports AIR-R5 |
| feature ledger parse/index | PASS: 114/114 index targets resolve |
| `git diff --check` over CRAFT, ledger and repaired follow-up | PASS; LF/CRLF warnings only |
| historical predecessor review hashes | PASS: SPEC `E70B8D68...B2F3D94`; IMPL `7083B3E2...28A13984` |

### Evidence boundary

Production pool, compiler, registrar, appender, telemetry and runtime remain unchanged by this
specification repair. The successful harness proves a proposed fixture contract, not production
migration, runtime ingestion or dispatch execution. CRAFT/ledger correctly keep the compiler stale
and runtime blocked despite their MINOR vector-count drift.

`exit_reason: resolved`; `agents_spawned: 0`; independent reviewer; no target fixes applied.

---

## Recheck 2 — AIR-R5 through AIR-R8 repair

Frozen predecessor review SHA-256 before this append:
`303056E6212AEE86C8AFD48A014108AA6C6162B4410573464F08207119509B31` — **MATCH**.

Verdict: **FIX**.

`recheck_required: true`

### Original finding disposition

| finding | status | recheck evidence |
|---|---|---|
| AIR-R5 — exact atomic telemetry scope | **PARTIALLY RESOLVED** | The work pack now includes the host dispatch/ingestion hooks, strict legacy resolver, dispatch-type registry successor, runtime-package successor, bridge, service, provenance and their named tests. Live v1/0.6.4 selectors remain outside the exact scope; see AIR-R9. |
| AIR-R6 — structural source-pool role IDs | **RESOLVED** | `source-agent-pool.schema.json` now constrains role IDs only by shape. An illustrative unaccepted v2 carries `researcher` through the unchanged schema, while registry v1 rejects it semantically. |
| AIR-R7 — missing authority attacks | **RESOLVED** | AIR-N39 through AIR-N41 now execute raw-source substitution, v1 row reorder and registry-name substitution with exact codes and paths. |
| AIR-R8 — stale vector count | **RESOLVED** | The package, feature CRAFT state and feature ledger now consistently report 41 vectors; no superseded 12/37 count remains outside immutable prior review text. |

### Recheck findings

#### AIR-R9 — The “exact” v2 migration scope still omits live registry/package selectors and a runtime opening producer

- **Severity:** MAJOR
- **Files / evidence:**
  - `WORK-PACK.md:13-53` calls the list “Exact implementation write scope” and includes the v2
    dispatch registry/package, row hooks, appender copies and selected runtime tests. Its catch-all
    at `:55-57` covers only newly discovered pool or shared-role readers.
  - `tools/install-register-dispatch-runtime.ps1:83` hard-codes
    `register-dispatch-runtime-package.v1.json`; `:101-115` admits only the v1 package/registry
    schemas, and `:121-125` requires the v1 registry file. The new v2 package cannot be selected,
    checked or installed through the repository's installer, yet this script is absent from the
    work pack.
  - `.agents/skills/domainspec-subagents-strategy/SKILL.md:46-49`,
    `.codex/skills/domainspec-subagents-strategy/SKILL.md:46-49`, and
    `.claude/skills/domainspec-subagents-strategy/SKILL.md:45-48` still call
    `dispatch-type-registry.v1.json` the sole live type authority. These installed operational
    instructions are also absent from the scope.
  - `implementations/server/runtime/confirmation.py:673-680` and `:721-732` produce the
    runtime-managed audit-opening effect/request with `appender_contract_version: "0.6.4"`.
    `implementations/tests/runtime/test_runtime_confirmation.py:14-15` exercises that producer;
    neither file is listed.
- **Verification:** Repository-wide source search over dispatch registry/package paths,
  `ledger_schema_version` and `appender_contract_version` found these live selectors outside the
  declared SWU. A v2 manifest would remain uninstallable by the canonical installer, route-facing
  skill text would continue selecting v1, and runtime confirmation would continue requesting the
  0.6.4 appender contract. Thus the plan does not yet guarantee that every new write selects the
  0.7.0 opening/close contract while the v1 branch remains immutable.
- **Required fix:** Add the installer, all three route-strategy skill copies, confirmation producer
  and its focused tests/fixture successor to the atomic scope. Specify one version-selection rule
  that installs/resolves v2 for new writes, retains v1 for historical verification, and proves no
  0.7 opening or close is emitted through a 0.6.4 effect/package selector.

#### AIR-R10 — Closed governance still disagrees on whether `agent-name` is a permanent accepted alias

- **Severity:** MAJOR
- **Files / evidence:**
  - `DECISION.md:9-18` says canonical v0.7 uses only `agent_name`, that `agent-name` is not a second
    permanent alias, and that steady-state loading rejects it.
  - `CRAFT.md:124-129`, under the closed decision `DEC-ACI-AGENT-IDENTITY-ROLE-001`, instead says:
    “A boundary loader accepts YAML `agent_name` or `agent-name`, normalizes it”.
  - `.craft/ledger.yml:704` repeats that the owner selected “YAML agent_name or agent-name as the
    display-name source”.
- **Verification:** This is not stale count/status wording: it is a contradictory accepted-input
  boundary in the feature's closed governance surfaces. Implementing the DECISION rejects
  `agent-name`; implementing CRAFT/ledger accepts it indefinitely.
- **Required fix:** Record the owner-selected canonical spelling once and align DECISION, CRAFT and
  ledger before implementation. If `agent_name` is canonical, remove the `or agent-name` claims;
  if both are intended, revise the schemas, negative vectors and migration contract explicitly
  rather than letting an implementation worker choose.

### Recheck checks

| check | result |
|---|---|
| frozen prior review hash | PASS: exact `303056E6...09B31` before append |
| `python validate_artifacts.py` | PASS: positive projection, Ed25519, singular `other`, structural future role, real 414-row migration and 41/41 exact negative vectors |
| Draft 2020-12 meta-validation | PASS: all 10 schemas |
| `python -m py_compile validate_artifacts.py` | PASS; generated cache removed after the check |
| vector manifest/dispatcher closure | PASS: 41 unique sequential IDs; all 38 distinct operations are listed and supported; no supported unlisted operation |
| v1 registry authority attacks | PASS: wrong order, name and same-version digest substitution rejected at exact typed paths |
| role-version boundary | PASS: `researcher` under v1 is rejected; illustrative v2 is untrusted by v1 authority but traverses the structural pool schema when supplied only as an illustrative semantic set |
| real raw-source substitution | PASS: `DG_POOL_SOURCE_SUBSTITUTION @ $.yaml` |
| telemetry contract prose | PASS: DECISION/delta/work pack consistently require identical refs on 0.7 opening/close and reject missing, mixed or mismatched pairs; this is planned, not implemented |
| scope-completeness search | FAIL: installer, route-strategy copies, confirmation producer and confirmation test omitted; supports AIR-R9 |
| focused immutable-legacy checks | PASS: accepted opening versions remain 0.6.1–0.6.4; existing open/close route-digest and strict legacy-close checks passed |
| broader selected production regression | NOT GREEN: 19 tests ran with 5 failures and 1 error in existing handoff/manifest behavior; no failure was caused or repaired by this spec recheck |
| feature ledger parse/index | PASS: 114/114 index targets resolve |
| CRAFT/ledger vector count and candidate/block status | PASS; alias-governance contradiction separately fails AIR-R10 |
| repaired-target final newline/trailing whitespace audit | PASS excluding immutable `review.md` |
| stale vector-count scan | PASS outside immutable prior review text |
| `git diff --check` over CRAFT, ledger and follow-up | PASS; LF/CRLF warnings only |

### Evidence boundary

The executable corpus proves a specification-fixture contract only. It does not implement telemetry
schema 0.7.0, a dispatch-type registry/package v2, runtime installation, registrar migration,
production pool migration, allocator service, or ExecutionGraph ingestion. The dirty worktree also
contains pre-existing production changes, so author attribution for “production untouched” cannot
be derived from `git status`; this reviewer changed no production target. The feature artifact
remains `candidate`, the compiler remains stale, and confirmation/runtime execution remain blocked.

`exit_reason: resolved`; `agents_spawned: 0`; independent reviewer; no target fixes applied.

---

## Recheck 3 — AIR-R9 and AIR-R10 repair

Frozen predecessor review SHA-256 before this append:
`FF27533D10B5D0DDD3190C3E5D0928185470182D3ED7F708B3BA416DCD8F68A1` — **MATCH**.

Verdict: **KEEP**.

`recheck_required: false`

### Original finding disposition

| finding | status | recheck evidence |
|---|---|---|
| AIR-R9 — omitted live v2/package selectors | **RESOLVED** | `MIGRATION-SURFACE.md` classifies the full bounded hit set, and `WORK-PACK.md:24-67` now includes the installer, all three route-strategy copies, confirmation producer/test, a new confirmed-dispatch-v2 fixture, registry/package successors, appender copies, row producers/readers and directly affected tests. Tasks `:81-93` make v2/0.7.0 the new-write default, retain v1 only for explicit legacy verification, and reject 0.7.0 output through a 0.6.4 selector. |
| AIR-R10 — canonical spelling governance conflict | **RESOLVED** | `CRAFT.md:126-130` and `.craft/ledger.yml:700-708` now agree with `DECISION.md:9-18`: canonical v0.7 uses only `agent_name`, and `agent-name` is rejected rather than retained as an alias. |

### Coverage and zero-findings defence

| lens | attack | why no finding survived |
|---|---|---|
| mechanics / correctness | Repeated file-level searches for 0.6.4, registry/package v1 selectors, role literals and governed-pool consumers; compared every active hit to the exact work scope. | All 28 selector/version hits are classified. Removing two immutable v1 authorities and five frozen experiment files leaves 21 active/test files, all named by the work pack. The broad role search found 14 files: one frozen L0 oracle plus 13 active files; the six registrar copies and four shared-role consumers migrate, while the three Refine generators demonstrably write a distinct `subagent_strategy.roles[].role_id` vocabulary. All seven direct governed-pool code/test/doc consumers are in scope. |
| ownership / reference integrity | Traced installer → runtime package → dispatch registry → route instructions/appender → confirmation/hook/workflow → bridge/strict resolver/service/provenance. | `MIGRATION-SURFACE.md:11-22`, `WORK-PACK.md:26-62`, and `FIELD-OWNERSHIP.md:31-34` now name every load-bearing selector/producer/consumer and its required change. The new `confirmed-dispatch-v2/` is additive; v1 fixture/registry/package artifacts stay immutable. |
| abuse / gaming | Attempted to route a 0.7 opening/close/effect/request through a 0.6.4 package selector, silently use v1 as the default, mix legacy/new pairs, or retain `agent-name` as a compatibility alias. | `MIGRATION-SURFACE.md:55-65` and `WORK-PACK.md:81-100` require explicit legacy-v1 selection, prohibit it from authorizing new rows, require identical role refs across every 0.7 artifact, reject mixed pairs, and remove only the legacy pool-name adapter after atomic migration. The done criteria repeat each guard. |
| fidelity / governance | Searched the repaired package, feature CRAFT/ledger and current non-historical repository surfaces for accepting `agent-name` language. | Every relevant governance occurrence states rejection; remaining package occurrences are negative vectors/schema discrimination, and unrelated `.agent-name` UI CSS selectors are not YAML keys. The 19-test limit text explicitly disclaims both pre-existence and causality. |

### Recheck checks

| check | result |
|---|---|
| frozen prior review hash | PASS: exact `FF27533D...7D095` before append |
| selector/version surface | PASS: 28 files classified; 21 active/test migration targets are all in scope, two v1 authorities are immutable, five L0 experiment files are non-authoritative evidence |
| broad role-literal surface | PASS: 14 raw hits; 13 active after the frozen L0 oracle, all migrated or explicitly justified as the distinct Refine vocabulary |
| governed-pool direct surface | PASS: seven code/test/doc consumers, all in the atomic scope |
| installer/route/confirmation seam | PASS at specification level: installer, three strategy copies, confirmation producer/test and additive confirmed-dispatch-v2 fixture are explicitly covered |
| new-write and anti-mix contract | PASS at specification level: v2/0.7.0 default, v1 explicit verification only, identical role refs, no 0.7 output through 0.6.4, mixed pair rejection |
| canonical name stale scan | PASS: `agent_name` is sole v0.7 key; all relevant `agent-name` occurrences reject or test rejection |
| `python validate_artifacts.py` | PASS: real 414-row migration and 41/41 exact negative vectors |
| Draft 2020-12 meta-validation | PASS: all 10 schemas |
| `python -m py_compile validate_artifacts.py` | PASS; generated cache removed after the check |
| feature ledger parse/index | PASS: 114/114 index targets resolve |
| repaired-target final newline/trailing whitespace audit | PASS excluding frozen `review.md` |
| `git diff --check` over CRAFT, ledger and follow-up | PASS; LF/CRLF warnings only |
| selected 19-test suite wording | PASS: retained as an unresolved validation limit, with no claim that failures pre-existed or were caused by this spec repair |

### Artifact verdicts

| artifact group | verdict | rationale |
|---|---|---|
| decision, compilation delta, schemas, fixtures and conformance validator | **KEEP** | identity, registry, evidence and canonical-name contracts remain closed and executable within their stated fixture ceiling |
| migration surface, ownership and implementation work pack | **KEEP** | AIR-R9's missing active selectors are now classified and included with explicit v2/legacy/anti-mix behavior |
| feature CRAFT and ledger | **KEEP** | AIR-R10 is aligned; candidate status, stale compiler and blocked runtime ceiling remain accurate |

### Evidence boundary

`KEEP` approves this repaired specification package and its implementation scope. It does not prove
that registry/package v2, telemetry 0.7.0, installer selection, confirmation propagation, registrar,
pool migration, allocator service or ExecutionGraph ingestion exists. Production remains stale and
blocked until the separately reviewed implementation satisfies the work-pack done criteria. The
previously observed 19-test result remains an undiagnosed external validation limit; it was not
rerun here and carries no causal attribution.

`exit_reason: resolved`; `agents_spawned: 0`; independent reviewer; no target fixes applied.
