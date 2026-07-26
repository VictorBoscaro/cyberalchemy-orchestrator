---
name: experiment-initial-definitions
description: Creates or revises the informational experiment-initial-definitions.md required before a governed experiment is designed or proposed. Use when opening an experiment topic or documenting its business context, purpose, refinable question, confirmed constraints, current evidence, and known gaps without choosing a hypothesis, criterion, method, or dispatch topology.
---

# Experiment Initial Definitions

Create `<experiment-folder>/experiment-initial-definitions.md` before a governed experiment is
designed or proposed. The document explains what the product or system needs to understand; it does
not prescribe how the experiment will be conducted.

## Required structure

### Context

Write one or two high-level paragraphs. Begin with the broader product or system and its purpose.
Then describe the local problem the future experiment supports resolving and why that problem
matters to a person using or governing the system.

Do not describe a candidate experiment, implementation, schema, topology, or expected result.

### Purpose

Explain what this document establishes and which later discovery, design, or decision it will
inform. Do not describe experiment execution.

### Experiment Question (Can be refined)

State the initial question clearly. Keep it refinable rather than treating its first wording as a
frozen hypothesis or criterion.

### Confirmed Product Constraints

Record decisions, requirements, and boundaries already established by the user or an authoritative
project artifact. Start with business meaning and user-facing constraints. Do not present
assumptions or candidate mechanisms as confirmed constraints.

### Current Evidence Baseline

Summarize relevant information already known before experiment design begins. Cite existing
artifacts when available. Do not run a probe or conduct new research merely to populate this
section.

### Known Gaps

Record what is not yet understood. Describe missing knowledge, unclear boundaries, or unresolved
concepts without turning them into tasks, hypotheses, criteria, or an experiment plan.

## Boundaries

Keep confirmed facts, existing evidence, and unknowns distinct. Do not include:

- a candidate hypothesis, falsification condition, success metric, or verdict rule;
- experiment methods, fixtures, probes, source selection, or execution steps;
- agent roles, tools, dispatch topology, budgets, schemas, or database tables;
- counterexamples, stopping conditions, output contracts, or implementation proposals; or
- findings, adjudication, handoffs, or recommended solutions.

Treat the document as informational context. It is not `criterion.md`, an experiment proposal, a
dispatch configuration, a specification, or runtime authority.

