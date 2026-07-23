---
canonical_kind: discovery
feature: agent-provenance-telemetry
title: Agent Provenance Telemetry — conversation, topic and source lineage
description: Minimal observational spine linking conversations and turns to dispatches, free per-agent topic tags and mediated source observations.
status: draft
version: 0.7.0
authority: observational-only
absorption_target: agents-communication-infra
created: 2026-07-22
last_updated: 2026-07-23
tags: [telemetry, provenance, conversations, dispatch, agents, topics, papers, sources]
question: What is the smallest observational contract that lets the system reconstruct dispatch lineage, topics encountered by each agent and papers accessed without prematurely imposing a taxonomy?
---

# Agent Provenance Telemetry — conversation, topic and source lineage

## Decision

Start with observation, not ontology, and acquire undeclared references through bounded Scouts rather
than ambient exploration by the working agent.

Each agent deposits a flat list of topic strings. The system records that list with the activation,
dispatch, conversation and turn that caused it. There are no tag IDs, canonical equivalents,
confidence scores, relation types, unmapped terms, assisted-selection phase or tag-registry mutation
protocol in v0.3.

This supersedes the registry/resolution design in v0.2. The older contract fixtures and curation notes
remain historical inputs, not active requirements.

Version 0.6 added a proposed tool under the legacy `reference-probe` name; its canonical name is now
`ReferenceScoutTool`, alongside the coarse session registry. This does not turn telemetry into a
truth authority. A small Scout uses one worker and one reviewer; a larger Scout uses two tensioned
worker/reviewer groups. Both retrieve relevant internal and/or external references,
commit their exchanges and recommendation bundle through the bus, and return only where-to-look
guidance to the caller. The full
contracts are [`probes/reference-scout-tool.md`](probes/reference-scout-tool.md) and
[`session-registry.md`](session-registry.md).

Version 0.7 adds the focused
[Session–Dispatch–Research discovery](discovery/session-dispatch-research-records.md). Session stays
coarse, Dispatch stays the lifecycle/assignment record, and Research becomes the owner of exact
questions, final returned answers, reference uses/checks, problems, claims and candidate
formalizations. Dispatch-level counts and statuses are projections over those research records.

## Questions this feature must answer

1. Which dispatches belong to this conversation?
2. Which turn or earlier dispatch originated each action or research dispatch?
3. What subjects did each logical agent seat say were relevant to its activation?
4. Which papers and other sources did each seat actually access through mediated tools?
5. What repeated terms, co-occurrences, differences and changes appear across those observations?
6. Which bounded ScoutRun found each reference, and to which activation or exchange was that
   committed bundle demonstrably delivered?
7. Which exact question did each research contribution investigate, and what final answer returned?
8. Which references were merely mentioned, host-observed, located or independently checked?
9. Which problems, claims and candidate mathematical/logical formalizations arose from each answer?

The fifth question is exploratory. A repeated string is evidence of repeated use, not proof of a
stable concept, consensus, truth or agent competence.

## Why this cut

The current dispatch ledger has `dispatch_id` and sometimes `parent_dispatch_id`, but no stable
conversation or turn identity. Static agent profiles describe likely expertise; outputs and prompts
contain dynamic topics and citations mostly as prose. That prevents reliable queries such as “show all
dispatches from this conversation” and “which research action accessed this paper?”

There is also too little runtime evidence to justify a canonical topic registry. Adding semantic
mapping now would turn guesses about equivalence into infrastructure. Raw attributed lists preserve
more optionality and are sufficient to measure vocabulary stability, overlap and drift.

## Identity and lineage

`conversation_id` identifies one host conversation. `turn_id` identifies a turn within it. A curated
session document may reference conversations but is not their identity.

Every dispatch records zero or more directed origin edges. The destination is the current dispatch;
the source may be a conversation turn or an earlier dispatch.

```json
{
  "dispatch_id": "dispatch-01",
  "conversation_id": "conversation-01",
  "turn_id": "turn-07",
  "origin_refs": [
    "conversation:conversation-01/turn:turn-07",
    "dispatch:dispatch-parent"
  ]
}
```

The first cut does not type these edges. Direction and stable endpoints are enough. A later version
may add relations such as `triggered`, `reviews` or `refines` without rewriting the original edge.

Agent observations bind to `group_id`, `seat_id`, `attempt_id` and `activation_id`. A retry keeps its
logical seat and creates a new attempt. Persona names are optional labels, not identity.

## Reference Scout and bus

Every ordinary activation may be offered one bounded `ReferenceScoutTool`. The minimum Scout has
one worker and one reviewer using robot-talks to check reference fit. A larger Scout has two such
groups tensioned by opposed angles—normally support versus refutation—and uses a persisted zig-zag:
each group publishes `v1`, receives the other lens and publishes `v2`. The caller may authorize one
additional cross round; it is never automatic.

Without an explicit user request, an agent may use its Scout when a material conclusion needs context
not already present. Greater human distance narrows the question, result count, budget and normally
selects the two-agent shape. A useful default is to seek references that could contradict the
caller's provisional conclusion.

The Scout is the first small bus slice: it persists seat contributions, group versions,
robot-talks/zig-zag handoffs when present, the final reference bundle and delivery receipt. Delivery
proves tool-boundary presentation, not attention or belief.

Scout agents may search mediated internet sources and a frozen snapshot of research towers. For the
first cut, a tower is any authorized directory whose path contains a segment exactly `research` or
beginning with `research-`. Corpus location never creates another group. Explicit tower
tagging/cataloguing is deferred and tracked in the repository backlog.

## Coarse session identity

Before dispatch/topic/reference detail, the runtime ensures one stable session identity. Any
orchestration or Scout/Probe tool calls an idempotent `ensure_session`: it creates a session only when the
current context lacks one, then every later skill, dispatch, group, seat, attempt and tool run inherits
the same ID.

The authoritative minimal facts are `session.started`, `session.name_changed` and
`session.dispatch_linked`. A rebuildable projection exposes the ID, origin, start time, current
conversation-relevant name and distinct dispatch count. Renaming never changes identity or overwrites
history. Runtime sessions, host conversations and curated Markdown session documents remain distinct
objects connected by references.

## Structured research lineage

The first content-rich descendant of a dispatch is `ResearchRecord`, defined in the focused
[three-level discovery](discovery/session-dispatch-research-records.md). It preserves a raw,
digest-pinned return and addressable question/answer, reference-use/check, problem, claim and
formalization records. A synthesis is another research record linked to the producer records it
synthesizes; it never overwrites them.

Dispatch may declare question/problem/reference scope before execution and later point to immutable
research manifests. Its table may project counts and statuses, but the exact answer, reference
evidence and notation remain owned by Research. Formal notation defaults to `candidate` and carries
a legend, plain-language reading, assumptions and scope; visual mathematical form alone grants no
authority.

## Topic emission

### Agent-owned payload

The complete payload authored by the agent is a JSON array of strings:

```json
[
  "software-engineering",
  "distributed-systems",
  "agent-orchestration",
  "event-sourcing",
  "idempotency",
  "causal-lineage"
]
```

That is the input to a tool such as `deposit_topic_tags(tags: string[])`. The agent does not author an
emission ID, tag ID, mapping, confidence or provenance envelope.

The tool boundary applies only mechanical safety limits: the input must be a JSON array with at most
24 items; every item must be a non-empty valid UTF-8 string of at most 96 bytes; and the encoded array
must not exceed 2 KiB. These limits constrain storage abuse, not vocabulary. Unknown labels are valid.

The [topic-emission skill](../../../.claude/skills/emit-topic-tags/SKILL.md) asks the agent to consider:

- broad domain/context labels, inspired by the open `domain` dimension in Knowledge Taxonomy; and
- granular subject/method labels, similar in specificity to expertise tags in `agent-pool.yaml`.

Both remain ordinary strings in one list. “Broad” and “granular” guide elicitation; they are not
schema fields and the system does not need to classify a tag into either bucket.

Static pool tags are prompt examples and selection priors, not evidence of what happened in an
activation. They are never copied automatically into the emission.

### System-owned envelope

The telemetry boundary stamps the list with trusted runtime lineage:

```json
{
  "schema_version": "apt.topic-observation@1",
  "emission_id": "topic-emission-01",
  "conversation_id": "conversation-01",
  "turn_id": "turn-07",
  "dispatch_id": "dispatch-01",
  "group_id": "group-01",
  "seat_id": "seat-02",
  "attempt_id": "attempt-01",
  "activation_id": "activation-03",
  "observed_at": "2026-07-22T20:00:00Z",
  "tags": [
    "software-engineering",
    "distributed-systems",
    "agent-orchestration",
    "event-sourcing",
    "idempotency",
    "causal-lineage"
  ]
}
```

The stored array preserves the submitted strings and order. The system may also calculate a
mechanical comparison key—Unicode normalization, lowercase and surrounding-space removal—but must
retain the raw value. Semantic stemming, synonym mapping and translation are not capture operations.

An empty list is valid when the agent has no honest topical observation. This makes missing evidence
distinguishable from a failed or skipped tool call.

### Cadence

Emit once near the end of every activation, including resumed activations. This gives topic drift a
time axis and avoids pretending the first activation describes all later work. Retries receive new
attempt and activation identities, so their observations do not overwrite earlier ones.

### Informational isolation

When multiple seats work on the same round, no seat sees another seat's current-round topic list
before depositing its own. This is informational isolation, not statistical independence: seats may
share a model, training, prompt and examples. Analyses must record and stratify model/persona
composition rather than describe the samples simply as independent agents.

## Relation to Knowledge Taxonomy

The inspected local Knowledge Taxonomy v2.2 separates an open `domain` facet from upper types and
other orthogonal facets. `domain` answers which field something comes from and is the relevant model
for broad topical tags.

The upper types (`Entity`, `Event`, `Process`, `Quality`, `Role`, `Disposition`,
`InformationObject`, `Proposition`) and facets such as `nature`, `temporality`,
`source_confidence` and `content_certainty` do not answer “what is this work about?”. They should not
be injected into the topic list merely to make it look taxonomic. They remain candidates for a future
classification layer if evidence produces that requirement.

The Knowledge Taxonomy repository was not present as a sibling checkout and was not publicly
accessible at the tested organization URLs. This comparison used the existing local temporary clone
at `C:\Users\victo\AppData\Local\Temp\knowledge-taxonomy-clone`, principally `schema/v2.2.md`,
`docs/system-tagging-engine.md` and `decisions/09-facet-value-enumeration.md`.

## Observed vocabulary and the emergent lens

The system may maintain a rebuildable projection over the observations:

- distinct raw and mechanically normalized strings;
- occurrence count by conversation, dispatch, seat and activation;
- co-occurrence between exact normalized strings;
- first and last observation;
- supporting emission IDs for every aggregate.

This projection is an observed vocabulary, not a registry. Agents enlarge it merely by depositing
new strings. No label becomes canonical, approved or equivalent by appearing in it.

The first “lens” is likewise just a view over exact observed strings: shared terms, per-seat terms,
co-occurrence and temporal additions/removals. Every projected item points back to supporting
emissions. Equivalence discovery can later be tested over accumulated evidence, but it must create a
new derived record and never rewrite the original lists.

## Source, paper and internal-reference observations

Paper/source capture belongs at the mediated search, open or fetch boundary rather than in agent
prose. Internal file references opened through a Scout use the same observation boundary, with a
workspace-relative locator plus content digest instead of a mutable path alone. The tool deposits an
observation when it actually returns or exposes a source:

```json
{
  "schema_version": "apt.source-observation@1",
  "source_observation_id": "source-observation-01",
  "dispatch_id": "dispatch-01",
  "seat_id": "seat-02",
  "attempt_id": "attempt-01",
  "activation_id": "activation-03",
  "action": "opened",
  "locator": "https://example.org/paper",
  "title_observed": "Observed title",
  "doi_observed": null,
  "observed_at": "2026-07-22T19:58:00Z"
}
```

Search-result visibility is distinct from opening or reading. Bibliographic metadata is observed,
not silently corrected. Full text and copyrighted content remain outside telemetry.

Each ScoutRun commits its own immutable reference bundle before delivery. At dispatch close,
the system may build a derived manifest of activation, topic-emission, Scout bundle and
source-observation references. The agent does not have to reproduce the bibliography in its final
answer for telemetry to exist.

The projection distinguishes:

- `observed_by_probe_operation`: tool operation that exposed the reference;
- `requested_by_activation`: ordinary activation that asked for the context;
- `delivered_to`: caller exchange or continuation that received the committed bundle;
- `cited_by`: accepted contributions or synthesis artifacts that explicitly referenced it.

The first three are host-observable. `cited_by` is an attributed claim of use, not evidence of
cognitive influence. Partial, contradictory and empty Scout results remain in provenance.

## Failure semantics

| Condition | Required behavior |
|---|---|
| Topic tool not called | Record capture as `missing`; do not synthesize profile tags. |
| Agent honestly reports no topics | Persist an empty list as a successful observation. |
| Duplicate string in one list | Preserve raw input; a comparison projection may de-duplicate with trace. |
| Previously unseen string | Accept it normally. |
| Similar-looking strings | Keep both; do not infer equivalence during capture. |
| Source tool fails before returning a source | Record tool failure, not a paper observation. |
| Retry occurs | Create a new attempt/activation observation; never overwrite. |
| Lineage is unavailable | Preserve explicit unresolved lineage rather than fabricate a parent. |
| Scout asks for a wider path/domain than authorized | Reject the widening and record it; never search anyway. |
| Scout budget is exhausted | Return `budget_insufficient` or a committed partial bundle with explicit residue. |
| Scout persistence fails before commit | Do not expose unlogged references to the caller. |
| One Scout seat fails | Preserve a typed partial; do not call it reviewed consensus. |

## Empirical work

The probes in [`probes/`](probes/README.md) were saved before implementation. Their registry-specific
assumptions came from the superseded v0.2 design. The separately versioned
[v0.3 raw-tag execution amendment](probes/v0.3-raw-tag-execution-amendment.md) preserves those files as
history while preregistering how agreement, noise and lens comparisons run on raw strings. The old
within-activation drift probe is inapplicable to the chosen close-only cadence; natural drift across
resumed activations is descriptive until a new controlled protocol is preregistered.
P003 becomes evidence about whether vocabulary management is warranted; it does not gate capture on
a seed registry.

Useful first measurements are:

- tag count and capture latency per activation;
- exact-string overlap for independent agents on the same task;
- proportion of new strings over time;
- coarse/granular mix under a frozen external rubric, with blind annotation and agreement reported,
  without changing stored payloads;
- source-observation completeness at the mediated-tool boundary;
- lineage replay from conversation to dispatch, activation, tag and source observations.

## Minimal implementation sequence

1. Mint or accept `conversation_id` and `turn_id` at the host boundary.
2. Add those IDs and untyped directed `origin_refs` to dispatch telemetry.
3. Add `deposit_topic_tags(tags: string[])` with the system-owned envelope.
4. Invoke it once at the end of every agent activation using the pinned prompt.
5. Instrument mediated paper/search/open and bounded internal-read tools to deposit source
   observations.
6. Add `ensure_session` plus the append-only coarse session facts and projection.
7. Freeze the Session–Dispatch–Research identities and raw-first research contracts/fixtures.
8. Capture exact final returns and link host source observations to attributed reference uses/checks.
9. Add the Reference Scout request/contribution/bundle/receipt bus slice, preserving frozen v1
   `reference-probe`, `probe_id` and `probe.*` identifiers at the wire boundary.
10. Persist before acknowledgement and return only committed reference bundles.
11. Build per-session, per-dispatch, per-research and per-conversation read projections.
12. Run the saved empirical probes before introducing semantic equivalence or registry machinery.

## Non-goals and deferred decisions

- no canonical topic registry;
- no tag IDs or lifecycle states;
- no model-based synonym mapper in the capture path;
- no forced use of profile tags or Knowledge Taxonomy facets;
- no claim that tag overlap proves consensus;
- no typed causal-edge vocabulary in the first cut;
- no knowledge promotion or claim adjudication;
- no second runtime beside `agents-communication-infra`.
- no claim that delivery proves attention, belief or causal influence;
- no ambient workspace/domain discovery by ordinary agents when reference scope is absent;
- no group partition by internal/external source or repository path;
- no implementation or final-answer work by Scout agents;
- no automatic promotion of research claims or mathematical/logical notation;
- no independently editable session registry beside the journal/bus projection.

After enough observations exist, a separate research task may test whether agents can propose useful
equivalence clusters. That future mechanism should consume immutable emissions and produce reversible,
versioned projections. It is not required to begin collecting evidence.

## Connections

| Document | Type | Description |
|---|---|---|
| [Session–Dispatch–Research records](discovery/session-dispatch-research-records.md) | `grounds` | Focused discovery that owns the structured research level introduced in v0.7. |
| [Coarse session registry](session-registry.md) | `grounds` | Owns the start-time session facts consumed by the three-level model. |
| [Reference Scout tool](probes/reference-scout-tool.md) | `grounds` | Owns host-observed acquisition/access evidence reused by research reference uses. |

## Appendix — Changelog

| Version | Date | Change |
|---|---|---|
| 0.7.0 | 2026-07-23 | Added the focused Session–Dispatch–Research companion and projected research lineage. The companion's APT-D decisions remain discovery-stage and are not locked by a SPEC. |
