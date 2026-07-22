---
id: player-onboarding-ui
feature: player-onboarding
title: Player Onboarding UI Specification
summary: Frontend design contract for public onboarding flow and admin candidate review.
status: draft
pillar: platform
domain: player-onboarding-ui
audience:
  - developers
priority: p1
lang: en
owners:
  - web-core
updatedAt: 2026-04-15
dependencies:
  - SPEC.md
  - interfaces.md
  - operations.md
  - queries.md
  - states.md
  - workflows.md
  - STORIES.md
includes: []
constitution: docs/UI-ARCHITECTURE.md
---

# UI Specification: Player Onboarding

> Governs the frontend presentation of the public onboarding flow and admin candidate review.
> Constrained by [UI-ARCHITECTURE.md](../../UI-ARCHITECTURE.md).

**Note:** This feature already has a complete UI implementation. This spec documents the existing contract for E2E test generation and audit alignment.

---

## Route Table

| Route               | Page Title        | Layout          | Auth Required | Permission                                |
| ------------------- | ----------------- | --------------- | ------------- | ----------------------------------------- |
| `/onboarding`       | Join Poker Team   | AuthLayout      | No            | Public                                    |
| `/admin/onboarding` | Onboarding Review | DashboardLayout | Yes           | `player-onboarding.review.listCandidates` |

---

## Page Layouts

### /onboarding (Public)

```
┌───────────────────────────────────────────┐
│           AuthLayout (centered)           │
│  ┌─────────────────────────────────────┐  │
│  │  OnboardingFlow                     │  │
│  │  ┌───────────────────────────────┐  │  │
│  │  │ Step indicator (1/N)          │  │  │
│  │  ├───────────────────────────────┤  │  │
│  │  │ Rules screen (grouped)       │  │  │
│  │  │  OR                          │  │  │
│  │  │ Candidate form (multi-field) │  │  │
│  │  ├───────────────────────────────┤  │  │
│  │  │ [Back] [Next/Submit]         │  │  │
│  │  └───────────────────────────────┘  │  │
│  └─────────────────────────────────────┘  │
└───────────────────────────────────────────┘
```

### /admin/onboarding (Review)

```
┌──────────────────────────────────────────────┐
│ Header: "Onboarding Review"                  │
│ Filter: [Status ▼]                           │
├──────────────────────────────────────────────┤
│ CandidateTable (list mode)                   │
│ ┌──────┬───────┬──────────┬────────────────┐ │
│ │Name  │Email  │Status    │Submitted       │ │
│ └──────┴───────┴──────────┴────────────────┘ │
│                                              │
│ — OR — (detail mode when candidate selected) │
│                                              │
│ CandidateDetail (read-only)                  │
│   All application fields displayed           │
│   [Approve] [Reject] buttons                 │
│   Review note textarea                       │
└──────────────────────────────────────────────┘
```

---

## Component Inventory

| Component               | Type  | Location                                          | Purpose                           |
| ----------------------- | ----- | ------------------------------------------------- | --------------------------------- |
| `OnboardingFlow`        | Flow  | `components/onboarding/OnboardingFlow.tsx`        | Multi-step rules + form wizard    |
| `AdminOnboardingReview` | Page  | `components/onboarding/AdminOnboardingReview.tsx` | Candidate list + detail + review  |
| `CandidateStatusBadge`  | Badge | `components/onboarding/CandidateStatusBadge.tsx`  | SUBMITTED/APPROVED/REJECTED badge |

---

## Data Flow

### /onboarding

| API Call                      | Hook/Method         | Triggers          |
| ----------------------------- | ------------------- | ----------------- |
| `GET /onboarding/flow`        | fetch on mount      | Page load         |
| `POST /onboarding/candidates` | form submit handler | User submits form |

### /admin/onboarding

| API Call                                  | Hook                          | Cache Key                      |
| ----------------------------------------- | ----------------------------- | ------------------------------ |
| `GET /admin/onboarding/candidates`        | `useCandidates(status, page)` | `queryKeys.onboarding.queue()` |
| `GET /admin/onboarding/candidates/:id`    | `useCandidate(id)`            | `queryKeys.onboarding.all, id` |
| `PATCH /onboarding/candidates/:id/review` | `useReviewCandidate()`        | Invalidate queue               |

---

## Form Contracts

### OnboardingForm (candidate submission)

| Field                     | Type     | HTML Input       | Validation                                 | Error Message                     |
| ------------------------- | -------- | ---------------- | ------------------------------------------ | --------------------------------- |
| fullName                  | string   | `text`           | Required                                   | "Full name is required"           |
| birthDate                 | date     | `date`           | Required, age >= 18                        | "Must be 18 or older"             |
| cityState                 | string   | `text`           | Required, pattern `City/State`             | "Format: City/State"              |
| whatsapp                  | string   | `tel`            | Required                                   | "WhatsApp number is required"     |
| email                     | string   | `email`          | Required, valid email                      | "Valid email is required"         |
| educationLevel            | string   | `select`         | Required                                   | "Select education level"          |
| currentWorkStatus         | string   | `select`         | Required                                   | "Select work status"              |
| dailyPokerAvailability    | string   | `select`         | Required                                   | "Select availability"             |
| preferredTimeWindows      | string[] | `checkbox-group` | Required, min 1                            | "Select at least one time window" |
| weeklyDaysAvailability    | string   | `select`         | Required                                   | "Select days available"           |
| pokerExperienceRange      | string   | `select`         | Required                                   | "Select experience range"         |
| primaryModality           | string   | `select`         | Required                                   | "Select modality"                 |
| hasOwnComputer            | boolean  | `checkbox`       | Required                                   | —                                 |
| hasDiscordFamiliarity     | boolean  | `checkbox`       | Required                                   | —                                 |
| trackerUsage              | string   | `select`         | Required                                   | "Select tracker usage"            |
| trackerDetail             | string   | `text`           | Required when trackerUsage in {YES, OTHER} | "Describe your tracker"           |
| nickPokerStars            | string   | `text`           | Optional                                   | —                                 |
| nickGGPoker               | string   | `text`           | Optional                                   | —                                 |
| nickSuprema               | string   | `text`           | Optional                                   | —                                 |
| lgpdConsentAccepted       | boolean  | `checkbox`       | Must be true                               | "LGPD consent is required"        |
| acceptedRegulationVersion | string   | hidden           | Set from flow response                     | —                                 |

**Error Code → UI Message Mapping:**

| API Error Code        | HTTP Status | UI Message                              |
| --------------------- | ----------- | --------------------------------------- |
| `DUPLICATE_CANDIDATE` | 409         | "An application with this info exists." |
| (validation)          | 400         | Show field-level errors                 |

### ReviewForm

| Field              | Type   | HTML Input | Validation        | Error Message |
| ------------------ | ------ | ---------- | ----------------- | ------------- |
| decision           | string | `button`   | APPROVE or REJECT | —             |
| reviewDecisionNote | string | `textarea` | Optional          | —             |

---

## State-to-UI Mapping

| Candidate Status | Badge Variant | Color             | Label        |
| ---------------- | ------------- | ----------------- | ------------ |
| SUBMITTED        | `outline`     | `text-blue-500`   | Submitted    |
| UNDER_REVIEW     | `outline`     | `text-yellow-500` | Under Review |
| APPROVED         | `default`     | `text-green-500`  | Approved     |
| REJECTED         | `destructive` | —                 | Rejected     |

---

## Accessibility Requirements

| Component            | Requirement                                                |
| -------------------- | ---------------------------------------------------------- |
| OnboardingFlow       | Step indicator with `aria-current="step"`, back/next focus |
| CandidateTable       | `role="table"`, row click announces selection              |
| ReviewForm           | Confirmation before destructive action (Reject)            |
| CandidateStatusBadge | `aria-label` includes full status text                     |
