---
status: accepted
date: 2026-08-06
scope: recursive-work-orchestrator-composition-forms
decision_id: DG-RWO-CFM-003
selected_option: LATE-RETAIN-NONCONTRIBUTING
---

# RWO FanIn late-arrival disposition

## Decision

An otherwise valid source arrival accepted after a FanIn release manifest has frozen is retained as non-contributing late evidence. It never reopens or revises the released FanIn.

The journal may append the accepted arrival, and a version-compatible reducer may advance its cursor past that record and emit a typed `LateArrivalRetained` observation. The following release state remains immutable:

- the frozen eligible-source set;
- canonical join-input manifest;
- release sequence and release identity;
- structural quorum result;
- join command identity and emission count; and
- downstream Work Run and Work Attempt identities.

An identical transport redelivery remains the same logical arrival and does not create another accepted fact. Divergent bytes under one logical identity follow the journal-owned quarantine route, not the ordinary late-arrival route.

If late evidence requires reconciliation, rework, compensation, notification, or another domain action, that behavior must be expressed as an ordinary separately owned Work or edge. FanIn does not infer it.

## Rationale

Retention preserves auditability, deduplication, reconciliation, and deterministic replay without making release timing mutable. Rejecting every otherwise valid late arrival would lose accepted-history visibility; quarantining normal lateness would conflate a valid timing outcome with corrupt or ambiguous evidence.

## Authority boundary

This decision settles the RWO projection of an owner-accepted late arrival. The journal owner still decides structural acceptance, fencing, duplicate handling, byte divergence, and persistence. This decision does not authorize journal, reducer, schema, design, ontology, implementation, projection, promotion, release, deployment, or production mutation.

## Source and consequences

- Source design: `docs/features/recursive-work-orchestrator/DESIGN.md` §6.2.
- Refined candidate and planned fixture: `docs/features/recursive-work-orchestrator/development/refinement-runs/20260806T173343Z-rwo-composition-form-metamodel/delegated-research/findings.md`.
- Admissibility receipt: `docs/features/recursive-work-orchestrator/development/decision-gates/20260806T203541Z-composition-form-owners/receipts/DG-RWO-CFM-003-option-admissibility.json`.
- Decision source: repository owner selected option `LATE-RETAIN-NONCONTRIBUTING` in the active 2026-08-06 Decision Gate.

Future candidate reducer contracts and fixtures may cite this record for evidence retention and the no-reopen/no-rewrite boundary. Runtime conformance remains unproved.
