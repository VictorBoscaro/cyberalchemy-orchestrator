---
node_type: agent-dialogue
status: synthesized
date: 2026-08-25
topic: relational-metaschema-research-design
---

# Robot-Talks — relational metaschema research design

## Scope and central question

Improve the Schema Service research framing before investigating
`domainspec-lean-formalization` and the primary literature on multilevel metamodeling.

Which parts of the proposed relational tower — objects typed by schemas, schema definitions typed
by metaschemas, relative schema/instance roles, and possible kernel or self-hosted closure — are
sound enough to become research context, and which must remain questions or challenged hypotheses?

## Assumptions challenged

- `x conformsTo S0 conformsTo S1` is a uniform or transitive architectural relation.
- Relative schema/instance roles eliminate governed record kinds.
- One population and one schema per level fits an open-world system.
- Metaschema conformance establishes semantic adequacy or normative authority.
- Kernel termination and structural self-hosting exhaust the closure architectures.
- Craft epistemic types should displace the accepted `skill`-first experiment.
- Multilevel-modeling vocabulary transfers directly into Schema Service.

## Chosen and rejected decompositions

The chosen decomposition used three independent concerns: formal soundness, operational
architecture, and evidence/literature framing. The rejected decomposition assigned one agent per
source corpus; it would optimize collection but make every agent mix formal, operational, and
epistemic judgment, weakening the tension test.

## Agent prompts and outputs

1. Formal soundness tested satisfaction, reference, validation, transitivity, identity of `S0`,
   global levels, regress closure, and self-hosting. Output:
   [`reports/01-formal-soundness.md`](reports/01-formal-soundness.md).
2. Operational architecture mapped the proposal to the current Schema Service roles, authority
   boundaries, and the `skill`-first witness. Output:
   [`reports/02-operational-architecture.md`](reports/02-operational-architecture.md).
3. Evidence framing audited what belongs in initial definitions and which literature claims need
   primary-source verification or competing models. Output:
   [`reports/03-evidence-framing.md`](reports/03-evidence-framing.md).

All three agents worked independently and wrote only their assigned report. No web research or
implementation occurred during exploration.

## Synthesis

The reports converge that relative roles are a useful hypothesis but do not erase absolute record
kinds, that `conformsTo` currently collapses several non-equivalent relations, and that the linear
tower is at most an illustrative path through an open graph. They also independently identify the
README's bootstrap-root wording as stronger than the current evidence and reject treating
multilevel-modeling terminology as already applicable.

The resulting tensions and dispositions are recorded in [`findings.md`](findings.md).

## Human gate

The repository owner explicitly authorized Robot-Talks, subsequent research, and final review to
proceed without additional confirmation. The parent therefore applied conservative provisional
dispositions: actionable tensions change only the research framing; they do not yet mutate the
Schema Service contract. Unsupported claims remain open research questions.

## Follow-up

- Revised research context:
  [`../../research-initial-definitions.md`](../../research-initial-definitions.md).
- Research and final review will be linked after completion.
