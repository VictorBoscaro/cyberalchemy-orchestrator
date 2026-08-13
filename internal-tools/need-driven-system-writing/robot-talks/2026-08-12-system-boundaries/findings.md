---
node_type: audit
status: draft
date: 2026-08-12
topic: need-driven-writing-system-boundaries-synthesis
human_disposition: pending
---

# Findings — Need-Driven Writing System Boundaries

## Evidence rule

This synthesis uses only the numbered formulations under the final `Eligible for synthesis`
heading of the four independent report reviews. Handles `01.1` through `04.5` identify those
formulations by review number and item order. Original reports and all other review sections are
provenance context only; they do not supply or strengthen any tension below. Primary-source
citations are trace links inherited from the reviews, not independently enlarged claims.

Every tension remains pending human disposition. The available dispositions are: **real and
actionable**, **real and deferred**, **misinterpretation**, or **uncertain and requiring targeted
follow-up**. Nothing here authorizes implementation, promotion, schema design, skill changes,
research, automation, or code.

## Cross-layer tensions

### T-01 — Durable personalization versus per-text and provisional evidence

- **Classification:** unresolved ownership and representation boundary, not an observed system
  failure.
- **Concern A — author sovereignty:** The available intake model is a candidate for one text, the
  interview procedure does not establish which writing evidence is sufficient, and inferred
  preferences cannot become canonical without a ratification lifecycle (`01.1`, `01.2`, `01.3`).
- **Concern B — operational architecture and formalization:** A durable profile is only a candidate
  boundary; observed-use residue needs an explicit promotion decision by an owner who has not yet
  been designated; and no stable profile schema or extension architecture has been established
  (`03.1`, `03.5`, `04.2`).
- **Exact tradeoff:** Personalization needs information that can affect later composition, but the
  only eligible intake evidence is per-text and the eligible architecture evidence forbids treating
  inference or residue as durable preference without an owner and promotion decision. Making the
  run state durable would overstate its authority; leaving everything per-run would leave no
  established durable personalization boundary.
- **Impact severity: HIGH.** A mistaken boundary could either let the system redefine an author's
  preferences or prevent author-approved preferences from remaining operative across uses.
- **Eligible evidence:** `01.1`, `01.2`, `01.3`, `03.1`, `03.5`, `04.2`.
- **Review trace:**
  - `reports/01-author-sovereignty.review.md#Eligible for synthesis`, items 1–3. Inherited primary
    traces: `.agents/skills/whisper/SKILL.md:21-25,51-55,79-83,116-126,143-156` and
    `.agents/skills/interrogation/SKILL.md:39-59,76-96`.
  - `reports/03-operational-architecture.review.md#Eligible for synthesis`, items 1 and 5.
    Inherited primary traces: `vault/essays/evaluating-text-as-composition.md:14-17,323-327`,
    `.codex/skills/write-need-driven-documents/SKILL.md:17-29`,
    `.agents/skills/whisper/SKILL.md:80-84,105-114`, and
    `vault/ontology-conventions.md:315-319,429-445`.
  - `reports/04-formalization-automation.review.md#Eligible for synthesis`, item 2. Inherited
    primary traces: `.codex/skills/write-need-driven-documents/SKILL.md:17-53,168-188`,
    `vault/essays/evaluating-text-as-composition.md:260-271`, and
    `internal-tools/need-driven-system-writing/README.md:47-58`.
- **Uncertainty or missing evidence:** No eligible formulation establishes whether a durable profile
  is necessary, which evidence can populate it, or who owns ratification and revocation.
- **Human disposition question:** Is this a real boundary requiring targeted follow-up on durable
  profile necessity and author ratification, or should personalization remain explicitly per-run
  until such evidence exists?
- **Human disposition:** pending.

### T-02 — A shared core versus bounded defaults and provisional theory

- **Classification:** prospective promotion and scope conflict.
- **Concern A — shared principles:** The eligible core candidates are scoped: reader transformation
  and part/whole contribution apply to purpose-driven writing or prose, and claim-force discipline
  applies where a reader is asked to rely on a claim. Most surface prescriptions remain
  preferences or context-specific criteria (`02.1`, `02.2`, `02.3`, `02.4`).
- **Concern B — author sovereignty, operations, and evidence status:** The current editorial method
  already contains strong bounded defaults that must remain distinguishable from author
  preferences; conceptual theory should remain separate from operational procedure; and the
  evaluation model remains a versioned hypothesis rather than universal law (`01.4`, `03.1`,
  `04.4`).
- **Exact tradeoff:** A system-wide core must be strong enough to constrain demonstrated failures,
  yet the eligible evidence supports only scoped candidates and explicitly denies universal status
  to most current prescriptions. Embedding current defaults as the core would silently promote a
  bounded method and draft model; withholding every shared constraint would discard the eligible
  purpose, composition, and reliance candidates.
- **Impact severity: HIGH.** Misclassification would either impose a disguised house style or leave
  no common basis for trustworthy, evaluable purpose-driven documents.
- **Eligible evidence:** `01.4`, `02.1`, `02.2`, `02.3`, `02.4`, `03.1`, `04.4`.
- **Review trace:**
  - `reports/01-author-sovereignty.review.md#Eligible for synthesis`, item 4. Inherited primary
    traces: `internal-tools/need-driven-system-writing/README.md:3-16,34-45`,
    `.codex/skills/write-need-driven-documents/SKILL.md:95-116`, and
    `vault/essays/evaluating-text-as-composition.md:204-223`.
  - `reports/02-shared-principles.review.md#Eligible for synthesis`, items 1–4. Inherited primary
    traces: `vault/essays/evaluating-text-as-composition.md:19-164,204-223,278-305`,
    `.codex/skills/write-need-driven-documents/SKILL.md:8-29,31-71,95-131`,
    `docs/essays/what-this-is-for/essay.md:27-57`, and
    `plans/governed-agent-work-infrastructure/essays/work-context-system-view/essay.md:301-320`.
  - `reports/03-operational-architecture.review.md#Eligible for synthesis`, item 1, and
    `reports/04-formalization-automation.review.md#Eligible for synthesis`, item 4. Inherited
    primary traces: `vault/essays/evaluating-text-as-composition.md:1-17,307-327` and
    `.codex/skills/write-need-driven-documents/SKILL.md:17-29`.
- **Uncertainty or missing evidence:** The eligible formulations do not establish cross-form
  universality, an admission test for the shared core, or evidence thresholds for promotion.
- **Human disposition question:** Should the current shared core remain a versioned set of scoped
  candidates for purpose-driven writing, with all surface prescriptions explicitly outside it,
  pending targeted evidence?
- **Human disposition:** pending.

### T-03 — Traceable formalization versus contextual editorial judgment

- **Classification:** untested tradeoff between interpretability and bureaucratic/formal
  overreach.
- **Concern A — operations and formalization:** Schemas can be justified at observed handoffs, and
  formal records can preserve the contextual basis and trace of a judgment. Initial mandatory
  fields should be limited to common information with justified interpretive or experimental value
  (`03.3`, `04.1`, `04.2`).
- **Concern B — shared principles:** Most surface prescriptions are not shared principles, and
  form-specific methods may choose expression (`02.4`).
- **Exact tradeoff:** Handoffs and later audits need enough stable structure to identify ownership,
  inputs, evidence, judgments, and dispositions, but representing contextual editorial judgment as
  completion of a universal form would convert preferences into apparent quality facts. The
  eligible evidence does not identify the minimum structure that gains traceability without doing
  that conversion.
- **Impact severity: HIGH.** Too much mandatory structure can manufacture objectivity and increase
  author burden; too little can make judgments uninterpretable and prevent comparable learning.
- **Eligible evidence:** `02.4`, `03.3`, `04.1`, `04.2`.
- **Review trace:**
  - `reports/02-shared-principles.review.md#Eligible for synthesis`, item 4. Inherited primary
    traces: `.codex/skills/write-need-driven-documents/SKILL.md:31-71,95-116` and
    `vault/essays/evaluating-text-as-composition.md:204-223,278-305`.
  - `reports/03-operational-architecture.review.md#Eligible for synthesis`, item 3. Inherited
    primary traces: `.agents/skills/whisper/SKILL.md:57-82`,
    `.agents/skills/interrogation/SKILL.md:62-74`, and
    `vault/essays/evaluating-text-as-composition.md:204-223,260-271`.
  - `reports/04-formalization-automation.review.md#Eligible for synthesis`, items 1–2. Inherited
    primary traces: `vault/essays/evaluating-text-as-composition.md:103-124,204-223,260-271,307-321`,
    `.codex/skills/write-need-driven-documents/SKILL.md:17-53,168-188`, and
    `internal-tools/need-driven-system-writing/README.md:47-58`.
- **Uncertainty or missing evidence:** No eligible formulation supplies a measured author-effort
  cost, a minimum field set, or comparative evidence for structured versus unstructured use.
- **Human disposition question:** Is the minimum-formalization boundary a real, actionable design
  question now, a deferred research question, or uncertain pending a bounded comparison of
  interpretability and author cost?
- **Human disposition:** pending.

### T-04 — Deterministic structural checks versus semantic review authority

- **Classification:** authority boundary with a prospective conflation risk.
- **Concern A — automation:** Explicit machine-readable predicates can support deterministic
  structural checks, and automation may assist semantic review, but those checks cannot establish
  evidence sufficiency, criterion adequacy, clarity, or reader effect (`04.3`).
- **Concern B — shared principles and review operations:** Claims asking for reliance must stay
  within their support, while authorial self-check and independent evidence-bearing red-team review
  remain distinct actions and authorities (`02.3`, `03.4`).
- **Exact tradeoff:** The system may legitimately automate explicit structural predicates, but a
  passing structural result cannot inherit the authority of an evidence-bearing semantic judgment.
  Conversely, refusing deterministic checks merely because they are not semantic would discard a
  defensible automation boundary. The unresolved issue is which result types may constrain delivery
  without masquerading as a textual-quality verdict.
- **Impact severity: HIGH.** Conflating the result types could block or approve work on evidence a
  check cannot supply; rejecting all automation would preserve avoidable omissions and repeated
  work.
- **Eligible evidence:** `02.3`, `03.4`, `04.3`.
- **Review trace:**
  - `reports/02-shared-principles.review.md#Eligible for synthesis`, item 3. Inherited primary
    traces: `vault/essays/evaluating-text-as-composition.md:103-151`,
    `.codex/skills/write-need-driven-documents/SKILL.md:118-131`,
    `docs/essays/what-this-is-for/essay.md:27-57`, and
    `plans/governed-agent-work-infrastructure/essays/work-context-system-view/essay.md:301-320`.
  - `reports/03-operational-architecture.review.md#Eligible for synthesis`, item 4. Inherited
    primary traces: `.codex/skills/write-need-driven-documents/SKILL.md:168-202` and
    `.agents/skills/review/SKILL.md:8-13,125-145`.
  - `reports/04-formalization-automation.review.md#Eligible for synthesis`, item 3. Inherited
    primary traces: `.agents/skills/interrogation/SKILL.md:39-85,99-113`,
    `.agents/skills/review/SKILL.md:128-152,194-201`, and
    `vault/ontology-conventions.md:67-92`.
- **Uncertainty or missing evidence:** No eligible formulation classifies concrete future checks by
  authority, warning/blocking behavior, false-positive rate, or demonstrated benefit.
- **Human disposition question:** Is this authority boundary real and actionable as a prerequisite
  to any automated check, or uncertain until concrete checks and failure cases are proposed?
- **Human disposition:** pending.

### T-05 — Form-dependent composition versus specialization without duplication

- **Classification:** prospective contract-boundary decision.
- **Concern A — shared composition and author intent:** Purpose-driven prose requires different
  relations according to form, and form-specific methods may choose expression; the available
  per-text intake is only one candidate and does not establish stable profile fields (`02.2`,
  `02.4`, `01.1`).
- **Concern B — operational architecture:** A specialization is justified only when it adds a
  distinct form, required field set, or gate rather than duplicating general guidance (`03.2`).
- **Exact tradeoff:** Form dependence creates pressure for specialization, but form variation alone
  does not prove that a new contract owner is needed. Specializing too early duplicates guidance
  and fragments ownership; refusing specialization where a distinct contract exists can hide
  form-specific requirements inside a purportedly general procedure.
- **Impact severity: MEDIUM.** The main demonstrated risk is ownership drift and duplication rather
  than immediate loss of author authority or evidential truth.
- **Eligible evidence:** `01.1`, `02.2`, `02.4`, `03.2`.
- **Review trace:**
  - `reports/01-author-sovereignty.review.md#Eligible for synthesis`, item 1. Inherited primary
    traces: `.agents/skills/whisper/SKILL.md:21-25,51-55,116-126`.
  - `reports/02-shared-principles.review.md#Eligible for synthesis`, items 2 and 4. Inherited
    primary traces: `vault/essays/evaluating-text-as-composition.md:57-101,153-164,204-223,278-305`
    and `.codex/skills/write-need-driven-documents/SKILL.md:31-71,95-116`.
  - `reports/03-operational-architecture.review.md#Eligible for synthesis`, item 2. Inherited
    primary traces: `.codex/skills/write-need-driven-documents/SKILL.md:14-15` and
    `.agents/skills/system-view/SKILL.md:29-40,63-79`.
- **Uncertainty or missing evidence:** No eligible formulation identifies which document forms
  require independent contracts or shows that any proposed specialization improves outcomes.
- **Human disposition question:** Should specialization remain deferred until a form demonstrates
  a required field set or gate not owned by the general procedure?
- **Human disposition:** pending.

### T-06 — Learning from use versus author and model promotion authority

- **Classification:** unresolved promotion authority with prospective silent-rewrite risk.
- **Concern A — learning and model evolution:** Observed-use lessons may remain as noncanonical
  residue, and the evaluation model should remain versioned until stronger evidence arrives
  (`03.5`, `04.4`).
- **Concern B — author sovereignty:** Decision traces and corrections provide partial support, but
  inferred preferences cannot become canonical without durable correction, explicit status, and an
  author-ratification lifecycle (`01.3`).
- **Exact tradeoff:** The system needs evidence from use to revise its working model, but the same
  residue cannot silently revise an author's durable preferences or shared rules. Promotion is
  necessary for learning to affect later behavior, while promotion without a designated owner and
  evidence boundary transfers authority from the author or human gate to the system.
- **Impact severity: HIGH.** Silent promotion could change personal or shared rules without valid
  authority; permanent nonpromotion could make the system unable to learn from evidence.
- **Eligible evidence:** `01.3`, `03.5`, `04.4`.
- **Review trace:**
  - `reports/01-author-sovereignty.review.md#Eligible for synthesis`, item 3. Inherited primary
    traces: `.agents/skills/interrogation/SKILL.md:55-59` and
    `.agents/skills/whisper/SKILL.md:79-83,143-156`.
  - `reports/03-operational-architecture.review.md#Eligible for synthesis`, item 5. Inherited
    primary traces: `.agents/skills/whisper/SKILL.md:80-84,105-114` and
    `vault/ontology-conventions.md:315-319,429-445`.
  - `reports/04-formalization-automation.review.md#Eligible for synthesis`, item 4. Inherited
    primary trace: `vault/essays/evaluating-text-as-composition.md:1-17,307-327`.
- **Uncertainty or missing evidence:** Promotion owners for profiles, principles, and skills are
  explicitly undefined; no eligible formulation establishes an evidence threshold or whether any
  promotion may be automatic.
- **Human disposition question:** Is explicit human/author promotion a required invariant for all
  durable preference and principle changes, or is this uncertain and in need of targeted research?
- **Human disposition:** pending.

## Eligibility coverage ledger

Every eligible handle is used in at least one cross-layer tension. The formulation column preserves
the final review wording; the trace column identifies the exact review item.

| Handle | Eligible formulation | Review source and item | Tension use |
|---|---|---|---|
| `01.1` | Whisper provides one candidate per-text intake model that extends beyond tone across felt effect, reader/domain fit, and intended movement. It supports asking about desired effect, relationship to the reader, structural movement, and aversions, but does not establish that all of its fields are required or stable components of an author-owned writing profile. | `reports/01-author-sovereignty.review.md`, Eligible item 1 | `T-01`, `T-05` |
| `01.2` | If Interrogation is adapted for writing-preference discovery, its supported procedural defaults are to inspect available evidence first, ask one high-discrimination question at a time, and preserve explicit uncertainty rather than invent answers. The bounded sources do not specify which writing evidence should be inspected or show that this process is sufficient to discover an author's preferences. | `reports/01-author-sovereignty.review.md`, Eligible item 2 | `T-01` |
| `01.3` | Existing practices partially support author ownership by tracing decisions and user corrections and by preventing learning residue from automatically becoming canonical author voice. They do not yet define a durable correction history, explicit-versus-inferred preference states, or an author-ratification lifecycle; inferred preferences therefore cannot be treated as canonical on the authority of these sources alone. | `reports/01-author-sovereignty.review.md`, Eligible item 3 | `T-01`, `T-06` |
| `01.4` | The current editorial method contains strong defaults suited to a bounded document class, while the composition essay treats adequacy criteria as context-dependent. A profile interview should therefore keep author-supplied preferences distinguishable from task/form constraints and method defaults; the bounded sources do not yet specify the exact return format needed to preserve that distinction. | `reports/01-author-sovereignty.review.md`, Eligible item 4 | `T-02` |
| `02.1` | For purpose-driven writing, a document should declare or make recoverable the change it is meant to produce for a situated reader, and its parts should be judged against that use. | `reports/02-shared-principles.review.md`, Eligible item 1 | `T-02` |
| `02.2` | For purpose-driven prose, relationships among parts should make a defensible contribution at both local and whole-document scales, while the relation required depends on form: cumulative prose may rely on prepared sequence, whereas modular or reference prose may rely on navigable routes, comparisons, dependencies, and locally sufficient context. This is a candidate beyond those forms, not a demonstrated universal. | `reports/02-shared-principles.review.md`, Eligible item 2 | `T-02`, `T-05` |
| `02.3` | Wherever a text asks a reader to rely on a factual, inferential, or normative claim, the claim's force should remain within the kind and strength of its support, and uncertainty, proposal status, provenance limits, and reliance limits should remain visible where they matter. | `reports/02-shared-principles.review.md`, Eligible item 3 | `T-02`, `T-04` |
| `02.4` | Most surface prescriptions in the bounded sources are preferences or context-specific criteria, not shared principles. A shared core should constrain demonstrated failures; profiles and form-specific methods may choose expression. | `reports/02-shared-principles.review.md`, Eligible item 4 | `T-02`, `T-03`, `T-05` |
| `03.1` | At minimum, keep the revisable conceptual model distinct from the operational composition procedure. Treat profiles, briefs, use residue, and promotion as candidate boundaries pending evidence and explicit contracts. | `reports/03-operational-architecture.review.md`, Eligible item 1 | `T-01`, `T-02` |
| `03.2` | Create a specialization only at a distinct contract boundary; it must add a form, required fields, or gate the composition core does not own rather than duplicate general prose guidance. | `reports/03-operational-architecture.review.md`, Eligible item 2 | `T-05` |
| `03.3` | Use schemas at observed handoffs that require explicit ownership, inputs, consumers, gates, or traceability. Do not predetermine the number of schemas or encode contextual editorial judgment as a universal quality form. | `reports/03-operational-architecture.review.md`, Eligible item 3 | `T-03` |
| `03.4` | Let writing and independent review share vocabulary while remaining distinct actions and authorities: authorial self-check before delivery versus read-only, evidence-bearing red-team review of an existing artifact. | `reports/03-operational-architecture.review.md`, Eligible item 4 | `T-04` |
| `03.5` | Preserve observed-use lessons as noncanonical residue until an explicit promotion decision by a designated owner; profile, principle, and skill promotion ownership is still undefined. | `reports/03-operational-architecture.review.md`, Eligible item 5 | `T-01`, `T-06` |
| `04.1` | The current evidence supports formalizing the contextual basis and trace of a judgment—such as purpose, reader, selected criteria, cited evidence, judgment, and disposition—without treating field completion or an aggregate score as proof that a text works. The sources do not yet establish whether any carefully bounded aggregate evaluation can be useful. | `reports/04-formalization-automation.review.md`, Eligible item 1 | `T-03` |
| `04.2` | Any initial schema should keep mandatory fields limited to common information whose interpretive or experimental value can be justified, treat the current candidate core as provisional, and allow document-specific criteria and personal preferences to vary. The sources do not yet determine the stable core or prove a particular extension architecture. | `reports/04-formalization-automation.review.md`, Eligible item 2 | `T-01`, `T-03` |
| `04.3` | Automation is most defensible where a machine-readable contract makes the predicate explicit—for example syntax, enum membership, required-field presence, or resolvable-reference existence under a defined state. Automation may also assist semantic review, but structural checks alone cannot establish that evidence is sufficient, a criterion is adequate, prose is clear, or a reader effect occurred; those conclusions still require an attributable, evidence-bearing judgment. | `reports/04-formalization-automation.review.md`, Eligible item 3 | `T-04` |
| `04.4` | The evaluation model must remain a versioned hypothesis until use supplies stronger evidence. Dimensions, lenses, and candidate shared principles should carry version and evidence status; their presence in a schema or skill must not silently promote them from working model to universal law. | `reports/04-formalization-automation.review.md`, Eligible item 4 | `T-02`, `T-06` |
| `04.5` | The ontology demonstrates that a useful non-redundancy heuristic can be overstated as statistical independence. The writing system may use an operational field-admission question without calling it zero mutual information, and it should make statistical independence claims only when an observed distribution and appropriate analysis support them; formal notation alone is not that evidence. | `reports/04-formalization-automation.review.md`, Eligible item 5 | Not used — supplies a compatible evidence guardrail, not a cross-layer tension. |

## Synthesis status

- Eligible source extraction: complete; 18 of 18 handles mapped.
- Cross-layer tensions: six, all pending independent review.
- Human dispositions: pending for `T-01` through `T-06`.
- Independent review artifact: pending at `reports/05-synthesis.review.md`.
- Promotion or implementation authority: none.
