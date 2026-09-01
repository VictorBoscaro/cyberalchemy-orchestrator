# POLICY-002 alignment and layering audit

Date: 2026-09-01

Verdict: **PASS for workpack authoring; not code entry**

No alignment or layering blocker requires widening the proposed three-path test-only scope. The
workpack may be authored for POLICY-002 only if it carries the entry predicates and read-only
boundaries below. Code entry remains separately blocked until a fresh descriptor/readiness pins the
final independently reviewed POLICY-001 implementation and the current POLICY-002 normative bytes.

## Scope reviewed

Candidate write scope, presently absent:

1. `implementations/tests/runtime/policy_denial_harness.py`;
2. `implementations/tests/runtime/execution_policy_denial_oracle_v1.json`;
3. `implementations/tests/runtime/test_execution_policy_denial.py`.

The audit compared that scope with the current POLICY-002 contract in `TECH-POLICY-D0.md`,
`SPEC.md`, `domain.md`, `interfaces.md`, `rules.md`, `TEST-SPEC.md`, `architecture.md` and
`capabilities/execution-policy-authority.md`; the reviewed POLICY-000 implementation; the current
POLICY-001 harness/oracle/tests; and the existing database, artifact and canonical helpers.

## Alignment evidence

The candidate topology is literal rather than inferred:

- `architecture.md` says: “POLICY-002 planning may name only its test-only denial harness, oracle
  and tests” and forbids migration, service, journal, API, export, real action attempts and L3 work.
- `interfaces.md` says the fake-denial boundary depends only on the exact persisted POLICY-001
  lineage, its harness, the pure parser, canonicalization/error helpers and the same temporary
  file-backed database.
- ACI-R23 says: “Temporary SQLite persistence is the only admitted I/O” and permits exactly one
  additional test-only receipt table.
- The current L1 implementation exposes the required public handoff:
  `SyntheticPolicyLineageHarness.reopen_synthetic_lineage(lineage_identity)`. It reopens through
  fresh database/artifact handles, reproduces all seven member bytes/digests, reruns the POLICY-000
  parsers and reasserts the production authority firewall.
- No fake-denial symbol or table currently exists in `implementations/server/runtime`, and the
  three proposed paths are absent. The focused current POLICY-001 suite passed 10/10 during this
  audit; that is diagnostic evidence, not final POLICY-001 promotion evidence.

Current normative pins relevant to the workpack include:

| Artifact | SHA-256 |
|---|---|
| `TECH-POLICY-D0.md` | `sha256:522a8cac79335e6190fb4799cbea95c0f58621f4f9ea5f72add2437690b8130e` |
| `specs/capabilities/execution-policy-authority.md` | `sha256:8b8fa86efbd49ed74dd49da9cd05e33ed183e5194d4c3c27f2d0a08d8f7f241a` |
| `specs/TEST-SPEC.md` | `sha256:07f9da9ff3a7f51f1b03ceed52c7a59b0857f45da9917a2e228db4d78c61aa0e` |
| `POLICY-001-PERSISTENCE-PATTERN-INVENTORY.md` | `sha256:d8eae9829069631caaef769635b3748b5440d5bfab4aacaf682f736eb546d84e` |
| `POLICY-000-IMPLEMENTATION-REVIEW.md` | `sha256:76ed9cd9efd6794e7b1d4c40421635db16edc8a580e789f837b415d892b13c8c` |
| `implementations/server/runtime/execution_policy.py` | `sha256:405b990c49edb330227e14af4ecc65a6d39566a8a6a298433fd7aa40eaf0e357` |

## Layer boundary

POLICY-002 is a valid L2 increment because it answers a decision not answered by either earlier
layer:

> After this layer, we know whether the exact reopened non-executable POLICY-001 package can route
> every closed synthetic action label to one durable package-level denial without attempting an
> external action or acquiring production authority.

| Layer | Preserved proof | POLICY-002 relationship |
|---|---|---|
| POLICY-000 / L0 | Pure closed parsing, canonical bytes/digests and test/production authority-domain separation. | Read-only dependency; every parser and firewall guarantee remains unchanged. |
| POLICY-001 / L1 | Exact seven-member artifact lineage, atomic persistence, replay/conflict and fresh-handle reopen. | Read-only source prerequisite; L2 consumes only its public reopened result. |
| POLICY-002 / L2 | One package-level fake denial persisted once with zero external calls. | Current workpack target. |
| POLICY-003 / L3 | Product-selected policy, target-host enforcement, real fence/provider admission. | Explicitly deferred; no L3 evidence or symbol may appear. |

The L2 value is denial durability plus proof that fixture lineage does not become executable
authority. Its cost is one local table, one harness, one independent oracle and one conformance
suite. Adding production integration, a launcher, effect or migration would answer the distinct L3
question at materially higher coordination and verification cost, so it does not belong in this
layer.

## Required symbol and dependency boundaries

### Test-only denial harness

The workpack should constrain `policy_denial_harness.py` to:

- closed constants for the receipt/preimage schemas, `test-only-non-executable` authority, exact
  two ordered reason codes, exact twelve-label corpus and one test-table name;
- typed validation, conflict and stored-integrity errors local to the test seam;
- one `SyntheticPolicyDenialHarness` with public `deny_synthetic_attempt(...)` and
  `reopen_fake_denial(...)` methods;
- a pure internal projection that derives the exact denial preimage, `denial_digest`, canonical
  receipt bytes and receipt content digest from the reopened lineage;
- one dual-axis lookup resolving `denial_key` and `lineage_identity` inside the same
  `RuntimeDatabase.write()` transaction;
- exactly the four named failpoints `policy_denial.after_begin`,
  `policy_denial.after_receipt`, `policy_denial.before_commit` and the post-transaction
  `policy_denial.after_commit` lost-response observation.

It must call only the public L1 reopen method. Importing or depending on L1 private validators,
tables or SQL would leak ownership and make the layers evolve together.

### Independent denial oracle

`execution_policy_denial_oracle_v1.json` must freeze, rather than derive from the harness under
test:

- the exact persisted POLICY-001 source identity/unit digest and both policy digests;
- the twelve unique selector literals;
- exact denial preimage bytes and
  `sha256:bc8655ac88276258d8e320b8a9757a8b625c9e9249dc7255a5578d2eb7e65399`;
- exact receipt bytes for `denial_key=policy-denial-command-001` and receipt content digest
  `sha256:5ffde80fbfb897ceb4b90cb85bcdb019538777c91ae3525ac0f7e0ebc43a9b11`;
- the four failpoint names.

The selector is test routing only. It must not appear in the preimage, receipt, persisted row,
identity or digest authority.

### Read-only dependency allowlist

The descriptor should pin at least these read-only inputs:

- current final POLICY-001 implementation review/evidence plus
  `policy_lineage_harness.py`, `execution_policy_lineage_oracle_v1.json` and
  `test_execution_policy_lineage.py`;
- POLICY-000 `execution_policy.py`, its oracle and tests;
- `database.py`, `artifacts.py`, `canonical.py` and `errors.py`;
- production confirmation and invocation-plan validation surfaces only as negative-test targets;
- migration names, service, journal and effect-bearing tables only as read-only inventory/spy
  targets.

There is no authorized production dependency in the denial harness itself. Production modules may
be imported by the test solely to prove rejection or install fail-on-call spies.

## Required negative coverage

| Test obligation | Minimum workpack coverage |
|---|---|
| T-ACI-POL2-1 | Independently compare exact preimage, denial digest, receipt bytes and receipt digest with the oracle. |
| T-ACI-POL2-2 | Missing/partial/reordered/tampered L1 receipt, member, artifact, unit digest and non-canonical bytes; each of six positive budget ceilings; read/write/network/process/credential grants; positive child-process ceiling; production-domain substitution. Every case rejects before the denial write and leaves zero denial rows. |
| T-ACI-POL2-3 | All and only twelve unique labels accept; every label returns the same decision and ordered reasons; unknown/missing label and decision/reason drift reject; label absence from every persisted/canonical authority surface is asserted. |
| T-ACI-POL2-4 | All three pre-commit failpoints reopen to zero denial rows; `after_commit` leaves one row and fresh retry returns the first receipt. |
| T-ACI-POL2-5 | Same key replay, alternate key with same lineage convergence, and same key against a second valid L1 identity conflict; changed denial projection under either uniqueness axis conflicts without a second row. Caller-supplied decision/reasons/digest are forbidden. |
| T-ACI-POL2-6 | Fresh database, L1-harness and L2-harness handles reproduce exact source binding, receipt bytes and both digests. In-memory SQLite is forbidden. |
| T-ACI-POL2-7 | Exercise every label independently while fail-on-call spies remain zero for workload filesystem, network, subprocess/process, credentials, tools, provider, runtime service, journal, audit, clock and environment. SQLite access to the supplied temporary path is the only exception. |
| T-ACI-POL2-8 | L1 cardinalities and bytes remain unchanged; exactly one L2 table/row is added; every production authority/runtime/event/effect/publication/message table remains empty; existing production policy/fence/confirmation/plan seams reject test-only values before mutation; no standalone request/effect API is to be invented merely to test rejection. |

Tests should also enforce an AST/import allowlist for the harness and assert its table name is absent
from `MIGRATION_NAMES`. Drift scenarios must use test fixture/database corruption or controlled
internal constant substitution; expanding the public method with caller-controlled decision,
reason, digest, external callable or policy dictionaries would violate the interface.

## Layer-leakage risks and controls

| Risk | Severity if introduced | Required control |
|---|---|---|
| Reusing L1 private SQL/validators | MAJOR | Consume only `reopen_synthetic_lineage`; reparse returned exact members through public POLICY-000 functions where an explicit L2 predicate is needed. |
| Persisting the action label | MAJOR | Oracle and tests prove byte absence from the table, preimage, receipt, digests and replay identity. |
| Adding caller-controlled decision/reasons/digest to manufacture conflict tests | MAJOR | Keep projection closed; create drift only through controlled test corruption/substitution. |
| Treating a denial as an attempted effect or host enforcement | MAJOR | No request/effect/fence/provider identity, observation or L3 evidence; exact production table emptiness. |
| Patching broad filesystem calls and accidentally counting SQLite | MINOR | Spy on workload boundaries specifically; admit only the supplied temporary SQLite path. |
| Adding a migration/service/journal/export for convenience | CRITICAL | Exact three-path write scope and static diff/import/migration checks. |

## Workpack entry predicates

The existing POLICY-001 descriptor/readiness is historical code-entry authority: it still says
`implementation_status: not-started-ready`, and its task requires the three L1 outputs to be absent,
while those outputs now exist. POLICY-002 must not reuse that receipt as current implementation
evidence.

Before POLICY-002 code entry, its new descriptor/readiness must:

1. pin an independent POLICY-001 implementation `PASS / KEEP` receipt and the exact final L1
   harness/oracle/test hashes;
2. pin the current POLICY-002 normative documents, not the pre-POLICY-002 digests in the historical
   L1 descriptor;
3. declare exactly the three candidate write paths and a capability profile limited to repository
   writes there plus temporary file-backed SQLite;
4. freeze the dependency allowlist, symbol boundaries, negative matrix and forbidden changes from
   this audit;
5. require focused POLICY-002, combined POLICY-000/001/002 regression, bounded compilation,
   three-path diff/scope checks and the repository-approved curated runtime regression without
   promoting unrelated artifacts as evidence;
6. assign independent implementation review after mutation.

## Final gate

- **Workpack:** PASS. The three-path L2 slice is coherent, decision-distinct and sufficiently
  bounded to plan.
- **Code entry:** not evaluated as PASS here; blocked until the workpack predicates above are
  satisfied by a fresh exact descriptor/readiness.
- **Production/L3:** BLOCK. No POLICY-002 result authorizes product values, confirmation, opening,
  request/effect creation, launcher/provider start, host enforcement or deployment.

Surviving alignment/layering blockers to workpack authoring: **none**.
