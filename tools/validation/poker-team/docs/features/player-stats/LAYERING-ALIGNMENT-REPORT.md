---
id: player-stats
feature: player-stats
title: Player Stats Layering Alignment Report
summary: 2026-04-24 layering refresh for stats window derivation ownership.
status: in-progress
pillar: operations
domain: player-stats-layering
audience:
  - developers
  - architecture
priority: p1
lang: en
owners:
  - backend-core
updatedAt: 2026-04-24
dependencies:
  - SPEC.md
  - ALIGNMENT-REPORT.md
includes: []
---

# Layering Alignment Report: player-stats

**Audited at:** 2026-04-24
**Framework version:** DomainSpec 1.8.2

## Executive Summary

1. Stats ingestion and retrieval flows remain correctly layered.
2. Derived stats-window policy logic is now centralized in a domain service.
3. Layering evidence is refreshed to current runtime structure.

## Findings

| ID | Status | Severity | Layering Issue | Evidence | Remediation Requirement |
| --- | --- | --- | --- | --- | --- |
| PST-LDR-01 | RESOLVED | MEDIUM | derived window policy partly in use-case | `backend/src/domain/player-stats/player-stats-window-policy.service.ts`, `backend/src/use-cases/player-stats/get-player-stats-window.ts`, `backend/src/domain/player-stats/player-stats-window-policy.service.test.ts` | None. Use-case now orchestrates and delegates derivation policy to domain authority. |
| PST-LDR-02 | RESOLVED | LOW | artifact freshness debt | [ALIGNMENT-REPORT.md](ALIGNMENT-REPORT.md), [TEST-SPEC.md](TEST-SPEC.md) | None. Layering artifact set is refreshed for current wave. |

## Layer Verdict

**PASS** - no open layering drift remains for stats derivation ownership.
