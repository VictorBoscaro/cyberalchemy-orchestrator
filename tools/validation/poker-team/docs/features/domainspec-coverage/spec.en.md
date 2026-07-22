---
id: domainspec-coverage
feature: domainspec-coverage
title: DomainSpec Coverage Audit
summary: Inventory and rollout status for DomainSpec adoption across implemented backend slices.
status: in-progress
pillar: platform
domain: documentation-governance
audience:
  - leadership
  - developers
priority: p1
lang: en
owners:
  - architecture-core
updatedAt: 2026-04-04
dependencies:
  - player-management
  - player-makeup
  - player-stats
  - player-progression
  - financial-settlement
includes:
  - gaps.en.md
  - layering-audit.en.md
  - layering-alignment-plan.en.md
---

## Coverage Summary

| Slice                   | Implementation Found  | DomainSpec Added      | Notes                                                         |
| ----------------------- | --------------------- | --------------------- | ------------------------------------------------------------- |
| player-management       | yes                   | yes                   | New DomainSpec baseline created                               |
| player-makeup           | yes                   | yes                   | Full DomainSpec set including states/events/workflows         |
| player-stats             | yes                   | yes                   | Operation and side-effects specified                          |
| player-progression      | yes                   | yes                   | Eligibility formulas and thresholds specified                 |
| financial-settlement    | yes                   | yes                   | Full mutation and policy workflow specified                   |
| ecosystem-api-expansion | partial strategy docs | no DomainSpec set yet | Not directly mapped to concrete route/use-case implementation |

## Next Milestone

Run the layering alignment waves in [layering-alignment-plan.en.md](layering-alignment-plan.en.md), then regenerate docs indexes and execute backend test suites per wave.
