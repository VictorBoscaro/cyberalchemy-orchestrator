---
feature: agent-provenance-telemetry
artifact: current-state-inventory
status: complete
version: 0.2.1
created: 2026-07-22
method: single-read-only-dispatch-plus-bounded-source-check
reviewed: false
---

# Current-state inventory — tags, lineage and source telemetry

This inventory records facts gathered by one bounded read-only subagent dispatch plus a later bounded
source check of the local pool and its sibling provenance repository. The dispatch had no reviewers
and made no edits. This remains input to the discovery, not independent validation of it.

The focused [Session–Dispatch–Research discovery](../discovery/session-dispatch-research-records.md)
derives its compatibility constraints from this inventory; that later discovery's review does not
retroactively mark this source inventory as independently reviewed.

## Existing vocabulary surfaces

- [`agent-pool.yaml`](../../../../telemetry/agents/agent-pool.yaml) is the local source of truth for
  agent profiles. Every entry also has a coarse `field` describing its principal contribution area;
  its tags describe finer topical expertise used to help select personas. Both are profile priors, not
  observations of what happened in a run. The current pool contains 414 entries and its header states
  that the usage-derived vocabulary has 721 tags.
- The pool header references `research/pool-tagging/canonical-vocabulary.md`, but that file is absent
  from this workspace. The running [agent-pool MCP](../../../../tools/agent-pool-mcp/README.md#why-it-exists)
  instead derives the vocabulary as the union of tags actually present in the pool
  ([`pool.mjs`, lines 23–36](../../../../tools/agent-pool-mcp/src/pool.mjs)).
- The referenced vocabulary and its decision trail do exist in the sibling source repository. Its
  field rule is contribution-first rather than credential-first. The current MCP ranking nevertheless
  uses tag overlap and omits `field` from its result projection, so telemetry must snapshot
  `profile_field` explicitly instead of assuming the selector exposed it.
- The MCP deliberately separates exact membership/ranking from semantic adjudication and rejects
  silent duplicate-tag coinage ([README, lines 9–25](../../../../tools/agent-pool-mcp/README.md#why-it-exists)).
- Knowledge Taxonomy is a faceted classification substrate, not a topic-tag list. Five facets are
  closed while `domain` is open; its system-tagging engine is a specification, not shipped software
  ([research trail, lines 47–58](../../../../research/agent-events-infra-hypothesis/research.md)).

## Existing capture and lineage decisions

- The assertion-capture discovery separates lenient source testimony from strict promotion. The
  emitter records but does not judge ([lines 98–115](../../../discovery/agent-assertion-capture/README.md#c1--emitter-as-stenographer-form--quality)).
- Source records are immutable testimony; refinement creates new records that point back rather than
  rewriting the source ([lines 134–143](../../../discovery/agent-assertion-capture/README.md#c4--source-layer--witness-coarsest-quality-finest-granularity)).
- Lineage must be writer-stamped, but the current resolution path for session/dispatch identity is an
  explicit build gap ([lines 199–219](../../../discovery/agent-assertion-capture/README.md#31-emission-record-shape)).
- Existing research distinguishes a-priori method/theme used for selection from a-posteriori observed
  subject. Divergence must preserve schema residue separately from instance residue
  ([findings, lines 47–58](../../../../research/agent-events-infra-hypothesis/findings.md)).

## Current dispatch and reader constraints

- The dispatch appender accepts exactly schema `0.6.1`, rejects unknown keys and has no
  conversation/turn/topic/manifest fields
  ([`append-dispatch.cjs`, lines 96–150](../../../../.claude/skills/register-dispatch/append-dispatch.cjs)).
- Its close row accepts only the existing close fields; a telemetry manifest requires a coordinated
  schema change ([lines 122–126](../../../../.claude/skills/register-dispatch/append-dispatch.cjs)).
- Pending sheets are the editable pre-confirm surface
  ([`ledger.py`, lines 388–429](../../../../implementations/server/ledger.py)), while dispatch and close
  rows remain append-only.
- The detail endpoint returns the joined full row, but list views use an explicit slim projection that
  would omit new fields until updated ([`ledger.py`, lines 650–696](../../../../implementations/server/ledger.py)).
- `parent_dispatch_id` already exists but carries a narrow meta-dispatch meaning. Generic causal
  lineage needs a separate origin edge instead of silently widening that field.

## Guardrails carried into the discovery

1. `profile_field`, `profile_tags`, predicted dispatch topics, isolated agent-observed topics,
   system-resolved tags and residue remain separate records.
2. `agent_name` is a persona label, not execution identity; provenance uses seat and attempt IDs.
3. “All papers” is bounded to papers observed through mediated tools.
4. A search result is not a researched paper; source progression remains explicit.
5. Telemetry cannot release work, close a run or promote knowledge.
6. Conversation identity is not the same namespace as a curated `sessions/*.md` document.
7. Any schema bump needs round-trip tests through pending sheet, appender, reader, detail and list
   projections; allowlisting a field without emitting it is an unacceptable false implementation.

## Unverified items

- The 414-entry/721-tag counts came from the read-only inventory and pool-derived vocabulary behavior;
  they should be recomputed by an executable fixture before becoming a version gate.
- No empirical tag-agreement, drift, coverage, capture-cost, paper-recall, replay or lens-utility result
  exists yet.
  The preregistered protocols live in [`../probes/`](../probes/README.md).

## Connections

| Document | Type | Description |
|---|---|---|
| [Session–Dispatch–Research records](../discovery/session-dispatch-research-records.md) | `grounds` | Supplies the current ledger, identity and reader constraints used by the focused discovery. |

## Appendix — Changelog

| Version | Date | Change |
|---|---|---|
| 0.2.1 | 2026-07-23 | Added the inverse provenance edge to the focused discovery; the inventory remains explicitly unreviewed source material. |
