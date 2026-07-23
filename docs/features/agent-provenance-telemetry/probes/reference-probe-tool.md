---
feature: agent-provenance-telemetry
artifact: reference-probe-tool
status: proposed
version: 0.4.0
created: 2026-07-23
last_updated: 2026-07-23
---

# Reference-probe tool

## Decision proposed

`reference-probe` is a small, session-bound multi-agent tool with one purpose: find, check and
persist recommendations of where the caller should look for relevant context. It may search
authorized internal research towers and mediated external sources. It does not answer the caller's
question, adjudicate the hypothesis, edit source material or start a full research project.

The conversational aliases are `probe` and `sonda`.

## Shapes

Assumption recorded: “at least two agents, one worker and two reviewers” was read as a counting typo.
The minimum below is one worker plus one reviewer. If two reviewers were intended, the minimum shape
must be revised from two to three agents.

### Small probe — two agents

```text
probe group
  worker   — finds candidate references
  reviewer — opens/checks them and challenges relevance
       ⇅ robot-talks
  reviewed reference recommendations
```

This is the default for a precise request, especially when invoked by an agent farther from the
human. The worker and reviewer have distinct functions; the reviewer does not merely rephrase the
worker.

### Tensioned probe — four agents

```text
group A: worker + reviewer  ⇄  group B: worker + reviewer
             robot-talks       robot-talks
                       zig-zag
```

The two groups receive tensioned angles. The default axis is `supports` versus `refutes` the supplied
hypothesis, but another explicit axis is valid when it predicts a meaningful difference in which
references will be recommended. Corpus location is not a tension axis: internal versus external,
Lean versus `research/**`, and similar path partitions do not create groups.

## Tensioned exchange

The four-agent probe follows this bounded sequence:

1. Both groups research independently from the same frozen objective and source-authority snapshot.
2. Inside each group, worker and reviewer use robot-talks to produce evaluation `v1`: recommended,
   partial and rejected references.
3. The bus reveals each group's `v1` to the other group through a persisted zig-zag handoff.
4. Each group evaluates again through the other group's lens and publishes `v2` plus the delta from
   `v1`.
5. The calling orchestrator receives both `v2` bundles and surviving disagreement.
6. The caller either evaluates them directly or authorizes one second cross-group round when a
   concrete unresolved tension justifies the cost.

The second cross-group round is never automatic. The first cross-lens reevaluation is mandatory for
the four-agent shape. “Robot-talks” and “zig-zag” retain their repository meanings and require a
probe-specific bounded recipe/profile before runtime enablement; they are not decorative labels.

## Invocation

The caller supplies:

```json
{
  "objective": "Recommend references bearing on whether ownership should terminate the work",
  "hypothesis": "An existing owner makes the proposed work unnecessary",
  "shape": "small",
  "source_mode": "internal-and-external",
  "precision_hint": "Look especially for already-deployed owners"
}
```

`shape` is `small` or `tensioned`. An explicit user request may select either. Without an explicit
shape, the host chooses the smallest shape that can answer the reference need; an agent-initiated
probe normally receives `small`. A caller may propose the larger shape when opposition is materially
useful, but does not silently spend it.

`source_mode` is `internal`, `external` or `internal-and-external`. Source class is recorded per
reference and never produces an extra group.

The caller supplies at most `shape` (or an untrusted `requested_profile_id` hint). The host resolves
the authorized profile version and digest from the registry, then validates shape, recipe, round
ceilings and budget against that profile. A trusted digest is never caller-authored.

The host stamps:

- mandatory `session_id`;
- `probe_id` and operation/idempotency identity;
- `dispatch_id`, `group_id`, `seat_id`, `attempt_id` and `activation_id` when present;
- caller human distance;
- authorized research-tower snapshot and external tool/domain policy;
- agent identities, models and per-seat budgets;
- robot-talks/zig-zag recipe version and round ceilings;
- exact ACI `protocol_profile_id`, version and digest;
- timestamps and tool version.

The caller cannot assert lineage, widen authority or select a larger budget than its inherited
session/run remainder.

When `dispatch_id` is present, the host resolves its sole `session.dispatch_linked` edge and requires
the stamped `session_id` to match exactly. An unlinked dispatch or mismatch is rejected before any
probe event is published. A probe without a dispatch continues to use its direct session lineage.

## Distance

Greater human distance narrows objective, tokens, returned reference count and available shape:

| caller distance | default shape | expectation |
|---:|---|---|
| `0` | `small`; may propose `tensioned` | bounded first-wave reference acquisition |
| `1` | `small` | one explicit uncertainty or counter-conclusion |
| `>= 2` | `small` with lower caps | one narrow fact that could change the caller's answer |

Distance is one input to a cumulative session/run budget. If even the two-agent shape cannot fit, the
tool returns `budget_insufficient`.

## Research towers and external sources

For the first implementation, a research tower is coarsely discovered under authorized repository
roots when a directory segment is exactly `research` or begins with `research-`. The host freezes the
resolved directory list as `research_tower_snapshot_ref` before launching agents so the scope is
auditable and replay does not depend on a later filesystem state.

This path convention is temporary. Research towers need explicit tags, identifiers, descriptions,
authority and coverage metadata; that work is parked separately in the repository backlog.

The same probe may also use mediated internet research. Every recommendation records:

- internal or external source class;
- observed locator and stable identifier/content digest;
- access state (`returned`, `opened`, `content_accessed`);
- bounded span/symbol/navigation anchor;
- which probe agent found it;
- which probe reviewer evaluated it;
- angle and evaluation status;
- short reason the caller may want to inspect it.

The probe returns navigation recommendations, not copied corpora. Full copyrighted text and secrets
are excluded.

## Bus slice

Reference-probe is the first deliberately bounded, preregistered slice of the agent bus. It exercises
multiple seats, durable publication, reveal, handoff, delivery and replay while keeping the semantic
output narrow.

```text
probe.requested
  → probe.group.started
  → probe.contribution.published
  → probe.group.v1.committed
  → tensioned-shape cross-group reveal / zig-zag
  → probe.group.v2.committed
  → probe.bundle.committed
  → durable receipt
  → probe.bundle.delivered
```

The small shape omits cross-group events and commits one reviewed group result. The tensioned shape
commits both pre-reveal `v1` results, exact reveal/handoff manifests, post-lens `v2` results and any
caller-authorized second round.

No agent writes directly to the bus store. Publications go through the bus boundary, which stamps
session/probe/seat/attempt identity, validates payloads and persists before acknowledging.
Every request, lifecycle event and committed bundle is stamped with the exact protocol profile ID,
version and digest. That profile must be registered with the ACI contract before the slice is
enabled; a missing or mismatched profile is rejected before publication.

A crash after commit and before response is recovered through the same operation identity. An
identical retry returns the same receipt; a changed request under the same key conflicts.

This slice reuses the journal, artifact, receipt and group-deliberation contracts of
`agents-communication-infra`. It must not become a second bus or runtime.

## Output bundle

```json
{
  "schema_version": "apt.reference-probe-result@1",
  "session_id": "session-01",
  "probe_id": "probe-01",
  "protocol_profile_id": "aci-profile:apt-reference-probe-small",
  "protocol_profile_version": "1",
  "protocol_profile_digest": "sha256:...",
  "shape": "small",
  "objective": "Recommend references bearing on the ownership hypothesis",
  "research_tower_snapshot_ref": "artifact-...",
  "recommendations": [
    {
      "recommendation_id": "recommendation-01",
      "reference_id": "ref-01",
      "source_class": "internal",
      "locator_observed": ".claude/skills/research/SKILL.md",
      "content_digest": "sha256:...",
      "access_state": "content_accessed",
      "navigation_anchor": "Ownership is a label, not a verdict.",
      "source_observation_refs": ["source-observation:01"],
      "found_by_seat_id": "probe-worker-01",
      "evaluated_by_seat_id": "probe-reviewer-01",
      "angle": "refutes",
      "evaluation": "recommended",
      "why_inspect": "May refute the premise that ownership terminates research."
    }
  ],
  "rejected_reference_ids": [],
  "surviving_disagreement": [],
  "committed_event_id": "event-...",
  "bundle_digest": "sha256:..."
}
```

The caller receives recommendations of where to inspect and why. The probe does not supply the
caller's final conclusion.

## Session and downstream research lineage

Every probe requires `session_id`, including probes launched outside a dispatch. When a later
research dispatch, research artifact or longer investigation arises from a probe recommendation, it
records:

```json
{
  "origin_refs": [
    "session:session-01",
    "probe:probe-01",
    "probe-bundle:sha256:..."
  ]
}
```

This is provenance, not ownership: the later research remains its own dispatch/artifact, while the
link answers which probe exposed the path that caused it.

The session projection may count probes and probe-originated dispatches later. Its minimal first
version still needs only session identity, origin, start time, current name and dispatch count.

## Failure semantics

| condition | result |
|---|---|
| no relevant reference found | Commit an empty reviewed bundle with searched-scope residue. |
| one probe seat fails | Commit a typed partial only if policy permits; never present it as reviewed consensus. |
| internal or external channel partially fails | Preserve surviving recommendations plus typed channel failure. |
| requested scope exceeds authority | Reject before acquisition and record the denied request. |
| persistence fails before commit | Do not deliver unlogged recommendations. |
| response is lost after commit | Retry returns the same receipt and bundle. |
| optional second round is not authorized | Stop after mandatory `v2`; caller evaluates. |

## Non-goals

- no implementation, specification or final-answer work;
- no general web/repository dump;
- no group split by source corpus;
- no automatic second zig-zag round;
- no claim adjudication or knowledge promotion;
- no direct source-tree writes;
- no second bus beside `agents-communication-infra`.

## Implementation order

1. Establish coarse session identity before probe registration.
2. Freeze small/tensioned recipes, response schemas, budgets and research-tower snapshots.
3. Implement the append-before-ack bus path and stable receipts.
4. Run the two-agent small shape against bounded internal towers.
5. Add mediated external acquisition to the same shape.
6. Add the four-agent tensioned shape, sealed `v1`, zig-zag reveal and `v2`.
7. Add caller-authorized second-round control.
8. Project session → probe → reference → later research lineage.
9. Test retries, crashes, partial seats, unauthorized scope, replay and lost delivery.

## Connections

| Document | Type | Description |
|---|---|---|
| [Session–Dispatch–Research records](../discovery/session-dispatch-research-records.md) | `grounds` | Supplies host-observed source/access evidence consumed by ResearchReferenceUse. |

## Appendix — Changelog

| Version | Date | Change |
|---|---|---|
| 0.4.0 | 2026-07-23 | Binds request, events and result bundle to an exact ACI protocol profile and adds recommendation/source-observation lineage. |
| 0.3.1 | 2026-07-23 | Added the inverse provenance edge to the focused research-record discovery; probe semantics are unchanged. |
