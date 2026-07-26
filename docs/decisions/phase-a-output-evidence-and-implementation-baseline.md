---
status: pending-owner-decision
date: 2026-07-26
scope: phase-a-host-binding-bus-repair
---

# Phase A output evidence and implementation baseline

## Decision-gate result

- Result: `BLOCK`
- Consequential work blocked:
  - F2 normative authoring and implementation;
  - brownfield code dispatch for F4/F5/F6.
- Work not blocked:
  - read-only inspection;
  - proposal preparation;
  - F1 authority-binding authoring that does not assume an F2 output model.

## D1 — What may count as `binding-output`?

Current runtime accepts a repository path when a named producer is merely terminal. Terminalization
persists no output artifact reference, membership list, or byte digest. Therefore repository bytes
cannot currently inherit producer attribution safely.

### Option A — Exact terminal response artifact (recommended)

Persist the host-observed terminal response as a content-addressed artifact. Only that exact
artifact may be `binding-output`; repository files remain unattributed `repository` sources until a
future write-capture contract exists.

- Benefit: smallest fail-closed model with real producer evidence.
- Cost: file outputs do not carry producer attribution yet.
- Choose when: correctness and near-term implementation leverage matter more than complete file
  provenance.
- Downstream impact: adds terminal output evidence to the binding/event/receipt model and rejects
  all path-based `binding-output`.

### Option B — Explicit produced-file receipt

At completion, persist an ordered list of repository paths, sizes, digests, and producer binding.
Only exact members may be consumed as `binding-output`.

- Benefit: preserves file-oriented multi-agent handoffs with producer attribution.
- Cost/risk: the current host lifecycle does not expose trustworthy file authorship; a declaration
  without write-observation would merely relocate the unsupported claim.
- Choose when: the host wrapper will also gain an authoritative write-observation/correlation
  mechanism.
- Downstream impact: larger Stage-F/Stage-G protocol, persistence, hook, and test scope.

### Option C — Disable `binding-output`

Reject the source kind and require every file to be declared as an unattributed repository source.

- Benefit: smallest and safest immediate repair.
- Cost: removes producer-linked handoffs rather than improving them.
- Choose when: rapid fail-closed closure is more important than preserving the workflow capability.
- Downstream impact: no output-evidence persistence, but a material loss of orchestration leverage.

## D2 — Which implementation baseline should govern the bounded repair?

The repository already implements a layered Python runtime and SQLite journal, but the current
DomainSpec implementer requires an explicit baseline decision record and architecture/database
package before brownfield edits.

### Option A — Ratify the current runtime + SQLite baseline (recommended)

Record the existing `implementations/server/runtime/` layering and SQLite database/migrations as
the baseline for this bounded repair; scaffold documentation that points to existing owners rather
than introducing a new framework.

- Benefit: preserves accepted architecture and minimizes unrelated work.
- Cost: documents and constrains the current design rather than reconsidering it.
- Choose when: the task is a repair of the accepted local pilot, not a platform rewrite.
- Downstream impact: enables alignment/layering audits and the code-readiness receipt.

### Option B — Bootstrap the canonical DomainSpec architecture/database pack

Introduce the canonical `lib/architecture/` and `lib/database/` package and translate the runtime
onto it before repair.

- Benefit: stronger canonical framework alignment.
- Cost/risk: materially expands scope and delays the six security/integrity repairs.
- Choose when: architecture migration is the actual objective.
- Downstream impact: new work-pack, translation, migration, and review work precedes Phase A.

### Option C — Custom baseline

Name another architecture/data-layer package and migrate or bind the repair to it.

- Benefit: accommodates an owner-selected target architecture.
- Cost/risk: unresolved until the exact package and migration boundary are supplied.
- Choose when: neither the current runtime nor canonical pack is the intended target.

## Pending decision

No option is selected yet. Source of the eventual decision must be an explicit owner response.

## Validation

- Phase-A closing review: six MAJOR findings verified.
- Read-only readiness helper: F4/F5/F6 behavior `PASS`, code dispatch `BLOCK` pending DomainSpec
  readiness; F1/F2 code `BLOCK` pending authoring.
- Frozen corpus recheck: 17/18 unchanged; the Stage-E source manifest changed coherently with its
  pinned `local_pilot.py` digest and remains an explicit merge target.

