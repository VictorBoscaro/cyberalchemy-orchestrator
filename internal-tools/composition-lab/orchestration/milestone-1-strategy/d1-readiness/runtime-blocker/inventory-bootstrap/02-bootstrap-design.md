---
artifact_kind: bounded-inventory-bootstrap-design
status: proposed-blocked-for-execution
date: 2026-08-13
scope: milestone-1-D1-descriptive-lens-use-inventory
capability_owner: inventory
registration: forbidden
inventory_root: .arcanum/inventory
runtime_shape: owner-directed-unregistered-connectionless
review_basis:
  - 01-source-location.md
  - 03-bootstrap-adversary.md
  - ../10-final-route-decision.md
  - ../11-inventory-governance.md
---

# Minimal bounded Inventory bootstrap for D1

## Disposition

**CONDITIONAL GO to ratify and fixture this design. BLOCK for execution, Inventory skill mutation,
generated-surface synchronization, D1 launch, or LIVE registration.**

The design removes the connected extractor -> assembler topology that the current runtime cannot
materialize. It uses exactly two seats in strict host-controlled order:

1. one `extractor-writer`, solely authorized to read the frozen corpus and write the D1 candidate
   read model; then
2. one independent `coverage-auditor`, authorized only to read the frozen corpus and the writer's
   frozen outputs and to return `PASS | BOUNDED_CORRECTIONS | BLOCK`.

There is no inter-seat return edge and no `connections` declaration. The only handoff is a
predeclared artifact path set frozen by hash after the writer terminates. This deliberately gives up
independent parallel extraction. D1 needs a reproducible description and an independent
completeness check; it does not need multiple epistemic judgments, novelty adjudication, or a
conversation among lenses. If later work requires several extractors whose returns must be merged,
this bootstrap is inapplicable and the connected-runtime blocker returns.

The canonical Inventory source has been found in the sibling Arcanum checkout, but local generated
surfaces are stale and their runtime metadata is inconsistent. That is ownership evidence, not
execution authority. This proposal does not amend or synchronize any skill surface.

## Objective, decision, and evidence of success

### Objective

Produce a durable, source-backed, mechanically queryable description of where the frozen D1 corpus
records perspective-like configurations, traces, explicit selector-bounded non-observations,
ambiguities, contradictions, and duplicate representations. Preserve enough trace and residue for
later Research work without deciding what a lens is or whether composition caused an effect.

### Decision

Adapt the already-installed `.arcanum/inventory/` package as the sole Inventory system. Keep
Composition Lab's milestone/session artifacts in their accepted tree and reference them from
Inventory; create no second schema, ID namespace, index, log, raw store, or synchronization loop
under `internal-tools/composition-lab/`.

The route is a capability-owned, bounded, unregistered bootstrap, following only the narrow local
precedent that an unregistered owner-directed workflow terminates inside its capability
([discovery-writing, Orchestration and Confirmation](../../../../../../../.codex/skills/discovery-writing/SKILL.md#orchestration-and-confirmation);
[routing, Select the capability](../../../../../../../.agents/skills/domainspec-subagents-strategy/SKILL.md#select-the-capability)).
It is not a dispatch type, ledger projection, ACI receipt, or new lifecycle.

### Evidence required before a success claim

Mechanical success requires all of the following:

- every frozen source x control obligation has one cited candidate observation,
  `not_observed_within_selector`, or unresolved gap;
- source hashes remain unchanged;
- all generated D1 records validate against the existing Inventory boundary and appear in both
  `.arcanum/inventory/index.md` and `.arcanum/inventory/index.json`;
- `index.json` parses and its validation boundary remains `inventory-read-model-only`;
- conflicting assignments and duplicate representations retain separate traces and residue;
- the independent auditor accepts coverage, provenance, immutability, and package boundaries; and
- the capability-local completion report truthfully distinguishes workflow evidence from durable
  ACI/ledger evidence.

No mechanical PASS supports a definition of lens/composition, truth beyond cited sources, causal
effect, novelty, soundness, ontology promotion, or GO/KILL judgment.

## Evidence ledger: fact, inference, proposal, gap

| class | statement | source |
|---|---|---|
| FACT | The canonical source exists at `C:/Users/victo/Arcanum/arcana/inventory/SKILL.md`; it is clean in the inspected sibling checkout. | [01 § Verdict](01-source-location.md#verdict) |
| FACT | `.agents`, `.codex`, and `.claude` Inventory skill files are byte-identical stale projections of an older canonical revision; their shared `runtime: claude` metadata is wrong or unexplained outside `.claude`. | [01 § Direct evidence](01-source-location.md#direct-evidence) |
| FACT | Selective sync currently covers `.agents` and `.claude`, not the tracked repo-local `.codex/skills` surface. | [01 § Unresolved gaps](01-source-location.md#unresolved-gaps) |
| FACT | `.arcanum/inventory/` is already installed; it declares one machine index, one human index, one append-only log, in-place source references, and candidate/non-authority records. | `.arcanum/inventory/{README.md,schema.md,index.json,log.md}` |
| FACT | Current legacy-managed compilation rejects non-empty connections; lower-level binding-output primitives do not constitute a connection scheduler. | [runtime diagnosis § Evidence](../01-runtime-diagnosis.md#evidence) and [§ Decision for D1a](../01-runtime-diagnosis.md#decision-for-d1a) |
| FACT | Inventory owns source-backed candidate records, trace, residue, indexes, lint, validation, and non-authority handoffs; Definitions, Ontology Vault, and Research own stronger judgments. | [Inventory § Authority rule](../../../../../../../.codex/skills/inventory/SKILL.md#authority-rule) |
| INFERENCE | Durable lookup and revalidation are plausibly useful to later Milestone work, but usefulness has not yet passed the human reuse gate. | [10 § Premises and the initial reuse gate](../10-final-route-decision.md#premises-and-the-initial-reuse-gate) |
| INFERENCE | One writer plus an independent auditor is the smallest shape that avoids unsupported inter-seat data delivery while preserving independent coverage checking. | Derived from the runtime fact above and D1's descriptive boundary. |
| PROPOSAL | Treat D1 values as candidate assignments, never validated constructs; define absence only relative to a frozen selector obligation. | This design § D1 candidate profile. |
| GAP | The canonical owner has not ratified a bounded Inventory bootstrap, local native surfaces remain stale, `.codex` regeneration ownership is unresolved, and no binding/close fixture proves this unregistered workflow on the current host. | [01 § Consequence for the D1 gate](01-source-location.md#consequence-for-the-d1-gate) |

## Applicability and routing discriminator

Use this bootstrap only when all conditions hold:

- the source corpus and controls can be frozen before confirmation;
- a single writer can inspect the corpus without downstream agent returns;
- durable lookup, revalidation, or stable source-linked reuse passes the human reuse gate;
- the requested output is candidate-level descriptive Inventory, not adjudication; and
- one independent read-only coverage audit materially reduces completeness or provenance risk.

Route ordinary lookup or a small one-shot description inline. Route precedent, witness,
non-vacuity, definitional soundness, novelty, causal effect, theory selection, and GO/KILL to a
separately confirmed Research dispatch. If multiple extractor returns must be combined, stop with
`inventory-connected-topology-required`; do not flatten the topology or route it as Research.

## Modes and terminal semantics

The bootstrap composes existing Inventory modes; it does not add a new public mode.

| Phase | Existing mode / local act | Mutation | Terminal output |
|---|---|---|---|
| prepare | read-only preflight | none | frozen proposal, corpus/control manifest, reuse decision |
| extract-write | `backfill` constrained to the confirmed D1 profile | confirmed D1 files plus existing indexes/log only | candidate bundle and writer report |
| audit | `validate` plus bounded `lint` | none | `PASS | BOUNDED_CORRECTIONS | BLOCK` |
| correct | same writer, same confirmed revision, cap 1 | same boundary | revised bundle and new hashes |
| retire | bounded `sync` semantics, only after separate human approval | tombstone/index/log changes only | retirement report |

`PASS` means source linkage, frozen-denominator coverage, schema validity, index consistency,
immutability, ambiguity preservation, and boundary compliance. `BOUNDED_CORRECTIONS` names exact
mechanical defects repairable inside the confirmed mutation scope. `BLOCK` covers missing or drifted
sources, authority escape, undeclared writes, unresolved conflict loss, bad indexes, exceeded
correction cap, binding/close failure, or connected-topology need.

## Single-system layout and artifact mapping

The only Inventory root is `.arcanum/inventory/`.

```text
.arcanum/inventory/
  raw/
    d1-lens-use-corpus.manifest.json
  entries/
    d1-lens-use/
      occurrence-cards.json
      control-cards.json
      residue.md
  lint/
    d1-lens-use-validation.md
  index.md
  index.json
  tags.md
  log.md

internal-tools/composition-lab/
  research/milestone-1/01-repository-inventory/
    research-initial-definitions.md
    research.md
    findings.md
```

The Composition Lab files remain milestone-facing artifacts. For this Inventory route:

- `research-initial-definitions.md` remains the existing informational boundary;
- `research.md` becomes a human-readable, append-only extraction/session trace generated from the
  same candidate bundle, not a Research-agent transcript;
- `findings.md` becomes a non-authority D1 handoff projection summarizing coverage, observations,
  controls, ambiguities, and gaps; it contains no Research verdict matrix;
- each is indexed by source/path reference from `.arcanum/inventory/index.json`; and
- neither directory gets an `index.json`, schema, Inventory log, or duplicate evidence-card store.

This mapping is a material change from the prepared D1 Research sheet and requires explicit human
approval before execution.

## Frozen source and immutability contract

Preparation records every in-repository source as `{repo_relative_path, git_commit, sha256,
selectors, control_obligations}` in `.arcanum/inventory/raw/d1-lens-use-corpus.manifest.json`.
Tracked repository files are referenced in place and never copied into `raw/`, matching
`.arcanum/inventory/schema.md#source-policy`.

Before and after each writer attempt, compute SHA-256 for every frozen source. Any mismatch is
`BLOCK/source-drift`; there is no substitution or dynamic corpus expansion. The only authorized
writes are the named D1 Inventory files, existing Inventory indexes/tags/log, and the two approved
Composition Lab projections. The writer must fail before mutation if any target lies outside those
resolved absolute roots. The auditor repeats the hashes independently.

## D1 candidate profile

This is a local use of the canonical `inventory.evidence-card.v0.2` envelope, not a canonical
definition, custom entry type, or new schema. The canonical schema permits additional properties;
D1 semantics therefore live only in the `d1_observation` extension while all required canonical
fields and controlled values remain intact. Each card has:

```yaml
id: inventory.card.d1-lens-use.<stable-occurrence-or-control-id>
schema_version: inventory.evidence-card.v0.2
profile: full
card_type: claim | context | contradiction-candidate | question
title: string
summary: string
source_refs:
  - path: repo-relative path
    selector: heading | line span | JSON/YAML selector
    selector_type: file | heading | line-span | anchor | query | fragment
    sha256: frozen source digest
authority_level: raw-source | session-evidence | inventory-knowledge
tags: [composition-lab, d1-lens-use]
selection_reason: why this selector satisfies or leaves open a frozen obligation
captured:
  by: agent
  at: timestamp
  source_stage: other
promotion_status: candidate
promotion_owner: other | none
handoff_targets: []
trace:
  - field: JSON pointer
    source_ref: source_refs selector identifier
    rule: literal transcription | candidate assignment | dedup link | unresolved
    confidence: 0.0-1.0
    decision: assigned | inferred | copied | rejected | deferred
residue:
  type: schema | instance | both | none
  status: open | proposed | deferred | scoped-out | declared | resolved
  surfaced_by: extractor-writer | coverage-auditor
  note: string
updated_at: timestamp
d1_observation:
  obligation_ref: frozen source x control cell ID
  observation_kind: occurrence | control | contradiction | gap
  assignment:
    state: prescribed | instantiated | executed | source-asserted-effect | unknown
    basis: literal | inference | open-question
    confidence: high | moderate | low
  not_observed_within_selector: boolean
  duplicate_of: card ID | null
  contradiction_refs: [card ID]
  excluded_interpretations: [string]
  residue_items:
    - type: ambiguity | missing-trace | schema-fit | provenance | disagreement
      status: open | bounded
      note: string
```

`card_type` is a projection onto the closest canonical kind: an occurrence candidate uses `claim`
or `context`, a negative control/gap uses `question` or `context`, and a contradiction uses
`contradiction-candidate`. These kinds do not validate `d1_observation.observation_kind`.
`authority_level` describes the cited material, not confidence in the D1 assignment.
`promotion_owner: none` is permitted while status remains `candidate`; a specific non-terminal
handoff uses `other` and names its destination in the non-authority projection, because Research is
not a canonical `promotion_owner` or `handoff_targets` enum value. `governed_ref` is omitted until a
real downstream governed artifact exists.

`source-asserted-effect` means only that the source literally asserts or directly records an effect;
it is not the former ambiguous label `effect-observed` and does not validate causation. The absence
value is not a state: a control card may record `not_observed_within_selector` only with the exact
selector/search obligation, method, and corpus digest. Otherwise the value is `unknown`.

Duplicate proposal/manifest/ledger/report representations remain individually cited but link to one
candidate occurrence identity through `duplicate_of`; ambiguous identity remains residue. Conflicts
are never majority-voted or normalized. Separate cards and field-level traces survive, and the
assembler role is absent by design.

The machine index receives stable rows for the two bundles, validation report, `research.md`, and
`findings.md`, with selectors, evidence-card IDs, sources, status, confidence, and residue. The
existing `inventory_root`, index families, and `validation_boundary` do not change. The human index
and append-only log update in the same writer attempt; a partial update is validation failure.

## Seats, connectionless topology, binding, handoff, and close

### Fixed seats

| seat | authority | inputs | writes | return |
|---|---|---|---|---|
| `extractor-writer` | Inventory candidate extraction and mechanical projection only | confirmed proposal; frozen manifest; existing package schema/index/log | exact confirmed D1 files and projections | `WriterHandoff` with paths, hashes, counts, residue, source before/after hashes |
| `coverage-auditor` | independent coverage, provenance, immutability, index and boundary validation | same confirmed proposal/manifest plus frozen writer artifacts | none | `PASS | BOUNDED_CORRECTIONS | BLOCK` with checks and exact defects |

No dynamic seats, helpers, Robot-Talks, parallel writers, or retries beyond one confirmed correction
attempt are allowed. `connections` is exactly `[]`. The auditor is launched only after the writer is
terminal and every expected output exists and hashes successfully.

### Binding and handoff

Every seat prompt must begin with the host-supplied
`ACI-WORKFLOW-BINDING-V1:<base64>` line required by repository policy. The immutable prompt template
contains role, authority, source/mutation boundary, output contract, stop rules, and only typed
data-slot declarations. The host may materialize the confirmed proposal and source/artifact hashes
into a workflow-only input manifest, following the bounded discovery precedent
([discovery-writing lines 238-246](../../../../../../../.codex/skills/discovery-writing/SKILL.md#L238)).

For the auditor handoff, the parent supplies only `{path, sha256, size, producer_attempt}` rows for
predeclared outputs. It does not paste, summarize, select, or reinterpret writer prose. The auditor
opens those exact files. This is workflow evidence, not a durable ACI `EffectiveInputArtifact`,
dispatch connection, or accepted-output receipt. A fixture must show that changed bytes, wrong path,
wrong producer attempt, absent artifact, or launch before writer termination fails closed.

If the current host cannot issue the mandatory first-line binding or preserve the workflow manifest
and attempt identity, execution remains BLOCK. The design does not permit an unbound manual spawn.

### Completion and close

Because Inventory is unregistered, the bootstrap does not append an Inventory dispatch row and does
not claim a dispatch close. It produces one capability-local completion report containing proposal
digest, human acknowledgements, seat bindings/attempt IDs, writer artifact hashes, auditor verdict,
correction count, mutation list, observability result, gaps, and exit reason. Any parent governed
workflow still uses its own bridge close. Bridge stdout stays in the journal, never the working
folder; a missed host hook is recorded through that close path.

This distinction is mandatory: capability completion is workflow evidence; it is not a bus receipt,
ledger projection, registered lifecycle, or proof of durable connected handoff.

## Human gates

Four gates are separate acts:

1. **Reuse gate:** answer the three closed questions in 10. At least one `yes` names a concrete
   downstream consumer or revalidation event. All `no` plus human confirmation returns
   `inventory-lifecycle-unwarranted` and stops.
2. **Owner/design gate:** canonical Inventory owner ratifies the semantic boundary and this
   owner-directed topology. Finding the source does not satisfy ratification.
3. **Exact-run gate:** human confirms together the corpus paths/digests/selectors, controls,
   resolved targets, two seat identities, immutable prompts, models/tools, budgets, correction cap,
   outputs, mutation scope, workflow manifest schema, observability, and close semantics. Any
   material change invalidates confirmation.
4. **Launch gate:** after fixtures and independent reviews pass, human explicitly authorizes D1.

The user's milestone-wide authorization to use agents does not substitute for these design- and
run-specific gates.

## Validation and observability

Validation checks structure and provenance only:

- source manifest complete and unchanged;
- one card or typed gap for every frozen source x control obligation;
- source refs and selectors resolve;
- IDs, duplicate links, contradiction refs, trace, residue, status, authority, and promotion fields
  conform;
- both indexes parse and agree; log entry matches the configured heading; no partial update exists;
- Composition Lab projections map back to the same card IDs and contain no Research verdicts;
- write set stays inside confirmed targets; and
- workflow completion truthfully records binding and close limitations.

When `.arcanum/observability/` exists, emit the Inventory signals already owned by the skill: mode,
source count, entries created/updated, contradictions, lint gaps, validation result, downstream
lookups, and filed synthesis count. Add D1 tags only as local dimensions: corpus digest, profile
version, writer attempt, auditor verdict, correction count, and exit reason. Observability is a
read-model of the run. It cannot promote claims, prove effect, or substitute for ACI/ledger facts.

## Reversibility and retirement

The bootstrap declares its maintenance owner and consumers before launch. A later retirement is a
separately approved Inventory operation that:

- marks D1 cards and their index rows `superseded` (the canonical terminal status) rather than
  inventing `retired` or deleting source history;
- appends a log tombstone with reason, affected IDs, last hashes, replacement if any, and unresolved
  consumers;
- removes no source, governed artifact, milestone projection, or unrelated Inventory entry;
- leaves resolvable tombstone/index history for former IDs; and
- fails if any undeclared active consumer or governed reference depends on the D1-only candidate
  profile.

No skill sync or mutation is part of this retirement path.

## Canonical-source and stale-surface boundary

The canonical source is FOUND, so the former orphan-source blocker is closed. The following remain
BLOCK and are deliberately outside this bootstrap:

- owner ratification and any amendment to `C:/Users/victo/Arcanum/arcana/inventory/`;
- preview/apply of `sync-generated-skill-package.sh`;
- resolution of tracked `.codex/skills/inventory` ownership;
- correction of `.agents`/`.codex` runtime metadata and package conformance; and
- claims that all native surfaces are synchronized.

This design may be reviewed against the canonical current Inventory contract, but execution must
not rely on a newly proposed bootstrap clause until its canonical amendment and all required runtime
surfaces have a separately reviewed, authorized recovery route. No generated skill is edited here.

## T1-T16 resolution matrix

| Test | Design resolution | Pre-launch evidence / disposition |
|---|---|---|
| T1 canonical owner | FOUND closes location only; stale projections and `.codex` gap remain. | BLOCK until owner ratification and a separately authorized conformance result; no sync here. |
| T2 reuse falsifier | Gate 1 is mandatory and precedes execution preparation. | Human note names consumer/revalidation; all-no stops with typed finding. |
| T3 single system | `.arcanum/inventory/` is the sole schema/index/log/ID owner. | Static scan finds no second Inventory index/root in Composition Lab. |
| T4 artifact fit | Explicit mapping preserves milestone paths while removing fake Research verdict semantics. | Human approves mapping; fixture verifies both projections trace to cards. |
| T5 lifecycle dry run | Narrowed to one writer then one auditor under owner-directed workflow; no connected extractor/assembler. | First-line bindings, attempts, manifest, hashes, terminal order, completion and parent close all fixture-pass; otherwise BLOCK. |
| T6 connection integrity | Original connected test is inapplicable by design; `connections` must be empty. Equivalent artifact-barrier test is load-bearing. | Early audit, wrong bytes/path/attempt, missing writer terminal, or parent-summarized handoff all fail. Need for extractor returns yields `inventory-connected-topology-required`. |
| T7 confirmation | Four gates freeze every material field and invalidate on drift. | Confirmed proposal digest plus explicit acknowledgements. |
| T8 immutability | In-place references and independent before/after hashes; exact write allowlist. | Writer and auditor hash reports match manifest; escape fails before write. |
| T9 schema challenge | Canonical v0.2 envelope/enums plus additional `d1_observation`; selector-bounded absence; literal/inference/open labels; residue mandatory. | Canonical schema validation plus occurrence, not-observed, ambiguity, contradiction, duplicate, and schema-fit fixtures pass without lens definition or custom type. |
| T10 authority escape | Forbidden judgments stop or become typed candidate/open-question handoffs. | Negative fixtures for definition, causal effect, novelty, soundness, ontology promotion, GO/KILL return BLOCK. |
| T11 denominator | Frozen source x control obligations live in source manifest, outside derived counts. | Each cell maps to cited card, selector-bounded not-observed, or gap; index cannot self-certify completeness. |
| T12 mechanical validation | Evidence cards validate against canonical `inventory.evidence-card.v0.2`; index, links, IDs, log and boundary checks remain non-epistemic. | Canonical schema, parse and cross-view checks pass; report says read-model-only and does not treat extension fields as governed vocabulary. |
| T13 observability | Existing Inventory signals plus bounded D1 dimensions; receipts excluded. | Signal fixture resolves to run artifacts and makes no authority claim. |
| T14 conflict preservation | No assembler; separate candidate assignments, traces and residue survive. | Disagreement fixture proves no overwrite, majority vote, or normalization. |
| T15 reversibility | Retire/tombstone protocol preserves history and blocks on consumers. | Removal fixture changes only D1 index/status/log records and leaves sources/governed artifacts intact. |
| T16 no-launch review | R1 contract, R2 epistemic, R3 infrastructure, final `/review`, then human launch gate. | Any unresolved material finding keeps BLOCK. |

T5/T6 are not waived. Their connected three-seat form is rejected because it cannot pass on the
current runtime. The replacement tests prove the narrower topology does not smuggle a connection
through parent prose or falsely claim durable binding.

## Fixtures required before launch

1. **Positive:** one frozen source and one control produce a cited occurrence card and a
   selector-bounded `not_observed` card, synchronized indexes, projections, log, signals, and PASS.
2. **Ambiguity/conflict:** two source passages support incompatible candidate assignments; both
   survive with trace and residue.
3. **Deduplication:** proposal, manifest, ledger, and report remain distinct refs linked to one
   candidate occurrence without forced identity when evidence is insufficient.
4. **Drift/escape:** changed source, copied source, target escape, undeclared tag, and partial index
   update all BLOCK without further writes.
5. **Authority:** definition, inferred causal effect, novelty, soundness, GO/KILL, and promotion all
   BLOCK or create a non-authority typed handoff.
6. **Workflow:** missing first-line binding, early auditor, wrong artifact hash/path/attempt,
   parent-summarized handoff, retry beyond cap, and missing parent close all BLOCK.
7. **Retirement:** tombstone preserves IDs/history and refuses removal with an active undeclared
   consumer.

## Self-red-team against 03

- **Could this be a second Inventory system?** No: the design has one root, index, log, and ID owner.
  Composition Lab receives only milestone-facing projections, already required by its program.
- **Does “unregistered” disguise a connected dispatch?** The design removes extractor/assembler
  edges and dynamic seats. It labels the artifact manifest and completion as workflow evidence only.
  If the host cannot bind/order the two seats, it blocks.
- **Does the schema settle the research question?** It replaces `effect-observed` with
  `source-asserted-effect`, bounds absence to selectors, labels assignments, and preserves residue.
  This reduces but does not eliminate observer judgment; therefore all rows remain candidates.
- **Is backfill merely a name for one-shot extraction?** It remains blocked until the human reuse
  falsifier names a durable consumer or revalidation event.
- **Can the writer manufacture completeness?** No: denominator obligations are frozen externally
  and the auditor recomputes source hashes and cell coverage.
- **Can workflow evidence be mistaken for ACI evidence?** The completion contract forbids that
  claim and the workflow negative fixtures check it. This remains a host-dependent gap until tested.
- **Is stale-surface recovery smuggled into execution?** No sync, skill mutation, or surface repair is
  authorized here. This means D1 launch remains BLOCK even if every design fixture passes until a
  separately governed recovery clears the installed-runtime contract.
- **Does one writer lose independent discovery?** Yes, intentionally. The auditor independently
  checks coverage but not alternative interpretation. Any requirement for independent extraction
  exceeds this bootstrap and returns the connected-topology blocker.

## Final gate state

| Decision | State |
|---|---|
| Preserve and independently review this design | **GO** |
| Ratify the bounded D1 candidate-profile intent | **CONDITIONAL GO**, human and canonical owner |
| Amend/sync Inventory skills | **BLOCK / separate work** |
| Register Inventory LIVE or edit dispatch infrastructure | **NO-GO** |
| Execute fixtures | **BLOCK until exact fixture proposal and host-binding path are confirmed** |
| Launch D1 | **BLOCK until T1-T16, R1-R4, exact human confirmation, and stale-surface recovery all pass** |

The next legitimate artifact is an independent review of this proposal. It is not an opening
record, launch authorization, skill amendment, sync command, or Inventory ingest.
