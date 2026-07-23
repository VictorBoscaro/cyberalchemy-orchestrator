---
feature: agents-communication-infra
adr: ADR-CVR-001
title: Parser, module, policy and delivery boundaries for canonical vault reads
status: proposed
acceptance_status: prepared-for-owner-review
date: 2026-07-23
layer: L0
slice: CVR
swu: SWU-ACI-CVR-000
runtime_gate: block
work_pack_gate_status: block
cvr_implementation_gate: approval_packet_prepared
---

# ADR-CVR-001: Parser, module, policy and delivery boundaries for canonical vault reads

## Status and decision boundary

This ADR is a **proposal prepared for owner review**. It records the result of the
CVR option analysis; it is not an owner ratification, review receipt or consumable
implementation authorization. The author is a controlled documentation writer and is
not an owner of any decision below.

Gate precedence is fail-closed:

```text
authorized = (runtimeGate=pass AND workPackGateStatus=pass) OR
             (verified active named authorization for exactly one enumerated CVR SWU
              AND its closed descriptor and predecessor evidence verify
              AND scope is exactly the descriptor-bound effect-free CVR core)
```

This per-SWU branch is a **non-operative proposal** until this ADR, the CVR spec,
TEST-SPEC, TASK-CVR and the selected deterministic descriptor are amended and accepted as one
five-entry packet. Consequently, `cvrImplementationGateStatus=approval_packet_prepared` is a non-pass state.
For initial bootstrap, the fifth entry is exactly
`docs/features/agents-communication-infra/work-pack/descriptors/SWU-ACI-CVR-GUARD-001.json`.
It cannot override either global block. Only the root/project owner together with the
owners named in [Required ratifications](#required-ratifications-and-approval-conditions) may create a nominal,
single-use authorization consumed by an enumerated SWU. This ADR does not create it.
The first proposed executable unit is `SWU-ACI-CVR-GUARD-001`, bootstrapped non-recursively by an
external trusted executor under an exact root-owned one-time authorization. Global gates continue to block runtime/integration, HTTP, MCP,
agent-tool and server work. No authorization or carve-out activation exists now, and
CVR-002 requires its own later decision and authorization.
The predicate is currently false.

## Context

The [Canonical Vault Reads contract](../specs/canonical-vault-reads.md) defines a
read-only projection over admitted Markdown bytes but intentionally left parser,
module, root policy, initial limits and delivery sequence open. Those choices must be
settled without importing the projection into the current audit-ledger server, treating
the working directory as policy, or allowing a YAML library to define canonical bytes.

A local capacity observation was made on 2026-07-23:

| Observed subtree | Regular files | Aggregate bytes | Largest file |
| --- | ---: | ---: | ---: |
| `vault/` | 12 | 193,801 | 48,374 |
| `docs/` | 143 | 1,855,196 | 77,532 |

The observation is a sizing receipt, not an admission rule or completeness proof. It
used a recursive local regular-file enumeration of the two named subtrees and measured
filesystem byte lengths. It did not validate repository identity, parse documents,
follow or characterize links/reparse points, classify privacy, measure projected result
cardinality, or prove behavior on another checkout or operating system.

## Proposed decision

### D1 — Explicit byte-to-projection pipeline

Use this versioned pipeline:

```text
captured source bytes
  -> strict UTF-8/BOM decode and frontmatter-fence split
  -> restricted YAML loader for the frontmatter payload
  -> local Markdown headings and Connections-table projection
  -> typed node/declaration residue
```

The sole dependency candidate for the YAML stage is `PyYAML==6.0.1`, because 6.0.1 is
the only version observed in the current host. Host presence is not reproducible
admission. `SWU-ACI-CVR-001` may consume this candidate only after an exact dependency
declaration and reproducible lock/install receipt exist and all golden parser vectors
pass against the resolved version.

The loader contract, rather than library defaults, must:

- reject duplicate mapping keys;
- reject unknown or application-specific tags;
- reject merge keys;
- either reject aliases entirely or admit a separately reviewed, finite alias policy;
- resolve timestamps as strings, never implicit datetime objects;
- use an explicit YAML 1.2-style boolean vocabulary (`true`/`false` only), avoiding
  implicit YAML 1.1 forms such as `yes`, `no`, `on` and `off`;
- bound scalar, collection and nesting work through the source-byte and implementation
  safety ceilings; and
- preserve invalid YAML and fences as typed residue without repair.

The parser ceilings are part of `parser_version`: frontmatter payload 65,536 bytes,
nesting depth 32, total YAML nodes 10,000, collection items 4,096 and one scalar at
most 32,768 UTF-8 bytes. Aliases, merge keys and custom/application tags are forbidden.
Each exact ceiling and its `+1` case requires a golden vector. A breach becomes one
whole-source `parse_limit_exceeded` residue and never a call-wide error or partial parse.
The scalar ceiling remains below both the 65,536-byte frontmatter ceiling and
`max_file_bytes=524288`. Parser-limit checks precede YAML construction; when several
parser limits collide, the earliest bytewise detection wins, with frontmatter bytes,
scalar bytes, depth, node count and collection count as the stable tie-break order.

PyYAML supplies parsing only. It owns neither source canonicalization, projection
canonicalization, path identity nor digests. Any failure to pin/install exactly,
enforce the restricted-loader contract, or reproduce golden vectors returns the gate
to `block` and requires an ADR amendment. Silent dependency upgrades are forbidden.

Invalid UTF-8 is a whole-source parse outcome, not a call-closing
`invalid_encoding` error. The node remains safely enumerable with its selector,
snapshot binding, source digest and a non-content locator; `title=null`,
`sections=[]`, and `connections=[]`. Frontmatter/fence/YAML failures likewise produce
typed residue and never synthesize repaired frontmatter, headings or edges.

### D2 — Separate core module and later transport

The future core belongs under `implementations/vault_read/`, with its tests under
`implementations/tests/vault_read/`. It must not import from, add routes to, or be
imported by `implementations/server/` during `SWU-ACI-CVR-001`. HTTP, MCP and agent-tool
adapters are later SWUs and must delegate to the same core instead of duplicating
capture, admission, parsing or projection.

The CVR dependency pin belongs only in
`implementations/vault_read/requirements.lock`. Reusing or editing the existing
`implementations/requirements.txt` is rejected for CVR because it couples the new
vault-read core to the audit-ledger control-plane dependency boundary.

### D3 — Explicit policy profiles with empty default

The default admitted-root set is empty. An empty or unratified policy returns
`policy_unavailable`; there is no fallback.

A proposed versioned development profile may admit only `vault/`, and only when:

1. the host/operator explicitly selects that profile;
2. the host validates the expected repository identity before resolving the root;
3. the lexical and resolved root are repository-contained; and
4. `allow_private=false`.

The current working directory, environment variables, filesystem discovery and request
fields cannot select, infer or widen roots. A request never carries roots, privacy or
limits.

Admission is staged in this order: lexical/resolved confinement, hidden-component and
link/reparse denial; bounded prefix/frontmatter quarantine parse sufficient to classify
privacy; privacy exclusion; then full capture and parsing. A malformed or unknown
privacy classification is non-enumerably excluded for an unprivileged scope; a
privileged scope may receive its typed residue. Private excluded sources do not enter
aggregate source/byte/result caps; visible private sources in a privileged scope do.
Capture rechecks the admitted source so mutation yields one coherent admitted snapshot
or `snapshot_conflict`.

Capture is operation-specific: list queries capture every admitted visible source;
direct get validates and captures only its selected visible source. Its snapshot binds
that selected set. List/get parity means the same policy and source state produce the
same visibility and node projection, not that direct get performs a global scan.

### D4 — Candidate limits and compiled ceilings

The proposed development profile values are:

| Limit | Candidate value |
| --- | ---: |
| `max_file_bytes` | 524,288 |
| `max_files` | 2,048 |
| `max_total_bytes` | 33,554,432 |
| `max_results` | 10,000 |

All four values are bounded by compiled safety ceilings, and each effective profile is
versioned. The source caps have substantial headroom over the 2026-07-23 local
observation. `max_results=10000` remains a candidate until a golden corpus measures the
actual node/residue projection cardinality. Exceeding any effective cap yields the same
call-closing `result_set_too_large` outcome and no partial result.

`max_results` is evaluated per method. `list_artifacts` counts top-level
`VaultNodeProjection` items; `get_artifact` counts exactly its one returned node;
`list_edges` counts top-level `LogicalVaultEdgeProjection` items; and `get_edge` counts
exactly its one returned logical edge. Nested declarations, sections and residue do not
consume additional result slots. A whole-source `invalid_utf8` item is one node and
therefore consumes one artifact-result slot.

### D5 — Four staged units, one core

| SWU | Scope | Global gates | Nominal CVR gate | Current state |
| --- | --- | --- | --- | --- |
| `SWU-ACI-CVR-000` | Five-entry packet plus seven derived indexes: 12 governed artifacts including the descriptor. | `runtimeGate=block`; `workPackGateStatus=block` | `approval_packet_prepared` | Documentation prepared; no runtime effect. |
| `SWU-ACI-CVR-GUARD-001` | Pure verifier, deterministic descriptors and common finalizer for CVR-001/002; bootstrap uses one external finalizer. | `runtimeGate=block`; `workPackGateStatus=block` | Proposed exact one-time bootstrap only. | Blocked pending coordinated packet acceptance. |
| `SWU-ACI-CVR-001` | Capture/snapshot core, artifact projection, raw Connections declaration preservation, `list_artifacts`, `get_artifact`, and applicable tests. | `runtimeGate=block`; `workPackGateStatus=block` | No `pass_with_named_swu_authorization` exists. | Blocked. |
| `SWU-ACI-CVR-002` | Endpoint resolution, logical-edge normalization, `list_edges`, `get_edge`, and applicable tests. | `runtimeGate=block`; `workPackGateStatus=block` | No `pass_with_named_swu_authorization` exists. | Blocked and deferred until CVR-001 acceptance. |

The public contract retains all four queries. Separating delivery does not create two
capture engines, parser policies or admission authorities: CVR-002 must extend the
CVR-001 core. Recognized declarations not resolved during CVR-001 carry `resolution=unresolved`.

## Exact future write scopes

These are maximum proposed scopes, not current authorization.

| SWU | Permitted future writes |
| --- | --- |
| `SWU-ACI-CVR-000` | Five-entry packet plus seven derived indexes (12 governed artifacts, descriptor included); indexes remain outside the packet digest. |
| `SWU-ACI-CVR-GUARD-001` | External trusted bootstrap executor may write only `implementations/vault_read_guard/**/*.py` and `implementations/tests/vault_read_guard/**/*.py`; descriptor and authority artifacts are excluded. |
| `SWU-ACI-CVR-001` | `implementations/vault_read/**/*.py`; `implementations/vault_read/requirements.lock`; `implementations/tests/vault_read/**/*.py`. All authority paths are excluded. |
| `SWU-ACI-CVR-002` | `implementations/vault_read/**/*.py`; `implementations/tests/vault_read/**/*.py`. All authority paths are excluded; no dependency mutation without a new ADR. |

Any need to touch another path blocks that SWU and requires a new scope decision.

## Alternatives considered

| Alternative | Disposition |
| --- | --- |
| Parse frontmatter with ad-hoc string splitting only | Rejected as the primary parser: it would underspecify nested YAML already admitted by the corpus and move edge cases into silent local behavior. |
| Use the host's unpinned PyYAML | Rejected: observed availability is not a reproducible dependency or semantic contract. |
| Use PyYAML safe-loader defaults as the contract | Rejected: defaults do not settle duplicate keys, merges, aliases, implicit coercions, canonicalization or digests. |
| Introduce another YAML library now | Deferred: no other exact version is evidenced on the host. A challenger may supersede this proposal only with reproducible installation and the same golden vectors. |
| Put CVR routes directly in `implementations/server/` | Rejected for CVR-001: the existing server is the audit-ledger control plane, not the vault-read bounded context. |
| Admit `docs/` and `vault/` by default | Rejected: local presence is not host/operator authorization, and `docs/` materially expands the corpus. |
| Infer the repository from `cwd` or environment | Rejected: ambient state would become an implicit authority and allow policy widening. |
| Return invalid encoding as a call-wide error | Rejected: one bad source would hide safely enumerable evidence and prevent complete corpus inspection. |
| Return partial results at a cap | Rejected: callers could mistake a truncated projection for complete canonical inventory. |
| Implement all four queries in one SWU | Rejected for the first slice: artifact reads can falsify capture, admission and residue semantics before edge identity is added. |

## Falsifiers

This proposal must be amended or rejected if any of these occurs:

1. `PyYAML==6.0.1` cannot be resolved reproducibly or a golden vector demonstrates that
   the restricted loader cannot enforce the listed duplicate/tag/merge/alias/coercion
   rules without unsafe or unstable behavior.
2. A parser permutation changes canonical projections or digests for identical captured
   bytes and parser version.
3. Invalid UTF-8, fence or YAML input invents a title, section, connection or logical
   edge, or disappears instead of producing the specified typed residue.
4. Root selection can be influenced by request data, `cwd`, environment or
   autodiscovery, or repository identity is not verified before profile activation.
5. A cap breach returns any partial item.
6. CVR-001 requires a server import/route or creates a transport-specific second
   capture/parser implementation.
7. Golden projection measurements show that a candidate limit is not safe or useful.
8. Direct get requires a global scan or produces visibility/node bytes different from list under
   the same policy and stable source state.

## Required ratifications and approval conditions

Before any executable CVR SWU can receive a nominal, consumable authorization:

1. the architecture owner must ratify D1, D2, the dependency/lock approach and the
   CVR-000/GUARD-001/001/002 taxonomy;
2. the host/operator owner must ratify D3, D4, repository-identity validation, compiled
   ceilings and the versioned development profile;
3. the architecture owner together with the product/protocol owner must ratify D5 and
   the artifact/edge delivery carve-out without changing the four-query contract;
4. independent reviewers must find no unresolved safety, ownership or contract
   objection in the exact ADR/SPEC digests;
5. the root/project owner must approve the five-entry packet and may issue only an exact,
   content-addressed, single-use authorization; and
6. GUARD bootstrap must use the external trusted executor; later workers are invoked directly by
   the guard, which alone creates the terminal `ExecutionReceipt`.

Each execution has exactly three authority artifacts under
`docs/features/agents-communication-infra/work-pack/authorizations/<authorization_id>/`: canonical `authorization.json`, `claim.json` and
`execution-receipt.json`. There is no `current` pointer, persisted `ClaimReceipt`, revocation file
or second receipt. Root withdrawal is pre-claim only; post-claim cancellation terminalizes.
This is an advisory governance boundary on the unrestricted host, not a sandbox.

The authorization binds a fixed three-owner acceptance set, external authority-policy and
repository-binding digests, audience, executor and finalizer. The claim is the single immutable
create-exclusive lease. An ephemeral `AuthorityLaunchContext` supplied outside the workspace binds
authenticated root/executor/finalizer identities, session, trusted observed time and all governing
digests; only its digest enters the receipt. It is not a fourth artifact or new authority. Hashes
prove integrity, never identity. A trust policy/provider, reproducible repository binding, trusted
clock/nonces, target-filesystem create-exclusive proof and authenticated executor/finalizer remain
external prerequisites, so the proposal remains non-pass.

Approval of this ADR alone is insufficient. The feature-wide `runtimeGate` and
`workPackGateStatus` remain independently controlling and blocked.

## Consequences

The proposal makes parser behavior, malformed-source visibility, policy admission and
delivery layering falsifiable before code. It preserves the existing server boundary
and leaves transport integration for a later adapter. It also adds dependency-lock and
golden-vector work to CVR-001 and deliberately delays edge queries to CVR-002.

## Connections

| Document | Type | Description |
| --- | --- | --- |
| [Canonical Vault Reads](../specs/canonical-vault-reads.md) | `refines` | Applies these prepared parser, policy, module and delivery decisions to the contract. |
| [ACI SPEC](../specs/SPEC.md) | `depends-on` | Retains the feature-wide blocked runtime gate and authority boundaries. |
| [Vault Conventions](../../../../vault/ontology-conventions.md) | `depends-on` | Supplies current source labels and connection conventions; it is not modified here. |
