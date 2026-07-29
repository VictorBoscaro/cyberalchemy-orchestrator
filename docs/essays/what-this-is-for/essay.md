---
tags: [objectives, warrant, provenance, composition, orchestration, decision-hygiene, work-context]
artifact_kind: essay
layer: project
status: draft
version: 0.1.0
last_updated: 2026-07-27
created_at: 2026-07-28T14:26:21-03:00
updated_at: 2026-07-28T14:26:21-03:00
authority: proposal-only
veracity: low
conviction: medium
owning_plan: plans/governed-agent-work-infrastructure/PLAN.md
predecessors:
  - docs/essays/macro-to-micro-context/macro-to-micro-context.md
  - docs/essays/from-context-to-governed-primitives/from-context-to-governed-primitives.md
  - plans/governed-agent-work-infrastructure/essays/work-context-system-view/essay.md
  - plans/governed-agent-work-infrastructure/essays/target-architecture-hypothesis/essay.md
---

# What This Is For

> `Claim ≤ proof`. This essay composes objectives that already exist in this repository; it
> ratifies nothing, closes no open question, and carries no authority. Where it argues that a
> framing fails, it says so in the text rather than in a footnote.

## 1. Being entitled to say something

Someone says a thing is so. Between saying it and being entitled to say it there is a gap, and
the gap is usually invisible. Two people can make the same statement with the same confidence
while one of them has looked and the other has not.

What closes the gap is a reason of the right kind. If the statement is about how the world
behaves, the right kind of reason is a test that could have come out the other way, and did not.
If the statement is about what follows from what, the right kind of reason is a derivation. If
the statement is about what a word means here, the right kind of reason is that the word has been
used this way, consistently, and nothing has broken. And if the statement is that some work may
proceed, the right kind of reason is that someone with standing said so, inside a boundary that
was named.

These are not four grades of the same thing. They are four different kinds of reason, and none
substitutes for another. A proof does not establish that a formal model resembles the world. A
test does not establish that a definition is coherent. An approval does not make a prediction
true. Anyone who has watched an argument go wrong has usually watched one of these substitute
for another without announcing it.

Work makes this harder, because work gets divided. An objective becomes a plan, a plan becomes
tasks, a task becomes an attempt, an attempt becomes a changed file. At each division the local
piece becomes clearer and its reason becomes more distant. The person doing the task can still
tell you what the task is. They may no longer be able to tell you what entitles anyone to rely
on the result — which question it answered, whose approval it ran under, which evidence it used,
what it was checked against.

That distance is not merely inconvenient. It is what makes governance unverifiable. A rule about
agent work — this was confirmed, this stayed inside its boundary, these two judgments were
independent — is real only if it can be checked against a record. Without one, every guarantee
is a claim about something nobody can inspect
([target-architecture-hypothesis/essay.md §2](../../../plans/governed-agent-work-infrastructure/essays/target-architecture-hypothesis/essay.md)).

This repository is building several things at once, and it has never said in one place what they
add up to. The programs are real and separately documented: a governed dispatch substrate that
runs, a decision-hygiene thesis, an agent-work language, a knowledge machine, a category-theoretic
typing obligation, and a macro-to-micro work-context objective. What is missing is the artifact
that composes them.

The gap is not hypothetical. Three independent readers, given the same prompt and no other
context, were asked to rank this project's top five objectives. All three put the built dispatch
substrate first, all three put `OBL-E3` last, and none of them found the macro-to-micro
work-context objective at all. That is unsurprising once you look: the work-context objective
lives only in proposal-only companion essays, and the root Plan's statement of the business
problem names three failure modes of judgment — correlated bias, noise, framing — and nothing
about the loss of context between levels of work
([PLAN.md §1, lines 66–88](../../../plans/governed-agent-work-infrastructure/PLAN.md)). *(The
reader study was reported by the dispatch that commissioned this essay and is not recorded in a
repository file; the part of it that is checkable — what §1 names — is checkable, and holds.)*

## 2. The composed objective

**Candidate.** The programs are not competing goals. They are one relation seen at different
strata: **warrant made explicit, typed, and composable.**

The anchor is not invented here. `AX-2` is titled *revision under type-appropriate warrant*, and
its 2026-07-21 correction enumerates the four kinds of reason described above — **falsify**
(empirical), **prove** (mathematical), **ground-by-use/coherence** (definitional), **owner + gate**
(decisional) — and then states that for an *applied* formalism the warrant **composes**:
`proof ∘ falsification`, because proof warrants internal consistency while falsification warrants
that the formalism represents the real phenomenon
([vault/axioms/axioms.md lines 62–81](../../../vault/axioms/axioms.md)).

So the composed objective is: **infrastructure in which the reason a piece of work may be relied
on is recorded rather than reconstructed, carries the type of reason it is, and can be followed
across a path only where that composition has been licensed.**

Each existing objective attaches to that by a different edge. The edges are not a tree; a single
`parent` relation is exactly the collapse this repository's own work-context essay forbids
([work-context-system-view/essay.md §6](../../../plans/governed-agent-work-infrastructure/essays/work-context-system-view/essay.md)).

| Objective | Edge | Standing today |
|---|---|---|
| Governed dispatch (ledger, strict appender, `check-tension`, mandatory Agent hook) | **enforces** — it is the one stratum where a warrant condition is machine-refused rather than requested | **built**, with a hole: `EG-1` sits at `veracity: medium` after the enum drift, and the write path is disabled by contract ([PLAN.md §4, lines 310–315](../../../plans/governed-agent-work-infrastructure/PLAN.md)) |
| Decision hygiene (`HYP-ORCH-NOISE`) | **substantiates** — it governs whether an agent judgment is the kind of thing that can bear warrant at all | **partly built**: the anti-bias gate runs; independence, aggregation, frame-dispersion and fork-guard are PENDING ([PLAN.md §3.1, lines 196–201](../../../plans/governed-agent-work-infrastructure/PLAN.md)) |
| Category-theoretic typing (`OBL-E3`) | **types** — it asks whether composition along a path of typed connections is licensed at all | **open**, and honestly narrow: nothing in this repo is typed in Lean, and the named risk is that the claim survives only on the sequential fragment ([OBLIGATIONS.md lines 33–51](../../../OBLIGATIONS.md)) |
| Definitions, ontology, meta-ontology (`BL-1`, `BL-3`, `research/meta-ontology`) | **grounds** — it supplies the definitional warrant: a node alphabet and edge catalog that can be used consistently | **proposal-only / parked**; the ledger's own type system is `OQ-5`, undecided ([SEED.md lines 127–131](../../../research/meta-ontology/SEED.md)) |
| Macro-to-micro work context and authority | **scopes** — it says which warrant applies here, and where a decision's boundary ends | **proposal-only**, and the load-bearing question is unowned: `D9` (who owns authority) is CRITICAL with no gate in the repository ([target-architecture-hypothesis/essay.md §9](../../../plans/governed-agent-work-infrastructure/essays/target-architecture-hypothesis/essay.md)) |
| The knowledge machine / T0 loop | **instantiates** — it is the operation that produces, keeps and revises warrant, not a fifth kind of warrant | **discipline runs, machine unbuilt** ([PLAN.md §2 coda, lines 123–128](../../../plans/governed-agent-work-infrastructure/PLAN.md)) |

The edges cross. The dispatch substrate *enforces* decision hygiene's anti-bias move and is also
the object `OBL-E3` proposes to *type*. The work-context program *scopes* the dispatch substrate
and is *grounded* by the same node alphabet the meta-ontology owes. One relation the table
deliberately does not draw: the work-context program does not *derive from* the dispatch
substrate. It was written from the shape of work, not from the inventory
([target-architecture-hypothesis/essay.md §3, method constraint](../../../plans/governed-agent-work-infrastructure/essays/target-architecture-hypothesis/essay.md)).

### The test: does the same machinery recur?

A unifying frame is a metaphor unless the strata share machinery. Three properties recur, and
each is stated in the repository independently at more than one stratum:

1. **The link is typed.** `part-of` is not `authorized-by`; `produced-by` is not `accepted-as`
   (work-context essay §9; `from-context-to-governed-primitives` under *Relation assertion*;
   target-architecture `R7`). The same requirement appears at the epistemic stratum as the edge
   catalog `BL-3`/`OQ-5` owes, and at the operational stratum as the ledger's typed `connections`
   that `OBL-E3` interrogates.
2. **Adjacency is not proof.** A folder does not establish membership (work-context §7); a
   timestamp does not establish causation (target-architecture `R7`); N agents on one base model
   do not establish independence, because a shared base model violates the conditional
   independence the argument needs ([axioms.md AX-4, lines 111–115](../../../vault/axioms/axioms.md)).
3. **Composition must be licensed, not presumed.** `Task authorized-by Decision` and
   `Decision part-of Plan` do not compose to `Plan authorized Task`; a derived conclusion needs a
   replayable witness, and that design is open under `OD-04` (work-context §30). The identical
   requirement is `OBL-E3`'s associativity question, and again `BET-VERACITY-PROP` in
   `vault/hypothesis/claim-graph.md`, which proposes veracity propagation along `premise-of`
   edges as a computation rather than an intuition.

That is the strongest evidence for the framing: nobody coordinated those three statements, and
they are the same three statements.

### One retrodiction the frame gets right

`PLAN.md` §5 records, as a suspicion, that a single missing provenance spine — assertion → the
dispatch that generated it → its trail — is behind three unrelated-looking symptoms at once: the
missing `enrich` step in the loop, the unenforced freeze, and the untyped self-reference
([PLAN.md lines 376–380](../../../plans/governed-agent-work-infrastructure/PLAN.md)). Under this
framing that is one fact, not three. The provenance spine *is* the warrant link. Without it, a
claim cannot be revised by what broke it (no `enrich`), the assertion "these judgments were
independent" has no witness (unenforced freeze), and the repository's own work has no typed edge
to what it is supposed to warrant (untyped self-reference).

That is a genuine consequence of the frame. It is also weak evidence, and should be scored as
such: §5 was written first and read while this was drafted. A retrodiction is not a prediction.

## 2b. Where the framing does not survive

Four places. None is fatal to the composed objective; all four change what may be claimed for it.

**The four faces do not map one-to-one onto four programs.** Decision hygiene is not "the
empirical face of warrant." `AX-1` is filed deliberately as a **value commitment**, not a method
invariant — what the project is *for*, held regardless of proven achievability
([axioms.md §2, lines 133–147](../../../vault/axioms/axioms.md)). The empirical face is served by
the collapse-test discipline that runs across every construct, not specifically by Front 1. The
honest edge is the one the table uses — *substantiates*, an input-quality program — and the tidy
"four faces, four programs" reading should be dropped. It is the kind of correspondence
`P-FACES-INSTANCE` already warns is false when drawn post hoc.

**Six objectives do not compose into four faces.** Two of the six are not faces at all. The T0
loop is the *operation* over warrant; the dispatch substrate is the *enforcement* of it. Counting
either as a fifth or sixth kind of warrant double-counts. The framing composes four faces and
places two objectives elsewhere. That is a weaker claim than "one relation across six
objectives," and it is the one the sources support.

**This unification claim already exists here, already tested, and it partially fired.**
`P-FACES-INSTANCE` — that the decision-science, categorical and engineering faces are faithful
instances of T0 — sits at `veracity: low` with a pre-registered functorial falsifier, and its
status line records that **the engineering face's `enrich` operation has no correspondent at the
current ledger design**: a partial fire pending `BL-3`
([axioms.md lines 83–98](../../../vault/axioms/axioms.md)). This essay's framing is close kin to
that premise and arrives pre-encumbered by the same result.

**"One relation at different strata" must not be read as self-similarity.** `AX-3` fixes only the
*stance* of self-recording; its reflexive claims — that the loops at different scales are the same
*structure* — are explicitly evidence-revisable and are held apart from the axiom layer as a
separate hypothesis ([axioms.md §3, lines 162–171](../../../vault/axioms/axioms.md)). So the claim
here is the weaker one: the strata share a *property* (typed, non-adjacent, licensed-composition
warrant), not a repeated *structure*. The stronger reading is not this essay's to make.

## 3. The properties a candidate design must have

Where the repository already states a property, its own formulation is used.

**P1 — Five paths, independently inspectable.** *Purpose, authority, assignment, causation,
realization.* "They may converge on the same outcome, but none can be inferred from another"
(work-context essay §3). *Check:* pick one outcome and try to answer each of the five separately;
if answering one required assuming another, the design fails.

**P2 — The seven record guarantees, R1–R7.** Identity survives description change; runs of a kind
are comparable; the confirmed shape is the executed shape; an independent judgment is not visible
before it is fixed; what was said is what is read; what happened is recoverable including
empty-payload acts; a connection means something specific
([target-architecture-hypothesis/essay.md §4](../../../plans/governed-agent-work-infrastructure/essays/target-architecture-hypothesis/essay.md)).
*Check:* R1, R6, R7 make the record exist; R2–R5 make it trustworthy. A candidate that satisfies
only the first group has a complete record of facts nobody should rely on.

**P3 — The candidate invariants, as candidates.** Projections cannot manufacture facts or
authority; lineage does not delegate tools, evidence, budget or effect permission; cheap
descriptions do not silently become types, truths or permissions; checker acceptance does not
imply physical enforcement; local validity does not imply global compatibility (work-context §31,
and the parallel list in `from-context-to-governed-primitives`). *Check:* each is stated as a
prohibition, so each is testable by constructing the forbidden case and seeing whether the system
refuses it.

**P4 — Warrant is a typed property of the thing relied on.** This one is *not* yet stated as a
single property anywhere in the repository; it is this essay's proposal, composed from `AX-2`,
`OD-04` and `BET-VERACITY-PROP`. Stated so it can be checked: **for any node a reader relies on,
the system returns the kind of reason it rests on (falsify / prove / ground-by-use / owner-gate),
the evidence that discharges it, and — for any path of more than one edge — the composition rule
and version that licensed the path, or the explicit answer "missing."** *Check:* the failure mode
to look for is a design that answers with a path but no rule. That answer is indistinguishable
from a guess, and the repository's own position is that missing context must remain visible
rather than be guessed.

**P5 — The typing must move a decision.** Naming warrant types is decoration if it never changes
what anyone does. This is the repository's own immunization guard, stated as `CT3` in
`vault/hypothesis/claim-graph.md`: edges that are reproducible yet never flag anything that
changes a decision are decoration. *Check:* name one design decision that came out differently
because a warrant type was recorded.

## 4. A proposed infrastructure

This part does not propose a rival architecture. The
[target-architecture hypothesis](../../../plans/governed-agent-work-infrastructure/essays/target-architecture-hypothesis/essay.md)
already derives services from what the record must do, and its
[x-ray](../../../plans/governed-agent-work-infrastructure/essays/target-architecture-hypothesis/x-ray/infrastructure-context-rich.html)
extends that with the current workflow surface. What follows adds one thing to it — where warrant
lives — and otherwise reports standing.

Eight services, each demanded by a requirement: **Identity** (mints identities, owns typed
relations), **Record** (the single durable-fact ingress, append-only), **Prompts** (typed,
versioned, addressable instructions), **Classifier** (the work kind), **Protocol** (the immutable
`protocol-kind@version` sequence), **Compiler** (protocol + question → the confirmable shape and
the machine plan), **Execution** (resolves bindings, collects returns), **Fabric** (addresses,
seals, delivers unchanged, records; never authors).

What exists today, honestly:

- **Record — partial.** The append-only ledger with a strict appender is the nearest thing, and
  it is real. But `EG-1` (one validated writer) stands at `veracity: medium` because two 2026-07-18
  close rows carried an out-of-enum `exit_reason` that could only have bypassed the appender, and
  the write path is disabled by contract ([PLAN.md §4](../../../plans/governed-agent-work-infrastructure/PLAN.md)).
  It also holds the *operational trace*, not the epistemic units; `BL-3` proposes the separation
  and it is parked.
- **A fragment of Fabric's purpose, without Fabric.** `check-tension` gates opposed angles before
  a fan-out runs, and the `PreToolUse(Agent)` hook can deny a launch. Sealing is not implemented;
  "freeze before the channel" is a prompt convention, and whether the reveal barrier can be a
  *technical* guarantee is listed as an open item, not a built one
  ([PLAN.md §3.1 and §5](../../../plans/governed-agent-work-infrastructure/PLAN.md)).
- **Read-side observability.** FastAPI + SSE control plane over ten UI variants, tested; the
  agent-pool MCP; an opt-in, off-by-default ACI/APT local pilot ([README.md](../../../README.md)).
- **Identity — absent.** Ids live in four disjoint spaces with no typed cross-link; the provenance
  spine row in the meta-ontology seed is marked *missing*
  ([SEED.md](../../../research/meta-ontology/SEED.md)).
- **Classifier, Protocol, Compiler, Prompts, Execution — absent.** There is no versioned protocol,
  no digest closing over a confirmed shape, no instruction service. `D3` (confirmed shape =
  executed shape) is CRITICAL and cites no repository gate.
- **Authority — unowned.** `D9` is CRITICAL: the architecture requires work to run under
  authority and no service provides it.

**Where warrant would live.** Not as a ninth service. On the record: a warrant is a typed
property of a node — kind of reason, discharging evidence, and for derived paths the composition
rule and version. That places it inside `Identity`'s typed relations and `Record`'s events rather
than beside them. Two things block deciding it, and both are already scheduled: `OQ-5` owes the
node alphabet and edge catalog, and `D9` may pull the decisional face out into its own owner. This
essay does not decide either.

**The next step is already written.** The smallest useful vertical slice in work-context essay §35
asks whether, from one candidate outcome, the system can reconstruct defensible purpose,
authority, assignment and causal paths *without treating adjacency as proof* — with negative cases
derived by breaking one binding at a time (§36). That slice tests P1, P2 and P4 together. Nothing
here suggests a different first move.

## Collapse test

The framing fails if the strata do not share machinery: if the work-link store, the claim graph
and the dispatch ledger require genuinely incompatible node and edge models with no common
envelope. Then "one relation at different strata" is a convenient description of three unrelated
systems, and each program should be planned separately.

That test is already scheduled, not invented here. `OQ-3` asks for the minimal event envelope and
the closed enum of the first event-type alphabet; `OQ-5` asks for the ledger's node-type alphabet,
edge-type catalog and per-type property schema
([SEED.md lines 117–131](../../../research/meta-ontology/SEED.md)). If those two land on one
envelope, this essay's composed objective survives its first real test. If they cannot, it does
not.

A second, quieter failure is worth naming because it does not announce itself: the framing could
be *true and inert* — every stratum genuinely sharing the property, and the sharing never changing
a design decision. That is `P5`, and it is the harder of the two to notice.

---

*Nothing here is ratified. Nothing in this repository is typed in Lean; the write-side cutover is
disabled; the fractality claim is falsified at the current design; and the portability claim is
asserted and partly engineered, not demonstrated on a second machine.*

*Note on citations: the work-context system-view essay lists its two predecessors at the paths
`docs/essays/macro-to-micro-context.md` and `docs/essays/from-context-to-governed-primitives.md`.
Both are now folders; this essay cites the current paths.*

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [`vault/axioms/axioms.md`](../../../vault/axioms/axioms.md) | `derives-from` | `AX-2`'s four warrant faces and its `proof ∘ falsification` composition rule are the anchor for §2's composed objective; §2b returns the essay's tidiest reading as unsupported by `AX-1`'s §2 filing. |
| [`plans/governed-agent-work-infrastructure/PLAN.md`](../../../plans/governed-agent-work-infrastructure/PLAN.md) | `refines` | Adds the composing statement the root Plan lacks, and supplies the objective §1's business problem omits, without changing the Plan's fronts or standings. |
| [`plans/governed-agent-work-infrastructure/essays/work-context-system-view/essay.md`](../../../plans/governed-agent-work-infrastructure/essays/work-context-system-view/essay.md) | `derives-from` | §1's register, the five inspectable paths (P1), the candidate invariants (P3) and the composition/`OD-04` argument are taken from it. |
| [`plans/governed-agent-work-infrastructure/essays/target-architecture-hypothesis/essay.md`](../../../plans/governed-agent-work-infrastructure/essays/target-architecture-hypothesis/essay.md) | `depends-on` | Part 4 reports standing against that essay's eight services and `R1`–`R7` rather than proposing a rival architecture; if its derivation falls, Part 4 falls with it. |
| [`docs/essays/macro-to-micro-context/macro-to-micro-context.md`](../macro-to-micro-context/macro-to-micro-context.md) | `derives-from` | The macro-to-micro objective this essay argues is missing from the root Plan's business problem originates here. |
| [`docs/essays/from-context-to-governed-primitives/from-context-to-governed-primitives.md`](../from-context-to-governed-primitives/from-context-to-governed-primitives.md) | `derives-from` | Supplies the typed-relation, witness and projection vocabulary reused in §2's recurrence test and P3. |
| [`OBLIGATIONS.md`](../../../OBLIGATIONS.md) | `contextualizes` | `OBL-E3` is the `types` edge in §2's table; the essay neither advances nor discharges it and repeats its named narrowing risk. |
| [`research/meta-ontology/SEED.md`](../../../research/meta-ontology/SEED.md) | `depends-on` | The closing collapse test is `OQ-3` (event envelope) and `OQ-5` (node alphabet and edge catalog); this essay's composed objective survives or fails with their landing. |
| [`BACKLOG.md`](../../../BACKLOG.md) | `contextualizes` | `BL-1` and `BL-3` are the `grounds` edge in §2's table and the redesign the partial fire of `P-FACES-INSTANCE` waits on. |
| [`vault/hypothesis/claim-graph.md`](../../../vault/hypothesis/claim-graph.md) | `derives-from` | `BET-VERACITY-PROP` supplies the licensed-composition property at the epistemic stratum, and `CT3` supplies P5's inertness test. |
| [`README.md`](../../../README.md) | `validates` | Source for the built-versus-thesis standings reported in Part 4 and in the closing disclaimer. |
