# Rules Playbook

This file is a rule ownership index.

It does not define operation-level rules directly.

## Rule authority model

1. Shared rules are authoritative in epic scope.
2. Operation rules are authoritative in capability files.
3. This file routes readers to the owning document for each rule family.

## Canonical reference format

Use canonical references in the form `OperationOrStateMachine.RuleId`.

Examples:
- `SubmitCandidateApplication.R1`
- `ReviewCandidateApplication.R1`
- `CandidateApplicationLifecycle.I1`
- `ReviewCandidateApplication.P6`

## Shared rules (authoritative in epic)

| Canonical reference | Description | Authority |
| --- | --- | --- |
| CandidateOnboardingFlow.I1 | Submission requires rules acceptance gate | [01-EPIC-POINT-OF-VIEW.md](01-EPIC-POINT-OF-VIEW.md) |
| SubmitCandidateApplication.R1 | Rules acceptance version/timestamp required | [01-EPIC-POINT-OF-VIEW.md](01-EPIC-POINT-OF-VIEW.md) |
| SubmitCandidateApplication.R2 | LGPD consent required | [01-EPIC-POINT-OF-VIEW.md](01-EPIC-POINT-OF-VIEW.md) |
| SubmitCandidateApplication.R5 | Duplicate by canonical email/WhatsApp blocked | [01-EPIC-POINT-OF-VIEW.md](01-EPIC-POINT-OF-VIEW.md) |
| ReviewCandidateApplication.R1 | Review requires auth/authz | [01-EPIC-POINT-OF-VIEW.md](01-EPIC-POINT-OF-VIEW.md) |
| ReviewCandidateApplication.P6 | Approved decisions publish deterministic handoff | [01-EPIC-POINT-OF-VIEW.md](01-EPIC-POINT-OF-VIEW.md) |
| CandidateApplicationLifecycle.I1 | Terminal states cannot return to active states | [01-EPIC-POINT-OF-VIEW.md](01-EPIC-POINT-OF-VIEW.md) |
| CandidateApplicationLifecycle.I2 | Rules acceptance evidence required after submission | [01-EPIC-POINT-OF-VIEW.md](01-EPIC-POINT-OF-VIEW.md) |
| CandidateApplicationLifecycle.I3 | LGPD consent evidence required after submission | [01-EPIC-POINT-OF-VIEW.md](01-EPIC-POINT-OF-VIEW.md) |

## Operation rules (authoritative in capability files)

| Capability | Owned operation or policy rules | Authority file |
| --- | --- | --- |
| CAP-01 | CandidateOnboardingFlow.I1, CandidateOnboardingFlow.I2, RuleScreenGroupingPolicy decision table | [CAP-01-COMPOSE-GUIDED-ONBOARDING-FLOW.md](capabilities/CAP-01-COMPOSE-GUIDED-ONBOARDING-FLOW.md) |
| CAP-02 | SubmitCandidateApplication.R1, SubmitCandidateApplication.R2 | [CAP-02-ENFORCE-COMPLIANCE-GATE.md](capabilities/CAP-02-ENFORCE-COMPLIANCE-GATE.md) |
| CAP-03 | SubmitCandidateApplication.R3, SubmitCandidateApplication.R4, SubmitCandidateApplication.R5, SubmitCandidateApplication.R6, SubmitCandidateApplication.R7, SubmitCandidateApplication.R8, SubmitCandidateApplication.R9 | [CAP-03-CAPTURE-QUALIFIED-APPLICATION.md](capabilities/CAP-03-CAPTURE-QUALIFIED-APPLICATION.md) |
| CAP-04 | ReviewCandidateApplication.R1, ReviewCandidateApplication.R2, ReviewCandidateApplication.R3, ReviewCandidateApplication.R4 | [CAP-04-EXECUTE-CONTROLLED-REVIEW.md](capabilities/CAP-04-EXECUTE-CONTROLLED-REVIEW.md) |
| CAP-05 | ReviewCandidateApplication.P6 plus CandidateApplicationReviewed payload/produced-by contracts | [CAP-05-HANDOFF-APPROVED-INTAKE.md](capabilities/CAP-05-HANDOFF-APPROVED-INTAKE.md) |
| CAP-06 | Observability metric-rule family | [CAP-06-OBSERVE-FUNNEL-HEALTH.md](capabilities/CAP-06-OBSERVE-FUNNEL-HEALTH.md) |

## Rule lookup matrix

| Canonical reference group | Rule scope | Authority |
| --- | --- | --- |
| CandidateOnboardingFlow.I1 and CandidateApplicationLifecycle.I1..I3 | Shared cross-capability integrity rules | [01-EPIC-POINT-OF-VIEW.md](01-EPIC-POINT-OF-VIEW.md) |
| SubmitCandidateApplication.R1..R2 | Submission compliance gate | [CAP-02-ENFORCE-COMPLIANCE-GATE.md](capabilities/CAP-02-ENFORCE-COMPLIANCE-GATE.md) |
| SubmitCandidateApplication.R3..R9 | Submission qualification and dedupe | [CAP-03-CAPTURE-QUALIFIED-APPLICATION.md](capabilities/CAP-03-CAPTURE-QUALIFIED-APPLICATION.md) |
| ReviewCandidateApplication.R1..R4 | Review decision governance | [CAP-04-EXECUTE-CONTROLLED-REVIEW.md](capabilities/CAP-04-EXECUTE-CONTROLLED-REVIEW.md) |
| ReviewCandidateApplication.P6 | Approved handoff integrity | [CAP-05-HANDOFF-APPROVED-INTAKE.md](capabilities/CAP-05-HANDOFF-APPROVED-INTAKE.md) |

## Governance note

If a rule appears to be duplicated between files, epic shared rules and capability-owned rules are the only valid authorities.
Any drift should be corrected by updating those authority files, not this index.
