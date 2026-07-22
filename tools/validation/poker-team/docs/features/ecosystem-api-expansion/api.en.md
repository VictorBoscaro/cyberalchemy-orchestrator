---
id: ecosystem-api-expansion
feature: ecosystem-api-expansion
title: Ecosystem API Expansion API
summary: Candidate API domains and endpoint families for stable operations and ecosystem growth.
status: planned
pillar: platform
domain: ecosystem-api
audience:
  - developers
  - leadership
priority: p1
lang: en
owners:
  - backend-core
updatedAt: 2026-03-24
dependencies:
  - spec.en.md
includes: []
---

## API Domains and Endpoint Families

1. Identity and Organization

- GET /orgs/:orgId
- GET /orgs/:orgId/members
- GET /players/:playerId/account-status

Business outcome: team-level governance, role-aware visibility, and compliance state tracking.

2. Wallet and Ledger

- GET /players/:playerId/wallet/balance
- GET /players/:playerId/wallet/transactions
- POST /wallet/reconciliations

Business outcome: automated make-up control, bankroll reset flows, and finance reconciliation without spreadsheets.

3. Session and Performance Events

- GET /players/:playerId/sessions
- GET /players/:playerId/performance
- GET /players/overview

Business outcome: progression and risk decisions based on verified operational data.

4. Settlement and Payout Orchestration

- POST /settlements
- GET /settlements/:settlementId
- POST /payouts

Business outcome: faster payout cycles, deterministic split application, and auditable cash operations.

5. Coaching and Study Signals

- GET /players/:playerId/study-events
- POST /players/:playerId/coaching-bookings
- GET /players/:playerId/progress

Business outcome: unified manager view of financial output plus training discipline and learning velocity.

6. Webhooks and Notifications

- POST /webhooks/subscriptions
- POST /webhooks/test
- Event types: session.closed, payout.completed, account.status.changed, tournament.finished

Business outcome: near real-time automation of routine workflows and reduced operational delay.

## Minimum Integration Requirements for Pilot

- Historical backfill for wallet transactions and session events
- Real-time webhooks for payout and session close events
- Stable identifiers across players, sessions, and transactions
- Basic SLA for event delivery and data freshness
