# RWO Semantic Contract 1.0.0

Status: lifecycle-neutral contract content
Canonical creation: authorized only by an external exact owner-acceptance receipt
Admission: complete only after canonical byte creation and post-creation validation
Effects: authority none; promotion none; implementation none
Contract: `RWO-SEMANTIC-CONTRACT/1.0.0`
Profile: `RWO-JCS-IJSON-SAFEINT/1.0.0`
Unicode data: `15.1.0`
Digest: `SHA-256`
Canonical payload: RFC 8785 JCS after admission and semantic normalization

This document is normative for the candidate content set. It defines semantic
identity shared by a future Python oracle, Rust kernel, Go service, and adapters.
It does not assign domain truth, journal acceptance, retry scheduling, effect
authority, or implementation ownership.

## Identifier grammar and version tuple

Contract, profile, schema, type, and version identifiers are ASCII and match
`[A-Za-z0-9][A-Za-z0-9._/-]*`. Every operation declares an exact tuple:

`(contract_id, contract_version, profile_id, profile_version, schema_id, schema_version, value_type)`.

Version 1 accepts only an exact registered tuple. Any unknown major, minor, patch,
schema, profile, or type version returns `VERSION_TUPLE_UNSUPPORTED`. Compatibility
projection requires a separately registered, owner-accepted artifact with source
and target tuples, total algorithm, loss declaration, and vectors.

## Raw admission

`admit(profile, schema, raw_utf8_json) -> Admitted(value) | Rejected(defects)`

Apply these rules in order:

1. Reject a leading UTF-8 BOM, invalid or incomplete UTF-8, incomplete JSON, and any
   non-whitespace trailing token.
2. Tokenize while preserving every object-name occurrence and raw number token.
   Decode escapes for name comparison and reject decoded-equivalent duplicate names
   before ordinary map construction.
3. Reject strings or names containing surrogate code points, Unicode
   noncharacters, code points unassigned by Unicode 15.1.0, or text unequal to its
   Unicode 15.1.0 NFC form. Admission never rewrites text.
4. A JSON number is admissible only when its raw token matches
   `0|-?[1-9][0-9]*` and its value is in
   `[-9007199254740991, 9007199254740991]`. Thus negative zero, fractions,
   exponents, leading zeros, plus signs, NaN, and infinity reject.
5. A schema-declared canonical-decimal string is admissible only when it matches
   `(?:0|-?(?:[1-9][0-9]*)(?:\.[0-9]*[1-9])?|-?0\.[0-9]*[1-9])`.
6. Validate the exact tuple and a closed schema. Reject missing required fields,
   unknown fields, invalid enum values, and undeclared versions.

Collect all recoverable defects expected by a vector and order them by the
structural-defect comparator.

## Semantic normalization

`normalize_semantics(schema, admitted_value) -> normalized_value`

- Objects retain their fields; JCS orders names.
- Ordered arrays retain input order.
- Every order-insensitive field declares
  `{elementType, primaryKeyPaths, duplicatePolicy}`.
- Version 1 supports only `duplicatePolicy: reject`.
- Normalize elements recursively and sort by
  `(primary-key component tuple, canonical payload bytes of the normalized element)`.
- String key components compare by unsigned UTF-16 code units, integers
  mathematically, and bytes unsigned lexicographically.
- Equal primary keys and fallback bytes are
  `DUPLICATE_SEMANTIC_IDENTITY`.

The comparator is total and uses canonical bytes, never a hash, as the fallback.

## Canonical payload bytes

`canonical_payload_bytes(profile, schema, normalized_value) -> bytes`

Apply RFC 8785 JCS:

- UTF-8, no BOM or trailing newline;
- JCS string escaping and object-name ordering by unsigned UTF-16 code units;
- normalized array order;
- canonical admitted integer tokens;
- canonical-decimal quantities remain JSON strings.

Payload bytes identify a representation, not a domain identity.

## Typed semantic digest

`semantic_digest(contract, profile, schema, value_type, payload_bytes)`
returns `sha256:` plus lowercase hexadecimal SHA-256.

```text
u32be(n) = unsigned 32-bit big-endian integer
u64be(n) = unsigned 64-bit big-endian integer
text(s)  = u32be(len(UTF8(s))) || UTF8(s)
blob(b)  = u64be(len(b)) || b

preimage =
  ASCII("RWO-SEMANTIC-DIGEST") || 0x00 ||
  text(contract_id) || text(contract_version) ||
  text(profile_id) || text(profile_version) ||
  text(schema_id) || text(schema_version) ||
  text(value_type) || blob(payload_bytes)
```

Lengths count bytes. Oversized fields reject before hashing. Protobuf and language
serialization never participate.

## First-slice value types

### Accepted event

`AcceptedEventIdentity/1.0.0` contains exactly `stream_id` and `event_id`.
`AcceptedEventPayload/1.0.0` contains exactly `event_type`,
`source_node_id`, and the event-specific `payload`.
`AcceptedEventView/1.0.0` is their closed merge.

`accepted_event_identity` and `event_payload_digest` are typed semantic digests.
Delivery ID, attempt, wall time, tracing, broker offset, and adapter metadata are
excluded.

### Work graph

`ExplicitComposition/1.0.0` and `WorkGraph/1.0.0` contain the exact contract
tuple, one composition ID, nodes keyed by `node_id`, and edges keyed by
`edge_id`. Nodes and edges are order-insensitive. An edge declares source,
target, accepted event type, event payload schema, emitted command type, command
payload schema, and `payload_derivation`. Version 1 admits only
`copy-event-payload`: normalize and validate the accepted event payload under its
declared schema, copy the resulting value without mutation, and validate it under
the declared command payload schema. Incompatible schemas reject compilation.
Compilation rejects missing endpoints and more than one matching edge for the
first slice. `graph_identity` is derived and not a graph field.

### Command intent

`CommandIntentIdentity/1.0.0` contains exactly graph identity, edge ID, accepted
event identity, command type, and target node ID.
`CommandIntentPayload/1.0.0` contains exactly command type, target node ID, and
the command-specific payload. The command intent envelope is their closed merge.

`command_intent_identity` and `command_payload_digest` are derived. A delivery
retry preserves both identities and the complete immutable intent.

### Cursor

`OrchestrationCursor/1.0.0` contains reducer semantics version, graph identity,
stream ID, accepted-event identity-to-payload-digest entries, satisfied edge IDs,
and emitted-command identity-to-payload-digest entries.

All three arrays are order-insensitive. They sort respectively by accepted-event
identity, edge ID, and command-intent identity, and reject duplicates. Cursor
identity is derived and not stored.

## Compile

1. Admit and normalize `ExplicitComposition/1.0.0`.
2. Validate identifiers, endpoints, event/command declarations, both payload schema
   references, `copy-event-payload` compatibility, and first-slice cardinalities.
3. On any defect, return ordered `Rejected(defects)` and no graph.
4. Construct and normalize `WorkGraph/1.0.0`.
5. Compute graph bytes and typed graph identity.
6. Return `Compiled(graph, canonical_bytes, graph_identity)`.

## Reduce

Reject with the byte-identical original cursor unless versions, graph identity, and
stream ID match. Derive event identity and payload digest.

- Existing identity and same digest: `Duplicate(original_cursor)`.
- Existing identity and different digest:
  `DivergentDuplicate(DIVERGENT_DUPLICATE, original_cursor)`.
- New event: record it, then select unsatisfied edges matching source and event
  type.
- More than one match: `Rejected(MULTIPLE_EDGE_MATCH, original_cursor)`.
- No match: `Applied(next_cursor, null)`.
- One match: copy the normalized event payload under the edge's declared
  `copy-event-payload` rule, validate it against the command payload schema, and
  derive the immutable command identity and payload.
- Existing command identity with another payload:
  `Rejected(DIVERGENT_COMMAND_INTENT, original_cursor)`.
- Existing same command: satisfy the edge if needed and return no new intent.
- Otherwise record edge and command identities and return
  `Applied(next_cursor, command_intent)`.

A non-matching new event remains observed. Duplicate, divergent duplicate, and
rejected outcomes do not mutate the cursor.

## Structural defects

Phase ranks are `decode=0`, `admission=1`, `schema=2`,
`normalization=3`, `compilation=4`, and `reduction=5`.
A path is an array of `field(name)` or `index(n)` segments; fields sort before
indices, field names by unsigned UTF-16 units, and indices numerically. Codes match
`[A-Z][A-Z0-9_]*` and compare bytewise. `detail_digest` is the typed digest of
one closed `DefectDetail/1.0.0` value.

Sort defects by `(phase_rank, path, code, detail_digest)`. A fully equal duplicate
defect is an implementation conformance failure.

## Retry boundary

The kernel returns semantic outcomes; it never schedules delivery. Service/adapter
policy maps one explicit `RetrySituation` to one treatment:
`DoNotRetry`, `RetrySame`, `ReconcileThenDecide`, `DeadLetter`, or
`Escalate`.

Unknown delivery does not default to retry. `RetrySame` must preserve command
identity, payload digest, and immutable intent. Kernel rejection, divergent replay,
invalid commands, authority denial, and acceptance-critical validation failure are
terminal. Attempts, deadlines, backoff, jitter, leases, and circuit state remain
outside semantic identity.

## Fixture governance

`CONFORMANCE-MANIFEST.json` binds the contract/profile/Unicode/schema registry,
all vector inputs, expected observations, expected bytes/digests where applicable,
and provenance. It contains no self digest or acceptance claim.

`CONFORMANCE-MANIFEST-REVIEW.json` binds the manifest digest and size, producer
identity, a distinct reviewer implementation identity, review method, accepted
vector IDs, and comparison result. The reviewer path must not import or call the
producer.

Ordinary tests read expectations and must never regenerate them. Manifest changes
invalidate the detached review. Owner acceptance binds the frozen candidate content
digest, then a separate material apply may create canonical targets.

## Non-effects

This contract does not prove an implementation, cross-language conformance,
performance, runtime integration, journal correctness, exactly-once effects,
publication, deployment, release, or production readiness.
