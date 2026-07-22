---
id: player-onboarding-stories
feature: player-onboarding
title: Player Onboarding User Stories
summary: Capability-scoped user stories for candidate onboarding flow with rules reading, submission, and review.
status: implemented
pillar: operations
domain: onboarding-candidates
audience:
  - operations
  - developers
priority: p1
lang: en
owners:
  - operations-core
  - web-core
updatedAt: 2026-04-14
dependencies:
  - SPEC.md
includes: []
---

# Player Onboarding — User Stories

> Source of storytelling truth for [player-onboarding](SPEC.md).

## US-01 Public Journey: Candidate Submits Onboarding Application After Reading Rules

**Classic format**
As a **candidate**, I want **to read grouped rules and only then submit my application**, so that **my registration is compliant and eligible for review**.

**BDD scenario**
Given the onboarding flow loads active grouped rule screens
When I accept the current regulation version and submit all required personal and operational fields
Then the system stores my application as `SUBMITTED` with rules acceptance metadata

**Acceptance checks**

- [ ] Submission is blocked unless regulation version and acceptance timestamp exist.
- [ ] Submission is rejected when mandatory fields, LGPD consent, or minimum age requirements fail.
- [ ] Successful submissions persist rule acceptance and expose confirmation state.

**Capability link**: [SPEC — Capabilities](SPEC.md#concepts)

**Concept and aspect links**

- player-onboarding.CandidateApplication: [CandidateApplication](domain.md#candidateapplication)
- player-onboarding.RuleAcceptance: [RuleAcceptance](domain.md#ruleacceptance)
- player-onboarding.SubmitCandidateApplication: [SubmitCandidateApplication](operations.md#submitcandidateapplication)
- player-onboarding.CandidateApplicationState: [CandidateApplicationLifecycle](states.md#candidateapplicationlifecycle)
- player-onboarding.PublicOnboardingAPI: [PublicOnboardingAPI](interfaces.md#external-publiconboardingapi-rest)
- player-onboarding.CandidateOnboardingFlow: [CandidateOnboardingFlow](workflows.md#candidateonboardingflow)

---

## US-02 Admin Operations Journey: Reviewer Records Manual Decision

**Classic format**
As an **operations reviewer**, I want **to approve or reject submitted applications with controlled permissions**, so that **candidate intake remains auditable and consistent**.

**BDD scenario**
Given I am authenticated with onboarding review permission and the candidate is in `SUBMITTED` or `UNDER_REVIEW`
When I send an approve or reject decision
Then the application transitions to a final reviewed status with deterministic retention behavior for rejections

**Acceptance checks**

- [ ] Unauthorized users cannot execute review decisions.
- [ ] Review decisions are accepted only for valid pre-review statuses.
- [ ] Rejected applications store retention cutoff based on review timestamp.

**Capability link**: [SPEC — Capabilities](SPEC.md#concepts)

**Concept and aspect links**

- player-onboarding.ReviewCandidateApplication: [ReviewCandidateApplication](operations.md#reviewcandidateapplication)
- player-onboarding.ApplicationStatus: [ApplicationStatus](domain.md#applicationstatus)
- player-onboarding.CandidateApplicationState: [CandidateApplicationLifecycle](states.md#candidateapplicationlifecycle)
- player-onboarding.PublicOnboardingAPI: [PublicOnboardingAPI](interfaces.md#external-publiconboardingapi-rest)
- player-onboarding.CandidateOnboardingFlow: [AdminCandidateReviewFlow](workflows.md#admincandidatereviewflow)

---

## US-03 Cross-Feature Integration: Approved Output Feeds Player Creation Pipeline

**Classic format**
As a **player-management consumer**, I want **approved onboarding records with validated intake data**, so that **player creation starts from reliable candidate evidence**.

**BDD scenario**
Given candidate applications include rules acceptance and validated identity/contact data
When operations approves a candidate
Then downstream player-management receives a trustworthy intake signal for the next flow

**Acceptance checks**

- [ ] Approved records preserve submitted onboarding payload and review metadata.
- [ ] The dependency contract with player-management remains explicit in feature docs.
- [ ] Produces-for contract remains aligned with onboarding workflow output.

**Capability link**: [SPEC — Cross-Feature Dependencies](SPEC.md#cross-feature-dependencies)

**Concept and aspect links**

- player-onboarding.CandidateApplication: [CandidateApplication](domain.md#candidateapplication)
- player-onboarding.CandidateOnboardingFlow: [CandidateOnboardingFlow](workflows.md#candidateonboardingflow)
- player-onboarding.CandidateApplicationState: [CandidateApplicationLifecycle](states.md#candidateapplicationlifecycle)

---

## US-04 Error And Edge Case Journey: Deterministic Feedback On Duplicates And Invalid Data

**Classic format**
As a **candidate**, I want **clear validation and conflict feedback during submission**, so that **I can correct errors without ambiguity**.

**BDD scenario**
Given I attempt to submit onboarding data
When validation rules fail or my contact already exists
Then the API returns deterministic error categories (`400` validation or `409` duplicate candidate)

**Acceptance checks**

- [ ] Duplicate by WhatsApp or canonical email returns conflict response.
- [ ] Validation failures map to documented rule checks and correction paths.
- [ ] Failure paths preserve mandatory acceptance gate behavior.

**Capability link**: [SPEC — Capabilities](SPEC.md#concepts)

**Concept and aspect links**

- player-onboarding.SubmitCandidateApplication: [SubmitCandidateApplication](operations.md#submitcandidateapplication)
- player-onboarding.SubmitCandidateRequestToEntity: [SubmitCandidateRequestToEntity](mappings.md#submitcandidaterequesttoentity)
- player-onboarding.CandidateApplicationState: [CandidateApplicationLifecycle](states.md#candidateapplicationlifecycle)
- player-onboarding.PublicOnboardingAPI: [PublicOnboardingAPI](interfaces.md#external-publiconboardingapi-rest)
- player-onboarding.CandidateOnboardingFlow: [CandidateOnboardingFlow](workflows.md#candidateonboardingflow)

---

## Story Coverage Matrix

| Slice                     | Story IDs | Covered Concepts                                                                          | Notes                                                 |
| ------------------------- | --------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| Public journey            | US-01     | CandidateApplication, RuleAcceptance, SubmitCandidateApplication, CandidateOnboardingFlow | Rules-first gating and submission flow                |
| Admin operations          | US-02     | ReviewCandidateApplication, ApplicationStatus, CandidateApplicationLifecycle              | Manual review with authorization and retention policy |
| Cross-feature integration | US-03     | CandidateApplication, CandidateOnboardingFlow                                             | Produces onboarding intake for player-management      |
| Error and edge cases      | US-04     | SubmitCandidateApplication, SubmitCandidateRequestToEntity                                | Deterministic conflict and validation outcomes        |

**Coverage gap check**: All concepts from the player-onboarding concept table are covered by at least one story slice. RuleScreenGroupingPolicy is implicitly covered by US-01 flow.
