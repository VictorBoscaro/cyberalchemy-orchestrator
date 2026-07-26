---
status: accepted
date: 2026-07-25
scope: repository-leverage-priority
---

# Repository Leverage Priority

## Decision

Advance both leading capabilities sequentially:

1. repair and ratify the existing Host Binding → BUS reveal/materialized-input dogfood seam;
2. prepare and implement ACI-005, the opening materializer.

## Rationale

The dogfood seam provides fast executable feedback and detects contract, identity, fixture, and
manifest drift. ACI-005 then adds the missing primitive with the strongest evidenced downstream
dependency centrality.

Parallel code implementation is rejected because the two slices share runtime, tests, manifests,
specification ownership, and authority/identity boundaries.

## Readiness amendment

A later independent readiness check found active `0.6.1` versus `0.6.2` schema drift and a red
focused Host Binding + BUS suite. Consequently, the first mutation-capable dispatch must be
preceded by compatibility review and reconciliation authoring. ACI-005 must not receive a code
dispatch until its discovery, tests, SWU descriptor, and readiness receipt are complete.

## Subsequent state change

The schema drift was repaired by concurrent repository work before a repair dispatch opened. Fresh
validation on the current bytes passed all five Host Workflow Binding tests and all seven BUS
Reveal Delivery tests. The next route is therefore a closing review of Phase A, not automatic
repair. ACI-005 readiness requirements remain unchanged.

## Source of decision

The repository owner explicitly selected implementing both candidates and delegated ongoing
readiness classification and dispatch organization to the primary orchestrator.

## Remaining blockers

- Ratify historical/current schema compatibility.
- Reconcile producers, fixtures, mappings, goldens, and source-integrity manifests.
- Produce and review the exact ACI-005 readiness package.
