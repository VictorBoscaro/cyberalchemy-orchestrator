# Repository Leverage Priority — Findings

## Verdict matrix

| Candidate | Owner/evidence | Witnessed? | Sound? | Verdict | Use mode |
|---|---|---:|---:|---|---|
| Repair and ratify Host Binding → BUS dogfood seam | Existing host-workflow and BUS runtime/tests | yes, but currently red under schema drift | yes | GO | build-from-owned |
| ACI-005 opening materializer | ACI WORK-PACK, TASK-020 and SWU manifest | contract witness exists; execution descriptor absent | yes, after readiness gaps close | GO | build-from-owned |
| Generic SkillExecutionProfile/compiler | Initial definitions only | no executable witness | unsettled | defer | future experiment |
| Prompt/request/tag/graph control plane | Invalidated research baseline | no accepted findings | unsettled | defer | regenerate research |
| General provider invocation pipeline | Multi-wave downstream program | partial prerequisites only | sound as later program | defer | downstream |

## Answer

The highest-leverage program is sequential:

1. repair and revalidate the existing Host Binding → BUS dogfood seam;
2. use the resulting stable compatibility and identity evidence to prepare and implement ACI-005.

Do not implement the two code slices in parallel because they overlap runtime, fixtures, manifests,
specification owners, and identity boundaries.

## Current readiness qualification

The dogfood slice is currently green on its focused 5-test Host Binding and 7-test BUS suites. Its
immediate next work is a closing review; repair authoring/code is conditional on a surviving FIX
finding. ACI-005 still needs a short discovery settlement, dedicated test obligations, an exact
SWU descriptor, and code-readiness evidence.

## Dispatch close

- Exit reason: `resolved`
- Research seats spawned: 3
- Accepted returns: 2
- Unavailable terminal return: 1
- Parent approval: accepted as a partial result with the limitation stated above
