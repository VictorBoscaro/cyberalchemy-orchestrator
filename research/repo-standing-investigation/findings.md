---
tags: [synthesis, repo-standing, claim-proof, enum-drift, obl-e3, phase-2, provenance-spine]
node_type: synthesis
is_session: false
layer: architecture, domain, ontology
nature: explanatory
status: draft
veracity: high
conviction: medium
version: 1.0.0
last_updated: 2026-07-21
dispatch: 2026-07-21-repo-standing-investigation
---

# Findings — Repo Standing (synthesis of three opposed vectors)

Three vectors ran: **Falsifier** (claim ≤ proof), **Builder** (value = a loop that
runs), **Theorist** (the formal ground is the product). This synthesizes; it does not
average. Every line cites the investigator file and the file/line *they* cited.

---

## 1. Where the three converge (high-confidence — reached despite opposed methods)

- **C1 — Trace the enum-drift reproduction. It is cheap and worth doing.** Falsifier
  ranks it most-urgent (`investigator-falsifier.md`, citing `ledger-enum-drift-finding.md:53-57`,
  `engine-constitution.md:388-392`). Builder says do it in parallel (`investigator-builder.md`,
  citing `ledger-enum-drift-finding.md`). Theorist ranks it #4 as a small empirical
  code-layer fix (`investigator-theorist.md`, citing `engine-constitution.md` EG-1).
  All three want the trace done; they split only on *whether it gates Phase 2* (→ T1).

- **C2 — The Front-2 category-theory layer is CANDIDATE, not result.** Falsifier:
  "everything in this vault is a typed candidate, not a result" (`README.md:453`;
  build gate pending `MAPPING.md:25`). Theorist: "coherent but currently cheap" — types
  the DAG scheduler and nothing more (`OrchestrationCategory.lean` sorry-free but trivial;
  count-beating bar closed-NEGATIVE `DiamondResidueInvariantFactors.lean:408`). Builder:
  "theory that types nothing buys nothing yet." Unanimous demotion from result-status.

- **C3 — The sibling Lean build is UNVERIFIED, and verifying it is cheap/binary.**
  Falsifier: "build unverified" (`PLAN.md:282`), re-verify pending (`MAPPING.md:25`).
  Theorist ranks `lake build` green + `#print axioms` clean at #2 — "converts the entire
  anchor table from 'authoritative location' to 'evidence' at once," and adds a **new
  fragmented-target risk**: OBL-E3 decls may not be in the compiled closure
  (`lean-formalization/files/` vs lakefile location). Builder does not contest this;
  it simply defers the layer.

- **C4 — OBL-E3 is dischargeable NOW and its likely verdict is deflationary.**
  Falsifier: "depends on nothing external — dischargeable now" (`OBLIGATIONS.md:47`); the
  alternative outcome is "decoration for the sequential fragment" (`OBLIGATIONS.md:38-43`).
  Theorist: sub-3 reaches only the separation bar, count-capped on concrete substrate
  (`DiamondResidueInvariantFactors.lean:408`, `PRIZES.md:67`). Both expect it to *bound*,
  not raise. They split on whether it's worth the session (→ T3).

---

## 2. The residue (live tensions — each side's strongest form, not merged)

- **T1 — Enum-drift: hard precondition vs mis-scoped.**
  *Falsifier:* it is the "sole precondition the repo itself places on Phase 2"; EG-1 is
  false-as-stated and sits `medium` (`engine-constitution.md:153-155`,
  `ledger-enum-drift-finding.md:36-41`) — the integrity spine is contradicted on disk.
  *Builder:* mis-scoped — it blocks EG-1's **promotion** (a veracity status), not the
  appender's **operation** (which wrote ~30 dispatches); the 2 bad rows *bypassed* it via
  manual YAML, and the marker-design has the validated appender still write the row, so
  wiring Phase 2 *reinforces* single-writer. *Theorist:* neither gate nor headline — a
  small fix that unblocks the code-layer consistency the golden-graph loop needs (#4).
  **Unresolved: is it a gate?**

- **T2 — build-first vs ground-first vs prove-first (the methodological core).**
  *Builder:* ship the loop now — one `POST /api/confirm` + one enabled button
  (`terminal/index.html:548`) + one `Monitor` wait closes a loop the substrate already
  runs by hand; new architecture is premature. *Theorist:* the provenance spine (BL-3) is
  **logically prior to everything** — with ids in four disjoint spaces (`PLAN.md §5`),
  ORCH's objects "are not even a well-defined set," so nothing can be typed *or* honestly
  traced first. *Falsifier:* freeze expansion and prove the base — trace the drift, attempt
  OBL-E3; adding surface on an unverified base "grows unproven surface while claiming rigor."
  Three incompatible orderings of the *same* backlog.

- **T3 — OBL-E3: attempt-as-diagnostic vs bound-only vs defer.**
  *Falsifier:* attempt it — largest surface reducer, and non-attempt "is itself the tell."
  *Theorist:* discharge only to *bound* the claim (confirms residue = decoration on concrete
  substrate), not to raise veracity. *Builder:* defer — buys nothing for the loop.

- **T4 — the single highest-leverage artifact (no shared answer).**
  *Falsifier:* the drift trace (urgent) / OBL-E3 (surface). *Theorist:* the **graded-
  convergence witness** — sub-family fails to separate → adding the probe restores FF; the
  repo formalized only the pessimistic *persistence* half and left the constructive
  *convergence* half un-witnessed (`FRAMINGS.md` F7, `PLAN.md §5`); "the deepest hole."
  *Builder:* the `POST` endpoint. Each vector's product is a different object.

---

## 3. Ranked — what should be done next (residue-respecting)

1. **Trace the enum-drift reproduction.** — **CONVERGENT.** All three; cheap, decidable,
   resolves a known counterexample. (Its *gate status* is T1, but doing it is not contested.)

2. **Verify the sibling Lean build: `lake build` green + `#print axioms` clean, and confirm
   OBL-E3 decls are in the compiled target.** — **CONVERGENT** among the two vectors that
   address the ground (Falsifier + Theorist); surfaces Theorist's fragmented-target risk.
   Builder raises no objection.

3. **Wire Phase-2-as-marker** (`POST /api/confirm` → pending sheet, enable the terminal
   button, `Monitor` wait). — **CONTESTED.** Builder's #1. **Waits on T1** (is the drift a
   Phase-2 gate?) and **T2** (ship vs build-ground-first). Safe to start iff T1 resolves to
   "mis-scoped" *and* the marker design (appender still writes the row) is kept.

4. **Build the provenance spine (BL-3).** — **CONTESTED.** Theorist's #1 ("prior to a
   non-toy OBL-E3"). **Waits on T2** (ground-first decision). If chosen, it reorders 3, 5, 6
   beneath it.

5. **Attempt OBL-E3 sub-3.** — **CONTESTED (T3).** Convergent that it's cheap and
   dischargeable now (C4); disputed on value — diagnostic (Falsifier) vs bound-only
   (Theorist) vs skip (Builder). Waits on the raise-vs-bound-vs-defer call.

6. **Shelve HYP-ORCH-FRACTAL.** — **Single-vector but proof-grounded.** Falsifier only, but
   its pre-registered falsifier already FIRED: "no close enriches C" from the appender schema
   (`close-row-enrich-c.md:15,54`) ⇒ current-design instance falsified
   (`framework-self-similarity.md:74-80`); survivor is double-gated below OBL-E3 *and* BL-3
   (`:28`). By claim ≤ proof, carry it as *shelved-pending-BL-3*, not as a live proof target.
   Theorist and Builder are silent, so not convergent — but nothing contradicts it.

**Reading.** The convergent core (1, 2) is proof-hygiene: two cheap, binary checks that both
demote current claims to their real status. The residue is entirely about *what comes after*
those checks — and it is a genuine three-way fork (ship / ground / prove), not a ranking
dispute. Do 1 and 2 first *because* they cost little and because their outcomes (does the
appender leak? does the Lean actually build?) are the evidence T1 and T2 are arguing without.

---

## Provenance

Dispatch `2026-07-21-repo-standing-investigation` (research, meta). anti_bias axis:
methodology. Init gate `check-tension` (Brandenburg, Martin / Capucci, Matteo) — both PASS.
Investigators (blind, independent): Popper, Karl (Falsifier) · Beck, Kent (Builder) ·
Lawvere, F. William (Theorist). Synthesis: 1 synthesizer. exit_reason: resolved.
Sources: `investigator-falsifier.md`, `investigator-builder.md`, `investigator-theorist.md`
in this folder.
