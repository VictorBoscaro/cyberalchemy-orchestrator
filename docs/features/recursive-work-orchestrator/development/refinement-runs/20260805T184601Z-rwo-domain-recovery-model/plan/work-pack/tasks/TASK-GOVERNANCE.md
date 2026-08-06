# TASK-GOVERNANCE — Evidence-Backed Knowledge Adoption

## Objective

Propose an ontology delta only after executable evidence exists and an ontology
owner separately admits the change. This task owns SWU-RRD-010 and maps to
S-004/L3/W4.

## Dependencies And Blocker

- SWU-RRD-006 through 009 must have terminal validation receipts.
- G4 ontology/definitions owner must select promotion scope.
- This task is absent from `allowed-routes.json`; it cannot execute automatically.

## SWU-RRD-010 — Candidate Ontology Delta

- Primary behavior: encode evidence-backed recovery concepts and relations
  without turning candidate design or implementation into authority.
- Dependencies: 006–009 and G4.
- Exact proposed target inventory (the owner may reject it but may not widen it
  silently):
  - `docs/features/recursive-work-orchestrator/ontology/nodes/nodes.json`
  - `docs/features/recursive-work-orchestrator/ontology/relations/relations.json`
  - `docs/features/recursive-work-orchestrator/ontology/views/typed-coordinated-work-atlas.json`
  - `docs/features/recursive-work-orchestrator/ontology/ontology.json`
  - `docs/features/recursive-work-orchestrator/ontology/ONTOLOGY.md`
  - `docs/features/recursive-work-orchestrator/ontology/evidence/RECOVERY-DECISION-CONTRACT-CANDIDATE-2.json`
- Candidate nodes: RecoveryDecisionContract, RecoveryTriggerHandle,
  RecoveryFrontier, eight RecoveryCase variants, CaseAdmissionResult,
  RecoveryClassifier, RecoveryDisposition, RecoveryDecision,
  DecisionValidationVector, IdentityTransition, ReconciliationIntent,
  CompensationIntent, and ExhaustionRoute.
- Candidate relations: producer/consumer/cause/owner/constraint links only;
  none implies truth, authorization, execution, or promotion.
- Done: every node has a direct evidence selector and claim ceiling; closed
  enums remain properties unless graph addressability is justified; current
  counts/views rebuild; all ontology validators pass.
- Acceptance evidence: exact owner decision, node/relation schema validation,
  build parity, invalid authority/effect fixtures, and source receipt links.
- Validation: `node docs/features/recursive-work-orchestrator/ontology/scripts/validate.mjs && node docs/features/recursive-work-orchestrator/ontology/scripts/validate-graph.mjs`.
- Execution owner: manual ontology owner route only.
- Split analysis: nodes without relations/evidence are not a meaningful graph
  delta; validation must assess the recomposed candidate change.

## Completion And Claim Ceiling

Completion means an owner-reviewed candidate ontology delta passes local graph
validation. It does not mean canonical definitions, authority-spine promotion,
publication, deployment, pilot adoption, release, or production evidence.
