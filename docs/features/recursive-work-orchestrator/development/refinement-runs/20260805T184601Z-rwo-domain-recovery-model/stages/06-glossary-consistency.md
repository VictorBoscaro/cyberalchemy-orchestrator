# Stage 06 Companion — Glossary Consistency

Status: `pass` with candidate-term boundary.

## Preserved Existing Meanings

| Existing term | Consistency result |
| --- | --- |
| WorkDefinition | unchanged: immutable/versioned definition identity |
| WorkRun | unchanged: one invocation; Attempts cannot change definition/graph/authority basis |
| Attempt | narrowed against transport delivery and effect attempt identities |
| BoundedRepeat | unchanged: decision work, explicit bound, exhaustion route |
| Command/Event | unchanged: request versus accepted fact; transport does not decide |
| Journal | unchanged: accepted history owner; not automatically domain truth |
| OrchestrationCursor | unchanged: rebuildable routing projection |
| ExecutorAdapter | unchanged: provider/effect boundary outside kernel |
| AuthorityReference | unchanged: evidence reference, not policy ownership |
| replay | unchanged: deterministic historical reconstruction, zero current authority/effect refresh |
| revalidation | clarified: new WorkRun over current sources and fresh receipts |

## Candidate Terms

The new recovery terms are local to this run and are not canonical definitions
or ontology promotions. Their exact candidate meanings live in
`06-invoke-design.md`.

## Resolved Vocabulary Collisions

- “retry” is not used as a generic umbrella disposition. Use the exact
  treatment name: redelivery, new Attempt, new round, new WorkRun,
  resume/replay, reconciliation, compensation, quarantine, stop, or escalation.
- `delivery_attempt_id`, Work `attempt_id`, and `effect_attempt_id` are distinct.
- ARE “reasoning” does not include RWO route selection.
- A terminal Work event does not mean business success.

## Remaining Governance

Definitions Governance owns any later canonical vocabulary. Ontology Vault
owns graph promotion. This report authorizes neither.

