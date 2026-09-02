# Review — IMPL-ACI-AGENT-IDENTITY-ROLE-001

Status: independent implementation review complete.

Verdict: **FIX**.

`recheck_required: true`

## Coverage

| reviewer | lens | corpus and attacks | result |
|---|---|---|---|
| independent reviewer paired to `/root/agent_identity_code_worker` | provenance / preservation | initial-status claim, `HEAD^` v0.6 source, production v0.7 pool, two documents, 414 rows, order and every non-identity field; current index/worktree and `local_pilot.py` manifest binding | pool value preserved; current manifest exact; post-commit proof is broken (AIR-I1) |
| same reviewer | authority / configurability | exact eight-role v1 registry, digest, `other`/unknown behavior, future revision boundary, Python/JS/appender consumers | current v1 is pinned; future-selection claim is false (AIR-I3) |
| same reviewer | mechanics / correctness | seven-input pure compiler, signed assignments, coverage/non-reuse/membership/role-fit/override, deterministic graph/digest, telemetry 0.7.0/ref propagation, anti-mix, confirmation, host, bridge, provenance | mechanics survived direct attacks; executable conformance is incomplete and non-reproducible (AIR-I1) |
| same reviewer | packaging / operability | three appender and skill copies, package v2, installer current and legacy modes, v1 immutability, Stage-E manifest and local-pilot digest | v2 current check passes; legacy verification fails (AIR-I2); skill drift check absent (AIR-I5) |
| same reviewer | governance / handoff | SPEC Recheck 3, CRAFT, ledger, runtime ceiling, Git state and claimed test evidence | runtime remains blocked, but live status is stale and implementation was committed before this review (AIR-I4) |

Every file in the implementation follow-up was read. The target corpus also included the accepted
SPEC work pack, migration surface and Recheck 3, the real write scope from `HEAD^..HEAD`, both
unstaged and staged diffs, current manifests, and the named active consumers. Historical telemetry,
v1 authorities, the v1 confirmed-dispatch fixture, prior reviews and L0 experiment files were
treated as immutable evidence rather than migration targets.

## Findings

### AIR-I1 — The migration and 41-vector conformance evidence is not reproducible after the implementation lands

- **Severity:** MAJOR
- **Files / evidence:**
  - `implementations/tests/runtime/test_agent_pool.py:34` says
    `subprocess.check_output(["git", "show", "HEAD:telemetry/agents/agent-pool.yaml"], cwd=REPO)`.
    After the implementation commit, `HEAD` is the v0.7 target, not the v0.6 source expected by the
    migration authority.
  - `IMPL-ACI-AGENT-IDENTITY-ROLE-001/VALIDATION.md:27` claims `PASS: 88 tests`.
  - `SPEC-ACI-AGENT-IDENTITY-ROLE-001/validate_artifacts.py:541-542` reads
    `real_raw = REAL_POOL.read_bytes()` and immediately passes it to
    `verify_and_migrate_real_pool(...)`; that validator also assumes the live file is still v0.6.
  - `IMPL-ACI-AGENT-IDENTITY-ROLE-001/fixtures/negative-vectors.json:19-44` declares identity and
    authority vectors AIR-N16 through AIR-N41, but `test_draft_graph_compiler.py` contains no
    assertions for `DG_AGENT_ASSIGNMENT_*`, `DG_AGENT_REUSED` or `DG_ROLE_FIT_*`. The copied manifest
    is not an executable implementation test.
- **Verification:** The claimed focused command ran 88 tests and returned one error:
  `DG_POOL_SOURCE_SUBSTITUTION` in
  `test_tracked_v06_migrates_exactly_to_current_value`. Running the accepted SPEC validator returned
  `DG_POOL_METADATA_DRIFT`. Direct independent attacks showed the implementation itself currently
  returns the expected typed failures for missing/extra/duplicate assignment, name reuse, unknown
  pool member, role-fit mismatch, invalid override, registry drift and pool drift, but those probes
  are not durable suite coverage. Manual comparison against `git show HEAD^` proved the current pool
  is the exact intended two-document/414-row migration and preserves row order plus every
  non-identity field.
- **Required fix:** Preserve the exact accepted v0.6 source as a versioned fixture or other immutable
  source artifact, make both migration validators consume that artifact rather than moving `HEAD`
  or the live target, and execute all AIR-N01..N41 against production loaders/compiler with exact
  code/path and no-result assertions. Rerun the same commands after committing, not only before.

### AIR-I2 — Explicit legacy-v1 verification is advertised but cannot verify the immutable package

- **Severity:** MAJOR
- **Files / evidence:**
  - `tools/install-register-dispatch-runtime.ps1:87` says
    `Legacy v1 is verification-only; use -LegacyVerification together with -Check.`
  - `implementations/contracts/register-dispatch-runtime-package.v1.json:9-14` pins the old v1
    `.claude/skills/register-dispatch/{SKILL.md,append-dispatch.cjs}` hashes.
  - `tools/install-register-dispatch-runtime.ps1:205-207` hashes those paths in the current source
    tree and throws `Canonical source digest mismatch` when they differ.
- **Verification:** Current v2 self-check passes. The required explicit command
  `-Check -LegacyVerification` fails on the first v1 skill hash: expected
  `6620C7...17C252`, current path `94FF36...505C6B`. The v1 manifest and dispatch registry are
  byte-unchanged, but their historical skill/appender bytes are no longer available at the paths
  the verifier reads.
- **Required fix:** Give v1 verification immutable archived source paths/content, or define a
  verifier that validates supplied historical package bytes without consulting overwritten current
  paths. Add a green legacy-verification test and retain the prohibition on legacy installation or
  new-row emission.

### AIR-I3 — A future role-registry revision still requires source/path mutation, contrary to the configuration boundary

- **Severity:** MAJOR
- **Files / evidence:**
  - `implementations/server/runtime/agent_roles.py:15` fixes
    `REGISTRY_PATH = Path("implementations/contracts/agent-role-registry.v1.json")`.
  - `tools/agent-pool-mcp/src/pool.mjs:16` and
    `.claude/skills/register-dispatch/append-dispatch.cjs:140` fix the same v1 filename; their
    authority filename is likewise fixed to v1.
  - `implementations/tests/runtime/test_agent_roles.py:52-63` calls its case
    `test_future_role_revision_is_data_only`, sets `value["version"] = "2"`, then writes those bytes
    back to `agent-role-registry.v1.json`.
  - The governing work pack requires a future accepted revision through configuration/authority
    data while retaining v1 as immutable evidence.
- **Verification:** Current v1 loads exactly the eight selected roles with digest
  `sha256:39b378...f4aa`; singular `other` passes and unknown `facilitator`/plural `others` fail. The
  purported future test passes only by replacing a file named and governed as v1. Updating a v2
  sibling plus dispatch authority would not be selected by Python, MCP or the appender without code
  changes.
- **Required fix:** Make the selected dispatch/package authority resolve a versioned role-registry
  path and trusted authority path, then pass that selection to every consumer. Test an immutable
  v1 beside a real v2 sibling; do not overwrite the v1 filename in the positive future-revision
  case.

### AIR-I4 — CRAFT/ledger report superseded pre-implementation state, and the candidate reached `master` before review

- **Severity:** MAJOR
- **Files / evidence:**
  - The accepted SPEC review says `## Recheck 3 — AIR-R9 and AIR-R10 repair` and
    `Verdict: **KEEP**` at `SPEC-ACI-AGENT-IDENTITY-ROLE-001/review.md:387-392`.
  - `docs/features/agents-communication-infra/CRAFT.md:45-47` still says the independent review and
    two rechecks were all `FIX`, another recheck is needed, and compiler adaptation remains pending.
  - `.craft/ledger.yml:249-254` and `:354` repeat that same stale next move and evidence state.
  - `IMPL-ACI-AGENT-IDENTITY-ROLE-001/TASK-SESSION.md` says `ready_for_review`, while the reviewed
    files are already in commit `f981397` on `master`; `origin/master` resolves to the same commit.
- **Verification:** Ledger YAML parses and all 124 `indexes.by_id` entries resolve. It correctly
  keeps runtime execution/OPEN blocked and does not prematurely promote the compiler. The defect is
  that it still says specification recheck and code adaptation have not happened, so the next move
  is false. Committing before the required independent KEEP also bypassed the work-pack entry gate;
  this review is `FIX`, so no acceptance exists retroactively.
- **Required fix:** Do not clear the compiler/runtime block. Update CRAFT/ledger to record SPEC
  Recheck 3 `KEEP`, implementation present but independently reviewed `FIX`, the exact surviving
  change requests, and runtime ingestion/execution still blocked. Repair through a normal follow-up
  commit and review; do not rewrite history or claim the current commit was reviewed before entry.

### AIR-I5 — Three-copy drift protection is incomplete

- **Severity:** MINOR
- **Files / evidence:**
  - The work pack requires a drift test across the three `register-dispatch` skill copies.
  - The three `append-dispatch.cjs` files currently have the same SHA-256
    `7FF42D...3D0C4`; the migration-relevant v2/ref/role wording is aligned across the three skills.
    However, no executable drift assertion for the three skill copies was found.
  - The complete `.claude` register skill intentionally contains additional anti-bias sections, so
    whole-file byte equality is not currently the contract.
- **Verification:** Direct hashes and no-index diffs confirmed appender byte equality, equality of
  `.agents`/`.codex` register skills, and the known extra `.claude` anti-bias text. Strategy copies
  contain the same v2/legacy routing rule but are not byte-identical.
- **Required fix:** Define the exact generated/shared fragment or normalized semantic fields that
  must remain equal and add one executable drift test across all three appender, register-skill and
  route-strategy copies.

## Artifact verdicts

| artifact group | verdict | rationale |
|---|---|---|
| production v0.7 pool and current v1 authority | **KEEP** | exact two-document/414-row migration and current raw/normalized refs verified |
| pure compiler mechanics and identity projection | **KEEP** as code mechanics, not accepted package | seven inputs, no YAML/filesystem I/O, real Popper/Dijkstra/Lamport names, signed assignment gates and deterministic digest survived direct attacks |
| implementation conformance/tests | **FIX** | AIR-I1 makes claimed post-commit proof false and leaves AIR-N16..N41 without durable implementation execution |
| role revision/configuration boundary | **FIX** | AIR-I3 mutates v1 paths rather than selecting a versioned sibling |
| telemetry 0.7.0, host/bridge/provenance and current v2 package | **KEEP** within bounded current-v1 behavior | focused host, confirmation, appender, provenance and current installer checks passed; no runtime execution claim |
| legacy installer/verifier | **FIX** | AIR-I2 prevents explicit v1 verification |
| CRAFT/ledger/handoff | **FIX** | AIR-I4 is materially stale and the review gate was bypassed |
| `local_pilot.py` / Stage-E source manifest current bytes | **KEEP** | current constant equals the exact 82-entry manifest digest and every manifest member hash matches |

## Commands and results

| check | result |
|---|---|
| pool migration from `git show HEAD^` | PASS: exact migrated value, 2 documents, 414 rows, order and all non-identity fields preserved |
| strict pool attacks | PASS: missing/dual/hyphen/empty/non-string/duplicate identity, duplicate YAML and unknown key rejected with typed codes |
| role v1 current authority | PASS: exact 8 roles/digest; `other` accepted; `others` and unknown role rejected |
| claimed focused suite | **FAIL:** 88 run, 1 error in `test_tracked_v06_migrates_exactly_to_current_value` |
| compiler excluding broken pool test | PASS: compiler 22/22; roles 4/4; direct assignment/ref attacks returned expected typed failures |
| Stage-B | PASS: 19/19 |
| confirmation | PASS: 8/8 |
| host dispatch + ingestion + workflow binding + bridge | PASS: 37/37 |
| agent reference + anti-bias appender + ingestion | PASS: 16/16 |
| provenance contracts | PASS: `aci_vectors=6 positive=5 rejection=8 candidates=16` |
| MCP smoke/RPC | PASS: 414 entries, 721 tags, three tools; results expose `agent_name` |
| current package installer self-check | PASS: runtime 0.7.0 |
| legacy package installer self-check | **FAIL:** immutable v1 manifest hash versus overwritten current skill path |
| Stage-C/local-pilot | PASS: 8/8; source manifest 82/82 exact; manifest hash equals local-pilot constant |
| runtime bootstrap + abuse | expected current-tree residue reproduced: 19 run, 4 failures + 1 error, all on absent sequential/feedback/zig-zag handoff/slot semantics |
| bootstrap causality inspection | PASS for current-tree independence only: production `dispatch_workflow.py` diff adds only `route_digest`; it does not remove handoff materialization, and current code still emits `slots: []` |
| SPEC conformance validator after migration | **FAIL:** `DG_POOL_METADATA_DRIFT` before vector execution |
| node syntax | PASS: 9 affected appender/MCP files |
| Python compile | PASS for changed Python files |
| changed JSON/YAML parse | PASS: 95 changed JSON files plus production pool and ledger YAML |
| target-scope `git diff --check` | PASS |
| ledger structure/index | PASS: YAML parse and 124/124 indexed IDs resolve |
| current Git index/worktree | no staged or unstaged tracked divergence; only three unrelated untracked files |

## Local-pilot index incident boundary

The requested premise that `local_pilot.py` is currently `MM` is no longer true and therefore was
not claimed as evidence. At review time both `git diff --cached` and `git diff` are empty for tracked
files. Commit `f981397` contains `STAGE_E_SOURCE_MANIFEST_SHA256 = 47c11e...403b6`, exactly the
current manifest digest, and all 82 manifest entries verify. A transient earlier wrong staged hash
cannot be reconstructed from the current repository and is not asserted.

The operational risk was real: staging the manifest and local-pilot constant at different moments
can commit an internally inconsistent preflight gate. The safe action if that divergence recurs is
to stage only the final manifest and matching `local_pilot.py` together after the 82-file hash check,
then inspect `git diff --cached` and rerun Stage-C before commit. Do not reset unrelated user work.

## Bootstrap residue and evidence boundary

The five bootstrap cases are specifically the current absence of ordered handoff slot
materialization and fail-closed feedback/zig-zag semantics. This review establishes independence
from the identity diff in the current tree; it does **not** claim historical preexistence.

No projector, confirmation of an ExecutionGraph v2 digest, persistent graph authority, graph
ingestion, scheduler, provider/tool execution or autonomous dispatch was implemented here. Even
after AIR-I1 through AIR-I5 are repaired, the correct bounded claim remains deterministic
DraftGraph-to-ExecutionGraph compilation with allocator-owned display names. Runtime execution
remains blocked.

## Change requests

1. **MAJOR** — Make the exact v0.6 migration source immutable and execute AIR-N01..N41 in the
   production implementation suite after commit.
2. **MAJOR** — Restore an actually runnable explicit legacy-v1 verification path.
3. **MAJOR** — Resolve future role registries through versioned selected paths without replacing
   immutable v1 files.
4. **MAJOR** — Correct CRAFT/ledger/handoff state while retaining the runtime/compiler block and
   record this `FIX` review.
5. **MINOR** — Add explicit three-copy semantic drift tests.

`exit_reason: resolved`; `agents_spawned: 0`; independent reviewer; no reviewed target, index or
prior review was modified.

---

## Recheck 1 - forward repair AIR-I1 through AIR-I5

Status: independent recheck complete.

Verdict: **KEEP**.

`recheck_required: false`

The predecessor review was frozen before this recheck. Its independently recomputed SHA-256 was
`B97763E69FF7D9FE61B205FA5B4859B9EB635A18E90C24A168B02770BB87B974`, exactly the expected value.
The accepted SPEC Recheck 3 review also resolves to
`285B4636739DE898607A9F49A898649D754D525ED809DC68597207357CE4BA1F`.

### Finding dispositions

| finding | disposition | independent evidence |
|---|---|---|
| AIR-I1 | **resolved** | The exact two-document v0.6 source is frozen as `fixtures/agent-pool.v0.6.yaml` with SHA-256 `5C7B9745...99EBA`; neither the SPEC validator nor the pool/vector tests depend on Git history. The validator proves the ordered 414-row projection and 41/41 exact typed vectors. `test_agent_identity_role_vectors` executes all 41 manifest operations against production pool, role, allocator and compiler paths and requires typed code/path plus no compilation result. The focused suite passed 96/96. |
| AIR-I2 | **resolved with a narrowed compatibility claim** | The archived package members match their archive manifest and the last recoverable predecessor bytes from `b3bc638`. The original immutable root-v1 manifest remains historically inconsistent and is not presented as reconstructed authority. The installer now reports `verified frozen recoverable v1 projection 0.6.4` and explicitly says the original root-v1 manifest authority is not verified or reconstructed. Current v2 check, frozen-v1 projection check and v2 anti-mix rejection passed 3/3. |
| AIR-I3 | **resolved** | `agent-role-registry-selection.json` selects the trusted versioned registry, authority and host-routing paths and digest. Python, MCP, appenders and installer resolve through that selection. The future-revision test creates real v2 siblings, selects them as data, and proves the v1 registry remains byte-unchanged; unknown or unpinned selection fails closed. |
| AIR-I4 | **resolved prospectively** | CRAFT, ledger, task and validation surfaces now record SPEC Recheck 3 `KEEP`, the premature `f981397` chronology, this forward repair and the continuing runtime block. Ledger YAML parses, all 125 `by_id` entries resolve, and its artifact accounting is accurate: 41 paths exist and the one absent path is the explicitly planned roadmap-closure review. This review does not retroactively approve the earlier commit. |
| AIR-I5 | **resolved** | `test_register_dispatch_copy_drift` enforces byte equality across the three appenders and normalized semantic equality for the register-skill migration facts and strategy authority paragraph. It is included in the green 96-test suite. |

### Recheck evidence

| check | result |
|---|---|
| focused role/pool/vector/compiler/confirmation/appender/drift/hook/bridge/installer suite | PASS: 96/96 |
| SPEC validator | PASS: frozen v0.6 to current v0.7 exact 414-row projection; 41/41 typed vectors |
| Stage-B plus APT Stage-B | PASS: 25/25 |
| register-dispatch installer tests | PASS: 3/3 after the narrowed legacy wording |
| current v2 installer repository check | PASS: runtime 0.7.0 |
| provenance contract validator | PASS: `aci_vectors=6 positive=5 rejection=8 candidates=16` |
| MCP smoke and RPC | PASS: 414 entries, 721 tags, three tools |
| Stage-E source manifest | PASS: 83/83 member hashes; manifest SHA-256 `919793A4...BCC4C2` equals the current `local_pilot.py` pin |
| frozen migration fixture | PASS: SHA-256 `5C7B9745...99EBA`; no `git show`, `HEAD^` or `HEAD:` dependency in the validator or migration/vector tests |
| ledger | PASS: 125 indexed IDs; 41 present artifact paths plus one intentionally absent planned review |
| Python compile and `git diff --check` | PASS; Git emitted line-ending conversion warnings only |
| runtime bootstrap plus abuse | **LIMIT:** 14/19; four failures and one error remain on absent handoff/slot semantics |

The five bootstrap outcomes are not identity/role conformance evidence and are not claimed green.
Inspection still establishes only current-tree independence from the identity changes; it does not
establish historical causality or preexistence.

### Final evidence boundary

This `KEEP` accepts the bounded agent-identity/role migration and deterministic
DraftGraph-to-ExecutionGraph compilation evidence. It does **not** establish an executable graph
runtime. Projectors, persistent graph authority, ExecutionGraph ingestion, scheduler behavior,
provider/tool/credential execution and autonomous JSON-to-dispatch execution remain outside this
implementation and blocked.

No MAJOR, CRITICAL or MINOR finding remains from AIR-I1 through AIR-I5.

`exit_reason: resolved`; `agents_spawned: 0`; independent reviewer; only this append to `review.md`
was authored by the reviewer; no reviewed target, index, prior review text, commit or remote was
modified.
