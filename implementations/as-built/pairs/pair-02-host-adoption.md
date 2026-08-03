# Pair 02 — Host adoption

**Question:** Does every real Codex and Claude subagent launch, follow-up, failure, and close obligatorily pass through the governed runtime?

**Worker/finalizer:** Lamport, Leslie  
**Reviewer:** Liskov, Barbara  
**Property served:** No meaningful work outside reconstructible memory.

## Executive answer

No. The governed route is implemented and tested when trusted project hooks load and the host emits a recognized `PreToolUse` event, but that condition is not obligatory.

A fresh trusted Codex session using embedded `codex-cli 0.146.0-alpha.3.1` created a child without a hook event, hook state, YAML lifecycle rows, `dispatch_links`, workflow binding, or `launch-authorized` receipt. Operational adoption is therefore **failed for that observed binary**. Adoption under the installed replacement binary is **unknown** pending reload and smoke. Claude has no model-originated live adoption evidence.

Prelaunch is fail-closed only inside the loaded and invoked hook boundary. Closure and post-tool ingestion are not globally fail-closed: `SessionEnd` errors return exit 0 with a system message, and ingestion runs after work has already executed. The focused 33/33 tests prove adapter and runtime behavior, not host adoption.

## Transition matrix

| Transition | Codex | Claude |
|---|---|---|
| Launch | **Failed operationally** on observed `0.146.0-alpha.3.1`; replacement **unknown**; adapter tested | **Tested/code-only**; live adoption unknown |
| Follow-up | **Tested/code-only**; unbound denied and bound route enforced; no live receipt | **Code-only/unknown** host mapping; no live receipt |
| Success | Controlled hook-wire observed and unit-tested; not model-originated | Simulated synchronous close tested; not live-observed |
| Failure | **Gap:** no `PostToolUseFailure` wiring; handler code exists but real reconciliation is unknown | Simulated `PostToolUseFailure` tested; live behavior unknown |
| Interruption | `SubagentStop` tested; `SessionEnd` configured but its closure errors do not block globally | `SessionEnd` tested and `Stop` configured; live behavior unknown |
| Durable close | Observed only in controlled hook-wire; bypassed real launch has no receipt | Tested only; no real-host receipt |

## Claims and evidence

### HA-01 — Observed Codex adoption failed; replacement adoption is unknown

[The matcher-repair receipt](../../../../docs/features/agent-provenance-telemetry/integration/stage-f/codex-namespaced-hook-matcher-repair-receipt.md) lines 53–57 records a fresh trusted session that created a child with no `PreToolUse` or durable runtime evidence. Lines 59–67 identify the embedded binary and required reload; lines 69–78 define the missing replacement smoke.

The universal adoption claim is false for the observed binary. It is not yet decidable for the replacement.

### HA-02 — Prelaunch enforcement is conditional but fail-closed inside its boundary

[The dispatch hook](../../../../implementations/server/runtime/host_dispatch_hook.py) lines 125–256 validates policy, performs local-pilot preflight, and issues an expiring operation-specific capability. Lines 373–526 require a `launch-authorized` workflow-binding or YAML/ACI opening receipt before returning. Lines 743–775 turn `PreToolUse` exceptions into denial.

This is a real enforcement point only when trusted hooks load and a recognized event reaches it. The policy pins an authorization reference/digest, but the frozen corpus does not contain the underlying human authorization content.

### HA-03 — Terminal persistence exists, but closure and ingestion are not globally fail-closed

[The dispatch hook](../../../../implementations/server/runtime/host_dispatch_hook.py) lines 528–594 can persist resolved, error, or cancelled workflow state and compatibility close receipts. [Migration 009](../../../../implementations/server/runtime/migrations/009_host_workflow_binding.sql) lines 20–30 enforces terminal-state consistency.

However, dispatch-hook lines 767–781 return exit 0 plus `systemMessage` for `SessionEnd` errors; only `SubagentStop` and `Stop` use the blocking close-error response. Post-tool ingestion occurs after execution and therefore cannot prevent already-performed work. Reconstructibility is partial, not guaranteed.

### HA-04 — Follow-up governance is implemented/tested, not operationally demonstrated

Dispatch-hook lines 398–463 deny unbound `followup_task` and enforce positive follow-up ordinals. [Workflow-binding tests](../../../../implementations/tests/runtime/test_host_workflow_binding.py) lines 331–364 verify frozen template and prior-agent identity requirements. No real-host follow-up receipt was found.

### HA-05 — Terminal-event configuration differs by host

[Codex configuration](../../../../.codex/hooks.json) registers `PreToolUse`, `PostToolUse`, `SubagentStop`, and `SessionEnd`, but not `PostToolUseFailure`. [Claude configuration](../../../../.claude/settings.json) registers `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `SessionEnd`, and `Stop`, but no `SubagentStop`. Shared handler code does not establish equivalent host behavior.

### HA-06 — Project configuration is not obligatory official adoption

[The Stage-F execution receipt](../../../../docs/features/agent-provenance-telemetry/integration/stage-f/execution-receipt.md) lines 78–84 states that repository configuration cannot force hook loading and that no administrator-level policy was installed. The hooks remain disableable.

## Gaps and smallest next actions

| Gap | Smallest next action | What it buys | Completion evidence |
|---|---|---|---|
| Replacement Codex binary unverified | Reload extension and run the prescribed single read-only helper smoke | Version-specific operational adoption verdict | Hook state, YAML open/close, `dispatch_links`, terminal workflow binding, `launch-authorized` |
| Claude live adoption unknown | Run one model-originated Claude launch and one terminal path after confirming hook load | Real event-shape and adoption verdict | Correlated host `PreToolUse`, opening receipt, and terminal receipt |
| No administrator enforcement | Install/verify supported managed policy, or classify adoption as voluntary | Defensible non-bypassable adoption claim | Managed-policy inspection plus negative disable/bypass test |
| Codex failure event missing | Establish current host failure event and wire/test it, or define mandatory reconciliation | Accurate failed-transition history | Real failure ending in `error` with no open binding |
| SessionEnd/ingestion recovery unspecified | Define and test retry/recovery semantics | Deterministic convergence after post-execution telemetry failure | One terminal lifecycle and intended ingestion receipt after induced failure/retry |

## Document drift

- [The host-input-binding decision](../../../../docs/decisions/host-agent-dispatch-input-binding.md) lines 17–18 says every `Agent` or `spawn_agent` is wrapped; the later observed Codex bypass falsifies that operational universal.
- The Stage-F receipt calls the wrapper mandatory, but lines 78–84 correctly narrow this to hosts that load project hooks and disclose absent administrator enforcement.
- The workflow-binding receipt establishes implemented/tested semantics, not live-host adoption.

## Verification and limits

`python -B -m unittest implementations.tests.runtime.test_host_dispatch_hook implementations.tests.runtime.test_host_workflow_binding implementations.tests.runtime.test_orchestration_bridge -v` passed **33/33**. The requested `C:/tmp/cyberalchemy-as-built/pair-02-host-adoption` directory could not be created due access denial, so the suite used and cleaned its own temporary fixtures; exact temp-root conformance is not claimed.

Snapshot commit from the frozen manifest: `63777abd838995c8512bcea806546c3f2ab6add6`. Frozen manifest SHA-256: `af35da963497918340ca7c74fa1a9e7a27d1a7027420e6edb517e55fd903cd11`. Dirty state is unknown because sandbox Git refused repository ownership.

## Robot-talk history

Round 1 resolved all material issues. The worker accepted the reviewer’s corrections: scope observed Codex failure to `0.146.0-alpha.3.1` and keep replacement adoption unknown; narrow fail-closed claims to loaded/invoked prelaunch; preserve SessionEnd and ingestion limitations; state absent administrator enforcement; preserve Codex/Claude event asymmetry and unknown Claude live behavior. **No dissent remains.**
