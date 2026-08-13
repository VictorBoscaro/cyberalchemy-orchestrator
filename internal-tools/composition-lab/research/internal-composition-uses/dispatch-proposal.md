---
artifact_kind: bounded-workflow-proposal
status: proposal-only-operationally-blocked
corpus_redesign: adopted-for-redesign
launch_readiness: not-launch-ready
date: 2026-08-13
owner_candidate: inventory
registration: forbidden-at-this-stage
---

# Proposal — internal comparative study of composition

## Status

**Proposal only; operationally BLOCKED.** This is not an opening record, route receipt, registered
dispatch, or run authorization. It must not be compiled, opened, registered, or launched. Inventory
is the intended semantic owner, but its canonical bounded delegated workflow does not yet exist in
an executable form.

## Objective

Build a source-backed description of how the repository claims or realizes composition across
lenses, skills, workflows, artifacts, knowledge, interfaces or whatever other kind of compositions that exists, only explicitly. Preserve differences between claim, prescription, configuration, instantiation, execution, observed effect, absence, ambiguity,
and contradiction. Do not decide in this stage what composition is or whether the domains share a
single mechanism.

This serves the [research program](../../research-program.md) and its progressive document. The
[initial definitions](research-initial-definitions.md) remain `proposed`; their [review](review.md)
approved the reviewed text and records that no material finding survives. Any gate that requires
an accepted informational baseline must still obtain explicit human promotion or acceptance; this
proposal does not supply it.

## Question

What source-backed occurrences, absences, relations, transformations, traces, and attributed
effects appear in the repository's candidate uses of composition, and what remains unknown when
claims, prescriptions, configurations, executions, and outcomes are kept distinct?

This acquisition question is deliberately narrower than the later question of what recurs, which
neighboring concept explains a case, or which hypothesis survives. Those are Research-owned
adjudicative questions.

## Corpus freeze — prerequisite, not yet a claim

No exact corpus is asserted here. A later preparation step must produce a manifest containing every
included repository-relative path, file digest, selector policy, source kind, inclusion reason, and
declared negative control. It must also list exclusions, generated outputs, orchestration advice,
and the temporal or commit boundary.

The manifest should seek bounded coverage of these contrast surfaces without presuming that each
contains composition:

- lens and perspective practices;
- skill and capability composition;
- workflow, topology, and handoff structures;
- artifacts and knowledge structures;
- interfaces and user-facing assembly mechanisms;
- negative controls for aggregation, sequence, configuration, integration, coordination, and
  retrospective interpretation.

The surface list is a sampling obligation, not an ontology. Until paths and digests are complete and
human-confirmed, corpus completeness and launch readiness are both false.

### Proposed external-local annex: DomainSpec v2

The internal ecosystem also includes `C:/Users/victo/domainspec-core/projects/domainspec-v2/`,
outside this checkout. Its bounded [proposed corpus annex](../../orchestration/dispatch-proposals/internal/domainspec-v2/corpus-manifest.md)
identifies exact candidate sources for lens practice, research/workflow composition, typed-artifact
and graph claims, work-pack recomposition, and UI/relationship formation. Because DomainSpec and its
authority spine are private, this is an internal ecosystem source—not external literature—and may
not be copied into public Arcanum surfaces.

The annex is **adopted for redesign**, not confirmation, and is explicitly **not launch-ready**. Its
exact paths, source revision, clean-path status, byte sizes and SHA-256 values must join the later
human-confirmed manifest. The earlier freeze of 22 sources, 41 hashes and 176 obligations is stale;
all derived partitions, prompts, corpus digests, fixtures and the human confirmation sheet must be
regenerated and independently re-audited before any new confirmation or launch decision. The annex
does not change Inventory ownership, the description/adjudication split, or the operational
bootstrap blocker below.

## Proposed bounded topology

This topology becomes usable only after the Inventory owner ratifies it.

### Isolated extractors

One or more agents inspect disjoint, frozen source partitions. They are read-only outside preserved
session-return locations and cannot read another extractor's return.

Immutable prompt intent:

> Inspect only the bound manifest partition. Record literal source-backed occurrences or explicit
> absences, source selectors, source kind, parts and relations explicitly present, claimed or
> observed transformation, evidence level, ambiguity, contradiction, exclusion, trace, and
> residue. Do not define composition or lens, import external theory, infer causal effect, resolve
> ambiguity, create novelty candidates, or issue GO/KILL. Report every manifest item.

### Controlled assembler

Exactly one agent consumes the frozen extractor returns and writes only to the confirmed Inventory
root. It preserves disagreement and absence rather than selecting the most persuasive account.

Immutable prompt intent:

> Assemble source-backed candidate Inventory records and human/machine indexes from the bound
> returns. Revalidate every material claim against its source selector. Preserve conflicts,
> exclusions, uncertainty, trace, and residue. Do not promote definitions, ontology, causal claims,
> or Research verdicts. Write only the confirmed Inventory artifacts.

### Independent coverage auditor

One agent reads the frozen corpus manifest and assembled result after writes cease. It performs no
assembly and has no authority to repair silently.

Immutable prompt intent:

> Verify manifest denominator coverage, source linkage, evidence-state discipline, explicit
> absences, ambiguity and contradiction preservation, schema validity, non-authority language,
> allowed write scope, and index parseability. Return `PASS`, `BOUNDED_CORRECTIONS`, or `BLOCK` with
> cited defects. Do not adjudicate composition, novelty, truth beyond sources, or causal effect.

Agent names, models, token budgets, exact prompts, partition assignment, ordering, correction
ceiling, and effective tool surface remain unset and must be frozen at the confirmation gate.

## Proposed outputs and writes

The later confirmed proposal must freeze three distinct destinations and file-level mutation
allowlists. None is selected or writable by this document.

**Inventory-native destination.** Inside one existing, explicitly selected Inventory root, only:

- source-backed occurrence/control evidence-cards or entries;
- `index.md` and parseable `index.json`;
- controlled tags and append-only maintenance log updates;
- a non-authority handoff projection for the next research stage.

**Workflow/session-evidence destination.** Outside the Inventory root, in a separately confirmed
session-evidence path, only immutable extractor returns and the frozen manifests needed to identify
their inputs and outputs. Extractor returns are workflow evidence, not Inventory-native records or
authority.

**Validation-evidence destination.** Outside the Inventory root and distinct from raw extractor
returns, in a separately confirmed validation path, only auditor findings, parseability results,
mutation-scope checks, and the terminal `PASS | BOUNDED_CORRECTIONS | BLOCK` result.

Bridge open/close/binding stdout or receipts must never be copied into any of these destinations or
the working folder; the bridge journal is their sole preservation surface.

Raw sources, initial definitions, research program, skills, registry, lifecycle, telemetry ledger,
and runtime are read-only. This proposal authorizes no writes at all. The exact Inventory root and
all three destination paths and file-level mutation allowlists remain confirmation prerequisites;
`.arcanum/inventory/` exists but must not be selected merely by default.

## Acceptance and validation

`PASS` requires all of the following against the frozen manifest:

- every source/control has a record or explicit absence;
- every material field has a source selector or is marked inference/open question;
- `effect-observed` appears only with a direct trace meeting the later frozen evidence rule;
- ambiguity, dissent, contradictions, exclusions, and residue remain visible;
- raw sources and all out-of-scope paths remain unchanged;
- indexes are synchronized and machine-parseable;
- handoff language denies definition, ontology, causal, and verdict authority;
- negative fixtures for hidden definition, unsupported effect, candidate fabrication, GO/KILL,
  source mutation, and package escape are rejected.

Correctable bounded defects yield `BOUNDED_CORRECTIONS` only within the preconfirmed correction
ceiling. Missing bindings, conflicting writes, authority escape, schema/index failure, or exhausted
corrections yield `BLOCK`.

## Gates before any launch

1. pass the durable-reuse gate and identify concrete downstream consumers or revalidation events;
2. locate or restore `arcana/inventory/SKILL.md` and verify canonical ownership and regeneration;
3. ratify the bounded/unregistered workflow in that canonical capability and synchronize generated
   surfaces;
4. resolve the currently failed execution-governance gate: the installed shared lifecycle requires
   a resolver-produced routable receipt and canonical registration-backed open/close, while the
   registration contract says to skip registration for capability-owned unregistered helpers.
   Therefore the shared lifecycle **does not currently represent this bootstrap**. A separately
   authorized decision and contract change by the host/runtime/lifecycle owner, coordinated with
   the canonical Inventory owner, must define an honestly bound unregistered open/run/close path.
   If registration is proposed instead, it requires separate registry authority and falls outside
   this proposal. Until an authorized path exists, no dry-run sheet may be produced and the result
   remains `BLOCK`;
5. pass skill-level positive and negative fixtures;
6. freeze and review the exact corpus manifest, controls, topology, prompts, agents, budgets,
   outputs, the three exact destination allowlists, commands, and correction ceiling;
7. obtain explicit human confirmation of the exact frozen proposal.

No gate may be waived by calling the work `research`, `meta`, `n = 1`, or “only a pilot.”

## Smallest executable post-gates

Before the full corpus, run one source plus one negative control through one extractor, one
assembler, and one independent auditor. Require one occurrence or explicit absence, valid trace and
residue, synchronized indexes, immutable inputs, and terminal validation. Failure returns `BLOCK`
and preserved residue; success authorizes only preparation of the full bounded proposal, not its
launch.

## Relation to the progressive document

Accepted Inventory records do not directly rewrite [the research program](../../research-program.md).
They first become a cited, non-authoritative evidence bundle. A dedicated later writer may update
the progressive document only with claims that survive the appropriate evidence and review gates,
clearly labeling repository observation, inference, hypothesis, and unknown.

## Separate future Research dispatch

After the descriptive inventory is accepted, a new registered Research proposal may ask which
candidate distinctions or mechanisms survive precedent, non-vacuity, and definitional soundness.
It may compare recurrence across domains and test whether cases collapse to aggregation, sequence,
configuration, integration, coordination, or retrospective interpretation. That dispatch must have
its own initial context, candidate matrix, route receipt, opening record, review, and human
confirmation. Inventory evidence is input, not a Research verdict.

The reason this proposal remains blocked is preserved in the
[route advice](../../orchestration/dispatch-proposals/internal/route-advisor.md), the earlier
[routing assessment](../../orchestration/milestone-1-strategy/d1-readiness/runtime-blocker/07-capability-routing.md),
and the [final route decision](../../orchestration/milestone-1-strategy/d1-readiness/runtime-blocker/10-final-route-decision.md).

## Correction response

The independent [proposal review](../../orchestration/dispatch-proposals/internal/review.md) records
`KEEP` for this proposal artifact while preserving the separate operational `BLOCK`; its documentary
verdict does not authorize or advance execution.

- Review finding 1: the shared lifecycle contradiction is now stated as a presently failed gate,
  with the required owners/change authority and prohibition on producing a dry-run sheet.
- Review finding 2: Inventory mutations, raw session returns, and validation evidence now have
  separate destination classes and must receive exact frozen allowlists; bridge receipts remain
  journal-only.
- Review finding 3: the initial-definitions artifact is described as reviewed and proposed, with
  explicit human acceptance or promotion still required where a gate depends on it.
