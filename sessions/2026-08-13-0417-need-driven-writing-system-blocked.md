---
tags: [need-driven-writing, author-sovereignty, dispatch-routing]
artifact_kind: session
layer: capability
version: 0.1.0
created_at: 2026-08-13T04:17:26-03:00
updated_at: 2026-08-13T04:17:26-03:00
expires: 2026-10-12
decisions_made: false
contradictions_found: false
specs_updated: []
promoted_candidates: []
expected_importance: 8
importance_rationale: "The record preserves reviewed writing-system boundaries and the exact infrastructure blockers that prevented implementation from starting."
---

# Need-driven writing system: investigated, not implemented

## Summary

The repository aims to keep agent work connected to the objectives, decisions, assumptions, actions, and evidence that give it meaning. This session investigated how a writing system could preserve each author's preferences while sharing only evidence-bounded principles and keeping editorial judgment distinct from mechanical checks. Robot-Talks produced independently reviewed tensions and recommendations, but `D-01`, `D-02`, `D-04`, and `D-06` remain unselected, while `D-03` and `D-05` remain reversible deferrals. A repaired implementation dispatch received independent `PASS` for exact SHA-256 `A8F4D0546B4732EA0A299552873439FD9DADF4ED75177B7FAE72885F6B7A4A1E`, but it remained pre-run and launched no implementation seat. Its canonical opening passed ledger-schema validation, then workflow compilation stopped before launch because capability `orchestrate` has no routable dispatch type; the attempt produced zero compiled output items and no product artifact. That failure is supported by the parent operator's reported command result and independently corroborated by the durable registry entry for `others`, which is live but has `routable=false` and `capability_ref=null`; no governed run receipt exists. The standalone close-session reroute contains and records the blocked work rather than replacing the implementation route, and this session produced no product implementation and no commit. Implementation remains blocked until routing is made explicit and routable, connected-topology handoffs can be materialized by the compiler, and the canonical opening compiles to a bound launch plan before any seat is started.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Robot-Talks dialogue](../internal-tools/need-driven-system-writing/robot-talks/2026-08-12-system-boundaries/dialogue.md) | `derives-from` | The session's investigation history, unresolved-decision status, and no-implementation boundary come from this preserved dialogue. |
| [Implementation dispatch](../internal-tools/need-driven-system-writing/implementation-dispatch.json) | `contextualizes` | This session records why the independently reviewed route remained pre-run and what infrastructure must change before it can be attempted. |

## Open questions

- Which reviewed options, if any, should ultimately be selected for `D-01`, `D-02`, `D-04`, and `D-06`?
- Should `orchestrate` become a routable capability for `others`, or should this workflow use a different live dispatch type with an explicit capability mapping?
- What governed representation should materialize the opening record's connected handoffs without weakening its sequencing and feedback constraints?

## Next steps

1. Route a separate infrastructure repair that supplies an explicit live, routable dispatch-type mapping for the intended capability.
2. Extend or replace the legacy workflow compiler so it can materialize the opening record's connected topology, including sequential, feedback, and zig-zag handoffs with their loop caps.
3. Re-run ledger-schema validation and workflow compilation into an empty repository-local temporary directory; require a non-empty bound launch plan before considering any seat launch.
4. Re-review the implementation dispatch if any frozen input, authority boundary, ownership rule, or opening record changes; do not infer the unresolved writing-system decisions from this closeout.

## Recommendation

Repair and verify capability routing first, then connected-topology materialization, because the current compiler fails at route resolution before it can reach its separate topology prohibition; preserve the implementation dispatch as unexecuted throughout that reroute.

## Files touched

- internal-tools/need-driven-system-writing/implementation-dispatch.json
- internal-tools/need-driven-system-writing/implementation-dispatch.review.md
- .codex/dispatch-proposals/need-driven-system-writing-implementation-v1-opening.json
- internal-tools/need-driven-system-writing/session-close-dispatch.json
- sessions/2026-08-13-0417-need-driven-writing-system-blocked.md
- .arcanum/observability/runs/need-driven-system-writing-blocked-session-close-v1/c01-close-session/initial/session_closing_agent.json
