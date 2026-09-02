# Task session — IMPL-ACI-AGENT-IDENTITY-ROLE-001

Status: `ready_for_review`; worker evidence, not approval.

## Route and gate

- Route: local `task-session`, one accepted implementation SWU.
- Controlling package: `../SPEC-ACI-AGENT-IDENTITY-ROLE-001/`, including independent Recheck 3
  `KEEP`.
- Objective: atomically migrate agent identity/role authority, pool, compiler and live telemetry
  consumers without adding scheduling/provider/tool execution.
- Formal `domainspec-implement` readiness is not claimed because the routed
  implementation-axioms prerequisite is unavailable.
- Worker has a separate reviewer and will stop at `ready_for_review`.

## Context pack

Strict local context was bounded to the work pack/review, migration inventory, real two-document
pool, role/dispatch registries, three appender/strategy copies, MCP consumers, compiler/gate,
workflow/hooks/resolver/bridge/confirmation surfaces, and their named tests. Historical telemetry,
v1 authorities, prior reviews and the L0 experiment are read-only.

## Decisions inherited

- canonical YAML identity is only `agent_name`; `agent-name` is rejected;
- DraftGraph authors `role`, not `display_name`;
- registry v1 is exactly the eight owner-selected roles and is byte-digest pinned;
- new rows are 0.7.0/v2 and pin the same registry ref on open/close;
- v1/0.6.x remains explicit historical verification only.

## Pool migration incident and recovery

The first PowerShell bulk rewrite used an unparenthesized `-replace` expression as an argument to
`List.Add`. PowerShell interpreted it as two arguments, emitted an error for every roster identity,
and nevertheless reached the final write because the command did not run with stop-on-error. The
result temporarily contained the migrated metadata but omitted all 414 identity lines.

The failure was detected immediately by the post-write count (`0` `agent_name` rows and only 2772
lines). No later task mutation used that malformed pool. Recovery reconstructed the candidate from
the tracked `HEAD:telemetry/agents/agent-pool.yaml` bytes and reapplied exactly the four accepted
transformations with `$ErrorActionPreference='Stop'`: metadata version, last-updated date, prepended
migration note, and 414 roster-key renames.

Evidence that this did not discard a pre-existing user pool edit:

- the task's initial `git status --short`, captured before mutation, did not list
  `telemetry/agents/agent-pool.yaml`; therefore the worktree pool equaled the tracked baseline;
- the source authority digest is the accepted v0.6 digest
  `sha256:5c7b9745a336670ecb55df1276912166954a0d7960443f0df787405564099eba`;
- the repaired file parses to exactly the same two-document value as the production migration
  function applied to `git show HEAD:telemetry/agents/agent-pool.yaml`;
- the comparison covers row order and every non-identity field for all 414 rows, not only counts.

The malformed intermediate bytes were not preserved because they had no valid identities and were
never an authority candidate. This incident must remain visible to independent review.

## Implemented result

- The accepted role registry contains exactly the eight owner-selected roles and is digest-pinned;
  host keyword routing is separate pinned data, and a synthetic future role revision loads without
  a Python/JavaScript enum edit.
- The real two-document pool is canonical v0.7 with 414 unique `agent_name` rows. Python and MCP
  steady-state loaders reject legacy/dual/malformed identity and role drift.
- DraftGraph no longer authors names. A signed, fresh allocator context supplies exact node-to-name
  assignments, and compilation fails closed on coverage, reuse, membership, role fit, override,
  registry/pool substitution, conflict and replay.
- New telemetry and confirmation writes select dispatch registry/package v2, schema 0.7.0 and one
  identical accepted role ref on opening/close/effect/request. The v1 registry, package and
  confirmed-dispatch fixture remain immutable compatibility evidence.
- The field-to-consumer proof is in `FIELD-CONSUMERS.md`; no new identity field is decorative.

## Review boundary

This worker does not approve the SWU. The dedicated reviewer must inspect the pool-recovery proof,
authority digests, strict failure paths, fixture migration and test residue before returning
`KEEP`, `REPAIR` or `REJECT`.
