---
node_type: agent-dialogue
status: accepted
date: 2026-08-10
topic: superinterviewer-repository-foundation
---

# Robot-Talks — Superinterviewer Repository Foundation

## Scope

Determine the smallest repository foundation that lets the Superinterviewer own its product vision
and large research program while reusing existing repositories without silently inheriting their
accidental architectures. This investigation identifies tensions and decision boundaries; it does
not create the new repository or implement the Superinterviewer.

## Central Question

What is the minimum foundation for the Superinterviewer to own its product vision and research
program while reusing other repositories without accidentally inheriting their architectures?

## Assumptions Challenged

- A new repository is necessary and preferable to an existing repository.
- One master `research-initial-definitions.md` plus scoped initial definitions is the right hierarchy.
- A living `research-plan.md` is the correct layer between the product vision and individual research runs.
- `subagent-work-infrastructure` should remain subordinate execution infrastructure.
- The authority machinery described by `mint` is appropriate, or can be reduced safely, for inception.
- A research-first start without product implementation is the right initial sequence.

## Chosen Decomposition

### Product and Research Authority

Concern: what the repository must own so the Superinterviewer remains the primary interface and
intellectual partner rather than becoming a generic framing framework or an infrastructure project.

Central question: which minimum product and research authorities must exist on day one?

Exclusions: runtime mechanics, deployment choices, and mathematical formalization details.

Report: `reports/01-product-research-authority.md`.

### Authority and Scaffold

Concern: what repository scaffold, governance, rules, and authority spine are justified by existing
creation mechanisms and precedents.

Central question: what can be inherited safely, and what would over-govern or prematurely freeze the project?

Exclusions: redefining the product thesis and selecting the interaction UX.

Report: `reports/02-authority-scaffold.md`.

### Integration and Execution Boundary

Concern: how the new repository relates to `subagent-work-infrastructure`, DomainSpec, Arcanum,
formalization repositories, source evidence, dispatches, and observability.

Central question: what must be owned locally versus referenced, invoked, imported, or kept external?

Exclusions: deciding the product's conversational behavior and implementing the infrastructure.

Report: `reports/03-integration-execution-boundary.md`.

## Rejected Alternative

Partitioning agents by repository was rejected. It would produce isolated inventories and hide the
contradictions between product authority, research governance, and execution infrastructure. Agents
therefore investigate distinct concerns across overlapping evidence corpora.

## Conversation Protocol

1. Each investigator works independently and reads only what is necessary for its concern.
2. Each report uses: Key Findings; Gaps or Inconsistencies; Local Tensions; Questions for Synthesis.
3. Every load-bearing finding cites a repository path and, where practical, a line or section.
4. The parent synthesizes contradictions across reports into `findings.md`.
5. No new repository is created and no source artifact outside this Robot-Talks folder is modified.
6. The final tensions return to the user for disposition before any implementation.

## Agent Prompts

The three prompts preserve the scope, role-specific concern, exclusions, required report shape, and
reserved output path declared above. Agents may inspect `cyberalchemy-orchestrator` and relevant
sibling repositories but may write only their own reserved report.

## Independent Reports

- `reports/01-product-research-authority.md`
- `reports/02-authority-scaffold.md`
- `reports/03-integration-execution-boundary.md`

All three reports use the required structure and cite their load-bearing sources. The reports were
frozen independently before synthesis.

## Cross-Agent Dialogue

No challenge ring was opened. The reports exposed complementary tensions without an unresolved
factual contradiction that required another agent round.

## Orchestrator Synthesis

The synthesis is preserved in `findings.md`. Six tensions survived: product authority versus
research authority; clean-repo direction versus untested necessity; research-first versus empirical
prototypes; full `mint` versus proportional bootstrap; subordinate-infrastructure language versus
SWI's peer-product authority; and exact lineage versus accidental architectural inheritance.

## Human Gate

The user accepted all six proposed dispositions on 2026-08-10. Planning may proceed. Repository
creation and implementation remain separate later gates.
