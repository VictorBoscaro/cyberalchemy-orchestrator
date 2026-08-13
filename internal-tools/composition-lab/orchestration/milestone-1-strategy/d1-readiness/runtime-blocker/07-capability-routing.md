---
artifact_kind: capability-routing-assessment
status: blocked-pending-inventory-lifecycle
date: 2026-08-13
scope: descriptive repository inventory of lens uses
---

# D1 capability routing: descriptive lens-use inventory

## Decision

**`inventory` is the only inspected installed capability that legitimately owns the descriptive
inventory D1 needs without imposing the `research` novelty-verdict matrix. It is not, however, a
routable dispatch and its skill defines no capability-owned bounded/unregistered bootstrap. Under
the user's dispatch-only constraint, D1 therefore remains `BLOCK`.**

Do not route D1 to `research`, `discovery-writing`, `architecture-pattern-inventory`,
`research-evidence-harness`, or `context-builder`. The smallest honest next change is an
owner-ratified lifecycle for `inventory`: either register an executable dispatch route or add an
explicit bounded/unregistered Inventory bootstrap. Then redesign D1 around Inventory's own
evidence-card/index outputs instead of forcing those observations into `findings.md` or a novelty
verdict table.

This agrees with the earlier replan's hard boundary: the observational occurrence matrix cannot be
silently substituted for Research's canonical candidate/verdict matrix
([04](04-epistemic-replan.md#L117-L125)). It also rejects 06's proposed six `research` dispatches:
connectionless execution does not cure a capability/output mismatch
([06](06-replan-compliance.md#L152-L167)).

## Classification rule

A semantic match is not automatically executable. `domainspec-subagents-strategy` requires the
installed capability to own the intent and requires registered work to resolve through the
executable registry; if no capability owns the work, routing stops
([strategy](../../../../../../.agents/skills/domainspec-subagents-strategy/SKILL.md#L17-L44)).
The registry currently exposes LIVE capability refs only for `research`,
`domainspec-implement`, `review`, and `experiment`; all five worker candidates below fail the
resolver with `has no routable dispatch type`
([registry](../../../../../../implementations/contracts/dispatch-type-registry.v1.json#L1)).

An unregistered route is usable only when its owning capability explicitly defines and bounds that
workflow. A tool allowance or a suggested mapper list is not itself a dispatch lifecycle,
confirmation contract, or close mechanism.

## Candidate assessment

### 1. `inventory` — semantic owner; operationally unavailable

**Owned intent.** Install and maintain a repository-local compiled knowledge layer. Its `ingest`
and `backfill` modes process raw sources into source-linked reusable knowledge; extraction expressly
includes concepts, workflows, implementation patterns, interfaces, observability signals,
contradictions, and open questions
([Inventory](../../../../../../.agents/skills/inventory/SKILL.md#L20-L40),
[ingest](../../../../../../.agents/skills/inventory/SKILL.md#L92-L115)). This legitimately covers a
descriptive inventory of lens-use occurrences when the local schema defines the occurrence fields
and keeps interpretation candidate-level.

**Outputs.** Inventory owns generated pages, evidence-cards, EvidenceSets, `index.md`,
`index.json`, tags, log, and lint/validation results. Claims must cite raw sources or be marked as
inference/open question, and downstream packets remain non-authority read models
([authority](../../../../../../.agents/skills/inventory/SKILL.md#L226-L250),
[authority rule](../../../../../../.agents/skills/inventory/SKILL.md#L300-L304)). It does not require
novelty candidates, `GO/KILL`, soundness, or a novelty verdict matrix. It does require adapting D1's
canonical output from a single `findings.md` to an Inventory package/read model.

**Dispatch/lifecycle.** Unregistered: registry resolution fails. The skill permits `Agent` as a
tool, but defines no subagent topology, confirmation model, bounded bootstrap, or operational
lifecycle. Therefore it may be an inline sigil, but it is not executable under the current
dispatch-only constraint.

**Incompatibilities/residue.** Inventory is long-lived knowledge infrastructure, not a research
dispatch. It expects a local schema plus human and machine indexes and warns against installing a
competing system when an existing inventory can be adapted
([quality bar](../../../../../../.agents/skills/inventory/SKILL.md#L321-L347)). Before execution,
the owner must choose/adapt the package root under `composition-lab`, declare occurrence/control
entry shapes, and bound the agent workflow. Inventory can record evidence levels and ambiguity; it
must not decide what a lens is or claim compositional effect during D1.

### 2. `architecture-pattern-inventory` — bounded mapper contract, wrong owner

**Owned intent.** Map repository architecture and produce a reusable architecture-pattern package:
layers, dependency rules, implementation patterns, concept/relationship cards, testing alignment,
and observability alignment
([objective and applicability](../../../../../../.agents/skills/architecture-pattern-inventory/SKILL.md#L18-L43)).

**Outputs.** A full `architecture/` package including `ARCHITECTURE.md`, pattern-library documents,
dependency rules, testing/observability alignment, and concept/relationship inventories
([process](../../../../../../.agents/skills/architecture-pattern-inventory/SKILL.md#L70-L101)). It
does not impose a novelty verdict matrix.

**Dispatch/lifecycle.** Unregistered: registry resolution fails. The skill does define a bounded
internal mapper contract (structure, layers, patterns, testing, observability), with the main agent
as synthesizer
([subagent contract](../../../../../../.agents/skills/architecture-pattern-inventory/SKILL.md#L46-L65)).
It does not define a registered open/close lifecycle, and the bounded topology is specifically for
architecture mapping.

**Incompatibilities.** D1 inventories uses of perspectives across normative skills,
configurations, traces, reports, reviews, and controls. That is not a repository architecture map.
Using this capability would require irrelevant layers/dependency/testing artifacts and would
misclassify social/epistemic occurrences as implementation patterns. Its available mapper topology
cannot be borrowed while rejecting its owned intent and output contract.

### 3. `discovery-writing` — explicitly bounded/unregistered, wrong artifact and stage

**Owned intent.** Author a discovery-stage design document that explains what is changing and why,
including problem space, concepts, decisions, open questions, and implementation-relevant detail
([purpose](../../../../../../.agents/skills/discovery-writing/SKILL.md#L9-L13)).

**Outputs.** One pipeline-visible discovery with mandatory business context, PascalCase core
concepts, detailed specifications, decisions, connections, diagram, changelog, and provenance
([location](../../../../../../.agents/skills/discovery-writing/SKILL.md#L42-L50),
[structure](../../../../../../.agents/skills/discovery-writing/SKILL.md#L76-L94)).

**Dispatch/lifecycle.** Explicit capability-owned bounded/unregistered bootstrap: exactly one
controlled writer plus predeclared probes and two or three isolated reviewers; it must not be
registered or misclassified while no LIVE discovery type exists
([bootstrap](../../../../../../.agents/skills/discovery-writing/SKILL.md#L229-L245)). Registry
resolution fails as expected.

**Incompatibilities.** D1 is evidence acquisition and descriptive indexing, not design discovery.
This route requires a confirmed discovery intention, owner, restricted target path, design concepts,
and decision register. Those requirements would prematurely turn observations into design and
cannot be used merely to gain access to its bounded agent lifecycle.

### 4. `research-evidence-harness` — unregistered inline harness; wrong stage

**Owned intent.** Convert an already bounded research protocol/experiment into run schemas,
append-only JSONL validation, fixtures, metrics, summaries, and claim-adjudication readiness
([objective and applicability](../../../../../../.agents/skills/research-evidence-harness/SKILL.md#L18-L43)).

**Outputs.** Schema, validator, passing/failing synthetic fixtures, optional metric calculators,
and result summary; it explicitly preserves dry-run/live evidence separation
([process](../../../../../../.agents/skills/research-evidence-harness/SKILL.md#L62-L100)). It does
not impose Research's novelty verdict matrix, but it presupposes claims/protocols and evidence
mechanics rather than acquiring the repository inventory.

**Dispatch/lifecycle.** Unregistered: registry resolution fails. It declares no `Agent` tool,
subagent topology, or bounded bootstrap; its execution shape is local/inline.

**Incompatibilities.** D1's immediate output is the source-backed occurrence inventory, not a
validator or synthetic fixture suite. This harness becomes relevant later when composition
hypotheses have experiment bundles and metrics. Routing D1 here would replace evidence collection
with evidence-mechanics scaffolding.

### 5. `context-builder` — unregistered inline selector; wrong completeness direction

**Owned intent.** Produce a compact, task-ready context bundle from selector-level evidence while
minimizing reading overhead
([objective](../../../../../../.agents/skills/context-builder/SKILL.md#L18-L25)).

**Outputs.** A bounded Markdown context pack and optional JSON/index runtime handoff mapped to task
obligations; persisted packs are session evidence, not canonical reusable knowledge
([handoff contract](../../../../../../.agents/skills/context-builder/SKILL.md#L38-L58),
[output](../../../../../../.agents/skills/context-builder/SKILL.md#L117-L140)). It has no novelty
verdict matrix.

**Dispatch/lifecycle.** Unregistered: registry resolution fails. It defines no subagent capability
or bounded bootstrap.

**Incompatibilities.** Context Builder intentionally selects and excludes evidence under file/line
budgets. D1 requires an enumerated denominator with an occurrence or explicit absence for every
source/control. A selective context pack cannot claim inventory completeness and is not a canonical
knowledge artifact.

### 6. `domainspec-subagents-strategy` — router only, never the worker

**Owned intent.** Decide inline versus delegate, select the owning capability, resolve its route,
apply an optional user-selected anti-bias overlay, and hand one typed route to lifecycle
([responsibility](../../../../../../.agents/skills/domainspec-subagents-strategy/SKILL.md#L9-L15)).

**Outputs/lifecycle.** A routing handoff for an already owned intent. It expressly does not own
topology, artifacts, verdicts, runtime mechanics, or unknown work.

**Incompatibility.** It cannot serve as a fallback capability. Its required result here is exactly
this stop: semantic owner found (`inventory`), but no executable registered or explicitly bounded
route exists.

## Required next gate

Before any D1 execution record is prepared:

1. the Inventory owner must ratify either a LIVE registered route or an explicit
   bounded/unregistered bootstrap with roles, topology, source and mutation boundaries,
   confirmation, outputs, validation, and terminal behavior;
2. D1 must be reshaped to Inventory-native outputs (`evidence-cards` plus `index.md`/`index.json`,
   with a local occurrence schema), preserving the frozen corpus, eight controls, explicit absence,
   ambiguity, dissent, and `prescribed | instantiated | executed | effect-observed | unknown` as
   descriptive fields;
3. the new route must forbid definition of “lens,” novelty adjudication, `GO/KILL`, and effect claims
   beyond source evidence;
4. only then may `domainspec-subagents-strategy` reassess executability and hand a concrete route to
   the proper lifecycle.

Until that gate passes, the decisive routing result is **semantic `inventory`; operational
`BLOCK`; no substitute capability**.
