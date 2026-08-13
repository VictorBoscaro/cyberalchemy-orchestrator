---
artifact_kind: final-route-decision
status: decided-awaiting-human-ratification
date: 2026-08-13
scope: milestone-1-d1-descriptive-lens-use-inventory
decision: A-bounded-inventory-bootstrap
decision_authority: human
supersedes:
  - 09-program-resolution-draft.md
---

# Final route decision for D1

## Decision

**Choose A: make the installed `inventory` capability executable through an explicit,
Inventory-owned bounded bootstrap for D1, using the common governed lifecycle wherever it can
represent the run honestly, and reshape D1 to Inventory-native evidence-cards and indexes. Do not
give Inventory a separate registered lifecycle or dispatch identity, do not add an observational
regime to `research`, and do not build the runtime DAG.**

**Governance disposition: conditional GO for the bounded/unregistered Inventory-owned bootstrap;
NO-GO for registering Inventory as a LIVE capability; NO-GO for launching D1 until the preparation,
review, and human-ratification gates pass.**

This is a program decision, not authorization to edit a skill, registry, lifecycle, runtime, or D1
record. The next authorized work is the implementation and review package specified below, followed
by a human ratification gate.

## Objective served

Produce the first source-backed, repeatable description of how lenses occur in the repository while
preserving occurrence, explicit absence, ambiguity, evidence level, dissent, and provenance. The
result must support later hypothesis formation without deciding what a lens is, whether a
composition caused an effect, or whether any candidate is novel, witnessed, sound, GO, or KILL.

The decision serves that objective by placing descriptive acquisition with the capability that owns
source-linked reusable inventory records, while leaving candidate adjudication with the capability
that owns epistemic gates and verdicts.

## Evidence incorporated and change from 09

The provisional decision in [09](09-program-resolution-draft.md#L49-L58) preferred B under the
premise that no installed capability owned descriptive inventory. It expressly required the choice
to fall to A if 07/08 found a distinct owner, lifecycle, consumers, or acceptance contract
incompatible with `research` ([09](09-program-resolution-draft.md#L115-L126)).

The later evidence changes that premise:

- [07](07-capability-routing.md#L12-L22) identifies `inventory` as the only inspected installed
  semantic owner of D1's descriptive work. Its blocker is operational: the capability has no
  routable or explicitly bounded agent lifecycle.
- Inventory `ingest` and `backfill` extract source-linked reusable knowledge, contradictions, and
  open questions ([Inventory](../../../../../../.agents/skills/inventory/SKILL.md#L32-L40),
  [Inventory](../../../../../../.agents/skills/inventory/SKILL.md#L92-L116)). Its evidence-card
  contract requires source references, trace, residue, promotion ownership, and non-authority
  handoffs ([Inventory](../../../../../../.agents/skills/inventory/SKILL.md#L226-L250)).
- [08](08-research-contract-adjudication.md#L17-L36) confirms that `research` cannot currently emit
  a purely descriptive inventory: `n = 1` reduces the required files, not the verdict semantics.
  Converting occurrences into candidates merely to satisfy the matrix would be nominal compliance
  and violate `claim <= proof` ([08](08-research-contract-adjudication.md#L80-L94)).
- `research` explicitly owns judgment, epistemic roles, skeptic gates, outputs, and verdicts
  ([Research](../../../../../../.agents/skills/research/SKILL.md#L20-L31)); its findings contract
  requires a verdict row per candidate ([Research](../../../../../../.agents/skills/research/SKILL.md#L127-L153)).

Therefore A now means a bounded semantic bootstrap for an existing owner under common lifecycle
governance, not the new capability or separate lifecycle assumed by 09. That is the load-bearing
change in the comparison.

### Concurrent governance review

The independent governance assessment [11](11-inventory-governance.md#L10-L28), produced after this
decision was formed, corroborates the bounded Inventory-owned bootstrap and rejects LIVE
registration before stable recurrence. It also sharpens two constraints adopted here:

- novelty, soundness, causal effect, and GO/KILL require a separately routed Research handoff
  ([11](11-inventory-governance.md#L97-L116)); and
- the generated Inventory surface declares `arcana/inventory/SKILL.md` as its canonical source, but
  that path is absent from this checkout. The review makes locating or restoring it a hard
  precondition to mutation ([11](11-inventory-governance.md#L49-L66)). A direct path check performed
  for this decision confirmed the absence on 2026-08-13.

This concurrent review is corroboration and a new implementation blocker, not evidence retroactively
used to produce the A/B decision.

## Updated criteria matrix

Scale: 1 is unfavorable; 5 is favorable. These are reasoned judgments, not measurements.

| criterion | A — bounded Inventory | B — observational Research | deciding reason |
|---|---:|---:|---|
| smallest expansion | 4 | 2 | A adds executability and a local schema to the existing owner. B changes a canonical, broadly routed adjudication contract, its generated surfaces, discriminators, and fixtures. |
| epistemic fidelity | 5 | 3 | A keeps description candidate-level and non-authoritative. B can separate regimes, but joins observation to a capability whose load-bearing contract is candidate adjudication. |
| traceability | 5 | 4 | A natively requires source refs, trace, residue, human/machine indexes, and validation boundaries. Research supports cited findings but not D1's observational denominator as its canonical read model. |
| time to first evidence | 3 | 4 | B already has a registered route. A first needs a bounded bootstrap and local schema; B's advantage remains provisional until its canonical contract and compatibility fixtures are changed. |
| reversibility | 4 | 3 | A can remain local and bounded. B alters the meaning and routing surface of every future `research` dispatch. A loses this advantage if it installs a competing knowledge system or gains undeclared permanent consumers. |
| lifecycle compatibility | 3 | 4 | B already resolves through the registered lifecycle. A is compatible only after its owner explicitly bounds roles, topology, confirmation, outputs, validation, terminal behavior, and ledger/bridge representation. |
| description/adjudication separation | 5 | 3 | A assigns the two jobs to different owners. B depends on a perfect regime discriminator inside one capability. |
| blast radius | 4 | 2 | A is constrained to D1 and Inventory-native artifacts. B changes a repository-wide dispatch type. |

The result is not that A is immediately executable. It is that A is the smallest semantically sound
change worth preparing. “Bounded Inventory” means a capability-owned bootstrap contract executed
through common governance; it does not mean that Inventory owns a new independent lifecycle.

## Decision boundaries

The bounded Inventory route may:

- enumerate a frozen corpus and declared controls;
- record occurrences, explicit absences, ambiguity, contradictions, exclusions, and evidence level;
- distinguish `prescribed`, `instantiated`, `executed`, `effect-observed`, and `unknown` only as
  source-backed descriptive states;
- produce source-backed evidence-cards, EvidenceSets when repeated retrieval warrants them,
  `index.md`, `index.json`, validation results, and a bounded handoff projection;
- synthesize what the corpus contains while marking inference, residue, and open questions.

It must not:

- define “lens” or settle the ontology;
- infer causal or compositional effect beyond what a source explicitly witnesses;
- create novelty candidates, run soundness/non-vacuity gates, or emit GO/KILL;
- treat an Inventory read model as canonical meaning, definition, or research verdict;
- install a competing repository-wide knowledge system merely to execute D1;
- borrow the `research` dispatch type or its registry entry as a transport workaround.

Anything crossing those boundaries becomes a separately routed downstream task. In particular,
candidate adjudication remains `research`.

## Premises and the initial reuse gate

The decision depends on four premises:

1. D1 needs a reusable and maintainable evidence surface, not only a one-shot cited snapshot.
2. The existing `composition-lab` structure can host or adapt an Inventory package without creating
   a competing repository knowledge system.
3. The Inventory owner can define a bounded, unregistered bootstrap compatible with the host's
   confirmation, binding, observation, and close requirements.
4. D1 accepts Inventory-native artifacts instead of requiring `findings.md` to impersonate a
   Research verdict artifact.

Premise 1 is contestable and must be tested first. Before drafting the bootstrap, the owner must
produce a one-page acceptance note answering these closed questions from the confirmed D1 program:

- Must the corpus be backfilled or revalidated after source changes?
- Must later milestone work retrieve occurrences by source, control, state, or evidence level without
  reparsing the corpus?
- Must downstream work cite stable source-linked records while preserving trace and residue?

The reuse gate passes when at least one answer is **yes** and the acceptance note names the concrete
downstream consumer or maintenance event. It fails only when all three answers are **no** and the
human confirms that a one-shot cited snapshot fully satisfies D1. This is a predeclared falsifier,
not an invitation to resurvey routes.

Failure stops A and returns the typed finding `inventory-lifecycle-unwarranted` to the human gate.
It permits reconsideration of B only through the reversal conditions below; it does not silently
authorize observational Research.

## Evidence of success

A successful route preparation must demonstrate, before D1 launches:

1. **Ownership:** the canonical Inventory owner accepts the bounded applicability and explicitly
   excludes adjudication.
2. **Canonical source:** `arcana/inventory/SKILL.md` is located or restored and its authority is
   verified before any mutation; generated `.agents`, `.codex`, or `.claude` copies are not edited
   as independent authorities.
3. **Routing:** `domainspec-subagents-strategy` selects Inventory from a discriminator that separates
   durable descriptive inventory from one-shot lookup and candidate adjudication.
4. **Lifecycle:** a dry-run proves confirmation, binding, bounded source/mutation scope, launch,
   observation, validation, terminal behavior, and close without inventing a fake registered type.
5. **Artifact fit:** a minimal fixture produces an occurrence and an explicit absence with valid
   `source_refs`, field-level trace, residue, evidence level, and machine-index entries.
6. **Negative controls:** fixtures reject a lens definition, unsupported effect claim, fabricated
   candidate, and GO/KILL verdict.
7. **Completeness:** every frozen source/control pair has an occurrence or explicit absence, and the
   machine index exposes the declared denominator and validation boundary.
8. **Non-authority:** downstream packets state that Inventory records do not promote ontology,
   definitions, or verdicts.
9. **No infrastructure drift:** the package adapts existing `composition-lab` conventions, records
   its maintenance boundary, and creates no unrelated repository-wide knowledge layer.

No success claim may exceed these demonstrations. In particular, completion of D1 will not prove
that any lens composition is effective.

## Collapse-tests and reversal condition

### Collapse-test for A

Remove durable index lookup, repeatable backfill/revalidation, stable source-linked reuse, and
maintenance from D1's acceptance. If a one-shot cited snapshot still satisfies every obligation,
Inventory has lost its distinctive job and A collapses to over-classification. That is exactly what
the initial reuse gate tests.

### Collapse-test for B

Remove candidates, GO/KILL, precedent, witness, and soundness from “observational Research.” If the
remaining work is repeatable corpus ingestion into source-backed records with indexes, trace,
residue, and downstream reuse, it collapses to the installed Inventory owner. B then adds routing
overlap without a distinct job.

B may replace A only if all of the following are evidenced and human-ratified:

1. the initial reuse gate fails;
2. at least two additional bounded repository cases show recurring observational research whose
   outputs are intentionally one-shot rather than maintained knowledge;
3. the Research owner specifies mutually exclusive observational/adjudication triggers and forces
   mixed objectives into separate stages;
4. compatibility fixtures prove the current adjudication matrix, skeptic gates, precedent-first
   rule, and existing dispatches remain unchanged;
5. routing fixtures distinguish observational Research from Inventory deterministically; and
6. the change is demonstrably removable without migrating persisted Inventory consumers or
   weakening prior Research records.

Until all six conditions hold, B is not a fallback shortcut.

## Implementation and review package

The next package is a proposal only. It must not implement the change in the same act.

### I1 — acceptance and discriminator

- Produce the closed reuse-gate note.
- Define the routing discriminator among inline lookup, bounded Inventory, and Research adjudication.
- Freeze the D1 corpus, controls, mutation boundary, and allowed claims.

### I2 — Inventory owner contract proposal

- Locate or restore the declared canonical source `arcana/inventory/SKILL.md` and verify how native
  surfaces are regenerated. Its current absence is BLOCK for mutation, not permission to edit a
  generated copy.
- Propose the smallest canonical Inventory amendment that owns a bounded/unregistered agent
  bootstrap.
- Declare roles, topology, source and mutation boundaries, confirmation, host binding, outputs,
  validation, failure modes, terminal behavior, and close responsibility.
- State whether the bootstrap uses the shared lifecycle and exactly how the bridge/ledger represents
  it. If no honest representation exists, remain BLOCK; do not infer a dispatch type from a schema.
- Keep a separate Inventory lifecycle and registry registration out of scope. Registration may be
  reconsidered only after at least two further materially distinct accepted uses share the same
  topology, acceptance contract, output boundaries, and at least one stable downstream consumer.

### I3 — D1 Inventory package proposal

- Select an existing `composition-lab`-compatible root rather than automatically installing
  `.arcanum/inventory/`.
- Define minimal occurrence/control evidence-card and index shapes, including stable IDs,
  `source_refs`, selectors, descriptive state, evidence level, trace, residue, contradiction,
  exclusion, and validation boundary.
- Define human and machine indexes, the frozen denominator, explicit-absence behavior, and a
  non-authority handoff projection.
- Map the old D1 outputs to these artifacts and retire any requirement that `findings.md` carry a
  fake Research matrix.

### I4 — fixtures and dry-run plan

- Add positive fixtures for occurrence, absence, ambiguity, contradiction, and revalidation.
- Add negative fixtures for definition, unsupported causal effect, candidate fabrication, verdict,
  source mutation, and package escape.
- Specify a one-source/one-control dry run that exercises binding, output capture, index validation,
  and close before the frozen corpus is launched.

### R1 — independent contract review

Review capability ownership, routing exclusivity, registry non-use, lifecycle compatibility, host
binding, and mutation boundaries. Any unresolved fake-type or close-path issue is BLOCK.

### R2 — epistemic red-team

Attack description/adjudication leakage, evidence inflation, effect claims, hidden definitions,
denominator incompleteness, and residue loss. Require a correction loop for material findings.

### R3 — infrastructure and reversibility review

Attack schema overfit, package sprawl, competing-system installation, undeclared consumers, sync
debt, and inability to remove the bootstrap. Verify the initial reuse gate and B reversal threshold.

### R4 — final `/review`

After I1–I4 and R1–R3 are preserved, run a final independent `/review` over the complete proposal.
The review may return `accept`, `bounded-corrections`, or `block`; only the human may ratify launch.

## Compatibility obligations

- **`domainspec-subagents-strategy`:** must route by owned intent, not by ledger convenience. Its
  output must name Inventory and the explicit bounded bootstrap; if that bootstrap is absent or its
  discriminator fails, routing stops.
- **Registry:** remains unchanged during this package. No existing registered dispatch type may be
  reused. A later registration decision requires recurrence evidence and its own governance review.
- **Lifecycle and host wrapper:** Inventory owns the bounded semantic bootstrap, not a parallel
  lifecycle. The proposal must use the common governed confirmation/open/run/close path when it can
  represent the bootstrap honestly and preserve the mandatory seat binding. If it cannot, remain
  BLOCK rather than minting a local lifecycle. Bridge receipts remain in the journal, never the
  working folder. A missed hook must be recorded through the bridge close path, not a side file.
- **Research:** remains unchanged. D1 Inventory outputs may later supply source evidence to a
  separately confirmed Research dispatch, but they are not Research findings or verdicts.

## Risks and mitigations

| risk | mitigation / stop condition |
|---|---|
| Inventory becomes “Research without verdicts” | Enforce the descriptive discriminator and negative fixtures; route definitions, causal effects, soundness, novelty, and verdicts elsewhere. |
| Bounded bootstrap becomes an ad hoc lifecycle exception | Require canonical owner ratification, shared lifecycle compatibility, explicit close behavior, and R1. If representation is not legitimate, BLOCK. |
| Declared canonical Inventory source is absent | Locate or restore `arcana/inventory/SKILL.md` and verify regeneration before mutation; never patch generated surfaces as a workaround. |
| D1 installs excessive knowledge infrastructure | Pass the reuse gate, adapt existing `composition-lab` conventions, use the minimal schema, and apply R3. |
| Custom schema promotes interpretation | Require source refs, trace, residue, evidence levels, non-authority language, and negative controls. |
| Package gains silent permanent consumers | Declare consumers and maintenance owner; undeclared consumers fail reversibility review. |
| Route overlap with Research | Preserve mutually exclusive boundaries and make mixed objectives separate dispatches. |
| Fast evidence pressure bypasses review | Separate proposal, review, human ratification, record preparation, and launch into distinct acts. |

## Final disposition

The program is **CONDITIONAL GO for the bounded/unregistered Inventory-owned bootstrap, NO-GO for
LIVE registration, and NO-GO for D1 launch until all stated gates pass**.

Proceed only with I1–I4 and R1–R4. Keep B closed unless the predeclared reversal conditions are all
met and human-ratified. Keep runtime DAG work in its separate roadmap. Do not launch D1, mutate a
skill, edit the registry, or infer a lifecycle route from this decision document.
