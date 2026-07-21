# OBLIGATIONS — falsifiable targets (candidate)

*What would have to be proven for the vault to stop being a metaphor. Each obligation is stated
with precision + carries its collapse-test. None is discharged. Not reviewed.*

---

## OBL-E3 — Is the orchestration language a category? *(the test that decides everything)*

**Claim to discharge.** There exists a category `ORCH` where:
- **objects** = dispatch groups;
- **morphisms** = typed `connections` (`sequential` / `zig-zag` / `feedback`);
- **composition** = pipeline concatenation;
- **identity** = pass-through group.

**Sub-obligations (all must hold):**
1. **Associativity.** `(h∘g)∘f = h∘(g∘f)` for chained connections.
2. **Identity laws.** pass-through is a left and right unit.
3. **Residue = same object.** The residue of a synthesis (what a `synthesizer`/merge loses)
   is the **same** object as `FunctorialResidueStructure`
   (`lean-formalization/FunctorialResidueStructure.lean:97`), via a functor from `ORCH`-syntheses
   to the residue structure — **not** just a count-shaped residue.

**Named risk (not hidden).** `zig-zag` and `feedback` are *loops*, not clearly
morphisms. Honest guess: only the `sequential` fragment is a category outright; `zig-zag`/`feedback`
are probably extra structure (2-cells? a bicategory? a factorization system?) and
**not** 1-level morphisms. If that's the case, the claim narrows to the sequential fragment.

**Collapse-test (double).**
- (a) If `zig-zag`/`feedback` do not compose associatively, `ORCH` is a category only on the
  `sequential` fragment (a DAG) — and the CT parallel is **decoration** for those edges.
- (b) If the synthesis-residue is demonstrably count-shaped (it does not reach
  `FunctorialResidueStructure`), sub-obligation 3 collapses the **analogy**, and the "same residue"
  drops to zero contribution.

**Where it lives.** Lean, in the repo `domainspec-lean-formalization`. Cost: dedicated session, not
inline. Depends on: nothing external — it is dischargeable now, if and when the investment is
worth it.

**Status.** OPEN. It's the first real target; until it's discharged (or it hits the collapse-test),
everything in the vault is a typed candidate, not a result.
