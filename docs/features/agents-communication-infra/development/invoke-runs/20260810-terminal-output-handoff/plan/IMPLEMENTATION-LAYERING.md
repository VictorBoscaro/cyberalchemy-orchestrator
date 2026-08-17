---
module: bounded-terminal-output-handoff
version: current
status: planned
updatedAt: 2026-08-16
docType: implementation-layering
---

# Implementation Layering: Bounded Terminal-Output Handoff

## Target and boundary

- Target: exact host-observed terminal output feeding staged workflow seats.
- Current state: binding and path-based receipt verification exist; exact terminal capture and staged scheduling do not.
- Governing decision: only exact host-observed terminal response bytes may satisfy `binding-output`.

## Layer decisions

| Layer | Decision question | Minimum working unit | Included now | Deferred | Exit evidence | Promotion |
| --- | --- | --- | --- | --- | --- | --- |
| L0 | After this layer, we know whether Codex terminal bytes can be committed with producer identity without caller-authored paths. | A non-runtime host-payload preflight, one runtime byte-commit primitive, then one Codex capture adapter. | `resolved` output only; one seat; fail-closed capture. | Downstream launch, fan-in, non-success output. | HTR-000 payload receipt, TOH-001–005 split across service/adapter tests, and one live-host smoke. | Continue only if the host field is canonical and complete, captured bytes equal it, and retry is idempotent. |
| L1 | After this layer, we know whether one producer can unlock one consumer exactly once. | One sequential edge compiled in two stages from accepted receipts. | Read port, one handoff, one downstream manifest, durable launch intent. | Fan-in and three-wave dispatch. | TOH-006–008 and restart/no-relaunch tests. | Continue only if replay is byte-identical and emits no duplicate launch. |
| L2 | After this layer, we know whether bounded fan-in preserves complete ordered evidence and cannot close early. | Ordered fan-in launch intent (HTR-004A), then a separate declared-seat close gate (HTR-004B). | Group completeness, fan-in, error/cancel fences, close completeness. | General workflow graph policies. | Partial/failure/tamper/fan-in matrix plus close-gate matrix. | Requires a new spec/design version before either unit is admitted. |
| L3 | After this layer, we know whether the research topology and its independent review remain auditable. | Research pilot (HTR-005), then separate review dispatch (HTR-006). | Three research waves, research close, review open/close, observability. | Cycles, rework, conditional branches, provider-complete input claims. | Live research receipts and `research.md`/`findings.md`; separate review receipt and `review.md`; full suite. | Retain, narrow, or roll back from evidence. |

## Non-regression guardrails

- Caller-authored repository paths never become terminal-response authority.
- A terminal state without accepted response bytes never satisfies a required slot.
- Later layers preserve same-dispatch, producer, digest, size, route and binding checks.
- The compiler fence relaxes only for the active proven layer.

## Recommended next layer

- Next: L0 preflight `SWU-ACI-HTR-000`; only then may `SWU-ACI-HTR-001` be selected.
- Decision unlocked: whether `PostToolUse.tool_response` exposes canonical, complete terminal text suitable for the accepted design.
- Major deferral: fan-in and the research dispatch remain blocked until L0 and L1 pass.
