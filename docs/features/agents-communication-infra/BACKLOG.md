---
tags: [agent-orchestration, cross-dispatch-workflows, task-graphs, durable-handoffs, review-gates]
artifact_kind: backlog
layer: feature
version: 0.1.0
last_updated: 2026-07-27
---

# Agents Communication Infrastructure backlog

This file records candidate work for the feature. An entry names an open capability to evaluate;
it is not a normative runtime contract, an implementation claim, or scheduled work.

## Connections

| Document | Type | Description |
|---|---|---|
| [Feature architecture](README.md) | `contextualizes` | Defines the current DispatchSpec, group, connection, recipe, BUS, recovery, and authority boundaries within which this candidate must be evaluated. |
| [Feature work pack](WORK-PACK.md) | `contextualizes` | Records the current delivery gates and bounded implementation status; this backlog entry does not expand either. |
| [Agent tools and delegated supervision discovery](discovery/agent-tools-and-delegated-supervision.md) | `derives-from` | Supplies the candidate durable task-state, review, rework, routing, handoff, and replay concepts summarized by this entry. |
| [BUS contracts discovery](discovery/bus-contracts/README.md) | `derives-from` | Supplies the mediated publication, digest binding, release-gate, and command-plane boundaries that constrain the candidate. |

## ACI-BL-001 — Promotion-gated cross-dispatch work graph

**Tags:** cross-dispatch orchestration, dependency graphs, typed dispatches, durable state,
content-addressed handoffs, independent review, recovery

**Objective:** Evaluate whether ACI needs a promotion-gated, recoverable parent work graph that can
coordinate typed child dispatches across parallel and sequential dependencies while retaining one
explicit authority path from confirmation through final parent approval.

**Description:** The open capability is a confirmed task graph whose nodes have durable task state
and launch typed child dispatches only when their declared dependency and authority predicates are
satisfied. Parallel nodes may proceed independently; sequential successors remain locked until
every required predecessor has produced a digest-bound BUS handoff, passed independent review, and
reached a `PASS` outcome. A `FIX` outcome must reopen or supersede the responsible work through an
explicit repair loop, preserve review and generation lineage, and prevent downstream promotion
until the repaired result passes. The parent must retain final approval over the assembled result
after all required successors pass.

The candidate must make crash recovery, replay, retries, replacement, and idempotency explicit:
durable identities and state must distinguish logical work from attempts, bind deliveries and
reviews to exact result digests, reject stale or divergent retries, and reconstruct which nodes are
ready, blocked, fixing, passed, or awaiting parent approval without repeating an accepted effect.
BUS messages remain mediated evidence and handoffs; they do not self-authorize execution, create a
child dispatch, unlock a successor, or grant final approval. Those transitions require the
confirmed graph plus the canonical command/runtime authority.

**Collapse condition:** If the current `DispatchSpec` groups, typed connections, and BUS contracts,
combined with a versioned recipe, can represent and recover this graph and its promotion gates
without introducing new cross-dispatch identity, do not add a `work` dispatch type. Prefer that
composition and close or narrow this candidate.
