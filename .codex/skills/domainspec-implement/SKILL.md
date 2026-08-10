---
name: domainspec-implement
description: Implement one bounded code task from accepted DomainSpec feature docs and generated test obligations. Use as the LIVE type skill for dispatch_type code after planner/work-pack readiness passes.
---

# DomainSpec Implement

Use the linked DomainSpec implementation package rather than inventing a local workflow:

1. Read `domainspec/.agents/skills/domainspec-implement/SKILL.md` completely.
2. When the attached DomainSpec package provides its implementation-axioms capability, read it
   completely and enforce AX-DS-1 through AX-DS-4; otherwise stop on the missing dependency.
3. Require planner preflight and `WORK-PACK.md` PASS before feature or implementation mutation.
4. Build the task context/scaffold from accepted feature specs and `TEST-SPEC.md`.
5. For brownfield code, obtain independent alignment and layering verdicts before edits. The
   implementer never approves its own work.
6. Implement only the selected task and declared write scope. Stop on a spec conflict or unrecorded
   blocker-level choice.
7. Add and run source-linked tests, run strict code tagging when available, inspect the actual diff,
   and report exact validation results.
8. Return a bounded diff plus traceability, tests, residual risks and `agents_spawned`; never claim
   completion from prose alone.

The linked skill is the procedural implementation authority. This wrapper makes it available to
the repository's code router while preserving local hooks, ledger and final-approval rules.

## Code dispatch contract

Every `dispatch_type: code` row carries a `code_contract` whose pinned files are verified by the
register-dispatch appender before the row is accepted:

- exact `type_skill_ref` and SHA-256 digest for this skill;
- exact `work_pack_ref`/digest and `test_spec_ref`/digest;
- exact `readiness_ref`/digest for a closed `domainspec-code-readiness@1` JSON receipt whose status
  is `PASS`, whose pinned inputs, `brownfield` decision and task scope equal the code contract, and whose closed capability
  profile denies credentials, production and destructive actions;
- `brownfield`, declared `write_scope`, and non-empty `validation_commands`;
- canonical group IDs for alignment, implementation, and verification.

The readiness receipt is the machine-verifiable planner PASS evidence; prose in a work pack cannot
substitute for it. A mismatch, missing file, path or symlink/junction escape, changed digest,
inflated topology, or capability-policy mismatch blocks registration and therefore blocks launch.

Canonical topology:

- Greenfield: `implementation` (exactly one `coder`) `sequential` to `verification` (exactly one
  `skeptic` or `auditor`).
- Brownfield: `alignment-audits` (exactly two independent `auditor`s, one alignment and one
  layering) `sequential` to `implementation`, then `sequential` to
  `verification`.

The coder may start only after every incoming group has returned PASS. The verifier receives the
task-owned diff, source-linked test results, strict tagging result, and the pinned input contract.
Any failing validation or scope escape returns to the coder only within the declared loop ceiling.
The final approver is outside every working group.

The only successful output bundle is:

- task-owned diff and changed-symbol inventory;
- work-pack/test-spec traceability;
- alignment and layering verdicts when brownfield;
- exact validation commands and exit results;
- strict tagging result or an explicit unavailable/blocking result;
- residual risks and `agents_spawned`.

Close as `resolved` only when the verifier accepts that bundle. Use `error` for execution/tool
failure, `loop_ceiling_reached` for non-convergent fixes, and `dissent_irreconcilable` for a
verifier/implementer conflict that cannot be settled inside the accepted specs.
