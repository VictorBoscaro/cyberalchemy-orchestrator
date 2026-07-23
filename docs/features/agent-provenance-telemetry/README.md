---
feature: agent-provenance-telemetry
title: Agent Provenance Telemetry
status: discovery
version: 0.7.0
authority: observational-only
absorption_target: agents-communication-infra
created: 2026-07-22
last_updated: 2026-07-23
---

# Agent Provenance Telemetry

Compatibility feature for reconstructing which conversation and turn caused a dispatch, which later
dispatches descended from it, what topics each logical agent seat reported working on and which papers
were observed through mediated research tools. Version 0.6 also proposes one bounded
`reference-probe` tool: ordinary agents may retrieve relevant internal and/or external references
through a small, bus-backed worker/reviewer group. A larger shape uses two tensioned groups and a
bounded cross-lens exchange.

Topic capture is intentionally weak and observational. An agent deposits only a flat JSON list of
free tags. The telemetry system adds lineage and stores the observation; it does not assign tag IDs,
map equivalents, reject unknown labels or maintain a canonical registry. Exact strings,
co-occurrence and provenance are enough for the first evidence-gathering phase.

It is deliberately **observational only**. It does not govern execution, make an agent output
official, classify knowledge as true or promote tags into a knowledge store. Its records are designed
to be absorbed later by the event journal, artifact boundary and projections of
[`agents-communication-infra`](../agents-communication-infra/README.md), without preserving a parallel
runtime.

## Documents

- [Feature discovery](discovery.md)
- [Session–Dispatch–Research records discovery](discovery/session-dispatch-research-records.md)
- [Agent topic-emission skill](../../../.claude/skills/emit-topic-tags/SKILL.md)
- [Topic-tag host contract](../../../.claude/skills/emit-topic-tags/references/host-contract.md)
- [Conformance and semantic release tests](../../../.claude/skills/emit-topic-tags/references/conformance.md)
- [Preregistered empirical probes](probes/README.md)
- [Reference-probe tool and first bus slice](probes/reference-probe-tool.md)
- [Coarse session registry](session-registry.md)
- [Current-state inventory](research/current-state-inventory.md)
- [Independent review of the previous registry design](reviews/2026-07-22-system-tags-and-lens-review.md)

The executable registry/resolution fixtures and registry-curation notes under `contracts/` and
`research/` are retained only as a discarded design exploration. They are not part of the active
contract.

## Current decision

Instrument the smallest useful slice: conversation/turn lineage, dispatch origin edges, mediated
source observations, reference-delivery manifests and one flat free-tag emission per agent
activation. Add a bounded, bus-backed `reference-probe` tool whose scope, human distance and budget
are host-stamped. Its minimum shape is one worker plus one reviewer; its larger shape is two
tensioned worker/reviewer groups. Both return only reviewed recommendations of where to look.
Introduce a still coarser session dataset above dispatches so all subsequent telemetry shares one
stable work identity.
Add a structured research level below dispatches: research records preserve exact questions and
final returns, then attach reference uses/checks, problems, claims and candidate formalizations.
Dispatch tables expose references and problem/result summaries only as traceable projections; they
do not duplicate the research content.
Use the prompt to elicit both broad domains and granular subjects. Accumulate raw observations first;
decide whether equivalence, canonicalization or a registry is warranted only after the probes expose
real vocabulary behavior.
