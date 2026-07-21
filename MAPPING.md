# MAPPING — construct ⟷ CT type parallels (living ledger)

> Status: brainstorm/candidate, **not reviewed**. Claim ≤ proof: each row is a
> **candidate parallel to be typed**, not a result. Where the anchor is weak (memory / uncommitted
> Lean / our own synthesis) it is labeled. Single source of truth for the mapping (PLAN protocol §3):
> the table lives **here**; PLAN §4 points to it, does not duplicate it.
>
> **Inherited rule.** Every construct of the agent-language → its type in CT + anchor in a
> real file. The operational base is the skill `domainspec-subagents-strategy`
> (`domainspec/.claude/skills/domainspec-subagents-strategy/SKILL.md`) + constitution
> `subagents-strategy-constitution-proposal.md` (v0.6.3). Created 2026-07-19.

---

## 1. Seed table (inherited from PLAN §4)

| Construct | Candidate CT type | Anchor | Strength |
|---|---|---|---|
| probe (recon) | generalized element / functor-of-points (Yoneda) | `YonedaAsTranslation.y`, `Probe.lean` | strong candidate |
| probe (experiment) | Popperian falsification | `experiment/SKILL.md` | nominal rhyme (≠ Yoneda) |
| zig-zag | triangle identities / `EqvGen` back-and-forth | `P1Positive.CommaConnected`, `probe_zigzag_nf.lean` | strong candidate |
| sequential | composition `∘` | `connections` | structural |
| dispatch | typed diagram `J → Cat` | schema v0.6.x | candidate |
| feedback / robot-talks | ? (2-cell / (co)limit of perspectives) | — | open → see §2 |
| residue of a synthesis | `FunctorialResidueStructure` / non-iso Lan unit | `FunctorialResidueStructure.lean:120` (`domainspec-lean-formalization @ 6edb664`, sorry-free per source + repo audit; build-gate re-verify pending) | structural |

> **Note (F7):** the "(recon)" in the *probe* row above is the **broad** sense (active probe vs.
> experiment), **not** the recognition *species* from F7 (object axis/`¬EssSurj`). The partition
> by species is in §2, row `probe: species`. Single source of truth for the term: DEF-ORCH-004.

## 2. Parallels derived from the `subagents-strategy` skill (2026-07-19 session)

| Construct | Literal semantics in the skill | Candidate CT type | Strength / what it resolves |
|---|---|---|---|
| **concat vs. synthesis** (P7) | `robot_talks:true → synthesizes`; otherwise `concat`; "aggregation is **derived**, never a field"; "a bare concat is never the final deliverable" | **concat = coproduct** (thin, count-shaped) vs. **synthesis = pushout/colimit** (identifies overlaps in the tension; **generates residue**) | **strong.** Links directly to `FunctorialResidueStructure` (DEF-ORCH-001); halfway point of OBL-E3's sub-obligation 3. **Ceiling (2026-07-21):** dischargeable at the *separation* bar (second instance à la the diamond), **not** the *invariant-factor* prize (needs non-concrete `C`) — see OBL-E3 sub-3 + `TO-ME/oble3-synthesis-as-second-residue-instance/` |
| **feedback edge** | "`feedback` edges **never count as dependencies**"; conditional; back-edge to pull material | **NOT a 1-morphism** — 2-cell / extra structure (outside the 1-skeleton) | **positive evidence** for the OBLIGATIONS risk. Moves P-CT: feedback = 2-cell, not a morphism |
| **check-tension / anti-bias axes** (P5) | tensioned n≥2 pair; axis ∈ {methodology, source-corpus, attack-vector, temporal-prior}; 2 agents verify | **separating family of probes** (jointly-faithful); each axis = orthogonal probe direction; the gate = enriching non-thin `C` | **strong.** Gives the probe (DEF-ORCH-004) a *plural* form; ties together F4 + F6 (axis = separator/anomaly) |
| **meta + lineage** (P13) | `meta:true` = dispatch *about* dispatching; `parent_dispatch_id`; finite/acyclic chain | **endofunctor / free monad**; lineage = well-founded tree (operad of dispatches) | **strong.** Thesis A6 ("framework as its own instance") mechanized in a registry field |
| **final_approver** (P12) | dedicated auditor, never a group member (no self-approval); receives the entire `working_folder` | **terminal cone / limit** of the diagram; auditor = apex outside the diagram | candidate |
| **exit_reason** | closed vocabulary `resolved\|loop_ceiling_reached\|dissent_irreconcilable\|user_abort\|error` | classifying map to a finite **thin** object = the run's **shadow** | candidate — links to DEF-ORCH-003 (scalar reading, lossy; the real residue is the artifact) |
| **dependency scheduling / READY** (P4) | READY when every incoming `sequential`/`zig-zag` edge has produced; all READY launch concurrently; declared order is only a tiebreak | `J → Cat` diagram; scale = topological order of the dependency **poset** | reinforces §1's `dispatch = J → Cat` |
| **collapse-detection** (P14) | the synthesizer downstream of robot-talks **needs** both the **initial AND final** positions | keep the **morphism**, not just the object = *beats count* (do not decategorify) | candidate — live instance of F1/F3 |
| **probe: recon/connection species** (F7) | the two probe species (normed in DEF-ORCH-004) on the two axes: recon↔`¬EssSurj`, connection↔`¬Full` (the `A→X`); order = presentation dependency | **partition by independent axis** = graded poset (object→relation stratification) | **candidate** — anchor `knowledge-evolution-typing.md` + `ProbeTypology.lean:38,:49` (separates, does not reconstruct); distinct from the broad "(recon)" alias in §1; see F7 + DEF-ORCH-004 |

## 3. Status and collapse-tests

- **concat/synthesis (the central finding).** *Collapse:* if the synthesis is, in practice, a
  count-shaped merge, it falls into the same collapse-test (b) as OBL-E3 — becomes an analogy, not a pushout.
- **feedback = 2-cell.** *Collapse:* if `feedback` composes associatively as a 1-level
  edge, it goes back to being a morphism and the OBLIGATIONS risk dissolves (unlikely given
  "never counts as a dependency").
- **plural probe.** *Collapse:* if the 4 axes are not jointly-faithful (some object
  indistinguishable across the whole family), the family does not reconstruct and the Yoneda-FF parallel weakens.
- **meta/A6.** *Collapse:* if the lineage admits a cycle, it stops being a well-founded tree / free
  monad — but the constitution requires it to be finite and acyclic.

## 4. Open items that these rows touch

- **P-CT** (PLAN): feedback/robot-talks — **advanced** by §2 (feedback = 2-cell; synthesis
  = colimit). Still needs typing in Lean.
- **OBL-E3 sub-3** (synthesis-residue = same object): the concat/synthesis row is the
  concrete discharge route — type `synthesize` as a pushout whose non-iso unit IS `FunctorialResidueStructure`.
  **Scoped (2026-07-21):** reachable at the *separation* bar only; the *invariant-factor* prize
  (`domainspec-lean-formalization/PRIZES.md`, OPEN) needs a non-concrete codomain and is **not** closed by sub-3.
  Design brief: `TO-ME/oble3-synthesis-as-second-residue-instance/`.
