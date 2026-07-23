---
feature: agent-provenance-telemetry
artifact: reference-scout-tool
status: proposed
version: 0.5.0
created: 2026-07-23
last_updated: 2026-07-23
---

# Reference Scout tool

## Decision proposed

`reference-scout` is a small, session-bound multi-agent tool with one purpose: find, check and
persist recommendations of where the caller should look for relevant context. It may search
authorized internal research towers and mediated external sources. It does not answer the caller's
question, adjudicate the hypothesis, edit source material or start a full research project.

`reference-probe`, `probe` and `sonda` are legacy conversational aliases. New product surfaces,
runtime operation names and projection names use Scout terminology. Already frozen v1 wire,
schema/profile and APT concept identifiers containing `probe` or `reference-probe` remain valid
compatibility identifiers until an explicit versioned migration; they do not rename the product
concept back to Probe.

## Naming boundary

Scout means bounded reconnaissance: it finds and checks references and returns navigation
recommendations. It is not a generic measurement probe and it does not compute a privileged domain
metric. The experimental ACI executable currently located at
[the publication spike](../../agents-communication-infra/experiments/bus-publication-probe/README.md)
is a distinct
**publication-receipt spike**: it tests durable publish/receipt mechanics and is not this tool.

## Classification and ownership

The host-callable Scout surface is an **Interface** coordinating a bounded **Workflow**. ACI owns
the executable bus, journal, canonicalization, protocol registry and receipt boundary. APT owns only
the receipt-gated **Mapping** from an already committed recommendation into typed research lineage.
This document does not create a second runtime owner.

## Compatibility table

| Surface | Canonical name in this version | Compatibility rule |
|---|---|---|
| Product, prose and new UI | Reference Scout / `reference-scout` | Do not introduce new product-facing `probe` labels. |
| Frozen v1 wire evidence | `probe_id`, `probe.*`, `apt.reference-probe-result@1`, `probe:*`, probe seat/group labels | Preserve byte/semantic compatibility; do not mass-rename. |
| Frozen v1 APT concept IDs | `ProbeRecommendationRef`, `AppendReferenceProbeLineage`, `ReferenceProbeLineageAppended` | Preserve until an explicit versioned SPEC migration. |
| New experimental E0 operations/projections | `start_reference_scout`, `publish_scout_contribution`, `reference_scout_runs`, `scout_run_id` | Local shadow vocabulary only; does not assert an ACI wire migration. |
| Technical publication experiment | publication-receipt spike | Existing directory name `bus-publication-probe` is a historical path, not product vocabulary. |

## Shapes

Assumption recorded: “at least two agents, one worker and two reviewers” was read as a counting typo.
The minimum below is one worker plus one reviewer. If two reviewers were intended, the minimum shape
must be revised from two to three agents.

### Small scout — two agents

```text
scout group
  worker   — finds candidate references
  reviewer — opens/checks them and challenges relevance
       ⇅ robot-talks
  reviewed reference recommendations
```

This is the default for a precise request, especially when invoked by an agent farther from the
human. The worker and reviewer have distinct functions; the reviewer does not merely rephrase the
worker.

### Tensioned scout — four agents

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

The four-agent scout follows this bounded sequence:

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
Scout-specific bounded recipe/profile before runtime enablement; they are not decorative labels.

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
Scout normally receives `small`. A caller may propose the larger shape when opposition is materially
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
Scout event is published. A Scout without a dispatch continues to use its direct session lineage.

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

The same scout may also use mediated internet research. Every recommendation records:

- internal or external source class;
- observed locator and stable identifier/content digest;
- access state (`returned`, `opened`, `content_accessed`);
- bounded span/symbol/navigation anchor;
- which Scout agent found it;
- which Scout reviewer evaluated it;
- angle and evaluation status;
- short reason the caller may want to inspect it.

The Scout returns navigation recommendations, not copied corpora. Full copyrighted text and secrets
are excluded.

## Bus slice

Reference Scout is the first deliberately bounded, preregistered slice of the agent bus. It exercises
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
  "protocol_profile_id": "apt.reference-probe-lineage",
  "protocol_profile_version": "1",
  "protocol_profile_digest": "sha256:<pending-aci-owner-registration>",
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

The profile values above identify the real pending v1 profile family but the digest placeholder is
illustrative. The Scout is not ACI-enabled until the exact registered digest and owner receipt
verify.

The caller receives recommendations of where to inspect and why. The probe does not supply the
caller's final conclusion.

## Session and downstream research lineage

Every scout requires `session_id`, including scouts launched outside a dispatch. When a later
research dispatch, research artifact or longer investigation arises from a scout recommendation, it
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
link answers which scout exposed the path that caused it. The legacy `probe:*` origin-ref namespace
is preserved for frozen v1 evidence; new experimental E0 records use `scout:*`.

The session projection may count Scouts and Scout-originated dispatches later. Its minimal first
version still needs only session identity, origin, start time, immutable initial name and dispatch
count. A current-name/rename projection is post-L0.

## Failure semantics

| condition | result |
|---|---|
| no relevant reference found | Commit an empty reviewed bundle with a typed `search_scope_summary`; `comparability_state` is exactly `comparable`, `incommensurable` or `count_capped`, never a numeric residue score. |
| one probe seat fails | Commit a typed partial only when the bound profile sets `partial_commit_policy=allow_typed_partial`; `forbid` rejects commit. A partial is never presented as reviewed consensus. |
| internal or external channel partially fails | Preserve surviving recommendations plus typed channel failure. |
| requested scope exceeds authority | Reject before acquisition and record the denied request. |
| persistence fails before commit | Do not deliver recommendations without an accepted `probe.bundle.committed` event and receipt whose member/event IDs and bundle digest verify. |
| response is lost after commit | Retry returns the same receipt and bundle. Delivery appends `probe.bundle.delivered` only after verifying that commit evidence. |
| optional second round is not authorized | Stop after mandatory `v2`; caller evaluates. |

## Non-goals

- no implementation, specification or final-answer work;
- no general web/repository dump;
- no group split by source corpus;
- no automatic second zig-zag round;
- no claim adjudication or knowledge promotion;
- no direct source-tree writes;
- no second bus beside `agents-communication-infra`.

## Gate and acceptance status

- Full Scout workflow status: `proposed`.
- Experimental E0 status: `shadow-only`; it may persist local lifecycle evidence but does not
  launch acquisition agents or claim ACI-compatible receipts.
- Runtime and mutation gates remain blocked.
- Small-profile enablement requires the exact ACI profile ID/version/digest, owner registration
  receipt, executable append-before-ack evidence, deterministic retry/conflict tests and the
  governing mutation-gate approval.
- Tensioned shape enablement additionally requires frozen reveal/handoff manifests, seat-failure
  policy and bounded-round tests; E0 supplies none of these.

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
| [Feature discovery — Reference probe and bus](../discovery.md#reference-probe-and-bus) | `grounds` | Introduces the bounded acquisition workflow and authority boundary. |
| [Feature specification](../specs/SPEC.md#capability-boundaries) | `specified-by` | Fixes Reference Scout lineage ownership and the frozen v1 compatibility surface. |
| [ACI receipt-gated deliberation](../../agents-communication-infra/specs/SPEC.md#receipt-gated-deliberation) | `depends-on` | Owns publication, profile and receipt execution. |
| [Session–Dispatch–Research records](../discovery/session-dispatch-research-records.md) | `consumed-by` | Downstream ResearchReferenceUse consumes host-observed Scout evidence. |

## Appendix — Changelog

| Version | Date | Change |
|---|---|---|
| 0.5.0 | 2026-07-23 | Renamed the product concept to Reference Scout; preserved frozen `reference-probe` schema/profile aliases and distinguished the ACI publication-receipt spike. |
| 0.4.0 | 2026-07-23 | Binds request, events and result bundle to an exact ACI protocol profile and adds recommendation/source-observation lineage. |
| 0.3.1 | 2026-07-23 | Added the inverse provenance edge to the focused research-record discovery; probe semantics are unchanged. |
