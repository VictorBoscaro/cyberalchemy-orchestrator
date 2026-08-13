---
node_type: agent-dialogue
status: resolved
date: 2026-08-12
topic: work-overview-composition
---

# Robot-Talks — Work overview composition

## Scope

Investigate how `work-and-knowledge-system-overview.md` should introduce concepts locally, when the
reader needs them, and later reveal the larger compositions those concepts form. The intended
reader is an intelligent, practical former mentor with strong product, growth, engineering, and
business training, but no assumed familiarity with this project's approach to AI-assisted work.

## Central question

How should the overview lead this reader from the product objective through the necessary local
concepts and then back to a small number of meaningful system compositions, without presenting a
catalogue, hiding design choices, or assuming internal vocabulary?

## Assumptions challenged

- Intelligence and fast learning do not imply familiarity with governed agent work.
- A component becomes understandable before its system-level grouping does.
- Larger groupings are synthesized explanatory models, not uniquely determined natural kinds.
- A grouping earns its place only if it explains a consequential relation or capability that its
  parts do not explain separately.
- The product subject is one person extending their capacity through AI agents while retaining
  comprehension and control.

## Chosen decomposition

Three independent concerns:

1. **Reader journey:** questions, order, pacing, terminology, and cognitive load.
2. **System composition:** local elements, consequential relations, larger groupings, boundaries,
   and what each composition makes possible.
3. **Product value and fidelity:** the user-level promise, practical consequences, present versus
   proposed capability, and protection against architectural drift.

No two agents own the same question. Evidence overlap is permitted.

## Alternative considered and rejected

Dividing the investigation by document sections was rejected. It would optimize passages locally
while obscuring the cross-section progression and the later synthesis of concepts—the central
question of this investigation.

## Agent prompts

### Reader-journey investigator

Read the complete overview and the two 2026-08-12 overview sessions. Determine the questions an
intelligent first-time reader will form, the order in which the document should answer them, where
concepts currently arrive too early or too late, and where a later compositional return would feel
earned. Do not design the architecture or adjudicate implementation status.

### System-composition investigator

Read the complete overview and its companion system views as needed. Identify the smallest local
concepts the reader must first understand, the consequential relations among them, and the few
larger compositions that can later synthesize those relations. For every proposed grouping, state
why it is useful, what new capability or explanation emerges, and where its boundary is arbitrary.
Do not optimize prose style or infer reader psychology beyond what is necessary.

### Product-fidelity investigator

Read the complete overview, owning Plan, predecessor roadmap, and 2026-08-12 overview sessions.
Test whether the narrative remains about expanding one person's capacity through AI agents while
preserving comprehension and control. Identify unsupported promises and distinctions between what
exists, what is proposed, and what is open. Do not propose detailed component groupings except
where required to expose product drift.

## Conversation protocol

Agents report independently in the mandatory Robot-Talks format: Key Findings with file-and-line
evidence, Gaps or Inconsistencies, Local Tensions, and Questions for Synthesis. The parent will
compare reports for cross-layer tensions. No implementation occurs inside Robot-Talks. The user
approved this strategy on 2026-08-12.

## Exploration result

All three agents completed independent reports:

- `reports/01-reader-journey.md`
- `reports/02-system-composition.md`
- `reports/03-product-fidelity.md`

The synthesis is recorded in `findings.md`. The reports converged on restoring the person working
through AI agents as the product subject, completing the user-visible loop before introducing
system vocabulary, and then making an explicit backward-looking pass that composes the local
concepts into three explanatory wholes. They also confirmed an architectural contradiction over
nested orchestration and a broader unresolved difference among the predecessor, active Plan, and
latest product objective.

## Synthesis

Six tensions were recorded: product subject versus generality; local clarity versus unexplained
wholes; user simplicity versus premature vocabulary; proposal status versus present-tense
behavior; contradictory orchestration-depth rules; and three related but unreconciled purpose
frames. Proposed dispositions appear in `findings.md`.

## Human gate

On 2026-08-12, the user accepted the proposed dispositions and authorized the overview rewrite.
The edit is a separate implementation act following this investigation. Two independent reviews
were requested after the rewrite.
