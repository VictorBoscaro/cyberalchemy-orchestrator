# Initial definitions: minimal meeting ontology

## Context

ResonantOS develops infrastructure that keeps community work connected to its objectives,
decisions, assumptions, actions, and evidence. Meetings are one place where those connections can
be created or lost, especially as participation and stewardship expand.

The existing meeting-model documents describe a broad candidate vocabulary. The local problem is
to avoid treating that breadth as necessary: the project first needs to understand the smallest
conceptual core that can represent the meeting domain without hiding distinctions that matter.

## Purpose

This document establishes the informational boundary for research into a minimal meeting
ontology. The result will inform later decisions about which concepts deserve definitions and
which broader concepts should be omitted, deferred, or treated only as proposals.

## Research Question (Can be refined)

What is the smallest ontology that represents the knowledge ResonantOS actually needs about
meetings, while permitting tentative definitions only for small, well-bounded concepts?

## Confirmed Product Constraints

- Minimize the number of concepts under consideration.
- Do not assume that every concept in the existing meeting-model documents belongs in the minimal
  ontology.
- Definitions may be proposed for small, bounded concepts; broader or contested concepts should
  remain provisional or outside the result.
- Independent attempts should use distinct participant, operational, and authority-boundary
  perspectives, with two attempts per perspective.
- The work concerns synchronous ResonantOS meetings and recurring meeting contexts, not the full
  governance or contribution-reward architecture.

## Current Evidence Baseline

- [`research-plan.md`](research-plan.md) establishes the earlier, broader meeting-model question
  and separates official facts from proposals.
- [`ontology-view.md`](ontology-view.md) contains an 18-term candidate vocabulary whose real-case
  and participant validation remains undone.
- [`system-view.md`](system-view.md) explains the current candidate shape without settling it.
- [`engineer-view.md`](engineer-view.md) records nine unresolved or critical decisions and
  candidate mechanics; none is ratified.
- [`paired-views-report.md`](paired-views-report.md) finds the documents structurally consistent but
  marks their content maturity as candidate.

## Known Gaps

- Which concepts are indispensable across perspectives is unknown.
- It is unclear which apparent concepts are merely attributes, relations, labels, or implementation
  details.
- The smallest useful boundary between one meeting and a recurring context is unresolved.
- It is unknown whether purpose, outcome, participation, memory, and authority all belong in the
  minimal core.
- The existing vocabulary has not been tested against real meeting cases or participant language.
