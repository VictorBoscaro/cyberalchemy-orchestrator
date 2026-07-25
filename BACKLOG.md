---
tags: [orquestrador, cyberalchemy, backlog, meta-types, domain-schema, portability, category-theory, discovery]
node_type: backlog
is_session: false
layer: ontology, architecture
nature: reference
status: draft
version: 0.2.0
last_updated: 2026-07-24
---

# BACKLOG — parked candidates (not committed work)

*A parking lot for directions that earned a name but not yet a plan. `Claim ≤ proof` still
holds: every item here is a candidate, none is scheduled, and each carries the falsifiable core
(or open question) that would decide whether it is worth building. An item graduates out of the
backlog by becoming an `OBL-*` (a falsifiable target), a `vault/hypothesis/` doc, or a `PLAN.md`
step — never by silent implementation. IDs are `BL-<n>`; they are stable once assigned.*

---

## BL-1 — Governed-extensible meta-type system *for the domain* ("v5")

**The idea.** A meta-type system for this repo's domain (knowledge / orchestration itself): the
domain is a **typed graph** — nodes carry a *meta-type*, edges carry a *typed connection* — and,
crucially, **the alphabet of meta-types and their connections is updatable under governance**, not
frozen. And there is **no fixed floor**: every level grows under its own gate — the *object-level*
(the actual meta-types and edges) under its gate, and *that gate* under a gate one level up
(`level_n = alphabet_n + gate_n`, `gate_n` governed at `level_{n+1}`). What repeats is the
recursion, not a fixed meta-level; the tower merely *converges* — upper levels mutate slower, so
they read as fixed without being fixed (a candidate, see H-META-1'). This is why it reads as a
**process of discovery**, plausibly a future version ("v5") rather than a thing to define once.

**Why it exists (the seam it closes).** It is the honest grounding for ORCH's
domain-independence — the one `H-PORT-6` reached for but could not carry. Last analysis:
categoricity ⊥ domain-independence, so "ORCH is a category" does **not** buy genericity. The real
grounding is different: ORCH is domain-independent **iff** there is a governance *recursion* `M`
such that every domain `D` is an instance-of-`M` at some practical level, and ORCH is written at
that level — its own gate governed one level up, not a single terminal `M`. Then genericity is a
*consequence of the recursion being well-founded* (not of the CT thesis) — and it is testable.

**The distinction that makes it non-contradictory.** This is emphatically **not** a *fixed
universal domain schema* — an alphabet of concrete types rich enough for every domain. In this
repo's own language, that is a search for a **terminal codomain `C`**, and
[`FRAMINGS.md` F6](FRAMINGS.md#f6--the-yoneda-point-as-target-the-anomaly-as-engine-the-dynamics)
denies it: in domains with self-modeling the Yoneda point is unreachable by construction — no
terminal object, ascension is *perpetual enrichment of `C`*. Believing both "ascend = enrich `C`
forever" and "one `C` is generic enough for everything" is a contradiction. What survives is a
**universal meta-schema + a governed extension protocol**: universality lives in the *method for
growing* the alphabet, never in a fixed alphabet. That reconciliation *is* the "v5" framing.

**Prior art (already a working prototype, restricted to one regime).**
[`domainspec-v2`'s meta-type system](../domainspec-core/projects/domainspec-v2/definitions/meta-types/meta-types.md)
(DS-D1) is exactly this governance recursion, built and machine-checked at (at least) two visible rungs — but only for the
*software* regime: 13 confirmed meta-types of 24 candidates (Entity, Value Object, Operation,
Query, Rule, Policy, Event, State Machine, …), each with a `.schema.yml` well-formedness
criterion, a `candidate → active` promotion lifecycle, and a *challenge contract*. Note the
alignment with F6: a challenge contract is a detected FF-failure (two things the current lens
fuses revealing themselves distinct — e.g. "equal-by-fields but must still be tracked by a
designated id"), and promotion is the enrichment. So domainspec-v2 is not a universal schema; it
is a **universal schema-evolution protocol**, demonstrated for software domains. BL-1 asks whether
the *same* meta-level can host *this* repo's domain (probe, verb, residue, dispatch, group,
connection) — the user's hunch is that it "maybe already is that same one."

**Falsifiable core — H-META-1 (the meta-level is universal / fixed).** Every target domain is
expressible as an instance-of-`M` by extending only the *object-level* (promote a new meta-type
through the gate), never the *meta-level* (the notion "meta-type + criterion + connection + gate"
stays fixed). *Collapse:*
- (a) **The meta-level is itself a codomain choice.** If some domain cannot become an `M`-instance
  without redefining what a node/edge *is* — continuous dynamical systems, probability fields,
  phenomenology may resist "discrete typed graph" — then `M` is generic only over
  graph-shaped domains, and F6's wall has merely moved up one level, not dissolved.
- (b) **Form ≠ coverage.** Even if the meta-level is universal, the object-level alphabet for a
  given domain `D` is perpetually under construction (F6). Genericity of the *form* (cheap, real —
  this is `H-PORT-1`) must not be conflated with genericity of *coverage* (never finished). If BL-1
  is ever sold as "coverage for free," it collapses to the same over-claim `H-PORT-6` made.

**Update 2026-07-21 — collapse-(a) fired; H-META-1 → H-META-1'.** The "meta-level is fixed" bet
failed its own collapse-test: a governed meta-level demonstrably moves — domainspec-core's
dispatch-trace schema bumped `schema_version` 0.5.2→0.6.0 (a *sibling* meta-level, stratum iv; the
kind-governance layer D48/D49/D40 moves by a different mechanism — D49 gates kind-table amendments
via constitution-governance). But (a)'s framing was itself off — "the wall moved up one level" is **not** a failure;
a level's gate being governed one level up is the *law at every `n`* (`gate_n` governed at
`level_{n+1}`), not a defect. The successor hypothesis is **H-META-1' — the governance *recursion*
is universal:** every level grows under its own gate; the tower is *convergent* (higher levels
mutate slower ⇒ practical, not terminal, fixity — F6-consistent, since F6 denies any terminal
level). H-META-1' is itself a **candidate**, with its own collapse-test: **does the tower converge —
is there a level whose gate churns as fast as what it governs (no practical fixity)?** Convergence
is *not* asserted as proven.

**Related prior art caveat.** Reading (a) — a fixed universal domain schema — is the classic
**upper-ontology** dream (Cyc, SUMO, BFO): decades of partial success, never universal coverage.
BL-1 escapes that failure mode *only* by enumerating the *kinds* of concept + a growth protocol,
not the concepts themselves. That escape is the whole bet; if the meta-level enumeration turns out
to be as open-ended as the object-level, the bet is lost.

**Connections.** Closes the seam in [`README.md` H-PORT-6](README.md#portability-hypotheses-candidates-falsifiable);
grounded by, and in tension with, [`FRAMINGS.md` F6/F7](FRAMINGS.md); would consume the vocabulary
in [`definitions/DEFINITIONS.md`](definitions/DEFINITIONS.md) as its object-level seed; sibling to
[`OBLIGATIONS.md` OBL-E3](OBLIGATIONS.md) (both ask whether the orchestration language has a
formal spine, from opposite ends — OBL-E3 about *composition*, BL-1 about *domain-independence*).

**Status.** IDEA / parked candidate. Prior-art sweeps run 2026-07-21 (see
[`research/meta-ontology/`](research/meta-ontology/SEED.md) + `SOURCES.md`); the structure of `M`
is drafted there. Graduation path: promote H-META-1' into a `vault/hypothesis/` doc, or open an
`OBL-META` once (and if) the genericity goal is prioritized. Depends on nothing external; the
prototypes to study already exist in `domainspec-core` (DS-D1, cav2 authority spine, Craft ledger).

---

## BL-2 — De-fuse carrier-kind ⊕ epistemic-role

**The idea.** Split the two things this repo's `node_type` (and even domainspec-core's
CANONICAL-KINDS) fuse into one label: the **document/carrier kind** (`readme`, `spec`, `session`,
`ledger`) and the **epistemic/claim role** (`axiom`, `premise`, `discovery`, `decision`). They are
different strata; a `readme` is not a claim, an `axiom` is *only* a claim.

**Why.** `vault/ontology-conventions.md`'s `node_type` is titled "Epistemic Role" but co-enumerates
carriers and claim-kinds, violating its own orthogonality principle (every label statistically
independent). Recognizing the strata *re-orthogonalizes* the schema — which the doc says it wants.

**Not novel — aligns upstream.** domainspec-core is already de-fusing this: OQ-7 +
`authority/decisions/2026-07-13-canonical-kind-one-label.md` split `canonical_kind` (carrier) from
`node_type` (role) and push role into *edges*. BL-2 = adopt that split here.

**Falsifiable core.** After the split, no instance needs two type labels to be classified: carrier
is read off the artifact, role off its claim. *Collapse:* if some artifact genuinely needs both an
independent carrier-type AND an independent role-type that cannot be derived from each other, the
two axes are not cleanly separable and the fusion was carrying real information.

**Connections.** Feeds [`research/meta-ontology/SEED.md`](research/meta-ontology/SEED.md) (the
Documents ⟂ Ledger-of-assertions separation); counter-example source A5/A8 in `SOURCES.md`.

**Status.** IDEA / actionable-today (independent of the rest). Not scheduled.

---

## BL-3 — The ledger as a typed knowledge-graph of epistemic units, separate from the operational trace

**The idea** *(owner direction, 2026-07-21).* The **ledger is where the epistemic units live** — an
append-only **typed graph** holding *several* kinds of node (assertions, **hypotheses**,
**definitions**, premises, decisions) that **connect via typed edges**, each node-type with its own
**properties**, and each node carrying a **provenance trail** (which research/dispatch generated it,
its lineage). This needs its own **type system**: a node-type alphabet, an edge-type catalog, and a
per-type property schema — the DS-D1 move (meta-types + relationship signatures + per-type schema)
applied to the epistemic stratum (see OQ-5 in the SEED). The **dispatch/operational trace is a
*separate* store** (events; may be agent-populated), bound to the ledger by the provenance link:
epistemic-node → generating dispatch/research → trail. Governance labels (veracity ⊥ conviction,
authority, promotion-state) ride on the nodes, not on the events.

**Why (and the v-next shape).** The ledger sweep found the operational trace (System A) is
append-only + hook-enforced but has a **closed 2-kind alphabet welded into `append-dispatch.cjs`**,
while Craft's `ledger-core.schema.yml` has the right **open id+type+payload envelope** but is
mutable-in-place and unenforced. v-next = **marry System A's discipline to Craft's envelope**, add a
`supersede`/`amend` event (append, never edit-in-place), and build the **provenance spine** that is
absent today (four disjoint id-spaces, no typed cross-link — the sweep's weakness #2, which is
*exactly* the trail the owner requires).

**F1 grounding.** Documents = shadow (state, discards the path); trail-linked ledger + trace =
structure (the ordered trajectory F6/F7 call the content). Editing state in place collapses
structure → shadow; an appended `supersede` preserves the trajectory. This is the *theoretical*
reason append-only is non-negotiable for the ledger.

**Falsifiable core.** Every assertion resolves to a non-empty provenance trail terminating in a
recorded dispatch/research event. *Collapse:* if assertions routinely exist with no recoverable
generating event (orphan claims), either the trace is lossy or assertions are authored outside the
machine — and the "trail" guarantee is decorative.

**Connections.** [`research/meta-ontology/SEED.md`](research/meta-ontology/SEED.md) (substrates
Ledger + Trace + spine); `SOURCES.md` B1/B2/B3/B7. Interacts with this repo's own ledger enum-drift
(local to this repo; domainspec-core's trace is clean).

**Status.** IDEA / parked candidate. Largest of the three; needs OQ-3 (event envelope) decided first.

---

## BL-4 — Open question: is the Domain ontology the same meta-type as the Code ontology?

**The question** *(owner, 2026-07-21).* The substrate model currently treats "domain" and "code" as
one meta-type (the Domain stratum). This may be wrong — it is explicitly open.

**Falsifiable core (either direction).** They are **one** iff a single meta-type alphabet types both
domain concepts and code constructs with no residue. *Collapse to two:* a construct exists in code
with no domain correlate (or vice-versa) that the shared alphabet cannot type without being
stretched. (domainspec-v2's spec-ontology-unification tower is prior art bearing on this — it
treats spec and code as one typed graph; study whether that holds or leaks.)

**Connections.** OQ-1 in [`research/meta-ontology/SEED.md`](research/meta-ontology/SEED.md).

**Status.** OPEN QUESTION. Resolve before fixing the Domain stratum's alphabet.

---

## BL-5 — Tag and catalogue research towers

**The idea** *(owner direction, 2026-07-23).* Replace path-shape discovery of research material with
an explicit catalogue. A research tower is currently approximated as any authorized directory with a
path segment exactly `research` or beginning with `research-`. That convention is useful for the
first Reference Scout slice but says nothing about subject, authority, freshness, coverage, source
kind or whether two towers overlap.

The future catalogue should give every tower a stable ID, repository/root reference, topic tags,
short description, authority/visibility policy and coverage metadata. Reference Scouts consume a
frozen catalogue snapshot rather than rediscovering directory names at runtime. This is indexing for
context acquisition, not the future knowledge/information system itself.

**Falsifiable core.** For a representative Scout corpus, a catalogue snapshot identifies every
eligible research root without path guessing and lets a caller select relevant towers more precisely
than the `research*` name heuristic. *Collapse:* if tower membership and relevance cannot be made
stable enough to outperform bounded path discovery, retain the heuristic as observation rather than
promoting a registry.

**Connections.** `docs/features/agent-provenance-telemetry/probes/reference-scout-tool.md`;
agent-provenance source observations; future information-system work deliberately deferred.

**Status.** IDEA / parked. The first Scout bus slice may use and record the coarse path snapshot;
catalogue design comes later.

---

## BL-6 — Multi-level, self-explaining system dashboard

**The idea.** Provide a family of connected dashboard views that makes the agent system legible at
different altitudes: system overview, architectural layer, pipeline, agent, task, session, event,
artifact and individual execution. The views should use progressive disclosure rather than one
screen containing everything, while preserving stable identity and drill-down paths across levels.

The dashboard should expose enough context to explain what is being shown, which concrete
instance or time window is selected, how fresh and complete the evidence is, and what cannot be
concluded from it. Provenance, partial data, conflicts, errors and unavailable layers must remain
visible. Aggregate health metrics should use bounded dimensions; occurrence-level identity belongs
in correlated events and traces.

**Reference only.** `../maestro-trama/vault/constitution/dashboard-contracts-constitution.md` and
the sibling dashboard observability material contain useful precedents for progressive detail,
self-explainability, honest degradation and provenance. They are inputs to later research, not
adopted authority or an implementation decision.

**Falsifiable core.** A user can begin at the system overview, reach the evidence for one concrete
execution without losing its layer and relationship context, and distinguish authoritative facts
from projections and explanations. *Collapse:* if the views require heuristic identity matching,
silently omit missing evidence, or cannot preserve context across drill-down, the dashboard is not
an adequate observability surface.

**Status.** TODO / reference for future discovery. No dashboard implementation is scheduled.

---

## BL-7 — Declarative typed-set rules and open-questions sessions

**The idea.** Allow a user to state a governed rule such as: “for every document of type X, create
or attach an open-questions session.” The rule targets a typed set instead of enumerating documents.
Each resulting session is an independently identifiable object with properties and lifecycle, bound
to its document through a typed, observable and provenance-carrying relationship.

This is a concrete acceptance case for the broader event/action language: applying the rule may be
requested manually or reconciled when membership changes, but the semantic requirement must not be
coupled to one trigger mechanism. The system must be able to represent the desired relationship
even when no event-driven automation is enabled.

**Falsifiable core.** Given a declared document type and a scope, the system can determine which
documents are covered, establish exactly one intended open-questions relationship per covered
document, explain why each relationship exists, and detect missing or excess instances.
*Collapse:* ambiguous type membership, duplicate sessions, silent retroactive expansion or
unexplainable exceptions make the rule unsafe.

**Open decisions.** Define snapshot versus continuous selection, existing versus future documents,
idempotency, exceptions and overrides, deletion/retirement behavior, session ownership, question
identity, resolution/reopening, and what happens when a document changes type.

**Status.** TODO / required acceptance case for future rule, ontology and session design.
