# Findings — skill control center meta-orchestration

## Decision

Use **no `MiniWave` entity or identifier**. “Mini-onda” is only a user-facing label for a
non-authoritative projection derived from the real Dispatch tree. The existing
`meta: true` plus `parent_dispatch_id` relation remains the only dispatch lineage identity.

The constructive return supplied useful view-model fields, but did not produce a relation that
cannot be derived from Dispatch ancestry and declared step metadata
([operator return](research.md#skill_control_center_meta__operator_projection)). The governance
attack therefore falsified the need for a new identity
([reviewer return](research.md#skill_control_center_meta__governance_review)).

## Verdict matrix

| candidate | owner (precedent) | witnessed? | sound? | verdict | use-mode |
|---|---|---:|---:|---|---|
| `MiniWaveId` or `miniwave.v0.1` entity | existing Dispatch lineage | no irreducible relation | no; duplicates identity | KILL | typed negative: no-witness / definitional collapse |
| “mini-onda” as presentation label | Dispatch-tree projection | yes | yes, if marked derived | GO | build-from-owned |
| `root`, `depth`, `order`, aggregate status | derived read model | yes | yes, with provenance/freshness | GO | build-from-owned |
| research → review → discovery → spec → backend → frontend → validation | mixed dispatch/workflow route | yes | yes after reclassification | GO | build-from-owned |
| three original frontend variants | user requirement | conditional | conditional on contract revision and rubric | GO | novel-attempt within ratified UI contract |

## Approved route

1. `research`: LIVE research dispatch with external and repository evidence.
2. `review`: LIVE persisted review dispatch over the research artifacts.
3. `discovery`: `discovery-writing` bootstrap workflow, not a dispatch type.
4. `spec`: `domainspec-spec-feature` workflow, not a dispatch type.
5. `backend`: separate `task-session` work unit; `code` dispatch remains RESERVED.
6. `frontend`: separate `task-session` work unit producing exactly three original variants after
   the UI contract is revised.
7. `validation`: inline test/evidence work plus a LIVE review dispatch when a red-team verdict is
   needed.

## Acceptance contract carried forward

The parent is the approval authority for every stage deliverable. Agents return completed stage
artifacts or evidence summaries, not narration of their internal process.

Implementation approval requires:

- backend, contract, and frontend tests executed with zero unexplained failures;
- evidence that the test set exercises the specified behavior rather than merely passing;
- identical functional contract, fixtures, test IDs, and viewports across all frontend variants;
- screenshots for every variant at the frozen states and viewports;
- visual assessment across **clarity, usability, visual consistency, and operational efficiency**;
- keyboard navigation and accessibility checks;
- provenance tying results and screenshots to the exact source revision.

“Original” means visually distinguishable art direction without changing behavior, information
semantics, mandatory content, API, or test IDs. Existing repository variants are negative
references and must not be used as creative templates.

## Lineage limitation

The current host hook registered the two seats as independent automatic dispatches. The shared
`skill_control_center_meta__` task-name prefix is only a discoverability aid; it is not authoritative
P13 lineage. Future true child rows may use `parent_dispatch_id` only when the launcher can preserve
the confirmed dispatch envelope.

## Close

- `exit_reason`: `resolved`
- final approver: `parent`
- execution seats: 2 (`explorer`: 1, `skeptic`: 1)
- proposal-gate/scout helpers used before execution: 10
- `agents_spawned.total`: 12
- `loops_used`: 1
- approval: accepted with the `MiniWaveId` candidate killed and the presentation-only projection
  retained.
