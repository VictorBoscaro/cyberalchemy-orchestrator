---
name: domainspec-subagents-strategy
description: Entry point for subagent work. Use it to decide whether delegation is warranted, select the installed capability that owns the requested work, resolve its canonical dispatch type, apply the user-selected anti-bias overlay, and hand one typed route to the operational dispatch lifecycle. It owns routing and that optional overlay, not persisted-record mechanics, runtime behavior, or type-specific judgment.
---

# DomainSpec subagent entry point

## Responsibility

Own only:

1. whether to work inline or delegate;
2. which installed capability owns the work;
3. whether the user opted into the anti-bias overlay for this dispatch;
4. which executable lifecycle receives the routed request.

Delegate when independent context, isolated exploration, parallel work, or an independent check
materially improves the result. Work inline when coordination costs more than the expected evidence.

## Select the capability

Read the selected skill in full. It owns roles, topology, evidence, artifacts, and verdicts.

| Intent | Capability |
|---|---|
| feature discovery authoring | `discovery-writing` |
| establish or synthesize a claim | `research` |
| attack an existing artifact | `review` |
| preregister a falsifiable experiment | `experiment` |
| implement an accepted DomainSpec task | `domainspec-implement` |

If no installed capability owns the request, stop. Never route unknown work to this skill or infer a
type merely because the ledger accepts its spelling. A capability-owned unregistered bootstrap
workflow, such as the bounded discovery bootstrap, terminates inside that capability.

## Resolve the canonical route

For a registered dispatch, resolve the selected capability through the executable registry:

```powershell
python -m implementations.server.runtime.dispatch_workflow --project-dir <repo-root> resolve `
  --capability-ref <capability-name> --authority-mode legacy-managed
```

Treat the returned route as one unit. It contains `dispatch_type_ref`, its ledger projection,
`capability_ref`, `execution_authority_mode`, and `tool_profile_ref`. Do not author, copy, or repair
those values manually. The sole type definition and LIVE/RESERVED status live in
`implementations/contracts/dispatch-type-registry.v1.json`.

Only routes returned successfully by this command are executable. `runtime-managed` is unavailable
until the registry advertises it and the corresponding runtime command surface exists. Never fall
back silently between authority modes.

## User-selected anti-bias overlay

This is the sole skill that defines, presents, or evaluates anti-bias behavior. Every new registered
opening record materializes exactly one of:

- `anti_bias_mode: enabled` when the user explicitly opts in for that dispatch;
- `anti_bias_mode: disabled` otherwise.

The mode is opt-in. Never enable it from agent count, work type, topology, a capability default, or
an earlier dispatch. The user may change the mode until the concrete opening record is frozen; a
later change creates a new record revision and invalidates any prior validation receipt.

With `disabled`, add no anti-bias fields or checks. Continue with the selected capability's ordinary
roles, topology, lenses, and evidence contract.

With `enabled`, apply this overlay to every group containing at least two agents:

- set the group's `anti_bias` to one declared axis: `methodology`, `source-corpus`,
  `attack-vector`, `temporal-prior`, or an explicitly named composite;
- set every agent's `angle` to its concrete position on that axis;
- record, for every unordered pair, the predicted disagreement question, both predicted positions,
  and the evidence supporting the prediction;
- set `anti_bias_global` when at least two groups contain at least two agents.

Then run two independent, read-only checkers in parallel against the same canonical record revision
and digest. Each checker applies all four tests to every affected group:

1. **Axis:** the declared axis is in the closed vocabulary above or is an explicit composite.
2. **Clone:** no pair shares the same core angle.
3. **Spread:** the group does not collapse onto one methodology, corpus, or attack gate.
4. **Evidence:** every pair has a concrete predicted disagreement and supporting evidence.

Both checkers must independently return `PASS`. Any failure, disagreement, missing field, or record
change returns the record to this skill for revision, recanonicalization, and two fresh checks. The
checkers are gate infrastructure: they are not ledger dispatches, write no deliverable, and are not
recursively checked. Store their result in `entry_validation_receipt` with exactly this closed
shape:

```json
{
  "schema": "entry-validation-receipt/v1",
  "subject_digest": "sha256:<64 lowercase hex>",
  "checks": [
    {"checker_id": "<non-empty id>", "verdict": "PASS"},
    {"checker_id": "<different non-empty id>", "verdict": "PASS"}
  ]
}
```

Compute `subject_digest` as SHA-256 over the canonical JSON bytes of the complete opening record
after removing `entry_validation_receipt` and `project_dir`. Do not add receipt fields, accept a
non-`PASS` verdict, reuse a checker ID, or hash a different projection.

Build the base concrete opening record by applying the selected capability exactly as written; do
not reinterpret its type-specific semantics here. Materialize the mode, apply the overlay when
enabled, and only then freeze the record for handoff.

## Handoff

Pass to `subagents-dispatch-lifecycle`:

- user objective, target, boundaries, result, and constraints;
- why delegation is warranted;
- selected capability;
- the complete route receipt returned by the resolver;
- the concrete opening record with explicit `anti_bias_mode`;
- when enabled, the entry-owned validation receipt bound to that record's digest.

Then stop acting as lifecycle or type owner. If the lifecycle needs to change the concrete record,
it must return the revised record here before confirmation so the entry-owned overlay can be applied
again.

## Guardrails

Do not define or duplicate dispatch-type or exit-reason enums, LIVE/RESERVED status, record or
manifest schemas, hashes, authorization, scheduling, close mechanics, tool enforcement, topology,
or type-specific epistemology. Reference their executable owners.
