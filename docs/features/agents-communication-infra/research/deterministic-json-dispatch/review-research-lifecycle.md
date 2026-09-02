# Review — deterministic JSON dispatch research lifecycle

- Reviewer: `/root/json_dispatch_research_lifecycle_reviewer`
- Coordinator: `/root/json_dispatch_research_lifecycle_worker`
- Dispatch: `2026-09-02-deterministic-json-dispatch-host-gap`
- Review date: 2026-09-02
- Verdict: **BLOCK**
- `recheck_required`: `true`
- Frozen opening SHA-256: `C4A4EE6409548DA652AA1182F1B6CFDACF16F4EDEB559EBBF867DE925306702C`
- Route digest: `sha256:8929f727df4315eedbc5b0cd627a7fc9beb1e08f671c88fb838553fdcb899974`

## Outcome

The opening is now structurally valid and correctly remains unexecuted. The only surviving blocker is the mandatory exact-sheet confirmation gate. The user's broad authorization to continue bounded dispatches removes the need to renegotiate the objective, but it does not satisfy the lifecycle's requirement to show and explicitly confirm this frozen record before registration or launch.

No compile, open, seat launch, close, ledger append, host-live witness, or research success is claimed.

## Evidence reproduced

- The final initial-definitions precondition is `KEEP`, with artifact SHA-256 `56039AD49883D94B5F4AC65D2D1DEDFCF527F95C90B598ADEA927267BA2D0B61` and review SHA-256 `20FC0888D1DE91AD5AA25176528C89696B2C6774C7CC67161175D188DBA6DECC`.
- The cited accepted local-runtime review independently matches SHA-256 `8B5F152CD04AE9BBE44BC868802241432C779ACAE5FA3C01E0828937EB8F9DFF`; the opening does not expand that evidence into a host-live claim.
- Re-running `dispatch_workflow resolve --capability-ref research --authority-mode legacy-managed` returned the exact `capability_route` embedded in the opening, including `research`, `legacy-managed`, `host/inherited@1`, and the route digest above.
- `validate_opening_record(root, record)` passed after repair.
- `node .claude/skills/register-dispatch/append-dispatch.cjs <opening> --validate-only` returned `valid dispatch record (schema v0.7.0)`.
- `anti_bias_mode` is exactly `disabled`; no group, agent, or top-level anti-bias overlay field is present.
- The research shape is bounded to one explorer and exactly one skeptic owning only the `non-vacuity` gate. The connection is sequential, with one capped feedback edge. The prompts require `research.md`, cited `findings.md`, the verdict matrix, inline collapse tests, a one-line answer, and `skeptic-review.md`.
- The agent names exist in the pinned pool and fit their declared roles: `Abramsky, Samson` as explorer and `Gödel, Kurt` as skeptic.
- The working folder contains only the accepted initial definitions and their review. It contains no bridge stdout, receipt copy, research return, findings, or fabricated completion evidence.
- The workflow-input directory contains only `opening.json`: no launch plan, binding manifest, close record, or receipt exists.
- The dispatch id appears only in `opening.json`; it is absent from `telemetry/agents/subagents-dispatch.yaml`. No bound or unbound seat for this dispatch exists in the active agent tree.

## Repair observed during review

The first opening, SHA-256 `B32B88C5CD8810CD41E5CE3350291D05FC130CF02C5D57E3993F22336DBA0841`, failed executable validation because `capability_route` was absent. The same coordinator repaired it by embedding the unmodified resolver receipt. The repaired opening is the frozen `C4A4EE...` artifact reviewed above and passes both runtime and appender validation.

## Blocking finding

### B1 — exact frozen record has not been explicitly confirmed

- Severity: **BLOCKER**
- Reproduction: there is no user confirmation of the exact `C4A4EE...` opening after its agents, prompts, effects, budgets, topology, and artifact destination were frozen. The available authorization precedes this concrete sheet and cannot establish that the human saw it.
- Required action: show the exact frozen record and obtain explicit confirmation. If any material field changes, freeze the revised record and reconfirm it.

Until B1 is satisfied, the correct lifecycle state is pre-compile and pre-open. Compiling bindings, appending the ledger, opening a session, spawning a seat, or closing the dispatch would violate the selected lifecycle. After confirmation, use only the runtime-generated launch plan and bindings, require parent-bound terminal seats, and close only after their journal-backed terminal receipts exist.

## Verdict

**BLOCK.** The record itself is valid and no orphan, fake success, hand-authored binding, source mutation attributable to the research run, or premature close was found. Execution cannot begin without the exact-sheet confirmation required by the governing lifecycle.

## Recheck 1 — exact confirmation received; compile remains blocked

- Recheck date: 2026-09-02
- Confirmed opening SHA-256: `C4A4EE6409548DA652AA1182F1B6CFDACF16F4EDEB559EBBF867DE925306702C`
- Recheck verdict: **BLOCK**
- `recheck_required`: `true`

The user explicitly confirmed the exact frozen opening, resolving B1. The coordinator then invoked the official compile path. Compilation failed before a launch plan or binding manifest could be emitted:

```text
GateBlockedError: required sequential handoff receipt is unavailable
```

### B2 — sequential handoff compilation has a pre-launch producer-output dependency

- Severity: **BLOCKER**
- Executable/source reproduction: `compile_bound_launch_plan` calls `_sequential_handoffs` before emitting any launch. For `host_gap_explorer -> non_vacuity_skeptic`, that function requires `handoff-0-1.json`; the receipt must already contain an immutable `aci-host-workflow-producer-output/v1` receipt covering every explorer seat and matching actual artifact bytes. Those bytes and their binding id cannot exist until the explorer is launched, but the explorer cannot be launched because no launch plan exists.
- Failure boundary: this is not missing research evidence. It is a compile/launch dependency cycle in the current lifecycle surface.
- Forbidden workaround: fabricating the handoff or producer-output receipt would create fake success and an unbound provenance claim.
- Required fix: revise the executable lifecycle or record staging so the initial ready group can be compiled and launched before downstream producer-output receipts are required. The downstream seat must later consume only runtime-produced, digest-verified outputs.

### B3 — the confirmed feedback edge is not executable

- Severity: **BLOCKER**
- Source reproduction: `_sequential_handoffs` accepts only connection objects whose keys are exactly `{from,to,type}` and then requires `type == "sequential"`. The confirmed feedback connection includes `loop_cap` and `type: feedback`, so it would be rejected even after B2.
- Required fix: either implement governed feedback scheduling and binding receipts, or remove the feedback edge from a revised research sheet when the capability owner judges it unnecessary. Either choice materially changes the confirmed record or runtime and requires a revised frozen record plus explicit confirmation.

### Post-failure integrity evidence

- The workflow-input directory still contains only `opening.json`; there is no `launch-plan.json`, manifest, generated binding, handoff receipt, or close record.
- The dispatch id remains absent from the append-only ledger.
- No session was opened, no seat was launched, and no bound or unbound agent exists for the dispatch.
- No `research.md`, `findings.md`, `skeptic-review.md`, bridge stdout file, terminal receipt, or close evidence was created.
- Consequently there is no host-live witness and no basis for a research success claim.

### Recheck verdict

**BLOCK.** Exact confirmation passed, but the current compiler cannot bootstrap the confirmed sequential research topology and cannot execute its feedback edge. This cannot be repaired silently inside the confirmed record. A revised executable staging design and frozen opening must be reviewed and explicitly confirmed before compile/open can resume.
