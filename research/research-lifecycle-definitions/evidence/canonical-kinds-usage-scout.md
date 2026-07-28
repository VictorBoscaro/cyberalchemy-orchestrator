---
tags: [research, evidence, canonical-kinds, lifecycle]
artifact_kind: research-evidence
status: draft
---

# Canonical-kinds usage scout

## Sources inspected

- Frozen local context: `research/research-lifecycle-definitions/research-initial-definitions.md:45-108` and `vault/ontology-conventions.md:1-35,391-408`.
- Frozen sibling corpus: `../domainspec-core/sessions/2026-07-13-2225-canonical-kinds-evidence-edges.md:1-106`; `../domainspec-core/cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md:120-170,296-362,457-505`; `../domainspec-core/cyberAlchemy-v2/ontology/canonical-kinds/EDGES.yaml:1-183`; and `../domainspec-core/cyberAlchemy-v2/ontology/reviews/2026-07-13-authority-vs-canonical-kinds/findings.md:1-165,169-240` and `attacks.md:24-344`.

## Observed generation and lifecycle

### Direct source facts

- The evidence-edge session records that it changed `CANONICAL-KINDS.md`, `ALLOWED-EDGES.yaml`, and `EDGES.yaml`; it describes decisions on the Evidence instance contract and four evidence relations. [`../domainspec-core/sessions/2026-07-13-2225-canonical-kinds-evidence-edges.md:14-17,24-38`]
- The declared research flow is a spiral: a research may derive from a discovery, findings may derive from research, and a later discovery may derive from research; at the instance level the stated normal flow is `D1 → R1 → F1 → D2`. [`../domainspec-core/cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md:307-314,347-351`]
- A cold research is expressly permitted: its motivating `question` is a field rather than a node, so it has no required incoming relation. Findings-to-research is likewise optional for an `n=1` research dispatch that emits no `research.md`. [`../domainspec-core/cyberAlchemy-v2/ontology/canonical-kinds/EDGES.yaml:72-95`]
- A session is allowed to claim only `creates` and `updates`; provenance is intentionally partial because a session file exists only when `close-session` ran, and absence of `creates` proves nothing. [`../domainspec-core/cyberAlchemy-v2/ontology/canonical-kinds/EDGES.yaml:4-15,48-66`]
- The session source itself reports unresolved lifecycle defects: no edge is mandatory; instance acyclicity is not enforced; and the research-to-discovery edge cannot identify which open question it answers. [`../domainspec-core/sessions/2026-07-13-2225-canonical-kinds-evidence-edges.md:66-76,85-89`; `../domainspec-core/cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md:316,350-362`]

### Interpretation

The demonstrated lifecycle vocabulary is useful as an optional provenance-and-grounding pattern, but it is not evidence for a universal requirement that every research artifact have a parent, an output edge, or complete session provenance. The frozen corpus explicitly admits all three absences. [`../domainspec-core/cyberAlchemy-v2/ontology/canonical-kinds/EDGES.yaml:54-57,74-86,88-95`; `../domainspec-core/cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md:316,334-337`]

## Observed discovery/research nodes

### Direct source facts

- The sibling instance contract is candidate-only and limited to four Evidence kinds: `discovery`, `research`, `findings`, and `session`; it expressly defers every other kind. [`../domainspec-core/cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md:120-124`]
- In that contract, one file is one artifact for the four kinds in scope. `research.md`, `discovery.md`, and `findings.md` carry their kind through filename; a session instead uses the `sessions/` path and a frontmatter mirror. [`../domainspec-core/cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md:128-153`]
- The same source says research and findings share a question; research is the aggregate and findings supplies the outcome, so research may correctly lack an outcome. [`../domainspec-core/cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md:163-166,219-222`]
- The sibling session records an earlier, incompatible result: `canonical_kind` “left the frontmatter entirely and became the filename.” It also says its evidence schema is safe to build on but its kind table is not. [`../domainspec-core/sessions/2026-07-13-2225-canonical-kinds-evidence-edges.md:24-38,91-99`]
- The authority review further reports that no file carries `canonical_kind`, the admission validator is not implemented, and the canonical branch has zero instances; it therefore characterizes the tables as unused by current artifacts. [`../domainspec-core/cyberAlchemy-v2/ontology/reviews/2026-07-13-authority-vs-canonical-kinds/findings.md:144-153`]
- Locally, the fixed constraint is one kind concept named `artifact_kind`, while the current corpus has inconsistent research frontmatter and connections; existing values outside the local catalog are evidence only of an unsettled contract. [`research/research-lifecycle-definitions/research-initial-definitions.md:50-52,67-76,84-100`]

### Interpretation

The reusable lesson is the lifecycle distinction—initial framing, collected research, synthesized findings—not the sibling filename/path carrier rule or its `canonical_kind` spelling. Those rules depend on a specific document layout, contradict another record in the same frozen corpus, and lack demonstrated deployed instances. Reusing them would import an unverified identity model rather than observed interoperability. [`../domainspec-core/cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md:128-153`; `../domainspec-core/sessions/2026-07-13-2225-canonical-kinds-evidence-edges.md:24-38`; `../domainspec-core/cyberAlchemy-v2/ontology/reviews/2026-07-13-authority-vs-canonical-kinds/findings.md:144-147`]

## Observed edges and evidence

### Direct source facts

- The declared allowed evidence edges are `research → discovery`, `discovery → research`, `findings → research` via `derives-from`, `discovery ↔ discovery` via `contradicts`, and `session → Evidence artifact` via `creates` or `updates`. [`../domainspec-core/cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md:307-314`]
- `contradicts` is explicitly a real but non-compositional conflict edge; sessions cannot originate it because it is a claim, not an act. [`../domainspec-core/cyberAlchemy-v2/ontology/canonical-kinds/EDGES.yaml:30-46`]
- The type graph is allowed to cycle, but the instance grounding graph is required to be acyclic and has no enforcement mechanism. [`../domainspec-core/cyberAlchemy-v2/ontology/canonical-kinds/EDGES.yaml:171-183`]
- The source marks `discovery → findings` forbidden but “UNEXAMINED,” and marks discovery-to-discovery derivation and `alternative-to` unruled because no repository instance forced either vocabulary item. [`../domainspec-core/cyberAlchemy-v2/ontology/canonical-kinds/EDGES.yaml:131-163`]

### Interpretation

The vocabulary is insufficient as a complete account of the observed research case: it cannot attach research to a particular discovery question, does not require findings to cite their aggregate, and deliberately leaves ordinary alternatives unmodeled pending a witness. It is better reused as a tested set of candidate meanings and typed negatives than as a closed local edge catalog. [`../domainspec-core/cyberAlchemy-v2/ontology/canonical-kinds/EDGES.yaml:82-86,131-163`; `../domainspec-core/cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md:316,360-362`]

## Declared-versus-used gaps

### Direct source facts

- The authority review verified that three quotations circulated by attackers were absent, and that `CANONICAL-KINDS.md` changed during the review session; it directs future readers to treat the resulting convergence as not independent confirmation. [`../domainspec-core/cyberAlchemy-v2/ontology/reviews/2026-07-13-authority-vs-canonical-kinds/findings.md:16-49,238-240`]
- The review found the candidate admission schema accepts `canonical_kind` and `authority_kind` as unconstrained strings, with no enum enforcement; it describes neither enumeration as machine-enforced. [`../domainspec-core/cyberAlchemy-v2/ontology/reviews/2026-07-13-authority-vs-canonical-kinds/findings.md:92-98`]
- The canonical-kinds document admits six kinds without a real producer and concludes that a declared producing process was never the membership test for canonicity. [`../domainspec-core/cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md:457-486`]
- The authority review identifies live routing drift, missing definitions of both head terms, and an unresolved ownership route for type changes. [`../domainspec-core/cyberAlchemy-v2/ontology/reviews/2026-07-13-authority-vs-canonical-kinds/findings.md:62-67,84-98,219-237`]

### Interpretation

The corpus demonstrates a design-and-review history, not effective admission control. In particular, it cannot support importing a claim that kinds are closed, derived, owner-governed, or process-born. The local constraint that each registered artifact have an identifiable generation process is a local product constraint, not a sibling behavior that has been shown to work across kinds. [`research/research-lifecycle-definitions/research-initial-definitions.md:45-54`; `../domainspec-core/cyberAlchemy-v2/ontology/reviews/2026-07-13-authority-vs-canonical-kinds/findings.md:92-98,144-147`; `../domainspec-core/cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md:462-476`]

## Reusable versus hidden assumptions

| Reuse candidate | Evidence-backed use | Hidden assumption to avoid |
|---|---|---|
| Separate work acts from artifact claims | Sessions creating/updating artifacts while artifacts carry grounding/conflict claims prevents an activity record from asserting truth. [`../domainspec-core/cyberAlchemy-v2/ontology/canonical-kinds/EDGES.yaml:4-15,30-40,48-66`] | That every artifact has a session witness; the source says provenance is partial. [`../domainspec-core/cyberAlchemy-v2/ontology/canonical-kinds/EDGES.yaml:53-57`] |
| Keep research aggregate distinct from findings synthesis | The declared findings-to-research edge captures a concrete aggregate/synthesis relationship. [`../domainspec-core/cyberAlchemy-v2/ontology/canonical-kinds/EDGES.yaml:88-95`] | That it is always present; `n=1` dispatches are an explicit countercase. [`../domainspec-core/cyberAlchemy-v2/ontology/canonical-kinds/EDGES.yaml:91-95`] |
| Make constraints progressively checkable | The corpus identifies an acyclicity invariant and states it needs a check. [`../domainspec-core/cyberAlchemy-v2/ontology/canonical-kinds/EDGES.yaml:171-183`] | That a declared constraint is already enforced or that a fixed vocabulary alone supplies the check. [`../domainspec-core/cyberAlchemy-v2/ontology/reviews/2026-07-13-authority-vs-canonical-kinds/findings.md:92-98`] |
| Preserve conflict as an edge when a concrete incompatibility exists | `contradicts` is explicitly retained as a non-morphism rather than erased. [`../domainspec-core/cyberAlchemy-v2/ontology/canonical-kinds/EDGES.yaml:30-46`] | That every useful relation must compose, or that missing vocabulary is evidence it should be invented; `alternative-to` remains unwitnessed. [`../domainspec-core/cyberAlchemy-v2/ontology/canonical-kinds/EDGES.yaml:157-164`] |

## Contradictions and gaps

- The frozen sibling sources disagree over whether `canonical_kind` is mirrored in frontmatter or removed from it; the review also documents source mutation and fabricated quotations during deliberation. This makes the sibling corpus unsuitable as an unqualified canonical schema source. [`../domainspec-core/cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md:132-153`; `../domainspec-core/sessions/2026-07-13-2225-canonical-kinds-evidence-edges.md:24-31`; `../domainspec-core/cyberAlchemy-v2/ontology/reviews/2026-07-13-authority-vs-canonical-kinds/findings.md:16-49`]
- The local baseline still uses `node_type` and a fourteen-value Connections catalog, whereas the local research constraint fixes `artifact_kind` as the single kind field and says edge representation/direction remain unsettled. No compatibility mapping is evidenced here. [`vault/ontology-conventions.md:1-9,391-408`; `research/research-lifecycle-definitions/research-initial-definitions.md:50-52,67-68,92-100`]
- Blocker: the frozen material contains no demonstrated end-to-end enforcement that validates artifact frontmatter, endpoint compatibility, generation provenance, or lifecycle transition for actual discovery/research/findings instances. The next decision needs local witnesses and a stated validation owner before treating any proposed envelope or edge rule as a repository invariant. [`../domainspec-core/cyberAlchemy-v2/ontology/reviews/2026-07-13-authority-vs-canonical-kinds/findings.md:92-98,144-147`; `research/research-lifecycle-definitions/research-initial-definitions.md:84-100`]

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [canonical-kinds-normative-scout.md](canonical-kinds-normative-scout.md) | `other` | Paired evidence from the normative/schema lens; the precise relation type remains intentionally unclassified. |
