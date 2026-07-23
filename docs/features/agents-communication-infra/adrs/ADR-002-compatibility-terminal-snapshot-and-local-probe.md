---
feature: agents-communication-infra
adr: ADR-002
title: Compatibility, terminal, snapshot and bounded local-probe contracts
status: proposed-accepted-pending-independent-review
acceptance_status: pending
acceptance_receipt: ../reviews/2026-07-23-stage-a-freeze/reviewer-receipt.json
date: 2026-07-23
layer: L0
slice: S-000
swu: SWU-ACI-002
runtime_gate: block
---

# ADR-002: Compatibility, terminal, snapshot and bounded local-probe contracts

## Decision boundary

This ADR completes the authored decision set for `SWU-ACI-002`. It becomes accepted only when the
independent reviewer receipt named above is `PASS` and binds the exact artifact manifest digest.
Until then, and independently of it, production, audit-ledger cutover, external networking and
automatic agent execution remain blocked.

The accepted local-pilot claim is intentionally smaller than the complete ACI runtime: one
single-host activation may create or reuse a Session, strictly link one existing legacy dispatch,
accept a generic or reference-probe contribution as a durable candidate, independently verify it
into exactly one official message, and expose committed facts through rebuildable projections.

## Decisions

### D-002-1 — Fixed decision rule

The general Slice-0 group proof retains `fixed-two-seat-proof@1`: two valid votes are required;
equal votes produce `consensus`, conflicting votes produce `dissent`, and fewer than two produce
`no_quorum`. The bounded local-probe profile does not execute reveal/vote/commit and must not claim
that this rule ran. Its only decision is parent receipt verification of one publication candidate.

### D-002-2 — Unique terminal mapping

Only a unique accepted run terminal cause maps to the audit ledger. The mapping is:

| Runtime terminal cause | Audit `exit_reason` |
|---|---|
| committed result satisfies the confirmed goal | `resolved` |
| committed irreconcilable dissent remains after permitted rounds | `dissent_irreconcilable` |
| bounded policy reaches its declared loop ceiling | `loop_ceiling_reached` |
| explicit authorized cancellation wins terminal CAS | `user_abort` |
| technical failure, corruption, exhausted retries or resource exhaustion prevents an outcome | `error` |

Attempt and group terminals do not map directly. The local-probe vertical slice creates no audit
close and therefore exercises none of these mappings.

### D-002-3 — Frozen input and strict legacy snapshot

Runtime acceptance uses content-addressed artifacts and exact profile/schema digests. A legacy
dispatch may be linked only through a strict read-only resolver that:

1. reads the ledger bytes without modifying them;
2. requires the one-line grammar used by the validated appender;
3. requires one top-level `dispatches:` key and unique opening/close identities;
4. resolves exactly one opening row for the requested dispatch;
5. records `dispatch_id`, row kind, appender identity, contract version, exact row-byte digest and
   a canonical semantic-row digest; and
6. fails closed on corruption, ambiguity, absence or digest mismatch.

The lenient UI reader is never an authorization source. Historical rows are not imported or
rewritten. Linking must prove the ledger byte digest is unchanged.

### D-002-4 — Exact-row reconciliation

For future materialization, the same ledger identity plus the exact normalized row is
`applied/verified`; the same identity with divergent content is `reconciliation_required`.
Subprocess exit zero or ID-only deduplication is insufficient evidence. `.confirmed` remains an
ephemeral compatibility marker, never journal or ledger authority.

### D-002-5 — Authority ownership and cutover

- The current validated appender remains the sole physical writer of the YAML audit ledger.
- ACI's journal writer owns command/event acceptance.
- ACI's ArtifactStore owns physical artifact BLOB/finalization writes.
- ACI's ProjectionManager is the sole writer of rebuildable runtime/APT projections.
- No legacy watcher and runtime worker may own the same dispatch.

The W0 contract for this split can freeze now. Target-host process identity, ACL, deployed writer
inventory and negative bypass results remain mandatory TASK-020 evidence before materializer
cutover.

### D-002-6 — Candidate is not official

`publication.persisted` reserves one active logical key and returns a
`status=persisted_candidate` receipt only after commit. A separate parent-authorized
`VerifyPublicationReceipt` command must atomically verify the complete receipt and authoritative
candidate/event/artifact facts, append the registered official acceptance event, insert exactly one
`messages` row, update the candidate to `officially_accepted`, advance heads and persist its stable
command receipt. A candidate alone is never visible as an official contribution and cannot ground
APT lineage.

### D-002-7 — Local probe is a named profile, not a hidden full runtime

`SWU-ACI-APT-VS-001` may use the registered `local-probe-publication@1` composition to freeze a
single session/dispatch/probe/group/seat/attempt/round context. It does not authorize provider
launch, audit materialization, reveal, voting, deliberation, group commit or production deployment.

## Artifact and storage policy

The normative physical ownership and rebuild boundary is
[storage-and-artifact-policy.md](../storage-and-artifact-policy.md). The full Slice-0 schema fixture,
not a hand-picked subset, is the migration baseline. Any artifact-BLOB, protocol-profile,
capability or APT-projection extension requires an immutable migration and the exact named-SWU
authorization.

## Fixtures and falsifiers

- [Compatibility fixtures](fixtures/slice0-compatibility-fixtures.json)
- [Sole-writer W0 test plan](fixtures/SWU-ACI-002-SOLE-WRITER-TEST-PLAN.md)
- [Golden fixture manifest](fixtures/SWU-ACI-002-GOLDEN-MANIFEST.json), binding exact opening bytes,
  close bytes and the complete command/event/state trace
- [Full Slice-0 schema](fixtures/slice0-schema.sql)
- [Canonical contract vectors](fixtures/canonical-contract-vectors.json)
- [Protocol profile registry](../profiles/README.md)

This ADR is falsified for W0 if any fixture leaves two authorities for one fact, allows a candidate
to become official without parent verification, authorizes via the lenient reader, permits a direct
artifact or projection writer, or treats lint as complete sole-writer evidence.

## Consequences

- B-001/B-002 may close after independent review of the digest-bound Stage-A corpus.
- B-003's W0 contract may freeze, but its physical proof and cutover remain blocked.
- Only the exact named test-mutation SWU may be selected after the cross-workpack predicate passes.
- Serve enablement is a later, separate local-pilot decision.
