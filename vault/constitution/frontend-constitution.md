---
constitution_id: CONST-FE
title: Frontend Constitution — Control Plane
status: candidate
owner: Victor
authority_level: candidate
updated_at: 2026-07-20
---

# Frontend Constitution — Control Plane

> Defines the enforceable patterns for every UI surface of the orchestrator (the
> control plane that organizes, dispatches, and observes subagents). Answers:
> *"how should any new screen or element be built here?"*
>
> **Not** an import of ZefraHub's React constitution. The fundamental ideas were
> brought over; the newspaper-specific machinery (*The Daily Graph*: `exec/tech/graph`
> tiering, atomic voting, the Gödel machine) was **left out on purpose** — it is a
> *measurement instrument* (see [Promotion Boundary](#promotion-boundary)), not a
> principle. Statute: `candidate`, unreviewed. Claim ≤ proof.

---

## Objective

This constitution governs **every UI surface of the orchestrator** — the control
plane that organizes, dispatches, and observes subagents. It answers one question:
*how should any new screen, component, badge, modal, tooltip, or diagram be built here?*

What we want is a single, measurable property: **the interface maximizes information
density while minimizing cognitive fatigue.** These two pull against each other, and
that tension — **density ⊥ fatigue** — is the axis every screen decision is judged on.

The mechanism is the repo's own lever, `residue = shadow ⊕ structure`
([FRAMINGS.md F1](../../FRAMINGS.md)). Every UI element has two faces:

- a **shadow** — its compact, scalar, *lossy* form (a badge, a count, a label, a
  truncated summary, a glyph): it fits on screen but says neither *what* nor *why*;
- a **structure** — the object behind it (the relations, fields, reasons, history)
  that the shadow projects away, and which strictly dominates the shadow whenever the
  content is non-trivial.

Two failures sit at the extremes. **Verbosity** dumps all the structure, always
(maximum fatigue). **Simplism** shows only the scalar shadow and loses the structure
(zero density). We require the honest middle: **structure stays reachable but collapsed
by default**, and the observer chooses to descend — element by element — instead of the
screen deciding for them.

A reader should leave this section knowing exactly what "good" means here: not *less
information*, but **information the observer summons, never information the screen
force-feeds.**

---

## Index

1. [Scope](#scope)
2. [Selection Predicates](#selection-predicates)
3. [Rules](#rules) (FE-1 … FE-9)
4. [Examples](#examples) · [Non-Examples](#non-examples)
5. [Composition](#composition)
6. [Validation](#validation)
7. [Promotion Boundary](#promotion-boundary)
8. [Connections and Falsifiability](#connections-and-falsifiability)
9. [Maintenance](#maintenance)

---

## Scope

Applies to:

- every surface under `implementations/static/ui/**` (the 10 variants and whichever
  one survives),
- the read endpoints that feed the screen (`/api/overview`, `/api/repo/{name}`,
  `/api/snapshot`, `/api/stream`) **as a presentation contract** — not their
  aggregation logic,
- the dispatch topology diagram (groups, agents, typed edges).

Does not apply to:

- `ledger.py` / the appender and the semantics of the dispatch model (governed by the
  definitions protocol and by `register-dispatch`),
- `UI-CONTRACT.md` as a data contract (this constitution governs *form*, not *schema*).

## Selection Predicates

Use this constitution when:

- creating or rewriting any UI level, component, badge, modal, tooltip, or diagram,
- the complaint is "too verbose / too much info / not intuitive,"
- deciding what appears on screen vs. what stays on demand.

Do not load this constitution when:

- the change is purely aggregation/backend with no presentation effect,
- it is a local task note with no reuse.

---

## Rules

> These rules are stated as **hypotheses, not ratified law.** Each is a `candidate` claim
> carrying two confidence labels from the vault's
> [ontology-conventions](../ontology-conventions.md): **veracidade** (external evidence —
> how tested against reality) and **convicção** (how hard we bet on it / how much it drives
> design). Every rule is **self-contained**: the claim (the rule text), its two labels,
> **what would falsify it**, and its validation mode (`deterministic` | `review` | `hybrid`
> | `none-yet`; `none-yet` = intent recorded but not promotable until a validation route
> exists). When a rule survives its falsifier under real use it graduates from hypothesis
> to **premise** and drops the confidence labels.

### FE-1: Density Is Opt-In, Per Element

No element renders its full depth unconditionally. Every dense element exposes a
**compact form** (the shadow) by default and **reveals its structure on demand**
(click/keyboard). Depth levels — summary → detail → structure — live *inside the item*,
not only in the route (`location.hash`).

- **veracidade:** low — the density ⊥ fatigue axis is `none-yet`; no harness or measurement exists yet.
- **convicção:** high — the whole constitution is built on this; it drives every other rule.
- **Falsified if:** revealing structure on demand does not lower measured fatigue versus a fixed layout at equal density — per-element opt-in yields equal-or-worse fatigue.
- **Validation:** `hybrid` — Playwright: a node/edge/card starts collapsed and expands under interaction.

### FE-2: Secondary Information Lives in Hover, Not On-Screen

Qualifiers, metadata, and legends (`loop_cap`, edge type `sequential`/`zig-zag`/`feedback`,
anti-bias axes) leave the visual flow and become tooltips. A single, universal tooltip
system (`#tt` + `data-tip` attributes), one per variant.

- **veracidade:** low — untested here, and it carries a known accessibility risk: hover-only info is unreachable on touch and keyboard.
- **convicção:** medium — a strong preference, weaker than FE-1 and in open tension with accessibility.
- **Falsified if:** moving qualifiers to hover measurably raises task error/time (users miss info they needed), or a real user population cannot reach hover — i.e., the "secondary" info turns out to be primary.
- **Validation:** `hybrid` — static check that `#tt` exists and `data-tip` renders; Playwright hover shows the text.

### FE-3: UI Physics — Ubiquitous Hover + Instant Dismiss

Every interactive element reacts to proximity (lowers visual entropy). Menus, drawers,
and modals close **instantly** on outside-click and `Esc` — zero delay.

- **veracidade:** low — borrowed "physics" from the newspaper (some external precedent), but untested in this repo.
- **convicção:** high — an explicit user requirement (the "item 3").
- **Falsified if:** zero-delay dismiss produces measurable accidental dismissals / rage-clicks — i.e., a small delay would cut error more than instant dismiss helps.
- **Validation:** `deterministic` — Playwright: outside-click and `Esc` close in < 1 frame; no close-`setTimeout`.

### FE-4: Every Element Carries Its Own Context (form ≡ content)

A badge, node, or edge explains its own genesis when inspected (the *what* and the *why*
embedded, not in a separate manual), exposed through a **discreet, uniform affordance**
(a quiet marker), never a permanently visible label. The explanation is **summoned, not
pushed.** **Bounded by FE-1:** collapsed by default — self-documentation does not license
verbosity.

- **veracidade:** low — untested; the affordance design is not built yet.
- **convicção:** high — the user elevated self-explanation to a principle (FE-9's sibling).
- **Falsified if:** elements cannot carry their context without either violating FE-1 (verbosity returns) or the context going unread — i.e., self-documentation adds cost with no measured comprehension gain.
- **Validation:** `review` — peer review: each new element has a compact form + context revealable via discreet affordance.

### FE-5: Three Explicit States — Loading · Error · Empty

Every list/screen that fetches data handles all three. **Never** a blank surface with
only headers. Empty = icon/signal + message in pt-BR (e.g., the gate watching an empty
pending store must *say* it is empty, not show a hollow table). Error = inline, visible,
with retry.

- **veracidade:** medium — a well-established industry pattern, though not yet tested in *this* system.
- **convicção:** high — non-negotiable, cheap, clearly right.
- **Falsified if:** explicit empty/error states do not reduce user confusion versus a blank surface. (Unlikely — this rule is closer to axiom than hypothesis; the weak falsifier is itself the signal it should promote early.)
- **Validation:** `hybrid` — tests in `implementations/tests/`: mock 0 rows → empty-state; mock 500 → error-state.

### FE-6: One Expanded Focus at a Time

Only one item/drawer/modal open simultaneously; opening another closes the previous.
Expanded state is tracked by a single key.

- **veracidade:** low — untested, and in known tension with the "observe N subagents" mission.
- **convicção:** medium — a UX choice, not load-bearing; may be scoped to modals/drawers only.
- **Falsified if:** monitoring multiple agents genuinely needs several simultaneous panels — i.e., single-focus measurably slows multi-agent observation.
- **Validation:** `deterministic` — Playwright: opening B while A is open closes A.

### FE-7: Time and Units Are Declared On-Screen, Never Implicit

Where a convention exists (day in UTC with a UTC-3 user; `toLocaleString` pt-BR; count
by type), the screen **declares** the convention instead of assuming silent agreement
between observers.

- **veracidade:** medium — declaring units/referents is established good practice.
- **convicção:** medium — worth doing, but rarely decisive.
- **Falsified if:** users never misread an undeclared convention — i.e., the declaration adds clutter (fatigue) with no measured drop in misinterpretation.
- **Validation:** `review` — review: every temporal/numeric scale names its referent.

### FE-8: One Canonical Variant — Density Is Measured, Not Guessed

There is **one** living variant; the others are candidates or dead. The choice goes
through a Decision Gate and uses the density ⊥ fatigue axis as a **measured** criterion
(see [Promotion Boundary](#promotion-boundary)), not preference.

- **veracidade:** low — explicitly `none-yet`: no measurement route (fitness harness) exists.
- **convicção:** high — this is the promotion mechanism for the whole constitution.
- **Falsified if:** "cleaner" can only ever be defended by preference and never by measure (the harness proves impossible or meaningless) — then FE-8 collapses and the constitution stays `candidate`.
- **Validation:** `none-yet` — the measurement route (fitness harness) is missing; blocks promotion.

### FE-9: The Obvious Needs No Manual + Discreet Self-Explanation

The primary action of any surface is evident without instruction. Every important element
has a **quiet marker** (always present, ignorable) and is self-explanatory via
**explain-mode**: with the mode on, *dwell* (mouse still) for a **configurable time
(default 3s)** over the element reveals "what it is + why it matters." Outside explain-mode,
nothing competes with the content. The explanation reuses the stable `data-*-id` the
harness uses to score (score and self-explanation are dual).

- **veracidade:** low — untested; explain-mode is not built yet.
- **convicção:** high — the user elevated "the obvious needs no manual" to a principle.
- **Falsified if:** explain-mode goes unused or users still cannot act without instruction — i.e., self-explanatory ⊥ discreet proves unsatisfiable (the marker is either missed because too quiet, or it competes with content).
- **Validation:** `hybrid` — deterministic (accessible name, keyboard focus, tab order; configurable dwell) + review (soft-gradient of friction/obviousness).

---

## Examples

- **FE-1 applied to the dispatch view:** the agent node shows role + name; clicking opens
  the full `initial_prompt` in a modal with managed focus (already done in the 2026-07-20
  session). The screen does not dump the prompt inline.
- **FE-2 applied to the open question "zig-zag vs feedback — does it survive without
  color?":** instead of coloring each edge (more entropy), the type becomes a `data-tip`
  on edge hover. The distinction stays discoverable at no permanent visual cost.
- **FE-5 applied to the gate:** today the pending-sheets panel watches only the `_example`
  fixture; the honest empty-state ("no sheet awaiting confirmation") is the correct form
  while the producer of pending sheets (Next Step 1) does not yet exist.
- **FE-9/FE-4 concrete:** a discreet `?` in the corner toggles **explain-mode**; in it,
  leaving the mouse still ~3s (configurable) over an agent node reveals its role and place
  in the pipeline. The quiet marker (a faint dot) is always there, signaling an explanation
  exists; the content is never covered by a permanent label. Resolves *self-explanatory ⊥
  discreet* by the same logic as FE-1: explanation density is opt-in (the mode) and summoned
  (the dwell).

## Non-Examples

- A repo grid with per-`dispatch_type` **counts as the first thing** on the home — leads
  with the scalar shadow and buries what matters (violates the spirit of FE-1: density
  pushed, not chosen).
- Coloring every edge + an always-visible label + a badge + a legend on screen at the same
  time (violates FE-2/FE-4: self-documentation turning into noise).
- A modal that closes with a 3s delay or only via the "X" (violates FE-3).
- A pending table with headers and an empty body (violates FE-5).

---

## Composition

Precedence (narrowest to broadest):

1. a screen-specific constitution pack (if one exists),
2. **this constitution** (artifact-type: frontend/UI),
3. the definitions protocol + `UI-CONTRACT.md` (data/schema — they govern the *what*, not the *how*),
4. the repo's categorical mapping discipline (`PLAN.md` §4).

Conflicts:

- **FE-4 (self-documentation) × FE-1/FE-2 (opt-in density):** a real conflict, **preserved**,
  not smoothed over. Resolution: FE-1 wins on screen by default; FE-4 is satisfied in the
  revealed state. If an element cannot carry its context *without* violating FE-1, that
  signals a missing depth level — route to Decision Gate.
- **FE-3 (instant dismiss/hover) × FE-9 (3s dwell):** an apparent tension, reconciled
  **by mode**. FE-3's physics (immediate reaction, zero-delay dismiss) is the default
  always. FE-9's *dwell* only exists **inside explain-mode** and governs only the
  *revelation* of the explanation — never the dismiss, which stays instant even with the
  mode on. Outside explain-mode, FE-9 introduces no delay.
- vs. `P1` of ZefraHub's constitution (do not encode filters in the URL): a **conscious
  divergence** — here the UI uses `location.hash` to deep-link between levels. Logged, not
  a bug.

---

## Validation

While the Playwright/pytest validators for FE-1..FE-6 do not exist, validation is manual
`review` against the [Non-Examples](#non-examples). Deterministically intended route:

```bash
# candidate — not yet implemented
cd implementations && python -m pytest tests/ -k "frontend or empty_state or dismiss"
# + shared Playwright suite for hover/tooltip/instant-dismiss
```

---

## Promotion Boundary

Required before canonical status:

- **The missing tool.** FE-8 and the density ⊥ fatigue axis are `none-yet` because
  *"cleaner"* is a judgment today, not a measure. What makes this constitution promotable
  is bringing over **what the newspaper did** — but as an *instrument*, not a newspaper:
  a **UI fitness harness** (variant matrix + fatigue/density signal + atomic per-component
  vote). Only that turns "felt verbose" into a measurable delta and closes the loop with
  the repo's own `MOGT`/decision-receipt (`PLAN.md` E4).
- Playwright/pytest validators for FE-1, FE-2, FE-3, FE-5, FE-6 implemented and green,
- one variant chosen via Decision Gate (the other 9 removed — a requirement inherited from
  earlier sessions; **not yet done**),
- **collapse-test:** if the "cleaner" UI can only be defended by preference and never by
  measure, FE-8 collapses and this constitution stays `candidate`.

---

## Connections and Falsifiability

This constitution **promotes from a hypothesis** and must stay falsifiable with it. Per
the repo's model (`vault/hypothesis/` holds falsifiable theses; a constitution ratifies
rules a thesis earns), the two are linked and share collapse-tests.

| Document | Relationship | Description |
|---|---|---|
| [FRAMINGS.md F1](../../FRAMINGS.md) (`residue = shadow ⊕ structure`) | `grounded-in` | The lever these rules apply to the visual surface. F1 is a `candidate`, unreviewed framing — so is this constitution. |
| The **density ⊥ fatigue** thesis | `promotes-from` | The falsifiable hypothesis behind the whole axis. It currently lives only as F1; it should graduate into its own `vault/hypothesis/` doc (like [[orquestracao-anti-ruido]]) so the promotion is auditable. |
| [[orquestracao-anti-ruido]] (HYP-ORCH-NOISE) | `sibling` | The anti-noise thesis uses the same `shadow ⊕ structure` decomposition (`residue = bias ⊕ noise`); shares the collapse-test discipline. |
| [[ontology-conventions]] | `governed-by` | Defines the `veracidade`/`convicção` labels and the hypothesis → premise arc each rule above carries. |
| `UI-CONTRACT.md` | `presentation-of` | The data contract this constitution presents but does not govern. |

**Falsifiability (collapse-tests for the axis itself):**

- If revealing structure on demand does **not** lower measured fatigue versus showing it
  all at once — i.e., density and fatigue turn out **not** orthogonal on this surface —
  the core axis collapses and this constitution is **retired**, not amended.
- If every element's structure is recoverable from its shadow (the shadow is lossless
  here), then `shadow ⊕ structure` is a false framing for UI and FE-1/FE-4 are ceremony.
  (Mirror of F1's own collapse-test: decategorification is irreversible — the "beats count"
  wall.)
- If "cleaner" can only ever be defended by preference and never by measure, FE-8 collapses
  (see [Promotion Boundary](#promotion-boundary)).

---

## Maintenance

Split trigger:

- if the topology diagram accumulates enough rules of its own, extract a narrower
  `CONST-FE-TOPOLOGY`.

Retirement trigger:

- if the repo migrates from static HTML/JS + SSE to a component framework, FE-3/FE-6
  (written today for vanilla DOM) are rewritten or retired; the fundamental axis
  (density ⊥ fatigue) survives the migration.
