# Host Workflow Binding Receipt

Date: 2026-07-25
Status: `PASS / BOUNDED_PARENT_DISPATCH_BINDING_IMPLEMENTED`

## Accepted result

The mandatory host wrapper now supports multiple agent seats and follow-up turns under one
confirmed parent Dispatch. A bound launch persists a journaled turn record and immutable workflow
input manifest instead of creating a compatibility Dispatch for each subagent.

The boundary is fail-closed:

- group, seat and turn must exist under an open parent Dispatch;
- turn-zero prompts must equal the confirmed seat prompt;
- follow-ups require a pre-confirmed prompt-template digest and the prior bound agent identity;
- repository and upstream-output sources require exact paths, bytes, sizes and SHA-256 digests;
- upstream producer bindings must be terminal and belong to the same parent;
- retries are idempotent only when their complete accepted identity is unchanged;
- the parent cannot close while a bound turn is running;
- unbound `followup_task` calls are denied.

## Verification

- Complete Python runtime suite: PASS, 77/77.
- Focused workflow-binding, hook, orchestration bridge and Stage-C suite: PASS, 31/31.
- Runtime and runtime-test compilation: PASS.
- Source-manifest integrity preflight: PASS through focused Stage-C and bridge tests.
- Task-owned files whitespace check: PASS.
- Repository-wide `git diff --check`: one out-of-scope working-tree finding remains in
  `docs/features/skill-control-center/interfaces.md`.

## Compatibility boundary

This receipt covers repository-local, host-observable workflow inputs and persisted output files.
It does not claim provider-side completeness and does not implement the general ACI
`EffectiveInputArtifact`, materialized invocation, execution-request or provider-admission
pipeline.
