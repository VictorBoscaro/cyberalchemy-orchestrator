---
id: player-onboarding
feature: player-onboarding
title: Candidate Onboarding
summary: Specification for candidate onboarding flow with mandatory rules reading and registration form submission.
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
  - backend-core
updatedAt: 2026-04-17
dependencies:
  - auth-access-control
  - player-management
includes:
  - domain.md
  - operations.md
  - states.md
  - events.md
  - interfaces.md
  - queries.md
  - mappings.md
  - workflows.md
  - STORIES.md
  - TEST-SPEC.md
  - tasks.en.md
  - decisions.en.md
---

# Player Onboarding

## Overview

This feature defines the public candidate onboarding journey: guided reading of the official rules, explicit acceptance of terms, and candidate form submission for manual leadership review.

The objective is to ensure each submitted application has confirmed acknowledgment of operational rules and includes the minimum data required for initial screening.

## Stories

See [STORIES.md](STORIES.md) for capability-scoped user stories with classic + BDD format, acceptance checks, and Story Coverage Matrix.

## User Stories

See [STORIES.md](STORIES.md) for classic and BDD story definitions.

## Story Coverage Matrix

See [Story Coverage Matrix](STORIES.md#story-coverage-matrix) for concept and capability coverage.

## Pilot Decisions

Pilot policy and verification decisions are recorded in [PILOT-DECISIONS.md](PILOT-DECISIONS.md).

## Concepts

| Concept                                                                      | ID                                               | Type          | Description                                                      |
| ---------------------------------------------------------------------------- | ------------------------------------------------ | ------------- | ---------------------------------------------------------------- |
| [CandidateApplication](domain.md#candidateapplication)                       | player-onboarding.CandidateApplication           | Entity        | Candidate application with personal and operational data         |
| [RuleAcceptance](domain.md#ruleacceptance)                                   | player-onboarding.RuleAcceptance                 | Value Object  | Rules acceptance record with version and timestamp               |
| [ApplicationStatus](domain.md#applicationstatus)                             | player-onboarding.ApplicationStatus              | Enum / Type   | Candidate application lifecycle states                           |
| [SubmitCandidateApplication](operations.md#submitcandidateapplication)       | player-onboarding.SubmitCandidateApplication     | Operation     | Submits application after mandatory rules acceptance             |
| [ReviewCandidateApplication](operations.md#reviewcandidateapplication)       | player-onboarding.ReviewCandidateApplication     | Operation     | Records manual review decision for application                   |
| [CandidateApplicationLifecycle](states.md#candidateapplicationlifecycle)     | player-onboarding.CandidateApplicationState      | State Machine | Defines application status transitions                           |
| [CandidateApplicationSubmitted](events.md#candidateapplicationsubmitted)     | player-onboarding.CandidateApplicationSubmitted  | Event         | Emitted after candidate submission is persisted                  |
| [CandidateApplicationReviewed](events.md#candidateapplicationreviewed)       | player-onboarding.CandidateApplicationReviewed   | Event         | Emitted after review decision is recorded                        |
| [PublicOnboardingAPI](interfaces.md#external-publiconboardingapi-rest)       | player-onboarding.PublicOnboardingAPI            | Interface     | Public HTTP contracts for onboarding flow and submission         |
| [SubmitCandidateRequestToEntity](mappings.md#submitcandidaterequesttoentity) | player-onboarding.SubmitCandidateRequestToEntity | Mapping       | Maps HTTP payload to candidate entity                            |
| [CandidateOnboardingFlow](workflows.md#candidateonboardingflow)              | player-onboarding.CandidateOnboardingFlow        | Workflow      | Orchestrates rules reading, acceptance, and candidate submission |
| [RuleScreenGroupingPolicy](workflows.md#rulescreengroupingpolicy)            | player-onboarding.RuleScreenGroupingPolicy       | Policy        | Policy for grouping rules into readable screens                  |

## Feature Concept Graph

| From                                               | Edge         | To                                                | Evidence                                          | Notes                                        |
| -------------------------------------------------- | ------------ | ------------------------------------------------- | ------------------------------------------------- | -------------------------------------------- |
| player-onboarding.PublicOnboardingAPI             | exposes      | player-onboarding.SubmitCandidateApplication      | interfaces.md#external-publiconboardingapi-rest   | Public API exposes candidate submission      |
| player-onboarding.CandidateOnboardingFlow         | orchestrates | player-onboarding.SubmitCandidateApplication      | workflows.md#candidateonboardingflow              | Workflow coordinates submission steps        |
| player-onboarding.SubmitCandidateRequestToEntity  | maps         | player-onboarding.CandidateApplication            | mappings.md#submitcandidaterequesttoentity        | Request payload mapped to domain entity      |
| player-onboarding.SubmitCandidateApplication      | produces     | player-onboarding.CandidateApplicationSubmitted   | operations.md#submitcandidateapplication          | Successful submission emits event            |
| player-onboarding.CandidateApplicationSubmitted   | transitions  | player-onboarding.CandidateApplicationState       | states.md#candidateapplicationlifecycle           | Submission event advances application state  |
| player-onboarding.RuleScreenGroupingPolicy        | applies      | player-onboarding.SubmitCandidateApplication      | workflows.md#rulescreengroupingpolicy             | Policy constrains rule grouping before submit |

## Aspects

- [Domain](domain.md)
- [Operations](operations.md)
- [States](states.md)
- [Events](events.md)
- [Interfaces](interfaces.md)
- [Queries](queries.md)
- [Mappings](mappings.md)
- [Workflows](workflows.md)

## Cross-Feature Dependencies

| Depends On          | Relationship | Why                                                               |
| ------------------- | ------------ | ----------------------------------------------------------------- |
| auth-access-control | exposes      | Reuses authentication and authorization for internal review stage |
| player-management   | produces     | Approved applications feed player creation flow                   |

## Produces For

| Consumer          | Via       | What                                               |
| ----------------- | --------- | -------------------------------------------------- |
| player-management | Workflow  | Validated intake for player creation               |
| operations        | Interface | Candidate backlog with data and rules acceptance   |
| web               | Interface | Public onboarding journey driven by rules and form |

## Undefined Or Pending Decisions

- Final LGPD legal consent text version and legal owner sign-off.
