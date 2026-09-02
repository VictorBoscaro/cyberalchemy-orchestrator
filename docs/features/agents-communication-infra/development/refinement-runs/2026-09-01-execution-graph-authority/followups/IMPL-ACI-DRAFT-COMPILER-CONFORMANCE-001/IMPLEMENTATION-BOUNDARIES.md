# Bounded compiler implementation contracts

Status: implementation-conformance boundary for `IMPL-ACI-DRAFT-COMPILER-CONFORMANCE-001`; not a
canonical ACI v2 specification and not runtime authority.

## Allocator evidence

The conformance gate accepts the frozen compilation-context JSON only with an Ed25519 receipt under
the embedded fixture allocator public key. The signed payload binds the canonical context digest,
key ID, latest-reservation assertion and accepted-pair-unbound assertion. No private signing key is
stored in this repository.

`VerifiedCompilationContext` is opaque, immutable and process-local. Direct construction, copying,
deep-copying and pickling fail. The compiler also requires object identity registered by the gate
and re-verifies the signed receipt on every compile call. This proves the fixture host boundary; it
does not claim a live allocator or production key lifecycle.

## Returned authority

Canonical bytes are the sole stored logical authority in `CompilationResult`. `digest` is computed
from those bytes on access. `graph` and the external restriction report are decoded as fresh values
on each access, so caller mutation cannot alter the bytes or create cross-node aliases.

## Selector subset

The only admitted DraftGraph v1 content selector is the literal `$`, meaning the whole bound content
member under the pinned fixture semantics. No path, URI, query, JSONPath or runtime-defined selector
is admitted. Other non-empty selectors fail as `DG_SELECTOR_UNSUPPORTED`; an empty selector is a
structural DraftGraph error.

## Resource subset

This SWU admits inline `utf-8` or `base64` content only and verifies SHA-256 over exact decoded
bytes. `immutable_uri` is structurally prohibited because this pure compiler has no retrieval proof
input. Adding content-addressed URI support requires a separately reviewed resolver-evidence
contract.

## Output-schema subset

Embedded schemas are strict JSON: duplicate keys, `NaN`, infinities and invalid JSON fail closed.
They must pass the Draft 2020-12 metaschema, have a closed top-level object, and admit a mechanically
constructed witness. The witness subset supports direct `type`, `const` and `enum`, closed required
objects and bounded arrays. References/composition are rejected for witness proof. A required
`false` property or any other witnessed contradiction is `DG_OUTPUT_CONTRACT_INVALID`.

This is a mechanical satisfiability proof for the admitted subset, not a general JSON Schema
satisfiability claim.

## Topology state machine

Data inputs create `data/on_success` routes. Non-feedback authored routes and ordinary data routes
form the initial DAG. Feedback edges and reverse data dependencies explicitly authorized by the
same feedback pair do not create initial predecessors, roots or DAG cycles. A reverse feedback input
must be optional so the entry node can start without future output.

Initial execution rules are:

- a node with no initial predecessor must be listed as an entry and use `roots_ready`;
- a node with an initial predecessor cannot use `roots_ready`;
- a required node-output input must reference a producer output that is itself required;
- the initial non-feedback graph must be acyclic and every node must be reachable from an entry;
- every initial branch must reach a terminal or a node with an explicit graph stop/fail action.

For this bounded compiler, an edge condition defines a route event: `on_success` carries states in
which its source succeeded, `on_failure` carries states in which it failed, and `always` carries
both outcomes. `any_predecessor_succeeded` selects the union of states that can activate any one
incoming route; `all_predecessors_succeeded` uses only compatible merges in which every incoming
route activated. The historical field names are retained from the proposed schema; this route-event
definition is the closed implementation semantics used for conformance.

Readiness is proved by a conditional must-availability dataflow over the topological order. Each
abstract state records disjoint sets of succeeded and failed nodes. A successful node outcome adds
that node to the succeeded set, which proves its required outputs materialized; a failed outcome
does not. An `any` join preserves every possible activating state. An `all` join computes compatible
Cartesian merges and rejects when no joint state exists. For every node, the intersection of
succeeded nodes across all its start states is the producer set guaranteed available. Every
required node-output input must belong to that intersection. Required resource inputs are already
materialized and digest-verified; optional inputs impose no availability obligation.

The proof retains at most 4,096 distinct outcome states per node or merge. Exceeding that limit is a
typed fail-closed rejection, so complex but safe graphs can be false negatives rather than authority
expansions. Feedback activation after the initial pass remains represented but is not scheduled or
included in this proof; reverse feedback inputs therefore remain optional and cannot establish a
required-input guarantee. A feedback target with any required node-output input is rejected because
the initial model cannot prove that input remains available on reactivation. Feedback targets whose
required inputs are all material resources remain admissible.

## Unicode domain

Every parsed context, allocator-evidence, draft, policy, catalog and resource tree is recursively
checked for Unicode scalar strings before structural validation, hashing or serialization. Lone
surrogates in values or member names return the input's typed structural error and stable path.
Embedded output-schema JSON receives the same guard after its inner parse. Canonicalization and
compilation-match helpers guard their public values independently, so no encoding site can expose a
raw `UnicodeEncodeError`.

## Structural validation

The delivered context, allocator-evidence, policy, catalog and resource schemas, the reviewed
DraftGraph schema and the proposed ExecutionGraph schema are compressed into the Python module as
exact artifact bytes. Each embedded byte string is checked against an explicit SHA-256 before its
Draft 2020-12 validator is constructed. `bundled_contract_schema_digests()` exposes defensive digest
values so the conformance test can prove correspondence to the seven review artifacts.

Module import and compilation perform no filesystem reads; the repository schema files are review
evidence and generation inputs, not runtime dependencies. Each parsed value passes the corresponding
embedded validator before semantic checks. Structural errors are wrapped into typed compiler errors
with a stable lexicographically selected instance path. Semantic table traversal follows fixed table
and draft order; it never depends on Python hash iteration.
