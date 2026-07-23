# SWU-ACI-APT-VS-001 — Session, Dispatch and Structured Research Vertical Slice

- Status: `ready-for-independent-review`
- Mutation authorization: `pending`
- Runtime implementation: `not-started`
- Scope owner: APT application contracts; ACI owns every authority-bearing runtime facility.

## Outcome

After this SWU, one authenticated local client can ensure or roll a Session, link exactly one
existing globally unambiguous Dispatch, append one structured Research result, restart the server,
and read back the Session, Dispatch provenance and Research record—including references, problems,
formalization and an separately authorized final answer—without modifying the dispatch ledger.

## Commands

All mutations require authenticated server-bound context and an `Idempotency-Key` header. Request
bodies reject IDs, timestamps, actors, owner fields, paths, digests, offsets and receipts.

| Command | Caller intent | Owner-bound checks | Atomic result |
|---|---|---|---|
| `EnsureSession` | display name | derive ensure key from principal + origin kind/ref | zero or one `apt.session_started`; stable receipt |
| `StartNewSession` | display name, expected current session ID | authorization and current-session CAS | successor start + context rebound in one group |
| `LinkSessionDispatch` | repo ID, dispatch ID | explicit repo mapping, global dispatch-ID uniqueness, strict opening-row snapshot | one `apt.session_dispatch_linked` |
| `AppendResearchSubmission` | session ID, contribution ID, question, final answer, references, problems, formalizations | exact accepted link/snapshot, closed limits, bound artifact and selectors | artifact + capture + ordered facts + heads + receipt |

`AppendResearchSubmission` constructs `apt.research-submission-envelope@1`: a deterministic header
and length-framed runtime-canonical JSON records for the exact accepted bound submission. Declared
caller records use `mode=declared`; a claim generated solely to ground a formalization uses
`mode=inferred` and an explicit deterministic derivation ref. Each emitted fact is reconstructed
from its selected frame and must be semantically equal to it.

## Event order and schemas

| Order | Event type | Schema ref |
|---:|---|---|
| independent | `apt.session_started` | `apt.session-started@1` |
| paired after rollover start | `apt.session_context_rebound` | `apt.session-context-rebound@1` |
| independent | `apt.session_dispatch_linked` | `apt.session-dispatch-linked@1` |
| 0 | `apt.research_capture_appended` | `apt.research-capture-appended@1` |
| 1 | `apt.research_fact_appended` question | `apt.research-fact-appended@1` |
| 2 | `apt.research_fact_appended` answer | `apt.research-fact-appended@1` |
| 3..N | reference and problem facts in canonical subject order | `apt.research-fact-appended@1` |
| next pairs | inferred claim immediately before its formalization | `apt.research-fact-appended@1` |

All event schemas and canonicalizer digests must be registered before append. Multi-aggregate CAS,
semantic uniqueness and every artifact/event/head/receipt member are preflighted before the first
insert and committed together.

Reference-probe lineage is a separate optional ordered group using
`apt.reference_probe_lineage_appended` / `apt.reference-probe-lineage-appended@1`. It may bind only
an official row in ACI `messages`, its official accepted event and verified publication receipt.
All three must belong to the same complete verified ACI command group and be visible at or before
the accepted-prefix boundary used for lineage. `publication_candidates` and persisted-candidate
events are never provenance authority.

## HTTP endpoints

| Method and path | Result |
|---|---|
| `POST /api/provenance/sessions/ensure` | Session + stable receipt |
| `POST /api/provenance/sessions/start-new` | successor Session + rebound receipt |
| `POST /api/provenance/sessions/{session_id}/dispatches` | accepted link + pinned snapshot |
| `POST /api/provenance/dispatches/{repo_id}/{dispatch_id}/research` | receipt and projection status |
| `GET /api/provenance/sessions/{session_id}` | Session record at reported source offset |
| `GET /api/provenance/dispatches/{repo_id}/{dispatch_id}` | dispatch provenance summary |
| `GET /api/provenance/research/{capture_id}` | structured metadata; never final-answer bytes |
| `GET /api/provenance/research/{capture_id}/answer` | authorized artifact-selector dereference |
| `GET /api/health` | migration, journal-tail and projector-offset readiness |

An accepted command whose projector is pending returns its durable receipt with HTTP 202 and
`projection_status=pending`. A GET that requires an offset beyond the APT source watermark returns
503 `PROJECTION_LAG`, never a stale 404.

## Rebuildable projections

ACI's `ProjectionManager` is the sole SQL executor. APT supplies pure event-to-row logic for:

- `apt_projection_state(apt_source_through_offset, projector_version)`;
- `apt_sessions`;
- `apt_session_dispatch_links`;
- `apt_research_captures`;
- `apt_research_facts`;
- `apt_research_questions`;
- `apt_research_answers` (artifact/selector metadata only);
- `apt_reference_uses`;
- `apt_research_problems`;
- `apt_research_claims`;
- `apt_formalizations`.

The watermark is the highest complete verified group scanned, including skipped non-APT groups.
Every projection row records accepted event ID, offset and payload digest. Projection tables are
discardable and may never become command, replay, receipt or dispatch authority.

## Strict dispatch compatibility

Mutation repos use an explicit stable repo-ID-to-realpath map; UI auto-discovery remains read-only.
A dedicated parser isolates opening-row blocks, accepts only the supported appender row contract,
requires one globally unique dispatch ID across mutation repos and hashes only the canonical
immutable opening row. The snapshot records stable symbolic owner `register-dispatch`, row-contract
version and row digest. Whole-ledger fingerprints and close-row locations are non-authoritative.
`implementations/server/ledger.py`, existing endpoints and `subagents-dispatch.yaml` remain
unchanged.

## Required executable evidence

1. Migration checksum/order/drift plus effective FK/WAL/FULL/busy settings.
2. Same key/same digest stable receipt; changed digest conflict; multi-aggregate CAS race.
3. Failure injection before/after each artifact/event/head/uniqueness/receipt boundary.
4. Complete-group reads, accepted-prefix boundary and corrupt/incomplete-group rejection.
5. Projector idempotency, skipped unrelated groups, rebuild from zero, lag and startup repair.
6. Strict resolver rejects paths, unknown repos, unsupported/corrupt/duplicate/ambiguous rows.
7. Authentication, closed fields, duplicate JSON keys and byte/count limits.
8. Grep/query proof that final-answer bytes occur only in `artifacts.body`.
9. Reference-probe rejects candidates, mismatched profile/bundle/receipt and unsupported access
   inference; it also rejects message/event/receipt records from different command groups or later
   accepted-prefix boundaries.
10. Missing, unknown or mismatched classification, retention, tombstone or authorization policy
    refs/digests reject before artifact append/read.
11. True subprocess E2E: start on a temporary database, ensure/link/research, stop, restart, read
    structured references/problems/notation and authorized answer, and prove dispatch-ledger bytes
    are unchanged.

## Gate ladder

| Gate | Requirement | Current |
|---|---|---|
| A | TASK-105 pure module receipt and frozen APT profile requests | ready |
| B | ACI registration receipts for all four exact profile digests | PASS |
| C | independent storage/artifact policy PASS | PASS |
| D | owner mutation-gate change plus independent post-change receipt | PASS |
| E | implementation + unit/contract/crash/security evidence | ready; not yet executed |
| F | subprocess restart E2E and root/reviewer closure | blocked by E |
