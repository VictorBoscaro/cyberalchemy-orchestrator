# Concept Relations

This map shows how concepts connect inside the player onboarding module and across module boundaries.

## Internal concept map

```mermaid
flowchart TD
  API[PublicOnboardingAPI] -->|exposes| OP1[SubmitCandidateApplication]
  WF1[CandidateOnboardingFlow] -->|orchestrates| OP1
  MAP1[SubmitCandidateRequestToEntity] -->|maps| ENT1[CandidateApplication]
  POL1[RuleScreenGroupingPolicy] -->|applies| OP1
  OP1 -->|produces| EVT1[CandidateApplicationSubmitted]
  EVT1 -->|transitions| STM1[CandidateApplicationLifecycle]
  OP2[ReviewCandidateApplication] -->|produces| EVT2[CandidateApplicationReviewed]
  EVT2 -->|transitions| STM1
  ENT1 -->|contains| VO1[RuleAcceptance]
  ENT1 -->|uses| ENUM1[ApplicationStatus]
```

## Internal relation table

| From | Edge | To | Why it matters |
| --- | --- | --- | --- |
| PublicOnboardingAPI | exposes | SubmitCandidateApplication | Public submission contract |
| CandidateOnboardingFlow | orchestrates | SubmitCandidateApplication | User journey execution |
| SubmitCandidateRequestToEntity | maps | CandidateApplication | Input normalization and field mapping |
| RuleScreenGroupingPolicy | applies | SubmitCandidateApplication | Readability and acceptance gate support |
| SubmitCandidateApplication | produces | CandidateApplicationSubmitted | Submission audit and event propagation |
| CandidateApplicationSubmitted | transitions | CandidateApplicationLifecycle | Lifecycle starts in `SUBMITTED` |
| ReviewCandidateApplication | produces | CandidateApplicationReviewed | Decision trace and downstream handoff |
| CandidateApplicationReviewed | transitions | CandidateApplicationLifecycle | Lifecycle closes to terminal state |
| CandidateApplication | contains | RuleAcceptance | Compliance evidence is embedded |
| CandidateApplication | uses | ApplicationStatus | Deterministic status model |

## External concept map

```mermaid
flowchart LR
  subgraph Onboarding Module
    POM[Player Onboarding]
    POM --> OPREV[ReviewCandidateApplication]
    POM --> OPPUB[SubmitCandidateApplication]
    POM --> Q1[ListCandidateApplications]
  end

  CAND[Candidate] -->|uses| OPPUB
  REV[Operations Reviewer] -->|uses| OPREV
  AAC[auth-access-control] -->|authorizes| OPREV
  PM[player-management] -->|consumes approved intake| POM
  OPS[Operations Backlog] -->|reads| Q1
  WEB[Web Frontend] -->|renders journey| POM
```

## Cross-boundary relationship table

| Source concept | Edge | External concept/module | Contract type | Evidence |
| --- | --- | --- | --- | --- |
| ReviewCandidateApplication | depends-on | auth-access-control | Authorization permission checks | `../SPEC.md` cross-feature dependencies, `../interfaces.md` |
| CandidateApplicationReviewed | produces-for | player-management | Approved intake handoff | `../SPEC.md` produces-for, `../events.md` |
| PublicOnboardingAPI | consumed-by | web | Public onboarding UX journey | `../SPEC.md` produces-for, `../interfaces.md` |
| ListCandidateApplications | consumed-by | operations | Manual review backlog | `../queries.md`, `../interfaces.md` |

## Relationship integrity checklist

- Every exposed mutation operation has explicit rule and error semantics.
- Every lifecycle transition is traceable to an operation or event.
- Every cross-module dependency has a named contract path.
- Approved output is explicitly tied to player-management intake.
