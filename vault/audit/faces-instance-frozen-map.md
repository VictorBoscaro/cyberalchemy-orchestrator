---
tags: [vault, ontology, self-similarity, category-theory, residue]
node_type: audit
is_session: false
session_ref: 2026-07-21-root-hypothesis-tension
layer: ontology, domain
nature: reference, technical
status: exploratory
veracity: medium
conviction: medium
version: 0.1.0
last_updated: 2026-07-21
---

# AUDIT — P-FACES-INSTANCE frozen correspondence map (pre-registration + adjudication)

## Objective

Write down **in advance** — before checking the outcome — a side-by-side map lining up each
step of the project's core method with a matching step in each of its three self-descriptions
(as a decision-science system, as a category-theory object, and as the actual running
orchestrator). Then judge honestly which steps have a real match and which don't.

## Context

The project describes itself through three "faces" and claims all three are versions of one
core loop: *state a claim, test it, keep what survives, learn something new from what breaks*.
If that's true, every step of the loop should have a genuine counterpart in each face. The
honest way to test it is to commit to the map *before* seeing how well it fits — so the result
can't be quietly fitted afterward. That's why this document is "frozen" and dated. The verdict:
the decision-science and category-theory faces line up completely, but the running-system face
is missing its "learn something new" step — the exact same gap found by [[close-row-enrich-c]].
That two independent checks break at the same joint is itself a weak sign they really are about
one structure. It also parks a decision for the future ledger redesign (BL-3): should closing a
batch of work be allowed to *teach the system something new*, or only record a richer log? The
owner has consciously left that open for now.

> **Frozen 2026-07-21, before adjudication** (the `OQ-11` discipline: a map drawn after seeing the
> outcome does not count). This is the pre-registration [[axioms]] P-FACES-INSTANCE requires so its
> falsifier can fire. **Result: the map fires *partially* — the engineering face's `enrich` operation
> has no faithful correspondent at the current design** (proved by [[close-row-enrich-c]]). Two of
> three faces are complete; the third is the same gap fractality hit.

## The frozen map — each T0 root operation ↦ a named operation per face

Root loop **T0** (AX-2): ① state a falsifiable claim · ② probe it · ③ keep what survives · ④ enrich
the model from what breaks.

| T0 op | decision-science face ([[anti-noise-orchestration]]) | categorical face (FRAMINGS/MAPPING) | engineering face (dispatch/ledger) |
|---|---|---|---|
| ① state claim | register a bet (`BET-*`, `claim ≤ proof`) | a MAPPING row: construct ⟷ CT type + strength | a pending dispatch sheet (`goal`/`context`/`groups`) |
| ② probe | tensioned generate + independent aggregation (anti-bias ⊕ anti-noise) | attempt the Lean anchor / run the collapse-test | `check-tension` gate → run the dispatch |
| ③ keep survivors | survived bets stay; falsified ones demoted to `low` | structural / strong-candidate rows stay | the close row: `exit_reason: resolved` records what survived |
| ④ **enrich** | add a new axis/OQ/bet from what broke (e.g. the anti-noise axis grown atop anti-bias) | **anomaly (F6) → enrich `C`** (a richer codomain / new framing) | **— NO CORRESPONDENT (current design)** — a close appends a shadow; it cannot add a distinction ([[close-row-enrich-c]]) |

## Adjudication

- **decision-science face — complete** (all four ops have named correspondents; op ④ is witnessed by
  the real history: the anti-noise axis was *added* to the model from what the anti-bias axis left open).
- **categorical face — complete** (op ④ is the repo's spine: anomaly drives codomain enrichment, F6/F7).
- **engineering face — ops ①–③ present, op ④ MISSING.** [[close-row-enrich-c]] proves no close-row
  enriches `C` at the current ledger design. So P-FACES-INSTANCE's falsifier condition "≥ 1 face has a
  root operation with no faithful correspondent" **is met for the engineering face's op ④** — a
  **partial fire**, pending **BL-3** (an enrich-capable, typed-graph ledger).

This is the same gap [[framework-self-similarity]] hit — because the engineering face *is* the
orchestration loop. UNITY and FRACTALITY fail at the **same joint**: the close step does not enrich
`C`. That convergence is itself a (weak) positive sign that the two claims are about one structure —
they break in the same place.

## The named design decision (step 3 — the decision the shared root must move)

> **Pre-registered decision (candidate — awaits owner ratification):** *When BL-3 redesigns the ledger,
> must the **close step carry a codomain enrichment** (add a distinction the vocabulary can now make),
> or only a richer event record?*

- **With the shared root (P-FACES-INSTANCE true):** the other two faces enrich at op ④, so the rule
  **transfers** — design BL-3's close to enrich `C` (the close *earns* a new type/distinction).
- **Without it:** BL-3 is just a richer append-log; no reason to make the close type-productive.

The two designs are **materially different**, the decision is **named and pending**, and it is judged
**before** the root is invoked — satisfying the "a rule transfers *because* they share the root, and
would be decided differently without it" disjunct (the anti-`OQ-11` requirement). If the owner ratifies
this as the bound decision, P-FACES-INSTANCE's decision-moving disjunct is discharged the moment BL-3's
close design is chosen.

> **Owner decision (2026-07-21): binding deferred — not bound.** The owner chose to keep this disjunct
> **unbound** for now. So P-FACES-INSTANCE currently rests on the **map falsifier only** (partially fired
> on the engineering face); the decision-moving disjunct stays a **candidate**, consciously parked, not
> forgotten. Revisit when BL-3 is scoped.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [[axioms]] (P-FACES-INSTANCE) | `validates` | The frozen pre-registration its falsifier requires; adjudicates a partial fire on the engineering face. |
| [[close-row-enrich-c]] | `depends-on` | Supplies the proof that the engineering face's op ④ has no correspondent today. |
| [[framework-self-similarity]] | `contextualizes` | UNITY and FRACTALITY break at the same joint (the close step's missing enrich-`C`), pending BL-3. |
