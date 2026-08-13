# Finding Review

## Finding 1 — AMEND

The essay supports separating dimension, lens, criterion, and evidence, making criteria contextual, citing the textual basis of judgments, avoiding form completion, and preserving uncertainty rather than forcing one aggregate score (`vault/essays/evaluating-text-as-composition.md:103-124,204-223,260-271`). It does not prove that every aggregate score is useless: whether any overall evaluation can be useful remains an open question (`vault/essays/evaluating-text-as-composition.md:307-321`). The proposed schema contents are plausible inference, not an established schema contract.

**Exact amended claim:** The current evidence supports formalizing the contextual basis and trace of a judgment—such as purpose, reader, selected criteria, cited evidence, judgment, and disposition—without treating field completion or an aggregate score as proof that a text works. The sources do not yet establish whether any carefully bounded aggregate evaluation can be useful.

## Finding 2 — AMEND

The skill supplies reusable reader-transformation inputs and review dimensions, while qualifying its sequence as a default and allowing modular forms (`.codex/skills/write-need-driven-documents/SKILL.md:17-53,168-188`). The essay says to use only distinctions needed for the document (`vault/essays/evaluating-text-as-composition.md:260-271`), and the README says the method is unfinished (`internal-tools/need-driven-system-writing/README.md:47-58`). These sources support minimizing premature mandatory structure, but they do not identify a stable core, prove that a core-plus-extensions architecture is best, or establish routing and provenance as the only legitimate required fields. A richer provisional schema could also enable comparable experiments.

**Exact amended claim:** Any initial schema should keep mandatory fields limited to common information whose interpretive or experimental value can be justified, treat the current candidate core as provisional, and allow document-specific criteria and personal preferences to vary. The sources do not yet determine the stable core or prove a particular extension architecture.

## Finding 3 — AMEND

Interrogation and Review define stable procedural and evidence contracts (`.agents/skills/interrogation/SKILL.md:39-85,99-113`; `.agents/skills/review/SKILL.md:128-152,194-201`), and the ontology defines enumerable frontmatter shapes (`vault/ontology-conventions.md:67-92`). These are examples of potentially machine-checkable predicates, not evidence that code currently checks them reliably. Syntax, enum membership, and presence of required fields can be deterministic once an explicit machine-readable contract exists; reference validity depends on a defined resolver and state; the presence of a citation does not establish that it is relevant or sufficient. The sources also permit agent judgment and verification, so “semantic” does not mean “human-only.”

**Exact amended claim:** Automation is most defensible where a machine-readable contract makes the predicate explicit—for example syntax, enum membership, required-field presence, or resolvable-reference existence under a defined state. Automation may also assist semantic review, but structural checks alone cannot establish that evidence is sufficient, a criterion is adequate, prose is clear, or a reader effect occurred; those conclusions still require an attributable, evidence-bearing judgment.

## Finding 4 — ACCEPT

The essay explicitly marks the categories as incomplete, potentially dependent, and unvalidated, identifies the inventory and flow as proposals, and asks for reviewer-consistency, reader-response, and improvement evidence (`vault/essays/evaluating-text-as-composition.md:14-17,307-327`). Its own frontmatter is versioned and `draft` (`vault/essays/evaluating-text-as-composition.md:1-9`). Keeping the model versioned and epistemically provisional follows directly and does not impede automation; it makes automated use revisable.

## Finding 5 — AMEND

The ontology defines orthogonality as zero mutual information and claims the seven labels reveal nothing about one another (`vault/ontology-conventions.md:323-340,354-382`), while explicitly acknowledging that `node_type` predicts `nature` and accepting the correlation (`vault/ontology-conventions.md:182-205`). Those claims cannot both satisfy the document’s statistical definition. This example justifies an evidence boundary between a practical non-redundancy heuristic and measured statistical independence. It does not by itself prove the investigator’s proposed decision/route/interpretation test is the uniquely correct admission rule.

**Exact amended claim:** The ontology demonstrates that a useful non-redundancy heuristic can be overstated as statistical independence. The writing system may use an operational field-admission question without calling it zero mutual information, and it should make statistical independence claims only when an observed distribution and appropriate analysis support them; formal notation alone is not that evidence.

# Gaps or Inconsistencies Review

- **Empirical baseline — source-grounded and essential.** The essay itself disclaims empirical validation and asks whether reviewers agree, reader response can be tested, and the framework improves decisions (`vault/essays/evaluating-text-as-composition.md:14-17,307-327`). No cited source reports author burden, reader outcomes, agreement, or error rates.
- **Missing schema and conflict contract — source-grounded and useful.** The cited sources provide candidate fields and document contracts but no writing-profile schema, extension/migration rule, or disposition for preference-versus-principle conflict.
- **Missing check classification — source-grounded and useful.** Interrogation provides verdicts and Review provides verified findings, but neither classifies writing checks as deterministic predicates, heuristics, or evidence-bearing judgments. This is an important authority boundary.
- **Conflicting judgments — source-grounded and useful.** The essay rejects forced aggregation and recognizes structured disagreement, but leaves consistency, comparison, and closure open (`vault/essays/evaluating-text-as-composition.md:186-223,307-321`).
- **Formal-language evidence gate — source-grounded, but one example supports a risk rather than a general rate.** The ontology contains the claimed contradiction. It demonstrates possibility, not prevalence across the repository.
- **Bureaucracy budget — source-grounded as an absence and useful.** The essay warns against form completion and instructs reviewers to use only necessary distinctions (`vault/essays/evaluating-text-as-composition.md:260-271`), but defines no cost threshold.
- **Missing counter-gap: cost of under-formalization.** The report audits bureaucracy and false authority but does not equally ask what is lost without structure: comparability, reproducibility, migration, discoverability, and the ability to test whether the method improves. The corpus contains no comparison of formalized and unformalized workflows, so neither maximal caution nor aggressive formalization is yet evidence-backed.

# Local Tensions Review

- **Repeatability versus contextual judgment — source-grounded, with the benefit side untested.** Reusable dimensions and inputs coexist with explicit contextual criteria and form variation (`.codex/skills/write-need-driven-documents/SKILL.md:17-53,168-188`; `vault/essays/evaluating-text-as-composition.md:204-223`). The sources do not measure the repeatability gained.
- **Traceability versus writing overhead — source-grounded and useful.** Evidence citation and decision traceability are required in the cited methods, while the essay rejects indiscriminate form completion (`.agents/skills/interrogation/SKILL.md:55-85`; `.agents/skills/review/SKILL.md:139-145`; `vault/essays/evaluating-text-as-composition.md:260-271`).
- **Helpful linting versus gaming — plausible but not demonstrated for writing.** Review names abuse/gaming as a legitimate attack lens (`.agents/skills/review/SKILL.md:66-75`), but no cited source reports a writing check being gamed. Preserve this as an experiment risk, not an observed tension.
- **Personal control versus system learning — relevant but not grounded in this report’s cited evidence and partly crosses the author-sovereignty concern.** The statement should enter synthesis only if supported by investigator 01’s independently reviewed evidence; this review cannot validate it from the cited corpus.
- **Early standardization versus empirical learning — source-grounded and useful.** The essay is explicitly provisional and unvalidated, while schemas would create stable categories (`vault/essays/evaluating-text-as-composition.md:14-17,307-327`). The inverse risk should remain visible: refusing any early standardization can make comparable learning impossible.

# Questions for Synthesis Review

Questions 1–5 are source-grounded, within the formalization concern, and useful. Question 6 is a legitimate cross-concern dependency on author sovereignty and data governance, but its privacy and disposability dimensions are not supported by this report’s cited sources; synthesis should source it elsewhere or retain it as an open requirement. Question 7 is biased toward a preselected automation boundary: the corpus does not prove that schema parsing, provenance checks, and bookkeeping are the only code worth attempting first. A neutral formulation is: **“What evidence, failure cases, reversibility requirements, and cost thresholds should precede each proposed automation, from structural validation through semantic assistance?”**

# Eligible for synthesis

1. The current evidence supports formalizing the contextual basis and trace of a judgment—such as purpose, reader, selected criteria, cited evidence, judgment, and disposition—without treating field completion or an aggregate score as proof that a text works. The sources do not yet establish whether any carefully bounded aggregate evaluation can be useful.
2. Any initial schema should keep mandatory fields limited to common information whose interpretive or experimental value can be justified, treat the current candidate core as provisional, and allow document-specific criteria and personal preferences to vary. The sources do not yet determine the stable core or prove a particular extension architecture.
3. Automation is most defensible where a machine-readable contract makes the predicate explicit—for example syntax, enum membership, required-field presence, or resolvable-reference existence under a defined state. Automation may also assist semantic review, but structural checks alone cannot establish that evidence is sufficient, a criterion is adequate, prose is clear, or a reader effect occurred; those conclusions still require an attributable, evidence-bearing judgment.
4. The evaluation model must remain a versioned hypothesis until use supplies stronger evidence. Dimensions, lenses, and candidate shared principles should carry version and evidence status; their presence in a schema or skill must not silently promote them from working model to universal law.
5. The ontology demonstrates that a useful non-redundancy heuristic can be overstated as statistical independence. The writing system may use an operational field-admission question without calling it zero mutual information, and it should make statistical independence claims only when an observed distribution and appropriate analysis support them; formal notation alone is not that evidence.
