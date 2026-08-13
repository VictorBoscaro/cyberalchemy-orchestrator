# Formalization and Automation Skepticism

## Key Findings

1. **Formalize the basis and trace of a judgment, not a universal verdict on textual quality.**
   **Evidence:** `vault/essays/evaluating-text-as-composition.md`, sections **5. Why “good
   writing” is too broad to evaluate**, **8. Criteria make a review actionable**, and **10. A
   lightweight review in practice**, separates dimension, lens, criterion, and evidence; makes
   criteria dependent on document, reader, and purpose; requires cited evidence; and explicitly
   rejects one aggregate score. **Inference:** a useful schema may preserve purpose, reader,
   selected criteria, cited passages, judgments, and dispositions. It should not produce a single
   quality score or treat field completion as proof that a text works.

2. **A schema should have a small stable core and context-specific extensions.** **Evidence:**
   `.codex/skills/write-need-driven-documents/SKILL.md`, sections **Establish the reader
   transformation** and **Review the composition**, defines reusable inputs and review dimensions;
   the same skill says its default sequence is a reasoning pattern rather than a mandatory table
   of contents. The essay's section **10. A lightweight review in practice** says to use only the
   distinctions needed for the document at hand. `internal-tools/need-driven-system-writing/README.md`,
   **Current status**, says the method is not yet a validator or finished editorial method.
   **Inference:** required fields should be limited to information needed for routing,
   provenance, and later interpretation. Document-specific criteria and profile preferences should
   be extensions, not an exhaustive form every author must complete.

3. **Automation is most defensible at mechanical boundaries; semantic adequacy still requires
   evidence-bearing human or agent judgment.** **Evidence:** `.agents/skills/interrogation/SKILL.md`,
   sections **process**, **mode-extension-contract**, and **output-contract**, gives a stable shell
   for mode selection, one-question turns, decision recording, exit criteria, and a readiness
   result. `.agents/skills/review/SKILL.md`, sections **Gate it** and **Standing rules**, requires
   literal artifact evidence, independent verification, and rejection of refuted findings.
   `vault/ontology-conventions.md`, lines 67–92, provides a concrete machine-checkable frontmatter
   contract. **Inference:** code can reliably check syntax, allowed values, missing references,
   required provenance, workflow state, and whether a review cites evidence. It cannot by those
   checks alone establish that a purpose is right, a criterion is adequate, prose is clear, or a
   reader was transformed.

4. **The evaluation model must remain a versioned hypothesis until use supplies stronger
   evidence.** **Evidence:** `vault/essays/evaluating-text-as-composition.md`, opening note,
   **12. Open questions**, and **13. Evidence boundary**, says the categories are not known to be
   complete, independent, or empirically validated; the dimensions, evaluation flow, and musical
   questions are proposals to test. The essay explicitly asks about reviewer consistency, reader
   testing, and measurable improvement. **Inference:** dimensions, lenses, and candidate shared
   principles should carry version and evidence status. Their presence in a schema or skill must
   not silently promote them from working model to universal law.

5. **Mathematical vocabulary can make a classification look more objective than its evidence
   permits.** **Evidence:** `vault/ontology-conventions.md`, lines 323–340, defines orthogonality as
   zero mutual information and says knowing one of seven labels gives no information about another;
   lines 197–201 then acknowledge that `node_type` predicts `nature` and call that correlation
   acceptable. These two claims cannot both satisfy the stated statistical definition. **Inference:**
   this writing system should use an operational non-redundancy question—whether a field changes a
   decision, route, or interpretation—unless actual observations support a statistical claim.
   Formal notation should not substitute for measured data.

## Gaps or Inconsistencies

- No source reports trials with authors, first-time readers, or multiple reviewers. There is no
  baseline for inter-reviewer agreement, document improvement, completion cost, or false-positive
  rate.
- The sources do not define the minimum profile schema, extension mechanism, migration policy, or
  what happens when a person's preference conflicts with a candidate shared principle.
- There is no explicit classification of checks into deterministic validation, heuristic warning,
  and judgment requiring evidence. Without it, a convenient heuristic may acquire blocking
  authority by accident.
- The essay rejects aggregate scoring but does not yet specify how several conflicting judgments
  are compared, prioritized, or closed.
- The repository already contains an example of a useful operational idea—non-redundancy—being
  overstated as a statistical invariant. This is direct evidence that formal language itself needs
  an evidence gate.
- No source defines a bureaucracy budget: the maximum author effort, number of required fields, or
  frequency of review that the expected improvement would justify.

## Local Tensions

- **Repeatability versus contextual judgment:** stable fields enable reuse and comparison, while
  fixed criteria can erase differences among audiences, purposes, and document forms.
- **Traceability versus writing overhead:** recording purpose, criteria, evidence, and decisions
  makes review auditable, but recording every distinction can turn composition into form
  completion.
- **Helpful linting versus gaming:** visible checks make omissions easier to catch, but authors and
  agents can optimize for passing them instead of producing the intended reader effect.
- **Personal control versus system learning:** structured profiles let people preserve preferences,
  while usage telemetry or inferred preferences can quietly make the system—not the author—the
  authority over what their style means.
- **Early standardization versus empirical learning:** a common schema makes experiments easier to
  compare, but freezing the present categories too early makes later correction expensive and
  politically harder.

## Questions for Synthesis

1. What is the smallest set of fields without which a writing or review result cannot be
   interpreted or audited later?
2. Which checks may block delivery, which may only warn, and which must always remain advisory
   judgments supported by cited evidence?
3. What evidence promotes a proposed shared principle into the common core, and what evidence can
   demote or remove it?
4. How should conflicting criteria or reviewers be preserved without collapsing them into one
   score or leaving every disagreement unresolved?
5. What author-effort budget and measured benefit would justify adding a field, interview step,
   review lens, or automated check?
6. Which data may the system infer from a person's writing, which must be explicitly confirmed,
   and what remains private or disposable?
7. What experiment should precede any code beyond schema parsing, provenance checks, and workflow
   bookkeeping?
