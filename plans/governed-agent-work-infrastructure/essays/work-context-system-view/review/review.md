# Review - work-context system-view essay

## Recommendation

No numbered section is wholly redundant. All 38 sections add a distinct property, boundary,
responsibility, open question, or validation consequence. The essay should remain one file for
now.

The recommended revision is navigational and local rather than structural:

1. repair the broken canonical-companion reference;
2. introduce the five candidate inspection paths after section 3;
3. add an explicit reading map and stopping points;
4. bound the philosophical opening so it does not imply that the infrastructure models human
   perception;
5. redraw section 29 so accepted history, graph families, and projections are not given a false
   singular order; and
6. retain the ACI/APT correspondence under a clearly repository-specific subsection.

The proposed compression of section 17 and mergers of sections 18/19 and 37/38 were independently
refuted. Those sections are close in subject, but they do different work.

**Overall verdict: FIX.**

## Coverage

| reviewer | method or lens | corpus | findings raised | result |
|---|---|---|---:|---|
| Christopher Alexander | reader journey and information scent | entire essay | 5 | complete |
| Charles Sanders Peirce | proposition entailment and lineage/reference integrity | entire essay plus eight frozen repository owners | 5 | complete |
| Parent | independent semantic/governance review and synthesis | entire essay | 10 candidates synthesized | 6 survived independent verification |
| David Parnas | literal-artifact and reference verifier | entire essay, candidate list, and eight frozen repository owners | 10 checked | 6 confirmed, 4 refuted and dropped; final statement: no objection |

- Robot-talks was explicitly excluded by the user. The two subagent reviewers remained isolated
  through their initial returns, so there was no convergence step or premature-collapse risk.
- Every numbered section was reviewed in the full essay by both declared reviewer methods and by
  the parent. Repository ownership claims were additionally checked by Peirce and Parnas.
- During the review, the target and companion filenames changed to `essay.md`. Their SHA-256
  digests remained unchanged, and the user explicitly confirmed rebinding to the current paths.
- Zero-findings flag: not triggered. Both attackers raised supported findings.
- The verifier checked every synthesized candidate. Four refuted candidates were dropped rather
  than softened.

## Artifact - `plans/governed-agent-work-infrastructure/essays/work-context-system-view/essay.md`

| # | file | evidence quoted from the artifact | severity | proposed fix |
|---|---|---|---|---|
| 1 | `essay.md:14` | "`companion_to: docs/architecture/agent-language-system-view.md`" | MAJOR | Replace the three dangling companion references at lines 14, 25, and 900 with the actual authoritative path, or establish the declared canonical path and explicitly state which document owns the system view. |
| 2 | `essay.md:88` | "The central purpose of the proposed system" | MINOR | After section 3, add a proposal-qualified thesis: the system should preserve independently inspectable paths for purpose, authority, assignment, causation, and realization. Say that the remainder derives the properties, responsibilities, and validation strategy needed to preserve them. |
| 3 | `essay.md:19` | "This companion essay explains the shape and stakes" | MINOR | Add a compact reading map after the early thesis: sections 1-16, problem/properties/governance boundaries; 17-30, system form; 31-34, invariants/formalization; 35-36, first test; 37-38, questions/limits. Mark these as optional stopping points. |
| 4 | `essay.md:40` | "The objective does not appear in isolation. Perception is situated." | MINOR | Add a boundary sentence: the system does not need to model human perception itself; it needs to preserve the attributable transition from a situated perception to a declared and revisable objective. |
| 5 | `essay.md:637` | "Context Graph" | MAJOR | Redraw the diagram so accepted assertions, decisions, and events feed durable history and candidate purpose/authority/evidence graph views, followed by task-specific projections. Prefer "Context Graph Family," but do not imply that every graph is derived or that all members carry equal authority; those ontology decisions remain open. |
| 6 | `essay.md:812` | "Authority evidence is referenced from its current owner rather than duplicated." | MINOR | Keep the ACI/APT material, but place lines 812-822 under `### Current repository correspondence for the first slice` so the general proposal does not appear to depend essentially on current runtime names. |

**Artifact verdict: FIX.**

## Section-by-section information-value judgment

| sections | judgment | reason |
|---|---|---|
| 1 | KEEP; local boundary clarification | Situated perception explains why objectives are incomplete and revisable. It does not duplicate later provenance; it needs only an explicit scope boundary. |
| 2-3 | KEEP; insert thesis/map after 3 | Section 2 establishes decomposition and loss of global purpose. Section 3 states the problem and distinguishes it from task, document, workflow, and multi-agent systems. |
| 4-5 | KEEP separately | Section 4 tests upward justification and authority; section 5 tests downward realization. Bidirectionality is substantive. |
| 6-7 | KEEP separately | Section 6 establishes simultaneous contexts; section 7 explains context as composition across typed relationships. Plurality is not composition. |
| 8-10 | KEEP | Stable identity, relation semantics, and progressive definition impose different constraints. |
| 11-12 | KEEP separately | Provenance identifies the source and acceptance status of claims; history preserves accepted change through time. |
| 13-16 | KEEP | These progressively separate decisions, acceptance, execution authority, authority levels, and containment. |
| 17 | KEEP | Its arrow diagram resembles section 2, but its new information is a recursive work-kind grammar with reopening, bypasses, and historical reconstruction. Compression was refuted. |
| 18-19 | KEEP separately | Section 18 defines lineage-preserving bounded assignment; section 19 defines execution-specific context selection and its access/authority trade-offs. Merging was refuted. |
| 20-23 | KEEP | Attempt/effect identity, the evidence-state ladder, strategic realization evidence, and honest incompleteness are distinct. |
| 24-26 | KEEP | Drift, detection mechanisms, and historical projections describe different responsibilities. |
| 27-28 | KEEP separately | Section 27 inventories system responsibilities; section 28 defers ontology-owned concepts. Deployment boundaries are not definitions. |
| 29 | KEEP; replace diagram | The graph/history/projection synthesis is necessary, but its current diagram gives a misleading order and singularity. |
| 30-34 | KEEP | Composition rules, candidate invariants, trusted-boundary options, formal warrants, and the category-theory gate add separate constraints. |
| 35 | KEEP; isolate repository correspondence | The vertical slice unifies the five paths and makes the proposal testable. The ACI/APT paragraph is useful evidence at a different altitude. |
| 36 | KEEP | It turns the slice into falsifiable fixtures, measures, and failure conditions. |
| 37-38 | KEEP separately | Section 37 is the broad research-question inventory. Section 38 records only five load-bearing open decisions plus deferred term ownership. Merging would blur questions, decisions, and owners. |
| System-view result | KEEP | It is artifact-status metadata and an exit summary, not a substitute for the proposed opening navigation. |

## Change requests

1. **MAJOR - repair canonical ownership navigation.** Fix the absent
   `docs/architecture/agent-language-system-view.md` references or establish that path as the
   canonical owner.
2. **MAJOR - correct the section 29 model.** Replace the singular graph -> accepted facts -> history
   diagram with a projection-aware graph-family model whose authority and derivation status remain
   explicit and open where undecided.
3. **MINOR - surface the thesis early.** Add the five candidate paths after section 3 without
   claiming that their necessity or sufficiency has been decided.
4. **MINOR - add navigation.** Introduce the five reading blocks and optional stopping points.
5. **MINOR - bound the philosophical opening.** State that the system preserves the attributable
   transition to a declared objective rather than modeling perception itself.
6. **MINOR - mark repository-specific altitude.** Keep the ACI/APT correspondence under a named
   subsection within the first vertical slice.

## Dispatch close

- recorded `exit_reason`: `error` - the append-only close row was written by an earlier
  continuation after conversation interruption, before the verifier's textual return was delivered
  to the parent
- recorded `agents_spawned`: total 3 - 2 explorers and 1 skeptic; 1 review loop
- proposal-gate infrastructure used before launch: 3 helpers
- resumed completion: the parent recovered Parnas's terminal return, revalidated the current source
  paths and frozen hashes, dropped all four refuted findings, replaced the stale partial report, and
  accepted the verifier's no-objection result
- no second close row was appended; the historical close remains immutable
