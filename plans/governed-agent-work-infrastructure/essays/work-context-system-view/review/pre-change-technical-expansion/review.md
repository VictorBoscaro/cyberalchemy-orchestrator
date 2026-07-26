# Pre-change review: redundancy and technical expansion

Status: verified with objections  
Target: `../../essay.md`  
Frozen target SHA-256: `1317A1D820F59ADA362A838FEF2052E4224A3D1002114EEFE9B5E31847DF98E4`

## Method

Three reviewers inspected the frozen essay independently:

- Forrester: reader progression, system dynamics, and repeated explanatory payload.
- Nonaka: knowledge lineage, provenance, acceptance, history, and projections.
- Liskov: contract integrity, reference ownership, path witnesses, and system-view altitude.

The parent synthesized ten candidate findings. Parnas then checked the complete frozen corpus and applied a drop-on-refutation rule: an inaccurate quotation, unsupported severity, false redundancy claim, or boundary-erasing fix removes the candidate rather than weakening it.

## Recommendation

Keep the essay as one file and keep all 38 numbered sections. No reviewer found a section that is wholly redundant, and the verifier found no evidence supporting wholesale removal.

Before adding more technical detail:

1. repair the dangling companion-owner reference;
2. preserve the five-path conceptual slice, but move exact runtime and failure-contract vocabulary behind an explicit repository-correspondence boundary;
3. make causal acceptance inspectable in the first-slice test;
4. describe both runtime-managed and legacy-ledger authority correspondence.

Four additional editorial changes have strong reviewer support but did not pass the strict evidence gate in their submitted forms: bring the five paths forward, add a reading map, bound the philosophical opening, and redraw the graph/history/projection diagram. They should be reconsidered alongside the separately verified technical-detail research, not represented as findings verified by this dispatch.

## Verified findings

### V-01 — Major: the delegated companion owner is unreachable

The front matter declares:

> `companion_to: docs/architecture/agent-language-system-view.md`

The same missing target is linked in the opening and named again in the result table. The available companion is `../agent-language-system-view/essay.md`. Because the essay says it does not create a second canonical owner, the ownership target must be inspectable.

Recommendation: either create the declared canonical artifact or point all references to the existing essay and state whether it is canonical, a predecessor, or a proposal-only peer.

### V-02 — Major: accepted causal bindings lack an acceptance witness in the first slice

Section 20 says:

> Only an accepted causal binding can attribute that change to a particular Attempt or EffectIntent.

Section 35 requires accepted producer or causation facts, but the fixture contract does not require the accepting process or occurrence to be inspectable. A label such as “accepted” could therefore pass without showing who or what accepted it, under which applicable scope or version, and against which evidence.

Recommendation: require the first-slice fixture to expose the assertion source, acceptance occurrence or process, applicable scope/version, and resolvable evidence reference. Leave the acceptance policy and sufficiency verdict open.

### V-03 — Major: exact first-slice contracts exceed system-view altitude

The conceptual five-path slice belongs in this essay. Exact relation vocabulary and the mandated `missing-terminal-binding` result do not: the selected system-view contract defers schemas, record fields, enums, failure codes, runtime mechanics, and load-bearing engineer-view verdicts.

Recommendation: retain conceptual path labels and falsifiable questions. Mark exact relation names, result vocabulary, fixtures, and normative runtime behavior as non-canonical repository correspondence or defer them to engineer-view, specification, and experiment owners.

### V-04 — Minor: authority correspondence covers only one supported variant

The current ACI/APT paragraph describes runtime-managed authority through ACI-owned `ConfirmedDispatch` and APT's corresponding authority snapshot. The frozen specifications also support legacy-managed dispatch and a `legacy_ledger` external-owner variant.

Recommendation: isolate the material under `Current repository correspondence for the first slice` and describe both variants without making either the general architecture.

## Refuted candidates

The verifier dropped these candidates:

| Candidate | Why it was dropped |
|---|---|
| Early five-path thesis and reading map | One synthesized quotation was not literal and `major` severity was unsupported. The change remains a navigation proposal. |
| Perception boundary sentence | The cited opening does not itself assign perception modelling to the infrastructure. The sentence remains an editorial clarification. |
| Compress section 17 | The synthesized quotation was not literal, and sections 2 and 17 carry distinct decomposition and recursive-work consequences. |
| Redraw section 29 | The conceptual concern was supported, but the submitted compressed diagram quotation was not literal. It may return only through separately evidenced work. |
| Durable home for rejection and supersession | The essay already preserves rejection as an occurrence and intentionally defers storage topology. |
| Downgrade completion status | The front matter remains `draft`, and “complete as a companion essay” already discloses missing downstream owners. |

## Redundancy inventory

`KEEP` means the section adds a distinct problem, property, responsibility, decision, or validation consequence. Local edits listed in the note do not imply removal of the section.

| Section | Verdict | Distinct contribution or local note |
|---:|---|---|
| 1 | KEEP | Situated and revisable origin of objectives. Optional perception-boundary sentence. |
| 2 | KEEP | Decomposition of intention and loss of global visibility. |
| 3 | KEEP | Central problem and insufficiency of adjacent tool categories. Best navigation insertion point. |
| 4 | KEEP | Upward purpose and authority inspection. |
| 5 | KEEP | Downward realization inspection. |
| 6 | KEEP | Simultaneous, non-hierarchical contexts. |
| 7 | KEEP | Context through meaningful relational composition. |
| 8 | KEEP | Stable identity versus mutable description. |
| 9 | KEEP | Non-interchangeable relation semantics. |
| 10 | KEEP | Progressive commitment without premature closure. |
| 11 | KEEP | Attribution, evidence, contextual acceptance, and responsibility. |
| 12 | KEEP | Reconstructable accepted change through time. |
| 13 | KEEP | Decisions, acceptance, and rejection as attributable occurrences. |
| 14 | KEEP | Separation of description, acceptance, execution authority, execution, and verification. |
| 15 | KEEP | Authority at workflow, dispatch, attempt, and effect levels. |
| 16 | KEEP | Multidimensional scope containment and ambiguity. |
| 17 | KEEP | Recursive work-kind grammar, reopening, bypass, and historical reconstruction; not redundant with section 2. |
| 18 | KEEP | Lineage-preserving bounded assignment. |
| 19 | KEEP | Execution-specific context selection and its trade-offs. |
| 20 | KEEP | Logical work, assignment, attempt, result, effect, artifact, and causal binding. |
| 21 | KEEP | Evidence-state ladder and non-implication between activity and progress. |
| 22 | KEEP | Objective-realization evidence beyond containment. |
| 23 | KEEP | Honest representation of missing grounding. |
| 24 | KEEP | Contextual drift. |
| 25 | KEEP | Detection mechanisms without semantic authority. |
| 26 | KEEP | Task-specific, non-authoritative projections. |
| 27 | KEEP | Candidate responsibility map. |
| 28 | KEEP | Explicit ontology ownership and term deferral. |
| 29 | KEEP / REDRAW CANDIDATE | Necessary synthesis; graph-family and derivation direction require separate evidence before editing. |
| 30 | KEEP | Witnessed composition and non-composable paths. |
| 31 | KEEP | Proposal-qualified desired preservation properties. Exact verdicts remain downstream. |
| 32 | KEEP | Trusted-boundary topology as an open decision. |
| 33 | KEEP | Different warrants supplied by formal and empirical methods. |
| 34 | KEEP | Gate against premature category-theoretic claims. |
| 35 | KEEP / BOUNDARY EDIT | Five-path vertical slice; separate conceptual obligations from exact repository contracts. |
| 36 | KEEP / BOUNDARY EDIT | Falsifiability and measurement shape; exact fixtures, vocabulary, and thresholds belong downstream. |
| 37 | KEEP | Broad unresolved research questions. |
| 38 | KEEP | Load-bearing decisions, ownership gaps, evidence boundaries, and deferrals. |
| Result block | KEEP | Artifact status and exit-state metadata. |

## Verifier statement

`OBJECTION`: only V-01 through V-04 survived the strict candidate gate. The other proposals must not be described as verified findings from this run.
