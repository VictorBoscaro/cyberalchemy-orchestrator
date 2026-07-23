---
title: Agent Provenance Telemetry Implementation Layering
status: active
updatedAt: 2026-07-23
owner: "@victor"
scope: infrastructure
---

# Agent Provenance Telemetry Implementation Layering

## Context and Method

APT is specified but not integrated. Its three read levels are Session, external Dispatch and
Research. ACI remains the sole bus, journal, receipt, canonicalizer registry and durable appender.
Sources are [WORK-PACK](WORK-PACK.md), [architecture](specs/architecture.md),
[domain](specs/domain.md), [rules](specs/rules.md), [states](specs/states.md), and
[TEST-SPEC](TEST-SPEC.md).

```text
Layer value = decision unlocked + operator-visible outcome + risk reduced
Layer cost = implementation time + verification time + coordination burden
```

## Layer Decisions

| Layer | Decision question | Minimum working unit | Deferred | Exit evidence |
|---|---|---|---|---|
| L0 | After this layer, we know whether the three-level model is coherent and deterministically reducible without owning infrastructure. | Pure TypeScript schemas, validation, APT normalization, payload candidates, injected canonicalizer contract, reducers/projectors and exact-ID tests. | ACI bytes/digests/receipts, durability, runtime export and enablement. | TASK-105 tests/typecheck and no-parallel-authority review PASS. |
| L1 | After this layer, we know whether APT can append through ACI without weakening authority or atomicity. | Exact registered profiles plus artifact-only ACI adapter. | Probe/runtime and read surfaces. | Crash/race/idempotency receipts and owner mutation gate PASS. |
| L2 | After this layer, we know whether replay and the bounded probe work under failure. | Verified-prefix replay, operations, probe lineage and classified telemetry. | UI and scale. | Replay/redaction/no-parallel-authority evidence. |
| L3 | After this layer, we know whether the increment is pilot-ready. | Read-surface wiring, closure audits and packaging. | Production deployment and global assertions. | Verification, alignment and layering reports PASS. |

## L0 Minimum Working Unit

Included: closed value shapes and validators; immutable artifact-only `ResearchCapture`; append-only
facts; typed reference lineage/checks and formalizations; APT normalization; candidate payloads;
an injected candidate canonicalizer whose output is explicitly non-authoritative; pure reducers
over exact-decoded fixture envelopes explicitly marked unverified; partial deterministic as-of
projector candidates owned finally by TASK-120; and test-only non-exported
in-memory doubles.

Deferred: every durable write/read path, ACI registration/profile digest/receipt, accepted prefix,
checkpoint, Dispatch mutation, artifact backend and probe runtime. Local JSON or test digests never
claim ACI compatibility.

## Progressive Improvement and Non-Regression

L1 adds owner-bound durability. L2 adds verified replay, bounded probe wiring and operational
telemetry. L3 adds read surfaces and packaging. Every layer preserves: no inline raw body; no
second bus/store/journal/receipt authority; no new Dispatch ledger keys; no inferred access or
support; no telemetry-driven decisions; and no projection without an explicit as-of boundary.

Recommended next layer: L0 through TASK-105. Promotion remains blocked until all required ACI
registrations have exact reviewer-verified digests and the owner records the mutation gate PASS.

## Experimental Runtime Track E0

E0 is a parallel evidence track, not a promotion or renumbering of L0–L3.

| Decision question | Minimum working unit | Explicitly deferred | Exit evidence |
|---|---|---|---|
| After E0, do append-before-ack journal facts and command receipts deterministically rebuild Session and Reference Scout projections under retry, conflict and replay? | One isolated local SQLite runtime with six commands, experimental receipts, four rebuildable projections and restart/replay tests. | ACI registration, production adapter, dispatch-ledger mutation/materializer, transcript storage, compression/masking, multi-agent acquisition, cutover and scale. | [Experimental runtime E0](specs/experimental-runtime-l0.md) required tests pass; receipts are visibly experimental; no YAML is written; replay matches live projections. |

Boundary heuristic: E0 stops after the minimum durability/replay decision. Adding a dispatch-ledger
writer, source acquisition or production registration would unlock different decisions at
substantially higher coordination cost and therefore belongs to a later layer.

Non-regression from the main track still applies: one authority per edge, no inline raw body, no
telemetry-driven mutation, no inferred source access and no projection without an explicit source
offset. E0 additionally preserves Session ≠ Conversation, Reference Scout compatibility aliases and
the separation of the two residue constructions.
