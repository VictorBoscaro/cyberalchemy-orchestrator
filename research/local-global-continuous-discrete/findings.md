# Findings — Local–Global and Continuous–Discrete

## One-line answer

The repository already owns a local-validity → compatibility → attempted globalization → witness/obstruction → residue/refinement pattern, but it does not own a continuous/discrete optimization theory or Selmer formalization; operationally, the pattern breaks at connected evidence delivery and verified return to the source objective.

## Verdict matrix

| candidate | owner (precedent) | witnessed? | sound? | verdict | use-mode |
|---|---|---:|---:|---|---|
| Local conditions can fail to compose globally | Operational Knowledge Language and work-context artifacts (`docs/temps/operational-knowledge-language/README.md:395-404`; `work-context-system-view/essay.md:701-728,752`) | Yes: locally satisfiable `x_A=0`, `x_B=1` plus interface `x_A=x_B` is jointly UNSAT (`predictive-epistemic-grammar/research.md:865-875`) | Yes | GO | already-deployed vocabulary; build-from-owned operationally |
| Compression is task-relative and must preserve what a readout needs | Operational Knowledge Language factorization criterion (`README.md:303-328`) | Yes: a pair collapsed by `R` but separated by `L` witnesses insufficiency | Yes, explicitly limited to `Set` | GO | build-from-owned |
| `explore → compress → globalize → residue → refine` is a new architecture | Existing Verb/residue/composition definitions (`definitions/category-theory-parallels/DEFINITIONS.md:18-31,153-164`) | No discriminator beyond existing owners has been supplied | No: collapses unless it adds carrier, map, invariant, obstruction and rejection case | KILL | tautological typed negative |
| The cycle is a useful operational diagnostic | Dispatch/runtime/observability owners (`append-dispatch.cjs`; `dispatch_workflow.py`; `OBSERVED-RUNS.md`) | Yes: connected topology is representable but compilation rejects nonempty connections (`dispatch_workflow.py:120`; `BACKLOG.md:298`) | Yes when stated as a diagnostic, not a deployed loop | GO | build-from-owned |
| Representation-induced optimization | precedent-clean inside this repo | Only an invented graph objective gives an example; the repo owns no objective-preserving optimization mechanism | Not yet | KILL | no-witness typed negative: constraint validation is supported, optimization is not |
| Continuous = local; discrete = global | precedent-clean as a repo mechanism | Counterexamples are immediate; no repository implementation found | No | KILL | tautological/false equivalence |
| Selmer-like formalization | conversational motivation only (`research-initial-definitions.md:25-33`) | No in-repo Selmer, descent, or lifting construction | Not yet | KILL | no-witness typed negative |

## What exists now

The strongest repository result is not hidden: `docs/temps/operational-knowledge-language/README.md:395-404` already names the sequence “local conditions → compatibility → attempted globalization → witness or obstruction.” The same artifact separates compatibility, composition, compression, witness, residue and obstruction, and supplies a factorization-based adequacy test for compression at lines 303-328.

This is reinforced by concrete countermodels. The smallest is a constraint interface: each local side is satisfiable, but the interface makes their conjunction inconsistent (`predictive-epistemic-grammar/research.md:865-875`). A second operational form is a pair of locally valid directed dependencies that form a global cycle (`research/agent-language-mathematical-formalization/research.md:162-173`).

The runtime owns several components: bounded local seats, immutable bindings, closed record vocabularies, append-only outcomes, and preservation of blockers/feedback fields. It does not yet own the whole cycle. The active compiler rejects connected topologies, feedback is not routed end-to-end, and close verifies terminal binding state rather than satisfaction of the dispatch goal (`dispatch_workflow.py:120`; `service.py:1395-1455`).

## What can already be inferred

1. **Local/global is the load-bearing axis.** It describes whether separately valid claims/work items compose under explicit interfaces and witnesses.
2. **Representation is a second, independent axis.** A compression is adequate only relative to what must be observed or preserved. It can enable a global constraint check without enabling global optimization.
3. **Obstruction must be typed.** Missing evidence, incompatibility, absence of lift, goal failure and suboptimality are different failures. Calling all of them “residue” destroys the diagnostic value.
4. **The useful cycle is epistemic, not yet optimization-theoretic:** local checks → representation → joint constraint check → explicit obstruction → justified refinement.
5. **Recent work strengthens observability and reconstruction**, especially the explicit preservation of uncertainty, but does not add the missing semantic handoff or optimization structure.

## What this gives the project

It gives a sharper readiness rule for multi-stage orchestration:

> Do not call a dispatch globally governed merely because every seat is locally bound and valid. Require digest-pinned downstream evidence, an explicit compatibility/witness obligation, typed obstruction, and a close check tied back to the source objective.

The first practical experiment should be an attacker → synthesizer → verifier → approver flow where every declared input is materialized as a nonempty digest-pinned slot and malformed or incompatible evidence is rejected before approval. This is measurable and targets the exact current break (`BACKLOG.md:298-301`).

## Where it breaks

The first conceptual break is the jump from **compatibility** to **optimization**. Compatibility restricts feasible candidates; it neither selects the best candidate nor proves that the representation preserves the objective. If `q:X→D` collapses a feasible/high-value source state with an infeasible/low-value one, success in `D` cannot establish feasibility or optimality in `X`.

The first operational break is earlier: connected evidence handoff. The schema can describe sequential, zig-zag and feedback edges, but the compiler currently refuses nonempty connections. Consequently, local results are not yet globalized through governed, integrity-bound evidence slots.

The Selmer analogy breaks unless five things are supplied: a global carrier, local projections, local conditions, a proof-relevant compatibility/lifting rule, and a separately represented obstruction. None is currently implemented as a Selmer/descent system in this repository.

## Follow-up research obligations

- Define a concrete `X`, representation map `q`, preserved invariant/readout and certified lift.
- Separate feasibility, compatibility, liftability, goal satisfaction and optimality in the vocabulary and runtime checks.
- Implement and test connected digest-pinned handoffs before claiming an end-to-end refinement loop.
- Decide whether “obstruction” is a strict subtype of canonical residue or a different object with its own witness contract.
- Only then compare the resulting structure with descent/Selmer machinery or optimization abstractions outside the repository.
