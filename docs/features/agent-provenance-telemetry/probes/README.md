---
feature: agent-provenance-telemetry
artifact: empirical-probe-registry
status: preregistered
version: 0.2.0
created: 2026-07-22
last_updated: 2026-07-22
---

> **v0.3 execution amendment:** preserve these preregistered protocols as written, but do not build
> their assumed seed registry. Initial executions use raw emitted strings and a declared mechanical
> comparison key. Registry-specific outcomes are reported as inapplicable; P003 instead gathers the
> evidence needed to decide whether vocabulary management is warranted. This amendment was made
> before any probe run and does not change the saved thresholds after observing results.

The executable amendment is [v0.3 raw-tag execution amendment](v0.3-raw-tag-execution-amendment.md).

# Agent Provenance Telemetry — empirical probes

The initial six probes were saved before the feature discovery so that it could not choose metrics or
success criteria after seeing favorable results. The amended registry tests whether per-agent topic snapshots are
stable, informative, vocabulary-compatible and cheap enough to capture. They do not promote tags to
knowledge, authorize dispatches or change the runtime gate.

P001–P006 were preregistered before discovery v0.1.0. P007 was added in v0.2.0 after the owner chose a
system-governed tag registry and isolated agent views, but before any empirical run. Its
metrics and decision thresholds therefore remain prospective rather than fitted to results.

## Meaning of Probe in this registry

These files are preregistered empirical Probe protocols: they observe a target under a declared
method and decision lens. In the agent-tool taxonomy, the reusable capability is `ProbeTool`
(displayed as **Sonda** in pt-BR), one execution is a `ProbeRun` with an explicit `lens_ref`, and its
owned results are `observations[]`.

They are not Reference Scout runs. Reference Scout uses
`ReferenceScoutTool -> ScoutRun -> recommendations[]` to find where to look. Probe records what was
observed through a lens. Neither family transforms its target or promotes its output to fact, and
Reference Scout is not declared a Probe subtype in this version. Frozen `probe_id`, `probe.*` and
`reference-probe` identifiers attached to the historical Scout v1 protocol remain compatibility
identifiers and do not change this distinction.

## Shared evidence boundary

- A topic snapshot is testimony: it records what one agent said it was working on at one activation.
- `profile_field`, `profile_tags`, `dispatch_topic_tags`, agent-emitted terms, system-resolved tags and
  adjudicated taxonomy tags are distinct surfaces and must never be merged in raw evidence.
- The harness gives no tagger another tagger's current-round emission before both are sealed. A
  contaminated round remains evidence about interaction but cannot support isolation claims.
- Conversation, turn, dispatch, group, seat, attempt, activation sequence and timestamps are stamped
  by the harness. An agent cannot supply or override them.
- Unknown terms are retained as `unmapped_terms` in a separate pinned resolution; the harness never
  silently invents a canonical tag or inserts residue into the raw emission.
- Exact string agreement is measured only after deterministic normalization: Unicode NFC, lowercase,
  trim, internal whitespace to `-`, repeated `-` collapsed and no semantic synonym expansion.
- Every run pins the input fixture, prompt, model/provider, vocabulary snapshot and probe version by
  digest. Results from different pins are not pooled silently.

## Common records

Raw agent emission:

```json
{
  "probe_version": "0.2.0",
  "fixture_ref": "fixture:sha256:...",
  "conversation_id": "harness:conversation:...",
  "turn_id": "harness:turn:...",
  "dispatch_id": "harness:dispatch:...",
  "group_id": "taggers",
  "seat_id": "seat-1",
  "attempt_id": "attempt-1",
  "activation_seq": 1,
  "trigger": "initial",
  "capture_phase": "free",
  "observed_terms": ["event-sourcing", "receipt-gated-publication"],
  "writer_observed_at": "2026-07-22T00:00:00Z",
  "emission_digest": "sha256:..."
}
```

Separate system resolution:

```json
{
  "emission_ref": "topic-emission:01...",
  "registry_version": "tag-registry:sha256:...",
  "resolver_version": "exact-alias-resolver/0.1.0",
  "system_resolved_tag_ids": ["tag:event-sourcing"],
  "unmapped_terms": ["receipt-gated-publication"],
  "resolution_digest": "sha256:..."
}
```

The example values are illustrative. A harness run must mint fresh IDs and canonical bytes. The
emission digest never includes system resolution or residue.

## Probe registry

| Probe | Question | Primary decision |
|---|---|---|
| [APT-P001](APT-P001-inter-tagger-agreement.md) | What overlap and divergence do isolated agents produce from the same input? | Whether agreement supports a shared core and what remains for a multi-perspective lens. |
| [APT-P002](APT-P002-topic-drift.md) | Does start/close capture reveal meaningful topic drift? | Whether more than one snapshot per activation is justified. |
| [APT-P003](APT-P003-vocabulary-coverage.md) | How much observed language maps to existing vocabularies without forced fit? | Whether to reuse, vendor, extend or keep vocabularies separate. |
| [APT-P004](APT-P004-capture-cost-noise.md) | Which capture cadence provides information without ritual noise or task degradation? | Default cadence for the compatibility slice. |
| [APT-P005](APT-P005-source-capture.md) | Can the system account for papers actually accessed by each agent without trusting a hand-written bibliography? | Whether source capture is gateway-derived, agent-deposited or hybrid. |
| [APT-P006](APT-P006-lineage-replay.md) | Can every observation resolve to conversation/turn/dispatch/seat/attempt and replay without duplication? | Whether the provenance spine is structurally usable. |
| [APT-P007](APT-P007-emergent-lens.md) | Do sealed isolated views yield a stable and attributable lens without erasing lexical disagreement? | Whether a lens projection is justified and which equal-information baseline it must beat. |

## Shared fixture rule

The initial pilot uses 12 immutable, sanitized task bundles: four `research`, four `review` and four
`code`/planning bundles, sampled from existing dispatches without exposing secrets. Each bundle
contains the exact task prompt, allowed context excerpt and expected dispatch type, but excludes prior
tags and the identity of the original agent. If 12 eligible bundles cannot be produced, the run is
reported as blocked rather than silently shrinking or changing the sample.

## Result location

Results belong under `probes/results/<probe-id>/<run-id>/`. Raw emissions, normalized sets, metrics,
environment pins and limitations must remain separate files. A summary never replaces raw evidence.

## Promotion rule

No single probe promotes the feature. The discovery may propose a compatibility implementation only
after all seven probes have either passed their decision rules or produced an explicit narrower design
that does not depend on the failed claim.
