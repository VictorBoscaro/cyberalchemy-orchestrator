# Illustrative Dispatch Confirmation

> These views are examples only. They omit exact agents, prompts, source digests, tools, permissions
> and budgets, so they are not confirmable dispatches.

## Shared review contract

| Boundary | Reviewers | Robot-talks | Zig-zag |
|---|---:|---:|---:|
| SPEC | 2 | 1 round | 1 loop |
| Other artifact | 1 | 0 | 1 loop |
| Complete corpus | 2 fresh | 1 round | 1 loop |
| Final approval | 1 fresh | 0 | 0 |

## Medium confirmation view

```text
Feature: sample-feature
Work granularity: MEDIUM

Production:
  1 SPEC writer
  1 persistent writer for architecture, glossary, rules and operations

Review:
  2 independent SPEC reviewers
  1 persistent inline reviewer for every remaining artifact
  2 fresh complete-corpus reviewers
  1 fresh final reviewer

Execution:
  SPEC first
  remaining artifacts sequentially
  corpus review after every inline review passes

Illustrative seats: 8
Parallel downstream production branches: 0
```

## High confirmation view

```text
Feature: sample-feature
Work granularity: HIGH

Production:
  1 SPEC writer
  parallel specialist cells for architecture, glossary, rules and operations
  1 integration writer

Review:
  2 independent SPEC reviewers
  1 inline reviewer inside each specialist cell
  2 fresh complete-corpus reviewers
  1 fresh final reviewer

Execution:
  SPEC first
  4 downstream production branches in parallel
  integration after every local review passes
  corpus review after integration

Illustrative seats: 15
Parallel downstream production branches: 4
```

## What a real confirmation must add

- exact agent/persona and model for every seat;
- immutable prompt and response contract for every seat;
- exact source path and digest bindings;
- exact write paths, tools, network and sandbox scopes;
- token, round and total-cost budgets;
- expanded aspect set;
- statically unrolled review/rework rounds;
- terminal and invalidation behavior;
- digest of the complete candidate dispatch.

A user confirmation binds that exact digest. Any later topology, prompt, source, agent, scope or
budget change requires a new candidate and confirmation.
