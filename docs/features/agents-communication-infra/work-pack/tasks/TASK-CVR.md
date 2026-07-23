# TASK-CVR — Canonical vault-read adjunct

## Objective and authority

Prepare and, only after exact authorization, deliver a transport-neutral, read-only projection of
admitted canonical Markdown bytes. This task does not own the audit-ledger server, APT, bus,
inventory, cache or canonical source files.

Canonical unit identities are:

| Canonical ID | Stage-1 shorthand alias | Purpose |
|---|---|---|
| `SWU-ACI-CVR-000` | `SWU-CVR-000` | Documentation decisions and contracts. |
| `SWU-ACI-CVR-GUARD-001` | `SWU-CVR-GUARD-001` | Authority verifier/descriptors and common CVR-001/002 finalizer; bootstrap uses one external finalizer. |
| `SWU-ACI-CVR-001` | `SWU-CVR-001` | Capture/snapshot and artifact list/get. |
| `SWU-ACI-CVR-002` | `SWU-CVR-002` | Declaration/logical-edge list/get. |

Aliases are references only, not distinct units. Promotion order is strictly
`SWU-ACI-CVR-000 -> SWU-ACI-CVR-GUARD-001 -> SWU-ACI-CVR-001 -> SWU-ACI-CVR-002`;
no later unit may be authorized from documentation alone or by skipping a predecessor.

## Gate precedence and ApprovalPacket

Current state:

- `workPackGateStatus=block`;
- SPEC `runtimeGate=block`;
- `cvrImplementationGateStatus=approval_packet_prepared` (**NON-PASS**);
- no active exception or `pass_with_named_swu_authorization`.

The sole predicate is:

```text
authorized = (runtimeGate=pass AND workPackGateStatus=pass) OR
             (verified active named authorization for exactly one enumerated CVR SWU
              AND every predecessor receipt/baseline required by its closed descriptor verifies
              AND scope is exactly the descriptor-bound isolated effect-free CVR core)
```

This predicate is a proposal and is non-operative. It becomes normative only after the same
ApprovalPacket amends and receives acceptance for ADR-CVR-001, the canonical-vault-reads spec,
TEST-SPEC and this task, plus its deterministic descriptor entry. Until that coordinated update
is accepted, only `(runtimeGate=pass AND workPackGateStatus=pass)` can authorize implementation.
The proposed carve-out branch never authorizes server, API, MCP, bus or runtime integration.

Implementation may begin only after the architecture owner, product/protocol owner and
host/operator owner accept the exact packet and the root/project owner gives final approval that
creates a current, single-use authorization naming one enumerated unit and its exact closed
descriptor. The first executable unit is `SWU-ACI-CVR-GUARD-001`; CVR-001 and CVR-002 remain
ineligible until their predecessor evidence exists. This is a narrow CVR carve-out: the CVR gate
may authorize only the isolated, effect-free core named by that authorization after all named
acceptances. `runtimeGate=block` and `workPackGateStatus=block` continue to block every
runtime/integration surface, including HTTP, MCP, agent tools and server wiring. The carve-out
authorizes no other code and is absent now.

### AuthoritySlots

Each future acceptance record binds a stable authenticated principal ID and evidence digest; role
labels or agent names are insufficient.

| Slot | Required decision scope | Current principal/evidence |
|---|---|---|
| `architecture_owner` | parser, module, dependency/lock and SWU taxonomy | absent / absent |
| `product_protocol_owner` | artifact/raw-declaration versus logical-edge delivery carve-out | absent / absent |
| `host_operator_owner` | repository identity, roots, privacy, ceilings and effective limits | absent / absent |
| `root_final_approver` | final exact-packet approval and authorization issuance request | session root orchestrator is designated final approver only; stable principal/evidence not yet recorded |

The controlled writer and independent reviewers fill no owner slot. The session root orchestrator
is final approver only and must not be inferred to be architecture, product/protocol or
host/operator owner.

### Canonical ApprovalPacket

Only these five normative entries are digest-bound:

1. `docs/features/agents-communication-infra/adrs/ADR-CVR-001.md`;
2. `docs/features/agents-communication-infra/specs/canonical-vault-reads.md`;
3. `docs/features/agents-communication-infra/TEST-SPEC.md`;
4. `docs/features/agents-communication-infra/work-pack/tasks/TASK-CVR.md`;
5. exactly one closed descriptor selected by canonical SWU ID at
   `docs/features/agents-communication-infra/work-pack/descriptors/<canonical_swu_id>.json`.

The only valid descriptor locators are:

- `docs/features/agents-communication-infra/work-pack/descriptors/SWU-ACI-CVR-GUARD-001.json`;
- `docs/features/agents-communication-infra/work-pack/descriptors/SWU-ACI-CVR-001.json`;
- `docs/features/agents-communication-infra/work-pack/descriptors/SWU-ACI-CVR-002.json`.

No case folding, percent-encoding or caller-controlled path component is permitted. Descriptors
are immutable governance documents and ApprovalPacket entries. They are not per-execution
authority artifacts and do not count among authorization, claim and `ExecutionReceipt`.

The other seven CVR-000 documents are derived status/navigation indexes. Link and diff validation
must keep them consistent, but changing one does not invalidate an accepted ApprovalPacket digest.

`aci.cvr.approval-packet/v1` is compact UTF-8 JSON with fixed top-level order
`domain`, `schema_version`, `entries`. Paths are POSIX repository-relative NFC strings; reject
absolute paths, empty/`.`/`..` segments, duplicates and Unicode/case-fold collisions. Entries,
whose fixed field order is `path`, `sha256`, sort by normalized-path UTF-8 bytes. File digests are
`sha256:<64 lowercase hex>` over exact bytes. Packet digest is SHA-256 over
`b"aci.cvr.approval-packet/v1\x00" + compact_json_bytes`, rendered in the same prefixed form.

The verifier independently validates paths, reads each file once, recomputes entry and packet
digests, checks all accepted packet digests and records the recomputation in the terminal receipt.
Missing/extra/nondeterministic entries or byte drift fail before repository or ephemeral effects.

### Future append-only authorization protocol

No authorization, claim or receipt exists in the documentation phase. A future authorized
execution persists exactly three authority artifacts, each at a content-addressed fixed path:

```text
work-pack/authorizations/<authorization_id>/authorization.json
work-pack/authorizations/<authorization_id>/claim.json
work-pack/authorizations/<authorization_id>/execution-receipt.json
```

The authorization preimage excludes `authorization_id` and every path derived from it. Its bytes
are `b"aci.cvr.authorization/v1\x00" + compact_json_bytes`, where the compact UTF-8 JSON has fixed
top-level order `domain`, `schema_version`, `body`, rejects duplicate/unknown fields and uses the
same NFC/path and canonical scalar rules as the ApprovalPacket. `authorization_id` is
`aci-cvr-auth-<64 lowercase hex SHA-256 of those preimage bytes>`. Only after deriving and
verifying that ID may the three paths above be formed. The persisted `authorization.json` is the
canonical envelope with fixed order `domain`, `schema_version`, `authorization_id`, `body`;
`authorization_sha256` is SHA-256 over its exact bytes.

These paths are authority-owned, immutable, create-exclusive and outside every implementation
writer's write scope. There is no persisted `ClaimReceipt`, separate revocation file, mutable
`current` pointer, SWU-fixed authorization path, writer-created receipt, or second finalization
receipt.

The authorization body closed schema binds:

```text
canonical_swu_id; descriptor_path; descriptor_sha256;
approval_packet_schema; approval_packet_digest; approval_packet[];
owner_acceptance_records[]; root_issuer{};
repository_write_scope[]; ephemeral_host_effect_scope[];
repository_write_scope_sha256; ephemeral_host_effect_scope_sha256;
test_ids[]; exact_commands[]; exact_commands_sha256; allowed_index_url;
issued_at; expires_at; reason
```

Before claim creation, the root may withdraw the offered authorization through its external
trusted control channel; withdrawal creates no repository artifact and the claim must not be
created. Authorization JSON contains no mutable or anticipatory revocation state. After claim
creation, withdrawal is no longer a state transition: the root requests controlled cancellation
and the guard/finalizer records a terminal `BLOCK` or `INTERRUPTED` receipt.

The claim body binds `authorization_id`, `authorization_sha256`, authenticated
`execution_session_id`, packet, descriptor, scopes and commands. The persisted `claim.json` bytes
are the closed compact-JSON envelope with fixed top-level order `domain`, `schema_version`, `body`
and the canonical-JSON rules above. The claim digest preimage is
`b"aci.cvr.claim/v1\x00" + persisted_claim_json_bytes`; `claim_sha256` is SHA-256 over that
preimage. The root creates the persisted JSON immediately before guard invocation at the derived
claim path. The expected authorization digest, claim digest and authenticated session ID reach
the guard through a root-controlled channel outside the repository/workspace. Workspace bytes
cannot select or override those values.

The receipt body binds authorization/claim/descriptor/packet digests, session, predecessor
evidence, observed effects, cleanup evidence, outcome and reason. The persisted
`execution-receipt.json` bytes are the closed compact-JSON envelope with fixed top-level order
`domain`, `schema_version`, `body` and the canonical-JSON rules above. The receipt digest preimage
is `b"aci.cvr.execution-receipt/v1\x00" + persisted_execution_receipt_json_bytes`;
`execution_receipt_sha256` is SHA-256 over that preimage. Its path is derived only after
`authorization_id` verifies. Create-if-absent idempotency compares the persisted JSON bytes
byte-for-byte and recomputes the digest using this single preimage rule; a divergent existing file
is an integrity failure and is never overwritten.

After GUARD bootstrap, the authority-owned common guard consists of one pure verifier, one closed descriptor for each enumerated
SWU and one finalizer. The caller supplies only the enumerated SWU ID plus the external expected
digests/session; it cannot supply paths, commands, tests, indices, write scopes or receipt
locations. Before the first repository or ephemeral-host effect, the pure verifier independently
reconstructs the ApprovalPacket and validates authorization ID/content, owner evidence, closed
descriptor, claim, session, expiry, predecessor receipts/baselines, scopes,
commands, tests and index. Unknown/duplicate fields, missing evidence or any mismatch fail closed.

On success the common guard directly invokes the CVR-001/002 worker under the descriptor; a successful
verification is never returned as a reusable capability. The worker may return only
non-authoritative structured outcome evidence. The guard/finalizer is the sole creator of the
terminal `ExecutionReceipt`, on pass, block or controlled interruption, with create-if-absent
semantics. Receipt existence consumes the authorization.

Crash and recovery behavior is closed:

| Observed state | Permitted transition |
|---|---|
| Hard crash, no receipt, repository and ephemeral scope proven pristine | Same authenticated session may retry through the guard. |
| Hard crash, no receipt, any partial write, unknown cleanup or digest drift | Worker is not reinvoked; root requests `BLOCK` from the one applicable finalizer (external authority-owned bootstrap finalizer for GUARD, common guard/finalizer for CVR-001/002). Root never writes a receipt. |
| Controlled cancellation/interruption | Guard stops the worker, performs bounded cleanup and creates terminal `INTERRUPTED` or `BLOCK`. |
| Existing receipt with byte-identical recomputation | Read succeeds idempotently; worker is never reinvoked. |
| Existing receipt with divergent bytes or digest | Integrity failure; no overwrite, repair or worker invocation is permitted. |

Every terminal outcome records cleanup status, exact residual paths and whether the host scope was
proven pristine. Unknown cleanup is a blocking outcome, never success.

This contract provides workflow integrity against drift and accidental bypass on the sanctioned
path. Because the current host grants agents unrestricted shell/filesystem authority, it is an
advisory governance boundary, not a sandbox or a structural security boundary; external expected
digests/session prevent workspace-only substitution but cannot stop a principal with equivalent
host authority from bypassing the sanctioned entry point.

## SWU-ACI-CVR-000 — Documentation packet

- **Governed scope:** five-entry ApprovalPacket plus seven derived indexes: 12 governed artifacts,
  including the selected deterministic descriptor.
- **Derived status/index scope:** exactly these seven documents:
  `docs/features/agents-communication-infra/WORK-PACK.md`;
  `docs/features/agents-communication-infra/IMPLEMENTATION-LAYERING.md`;
  `docs/features/agents-communication-infra/CHANGELOG.md`;
  `docs/features/agents-communication-infra/work-pack/shared/swu-manifest.md`;
  `docs/features/agents-communication-infra/work-pack/shared/cross-task-decisions.md`;
  `docs/features/agents-communication-infra/work-pack/shared/cross-task-gaps.md`;
  `docs/features/agents-communication-infra/work-pack/waves/W0.md`.
- **State:** `documentation_prepared`; not owner/root accepted and not implementation authority.
- **Done for preparation:** identities, exact scopes, gates, prerequisites, tests, decisions and
  gaps are mutually traceable.

## SWU-ACI-CVR-GUARD-001 — Authority guard and finalizer

### Non-recursive bootstrap authority

GUARD-001 cannot verify, finalize or authorize its own creation. After the coordinated five-entry packet is
amended and accepted, root may issue exactly one root-owned bootstrap authorization and claim for
`SWU-ACI-CVR-GUARD-001`. An external trusted executor, supplied with expected packet,
authorization and claim digests/session outside the workspace, independently validates that
bootstrap and directly invokes the guard implementation worker. Its exactly one external
authority-owned bootstrap finalizer—not the guard being created—performs create-exclusive
terminalization using the same three-artifact canonical protocol and crash matrix. Root may
request cancellation or `BLOCK` but never writes the receipt.

The bootstrap repository write scope is exactly:

- `implementations/vault_read_guard/__init__.py`;
- `implementations/vault_read_guard/canonical.py`;
- `implementations/vault_read_guard/descriptors.py`;
- `implementations/vault_read_guard/finalizer.py`;
- `implementations/vault_read_guard/guard.py`;
- `implementations/vault_read_guard/verifier.py`;
- `implementations/tests/vault_read_guard/test_authority_identity.py`;
- `implementations/tests/vault_read_guard/test_bootstrap_boundary.py`;
- `implementations/tests/vault_read_guard/test_crash_matrix.py`;
- `implementations/tests/vault_read_guard/test_descriptor_scope.py`;
- `implementations/tests/vault_read_guard/test_finalizer.py`.

The exact proposed commands are `py -3.12 -m compileall implementations/vault_read_guard
implementations/tests/vault_read_guard` followed by `py -3.12 -m unittest discover -s
implementations/tests/vault_read_guard -p "test_*.py"`. The implementation is Python-standard-
library-only: dependency and network/index scopes are empty.

Its ephemeral scope is one descriptor-named OS temporary directory used only for the isolated
interpreter and test cache. The accepted GUARD descriptor freezes exact
expanded file paths, pre-write hashes/absence, commands, tests, dependency/index policy and that
temporary locator before bootstrap execution. It excludes `implementations/vault_read/**`,
server, API, MCP, bus, APT, canonical data, every governance descriptor and all authority artifact
paths. No generic shell session, nested authorization, self-verification, root-written receipt or
second bootstrap/finalizer is permitted.

### Minimum working unit

After this layer, we know whether one authority-owned entry point can validate an exact
authorization and directly execute a closed SWU without transferring authority to an
implementation writer.

Its exact future scope is the pure verifier, canonical schemas, closed descriptors for CVR-001 and
CVR-002, the guard/finalizer, and tests proving fail-closed behavior and sole receipt ownership.
The selected descriptor is immutable and digest-bound as the fifth ApprovalPacket entry. It
contains all paths, commands, tests, scopes, index policy, predecessor requirements and receipt
schema; callers may select only an enumerated SWU ID.

Exit evidence must prove:

- reconstruction of all five ApprovalPacket entries from exact bytes;
- validation against externally supplied expected authorization/claim digests and session;
- rejection of expiry, consumption, unknown fields, path collisions, scope drift, command drift,
  test drift and predecessor mismatch before worker invocation;
- proof that external root withdrawal prevents claim creation and worker invocation;
- direct worker invocation with no reusable `PASS` token or verification-only mode;
- exactly one content-addressed authorization, claim and authority-created `ExecutionReceipt`;
- create-exclusive/idempotent receipt behavior for pass, block, crash recovery and divergence;
- implementation workers cannot import, write or invoke authority artifact paths; and
- the advisory-boundary limitation is observable in operator documentation and test names.

Explicitly deferred are artifact semantics, edge semantics, server/API/MCP/bus wiring and any
claim that unrestricted host access has become sandboxed. Promotion to CVR-001 requires a terminal
`PASS` receipt for this guard SWU and independent authority/implementability review.

## SWU-ACI-CVR-001 — Artifact projection

### Exact future write scope

- `implementations/vault_read/**/*.py`
- `implementations/vault_read/requirements.lock`
- `implementations/tests/vault_read/**/*.py`

Explicitly excluded: `implementations/server/**`, `implementations/requirements.txt`, APIs/routes,
bus, APT, inventory/cache implementation, canonical-source mutation and every path not listed
above. Every authority implementation path and every artifact under
`work-pack/authorizations/**` is excluded; the implementation writer returns outcome evidence to
the guard and creates no authorization, claim or receipt.

`repository_write_scope` is exactly those implementation/test paths. Authorization, claim and
receipt paths belong exclusively to root-owned authority scope. Separately,
`ephemeral_host_effect_scope` permits one unique OS temporary root
`<system-temp>/aci-cvr-001-<GUID>/` for the CPython 3.12 venv, pip staging and pytest caches. It
permits no repository write. Pip uses no cache and only `https://pypi.org/simple`; cleanup of that
exact temp root is mandatory and recorded.

### Prerequisites

1. exact ADR/SPEC/test/work-pack digests have clean independent document reviews;
2. architecture, product/protocol and host/operator accept their named decisions;
3. root issues a current exact-scope single-use authorization;
4. the source-cap measurement is recorded with command, scope and limitations;
5. exact `PyYAML==6.0.1`, `pytest` and every transitive dependency resolve reproducibly with hashes
   from the CVR-local lock;
6. restricted-loader golden vectors cover duplicates, tags, merges, aliases and timestamp/boolean
   coercions before semantic code can be accepted; and
7. artifact golden projections calibrate `max_results`.

### Done criteria and required future verification

- capture/snapshot, artifact projection and raw Connections declaration preservation are coherent,
  deterministic and effect-free; recognized unresolved targets use `resolution=unresolved`;
- `list_artifacts` and `get_artifact` satisfy applicable T-CVR-1–6, artifact half of T-CVR-9,
  artifact portions of T-CVR-10, raw-declaration portion of T-CVR-8, and T-CVR-11–12;
- import-boundary checks prove no `implementations.server` dependency;
- zero-effect spies prove no write, event, bus, APT, inventory or cache effect;
- the receipt records exact files, resolved dependency, golden/cap measurements, commands and
  results, pre-claim withdrawal or post-claim cancellation evidence when applicable,
  authorization consumption and remaining blockers.

No executable CVR tests are claimed to exist yet. At selection time the CVR-001 closed descriptor
must freeze exact test paths and commands. The guard owns environment creation, dependency
installation, worker invocation, diff validation, cleanup and finalization; duplicated
PowerShell bootstrap/wrapper logic is forbidden.

The sole CVR-001 `ExecutionReceipt` records exact CPython, pip and configured index identities,
downloaded artifact filenames/hashes, resolved package hashes, proof that install and tests used
the same isolated interpreter, cache confinement, cleanup evidence and the exact test outcomes.
It also includes a canonical byte-level baseline manifest covering every CVR-001-created or
modified repository file: normalized path, pre-write state/hash, final SHA-256, size and artifact
schema/version. The guard creates this receipt even for a blocked outcome. CVR-002 must consume
this receipt and baseline as authority preconditions.

## SWU-ACI-CVR-002 — Edge projection

### Exact future write scope

- `implementations/vault_read/**/*.py`
- `implementations/tests/vault_read/**/*.py`

No dependency mutation is allowed without a newly accepted ADR. All exclusions from CVR-001
continue to apply, including every authority implementation path and
`work-pack/authorizations/**`.

### Dependencies, done criteria and verification

CVR-002 requires an authority-created CVR-001 `ExecutionReceipt` with outcome `PASS`, its complete
byte-level baseline manifest and a new content-addressed, single-use authorization/claim pair for
the authenticated CVR-002 session. Its closed descriptor binds the predecessor receipt digest,
baseline digest, exact allowed file delta and pre-write hash (or explicit `absent`) of every
allowed path. Any unlisted change, baseline drift, missing predecessor evidence or pre-write hash
mismatch blocks before worker invocation.

The worker consumes CVR-001 raw declarations and extends the same core with endpoint resolution,
logical-edge normalization, `list_edges` and `get_edge`. The guard must rerun the complete
CVR-001 test selection before the CVR-002 tests, in the same isolated interpreter, then run the
resolution portion of T-CVR-8, T-CVR-7, projection half of T-CVR-9 and edge portions of
T-CVR-6/10/12. The final diff must equal the descriptor-bound allowed delta. The sole
authority-created CVR-002 `ExecutionReceipt` records both test groups, predecessor and baseline
digests, observed pre-write hashes, final delta, cleanup and outcome.

At selection, the CVR-002 closed descriptor freezes all exact commands and test paths. The common
guard owns bootstrap, verification, invocation, cleanup and receipt creation; no CVR-002-specific
PowerShell wrapper exists. CVR-002 never reuses the CVR-001 environment, authorization or claim.

## Terminal states

`pass`, `block`, `flag` and `interrupted` require the authority-owned exact `ExecutionReceipt`,
which consumes the named authorization and records the outcome/reason. Retry requires a new
authorization and claim. No CVR unit promotes TASK-000, W0 or unrelated runtime work.
