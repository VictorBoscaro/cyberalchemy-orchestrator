---
tags: [orquestrador, cyberalchemy, backlog, meta-types, domain-schema, portability, category-theory, discovery]
node_type: backlog
is_session: false
layer: ontology, architecture
nature: reference
status: draft
version: 0.1.0
last_updated: 2026-07-20
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
frozen. The fixed part is the *meta-level* (what counts as a meta-type, a connection, a
well-formedness criterion, a promotion gate); the *object-level* (the actual meta-types and the
edges between them) grows over the life of the project. This is why it reads as a **process of
discovery**, plausibly a future version ("v5") rather than a thing to define once.

**Why it exists (the seam it closes).** It is the honest grounding for ORCH's
domain-independence — the one `H-PORT-6` reached for but could not carry. Last analysis:
categoricity ⊥ domain-independence, so "ORCH is a category" does **not** buy genericity. The real
grounding is different: ORCH is domain-independent **iff** there is a meta-schema `M` such that
every domain `D` is an instance-of-`M`, and ORCH is written at the level of `M`, not of any `D`.
Then genericity is a *consequence of the meta-schema* (not of the CT thesis) — and it is testable.

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
(DS-D1) is exactly this two-level structure, built and machine-checked — but only for the
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

**Status.** IDEA / parked candidate. Not researched (deliberately — no dispatch run). Graduation
path: promote H-META-1 into a `vault/hypothesis/` doc, or open an `OBL-META` once (and if) the
genericity goal is prioritized. Depends on nothing external; the prototype to study already exists
in `domainspec-v2`.
