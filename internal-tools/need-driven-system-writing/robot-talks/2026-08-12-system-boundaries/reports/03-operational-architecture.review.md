# Review — Operational Architecture

## Finding 1 — AMEND

The sources support separating a revisable conceptual model from an operational composition
procedure. The essay explicitly labels its categories and evaluation flow as unvalidated proposals
(`vault/essays/evaluating-text-as-composition.md:14-17, 323-327`), while the skill turns reader,
purpose, boundary, and claim status into drafting inputs
(`.codex/skills/write-need-driven-documents/SKILL.md:17-29`). They do not establish that **author
profile**, **document brief**, **observed-use residue**, and **explicit promotion** must each be a
separate compartment, nor that the proposed seven-part chain is the smallest coherent
architecture. Indeed, the report's own Gaps section says no profile artifact or contract exists.

**Amended claim:** At minimum, the architecture should keep the revisable conceptual model
distinct from the operational composition procedure so that a draft theory does not become an
implicit runtime rule. Author profiles, document briefs, use residue, and promotion mechanisms are
candidate boundaries whose necessity and contracts still require evidence.

## Finding 2 — ACCEPT

The ownership claim is directly supported. The composition skill says it governs editorial
composition while artifact-specific skills retain their formal contracts
(`.codex/skills/write-need-driven-documents/SKILL.md:14-15`). `system-view` gives a concrete example:
it owns narrative shape and stance naming, while deferring definitions, verdicts, schemas, and
mechanics (`.agents/skills/system-view/SKILL.md:29-40, 63-79`). Requiring a specialization to add a
distinct form, contract, field set, or gate is a defensible anti-duplication rule, not a demand that
every candidate specialization be built.

## Finding 3 — AMEND

The sources justify schemas at explicit handoffs: Whisper names state owners, consumers, and gates
(`.agents/skills/whisper/SKILL.md:57-82`), and Interrogation defines a mode extension contract
(`.agents/skills/interrogation/SKILL.md:62-74`). The essay also says criteria vary by document and
must not become mechanical or form completion
(`vault/essays/evaluating-text-as-composition.md:204-223, 260-271`). However, the evidence does not
show that exactly three contracts — profile, brief/transport, and review findings — are the minimum.
The profile artifact is not yet defined, and Whisper's transport schema is specific to its own
composition lifecycle rather than proof of a universal document brief.

**Amended claim:** Schemas are justified where a handoff needs explicit ownership, inputs,
consumers, gates, or traceability. Their number and fields should follow observed handoffs rather
than a predetermined component list. Context-specific editorial judgment should remain
evidence-bearing judgment, not be represented as completion of a universal quality schema.

## Finding 4 — ACCEPT

The distinction is explicit and useful. The writing skill includes an authorial composition check
before delivery (`.codex/skills/write-need-driven-documents/SKILL.md:168-202`). The review skill owns
a different act: red-teaming an existing artifact, remaining read-only over the target, and
producing verified change requests supported by literal evidence
(`.agents/skills/review/SKILL.md:8-13, 125-145`). Shared vocabulary does not require shared action or
authority.

## Finding 5 — AMEND

Whisper explicitly distinguishes learning residue from canonical voice or transport rules and
defers durable promotion to an owner (`.agents/skills/whisper/SKILL.md:80-84, 105-114`). The vault
conventions distinguish validation from promotion and require review or real-world evidence for
higher maturity (`vault/ontology-conventions.md:315-319, 429-445`). This supports a noncanonical
residue boundary. It does not establish the owners of a personal profile, shared principle, or
writing skill, so the report cannot yet assign promotion authority to those owners.

**Amended claim:** Observations from use may be retained as noncanonical residue, but they should
not alter durable rules or preferences without an explicit promotion decision by a designated
owner. The ownership and promotion contracts for profiles, principles, and skills remain open.

## Gaps or Inconsistencies Review

- **Personal profile — confirmed.** No bounded source defines a durable, person-owned writing
  profile, its location, minimum fields, amendment authority, or lifecycle. Whisper's resonance,
  relevance, and trajectory fields are owned as run state
  (`.agents/skills/whisper/SKILL.md:57-66, 116-126`).
- **Precedence — confirmed.** None of the cited contracts decides conflicts among evidence,
  shared principles, personal preferences, and document/transport requirements. This is a
  load-bearing omission if profiles become operative.
- **Generated-source reachability — amend.** The declared repository-relative canonical paths
  `spells/whisper/README.md` and `arcana/structured-interview-kits/SKILL.md` do not exist in this
  checkout, as a direct path check confirms. This establishes a repo-local maintenance and
  navigation gap. It does not prove that the canonical sources are unreachable in the generating
  system or another repository.
- **Internal-tool navigation — amend.** The README does point to the `.agents` writing skill as a
  comparison target (`internal-tools/need-driven-system-writing/README.md:49-53`), so saying it has
  no navigation is too broad. It does not link the draft composition essay, identify current
  canonical ownership, or define a promotion path; that narrower gap survives.
- **Research ownership — confirmed.** The essay lists testable questions
  (`vault/essays/evaluating-text-as-composition.md:307-327`) but assigns no intake format,
  experiment owner, evidence gate, or promotion decision.

## Local Tensions Review

- **Whisper overlap — confirmed.** Whisper claims intake, planning, drafting, validation, review,
  and learning (`.agents/skills/whisper/SKILL.md:21-25, 68-84, 105-114`). That is a coherent
  end-to-end workflow, but its relationship to the general composition, interrogation, and review
  contracts is not explicit enough to rule out double ownership.
- **Self-check versus independent review — amend.** The semantic boundary can be inferred:
  `write-need-driven-documents` performs a before-delivery self-check, whereas `review` attacks an
  existing artifact and produces verified change requests. The unresolved tension is operational
  naming and routing: both use “review,” but no routing contract says which action a request should
  invoke.
- **Provisional theory versus fixed table — confirmed.** The skill embeds a stable-looking
  dimension inventory (`.codex/skills/write-need-driven-documents/SKILL.md:168-188`) while the essay
  explicitly describes that inventory as a proposal to test
  (`vault/essays/evaluating-text-as-composition.md:309-327`). Treating the table as settled doctrine
  would exceed the evidence.
- **Operational non-redundancy versus statistical independence — confirmed.** The vault requires
  zero mutual information (`vault/ontology-conventions.md:24-45, 323-340`) while acknowledging that
  `node_type` predicts `nature` (`vault/ontology-conventions.md:197-201`). The removable-information
  test at lines 342-350 remains useful; statistical independence has not been demonstrated.

## Questions for Synthesis Review

All five questions expose unresolved ownership or promotion decisions and are eligible for
synthesis. Two should carry explicit cautions:

- The question about a composition core must not assume that a new extracted skill is necessary;
  it should allow the answer that `write-need-driven-documents` remains the bounded specialization
  and no general core is built yet.
- The Whisper question should distinguish ownership of an end-to-end workflow from ownership of
  the semantic contracts it composes. A workflow may coordinate a capability without becoming its
  canonical definition.

The precedence, author-confirmation, and research-promotion questions follow directly from the
confirmed gaps and do not presuppose a component implementation.

## Eligible for synthesis

1. **Amended Finding 1:** At minimum, keep the revisable conceptual model distinct from the
   operational composition procedure. Treat profiles, briefs, use residue, and promotion as
   candidate boundaries pending evidence and explicit contracts.
2. **Accepted Finding 2:** Create a specialization only at a distinct contract boundary; it must
   add a form, required fields, or gate the composition core does not own rather than duplicate
   general prose guidance.
3. **Amended Finding 3:** Use schemas at observed handoffs that require explicit ownership,
   inputs, consumers, gates, or traceability. Do not predetermine the number of schemas or encode
   contextual editorial judgment as a universal quality form.
4. **Accepted Finding 4:** Let writing and independent review share vocabulary while remaining
   distinct actions and authorities: authorial self-check before delivery versus read-only,
   evidence-bearing red-team review of an existing artifact.
5. **Amended Finding 5:** Preserve observed-use lessons as noncanonical residue until an explicit
   promotion decision by a designated owner; profile, principle, and skill promotion ownership is
   still undefined.
