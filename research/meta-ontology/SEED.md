---
tags: [meta-ontology, portability, kinds, ledger, provenance, category-theory, discovery]
node_type: discovery
is_session: false
layer: ontology, architecture
nature: reference
status: exploratory
veracity: low
conviction: medium
version: 0.1.0
last_updated: 2026-07-21
---

# meta-ontology `M` — seed

> Exploration, not a decision. `Claim ≤ proof`: every structure below is a candidate with an
> open question or collapse-test. Supersede it with a governed decision, don't cite it as settled.
> Sources for everything asserted here: [SOURCES.md](SOURCES.md) (two read-only sweeps of
> `domainspec-core`, dispatch ids `2026-07-21-cav2-canonical-kinds-sweep` and
> `2026-07-21-ledger-meta-ontology-sweep`).

## The question

Does a governance recursion `M` exist such that **every domain `D` is an instance-of-`M` at some
practical level `n`**, and the orchestrator (`ORCH`) is written **at the level of `M_n`, not of any
`D`** — with `M_n`'s own gate governed at `M_{n+1}`? If so, `ORCH`'s domain-independence is a
*consequence of the recursion being well-founded (convergent-in-practice)*, not of any single
terminal `M` — the honest grounding that
[`README.md` H-PORT-6](../../README.md) reached for but could not carry through categoricity
(categoricity ⊥ domain-independence). See [`BACKLOG.md` BL-1](../../BACKLOG.md) / `H-META-1'`.

**Not** a fixed universal *domain schema* (an alphabet of concrete types rich enough for
everything). In this repo's own language that is a **terminal codomain `C`**, and
[`FRAMINGS.md` F6](../../FRAMINGS.md) denies it: in self-modeling domains the Yoneda point is
unreachable, ascension is *perpetual enrichment of `C`*. What can exist is a **governed extension
protocol applied recursively**: each level grows under its own gate, and that gate is governed one
level up — `level_n = alphabet_n + gate_n`. domainspec-core already practices this recursion, not a
fixed two-level split: the ~22 canonical-kinds / 24 DS-D1 meta-types grow under D48/D49/D40, and
the governance layer is itself *built to move* (D49 gates kind-table amendments via
constitution-governance). That a governed meta-level *can* move at all is shown by a **sibling**
layer — domainspec-core's dispatch-trace schema bumped 0.5.2→0.6.0 (stratum iv, not D48/D49/D40).
Whether upper layers move *slower* than the object-level (practical fixity) is the convergence
candidate (`H-META-1'`), not established.

## The substrate model *(corrected by owner, 2026-07-21)*

`M` types **four substrates** plus one **spine**. Each substrate wants the same recursive shape —
a tower of `level_n = alphabet_n + gate_n` with `gate_n` governed at `level_{n+1}`, not a fixed
meta-level over a growing object-level.

| Substrate | What it holds | Question it answers | Prototype in domainspec-core | State |
|---|---|---|---|---|
| **Domain** *(⟂ Code? — see OQ-1)* | the vocabulary of the world (nouns/verbs) | "what is the world made of?" | DS-D1 meta-types + per-type `.schema.yml` validator | **built + enforced** (the only genuinely validated stratum) |
| **Documents** | carriers / **state snapshots** | "where is the knowledge stored?" | CANONICAL-KINDS Tier-1 carrier enumeration | candidate, "uncited by construction" |
| **Ledger of epistemic units** | append-only **typed knowledge graph**: nodes are epistemic units — assertions, **hypotheses**, **definitions**, premises, decisions — connected by **typed edges**; each node-type has its own **properties**; every node carries a **provenance trail**; governance labels (veracity ⊥ conviction, authority, promotion-state) ride on the node | "what do we claim/hypothesize/define, how do they connect, how sure, under whose authority — and where did it come from?" | node-kinds + edge catalog sketched in CANONICAL-KINDS + `ontology-conventions.md` Appendix C; DS-D1 is the *shape* to reuse | to build (its own type system — see OQ-5) |
| **Dispatch / operational trace** | **events** — what the orchestrator *did* (dispatch, close, loop, receipt); **separate** store, may be **agent-populated** | "what runs happened?" | System A (`subagents-dispatch.yaml`) — append-only + deny-hook, but a **closed 2-kind alphabet welded into `append-dispatch.cjs`** | append-only enforced; not extensible |
| **spine: provenance links** | edges: *assertion → generating research/dispatch → trail* | "what is the lineage of this affirmation?" | absent — the ledger sweep's weakness #2 (four disjoint id-spaces, no typed cross-link) | missing |

**The owner's correction (the load-bearing distinction).** The **ledger holds the affirmations**,
*not* the operational trace. The dispatch/close events live in a **separate** store (populated by
the agents themselves). What binds them is the **trail**: every assertion must carry where it came
from, which research produced it, its lineage. This is independently *the same fix* the ledger
sweep identified as most-missing — so the design pressure converges from two directions.

**The ledger is a typed graph, not a flat log** *(owner, 2026-07-21).* It holds *several* kinds of
epistemic unit — assertions, hypotheses, definitions, premises, decisions — and they **connect**.
So the ledger needs its **own type system**: a node-type alphabet, an edge-type catalog, and a
per-type property schema — exactly the DS-D1 move (meta-types + relationship signatures + per-type
`.schema.yml`), applied to the epistemic stratum instead of the software-domain stratum.

**Convergence — Domain and Ledger are the *same kind of object*.** Both reduce to "a governed
**typed graph**: node-types + edge-types + per-type properties + a promotion gate." So does the
records envelope (Craft's row-families). This *may be* the strongest evidence yet *for* `H-META-1'`:
`M`'s top-visible level may be exactly **"a governed typed graph"** — itself a `level_n` whose
`gate_n` (what counts as a valid node/edge-type) is governed at `level_{n+1}`, not a terminal floor.
If that holds, genericity is structural, not accidental. *Two collapse-tests, neither discharged:*
(i) a substrate that cannot be a governed typed graph without redefining what a node/edge *is*
(OQ-4); (ii) the tower fails to converge — `gate_{n+1}` churns as fast as `gate_n` (no practical
fixity). The convergence in (ii) is a **candidate, not a proven fact**.

## The dual that survives (F1)

`residue = shadow ⊕ structure`. **Documents = the shadow** (current-state snapshot; discards the
path). The **trail-linked ledger + trace = the structure** (the ordered trajectory F6/F7 call *the
content*). This gives the *theoretical* reason for the append-only + `supersede`-not-edit
discipline: editing state in place (Craft's sin) collapses structure back into shadow; an appended
`supersede` event preserves the trajectory while correcting the state. Today no `supersede`/`amend`
event exists anywhere — System A can only *close*, never *amend*.

## The governance recursion — prototypes that already exist here

- **Domain:** DS-D1 — `meta-type = a candidate concept type` (slow-governed, not frozen) + growing 24 meta-types, each
  with a `.schema.yml` criterion + Challenge/Confirm contract. *The most enforced example.*
- **Records:** Craft `ledger-core.schema.yml` — a fixed row-family envelope (id + type + lifecycle)
  + a growing family set, and it *even names families it hasn't built yet* (`receipts`,
  `route_handoffs`). The right shape — but mutable-in-place and with no validator binary.
- **Governance:** cav2 `D48` (promotion-lifecycle, *parent of the per-kind lifecycles and of its
  own* — the recursion made explicit in the definitions tower itself), `D49` (kind-enumeration
  closure, default-deny), `D40` (challenge contract), `D23` (veracity ⊥ conviction). Review-enforced
  and **not frozen** — D49 gates kind-table amendments via constitution-governance (how this layer
  moves). Whether it moves *slower* than the object-level it governs (practical fixity) is the
  convergence candidate (`H-META-1'`), not proven; the `schema_version` 0.5.2→0.6.0 bump is a
  *sibling* (trace, stratum iv) example that a governed meta-level moves at all.

So the v-next of the operational trace has a concrete name: **marry System A's discipline
(append-only + deny-hook + validating appender) to Craft's open-alphabet envelope**, add a
`supersede` event, and grow the provenance spine.

## Open questions

- **OQ-1 — Domain = Code?** The owner currently treats the domain-ontology and the code-ontology as
  one meta-type. Unconfirmed. *Collapse either way:* if a construct exists in code with no domain
  correlate (or vice-versa) that the shared alphabet cannot type, they are two substrates, not one.
- **OQ-2 — Is governance a substrate or cross-cutting?** The owner puts assertions in the ledger and
  lets governance labels ride on them (favoring cross-cutting). Earlier framing had governance as a
  peer stratum. Decide once, name once.
- **OQ-3 — Minimal event envelope.** What are the required columns of the unified trace event
  (`event_id`, `event_type` from an open governed alphabet, stamped `timestamp`, `schema_version`,
  typed `payload`, `refs[]`)? And the closed enum of the *first* event-type alphabet.
- **OQ-4 — Is the governance recursion universal *and convergent*?** (= `H-META-1'`; supersedes the
  retired "is the meta-level fixed?" — see BL-1's 2026-07-21 update.) Two axes: *(horizontal)*
  collapse if a domain can't be an `M`-instance without redefining what a node/edge *is* (e.g.
  "typed graph" is itself a codomain choice — continuous/probabilistic domains); *(vertical)*
  collapse if `M`'s own gate cannot be stated without appeal to a `level_{M+1}` that churns as fast
  as `M` — then "universal" can only mean "practically stable", never "terminal". Form-genericity ≠
  coverage-genericity.
- **OQ-5 — The ledger's type system.** *(owner)* Define the ledger's **node-type alphabet**
  (assertion, hypothesis, definition, premise, decision, …), its **edge-type catalog** (what may
  link to what, with what meaning), and the **per-type property schema**. Prior art to mine: the
  epistemic kinds in CANONICAL-KINDS, the edge catalog in `ontology-conventions.md` Appendix C, and
  DS-D1 as the reusable *shape*. Governs BL-3.

## Links

[`BACKLOG.md`](../../BACKLOG.md): BL-1 (meta-type system / H-META-1'), BL-2 (de-fusion), BL-3
(assertion-ledger + trail, separate from trace), BL-4 (OQ-1 domain=code). Source anchors +
verdicts: [SOURCES.md](SOURCES.md).
