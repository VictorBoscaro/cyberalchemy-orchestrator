# Task Session Closeout Contract

## Ownership

Task Session owns one selected SWU and its terminal execution receipt. `invoke:refresh:apply-approved` may update only the planning/evidence targets declared for that SWU. Closeout cannot implement a successor, change authority, publish, deploy, or select the next unit.

## Baseline and source receipt

Before mutation, Task Session records exact existence/kind/SHA-256 for the selected SWU write scope and scoped porcelain state under `plan/session-evidence/<SWU-ID>/baseline.json`. After validation it writes `task-session-receipt.json` binding the work-pack digest, SWU, baseline, touched files, commands, blockers, undeclared writes and authority effect `none`.

## Closeout receipt

The owner writes `plan/session-evidence/<SWU-ID>/owner-receipt.json`, binding the source receipt digest, exact validated targets, admitted deltas, validation result, empty blockers and the unique eligible-but-unselected successor (or none).

## Admitted deltas

Only `evidence_added`, `blocker_opened`, `blocker_resolved`, `status_changed`, and `route_changed` are admitted. Implementation, deletion, promotion, publication, deployment and successor selection are forbidden closeout deltas.

## Successor rule

The successor is the next unit in `EXECUTION-ENTRY.json.frontier` only when all predecessor owner receipts pass and no blocker affects its boundary. Eligibility does not imply selection.
