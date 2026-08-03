---
name: subagents-dispatch-lifecycle
description: Execute an already-routed legacy-managed subagent dispatch through confirmation, canonical registration, parent-bound host launches, receipt verification, and close. Use only after domainspec-subagents-strategy returns a route receipt for an installed work-type capability.
---

# Session-owned subagent dispatch lifecycle

## Boundary

Coordinate one `legacy-managed` dispatch. The selected capability owns work judgment, the canonical
registry owns type resolution, the bridge/appender own registration, and the host/runtime own launch
authorization and binding receipts.

Require the objective, boundaries, selected capability, the unmodified route receipt, and the
entry-prepared concrete opening record with any entry-owned validation receipt. Reject a missing,
hand-authored, reserved, non-routable, or non-legacy route.

## Lifecycle

1. **Shape.** Read the selected capability in full and verify the entry-prepared concrete opening
   record against it. Set
   `dispatch_type` only from `route.ledger_dispatch_type`; never type it from memory. Preserve the
   capability's roles, prompts, topology, evidence, output, approval contract, and every
   entry-owned field or receipt. If shaping requires a material record change, return the revised
   record to the entry skill before confirmation; do not repair or regenerate its receipt here.
2. **Confirm.** Show the exact record, agents, prompts, effects, budgets, and artifact destination.
   Obtain explicit user confirmation. Any material change invalidates confirmation.
3. **Compile bindings.** After confirmation, compile the frozen record:

   ```powershell
   python -m implementations.server.runtime.dispatch_workflow --project-dir <repo-root> compile `
     --record <opening.json> --capability-ref <route.capability_ref> `
     --authority-mode legacy-managed `
     --output-dir .codex/workflow-inputs/<dispatch-id>
   ```

   Use only the generated `launch-plan.json`. Do not synthesize or edit binding envelopes. If a seat
   needs dynamic or upstream inputs, replace its empty generated manifest with an exact
   `aci-workflow-input-manifest/v1` before opening, recompute through a governed compiler extension,
   and reconfirm any changed instruction or source boundary.
4. **Open once.** Send the parent record through the bridge, which invokes the sole validated ledger
   writer and creates the ACI/session opening:

   ```powershell
   python -m implementations.server.runtime.dispatch_workflow --project-dir <repo-root> open `
     --record <opening.json> --host <codex|claude> `
     --session-name <session-name> --origin-ref <origin-ref> --nonce <unique-nonce>
   ```

   Require `status=launch-authorized`, one `session_id`, and YAML plus orchestration receipts before
   launching. Do not separately call `register-dispatch`; `open` already calls its appender. Never
   persist bridge stdout in the dispatch working folder.
5. **Launch bound seats.** For each ready seat, call the authorized host subagent tool with exactly
   the generated `spawn_arguments`. Its message begins with `ACI-WORKFLOW-BINDING-V1:`. The hook must
   return bound-seat authorization for the same parent; a compatibility-mode dispatch ID, missing
   hook proof, or altered prompt is a failure. Do not call unbound `followup_task`.
6. **Verify.** Join every launched agent, inspect its actual artifacts and checks, apply the selected
   capability's verdict contract, and verify that every binding is terminal. Requested model or
   tools are not effective merely because they appear in a prompt or record. The current registry's
   `host/inherited@1` profile means the host-provided surface is used; if the capability needs a tool
   absent from that surface, stop before launch.
7. **Close once.** Build the close record according to `register-dispatch` and run:

   ```powershell
   python -m implementations.server.runtime.dispatch_workflow --project-dir <repo-root> close `
     --record <close.json> --host <codex|claude> `
     --session-id <open.session_id> --nonce <unique-nonce>
   ```

   Require `status=closed` and YAML plus orchestration close receipts. The runtime rejects close
   while any bound seat is running.

## Failure policy

Fail closed on registry drift, unavailable capability, rejected appender input, missing opening or
binding receipt, prompt/manifest digest mismatch, unavailable required tool, open seat, or close
failure. Never downgrade a governed dispatch to independent compatibility calls.
