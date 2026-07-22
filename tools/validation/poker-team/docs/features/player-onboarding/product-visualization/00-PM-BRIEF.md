# Player Onboarding PM Brief

## What this module is

Player Onboarding is the recruitment intake gate for new candidates.

It ensures that every submitted candidate record is:
- compliant (rules acceptance and LGPD consent),
- complete enough for screening,
- reviewable by authorized operations,
- reliable for downstream player-management handoff.

## Why this matters for product

This module protects three outcomes at the same time:
1. Candidate experience quality.
2. Compliance and governance safety.
3. Operational throughput from intake to decision.

## Capability overview (product view)

| Capability | Product outcome |
| --- | --- |
| CAP-01 Compose Guided Onboarding Flow | Candidate can start and understand onboarding clearly |
| CAP-02 Enforce Compliance Gate | Submission cannot bypass legal/policy prerequisites |
| CAP-03 Capture Qualified Application | Operations receives clean and deduplicated submissions |
| CAP-04 Execute Controlled Review | Decisions are authorized, auditable, and deterministic |
| CAP-05 Handoff Approved Intake | Approved candidates move forward with reliable payload |
| CAP-06 Observe Funnel Health | Team can optimize using measurable funnel signals |

## Shared rule authority (canonical)

This pack uses canonical rule references from the feature spec.

Critical shared references:
- CandidateOnboardingFlow.I1
- SubmitCandidateApplication.R1
- SubmitCandidateApplication.R2
- SubmitCandidateApplication.R5
- ReviewCandidateApplication.R1
- ReviewCandidateApplication.P6
- CandidateApplicationLifecycle.I1
- CandidateApplicationLifecycle.I2
- CandidateApplicationLifecycle.I3

## Product KPIs to watch weekly

| KPI | Healthy signal | Risk signal |
| --- | --- | --- |
| Submission volume | Stable or growing qualified submissions | Sudden drop |
| SubmitCandidateApplication.R1 and SubmitCandidateApplication.R2 violations | Below 5% each | Rising trend indicates gate/UX weakness |
| Duplicate block ratio (SubmitCandidateApplication.R5) | Stable baseline | Spikes indicate abuse or poor messaging |
| Time to review | p50 < 24h, p95 < 72h | Growing backlog |
| Approved handoff completeness | 100% complete payload | Any missing field blocks downstream flow |

## PM decisions to confirm before release

1. Compliance language sign-off (rules acceptance and LGPD wording).
2. Funnel thresholds for alerting and escalation.
3. Review queue operating target (staffing/SLA).
4. Release gate policy when critical invariants fail.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Compliance gate bypass | Fail closed and block release |
| Duplicate abuse | Enforce canonical duplicate checks before persistence |
| Review bottlenecks | Monitor latency and adjust staffing/process |
| Observability blind spots | Keep telemetry coverage aligned with declared contracts |

## Where to read next

- Holistic module view: [01-EPIC-POINT-OF-VIEW.md](01-EPIC-POINT-OF-VIEW.md)
- Capability atlas: [02-CAPABILITY-MAP.md](02-CAPABILITY-MAP.md)
- Rule authority index: [03-RULES-PLAYBOOK.md](03-RULES-PLAYBOOK.md)
