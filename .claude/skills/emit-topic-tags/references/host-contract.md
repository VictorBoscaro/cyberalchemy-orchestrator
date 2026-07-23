# Topic-tag host contract

This reference is for telemetry implementation and release evaluation. Do not load it into the agent's
ordinary tag-emission context. The agent-facing instrument is `../SKILL.md`.

## Boundary

The host owns scheduling, trusted mode selection, activation identity, evidence construction,
authorization, validation, persistence, idempotency, state, privacy, normalization and projection.
Invoke `deposit` from a close/`finally` hook; the skill cannot guarantee its own execution.

Stamp `agent_instrument_version: emit-topic-tags/1.0.0` plus a digest of the exact instrument records
shown to the model. Version this host contract independently as `apt-topic-host-contract/1`.

## Evidence

Construct instrument and evidence records separately; never recover membership through semantic
slicing after inference. For each observation stamp:

- `evidence_form`: `verbatim | compacted | mixed | unknown`;
- `evidence_coverage`: `complete | partial | unknown`, structurally relative to enumerated expected
  evidence-record IDs through cutoff;
- `semantic_compression_loss`: `none | possible | known | unknown`;
- `evidence_scope`: `full-activation | caller-authorized-view`;
- evidence/disclosure-policy references and digests.

Use `none` only for verbatim or proven-lossless evidence, `possible` for a known lossy transform with
no identified material omission, `known` for documented omission and `unknown` otherwise. Coverage is
relative to scope; do not compare absence claims across scopes as equivalent.

For `produce`, require a caller-supplied record or a host-filtered/authorized view. Never use the model
as the access-control boundary.

## Instrument and evidence digests

For `apt-instrument-digest/1`, SHA-256 the ASCII prefix `apt-instrument-digest/1\n` followed by each
ordered instrument record. Frame a record as: 4-byte unsigned big-endian role-name byte length, UTF-8
role name, 8-byte unsigned big-endian content byte length, exact UTF-8 content. Instrument records are
explicitly typed at prompt construction and contain the governing instrument instructions, skill body
and trusted mode/cutoff invocation.

`apt-evidence-digest/1` uses the same framing with prefix `apt-evidence-digest/1\n` over every ordered
evidence record supplied to the observer. Keep deterministic evidence digests inside the evidence's
access boundary. For less-restricted correlation, use an opaque random reference or versioned
HMAC-SHA-256 with a restricted rotatable key and recorded non-secret key ID/scope.

Also record model/provider version, requested inference parameters, provider-reported effective
values (`unknown`/`unreported` when unavailable), effective persona/configuration, visible tool
description/schema digests and sensitive-detector configuration digests.

## Payload validation

Validate in order: parse strict RFC 8259 JSON/tool arguments; validate decoded Unicode scalar strings;
run sensitive-value detectors; accept; then derive comparison keys.

Require 0–24 unique non-empty strings, each at most 96 UTF-8 bytes. Measure the 2 KiB limit after
canonical compact serialization: brackets and commas, quoted strings, no optional whitespace, `/`
unescaped, quotation mark and reverse solidus escaped, all other allowed scalars as direct UTF-8.

Under Unicode 15.1 reject malformed scalars, `Cc`, leading/trailing `White_Space`, and `Cf` except
U+200C/U+200D when internal and adjacent on both sides to category `L*` or `M*` code points.

Before acceptance/publication run versioned deterministic detectors for credentials, private
URLs/paths and configured identifiers. Reject/quarantine a match without echoing its value. Detection
is defense in depth, not proof of non-sensitivity.

## Attempts and idempotency

Create one opaque `emission_operation_id` before the first attempt and reuse it across retries and
reconciliation. Maintain an immutable attempt log and a derived capture state:

- `accepted` if any attempt is accepted;
- otherwise `acceptance-unknown` if ambiguity remains unresolved;
- otherwise `failed` if a definite failure exists;
- otherwise `rejected` if an explicit rejection exists;
- otherwise `missing`.

Append repair and reconciliation events; never rewrite history. Permit one total agent repair retry
for explicit pre-acceptance rejection. Retry ambiguous transport only under a declared idempotency
contract. At most one logical emission per operation may be accepted.

For rejected attempts retain safe status/time/code/counts and a protected reference. Never expose a
public digest oracle for low-entropy candidate values. Quarantined raw payloads require controls at
least as restrictive as accepted observations.

A quarantine release is a new validation plus authorization event recording approver identity/role,
safe rationale, policy/detector versions and scoped bypass. It may accept only while the operation has
no accepted emission. A later release is audit-only or a distinct non-original operation.

## Sensitivity and projection

Apply category-level sensitivity policy at the host boundary. Ingestion-required policy failure makes
capture `failed` and accepts no raw. Projection-only policy failure leaves authorized capture
`accepted`, marks projection `projection-failed` and publishes nothing affected. Neither blocks the
substantive deliverable.

Keep protected and disclosed planes separate. Protected analysis may key raw tags internally. Public
projection first suppresses/generalizes, validates projected strings, then derives/coalesces keys.
Raw keys and raw support links never cross the disclosure boundary. Apply disclosure policy to flags,
counts, digests and support links as well as values.

Generalized outputs must satisfy tag scalar invariants. Coalesce projected collisions while retaining
authorized lineage to all raw origins and transforms.

## Comparison keys

Preserve accepted raw strings. `apt-tag-key/1` applies Unicode 15.1 NFC, removes leading/trailing
Unicode 15.1 `White_Space`, then applies Unicode 15.1 full default case folding. It performs no
stemming, translation, tokenization or semantic mapping.

Within one emission, count a comparison key once. If distinct raws collapse to one key, retain all
authorized raw support links. A Unicode/algorithm change creates a new key version and never rewrites
old observations.

## Release

Run every case in [`conformance.md`](conformance.md). Mechanical conformance is necessary but not
sufficient; the frozen semantic forward-test is the release gate for the agent-facing instrument.

